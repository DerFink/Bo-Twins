import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ================= Kern =================
f.line("  envEps: 0.85,","""  envEps: 0.90,    // Emissionsgrad der Hülle im Infraroten: weißes, PVC-beschichtetes Gewebe (Annahme; Kunststoffe liegen bei rund 0,9)
  envAlpha: 0.25,  // Anteil des Sonnenlichts, den die weiße Hülle aufnimmt (Annahme; weiße Anstriche liegen bei 0,2 bis 0,3)
  rainFilm: 0.10,  // kg Wasser je m² Hüllenfläche, die bei Regen höchstens haften bleiben: ein Film von 0,1 mm (Annahme)
  dryTau: 1800,    // s, Zeit, in der das Wasser nach dem Regen abtropft und abtrocknet (Annahme)""")
f.rep("const DZ = 25, ZTOP = 10000;","""const DZ = 25, ZTOP = 10000;
/* Sonnenstand: Sinus der Sonnenhöhe für Ort und Zeitpunkt (UTC in ms), Näherung der NOAA (Deklination und Zeitgleichung als Fourierreihe). */
function sunSin(lat, lon, ms){
  const d = new Date(ms), y0 = Date.UTC(d.getUTCFullYear(), 0, 1), hr = d.getUTCHours() + d.getUTCMinutes() / 60 + d.getUTCSeconds() / 3600;
  const g = 2 * Math.PI / 365.24 * ((ms - y0) / 864e5 - hr / 24 + (hr - 12) / 24);
  const dec = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
  const eot = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));   // Minuten
  const ha = ((hr * 60 + eot + 4 * lon) / 4 - 180) * Math.PI / 180, la = lat * Math.PI / 180;
  return Math.sin(la) * Math.sin(dec) + Math.cos(la) * Math.cos(dec) * Math.cos(ha);
}
/* Die Simulation spielt immer an einem Sommermorgen ohne Wolken und Regen (Vorgabe Nutzer): 21. Juni, 7 Uhr Sonnenzeit am Startplatz. */
const SIM_LAT = 51.6246, SIM_LON = 12.2946;
const simT0 = lon => Date.UTC(2026, 5, 21, 7, 0, 0) - lon / 15 * 3600e3;
/* Wolken über und unter jeder Tabellenhöhe (größter Bedeckungsgrad 0 bis 1) und die Obergrenze der untersten Wolkenschicht:
   Darunter und darin fällt der Regen, wenn das Wettermodell Niederschlag meldet. */
function cloudInfo(tab){
  if (tab._ci) return tab._ci;
  const n = tab.length, up = new Float32Array(n), dn = new Float32Array(n); let m = 0, b = -1, t = -1;
  for (let i = n - 1; i >= 0; i--){ m = Math.max(m, tab[i].c || 0); up[i] = m; }
  m = 0; for (let i = 0; i < n; i++){ dn[i] = m; m = Math.max(m, tab[i].c || 0); }
  for (let i = 0; i < n; i++){ if ((tab[i].c || 0) >= 0.5){ if (b < 0) b = i; t = i; } else if (b >= 0) break; }
  return tab._ci = {up, dn, base: b >= 0 ? b * DZ : null, top: b >= 0 ? (t + 1) * DZ : null, rainTop: b >= 0 ? (t + 1) * DZ : 2000};
}
/* Umgebung des Ballons für Strahlung und Regen: Sonnenstand, Wolken darüber und darunter, Boden, Regen in dieser Höhe. */
function radEnv(B, tab){
  const ci = cloudInfo(tab), i = Math.max(0, Math.min(tab.length - 1, Math.round(B.h / DZ)));
  const lat = (B.lat0 == null ? SIM_LAT : B.lat0) + B.n / 111320, lon = (B.lon0 == null ? SIM_LON : B.lon0) + B.e / (111320 * Math.cos(lat * Math.PI / 180));
  const rain = (tab.rain || 0) > 0.05 && B.h < ci.rainTop ? tab.rain : 0;
  return {s: sunSin(lat, lon, (B.t0 == null ? simT0(SIM_LON) : B.t0) + B.t * 1000), cu: ci.up[i], cd: ci.dn[i], Ts: tab[0].T, ps: tab[0].p, rain};
}""")
f.rep("    tab.push({T, p, u: A[0] + (B[0] - A[0]) * f, v: A[1] + (B[1] - A[1]) * f});","    tab.push({T, p, u: A[0] + (B[0] - A[0]) * f, v: A[1] + (B[1] - A[1]) * f, c: 0});")
f.rep("    T = T2;\n  }\n  return tab;\n}","    T = T2;\n  }\n  tab.rain = 0; tab.lat = wx.lat == null ? SIM_LAT : wx.lat; tab.lon = wx.lon == null ? SIM_LON : wx.lon; tab.t0 = wx.t0 == null ? simT0(tab.lon) : wx.t0;\n  return tab;\n}")
f.rep("    return {T, p: a.p * Math.exp(-G0 * M_AIR * h / (R_GAS * (a.T + T) / 2)), u: a.u, v: a.v};","    return {T, p: a.p * Math.exp(-G0 * M_AIR * h / (R_GAS * (a.T + T) / 2)), u: a.u, v: a.v, c: a.c || 0};")
f.rep("  return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f};\n}\n","  return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f, c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f};\n}\n")
f.rep("  return {ok: Lo.ok, h: 0, w: 0, e: 0, n: 0, t: 0, dist: 0, maxH: 0, gas: Lo.n, gas0: Lo.n, Tg: a.T, Tf: a.T,","  return {ok: Lo.ok, h: 0, w: 0, e: 0, n: 0, t: 0, dist: 0, maxH: 0, gas: Lo.n, gas0: Lo.n, Tg: a.T, Tf: a.T, wet: 0, t0: tab.t0, lat0: tab.lat, lon0: tab.lon,")
# Wärmehaushalt
f.rep("   Hülle ↔ Luft: freie Konvektion an der Kugel (Churchill 1983)","   Strahlung (STE-23): Die Hülle nimmt Sonnenlicht auf (direkt auf ihre Querschnittsfläche, dazu Himmelslicht und vom Boden oder von Wolken\n   zurückgeworfenes Licht), sie nimmt Wärmestrahlung vom Himmel und vom Boden auf und strahlt selbst mit ihrer Temperatur ab. Der klare\n   Himmel strahlt schwächer als die Luft warm ist; deshalb kühlt die Hülle nachts unter die Lufttemperatur. Wolken darüber heben das auf.\n   Hülle ↔ Luft: freie Konvektion an der Kugel (Churchill 1983)")
f.rep("   weil er waagerecht mit dem Wind treibt. Dazu Wärmestrahlung der Hülle; die Umgebung strahlt vereinfacht mit Lufttemperatur.\n   Sonneneinstrahlung ist nicht berücksichtigt. Das Gas gilt als durchmischt. */","   weil er waagerecht mit dem Wind treibt. Regen kühlt die Hülle auf Lufttemperatur. Das Gas gilt als durchmischt, die Hülle als gleichmäßig warm. */")
f.rep("function heatExchange(B, cfg, a, V, dt){","function heatExchange(B, cfg, a, V, dt, env){")
f.rep("  const hR = 4 * cfg.envEps * SIGMA * Tfa * Tfa * Tfa;\n","""  // Strahlung
  env = env || {s: -1, cu: 0, cd: 0, Ts: a.T, ps: a.p, rain: 0};
  const R2 = Math.PI * D * D / 4, T4 = a.T * a.T * a.T * a.T;
  let qSun = 0;
  if (env.s > 0.01){
    const elDeg = Math.asin(Math.min(1, env.s)) * 180 / Math.PI, am = (a.p / 101325) / (env.s + 0.50572 * Math.pow(elDeg + 6.07995, -1.6364));   // Luftmasse nach Kasten und Young, mit dem Druck verkürzt
    const dni0 = 1361 * Math.pow(0.7, Math.pow(am, 0.678)), dif0 = 0.15 * dni0 * env.s;                                                   // klarer Himmel: Direktstrahlung nach Meinel, Himmelslicht waagerecht
    const dni = dni0 * (1 - env.cu), dif = dif0 * (1 - env.cu) + 0.3 * env.cu * (dni0 * env.s + dif0), ghi = dni * env.s + dif;        // Wolken darüber lassen rund 30 % als Streulicht durch
    qSun = cfg.envAlpha * R2 * (dni + 2 * dif + 2 * (0.2 + 0.4 * env.cd) * ghi);                                                         // Rückstrahlung: Boden 0,2, Wolkendecke darunter 0,6
  }
  const eSky = 0.74 * Math.sqrt(a.p / 101325), fUp = Math.min(1, a.p / env.ps);
  const Esky = (eSky + (1 - eSky) * env.cu) * SIGMA * T4;                                                                              // Gegenstrahlung des Himmels; Wolken strahlen wie die Luft
  const Eup = SIGMA * ((1 - env.cd) * (fUp * Math.pow(env.Ts, 4) + (1 - fUp) * T4) + env.cd * T4);                                      // von unten: Boden, mit der Höhe zunehmend die Luft; über Wolken deren Oberseite
  const qIR = cfg.envEps * (2 * R2 * (Esky + Eup) - A * SIGMA * Math.pow(B.Tf, 4));
  const qRain = env.rain / 3600 * R2 * 4186 * (a.T - B.Tf);                                                                            // Regenwasser mit Lufttemperatur
""")
f.rep("  const qEnv = (hE + hR) * A * (a.T - B.Tf) - qGas;    // W, Umgebung an Hülle abzüglich der Abgabe ans Gas","  const qEnv = hE * A * (a.T - B.Tf) + qSun + qIR + qRain - qGas;    // W, Luft, Sonne, Wärmestrahlung und Regen an die Hülle, abzüglich der Abgabe ans Gas")
f.rep("  B.hI = hI; B.hE = hE; B.hR = hR;","  B.hI = hI; B.hE = hE; B.qSun = qSun; B.qIR = qIR;")
# Schritt: Umgebung, Regenwasser
f.rep("  const a = atmAt(tab, B.h);\n  if (valve > 0 && B.gas > 0){","  const a = atmAt(tab, B.h), env = radEnv(B, tab);\n  if (valve > 0 && B.gas > 0){")
f.rep("  const load = fixedKg(cfg) + sandKg(B, cfg) + B.marks * cfg.markKg - B.ropeOn;","""  if (B.air || B.go){                                                      // Regen (STE-24): Wasser bleibt auf der Hülle haften, bis ein Film gesättigt ist; danach trocknet es ab
    const D0 = Math.cbrt(6 * cfg.vol / Math.PI), wMax = cfg.rainFilm * Math.PI * D0 * D0;
    if (env.rain > 0) B.wet = Math.min(wMax, (B.wet || 0) + env.rain / 3600 * Math.PI * D0 * D0 / 4 * Math.max(0, 1 - (B.wet || 0) / wMax) * dt);
    else if (B.wet > 0) B.wet = Math.max(0, B.wet - B.wet / cfg.dryTau * dt - 0.0005 * dt);
  }
  B.rain = env.rain; B.sun = env.s; B.cu = env.cu;
  const load = fixedKg(cfg) + sandKg(B, cfg) + B.marks * cfg.markKg - B.ropeOn + (B.wet || 0);""")
f.rep("  heatExchange(B, cfg, a2, V, dt);","  heatExchange(B, cfg, a2, V, dt, env);")
# Wetter: Wolken und Niederschlag
f.block("function wxUrl(lat, lon){","const windUV","""function wxUrl(lat, lon, lite){                           // lite: ohne Wolken und Niederschlag, falls der Dienst die erweiterte Abfrage ablehnt
  const h = ['temperature_2m', 'wind_speed_10m', 'wind_direction_10m', 'surface_pressure'];
  if (!lite) h.push('precipitation', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high');
  WX_LEVELS.forEach(L => ['temperature', 'wind_speed', 'wind_direction', 'geopotential_height'].concat(lite ? [] : ['cloud_cover']).forEach(v => h.push(v + '_' + L + 'hPa')));
  return 'https://api.open-meteo.com/v1/forecast?latitude=' + lat.toFixed(4) + '&longitude=' + lon.toFixed(4) + '&hourly=' + h.join(',') + '&wind_speed_unit=ms&timezone=UTC&forecast_days=3';
}
""")
f.rep("const uv0 = windUV(g('wind_speed_10m'), g('wind_direction_10m') || 0); pts.push({z: elev, T: g('temperature_2m') + 273.15, u: uv0[0], v: uv0[1]});","""const uv0 = windUV(g('wind_speed_10m'), g('wind_direction_10m') || 0); pts.push({z: elev, T: g('temperature_2m') + 273.15, u: uv0[0], v: uv0[1]});
      const lay = z => { const q = z - elev < 3000 ? g('cloud_cover_low') : z - elev < 8000 ? g('cloud_cover_mid') : g('cloud_cover_high'); return q == null ? 0 : q / 100; };   // Ersatz, wenn die Bedeckung je Druckfläche fehlt""")
f.rep("if (z != null && T != null && sp != null && d != null && z > elev + 40){ const uv = windUV(sp, d); pts.push({z, T: T + 273.15, u: uv[0], v: uv[1], pl: L * 100}); }","if (z != null && T != null && sp != null && d != null && z > elev + 40){ const uv = windUV(sp, d), cc = g('cloud_cover_' + L + 'hPa'); pts.push({z, T: T + 273.15, u: uv[0], v: uv[1], pl: L * 100, c: cc == null ? lay(z) : cc / 100}); }")
f.rep("      if (pts.length < 4) continue;","      if (pts.length < 4) continue;\n      pts[0].c = 0;                                                         // am Boden keine Wolke (Nebel ist nicht nachgebildet)")
f.rep("      hours.push({t: tt[k], p0, pts});","      hours.push({t: tt[k], p0, pts, rain: g('precipitation') || 0, cloud: g('cloud_cover')});")
f.rep("    const z = zref + k * DZ; let T, u, v;\n    if (z <= P[0].z){ T = P[0].T + 0.0065 * (P[0].z - z); u = P[0].u; v = P[0].v; }","    const z = zref + k * DZ; let T, u, v, c = 0;\n    if (z <= P[0].z){ T = P[0].T + 0.0065 * (P[0].z - z); u = P[0].u; v = P[0].v; }")
f.rep("if (z <= b.z){ const f = (z - a.z) / (b.z - a.z); T = a.T + (b.T - a.T) * f; u = a.u + (b.u - a.u) * f; v = a.v + (b.v - a.v) * f; }","if (z <= b.z){ const f = (z - a.z) / (b.z - a.z); T = a.T + (b.T - a.T) * f; u = a.u + (b.u - a.u) * f; v = a.v + (b.v - a.v) * f; c = (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f; }")
f.rep("    tab[k] = {T, p: 0, u, v};","    tab[k] = {T, p: 0, u, v, c};")
f.rep("  for (let k = ks - 1; k >= 0; k--) tab[k].p = hyd(tab[k + 1].p, -DZ, tab[k + 1].T, tab[k].T);\n  return tab;","  for (let k = ks - 1; k >= 0; k--) tab[k].p = hyd(tab[k + 1].p, -DZ, tab[k + 1].T, tab[k].T);\n  tab.rain = hr.rain || 0;\n  return tab;")
f.rep("const lerpTab = (A, B, f) => A.map((a, k) => { const b = B[k]; return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f}; });",
"function lerpTab(A, B, f){\n  const r = A.map((a, k) => { const b = B[k]; return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f, c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f}; });\n  r.rain = (A.rain || 0) + ((B.rain || 0) - (A.rain || 0)) * f; r.t0 = A.t0; r.lat = A.lat; r.lon = A.lon;\n  return r;\n}")
# ================= Oberfläche =================
f.rep("    const r = await fetch(wxUrl(lat, lon), {signal: ac.signal}); clearTimeout(to);\n    if (!r.ok) throw new Error('http ' + r.status);","    let r = await fetch(wxUrl(lat, lon), {signal: ac.signal});\n    if (!r.ok && r.status >= 400 && r.status < 500) r = await fetch(wxUrl(lat, lon, true), {signal: ac.signal});   // erweiterte Abfrage abgelehnt: ohne Wolken und Regen\n    clearTimeout(to);\n    if (!r.ok) throw new Error('http ' + r.status);")
f.rep("ATM = wxTabAt(WX, WXRUN.clock0, WXRUN.zref); }","ATM = wxTabAt(WX, WXRUN.clock0, WXRUN.zref); atmStamp(); }")
f.rep("function wxStart(){","// Zeit und Ort für den Sonnenstand: mit echtem Wetter die jetzige Uhrzeit am Startplatz, in der Simulation ein Sommermorgen\nfunction atmStamp(){ ATM.lat = START.lat; ATM.lon = START.lon; ATM.t0 = WX ? WXRUN.clock0 : simT0(START.lon); }\nfunction wxStart(){")
f.rep("1 - Math.pow(0.9, steps));       // rund 10 Spielminuten Angleichzeit","1 - Math.pow(0.9, steps)); atmStamp();       // rund 10 Spielminuten Angleichzeit")
f.rep("function newSim(k){ SIM_ATM = buildAtm(randomWx(Math.random, k === 'mid')); ATM = SIM_ATM; }","function newSim(k){ SIM_ATM = buildAtm(randomWx(Math.random, k === 'mid')); ATM = SIM_ATM; atmStamp(); }")
# Anzeige
f.rep('        <div class="kv gasaid" hidden><span>m³</span><b id="i-gas">–</b></div>','        <div class="kv"><span id="i-skyl">☀</span><b id="i-sky">–</b></div>\n        <div class="kv" id="row-wet" hidden><span data-i="wet">Wasser</span><b id="i-wet">–</b></div>\n        <div class="kv gasaid" hidden><span>m³</span><b id="i-gas">–</b></div>')
f.rep("  $('i-time').textContent = fmtT(B.t); $('i-dist').textContent = fmtD(B.dist);","""  $('i-time').textContent = fmtT(B.t); $('i-dist').textContent = fmtD(B.dist);
  { const e = radEnv(B, ATM), el = Math.asin(Math.max(-1, Math.min(1, e.s))) * 180 / Math.PI;      // Himmel: Sonne mit Höhe in Grad, Nacht, Wolken darüber, Regen
    $('i-skyl').textContent = e.rain > 0 ? '☂' : e.cu > 0.5 ? '☁' : el > 0 ? '☀' : '☾';
    $('i-sky').textContent = e.rain > 0 ? nf(e.rain, 1) + ' mm/h' : el > 0 ? nf(Math.round(el)) + '°' : tr('night');
    $('row-wet').hidden = !(B.wet > 0.5); $('i-wet').textContent = '+' + nf(B.wet || 0, 1) + ' kg';
    if (STATE === 'play' && !!B.rainSeen !== (e.rain > 0)){ B.rainSeen = e.rain > 0; if (e.rain > 0) toast(tr('rain_on')); } }""")
# Vertikalprofil: Wolken und Regen
f.rep("  // Wind\n  let stepW = 250;","""  // Wolken: heller Streifen rechts neben der Schichtung, je dichter desto heller; darunter Regen als Punkte
  { const ci = cloudInfo(ATM), x0 = xS + 5;
    for (let z = Math.max(0, zb); z < top; z += 50){ const cc = atmAt(ATM, z + 25).c || 0; if (cc > 0.08){ c.fillStyle = 'rgba(238,243,250,' + (0.15 + 0.75 * cc).toFixed(2) + ')'; c.fillRect(x0, y(z + 50), 4, y(z) - y(z + 50) + .5); } }
    if ((ATM.rain || 0) > 0.05){ c.fillStyle = '#4cc9ff'; for (let z = Math.max(0, zb) + 30; z < Math.min(top, ci.rainTop); z += Math.max(60, (top - zb) / 28)) c.fillRect(x0 + 1.2, y(z), 1.6, 3); } }
  // Wind
  let stepW = 250;""")
f.rep('<span data-i="lg_acc"></span></p>','<span data-i="lg_acc"></span></p>\n    <p class="note lg"><i style="background:#eef3fa;width:5px;height:16px;margin:0 5px"></i><span data-i="lg_cloud"></span></p>')
f.rep(" : tr('sw_wx_sim')) + ' ' + tr('sw_wx_val',"," : tr('sw_wx_sim')) + ' ' + (WX ? tr('sw_sky', {c: nf(Math.round(100 * cloudInfo(ATM).up[0])), r: nf(ATM.rain || 0, 1)}) + ' ' : '') + tr('sw_wx_val',")
SIMTXT={'Simuliert.':'Simuliert: Sommermorgen, wolkenlos, ohne Regen.','Simulated.':'Simulated: summer morning, no clouds, no rain.','Simulée.':'Simulée : matin d’été, sans nuages ni pluie.','Symulowana.':'Symulowana: letni poranek, bez chmur i deszczu.','Simulované.':'Simulované: letní ráno, bez mraků a deště.','模擬天氣。':'模擬天氣：夏日清晨，無雲無雨。','Simulado.':'Simulado: mañana de verano, sin nubes ni lluvia.'}
for a,b in SIMTXT.items(): f.rep("sw_wx_sim:'"+a+"'","sw_wx_sim:'"+b+"'")
T={'de':("wet:'Wasser'","night:'Nacht'","rain_on:'Es regnet: Wasser auf der Hülle macht den Ballon schwerer'","sw_sky:'Bewölkung {c} %, Niederschlag {r} mm/h.'","lg_cloud:'Heller Streifen: Wolken, je heller, desto dichter; blaue Punkte darunter: Regen. In der Anzeige: ☀ Sonnenhöhe, ☾ Nacht, ☁ Wolken über dem Ballon, ☂ Regen'"),
 'en':("wet:'Water'","night:'Night'","rain_on:'It is raining: water on the envelope makes the balloon heavier'","sw_sky:'Cloud cover {c} %, precipitation {r} mm/h.'","lg_cloud:'Light strip: clouds, the lighter the denser; blue dots below: rain. In the display: ☀ sun elevation, ☾ night, ☁ clouds above the balloon, ☂ rain'"),
 'fr':("wet:'Eau'","night:'Nuit'","rain_on:'Il pleut : l’eau sur l’enveloppe alourdit le ballon'","sw_sky:'Nébulosité {c} %, précipitations {r} mm/h.'","lg_cloud:'Bande claire : nuages, plus elle est claire, plus ils sont denses ; points bleus en dessous : pluie. Dans l’affichage : ☀ hauteur du soleil, ☾ nuit, ☁ nuages au-dessus du ballon, ☂ pluie'"),
 'pl':("wet:'Woda'","night:'Noc'","rain_on:'Pada deszcz: woda na powłoce obciąża balon'","sw_sky:'Zachmurzenie {c} %, opad {r} mm/h.'","lg_cloud:'Jasny pasek: chmury, im jaśniejszy, tym gęstsze; niebieskie kropki poniżej: deszcz. Na wskaźniku: ☀ wysokość słońca, ☾ noc, ☁ chmury nad balonem, ☂ deszcz'"),
 'cs':("wet:'Voda'","night:'Noc'","rain_on:'Prší: voda na obalu balon zatěžuje'","sw_sky:'Oblačnost {c} %, srážky {r} mm/h.'","lg_cloud:'Světlý pruh: oblaka, čím světlejší, tím hustší; modré tečky pod ním: déšť. Na ukazateli: ☀ výška slunce, ☾ noc, ☁ oblaka nad balonem, ☂ déšť'"),
 'zh-TW':("wet:'積水'","night:'夜間'","rain_on:'下雨了：球囊上的雨水讓氣球變重'","sw_sky:'雲量 {c} %，降水 {r} 毫米/小時。'","lg_cloud:'亮色長條：雲，越亮越厚；下方藍點：雨。顯示欄：☀ 太陽高度、☾ 夜間、☁ 氣球上方有雲、☂ 下雨'"),
 'es':("wet:'Agua'","night:'Noche'","rain_on:'Llueve: el agua sobre la envoltura hace más pesado el globo'","sw_sky:'Nubosidad {c} %, precipitación {r} mm/h.'","lg_cloud:'Franja clara: nubes, cuanto más clara, más densas; puntos azules debajo: lluvia. En el indicador: ☀ altura del sol, ☾ noche, ☁ nubes sobre el globo, ☂ lluvia'")}
order=['de','en','fr','pl','cs','zh-TW','es']; it=iter(order); n=[0]
def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[next(it)])+m.group(2)
f.s=re.sub(r"(upd_later:'[^']*')( \})",r,f.s); assert n[0]==7,n
f.rep("const BUILD = '2026-10-09.2';","const BUILD = '2026-10-09.3';")
# Kern-Export für die Tests erweitern
f.save()
