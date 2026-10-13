import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add,tx_set
f=F()
# ================= Platz jetzt: Zeile lief über =================
tx_set(f,'gb_ranknow',['Platz','Rank','Rang','Miejsce','Pořadí','名次','Puesto'])
f.rep("(GB_TEAMS.filter(t => t[2] > gbKm()).length + 1) + ' / ' + (GB_TEAMS.length + 1)","(GB_TEAMS.filter(t => t[2] > gbKm()).length + 1) + '/' + (GB_TEAMS.length + 1)")
# ================= HTML =================
f.rep('''        <button class="iconbtn" id="rv-btn" hidden''','''        <button class="iconbtn" id="side-btn" hidden data-ia="side_a" aria-label="Seitenansicht" aria-pressed="false"><svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="11" cy="7.5" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 12.5l1 3h3l1-3" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M1.5 19.5c4-2 7 1 11-1s5 0 8 0" fill="none" stroke="#5fe3a1" stroke-width="1.8" stroke-linecap="round"/></svg></button>
        <button class="iconbtn" id="rv-btn" hidden''')
f.rep('''      <button class="ov" id="follow" hidden''','''      <div class="ov card" id="side" hidden><canvas id="side-cv" role="img" data-ia="side_hint" aria-label="Seitenansicht"></canvas></div>
      <button class="ov" id="follow" hidden''')
f.rep('    <!-- Ballon im Detail (STE-26)','''    <!-- Temp: Stüve-Diagramm (STE-27); Antippen schließt -->
    <div class="full" id="stuve" hidden>
      <div class="card">
        <canvas id="stuve-cv" role="img" data-ia="st_title" aria-label="Temp"></canvas>
        <p class="note" data-i="st_note"></p>
      </div>
    </div>

    <!-- Karten und Daten (DOC-01): Quellen, Abdeckung, Aktualität -->
    <div class="full" id="info" hidden>
      <div class="card">
        <h2 data-i="in_title"></h2>
        <div id="in-rows"></div>
        <button class="sec" id="in-close" data-i="close"></button>
      </div>
    </div>

    <!-- Ballon im Detail (STE-26)''')
f.rep('''    <div class="row"><span data-i="v_unit"></span>''','''    <div class="row"><span data-i="v_ofm"></span><div class="seg" id="seg-ofm"><button data-v="0" data-i="off"></button><button data-v="1" data-i="on"></button></div></div>
    <div class="row"><span data-i="v_side"></span><div class="seg" id="seg-side"><button data-v="auto" data-i="side_auto"></button><button data-v="off" data-i="off"></button></div></div>
    <p class="note"><button class="sm" id="in-btn" data-i="in_title"></button></p>
    <div class="row"><span data-i="v_unit"></span>''')
# ================= CSS =================
f.rep("#detail{z-index:885}","""#side{left:6px;bottom:8px;width:176px;height:168px;padding:0;overflow:hidden;cursor:pointer;background:#0d1626}
#side[hidden],#side-btn[hidden]{display:none}
#side-cv{display:block;width:100%;height:100%}
#side-btn.on{border-color:var(--orb);color:var(--orb)}
#stuve{z-index:886;cursor:pointer}
#stuve .card{width:min(560px,100%);max-height:calc(100% - 8px);overflow:auto;padding:8px 8px 8px;background:#0d1626}
#stuve-cv{display:block;width:100%;height:min(74vh,620px)}
#stuve .note{margin:6px 4px 2px;font-size:12px}
#info{z-index:887}
#info .card{width:min(520px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px;background:#0d1626}
#in-rows h3{margin:12px 0 3px;font-size:15px;color:var(--orb)}
#in-rows p{margin:0 0 4px;font-size:13.5px;line-height:1.4}
.leaflet-tile.tiles-ofm{background:rgba(238,238,232,.92)}
#detail{z-index:885}""")
# ================= Texte =================
tx_set(f,'prof_hint',['Vertikalprofil: links antippen für das Temp-Diagramm, rechts zum Vergrößern','Vertical profile: tap left for the sounding diagram, right to enlarge','Profil vertical : toucher à gauche pour l’émagramme, à droite pour agrandir','Profil pionowy: dotknij z lewej, aby otworzyć diagram, z prawej, aby powiększyć','Vertikální profil: klepnutím vlevo otevřete diagram, vpravo zvětšíte','垂直剖面：點左側開啟探空圖，點右側放大','Perfil vertical: toca a la izquierda para el diagrama, a la derecha para ampliar'])
tx_add(f,{
 'side_a':['Seitenansicht ein- oder ausblenden','Show or hide the side view','Afficher ou masquer la vue de côté','Pokaż lub ukryj widok z boku','Zobrazit nebo skrýt boční pohled','顯示或隱藏側視圖','Mostrar u ocultar la vista lateral'],
 'side_hint':['Seitenansicht: Ballon, Schlepptau und Gelände in Fahrtrichtung. Antippen blendet aus.','Side view: balloon, trail rope and terrain along the track. Tap to hide.','Vue de côté : ballon, guiderope et relief dans le sens de la marche. Touchez pour masquer.','Widok z boku: balon, lina wleczna i teren w kierunku lotu. Dotknij, aby ukryć.','Boční pohled: balon, vlečné lano a terén ve směru letu. Klepnutím skryjete.','側視圖：氣球、拖繩與前進方向的地形。點一下隱藏。','Vista lateral: globo, cuerda guía y terreno en el sentido de la marcha. Toca para ocultar.'],
 'side_agl':['über Grund','above ground','sol','nad ziemią','nad zemí','離地','sobre el suelo'],
 'v_ofm':['Lufträume (open flightmaps)','Airspace (open flightmaps)','Espaces aériens (open flightmaps)','Przestrzenie (open flightmaps)','Vzdušné prostory (open flightmaps)','空域（open flightmaps）','Espacio aéreo (open flightmaps)'],
 'v_side':['Seitenansicht unter 50 m','Side view below 50 m','Vue de côté sous 50 m','Widok z boku poniżej 50 m','Boční pohled pod 50 m','50 公尺以下顯示側視圖','Vista lateral bajo 50 m'],
 'side_auto':['Automatisch','Automatic','Automatique','Automatycznie','Automaticky','自動','Automática'],
 'ofm_hint':['Lufträume: nur zur Orientierung, ersetzt keine amtliche Karte und wirkt nicht auf das Spiel. Sichtbar ab Zoomstufe 7. Nicht alle Länder sind abgedeckt, siehe „Karten und Daten“.','Airspace: for orientation only, not a substitute for an official chart, no effect on the game. Visible from zoom level 7. Not all countries are covered, see “Maps and data”.','Espaces aériens : à titre indicatif, ne remplace pas une carte officielle, sans effet sur le jeu. Visible à partir du zoom 7. Tous les pays ne sont pas couverts, voir « Cartes et données ».','Przestrzenie: tylko orientacyjnie, nie zastępuje mapy urzędowej, bez wpływu na grę. Widoczne od powiększenia 7. Nie wszystkie kraje są objęte, zob. „Mapy i dane”.','Vzdušné prostory: jen pro orientaci, nenahrazuje úřední mapu, bez vlivu na hru. Viditelné od přiblížení 7. Nejsou pokryty všechny země, viz „Mapy a data“.','空域：僅供參考，不能取代官方航圖，也不影響遊戲。縮放等級 7 以上才顯示。並非所有國家都有資料，請見「地圖與資料」。','Espacio aéreo: solo orientativo, no sustituye a una carta oficial y no afecta al juego. Visible desde el nivel de zoom 7. No todos los países están cubiertos; véase «Mapas y datos».'],
 'st_title':['Temp (Stüve-Diagramm)','Sounding (Stüve diagram)','Émagramme (diagramme de Stüve)','Sondaż (diagram Stüvego)','Výstup (Stüveho diagram)','探空圖（Stüve 圖）','Sondeo (diagrama de Stüve)'],
 'st_note':['Weiße Kurve: Lufttemperatur, eingefärbt wie im Vertikalprofil. Orange Linien: Trockenadiabaten. Oranger Punkt: Ballon; gelbe Raute: Gastemperatur. Rechts: Wind. Ohne Taupunkt und Feuchtadiabaten. Antippen schließt.','White curve: air temperature, coloured as in the vertical profile. Orange lines: dry adiabats. Orange dot: balloon; yellow diamond: gas temperature. Right: wind. No dew point or moist adiabats. Tap to close.','Courbe blanche : température de l’air, colorée comme dans le profil vertical. Lignes orange : adiabatiques sèches. Point orange : ballon ; losange jaune : température du gaz. À droite : vent. Sans point de rosée ni adiabatiques humides. Touchez pour fermer.','Biała krzywa: temperatura powietrza, kolory jak w profilu pionowym. Pomarańczowe linie: adiabaty suche. Pomarańczowy punkt: balon; żółty romb: temperatura gazu. Z prawej: wiatr. Bez punktu rosy i adiabat wilgotnych. Dotknij, aby zamknąć.','Bílá křivka: teplota vzduchu, barvy jako ve vertikálním profilu. Oranžové čáry: suché adiabaty. Oranžový bod: balon; žlutý kosočtverec: teplota plynu. Vpravo: vítr. Bez rosného bodu a vlhkých adiabat. Klepnutím zavřete.','白色曲線：氣溫，顏色與垂直剖面相同。橘線：乾絕熱線。橘點：氣球；黃色菱形：氣體溫度。右側：風。不含露點與濕絕熱線。點一下關閉。','Curva blanca: temperatura del aire, coloreada como en el perfil vertical. Líneas naranjas: adiabáticas secas. Punto naranja: globo; rombo amarillo: temperatura del gas. Derecha: viento. Sin punto de rocío ni adiabáticas húmedas. Toca para cerrar.'],
 'in_title':['Karten und Daten','Maps and data','Cartes et données','Mapy i dane','Mapy a data','地圖與資料','Mapas y datos'],
})
# ================= JS =================
js = r'''/* ---------- Lufträume (KRT-05): open flightmaps als zuschaltbare Ebene, wie in der Tracker-App ---------- */
const OFM = {url: 'https://nwy-tiles-api.prod.newaydata.com/tiles/{z}/{x}/{y}.png?path=latest/aero/latest', attr: '© open flightmaps association', minZoom: 7, maxNativeZoom: 12, layer: null};   // Kacheln gibt es nur bis Zoomstufe 12
function applyOfm(tell){
  if (UI.ofm){ if (!OFM.layer) OFM.layer = L.tileLayer(OFM.url, {minZoom: OFM.minZoom, maxZoom: 19, maxNativeZoom: OFM.maxNativeZoom, className: 'tiles-ofm', attribution: OFM.attr, opacity: .9, zIndex: 5}); OFM.layer.addTo(map); if (tell) toast(tr('ofm_hint')); }
  else if (OFM.layer) map.removeLayer(OFM.layer);
}

/* ---------- Karten und Daten (DOC-01): Was die App woher lädt, wie weit es reicht und wie alt es sein kann. Deutsch und Englisch; andere Sprachen zeigen Englisch. ---------- */
const INFO = {
 de: [['Karte', 'OpenStreetMap, weltweit. © OpenStreetMap-Mitwirkende (ODbL). Angezeigte Kartenteile bleiben auf dem Gerät gespeichert und werden nicht erneut geladen.'],
  ['Lufträume', 'open flightmaps (© open flightmaps association), als Bild über der Karte, ein- und ausschaltbar in den Einstellungen. Sichtbar ab Zoomstufe 7. Abdeckung laut openflightmaps.org, Stand 10.10.2026: Belgien, Dänemark, Deutschland, Finnland, Frankreich, Griechenland, Italien, Kroatien, Malta, Namibia, Niederlande, Österreich, Polen, Rumänien, Schweden, Schweiz, Slowakei, Slowenien, Südafrika, Tschechien, Ungarn. In anderen Ländern, zum Beispiel im Baltikum, bleibt die Ebene leer. Auf dem Gerät höchstens 14 Tage gespeichert. Nur zur Orientierung: kein Ersatz für amtliche Karten, Hindernisse und Leitungen können fehlen, im Spiel ohne Wirkung.'],
  ['Wetter', 'Open-Meteo (open-meteo.com, CC BY 4.0): Vorhersage der Wetterdienste für den Ort des Ballons, stündlich, auf 13 Druckflächen von 1000 bis 250 hPa mit Temperatur, Wind und Bewölkung, dazu Bodendruck und Niederschlag. Die App rechnet zwischen den Flächen und Stunden linear. Wie fein das Modell auflöst, hängt von der Region ab. Bei langen Fahrten wird unterwegs nachgeladen. Feuchte und Taupunkt werden nicht geladen.'],
  ['Wetter der Meisterschaft', 'Open-Meteo, Archiv der Vorhersagen (Historical Forecast) für den 29. bis 31. August 2026. Es ist die damalige Vorhersage, nicht das gemessene Wetter; der echte Wind kann abgewichen sein.'],
  ['Gelände', 'Open-Meteo Elevation (Höhenmodell Copernicus, rund 90 m Raster). Die App lädt um den Ballon ein Raster von 400 m und weiter außen von 2 km. Bäume, Gebäude und Leitungen sind nicht enthalten.'],
  ['Zielorte und Ortsnamen', 'Overpass und Nominatim (beide aus OpenStreetMap-Daten): Sportplätze und Wiesen als Ziele, Ortsnamen für Start und Ziel. Die Angaben sind so vollständig wie OpenStreetMap am jeweiligen Ort.'],
  ['Ländergrenzen der Meisterschaft', 'Paket world-atlas aus Natural Earth, Maßstab 1:50 Mio. (gemeinfrei). Die Grenzen sind vereinfacht und können um einige Kilometer vom wirklichen Verlauf abweichen. Der rote Rand von 10 km wird aus diesen Grenzen gerechnet. Die offizielle Restricted Area des Rennens ist nicht hinterlegt.'],
  ['Simulation', 'In der Spielart Simulation kommt nichts aus dem Netz: Wetter und Gelände werden in der App erzeugt.'],
  ['Wichtig', 'Die App ist ein Spiel. Sie ersetzt keine Flugvorbereitung, keine Wetterberatung und keine Luftfahrtkarte.']],
 en: [['Map', 'OpenStreetMap, worldwide. © OpenStreetMap contributors (ODbL). Map tiles you have seen stay stored on the device and are not loaded again.'],
  ['Airspace', 'open flightmaps (© open flightmaps association), shown as an image over the map, switched on and off in the settings. Visible from zoom level 7. Coverage according to openflightmaps.org as of 10 Oct 2026: Austria, Belgium, Croatia, Czech Republic, Denmark, Finland, France, Germany, Greece, Hungary, Italy, Malta, Namibia, Netherlands, Poland, Romania, Slovakia, Slovenia, South Africa, Sweden, Switzerland. In other countries, for example the Baltic states, the layer stays empty. Stored on the device for 14 days at most. For orientation only: not a substitute for official charts, obstacles and power lines may be missing, no effect on the game.'],
  ['Weather', 'Open-Meteo (open-meteo.com, CC BY 4.0): forecast of the weather services for the balloon’s position, hourly, on 13 pressure levels from 1000 to 250 hPa with temperature, wind and cloud cover, plus surface pressure and precipitation. The app interpolates linearly between levels and hours. Model resolution depends on the region. On long flights the weather is reloaded along the way. Humidity and dew point are not loaded.'],
  ['Weather of the championship', 'Open-Meteo Historical Forecast for 29 to 31 August 2026. This is the forecast of that time, not measured weather; the real wind may have differed.'],
  ['Terrain', 'Open-Meteo Elevation (Copernicus elevation model, about 90 m grid). The app loads a 400 m grid around the balloon and a 2 km grid farther out. Trees, buildings and power lines are not included.'],
  ['Targets and place names', 'Overpass and Nominatim (both from OpenStreetMap data): sports fields and meadows as targets, place names for launch and target. As complete as OpenStreetMap is at that place.'],
  ['Borders in the championship', 'Package world-atlas from Natural Earth, scale 1:50 million (public domain). The borders are simplified and may be off by a few kilometres. The red 10 km margin is computed from these borders. The official restricted area of the race is not included.'],
  ['Simulation', 'In simulation mode nothing is loaded from the network: weather and terrain are generated in the app.'],
  ['Important', 'The app is a game. It does not replace flight preparation, a weather briefing or an aeronautical chart.']]};
function infoOpen(){ const box = $('in-rows'); box.textContent = ''; (INFO[UI.lang] || INFO.en).forEach(r => { const h = document.createElement('h3'), p = document.createElement('p'); h.textContent = r[0]; p.textContent = r[1]; box.appendChild(h); box.appendChild(p); }); $('info').hidden = false; }
$('in-btn').addEventListener('click', infoOpen); $('in-close').addEventListener('click', () => { $('info').hidden = true; });

/* ---------- Temp als Stüve-Diagramm (STE-27): Temperatur waagerecht, Druck hoch p^0,286 senkrecht; darin sind die Trockenadiabaten Geraden ---------- */
function stuveDraw(){
  const cv = $('stuve-cv'), W = cv.clientWidth, H = cv.clientHeight; if (!W || !H) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 3); if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  const num = '600 12px "Barlow Condensed","Arial Narrow",sans-serif', small = '500 11px Barlow,"Segoe UI",sans-serif';
  const zTop = Math.min(9500, Math.max(6500, Math.ceil((B.h + 800) / 500) * 500)), a0 = atmAt(ATM, Math.min(0, B.gnd)), aT = atmAt(ATM, zTop);
  const pB = Math.ceil((a0.p / 100 + 8) / 10) * 10, pT = Math.floor(aT.p / 100 / 10) * 10, K = 0.286, yk = p => Math.pow(p, K);
  const L = 42, R = W - 58, T = 26, Bm = H - 26, y = p => T + (yk(pB) - yk(p)) / (yk(pB) - yk(pT)) * (Bm - T);
  let t0 = 1e9, t1 = -1e9; for (let z = Math.min(0, B.gnd); z <= zTop; z += 100){ const t = atmAt(ATM, z).T - 273.15; t0 = Math.min(t0, t); t1 = Math.max(t1, t); }
  t1 = Math.max(t1, B.Tg - 273.15); t0 = Math.floor((t0 - 4) / 10) * 10; t1 = Math.ceil((t1 + 4) / 10) * 10; const x = t => L + (t - t0) / (t1 - t0) * (R - L);
  c.save(); c.beginPath(); c.rect(L, T, R - L, Bm - T); c.clip();
  c.lineWidth = 1; c.strokeStyle = 'rgba(255,159,28,.42)';                                   // Trockenadiabaten: T = θ·(p/1000)^κ
  for (let th = 230; th <= 460; th += 10){ c.beginPath(); c.moveTo(x(th * Math.pow(pB / 1000, K) - 273.15), y(pB)); c.lineTo(x(th * Math.pow(pT / 1000, K) - 273.15), y(pT)); c.stroke(); }
  c.restore();
  c.font = num; c.textBaseline = 'middle';
  for (const p of [1000, 925, 850, 700, 600, 500, 400, 300, 250]){ if (p > pB || p < pT) continue; c.strokeStyle = 'rgba(154,171,196,.22)'; c.beginPath(); c.moveTo(L, y(p) + .5); c.lineTo(R, y(p) + .5); c.stroke(); c.fillStyle = '#9aabc4'; c.textAlign = 'right'; c.fillText(p, L - 4, y(p)); }
  c.textBaseline = 'alphabetic'; c.textAlign = 'center';
  for (let t = t0; t <= t1; t += 10){ c.strokeStyle = t === 0 ? 'rgba(76,201,255,.6)' : 'rgba(154,171,196,.22)'; c.beginPath(); c.moveTo(x(t) + .5, T); c.lineTo(x(t) + .5, Bm); c.stroke(); c.fillStyle = t === 0 ? '#4cc9ff' : '#9aabc4'; c.fillText(t + '°', x(t), Bm + 14); }
  c.strokeStyle = '#28395a'; c.strokeRect(L, T, R - L, Bm - T);
  c.font = small; c.fillStyle = '#9aabc4'; c.textAlign = 'left'; c.fillText('hPa', 4, 14); c.textAlign = 'center'; c.fillText(tr('st_title'), (L + R) / 2, 14); c.textAlign = 'right'; c.fillText('m · ' + UNITS[UI.unit][1], W - 4, 14);
  // Höhen in m über Grund am rechten Rand des Feldes, Wolken als heller Streifen
  c.font = num; c.textAlign = 'left'; c.textBaseline = 'middle';
  for (let z = 0; z <= zTop; z += zTop > 7000 ? 2000 : 1000){ const p = atmAt(ATM, z).p / 100; if (p < pT) break; c.fillStyle = '#9aabc4'; c.fillText(z, R + 3, y(p)); c.strokeStyle = 'rgba(154,171,196,.5)'; c.beginPath(); c.moveTo(R - 4, y(p) + .5); c.lineTo(R, y(p) + .5); c.stroke(); }
  for (let z = 0; z < zTop; z += 50){ const cc = atmAt(ATM, z + 25).c || 0; if (cc > 0.08){ const pa = atmAt(ATM, z).p / 100, pb = atmAt(ATM, z + 50).p / 100; c.fillStyle = 'rgba(238,243,250,' + (0.12 + 0.6 * cc).toFixed(2) + ')'; c.fillRect(L + 1, y(pb), 5, y(pa) - y(pb) + .6); } }
  // Temperaturkurve in den Farben der Schichtung
  const cls = g => g > 0.0005 ? 3 : g > -0.004 ? 2 : g > -0.0090 ? 1 : 0, col = ['#ff6e5f', '#eef3fa', '#5fe3a1', '#4cc9ff'];
  c.lineWidth = 2.6; c.lineCap = 'round';
  for (let z = Math.min(0, B.gnd); z < zTop; z += 50){ const a = atmAt(ATM, z), b = atmAt(ATM, z + 50); c.strokeStyle = col[cls((b.T - a.T) / 50)]; c.beginPath(); c.moveTo(x(a.T - 273.15), y(a.p / 100)); c.lineTo(x(b.T - 273.15), y(b.p / 100)); c.stroke(); }
  // Wind
  for (const p of [1000, 925, 850, 700, 600, 500, 400, 300]){ if (p > pB - 5 || p < pT) continue; let z = 0; for (let q = 0; q <= zTop; q += 50) if (atmAt(ATM, q).p / 100 >= p) z = q; const a = atmAt(ATM, z); drawBarb(c, W - 16, y(p), Math.atan2(-a.u, -a.v), Math.hypot(a.u, a.v) * 1.943844, 17); }
  // Ballon und Gastemperatur
  const ab = atmAt(ATM, B.h), yb = y(ab.p / 100), xa = x(ab.T - 273.15), xg = x(B.Tg - 273.15);
  c.strokeStyle = 'rgba(255,159,28,.8)'; c.lineWidth = 1; c.setLineDash([4, 3]); c.beginPath(); c.moveTo(L, yb); c.lineTo(R, yb); c.stroke(); c.setLineDash([]);
  c.strokeStyle = '#ffe14d'; c.lineWidth = 1.5; c.beginPath(); c.moveTo(xa, yb); c.lineTo(xg, yb); c.stroke();
  c.fillStyle = '#ffe14d'; c.beginPath(); c.moveTo(xg, yb - 6); c.lineTo(xg + 6, yb); c.lineTo(xg, yb + 6); c.lineTo(xg - 6, yb); c.closePath(); c.fill();
  c.fillStyle = '#ff9f1c'; c.strokeStyle = '#0a1019'; c.lineWidth = 2; c.beginPath(); c.arc(xa, yb, 6, 0, 7); c.fill(); c.stroke();
  c.font = small; c.fillStyle = '#eef3fa'; c.textAlign = xa > (L + R) / 2 ? 'right' : 'left'; c.textBaseline = 'alphabetic';
  c.fillText(nf(Math.round(B.h - B.gnd)) + ' m · ' + nf(ab.T - 273.15, 1) + ' °C · ' + tr('dt_dt') + ' ' + fmtV(B.Tg - ab.T) + ' K', xa > (L + R) / 2 ? R - 6 : L + 10, yb - 9);
}
$('prof').addEventListener('click', e => { const r = $('prof').getBoundingClientRect(); if (e.clientX - r.left < r.width * 0.55){ e.stopImmediatePropagation(); $('stuve').hidden = false; stuveDraw(); } }, true);
$('stuve').addEventListener('click', () => { $('stuve').hidden = true; });

/* ---------- Seitenansicht (STE-28): Ballon, Schlepptau und Gelände in Fahrtrichtung; unter 50 m über Grund von selbst, sonst über den Knopf ---------- */
const SIDE = {user: null, sand: [], puff: [], lastSand: null, t: 0, dir: [1, 0]};
function sideWanted(){ if (STATE !== 'play') return false; if (SIDE.user != null) return SIDE.user; return UI.side !== 'off' && (B.h - B.gnd) < 50; }
function sideTick(real){
  const b = $('side-btn'); b.hidden = STATE !== 'play'; const on = sideWanted(); if ($('side').hidden === on) $('side').hidden = !on; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
  const s = sandKg(B, CFG); if (SIDE.lastSand != null && SIDE.lastSand - s > 0.05 && on){ const n = Math.min(40, Math.ceil((SIDE.lastSand - s) * 2.5)); for (let i = 0; i < n; i++) SIDE.sand.push({t: -Math.random() * 0.5, x: (Math.random() - .5) * 3, v: 5 + Math.random() * 4}); } SIDE.lastSand = s;
  if (valve > 0 && on && Math.random() < 0.25 + valve * 0.6) SIDE.puff.push({t: 0, x: (Math.random() - .5) * 3, s: 0.6 + valve});
  if (!on){ SIDE.sand.length = 0; SIDE.puff.length = 0; return; }
  SIDE.sand.forEach(p => { p.t += real; }); SIDE.sand = SIDE.sand.filter(p => p.t < 3); SIDE.puff.forEach(p => { p.t += real; }); SIDE.puff = SIDE.puff.filter(p => p.t < 1.4);
  sideDraw();
}
function sideDraw(){
  const cv = $('side-cv'), W = cv.clientWidth, H = cv.clientHeight; if (!W || !H) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 3); if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  const agl = Math.max(0, B.h - B.gnd), night = (B.sun == null ? 1 : B.sun) <= 0; c.fillStyle = night ? '#0c1830' : '#14315a'; c.fillRect(0, 0, W, H);
  const span = Math.max(70, agl * 1.3 + 30), m = (H - 26) / span;                              // m je Bild senkrecht, Maßstab px je m (waagerecht derselbe)
  const sp = Math.hypot(B.gu || 0, B.gv || 0); if (sp > 0.3) SIDE.dir = [B.gu / sp, B.gv / sp]; else if (!B.air){ const a = atmAt(ATM, 100), w = Math.hypot(a.u, a.v); if (w > 0.3) SIDE.dir = [a.u / w, a.v / w]; }
  const bx = W * 0.36, yOf = z => H - 18 - (z - B.gnd) * m - 8 * 0, gz = d => TER.on ? terAt(B.e + d * SIDE.dir[0], B.n + d * SIDE.dir[1]) : B.gnd;
  // Gelände in Fahrtrichtung
  const N = 44, pts = []; for (let i = 0; i <= N; i++){ const X = i / N * W, d = (X - bx) / m; pts.push([X, yOf(i === Math.round(bx / W * N) ? B.gnd : gz(d))]); }
  c.fillStyle = night ? '#16302a' : '#234a3a'; c.beginPath(); c.moveTo(0, H); pts.forEach(p => c.lineTo(p[0], Math.min(H, p[1]))); c.lineTo(W, H); c.closePath(); c.fill();
  c.strokeStyle = '#5fe3a1'; c.lineWidth = 1.5; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke();
  // Ballon: Größe maßstäblich, aber nie kleiner als ein Symbol; die Form folgt dem Füllgrad
  const fI = fillNow(), Dm = Math.cbrt(6 * CFG.vol / Math.PI), r = Math.max(9, Dm * m / 2), yBask = yOf(B.h), bh = Math.max(4, 1.3 * m), bw = Math.max(5, 1.5 * m), cy = yBask - bh - r * 1.55;
  c.strokeStyle = '#c9d6e8'; c.lineWidth = 1; c.beginPath(); c.moveTo(bx - r * 0.72, cy + r * 0.7); c.lineTo(bx - bw / 2, yBask - bh); c.moveTo(bx + r * 0.72, cy + r * 0.7); c.lineTo(bx + bw / 2, yBask - bh); c.stroke();
  const slack = 1 - fI, wB = r * (1 - 0.75 * slack), yB = cy + r * (1 + 0.25 * slack);          // schlaffe Hülle: unten schmal und etwas länger
  c.fillStyle = '#f4f1ea'; c.strokeStyle = '#0a1019'; c.lineWidth = 1.2; c.beginPath(); c.arc(bx, cy, r, Math.PI, 0); c.bezierCurveTo(bx + r, cy + r * 0.6, bx + wB, cy + r * (0.9 - 0.3 * slack), bx + Math.max(1.5, wB * 0.25), yB); c.lineTo(bx - Math.max(1.5, wB * 0.25), yB); c.bezierCurveTo(bx - wB, cy + r * (0.9 - 0.3 * slack), bx - r, cy + r * 0.6, bx - r, cy); c.closePath(); c.fill(); c.stroke();
  c.fillStyle = '#b98a4a'; c.fillRect(bx - bw / 2, yBask - bh, bw, bh); c.strokeRect(bx - bw / 2, yBask - bh, bw, bh);
  // Schlepptau: hängt bis zum Boden, der Rest liegt hinter dem Ballon auf
  if (B.rope){ const hang = Math.min(CFG.ropeLen, agl), lie = CFG.ropeLen - hang; c.strokeStyle = '#d9b36c'; c.lineWidth = Math.max(1.5, 0.25 * m); c.lineCap = 'round'; c.beginPath(); c.moveTo(bx + bw / 2, yBask - 1);
    if (lie <= 0) c.lineTo(bx + bw / 2 - 2, yBask + hang * m);
    else { const x0 = bx - Math.min(6, hang * m * 0.4); c.quadraticCurveTo(bx + bw / 2, yOf(B.gnd) - 1, x0, yOf(gz((x0 - bx) / m)) - 1); for (let d = 2; d <= lie; d += 2){ const X = x0 - d * m; if (X < 0) break; c.lineTo(X, yOf(gz((X - bx) / m)) - 1); } }
    c.stroke(); }
  // Sand rieselt, Gas tritt am Ventil aus
  c.fillStyle = '#ffe14d'; SIDE.sand.forEach(p => { if (p.t < 0) return; const fall = p.v * p.t + 4.9 * p.t * p.t, Y = yBask + Math.min(fall * Math.max(m, 0.8), yOf(B.gnd) - yBask); c.fillRect(bx - bw / 2 - 2 + p.x, Y, 1.6, 1.6); });
  SIDE.puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,' + (0.9 - p.t / 1.6).toFixed(2) + ')'; c.lineWidth = 1.4; c.beginPath(); c.arc(bx + p.x * (1 + p.t * 2), cy - r - 3 - p.t * 14 * p.s, 2 + p.t * 5, 0, 7); c.stroke(); });
  // Höhe über Grund und Maßstab
  c.strokeStyle = 'rgba(238,243,250,.55)'; c.lineWidth = 1; c.setLineDash([2, 3]); c.beginPath(); c.moveTo(bx + bw / 2 + 9, yBask); c.lineTo(bx + bw / 2 + 9, yOf(B.gnd)); c.stroke(); c.setLineDash([]);
  c.font = '600 15px "Barlow Condensed","Arial Narrow",sans-serif'; c.fillStyle = '#eef3fa'; c.textAlign = 'left'; c.textBaseline = 'middle'; if (agl > 1.5) c.fillText(nf(Math.round(agl)) + ' m', bx + bw / 2 + 13, Math.min(H - 26, (yBask + yOf(B.gnd)) / 2));
  const bar = [10, 20, 50, 100, 200, 500, 1000, 2000].find(v => v * m >= 34) || 5000; c.strokeStyle = '#9aabc4'; c.beginPath(); c.moveTo(W - 8 - bar * m, H - 7); c.lineTo(W - 8, H - 7); c.moveTo(W - 8 - bar * m, H - 10); c.lineTo(W - 8 - bar * m, H - 4); c.moveTo(W - 8, H - 10); c.lineTo(W - 8, H - 4); c.stroke();
  c.font = '500 10px Barlow,"Segoe UI",sans-serif'; c.fillStyle = '#9aabc4'; c.textAlign = 'right'; c.textBaseline = 'alphabetic'; c.fillText(bar >= 1000 ? bar / 1000 + ' km' : bar + ' m', W - 10, H - 11);
  c.textAlign = 'left'; c.fillText('→ ' + deg3((Math.atan2(SIDE.dir[0], SIDE.dir[1]) * 180 / Math.PI + 360) % 360) + '°', 6, 13);
}
$('side').addEventListener('click', () => { SIDE.user = false; });
$('side-btn').addEventListener('click', () => { SIDE.user = !sideWanted(); });

/* ---------- Ballon im Detail (STE-26) ---------- */'''
f.rep("/* ---------- Ballon im Detail (STE-26) ---------- */", js)
f.rep("  pvTick(real);\n","  pvTick(real); sideTick(real); if (!$('stuve').hidden) stuveDraw();\n")
f.rep("function resetRun(){\n","function resetRun(){\n  if (typeof SIDE !== 'undefined'){ SIDE.user = null; SIDE.lastSand = null; SIDE.sand.length = 0; SIDE.puff.length = 0; }\n")
f.rep("bindSeg('seg-map', UI.map, v => { UI.map = v; saveUI(); applyTiles(); });","bindSeg('seg-map', UI.map, v => { UI.map = v; saveUI(); applyTiles(); });\nbindSeg('seg-ofm', UI.ofm ? 1 : 0, v => { UI.ofm = +v; saveUI(); applyOfm(true); });\nbindSeg('seg-side', UI.side || 'auto', v => { UI.side = v; saveUI(); SIDE.user = null; });")
f.rep("applyLang(); applyTiles(); renderSand(true); showMenu();","applyLang(); applyTiles(); applyOfm(false); renderSand(true); showMenu();")
f.rep("const BUILD = '2026-10-10.1'","const BUILD = '2026-10-10.2'")
f.save()
# ================= Service Worker: Luftfahrtkarte mit eigenem Zwischenspeicher für 14 Tage =================
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read()
def rep(a,b):
    global s; assert s.count(a)==1,a; s=s.replace(a,b)
rep("const VER = 'v33';","const VER = 'v34';")
rep("const LIB_HOST =","const OFM_HOST = /(^|\\.)(newaydata\\.com)$/;                   // open flightmaps: Luftfahrtdaten dürfen nicht lange veralten\nconst ofmName = () => 'gb-ofm-' + Math.floor(Date.now() / (14 * 864e5));   // alle 14 Tage ein neuer Zwischenspeicher\nconst LIB_HOST =")
rep("![SHELL, LIBS, TILES].includes(k)","![SHELL, LIBS, TILES, ofmName()].includes(k)")
rep("  if (TILE_HOST.test(url.hostname)) { e.respondWith(tile(req)); return; }","  if (TILE_HOST.test(url.hostname)) { e.respondWith(tile(req)); return; }\n  if (OFM_HOST.test(url.hostname)) { e.respondWith(ofmTile(req)); return; }")
s+='''
async function ofmTile(req) {                       // Lufträume: eigener Zwischenspeicher je 14 Tage; ältere werden gelöscht
  const name = ofmName();
  caches.keys().then(ks => ks.forEach(k => { if (k.startsWith('gb-ofm-') && k !== name) caches.delete(k); }));
  const cache = await caches.open(name);
  const hit = await cache.match(req.url);
  if (hit) return hit;
  try {
    const res = await fetch(req.url, {mode: 'cors', credentials: 'omit'});
    if (res.ok) cache.put(req.url, res.clone()).then(() => trim(cache));
    return res;
  } catch (err) {
    try { return await fetch(req); } catch (e2) { return Response.error(); }
  }
}
'''
open(p,'w').write(s)
