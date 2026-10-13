import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add,tx_set
f=F()
# ============ Musik: auf dem Handy nicht zu hören (zu tief, zu leise) ============
f.rep("const CALM = {bar: 4, vol: 0.11,","const CALM = {bar: 4, vol: 0.34, up: 12,   // up: eine Oktave höher, denn Handy-Lautsprecher geben unter rund 300 Hz kaum etwas wieder")
f.rep("o.type = 'triangle'; o2.type = 'sine'; o.frequency.value = mf(n); o2.frequency.value = mf(n) * 1.003; lp.type = 'lowpass'; lp.frequency.value = 900;","o.type = 'triangle'; o2.type = 'triangle'; o.frequency.value = mf(n + CALM.up); o2.frequency.value = mf(n + CALM.up + 12) * 1.003; lp.type = 'lowpass'; lp.frequency.value = 1700;")
f.rep("CALM.chords[k].forEach((n, j) => mPad(n, t, CALM.bar, j === 0 ? 0.20 : 0.11));","CALM.chords[k].forEach((n, j) => mPad(n, t, CALM.bar, j === 0 ? 0.20 : 0.13));")
f.rep("if (n) mBell(n, t + j * CALM.bar / 4 + 0.02, 0.10); });","if (n) mBell(n, t + j * CALM.bar / 4 + 0.02, 0.20); });")
# ============ GPS: 15 s ============
f.rep("const GPS_AVG = 10; ","const GPS_AVG = 15; ")
# ============ Startseite: Sand fällt nur bis zum Boden; Installationslink; Rollhinweis; kompakter ============
f.rep("c.fillStyle = '#ffe14d'; sand.forEach(p => c.fillRect(bx - bw / 2 - 3 + p.x, yb + 40 * p.t + 30 * p.t * p.t, 2, 2));","c.fillStyle = '#ffe14d'; sand.forEach(p => c.fillRect(bx - bw / 2 - 3 + p.x, Math.min(gB - 2, yb + 40 * p.t + 30 * p.t * p.t), 2, 2));   // der Sand fällt nur bis zum Boden")
f.rep("Buy me a Beer</button>\n      </div>","Buy me a Beer</button>\n        <button class=\"mbeer\" id=\"m-inst\" hidden data-i=\"inst_t\"></button>\n      </div>")
f.rep("    $('install').hidden = !on; $('inst-set').hidden = !possible();","    $('install').hidden = !on; $('inst-set').hidden = !possible(); $('m-inst').hidden = !possible() || on;")
f.rep("  $('inst-set').addEventListener('click', () => { forced = true; steps = !ev; openSheet(false); show(); });","  $('inst-set').addEventListener('click', () => { forced = true; steps = !ev; openSheet(false); show(); });\n  $('m-inst').addEventListener('click', () => { forced = true; steps = !ev; show(); });")
f.rep("#hero{flex:none;display:block;width:100%;height:clamp(120px,25%,280px);","#hero{flex:none;display:block;width:100%;height:clamp(110px,22%,260px);")
f.rep("/* Tutorial (SPI-18) */","""/* Rollhinweis (NFA-07): Wo ein Fenster nach unten weitergeht, liegt am unteren Rand ein Pfeil */
.shint{position:sticky;bottom:0;height:0;pointer-events:none;display:none;z-index:5}
.more > .shint{display:block}
.shint i{position:absolute;left:-14px;right:-14px;bottom:-12px;height:44px;display:grid;place-items:end center;padding-bottom:5px;background:linear-gradient(rgba(10,16,25,0),rgba(10,16,25,.96) 62%)}
.shint svg{animation:shint 1.3s ease-in-out infinite}
@keyframes shint{0%,100%{transform:translateY(-3px)}50%{transform:translateY(3px)}}
@media (prefers-reduced-motion:reduce){.shint svg{animation:none}}
/* Tutorial (SPI-18) */""")
f.rep("/* ---------- Zeitschleife ---------- */","""/* ---------- Rollhinweis (NFA-07) ---------- */
const SHINT = [];
function scrollHint(el){ if (!el) return; const d = document.createElement('div'); d.className = 'shint'; d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<i><svg width="26" height="16" viewBox="0 0 26 16"><path d="M3 3l10 9 10-9" fill="none" stroke="#ff9f1c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></i>'; el.appendChild(d); SHINT.push(el); el.addEventListener('scroll', shintUpd, {passive: true}); }
function shintUpd(){ SHINT.forEach(el => el.classList.toggle('more', el.scrollHeight - el.clientHeight - el.scrollTop > 10)); }
['.mcard', '#sheet', '#startwin .card', '#setup .card', '#info .card', '#chal .card', '#detail .card'].forEach(q => scrollHint(document.querySelector(q)));
setInterval(shintUpd, 500); window.addEventListener('resize', shintUpd);

/* ---------- Zeitschleife ---------- */""")
# ============ Seitenansicht: solange sie sichtbar ist, folgt die Karte dem Ballon ============
f.rep("  if (!on){ SIDE.sand.length = 0; SIDE.puff.length = 0; return; }","  if (!on){ SIDE.sand.length = 0; SIDE.puff.length = 0; return; }\n  if (!follow || !$('follow').hidden){ follow = true; $('follow').hidden = true; }                          // der Knopf „Ballon folgen“ läge sonst über der Seitenansicht")
# ============ Vertikalprofil bleibt fest; darunter der Knopf für den Temp ============
f.rep("#prof{left:0;top:0;width:96px;height:62%;padding:0;overflow:hidden;border-left:0;border-top:0;border-radius:0 0 14px 0;cursor:pointer}\n#prof.big{width:150px;height:auto;bottom:0;border-radius:0}\n#prof canvas{display:block;width:100%;height:100%}",
"#prof{left:0;top:0;width:96px;height:62%;padding:0;overflow:hidden;border-left:0;border-top:0;border-radius:0 0 14px 0;display:flex;flex-direction:column}\n#prof canvas{display:block;width:100%;flex:1;min-height:0}\n#temp-btn{flex:none;height:34px;border:0;border-top:1px solid var(--line);background:var(--pan2);color:var(--tx);font-family:var(--num);font-size:15px;font-weight:600;letter-spacing:.02em}\n#temp-btn.on{background:var(--orb);color:#1a1000}")
f.rep('<canvas id="prof-cv" role="img" data-ia="prof_hint" aria-label="Vertikalprofil"></canvas></div>','<canvas id="prof-cv" role="img" data-ia="prof_hint" aria-label="Vertikalprofil"></canvas><button id="temp-btn" aria-pressed="false" data-i="temp_btn"></button></div>')
f.rep("$('prof').addEventListener('click', () => $('prof').classList.toggle('big'));\n","")
a=f.s.index("$('prof').addEventListener('click', e => { const r = $('prof').getBoundingClientRect();"); b=f.s.index("\n",a); f.s=f.s[:a]+"function tempShow(on){ $('stuve').hidden = !on; $('temp-btn').classList.toggle('on', on); $('temp-btn').setAttribute('aria-pressed', on ? 'true' : 'false'); if (on) stuveDraw(); }\n$('temp-btn').addEventListener('click', () => tempShow($('stuve').hidden));"+f.s[b:]
f.rep("$('stuve').addEventListener('click', () => { $('stuve').hidden = true; });","$('stuve').addEventListener('click', () => tempShow(false));")
f.rep("#stuve{z-index:886;cursor:pointer}","#stuve{z-index:886;cursor:pointer;place-items:center end;padding-left:100px}")
tx_set(f,'prof_hint',['Vertikalprofil: Wind und Temperatur über der Höhe','Vertical profile: wind and temperature against height','Profil vertical : vent et température selon la hauteur','Profil pionowy: wiatr i temperatura w funkcji wysokości','Vertikální profil: vítr a teplota podle výšky','垂直剖面：各高度的風與溫度','Perfil vertical: viento y temperatura según la altura'])
tx_set(f,'st_title',['Temp (Skew-T)','Sounding (skew-T)','Émagramme (skew-T)','Sondaż (skew-T)','Výstup (skew-T)','探空圖（斜溫圖）','Sondeo (skew-T)'])
tx_set(f,'st_note',['Rot: Temperatur. Blau: Taupunkt (nur mit echtem Wetter). Orange: Trockenadiabaten. Grün: Feuchtadiabaten. Blaue schräge Linien: Isothermen. Hellblaues Band: Inversion. Weißer Strich: Wolken. Oranger Punkt: Ballon, gelbe Raute: Gas. Antippen schließt.','Red: temperature. Blue: dew point (real weather only). Orange: dry adiabats. Green: moist adiabats. Blue slanted lines: isotherms. Light blue band: inversion. White line: cloud. Orange dot: balloon, yellow diamond: gas. Tap to close.','Rouge : température. Bleu : point de rosée (météo réelle seulement). Orange : adiabatiques sèches. Vert : adiabatiques humides. Lignes bleues inclinées : isothermes. Bande bleu clair : inversion. Trait blanc : nuages. Point orange : ballon, losange jaune : gaz. Touchez pour fermer.','Czerwona: temperatura. Niebieska: punkt rosy (tylko prawdziwa pogoda). Pomarańczowe: adiabaty suche. Zielone: adiabaty wilgotne. Niebieskie ukośne: izotermy. Jasnoniebieski pas: inwersja. Biała kreska: chmury. Pomarańczowy punkt: balon, żółty romb: gaz. Dotknij, aby zamknąć.','Červená: teplota. Modrá: rosný bod (jen skutečné počasí). Oranžové: suché adiabaty. Zelené: vlhké adiabaty. Modré šikmé čáry: izotermy. Světle modrý pás: inverze. Bílá čára: oblačnost. Oranžový bod: balon, žlutý kosočtverec: plyn. Klepnutím zavřete.','紅：氣溫。藍：露點（僅真實天氣）。橘：乾絕熱線。綠：濕絕熱線。藍色斜線：等溫線。淺藍帶：逆溫。白線：雲。橘點：氣球，黃菱形：氣體。點一下關閉。','Rojo: temperatura. Azul: punto de rocío (solo tiempo real). Naranja: adiabáticas secas. Verde: adiabáticas húmedas. Líneas azules inclinadas: isotermas. Banda azul claro: inversión. Línea blanca: nubes. Punto naranja: globo, rombo amarillo: gas. Toca para cerrar.'])
tx_add(f,{'temp_btn':['Temp','Temp','Émagr.','Temp','Temp','探空圖','Temp'],
 'st_cloud':['Wolken ab {a} m','Cloud from {a} m','Nuages dès {a} m','Chmury od {a} m','Oblačnost od {a} m','雲底 {a} m','Nubes desde {a} m'],
 'st_ctop':['bis {a} m','to {a} m','jusqu’à {a} m','do {a} m','do {a} m','至 {a} m','hasta {a} m']})
# ---- Wetter: relative Feuchte je Druckfläche für den Taupunkt (nur in der erweiterten Abfrage) ----
f.rep("  if (!lite) h.push('precipitation', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high');\n  WX_LEVELS.forEach(L => ['temperature', 'wind_speed', 'wind_direction', 'geopotential_height'].concat(lite ? [] : ['cloud_cover']).forEach(v => h.push(v + '_' + L + 'hPa')));",
      "  if (!lite) h.push('precipitation', 'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high', 'relative_humidity_2m');\n  WX_LEVELS.forEach(L => ['temperature', 'wind_speed', 'wind_direction', 'geopotential_height'].concat(lite ? [] : ['cloud_cover', 'relative_humidity']).forEach(v => h.push(v + '_' + L + 'hPa')));")
f.rep("const windUV = (spd, dir) =>","const dewK = (Tc, rh) => { if (rh == null || !(rh > 0)) return null; const g = Math.log(Math.min(100, rh) / 100) + 17.625 * Tc / (243.04 + Tc); return 243.04 * g / (17.625 - g) + 273.15; };   // Taupunkt nach Magnus\nconst windUV = (spd, dir) =>")
f.rep("pts.push({z: elev, T: g('temperature_2m') + 273.15, u: uv0[0], v: uv0[1]});","pts.push({z: elev, T: g('temperature_2m') + 273.15, u: uv0[0], v: uv0[1], d: dewK(g('temperature_2m'), g('relative_humidity_2m'))});")
f.rep("pts.push({z, T: T + 273.15, u: uv[0], v: uv[1], pl: L * 100, c: cc == null ? lay(z) : cc / 100}); }","pts.push({z, T: T + 273.15, u: uv[0], v: uv[1], pl: L * 100, c: cc == null ? lay(z) : cc / 100, d: dewK(T, g('relative_humidity_' + L + 'hPa'))}); }")
f.rep("    const z = zref + k * DZ; let T, u, v, c = 0;\n    if (z <= P[0].z){ T = P[0].T + 0.0065 * (P[0].z - z); u = P[0].u; v = P[0].v; }","    const z = zref + k * DZ; let T, u, v, c = 0, d = null;\n    if (z <= P[0].z){ T = P[0].T + 0.0065 * (P[0].z - z); u = P[0].u; v = P[0].v; d = P[0].d == null ? null : P[0].d + 0.0018 * (P[0].z - z); }")
f.rep("c = (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f; }\n      else { T = Math.max(216.65, b.T - 0.0065 * (z - b.z)); u = b.u; v = b.v; }","c = (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f; d = a.d == null || b.d == null ? null : a.d + (b.d - a.d) * f; }\n      else { T = Math.max(216.65, b.T - 0.0065 * (z - b.z)); u = b.u; v = b.v; }")
f.rep("    tab[k] = {T, p: 0, u, v, c};","    tab[k] = {T, p: 0, u, v, c, d};")
f.rep("u: a.u, v: a.v, c: a.c || 0};\n  }","u: a.u, v: a.v, c: a.c || 0, d: a.d == null ? null : a.d};\n  }")
f.rep("  return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f, c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f};","  return {T: a.T + (b.T - a.T) * f, p: a.p + (b.p - a.p) * f, u: a.u + (b.u - a.u) * f, v: a.v + (b.v - a.v) * f, c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f, d: a.d == null || b.d == null ? null : a.d + (b.d - a.d) * f};")
f.rep("c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f}; });\n  r.rain =","c: (a.c || 0) + ((b.c || 0) - (a.c || 0)) * f, d: a.d == null || b.d == null ? null : a.d + (b.d - a.d) * f}; });\n  r.rain =")
# ---- Diagramm neu: Skew-T wie im Temp des Wetterdienstes ----
a=f.s.index("/* ---------- Temp als Stüve-Diagramm (STE-27)"); b=f.s.index("function tempShow(on){")
f.s=f.s[:a]+r'''/* ---------- Temp als Skew-T-Diagramm (STE-27), wie beim Wetterdienst: Druck logarithmisch nach oben, Isothermen schräg nach rechts oben,
   Trockenadiabaten orange, Feuchtadiabaten grün, Sättigungsmischungsverhältnis gepunktet. Temperatur rot, Taupunkt blau (nur mit echtem Wetter).
   Inversionen als Band, Wolken als Strich mit Schrift, Windfahnen wie im Vertikalprofil. ---------- */
function stuveDraw(){
  const cv = $('stuve-cv'), W = cv.clientWidth, H = cv.clientHeight; if (!W || !H) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 3); if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
  const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  const num = '600 12px "Barlow Condensed","Arial Narrow",sans-serif', small = '500 11px Barlow,"Segoe UI",sans-serif';
  const zb = Math.min(0, B.gnd), zTop = ZTOP - DZ, a0 = atmAt(ATM, zb), pB = Math.ceil((a0.p / 100 + 4) / 10) * 10, pT = Math.max(280, Math.floor(atmAt(ATM, zTop).p / 100 / 10) * 10);
  const L = 36, R = W - 62, Tp = 24, Bm = H - 24, y = p => Bm - Math.log(pB / p) / Math.log(pB / pT) * (Bm - Tp);
  const Ts = a0.T - 273.15, tR = Math.ceil((Ts + 12) / 10) * 10, tL = tR - 60, SK = 0.62 * (R - L) / (Bm - Tp), x = (t, p) => L + (t - tL) / (tR - tL) * (R - L) + SK * (Bm - y(p));
  const poly = (pts, col, w, dash) => { c.strokeStyle = col; c.lineWidth = w; c.setLineDash(dash || []); c.beginPath(); pts.forEach((q, i) => i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1])); c.stroke(); c.setLineDash([]); };
  c.save(); c.beginPath(); c.rect(L, Tp, R - L, Bm - Tp); c.clip();
  for (let t = -130; t <= 50; t += 10) poly([[x(t, pB), Bm], [x(t, pT), Tp]], t === 0 ? 'rgba(76,201,255,.75)' : 'rgba(76,201,255,.3)', 1);                                   // Isothermen
  for (let th = -30; th <= 180; th += 10){ const q = []; for (let p = pB; p >= pT - 1; p -= 20) q.push([x((th + 273.15) * Math.pow(p / 1000, 0.286) - 273.15, p), y(p)]); poly(q, 'rgba(255,159,28,.42)', 1); }   // Trockenadiabaten
  const es = T => 6.112 * Math.exp(17.67 * (T - 273.15) / (T - 29.65));
  for (let t0 = -16; t0 <= 36; t0 += 4){ const q = []; let T = t0 + 273.15, p = 1000;                                                      // Feuchtadiabaten ab 1000 hPa
    const step = dp => { const rs = 0.622 * es(T) / (p - es(T)); T += dp * (287 * T + 2.5e6 * rs) / (p * (1004 + 2.5e6 * 2.5e6 * rs * 0.622 / (287 * T * T))); p += dp; };
    while (p < pB) step(5); q.push([x(T - 273.15, p), y(p)]); T = t0 + 273.15; p = 1000; const lo = [q[0]];
    while (p > pT){ step(-5); if (p <= pB) lo.push([x(T - 273.15, p), y(p)]); } poly(lo, 'rgba(95,227,161,.38)', 1); }
  for (const r of [1, 2, 4, 7, 10, 16]){ const q = []; for (let p = pB; p >= 600; p -= 50){ const e = r / 1000 * p / (0.622 + r / 1000), g = Math.log(e / 6.112); q.push([x(243.5 * g / (17.67 - g), p), y(p)]); } poly(q, 'rgba(255,122,217,.5)', 1, [2, 4]); }   // Mischungsverhältnis g/kg
  // Inversionen als Band
  { let z0 = -1; for (let z = zb; z <= zTop; z += 50){ const inv = z < zTop && atmAt(ATM, z + 50).T - atmAt(ATM, z).T > 0.025; if (inv && z0 < 0) z0 = z; if (!inv && z0 >= 0){ const ya = y(atmAt(ATM, z0).p / 100), yb2 = y(atmAt(ATM, z).p / 100); c.fillStyle = 'rgba(76,201,255,.2)'; c.fillRect(L, yb2, R - L, Math.max(2, ya - yb2)); c.fillStyle = '#9fdcff'; c.font = small; c.textAlign = 'left'; c.textBaseline = 'bottom'; c.fillText(tr('inv') + ' ' + nf(Math.round(z0 - B.gnd > 0 ? z0 : z0)) + '–' + nf(z) + ' m', L + 5, yb2 - 1); z0 = -1; } } }
  c.restore();
  c.font = num; c.textBaseline = 'middle';
  for (const p of [1000, 925, 850, 700, 600, 500, 400, 300]){ if (p > pB || p < pT) continue; c.strokeStyle = 'rgba(238,243,250,.3)'; c.lineWidth = 1; c.beginPath(); c.moveTo(L, y(p) + .5); c.lineTo(R, y(p) + .5); c.stroke(); c.fillStyle = '#9aabc4'; c.textAlign = 'right'; c.fillText(p, L - 4, y(p)); }
  c.textBaseline = 'alphabetic'; c.textAlign = 'center'; for (let t = tL; t <= tR; t += 10){ c.fillStyle = t === 0 ? '#4cc9ff' : '#9aabc4'; c.fillText(t + '°', x(t, pB), Bm + 14); }
  c.strokeStyle = '#28395a'; c.strokeRect(L, Tp, R - L, Bm - Tp);
  c.font = small; c.fillStyle = '#9aabc4'; c.textAlign = 'left'; c.fillText('hPa', 3, 14); c.textAlign = 'center'; c.fillText(tr('st_title'), (L + R) / 2, 14); c.textAlign = 'right'; c.fillText('km · ' + UNITS[UI.unit][1], W - 3, 14);
  // Höhe in km über Grund
  c.font = num; c.textAlign = 'left'; c.textBaseline = 'middle';
  for (let z = 0; z <= zTop; z += 1000){ const p = atmAt(ATM, z).p / 100; if (p < pT) break; c.fillStyle = '#9aabc4'; c.fillText(z / 1000, R + 4, y(p)); c.strokeStyle = 'rgba(154,171,196,.6)'; c.beginPath(); c.moveTo(R - 4, y(p) + .5); c.lineTo(R, y(p) + .5); c.stroke(); }
  // Wolken: Strich an Unter- und Obergrenze mit Schrift
  { let z0 = -1, n = 0; for (let z = Math.max(0, zb); z <= zTop && n < 3; z += 50){ const cl = z < zTop && (atmAt(ATM, z + 25).c || 0) > 0.5; if (cl && z0 < 0) z0 = z; if (!cl && z0 >= 0){ n++; const ya = y(atmAt(ATM, z0).p / 100), yb2 = y(atmAt(ATM, z).p / 100);
      c.strokeStyle = '#eef3fa'; c.lineWidth = 2; c.beginPath(); c.moveTo(L, ya); c.lineTo(R, ya); c.stroke(); c.lineWidth = 1; c.setLineDash([6, 4]); c.beginPath(); c.moveTo(L, yb2); c.lineTo(R, yb2); c.stroke(); c.setLineDash([]);
      c.fillStyle = '#eef3fa'; c.font = small; c.textAlign = 'right'; c.textBaseline = 'top'; c.fillText(tr('st_cloud', {a: nf(z0)}), R - 5, ya + 2); if (ya - yb2 > 26){ c.textBaseline = 'bottom'; c.fillText(tr('st_ctop', {a: nf(z)}), R - 5, yb2 - 1); } z0 = -1; } } }
  // Temperatur und Taupunkt
  c.save(); c.beginPath(); c.rect(L, Tp, R - L, Bm - Tp); c.clip(); c.lineCap = 'round'; c.lineJoin = 'round';
  { const qt = [], qd = []; for (let z = zb; z <= zTop; z += 50){ const a = atmAt(ATM, z), p = a.p / 100; if (p < pT) break; qt.push([x(a.T - 273.15, p), y(p)]); if (a.d != null) qd.push([x(Math.min(a.d, a.T) - 273.15, p), y(p)]); }
    if (qd.length > 3) poly(qd, '#3d7dff', 2.4); poly(qt, '#ff4d3d', 2.8); }
  c.restore();
  // Wind
  for (const p of [1000, 925, 850, 700, 600, 500, 400, 300]){ if (p > pB - 5 || p < pT) continue; let z = 0; for (let q = 0; q <= zTop; q += 50) if (atmAt(ATM, q).p / 100 >= p) z = q; const a = atmAt(ATM, z); drawBarb(c, W - 16, y(p), Math.atan2(-a.u, -a.v), Math.hypot(a.u, a.v) * 1.943844, 17); }
  // Ballon und Gastemperatur
  const ab = atmAt(ATM, B.h), pb = ab.p / 100, yb = y(pb), xa = x(ab.T - 273.15, pb), xg = x(B.Tg - 273.15, pb);
  c.strokeStyle = 'rgba(255,159,28,.85)'; c.lineWidth = 1; c.setLineDash([4, 3]); c.beginPath(); c.moveTo(L, yb); c.lineTo(R, yb); c.stroke(); c.setLineDash([]);
  c.strokeStyle = '#ffe14d'; c.lineWidth = 1.5; c.beginPath(); c.moveTo(xa, yb); c.lineTo(xg, yb); c.stroke();
  c.fillStyle = '#ffe14d'; c.beginPath(); c.moveTo(xg, yb - 6); c.lineTo(xg + 6, yb); c.lineTo(xg, yb + 6); c.lineTo(xg - 6, yb); c.closePath(); c.fill();
  c.fillStyle = '#ff9f1c'; c.strokeStyle = '#0a1019'; c.lineWidth = 2; c.beginPath(); c.arc(xa, yb, 6, 0, 7); c.fill(); c.stroke();
  c.font = small; c.fillStyle = '#eef3fa'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
  c.fillText(nf(Math.round(B.h - B.gnd)) + ' m · ' + nf(ab.T - 273.15, 1) + ' °C' + (ab.d != null ? ' · ' + tr('st_td') + ' ' + nf(ab.d - 273.15, 1) + ' °C' : ''), L + 6, yb > Tp + 40 ? yb - 9 : yb + 18);
}
'''+f.s[b:]
tx_add(f,{'st_td':['Taupunkt','dew point','point de rosée','punkt rosy','rosný bod','露點','punto de rocío']})
# ============ Tutorial ============
f.rep('<button class="sm" id="tut-skip"></button><button class="sm" id="tut-next"></button>','<button class="sm" id="tut-next"></button>')
f.rep("#tut.mid{top:47%}","#tut.mid{top:47%}\n#tut.low{top:auto;bottom:150px;z-index:900}\n#tut-next:disabled{opacity:.38}")
f.rep("  hide: ['box-sacks', 'box-trough', 'box-valve', 'box-rope', 'prof', 'inst', 'seg-speed', 'btn-set', 'corner', 'hint'],","  hide: ['box-sacks', 'box-trough', 'box-valve', 'box-rope', 'prof', 'inst', 'seg-speed', 'btn-set', 'corner', 'hint'], seen: false,")
a=f.s.index("  steps: [{k: 'intro'}"); b=f.s.index("]};",a)+3
f.s=f.s[:a]+"""  steps: [{k: 'intro'}, {k: 'sacks', show: ['box-sacks'], at: 'rack', done: () => B.go}, {k: 'go', ready: () => B.h - B.gnd > 30}, {k: 'inst', show: ['inst'], mid: 1}, {k: 'prof', show: ['prof'], mid: 1},
    {k: 'temp', mid: 1, at: 'temp-btn', done: () => !$('stuve').hidden}, {k: 'temp2', low: 1, done: () => $('stuve').hidden},
    {k: 'scoop', show: ['box-trough'], at: 'scoop', done: () => B.mU < TUT.mU0 || B.sacks < TUT.s0}, {k: 'scoop2'}, {k: 'valve', show: ['box-valve'], at: 'valve', done: () => TUT.vT > 1.6}, {k: 'valve2'},
    {k: 'speed', show: ['seg-speed', 'corner'], at: 'seg-speed'}, {k: 'opts', show: ['btn-set'], at: 'btn-set'}, {k: 'rope', show: ['box-rope'], at: 'rope', done: () => B.rope},
    {k: 'land', at: 'valve', done: () => B.landed || (B.go && !B.air && B.h <= B.gnd + 0.01 && B.free < 0)}, {k: 'done'}]};"""+f.s[b:]
f.rep("$('tut-next').hidden = !!s.done || !!(s.ready && !s.ready());","$('tut-next').disabled = !!s.done || !!(s.ready && !s.ready());")
f.rep("$('tut-skip').textContent = tr('tut_skip'); $('tut-skip').hidden = TUT.i === TUT.steps.length - 1;\n","\n")
f.rep("  $('tut').classList.toggle('mid', !!s.mid);","  $('tut').classList.toggle('mid', !!s.mid); $('tut').classList.toggle('low', !!s.low);")
f.rep("  if (s.ready && $('tut-next').hidden && s.ready()) $('tut-next').hidden = false;","  if (s.ready && $('tut-next').disabled && s.ready()) $('tut-next').disabled = false;")
f.rep("$('tut-next').addEventListener('click', tutNext); $('tut-skip').addEventListener('click', () => tutEnd(false));","$('tut-next').addEventListener('click', () => { if (!$('tut-next').disabled) tutNext(); });")
def tt(lang,key,new,after=None):
    global f
    blk_a=f.s.index(" %s: {intro:"%lang); 
    if key+": '" in f.s[blk_a:blk_a+9000] and after is None:
        a=f.s.index("  %s: '"%key,blk_a); b=f.s.index("',\n",a) if f.s.find("',\n",a)!=-1 else None; f.s=f.s[:a]+"  %s: '%s"%(key,new.replace("'","\\'"))+f.s[b:]
    else:
        a=f.s.index("  %s: '"%after,blk_a); b=f.s.index("',\n",a)+3; f.s=f.s[:b]+"  %s: '%s',\n"%(key,new.replace("'","\\'"))+f.s[b:]
tt('de','go','Die Crew hat losgelassen, der Ballon steigt. Sand abgeben ist der einzige Weg nach oben, und was weg ist, kommt nicht wieder. Weiter geht es, sobald der Ballon 30 m hoch ist.')
tt('en','go','The crew has let go and the balloon climbs. Releasing sand is the only way up, and what is gone does not come back. We continue as soon as the balloon is 30 m up.')
tt('de','temp','Unter dem Profil sitzt der Knopf „Temp“. Er blendet das Diagramm der Meteorologen ein: Temperatur, Taupunkt und Wind über der Höhe. Tippe darauf.',after='prof')
tt('en','temp','Below the profile is the button “Temp”. It shows the meteorologists’ diagram: temperature, dew point and wind against height. Tap it.',after='prof')
tt('de','temp2','Rot ist die Temperatur, blau der Taupunkt (nur mit echtem Wetter). Ein hellblaues Band ist eine Inversion, ein weißer Strich eine Wolkendecke; der orange Punkt bist du. Tippe auf das Diagramm oder noch einmal auf „Temp“, um es auszublenden.',after='temp')
tt('en','temp2','Red is the temperature, blue the dew point (real weather only). A light blue band is an inversion, a white line a cloud layer; the orange dot is you. Tap the diagram or “Temp” again to hide it.',after='temp')
tt('de','valve','Nach unten geht es mit dem Ventil: Es lässt Gas ab. Zieh den Regler nach unten und halte ihn zwei Sekunden. Ziehst du stark, beginnt das Parachute-Ventil oben in der Hülle zu flattern; das hörst du auch. Solange du ziehst, läuft die Zeit 1×.')
tt('en','valve','The valve takes you down: it releases gas. Pull the slider down and hold it for two seconds. If you pull hard, the parachute valve at the top of the envelope starts to flutter; you can hear that too. While you pull, time runs at 1×.')
tt('de','opts','Oben rechts sind die Einstellungen: helle oder dunkle Karte, Lufträume, Einheiten, Ton, die Daten deines Ballons und die Seite „Karten und Daten“. Viele entdecken diesen Knopf erst spät.',after='speed')
tt('en','opts','At the top right are the settings: light or dark map, airspace, units, sound, the data of your balloon and the page “Maps and data”. Many people discover this button late.',after='speed')
tt('de','rope','Das Schlepptau ist 50 m lang. Sinnvoll ist es erst unter 50 m über Grund, kurz vor der Landung: Berührt es den Boden, trägt der Boden einen Teil seines Gewichts, das fängt das Sinken ab und bremst die Fahrt. Zum Üben werfen wir es jetzt schon aus. Es lässt sich nicht wieder einrollen.')
tt('en','rope','The trail rope is 50 m long. It only makes sense below 50 m above ground, shortly before landing: when it touches the ground, the ground carries part of its weight, which stops the sink and slows the balloon. For practice we deploy it now. It cannot be hauled in again.')
f.rep("const BUILD = '2026-10-10.3'","const BUILD = '2026-10-10.4'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v35'" in s; open(p,'w').write(s.replace("'v35'","'v36'"))
