import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
gb=open('/home/claude/w/gb.js',encoding='utf-8').read()
# ---------- Kern: Archiv-Wetter ----------
f.rep("function wxUrl(lat, lon, lite){","function wxUrl(lat, lon, lite, hist){                     // hist: Zeitpunkt in ms für das Archiv der Vorhersagen (Meisterschaft), sonst die laufende Vorhersage")
f.rep("  return 'https://api.open-meteo.com/v1/forecast?latitude=' + lat.toFixed(4) + '&longitude=' + lon.toFixed(4) + '&hourly=' + h.join(',') + '&wind_speed_unit=ms&timezone=UTC&forecast_days=3';",
"""  const day = ms => new Date(ms).toISOString().slice(0, 10);
  return (hist ? 'https://historical-forecast-api.open-meteo.com' : 'https://api.open-meteo.com') + '/v1/forecast?latitude=' + lat.toFixed(4) + '&longitude=' + lon.toFixed(4) + '&hourly=' + h.join(',') + '&wind_speed_unit=ms&timezone=UTC' +
    (hist ? '&start_date=' + day(hist) + '&end_date=' + day(hist + 2 * 864e5) : '&forecast_days=3');""")
# ---------- Oberfläche ----------
f.rep("const TASK = () => UI.mode === 'challenge' ? (UI.task || 'target') : 'free';","const TASK = () => UI.mode === 'challenge' ? (UI.task || 'target') : UI.mode === 'champ' ? 'gb' : 'free';")
f.rep("async function loadWx(lat, lon, useCache){","async function loadWx(lat, lon, useCache, hist){            // hist: {t} lädt das Archiv der Vorhersagen für diesen Zeitpunkt")
f.rep("    let r = await fetch(wxUrl(lat, lon), {signal: ac.signal});\n    if (!r.ok && r.status >= 400 && r.status < 500) r = await fetch(wxUrl(lat, lon, true), {signal: ac.signal});",
      "    const ht = hist ? hist.t : 0;\n    let r = await fetch(wxUrl(lat, lon, false, ht), {signal: ac.signal});\n    if (!r.ok && r.status >= 400 && r.status < 500) r = await fetch(wxUrl(lat, lon, true, ht), {signal: ac.signal});")
f.rep("    const m = wxParse(await r.json(), Date.now()); if (!m) throw new Error('parse');","    const m = wxParse(await r.json(), hist ? hist.t : Date.now()); if (!m) throw new Error('parse');")
f.rep("function wxStart(){ WXRUN.clock0 = Date.now();","function wxStart(){ WXRUN.clock0 = isGB() ? GB.t0 : Date.now();")
f.rep("    loadWx(q[0], q[1], false).then(m => {","    loadWx(q[0], q[1], false, isGB() ? {t: WXRUN.clock0 + B.t * 1000} : null).then(m => {")
f.rep("      if (sim > m.hours[m.hours.length - 1].t) m.hours.forEach(h => { h.t += sim - Date.now(); });","      if (!isGB() && sim > m.hours[m.hours.length - 1].t) m.hours.forEach(h => { h.t += sim - Date.now(); });")
f.rep("async function prepareRun(){\n  const k = TASK();\n","async function prepareRun(){\n  const k = TASK();\n  if (k === 'gb') return gbPrepare();\n  gbLeave();\n")
f.rep("function showMenu(){\n","function showMenu(){\n  gbLeave();\n")
f.rep("$('sw-back').addEventListener('click', () => openSetup(UI.mode));","$('sw-back').addEventListener('click', () => isGB() ? showMenu() : openSetup(UI.mode));")
f.rep("  if (k === 'mdt' || k === 'mid') return {e: 0, n: 0, lbl: tr('launch'), zoom: false};","  if (k === 'mdt' || k === 'mid') return {e: 0, n: 0, lbl: tr('launch'), zoom: false};\n  if (k === 'gb') return {e: (GB.start.lon - START.lon) * klon(), n: (GB.start.lat - START.lat) * KLAT, lbl: tr('launch'), zoom: false, km: gbKm()};")
f.rep("$('i-tdist').textContent = fmtD(Math.hypot(de, dn));","$('i-tdist').textContent = np.km != null ? nf(np.km, 1) + ' km' : fmtD(Math.hypot(de, dn));")
f.rep("$('i-tbrg').textContent = deg3((Math.atan2(de, dn) * 180 / Math.PI + 360) % 360); }","$('i-tbrg').textContent = deg3((Math.atan2(de, dn) * 180 / Math.PI + 360) % 360); }\n  { const z = k === 'gb' && GB.zone != null && GB.zone < 100000 && STATE === 'play'; $('row-zone').hidden = !z; if (z){ const el = $('i-zone'); el.textContent = nf(Math.max(0, (GB.zone - GB.buffer) / 1000), 0) + ' km'; el.style.color = GB.zone < 30000 ? 'var(--dn)' : 'var(--warn)'; } }")
f.rep("  const lim = LIMITS[k] || 0; $('timer').hidden = !lim || (STATE !== 'play' && STATE !== 'done');","  const lim = LIMITS[k] || 0; $('timer').hidden = (!lim && k !== 'gb') || (STATE !== 'play' && STATE !== 'done');\n  $('tm-lbl').textContent = k === 'gb' ? gbClock().toISOString().slice(8, 10) + '.' + gbClock().toISOString().slice(5, 7) + '. MESZ' : tr('tm_left');\n  if (k === 'gb'){ const tv = $('tm-val'); tv.textContent = gbClock().toISOString().slice(11, 16); tv.style.color = 'var(--tx)'; }\n  $('gb-save').hidden = !(k === 'gb' && STATE === 'play'); $('btn-500').hidden = !(k === 'gb' && STATE === 'play');")
f.rep('<div class="card" id="timer" hidden><span data-i="tm_left"></span><b id="tm-val">00:00:00</b></div>','<div class="card" id="timer" hidden><span id="tm-lbl"></span><b id="tm-val">00:00:00</b></div>\n        <button class="sm" id="gb-save" hidden data-i="gb_save"></button>')
f.rep('        <div class="kv gasaid" hidden><span>m³</span><b id="i-gas">–</b></div>','        <div class="kv" id="row-zone" hidden><span data-i="gb_zone"></span><b id="i-zone">–</b></div>\n        <div class="kv gasaid" hidden><span>m³</span><b id="i-gas">–</b></div>')
# Zeitraffer 500× und Zeitschleife
s=f.s; a=s.index('<div class="seg" id="seg-speed"'); b=s.index('</div>',a); assert '100×</button>' in s[a:b]
f.s=s[:b]+'<button id="btn-500" hidden data-ia="gb_500_a" aria-label="500×">500×</button>'+s[b:]
f.rep("let simDt = real * (valve > 0 ? 1 : UI.speed);","let simDt = real * (valve > 0 ? 1 : GB.hold && isGB() ? 500 : UI.speed);")
f.rep("    stepMarkers(adv);\n    if (Math.hypot(B.e - lastPathE, B.n - lastPathN) > 25){","    stepMarkers(adv);\n    if (isGB() && !B.landed) gbTick(real);\n    if (Math.hypot(B.e - lastPathE, B.n - lastPathN) > (isGB() ? 400 : 25)){")
f.rep("function setState(s){ STATE = s;","function setState(s){ STATE = s; $('app').classList.toggle('gb', UI.mode === 'champ' && (s === 'play' || s === 'done' || s === 'brief'));")
f.rep("#app.home #btn-menu{display:none}","#app.home #btn-menu{display:none}\n#app.gb #seg-speed button[data-v=\"5\"]{display:none}\n#btn-500{touch-action:none;user-select:none;-webkit-user-select:none}\n#btn-500[hidden]{display:none}\n#gb-save{background:var(--pan);min-height:40px}\n.gbtip{font-size:10.5px;padding:0 4px;opacity:.9}\ntable.gbres td{font-size:13px;padding:3px 4px}\ntable.gbres td:nth-child(3){font-family:var(--ui);font-size:12px;color:var(--mut);font-weight:400}\ntable.gbres td:nth-child(4){text-align:right;font-weight:700;color:var(--tx)}\ntable.gbres tr.me td{background:rgba(255,159,28,.18);color:var(--orb)}\n#r-list{max-height:210px;overflow:auto;margin:6px 0;border:1px solid var(--line);border-radius:8px}\n#r-list[hidden]{display:none}\n#sc-kind{margin-bottom:8px}")
# Startfenster
f.rep("  } else if (k === 'mid') tg = tr('sw_mid');","  } else if (k === 'mid') tg = tr('sw_mid');\n  else if (k === 'gb') tg = tr('gb_story');")
f.rep("  $('sw-note').textContent = B.ok ? tr('sw_note') : '';","  $('sw-note').textContent = B.ok ? (k === 'gb' ? tr('gb_rules') : tr('sw_note')) : '';")
# Auswertung
f.rep('        <p class="note" id="r-note" hidden></p>','        <div id="r-list" hidden></div>\n        <p class="note" id="r-note" hidden></p>')
f.rep("  } else if (k === 'mid'){\n    const r = scoreMid(dStart, B.t, LIMITS.mid); pts = r.pts;","  } else if (k === 'gb'){\n    gbRes = gbResult(rows); note = (gbRes.verdict ? gbRes.verdict + ' ' : '') + tr('gb_note');\n  } else if (k === 'mid'){\n    const r = scoreMid(dStart, B.t, LIMITS.mid); pts = r.pts;")
f.rep("  cheerQ = 0.5; const k = TASK(), rows = [], dStart = Math.hypot(B.e, B.n); let pts = null, note = '';","  cheerQ = 0.5; const k = TASK(), rows = [], dStart = Math.hypot(B.e, B.n); let pts = null, note = '', gbRes = null;")
f.rep("  $('r-ptsrow').hidden = pts == null;","  { const bx = $('r-list'); bx.textContent = ''; bx.hidden = !gbRes; if (gbRes) gbTable(bx, gbRes); }\n  $('r-ptsrow').hidden = pts == null;")
f.rep("SND.land(B.vLand); if (B.vLand < LAND_HARD) SND.cheer(cheerQ); renderSand(true);","if (!(k === 'gb' && GB.dq)){ SND.land(B.vLand); if (B.vLand < LAND_HARD) SND.cheer(cheerQ); } renderSand(true);")
f.rep("  $('r-head').textContent = tr(landClass(B.vLand));                                       // Rückmeldung zur Landung (PUN-08)\n","  $('r-head').textContent = tr(landClass(B.vLand));                                       // Rückmeldung zur Landung (PUN-08)\n", 1)
# r-head/r-line werden in gbResult überschrieben: Reihenfolge sichern
s=f.s; i=s.index("  $('r-line').textContent = fmtD(dStart);"); j=s.index("  if (k === 'target' && TARGET){\n    const d = Math.hypot(TARGET.e - B.e", i); assert j>i
# Hauptmenü zurück in der Luft: Meisterschaft speichert
f.rep("  if (STATE === 'play' && B.air && !B.landed && !(await confirmBox(tr('cf_menu'), tr('cf_menu_ok')))) return;\n  if (typeof gpsStop","  if (STATE === 'play' && B.air && !B.landed && !(await confirmBox(tr(isGB() ? 'gb_menu_q' : 'cf_menu'), tr('cf_menu_ok')))) return;\n  if (isGB()) gbSave(true);\n  if (typeof gpsStop")
# Menü: Wettkampf ausblenden, Meisterschaft freischalten
f.rep('        <button class="mbtn" disabled><em data-i="soon"></em><b data-i="m_comp"></b><span data-i="m_comp_d"></span></button>\n','')
f.rep('        <button class="mbtn" disabled><em data-i="soon"></em><b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>','        <button class="mbtn" id="m-champ"><b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>')
# Bestenliste mit zweiter Liste
f.rep('        <div id="sc-list"></div>','        <div class="seg wide" id="sc-kind"><button data-v="chal" class="on" data-i="sc_chal"></button><button data-v="gb" data-i="gb_list"></button></div>\n        <div id="sc-list"></div>')
f.rep("async function showScores(){\n  setState('scores'); const box = $('sc-list'); box.textContent = '';","""let scKind = 'chal';
document.querySelectorAll('#sc-kind button').forEach(b => b.addEventListener('click', () => { scKind = b.dataset.v; showScores(); }));
async function showScores(){
  setState('scores'); const box = $('sc-list'); box.textContent = '';
  document.querySelectorAll('#sc-kind button').forEach(b => b.classList.toggle('on', b.dataset.v === scKind));
  if (scKind === 'gb'){                                    // Liste „69. Gordon Bennett“: alle Fahrten dieses Geräts, auch mehrere je Spieler
    const g = gbList(); if (!g.length){ const q = document.createElement('p'); q.className = 'note'; q.textContent = tr('sc_empty'); box.appendChild(q); return; }
    const tb = document.createElement('table'); tb.className = 'sc';
    const row = (cells, tag) => { const r = document.createElement('tr'); cells.forEach(c => { const x = document.createElement(tag); x.textContent = c; r.appendChild(x); }); tb.appendChild(r); };
    row([tr('sc_rank'), tr('name_lbl'), 'km', tr('gb_col_rank')], 'th');
    g.forEach((e, i) => row([i + 1, e.n, nf(e.km, 1), e.dq ? 'DSQ' : tr('gb_of', {r: e.rank})], 'td'));
    box.appendChild(tb); return;
  }""")
f.rep("$('m-score').addEventListener('click', showScores);","$('m-score').addEventListener('click', () => showScores());")
# Musik deutlich leiser
f.rep("    mus.g.gain.value = 1; mus.g.connect(master);","    mus.g.gain.value = 0.3; mus.g.connect(master);")
f.rep("g.setValueAtTime(1, t0); g.setValueAtTime(1, t0 + 8); g.linearRampToValueAtTime(0.45, t0 + 14); }","g.setValueAtTime(0.3, t0); g.setValueAtTime(0.3, t0 + 8); g.linearRampToValueAtTime(0.14, t0 + 14); }")
# Baustein einfügen
f.rep("/* ---------- Zeitschleife ---------- */", gb+"\n/* ---------- Zeitschleife ---------- */")
T={'de':dict(m_champ_d='69. Gordon Bennett 2026 nachfahren: ab Gladbeck gegen die 23 echten Teams',st_name_gb='Gladbeck, 29.08.2026, 02:45 Uhr',
 gb_story='Nachfahrt des 69. Coupe Aéronautique Gordon Bennett. 23 Teams sind in der Nacht zum 29. August 2026 in Gladbeck gestartet. Als 25. Team tritt spontan Jamaika an: die CoolRidings, und das bist du. Du startest als Letzter. Wer am weitesten vom Startplatz landet, gewinnt.',
 gb_rules='Rot auf der Karte: gesperrte Länder (Russland, Belarus, Ukraine, Moldau, Afrika, Naher Osten). Wer näher als 10 km herankommt oder im Wasser landet, ist disqualifiziert. 500× läuft nur, solange der Knopf gedrückt ist. Zum Abheben zwei Säcke abwerfen.',
 gb_data='Die Meisterschaft lädt das Wetter des Renntages und die Karte entlang der ganzen Strecke. Das können einige zehn MB werden, vor allem durch die Karte. Eine WLAN-Verbindung wird empfohlen.',gb_go='Starten',gb_busy_zone='Sperrzonen werden geladen …',
 gb_nozone='Die Ländergrenzen für die Sperrzonen ließen sich nicht laden. Bitte mit Netz noch einmal versuchen.',gb_nowx='Das Wetter des Renntages ließ sich nicht laden. Bitte mit Netz noch einmal versuchen.',gb_zone='Sperrzone',gb_zone_near='Achtung: Sperrzone in {km} km',
 gb_km='Entfernung vom Start',gb_rank='Dein Platz',gb_of='Platz {r} von 24',gb_col_rank='Im Rennen',gb_dq_head='Disqualifiziert',gb_dq_zone='in die Sperrzone eingefahren',gb_dq_water='im Wasser gelandet',
 gb_v_top='Aufs Podium gefahren: besser als fast alle echten Teams.',gb_v_good='Ein guter Platz im vorderen Drittel.',gb_v_mid='Mittelfeld: Da geht noch mehr.',gb_v_low='Hinteres Feld: Die echten Teams waren weiter.',gb_ahead='{a} Teams liegen vor dir, {b} hinter dir.',
 gb_note='Gestrichelt auf der Karte: Start und Landeort der echten Teams, nicht ihr Fahrtweg.',gb_save='Speichern',gb_saved='Spielstand gespeichert',gb_saveq='Du spielst seit 30 Minuten ohne Zwischenspeichern. Jetzt speichern?',
 gb_resume_q='Es gibt einen gespeicherten Spielstand: {km} km vom Start, Fahrzeit {t}. Fortsetzen?',gb_resume='Fortsetzen',gb_new='Neu starten',gb_resumed='Spielstand geladen. Die Fahrt ist angehalten.',gb_menu_q='Zum Hauptmenü? Die Fahrt wird gespeichert und lässt sich fortsetzen.',
 gb_offline='Achtung: keine Verbindung mehr. Ohne Netz fehlen neues Wetter und neue Kartenteile. Weiterfahren?',gb_wifi='Achtung: WLAN weg, die App lädt jetzt über das Mobilfunknetz. Weiterfahren?',gb_cont='Weiterfahren',gb_list='69. Gordon Bennett',gb_500_a='Zeitraffer 500×, solange gedrückt'),
'en':dict(m_champ_d='Re-fly the 69th Gordon Bennett 2026: from Gladbeck against the 23 real teams',st_name_gb='Gladbeck, 29 Aug 2026, 02:45 CEST',
 gb_story='A re-flight of the 69th Coupe Aéronautique Gordon Bennett. 23 teams launched from Gladbeck in the night to 29 August 2026. Jamaica enters spontaneously as the 25th team: the CoolRidings, and that is you. You launch last. Whoever lands farthest from the launch site wins.',
 gb_rules='Red on the map: prohibited countries (Russia, Belarus, Ukraine, Moldova, Africa, Middle East). Coming closer than 10 km or landing in water means disqualification. 500× only runs while the button is held. Drop two bags to lift off.',
 gb_data='The championship loads the weather of the race day and the map along the whole route. That can be several tens of MB, mostly map tiles. A Wi-Fi connection is recommended.',gb_go='Start',gb_busy_zone='Loading prohibited zones …',
 gb_nozone='The country borders for the prohibited zones could not be loaded. Please try again with a connection.',gb_nowx='The weather of the race day could not be loaded. Please try again with a connection.',gb_zone='No-fly zone',gb_zone_near='Warning: prohibited zone in {km} km',
 gb_km='Distance from launch',gb_rank='Your place',gb_of='Place {r} of 24',gb_col_rank='In the race',gb_dq_head='Disqualified',gb_dq_zone='entered a prohibited zone',gb_dq_water='landed in water',
 gb_v_top='On the podium: better than almost all real teams.',gb_v_good='A good place in the top third.',gb_v_mid='Midfield: there is more in it.',gb_v_low='Back of the field: the real teams went farther.',gb_ahead='{a} teams are ahead of you, {b} behind.',
 gb_note='Dashed on the map: launch and landing site of the real teams, not their track.',gb_save='Save',gb_saved='Game saved',gb_saveq='You have been playing for 30 minutes without saving. Save now?',
 gb_resume_q='There is a saved game: {km} km from launch, flight time {t}. Continue?',gb_resume='Continue',gb_new='Start anew',gb_resumed='Saved game loaded. The flight is paused.',gb_menu_q='Go to the main menu? The flight is saved and can be continued.',
 gb_offline='Warning: no connection. Without a network, new weather and new map tiles are missing. Keep flying?',gb_wifi='Warning: Wi-Fi lost, the app now loads over mobile data. Keep flying?',gb_cont='Keep flying',gb_list='69th Gordon Bennett',gb_500_a='Time lapse 500× while held'),
'fr':dict(m_champ_d='Revivre la 69e Gordon Bennett 2026 : depuis Gladbeck face aux 23 vraies équipes',st_name_gb='Gladbeck, 29.08.2026, 02 h 45',
 gb_story='Reprise de la 69e Coupe Aéronautique Gordon Bennett. 23 équipes ont décollé de Gladbeck dans la nuit du 29 août 2026. La Jamaïque s’inscrit à l’improviste comme 25e équipe : les CoolRidings, c’est vous. Vous décollez en dernier. L’équipe qui atterrit le plus loin du départ gagne.',
 gb_rules='En rouge sur la carte : pays interdits (Russie, Biélorussie, Ukraine, Moldavie, Afrique, Moyen-Orient). S’en approcher à moins de 10 km ou atterrir dans l’eau entraîne la disqualification. 500× ne fonctionne que tant que le bouton est maintenu. Lâchez deux sacs pour décoller.',
 gb_data='Le championnat charge la météo du jour de course et la carte sur tout le trajet. Cela peut représenter plusieurs dizaines de Mo, surtout pour la carte. Une connexion Wi-Fi est recommandée.',gb_go='Démarrer',gb_busy_zone='Chargement des zones interdites …',
 gb_nozone='Les frontières des zones interdites n’ont pas pu être chargées. Réessayez avec une connexion.',gb_nowx='La météo du jour de course n’a pas pu être chargée. Réessayez avec une connexion.',gb_zone='Zone interdite',gb_zone_near='Attention : zone interdite à {km} km',
 gb_km='Distance depuis le départ',gb_rank='Votre place',gb_of='Place {r} sur 24',gb_col_rank='En course',gb_dq_head='Disqualifié',gb_dq_zone='entrée dans une zone interdite',gb_dq_water='atterrissage dans l’eau',
 gb_v_top='Sur le podium : mieux que presque toutes les vraies équipes.',gb_v_good='Une bonne place dans le premier tiers.',gb_v_mid='Milieu de classement : on peut faire mieux.',gb_v_low='Fin de classement : les vraies équipes sont allées plus loin.',gb_ahead='{a} équipes devant vous, {b} derrière.',
 gb_note='En pointillé sur la carte : départ et lieu d’atterrissage des vraies équipes, pas leur trajet.',gb_save='Enregistrer',gb_saved='Partie enregistrée',gb_saveq='Vous jouez depuis 30 minutes sans enregistrer. Enregistrer maintenant ?',
 gb_resume_q='Une partie est enregistrée : {km} km du départ, durée de vol {t}. Continuer ?',gb_resume='Continuer',gb_new='Recommencer',gb_resumed='Partie chargée. Le vol est en pause.',gb_menu_q='Retour au menu principal ? Le vol est enregistré et pourra être repris.',
 gb_offline='Attention : plus de connexion. Sans réseau, la nouvelle météo et les nouvelles tuiles manquent. Continuer le vol ?',gb_wifi='Attention : Wi-Fi perdu, l’application charge maintenant par le réseau mobile. Continuer le vol ?',gb_cont='Continuer le vol',gb_list='69e Gordon Bennett',gb_500_a='Accéléré 500× tant que maintenu'),
'pl':dict(m_champ_d='Przeleć 69. Gordon Bennett 2026: z Gladbeck przeciw 23 prawdziwym załogom',st_name_gb='Gladbeck, 29.08.2026, 02:45',
 gb_story='Powtórka 69. Coupe Aéronautique Gordon Bennett. 23 załogi wystartowały z Gladbeck w nocy na 29 sierpnia 2026. Jako 25. załoga spontanicznie startuje Jamajka: CoolRidings, czyli ty. Startujesz ostatni. Wygrywa ten, kto wyląduje najdalej od miejsca startu.',
 gb_rules='Na czerwono na mapie: kraje zakazane (Rosja, Białoruś, Ukraina, Mołdawia, Afryka, Bliski Wschód). Zbliżenie na mniej niż 10 km lub lądowanie w wodzie oznacza dyskwalifikację. 500× działa tylko, gdy przycisk jest wciśnięty. Aby wystartować, zrzuć dwa worki.',
 gb_data='Mistrzostwa pobierają pogodę z dnia wyścigu i mapę wzdłuż całej trasy. To może być kilkadziesiąt MB, głównie mapa. Zalecane jest połączenie Wi-Fi.',gb_go='Start',gb_busy_zone='Wczytywanie stref zakazanych …',
 gb_nozone='Nie udało się wczytać granic stref zakazanych. Spróbuj ponownie z dostępem do sieci.',gb_nowx='Nie udało się wczytać pogody z dnia wyścigu. Spróbuj ponownie z dostępem do sieci.',gb_zone='Strefa zakazana',gb_zone_near='Uwaga: strefa zakazana za {km} km',
 gb_km='Odległość od startu',gb_rank='Twoje miejsce',gb_of='Miejsce {r} z 24',gb_col_rank='W wyścigu',gb_dq_head='Dyskwalifikacja',gb_dq_zone='wlot w strefę zakazaną',gb_dq_water='lądowanie w wodzie',
 gb_v_top='Na podium: lepiej niż prawie wszystkie prawdziwe załogi.',gb_v_good='Dobre miejsce w czołówce.',gb_v_mid='Środek stawki: stać cię na więcej.',gb_v_low='Koniec stawki: prawdziwe załogi doleciały dalej.',gb_ahead='{a} załóg przed tobą, {b} za tobą.',
 gb_note='Linia przerywana na mapie: start i miejsce lądowania prawdziwych załóg, nie ich trasa.',gb_save='Zapisz',gb_saved='Stan gry zapisany',gb_saveq='Grasz od 30 minut bez zapisu. Zapisać teraz?',
 gb_resume_q='Jest zapisany stan gry: {km} km od startu, czas lotu {t}. Kontynuować?',gb_resume='Kontynuuj',gb_new='Zacznij od nowa',gb_resumed='Wczytano stan gry. Lot jest wstrzymany.',gb_menu_q='Przejść do menu głównego? Lot zostanie zapisany i można go kontynuować.',
 gb_offline='Uwaga: brak połączenia. Bez sieci zabraknie nowej pogody i nowych fragmentów mapy. Lecieć dalej?',gb_wifi='Uwaga: brak Wi-Fi, aplikacja pobiera teraz przez sieć komórkową. Lecieć dalej?',gb_cont='Leć dalej',gb_list='69. Gordon Bennett',gb_500_a='Przyspieszenie 500×, gdy wciśnięty'),
'cs':dict(m_champ_d='Zaleťte si 69. Gordon Bennett 2026: z Gladbecku proti 23 skutečným týmům',st_name_gb='Gladbeck, 29. 8. 2026, 02:45',
 gb_story='Opakování 69. Coupe Aéronautique Gordon Bennett. 23 týmů odstartovalo z Gladbecku v noci na 29. srpna 2026. Jako 25. tým se spontánně hlásí Jamajka: CoolRidings, a to jste vy. Startujete poslední. Vyhrává, kdo přistane nejdál od místa startu.',
 gb_rules='Červeně na mapě: zakázané země (Rusko, Bělorusko, Ukrajina, Moldavsko, Afrika, Blízký východ). Přiblížení na méně než 10 km nebo přistání ve vodě znamená diskvalifikaci. 500× běží jen při stisknutém tlačítku. Ke startu shoďte dva pytle.',
 gb_data='Mistrovství načítá počasí závodního dne a mapu podél celé trasy. Mohou to být desítky MB, hlavně kvůli mapě. Doporučuje se připojení Wi-Fi.',gb_go='Start',gb_busy_zone='Načítají se zakázané zóny …',
 gb_nozone='Hranice zakázaných zón se nepodařilo načíst. Zkuste to znovu s připojením.',gb_nowx='Počasí závodního dne se nepodařilo načíst. Zkuste to znovu s připojením.',gb_zone='Zakázaná zóna',gb_zone_near='Pozor: zakázaná zóna za {km} km',
 gb_km='Vzdálenost od startu',gb_rank='Vaše místo',gb_of='{r}. místo z 24',gb_col_rank='V závodě',gb_dq_head='Diskvalifikace',gb_dq_zone='vlet do zakázané zóny',gb_dq_water='přistání ve vodě',
 gb_v_top='Na stupních vítězů: lepší než téměř všechny skutečné týmy.',gb_v_good='Dobré místo v první třetině.',gb_v_mid='Střed pole: jde to i lépe.',gb_v_low='Konec pole: skutečné týmy doletěly dál.',gb_ahead='{a} týmů před vámi, {b} za vámi.',
 gb_note='Čárkovaně na mapě: start a místo přistání skutečných týmů, ne jejich trasa.',gb_save='Uložit',gb_saved='Hra uložena',gb_saveq='Hrajete 30 minut bez uložení. Uložit teď?',
 gb_resume_q='Existuje uložená hra: {km} km od startu, doba letu {t}. Pokračovat?',gb_resume='Pokračovat',gb_new='Začít znovu',gb_resumed='Uložená hra načtena. Let je pozastaven.',gb_menu_q='Do hlavní nabídky? Let se uloží a lze v něm pokračovat.',
 gb_offline='Pozor: žádné připojení. Bez sítě chybí nové počasí a nové části mapy. Letět dál?',gb_wifi='Pozor: Wi-Fi je pryč, aplikace teď načítá přes mobilní síť. Letět dál?',gb_cont='Letět dál',gb_list='69. Gordon Bennett',gb_500_a='Zrychlení 500× při stisku'),
'zh-TW':dict(m_champ_d='重飛 2026 年第 69 屆戈登·貝內特盃：從格拉德貝克出發，對上 23 支真實隊伍',st_name_gb='格拉德貝克，2026/08/29 02:45',
 gb_story='重現第 69 屆戈登·貝內特盃。2026 年 8 月 29 日凌晨，23 支隊伍從格拉德貝克起飛。牙買加臨時報名成為第 25 隊：CoolRidings，也就是你。你最後一個起飛。降落點離起飛點最遠者獲勝。',
 gb_rules='地圖上的紅色區域為禁飛國家（俄羅斯、白俄羅斯、烏克蘭、摩爾多瓦、非洲、中東）。距離小於 10 公里或降落在水中即取消資格。500× 只在按住按鈕時有效。拋下兩袋沙即可起飛。',
 gb_data='錦標賽會下載比賽當天的天氣與整條航線的地圖，可能達數十 MB，主要是地圖。建議使用 Wi-Fi。',gb_go='開始',gb_busy_zone='正在載入禁飛區…',
 gb_nozone='無法載入禁飛區的國界資料。請連上網路後再試一次。',gb_nowx='無法載入比賽當天的天氣。請連上網路後再試一次。',gb_zone='禁飛區',gb_zone_near='注意：距禁飛區 {km} 公里',
 gb_km='距起飛點',gb_rank='你的名次',gb_of='24 隊中第 {r} 名',gb_col_rank='比賽名次',gb_dq_head='取消資格',gb_dq_zone='飛入禁飛區',gb_dq_water='降落在水中',
 gb_v_top='登上頒獎台：勝過幾乎所有真實隊伍。',gb_v_good='前三分之一的好名次。',gb_v_mid='中段班：還能更好。',gb_v_low='後段班：真實隊伍飛得更遠。',gb_ahead='前面有 {a} 隊，後面有 {b} 隊。',
 gb_note='地圖上的虛線：真實隊伍的起飛點與降落點，不是他們的航跡。',gb_save='儲存',gb_saved='已儲存進度',gb_saveq='你已連續玩 30 分鐘沒有儲存。現在儲存嗎？',
 gb_resume_q='有儲存的進度：距起飛點 {km} 公里，飛行時間 {t}。要繼續嗎？',gb_resume='繼續',gb_new='重新開始',gb_resumed='已載入進度，飛行已暫停。',gb_menu_q='要回到主選單嗎？飛行會被儲存，之後可以繼續。',
 gb_offline='注意：連線中斷。沒有網路就無法取得新的天氣與地圖。要繼續飛行嗎？',gb_wifi='注意：Wi-Fi 中斷，現在改用行動網路下載。要繼續飛行嗎？',gb_cont='繼續飛行',gb_list='第 69 屆戈登·貝內特盃',gb_500_a='按住時 500 倍速'),
'es':dict(m_champ_d='Revive la 69.ª Gordon Bennett 2026: desde Gladbeck contra los 23 equipos reales',st_name_gb='Gladbeck, 29.08.2026, 02:45',
 gb_story='Recreación de la 69.ª Coupe Aéronautique Gordon Bennett. 23 equipos despegaron de Gladbeck en la noche del 29 de agosto de 2026. Jamaica se inscribe a última hora como equipo 25: los CoolRidings, y ese eres tú. Despegas el último. Gana quien aterrice más lejos del lugar de despegue.',
 gb_rules='En rojo en el mapa: países prohibidos (Rusia, Bielorrusia, Ucrania, Moldavia, África, Oriente Medio). Acercarse a menos de 10 km o aterrizar en el agua supone la descalificación. 500× solo funciona mientras se mantiene pulsado el botón. Suelta dos sacos para despegar.',
 gb_data='El campeonato carga el tiempo del día de la carrera y el mapa a lo largo de toda la ruta. Pueden ser varias decenas de MB, sobre todo por el mapa. Se recomienda una conexión Wi-Fi.',gb_go='Empezar',gb_busy_zone='Cargando zonas prohibidas …',
 gb_nozone='No se pudieron cargar las fronteras de las zonas prohibidas. Inténtalo de nuevo con conexión.',gb_nowx='No se pudo cargar el tiempo del día de la carrera. Inténtalo de nuevo con conexión.',gb_zone='Zona prohibida',gb_zone_near='Atención: zona prohibida a {km} km',
 gb_km='Distancia desde el despegue',gb_rank='Tu puesto',gb_of='Puesto {r} de 24',gb_col_rank='En la carrera',gb_dq_head='Descalificado',gb_dq_zone='entró en una zona prohibida',gb_dq_water='aterrizó en el agua',
 gb_v_top='En el podio: mejor que casi todos los equipos reales.',gb_v_good='Un buen puesto en el primer tercio.',gb_v_mid='Mitad de la tabla: se puede más.',gb_v_low='Parte baja: los equipos reales llegaron más lejos.',gb_ahead='{a} equipos por delante, {b} por detrás.',
 gb_note='Línea discontinua en el mapa: despegue y lugar de aterrizaje de los equipos reales, no su ruta.',gb_save='Guardar',gb_saved='Partida guardada',gb_saveq='Llevas 30 minutos jugando sin guardar. ¿Guardar ahora?',
 gb_resume_q='Hay una partida guardada: {km} km desde el despegue, tiempo de vuelo {t}. ¿Continuar?',gb_resume='Continuar',gb_new='Empezar de nuevo',gb_resumed='Partida cargada. El vuelo está en pausa.',gb_menu_q='¿Ir al menú principal? El vuelo se guarda y se puede continuar.',
 gb_offline='Atención: sin conexión. Sin red faltan el tiempo nuevo y las nuevas partes del mapa. ¿Seguir volando?',gb_wifi='Atención: sin Wi-Fi, la aplicación descarga ahora por datos móviles. ¿Seguir volando?',gb_cont='Seguir volando',gb_list='69.ª Gordon Bennett',gb_500_a='Cámara rápida 500× mientras se pulsa')}
order=['de','en','fr','pl','cs','zh-TW','es']; keys=list(T['de'].keys())
for L in order: assert list(T[L].keys())==keys,(L,set(keys)^set(T[L].keys()))
for L in order:
    for k,v in T[L].items(): assert "'" not in v,(L,k)
# m_champ_d ersetzen, Rest anhängen
it=iter(order); n=[0]
def r1(m): n[0]+=1; return "m_champ_d:'"+T[next(it)]['m_champ_d']+"'"
f.s=re.sub(r"m_champ_d:'[^']*'",r1,f.s); assert n[0]==7,n
it=iter(order); n=[0]
def r(m):
    n[0]+=1; L=next(it); return m.group(1)+', '+', '.join(k+":'"+v+"'" for k,v in T[L].items() if k!='m_champ_d')+m.group(2)
f.s=re.sub(r"(gps_avg:'[^']*')( \})",r,f.s); assert n[0]==7,n
f.rep("const BUILD = '2026-10-09.3';","const BUILD = '2026-10-09.4';")
f.save()
