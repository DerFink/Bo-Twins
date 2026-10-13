import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep('          <div class="lbl" id="st-info"></div>','          <div class="lbl" id="st-info"></div>\n          <div id="gps-big" hidden><b id="gps-n">10</b><span id="gps-cap"></span></div>')
f.rep("#toast.on{opacity:1;","/* GPS: großer Countdown, solange der Standort gesucht und gemittelt wird */\n#gps-big{display:flex;align-items:center;gap:14px;margin:8px 0 2px;padding:8px 14px;border:1px solid var(--orb);border-radius:12px;background:var(--pan)}\n#gps-big[hidden]{display:none}\n#gps-big b{font-family:var(--num);font-size:64px;font-weight:700;line-height:1;color:var(--orb);min-width:1.2em;text-align:center;font-variant-numeric:tabular-nums}\n#gps-big span{font-size:14px;line-height:1.35}\n#toast.on{opacity:1;")
f.block("function gpsStop(){","$('st-map').addEventListener('click', () => { gpsStop();","""const GPS_AVG = 10;                                        // s, so lange wird der Standort gemittelt (Vorgabe Nutzer)
let gpsTimer = null;
function gpsStop(){ if (stWatch !== null){ navigator.geolocation.clearWatch(stWatch); stWatch = null; } clearInterval(gpsTimer); gpsTimer = null; $('gps-big').hidden = true; $('su-go').disabled = false; }
""")
f.block("$('st-gps').addEventListener('click', () => {","/* ---------- Rückfrage","""$('st-gps').addEventListener('click', () => {
  if (!navigator.geolocation){ stShow(tr('st_err')); return; }
  gpsStop();
  const pts = []; let t0 = null, acc = null; stShow(tr('st_wait')); $('su-go').disabled = true; $('gps-big').hidden = false;
  const finish = () => {
    gpsStop();
    const m = k => pts.reduce((a, c) => a + (c[k] || 0), 0) / pts.length, hasAlt = pts.every(c => c.altitude != null);
    stSet({lat: m('latitude'), lon: m('longitude'), alt: hasAlt ? Math.round(m('altitude')) : null, kind: 'gps'});
  };
  const tick = () => {                                                                                                  // großer Countdown: erst Suche nach einem brauchbaren Fix, dann die Sekunden der Mittelung
    if (STATE !== 'setup'){ gpsStop(); return; }                                                                        // Vorbereitung verlassen: Standort nicht mehr übernehmen
    if (t0 === null){ $('gps-n').textContent = '…'; $('gps-cap').textContent = tr('gps_search') + (acc != null ? ' (±' + Math.round(acc) + ' m)' : ''); return; }
    const el = (Date.now() - t0) / 1000;
    $('gps-n').textContent = Math.max(0, Math.ceil(GPS_AVG - el)); $('gps-cap').textContent = tr('gps_avg'); stShow(tr('st_avg', {n: Math.max(0, Math.ceil(GPS_AVG - el))}));
    if (el >= GPS_AVG && pts.length >= 3) finish();
  };
  tick(); gpsTimer = setInterval(tick, 200);
  stWatch = navigator.geolocation.watchPosition(p => {
    acc = p.coords.accuracy;
    if (p.coords.accuracy > 30) return;                                                                                 // erst ein brauchbarer Fix (besser als 30 m)
    if (t0 === null) t0 = Date.now();
    pts.push(p.coords);
  }, () => { gpsStop(); stShow(tr('st_err')); }, {enableHighAccuracy: true, maximumAge: 0, timeout: 60000});
});

""")
T={'de':("gps_search:'Suche den Standort. Die Fahrt kann erst beginnen, wenn das GPS genau genug ist.'","gps_avg:'Sekunden: Der Standort wird gemittelt, damit der Startplatz genau stimmt.'"),
 'en':("gps_search:'Looking for your position. The flight can only begin once GPS is accurate enough.'","gps_avg:'seconds: the position is being averaged so that the launch site is exact.'"),
 'fr':("gps_search:'Recherche de la position. Le vol ne peut commencer que lorsque le GPS est assez précis.'","gps_avg:'secondes : la position est moyennée pour que le lieu de départ soit exact.'"),
 'pl':("gps_search:'Szukam pozycji. Lot może się zacząć dopiero, gdy GPS będzie wystarczająco dokładny.'","gps_avg:'sekund: pozycja jest uśredniana, aby miejsce startu było dokładne.'"),
 'cs':("gps_search:'Hledám polohu. Let může začít, až bude GPS dostatečně přesná.'","gps_avg:'sekund: poloha se průměruje, aby místo startu bylo přesné.'"),
 'zh-TW':("gps_search:'正在定位。GPS 夠精確後才能開始飛行。'","gps_avg:'秒：正在平均定位結果，讓起飛點更準確。'"),
 'es':("gps_search:'Buscando la posición. El vuelo solo puede empezar cuando el GPS sea lo bastante preciso.'","gps_avg:'segundos: se promedia la posición para que el lugar de despegue sea exacto.'")}
order=['de','en','fr','pl','cs','zh-TW','es']; it=iter(order); n=[0]
def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[next(it)])+m.group(2)
f.s=re.sub(r"(lg_cloud:'[^']*')( \})",r,f.s); assert n[0]==7,n
f.save()
