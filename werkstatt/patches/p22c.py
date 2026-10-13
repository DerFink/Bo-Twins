import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("function loadout(cfg, tab){\n  const a = atmAt(tab, 0);\n  const n = a.p * cfg.vol / (R_GAS * a.T);              // mol Traggas in der vollen Hülle\n  const lift = n * (M_AIR - M_H2);                      // kg: verdrängte Luft minus Gas",
"function loadout(cfg, tab, Tg){                           // Tg: Temperatur des Traggases am Startplatz; ohne Angabe die der Luft\n  const a = atmAt(tab, 0);\n  const n = a.p * cfg.vol / (R_GAS * (Tg || a.T));      // mol Traggas in der vollen Hülle\n  const lift = a.p * cfg.vol / R_GAS * M_AIR / a.T - n * M_H2;   // kg: verdrängte Luft minus Gas")
f.block("function newBalloon(cfg, tab){","const sandKg","""function newBalloon(cfg, tab){
  // Der Ballon steht schon eine Weile am Startplatz: Hülle und Gas haben die Temperatur, die sich in Sonne oder Nacht einstellt (STE-23).
  // Bei dieser Temperatur ist die Hülle prall gefüllt und der Trimmballast abgewogen.
  const a = atmAt(tab, 0), T = {h: 0, e: 0, n: 0, t: 0, gas: a.p * cfg.vol / (R_GAS * a.T), Tg: a.T, Tf: a.T, w: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon};
  const env = radEnv(T, tab); for (let i = 0; i < 360; i++) heatExchange(T, cfg, a, cfg.vol, 10, env);
  const Lo = loadout(cfg, tab, T.Tg);
  return {ok: Lo.ok, h: 0, w: 0, e: 0, n: 0, t: 0, dist: 0, maxH: 0, gas: Lo.n, gas0: Lo.n, Tg: T.Tg, Tf: T.Tf, wet: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon,
          sacks: Lo.sacks, mU: Lo.mU, marks: 0, rope: false, ropeOn: 0, gnd: 0, air: false, landed: false, vLand: 0, free: 0, full: true, lift: Lo.lift, trim: Lo.trim};
}
""")
f.save()
import re
s=open('/home/claude/w/ph.py').read()
if 'autopilot,' not in s: s=s.replace("names='sunSin,","names='autopilot,sunSin,"); open('/home/claude/w/ph.py','w').write(s)
