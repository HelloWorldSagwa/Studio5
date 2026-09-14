"""Shared, dependency-free HTML shell for the HYPE CHEESE static documents."""
from html import escape

BASE = "https://studio5-ashy.vercel.app"

def page(title, description, body, path, active="", narrow=False):
    nav = "".join(f'<a href="{url}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a>' for key, url, label in [
        ("guide", "/hypecheese/guide.html", "이용가이드"),
        ("notices", "/hypecheese/notices/", "공지"),
        ("updates", "/hypecheese/updates/", "업데이트")])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#101010">
  <title>{escape(title)} · 하입치즈</title>
  <link rel="canonical" href="{BASE}{path}">
  <link rel="icon" type="image/png" href="/hypecheese/assets/icon.png">
  <link rel="stylesheet" href="/hypecheese/assets/hypecheese.css">
</head>
<body id="top">
  <a class="skip-link" href="#main">본문으로 이동</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="/hypecheese/" aria-label="하입치즈 홈"><img src="/hypecheese/assets/icon.png" width="36" height="36" alt="">HYPE CHEESE</a>
      <nav class="site-nav" aria-label="하입치즈 문서">{nav}</nav>
    </div>
  </header>
  <main id="main"{' class="narrow"' if narrow else ''}>
{body}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <nav class="footer-nav" aria-label="정책과 문의">
        <a href="/hypecheese/terms.html">이용약관</a>
        <a href="/hypecheese/privacy.html"><strong>개인정보처리방침</strong></a>
        <a href="/hypecheese/guide.html#help">도움말</a>
        <a href="/#projects">Studio5 프로젝트</a>
      </nav>
      <p class="operator">Studio5 · 대표 김성현</p>
      <p>사업자등록번호 897-78-00494 · 통신판매업신고번호 2024-부산진-1049</p>
      <p>서비스·개인정보 문의 <a href="mailto:studiofiveteam@gmail.com">studiofiveteam@gmail.com</a></p>
      <p>© 2026 Studio5</p>
    </div>
  </footer>
</body>
</html>
'''

def document(title, description, sections, *, legal=False, version="2026-09-14-local-v1"):
    toc = ''.join(f'<li><a href="#{escape(id, quote=True)}">{escape(label)}</a></li>' for id, label, _ in sections)
    content = ''.join(f'<section class="doc-section" id="{escape(id, quote=True)}"><span class="section-number">{i:02d}</span><h2><a class="heading-link" href="#{escape(id, quote=True)}">{escape(label)}</a></h2>{body}</section>' for i, (id, label, body) in enumerate(sections, 1))
    date = '<span>시행일 2026.09.14</span>' if legal else ''
    scope = ('이 문서는 현재 로컬 테스트 버전에 적용됩니다. 클라우드 계정·동기화와 정식 유료 서비스의 처리 조건은 도입 전에 별도로 안내합니다.' if legal else '현재 로컬 테스트 버전을 기준으로 안내합니다. 계정과 콘텐츠는 기기에 저장되며, AI 생성에는 연결된 서버를 사용합니다. 기기 간 자동 동기화는 제공하지 않습니다.')
    return f'''<nav class="breadcrumb" aria-label="현재 위치"><a href="/hypecheese/">하입치즈</a><span aria-hidden="true">/</span><span>{escape(title)}</span></nav>
    <p class="eyebrow">HYPE CHEESE {'POLICY' if legal else 'GUIDE'}</p>
    <h1>{escape(title)}</h1>
    <p class="lead">{description}</p>
    <p class="meta">{date}<span>최종 수정 2026.09.14</span>{f'<span>문서 버전 {version}</span>' if legal else ''}</p>
    <p class="scope-note"><strong>현재 제공 범위</strong><br>{scope}</p>
    <div class="doc-layout">
      <nav class="toc" aria-label="문서 목차"><h2>이 페이지에서</h2><ol>{toc}</ol></nav>
      <article class="doc-content">{content}<a class="back-top" href="#top">맨 위로 ↑</a></article>
    </div>'''
