#!/usr/bin/env python3
"""Check publishable routes, anchors and public feed consistency without dependencies."""
import json
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://studio5-ashy.vercel.app"
errors = []
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.images = path, [], [], []
        self.h1, self.title, self.viewport = 0, False, False
        self.feed(path.read_text(encoding="utf-8"))
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if "id" in attrs: self.ids.append(attrs["id"])
        if tag == "h1": self.h1 += 1
        if tag == "title": self.title = True
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
            if "user-scalable=no" in attrs.get("content", "") or "maximum-scale=1" in attrs.get("content", ""):
                errors.append(f"{self.path}: zoom disabled")
        if tag in ("a", "link") and "href" in attrs: self.links.append(attrs["href"])
        if tag in ("img", "script") and "src" in attrs: self.links.append(attrs["src"])
        if tag == "img" and ("alt" not in attrs or "width" not in attrs or "height" not in attrs):
            errors.append(f"{self.path}: image dimensions or alt missing")

paths = sorted((ROOT / "hypecheese").rglob("*.html"))
docs = {p.resolve(): Document(p) for p in paths + [ROOT / "index.html"]}
for path in paths:
    doc = docs[path.resolve()]
    if doc.h1 != 1 or not doc.title or not doc.viewport:
        errors.append(f"{path}: missing/duplicate h1, title or viewport")
    if any(v > 1 for v in Counter(doc.ids).values()): errors.append(f"{path}: duplicate anchor IDs")
    for href in doc.links:
        parsed = urlsplit(href)
        if parsed.scheme and not href.startswith(BASE + "/"): continue
        target_path = unquote(parsed.path)
        target = ROOT / target_path.lstrip("/") if target_path.startswith("/") else path.parent / target_path
        if not target_path: target = path
        if target.is_dir(): target /= "index.html"
        target = target.resolve()
        if not target.is_relative_to(ROOT):
            errors.append(f"{path}: link escapes root {href}")
            continue
        if not target.exists():
            errors.append(f"{path}: broken local link {href}")
            continue
        if parsed.fragment and target.suffix == ".html":
            linked = docs.get(target) or Document(target)
            if unquote(parsed.fragment) not in linked.ids: errors.append(f"{path}: missing anchor {href}")

feed = json.loads((ROOT / "hypecheese/feed.json").read_text())
assert feed["schemaVersion"] == 1
datetime.fromisoformat(feed["updatedAt"].replace("Z", "+00:00"))
ids = []
for kind in ("notices", "updates"):
    for entry in feed[kind]:
        ids.append(entry["id"])
        for field in ("id", "title", "summary", "publishedAt", "url"):
            if not entry.get(field): errors.append(f"feed {kind}: missing {field}")
        datetime.fromisoformat(entry["publishedAt"].replace("Z", "+00:00"))
        if not entry["url"].startswith(BASE + "/hypecheese/"): errors.append("feed detail outside HYPE CHEESE")
        target = ROOT / urlsplit(entry["url"]).path.lstrip("/")
        if not target.exists(): errors.append(f"feed missing detail {target}")
        else:
            text = target.read_text()
            if entry["title"] not in text or entry["summary"] not in text: errors.append(f"feed/detail mismatch {entry['id']}")
        if kind == "updates":
            if not entry.get("version"): errors.append("update version missing")
            if not set(entry.get("changes", {})) <= {"added", "improved", "fixed"}: errors.append("unknown update change type")
if len(ids) != len(set(ids)): errors.append("duplicate public feed IDs")
for page in ("terms", "privacy", "collection", "marketing"):
    text = (ROOT / f"hypecheese/{page}.html").read_text()
    if "2026-09-14-local-v1" not in text or "시행일 2026.09.14" not in text:
        errors.append(f"{page}: policy version/date mismatch")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(json.dumps({"status":"PASS", "hypecheese_pages":len(paths), "notices":len(feed['notices']), "updates":len(feed['updates']), "checks":["local routes and fragment anchors", "unique document IDs", "document title/h1/viewport", "image alt and dimensions", "feed/detail content agreement", "policy version/date agreement"]}, ensure_ascii=False, indent=2))
