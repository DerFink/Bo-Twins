// Entwürfe für ein einheitliches Gasballon-Bild (Symbol, Karte, Seitenansicht). Koordinaten 100 × 130.
function bal(D, f, o){
  o = o || {}; const P = hullProf(f), R = 36, H = 74, cx = 50, y0 = 6, fl = o.t || 0;
  const X = (p, s) => cx + Math.sin(p.q * 7 + 1 + fl) * 9 * p.a + s * p.w * R, Y = p => y0 + H * (1 - p.q);
  const L = P.map(p => [X(p, -1), Y(p)]), Rr = P.map(p => [X(p, 1), Y(p)]).reverse();
  const hull = 'M' + L.concat(Rr).map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z';
  const at0 = (q, s) => { let i = 0; while (i < P.length - 1 && P[i + 1].q < q) i++; const a = P[i], b = P[Math.min(i + 1, P.length - 1)], t = b.q > a.q ? (q - a.q) / (b.q - a.q) : 0;
    const p = {q, w: a.w + (b.w - a.w) * t, a: a.a + (b.a - a.a) * t}; return [X(p, s), Y(p)]; };
  const at = (q, s) => at0(q, s);
  const bot = at(0, 0), by = bot[1], ringY = by + 9, baskY = by + 20, bw = 13, bh = 10, k = o.k || 1;
  let g = '';
  const defs = `<defs><radialGradient id="sh${D.id}" cx="35%" cy="28%" r="75%"><stop offset="0" stop-color="${D.hi}"/><stop offset=".55" stop-color="${D.env}"/><stop offset="1" stop-color="${D.lo}"/></radialGradient><clipPath id="cl${D.id}${o.uid||''}"><path d="${hull}"/></clipPath></defs>`;
  // Füllansatz (Schlauch unten an der Hülle)
  if (D.app) g += `<path d="M${bot[0] + 1.5} ${by - 2} q 4 5 2.5 10" fill="none" stroke="${D.appC}" stroke-width="${2.2 * k}" stroke-linecap="round"/>`;
  // Hülle
  g += `<path d="${hull}" fill="${D.flat ? D.env : 'url(#sh' + D.id + ')'}" stroke="${D.out}" stroke-width="${D.ow * k}" stroke-linejoin="round"/>`;
  // Bahnen (Gores)
  if (D.gores) { let s = ''; for (const m of [-0.5, 0, 0.5]) { s += 'M' + P.filter(p => p.q > 0.04).map(p => { const x = cx + Math.sin(p.q * 7 + 1 + fl) * 9 * p.a + m * p.w * R; return x.toFixed(1) + ' ' + Y(p).toFixed(1); }).join('L'); }
    g += `<path d="${s}" fill="none" stroke="${D.goreC}" stroke-opacity=".35" stroke-width="${1.6 * k}"/>`; }
  // Netz
  if (D.net){ const lv = D.net === 'diamond' ? [0.12, 0.3, 0.48, 0.66, 0.82, 0.94] : [0.3, 0.6, 0.85], N = D.net === 'diamond' ? 3 : 3; let s = '';
    if (D.net === 'diamond'){ const QT = 0.94, M = 14, kq = 7.2;                  // Netz als Rauten auf der Kugel: Linien schräg über die Längengrade, oben am Kronenring
      for (const sg of [1, -1]) for (let j = 0; j < M; j++){ let on = false;
        for (let q = 0.03; q <= QT + 1e-6; q += 0.02){ const ph = 2 * Math.PI * j / M + sg * kq * (QT - q) * 0.5, c = Math.cos(ph);
          if (c < 0.05){ on = false; continue; } const p = at(q, Math.sin(ph)); s += (on ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); on = true; } }
      const cr = at(QT, 1), cl = at(QT, -1); s += `M${cl[0].toFixed(1)} ${cl[1].toFixed(1)}Q${((cl[0] + cr[0]) / 2).toFixed(1)} ${(cl[1] + 2.4).toFixed(1)} ${cr[0].toFixed(1)} ${cr[1].toFixed(1)}`; }
    else { lv.forEach(q => { let pts = []; for (let m = -1; m <= 1.001; m += 0.1){ const p = at(q, m); pts.push([p[0], p[1] + 3 * (1 - m * m) * (P[0].w > 0.5 ? 1 : 0.3)]); } s += 'M' + pts.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L'); });
      for (const m of [-0.75, -0.25, 0.25, 0.75]) s += 'M' + [0.05, 0.3, 0.6, 0.85, 0.97].map(q => at(q, m)).map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L'); }
    g += `<g clip-path="url(#cl${D.id}${o.uid||''})"><path d="${s}" fill="none" stroke="${D.netC}" stroke-opacity="${D.netO}" stroke-width="${D.netW * k}" stroke-linecap="round"/></g>`; }
  // Ventil oben
  if (D.valve){ const t = at(1, 0); g += `<ellipse cx="${t[0]}" cy="${t[1] + 1.5}" rx="${4.5}" ry="${2.2}" fill="${D.valveC}" stroke="${D.out}" stroke-width="${1 * k}"/>`; }
  // Leinen: Netzunterkante -> Lastring -> Korb
  const ln = [-0.9, -0.45, 0.45, 0.9].map(m => at(0.12, m)); let s = '';
  ln.forEach(p => { s += `M${p[0].toFixed(1)} ${p[1].toFixed(1)}L${cx + (p[0] < cx ? -2.5 : 2.5)} ${ringY}`; });
  s += `M${cx - 3} ${ringY}L${cx - bw / 2 + 1} ${baskY}M${cx + 3} ${ringY}L${cx + bw / 2 - 1} ${baskY}`;
  g += `<path d="${s}" fill="none" stroke="${D.line}" stroke-width="${1.1 * k}"/>`;
  if (D.ring) g += `<ellipse cx="${cx}" cy="${ringY}" rx="4" ry="1.4" fill="none" stroke="${D.line}" stroke-width="${1.6 * k}"/>`;
  // Korb
  g += `<rect x="${cx - bw / 2}" y="${baskY}" width="${bw}" height="${bh}" rx="2" fill="${D.bask}" stroke="${D.out}" stroke-width="${1.2 * k}"/>`;
  if (D.weave) g += `<path d="M${cx - bw / 2 + 1.5} ${baskY + 3.5}h${bw - 3}M${cx - bw / 2 + 1.5} ${baskY + 6.5}h${bw - 3}" stroke="${D.weaveC}" stroke-width="${0.9 * k}"/>`;
  if (D.sand) [-1, 1].forEach(sg => { g += `<path d="M${cx + sg * bw / 2} ${baskY + 1.5}l${sg * 2.5} 3" stroke="${D.line}" stroke-width=".8"/><rect x="${cx + sg * (bw / 2 + 1.5) - 2.2}" y="${baskY + 4}" width="4.4" height="6" rx="1.6" fill="${D.sandC}" stroke="${D.out}" stroke-width=".7"/>`; });
  return defs + g;
}
const DES0 = [
 {id: 'A', name: 'A · Orange mit Netz', env: '#ff9f1c', hi: '#ffc266', lo: '#d97a00', out: '#0a1019', ow: 2, gores: false, goreC: '#7a4300', net: 'grid', netC: '#3a2200', netO: .45, netW: .9, valve: true, valveC: '#c9d6e8', ring: true, line: '#c9d6e8', bask: '#b98a4a', weave: true, weaveC: '#8a6332', sand: true, sandC: '#e8c27a', app: true, appC: '#ff9f1c'},
 {id: 'B', name: 'B · Silberhülle, oranges Rautennetz', env: '#e4e9ef', hi: '#ffffff', lo: '#9fb0c4', out: '#0a1019', ow: 1.8, gores: false, net: 'diamond', netC: '#ff9f1c', netO: .95, netW: 1.1, valve: true, valveC: '#ff9f1c', ring: true, line: '#c9d6e8', bask: '#b98a4a', weave: true, weaveC: '#8a6332', sand: true, sandC: '#e8c27a', app: true, appC: '#d5dbe3'},
 {id: 'C', name: 'C · Klar und flächig', env: '#ff9f1c', hi: '#ff9f1c', lo: '#ff9f1c', flat: true, out: '#0a1019', ow: 3, gores: false, net: 'grid', netC: '#0a1019', netO: .55, netW: 1.6, valve: false, ring: false, line: '#eef3fa', bask: '#eef3fa', weave: false, sand: false, app: false}
];
function svg(D, f, w, h, vb, extra, o){ return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="${vb || '0 0 100 130'}">${extra || ''}${bal(D, f, o)}</svg>`; }
function icon(D){ return svg(D, 1, 150, 150, '-15 -5 130 130', `<rect x="-15" y="-5" width="130" height="130" rx="28" fill="#0e1726"/>`, {k: 1.2}); }
function side(D){ // Seitenansicht: Himmel, Gelände, Schlepptau
  const sky = `<rect x="-60" y="-10" width="220" height="160" fill="#14315a"/><path d="M-60 132 C-10 124 30 136 80 128 C120 122 140 132 160 128 L160 150 L-60 150Z" fill="#234a3a" stroke="#5fe3a1" stroke-width="1"/>`;
  const rope = `<path d="M56 120 C60 128 70 131 90 131 L130 130" fill="none" stroke="#d9b36c" stroke-width="1.6"/>`;
  return svg(D, 0.9, 260, 175, '-60 -14 220 152', sky + rope, {uid: 's'}); }
function marker(D, f, bg){ return `<div style="display:inline-block;background:${bg};padding:6px;border-radius:6px">` + svg(D, f, 44, 57, '0 0 100 130', '', {k: 1.6, uid: 'm' + f + bg.slice(1)}) + '</div>'; }

const Bx = DES0[1];
const DES = [Object.assign({}, Bx, {id: 'B', name: 'B wie bisher: vier Reihen'}),
 Object.assign({}, Bx, {id: 'B1', name: 'B1 · eine Reihe mehr, Rauten flacher', Q: [0.04, 0.232, 0.424, 0.616, 0.808, 1]}),
 Object.assign({}, Bx, {id: 'B2', name: 'B2 · eine Reihe mehr, Rauten schmaler (Form bleibt)', Q: [0.04, 0.232, 0.424, 0.616, 0.808, 1], dm: 0.76})];
module.exports = {bal, DES, svg, icon, side, marker};
