// Routen für die Meisterschaft aus dem Wetterpaket rechnen (läuft nur in der Entwicklung, nicht in der App)
const fs = require('fs'), zlib = require('zlib'), C = require('./core.js');
eval(fs.readFileSync('vin.js', 'utf8'));
const raw = zlib.gunzipSync(fs.readFileSync('gb69-wetter.bin.gz')), hl = raw.readUInt32LE(6), head = JSON.parse(raw.slice(10, 10 + hl).toString());
const D = new Int16Array(raw.buffer.slice(raw.byteOffset + 10 + hl, raw.byteOffset + raw.length));
const LATS = head.lats, LONS = head.lons, NT = head.nT, REC = head.rec, NL = head.levels.length, PL = head.levels.map(x => x === 'sfc' ? null : x * 100);
const T0 = Date.UTC(2026, 7, 29, 0, 45, 0), PACK0 = head.t0, START = [51 + 33.460 / 60, 6 + 58.373 / 60];
const cfg = Object.assign({}, C.DEFAULT_CFG, {vol: 1000, rust: 200, envKg: 135, equip: 90, pax: 2, paxKg: 80});
const elevP = ip => D[ip * NT * REC];
function gridPos(lat, lon){ const fy = Math.max(0, Math.min(LATS.length - 1.001, (lat - LATS[0]) / (LATS[1] - LATS[0]))), fx = Math.max(0, Math.min(LONS.length - 1.001, (lon - LONS[0]) / (LONS[1] - LONS[0]))); return {iy: Math.floor(fy), ix: Math.floor(fx), wy: fy - Math.floor(fy), wx: fx - Math.floor(fx)}; }
function elevAt(lat, lon){ const g = gridPos(lat, lon), e = (a, b) => elevP((g.iy + a) * LONS.length + g.ix + b); return (e(0, 0) * (1 - g.wx) + e(0, 1) * g.wx) * (1 - g.wy) + (e(1, 0) * (1 - g.wx) + e(1, 1) * g.wx) * g.wy; }
function landSure(lat, lon){ if (lat >= 60.5 && lat <= 61.05 && lon >= 22.5 && lon <= 27.6) return true;   /* Südfinnland: das grobe Raster hält den Streifen 60 bis 61 Grad Nord für See */ const g = gridPos(lat, lon), e = (a, b) => elevP((g.iy + a) * LONS.length + g.ix + b); return Math.min(e(0, 0), e(0, 1), e(1, 0), e(1, 1)) > 10; }
const ZREF = Math.round(elevAt(START[0], START[1]));
const tabCache = new Map();
function tabPH(ip, k){                                       // Tabelle der Atmosphäre für einen Rasterpunkt und eine Stunde
  const key = ip * 100 + k; let t = tabCache.get(key); if (t) return t;
  const o = (ip * NT + k) * REC, pts = [];
  for (let li = 0; li < NL; li++){ const z = D[o + li * 5], T = D[o + li * 5 + 1], u = D[o + li * 5 + 2], v = D[o + li * 5 + 3], c = D[o + li * 5 + 4];
    if (z === -32768 || T === -32768 || u === -32768) continue; if (li > 0 && z <= D[o] + 40) continue;
    pts.push({z, T: T / 10 + 273.15, u: u / 10, v: v / 10, c: c === -32768 ? 0 : c / 100, pl: PL[li] || undefined}); }
  pts.sort((a, b) => a.z - b.z); pts[0].c = 0;
  let p0 = D[o + 65]; p0 = p0 === -32768 ? 101325 : (p0 / 10 + 1000) * 100;
  t = C.buildAtmFromHour({pts, p0, rain: Math.max(0, D[o + 66] === -32768 ? 0 : D[o + 66] / 10)}, D[o], ZREF); tabCache.set(key, t); if (tabCache.size > 6000) tabCache.clear(); return t;
}
function column(lat, lon, ms){                              // Atmosphäre am Ort und zur Zeit: vier Rasterpunkte, zwei Stunden
  const g = gridPos(lat, lon), th = Math.max(0, Math.min(NT - 1.001, (ms - PACK0) / 3600e3)), k = Math.floor(th), wt = th - k;
  const parts = []; for (const [a, b, w] of [[0, 0, (1 - g.wy) * (1 - g.wx)], [0, 1, (1 - g.wy) * g.wx], [1, 0, g.wy * (1 - g.wx)], [1, 1, g.wy * g.wx]]){ const ip = (g.iy + a) * LONS.length + g.ix + b; parts.push([tabPH(ip, k), w * (1 - wt)], [tabPH(ip, k + 1), w * wt]); }
  const n = parts[0][0].length, tab = new Array(n); let rain = 0;
  for (let i = 0; i < n; i++){ let T = 0, p = 0, u = 0, v = 0, c = 0; for (const [t, w] of parts){ const r = t[i]; T += r.T * w; p += r.p * w; u += r.u * w; v += r.v * w; c += (r.c || 0) * w; } tab[i] = {T, p, u, v, c}; }
  for (const [t, w] of parts) rain += (t.rain || 0) * w; tab.rain = rain; tab.t0 = T0; tab.lat = lat; tab.lon = lon; return tab;
}
// Gesperrte Gebiete, grob von Hand (nur für die Planung; die App prüft mit den echten Grenzen). Breite, Länge.
const KALI = [[54.36, 19.60], [54.46, 19.80], [54.95, 19.95], [55.30, 20.95], [55.20, 21.30], [55.08, 22.60], [54.80, 22.88], [54.363, 22.792], [54.33, 21.5], [54.36, 19.60]];
const EAST = [[45.4, 28.2], [47.0, 27.9], [48.25, 26.6], [47.95, 24.9], [47.95, 22.9], [48.4, 22.15], [49.0, 22.55], [49.5, 22.7], [50.4, 23.7], [50.85, 24.1], [51.5, 23.6], [52.1, 23.65], [52.2, 23.2], [52.6, 23.9], [53.2, 23.9], [53.956, 23.515],
  [54.0, 24.0], [54.15, 25.5], [54.3, 25.8], [54.55, 25.75], [55.0, 26.2], [55.15, 26.6], [55.68, 26.63], [55.85, 27.6], [56.17, 28.15], [56.8, 27.9], [57.3, 27.85], [57.52, 27.35], [57.85, 27.8], [58.0, 27.6], [59.0, 27.7], [59.47, 28.05], [60.0, 27.3], [60.55, 27.8], [61.1, 28.8], [62.0, 30.1], [62.9, 31.6], [63.6, 30.4], [65, 29.8], [65, 60], [45.4, 60], [45.4, 28.2]];
function inPoly(P, lat, lon){ let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++){ const a = P[i], b = P[j]; if ((a[0] > lat) !== (b[0] > lat) && lon < (b[1] - a[1]) * (lat - a[0]) / (b[0] - a[0]) + a[1]) c = !c; } return c; }
function polyDist(P, lat, lon){ const kx = 111320 * Math.cos(lat * Math.PI / 180), ky = 111320; let best = 1e12; for (let i = 0, j = P.length - 1; i < P.length; j = i++){ const ax = (P[j][1] - lon) * kx, ay = (P[j][0] - lat) * ky, bx = (P[i][1] - lon) * kx, by = (P[i][0] - lat) * ky, ux = bx - ax, uy = by - ay, L2 = ux * ux + uy * uy, t = L2 ? Math.max(0, Math.min(1, -(ax * ux + ay * uy) / L2)) : 0; best = Math.min(best, Math.hypot(ax + t * ux, ay + t * uy)); } return best; }
const banDist = (lat, lon) => (inPoly(KALI, lat, lon) || inPoly(EAST, lat, lon)) ? 0 : Math.min(polyDist(KALI, lat, lon), polyDist(EAST, lat, lon));
const inPack = (lat, lon) => lat > LATS[0] + 0.3 && lat < LATS[LATS.length - 1] - 0.3 && lon > LONS[0] + 0.3 && lon < LONS[LONS.length - 1] - 0.3;

// Zustand einer Fahrt
function start(){ const tab = column(START[0], START[1], T0), B = C.newBalloon(cfg, tab); return {B, lat: START[0], lon: START[1], tab, tabAt: 0, minBan: 1e9, sea: 0, log: [], ok: true, why: ''}; }
const clone = S => ({B: JSON.parse(JSON.stringify(S.B)), lat: S.lat, lon: S.lon, tab: S.tab, tabAt: S.tabAt, minBan: S.minBan, sea: S.sea, log: S.log.slice(), ok: S.ok, why: S.why, ctl: S.ctl, plan: (S.plan || []).slice()});
function anchor(S){ const B = S.B; S.lat += B.n / 111320; S.lon += B.e / (111320 * Math.cos(S.lat * Math.PI / 180)); B.e = 0; B.n = 0; B.lat0 = S.lat; B.lon0 = S.lon; }
// Steuerung: Höhe in einem Band halten, sparsam mit Sand und Gas; große Höhenwechsel und die Landung über die Selbststeuerung des Kerns
function control(S, target){                                // target: Zahl (Band ±200 m) oder [unten, oben]; 0 = landen
  const B = S.B, agl = B.h - B.gnd;
  if (target === 0){ C.autopilot(B, cfg, S.tab, 0); return; }
  const lo = Array.isArray(target) ? target[0] : target - 200, hi = Array.isArray(target) ? target[1] : target + 200;
  if (!B.air){ C.autopilot(B, cfg, S.tab, Math.max(lo, 300)); return; }
  if (agl < Math.min(150, Math.max(30, lo * 0.5)) && B.w < -0.3){ C.dropKg(B, cfg, Math.min(10, 2 - B.w * 6)); S.ctl = B.t; return; }   // dem Boden zu nah
  if (B.t - (S.ctl || 0) < 40) return;                                                            // Wirkung abwarten
  const K = 3.4, sq = x => x * Math.abs(x);
  if (B.h < lo){ const ws = Math.max(0.15, Math.min(1.5, (lo - B.h) / 400)), need = K * (sq(ws) - sq(B.w)); if (need > 0.25){ C.dropKg(B, cfg, Math.min(6, need)); S.ctl = B.t; } }
  else if (B.h > hi){ const ws = -Math.max(0.15, Math.min(1.5, (B.h - hi) / 400)), need = K * (sq(B.w) - sq(ws)); if (need > 0.25){ const a = C.atmAt(S.tab, B.h); B.gas = Math.max(0, B.gas - Math.min(6, need) / (C.M_AIR * B.Tg / a.T - C.M_H2)); S.ctl = B.t; } }
  else if (B.w < -0.8 && B.h - lo < 400){ C.dropKg(B, cfg, Math.min(6, K * (sq(B.w + 0.3) * -1))); S.ctl = B.t; }
  else if (B.w > 0.8 && hi - B.h < 400){ const a = C.atmAt(S.tab, B.h); B.gas = Math.max(0, B.gas - Math.min(6, K * sq(B.w - 0.3)) / (C.M_AIR * B.Tg / a.T - C.M_H2)); S.ctl = B.t; }
}
function advance(S, target, dur, lim){                      // dur Sekunden mit Zielhöhe fahren (target 0 = landen); lim: Grenzen der Route
  const B = S.B;
  for (let t = 0; t < dur && !B.landed; t++){
    if (B.t - S.tabAt >= 600 || S.tabAt === 0 && t === 0 || Math.hypot(B.e, B.n) > 12000){ anchor(S); S.tab = column(S.lat, S.lon, T0 + B.t * 1000); S.tabAt = B.t || 1; B.gnd = Math.max(0, elevAt(S.lat, S.lon) - ZREF);
      const d = banDist(S.lat, S.lon); S.minBan = Math.min(S.minBan, d); const land = landSure(S.lat, S.lon); if (!land) S.sea++;
      if (d < lim.ban){ S.ok = false; S.why = 'Sperrzone'; return S; } if (!inPack(S.lat, S.lon)){ S.ok = false; S.why = 'Rand'; return S; } if (lim.noSea && !land && B.air){ S.ok = false; S.why = 'See'; return S; }
      if (lim.hMax && B.h > lim.hMax + 600){ S.ok = false; S.why = 'Höhe'; return S; } }
    if (B.t % 10 < 1) control(S, target);
    C.stepBalloon(B, cfg, S.tab, 1, 0);
    if (B.t % 600 < 1 && B.go){ const la = S.lat + B.n / 111320, lo = S.lon + B.e / (111320 * Math.cos(S.lat * Math.PI / 180)); S.log.push([Math.round(B.t), +la.toFixed(4), +lo.toFixed(4), Math.round(B.h + ZREF), Math.round(Math.max(0, elevAt(la, lo))), Math.round(C.sandKg(B, cfg)), +(100 * B.gas / B.gas0).toFixed(1), +(B.w).toFixed(1)]); }
    if (T0 + B.t * 1000 > PACK0 + (NT - 1.5) * 3600e3){ S.ok = false; S.why = 'Zeit'; return S; }
  }
  anchor(S); return S;
}
function landFrom(S, lim){ const L = clone(S); advance(L, 0, 4 * 3600, {ban: lim.ban, noSea: lim.noSea}); if (!L.B.landed || !L.ok) return null;
  const d = banDist(L.lat, L.lon); if (d < lim.ban || !landSure(L.lat, L.lon) || L.B.vLand > 2.5) return null;
  if (lim.day && C.sunSin(L.lat, L.lon, T0 + L.B.t * 1000) < 0.09) return null;
  const B = L.B; L.log.push([Math.round(B.t), +L.lat.toFixed(4), +L.lon.toFixed(4), Math.round(Math.max(0, elevAt(L.lat, L.lon))), Math.round(Math.max(0, elevAt(L.lat, L.lon))), Math.round(C.sandKg(B, cfg)), +(100 * B.gas / B.gas0).toFixed(1), 0]);
  L.km = geoDist(START[0], START[1], L.lat, L.lon) / 1000; return L; }
function lineDist(P, lat, lon){ const kx = 111320 * Math.cos(lat * Math.PI / 180), ky = 111320; let best = 1e12; for (let i = 1; i < P.length; i++){ const ax = (P[i-1][1] - lon) * kx, ay = (P[i-1][0] - lat) * ky, bx = (P[i][1] - lon) * kx, by = (P[i][0] - lat) * ky, ux = bx - ax, uy = by - ay, L2 = ux * ux + uy * uy, t = L2 ? Math.max(0, Math.min(1, -(ax * ux + ay * uy) / L2)) : 0; best = Math.min(best, Math.hypot(ax + t * ux, ay + t * uy)); } return best; }
function search(name, lim, ALTS, BLOCK, BEAM){
  let beam = [Object.assign(start(), {plan: []})], best = null; const t00 = Date.now();
  for (let lev = 0; lev < (lim.maxLev || 30) && beam.length; lev++){
    const next = [], dead = {};
    for (const S of beam) for (const h of ALTS){
      if (S.plan.length && Math.abs(h[0] - S.plan[S.plan.length - 1][0]) > lim.jump) continue;
      const N = clone(S); N.plan.push(h); advance(N, h, BLOCK, lim);
      if (!N.ok || N.B.landed){ const w = N.ok ? 'gelandet' : N.why; dead[w] = (dead[w] || 0) + 1; continue; } if (lim.tMax && N.B.t > lim.tMax) continue; const sand = C.sandKg(N.B, cfg); if (sand < lim.sandMin) continue;
      N.km = geoDist(START[0], START[1], N.lat, N.lon) / 1000; N.score = (lim.track ? -(lim.trackW || 3) * lineDist(lim.track, N.lat, N.lon) / 1000 : 0) + (lim.goal ? -geoDist(lim.goal[0], lim.goal[1], N.lat, N.lon) / 1000 : 0) + (lim.latW || 0) * (N.lat - 51.5) + N.km + lim.sandW * sand + (lim.roomW || 0) * Math.min(lim.roomKm || 300, banDist(N.lat, N.lon) / 1000); next.push(N);
    }
    next.sort((a, b) => b.score - a.score);
    const keep = [], seen = new Map(); for (const N of next){ const key = Math.round(N.lat * (lim.cell || 2)) + ',' + Math.round(N.lon * (lim.cell || 2) / 2) + (lim.perCell ? '' : ',' + N.plan[N.plan.length - 1][0]); const cnt = seen.get(key) || 0; if (cnt >= (lim.perCell || 1)) continue; seen.set(key, cnt + 1); keep.push(N); if (keep.length >= BEAM) break; }
    beam = keep;
    for (const N of beam.slice(0, lim.landTry)){ const L = landFrom(N, lim); if (L && (!best || L.km > best.km)) best = L; }
    console.log(name, 'Abschnitt', lev + 1, 't', ((lev + 1) * BLOCK / 3600).toFixed(0) + ' h', '| Kandidaten', next.length, '| vorn', beam[0] ? beam[0].km.toFixed(0) + ' km, Sand ' + C.sandKg(beam[0].B, cfg).toFixed(0) + ', ' + beam[0].lat.toFixed(1) + '/' + beam[0].lon.toFixed(1) + ', Höhe ' + beam[0].plan[lev][0] : '-', '| aus', JSON.stringify(dead), '| beste Landung', best ? best.km.toFixed(0) + ' km' : '-', '|', ((Date.now() - t00) / 1000).toFixed(0) + ' s');
  }
  return best;
}
module.exports = {search, start, advance, landFrom, clone, cfg, C, ZREF, START, T0, banDist, landSure, elevAt, column, geoDist};
if (require.main === module){
  const S = start(); console.log('Start: Höhe Startplatz', ZREF, 'm | Sand', C.sandKg(S.B, cfg).toFixed(0), 'kg | Crew lässt los bei', S.B.holdKg, 'kg | Gas−Luft', (S.B.Tg - C.atmAt(S.tab, 0).T).toFixed(1), 'K');
  const a = C.atmAt(S.tab, 0), b = C.atmAt(S.tab, 1000), c = C.atmAt(S.tab, 3000); const dir = q => ((Math.atan2(-q.u, -q.v) * 180 / Math.PI + 360) % 360).toFixed(0) + '°/' + Math.hypot(q.u, q.v).toFixed(0) + ' m/s';
  console.log('Wind am Start: Boden', dir(a), (a.T - 273.15).toFixed(1) + ' °C | 1000 m', dir(b), (b.T - 273.15).toFixed(1) + ' °C | 3000 m', dir(c));
  console.log('Probe: 6 h in 1500 m'); const t0 = Date.now(); advance(S, 1500, 6 * 3600, {ban: 20000}); console.log(' Position', S.lat.toFixed(2), S.lon.toFixed(2), '| km', (geoDist(START[0], START[1], S.lat, S.lon) / 1000).toFixed(0), '| Höhe', S.B.h.toFixed(0), '| Sand', C.sandKg(S.B, cfg).toFixed(0), '| Gas', (100 * S.B.gas / S.B.gas0).toFixed(1), '% | ok', S.ok, S.why, '| Rechenzeit', Date.now() - t0, 'ms');
}
