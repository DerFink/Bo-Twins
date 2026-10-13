import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# Text
for a,b in [("Ein Team schied leider spontan aus.","Ein Team schied leider aus."),("Sadly, one team dropped out at short notice.","Sadly, one team dropped out."),("Une équipe a malheureusement dû renoncer au dernier moment.","Une équipe a malheureusement dû renoncer."),("Jedna załoga niestety wycofała się w ostatniej chwili.","Jedna załoga niestety się wycofała."),("Jeden tým bohužel na poslední chvíli odstoupil.","Jeden tým bohužel odstoupil."),("可惜有一隊臨時退出。","可惜有一隊退出了。"),("Por desgracia, un equipo se retiró a última hora.","Por desgracia, un equipo se retiró.")]: f.rep(a,b)
# OP-41: Durchmesser 100 m
f.rep("const ZONE_R = 100;                       // m, Radius der Landezone beim Zielfahren","const ZONE_R = 50;                        // m, Radius der Landezone beim Zielfahren: Kreis mit 100 m Durchmesser (Entscheidung Nutzer 09.10.2026)")
f.rep("Math.max(3 * ZONE_R, 0.2 * targetDist)","Math.max(300, 0.2 * targetDist)")
for a,b in [("ein Kreis mit 100 m Radius","ein Kreis mit 100 m Durchmesser"),("a circle of 100 m radius","a circle 100 m across"),("un cercle de 100 m de rayon","un cercle de 100 m de diamètre"),("koło o promieniu 100 m","koło o średnicy 100 m"),("kruh o poloměru 100 m","kruh o průměru 100 m"),("半徑 100 公尺的圓","直徑 100 公尺的圓"),("un círculo de 100 m de radio","un círculo de 100 m de diámetro")]:
    assert f.s.count(a)>=1,a; f.s=f.s.replace(a,b)
# OP-05: härter als 2,5 m/s = disqualifiziert
f.rep("const LAND_SOFT = 1.0, LAND_HARD = 2.9;","const LAND_DQ = 2.5;                      // m/s: härter aufgesetzt gilt als disqualifiziert (Entscheidung Nutzer 09.10.2026, OP-05)\nconst LAND_SOFT = 1.0, LAND_HARD = 2.9;")
f.rep("  const R = scoreRadius(targetDist), base =","  if (vLand > LAND_DQ) return 0;\n  const R = scoreRadius(targetDist), base =")
f.rep("  const ex = $('r-extra'); ex.textContent = '';","  if (k !== 'gb' && pts != null && B.vLand > LAND_DQ){ pts = 0; $('r-head').textContent = tr('gb_dq_head') + ': ' + tr('gb_dq_hard'); }   // OP-05\n  const ex = $('r-extra'); ex.textContent = '';")
f.rep("  if (!GB.dq && !gbOnLand(p[0], p[1])) GB.dq = 'water';","  if (!GB.dq && !gbOnLand(p[0], p[1])) GB.dq = 'water';\n  if (!GB.dq && B.vLand > LAND_DQ) GB.dq = 'hard';")
HARD=['härter als 2,5 m/s gelandet','landed harder than 2.5 m/s','atterrissage à plus de 2,5 m/s','lądowanie twardsze niż 2,5 m/s','přistání tvrdší než 2,5 m/s','落地速度超過 2.5 m/s','aterrizaje a más de 2,5 m/s']
RANK=['Platz jetzt','Rank now','Rang actuel','Miejsce teraz','Pořadí teď','目前名次','Puesto ahora']
PRIV=[' Der Name wird ausschließlich für die Bestenliste verwendet und dort gespeichert.',' The name is used only for the high scores and stored there.',' Le nom sert uniquement au classement et y est enregistré.',' Imię służy wyłącznie do tabeli wyników i tam jest zapisywane.',' Jméno se používá výhradně pro tabulku výsledků a ukládá se tam.','名字只用於排行榜，並儲存在那裡。',' El nombre se usa únicamente para la clasificación y se guarda allí.']
pos=[m.start() for m in re.finditer(r"gb_story:'",f.s)]; assert len(pos)==7
for p,i in sorted(zip(pos,range(7)),reverse=True): f.s=f.s[:p]+"gb_dq_hard:'%s', gb_ranknow:'%s', "%(HARD[i],RANK[i])+f.s[p:]
ms=list(re.finditer(r"name_hint:'([^']*)'",f.s)); assert len(ms)==7
for m,i in sorted(zip(ms,range(7)),key=lambda x:-x[0].start()): f.s=f.s[:m.end()-1]+PRIV[i]+f.s[m.end()-1:]
# Platz jetzt
f.rep('''        <div class="kv" id="row-zone" hidden>''','''        <div class="kv" id="row-rank" hidden><span data-i="gb_ranknow"></span><b id="i-rank">–</b></div>
        <div class="kv" id="row-zone" hidden>''')
f.rep("  { const z = k === 'gb' && GB.zone != null","  { const z = k === 'gb' && STATE === 'play' && B.go; $('row-rank').hidden = !z; if (z) $('i-rank').textContent = (GB_TEAMS.filter(t => t[2] > gbKm()).length + 1) + ' / ' + (GB_TEAMS.length + 1); }\n  { const z = k === 'gb' && GB.zone != null")
f.rep("#row-wet[hidden]","#row-rank[hidden],#row-wet[hidden]") if f.s.count("#row-wet[hidden]")==1 else None
# Sperrzone: Abstand von 10 km plus 1 km Reserve als roter Streifen um die Grenzen
f.rep("  GB_TEAMS.forEach((t, i) => {\n    add(L.circleMarker","  GB.strips = [];                                                               // Streifen entlang der Grenzen: 10 km Abstand und 1 km Reserve, Breite je nach Zoom und Breitengrad\n  (GB.ban || []).forEach(P => { if (P.box[3] < 30 || P.box[1] > 75 || P.box[2] < -15 || P.box[0] > 65) return; P.rings.forEach(r => { for (let i = 0; i < r.length - 1; i += 60){ const seg = r.slice(i, i + 61); if (i + 61 >= r.length) seg.push(r[0]); const lat = seg.reduce((s, p) => s + p[1], 0) / seg.length; if (lat < 30 || lat > 75) continue; GB.strips.push({lat, ln: add(L.polyline(seg.map(p => [p[1], p[0]]), {renderer: GB.rend, color: '#ff3b30', opacity: .22, weight: 2, lineCap: 'round', lineJoin: 'round', interactive: false}))}); } }); });\n  gbStrips();\n  GB_TEAMS.forEach((t, i) => {\n    add(L.circleMarker")
f.rep("function gbUndraw(){","function gbStrips(){ if (!GB.strips || !GB.strips.length) return; const z = map.getZoom(); GB.strips.forEach(s => s.ln.setStyle({weight: Math.max(2, 2 * (GB.buffer + GB.margin) / (156543.03392 * Math.cos(s.lat * Math.PI / 180) / Math.pow(2, z)))})); }\nmap.on('zoomend', gbStrips);\nfunction gbUndraw(){ GB.strips = [];")
f.rep("  buffer: 10000,","  margin: 1000,                                                                   // m, um so viel breiter ist der rote Streifen gezeichnet, als die Regel verlangt\n  buffer: 10000,")
f.rep("const BUILD = '2026-10-09.7'","const BUILD = '2026-10-09.8'")
f.save()
s=open('/mnt/user-data/outputs/spiel/sw.js').read(); assert "'v29'" in s; open('/mnt/user-data/outputs/spiel/sw.js','w').write(s.replace("'v29'","'v30'"))
