// Keep native anchor navigation/history; only track the reader's current section.
document.querySelectorAll('.toc').forEach((toc) => {
  const entries = Array.from(toc.querySelectorAll('a[href^="#"]'))
    .map((link) => ({ link, section: document.getElementById(link.hash.slice(1)) }))
    .filter(({ section }) => section);
  if (!entries.length) return;

  let active;
  let destination;
  let frame;
  let settleTimer;

  function activate(entry) {
    if (entry === active) return;
    active = entry;
    entries.forEach(({ link }) => {
      if (link === entry.link) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });

    // Scroll a short desktop sidebar independently, never move the document.
    if (getComputedStyle(toc).position === 'sticky') {
      const bounds = toc.getBoundingClientRect();
      const item = entry.link.getBoundingClientRect();
      if (item.top < bounds.top) toc.scrollTop += item.top - bounds.top;
      else if (item.bottom > bounds.bottom) toc.scrollTop += item.bottom - bounds.bottom;
    }
  }

  function update() {
    frame = undefined;
    if (destination) return;
    let current = entries[0];
    for (const entry of entries) {
      const offset = parseFloat(getComputedStyle(entry.section).scrollMarginTop) || 0;
      if (entry.section.getBoundingClientRect().top <= offset + 2) current = entry;
    }
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
      current = entries[entries.length - 1];
    }
    activate(current);
  }

  function schedule() {
    if (frame === undefined) frame = requestAnimationFrame(update);
  }

  function finishNavigation() {
    clearTimeout(settleTimer);
    destination = undefined;
    schedule();
  }

  function followAnchor(hash) {
    let target;
    try { target = document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch { return; }
    const section = target?.closest('.doc-section');
    const entry = entries.find((item) => item.section === section);
    if (!entry) { finishNavigation(); return; }
    destination = entry;
    activate(entry);
    clearTimeout(settleTimer);
    // Also release when clicking the same anchor without triggering a scroll.
    settleTimer = setTimeout(finishNavigation, 1500);
  }

  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    if (!link || link.target === '_blank' || link.hasAttribute('download')) return;
    const url = new URL(link.href, location.href);
    if (url.origin === location.origin && url.pathname === location.pathname && url.search === location.search) {
      followAnchor(url.hash);
    }
  });
  window.addEventListener('hashchange', () => followAnchor(location.hash));
  window.addEventListener('scroll', () => {
    schedule();
    if (destination) {
      clearTimeout(settleTimer);
      settleTimer = setTimeout(finishNavigation, 160);
    }
  }, { passive: true });
  window.addEventListener('scrollend', finishNavigation);
  window.addEventListener('wheel', finishNavigation, { passive: true });
  window.addEventListener('touchstart', finishNavigation, { passive: true });
  window.addEventListener('keydown', (event) => {
    if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '].includes(event.key)) finishNavigation();
  });
  window.addEventListener('resize', schedule);
  window.addEventListener('pageshow', schedule);
  window.addEventListener('load', schedule);
  const content = document.querySelector('.doc-content');
  if (content && 'ResizeObserver' in window) new ResizeObserver(schedule).observe(content);
  followAnchor(location.hash);
  schedule();
});
