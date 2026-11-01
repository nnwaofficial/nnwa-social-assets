// Collision audit, evaluated inside a rendered creative page.
// Reports text that touches photos, dashed rings, seals, logos or other text,
// and text outside the safe area. Returns a list of strings.
() => {
  const W = innerWidth, H = innerHeight, out = [];
  const name = el => (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : el.tagName.toLowerCase());
  const path = el => { const p = []; for (let e = el; e && e !== document.body && p.length < 3; e = e.parentElement) p.unshift(name(e)); return p.join('>'); };
  // text line boxes: one rect per text node line
  const texts = [];
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = tw.nextNode());) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement, cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    // Range rects cover the font's full ascent+descent; trim to roughly the inked glyphs
    const fs = parseFloat(cs.fontSize);
    let rot = false; for (let e = el; e; e = e.parentElement) { const tf = getComputedStyle(e).transform; if (tf && tf !== 'none' && !/^matrix\(1, 0, 0, 1/.test(tf)) { rot = true; break; } }
    for (const q of r.getClientRects()) {
      if (q.width <= 1 || q.height <= 1) continue;
      let b = { left: q.left, right: q.right, top: q.top, bottom: q.bottom };
      if (rot && q.height > q.width) { b.left += 0.30 * fs; b.right -= 0.30 * fs; }
      else { b.top += 0.26 * fs; b.bottom -= 0.14 * fs; }
      texts.push({ el, b, t: n.textContent.trim().slice(0, 40) });
    }
  }
  const block = q => [...document.querySelectorAll(q)].filter(e => getComputedStyle(e).display !== 'none');
  const obst = [];
  for (const e of block('.photo, .tile, .page, .feed')) {
    if (e.parentElement.classList.contains('panel')) continue; // report header: text on a dimmed photo panel by design
    const b = e.getBoundingClientRect(), circ = e.classList.contains('circle');
    obst.push({ e, b, kind: circ ? 'circle' : 'rect' });
  }
  for (const e of block('.ring')) obst.push({ e, b: e.getBoundingClientRect(), kind: 'ring' });
  for (const e of block('.seal, .logo, .dots, .bar, .deco')) obst.push({ e, b: e.getBoundingClientRect(), kind: 'rect' });
  const pad = 6;
  const hitRect = (a, b) => a.left < b.right + pad && a.right > b.left - pad && a.top < b.bottom + pad && a.bottom > b.top - pad;
  const near = (cx, cy, b) => { const x = Math.max(b.left, Math.min(cx, b.right)), y = Math.max(b.top, Math.min(cy, b.bottom)); return Math.hypot(x - cx, y - cy); };
  const far = (cx, cy, b) => Math.max(...[[b.left, b.top], [b.right, b.top], [b.left, b.bottom], [b.right, b.bottom]].map(([x, y]) => Math.hypot(x - cx, y - cy)));
  for (const t of texts) {
    for (const o of obst) {
      if (o.e.contains(t.el)) continue;
      // text sitting on a full-bleed photo with an overlay is intended
      if (o.kind === 'rect' && o.b.width >= W - 2 && o.b.height >= H - 2) continue;
      const cx = (o.b.left + o.b.right) / 2, cy = (o.b.top + o.b.bottom) / 2, r = o.b.width / 2;
      let hit = false;
      if (o.kind === 'rect') hit = hitRect(t.b, o.b);
      else if (o.kind === 'circle') hit = near(cx, cy, t.b) < r + pad;
      else hit = near(cx, cy, t.b) < r + pad && far(cx, cy, t.b) > r - pad;
      if (hit) out.push(`TEXT/${o.kind.toUpperCase()}  "${t.t}" [${path(t.el)}] x ${path(o.e)}`);
    }
    if (t.b.left < 0 || t.b.right > W || t.b.top < 0 || t.b.bottom > H) out.push(`OFFCANVAS "${t.t}"`);
  }
  // text on text (different elements, not ancestors)
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i], b = texts[j];
    if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ox = Math.min(a.b.right, b.b.right) - Math.max(a.b.left, b.b.left), oy = Math.min(a.b.bottom, b.b.bottom) - Math.max(a.b.top, b.b.top);
    if (ox > 2 && oy > 2) out.push(`TEXT/TEXT "${a.t}" x "${b.t}"`);
  }
  // non-text block overlaps that look accidental: photo vs ring is intended; photo vs logo/seal is not
  return [...new Set(out)];
}
