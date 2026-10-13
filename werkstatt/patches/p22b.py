import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.block("function newBalloon(cfg, tab){","const sandKg","""function newBalloon(cfg, tab){
  const Lo = loadout(cfg, tab), a = atmAt(tab, 0);
  const B = {ok: Lo.ok, h: 0, w: 0, e: 0, n: 0, t: 0, dist: 0, maxH: 0, gas: Lo.n, gas0: Lo.n, Tg: a.T, Tf: a.T, wet: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon,
          sacks: Lo.sacks, mU: Lo.mU, marks: 0, rope: false, ropeOn: 0, gnd: 0, air: false, landed: false, vLand: 0, free: 0, full: true, lift: Lo.lift, trim: Lo.trim};
  if (B.ok){                                               // Der Ballon steht schon eine Weile am Startplatz: Hülle und Gas haben die Temperatur, die sich in Sonne oder Nacht einstellt,
    const env = radEnv(B, tab);                            // und die Hülle ist bei dieser Temperatur prall gefüllt
    for (let i = 0; i < 360; i++) heatExchange(B, cfg, a, cfg.vol, 10, env);
    B.gas = B.gas0 = a.p * cfg.vol / (R_GAS * B.Tg);
  }
  return B;
}
""")
f.rep("    if (free < (cfg.holdKg || 0)){ B.held = true; B.Tg = B.Tf = a.T; B.w = 0; B.acc = 0; B.h = B.gnd; return; }","    if (free < (cfg.holdKg || 0)){ B.held = true; B.w = 0; B.acc = 0; B.h = B.gnd; return; }")
f.rep("    if (B.air){ B.landed = true; B.vLand = Math.max(0, -B.w); } else B.Tg = B.Tf = a.T;\n","    if (B.air){ B.landed = true; B.vLand = Math.max(0, -B.w); }\n")
f.save()
