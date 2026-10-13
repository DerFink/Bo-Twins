import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. GPS: erst weiter, wenn der Standort da ist ----------
f.block("let stWatch = null;\n","/* ---------- Rückfrage",
"""let stWatch = null;
// Solange das GPS gesucht und gemittelt wird, bleibt „Weiter“ gesperrt: Sonst begänne die Fahrt am alten Startplatz und der Ballon spränge später auf den GPS-Ort.
function gpsStop(){ if (stWatch !== null){ navigator.geolocation.clearWatch(stWatch); stWatch = null; } $('su-go').disabled = false; }
$('st-map').addEventListener('click', () => { gpsStop(); clearGoals(); pathLine.setLatLngs([]); map.setView(ll(0, 0), 12); setState('pick'); toast(tr('st_tap')); });
map.on('click', e => { if (STATE !== 'pick') return; stSet({lat: e.latlng.lat, lon: e.latlng.lng, alt: null, kind: 'map'}); setState('setup'); });
$('st-def').addEventListener('click', () => { gpsStop(); stSet(BITTERFELD); });
$('st-gps').addEventListener('click', () => {
  if (!navigator.geolocation){ stShow(tr('st_err')); return; }
  gpsStop();
  const pts = []; let t0 = null; stShow(tr('st_wait')); $('su-go').disabled = true;
  stWatch = navigator.geolocation.watchPosition(p => {
    if (STATE !== 'setup'){ gpsStop(); return; }                                                                        // Vorbereitung verlassen: Standort nicht mehr übernehmen
    if (p.coords.accuracy > 30){ stShow(tr('st_wait') + ' (±' + Math.round(p.coords.accuracy) + ' m)'); return; }     // erst ein brauchbarer Fix
    if (t0 === null) t0 = Date.now();
    pts.push(p.coords); const el = (Date.now() - t0) / 1000;
    stShow(tr('st_avg', {n: Math.max(0, Math.ceil(15 - el))}));
    if (el >= 15 && pts.length >= 3){
      gpsStop();
      const m = k => pts.reduce((a, c) => a + (c[k] || 0), 0) / pts.length, hasAlt = pts.every(c => c.altitude != null);
      stSet({lat: m('latitude'), lon: m('longitude'), alt: hasAlt ? Math.round(m('altitude')) : null, kind: 'gps'});
    }
  }, () => { gpsStop(); stShow(tr('st_err')); }, {enableHighAccuracy: true, maximumAge: 0, timeout: 60000});
});

""")
f.rep("$('su-back').addEventListener('click', () => { if (UI.mode","$('su-back').addEventListener('click', () => { gpsStop(); if (UI.mode")
f.rep("function openSetup(mode, task){","function openSetup(mode, task){\n  gpsStop();")
f.rep("$('su-go').addEventListener('click', prepareRun);","$('su-go').addEventListener('click', () => { if (stWatch === null) prepareRun(); });")

# ---------- 2. Simulation: mehr Richtungswechsel, bis 270° bis 3000 m ----------
f.block("function randomWx(rnd, full){","function buildAtm(wx){",
"""function randomWx(rnd, full){
  rnd = rnd || Math.random;
  const R = (a, b) => a + rnd() * (b - a), SPLIT = 3000;
  // Schichtgrenzen in unregelmäßigen Abständen; unter 3000 m liegen sie dichter, dort wechselt die Richtung häufiger
  const hs = [0]; while (hs[hs.length - 1] < 6000){ const h = hs[hs.length - 1], nx = h + R(100, 280) + rnd() * rnd() * (h < SPLIT ? 700 : 1500); hs.push(h < SPLIT && nx > SPLIT ? SPLIT : Math.min(6000, nx)); }
  const n = hs.length - 1, w = []; let sLo = 0, sHi = 0;
  for (let i = 0; i < n; i++){ const x = (0.15 + rnd() * rnd() * 2.5) * (hs[i + 1] - hs[i]) / 600; w.push(x); if (hs[i] < SPLIT) sLo += x; else sHi += x; }   // Anteil der Drehung je Schicht
  // Drehung vom Boden bis 3000 m: 150° bis 270° (Vorgabe Nutzer: bis 270°); darüber dreht der Wind weiter. Mit full (Aufgabe MID) kommen bis 6000 m alle Richtungen vor.
  const lo = full ? R(230, 270) : R(150, 270), hi = full ? R(130, 170) : R(30, 110), sign = rnd() < 0.75 ? 1 : -1;
  let dir = R(0, 360), spd = R(1.5, 3.5); const pts = [[0, dir, spd]];
  for (let i = 0; i < n; i++){ dir += sign * (hs[i] < SPLIT ? lo * w[i] / sLo : hi * w[i] / sHi); spd = Math.max(1.2, spd + (hs[i + 1] - hs[i]) * R(0.0008, 0.0035) + R(-0.8, 0.8)); pts.push([hs[i + 1], dir, spd]); }
  const wind = [];                                                                                                               // Stützstellen alle 100 m, damit die Drehung gleichmäßig durchlaufen wird
  for (let z = 0; z <= 6000; z += 100){
    let i = 0; while (i < n - 1 && hs[i + 1] < z) i++;
    const q = (z - hs[i]) / (hs[i + 1] - hs[i]);
    wind.push([z, ((pts[i][1] + (pts[i + 1][1] - pts[i][1]) * q) % 360 + 360) % 360, pts[i][2] + (pts[i + 1][2] - pts[i][2]) * q]);
  }
  const top = wind[wind.length - 1]; wind.push([10000, top[1], top[2] * 1.3]);
  const ib = R(250, 1100), it = ib + R(80, 220);                                                                                 // Inversion in zufälliger Höhe
  return {p0: R(100300, 102600), T0: R(6, 18), layers: [[ib, -R(0.006, 0.0095)], [it, R(0.006, 0.016)], [R(1800, 2600), -0.0060], [1e5, -0.0065]], wind};
}

""")

# ---------- 3. Farben im Vertikalprofil: blau Inversion, grün sehr stabil, grau gewöhnlich, rot labil ----------
f.rep("col = ['#4cc9ff', '#5d6f8f', '#ffe14d', '#ff6e5f'];","col = ['#ff6e5f', '#5d6f8f', '#5fe3a1', '#4cc9ff'];   // labil rot, gewöhnlich grau, sehr stabil grün, Inversion blau (Vorgabe Nutzer)")
f.rep("c.fillStyle = 'rgba(255,110,95,.18)'; c.fillRect(xS, y(z + 50), W - xS","c.fillStyle = 'rgba(76,201,255,.16)'; c.fillRect(xS, y(z + 50), W - xS")
f.rep("c.fillStyle = '#ff9d92'; c.font = small;","c.fillStyle = '#9fdcff'; c.font = small;")
f.rep('<i style="background:#ff6e5f"></i><span data-i="lg_inv">','<i style="background:#4cc9ff"></i><span data-i="lg_inv">')
f.rep('<i style="background:#ffe14d"></i><span data-i="lg_stable">','<i style="background:#5fe3a1"></i><span data-i="lg_stable">')
f.rep('<i style="background:#4cc9ff"></i><span data-i="lg_labile">','<i style="background:#ff6e5f"></i><span data-i="lg_labile">')
W={'lg_inv':['Rot|Blau','Red|Blue','Rouge|Bleu','Czerwony|Niebieski','Červená|Modrá','紅色|藍色','Rojo|Azul'],
   'lg_stable':['Gelb|Grün','Yellow|Green','Jaune|Vert','Żółty|Zielony','Žlutá|Zelená','黃色|綠色','Amarillo|Verde'],
   'lg_labile':['Blau|Rot','Blue|Red','Bleu|Rouge','Niebieski|Czerwony','Modrá|Červená','藍色|紅色','Azul|Rojo']}
for k,L in W.items():
    for p in L:
        a,b=p.split('|'); f.rep(k+":'"+a, k+":'"+b)
f.rep("const BUILD = '2026-10-08.9';","const BUILD = '2026-10-08.10';")
f.save()
