// Fake cursor, click ripple and caption pill for headless screenshots.
// Idempotent: eval it before every call, it only builds the DOM once per page load.
(function () {
  const ARROW = '<svg width="26" height="26" viewBox="0 0 24 24" style="filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.35))"><path d="M3 2 L3 19.2 L7.4 15 L10.4 21.6 L13.4 20.3 L10.5 13.9 L16.6 13.9 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  if (!document.getElementById('__cur')) {
    const root = document.documentElement;
    const c = document.createElement('div'); c.id = '__cur';
    c.style.cssText = 'position:fixed;left:0;top:0;width:26px;height:26px;pointer-events:none;z-index:2147483647;will-change:transform;';
    c.innerHTML = ARROW;
    const r = document.createElement('div'); r.id = '__rip';
    r.style.cssText = 'position:fixed;left:0;top:0;pointer-events:none;z-index:2147483646;border-radius:50%;border:3px solid rgba(200,16,46,.85);background:rgba(200,16,46,.18);display:none;';
    const p = document.createElement('div'); p.id = '__cap';
    p.style.cssText = 'position:fixed;top:22px;left:50%;transform:translateX(-50%);pointer-events:none;z-index:2147483645;background:rgba(17,24,39,.88);color:#fff;font:600 20px/1.2 -apple-system,Helvetica,Arial,sans-serif;padding:10px 22px;border-radius:999px;box-shadow:0 4px 14px rgba(0,0,0,.18);display:none;white-space:nowrap;';
    root.appendChild(r); root.appendChild(p); root.appendChild(c);
  }
  // arrow tip (or tap dot center) sits at (x, y)
  window.__pos = (x, y) => {
    const c = document.getElementById('__cur'), t = c.dataset.touch === '1';
    c.style.transform = `translate(${x - (t ? 13 : 3)}px,${y - (t ? 13 : 2)}px)`;
  };
  window.__rip = (x, y, d) => {
    const r = document.getElementById('__rip');
    if (d <= 0) { r.style.display = 'none'; return; }
    Object.assign(r.style, { display: 'block', width: d + 'px', height: d + 'px',
      transform: `translate(${x - d / 2}px,${y - d / 2}px)`, opacity: String(1 - d / 70) });
  };
  window.__cap = t => { const p = document.getElementById('__cap'); p.style.display = t ? 'block' : 'none'; p.textContent = t || ''; };
  // touch mode (phone viewports): a soft round dot instead of the arrow
  window.__touch = on => {
    const c = document.getElementById('__cur');
    if (!!on === (c.dataset.touch === '1')) return;
    c.dataset.touch = on ? '1' : '0';
    c.innerHTML = on
      ? '<div style="width:26px;height:26px;border-radius:50%;background:rgba(17,24,39,.35);border:2px solid rgba(255,255,255,.9);box-shadow:0 1px 4px rgba(0,0,0,.3)"></div>'
      : ARROW;
  };
  // scrollto: find the element's scroll container, plan the distance, then step it with an ease
  window.__scrollPlan = (sel, offset) => {
    const el = document.querySelector(sel);
    if (!el) return 'missing';
    let s = el.parentElement;
    while (s && s !== document.body && s !== document.documentElement) {
      const oy = getComputedStyle(s).overflowY;
      if (/(auto|scroll)/.test(oy) && s.scrollHeight > s.clientHeight + 1) break;
      s = s.parentElement;
    }
    if (!s || s === document.body || s === document.documentElement) s = document.scrollingElement;
    window.__scr = { s, dy: el.getBoundingClientRect().top - offset, done: 0 };
    return 'ok';
  };
  window.__scrollStep = (i, n) => {
    const p = window.__scr, e = t => t * t * (3 - 2 * t);
    const want = Math.round(p.dy * e(i / n));
    p.s.scrollBy(0, want - p.done); p.done = want;
  };
  // center of an element; "sel@2" picks the third match
  window.__ctr = sel => {
    const m = sel.match(/^(.*)@(\d+)$/);
    const el = m ? document.querySelectorAll(m[1])[+m[2]] : document.querySelector(sel);
    if (!el) return 'missing';
    const b = el.getBoundingClientRect();
    return Math.round(b.left + b.width / 2) + ',' + Math.round(b.top + b.height / 2);
  };
})();
