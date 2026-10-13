import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---- Bodencrew: Mindestüberschuss je angefangene 500 m³ ein Sack (Vorgabe Nutzer 13.10.2026) ----
f.rep("  holdKg: 30,      // kg Auftriebsüberschuss, ab dem die Bodencrew den Ballon loslässt (Vorgabe Nutzer: rund 30 kg, zwei Säcke)",
      "  holdKg: null,    // kg Auftriebsüberschuss, ab dem die Bodencrew mindestens loslässt; null = je angefangene 500 m³ ein Sack (Vorgabe Nutzer 13.10.2026: 400 m³ ein Sack, 1000 m³ zwei)")
f.rep("  return Math.max(cfg.holdKg || 0, Math.ceil(","  return Math.max(crewMinKg(cfg), Math.ceil(")
f.rep("/* Auftriebsüberschuss, bei dem die Bodencrew loslässt (STE-22):","""const crewMinKg = cfg => cfg.holdKg != null ? cfg.holdKg : (cfg.sackKg || 15) * Math.max(1, Math.ceil((cfg.vol || 1000) / 500));   // Untergrenze der Bodencrew
/* Auftriebsüberschuss, bei dem die Bodencrew loslässt (STE-22):""")
f.rep("if (free < (B.holdKg == null ? cfg.holdKg || 0 : B.holdKg) - 0.1)","if (free < (B.holdKg == null ? crewMinKg(cfg) : B.holdKg) - 0.1)")
f.rep("(B.holdKg == null ? cfg.holdKg || 0 : B.holdKg) + 1 - B.free","(B.holdKg == null ? crewMinKg(cfg) : B.holdKg) + 1 - B.free")
f.s=f.s.replace("B.holdKg == null ? CFG.holdKg : B.holdKg","B.holdKg == null ? crewMinKg(CFG) : B.holdKg")
# ---- Tutorial nennt den tatsächlichen Wert ----
f.rep("Die Crew lässt los, sobald der Ballon 30 kg leichter als die Luft ist.","Die Crew lässt los, sobald der Ballon {kg} kg leichter als die Luft ist.")
f.rep("The crew lets go as soon as the balloon is 30 kg lighter than the air.","The crew lets go as soon as the balloon is {kg} kg lighter than the air.")
f.rep("function tutText(k){ return (TUT_TX[UI.lang] || TUT_TX.en)[k]; }","function tutText(k){ return (TUT_TX[UI.lang] || TUT_TX.en)[k].replace('{kg}', () => nf(B && B.holdKg != null ? B.holdKg : crewMinKg(CFG))); }")
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-13.1', de: ['Start: Wie viel Sand die Bodencrew mindestens sehen will, hängt jetzt vom Ballon ab, je angefangene 500 m³ ein Sack. Ein 400-m³-Ballon startet mit einem Sack, der 1000-m³-Ballon wie bisher mit zwei. Steigt der Ballon damit nicht bis 250 m, verlangt die Crew wie bisher mehr.'],
  en: ['Launch: the minimum the ground crew wants to see now depends on the balloon, one sandbag per started 500 m³. A 400 m³ balloon launches with one bag, the 1000 m³ balloon with two as before. If that does not take the balloon to 250 m, the crew asks for more as before.']},
""")
f.rep("const BUILD = '2026-10-12.2'","const BUILD = '2026-10-13.1'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v46'" in s; open(p,'w').write(s.replace("'v46'","'v47'"))
