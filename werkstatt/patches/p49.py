import sys
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add
f=F(); s=f.s
NEW=open('/tmp/claude-0/b2/bal.js').read()
a=s.index("const balloonSVG = (c, f) =>"); b=s.index("const flagSVGmap")
s=s[:a]+NEW+s[b:]
s=s.replace("iconSize: [44, 54], iconAnchor: [22, 51]","iconSize: [44, 57], iconAnchor: [22, 48]")
f.s=s
# ---- Seitenansicht ----
a=f.s.index("  { const yM = yBask - bh - 0.55 * r * Math.sqrt(fI),"); b=f.s.index("  // Schlepptau: hängt bis zum Boden")
f.s=f.s[:a]+"""  { const sc = r / 36; SIDE.top = balDraw(c, fI, performance.now() / 1000 * 11, bx, yBask, sc); }          // Zeichnung wie Kartensymbol und App-Symbol (Entwurf B2)
"""+f.s[b:]
f.rep("const fI = fillNow(), Dm = Math.cbrt(6 * CFG.vol / Math.PI), r = Math.max(9, Dm * m / 2), yBask = yOf(B.h), bh = Math.max(4, 1.3 * m), bw = Math.max(5, 1.5 * m), cy = yBask - bh - r * 1.55;",
      "const fI = fillNow(), Dm = Math.cbrt(6 * CFG.vol / Math.PI), r = Math.max(9, Dm * m / 2), yBask = yOf(B.h), bh = r / 36 * 10, bw = r / 36 * 13;")
# ---- Startseite ----
f.rep("""    c.strokeStyle = '#c9d6e8'; c.lineWidth = 1.2; c.beginPath(); c.moveTo(bx - r * 0.72, cy + r * 0.7); c.lineTo(bx - bw / 2, yb - bh); c.moveTo(bx + r * 0.72, cy + r * 0.7); c.lineTo(bx + bw / 2, yb - bh); c.stroke();
    c.fillStyle = '#f4f1ea'; c.beginPath(); c.arc(bx, cy, r, 0, 7); c.fill(); c.strokeStyle = '#d2cdc0'; c.lineWidth = 1.2; c.beginPath(); c.ellipse(bx, cy, r * 0.42, r, 0, 0, 7); c.stroke();
    c.fillStyle = '#b98a4a'; c.fillRect(bx - bw / 2, yb - bh, bw, bh);""","""    balDraw(c, 1, 0, bx, yb, r / 36);                                                // Zeichnung wie Karte und Seitenansicht (Entwurf B2)""")
f.rep("const gB = gy(bx), yb = gB - h * m, r = Math.max(13, 6.2 * m * 2.1), bw = r * 0.48, bh = r * 0.36, cy = yb - bh - r * 1.5;",
      "const gB = gy(bx), yb = gB - h * m, r = Math.max(13, 6.2 * m * 2.1), bw = r / 36 * 13, bh = r / 36 * 10, cy = yb - r / 36 * 72;")
# ---- Logo oben links ----
f.rep("""        <svg width="22" height="28" viewBox="0 0 44 54" aria-hidden="true"><path d="M22 2C11 2 4 10 4 20c0 8 6 14.5 13 19h10c7-4.5 13-11 13-19C40 10 33 2 22 2z" fill="#ff9f1c"/><path d="M17 39l3 6M27 39l-3 6" stroke="#eef3fa" stroke-width="2"/><rect x="18" y="45" width="8" height="6" rx="1.5" fill="#eef3fa"/></svg>""",
      """        <span id="brand-bal" aria-hidden="true"></span>""")
f.rep("const balMk = L.marker(","$('brand-bal').innerHTML = balloonSVG('', 1, {w: 24, k: 2.4});\nconst balMk = L.marker(")
f.rep("\n.brand{min-width:0;","\n#brand-bal{display:inline-flex;line-height:0}\n.brand{min-width:0;")
# ---- Was ist neu: nach einem Update nur ein Satz; Schließen-Knopf bleibt sichtbar ----
f.rep("if (seen !== BUILD && NEWS[0].b === BUILD && STATE === 'menu') newsOpen(); }   // nach einem Update einmal von selbst zeigen; bei der ersten Nutzung nicht",
      "if (seen !== BUILD && STATE === 'menu'){ store.set('gb-news', BUILD); toast(tr('upd_done')); } }   // nach einem Update nur ein Satz (Wunsch Nutzer 26.10.2026); die Liste unter „Was ist neu“")
f.rep("#news .card{width:min(480px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px;background:#0d1626}",
      "#news .card{width:min(480px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px 14px 0;background:#0d1626}\n#nw-close{position:sticky;bottom:0;margin:8px 0 0;box-shadow:0 -10px 14px #0d1626}\n#news .card::after{content:'';display:block;height:12px}")
tx_add(f,{'upd_done':['Die App wurde aktualisiert, Neues steht unter „Was ist neu“.','The app was updated; see “What’s new”.','L’application a été mise à jour, voir « Nouveautés ».','Aplikacja została zaktualizowana, szczegóły w „Co nowego”.','Aplikace byla aktualizována, novinky najdeš v „Co je nového“.','App 已更新，詳見「新功能」。','La app se ha actualizado; mira «Novedades».']})
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-26.4', de: ['Neues Ballonbild: silberne Hülle mit orangem Netz, Ventil, Füllansatz, Lastring und Korb mit Sandsäcken. Dieselbe Zeichnung im App-Symbol, auf der Karte, in der Seitenansicht und auf der Startseite.', 'Nach einem Update erscheint nur noch ein kurzer Hinweis statt dieser Liste. In der Liste bleibt der Knopf „Schließen“ immer sichtbar.'],
  en: ['New balloon picture: silver envelope with orange net, valve, appendix, load ring and basket with sandbags. The same drawing in the app icon, on the map, in the side view and on the start page.', 'After an update only a short note appears instead of this list. In the list the “Close” button always stays visible.']},
""")
f.rep("const BUILD = '2026-10-26.3'","const BUILD = '2026-10-26.4'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; t=open(p).read(); assert "'v50'" in t; open(p,'w').write(t.replace("'v50'","'v51'"))
print('ok')
