import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add,tx_set
f=F()
# ---- Tau ohne Rückfrage ----
a=f.s.index("$('rope').addEventListener('click', () => { if (STATE !== 'play' || B.landed || !B.ok) return; if (B.rope){ toast(tr('rope_out')); return; }"); b=f.s.index("\n",f.s.index("confirmBox(tr('rope_q')",a))
f.s=f.s[:a]+"$('rope').addEventListener('click', () => { if (STATE !== 'play' || B.landed || !B.ok) return; if (B.rope){ toast(tr('rope_out')); return; } ropeThrow(); });   // ohne Rückfrage (Vorgabe Nutzer 10.10.2026)"+f.s[b:]
# ---- Pause: Antippen der Anzeige „Pause“ setzt fort ----
f.rep("#paused{left:50%;top:42%;","#paused{cursor:pointer;left:50%;top:42%;")
f.rep("$('btn-pause').addEventListener('click', () => setPaused(!PAUSED));","$('btn-pause').addEventListener('click', () => setPaused(!PAUSED));\n$('paused').addEventListener('click', () => setPaused(false));")
# ---- Lufträume: Schalter rechts unter den Anzeigen ----
f.rep('      <div class="ov card" id="hint" hidden></div>','      <button class="ov" id="ofm-btn" hidden aria-pressed="false" data-i="ofm_btn"></button>\n      <div class="ov card" id="hint" hidden></div>')
f.rep("#side{left:6px;bottom:8px;","#ofm-btn{right:0;top:230px;min-height:34px;padding:0 9px;border:1px solid var(--line);border-right:0;border-radius:12px 0 0 12px;background:var(--pan);color:var(--mut);font-size:13px;font-weight:500}\n#ofm-btn.on{background:var(--orb);border-color:var(--orb);color:#1a1000}\n#ofm-btn[hidden]{display:none}\n#side{left:6px;bottom:8px;")
f.rep("function applyOfm(tell){","function applyOfm(tell){\n  { const b = $('ofm-btn'); b.classList.toggle('on', !!UI.ofm); b.setAttribute('aria-pressed', UI.ofm ? 'true' : 'false'); document.querySelectorAll('#seg-ofm button').forEach(q => q.classList.toggle('on', q.dataset.v === (UI.ofm ? '1' : '0'))); }")
f.rep("$('in-btn').addEventListener('click', infoOpen);","$('ofm-btn').addEventListener('click', () => { UI.ofm = UI.ofm ? 0 : 1; saveUI(); applyOfm(true); });\n$('in-btn').addEventListener('click', infoOpen);")
f.rep("  $('i-fill').textContent = nf(fillNow() * 100, 0) + ' %';","  $('i-fill').textContent = nf(fillNow() * 100, 0) + ' %';\n  { const b = $('ofm-btn'), on = STATE === 'play' || STATE === 'done'; if (b.hidden === on) b.hidden = !on; if (on){ const t = ($('inst').offsetHeight + 6) + 'px'; if (b.style.top !== t) b.style.top = t; } }")
tx_add(f,{'ofm_btn':['Lufträume','Airspace','Espaces aér.','Przestrzenie','Vzd. prostory','空域','Espacio aéreo'],
 'r_map':['Weg auf der Karte','Track on the map','Trajet sur la carte','Trasa na mapie','Trasa na mapě','在地圖上看航跡','Recorrido en el mapa'],
 'r_full':['Auswertung','Results','Résultats','Wyniki','Vyhodnocení','結果','Resultados']})
# ---- Nach der Landung: Weg auf der Karte, Ergebnis klein links unten ----
f.rep('        <button class="sec" id="r-review" data-i="rv_title"></button>','        <button class="sec" id="r-full" data-i="r_full"></button>\n        <button class="sec" id="r-map" data-i="r_map"></button>\n        <button class="sec" id="r-review" data-i="rv_title"></button>')
f.rep("#result #r-review{margin-bottom:6px}","#result #r-review{margin-bottom:6px}\n#result #r-full{display:none}\n#result.mini{left:6px;top:auto;bottom:8px;transform:none;width:178px;padding:9px 10px 8px}\n#result.mini > *{display:none}\n#result.mini > h2{display:block;font-size:17px;margin:0 0 2px}\n#result.mini > #r-full,#result.mini > #r-review,#result.mini > #r-menu{display:block;min-height:36px;margin:5px 0 0}")
f.rep("$('r-menu').addEventListener('click', showMenu);","$('r-menu').addEventListener('click', showMenu);\n$('r-map').addEventListener('click', () => { $('result').classList.add('mini'); follow = false; $('follow').hidden = true; map.invalidateSize(); if (pathPts.length > 1) map.fitBounds(L.latLngBounds(pathPts), {paddingTopLeft: [110, 20], paddingBottomRight: [115, 170]}); else map.setView(balMk.getLatLng(), 13); });   // Weg ansehen (SPI-19)\n$('r-full').addEventListener('click', () => $('result').classList.remove('mini'));")
f.rep("  cheerQ = 0.5; const k = TASK(), rows = [],","  $('result').classList.remove('mini'); cheerQ = 0.5; const k = TASK(), rows = [],")
# ---- Tutorial ----
f.rep("'seg-speed', 'btn-set', 'corner', 'hint'], seen: false,","'seg-speed', 'btn-set', 'corner', 'hint', 'ofm-btn'], gone: false, tS: 0,")
f.rep("{k: 'opts', show: ['btn-set'], at: 'btn-set'}","{k: 'opts', show: ['btn-set', 'ofm-btn'], at: 'btn-set'}")
f.rep("{k: 'land', at: 'valve', done:","{k: 'land', at: 'valve', away: 3, done:")
f.rep("  TUT.mU0 = B.mU; TUT.s0 = B.sacks; TUT.vT = 0;","  TUT.mU0 = B.mU; TUT.s0 = B.sacks; TUT.vT = 0; TUT.gone = false; TUT.tS = performance.now();")
f.rep("function tutNext(){ if (TUT.i >= TUT.steps.length - 1){ tutEnd(true); return; } TUT.i++; tutShow(); }","function tutNext(){ if (TUT.i >= TUT.steps.length - 1){ tutEnd(true); return; } TUT.i++; tutShow(); }\nfunction tutClick(){\n  if (PAUSED){ setPaused(false); return; }                                   // nach einer Pause (Handy war aus) geht es mit „Weiter“ weiter\n  const s = TUT.steps[TUT.i]; if ($('tut-next').disabled) return;\n  if (s.done && s.away){ TUT.gone = true; $('tut').hidden = true; $('tut-hand').hidden = true; return; }   // Fenster ausblenden und die Fahrt in Ruhe zu Ende fahren\n  tutNext();\n}")
f.rep("$('tut-next').addEventListener('click', () => { if (!$('tut-next').disabled) tutNext(); });","$('tut-next').addEventListener('click', tutClick);")
f.rep("  if (s.ready && $('tut-next').disabled && s.ready()) $('tut-next').disabled = false;","  if (PAUSED){ if ($('tut').hidden){ $('tut').hidden = false; } $('tut-next').disabled = false; return; }\n  if (TUT.gone && !$('tut').hidden && !(s.done && s.done())){ $('tut').hidden = true; }\n  if (s.ready && $('tut-next').disabled && s.ready()) $('tut-next').disabled = false;\n  if (s.away && $('tut-next').disabled && performance.now() - TUT.tS > s.away * 1000) $('tut-next').disabled = false;\n  if (!PAUSED && !s.away && !s.ready && !!s.done !== $('tut-next').disabled) $('tut-next').disabled = !!s.done;")
f.rep("Sinkt er zu schnell, gib eine Schaufel Sand ab.'","Sinkt er zu schnell, gib eine Schaufel Sand ab. „Weiter“ blendet dieses Fenster aus; nach der Landung geht es weiter.'")
f.rep("Touch down at less than 1 m/s for a gentle landing. If it sinks too fast, release a scoop of sand.'","Touch down at less than 1 m/s for a gentle landing. If it sinks too fast, release a scoop of sand. “Next” hides this window; after landing the tutorial continues.'")
f.rep("und die Seite „Karten und Daten“. Viele entdecken diesen Knopf erst spät.'","und die Seite „Karten und Daten“. Viele entdecken diesen Knopf erst spät. Der Schalter „Lufträume“ unter den Anzeigen blendet die Luftfahrtkarte ein und aus.'")
f.rep("and the page “Maps and data”. Many people discover this button late.'","and the page “Maps and data”. Many people discover this button late. The switch “Airspace” below the instruments shows and hides the aeronautical chart.'")
f.rep("const BUILD = '2026-10-10.4'","const BUILD = '2026-10-10.5'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v36'" in s; open(p,'w').write(s.replace("'v36'","'v37'"))
