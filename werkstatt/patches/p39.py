import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---- Was ist neu: Knopf unten neben „Neueste Version laden“; Wetterpaket ausgeblendet ----
f.rep('<button class="sm" id="in-btn" data-i="in_title"></button><button class="sm" id="nw-btn" data-i="news_title"></button>','<button class="sm" id="in-btn" data-i="in_title"></button>')
f.rep('<button class="sm" id="reload" data-i="reload"></button> <button class="sm" id="inst-set"','<button class="sm" id="reload" data-i="reload"></button> <button class="sm" id="nw-btn" data-i="news_title"></button> <button class="sm" id="inst-set"')
f.rep('    <p class="note"><button class="sm" id="wxp-btn" data-i="wxp_btn"></button> <span id="wxp-info"></span></p>','    <p class="note" hidden><button class="sm" id="wxp-btn" data-i="wxp_btn"></button> <span id="wxp-info"></span></p>   <!-- Wetterpaket für die Routenrechnung: ausgeblendet (Vorgabe Nutzer 11.10.2026), die Funktion bleibt erhalten -->')
# ---- Standort: Wetter für einen auf rund 1 km gerundeten Ort (REC-04) ----
f.rep("'/v1/forecast?latitude=' + lat.toFixed(4) + '&longitude=' + lon.toFixed(4) +","'/v1/forecast?latitude=' + lat.toFixed(2) + '&longitude=' + lon.toFixed(2) +   // auf zwei Nachkommastellen gerundet, rund 1 km: Der genaue Standort verlässt das Gerät dafür nicht (REC-04)\n   ")
# ---- Füllgrad nahe null: die Hülle hängt als schlaffe, flatternde Wurst (STE-29) ----
f.rep("  return `<svg viewBox=\"0 0 44 54\" width=\"44\" height=\"54\"><path d=\"M4 20C4 10 11 2 22 2C33 2 40 10 40 20C","  if ((f == null ? 1 : f) < 0.08) return `<svg viewBox=\"0 0 44 54\" width=\"44\" height=\"54\"><path d=\"M19 4C13 11 26 15 19.5 23C14.5 30 25 33 20.5 39L23.5 39C29 33 18.5 30 24.5 23C31 15 18 11 24 4z\" fill=\"${c}\" stroke=\"#0a1019\" stroke-width=\"2\" stroke-linejoin=\"round\"/><path d=\"M20.5 39L20 45M23.5 39L24 45\" stroke=\"#eef3fa\" stroke-width=\"1.4\"/><rect x=\"18\" y=\"45\" width=\"8\" height=\"6\" rx=\"1.5\" fill=\"#eef3fa\" stroke=\"#0a1019\" stroke-width=\"1.5\"/></svg>`;\n  return `<svg viewBox=\"0 0 44 54\" width=\"44\" height=\"54\"><path d=\"M4 20C4 10 11 2 22 2C33 2 40 10 40 20C")
a=f.s.index("  c.strokeStyle = '#c9d6e8'; c.lineWidth = 1; c.beginPath(); c.moveTo(bx - r * 0.72, cy + r * 0.7); c.lineTo(bx - bw / 2, yBask - bh);"); b=f.s.index("  c.fillStyle = '#b98a4a'; c.fillRect(bx - bw / 2, yBask - bh, bw, bh); c.strokeRect(",a)
old=f.s[a:b]
f.s=f.s[:a]+"  if (fI < 0.08){                                                             // fast leer: eine schlaffe Wurst, die im Fahrtwind flattert\n    const tt = performance.now() / 1000, pts = []; for (let i = 0; i <= 12; i++){ const q = i / 12; pts.push([bx + Math.sin(tt * 11 + q * 7) * r * 0.28 * q, yBask - bh - q * r * 2.5]); }\n    c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = '#0a1019'; c.lineWidth = Math.max(5, r * 0.42) + 2.4; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke();\n    c.strokeStyle = '#f4f1ea'; c.lineWidth = Math.max(5, r * 0.42); c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke(); c.lineCap = 'butt';\n  } else {\n"+old+"  }\n"+f.s[b:]
f.rep("  SIDE.puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,'","  if (fI >= 0.08) SIDE.puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,'")
# ---- Meisterschaft: rote Randstreifen nur in der Nähe des Ballons zeichnen (flüssigere Karte, NFA-01) ----
a=f.s.index("  GB.strips = [];                                                               // Streifen entlang der Grenzen"); b=f.s.index("  gbStrips();\n  GB_TEAMS.forEach(",a)
f.s=f.s[:a]+"""  GB.strips = []; GB.segs = [];                                                 // Streifen entlang der Grenzen: 10 km Abstand, Breite je nach Zoom und Breitengrad
  (GB.ban || []).forEach(P => { if (P.box[3] < 30 || P.box[1] > 83 || P.box[2] < -15 || P.box[0] > 70) return; P.rings.forEach(r => { for (let i = 0; i < r.length - 1; i += 60){ const seg = r.slice(i, i + 61); if (i + 61 >= r.length) seg.push(r[0]); const lat = seg.reduce((s, p) => s + p[1], 0) / seg.length, lon = seg.reduce((s, p) => s + p[0], 0) / seg.length; if (lat < 30 || lat > 83) continue; if (seg[0][0] > 75 && seg[seg.length - 1][0] > 75) continue; GB.segs.push({lat, lon, pts: seg.map(p => [p[1], p[0]]), ln: null}); } }); });
  gbNear();
"""+f.s[b:]
f.rep("function gbStrips(){ if (!GB.strips || !GB.strips.length) return;","""/* Nur die Streifen im Umkreis von 450 km um den Ballon liegen auf der Karte. Die sehr breiten Linien aller Grenzen bei jedem Bild neu zu zeichnen, ließ die Karte ruckeln. */
function gbNear(){
  if (!GB.segs) return; const p = (typeof B !== 'undefined' && B && STATE !== 'menu') ? gbPos() : [GB.start.lat, GB.start.lon], kx = Math.cos(p[0] * Math.PI / 180); let ch = false;
  GB.segs.forEach(s => { const near = Math.hypot((s.lat - p[0]) * 111.3, (s.lon - p[1]) * 111.3 * kx) < 450;
    if (near && !s.ln){ s.ln = L.polyline(s.pts, {renderer: GB.rend, color: '#ff3b30', opacity: .22, weight: 2, lineCap: 'round', lineJoin: 'round', interactive: false}).addTo(map); GB.layers.push(s.ln); ch = true; }
    else if (!near && s.ln){ map.removeLayer(s.ln); GB.layers = GB.layers.filter(x => x !== s.ln); s.ln = null; ch = true; } });
  GB.strips = GB.segs.filter(s => s.ln); if (ch) gbStrips();
}
function gbStrips(){ if (!GB.strips || !GB.strips.length) return;""")
f.rep("function gbUndraw(){ GB.strips = [];","function gbUndraw(){ GB.strips = []; GB.segs = null;")
f.rep("function gbAnchor(){\n  const p = gbPos(), de = B.e, dn = B.n;","function gbAnchor(){\n  const p = gbPos(), de = B.e, dn = B.n; GB.nearN = (GB.nearN || 0) + 1; if (GB.nearN % 3 === 0) setTimeout(gbNear, 0);   // alle 60 km die Randstreifen nachziehen")
# ---- Zielfahren: Das Startfenster kommt sofort; der Ort des Ziels wird im Hintergrund gesucht (NFA-03) ----
f.rep("async function placeTarget(){\n  for (let attempt = 0; attempt < 2; attempt++){","const PLACE = {run: 0};\nasync function placeTarget(still){                         // still(): gilt die Suche noch? Wenn der Spieler schon losgefahren ist, bleibt das Ziel, wie es ist\n  for (let attempt = 0; attempt < 2; attempt++){")
f.rep("    try{ els = await osmFetch(p[0], p[1], rP); }catch(e){ TARGET.place = {kind: 'zone', name: null, unchecked: true}; return; }","    try{ els = await osmFetch(p[0], p[1], rP); }catch(e){ if (still && !still()) return false; TARGET.place = {kind: 'zone', name: null, unchecked: true}; return true; }\n    if (still && !still()) return false;")
f.rep("    TARGET.place = {kind: r.kind, name: r.name, unchecked: !r.clear};\n    return;\n  }\n}","    TARGET.place = {kind: r.kind, name: r.name, unchecked: !r.clear};\n    return true;\n  }\n  return true;\n}")
f.rep("      if (TARGET){ busy(tr('busy_place')); await placeTarget(); }","      if (TARGET){ TARGET.place = {kind: 'zone', name: null, unchecked: true, pending: true}; const run = ++PLACE.run, still = () => run === PLACE.run && STATE === 'brief' && !!TARGET;\n        placeTarget(still).then(ok => { if (ok && still()){ drawGoals(); showStart(); } else if (TARGET && TARGET.place && TARGET.place.pending) TARGET.place.pending = false; }); }")
f.rep("(TARGET.place && TARGET.place.unchecked ? ' ' + tr('sw_unchecked') : '')","(TARGET.place && TARGET.place.pending ? ' ' + tr('busy_place') : TARGET.place && TARGET.place.unchecked ? ' ' + tr('sw_unchecked') : '')")
f.rep("function resetRun(){\n","function resetRun(){\n  if (typeof PLACE !== 'undefined') PLACE.run++;\n")
# ---- Was ist neu ----
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-11.2', de: ['Zielfahren startet schneller: Das Startfenster erscheint sofort, der Ort des Ziels wird währenddessen gesucht.', 'Meisterschaft: Die Karte läuft flüssiger, weil nur noch die Sperrzonen in der Nähe gezeichnet werden.', 'Ein fast leerer Ballon hängt jetzt als flatternde Hülle am Korb, auf der Karte und in der Seitenansicht.', 'Der Wetterdienst erhält den Standort nur noch auf rund 1 km gerundet.', '„Was ist neu“ steht jetzt unten in den Einstellungen neben „Neueste Version laden“.'],
  en: ['Target flight starts faster: the start window appears at once while the place of the target is being looked up.', 'Championship: the map runs more smoothly because only the no-fly zones nearby are drawn.', 'An almost empty balloon now hangs as a fluttering envelope from the basket, on the map and in the side view.', 'The weather service now receives the location rounded to about 1 km.', '“What’s new” is now at the bottom of the settings next to “Load newest version”.']},
""")
f.rep("const BUILD = '2026-10-11.1'","const BUILD = '2026-10-11.2'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v40'" in s; open(p,'w').write(s.replace("'v40'","'v41'"))
