import sys
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add
f=F()
# ---- Prallhöhe als gelb gestrichelte Linie im Vertikalprofil (Freigabe Nutzer 12.10.2026) ----
f.rep("  // Ballon\n  const yb = y(Math.min(Math.max(B.h, zb), top));","""  // Prallhöhe: In dieser Höhe füllt das jetzige Gas die Hülle ganz aus (Gastemperatur mit dem heutigen Abstand zur Luft). Entweicht Gas, wandert sie nach oben
  { const dT = B.Tg - atmAt(ATM, B.h).T; let zp = null; for (let z = zb; z <= top; z += 25){ const a = atmAt(ATM, z); if (B.gas * R_GAS * (a.T + dT) / a.p >= CFG.vol){ zp = z; break; } }
    if (zp != null){ const Y = y(zp); c.save(); c.setLineDash([5, 3]); c.strokeStyle = '#ffe14d'; c.lineWidth = 1.6; c.beginPath(); c.moveTo(xL, Y); c.lineTo(W, Y); c.stroke(); c.setLineDash([]);
      c.fillStyle = '#ffe14d'; c.font = num; c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.fillText(tr('prall_lbl'), xL + 2, Y - 3); c.restore(); } }
  // Ballon
  const yb = y(Math.min(Math.max(B.h, zb), top));""")
# ---- Meldung beim Erreichen, im Fenster der Crew-Meldung ----
f.rep("  else if (heldSeen && B.go){ heldSeen = false; hint.hidden = true; toast(tr('hold_go')); }","  else if (heldSeen && B.go){ heldSeen = false; hint.hidden = true; toast(tr('hold_go')); }\n  else if (B.full && PRALL.armed && B.air && !B.landed){ PRALL.armed = false; hint.hidden = true; toast(tr('prall_hit')); }   // einmal; wieder scharf erst unter 98 % Füllgrad")
f.rep("let heldSeen = false;","let heldSeen = false;\nconst PRALL = {armed: true};")
f.rep("  const hint = $('hint');\n","  const hint = $('hint');\n  if (!B.full && fillNow() < 0.98) PRALL.armed = true;\n")
f.rep("function resetRun(){\n","function resetRun(){\n  PRALL.armed = true;\n")
tx_add(f,{'prall_hit':['Prallhöhe erreicht','Pressure height reached','Altitude de plénitude atteinte','Osiągnięto pułap pełności','Dosažena tlaková výška','已達飽滿高度','Altura de plenitud alcanzada'],
          'prall_lbl':['prall','full','plein','pełny','plný','飽滿','lleno']})
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-12.1', de: ['Prallhöhe: Eine gelb gestrichelte Linie im Vertikalprofil zeigt, in welcher Höhe der Ballon mit dem jetzigen Gas prall wird. Entweicht Gas, wandert sie nach oben. Wird sie erreicht, erscheint „Prallhöhe erreicht“.'],
  en: ['Pressure height: a dashed yellow line in the vertical profile shows at which height the balloon becomes full with its present gas. When gas escapes, it moves up. On reaching it, “Pressure height reached” appears.']},
""")
f.rep("const BUILD = '2026-10-11.5'","const BUILD = '2026-10-12.1'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v44'" in s; open(p,'w').write(s.replace("'v44'","'v45'"))
