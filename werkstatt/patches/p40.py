import sys,re,json
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
s=f.s
# ---- Hülle: ein stetiger Übergang von der vollen Kugel zur schlaffen, flatternden Hülle (STE-29) ----
a=s.index("const balloonSVG = (c, f) =>"); b=s.index("const flagSVGmap")
new='''// Form der Hülle nach Füllgrad, in Einheiten des Radius der vollen Hülle. Das Gas sammelt sich oben in einer Blase (Radius rb), darunter hängt der Stoff
// als Schlauch (halbe Breite wt). q läuft von der Öffnung unten (0) zum Scheitel (1), w ist die halbe Breite, a das Maß für das Flattern (ab 45 % abwärts).
function hullProf(f, Lr, n){ f = Math.max(0, Math.min(1, f == null ? 1 : f)); const wt = 0.21, rb = wt + (1 - wt) * Math.pow(f, 0.55), qc = Math.max(0.05, 1 - rb / Lr), p = 0.9 + 5 * (1 - f), amp = Math.pow(Math.max(0, Math.min(1, (0.45 - f) / 0.37)), 1.5), out = [];
  for (let i = 0; i <= n; i++){ const q = i / n, x = (q - qc) / (1 - qc); out.push({q, w: q >= qc ? rb * Math.sqrt(Math.max(0, 1 - x * x)) : wt + (rb - wt) * Math.pow(Math.sin(Math.PI / 2 * q / qc), p), a: amp * q}); }
  return out; }
const balloonSVG = (c, f) => { const P = hullProf(f, 37 / 18, 16), r = x => x.toFixed(1), side = (sg, k) => P.map(p => r(22 + Math.sin(p.q * 7 + 1) * 5 * p.a + sg * k * p.w * 18) + ' ' + r(39 - p.q * 37)), m = 0.21 * 18;
  return `<svg viewBox="0 0 44 54" width="44" height="54"><path d="M${side(-1, 1).join('L')}L${side(1, 1).reverse().join('L')}z" fill="${c}" stroke="#0a1019" stroke-width="2" stroke-linejoin="round"/><path d="M${side(-1, 0.45).join('L')}M${side(1, 0.45).join('L')}" fill="none" stroke="#0a1019" stroke-opacity=".35" stroke-width="1.6" stroke-linejoin="round"/><path d="M${r(22 - m)} 39L20 45M${r(22 + m)} 39L24 45" stroke="#eef3fa" stroke-width="1.4"/><rect x="18" y="45" width="8" height="6" rx="1.5" fill="#eef3fa" stroke="#0a1019" stroke-width="1.5"/></svg>`; };
'''
s=s[:a]+new+s[b:]
a=s.index("  if (fI < 0.08){                                                             // fast leer"); b=s.index("  c.fillStyle = '#b98a4a'; c.fillRect(bx - bw / 2, yBask - bh, bw, bh);")
new='''  { const yM = yBask - bh - 0.55 * r * Math.sqrt(fI), yT = yBask - bh - 2.55 * r, Lh = yM - yT, tt = performance.now() / 1000, HP = hullProf(fI, Lh / r, 24), hx = p => bx + Math.sin(tt * 11 + p.q * 7) * r * 0.28 * p.a, hy = p => yM - p.q * Lh, g = HP[6];
    SIDE.top = [hx(HP[24]), yT];                                                // Scheitel mit dem Ventil: dort tritt das Gas aus
    c.strokeStyle = '#c9d6e8'; c.lineWidth = 1; c.beginPath(); c.moveTo(hx(g) - g.w * r * 0.9, hy(g)); c.lineTo(bx - bw / 2, yBask - bh); c.moveTo(hx(g) + g.w * r * 0.9, hy(g)); c.lineTo(bx + bw / 2, yBask - bh); c.stroke();
    c.fillStyle = '#f4f1ea'; c.strokeStyle = '#0a1019'; c.lineWidth = 1.2; c.lineJoin = 'round'; c.beginPath(); HP.forEach((p, i) => { const X = hx(p) - Math.max(1.5, p.w * r) * (i === 24 ? 0 : 1); i ? c.lineTo(X, hy(p)) : c.moveTo(X, hy(p)); });
    for (let i = 23; i >= 0; i--){ const p = HP[i]; c.lineTo(hx(p) + Math.max(1.5, p.w * r), hy(p)); } c.closePath(); c.fill(); c.stroke(); }
'''
s=s[:a]+new+s[b:]
old="  if (fI >= 0.08) SIDE.puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,' + (0.9 - p.t / 1.6).toFixed(2) + ')'; c.lineWidth = 1.4; c.beginPath(); c.arc(bx + p.x * (1 + p.t * 2), cy - r - 3 - p.t * 14 * p.s,"
assert old in s
s=s.replace(old,"  SIDE.puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,' + (0.9 - p.t / 1.6).toFixed(2) + ')'; c.lineWidth = 1.4; c.beginPath(); c.arc(SIDE.top[0] + p.x * (1 + p.t * 2), SIDE.top[1] - 3 - p.t * 14 * p.s,")
# ---- Vorschau „KI-optimiert“: neue Route entlang der Siegerspur über die Ostsee nach Finnland ----
m=re.search(r"const GB_ROUTES = (\{.*\});\n",s); R=json.loads(m.group(1)); j=json.load(open('/home/claude/w/route_y1.json')); R['max']={'km':round(j['km'],1),'log':j['log']}
s=s[:m.start(1)]+json.dumps(R,separators=(',',':'))+s[m.end(1):]
f.s=s
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-11.3', de: ['Die Hülle wird mit sinkendem Füllgrad gleichmäßig schmaler, auch oben, und beginnt unter etwa 45 % zu flattern. Der Übergang zur schlaffen Hülle kommt nicht mehr plötzlich.', 'Meisterschaft, Vorflug „KI-optimiert“: neue Route tief über die Ostsee bis nach Finnland.'],
  en: ['The envelope now narrows evenly as the fill drops, at the top as well, and starts to flutter below about 45 %. The change to the limp envelope is no longer sudden.', 'Championship, pre-flight “AI-optimised”: new route low across the Baltic Sea to Finland.']},
""")
f.rep("const BUILD = '2026-10-11.2'","const BUILD = '2026-10-11.3'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v41'" in s; open(p,'w').write(s.replace("'v41'","'v42'"))
