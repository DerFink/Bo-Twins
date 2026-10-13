import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
qr=open('/home/claude/w/qr.js',encoding='utf-8').read()
# ---------- Buy me a Beer ----------
f.rep('''<span data-i="m_score_d"></span></button>
      </div>''','''<span data-i="m_score_d"></span></button>
        <button class="mbeer" id="m-beer"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 6h9v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zM13 8h2.5a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5H13" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M4 6c-1-3 2-4 3-2.500 1-2 4-1.500 4 .5 2-.5 3 1 2 2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg> Buy me a Beer</button>
      </div>'''.replace('2.500','2.5').replace('1.500','1.5'))
f.rep('    <!-- Rückblick auf die Fahrt:','''    <!-- Buy me a Beer: freiwillige Unterstützung über PayPal, Betrag frei wählbar -->
    <div class="full" id="beer" hidden>
      <div class="card">
        <h2>Buy me a Beer</h2>
        <p id="beer-text"></p>
        <label class="beeramt"><span data-i="beer_amt"></span><input id="beer-in" type="text" inputmode="decimal" autocomplete="off" maxlength="8"><b>€</b></label>
        <a class="pri" id="beer-go" target="_blank" rel="noopener" data-i="beer_open"></a>
        <p class="note" data-i="beer_qr"></p>
        <canvas id="beer-cv" width="10" height="10"></canvas>
        <p class="note" id="beer-url"></p>
        <button class="sec" id="beer-close" data-i="close"></button>
      </div>
    </div>

    <!-- Rückblick auf die Fahrt:''')
f.rep("#sc-kind{margin-bottom:8px}","#sc-kind{margin-bottom:8px}\n.mbeer{display:flex;align-items:center;justify-content:center;gap:7px;width:100%;margin-top:10px;padding:6px;border:0;background:none;color:#B8C76F;font-family:\"Courier New\",Courier,monospace;font-size:13.5px;letter-spacing:.04em}\n.mbeer:active{color:#eef3fa}\n#beer{z-index:880}\n#beer .card{width:min(380px,100%);max-height:calc(100% - 8px);overflow:auto;text-align:left}\n#beer-text{margin:0 0 10px;line-height:1.45}\n.beeramt{display:flex;align-items:center;gap:8px;margin:0 0 10px}\n.beeramt span{font-size:13px;color:var(--mut)}\n.beeramt input{flex:1;min-width:0;min-height:44px;padding:0 10px;border-radius:10px;border:1px solid var(--line);background:var(--pan);font-family:var(--num);font-size:22px;font-weight:600;color:var(--tx);text-align:right}\n.beeramt input::placeholder{color:#6b7c98}\n.beeramt b{font-family:var(--num);font-size:22px}\na.pri{display:block;text-align:center;text-decoration:none}\n#beer-cv{display:block;margin:6px auto;width:min(220px,70%);height:auto;border-radius:8px;image-rendering:pixelated}\n#beer-url{text-align:center;word-break:break-all}")
f.rep("/* ---------- Zeitschleife ---------- */", qr + """
/* ---------- Buy me a Beer (SPI-16) ----------
   Der Preis für ein gezapftes Pils (0,3 l) in Berlin wird bei jedem Build neu ermittelt und hier eingetragen. Er steht grau im Betragsfeld;
   jede Summe ist möglich. Der Betrag geht in die Adresse von PayPal.me und in den QR-Code. */
const BEER = {price: 3.50, asOf: '2026-10', paypal: 'LuftschiffFink'};
function beerAmount(){ const raw = $('beer-in').value.trim().replace(/\\s/g, '').replace(',', '.'), v = raw === '' ? BEER.price : parseFloat(raw); return isFinite(v) && v > 0 ? Math.min(99999, Math.round(v * 100) / 100) : null; }
function beerShow(){
  const v = beerAmount(), url = 'https://paypal.me/' + BEER.paypal + (v ? '/' + v.toFixed(2) + 'EUR' : '');
  $('beer-go').href = url; $('beer-url').textContent = url.replace('https://', ''); qrDraw($('beer-cv'), url, 240);
}
function beerOpen(){
  const d = new Date(BEER.asOf + '-01T00:00:00Z'), old = Date.now() - d.getTime() > 366 * 864e5;
  $('beer-text').textContent = tr('beer_text', {p: nf(BEER.price, 2), d: d.toLocaleDateString(UI.lang, {month: 'long', year: 'numeric', timeZone: 'UTC'})}) + (old ? ' ' + tr('beer_old') : '');
  $('beer-in').value = ''; $('beer-in').placeholder = nf(BEER.price, 2); $('beer').hidden = false; beerShow();
}
$('m-beer').addEventListener('click', beerOpen); $('beer-in').addEventListener('input', beerShow); $('beer-close').addEventListener('click', () => { $('beer').hidden = true; });

/* ---------- Zeitschleife ---------- */""")
# ---------- Meisterschaft: keine Linien zu den Landeorten, 30 Minuten zurück, Zeitraffer bremst in Bodennähe ----------
f.rep("    add(L.polyline([S, [t[5], t[6]]], {renderer: GB.rend, color: '#9aabc4', weight: 1.2, opacity: .55, dashArray: '3 7', interactive: false}));\n","")
f.rep("  polys: null, ban: null, layers: [],","  snaps: [], snapT: -1e9, lastAt: 0, slowTold: false,\n  polys: null, ban: null, layers: [],")
f.rep("  GB.playS += real;                                                                // nach 30 Minuten ohne Speichern nachfragen","""  if (B.t - GB.snapT >= 300){                                                      // alle 5 Minuten Spielzeit ein Zwischenstand, damit sich die letzten 30 Minuten wiederholen lassen
    GB.snapT = B.t; GB.snaps.push({t: B.t, B: JSON.parse(JSON.stringify(B)), START: Object.assign({}, START), pathN: pathPts.length, lastE: lastPathE, lastN: lastPathN, we: WXRUN.e, wn: WXRUN.n});
    if (GB.snaps.length > 16) GB.snaps.shift();
  }
  GB.playS += real;                                                                // nach 30 Minuten ohne Speichern nachfragen""")
f.rep("/* Spielstand: Ballon, Bezugspunkt,","""/* Die letzten 30 Minuten noch einmal (MEI-13): zurück auf den Zwischenstand, der mindestens 30 Minuten vor dem Ende liegt. Das Ergebnis der
   beendeten Fahrt wird aus der Liste genommen. */
function gbRewind(){
  if (!GB.snaps.length) return;
  let s = GB.snaps[0]; for (const q of GB.snaps) if (q.t <= B.t - 1800) s = q;
  const back = Math.round((B.t - s.t) / 60);
  store.set('gb-list69', gbList().filter(e => e.at !== GB.lastAt));
  B = JSON.parse(JSON.stringify(s.B)); START = Object.assign({}, s.START); WXRUN.e = s.we; WXRUN.n = s.wn; WXRUN.lastT = B.t; lastPathE = s.lastE; lastPathN = s.lastN;
  pathPts.length = Math.min(pathPts.length, s.pathN); pathLine.setLatLngs(pathPts); balMk.setLatLng(gbPos());
  { const n = REC.t.findIndex(t => t > s.t); if (n >= 0) REC.k.forEach(k => { REC[k].length = n; }); REC.last = s.t; }
  TER.grid = null; TER.fine = null; TER.failAt = 0; terLoad(B.e, B.n, false);
  GB.snaps = GB.snaps.filter(q => q.t <= s.t); GB.snapT = s.t; GB.dq = null; GB.zone = null; GB.chkAt = -1e9; GB.warned = 0; GB.playS = 0; valve = 0; shown = false;
  $('result').hidden = true; setState('play'); setSpeed(1); renderSand(true); follow = true; userZoom = false; map.setView(gbPos(), 11); setPaused(true); toast(tr('gb_rewound', {m: back}));
}
// Zeitraffer der Meisterschaft: in Bodennähe und im Sinken höchstens 10×, damit der Ballon nicht ungewollt landet
function gbSpeed(){
  let sp = GB.hold ? 1000 : UI.speed; const agl = B.h - B.gnd;
  if (sp > 10 && B.air && agl < 250 && B.w < -0.3){ sp = 10; if (!GB.slowTold){ GB.slowTold = true; toast(tr('gb_slow')); } } else if (agl > 400) GB.slowTold = false;
  return sp;
}
/* Spielstand: Ballon, Bezugspunkt,""")
f.rep("GB.hold && isGB() ? 1000 : UI.speed","isGB() ? gbSpeed() : UI.speed")
f.rep("  resetRun(); GB.dq = null; GB.zone = null; GB.playS = 0; GB.warned = 0; GB.chkAt = -1e9;","  resetRun(); GB.dq = null; GB.zone = null; GB.playS = 0; GB.warned = 0; GB.chkAt = -1e9; GB.snaps = []; GB.snapT = -1e9;")
f.rep("  GB.dq = null; GB.zone = null; GB.playS = 0; GB.warned = 0; GB.chkAt = -1e9;\n  gbDraw(); setState('play');","  GB.dq = null; GB.zone = null; GB.playS = 0; GB.warned = 0; GB.chkAt = -1e9; GB.snaps = []; GB.snapT = -1e9;\n  gbDraw(); setState('play');")
f.rep("at: Date.now()}; gbListAdd(e);","at: Date.now()}; GB.lastAt = e.at; gbListAdd(e);")
f.rep('        <button class="sec" id="r-review" data-i="rv_title"></button>','        <button class="sec" id="r-rewind" hidden data-i="gb_rewind"></button>\n        <button class="sec" id="r-review" data-i="rv_title"></button>')
f.rep("#rv-btn[hidden],#r-review[hidden]{display:none}","#rv-btn[hidden],#r-review[hidden],#r-rewind[hidden]{display:none}\n#result #r-rewind{margin-bottom:6px;border-color:var(--orb);color:var(--orb)}")
f.rep("  { const bx = $('r-list'); bx.textContent = '';","  $('r-rewind').hidden = !(k === 'gb' && GB.snaps.length);\n  { const bx = $('r-list'); bx.textContent = '';")
f.rep("$('gb-save').addEventListener('click', () => gbSave());","$('gb-save').addEventListener('click', () => gbSave());\n$('r-rewind').addEventListener('click', gbRewind);")
NOTE={'de':'Punkte auf der Karte: Landeorte der echten Teams mit Rang.','en':'Dots on the map: landing sites of the real teams with their rank.','fr':'Points sur la carte : lieux d’atterrissage des vraies équipes avec leur rang.','pl':'Punkty na mapie: miejsca lądowania prawdziwych załóg z miejscem w klasyfikacji.','cs':'Body na mapě: místa přistání skutečných týmů s pořadím.','zh-TW':'地圖上的圓點：真實隊伍的降落點與名次。','es':'Puntos en el mapa: lugares de aterrizaje de los equipos reales con su puesto.'}
FAN={'de':' Inoffizielles Fan-Projekt.','en':' Unofficial fan project.','fr':' Projet de fans non officiel.','pl':' Nieoficjalny projekt fanowski.','cs':' Neoficiální fanouškovský projekt.','zh-TW':'非官方的愛好者專案。','es':' Proyecto de aficionados no oficial.'}
T={'de':dict(beer_text='Diese App ist komplett kostenlos und werbefrei. Wenn dir die App gefällt und du meine Serverkosten und die Weiterentwicklung unterstützen möchtest, kannst du mir hier ein Bier spendieren. Ein gezapftes Pils (0,3 l) kostet in Berlin aktuell rund {p} € (Stand {d}).',beer_old='Der Preis ist älter als ein Jahr.',beer_amt='Betrag',beer_open='Mit PayPal öffnen',beer_qr='Oder diesen Code mit dem Handy scannen:',gb_rewind='Die letzten 30 Minuten noch einmal',gb_rewound='{m} Minuten zurückgesetzt. Die Fahrt ist angehalten.',gb_slow='Bodennähe: Die Zeit läuft höchstens 10×'),
 'en':dict(beer_text='This app is completely free and has no ads. If you like it and want to support my server costs and further development, you can buy me a beer here. A draught pilsner (0.3 l) in Berlin currently costs about €{p} (as of {d}).',beer_old='The price is more than a year old.',beer_amt='Amount',beer_open='Open with PayPal',beer_qr='Or scan this code with your phone:',gb_rewind='Replay the last 30 minutes',gb_rewound='Set back {m} minutes. The flight is paused.',gb_slow='Near the ground: time runs at 10× at most'),
 'fr':dict(beer_text='Cette application est entièrement gratuite et sans publicité. Si elle vous plaît et que vous souhaitez soutenir mes frais de serveur et son développement, vous pouvez m’offrir une bière ici. Une pils pression (0,3 l) coûte actuellement environ {p} € à Berlin (état : {d}).',beer_old='Ce prix date de plus d’un an.',beer_amt='Montant',beer_open='Ouvrir avec PayPal',beer_qr='Ou scannez ce code avec votre téléphone :',gb_rewind='Rejouer les 30 dernières minutes',gb_rewound='Retour de {m} minutes. Le vol est en pause.',gb_slow='Près du sol : le temps défile à 10× au maximum'),
 'pl':dict(beer_text='Ta aplikacja jest całkowicie darmowa i bez reklam. Jeśli ci się podoba i chcesz wesprzeć koszty serwera i dalszy rozwój, możesz postawić mi tutaj piwo. Lany pils (0,3 l) kosztuje w Berlinie obecnie około {p} € (stan: {d}).',beer_old='Cena ma ponad rok.',beer_amt='Kwota',beer_open='Otwórz w PayPal',beer_qr='Albo zeskanuj ten kod telefonem:',gb_rewind='Zagraj ostatnie 30 minut jeszcze raz',gb_rewound='Cofnięto o {m} minut. Lot jest wstrzymany.',gb_slow='Blisko ziemi: czas biegnie najwyżej 10×'),
 'cs':dict(beer_text='Tato aplikace je zcela zdarma a bez reklam. Pokud se vám líbí a chcete podpořit náklady na server a další vývoj, můžete mi zde koupit pivo. Točený pils (0,3 l) stojí v Berlíně aktuálně kolem {p} € (stav: {d}).',beer_old='Cena je starší než rok.',beer_amt='Částka',beer_open='Otevřít v PayPalu',beer_qr='Nebo naskenujte tento kód telefonem:',gb_rewind='Posledních 30 minut znovu',gb_rewound='Vráceno o {m} minut. Let je pozastaven.',gb_slow='Blízko země: čas běží nejvýše 10×'),
 'zh-TW':dict(beer_text='這個 App 完全免費，也沒有廣告。如果你喜歡它，並想支持我的伺服器費用與後續開發，可以在這裡請我喝一杯啤酒。柏林一杯生啤皮爾森（0.3 公升）目前約 {p} 歐元（{d}）。',beer_old='這個價格已超過一年。',beer_amt='金額',beer_open='用 PayPal 開啟',beer_qr='或用手機掃描這個條碼：',gb_rewind='重玩最後 30 分鐘',gb_rewound='已倒回 {m} 分鐘，飛行已暫停。',gb_slow='接近地面：時間最多 10 倍速'),
 'es':dict(beer_text='Esta aplicación es totalmente gratuita y sin publicidad. Si te gusta y quieres apoyar mis gastos de servidor y su desarrollo, aquí puedes invitarme a una cerveza. Una pilsner de barril (0,3 l) cuesta ahora en Berlín unos {p} € (a fecha de {d}).',beer_old='El precio tiene más de un año.',beer_amt='Importe',beer_open='Abrir con PayPal',beer_qr='O escanea este código con el móvil:',gb_rewind='Repetir los últimos 30 minutos',gb_rewound='Retrocedido {m} minutos. El vuelo está en pausa.',gb_slow='Cerca del suelo: el tiempo corre a 10× como máximo')}
order=['de','en','fr','pl','cs','zh-TW','es']; keys=list(T['de'].keys())
for L in order:
    assert list(T[L].keys())==keys,L
    for k,v in T[L].items(): assert "'" not in v,(L,k)
it=iter(order); n=[0]
def r(m): n[0]+=1; L=next(it); return m.group(1)+', '+', '.join(k+":'"+v+"'" for k,v in T[L].items())+m.group(2)
f.s=re.sub(r"(rv_legend:'[^']*')( \})",r,f.s); assert n[0]==7,n
it=iter(order); n=[0]
def r2(m): n[0]+=1; return "gb_note:'"+NOTE[next(it)]+"'"
f.s=re.sub(r"gb_note:'[^']*'",r2,f.s); assert n[0]==7,n
it=iter(order); n=[0]
def r3(m): n[0]+=1; L=next(it); return m.group(1)+('。' if L=='zh-TW' else '.')+FAN[L]+"'"
f.s=re.sub(r"(m_champ_d:'[^']*)'",r3,f.s); assert n[0]==7,n
f.rep("const BUILD = '2026-10-09.6';","const BUILD = '2026-10-09.7';")
f.save()
