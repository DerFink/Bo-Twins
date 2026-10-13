import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("/* Eine Fahrt nach Plan durchrechnen:","""/* Autopilot des Spielers: hält die Höhe hT (m über Start) auf ±5 m, mit kleinen Portionen Sand oder Gas. Alle 2 s aufrufen.
   Gesteuert wird der Auftriebsüberschuss: Er bestimmt die Geschwindigkeit, auf die der Ballon zuläuft. Gibt {sand, gas} zurück (kg Sand, kg Auftrieb aus Gas),
   damit die Oberfläche Vorräte und Abschaltgrenzen prüfen kann; ausgeführt wird erst, wenn ok(…) zustimmt. */
function holdAlt(B, cfg, tab, hT, ok){
  const a = atmAt(tab, B.h), rho = a.p * M_AIR / (R_GAS * a.T), k = 0.5 * rho * dragArea(cfg, B.fill == null ? 1 : B.fill);
  const err = hT - B.h, wSoll = Math.max(-1.2, Math.min(1.2, err / 25)), lead = B.w * 8;     // Vorhalt: wohin der Ballon in 8 s kommt
  const near = Math.abs(err - lead) < 4 && Math.abs(B.w) < 0.25;
  const need = k * wSoll * Math.abs(wSoll) / G0 - (B.free || 0) - (near ? 0 : 0.6 * k * B.w * Math.abs(B.w) / G0) * 0;
  const thr = near ? 0.5 : 0.12;                                                   // im Band nur gröbere Abweichungen ausgleichen, sonst ständiges Hin und Her
  if (need > thr){ const kg = Math.min(3, need); if (!ok || ok('sand', kg)){ dropKg(B, cfg, kg); return {sand: kg, gas: 0}; } }
  else if (need < -thr){ const kg = Math.min(3, -need); if (!ok || ok('gas', kg)){ B.gas = Math.max(0, B.gas - kg / (M_AIR * B.Tg / a.T - M_H2)); return {sand: 0, gas: kg}; } }
  return {sand: 0, gas: 0};
}
/* Eine Fahrt nach Plan durchrechnen:""")
f.save()
