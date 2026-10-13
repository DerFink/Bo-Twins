import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.block("$('mk-drop').addEventListener('click', () => {","/* ---------- Hauptmenü und Vorbereitung ---------- */",
"""/* Säckchen (AUF-03): Es fällt in der Spielzeit mit MK_VF und treibt in jeder Höhe mit dem dortigen Wind, so wie der Ballon in seiner Höhe.
   Bis zum Aufschlag ist es als kleiner Punkt auf der Karte zu sehen; erst dann stehen Landepunkt und Abstand fest. */
const MK_VF = 9;                                           // m/s Fallgeschwindigkeit
let FLY = [];
function markerLand(m){
  if (m.mk){ map.removeLayer(m.mk); m.mk = null; }
  let bi = 0, bd = 1e9; WZ.crosses.forEach((c, i) => { const d = Math.hypot(c.e - m.e, c.n - m.n); if (d < bd){ bd = d; bi = i; } });      // gewertet wird am nächstgelegenen Kreuz
  WZ.drops.push({e: m.e, n: m.n, cross: bi, d: bd});
  goalLayers.push(L.circleMarker(ll(m.e, m.n), {radius: 6, color: '#0a1019', weight: 2, fillColor: m.col, fillOpacity: 1, interactive: false}).addTo(map));
  return [bd, bi];
}
function stepMarkers(dt, all){                             // all: Fahrt ist zu Ende, alle Säckchen fallen zu Ende
  if (!FLY.length || !WZ) return;
  for (const m of FLY){
    let t = all ? 1e9 : dt;
    while (t > 1e-6){
      const d = Math.min(0.25, t), a = atmAt(ATM, m.z), g = TER.on ? terAt(m.e, m.n) : 0;
      if (m.z <= g){ m.done = true; break; }
      const s = Math.min(d, (m.z - g) / MK_VF); m.e += a.u * s; m.n += a.v * s; m.z -= MK_VF * s; t -= d;
    }
    if (m.done){ const r = markerLand(m); if (!all){ SND.marker(); toast(tr('mk_toast', {d: fmtD(r[0]), n: r[1] + 1})); } }
    else if (m.mk) m.mk.setLatLng(ll(m.e, m.n));
  }
  FLY = FLY.filter(m => !m.done);
}
$('mk-drop').addEventListener('click', () => {
  if (STATE !== 'play' || PAUSED || !WZ || !(B.marks > 0) || B.landed || !B.air) return;
  const col = WZ_COL[(WZ.drops.length + FLY.length) % 3]; B.marks--;
  const mk = L.circleMarker(ll(B.e, B.n), {radius: 4, color: '#eef3fa', weight: 1.5, fillColor: col, fillOpacity: 1, interactive: false}).addTo(map); goalLayers.push(mk);
  FLY.push({e: B.e, n: B.n, z: B.h, col, mk}); SND.marker();
});

""")
f.rep("  TARGET = null; WZ = null; MDT = null;","  TARGET = null; WZ = null; MDT = null; FLY = [];")
f.rep("let simDt = real * (valve > 0 ? 1 : UI.speed);                    // solange das Ventil gezogen ist, läuft die Zeit 1×","let simDt = real * (valve > 0 ? 1 : UI.speed);                    // solange das Ventil gezogen ist, läuft die Zeit 1×\n    const adv = simDt;")
f.rep("    if (Math.hypot(B.e - lastPathE, B.n - lastPathN) > 25){","    stepMarkers(adv);\n    if (Math.hypot(B.e - lastPathE, B.n - lastPathN) > 25){")
f.rep("    const r = scoreCrosses(WZ.crosses, WZ.drops); pts = r.pts;","    stepMarkers(0, true);                                             // Säckchen, die noch fallen, zählen mit\n    const r = scoreCrosses(WZ.crosses, WZ.drops); pts = r.pts;")
f.rep("const BUILD = '2026-10-08.13';","const BUILD = '2026-10-08.14';")
f.save()
