import sys; sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- Säckchen als Masse
f.rep("  ropeMu: 3.8      // Schleppwiderstand","  ropeMu: 3.8,     // Schleppwiderstand")
f.rep("Hängt in Wirklichkeit vom Gelände ab (OP-28)\n};","Hängt in Wirklichkeit vom Gelände ab (OP-28)\n  markKg: 0.07     // kg, ein Säckchen (Marker) für die Aufgabe Wandziel (Vorgabe Nutzer)\n};")
f.rep("sacks: Lo.sacks, mU: Lo.mU, rope: false,","sacks: Lo.sacks, mU: Lo.mU, marks: 0, rope: false,")
f.rep("  const load = fixedKg(cfg) + sandKg(B, cfg) - B.ropeOn;","  const load = fixedKg(cfg) + sandKg(B, cfg) + B.marks * cfg.markKg - B.ropeOn;")
# ---------- Zufälliges Wetter für die Simulation
f.rep("const DZ = 25, ZTOP = 10000;\n","""const DZ = 25, ZTOP = 10000;

/* Zufällige simulierte Atmosphäre (MET-06): Bei jedem Start kommt der Wind aus einer anderen Richtung und dreht mit der Höhe
   in unregelmäßigen Abständen und unregelmäßig stark. full: Die Drehung deckt bis 6000 m alle Windrichtungen ab (Aufgabe MID). */
function randomWx(rnd, full){
  rnd = rnd || Math.random;
  const R = (a, b) => a + rnd() * (b - a);
  const hs = [0]; while (hs[hs.length - 1] < 6000) hs.push(Math.min(6000, hs[hs.length - 1] + R(120, 350) + rnd() * rnd() * 1500));   // Schichtgrenzen
  const n = hs.length - 1, w = []; let sum = 0;
  for (let i = 0; i < n; i++){ const x = 0.15 + rnd() * rnd() * 2.5; w.push(x); sum += x; }                                          // Anteil der Drehung je Schicht
  const total = full ? R(360, 420) : R(50, 170), sign = rnd() < 0.75 ? 1 : -1;
  let dir = R(0, 360), spd = R(1.5, 3.5); const pts = [[0, dir, spd]];
  for (let i = 0; i < n; i++){ dir += sign * total * w[i] / sum; spd = Math.max(1.2, spd + (hs[i + 1] - hs[i]) * R(0.0008, 0.0035) + R(-0.8, 0.8)); pts.push([hs[i + 1], dir, spd]); }
  const wind = [];                                                                                                               // Stützstellen alle 100 m, damit die Drehung gleichmäßig durchlaufen wird
  for (let z = 0; z <= 6000; z += 100){
    let i = 0; while (i < n - 1 && hs[i + 1] < z) i++;
    const q = (z - hs[i]) / (hs[i + 1] - hs[i]);
    wind.push([z, ((pts[i][1] + (pts[i + 1][1] - pts[i][1]) * q) % 360 + 360) % 360, pts[i][2] + (pts[i + 1][2] - pts[i][2]) * q]);
  }
  const top = wind[wind.length - 1]; wind.push([10000, top[1], top[2] * 1.3]);
  const ib = R(250, 1100), it = ib + R(80, 220);                                                                                 // Inversion in zufälliger Höhe
  return {p0: R(100300, 102600), T0: R(6, 18), layers: [[ib, -R(0.006, 0.0095)], [it, R(0.006, 0.016)], [R(1800, 2600), -0.0060], [1e5, -0.0065]], wind};
}
""")
# ---------- Vergleichsfahrt merkt sich die Orte am Ende jedes Abschnitts
f.rep("  const B = newBalloon(cfg, tab), path = [[0, 0, 0]]; if (!B.ok) return {ok: false};","  const B = newBalloon(cfg, tab), path = [[0, 0, 0]], marks = []; if (!B.ok) return {ok: false};")
f.rep("    if (leg < legs.length && t >= tEnd){ leg++; if (leg < legs.length) tEnd += legs[leg].dur; }","    if (leg < legs.length && t >= tEnd){ marks.push([B.e, B.n, B.h]); leg++; if (leg < legs.length) tEnd += legs[leg].dur; }")
f.rep("sandLeft: sandKg(B, cfg), sand0, gasLeft: B.gas / B.gas0, path};","sandLeft: sandKg(B, cfg), sand0, gasLeft: B.gas / B.gas0, path, marks};")
# ---------- Ziel nach Entfernung
f.block("/* Ziel für die Aufgabe Ziellanden:","/* ---------- Zielort aus OpenStreetMap","""/* Ziel für die Aufgabe Zielfahren: Fahrten mit zufälligen Höhenplänen rechnen; der Landepunkt einer passenden Fahrt wird das Ziel.
   Entfernung des Ziels je Stufe (Vorgabe Nutzer): einfach 2 bis 3 km, mittel rund 5 km, schwer rund 10 km. Die Fahrzeit wird so
   lange angepasst, bis der Landepunkt in diesem Bereich liegt.
   level: 0 einfach (eine Höhe), 1 mittel (ein Wechsel der Höhe), 2 schwer (hohe Schicht mit anderer Windrichtung). */
const TARGET_KM = [[2000, 3000], [4000, 6000], [8000, 12000]];
function makeTarget(cfg, tab, level, rnd){
  rnd = rnd || Math.random;
  const pick = arr => arr[Math.floor(rnd() * arr.length)], span = (a, b) => a + rnd() * (b - a);
  const lowE = [150, 200, 300, 400], low = [200, 300, 400, 500, 600, 800], high = [1000, 1200, 1500, 1800];
  const dMin = TARGET_KM[level][0], dMax = TARGET_KM[level][1], dMid = (dMin + dMax) / 2;
  let best = null, lowShear = false, maxLo = 0, maxHi = 0;                 // größte Richtungsänderung, die das Profil hergibt
  for (const a of low) for (const b of low) maxLo = Math.max(maxLo, angDiff(windDirTo(tab, a), windDirTo(tab, b)));
  for (const a of low) for (const b of high) maxHi = Math.max(maxHi, angDiff(windDirTo(tab, a), windDirTo(tab, b)));
  const needMid = Math.min(25, maxLo * 0.7), needHi = Math.min(45, maxHi * 0.7);
  if ((level === 1 && maxLo < 15) || (level === 2 && maxHi < 25)) lowShear = true;
  for (let tries = 0; tries < 14; tries++){
    let hs, fr;                                                            // Höhen der Abschnitte und ihr Anteil an der Fahrzeit
    if (level === 0){ hs = [pick(lowE)]; fr = [1]; }
    else if (level === 1){
      let a, b, n = 0; do { a = pick(low); b = pick(low); } while ((a === b || angDiff(windDirTo(tab, a), windDirTo(tab, b)) < needMid) && ++n < 40);
      const q = span(0.35, 0.65); hs = [a, b]; fr = [q, 1 - q];
    } else {
      let a, b, n = 0; do { a = pick(low); b = pick(high); } while (angDiff(windDirTo(tab, a), windDirTo(tab, b)) < needHi && ++n < 40);
      const q1 = span(0.15, 0.25), q3 = span(0.2, 0.3); hs = [a, b, pick(low)]; fr = [q1, 1 - q1 - q3, q3];
    }
    let su = 0, sv = 0; hs.forEach((h, i) => { const a = atmAt(tab, h); su += fr[i] * a.u; sv += fr[i] * a.v; });
    const vbar = Math.max(0.6, Math.hypot(su, sv)), tLow = 50 * hs.length;   // mittlere Drift über die Abschnitte
    const run = T => { const legs = hs.map((h, i) => ({h, dur: Math.max(40, fr[i] * T)})); return Object.assign(planFlight(cfg, tab, legs), {legs}); };
    let T = Math.min(7200, Math.max(tLow, 0.7 * dMid / vbar)), r = run(T), d = r.ok ? Math.hypot(r.e, r.n) : 0;
    for (let it = 0; it < 3 && r.ok && (d < dMin || d > dMax); it++){      // Fahrzeit nachstellen, bis die Entfernung passt
      const T2 = Math.min(7200, Math.max(tLow, T + (dMid - d) / vbar)); if (Math.abs(T2 - T) < 5) break;
      T = T2; r = run(T); d = r.ok ? Math.hypot(r.e, r.n) : 0;
    }
    if (!r.ok || r.vLand > 1.5) continue;
    const okDist = d >= dMin && d <= dMax, okSand = r.sandLeft >= 0.12 * r.sand0;
    const cand = Object.assign(r, {dist: d, brg: (Math.atan2(r.e, r.n) * 180 / Math.PI + 360) % 360, level, lowShear});
    if (okDist && okSand) return cand;
    if (okSand && (!best || Math.abs(d - dMid) < Math.abs(best.dist - dMid))) best = cand;      // Notlösung: die Fahrt, deren Entfernung der Stufe am nächsten kommt
  }
  return best;
}

/* ---------- Aufgabe Wandziel (AUF-01 bis AUF-03) ----------
   Target Cross: Eine Fahrt in zwei oder drei niedrigen Höhen wird durchgerechnet; die Orte am Ende jedes Abschnitts werden die Kreuze.
   So sind sie mit dem Wind des Tages nacheinander erreichbar. Drei Kreuze gibt es, wenn die unteren Schichten genug Richtungsunterschied
   haben, sonst zwei. Abstand der Kreuze untereinander: 100 m bis 2 km (Vorgabe Nutzer). */
const WZ_R = 100;      // m, Wertungsradius um ein Target Cross (Vorschlag Claude, OP-31)
function makeCrosses(cfg, tab, rnd){
  rnd = rnd || Math.random;
  const pick = arr => arr[Math.floor(rnd() * arr.length)], span = (a, b) => a + rnd() * (b - a), hsAll = [100, 150, 200, 300, 400];
  let maxD = 0; for (const a of hsAll) for (const b of hsAll) maxD = Math.max(maxD, angDiff(windDirTo(tab, a), windDirTo(tab, b)));
  const n = maxD >= 12 ? 3 : 2; let best = null;
  for (let tries = 0; tries < 12; tries++){
    const legs = []; let prev = 0;
    for (let i = 0; i < n; i++){
      let h; do { h = pick(hsAll); } while (h === prev); prev = h;
      const a = atmAt(tab, h), v = Math.max(0.8, Math.hypot(a.u, a.v)), gap = i === 0 ? span(900, 1800) : span(150, 1700);
      legs.push({h, dur: Math.min(1500, Math.max(50, gap / v))});
    }
    const r = planFlight(cfg, tab, legs); if (!r.ok || r.marks.length < n) continue;
    const cr = r.marks.slice(0, n).map(m => ({e: m[0], n: m[1]})); let bad = 0;
    for (let i = 0; i < n; i++) for (let k = i + 1; k < n; k++){ const d = Math.hypot(cr[i].e - cr[k].e, cr[i].n - cr[k].n); if (d < 100) bad += 100 - d; if (k === i + 1 && d > 2000) bad += d - 2000; }
    const cand = {crosses: cr, path: r.path, legs, t: r.t, bad};
    if (!bad) return cand;
    if (!best || bad < best.bad) best = cand;
  }
  return best;
}
/* Fall eines Säckchens: Es fällt mit rund 9 m/s und treibt dabei mit dem Wind der Schichten, durch die es fällt (Annahme, OP-31). */
function markerFall(tab, e, n, h, gnd, vf){
  vf = vf || 9; let z = h;
  while (z > gnd){ const dz = Math.min(10, z - gnd), a = atmAt(tab, z - dz / 2), dt = dz / vf; e += a.u * dt; n += a.v * dt; z -= dz; }
  return [e, n, Math.max(0, h - gnd) / vf];
}
/* Wertung Wandziel (Vorschlag Claude, OP-31): je Kreuz zählt das nächstgelegene Säckchen, 100 Punkte auf dem Kreuz (bis 3 m),
   linear fallend auf 0 am Wertungsradius; die Punktzahl der Fahrt ist der Mittelwert über alle Kreuze. */
const scoreMarker = d => d <= 3 ? 100 : d >= WZ_R ? 0 : 100 * (WZ_R - d) / (WZ_R - 3);
function scoreCrosses(crosses, drops){
  const per = crosses.map(() => ({d: null, p: 0}));
  drops.forEach(q => { const x = per[q.cross]; if (x && (x.d == null || q.d < x.d)){ x.d = q.d; x.p = Math.round(scoreMarker(q.d)); } });
  return {per, pts: Math.round(per.reduce((s, x) => s + (x.d == null ? 0 : scoreMarker(x.d)), 0) / crosses.length)};
}

/* ---------- Aufgabe MDT, Max Distance (AUF-04, AUF-05) ----------
   Bestweite: Fahrten in jeweils einer Höhe über die ganze Zeit werden durchgerechnet, so dass die Landung in der Zeit liegt; die
   weiteste zählt. Das ist die beste Fahrt mit dem Wetter des Startzeitpunkts in gleichbleibender Höhe (Vorschlag Claude, OP-32). */
function bestDistance(cfg, tab, limit){
  let best = null;
  for (const h of [300, 600, 1000, 1500, 2000, 3000, 4000, 5000, 6000]){
    let dur = limit - h / 2 - 240, r = planFlight(cfg, tab, [{h, dur}]);
    if (r.ok && r.t > limit){ dur -= (r.t - limit) + 30; if (dur < 300) continue; r = planFlight(cfg, tab, [{h, dur}]); }
    if (!r.ok || r.t > limit + 60) continue;
    const d = Math.hypot(r.e, r.n); if (!best || d > best.dist) best = Object.assign(r, {dist: d, h});
  }
  return best;
}
/* Wertung MDT: 100 Punkte für die Bestweite, anteilig weniger; je volle Minute über der Zeit ein Punkt Abzug. */
function scoreMdt(d, best, t, limit){
  const base = best > 0 ? Math.round(100 * Math.min(1, d / best)) : 0, pen = t > limit ? Math.floor((t - limit) / 60) : 0;
  return {base, pen, pts: Math.max(0, base - pen)};
}
/* Wertung MID, Min Distance (AUF-06): 100 Punkte bei Landung bis 200 m vom Start; je weitere angefangene 200 m ein Punkt Abzug;
   je volle Minute, die früher oder später als nach der Sollzeit gelandet wird, ein Punkt Abzug. */
function scoreMid(d, t, limit){
  const penD = d <= 200 ? 0 : Math.ceil((d - 200) / 200), penT = Math.floor(Math.abs(t - limit) / 60);
  return {penD, penT, pts: Math.max(0, 100 - penD - penT)};
}
/* Rückmeldung zur Landung nach der Sinkgeschwindigkeit beim Aufsetzen, auf eine Nachkommastelle gerundet (PUN-08, Vorgabe Nutzer). */
const landClass = v => { const x = Math.round(v * 10) / 10; return x <= 0.5 ? 'ld_soft' : x <= 1.5 ? 'ld_sport' : x <= 2.8 ? 'ld_wild' : 'ld_crash'; };

""")
# ---------- Zielort: Suchradius an die Entfernung anpassen, kürzere Wartezeit
f.block("function osmQuery(lat, lon){","function osmClass(t){","""function osmQuery(lat, lon, rP){
  rP = rP || OSM.rPlace;
  const c = lat.toFixed(5) + ',' + lon.toFixed(5), a = '(around:' + Math.round(rP) + ',' + c + ')', b = '(around:' + Math.round(rP + OSM.clear.sens + 100) + ',' + c + ')', d = '(around:' + Math.round(rP + OSM.clear.aero + 100) + ',' + c + ')';
  return '[out:json][timeout:6];(' +
    'nwr["leisure"="pitch"]' + a + ';' +
    'nwr["aeroway"~"^(aerodrome|heliport)$"]' + d + ';' +
    'nwr["amenity"~"^(hospital|clinic|prison|school|kindergarten|police|fire_station)$"]' + b + ';' +
    'nwr["landuse"="military"]' + b + ';nwr["military"]' + b + ';' +
    'nwr["power"~"^(plant|substation)$"]' + b + ';nwr["railway"="station"]' + b + ';' +
    'nwr["natural"="water"]' + b + ';' +
    ');out tags center 400;';
}
""")
f.rep("const LAND_SOFT = 1.0, LAND_HARD = 3.0;   // m/s Sinken beim Aufsetzen","const LAND_SOFT = 1.0, LAND_HARD = 2.9;   // m/s Sinken beim Aufsetzen; ab LAND_HARD gilt die Landung als Bruchlandung (PUN-08)")
f.save(); print('ok')
