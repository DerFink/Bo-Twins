import re,sys,json
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- Text der Meisterschaft ----------
ST={'de':("Als 25. Team tritt spontan Jamaika an: die CoolRidings, und das bist du.","Ein Team schied leider spontan aus. Spontan nimmt jetzt noch ein 25. Team teil, das bist du."),
'en':("Jamaica enters spontaneously as the 25th team: the CoolRidings, and that is you.","Sadly, one team dropped out at short notice. Now a 25th team joins spontaneously, and that is you."),
'fr':("La Jamaïque s’inscrit à l’improviste comme 25e équipe : les CoolRidings, c’est vous.","Une équipe a malheureusement dû renoncer au dernier moment. Une 25e équipe s’inscrit maintenant à l’improviste : c’est vous."),
'pl':("Jako 25. załoga spontanicznie startuje Jamajka: CoolRidings, czyli ty.","Jedna załoga niestety wycofała się w ostatniej chwili. Teraz spontanicznie dołącza 25. załoga, czyli ty."),
'cs':("Jako 25. tým se spontánně hlásí Jamajka: CoolRidings, a to jste vy.","Jeden tým bohužel na poslední chvíli odstoupil. Nyní se spontánně přidává 25. tým, a to jste vy."),
'zh':("牙買加臨時報名成為第 25 隊：CoolRidings，也就是你。","可惜有一隊臨時退出。現在又有第 25 隊臨時加入，那就是你。"),
'es':("Jamaica se inscribe a última hora como equipo 25: los CoolRidings, y ese eres tú.","Por desgracia, un equipo se retiró a última hora. Ahora se suma de improviso un equipo 25, y ese eres tú.")}
for a,b in ST.values(): f.rep(a,b)
# ---------- Vorschau-Routen ----------
R={}
for k,fn in (('max','route_m3d.json'),('kons','route_kons.json')):
    j=json.load(open('/home/claude/w/'+fn)); R[k]={'km':round(j['km'],1),'log':j['log']}
routes='/* Vorschau der Meisterschaft (MEI-11): zwei einmal gerechnete Fahrten mit der Physik des Spiels und dem Wetter des Rennens, als feste Spuren.\n   Je 10 Minuten: Zeit s, Breite, Länge, Höhe m NN, Gelände m, Sand kg, Gas %, Steigen m/s. Erzeugt mit gbroute.js (nicht Teil der App). */\nconst GB_ROUTES = '+json.dumps(R,separators=(',',':'))+';\n'
TXN={'de':dict(pv_title:='Vorschau',pv_max='KI-optimiert',pv_kons='Konservativ',pv_lbl='Vorflug ansehen',pv_head='{name}: {km} km in {h} h',pv_read='{t} · {clk} · {alt} m NN ({agl} m über Grund) · {w} m/s · Sand {sand} kg · Gas {gas} % · {km} km',pv_leg='Orange: Höhe. Grau: Gelände. Gelb: Sand. Blau: Gas. Gerechnet mit der Physik des Spiels und dem Wetter des Rennens; beim Nachfahren kommt es auf jede Minute an.',pv_warn='Achtung: Mit den genauen Grenzen kommt diese Route der Sperrzone auf {km} km nahe.')} if False else {}
TXN={
'de':{'pv_max':'KI-optimiert','pv_kons':'Konservativ','pv_lbl':'Vorflug ansehen','pv_head':'{name}: {km} km in {h} h','pv_read':'{t} · {clk} · {alt} m NN ({agl} m über Grund) · {w} m/s · Sand {sand} kg · Gas {gas} % · {km} km','pv_leg':'Orange: Höhe. Grau: Gelände. Gelb: Sand. Blau: Gas. Einmal gerechnet mit der Physik des Spiels und dem Wetter des Rennens.','pv_warn':'Achtung: Mit den genauen Grenzen kommt diese Route der Sperrzone bis auf {km} km nahe.'},
'en':{'pv_max':'AI-optimised','pv_kons':'Conservative','pv_lbl':'Watch a pre-flight','pv_head':'{name}: {km} km in {h} h','pv_read':'{t} · {clk} · {alt} m AMSL ({agl} m above ground) · {w} m/s · sand {sand} kg · gas {gas} % · {km} km','pv_leg':'Orange: altitude. Grey: terrain. Yellow: sand. Blue: gas. Computed once with the game physics and the weather of the race.','pv_warn':'Caution: with the exact borders this route comes within {km} km of the no-fly zone.'},
'fr':{'pv_max':'Optimisé par IA','pv_kons':'Prudent','pv_lbl':'Voir un vol de démonstration','pv_head':'{name} : {km} km en {h} h','pv_read':'{t} · {clk} · {alt} m AMSL ({agl} m sol) · {w} m/s · sable {sand} kg · gaz {gas} % · {km} km','pv_leg':'Orange : altitude. Gris : relief. Jaune : sable. Bleu : gaz. Calculé une fois avec la physique du jeu et la météo de la course.','pv_warn':'Attention : avec les frontières exactes, cette route s’approche à {km} km de la zone interdite.'},
'pl':{'pv_max':'Zoptymalizowana przez AI','pv_kons':'Zachowawcza','pv_lbl':'Zobacz przelot pokazowy','pv_head':'{name}: {km} km w {h} h','pv_read':'{t} · {clk} · {alt} m n.p.m. ({agl} m nad ziemią) · {w} m/s · piasek {sand} kg · gaz {gas} % · {km} km','pv_leg':'Pomarańczowy: wysokość. Szary: teren. Żółty: piasek. Niebieski: gaz. Obliczone raz z fizyką gry i pogodą wyścigu.','pv_warn':'Uwaga: przy dokładnych granicach ta trasa zbliża się do strefy zakazanej na {km} km.'},
'cs':{'pv_max':'Optimalizováno AI','pv_kons':'Opatrná','pv_lbl':'Zhlédnout předlet','pv_head':'{name}: {km} km za {h} h','pv_read':'{t} · {clk} · {alt} m n. m. ({agl} m nad zemí) · {w} m/s · písek {sand} kg · plyn {gas} % · {km} km','pv_leg':'Oranžová: výška. Šedá: terén. Žlutá: písek. Modrá: plyn. Spočítáno jednou s fyzikou hry a počasím závodu.','pv_warn':'Pozor: s přesnými hranicemi se tato trasa blíží k zakázané zóně na {km} km.'},
'zh':{'pv_max':'AI 最佳化','pv_kons':'保守','pv_lbl':'觀看示範飛行','pv_head':'{name}：{km} 公里，{h} 小時','pv_read':'{t} · {clk} · 海拔 {alt} m（離地 {agl} m）· {w} m/s · 沙 {sand} kg · 氣體 {gas} % · {km} km','pv_leg':'橘：高度。灰：地形。黃：沙。藍：氣體。以遊戲的物理與比賽當時的天氣計算一次。','pv_warn':'注意：以精確邊界計算，此路線距禁區僅 {km} 公里。'},
'es':{'pv_max':'Optimizada por IA','pv_kons':'Conservadora','pv_lbl':'Ver un vuelo de muestra','pv_head':'{name}: {km} km en {h} h','pv_read':'{t} · {clk} · {alt} m s. n. m. ({agl} m sobre el suelo) · {w} m/s · arena {sand} kg · gas {gas} % · {km} km','pv_leg':'Naranja: altitud. Gris: terreno. Amarillo: arena. Azul: gas. Calculada una vez con la física del juego y el tiempo de la carrera.','pv_warn':'Atención: con las fronteras exactas, esta ruta se acerca a {km} km de la zona prohibida.'}}
pos=[m.start() for m in re.finditer(r"gb_story:'",f.s)]; assert len(pos)==7
for p,lang in sorted(zip(pos,['de','en','fr','pl','cs','zh','es']),reverse=True):
    add=''.join("%s:'%s', "%(k,v.replace("'","\\'")) for k,v in TXN[lang].items()); f.s=f.s[:p]+add+f.s[p:]
# ---------- Oberfläche ----------
f.rep('''        <p class="note" id="sw-note"></p>
        <button class="pri" id="sw-go" data-i="sw_go"></button>''','''        <p class="note" id="sw-note"></p>
        <div id="sw-pv" hidden><span data-i="pv_lbl"></span><div class="seg wide"><button data-pv="max"></button><button data-pv="kons"></button></div></div>
        <button class="pri" id="sw-go" data-i="sw_go"></button>''')
f.rep('    <!-- Buy me a Beer:','''    <!-- Vorflug: eine gerechnete Route der Meisterschaft auf der Karte abspielen -->
    <div class="card" id="pv" hidden>
      <div class="pvh"><b id="pv-head"></b><button class="sm" id="pv-close" data-i="close"></button></div>
      <canvas id="pv-cv"></canvas>
      <div class="pvc"><button class="sm" id="pv-play" aria-label="Play"></button><input type="range" id="pv-pos" min="0" max="1000" value="0"></div>
      <p id="pv-read"></p>
      <p class="note" id="pv-leg"></p>
    </div>

    <!-- Buy me a Beer:''')
f.rep('#review{z-index:880}','''#sw-pv{margin-top:10px;font-size:13px;color:var(--mut,#9aabc4)}
#sw-pv[hidden],#pv[hidden]{display:none}
#sw-pv .seg{margin-top:5px}
#sw-pv .seg button{min-height:38px;font-size:13px}
#pv{position:absolute;left:6px;right:6px;bottom:6px;z-index:870;padding:9px 11px 8px;background:#0d1626;max-width:560px;margin:0 auto}
#pv .pvh{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:14px}
#pv-cv{display:block;width:100%;height:120px;margin:6px 0 4px;touch-action:none}
#pv .pvc{display:flex;align-items:center;gap:8px}
#pv-play{min-width:44px;min-height:36px;font-size:15px}
#pv-pos{flex:1;min-width:0;height:30px;accent-color:var(--orb)}
#pv-read{margin:5px 0 3px;font-family:var(--num);font-size:14.5px;line-height:1.3}
#pv .note{margin:0;font-size:11.5px}
#review{z-index:880}''')
f.rep("  $('sw-note').textContent = B.ok ?","  $('sw-pv').hidden = k !== 'gb'; document.querySelectorAll('#sw-pv button').forEach(b => { const r = GB_ROUTES[b.dataset.pv]; b.textContent = tr('pv_' + b.dataset.pv) + ' · ' + nf(r.km, 0) + ' km'; });\n  $('sw-note').textContent = B.ok ?")
js=routes+'''/* Vorflug (MEI-14): die Route auf der Karte abspielen, mit Höhe, Sand und Gas über der Zeit */
const PV = {r: null, id: '', x: 0, play: false, line: null, mk: null};
function pvAt(x){ const L = PV.r.log, i = Math.max(0, Math.min(L.length - 2, Math.floor(x))), f = Math.max(0, Math.min(1, x - i)), a = L[i], b = L[i + 1]; return a.map((v, k) => v + (b[k] - v) * f); }
function pvDraw(){
  const cv = $('pv-cv'), dpr = window.devicePixelRatio || 1, W = cv.clientWidth, H = cv.clientHeight; if (!W) return;
  if (cv.width !== Math.round(W * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
  const L = PV.r.log, n = L.length, tMax = L[n - 1][0], hMax = Math.max(1000, Math.ceil(Math.max.apply(null, L.map(p => p[3])) / 500) * 500), s0 = L[0][5];
  const X = t => 30 + (W - 34) * t / tMax, Y = h => H - 14 - (H - 20) * h / hMax;
  g.font = '10px sans-serif'; g.fillStyle = '#9aabc4'; g.strokeStyle = 'rgba(154,171,196,.22)'; g.lineWidth = 1; g.textAlign = 'right';
  for (let h = 0; h <= hMax; h += hMax > 3000 ? 1000 : 500){ g.beginPath(); g.moveTo(30, Y(h)); g.lineTo(W - 4, Y(h)); g.stroke(); g.fillText(h, 27, Y(h) + 3); }
  g.textAlign = 'center'; for (let t = 0; t <= tMax; t += 6 * 3600) g.fillText(t / 3600 + ' h', X(t), H - 2);
  for (let i = 0; i < n - 1; i++) if (sunSin(L[i][1], L[i][2], GB.t0 + L[i][0] * 1000) < 0){ g.fillStyle = 'rgba(40,60,110,.35)'; g.fillRect(X(L[i][0]), 3, X(L[i + 1][0]) - X(L[i][0]) + .6, H - 17); }   // Nacht
  g.beginPath(); g.moveTo(X(0), Y(0)); L.forEach(p => g.lineTo(X(p[0]), Y(p[4]))); g.lineTo(X(tMax), Y(0)); g.closePath(); g.fillStyle = 'rgba(154,171,196,.45)'; g.fill();
  const line = (k, sc, col, dash) => { g.beginPath(); L.forEach((p, i) => { const y = Y(p[k] * sc); i ? g.lineTo(X(p[0]), y) : g.moveTo(X(p[0]), y); }); g.strokeStyle = col; g.lineWidth = dash ? 1.5 : 2.2; g.setLineDash(dash || []); g.stroke(); g.setLineDash([]); };
  line(5, hMax / s0, '#ffe14d', [5, 3]); line(6, hMax / 100, '#4cc9ff', [2, 3]); line(3, 1, '#ff9f1c');
  const c = pvAt(PV.x); g.strokeStyle = '#fff'; g.lineWidth = 1; g.beginPath(); g.moveTo(X(c[0]), 3); g.lineTo(X(c[0]), H - 14); g.stroke(); g.fillStyle = '#ff9f1c'; g.beginPath(); g.arc(X(c[0]), Y(c[3]), 4, 0, 7); g.fill(); g.stroke();
}
function pvSet(x){
  const n = PV.r.log.length; PV.x = Math.max(0, Math.min(n - 1, x)); const c = pvAt(PV.x), clk = new Date(GB.t0 + c[0] * 1000 + 2 * 3600e3);
  if (PV.mk) PV.mk.setLatLng([c[1], c[2]]);
  $('pv-pos').value = Math.round(1000 * PV.x / (n - 1));
  $('pv-read').textContent = tr('pv_read', {t: fmtT(c[0]).slice(0, -3) + ' h', clk: clk.toLocaleDateString(UI.lang, {weekday: 'short', timeZone: 'UTC'}) + ' ' + clk.toISOString().slice(11, 16), alt: nf(Math.round(c[3] / 10) * 10), agl: nf(Math.max(0, Math.round((c[3] - c[4]) / 10) * 10)), w: (c[7] >= 0.05 ? '+' : '') + nf(c[7], 1), sand: nf(c[5], 0), gas: nf(c[6], 0), km: nf(geoDist(GB.start.lat, GB.start.lon, c[1], c[2]) / 1000, 0)});
  pvDraw();
}
function pvPlay(p){ PV.play = p; $('pv-play').textContent = p ? 'II' : '▶'; }
function pvOpen(id){
  const r = GB_ROUTES[id], pts = r.log.map(p => [p[1], p[2]]); pvClose(true); PV.r = r; PV.id = id;
  PV.line = L.polyline(pts, {color: id === 'max' ? '#ffe14d' : '#4cc9ff', weight: 3.5, opacity: .95, interactive: false}).addTo(map);
  PV.mk = L.circleMarker(pts[0], {radius: 8, color: '#0a1019', weight: 2, fillColor: '#ff9f1c', fillOpacity: 1, interactive: false}).addTo(map);
  $('startwin').hidden = true; $('pv').hidden = false; $('pv-head').textContent = tr('pv_head', {name: tr('pv_' + id), km: nf(r.km, 0), h: nf(r.log[r.log.length - 1][0] / 3600, 0)});
  let near = Infinity; if (GB.ban) for (const p of r.log) near = Math.min(near, gbBanDist(p[1], p[2], 60000));
  $('pv-leg').textContent = (near < GB.buffer + 2000 ? tr('pv_warn', {km: nf(near / 1000, 0)}) + ' ' : '') + tr('pv_leg');
  map.invalidateSize(); if (L.latLngBounds) map.fitBounds(L.latLngBounds(pts), {paddingTopLeft: [20, 60], paddingBottomRight: [20, 300]});
  pvSet(0); pvPlay(true);
}
function pvClose(keep){
  if (PV.line) map.removeLayer(PV.line); if (PV.mk) map.removeLayer(PV.mk); PV.line = PV.mk = null; PV.play = false; if (!PV.r) return; PV.r = null; $('pv').hidden = true;
  if (keep !== true && STATE === 'brief'){ $('startwin').hidden = false; startView(); }
}
function pvTick(real){ if (!PV.r || !PV.play) return; const n = PV.r.log.length; pvSet(PV.x + real * (n - 1) / 60); if (PV.x >= n - 1) pvPlay(false); }   // die ganze Fahrt in einer Minute
document.querySelectorAll('#sw-pv button').forEach(b => b.addEventListener('click', () => pvOpen(b.dataset.pv)));
$('pv-close').addEventListener('click', pvClose); $('pv-play').addEventListener('click', () => { if (!PV.play && PV.x >= PV.r.log.length - 1) pvSet(0); pvPlay(!PV.play); });
$('pv-pos').addEventListener('input', () => { pvPlay(false); pvSet(+$('pv-pos').value / 1000 * (PV.r.log.length - 1)); });

'''
f.rep("/* ---------- Zeitschleife ---------- */",js+"/* ---------- Zeitschleife ---------- */")
f.rep("  const real = Math.min(0.1, (ts - lastTs) / 1000 || 0); lastTs = ts;\n","  const real = Math.min(0.1, (ts - lastTs) / 1000 || 0); lastTs = ts;\n  pvTick(real);\n")
f.rep("function setState(s){ STATE = s;","function setState(s){ if (s !== 'brief' && PV.r) pvClose(true); STATE = s;")
f.rep("const BUILD = '2026-10-09.7'","const BUILD = '2026-10-09.7'")
f.save()
