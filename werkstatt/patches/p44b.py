import sys
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add
f=F()
# ---- Bedienfeld: Autopilot-Knopf und Wahl NN / über Grund in der Spalte des Taus ----
f.rep("""          <b id="n-rope"></b>
        </button>
      </div>""","""          <b id="n-rope"></b>
        </button>
        <button id="ap-btn" data-ia="ap_a" aria-label="Autopilot" aria-pressed="false">AP</button>
        <button id="ap-mode" data-ia="ap_mode_a" aria-label="Autopilot: Höhe NN oder über Grund">NN</button>
      </div>""")
f.rep("#rope{flex:1;margin-top:3px;min-height:62px;","#rope{flex:1;margin-top:3px;min-height:34px;")
f.rep("#rope .hang{display:none}","""#ap-btn{margin-top:4px;min-height:32px;border-radius:10px;border:1px solid var(--line);background:#0d1626;color:var(--tx);font-family:var(--num);font-size:15px;font-weight:700;letter-spacing:.04em;padding:0}
#ap-btn.on{background:#2d1f4d;border-color:#c08cff;color:#eadcff;box-shadow:0 0 0 1px #c08cff inset}
#ap-mode{margin-top:3px;min-height:22px;border-radius:7px;border:1px solid var(--line);background:transparent;color:var(--mut);font-family:var(--num);font-size:11px;font-weight:600;padding:0}
#rope .hang{display:none}""")
# ---- Logik ----
f.rep("let heldSeen = false;","""let heldSeen = false;
/* Autopilot (Wunsch Nutzer 12.10.2026): hält die Höhe beim Einschalten auf ±5 m, NN oder über Grund. Steuerung: holdAlt im Rechenkern.
   Aus bei eigenem Sand oder Ventil, bei Sand unter der Landereserve (6 kg je 100 m³ Hülle) und wenn Gas nötig wäre, der Füllgrad aber unter 40 % liegt. */
const AP_HIDE = [];                                  // Aufgaben (TASK()), in denen der Autopilot ausgeblendet ist, z. B. ['gb']; Vorgabe Nutzer: erst einmal überall
const AP = {on: false, agl: store.get('gb-apmode', 0) === 1, h: 0, t: 0, sandX: null};
const apReserve = () => 0.06 * CFG.vol;
const apAllowed = () => !AP_HIDE.includes(TASK()) && !(typeof TUT !== 'undefined' && TUT.on);
function apShow(){ const b = $('ap-btn'), m = $('ap-mode'), vis = apAllowed(); b.hidden = !vis; m.hidden = !vis; b.classList.toggle('on', AP.on); b.setAttribute('aria-pressed', AP.on ? 'true' : 'false'); m.textContent = tr(AP.agl ? 'ap_agl' : 'ap_nn'); }
function apOff(why){ if (!AP.on) return; AP.on = false; AP.sandX = null; apShow(); if (why) toast(tr('ap_off_' + why)); }
function apOn(){
  if (STATE !== 'play' || !B.air || B.landed || !B.ok){ toast(tr('ap_air')); return; }
  const agl = B.h - B.gnd; if (AP.agl && agl < 100){ toast(tr('ap_low')); return; }
  if (sandKg(B, CFG) <= apReserve()){ toast(tr('ap_off_sand')); return; }
  AP.on = true; AP.h = AP.agl ? agl : B.h; AP.t = B.t; AP.sandX = sandKg(B, CFG); apShow(); toast(tr('ap_on'));
}
function apStep(){                                   // in jedem Rechenschritt; gesteuert wird alle 2 s Fahrzeit
  if (!AP.on) return;
  if (B.landed || !B.ok || STATE !== 'play'){ apOff(null); return; }
  const s = sandKg(B, CFG); if (valve > 0 || (AP.sandX != null && s < AP.sandX - 0.05)){ apOff('hand'); return; }
  if (B.t - AP.t < 2) return; AP.t = B.t;
  holdAlt(B, CFG, ATM, AP.agl ? B.gnd + AP.h : AP.h, (what, kg) => {
    if (what === 'sand' && s - kg < apReserve()){ apOff('sand'); return false; }
    if (what === 'gas' && fillNow() < 0.4){ apOff('gas'); return false; }
    return true; });
  AP.sandX = sandKg(B, CFG);
}
$('ap-btn').addEventListener('click', () => { if (AP.on) apOff('hand'); else apOn(); });
$('ap-mode').addEventListener('click', () => { AP.agl = !AP.agl; store.set('gb-apmode', AP.agl ? 1 : 0);
  if (AP.on){ const agl = B.h - B.gnd; if (AP.agl && agl < 100){ apOff(null); toast(tr('ap_low')); } else AP.h = AP.agl ? agl : B.h; }
  apShow(); });""")
f.rep("while (simDt > 1e-6 && !B.landed){ const d = Math.min(0.25, simDt); stepBalloon(B, CFG, ATM, d, valve);","while (simDt > 1e-6 && !B.landed){ const d = Math.min(0.25, simDt); apStep(); stepBalloon(B, CFG, ATM, d, valve);")
f.rep("function resetRun(){\n","function resetRun(){\n  AP.on = false; AP.sandX = null;\n")
f.rep("  B = s.B; valve = 0; shown = false; SND.valve(0); recReset();","  B = s.B; valve = 0; shown = false; SND.valve(0); recReset(); AP.on = false; AP.sandX = null;")
f.rep("+ (B.rope ? ' · ' + tr('rope') : '');","+ (B.rope ? ' · ' + tr('rope') : '') + (AP.on ? ' · AP' : '');")
f.rep("  const hint = $('hint');\n","  const hint = $('hint');\n  if ($('ap-btn').hidden === apAllowed() || $('ap-btn').classList.contains('on') !== AP.on) apShow();\n")
# ---- Sollhöhe im Vertikalprofil ----
f.rep("  // Ballon\n  const yb = y(Math.min(Math.max(B.h, zb), top));","""  if (AP.on){ const hT = AP.agl ? B.gnd + AP.h : AP.h; if (hT >= zb && hT <= top){ const Y = y(hT); c.save(); c.strokeStyle = '#c08cff'; c.lineWidth = 1.6; c.beginPath(); c.moveTo(xL, Y); c.lineTo(W, Y); c.stroke();
    c.fillStyle = '#c08cff'; c.font = num; c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText('AP', xL + 2, Y + 2); c.restore(); } }   // Sollhöhe des Autopiloten
  // Ballon
  const yb = y(Math.min(Math.max(B.h, zb), top));""")
tx_add(f,{
 'ap_a':['Autopilot: Höhe halten','Autopilot: hold altitude','Pilote automatique : maintenir l’altitude','Autopilot: utrzymuj wysokość','Autopilot: držet výšku','自動駕駛：保持高度','Piloto automático: mantener altura'],
 'ap_mode_a':['Autopilot: Höhe NN oder über Grund','Autopilot: altitude above sea level or above ground','Pilote automatique : altitude mer ou sol','Autopilot: wysokość n.p.m. lub nad terenem','Autopilot: výška n. m. nebo nad terénem','自動駕駛：海拔或離地高度','Piloto automático: altura s. n. m. o sobre el suelo'],
 'ap_nn':['NN','MSL','mer','n.p.m.','n. m.','海拔','s.n.m.'],
 'ap_agl':['Grund','AGL','sol','teren','terén','離地','suelo'],
 'ap_on':['Autopilot hält die Höhe','Autopilot holds the altitude','Le pilote automatique maintient l’altitude','Autopilot utrzymuje wysokość','Autopilot drží výšku','自動駕駛保持高度','El piloto automático mantiene la altura'],
 'ap_off_hand':['Autopilot aus','Autopilot off','Pilote automatique coupé','Autopilot wyłączony','Autopilot vypnut','自動駕駛已關閉','Piloto automático desactivado'],
 'ap_off_sand':['Autopilot aus: Sandreserve','Autopilot off: sand reserve','Pilote automatique coupé : réserve de sable','Autopilot wyłączony: rezerwa piasku','Autopilot vypnut: rezerva písku','自動駕駛關閉：沙袋存量','Piloto automático desactivado: reserva de arena'],
 'ap_off_gas':['Autopilot aus: wenig Gas','Autopilot off: low gas','Pilote automatique coupé : peu de gaz','Autopilot wyłączony: mało gazu','Autopilot vypnut: málo plynu','自動駕駛關閉：氣體不足','Piloto automático desactivado: poco gas'],
 'ap_low':['Autopilot über Grund erst ab 100 m','Autopilot above ground only from 100 m','Pilote automatique sol à partir de 100 m','Autopilot nad terenem dopiero od 100 m','Autopilot nad terénem až od 100 m','離地自動駕駛需 100 公尺以上','Piloto automático sobre el suelo desde 100 m'],
 'ap_air':['Autopilot erst in der Luft','Autopilot only in the air','Pilote automatique seulement en vol','Autopilot dopiero w powietrzu','Autopilot až ve vzduchu','自動駕駛僅在空中可用','Piloto automático solo en el aire']})
# ---- Tutorial: Hinweise auf die Griffe (Findings 1 und 2) ----
s=f.s
for a,b in [("ob der Ballon gerade beschleunigt.',\n  prof:","ob der Ballon gerade beschleunigt. Mit dem kleinen Griff unten klappst du die Anzeigen in drei Längen ein; die kürzeste zeigt nur Höhe und Vario.',\n  prof:"),
            ("sobald der Ballon 30 kg leichter als die Luft ist.',","sobald der Ballon 30 kg leichter als die Luft ist. Über den kleinen Griff am Rand lässt sich dieses Bedienfeld klein machen, wenn du mehr Karte sehen willst.',")]:
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
f.s=s
f.save()
