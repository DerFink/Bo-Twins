import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add,tx_set
f=F()
# ---------- Physik: Füllgrad bestimmt die Form und damit den Widerstand (STE-25) ----------
f.rep("  cw: 0.45,        // Widerstandsbeiwert der Hülle, Kugel (Annahme, OP-16)",
"""  cw: 0.45,        // Widerstandsbeiwert der prallen Hülle, Kugel (Annahme, OP-16)
  cdaMin: 6,       // m², Widerstandsfläche (cw × Fläche) der leeren, flatternden Hülle mit Korb: ergibt rund 50 m/s im freien Fall (Angabe eines Ballonpiloten)
  shapeK: 5,       // Form der Kurve zwischen leer und prall: Die Wirkung ist anfangs sehr gering und am Ende sehr deutlich (Vorgabe Nutzer 10.10.2026; die Kurve selbst ist eine Annahme)""")
f.rep("function stepBalloon(B, cfg, tab, dt, valve){",
"""/* Widerstandsfläche cw × A in m² je nach Füllgrad f (0 bis 1). Prall: Kugel wie bisher. Verliert der Ballon Gas, hängt der untere Teil der
   Hülle schlaff; bis etwa zur Hälfte ändert das den Querschnitt kaum, die fast leere Hülle bietet der Luft kaum noch Fläche. */
function dragArea(cfg, f){
  const full = cfg.cw * Math.PI * Math.pow(3 * cfg.vol / (4 * Math.PI), 2 / 3), lo = Math.min(full, cfg.cdaMin == null ? full : cfg.cdaMin), K = cfg.shapeK || 5;
  return lo + (full - lo) * (1 - Math.exp(-K * Math.max(0, Math.min(1, f)))) / (1 - Math.exp(-K));
}
function stepBalloon(B, cfg, tab, dt, valve){""")
f.rep("  const area = Math.PI * Math.pow(3 * cfg.vol / (4 * Math.PI), 2 / 3);\n  const k = 0.5 * rho * cfg.cw * area;",
      "  B.fill = Math.min(1, V / cfg.vol);                                       // Füllgrad: Gasvolumen bei Druck und Gastemperatur am Ort, bezogen auf das Hüllenvolumen\n  const k = 0.5 * rho * dragArea(cfg, B.fill);")
f.rep("  const k = 0.5 * rho * cfg.cw * Math.PI * Math.pow(3 * cfg.vol / (4 * Math.PI), 2 / 3);\n  let wSoll;","  const k = 0.5 * rho * dragArea(cfg, B.fill == null ? 1 : B.fill);\n  let wSoll;")
f.rep("marks: 0, rope: false, ropeOn: 0,","marks: 0, rope: false, ropeOn: 0, fill: 1,")
# ---------- Anzeige: Füllgrad statt Gas relativ zum Start ----------
f.rep("  $('i-fill').textContent = nf(B.gas0 > 0 ? B.gas / B.gas0 * 100 : 0, 1) + ' %';","  $('i-fill').textContent = nf(fillNow() * 100, 0) + ' %';\n  if (!$('detail').hidden) detailDraw();")
tx_set(f,'fill',['Füllgrad','Fill','Rempl.','Wypełn.','Naplnění','充氣率','Llenado'])
# ---------- Detailfenster: Tipp auf den Ballon ----------
f.rep("keyboard: false, interactive: false, zIndexOffset: 500, icon: L.divIcon({className: 'mk', iconSize: [44, 54]","keyboard: false, interactive: true, zIndexOffset: 500, icon: L.divIcon({className: 'mk', iconSize: [44, 54]")
f.rep('    <div class="full" id="busy" hidden>','''    <!-- Ballon im Detail (STE-26): Tipp auf den Ballon öffnet, Tipp auf das Fenster schließt -->
    <div class="full" id="detail" hidden>
      <div class="card">
        <h2 data-i="dt_title"></h2>
        <div id="dt-rows"></div>
        <p class="note" data-i="dt_note"></p>
      </div>
    </div>

    <div class="full" id="busy" hidden>''')
f.rep("#review{z-index:880}","#detail{z-index:885}\n#detail .card{width:min(360px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px 14px 10px;background:#0d1626}\n#detail .kv{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid rgba(154,171,196,.14);font-size:14.5px}\n#detail .kv b{font-family:var(--num);font-size:16px;white-space:nowrap}\n#review{z-index:880}")
f.rep("/* ---------- Zeitschleife ---------- */","""/* ---------- Ballon im Detail (STE-26) ---------- */
function fillNow(){ const a = atmAt(ATM, B.h); return Math.max(0, Math.min(1, B.gas * R_GAS * B.Tg / a.p / CFG.vol)); }
function detailDraw(){
  const a = atmAt(ATM, B.h), V = B.gas * R_GAS * B.Tg / a.p, f = fillNow(), load = fixedKg(CFG) + sandKg(B, CFG) + B.marks * CFG.markKg + (B.wet || 0);
  const rows = [['dt_fill', nf(f * 100, 1) + ' %'], ['dt_gasrel', nf(B.gas0 > 0 ? 100 * B.gas / B.gas0 : 0, 1) + ' %'], ['dt_vol', nf(Math.round(Math.min(V, CFG.vol))) + ' / ' + nf(CFG.vol) + ' m³'],
    ['dt_tg', nf(B.Tg - 273.15, 1) + ' °C'], ['dt_ta', nf(a.T - 273.15, 1) + ' °C'], ['dt_dt', fmtV(B.Tg - a.T) + ' K'], ['dt_free', fmtV(B.free || 0) + ' kg'],
    ['dt_mass', nf(Math.round(load + B.gas * M_H2)) + ' kg'], ['dt_sand', nf(sandKg(B, CFG), 1) + ' kg'], ['dt_gasm', nf(B.gas * M_H2, 1) + ' kg'], ['dt_wet', nf(B.wet || 0, 1) + ' kg'],
    ['dt_rope', B.rope ? (B.ropeOn > 0.05 ? nf(B.ropeOn / CFG.ropeKgM) + ' m · −' + nf(B.ropeOn, 1) + ' kg' : tr('dt_rope_air')) : tr('dt_rope_in')], ['dt_cda', nf(dragArea(CFG, f), 1) + ' m²']];
  const box = $('dt-rows'); box.textContent = '';
  rows.forEach(r => { const d = document.createElement('div'), s = document.createElement('span'), v = document.createElement('b'); d.className = 'kv'; s.textContent = tr(r[0]); v.textContent = r[1]; d.appendChild(s); d.appendChild(v); box.appendChild(d); });
}
function detailOpen(){ if (STATE !== 'play' && STATE !== 'done') return; $('detail').hidden = false; detailDraw(); }
balMk.on('click', detailOpen); $('detail').addEventListener('click', () => { $('detail').hidden = true; });

/* ---------- Zeitschleife ---------- */""")
tx_add(f,{
 'dt_title':['Ballon im Detail','Balloon details','Le ballon en détail','Balon w szczegółach','Balon podrobně','氣球詳細資料','El globo en detalle'],
 'dt_note':['Füllgrad: wie prall die Hülle ist; er bestimmt Form und Luftwiderstand. Gas zum Start: wie viel Gas noch an Bord ist. Tippen schließt.','Fill: how taut the envelope is; it sets shape and drag. Gas vs. launch: how much gas is still on board. Tap to close.','Remplissage : tension de l’enveloppe ; il fixe la forme et la traînée. Gaz par rapport au départ : gaz encore à bord. Touchez pour fermer.','Wypełnienie: jak napięta jest powłoka; decyduje o kształcie i oporze. Gaz względem startu: ile gazu zostało. Dotknij, aby zamknąć.','Naplnění: jak napnutý je obal; určuje tvar a odpor. Plyn vůči startu: kolik plynu zbývá. Klepnutím zavřete.','充氣率：氣囊有多飽滿，決定外形與阻力。相對起飛的氣體：機上還剩多少氣體。點一下關閉。','Llenado: lo tensa que está la envoltura; fija la forma y la resistencia. Gas respecto al despegue: cuánto gas queda. Toca para cerrar.'],
 'dt_fill':['Füllgrad','Fill','Remplissage','Wypełnienie','Naplnění','充氣率','Llenado'],
 'dt_gasrel':['Gas zum Start','Gas vs. launch','Gaz / départ','Gaz względem startu','Plyn vůči startu','相對起飛的氣體','Gas respecto al despegue'],
 'dt_vol':['Gasvolumen','Gas volume','Volume de gaz','Objętość gazu','Objem plynu','氣體體積','Volumen de gas'],
 'dt_tg':['Gastemperatur','Gas temperature','Température du gaz','Temperatura gazu','Teplota plynu','氣體溫度','Temperatura del gas'],
 'dt_ta':['Lufttemperatur','Air temperature','Température de l’air','Temperatura powietrza','Teplota vzduchu','氣溫','Temperatura del aire'],
 'dt_dt':['Gas gegen Luft','Gas minus air','Gaz − air','Gaz − powietrze','Plyn − vzduch','氣體減氣溫','Gas − aire'],
 'dt_free':['Auftriebsüberschuss','Free lift','Force ascensionnelle libre','Nadmiar wyporu','Volný vztlak','淨浮力','Empuje libre'],
 'dt_mass':['Gesamtmasse','Total mass','Masse totale','Masa całkowita','Celková hmotnost','總質量','Masa total'],
 'dt_sand':['Sand','Sand','Sable','Piasek','Písek','沙','Arena'],
 'dt_gasm':['Masse des Gases','Mass of the gas','Masse du gaz','Masa gazu','Hmotnost plynu','氣體質量','Masa del gas'],
 'dt_wet':['Wasser auf der Hülle','Water on the envelope','Eau sur l’enveloppe','Woda na powłoce','Voda na obalu','氣囊上的水','Agua en la envoltura'],
 'dt_rope':['Schlepptau','Trail rope','Guiderope','Lina wleczna','Vlečné lano','拖繩','Cuerda guía'],
 'dt_rope_in':['eingerollt','stowed','enroulé','zwinięta','svinuté','收著','recogida'],
 'dt_rope_air':['hängt frei','hanging free','pend librement','wisi swobodnie','visí volně','懸空','cuelga libre'],
 'dt_cda':['Widerstandsfläche','Drag area','Surface de traînée','Powierzchnia oporu','Odporová plocha','阻力面積','Área de resistencia'],
 'rope_q':['Schlepptau auswerfen? Es lässt sich in dieser Fahrt nicht wieder einrollen.','Deploy the trail rope? It cannot be hauled in again during this flight.','Déployer le guiderope ? Il ne peut plus être remonté pendant ce vol.','Wypuścić linę wleczną? W tym locie nie da się jej już wciągnąć.','Spustit vlečné lano? V tomto letu ho už nelze vytáhnout.','要放下拖繩嗎？這次飛行中無法再收回。','¿Soltar la cuerda guía? No se puede recoger de nuevo en este vuelo.'],
 'rope_ok':['Auswerfen','Deploy','Déployer','Wypuść','Spustit','放下','Soltar'],
 'rope_out':['Das Schlepptau ist draußen und bleibt es bis zur Landung.','The trail rope is out and stays out until landing.','Le guiderope est sorti et le reste jusqu’à l’atterrissage.','Lina wleczna jest wypuszczona i zostaje do lądowania.','Vlečné lano je venku a zůstane do přistání.','拖繩已放下，直到降落都不能收回。','La cuerda guía está fuera y así sigue hasta aterrizar.'],
 'rv_rope':['Schlepptau ausgeworfen','trail rope deployed','guiderope déployé','wypuszczono linę wleczną','vlečné lano spuštěno','已放下拖繩','cuerda guía soltada'],
 'rv_legend2':['Sandfarbene gestrichelte Linie: Schlepptau ausgeworfen.','Sand-coloured dashed line: trail rope deployed.','Ligne pointillée couleur sable : guiderope déployé.','Piaskowa linia przerywana: wypuszczono linę wleczną.','Písková čárkovaná čára: vlečné lano spuštěno.','沙色虛線：放下拖繩。','Línea discontinua color arena: cuerda guía soltada.'],
})
# ---------- Schlepptau: nur auswerfen, nicht wieder einrollen (STE-20) ----------
f.rep("$('rope').addEventListener('click', () => { if (STATE !== 'play' || B.landed || !B.ok) return; B.rope = !B.rope; SND.rope(); });",
"""function ropeThrow(){ if (STATE !== 'play' || B.landed || !B.ok || B.rope) return false; B.rope = true; B.ropeT = B.t; SND.rope(); return true; }
$('rope').addEventListener('click', () => { if (STATE !== 'play' || B.landed || !B.ok) return; if (B.rope){ toast(tr('rope_out')); return; }
  if (typeof TUT !== 'undefined' && TUT.on){ ropeThrow(); return; }
  confirmBox(tr('rope_q'), tr('rope_ok')).then(ok => { if (ok) ropeThrow(); }); });""")
tx_set(f,'rope_a',['Schlepptau auswerfen (einmal je Fahrt)','Deploy the trail rope (once per flight)','Déployer le guiderope (une fois par vol)','Wypuść linę wleczną (raz na lot)','Spustit vlečné lano (jednou za let)','放下拖繩（每次飛行一次）','Soltar la cuerda guía (una vez por vuelo)'])
# ---------- Rückblick: Füllgrad und Tau ----------
f.rep("const REC = {k: ['t', 'h', 'g', 'w', 'dT', 'Ta', 'sand', 'gas', 'wet', 'sun', 'cu', 'rain', 'free', 'valve'],","const REC = {k: ['t', 'h', 'g', 'w', 'dT', 'Ta', 'sand', 'gas', 'fill', 'rope', 'wet', 'sun', 'cu', 'rain', 'free', 'valve'],")
f.rep("REC.gas.push(B.gas0 > 0 ? 100 * B.gas / B.gas0 : 0);","REC.gas.push(B.gas0 > 0 ? 100 * B.gas / B.gas0 : 0); REC.fill.push(100 * fillNow()); REC.rope.push(B.rope ? 1 : 0);")
f.rep("    const v = REC.valve; for (let i = 0; i + 1 < v.length; i += 2) v[i] = v[i] || v[i + 1];","    const v = REC.valve; for (let i = 0; i + 1 < v.length; i += 2) v[i] = v[i] || v[i + 1];\n    { const r = REC.rope; for (let i = 0; i + 1 < r.length; i += 2) r[i] = r[i] && (i === 0 || r[i - 1] || !r[i + 1]) ? r[i] : r[i]; }")
f.rep("    if (REC.valve[i]){ c.fillStyle = '#ff6e5f'; c.fillRect(X - 1.2, P[0][1] - 12, 2.4, 12); }",
"    if (REC.valve[i]){ c.fillStyle = '#ff6e5f'; c.fillRect(X - 1.2, P[0][1] - 12, 2.4, 12); }\n    if (REC.rope[i] && !REC.rope[i - 1]){ c.strokeStyle = '#d9b36c'; c.lineWidth = 1.6; c.setLineDash([5, 3]); c.beginPath(); c.moveTo(X, P[0][0]); c.lineTo(X, P[0][1]); c.stroke(); c.setLineDash([]); c.fillStyle = '#d9b36c'; c.font = small; c.textAlign = X > xR - 60 ? 'right' : 'left'; c.textBaseline = 'alphabetic'; c.fillText(tr('rope'), X + (X > xR - 60 ? -4 : 4), P[0][1] - 4); }")
f.rep("' kg · ' + tr('fill') + ' ' + nf(REC.gas[i], 1) + ' % · ' + sky","' kg · ' + tr('fill') + ' ' + nf(REC.fill[i], 0) + ' % · ' + tr('dt_gasrel') + ' ' + nf(REC.gas[i], 1) + ' % · ' + sky")
f.rep("  if (dSand >= 0.15) parts.push([dSand, tr('rv_sand', {kg: nf(dSand, 1)})]);","  if (dSand >= 0.15) parts.push([dSand, tr('rv_sand', {kg: nf(dSand, 1)})]);\n  if (REC.rope[i] && !REC.rope[j]) parts.push([0.01, tr('rv_rope')]);")
f.rep('<p class="note" data-i="rv_legend"></p>','<p class="note"><span data-i="rv_legend"></span> <span data-i="rv_legend2"></span></p>')
# ---------- Sandsäcke werden entleert, nicht abgeworfen ----------
tx_set(f,'sw_note',['Der Ballon steht im Gleichgewicht. Die Zeit läuft zu Beginn 1×; zum Abheben Sand abgeben.','The balloon is in equilibrium. Time starts at 1×; release sand to take off.','Le ballon est en équilibre. Le temps démarre à 1× ; videz du sable pour décoller.','Balon jest w równowadze. Czas biegnie na początku 1×; aby wystartować, wysyp piasek.','Balón je v rovnováze. Čas běží zpočátku 1×; ke vzletu vysypte písek.','氣球處於平衡狀態。開始時時間為 1×；倒出沙子即可升空。','El globo está en equilibrio. El tiempo empieza a 1×; vacía arena para despegar.'])
tx_set(f,'hint_start',['Der Ballon steht im Gleichgewicht. Tippe auf die Sandsäcke oder die Schaufel, um Sand abzugeben.','The balloon is in equilibrium. Tap the sandbags or the scoop to release sand.','Le ballon est en équilibre. Touchez les sacs de sable ou la pelle pour vider du sable.','Balon jest w równowadze. Dotknij worków z piaskiem lub łopatki, aby wysypać piasek.','Balón je v rovnováze. Klepněte na pytle s pískem nebo na lopatku a vysypte písek.','氣球處於平衡狀態。點一下沙袋或沙鏟以倒出沙子。','El globo está en equilibrio. Toca los sacos de arena o la pala para vaciar arena.'])
tx_set(f,'drop_sack',['Sandsack entleeren','Empty a sandbag','Vider un sac de sable','Opróżnij worek z piaskiem','Vysypat pytel s pískem','倒空一個沙袋','Vaciar un saco de arena'])
tx_set(f,'hint_hold',['Die Bodencrew hält den Ballon, bis er {kg} kg leichter als Luft ist. Noch {rest} kg Sand abgeben.','The ground crew holds the balloon until it is {kg} kg lighter than air. Release another {rest} kg of sand.','L’équipe au sol retient le ballon jusqu’à ce qu’il soit plus léger que l’air de {kg} kg. Encore {rest} kg de sable à vider.','Obsługa naziemna trzyma balon, aż będzie o {kg} kg lżejszy od powietrza. Wysyp jeszcze {rest} kg piasku.','Pozemní posádka drží balon, dokud není o {kg} kg lehčí než vzduch. Vysypte ještě {rest} kg písku.','地勤人員會拉住氣球，直到它比空氣輕 {kg} 公斤。還需倒出 {rest} 公斤沙。','El equipo de tierra sujeta el globo hasta que sea {kg} kg más ligero que el aire. Vacía otros {rest} kg de arena.'])
tx_set(f,'rv_sand',['{kg} kg Sand abgegeben','{kg} kg sand released','{kg} kg de sable vidés','wysypano {kg} kg piasku','vysypáno {kg} kg písku','倒出 {kg} 公斤沙','{kg} kg de arena vaciados'])
for a,b in [("Zum Abheben zwei Säcke abwerfen.","Zum Abheben zwei Säcke entleeren."),("Drop two bags to lift off.","Empty two bags to lift off."),("Lâchez deux sacs pour décoller.","Videz deux sacs pour décoller."),("Aby wystartować, zrzuć dwa worki.","Aby wystartować, opróżnij dwa worki."),("Ke startu shoďte dva pytle.","Ke startu vysypte dva pytle."),("拋下兩袋沙即可起飛。","倒空兩袋沙即可起飛。"),("Suelta dos sacos para despegar.","Vacía dos sacos para despegar.")]: f.rep(a,b)
f.rep("const BUILD = '2026-10-09.11'","const BUILD = '2026-10-10.1'")
f.save()
