import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add
f=F()
# ---- Nutzungszeit zuverlässig melden: jede Minute, nur solange die App sichtbar ist ----
a=f.s.index("  addEventListener('pagehide', () => { try{ navigator.sendBeacon(ONLINE.api + '?action=leave'"); b=f.s.index("\n",a)
f.s=f.s[:a]+"""  let vis = 0, last = t0, sent = 0;                                           // Nutzungszeit: nur solange die App sichtbar ist
  const tick = () => { const n = Date.now(); if (document.visibilityState !== 'hidden') vis += Math.min(n - last, 5000); last = n; };
  const send = beacon => { tick(); const sec = Math.round(vis / 1000); if (sec === sent) return; sent = sec; const body = JSON.stringify({id: uid(), sec});
    try{ if (beacon && navigator.sendBeacon) navigator.sendBeacon(ONLINE.api + '?action=leave', body); else onlineCall('leave', {id: uid(), sec}).catch(() => {}); }catch(e){} };
  setInterval(tick, 2000); setInterval(() => send(false), 60000);                // jede Minute melden: Auf dem Handy kommt die Meldung beim Schließen oft nicht mehr an
  addEventListener('pagehide', () => send(true)); document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') send(true); else last = Date.now(); });"""+f.s[b:]
# ---- Statistik für alle (SRV-07) ----
f.rep('<button class="sm" id="in-btn" data-i="in_title"></button></div>','<button class="sm" id="in-btn" data-i="in_title"></button><button class="sm" id="sx-btn" data-i="sx_title" hidden></button></div>')
f.rep('    <!-- Ballon im Detail (STE-26)','''    <!-- Statistik für alle (SRV-07): nur mit dem Dienst auf dem Server -->
    <div class="full" id="stats" hidden>
      <div class="card">
        <h2 data-i="sx_title"></h2>
        <div id="sx-rows"></div>
        <canvas id="sx-cv" role="img" data-ia="sx_hist" aria-label="Verteilung"></canvas>
        <p class="note" id="sx-note"></p>
        <button class="sec" id="sx-close" data-i="close"></button>
      </div>
    </div>

    <!-- Ballon im Detail (STE-26)''')
f.rep("#info{z-index:950}","#stats{z-index:950}\n#stats .card{width:min(420px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px;background:#0d1626}\n#stats .kv{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid rgba(154,171,196,.14);font-size:14.5px}\n#stats .kv b{font-family:var(--num);font-size:17px;white-space:nowrap}\n#stats .kv.hd{border:0;padding:10px 0 0;color:var(--orb);font-size:13px}\n#sx-cv{display:block;width:100%;height:130px;margin:10px 0 4px}\n#sx-btn[hidden]{display:none}\n#info{z-index:950}")
f.rep("/* ---------- Rollhinweis (NFA-07) ---------- */","""/* ---------- Statistik für alle (SRV-07): Zahl der Geräte und Verteilung der Nutzungszeit. Die Zeiten sind schief verteilt (viele kurz, wenige sehr lang),
   deshalb Median und mittlere Hälfte statt Mittelwert und Streuung einer Glockenkurve. ---------- */
const fmtDur = s => s >= 3600 ? Math.floor(s / 3600) + ' h ' + String(Math.round(s % 3600 / 60)).padStart(2, '0') + ' min' : s >= 60 ? Math.round(s / 60) + ' min' : Math.round(s) + ' s';
async function statsOpen(){
  const box = $('sx-rows'); box.textContent = ''; $('sx-note').textContent = tr('busy_wx'); $('stats').hidden = false; let d = null;
  try{ d = await onlineCall('pubstats'); }catch(e){}
  if (!d || !d.ok){ $('sx-note').textContent = tr('sc_online_fail'); return; }
  const row = (k, v, hd) => { const e = document.createElement('div'), s = document.createElement('span'), b = document.createElement('b'); e.className = 'kv' + (hd ? ' hd' : ''); s.textContent = tr(k); b.textContent = v; e.appendChild(s); e.appendChild(b); box.appendChild(e); };
  row('sx_users', nf(d.users)); row('sx_users7', nf(d.users7)); row('sx_flights', nf(d.flights)); row('sx_sum', fmtDur(d.sum));
  row('sx_time', '', true); row('sx_low', fmtDur(d.low)); row('sx_most', fmtDur(d.q1) + ' – ' + fmtDur(d.q3)); row('sx_median', fmtDur(d.median)); row('sx_mean', fmtDur(d.mean)); row('sx_max', fmtDur(d.max));
  $('sx-note').textContent = tr('sx_note', {n: nf(d.timed), d: d.since ? new Date(d.since).toLocaleDateString(UI.lang) : '–'});
  const cv = $('sx-cv'), W = cv.clientWidth, H = cv.clientHeight, dpr = Math.min(window.devicePixelRatio || 1, 3); cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
  const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  const lab = ['< 5 min', '5–15', '15–30', '30–60', '1–3 h', '3–10 h', '> 10 h'], mx = Math.max(1, Math.max.apply(null, d.hist)), bw = W / d.hist.length;
  d.hist.forEach((v, i) => { const h = (H - 34) * v / mx; c.fillStyle = '#ff9f1c'; c.fillRect(i * bw + 4, H - 18 - h, bw - 8, Math.max(v ? 2 : 0, h)); c.fillStyle = '#eef3fa'; c.font = '600 12px "Barlow Condensed","Arial Narrow",sans-serif'; c.textAlign = 'center'; c.fillText(v, i * bw + bw / 2, H - 22 - h); c.fillStyle = '#9aabc4'; c.font = '500 10px Barlow,"Segoe UI",sans-serif'; c.fillText(lab[i], i * bw + bw / 2, H - 4); });
}
$('sx-btn').addEventListener('click', statsOpen); $('sx-close').addEventListener('click', () => { $('stats').hidden = true; });
onlineInit().then(ok => { $('sx-btn').hidden = !ok; });

/* ---------- Rollhinweis (NFA-07) ---------- */""")
tx_add(f,{
 'sx_title':['Statistik','Statistics','Statistiques','Statystyki','Statistika','統計','Estadísticas'],
 'sx_hist':['Verteilung der Nutzungszeit je Gerät','Distribution of time spent per device','Répartition du temps passé par appareil','Rozkład czasu na urządzenie','Rozložení času na zařízení','每台裝置使用時間的分布','Distribución del tiempo por dispositivo'],
 'sx_users':['Geräte insgesamt','Devices in total','Appareils au total','Urządzenia łącznie','Zařízení celkem','裝置總數','Dispositivos en total'],
 'sx_users7':['davon in den letzten 7 Tagen','of these in the last 7 days','dont ces 7 derniers jours','z tego w ostatnich 7 dniach','z toho za posledních 7 dní','其中最近 7 天','de ellos en los últimos 7 días'],
 'sx_flights':['Gewertete Fahrten','Scored flights','Vols notés','Loty z oceną','Hodnocené lety','計分飛行','Vuelos puntuados'],
 'sx_sum':['Zeit aller zusammen','Time of all together','Temps cumulé','Łączny czas','Čas všech dohromady','所有人合計時間','Tiempo de todos'],
 'sx_time':['Zeit mit der App je Gerät','Time with the app per device','Temps passé par appareil','Czas z aplikacją na urządzenie','Čas s aplikací na zařízení','每台裝置的使用時間','Tiempo con la app por dispositivo'],
 'sx_low':['Wenigspieler (untere 10 %) bis','Light users (lowest 10 %) up to','Petits joueurs (10 % les plus bas) jusqu’à','Najmniej grający (dolne 10 %) do','Nejméně hrající (spodních 10 %) do','最少的 10 % 不超過','Los que menos juegan (10 % inferior) hasta'],
 'sx_most':['Die meisten (mittlere Hälfte)','Most people (middle half)','La plupart (moitié centrale)','Większość (środkowa połowa)','Většina (prostřední polovina)','多數人（中間一半）','La mayoría (mitad central)'],
 'sx_median':['Typisch (Median)','Typical (median)','Typique (médiane)','Typowo (mediana)','Typicky (medián)','典型（中位數）','Típico (mediana)'],
 'sx_mean':['Durchschnitt','Average','Moyenne','Średnia','Průměr','平均','Media'],
 'sx_max':['Längste Zeit','Longest time','Temps le plus long','Najdłuższy czas','Nejdelší čas','最長時間','Tiempo más largo'],
 'sx_note':['Gezählt werden Geräte, nicht Personen; ausgewertet sind {n} Geräte mit mindestens 30 Sekunden, seit {d}. Gemessen wird die Zeit, in der die App sichtbar geöffnet ist. Es werden nur Summen gezeigt, keine Namen.','Devices are counted, not people; {n} devices with at least 30 seconds are evaluated, since {d}. Measured is the time the app is open and visible. Only totals are shown, no names.','On compte des appareils, pas des personnes ; {n} appareils avec au moins 30 secondes, depuis le {d}. On mesure le temps pendant lequel l’application est ouverte et visible. Seuls des totaux sont affichés, aucun nom.','Liczone są urządzenia, nie osoby; uwzględniono {n} urządzeń z co najmniej 30 sekundami, od {d}. Mierzony jest czas, gdy aplikacja jest otwarta i widoczna. Pokazywane są tylko sumy, bez imion.','Počítají se zařízení, ne osoby; vyhodnoceno {n} zařízení s alespoň 30 sekundami, od {d}. Měří se čas, kdy je aplikace otevřená a viditelná. Zobrazují se jen součty, žádná jména.','統計的是裝置而非人數；共計 {n} 台使用至少 30 秒的裝置，自 {d} 起。計算的是 App 開啟且可見的時間。只顯示總計，不顯示名字。','Se cuentan dispositivos, no personas; se evalúan {n} dispositivos con al menos 30 segundos, desde el {d}. Se mide el tiempo en que la app está abierta y visible. Solo se muestran totales, sin nombres.'],
})
f.rep("const BUILD = '2026-10-10.5'","const BUILD = '2026-10-10.6'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v37'" in s; open(p,'w').write(s.replace("'v37'","'v38'"))
