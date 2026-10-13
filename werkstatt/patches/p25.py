import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. Fallgeräusch des Säckchens ----------
f.rep("    drag(x){  // Schlepptau schleift über den Boden","""    fall(x){  // Säckchen im Fall: Pfeifton, der mit der Resthöhe (1 oben, 0 am Boden) tiefer wird; x < 0 schaltet ab
      if (x < 0 || !UI.sound){ if (fallS){ const s = fallS; fallS = null; s.g.gain.setTargetAtTime(0, ctx.currentTime, 0.03); setTimeout(() => { try{ s.o.stop(); s.l.stop(); }catch(e){} }, 300); } return; }
      const c = ensure(); if (!c) return;
      if (!fallS){
        const o = c.createOscillator(), l = c.createOscillator(), lg = c.createGain(), g = c.createGain();
        o.type = 'sine'; l.frequency.value = 9; lg.gain.value = 14; l.connect(lg); lg.connect(o.frequency);       // leichtes Flattern
        g.gain.value = 0; o.connect(g); g.connect(master); o.start(); l.start(); fallS = {o, l, g};
      }
      fallS.o.frequency.setTargetAtTime(620 + 1100 * Math.max(0, Math.min(1, x)), c.currentTime, 0.05);
      fallS.g.gain.setTargetAtTime(0.05, c.currentTime, 0.05);
    },
    thud(){   // Säckchen schlägt auf
      noise({f0: 380, f1: 90, dur: 0.16, peak: 0.26});
      tone({f0: 150, f1: 70, dur: 0.14, peak: 0.14});
    },
    drag(x){  // Schlepptau schleift über den Boden""")
f.rep("  let drag = null;\n  return {\n    music,","  let drag = null, fallS = null;\n  return {\n    music,")
f.rep("    if (m.done){ const r = markerLand(m); if (!all){ SND.marker(); toast(","    if (m.done){ const r = markerLand(m); if (!all){ SND.thud(); toast(")
f.rep("  FLY = FLY.filter(m => !m.done);","  FLY = FLY.filter(m => !m.done);\n  SND.fall(FLY.length && !all ? Math.min(...FLY.map(m => m.z / Math.max(1, m.z0))) : -1);        // solange ein Säckchen fällt, pfeift es")
f.rep("  FLY.push({e: B.e, n: B.n, z: B.h, col, mk}); SND.marker();","  FLY.push({e: B.e, n: B.n, z: B.h, z0: B.h - B.gnd, col, mk}); SND.marker();")
f.rep("if (s !== 'play'){ SND.valve(0); SND.drag(0);","if (s !== 'play'){ SND.valve(0); SND.drag(0); SND.fall(-1);")
f.rep("  $('paused').hidden = !PAUSED;","  if (PAUSED) SND.fall(-1);\n  $('paused').hidden = !PAUSED;")
# ---------- 2. Wetterpaket für die Meisterschaft ----------
f.rep('<button class="sm" id="inst-set" data-i="inst_set" hidden></button></p>','<button class="sm" id="inst-set" data-i="inst_set" hidden></button></p>\n    <p class="note"><button class="sm" id="wxp-btn" data-i="wxp_btn"></button> <span id="wxp-info"></span></p>')
f.rep("/* ---------- Zeitschleife ---------- */","""/* ---------- Wetterpaket für die Meisterschaft (MEI-12) ----------
   Lädt die archivierte Vorhersage des Renntages für ein Raster über Nord- und Osteuropa und speichert sie als eine Datei. Daraus lassen sich
   die Vorschau-Routen rechnen; später kann das Paket allen Spielern als Wetter dienen. Aufbau der Datei gb69-wetter.bin:
   6 Zeichen „GBWX1“ und Zeilenende, Länge des Kopfes als 32-Bit-Zahl, Kopf als JSON (Raster, Zeiten, Flächen, Felder, Maßstäbe), auf gerade
   Länge aufgefüllt, dann 16-Bit-Zahlen: je Ort (Breite außen, Länge innen), je Stunde, je Fläche die Felder Höhe m, Temperatur 0,1 °C,
   Wind Ost und Nord 0,1 m/s, Bedeckung %; danach je Stunde Bodendruck minus 1000 hPa in 0,1 hPa, Niederschlag 0,1 mm, Gesamtbedeckung %.
   Fehlende Werte sind −32768. Ist die Datei mit gzip gepackt, endet ihr Name auf .gz. */
const WXPACK = (() => {
  const LV = [1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300], lats = [], lons = [];
  for (let a = 47; a <= 63; a += 1) lats.push(a); for (let o = 2; o <= 33.5; o += 1.5) lons.push(o);
  const D0 = '2026-08-29', D1 = '2026-08-31', NT = 72, REC = (LV.length + 1) * 5 + 3, BATCH = 20;
  let running = false, stop = false;
  const url = pts => {
    const h = ['temperature_2m', 'wind_speed_10m', 'wind_direction_10m', 'surface_pressure', 'precipitation', 'cloud_cover'];
    LV.forEach(L => ['temperature', 'wind_speed', 'wind_direction', 'geopotential_height', 'cloud_cover'].forEach(v => h.push(v + '_' + L + 'hPa')));
    return 'https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=' + pts.map(p => p[0]).join(',') + '&longitude=' + pts.map(p => p[1]).join(',') + '&hourly=' + h.join(',') + '&wind_speed_unit=ms&timezone=UTC&start_date=' + D0 + '&end_date=' + D1;
  };
  const i16 = (x, s) => x == null || !isFinite(x) ? -32768 : Math.max(-32767, Math.min(32767, Math.round(x * s)));
  function pack(j, out, off){
    const H = j.hourly; if (!H || !H.time || H.time.length < NT || H.time[0].slice(0, 10) !== D0) throw new Error('Zeitachse');
    const g = (n, k) => H[n] && H[n][k] != null ? +H[n][k] : null, wind = (sp, d) => sp == null || d == null ? [null, null] : windUV(sp, d);
    for (let k = 0; k < NT; k++){
      let o = off + k * REC; const w0 = wind(g('wind_speed_10m', k), g('wind_direction_10m', k));
      out[o++] = i16(+j.elevation, 1); out[o++] = i16(g('temperature_2m', k), 10); out[o++] = i16(w0[0], 10); out[o++] = i16(w0[1], 10); out[o++] = 0;
      for (const L of LV){ const w = wind(g('wind_speed_' + L + 'hPa', k), g('wind_direction_' + L + 'hPa', k));
        out[o++] = i16(g('geopotential_height_' + L + 'hPa', k), 1); out[o++] = i16(g('temperature_' + L + 'hPa', k), 10); out[o++] = i16(w[0], 10); out[o++] = i16(w[1], 10); out[o++] = i16(g('cloud_cover_' + L + 'hPa', k), 1); }
      const p0 = g('surface_pressure', k); out[o++] = i16(p0 == null ? null : p0 - 1000, 10); out[o++] = i16(g('precipitation', k), 10); out[o++] = i16(g('cloud_cover', k), 1);
    }
  }
  const info = t => { $('wxp-info').textContent = t || ''; };
  async function make(){
    const pts = []; lats.forEach(a => lons.forEach(o => pts.push([a, o])));
    const out = new Int16Array(pts.length * NT * REC).fill(-32768), nB = Math.ceil(pts.length / BATCH); let gap = 3000;
    for (let b = 0; b < nB; b++){
      const part = pts.slice(b * BATCH, (b + 1) * BATCH); let tries = 0;
      for (;;){
        if (stop) throw new Error('abgebrochen');
        info(tr('wxp_prog', {a: b + 1, b: nB}));
        let j = null, limited = false;
        try{ const r = await fetch(url(part)); limited = r.status === 429; j = await r.json(); if (j && j.error){ limited = limited || /limit/i.test(j.reason || ''); if (!limited) throw new Error(j.reason || 'Dienst'); j = null; } }
        catch(e){ if (!limited && ++tries > 3) throw e; }
        if (j){ const arr = Array.isArray(j) ? j : [j]; if (arr.length !== part.length) throw new Error('Antwort unvollständig'); arr.forEach((x, i) => pack(x, out, (b * BATCH + i) * NT * REC)); break; }
        if (limited){ gap = Math.min(20000, gap * 2); for (let s = 65; s > 0 && !stop; s -= 5){ info(tr('wxp_wait', {s})); await pause(5000); } } else await pause(4000);
      }
      await pause(gap);
    }
    const head = JSON.stringify({v: 1, name: 'gb69', t0: Date.UTC(2026, 7, 29), dtH: 1, nT: NT, lats, lons, levels: ['sfc'].concat(LV), fields: ['z_m', 'T_0.1C', 'u_0.1ms', 'v_0.1ms', 'cloud_pct'],
      extra: ['p0_minus_1000hPa_0.1', 'precip_0.1mm', 'cloud_total_pct'], rec: REC, order: 'point(lat outer, lon inner), hour, level x field, extra', missing: -32768, src: 'Open-Meteo Historical Forecast API (CC BY 4.0)', made: new Date().toISOString(), build: BUILD});
    let hb = new TextEncoder().encode(head); if (hb.length % 2){ const p = new Uint8Array(hb.length + 1); p.set(hb); p[hb.length] = 32; hb = p; }
    const pre = new Uint8Array(10); pre.set(new TextEncoder().encode('GBWX1\\n')); new DataView(pre.buffer).setUint32(6, hb.length, true);
    let blob = new Blob([pre, hb, out.buffer], {type: 'application/octet-stream'}), name = 'gb69-wetter.bin';
    if (window.CompressionStream){ try{ blob = await new Response(blob.stream().pipeThrough(new CompressionStream('gzip'))).blob(); name += '.gz'; }catch(e){} }
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
    return blob.size;
  }
  $('wxp-btn').addEventListener('click', async () => {
    if (running){ stop = true; return; }
    if (!(await confirmBox(tr('wxp_q'), tr('wxp_go')))) return;
    running = true; stop = false; $('wxp-btn').textContent = tr('cancel');
    try{ const n = await make(); info(tr('wxp_done', {mb: nf(n / 1048576, 1)})); }catch(e){ info(tr('wxp_fail', {why: (e && e.message) || '?'})); }
    running = false; $('wxp-btn').textContent = tr('wxp_btn');
  });
  return {lats, lons, LV, REC, NT};
})();

/* ---------- Zeitschleife ---------- */""")
T={'de':("wxp_btn:'Wetterpaket für die Meisterschaft erstellen'","wxp_q:'Lädt das Wetter des Renntages für Nord- und Osteuropa (374 Orte, rund 12 MB, einige Minuten) und speichert es als Datei gb69-wetter. Bitte nur mit WLAN und die App dabei offen lassen. Die Datei wird für die Vorschau-Routen gebraucht.'","wxp_go:'Laden'","wxp_prog:'Wetterpaket: Teil {a} von {b} …'","wxp_wait:'Der Dienst bremst, weiter in {s} s …'","wxp_done:'Wetterpaket gespeichert ({mb} MB). Die Datei liegt bei den Downloads.'","wxp_fail:'Wetterpaket nicht erstellt: {why}'"),
 'en':("wxp_btn:'Create weather package for the championship'","wxp_q:'Loads the weather of the race day for northern and eastern Europe (374 places, about 12 MB, a few minutes) and saves it as the file gb69-wetter. Please use Wi-Fi and keep the app open. The file is needed for the preview routes.'","wxp_go:'Load'","wxp_prog:'Weather package: part {a} of {b} …'","wxp_wait:'The service is throttling, continuing in {s} s …'","wxp_done:'Weather package saved ({mb} MB). The file is in your downloads.'","wxp_fail:'Weather package not created: {why}'")}
for L in ('de','en'):
    n=[0]
    def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[L])+m.group(2)
    key = 'gb_500_a'
    # deutsche und englische Fassung genügen: tr() fällt für die übrigen Sprachen auf Englisch zurück
    pat = r"(gb_500_a:'Zeitraffer 500×, solange gedrückt')( \})" if L=='de' else r"(gb_500_a:'Time lapse 500× while held')( \})"
    f.s=re.sub(pat,r,f.s); assert n[0]==1,(L,n)
f.rep("const BUILD = '2026-10-09.4';","const BUILD = '2026-10-09.5';")
f.save()
