import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F(); s=f.s
a=s.index("// Form der Hülle nach Füllgrad, in Einheiten des Radius der vollen Hülle."); b=s.index("const flagSVGmap")
new='''// Form der Hülle nach Füllgrad (Wahl des Nutzers 11.10.2026, „Version C“), in Einheiten des Radius der vollen Hülle.
// Bis 50 % Pilzform: oben volle Breite, unten zieht das Netz die Hülle schmal. Darunter wird sie auch oben schmaler (Faktor k, zuerst langsam)
// und geht unter 20 % in die schlaffe, flatternde Hülle über. q läuft von der Öffnung unten (0) zum Scheitel (1), w ist die halbe Breite, a das Maß für das Flattern.
function hullProf(f){ f = Math.max(0, Math.min(1, f == null ? 1 : f)); const bz = (a, b, c, d, t) => { const u = 1 - t; return u * u * u * a + 3 * u * u * t * b + 3 * u * t * t * c + t * t * t * d; };
  const s = Math.min(1, Math.pow(1 - Math.max(f, 0.5), 0.7) + (f < 0.5 ? (0.5 - f) * 0.5 : 0)), nw = 5 - 3.2 * s, k = f >= 0.5 ? 1 : 0.15 + 0.85 * Math.pow(Math.sin(Math.PI / 2 * Math.min(1, f / 0.5 * 1.15)), 0.9), amp = Math.pow(Math.max(0, Math.min(1, (0.3 - f) / 0.25)), 1.5), R = [];
  for (let i = 0; i <= 10; i++){ const t = i / 10; R.push([bz(0, 11, 18, 18, t), bz(2, 2, 10, 20, t)]); }
  for (let i = 1; i <= 12; i++){ const t = i / 12; R.push([bz(18, 18 - 15 * s, 12 - 9 * s, nw, t), bz(20, 28 - 2 * s, 34.5, 39, t)]); }
  return R.reverse().map(p => { const q = (39 - p[1]) / 37; return {q, w: Math.max(k * p[0], Math.min(p[0], 2.3)) / 18, a: amp * q}; }); }
const balloonSVG = (c, f) => { const P = hullProf(f), r = x => x.toFixed(1), side = (sg, k) => P.map(p => r(22 + Math.sin(p.q * 7 + 1) * 5 * p.a + sg * k * p.w * 18) + ' ' + r(39 - p.q * 37)), m = P[0].w * 18;
  return `<svg viewBox="0 0 44 54" width="44" height="54"><path d="M${side(-1, 1).join('L')}L${side(1, 1).reverse().join('L')}z" fill="${c}" stroke="#0a1019" stroke-width="2" stroke-linejoin="round"/><path d="M${side(-1, 0.45).join('L')}M${side(1, 0.45).join('L')}" fill="none" stroke="#0a1019" stroke-opacity=".35" stroke-width="1.6" stroke-linejoin="round"/><path d="M${r(22 - m)} 39L20 45M${r(22 + m)} 39L24 45" stroke="#eef3fa" stroke-width="1.4"/><rect x="18" y="45" width="8" height="6" rx="1.5" fill="#eef3fa" stroke="#0a1019" stroke-width="1.5"/></svg>`; };
'''
s=s[:a]+new+s[b:]; f.s=s
f.rep("HP = hullProf(fI, Lh / r, 24),","HP = hullProf(fI), nH = HP.length - 1,")
f.rep("g = HP[6];","g = HP[5];")
f.rep("SIDE.top = [hx(HP[24]), yT];","SIDE.top = [hx(HP[nH]), yT];")
f.rep("* (i === 24 ? 0 : 1);","* (i === nH ? 0 : 1);")
f.rep("for (let i = 23; i >= 0; i--){ const p = HP[i];","for (let i = nH - 1; i >= 0; i--){ const p = HP[i];")
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-11.5', de: ['Füllgrad an der Hülle ablesen: Bis 50 % wird der Ballon pilzförmig, oben breit und unten vom Netz schmal gezogen. Darunter wird er auch oben schmaler, unter 20 % hängt er als flatternde Hülle am Korb.'],
  en: ['Read the fill from the envelope: down to 50 % the balloon turns mushroom-shaped, wide at the top and pulled narrow by the net below. Under that it narrows at the top as well, below 20 % it hangs from the basket as a fluttering envelope.']},
""")
f.rep("const BUILD = '2026-10-11.4'","const BUILD = '2026-10-11.5'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v43'" in s; open(p,'w').write(s.replace("'v43'","'v44'"))
