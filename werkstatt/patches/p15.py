import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F(); old=open('/home/claude/w/index_087.html',encoding='utf-8').read()

# ---------- 1. Zielfahren: Landezone 100 m ----------
f.block("/* Punkte (PUN-01, PUN-02):","const LAND_SOFT",
"""/* Punkte (PUN-01, PUN-02): Die Landezone ist ein Kreis mit 100 m Radius um das Ziel (Vorgabe Nutzer); wer darin landet, bekommt 100 Punkte.
   Außerhalb fallen die Punkte linear auf 0 am Punkteradius. Der Punkteradius ist 20 % der Entfernung vom Start zum Ziel, mindestens 300 m.
   Harte Landung kostet bis zur Hälfte (vorläufig, OP-05). */
const ZONE_R = 100;                       // m, Radius der Landezone beim Zielfahren
""")
f.rep("const scoreRadius = targetDist => Math.max(200, 0.2 * targetDist);","const scoreRadius = targetDist => Math.max(3 * ZONE_R, 0.2 * targetDist);")
f.rep("base = distM <= 20 ? 100 : distM >= R ? 0 : 100 * (R - distM) / (R - 20);","base = distM <= ZONE_R ? 100 : distM >= R ? 0 : 100 * (R - distM) / (R - ZONE_R);")
f.rep("const tgtCore = L.circle([START.lat, START.lon], {radius: 150,","const tgtCore = L.circle([START.lat, START.lon], {radius: ZONE_R,")
add=[" Die Landezone ist ein Kreis mit 100 m Radius: Wer darin landet, bekommt 100 Punkte."," The landing zone is a circle of 100 m radius: land inside it for 100 points."," La zone d’atterrissage est un cercle de 100 m de rayon : y atterrir vaut 100 points."," Strefa lądowania to koło o promieniu 100 m: lądowanie w nim daje 100 punktów."," Přistávací zóna je kruh o poloměru 100 m: přistání v něm dává 100 bodů.","降落區是半徑 100 公尺的圓，降落在圓內可得 100 分。"," La zona de aterrizaje es un círculo de 100 m de radio: aterrizar dentro vale 100 puntos."]
it=iter(add); n=[0]
def r(m): n[0]+=1; return m.group(1)+next(it)+"'"
f.s=re.sub(r"(task_target_d:'[^']*)'",r,f.s); assert n[0]==7,n

# ---------- 2. Schlepptau ----------
f.block("  ropeMu: 3.8,","  markKg:",
"""  ropeMu: 3.8,     // Reibungsbeiwert des Schlepptaus am Boden (Annahme, OP-28): Bremskraft = ropeMu × Gewicht des aufliegenden Taus.
                   // Reine Gleitreibung von Kokosfaser auf Gras läge bei etwa 0,6 bis 1. Das rund 10 cm dicke, sehr raue Tau pflügt aber durch
                   // den Bewuchs der Felder und bremst um ein Mehrfaches. Abgestimmt auf die Vorgabe: Liegen 40 m auf, steht der Ballon bei 4 m/s Wind fast.
""")
f.block("  if (B.ropeOn > 0){   ","  B.gs = Math.hypot(u, v);",
"""  if (B.ropeOn > 0 || B.lag){
    // Das aufliegende Tau bremst mit ropeMu × Gewicht. Im Gleichgewicht ist das die Luftkraft auf die Hülle: so viel bleibt der Ballon hinter dem
    // Wind zurück. Reicht der Wind nicht gegen die Reibung, steht er. Wegen seiner Masse bremst und beschleunigt der Ballon nicht schlagartig.
    const ws = Math.hypot(u, v), lag = Math.sqrt(cfg.ropeMu * G0 * B.ropeOn / k), f = ws > 0 ? Math.max(0, 1 - lag / ws) : 0;
    const pu = B.gu || 0, pv = B.gv || 0, rel = Math.hypot(u - pu, v - pv);
    const q = 1 - Math.exp(-dt * 2 * k * Math.max(0.5, rel) / mEff);
    const nu = pu + (u * f - pu) * q, nv = pv + (v * f - pv) * q;
    B.lag = B.ropeOn > 0 || Math.hypot(u - nu, v - nv) > 0.05;             // nach dem Abheben des Taus holt der Ballon den Wind wieder ein
    if (B.lag){ u = nu; v = nv; }
  }
""")
assert "if (B.ropeOn > 0){ " not in f.s
f.rep("sp = B.ropeOn > 0 ? (B.gs || 0) : Math.hypot(a.u, a.v);","sp = (B.ropeOn > 0 || B.lag) ? (B.gs || 0) : Math.hypot(a.u, a.v);")
f.rep("$('i-track').textContent = moving ? deg3(dirTo(a.u, a.v))","$('i-track').textContent = moving ? deg3(sp > 0.05 && B.lag ? dirTo(B.gu, B.gv) : dirTo(a.u, a.v))")
# Anzeige am Tauknopf: aufliegende Länge und Entlastung
f.rep("(B.ropeOn > 0.05 ? '−' + nf(B.ropeOn, 1) + ' kg' : nf(CFG.ropeLen) + ' m')","(B.ropeOn > 0.05 ? nf(B.ropeOn / CFG.ropeKgM) + ' m · −' + nf(B.ropeOn, 1) + ' kg' : nf(CFG.ropeLen) + ' m')")

# ---------- 3. Startbild der 80er im Rahmen der App ----------
a=old.index("/* ---------- Hauptmenü: bewegtes Bild im Stil der Heimcomputer"); b=old.index("/* ---------- Zeitschleife")
f.block("/* ---------- Hauptmenü: ruhig bewegtes Bild","/* ---------- Zeitschleife",old[a:b])
f.rep("MENUBG.","RETRO.",2)
f.block("    <!-- Hauptmenü im Stil der App","      <div class=\"mcard\">",
"""    <!-- Hauptmenü: Rahmen im Stil der App, darin das Startbild im Stil der Heimcomputer der 80er -->
    <div class="full" id="menu">
      <div class="mframe">
      <div class="mbar"><i></i><b data-i="brand">Gasballon</b><span id="m-ver"></span></div>
      <div class="mscreen">
      <canvas id="c64" aria-hidden="true"></canvas>
""")
f.rep("""<b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>
      </div>
    </div>""","""<b data-i="m_champ"></b><span data-i="m_champ_d"></span></button>
      </div>
      </div>
      </div>
    </div>""")
f.rep('        <h1 data-i="brand">Gasballon</h1>\n        <label class="mname">','        <label class="mname">')
f.line("#menu{","#menu{z-index:850;padding:max(8px,env(safe-area-inset-top)) 8px max(8px,env(safe-area-inset-bottom));background:var(--bg)}")
f.line("#menubg{",""".mframe{width:min(100%,600px);height:min(100%,860px);display:flex;flex-direction:column;border:1px solid var(--line);border-radius:14px;background:var(--pan);box-shadow:0 18px 40px rgba(0,0,0,.45);overflow:hidden}
.mbar{flex:none;display:flex;align-items:center;gap:8px;padding:7px 12px;border-bottom:1px solid var(--line);font-family:var(--num);font-size:18px;font-weight:600;letter-spacing:.02em}
.mbar i{flex:none;width:10px;height:10px;border-radius:50%;background:var(--orb)}
.mbar span{margin-left:auto;font-size:12px;font-weight:500;color:var(--mut)}
.mscreen{position:relative;flex:1;min-height:0;margin:8px;display:grid;place-items:center;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#352879}
#c64{position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges}""")
f.line(".mcard{",".mcard{position:relative;width:min(340px,calc(100% - 20px));max-height:calc(100% - 12px);overflow:auto;padding:10px 12px 12px;background:rgba(10,16,25,.9);border:3px solid #6C5EB5;border-radius:4px}")
f.line(".mcard h1{","")
f.line("/* Das Menü erscheint nach einer Sekunde und wird","/* Das Menü erscheint nach einer Sekunde und baut sich ruckelnd auf, wie auf einem alten Heimcomputer */")
f.line(".mcard.boot{",".mcard.boot{animation:c64in 1.5s steps(1,end) 1s both}")
f.line("@keyframes menuin","@keyframes c64in{0%{opacity:0;visibility:hidden}12%{opacity:.18;visibility:visible}27%{opacity:.4}36%{opacity:.32}52%{opacity:.6}60%{opacity:.52}78%{opacity:.82}86%{opacity:.74}100%{opacity:1;visibility:visible}}")
f.line(".mname{",'.mname{display:flex;align-items:center;gap:8px;font-family:"Courier New",Courier,monospace;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#B8C76F}')
f.line(".mname input{",'.mname input{flex:1;min-width:0;min-height:38px;padding:0 9px;border-radius:4px;border:2px solid #6C5EB5;background:#0d1626;font-family:"Courier New",Courier,monospace;font-size:16px;color:#eef3fa}')
f.line(".mbtn:not(:disabled):active{",""".mbtn:not(:disabled):active{background:#22355a}
.mscreen .mbtn{margin-top:6px;padding:6px 11px;border-radius:4px;border:2px solid #6C5EB5;background:#17253b}
.mscreen .mbtn em{color:#B8C76F;border-color:#B8C76F}""")
f.rep("$('ver').textContent = BUILD;","$('ver').textContent = BUILD; $('m-ver').textContent = BUILD;")
f.rep("const BUILD = '2026-10-08.8';","const BUILD = '2026-10-08.9';")
f.save()
