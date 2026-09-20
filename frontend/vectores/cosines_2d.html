/* Utilidades compartidas por los visualizadores. Se inyectan en cada componente HTML. */
const VZ = (() => {
'use strict';

/* ---------- constantes ---------- */
const C = {bg:'#0d0f16', text:'#eeeae2', muted:'#8c92a4', sol:'#e8b94e',
           a:'#e0674f', b:'#3fa796', n:'#8b7fd6', k:'#d45a94'};
const FONT = {
  serif:  "italic 500 22px Newsreader, 'Iowan Old Style', Georgia, serif",
  serifS: "italic 500 19px Newsreader, 'Iowan Old Style', Georgia, serif",
  sans:   "500 12.5px Figtree, ui-sans-serif, system-ui, sans-serif",
  sansM:  "500 13.5px Figtree, ui-sans-serif, system-ui, sans-serif",
};
const $ = id => document.getElementById(id);
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- números y texto ---------- */
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const fmt = (n, d = 2) => {
  if (Math.abs(n) < 0.5 * Math.pow(10, -d)) n = 0;
  return n.toFixed(d).replace('-', '−');
};
const par = n => n < -0.005 ? `(${fmt(n)})` : fmt(n);
const tup = (v, d = 2) => `(${v.map(x => fmt(x, d)).join(', ')})`;

/* ---------- álgebra 3D ---------- */
const add = (u, v) => [u[0] + v[0], u[1] + v[1], u[2] + v[2]];
const sub = (u, v) => [u[0] - v[0], u[1] - v[1], u[2] - v[2]];
const mul = (u, k) => [u[0] * k, u[1] * k, u[2] * k];
const dot = (u, v) => u[0] * v[0] + u[1] * v[1] + u[2] * v[2];
const cross = (u, v) => [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
const len = u => Math.hypot(u[0], u[1], u[2]);
const norm = u => { const l = len(u); return l < 1e-9 ? [0, 0, 0] : mul(u, 1 / l); };

/** Rota v un ángulo a alrededor del eje unitario k (fórmula de Rodrigues). */
function rotAbout(v, k, a) {
  const c = Math.cos(a), s = Math.sin(a);
  return add(add(mul(v, c), mul(cross(k, v), s)), mul(k, dot(k, v) * (1 - c)));
}

/** Interpolación esférica entre dos vectores unitarios. */
function slerp(u, v, t) {
  const c = clamp(dot(u, v), -1, 1), th = Math.acos(c);
  if (th < 1e-4) return v.slice();
  if (Math.PI - th < 1e-3) {                                 // opuestos: girar por un perpendicular
    const p = norm(cross(u, Math.abs(u[2]) < .9 ? [0, 0, 1] : [1, 0, 0]));
    return add(mul(u, Math.cos(Math.PI * t)), mul(p, Math.sin(Math.PI * t)));
  }
  const s = Math.sin(th);
  return add(mul(u, Math.sin((1 - t) * th) / s), mul(v, Math.sin(t * th) / s));
}

/* ---------- dibujo 2D ---------- */
function text(ctx, str, x, y, font, color, align = 'center') {
  ctx.save();
  ctx.font = font; ctx.textAlign = align; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.lineWidth = 5; ctx.strokeStyle = C.bg; ctx.strokeText(str, x, y);
  ctx.fillStyle = color; ctx.fillText(str, x, y);
  ctx.restore();
}

function hull(pts) {
  pts = pts.slice().sort((p, q) => p.x - q.x || p.y - q.y);
  const cr = (o, a, b) => (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
  const lo = [], up = [];
  for (const p of pts) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
  for (let i = pts.length - 1; i >= 0; i--) { const p = pts[i]; while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
  up.pop(); lo.pop();
  return lo.concat(up);
}

/** Flecha 2D en coordenadas de pantalla. */
function arrow2(ctx, x0, y0, x1, y1, color, w = 3.6, head = 17) {
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy);
  if (L < 1) return;
  const ux = dx / L, uy = dy / L, hl = Math.min(head, L * .6), hw = hl * .4;
  ctx.save();
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1 - ux * hl * .8, y1 - uy * hl * .8); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x1 - ux * hl + uy * hw, y1 - uy * hl - ux * hw);
  ctx.lineTo(x1 - ux * hl - uy * hw, y1 - uy * hl + ux * hw);
  ctx.closePath(); ctx.fill();
  ctx.restore();
}

/** Anillo de agarre alrededor de una punta arrastrable. */
function ring2(ctx, x, y, color, hot, r = 14) {
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = 1.6; ctx.globalAlpha = hot ? .95 : .5;
  ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI);
  if (hot) { ctx.save(); ctx.globalAlpha = .15; ctx.fillStyle = color; ctx.fill(); ctx.restore(); }
  ctx.stroke(); ctx.restore();
}

/**
 * Sector y arco entre las direcciones matemáticas a0 y a1 (camino corto, y hacia arriba).
 * Si el ángulo es recto y o.right = true, dibuja un cuadrado. Devuelve {mid, d}.
 */
function arc2(ctx, cx, cy, a0, a1, r, o = {}) {
  let d = a1 - a0;
  while (d > Math.PI) d -= 2 * Math.PI;
  while (d <= -Math.PI) d += 2 * Math.PI;
  if (Math.abs(d) < 1e-3) return {mid: a0, d};
  ctx.save();
  ctx.setLineDash([]); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.fillStyle = o.fill || 'rgba(232,185,78,.16)'; ctx.strokeStyle = o.stroke || C.sol; ctx.lineWidth = o.width || 2.4;
  if (o.right && Math.abs(Math.abs(d) - Math.PI / 2) < .0175) {
    const s = r * .62, u = [Math.cos(a0), -Math.sin(a0)], w = [Math.cos(a1), -Math.sin(a1)];
    const p1 = [cx + u[0] * s, cy + u[1] * s], p2 = [cx + (u[0] + w[0]) * s, cy + (u[1] + w[1]) * s], p3 = [cx + w[0] * s, cy + w[1] * s];
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(...p1); ctx.lineTo(...p2); ctx.lineTo(...p3); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(...p1); ctx.lineTo(...p2); ctx.lineTo(...p3); ctx.stroke();
  } else {
    ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, r, -a0, -a0 - d, d > 0); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.arc(cx, cy, r, -a0, -a0 - d, d > 0); ctx.stroke();
  }
  ctx.restore();
  return {mid: a0 + d / 2, d};
}

/* ---------- cámara 3D (proyección ortogonal) ---------- */
class View3D {
  constructor(cv, o = {}) {
    this.cv = cv; this.ctx = cv.getContext('2d');
    this.ext = o.ext || 4;
    this.yaw0 = o.yaw !== undefined ? o.yaw : Math.PI + .62;
    this.pitch0 = o.pitch !== undefined ? o.pitch : .58;
    this.yaw = this.yaw0; this.pitch = this.pitch0;
    this.W = this.H = 0; this.S = this.S0 = 1; this.cx = this.cy = 0; this.dpr = 1;
    this.RX = [1, 0, 0]; this.RU = [0, 0, 1]; this.RD = [0, 1, 0];   // derecha, arriba, profundidad
  }
  basis() {
    const cf = Math.cos(this.yaw), sf = Math.sin(this.yaw), ce = Math.cos(this.pitch), se = Math.sin(this.pitch);
    this.RX = [cf, -sf, 0];
    this.RU = [sf * se, cf * se, ce];
    this.RD = [sf * ce, cf * ce, -se];
  }
  resize() {
    const r = this.cv.getBoundingClientRect();
    this.dpr = window.devicePixelRatio || 1; this.W = r.width; this.H = r.height;
    this.cv.width = Math.round(this.W * this.dpr); this.cv.height = Math.round(this.H * this.dpr);
    this.S0 = this.S = Math.max(1, Math.min(this.H / (2 * (this.ext + .6)), this.W / (2 * this.ext * 1.35)));
    this.cx = this.W / 2; this.cy = this.H / 2;
  }
  begin() {
    this.basis(); this.S = this.S0;
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    this.ctx.clearRect(0, 0, this.W, this.H);
  }
  proj(p) { return {x: this.cx + this.S * dot(this.RX, p), y: this.cy - this.S * dot(this.RU, p), d: dot(this.RD, p)}; }
  poly(pts3, close = true) {
    const c = this.ctx; c.beginPath();
    pts3.forEach((p, i) => { const q = this.proj(p); i ? c.lineTo(q.x, q.y) : c.moveTo(q.x, q.y); });
    if (close) c.closePath();
  }
  line3(a, b) { const p = this.proj(a), q = this.proj(b), c = this.ctx; c.beginPath(); c.moveTo(p.x, p.y); c.lineTo(q.x, q.y); }

  floor() {
    const c = this.ctx, E = this.ext;
    c.save(); c.lineWidth = 1;
    c.fillStyle = 'rgba(238,234,226,.018)';
    this.poly([[-E, -E, 0], [E, -E, 0], [E, E, 0], [-E, E, 0]]); c.fill();
    c.strokeStyle = 'rgba(238,234,226,.055)';
    for (let i = -E; i <= E; i++) { this.line3([-E, i, 0], [E, i, 0]); c.stroke(); this.line3([i, -E, 0], [i, E, 0]); c.stroke(); }
    c.restore();
  }
  /** Ejes x, y, z. o.pos: colores opcionales de las semirrectas positivas; o.labels: nombres. */
  axes(o = {}) {
    const c = this.ctx, E = this.ext, pos = o.pos || [], labels = o.labels || ['x', 'y', 'z'];
    const dirs = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    c.save(); c.lineWidth = 1.2; c.strokeStyle = 'rgba(238,234,226,.30)';
    dirs.forEach(d => { this.line3(mul(d, -E), mul(d, E)); c.stroke(); });
    pos.forEach((col, i) => {
      if (!col) return;
      c.strokeStyle = col; c.globalAlpha = .65; c.lineWidth = 1.8;
      this.line3([0, 0, 0], mul(dirs[i], E)); c.stroke();
    });
    c.restore();
    dirs.forEach((d, i) => { const q = this.proj(mul(d, E + .45)); text(c, labels[i], q.x, q.y, FONT.serifS, pos[i] || C.muted); });
  }
  /** Flecha 3D con punta cónica. ring: null | 'idle' | 'hot'. */
  arrow(v, color, ring, width = 3.6) {
    const L = len(v);
    if (L < 1e-6) return;
    const c = this.ctx, dir = mul(v, 1 / L), hl = Math.min(.34, L * .4), hr = hl * .38;
    const baseC = mul(dir, L - hl);
    const o = this.proj([0, 0, 0]), b = this.proj(baseC), t = this.proj(v);
    c.save(); c.lineCap = 'round'; c.lineJoin = 'round';
    c.strokeStyle = color; c.lineWidth = width;
    c.beginPath(); c.moveTo(o.x, o.y); c.lineTo(b.x, b.y); c.stroke();
    const ref = Math.abs(dir[2]) < .9 ? [0, 0, 1] : [1, 0, 0];
    const u = norm(cross(dir, ref)), w = cross(dir, u), rim = [];
    for (let k = 0; k < 18; k++) {
      const a = k / 18 * 2 * Math.PI;
      const q = this.proj(add(baseC, add(mul(u, hr * Math.cos(a)), mul(w, hr * Math.sin(a)))));
      rim.push({x: q.x, y: q.y});
    }
    const sil = hull(rim.concat([{x: t.x, y: t.y}]));
    c.fillStyle = color; c.beginPath();
    sil.forEach((p, i) => i ? c.lineTo(p.x, p.y) : c.moveTo(p.x, p.y)); c.closePath(); c.fill();
    if (dot(dir, this.RD) > 0) {                              // se ve la base del cono
      c.fillStyle = 'rgba(13,15,22,.32)'; c.beginPath();
      rim.forEach((p, i) => i ? c.lineTo(p.x, p.y) : c.moveTo(p.x, p.y)); c.closePath(); c.fill();
    }
    c.restore();
    if (ring) ring2(c, t.x, t.y, color, ring === 'hot');
  }
  /** Etiqueta junto a la punta de v, alejada del origen en pantalla. */
  tipLabel(v, str, font, color, gap = 30) {
    const o = this.proj([0, 0, 0]), t = this.proj(v), dx = t.x - o.x, dy = t.y - o.y, L = Math.hypot(dx, dy);
    const ux = L < 1 ? 0 : dx / L, uy = L < 1 ? -1 : dy / L;
    text(this.ctx, str, t.x + ux * gap, t.y + uy * gap, font, color);
  }
}

/**
 * Interacción 3D: arrastrar puntas (en el plano de la pantalla, o solo en z) y girar la vista arrastrando el fondo.
 * o.tips() → [{k, v}]; o.set(k, v); o.redraw(); o.vertical(e) → bool; o.onStart(); o.onDblBg().
 */
function bind3D(view, o) {
  const cv = view.cv, st = {hover: null, drag: null, orbit: null};
  const pos = e => { const r = cv.getBoundingClientRect(); return {px: e.clientX - r.left, py: e.clientY - r.top}; };
  const find = k => o.tips().find(t => t.k === k);
  const hit = (px, py, touch) => {
    let best = null, bd = touch ? 36 : 24;
    o.tips().forEach(t => { const q = view.proj(t.v), d = Math.hypot(px - q.x, py - q.y); if (d <= bd) { bd = d; best = t.k; } });
    return best;
  };
  cv.addEventListener('pointerdown', e => {
    const {px, py} = pos(e), k = hit(px, py, e.pointerType === 'touch');
    if (o.onStart) o.onStart();
    cv.setPointerCapture(e.pointerId); cv.style.cursor = 'grabbing';
    if (k) { const q = view.proj(find(k).v); st.drag = {k, ox: px - q.x, oy: py - q.y, ly: py}; }
    else st.orbit = {lx: px, ly: py};
    o.redraw();
  });
  cv.addEventListener('pointermove', e => {
    const {px, py} = pos(e);
    if (st.drag) {
      const d = st.drag, v = find(d.k).v;
      if (o.vertical(e)) {                                     // solo en z
        const dz = (-(py - d.ly) / view.S) / Math.max(.3, Math.cos(view.pitch));
        o.set(d.k, add(v, [0, 0, dz]));
        const q = view.proj(find(d.k).v); d.ox = px - q.x; d.oy = py - q.y;
      } else {                                                 // en el plano paralelo a la pantalla
        const q = view.proj(v);
        const ds = (px - d.ox - q.x) / view.S, du = -(py - d.oy - q.y) / view.S;
        o.set(d.k, add(v, add(mul(view.RX, ds), mul(view.RU, du))));
      }
      d.ly = py; o.redraw(); return;
    }
    if (st.orbit) {
      view.yaw += (px - st.orbit.lx) * 0.008;
      view.pitch = clamp(view.pitch + (py - st.orbit.ly) * 0.006, -1.5, 1.5);
      st.orbit.lx = px; st.orbit.ly = py; o.redraw(); return;
    }
    if (e.pointerType === 'touch') return;
    const k = hit(px, py, false);
    if (k !== st.hover) { st.hover = k; cv.style.cursor = k ? 'grab' : 'default'; o.redraw(); }
  });
  const end = () => { st.drag = null; st.orbit = null; cv.style.cursor = st.hover ? 'grab' : 'default'; o.redraw(); };
  cv.addEventListener('pointerup', end);
  cv.addEventListener('pointercancel', end);
  cv.addEventListener('pointerleave', () => { if (!st.drag && !st.orbit && st.hover) { st.hover = null; o.redraw(); } });
  cv.addEventListener('dblclick', e => {
    if (!o.onDblBg) return;
    const {px, py} = pos(e); if (!hit(px, py, false)) o.onDblBg();
  });
  return st;
}

/* ---------- altura del iframe en pantallas estrechas ---------- */
let fitted = false, fitQueued = false;
function fitNow() {
  try {
    const fe = window.frameElement;
    if (!fe || !window.innerWidth) return;
    if (!window.matchMedia('(max-width:820px)').matches) {
      if (fitted) { fe.style.removeProperty('height'); fitted = false; }
      return;
    }
    const app = document.querySelector('.app');
    const h = Math.ceil(app.getBoundingClientRect().bottom + window.scrollY) + 6;
    if (Math.abs(fe.getBoundingClientRect().height - h) > 2) { fe.style.height = h + 'px'; fitted = true; }
  } catch (e) { /* iframe sin acceso al documento padre: queda el scroll interno */ }
}
const fit = () => {
  if (fitQueued) return;
  fitQueued = true;
  requestAnimationFrame(() => { fitQueued = false; fitNow(); });
};
window.addEventListener('resize', fit);

return {C, FONT, $, reduce, clamp, fmt, par, tup, add, sub, mul, dot, cross, len, norm,
        rotAbout, slerp, text, hull, arrow2, ring2, arc2, View3D, bind3D, fit};
})();
