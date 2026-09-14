#!/usr/bin/env python3
"""Render public notices/updates from the same feed consumed by the app.
Run from any directory: python3 scripts/render-hypecheese-feed.py
"""
import json
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse
from hypecheese_layout import BASE, page

ROOT = Path(__file__).resolve().parents[1]
FEED = json.loads((ROOT / "hypecheese/feed.json").read_text())
assert FEED["schemaVersion"] == 1

def date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y.%m.%d")

def local_path(url):
    parsed = urlparse(url)
    assert f"{parsed.scheme}://{parsed.netloc}" == BASE
    assert parsed.path.startswith("/hypecheese/") and ".." not in parsed.path
    return parsed.path

def write(path, html):
    target = ROOT / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")

for kind, title, intro in [
    ("notices", "공지", "운영 안내와 이용에 필요한 소식을 확인하세요."),
    ("updates", "업데이트", "공개한 앱 버전의 추가·개선·수정 내용을 기록합니다.")
]:
    entries = sorted(FEED[kind], key=lambda item: item["publishedAt"], reverse=True)
    body = f'<nav class="breadcrumb" aria-label="현재 위치"><a href="/hypecheese/">하입치즈</a><span aria-hidden="true">/</span><span>{title}</span></nav><p class="eyebrow">HYPE CHEESE NEWS</p><h1>{title}</h1><p class="lead">{intro}</p>'
    if entries:
        body += '<ul class="news-list">'
        for entry in entries:
            path = local_path(entry["url"])
            label = entry.get("category") or entry["version"]
            meta = f'<div class="news-meta"><span class="category">{escape(label)}</span><time datetime="{escape(entry["publishedAt"], quote=True)}">{date(entry["publishedAt"])}</time></div>'
            body += f'<li><a class="news-link" href="{path}">{meta}<h2>{escape(entry["title"])}</h2><p>{escape(entry["summary"])}</p></a></li>'
            detail = f'<nav class="breadcrumb" aria-label="현재 위치"><a href="/hypecheese/">하입치즈</a><span aria-hidden="true">/</span><a href="/hypecheese/{kind}/">{title}</a></nav>{meta}<h1>{escape(entry["title"])}</h1><p class="lead">{escape(entry["summary"])}</p><article class="doc-content">'
            if kind == "notices":
                content = json.loads((ROOT / "hypecheese/content" / (entry["id"] + ".json")).read_text())
                detail += ''.join(f'<p>{escape(text)}</p>' for text in content["paragraphs"])
                link = content.get("link")
                if link:
                    assert link["url"].startswith("/hypecheese/")
                    detail += f'<div class="actions"><a class="button" href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a></div>'
            else:
                for key, heading in [("added", "추가"), ("improved", "개선"), ("fixed", "수정")]:
                    changes = entry.get("changes", {}).get(key, [])
                    if changes:
                        detail += f'<h2>{heading}</h2><ul>' + ''.join(f'<li>{escape(text)}</li>' for text in changes) + '</ul>'
            detail += f'<a class="back-top" href="/hypecheese/{kind}/">← {title} 목록</a></article>'
            write(path, page(entry["title"], entry["summary"], detail, path, kind, narrow=True))
        body += '</ul>'
    else:
        body += '<div class="empty-state"><strong>아직 등록된 업데이트가 없습니다.</strong><p>앱 버전이 공개되면 변경 내용을 이곳에서 안내합니다. 현재 이용 방법은 이용가이드에서 확인할 수 있습니다.</p><a href="/hypecheese/guide.html">이용가이드 보기 →</a></div>'
    write(f"/hypecheese/{kind}/index.html", page(title, intro, body, f"/hypecheese/{kind}/", kind, narrow=True))
print(f"Rendered {len(FEED['notices'])} notices and {len(FEED['updates'])} updates.")
