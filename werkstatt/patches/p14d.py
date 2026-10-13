import sys; sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("const BUILD = '2026-10-08.7';","const BUILD = '2026-10-08.8';")
f.rep('2.500-9-7c0-4 2-8.500 6.500-11z" fill="#ff7ad9" stroke="#0a1019" stroke-width="1.500"/><path d="M6.500 8h9"','2.5-9-7c0-4 2-8.5 6.5-11z" fill="#ff7ad9" stroke="#0a1019" stroke-width="1.5"/><path d="M6.5 8h9"')
f.rep("mode: 'free', wx: 'real', level: 0}","mode: 'free', task: 'target', wx: 'real', level: 0}")

# ================= Musik: deutlich hörbar einsetzen, dann leiser werden =================
f.rep("mNote('square', hz(n), t, S * 1.8, 0.075);","mNote('square', hz(n), t, S * 1.8, 0.13);")
f.rep("      mNote('triangle', hz(SONG.bass[bar] + (st % 4 === 0 ? 0 : 12)), t, S * 1.7, 0.22);","      mNote('triangle', hz(SONG.bass[bar] + (st % 4 === 0 ? 0 : 12)), t, S * 1.7, 0.22);\n      mNote('square', hz(SONG.bass[bar] + 24), t, S * 1.2, 0.03);                                // Bass eine Lage höher mitspielen: Handy-Lautsprecher geben tiefe Töne kaum wieder")
f.rep("a = mNote('square', hz(ch[0] + 12), t, S, 0.028);","a = mNote('square', hz(ch[0] + 12), t, S, 0.05);")
f.rep("      if (mus){ clearInterval(mus.timer); const g = mus.g; g.gain.setTargetAtTime(0, ctx.currentTime, 0.08);","      if (mus){ clearInterval(mus.timer); const g = mus.g; g.gain.cancelScheduledValues(ctx.currentTime); g.gain.setTargetAtTime(0, ctx.currentTime, 0.08);")
f.rep("    mus.g.gain.value = 0.42; mus.g.connect(master);            // leiser als die Geräusche der Fahrt","    mus.g.gain.value = 1; mus.g.connect(master);")
f.rep("      while (mus.next < ctx.currentTime + 0.3){ mStep(mus.i++, mus.next); mus.next += mus.S; }",
      "      if (mus.i === 0){ const g = mus.g.gain, t0 = mus.next; g.setValueAtTime(1, t0); g.setValueAtTime(1, t0 + 8); g.linearRampToValueAtTime(0.45, t0 + 14); }   // setzt deutlich hörbar ein und wird nach einigen Takten leiser\n      while (mus.next < ctx.currentTime + 0.3){ mStep(mus.i++, mus.next); mus.next += mus.S; }")
f.rep("""    rope(){   // Tau läuft aus oder wird eingeholt""","""    marker(){ // Säckchen fliegt über den Korbrand
      tone({f0: 620, f1: 240, dur: 0.22, peak: 0.16});
      noise({type: 'bandpass', f0: 2600, f1: 1200, q: 1, dur: 0.20, peak: 0.07, attack: 0.02});
    },
    rope(){   // Tau läuft aus oder wird eingeholt""")

# ================= Zustand =================
f.rep("let START = (() => { const s = store.get('gb-start', null); return s && isFinite(s.lat) && isFinite(s.lon) ? s : BITTERFELD; })();",
      "let START = (() => { const s = store.get('gb-start', null); return s && isFinite(s.lat) && isFinite(s.lon) ? s : BITTERFELD; })();\nlet USER_START = START;                                   // vom Spieler gewählter Startplatz; Wandziel, MDT und MID starten fest in Bitterfeld")
f.rep("const SIM_ATM = buildAtm(SIM_WX);","let SIM_ATM = buildAtm(SIM_WX);                           // simulierte Atmosphäre; wird vor jeder Fahrt mit Simulation neu ausgewürfelt (MET-06)")
f.rep("let B = newBalloon(CFG, ATM), TARGET = null;","""let B = newBalloon(CFG, ATM), TARGET = null;
let WZ = null, MDT = null;                                // Aufgabe Wandziel: {crosses, drops}; Aufgabe MDT: {best}
const TASK = () => UI.mode === 'challenge' ? (UI.task || 'target') : 'free';     // free, target, wz, mdt, mid
const FIXED = k => k === 'wz' || k === 'mdt' || k === 'mid';                       // Aufgaben mit festem Startplatz Bitterfeld
const LIMITS = {mdt: 3 * 3600, mid: 3600};                                          // Sollzeit in s
const WZ_COL = ['#ff7ad9', '#4cc9ff', '#ffe14d'];""")
f.rep("const musicWanted = () => !!UI.music && ['menu', 'setup', 'pick', 'busy', 'brief', 'scores'].includes(STATE) && document.visibilityState !== 'hidden' && performance.now() - menuAt > 2500;",
      "const musicWanted = () => !!UI.music && ['menu', 'chal', 'setup', 'pick', 'busy', 'brief', 'scores'].includes(STATE) && document.visibilityState !== 'hidden' && performance.now() - menuAt > 1700;")
f.rep("$('menu').hidden = s !== 'menu' && s !== 'scores';","$('menu').hidden = s !== 'menu' && s !== 'scores' && s !== 'chal'; $('chal').hidden = s !== 'chal';")

# ================= Karte: Ziele aller Aufgaben =================
f.block("function drawTarget(){","\n/* ---------- Wetter laden","""let goalLayers = [];
function clearGoals(){ [tgtRing0, tgtRing, tgtCore, tgtMk].forEach(x => map.removeLayer(x)); goalLayers.forEach(x => map.removeLayer(x)); goalLayers = []; bestLine.setLatLngs([]); }
const crossIcon = col => L.divIcon({className: 'mk', iconSize: [30, 30], iconAnchor: [15, 15], html: `<svg viewBox="0 0 30 30" width="30" height="30"><path d="M6 6l18 18M24 6L6 24" stroke="#0a1019" stroke-width="8" stroke-linecap="round"/><path d="M6 6l18 18M24 6L6 24" stroke="${col}" stroke-width="4.5" stroke-linecap="round"/></svg>`});
function drawGoals(){
  clearGoals(); const k = TASK(), add = x => { goalLayers.push(x.addTo(map)); return x; };
  if (k === 'target' && TARGET){
    const p = ll(TARGET.e, TARGET.n); tgtRing0.setRadius(scoreRadius(TARGET.dist)); tgtRing0.setLatLng(p).addTo(map); tgtRing.setRadius(scoreRadius(TARGET.dist)); tgtRing.setLatLng(p).addTo(map); tgtCore.setLatLng(p).addTo(map); tgtMk.setLatLng(p).addTo(map); tgtMk.setTooltipContent(placeName());
    map.fitBounds([ll(0, 0), p], {padding: [50, 50]});
  } else if (k === 'wz' && WZ){
    WZ.crosses.forEach((c, i) => {
      const p = ll(c.e, c.n), col = WZ_COL[i % 3];
      add(L.circle(p, {radius: WZ_R, color: '#0a1019', weight: 7, opacity: .6, fill: false, interactive: false}));
      add(L.circle(p, {radius: WZ_R, color: col, weight: 3, dashArray: '8 7', fill: false, interactive: false}));       // Wertungsradius
      for (const ang of [Math.PI / 4, -Math.PI / 4]){                                                                    // das Kreuz selbst: 6 m breit, jeder Strich 1 m breit
        const ca = Math.cos(ang), sa = Math.sin(ang), q = (x, y) => ll(c.e + x * ca - y * sa, c.n + x * sa + y * ca);
        add(L.polygon([q(-3, -.5), q(3, -.5), q(3, .5), q(-3, .5)], {stroke: false, fillColor: col, fillOpacity: 1, interactive: false}));
      }
      add(L.marker(p, {keyboard: false, interactive: false, zIndexOffset: 300, icon: crossIcon(col)}).bindTooltip(tr('wz_cross', {n: i + 1}), {permanent: true, direction: 'right', offset: [14, 0], className: 'ptip'}));
    });
    map.fitBounds([ll(0, 0)].concat(WZ.crosses.map(c => ll(c.e, c.n))), {padding: [50, 50]});
  } else if (k === 'mid'){
    add(L.circle(ll(0, 0), {radius: 200, color: '#0a1019', weight: 7, opacity: .6, fill: false, interactive: false}));
    add(L.circle(ll(0, 0), {radius: 200, color: '#ffe14d', weight: 3, dashArray: '8 7', fill: false, interactive: false}));   // volle Punktzahl innerhalb von 200 m
  }
}
/* Wohin die Anzeige „Ziel“ zeigt: Ziel, nächstes Target Cross ohne Säckchen oder (MDT, MID) der Startplatz */
function navPoint(){
  const k = TASK();
  if (k === 'target' && TARGET) return {e: TARGET.e, n: TARGET.n, lbl: tr('tgt'), zoom: true};
  if (k === 'wz' && WZ){
    const open = WZ.crosses.map((c, i) => ({c, i})).filter(x => !WZ.drops.some(q => q.cross === x.i)), list = open.length ? open : WZ.crosses.map((c, i) => ({c, i}));
    let best = null; for (const x of list){ const d = Math.hypot(x.c.e - B.e, x.c.n - B.n); if (!best || d < best.d) best = {e: x.c.e, n: x.c.n, d, lbl: '✕ ' + (x.i + 1), zoom: true}; }
    return best;
  }
  if (k === 'mdt' || k === 'mid') return {e: 0, n: 0, lbl: tr('launch'), zoom: false};
  return null;
}
""")

# ================= Wetterherkunft: Entfernung immer in km =================
f.rep("  return [WX.place, d >= 500 ? tr('sw_wx_at', {dist: nf(d / 1000, d < 9950 ? 1 : 0), card: card(brg)}) : tr('sw_wx_here')].filter(Boolean).join(', ');",
      "  return [WX.place, tr('sw_wx_at', {dist: nf(d / 1000, 1), card: card(brg)})].filter(Boolean).join(', ');        // Entfernung immer in km, auch wenn der Gitterpunkt nah am Startplatz liegt")

# ================= Fahrt vorbereiten =================
f.block("/* ---------- Fahrt vorbereiten:","function resetRun(){","""/* ---------- Fahrt vorbereiten: Wetter, Ballon, Aufgabe, dann das Startfenster ---------- */
function newSim(k){ SIM_ATM = buildAtm(randomWx(Math.random, k === 'mid')); ATM = SIM_ATM; }      // Simulation: jedes Mal ein anderer Wind; MID mit allen Richtungen bis 6000 m
async function prepareRun(){
  const k = TASK();
  clearGoals(); applyStart(FIXED(k) ? BITTERFELD : USER_START);
  TARGET = null; WZ = null; MDT = null;
  if (UI.wx === 'real' && k !== 'mid'){
    busy(tr('busy_wx'));
    TER.on = true; TER.grid = null; TER.fine = null; TER.base = null; TER.failAt = 0;
    const got = await Promise.all([loadWx(START.lat, START.lon, true), terLoad(0, 0, false), terLoad(0, 0, true)]), m = got[0];     // Wetter und Gelände gleichzeitig laden
    if (m){ WX = m; groundAlt = Math.round(m.elev); if (m.cached) toast(tr('wx_cached')); }
    else { WX = null; newSim(k); toast(tr('wx_fail')); }
    if (TER.grid){ TER.base = terRaw(0, 0); groundAlt = Math.round(TER.base); } else TER.on = false;
    if (WX){ wxStart(); wxWhere().then(() => { if (STATE === 'brief') showStart(); }); }           // der Ortsname des Gitterpunkts kommt im Hintergrund nach
  } else { WX = null; newSim(k); TER.on = false; }
  resetRun();
  if (B.ok){
    if (k === 'target'){
      busy(tr('busy_target')); await pause(40); TARGET = makeTarget(CFG, ATM, UI.level);
      if (TARGET){ busy(tr('busy_place')); await placeTarget(); }
    } else if (k === 'wz'){
      busy(tr('busy_target')); await pause(40); const w = makeCrosses(CFG, ATM);
      if (w){ WZ = {crosses: w.crosses, drops: [], path: w.path}; B.marks = w.crosses.length; B.mU = Math.max(0, B.mU - Math.round(B.marks * CFG.markKg * 10)); renderSand(true); }   // Säckchen an Bord, dafür etwas weniger Sand
    } else if (k === 'mdt'){
      busy(tr('busy_best')); await pause(40); MDT = {best: bestDistance(CFG, ATM, LIMITS.mdt)};
    }
  }
  drawGoals(); showStart();
}
/* Zielort (ZIE-04, ZIE-07): Sportplatz in der Nähe des berechneten Landepunkts, sonst Landezone; gesperrte Orte werden gemieden.
   Der Kartendienst bekommt höchstens 7 Sekunden je Abfrage und höchstens zwei Abfragen; Antworten werden für die Sitzung gemerkt. */
const osmSeen = new Map();
async function osmFetch(lat, lon, rP){
  const key = lat.toFixed(3) + ',' + lon.toFixed(3) + ',' + Math.round(rP / 100); if (osmSeen.has(key)) return osmSeen.get(key);
  const ac = new AbortController(), to = setTimeout(() => ac.abort(), 7000);
  try{
    const r = await fetch(OSM.url, {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: 'data=' + encodeURIComponent(osmQuery(lat, lon, rP)), signal: ac.signal});
    if (!r.ok) throw new Error('http ' + r.status);
    const els = (await r.json()).elements || []; osmSeen.set(key, els); return els;
  } finally { clearTimeout(to); }
}
async function placeTarget(){
  for (let attempt = 0; attempt < 2; attempt++){
    const p = ll(TARGET.e, TARGET.n), rP = Math.max(300, Math.min(OSM.rPlace, 0.25 * TARGET.dist)); let els;
    try{ els = await osmFetch(p[0], p[1], rP); }catch(e){ TARGET.place = {kind: 'zone', name: null, unchecked: true}; return; }
    const r = pickPlace(els, p[0], p[1], rP);
    if (r.blocked && attempt < 1){ const t2 = makeTarget(CFG, ATM, UI.level); if (t2){ TARGET = t2; continue; } }   // Landepunkt liegt an einem gesperrten Ort: einmal ein anderes Ziel rechnen
    const de = (r.lon - p[1]) * klon(), dn = (r.lat - p[0]) * KLAT;
    TARGET.refMiss = Math.hypot(de, dn); TARGET.e += de; TARGET.n += dn;
    TARGET.dist = Math.hypot(TARGET.e, TARGET.n); TARGET.brg = (Math.atan2(TARGET.e, TARGET.n) * 180 / Math.PI + 360) % 360;
    TARGET.place = {kind: r.kind, name: r.name, unchecked: !r.clear};
    return;
  }
}
const placeName = () => TARGET && TARGET.place ? (TARGET.place.name || tr(TARGET.place.kind === 'pitch' ? 'pl_pitch' : 'pl_zone')) : tr('target');
""")

# ================= Startfenster =================
f.block("function showStart(){","let introUntil = 0;","""function showStart(){
  const a = atmAt(ATM, 0), sp = Math.hypot(a.u, a.v), k = TASK();
  let i0 = -1, i1 = -1;                                    // unterste Inversion suchen
  for (let z = 0; z < 5000; z += 50){ const inv = atmAt(ATM, z + 50).T - atmAt(ATM, z).T > 0.025; if (inv && i0 < 0) i0 = z; if (!inv && i0 >= 0){ i1 = z; break; } }
  const lv = ['lv_easy', 'lv_mid', 'lv_hard'];
  let tg = tr('sw_target_none'), ok = B.ok;
  if (k === 'target'){
    tg = TARGET ? (TARGET.place ? placeName() + '. ' : '') + tr('sw_target_val', {dist: nf(TARGET.dist / 1000, 1), brg: deg3(TARGET.brg), card: card(TARGET.brg), lvl: tr(lv[TARGET.level]), min: Math.round(TARGET.t / 60)}) + (TARGET.lowShear ? ' ' + tr('sw_lowshear') : '') + (TARGET.place && TARGET.place.unchecked ? ' ' + tr('sw_unchecked') : '') : tr('sw_notarget');
    ok = ok && !!TARGET;
  } else if (k === 'wz'){
    if (WZ){ const c = WZ.crosses[0], brg = (Math.atan2(c.e, c.n) * 180 / Math.PI + 360) % 360; tg = tr('sw_wz', {n: WZ.crosses.length, dist: nf(Math.hypot(c.e, c.n) / 1000, 1), brg: deg3(brg), card: card(brg)}); }
    else { tg = tr('sw_notarget'); ok = false; }
  } else if (k === 'mdt'){
    tg = MDT && MDT.best ? tr('sw_mdt') : tr('sw_notarget'); ok = ok && !!(MDT && MDT.best);
  } else if (k === 'mid') tg = tr('sw_mid');
  $('sw-tlbl').textContent = tr(k === 'free' || k === 'target' ? 'sw_target' : 'su_task');
  $('sw-target').textContent = tg;
  $('sw-start').textContent = tr('st_name_' + (START.kind || 'map')) + ' (' + START.lat.toFixed(4) + ', ' + START.lon.toFixed(4) + ')';
  $('sw-wx').textContent = (WX ? tr('sw_wx_real', {time: new Date(WX.valid).toISOString().slice(11, 16), where: isFinite(WX.lat) && isFinite(WX.lon) ? wxWhereText() : '–'}) : tr('sw_wx_sim')) + ' ' + tr('sw_wx_val', {dir: deg3(dirFrom(a.u, a.v)), spd: spd(sp) + ' ' + UNITS[UI.unit][1], t: nf(a.T - 273.15), p: nf(Math.round(a.p / 100))}) + (i0 >= 0 && i1 > i0 ? ' ' + tr('sw_inv', {i0, i1}) : '');
  $('sw-bal').textContent = tr('sw_bal_val', {vol: nf(CFG.vol), pax: CFG.pax, rust: nf(CFG.rust), eq: nf(CFG.equip)});
  $('sw-sand').textContent = B.ok ? tr('sw_sand_val', {trim: nf(sandKg(B, CFG), 1), sacks: B.sacks, sk: nf(CFG.sackKg), mulde: nf(B.mU / 10, 1)}) : tr('hint_heavy');
  $('sw-note').textContent = B.ok ? tr('sw_note') : '';
  $('sw-go').disabled = !ok; $('sw-go').style.opacity = ok ? 1 : .45;
  document.querySelectorAll('.tgt').forEach(el => { el.hidden = !navPoint(); });
  setState('brief');
}
""")
f.block("function startView(){","$('sw-go').addEventListener('click'","""function startView(){                                      // vor dem Start: erst das Ziel zeigen, dann wandert die Karte vom Ziel zum Start
  map.invalidateSize(); const k = TASK(); let g = null;
  if (k === 'target' && TARGET) g = {e: TARGET.e, n: TARGET.n, txt: placeName() + ' · ' + nf(TARGET.dist / 1000, 1) + ' km ' + card(TARGET.brg)};
  else if (k === 'wz' && WZ){ const c = WZ.crosses[0]; g = {e: c.e, n: c.n, txt: tr('wz_cross', {n: 1}) + ' · ' + nf(Math.hypot(c.e, c.n) / 1000, 1) + ' km ' + card((Math.atan2(c.e, c.n) * 180 / Math.PI + 360) % 360)}; }
  if (g){
    map.setView(ll(g.e, g.n), 14, {animate: false}); toast(g.txt);
    introUntil = performance.now() + 2000 + 5000 + 300;
    setTimeout(() => { if (STATE === 'play' && !B.air) map.flyTo(ll(0, 0), 14, {duration: 5, easeLinearity: 0.15}); else introUntil = 0; }, 2000);
  } else { map.setView(ll(0, 0), 14, {animate: false}); introUntil = 0; }
}
function followView(p){                                    // Ballon in der Mitte; im Anflug Ballon und Ziel (oder nächstes Kreuz) zusammen im Bild
  const np = navPoint(), wz = TASK() === 'wz';
  if (np && np.zoom && Math.hypot(np.e - B.e, np.n - B.n) < (wz ? 2500 : 8000)){
    const bnd = L.latLngBounds([p, ll(np.e, np.n)]), z = Math.min(wz ? 17 : 15, map.getBoundsZoom(bnd, false, L.point(230, 130))), c = bnd.getCenter();
    if (Math.abs(z - map.getZoom()) >= 0.25) map.setView(c, z, {animate: false}); else map.panTo(c, {animate: false});
  } else map.panTo(p, {animate: false});
}
""")

# ================= Hauptmenü, Aufgabenauswahl, Vorbereitung =================
f.block("function showMenu(){","/* Startplatz (SPI-01)","""function showMenu(){
  $('result').hidden = true; $('hint').hidden = true; $('follow').hidden = true;
  const m = document.querySelector('.mcard'); m.classList.remove('boot'); void m.offsetWidth; m.classList.add('boot');   // Menü neu einblenden
  menuAt = performance.now(); setTimeout(() => SND.music(musicWanted()), 1800);          // die Musik setzt nach dem Einblenden ein
  MENUBG.reset(); setState('menu');
}
function applyStart(s){ START = s; groundAlt = s.alt; startMk.setLatLng(ll(0, 0)); balMk.setLatLng(ll(0, 0)); pathLine.setLatLngs([]); map.setView(ll(0, 0), 13); }
function openSetup(mode, task){
  UI.mode = mode; if (task) UI.task = task; saveUI(); const k = TASK();
  clearGoals(); applyStart(FIXED(k) ? BITTERFELD : USER_START);
  $('su-title').textContent = k === 'free' ? tr('m_free') : tr('task_' + k);
  $('su-task').hidden = k === 'free'; if (k !== 'free') $('su-tdesc').textContent = tr('task_' + k + '_d');
  $('su-levelbox').hidden = k !== 'target'; $('su-startsel').hidden = FIXED(k); $('su-startfix').hidden = !FIXED(k);
  $('seg-wx').hidden = k === 'mid'; $('su-wxmid').hidden = k !== 'mid';
  stShow(); setState('setup');
}
$('m-free').addEventListener('click', () => openSetup('free'));
$('m-chal').addEventListener('click', () => setState('chal'));
document.querySelectorAll('#chal [data-task]').forEach(b => b.addEventListener('click', () => openSetup('challenge', b.dataset.task)));
$('ch-back').addEventListener('click', () => setState('menu'));
$('m-score').addEventListener('click', showScores);
$('sc-back').addEventListener('click', () => setState('menu'));
$('m-name').value = UI.name || '';
$('m-name').addEventListener('input', () => { UI.name = $('m-name').value.slice(0, 16); saveUI(); });
$('su-back').addEventListener('click', () => { if (UI.mode === 'challenge') setState('chal'); else setState('menu'); });
$('su-go').addEventListener('click', prepareRun);

""")
f.line("function stSet(s){","function stSet(s){ USER_START = s; store.set('gb-start', s); applyStart(s); stShow(); toast(tr('st_ok')); }")
f.rep("$('st-map').addEventListener('click', () => { [tgtRing0, tgtRing, tgtCore, tgtMk].forEach(x => map.removeLayer(x)); bestLine.setLatLngs([]); pathLine.setLatLngs([]);","$('st-map').addEventListener('click', () => { clearGoals(); pathLine.setLatLngs([]);")
f.rep("$('sw-back').addEventListener('click', () => openSetup(UI.mode));","$('sw-back').addEventListener('click', () => openSetup(UI.mode));\n\n/* ---------- Säckchen abwerfen (Wandziel, AUF-02) ---------- */\n$('mk-drop').addEventListener('click', () => {\n  if (STATE !== 'play' || PAUSED || !WZ || !(B.marks > 0) || B.landed || !B.air) return;\n  const q = markerFall(ATM, B.e, B.n, B.h, B.gnd), col = WZ_COL[WZ.drops.length % 3]; B.marks--;\n  let bi = 0, bd = 1e9; WZ.crosses.forEach((c, i) => { const d = Math.hypot(c.e - q[0], c.n - q[1]); if (d < bd){ bd = d; bi = i; } });      // gewertet wird am nächstgelegenen Kreuz\n  WZ.drops.push({e: q[0], n: q[1], cross: bi, d: bd});\n  goalLayers.push(L.circleMarker(ll(q[0], q[1]), {radius: 6, color: '#0a1019', weight: 2, fillColor: col, fillOpacity: 1, interactive: false}).addTo(map));\n  SND.marker(); toast(tr('mk_toast', {d: fmtD(bd), n: bi + 1}));\n});")

# ================= Anzeige =================
f.rep("  if (TARGET){ const de = TARGET.e - B.e, dn = TARGET.n - B.n; $('i-tdist').textContent = fmtD(Math.hypot(de, dn)); $('i-tbrg').textContent = deg3((Math.atan2(de, dn) * 180 / Math.PI + 360) % 360); }",
"""  const k = TASK(), np = navPoint();
  if (np){ const de = np.e - B.e, dn = np.n - B.n; $('i-tlbl').textContent = np.lbl; $('i-tdist').textContent = fmtD(Math.hypot(de, dn)); $('i-tbrg').textContent = deg3((Math.atan2(de, dn) * 180 / Math.PI + 360) % 360); }
  const lim = LIMITS[k] || 0; $('timer').hidden = !lim || STATE === 'brief' || STATE === 'busy';                         // Zeit für MDT und MID: Rest bis zur Sollzeit, danach die Überzeit
  if (lim){ const left = lim - B.t, tv = $('tm-val'); tv.textContent = (left < 0 ? '+' : '') + fmtHMS(Math.abs(left)); tv.style.color = left < 0 ? 'var(--dn)' : left < 300 ? 'var(--warn)' : 'var(--tx)'; }
  const mk = $('mk-drop'); mk.hidden = !(k === 'wz' && WZ); if (!mk.hidden){ $('mk-n').textContent = B.marks; mk.disabled = !(B.marks > 0) || !B.air || B.landed; }""")
f.rep("  $('i-fill').textContent = nf(B.gas0 > 0 ? B.gas / B.gas0 * 100 : 0) + ' %';","  $('i-fill').textContent = nf(B.gas0 > 0 ? B.gas / B.gas0 * 100 : 0, 1) + ' %';")
f.rep("const fmtT = t => {","const fmtHMS = t => { t = Math.floor(t); return String(Math.floor(t / 3600)).padStart(2, '0') + ':' + String(Math.floor(t / 60) % 60).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); };\nconst fmtT = t => {")

# ================= Bestenliste, Auswertung, Online-Dienst =================
f.block("/* ---------- Bestenliste (PUN-07)","/* ---------- Hauptmenü: bewegtes Bild","""/* ---------- Online-Dienst (SRV-02 bis SRV-04): vorbereitet, aber abgeschaltet, solange keine Adresse eingetragen ist ----------
   Mit einer Adresse meldet die App jede gewertete Fahrt an den Dienst, holt die gemeinsame Bestenliste dort ab und meldet
   Besuch und Nutzungsdauer. Schnittstelle (IF-09): ?action=top (GET) liefert bis zu 100 Einträge {n, p, c, l, s, at};
   ?action=score, ?action=visit und ?action=leave (POST, JSON als Text) nehmen Meldungen entgegen. */
const ONLINE = {api: ''};                                  // zum Beispiel 'https://example.org/gasballon/api.php'
const uid = () => { let u = store.get('gb-uid', null); if (!u){ u = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Math.random()).slice(2) + Date.now(); store.set('gb-uid', u); } return u; };   // zufällige Kennung des Geräts, kein Name
async function onlineCall(action, body){
  const ac = new AbortController(), to = setTimeout(() => ac.abort(), 6000);
  try{
    const r = await fetch(ONLINE.api + '?action=' + action, body ? {method: 'POST', headers: {'Content-Type': 'text/plain'}, body: JSON.stringify(body), signal: ac.signal} : {signal: ac.signal});
    if (!r.ok) throw new Error('http ' + r.status); return await r.json();
  } finally { clearTimeout(to); }
}
function onlineScore(e){ if (ONLINE.api) onlineCall('score', Object.assign({id: uid(), build: BUILD}, e)).catch(() => {}); }
function onlineVisit(){
  if (!ONLINE.api) return;
  const q = new URLSearchParams(location.search), t0 = Date.now(); let ref = ''; try{ ref = document.referrer ? new URL(document.referrer).hostname : ''; }catch(e){}
  onlineCall('visit', {id: uid(), src: q.get('src') || q.get('utm_source') || '', ref, lang: UI.lang, build: BUILD}).catch(() => {});   // src: Kennung im Link oder QR-Code, ref: verweisende Seite
  addEventListener('pagehide', () => { try{ navigator.sendBeacon(ONLINE.api + '?action=leave', JSON.stringify({id: uid(), sec: Math.round((Date.now() - t0) / 1000)})); }catch(e){} });
}

/* ---------- Bestenliste (PUN-07): alle gewerteten Fahrten aller Aufgaben; bei gleicher Punktzahl liegt vorn, wer mehr Sand übrig hat (PUN-06) ---------- */
const scoreList = () => { const a = store.get('gb-scores', []); return Array.isArray(a) ? a : []; };
function scoreAdd(e){
  const a = scoreList(); a.push(e); a.sort((x, y) => y.p - x.p || y.s - x.s || x.at - y.at);
  const rank = a.indexOf(e) + 1; store.set('gb-scores', a.slice(0, 100)); return rank <= 100 ? rank : 0;
}
const chalName = e => { const c = e.c || 'target'; return tr('task_' + c) + (c === 'target' ? ' · ' + tr(['lv_easy', 'lv_mid', 'lv_hard'][e.l] || 'lv_easy') : ''); };
async function showScores(){
  setState('scores'); const box = $('sc-list'); box.textContent = '';
  let a = scoreList(), fail = false;
  if (ONLINE.api){ try{ const r = await onlineTop(); if (Array.isArray(r)) a = r; else fail = true; }catch(e){ fail = true; } if (STATE !== 'scores') return; box.textContent = ''; }
  if (fail){ const q = document.createElement('p'); q.className = 'note'; q.textContent = tr('sc_online_fail'); box.appendChild(q); }
  if (!a.length){ const q = document.createElement('p'); q.className = 'note'; q.textContent = tr('sc_empty'); box.appendChild(q); return; }
  const tb = document.createElement('table'); tb.className = 'sc';
  const row = (cells, tag) => { const r = document.createElement('tr'); cells.forEach(c => { const x = document.createElement(tag); x.textContent = c; r.appendChild(x); }); tb.appendChild(r); };
  row([tr('sc_rank'), tr('name_lbl'), tr('r_pts'), tr('sc_chal')], 'th');
  a.slice(0, 100).forEach((e, i) => row([i + 1, e.n, e.p, chalName(e)], 'td'));
  box.appendChild(tb);
}
const onlineTop = () => onlineCall('top');
let cheerQ = 0.5;
function showResult(){
  cheerQ = 0.5; const k = TASK(), rows = [], dStart = Math.hypot(B.e, B.n); let pts = null, note = '';
  $('r-head').textContent = tr(landClass(B.vLand));                                       // Rückmeldung zur Landung (PUN-08)
  $('r-sink').textContent = nf(B.vLand, 1) + ' m/s'; $('r-time').textContent = fmtT(B.t); $('r-dist').textContent = fmtD(B.dist);
  $('r-line').textContent = fmtD(dStart); $('r-max').textContent = nf(Math.round(B.maxH)) + ' m'; $('r-sand').textContent = nf(sandKg(B, CFG), 1) + ' kg'; $('r-gas').textContent = nf(B.gas / B.gas0 * 100, 1) + ' %';
  if (k === 'target' && TARGET){
    const d = Math.hypot(TARGET.e - B.e, TARGET.n - B.n); pts = scoreLanding(d, B.vLand, TARGET.dist);
    rows.push([tr('r_tdist'), fmtD(d)]); note = tr('r_best');
    bestLine.setLatLngs(TARGET.path.map(p => ll(p[0], p[1])));                              // Vergleichsfahrt zeigen (SPI-06)
  } else if (k === 'wz' && WZ){
    const r = scoreCrosses(WZ.crosses, WZ.drops); pts = r.pts;
    r.per.forEach((x, i) => rows.push([tr('wz_cross', {n: i + 1}), x.d == null ? tr('wz_none') : fmtD(x.d) + ' · ' + x.p]));
  } else if (k === 'mdt' && MDT && MDT.best){
    const r = scoreMdt(dStart, MDT.best.dist, B.t, LIMITS.mdt); pts = r.pts;
    rows.push([tr('mdt_best'), fmtD(MDT.best.dist)], [tr('mdt_you'), fmtD(dStart)], [tr('mdt_base'), r.base], [tr('mdt_pen'), '−' + r.pen]);
    note = tr('mdt_note', {h: nf(MDT.best.h)}); bestLine.setLatLngs(MDT.best.path.map(p => ll(p[0], p[1])));
  } else if (k === 'mid'){
    const r = scoreMid(dStart, B.t, LIMITS.mid); pts = r.pts;
    rows.push([tr('mid_dist'), fmtD(dStart)], [tr('mid_pen_d'), '−' + r.penD], [tr('mid_pen_t'), '−' + r.penT]);
  }
  const ex = $('r-extra'); ex.textContent = '';
  rows.forEach(x => { const d = document.createElement('div'), s = document.createElement('span'), v = document.createElement('b'); d.className = 'kv'; s.textContent = x[0]; v.textContent = x[1]; d.appendChild(s); d.appendChild(v); ex.appendChild(d); });
  $('r-ptsrow').hidden = pts == null; $('r-rankrow').hidden = pts == null; $('r-note').hidden = !note; $('r-note').textContent = note;
  if (pts != null){
    const e = {n: (UI.name || '').trim() || 'Pilot', p: pts, c: k, l: k === 'target' ? TARGET.level : null, s: Math.round(sandKg(B, CFG) * 10) / 10, t: Math.round(B.t), at: Date.now()};
    const rank = scoreAdd(e); onlineScore(e);
    $('r-pts').textContent = pts; $('r-rank').textContent = rank ? rank + '.' : '–'; cheerQ = pts / 100;
  }
  $('result').hidden = false; valve = 0; setState('done'); SND.land(B.vLand); if (B.vLand < LAND_HARD) SND.cheer(cheerQ); renderSand(true);
}
$('again').addEventListener('click', prepareRun);
$('r-menu').addEventListener('click', showMenu);

""")

# ================= Menühintergrund im Stil der App =================
f.block("/* ---------- Hauptmenü: bewegtes Bild","/* ---------- Zeitschleife","""/* ---------- Hauptmenü: ruhig bewegtes Bild in den Farben der App. Ein Ballon wirft Sand ab, steigt, lässt Gas ab und sinkt wieder. ---------- */
const MENUBG = (() => {
  const cv = $('menubg'); let c = null, W = 0, H = 0, t = 0, acc = 0, sand = [], puffs = [];
  const clouds = [[0.15, 0.12, 70], [0.62, 0.22, 95], [0.95, 0.07, 60], [0.40, 0.36, 80]];
  function size(){
    const r = cv.getBoundingClientRect(); if (!r.width || !r.height) return false;
    const d = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height;
    if (cv.width !== Math.round(W * d) || cv.height !== Math.round(H * d)){ cv.width = Math.round(W * d); cv.height = Math.round(H * d); }
    c = cv.getContext('2d'); c.setTransform(d, 0, 0, d, 0, 0); return true;
  }
  function draw(dt){
    if (!size()) return; t += dt;
    // Der Ballon beginnt unten links am Boden und treibt beim Steigen und Sinken langsam nach rechts
    const R = Math.max(18, Math.min(30, W * 0.065)), ground = H - 44, yBot = ground - R * 1.9, yTop = R + 26, T = 18;
    const ph = (t % T) / T, by = yBot - (yBot - yTop) * (0.5 - 0.5 * Math.cos(2 * Math.PI * ph)), bx = ((W * 0.22 + W * 0.018 * t) % (W + 4 * R)) - 2 * R;
    const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#0a1019'); g.addColorStop(1, '#17253b'); c.fillStyle = g; c.fillRect(0, 0, W, H);
    c.fillStyle = 'rgba(154,171,196,.09)';
    for (const cl of clouds){ const cx = ((cl[0] * W - t * 5) % (W + 240) + W + 240) % (W + 240) - 120, cy = cl[1] * H; c.beginPath(); c.ellipse(cx, cy, cl[2], cl[2] * .26, 0, 0, 7); c.fill(); c.beginPath(); c.ellipse(cx + cl[2] * .45, cy + 5, cl[2] * .7, cl[2] * .2, 0, 0, 7); c.fill(); }
    c.fillStyle = '#122035'; c.beginPath(); c.moveTo(0, H);
    for (let x = 0; x <= W + 8; x += 8) c.lineTo(x, ground - 12 - 10 * Math.sin((x + t * 12) / 70) - 6 * Math.sin((x + t * 12) / 29));
    c.lineTo(W, H); c.fill();
    c.fillStyle = '#0d1828'; c.fillRect(0, ground, W, H - ground);
    if (ph < 0.12 || ph > 0.94) sand.push({x: bx - R * .2 + Math.random() * 4, y: by + R * 1.85, v: 30 + Math.random() * 30});
    if (ph > 0.44 && ph < 0.54 && Math.random() < 0.5) puffs.push({x: bx - 5 + Math.random() * 10, y: by - R - 2, a: 1});
    sand = sand.filter(q => (q.y += q.v * dt, q.v += 260 * dt, q.y < ground + 3)); c.fillStyle = '#d9b36c'; for (const q of sand) c.fillRect(q.x, q.y, 2, 2);
    puffs = puffs.filter(q => (q.y -= 34 * dt, q.a -= dt * 0.9, q.a > 0)); for (const q of puffs){ c.fillStyle = 'rgba(238,243,250,' + (0.5 * q.a).toFixed(2) + ')'; c.fillRect(q.x, q.y, 3, 2); }
    c.fillStyle = '#ff9f1c'; c.beginPath(); c.arc(bx, by, R, 0, 7); c.fill();                                                           // Hülle mit Füllansatz
    c.beginPath(); c.moveTo(bx - R * .64, by + R * .77); c.lineTo(bx + R * .64, by + R * .77); c.lineTo(bx + R * .2, by + R * 1.28); c.lineTo(bx - R * .2, by + R * 1.28); c.fill();
    c.strokeStyle = 'rgba(10,16,25,.3)'; c.lineWidth = 1.5; c.beginPath(); c.ellipse(bx, by, R * .5, R, 0, 0, 7); c.stroke(); c.beginPath(); c.moveTo(bx, by - R); c.lineTo(bx, by + R); c.stroke();
    c.strokeStyle = '#eef3fa'; c.lineWidth = 1.2; c.beginPath(); c.moveTo(bx - R * .2, by + R * 1.28); c.lineTo(bx - R * .16, by + R * 1.6); c.moveTo(bx + R * .2, by + R * 1.28); c.lineTo(bx + R * .16, by + R * 1.6); c.stroke();
    c.fillStyle = '#eef3fa'; c.fillRect(bx - R * .18, by + R * 1.6, R * .36, R * .26);                                                  // Korb
  }
  return { tick(real){ acc += real; if (acc < 1 / 30) return; draw(acc); acc = 0; }, reset(){ t = 0; acc = 0; sand = []; puffs = []; } };
})();

""")
f.rep("  if (STATE === 'menu' || STATE === 'scores'){ RETRO.tick(real); requestAnimationFrame(frame); return; }","  if (STATE === 'menu' || STATE === 'scores' || STATE === 'chal'){ MENUBG.tick(real); requestAnimationFrame(frame); return; }")
f.rep("  if (STATE === 'setup') $('su-title').textContent = tr(UI.mode === 'challenge' ? 'm_chal' : 'm_free');","  if (STATE === 'setup') openSetup(UI.mode);\n  if (WZ && STATE !== 'menu') goalLayers.forEach(x => { if (x.getTooltip && x.getTooltip()) x.setTooltipContent(x.getTooltip().getContent().replace(/^.*?(\\d+)$/, (m, n) => tr('wz_cross', {n}))); });")
f.rep("applyLang(); applyTiles(); renderSand(true); showMenu();","applyLang(); applyTiles(); renderSand(true); showMenu(); onlineVisit();")
f.save(); print('ok')
