import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.block("  if (B.ropeOn > 0 || B.lag){","  B.gs = Math.hypot(u, v);",
"""  if (B.ropeOn > 0 || B.lag){
    // Das aufliegende Tau bremst mit ropeMu × Gewicht, entgegen der Fahrt über Grund. Die Luftkraft auf die Hülle zieht den Ballon zum Wind hin.
    // Aus beiden Kräften und der Masse folgt die Fahrt: Der Ballon bremst nicht schlagartig, und reicht der Wind nicht gegen die Reibung, steht er.
    let pu = B.gu || 0, pv = B.gv || 0; const ru = u - pu, rv = v - pv, rel = Math.hypot(ru, rv);
    pu += k * rel * ru / mEff * dt; pv += k * rel * rv / mEff * dt;                                   // Luftkraft
    const s = Math.hypot(pu, pv), s2 = Math.max(0, s - cfg.ropeMu * G0 * B.ropeOn / mEff * dt);     // Reibung des Taus
    if (s > 0){ pu *= s2 / s; pv *= s2 / s; }
    B.lag = B.ropeOn > 0 || Math.hypot(u - pu, v - pv) > 0.05;             // nach dem Abheben des Taus holt der Ballon den Wind wieder ein
    if (B.lag){ u = pu; v = pv; }
  }
""")
f.save()
