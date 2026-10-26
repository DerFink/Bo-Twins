const fs = require('fs'); eval(fs.readFileSync('hull.js', 'utf8')); const G = (()=>{ const m = {exports:{}}; eval(fs.readFileSync('gen2.js','utf8').replace('module.exports =','m.exports =')); return m.exports; })();
const FS = [1, 0.6, 0.4, 0.2, 0.05];
let h = `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#0a1019;color:#eef3fa;font:14px Arial,sans-serif;padding:16px;width:1180px}
h2{font-size:19px;margin:22px 0 8px}.row{display:flex;gap:22px;align-items:flex-end}.c{text-align:center}.c small{display:block;color:#9db3d1;margin-top:4px}
.fill{display:flex;gap:6px;background:#1d4a6b;border-radius:8px;padding:6px 8px}.fill div{text-align:center;font-size:12px;color:#c9d6e8}</style>
<h1 style="font-size:22px;margin:0">Gasballon: Entwurf B mit einer weiteren Reihe Rauten</h1>
<p style="color:#9db3d1;margin:4px 0 0">Je Entwurf dieselbe Zeichnung überall. Typisch Gasballon: runde Hülle mit Netz, Ventil oben, Füllansatz unten, Lastring, Korb mit Sandsäcken. Die Form folgt dem Füllgrad (Pilz bis 50 %, darunter schmaler, unter 20 % flatternd).</p>`;
for (const D of G.DES){
  h += `<h2>${D.name}</h2><div class="row">`;
  h += `<div class="c">${G.icon(D)}<small>App-Symbol</small></div>`;
  h += `<div class="c">${G.side(D)}<small>Seitenansicht</small></div>`;
  h += `<div class="c">${G.marker(D, 1, '#aad3df')} ${G.marker(D, 1, '#e8e0d0')} ${G.marker(D, 0.5, '#1d2a3a')}<small>Karte, Originalgröße (hell, Land, dunkel; rechts 50 %)</small></div>`;
  h += `<div class="c"><div class="fill">` + FS.map(f => `<div>${G.svg(D, f, 58, 75, '0 0 100 130', '', {uid: 'f' + Math.round(f * 100), k: 1.2})}<br>${Math.round(f * 100)} %</div>`).join('') + `</div><small>Füllgrad</small></div>`;
  h += '</div>';
}
fs.writeFileSync('vorschlag2.html', h);
