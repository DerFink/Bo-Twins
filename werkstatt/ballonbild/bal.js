/* Ballonbild (Entwurf B2, Wahl Nutzer 26.10.2026): Silberhülle mit orangem Rautennetz, Ventil oben, Füllansatz, Lastring, Weidenkorb mit Sandsäcken.
   Dieselbe Zeichnung für Kartensymbol, Seitenansicht, Startseite und App-Symbol. Einheiten: Kasten 100 × 130, Korbunterkante bei (50, 110).
   Die Hülle folgt dem Füllgrad (hullProf); fl ist die Phase des Flatterns. */
const BAL = {env: '#e4e9ef', hi: '#ffffff', lo: '#9fb0c4', out: '#0a1019', net: '#ff9f1c', line: '#c9d6e8', bask: '#b98a4a', weave: '#8a6332', sand: '#e8c27a', app: '#d5dbe3', n: 0};
function balGeo(f, fl){
  const P = hullProf(f), R = 36, H = 74, cx = 50, y0 = 6, F = fl || 0;
  const X = (p, s) => cx + Math.sin(p.q * 7 + 1 + F) * 9 * p.a + s * p.w * R, Y = p => y0 + H * (1 - p.q), r1 = v => v.toFixed(1);
  const at = (q, s) => { let i = 0; while (i < P.length - 1 && P[i + 1].q < q) i++; const a = P[i], b = P[Math.min(i + 1, P.length - 1)], t = b.q > a.q ? (q - a.q) / (b.q - a.q) : 0;
    const p = {q, w: a.w + (b.w - a.w) * t, a: a.a + (b.a - a.a) * t}; return [X(p, s), Y(p)]; };
  const hull = 'M' + P.map(p => [X(p, -1), Y(p)]).concat(P.map(p => [X(p, 1), Y(p)]).reverse()).map(p => r1(p[0]) + ' ' + r1(p[1])).join('L') + 'Z';
  const Q = [0.04, 0.232, 0.424, 0.616, 0.808, 1], N = 3; let net = '';
  for (const sg of [1, -1]) for (let j = -2 * N; j <= 2 * N; j++) net += 'M' + Q.map((q, i) => at(q, (j + sg * i) / N * 0.76)).map(p => r1(p[0]) + ' ' + r1(p[1])).join('L');
  const bot = at(0, 0), by = bot[1], ringY = by + 9, baskY = by + 20, bw = 13, bh = 10, top = at(1, 0);
  let lines = ''; [-0.9, -0.45, 0.45, 0.9].map(m => at(0.12, m)).forEach(p => { lines += `M${r1(p[0])} ${r1(p[1])}L${cx + (p[0] < cx ? -2.5 : 2.5)} ${ringY}`; });
  lines += `M${cx - 3} ${ringY}L${cx - bw / 2 + 1} ${baskY}M${cx + 3} ${ringY}L${cx + bw / 2 - 1} ${baskY}`;
  const dy = 110 - (baskY + bh);                                                // alles so verschieben, dass die Korbunterkante immer bei y = 110 liegt
  return {hull, net, lines, app: `M${r1(bot[0] + 1.5)} ${r1(by - 2)}q4 5 2.5 10`, ringY, baskY, bw, bh, top, dy};
}
function balloonSVG(c, f, o){
  const g = balGeo(f, o && o.fl), k = (o && o.k) || 1.6, id = 'bal' + (++BAL.n), w = (o && o.w) || 44, h = Math.round(w * 1.3);
  const sb = [-1, 1].map(s => `<path d="M${50 + s * 6.5} ${g.baskY + 1.5}l${s * 2.5} 3" stroke="${BAL.line}" stroke-width=".8"/><rect x="${50 + s * 8 - 2.2}" y="${g.baskY + 4}" width="4.4" height="6" rx="1.6" fill="${BAL.sand}" stroke="${BAL.out}" stroke-width=".7"/>`).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 ${-g.dy} 100 130" width="${w}" height="${h}"><defs><radialGradient id="${id}g" cx="35%" cy="28%" r="75%"><stop offset="0" stop-color="${BAL.hi}"/><stop offset=".55" stop-color="${BAL.env}"/><stop offset="1" stop-color="${BAL.lo}"/></radialGradient><clipPath id="${id}c"><path d="${g.hull}"/></clipPath></defs>` +
    `<path d="${g.app}" fill="none" stroke="${BAL.app}" stroke-width="${2.2 * k}" stroke-linecap="round"/><path d="${g.hull}" fill="url(#${id}g)" stroke="${BAL.out}" stroke-width="${1.8 * k}" stroke-linejoin="round"/>` +
    `<g clip-path="url(#${id}c)"><path d="${g.net}" fill="none" stroke="${BAL.net}" stroke-width="${1.1 * k}" stroke-linecap="round"/></g>` +
    `<ellipse cx="${g.top[0]}" cy="${g.top[1] + 1.5}" rx="4.5" ry="2.2" fill="${BAL.net}" stroke="${BAL.out}" stroke-width="${k}"/>` +
    `<path d="${g.lines}" fill="none" stroke="${BAL.line}" stroke-width="${1.1 * k}"/><ellipse cx="50" cy="${g.ringY}" rx="4" ry="1.4" fill="none" stroke="${BAL.line}" stroke-width="${1.6 * k}"/>` +
    `<rect x="${50 - g.bw / 2}" y="${g.baskY}" width="${g.bw}" height="${g.bh}" rx="2" fill="${BAL.bask}" stroke="${BAL.out}" stroke-width="${1.2 * k}"/><path d="M${51.5 - g.bw / 2} ${g.baskY + 3.5}h${g.bw - 3}M${51.5 - g.bw / 2} ${g.baskY + 6.5}h${g.bw - 3}" stroke="${BAL.weave}" stroke-width="${0.9 * k}"/>` + sb + '</svg>';
}
/* Dieselbe Zeichnung auf einer Leinwand: Korbunterkante bei (x, y), sc Pixel je Einheit (Hüllenradius 36 Einheiten). Gibt den Scheitel (Ventil) zurück. */
function balDraw(c, f, fl, x, y, sc){
  const g = balGeo(f, fl), lw = (u, minPx) => Math.max(u, (minPx || 0.8) / sc);
  c.save(); c.translate(x - 50 * sc, y - 110 * sc); c.scale(sc, sc); c.translate(0, g.dy); c.lineCap = 'round'; c.lineJoin = 'round';
  const hull = new Path2D(g.hull), gr = c.createRadialGradient(38, 25, 2, 42, 32, 62); gr.addColorStop(0, BAL.hi); gr.addColorStop(.55, BAL.env); gr.addColorStop(1, BAL.lo);
  c.strokeStyle = BAL.app; c.lineWidth = lw(3.4); c.stroke(new Path2D(g.app));
  c.fillStyle = gr; c.fill(hull);
  c.save(); c.clip(hull); c.strokeStyle = BAL.net; c.lineWidth = lw(1.6, 0.7); c.stroke(new Path2D(g.net)); c.restore();
  c.strokeStyle = BAL.out; c.lineWidth = lw(2.6, 1); c.stroke(hull);
  c.fillStyle = BAL.net; c.beginPath(); c.ellipse(g.top[0], g.top[1] + 1.5, 4.5, 2.2, 0, 0, 7); c.fill(); c.lineWidth = lw(1.4, 0.7); c.stroke();
  c.strokeStyle = BAL.line; c.lineWidth = lw(1.5, 0.8); c.stroke(new Path2D(g.lines)); c.beginPath(); c.ellipse(50, g.ringY, 4, 1.4, 0, 0, 7); c.lineWidth = lw(2.2, 0.8); c.stroke();
  [-1, 1].forEach(s => { c.strokeStyle = BAL.line; c.lineWidth = lw(1, 0.6); c.beginPath(); c.moveTo(50 + s * 6.5, g.baskY + 1.5); c.lineTo(50 + s * 9, g.baskY + 4.5); c.stroke();
    c.fillStyle = BAL.sand; c.strokeStyle = BAL.out; c.beginPath(); c.roundRect ? c.roundRect(50 + s * 8 - 2.2, g.baskY + 4, 4.4, 6, 1.6) : c.rect(50 + s * 8 - 2.2, g.baskY + 4, 4.4, 6); c.fill(); c.stroke(); });
  c.fillStyle = BAL.bask; c.strokeStyle = BAL.out; c.lineWidth = lw(1.6, 0.8); c.beginPath(); c.roundRect ? c.roundRect(50 - g.bw / 2, g.baskY, g.bw, g.bh, 2) : c.rect(50 - g.bw / 2, g.baskY, g.bw, g.bh); c.fill(); c.stroke();
  c.strokeStyle = BAL.weave; c.lineWidth = lw(1.2, 0.6); c.beginPath(); c.moveTo(51.5 - g.bw / 2, g.baskY + 3.5); c.lineTo(48.5 + g.bw / 2, g.baskY + 3.5); c.moveTo(51.5 - g.bw / 2, g.baskY + 6.5); c.lineTo(48.5 + g.bw / 2, g.baskY + 6.5); c.stroke();
  c.restore();
  return [x + (g.top[0] - 50) * sc, y + (g.top[1] + g.dy - 110) * sc];
}
