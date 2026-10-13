import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
rec=open('/home/claude/w/rec.js',encoding='utf-8').read()
# ---------- Kern: Die Crew lässt los, wenn der Ballon sicher steigt ----------
f.rep("function newBalloon(cfg, tab){","""/* Auftriebsüberschuss, bei dem die Bodencrew loslässt (STE-22): mindestens holdKg, und so viel, dass der pralle Ballon bis 250 m über Grund steigt.
   In einer Bodeninversion (nachts) wird die Luft nach oben wärmer und dünner; dann braucht es deutlich mehr als zwei Säcke. */
function holdNeed(cfg, tab, Tg0){
  const a0 = atmAt(tab, 0), a = atmAt(tab, 250), lift = (q, Tg) => q.p * cfg.vol / R_GAS * (M_AIR / q.T - M_H2 / Tg);
  return Math.max(cfg.holdKg || 0, Math.ceil(lift(a0, Tg0) - lift(a, Tg0 * Math.pow(a.p / a0.p, KAPPA))));
}
function newBalloon(cfg, tab){""")
f.rep("wet: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon,\n          sacks: Lo.sacks,","wet: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon, holdKg: holdNeed(cfg, tab, T.Tg),\n          sacks: Lo.sacks,")
f.rep("    if (free < (cfg.holdKg || 0) - 0.1){ B.held = true;","    if (free < (B.holdKg == null ? cfg.holdKg || 0 : B.holdKg) - 0.1){ B.held = true;")
f.rep("B.go ? 0 : (cfg.holdKg || 0) + 1 - B.free)); return; }","B.go ? 0 : (B.holdKg == null ? cfg.holdKg || 0 : B.holdKg) + 1 - B.free)); return; }")
f.rep("tr('hint_hold', {kg: nf(CFG.holdKg), rest: nf(Math.max(0, CFG.holdKg - (B.free || 0)), 1)})","tr('hint_hold', {kg: nf(B.holdKg == null ? CFG.holdKg : B.holdKg), rest: nf(Math.max(0, (B.holdKg == null ? CFG.holdKg : B.holdKg) - (B.free || 0)), 1)})")
for a in [' (zwei Säcke)',' (two bags)',' (deux sacs)',' (dwa worki)',' (dva pytle)','（兩袋沙）',' (dos sacos)']: f.rep(a+'.' if a!='（兩袋沙）' else a+'。', '.' if a!='（兩袋沙）' else '。')
# ---------- Anzeige: Uhrzeit, Lufttemperatur, Profil bis 6000 m ----------
f.rep("  const top = Math.min(9000, Math.max(2000, Math.ceil((B.h + 300) / 1000) * 1000));","  const top = Math.min(9000, Math.max(6000, Math.ceil((B.h + 300) / 1000) * 1000));   // immer bis 6000 m (Vorgabe Nutzer), darüber wächst die Achse mit")
f.rep("    $('i-sky').textContent = e.rain > 0 ? nf(e.rain, 1) + ' mm/h' : el > 0 ? nf(Math.round(el)) + '°' : tr('night');","    $('i-sky').textContent = e.rain > 0 ? nf(e.rain, 1) + ' mm/h' : (el > 0 ? nf(Math.round(el)) + '° ' : '') + skyClock();\n    $('i-temp').textContent = fmtV(a.T - 273.15);")
f.rep("let heldSeen = false;","""// Uhrzeit am Ballon auf halbe Stunden: Meisterschaft in MESZ, echtes Wetter in der Zeit des Geräts, Simulation in Sonnenzeit
function skyClock(){
  const ms = (B.t0 == null ? simT0(SIM_LON) : B.t0) + B.t * 1000; let h, m;
  if (isGB()){ const d = new Date(ms + 2 * 3600e3); h = d.getUTCHours(); m = d.getUTCMinutes(); }
  else if (WX){ const d = new Date(ms); h = d.getHours(); m = d.getMinutes(); }
  else { const d = new Date(ms + START.lon / 15 * 3600e3); h = d.getUTCHours(); m = d.getUTCMinutes(); }
  return String(h).padStart(2, '0') + ':' + (m < 30 ? '00' : '30');
}
let heldSeen = false;""")
f.rep('        <div class="kv" id="row-wet" hidden>','        <div class="kv"><span>°C</span><b id="i-temp">–</b></div>\n        <div class="kv" id="row-wet" hidden>')
# ---------- Zeitraffer: 500× fest, 1000× solange gedrückt (Meisterschaft) ----------
f.rep('<button data-v="100">100×</button>\n      <button id="btn-500" hidden data-ia="gb_500_a" aria-label="500×">500×</button></div>','<button data-v="100">100×</button><button data-v="500">500×</button>\n      <button id="btn-500" hidden data-ia="gb_500_a" aria-label="1000×">1000×</button></div>')
f.rep('#app.gb #seg-speed button[data-v="5"]{display:none}','#app.gb #seg-speed button[data-v="5"],#app.gb #seg-speed button[data-v="30"],#app:not(.gb) #seg-speed button[data-v="500"]{display:none}\n#app.gb #seg-speed button{padding-left:7px;padding-right:7px}')
f.rep("GB.hold && isGB() ? 500 : UI.speed","GB.hold && isGB() ? 1000 : UI.speed")
n=[0]
def r500(m): n[0]+=1; return m.group(0).replace('500×','1000×').replace('500 倍速','1000 倍速')
f.s=re.sub(r"gb_(rules|500_a):'[^']*'",r500,f.s); assert n[0]==14,n
# ---------- Startseite ----------
f.rep('''        <button class="mbtn" id="m-score"><b data-i="m_score"></b><span data-i="m_score_d"></span></button>
        <button class="mbtn" id="m-champ"><b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>''','''        <button class="mbtn" id="m-champ"><b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>
        <button class="mbtn alt" id="m-score"><b>★ <span data-i="m_score"></span> ★</b><span data-i="m_score_d"></span></button>''')
f.rep('spellcheck="false" data-ip="name_ph"></label>','spellcheck="false" data-ip="name_ph"></label>\n        <p class="mhint" data-i="name_hint"></p>')
f.rep(".mscreen .mbtn em{color:#B8C76F;border-color:#B8C76F}",".mscreen .mbtn em{color:#B8C76F;border-color:#B8C76F}\n.mscreen .mbtn.alt{margin-top:12px;text-align:center;border:2px dashed #B8C76F;background:#0d1626}\n.mscreen .mbtn.alt b{color:#B8C76F;font-family:\"Courier New\",Courier,monospace;letter-spacing:.06em;text-transform:uppercase;font-size:15px}\n.mscreen .mbtn.alt b span{display:inline;font-size:inherit;color:inherit}\n.mhint{margin:5px 0 2px;font-size:12px;line-height:1.35;color:#9aabc4}")
SC={'Die besten Fahrten auf diesem Gerät':'Die besten Fahrten','The best flights on this device':'The best flights','Les meilleurs vols sur cet appareil':'Les meilleurs vols','Najlepsze loty na tym urządzeniu':'Najlepsze loty','Nejlepší lety na tomto zařízení':'Nejlepší lety','此裝置上的最佳飛行':'最佳飛行','Los mejores vuelos en este dispositivo':'Los mejores vuelos'}
for a,b in SC.items(): f.rep("m_score_d:'"+a+"'","m_score_d:'"+b+"'")
# ---------- Rückblick ----------
f.rep('        <button class="sm" id="gb-save" hidden data-i="gb_save"></button>','        <button class="sm" id="gb-save" hidden data-i="gb_save"></button>\n        <button class="iconbtn" id="rv-btn" hidden data-ia="rv_title" aria-label="Rückblick"><svg width="22" height="20" viewBox="0 0 22 20" aria-hidden="true"><path d="M2 2v16h18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M5 14l4-6 3 3 3-7 4 5" fill="none" stroke="#ff9f1c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>')
f.rep('        <button class="pri" id="again" data-i="again">Neue Fahrt</button>','        <button class="sec" id="r-review" data-i="rv_title"></button>\n        <button class="pri" id="again" data-i="again">Neue Fahrt</button>')
f.rep('    <div class="full" id="busy" hidden>','''    <!-- Rückblick auf die Fahrt: Höhe, Gastemperatur gegen Luft und Steigen über der Zeit -->
    <div class="full" id="review" hidden>
      <div class="card">
        <h2 data-i="rv_title"></h2>
        <div class="seg wide" id="rv-span"><button data-v="1800" class="on">30 min</button><button data-v="7200">2 h</button><button data-v="0" data-i="rv_all"></button></div>
        <canvas id="rv-cv"></canvas>
        <p id="rv-read"></p>
        <p class="note" id="rv-why"></p>
        <p class="note" data-i="rv_legend"></p>
        <button class="sec" id="rv-close" data-i="close"></button>
      </div>
    </div>

    <div class="full" id="busy" hidden>''')
f.rep("#sc-kind{margin-bottom:8px}","#sc-kind{margin-bottom:8px}\n#review{z-index:880}\n#review .card{width:min(560px,100%);max-height:calc(100% - 8px);overflow:auto}\n#rv-cv{display:block;width:100%;height:min(46vh,340px);margin:8px 0 6px;touch-action:none}\n#rv-read{margin:0 0 6px;font-family:var(--num);font-size:15px;line-height:1.35}\n#rv-btn[hidden],#r-review[hidden]{display:none}\n#result #r-review{margin-bottom:6px}")
f.rep("  $('gb-save').hidden = !(k === 'gb' && STATE === 'play');","  $('rv-btn').hidden = !((STATE === 'play' || STATE === 'done') && REC.t.length > 1);\n  $('gb-save').hidden = !(k === 'gb' && STATE === 'play');")
f.rep("function resetRun(){\n  B = newBalloon(CFG, ATM); valve = 0; shown = false; SND.valve(0);","function resetRun(){\n  B = newBalloon(CFG, ATM); valve = 0; shown = false; SND.valve(0); recReset();")
f.rep("  B = s.B; valve = 0; shown = false; SND.valve(0);","  B = s.B; valve = 0; shown = false; SND.valve(0); recReset();")
f.rep("    if (isGB() && !B.landed) gbTick(real);","    recTick();\n    if (isGB() && !B.landed) gbTick(real);")
f.rep("/* ---------- Zeitschleife ---------- */", rec+"\n/* ---------- Zeitschleife ---------- */")
T={'de':dict(name_hint='Trage hier Deinen Namen ein und finde Dich in der Bestenliste zwischen den anderen Mitspielern.',rv_title='Rückblick',rv_all='alles',rv_alt='Höhe',rv_dt='Gas gegen Luft',rv_vario='Steigen',rv_empty='Noch keine Aufzeichnung: erst nach dem Abheben.',
  rv_before='In den {m} Minuten davor:',rv_cool='Gas {k} K kälter geworden (rund −{kg} kg Auftrieb)',rv_warm='Gas {k} K wärmer geworden (rund +{kg} kg Auftrieb)',rv_water='Wasser auf der Hülle {kg} kg',rv_gasloss='{p} % Gas abgegeben (rund −{kg} kg Auftrieb)',rv_sand='{kg} kg Sand abgeworfen',rv_none='kaum eine Änderung.',rv_free='Auftriebsüberschuss jetzt {kg} kg.',
  rv_legend='Tippe ins Diagramm, um einen Zeitpunkt zu wählen. Sandfarbene Striche oben: Ballast. Rote Striche: Ventil. Dunkel hinterlegt: Nacht. Blau hinterlegt: Regen. Heller Strich oben: Wolken über dem Ballon. Braun: Gelände.'),
 'en':dict(name_hint='Enter your name here and find yourself in the high scores among the other players.',rv_title='Review',rv_all='all',rv_alt='Height',rv_dt='Gas vs. air',rv_vario='Climb',rv_empty='Nothing recorded yet: only after lift-off.',
  rv_before='In the {m} minutes before:',rv_cool='gas became {k} K colder (about −{kg} kg lift)',rv_warm='gas became {k} K warmer (about +{kg} kg lift)',rv_water='water on the envelope {kg} kg',rv_gasloss='{p} % gas released (about −{kg} kg lift)',rv_sand='{kg} kg sand dropped',rv_none='hardly any change.',rv_free='Free lift now {kg} kg.',
  rv_legend='Tap the chart to pick a moment. Sand-coloured marks at the top: ballast. Red marks: valve. Dark background: night. Blue background: rain. Light line at the top: clouds above the balloon. Brown: terrain.'),
 'fr':dict(name_hint='Saisissez votre nom ici et retrouvez-vous dans le classement parmi les autres joueurs.',rv_title='Rétrospective',rv_all='tout',rv_alt='Hauteur',rv_dt='Gaz / air',rv_vario='Montée',rv_empty='Rien d’enregistré : seulement après le décollage.',
  rv_before='Dans les {m} minutes précédentes :',rv_cool='gaz refroidi de {k} K (environ −{kg} kg de portance)',rv_warm='gaz réchauffé de {k} K (environ +{kg} kg de portance)',rv_water='eau sur l’enveloppe {kg} kg',rv_gasloss='{p} % de gaz évacué (environ −{kg} kg de portance)',rv_sand='{kg} kg de sable lâchés',rv_none='presque aucun changement.',rv_free='Excédent de portance actuel {kg} kg.',
  rv_legend='Touchez le graphique pour choisir un instant. Traits couleur sable en haut : lest. Traits rouges : soupape. Fond sombre : nuit. Fond bleu : pluie. Trait clair en haut : nuages au-dessus du ballon. Brun : relief.'),
 'pl':dict(name_hint='Wpisz tutaj swoje imię i znajdź się w tabeli wyników wśród innych graczy.',rv_title='Przegląd lotu',rv_all='wszystko',rv_alt='Wysokość',rv_dt='Gaz względem powietrza',rv_vario='Wznoszenie',rv_empty='Brak zapisu: dopiero po starcie.',
  rv_before='W ciągu {m} minut wcześniej:',rv_cool='gaz ochłodził się o {k} K (około −{kg} kg siły nośnej)',rv_warm='gaz ogrzał się o {k} K (około +{kg} kg siły nośnej)',rv_water='woda na powłoce {kg} kg',rv_gasloss='wypuszczono {p} % gazu (około −{kg} kg siły nośnej)',rv_sand='zrzucono {kg} kg piasku',rv_none='prawie bez zmian.',rv_free='Nadmiar siły nośnej teraz {kg} kg.',
  rv_legend='Dotknij wykresu, aby wybrać chwilę. Piaskowe kreski u góry: balast. Czerwone kreski: zawór. Ciemne tło: noc. Niebieskie tło: deszcz. Jasna kreska u góry: chmury nad balonem. Brąz: teren.'),
 'cs':dict(name_hint='Zadejte zde své jméno a najděte se v tabulce výsledků mezi ostatními hráči.',rv_title='Ohlédnutí',rv_all='vše',rv_alt='Výška',rv_dt='Plyn vůči vzduchu',rv_vario='Stoupání',rv_empty='Zatím žádný záznam: až po startu.',
  rv_before='Během {m} minut předtím:',rv_cool='plyn se ochladil o {k} K (asi −{kg} kg vztlaku)',rv_warm='plyn se ohřál o {k} K (asi +{kg} kg vztlaku)',rv_water='voda na obalu {kg} kg',rv_gasloss='vypuštěno {p} % plynu (asi −{kg} kg vztlaku)',rv_sand='shozeno {kg} kg písku',rv_none='téměř beze změny.',rv_free='Přebytek vztlaku nyní {kg} kg.',
  rv_legend='Klepnutím do grafu zvolíte okamžik. Pískové čárky nahoře: zátěž. Červené čárky: ventil. Tmavé pozadí: noc. Modré pozadí: déšť. Světlá čára nahoře: oblaka nad balonem. Hnědá: terén.'),
 'zh-TW':dict(name_hint='在這裡輸入你的名字，就能在排行榜上和其他玩家一起看到自己。',rv_title='回顧',rv_all='全部',rv_alt='高度',rv_dt='氣體與空氣溫差',rv_vario='升降',rv_empty='尚無紀錄：起飛後才開始。',
  rv_before='在之前的 {m} 分鐘內：',rv_cool='氣體降溫 {k} K（升力約 −{kg} 公斤）',rv_warm='氣體升溫 {k} K（升力約 +{kg} 公斤）',rv_water='球囊積水 {kg} 公斤',rv_gasloss='排出 {p} % 氣體（升力約 −{kg} 公斤）',rv_sand='拋下 {kg} 公斤沙',rv_none='幾乎沒有變化。',rv_free='目前淨升力 {kg} 公斤。',
  rv_legend='點一下圖表選擇時間點。上方沙色短線：壓艙物。紅色短線：排氣閥。深色背景：夜間。藍色背景：下雨。上方淺色線：氣球上方有雲。棕色：地形。'),
 'es':dict(name_hint='Escribe aquí tu nombre y encuéntrate en la clasificación entre los demás jugadores.',rv_title='Repaso',rv_all='todo',rv_alt='Altura',rv_dt='Gas frente al aire',rv_vario='Ascenso',rv_empty='Aún no hay registro: solo tras el despegue.',
  rv_before='En los {m} minutos anteriores:',rv_cool='el gas se enfrió {k} K (unos −{kg} kg de sustentación)',rv_warm='el gas se calentó {k} K (unos +{kg} kg de sustentación)',rv_water='agua en la envoltura {kg} kg',rv_gasloss='{p} % de gas soltado (unos −{kg} kg de sustentación)',rv_sand='{kg} kg de arena soltados',rv_none='casi sin cambios.',rv_free='Exceso de sustentación ahora {kg} kg.',
  rv_legend='Toca el gráfico para elegir un momento. Marcas color arena arriba: lastre. Marcas rojas: válvula. Fondo oscuro: noche. Fondo azul: lluvia. Línea clara arriba: nubes sobre el globo. Marrón: terreno.')}
order=['de','en','fr','pl','cs','zh-TW','es']; keys=list(T['de'].keys())
for L in order:
    assert list(T[L].keys())==keys,L
    for k,v in T[L].items(): assert "'" not in v,(L,k)
it=iter(order); n=[0]
def r(m):
    n[0]+=1; L=next(it); return m.group(1)+', '+', '.join(k+":'"+v+"'" for k,v in T[L].items())+m.group(2)
f.s=re.sub(r"(gb_500_a:'[^']*'(?:, wxp_[a-z]+:'[^']*')*)( \})",r,f.s); assert n[0]==7,n
f.rep("const BUILD = '2026-10-09.5';","const BUILD = '2026-10-09.6';")
f.save()
s=open('/home/claude/w/ph.py').read()
if 'holdNeed,' not in s: s=s.replace("names='autopilot,","names='holdNeed,autopilot,"); open('/home/claude/w/ph.py','w').write(s)
