import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("  topoDecode(topo, 'countries').forEach(c => c.polys.forEach(rings => {\n    if (!rings.length || rings[0].length < 3) return;",
"""  topoDecode(topo, 'countries').forEach(c => c.polys.forEach(rings0 => {
    if (!rings0.length || rings0[0].length < 3) return;
    const rings = gbUnwrap(rings0);""")
f.rep("async function gbLoadZones(){","""/* Länder, die über den 180. Längengrad reichen (Russland): Die Grenzdatei springt dort von +180 auf −180. Ohne Korrektur entstünden
   Linien rund um die Erde (bei rund 65° und 70° Nord, also quer durch Finnland) samt Sperrstreifen. Die Längen werden deshalb
   fortlaufend gemacht (Russland reicht dann bis 191°) und der Ring so verschoben, dass seine Mitte zwischen −180 und 180 liegt. */
function gbUnwrap(rings){
  let shift = null;
  return rings.map(r => {
    const u = r.map(p => [p[0], p[1]]); let x0 = u[0][0], x1 = u[0][0];
    for (let i = 1; i < u.length; i++){ const d = u[i][0] - u[i - 1][0]; if (Math.abs(d) > 180) u[i][0] -= 360 * Math.round(d / 360); x0 = Math.min(x0, u[i][0]); x1 = Math.max(x1, u[i][0]); }
    if (shift == null) shift = -360 * Math.round((x0 + x1) / 2 / 360);                // der äußere Ring bestimmt die Verschiebung, Löcher folgen ihm
    if (shift) u.forEach(p => { p[0] += shift; });
    return u;
  });
}
async function gbLoadZones(){""")
f.rep("if (P.box[3] < 30 || P.box[1] > 75 || P.box[2] < -15 || P.box[0] > 65) return;","if (P.box[3] < 30 || P.box[1] > 83 || P.box[2] < -15 || P.box[0] > 70) return;")
f.rep("if (lat < 30 || lat > 75) continue;","if (lat < 30 || lat > 83) continue; if (seg[0][0] > 75 && seg[seg.length - 1][0] > 75) continue;")
f.rep("const BUILD = '2026-10-09.10'","const BUILD = '2026-10-09.11'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v32'" in s; open(p,'w').write(s.replace("'v32'","'v33'"))
