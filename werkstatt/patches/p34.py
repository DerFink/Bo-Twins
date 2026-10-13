import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add,tx_set
f=F()
# ================= Startseite: Seitenansicht statt Retro-Bild =================
f.rep('''      <div class="mscreen">
      <canvas id="c64" aria-hidden="true"></canvas>
      <div class="mcard">''','''      <canvas id="hero" role="img" data-ia="hero_a" aria-label="Gasballon von der Seite"></canvas>
      <div class="mcard">''')
f.rep('''        <p class="mhint" data-i="name_hint"></p>
        <button class="mbtn" id="m-free">''','''        <p class="mhint" data-i="name_hint"></p>
        <button class="mbtn tut" id="m-tut"><b data-i="m_tut"></b><span data-i="m_tut_d"></span></button>
        <button class="mbtn" id="m-free">''')
f.rep('''Buy me a Beer</button>
      </div>
      </div>
      </div>
    </div>''','''Buy me a Beer</button>
      </div>
      </div>
    </div>''')
f.rep("#scores,#chal{z-index:860}","""/* Startseite (SPI-17): oben der Ballon von der Seite, darunter das Menü im Stil der App */
#hero{flex:none;display:block;width:100%;height:clamp(130px,30%,300px);background:#10203a;border-bottom:1px solid var(--line)}
.mframe .mcard{flex:1;min-height:0;width:100%;max-height:none;overflow:auto;padding:10px 14px 12px;background:none;border:0;border-radius:0;-webkit-overflow-scrolling:touch}
.mcard.boot{animation:mfade .7s ease both}
@keyframes mfade{from{opacity:0}to{opacity:1}}
.mframe .mname{font-family:var(--ui);font-size:13px;letter-spacing:0;text-transform:none;color:var(--mut)}
.mframe .mname input{border-radius:12px;border:1px solid var(--line);font-family:var(--ui);font-weight:500}
.mframe .mbtn{background:var(--pan2);min-height:54px}
.mframe .mbtn b{font-family:var(--num);font-size:20px}
.mframe #m-free{background:var(--orb);border-color:var(--orb);color:#1a1000}
.mframe #m-free span{color:#3a2600}
.mframe .mbtn.tut{min-height:0;padding:6px 12px;background:transparent;border:1px solid var(--base)}
.mframe .mbtn.tut b{font-size:16px;color:var(--base)}
.mframe .mbtn.tut.new{animation:tutnew 1.6s ease-in-out infinite}
@keyframes tutnew{0%,100%{box-shadow:0 0 0 0 rgba(76,201,255,0)}50%{box-shadow:0 0 0 5px rgba(76,201,255,.28)}}
.mframe .mbtn.alt{margin-top:10px;text-align:center;border:1px dashed #4a5f80;background:transparent;min-height:0}
.mframe .mbtn.alt b{font-size:16px}
.mframe .mbtn.alt b span{display:inline;font-size:inherit;color:inherit}
/* Tutorial (SPI-18) */
#tut{position:absolute;left:50%;top:60px;transform:translateX(-50%);z-index:700;width:min(300px,calc(100% - 24px));padding:10px 12px;background:#0d1626;border:1px solid var(--base);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
#tut[hidden],#tut-hand[hidden]{display:none}
#tut p{margin:0 0 8px;font-size:14.5px;line-height:1.4}
#tut .btns{display:flex;gap:8px;justify-content:flex-end;align-items:center}
#tut-step{margin-right:auto;font-size:12px;color:var(--mut)}
#tut-hand{position:absolute;z-index:710;width:44px;height:52px;pointer-events:none;animation:tuthand 1.1s ease-in-out infinite}
@keyframes tuthand{0%,100%{transform:translate(-50%,6px)}50%{transform:translate(-50%,-8px)}}
@media (prefers-reduced-motion:reduce){#tut-hand,.mframe .mbtn.tut.new,.mcard.boot{animation:none}#tut-hand{transform:translate(-50%,0)}}
#scores,#chal{z-index:860}""")
f.rep('      <div class="ov card" id="side" hidden>','''      <div id="tut" hidden role="status"><p id="tut-text"></p><div class="btns"><span id="tut-step"></span><button class="sm" id="tut-skip"></button><button class="sm" id="tut-next"></button></div></div>
      <div id="tut-hand" hidden aria-hidden="true"><svg viewBox="0 0 44 52" width="44" height="52"><path d="M17 26V8a4 4 0 0 1 8 0v14l10 2.500a5 5 0 0 1 3.800 5.500L37 42a8 8 0 0 1-8 7h-7a8 8 0 0 1-6.500-3.300L7 34a3.300 3.300 0 0 1 5-4.300z" fill="#eef3fa" stroke="#0a1019" stroke-width="2" stroke-linejoin="round"/></svg></div>
      <div class="ov card" id="side" hidden>'''.replace('2.500','2.5').replace('3.800','3.8').replace('5.500','5.5').replace('6.500','6.5').replace('3.300','3.3').replace('4.300','4.3'))
tx_add(f,{
 'hero_a':['Gasballon von der Seite: Er steigt, wenn Sand abgegeben wird, und sinkt, wenn Gas durch das Ventil entweicht.','Gas balloon from the side: it climbs when sand is released and sinks when gas escapes through the valve.','Ballon à gaz vu de côté : il monte quand on vide du sable et descend quand du gaz s’échappe par la soupape.','Balon gazowy z boku: wznosi się, gdy wysypuje się piasek, i opada, gdy gaz uchodzi przez zawór.','Plynový balon z boku: stoupá, když se vysype písek, a klesá, když ventilem uniká plyn.','側面看的氣體氣球：倒出沙子就上升，氣體從閥門排出就下降。','Globo de gas visto de lado: sube al vaciar arena y baja cuando el gas sale por la válvula.'],
 'm_tut':['Erste Fahrt','First flight','Premier vol','Pierwszy lot','První let','第一次飛行','Primer vuelo'],
 'm_tut_d':['Tutorial: Schritt für Schritt abheben, steuern und landen','Tutorial: lift off, steer and land step by step','Tutoriel : décoller, piloter et atterrir pas à pas','Samouczek: start, sterowanie i lądowanie krok po kroku','Výuka: vzlet, řízení a přistání krok za krokem','教學：一步一步起飛、操控與降落','Tutorial: despegar, pilotar y aterrizar paso a paso'],
 'tut_next':['Weiter','Next','Suivant','Dalej','Dále','下一步','Siguiente'],
 'tut_skip':['Beenden','Quit','Quitter','Zakończ','Ukončit','結束','Salir'],
})
# ================= Musik: ruhiges Stück, sanft ein- und ausgeblendet =================
f.block("  /* Musik im Hauptmenü: frei erfundenes Stück","  let drag = null, fallS = null;",r'''  /* Musik im Hauptmenü (SND-07): frei erfundenes, ruhiges Stück. Weiche Flächenklänge wechseln alle vier Sekunden den Akkord,
     darüber einzelne glockenartige Töne. Es blendet in vier Sekunden ein und in rund drei Sekunden aus. */
  const CALM = {bar: 4, vol: 0.11,
    chords: [[48, 55, 59, 64], [45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 55, 59], [48, 55, 59, 64], [40, 47, 52, 55], [41, 48, 52, 57], [43, 50, 54, 59]],
    bells: [[76, 0, 79, 0], [72, 0, 0, 76], [69, 0, 72, 0], [74, 0, 0, 71], [79, 0, 76, 0], [71, 0, 0, 67], [72, 0, 69, 0], [74, 0, 0, 0]]};
  const mf = n => 440 * Math.pow(2, (n - 69) / 12);
  let mus = null;
  function mPad(n, t, dur, peak){
    const o = ctx.createOscillator(), o2 = ctx.createOscillator(), lp = ctx.createBiquadFilter(), g = ctx.createGain();
    o.type = 'triangle'; o2.type = 'sine'; o.frequency.value = mf(n); o2.frequency.value = mf(n) * 1.003; lp.type = 'lowpass'; lp.frequency.value = 900;
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(peak, t + dur * 0.35); g.gain.linearRampToValueAtTime(peak * 0.8, t + dur * 0.8); g.gain.linearRampToValueAtTime(0.0001, t + dur * 1.25);
    o.connect(lp); o2.connect(lp); lp.connect(g); g.connect(mus.g); o.start(t); o2.start(t); o.stop(t + dur * 1.3); o2.stop(t + dur * 1.3);
  }
  function mBell(n, t, peak){
    const o = ctx.createOscillator(), g = ctx.createGain(); o.type = 'sine'; o.frequency.value = mf(n);
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(peak, t + 0.03); g.gain.exponentialRampToValueAtTime(0.0001, t + 2.6);
    o.connect(g); g.connect(mus.g); o.start(t); o.stop(t + 2.7);
  }
  function mBar(i, t){
    const k = i % CALM.chords.length; CALM.chords[k].forEach((n, j) => mPad(n, t, CALM.bar, j === 0 ? 0.20 : 0.11));
    CALM.bells[k].forEach((n, j) => { if (n) mBell(n, t + j * CALM.bar / 4 + 0.02, 0.10); });
  }
  function music(on){
    if (!on || !UI.music){
      if (mus){ const m = mus; mus = null; clearInterval(m.timer); const g = m.g; g.gain.cancelScheduledValues(ctx.currentTime); g.gain.setTargetAtTime(0, ctx.currentTime, 0.9); setTimeout(() => { try{ g.disconnect(); }catch(e){} }, 5000); }   // sanft ausblenden
      return;
    }
    if (mus) { if (ctx.state === 'suspended') ctx.resume(); return; }
    if (!audio()) return;
    mus = {g: ctx.createGain(), i: 0, next: ctx.currentTime + 0.15};
    mus.g.gain.setValueAtTime(0.0001, ctx.currentTime); mus.g.gain.linearRampToValueAtTime(CALM.vol, ctx.currentTime + 4); mus.g.connect(master);   // sanft einblenden
    mus.timer = setInterval(() => {
      if (!mus) return;
      if (ctx.state !== 'running'){ mus.next = ctx.currentTime + 0.15; return; }
      if (mus.next < ctx.currentTime) mus.next = ctx.currentTime + 0.05;
      while (mus.next < ctx.currentTime + 0.6){ mBar(mus.i++, mus.next); mus.next += CALM.bar; }
    }, 200);
  }
''')
f.rep("const musicWanted = () => !!UI.music && ['menu', 'chal', 'setup', 'pick', 'busy', 'brief', 'scores'].includes(STATE) && document.visibilityState !== 'hidden' && performance.now() - menuAt > 1700;","const musicWanted = () => !!UI.music && ['menu', 'chal', 'setup', 'pick', 'busy', 'brief', 'scores'].includes(STATE) && document.visibilityState !== 'hidden' && performance.now() - menuAt > 600;")
f.rep("menuAt = performance.now(); setTimeout(() => SND.music(musicWanted()), 1800);","menuAt = performance.now(); setTimeout(() => SND.music(musicWanted()), 700);")
f.rep("  RETRO.reset(); setState('menu');","  HERO.reset(); $('m-tut').classList.toggle('new', !store.get('gb-tut', 0)); setState('menu');")
f.rep("{ RETRO.tick(real); requestAnimationFrame(frame); return; }","{ HERO.tick(real); requestAnimationFrame(frame); return; }")
# ================= Bild der Startseite =================
f.block("/* ---------- Hauptmenü: bewegtes Bild im Stil der Heimcomputer","/* ---------- Meisterschaft (MEI-01 bis MEI-10)",r'''/* ---------- Startseite (SPI-17): der Ballon von der Seite über einer Landschaft. Er steigt, wenn Sand rieselt, und sinkt, wenn Gas am Ventil austritt;
   tief über dem Boden schleift das Tau. Dieselbe Darstellung wie die Seitenansicht in der Fahrt. Bei „Bewegung reduzieren“ steht das Bild. ---------- */
const HERO = (() => {
  const cv = $('hero'), still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; let t = 0, acc = 0, sand = [], puff = [], drawn = false;
  const CYC = 26, ease = x => 0.5 - 0.5 * Math.cos(Math.PI * Math.max(0, Math.min(1, x)));
  const alt = s => s < 9 ? 34 + 96 * ease(s / 9) : s < 13 ? 130 : s < 22 ? 130 - 96 * ease((s - 13) / 9) : 34;          // m über Grund
  const hill = (x, k) => k ? 10 * Math.sin(x / 61) + 6 * Math.sin(x / 23 + 1.3) : 7 * Math.sin(x / 47 + 0.6) + 4 * Math.sin(x / 17);
  function draw(dt){
    const W = cv.clientWidth, H = cv.clientHeight; if (!W || !H) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 3); if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)){ cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
    t += dt; const s = t % CYC, h = alt(s), w = (alt(s + 0.2) - alt(s - 0.2)) / 0.4, scroll = t * 9;
    const g0 = H - 26, m = (g0 - 18) / 175, y = z => g0 - z * m, bx = W * 0.42;
    c.fillStyle = '#10203a'; c.fillRect(0, 0, W, H); c.fillStyle = '#16294a'; c.fillRect(0, y(38), W, g0 - y(38) + 30);
    c.font = '600 12px "Barlow Condensed","Arial Narrow",sans-serif'; c.textBaseline = 'middle';
    for (const z of [50, 100, 150]){ c.strokeStyle = '#2b4168'; c.lineWidth = 1; c.beginPath(); c.moveTo(40, y(z) + .5); c.lineTo(W, y(z) + .5); c.stroke(); c.fillStyle = '#9db3d1'; c.textAlign = 'right'; c.fillText(z + ' m', 36, y(z)); }
    [[150, 4.4, 26], [100, 4.25, 17], [50, 4.0, 9]].forEach(b => drawBarb(c, W - 30, y(b[0]), b[1], b[2], 17));
    // Landschaft: zwei Hügelketten, die langsam vorbeiziehen
    c.fillStyle = '#1d3a2f'; c.beginPath(); c.moveTo(0, H); for (let X = 0; X <= W; X += 6) c.lineTo(X, g0 - 12 - hill(X + scroll * 0.5, 1)); c.lineTo(W, H); c.closePath(); c.fill();
    const gy = X => g0 - hill(X + scroll, 0); c.fillStyle = '#17302a'; c.beginPath(); c.moveTo(0, H); for (let X = 0; X <= W; X += 5) c.lineTo(X, gy(X)); c.lineTo(W, H); c.closePath(); c.fill();
    c.fillStyle = '#24483a'; for (let k = Math.floor(scroll / 140) - 1; k < Math.floor((scroll + W) / 140) + 1; k++){ const X = k * 140 + 60 - scroll, Y = gy(X); if (k % 3 === 0){ c.fillRect(X, Y - 9, 14, 9); c.beginPath(); c.moveTo(X - 2, Y - 9); c.lineTo(X + 7, Y - 16); c.lineTo(X + 16, Y - 9); c.fill(); } else { c.beginPath(); c.moveTo(X, Y); c.lineTo(X + 6, Y - 15); c.lineTo(X + 12, Y); c.fill(); } }
    // Ballon
    const gB = gy(bx), yb = gB - h * m, r = Math.max(13, 6.2 * m * 2.1), bw = r * 0.48, bh = r * 0.36, cy = yb - bh - r * 1.5;
    const hang = Math.min(50, h), lie = 50 - hang; c.strokeStyle = '#c9a66b'; c.lineWidth = 2.2; c.lineCap = 'round'; c.beginPath(); c.moveTo(bx + bw / 2, yb - 2);          // Schlepptau
    if (lie <= 0) c.lineTo(bx + bw / 2 - 3, yb + 50 * m); else { const x0 = bx - 5; c.quadraticCurveTo(bx + bw / 2, gB - 1, x0, gy(x0) - 1); for (let d = 3; d <= lie; d += 3){ const X = x0 - d * m; c.lineTo(X, gy(X) - 1); } } c.stroke();
    c.strokeStyle = '#c9d6e8'; c.lineWidth = 1.2; c.beginPath(); c.moveTo(bx - r * 0.72, cy + r * 0.7); c.lineTo(bx - bw / 2, yb - bh); c.moveTo(bx + r * 0.72, cy + r * 0.7); c.lineTo(bx + bw / 2, yb - bh); c.stroke();
    c.fillStyle = '#f4f1ea'; c.beginPath(); c.arc(bx, cy, r, 0, 7); c.fill(); c.strokeStyle = '#d2cdc0'; c.lineWidth = 1.2; c.beginPath(); c.ellipse(bx, cy, r * 0.42, r, 0, 0, 7); c.stroke();
    c.fillStyle = '#b98a4a'; c.fillRect(bx - bw / 2, yb - bh, bw, bh);
    // Sand beim Steigen, Gas beim Sinken
    const climbing = s > 0.3 && s < 3.2, venting = s > 13 && s < 16;
    if (!still){ if (climbing && Math.random() < 0.7) sand.push({t: 0, x: (Math.random() - .5) * 4}); if (venting && Math.random() < 0.3) puff.push({t: 0, x: (Math.random() - .5) * 6}); }
    sand.forEach(p => { p.t += dt; }); sand = sand.filter(p => p.t < 1.6); puff.forEach(p => { p.t += dt; }); puff = puff.filter(p => p.t < 1.5);
    c.fillStyle = '#ffe14d'; sand.forEach(p => c.fillRect(bx - bw / 2 - 3 + p.x, yb + 40 * p.t + 30 * p.t * p.t, 2, 2));
    puff.forEach(p => { c.strokeStyle = 'rgba(127,216,255,' + (0.9 - p.t / 1.7).toFixed(2) + ')'; c.lineWidth = 1.5; c.beginPath(); c.arc(bx + p.x * (1 + p.t), cy - r - 4 - p.t * 16, 2.5 + p.t * 5, 0, 7); c.stroke(); });
    c.font = '500 12px Barlow,"Segoe UI",sans-serif'; c.fillStyle = '#e8eef7'; c.textAlign = 'left';
    if (climbing || (still && true)) c.fillText(tr('sand'), bx - bw / 2 - 44, yb + 16);
    if (venting) c.fillText(tr('valve'), bx + r * 0.5, cy - r - 12);
    if (lie > 3) c.fillText(tr('dt_rope'), Math.max(44, bx - lie * m - 70), gB - 12);
    c.font = '600 14px "Barlow Condensed","Arial Narrow",sans-serif'; c.fillStyle = w > 0.4 ? '#5fe3a1' : w < -0.4 ? '#ff6e5f' : '#9db3d1'; c.textAlign = 'left'; c.fillText((w >= 0 ? '+' : '−') + Math.abs(w / 6).toFixed(1) + ' m/s', bx + r + 8, cy);
    drawn = true;
  }
  return { tick(real){ if (still){ if (!drawn || cv.width !== Math.round(cv.clientWidth * Math.min(window.devicePixelRatio || 1, 3))){ t = 2; draw(0); } return; } acc += real; if (acc < 1 / 30) return; draw(acc); acc = 0; }, reset(){ t = 0; acc = 0; sand = []; puff = []; drawn = false; } };
})();

/* ---------- Tutorial „Erste Fahrt“ (SPI-18): Simulation ab Bitterfeld. Am Anfang ist nur der Ballon zu sehen; die Bedienelemente kommen
   einzeln dazu. Eine Hand zeigt, was anzutippen ist, danach erklärt ein Satz, was geschehen ist und wozu es dient. Deutsch und Englisch;
   andere Sprachen zeigen Englisch. ---------- */
const TUT_TX = {
 de: {intro: 'Willkommen an Bord. Dein Gasballon ist mit Wasserstoff gefüllt und steht im Gleichgewicht: Er ist genau so schwer wie die Luft, die er verdrängt. Die Bodencrew hält ihn noch fest. Unten links siehst du ihn von der Seite.',
  sacks: 'Das sind deine Sandsäcke, je 15 kg. Tippe auf einen Sack, um ihn zu entleeren. Die Crew lässt los, sobald der Ballon 30 kg leichter als die Luft ist.',
  go: 'Die Crew hat losgelassen, der Ballon steigt. Sand abgeben ist der einzige Weg nach oben, und was weg ist, kommt nicht wieder.',
  inst: 'Rechts stehen deine Anzeigen: Höhe über Grund, darunter das Vario (Steigen und Sinken in m/s), Fahrtrichtung, Sand und Füllgrad. Der Balken am Vario zeigt, ob der Ballon gerade beschleunigt.',
  prof: 'Links das Vertikalprofil: Die Fähnchen zeigen, woher und wie stark der Wind in jeder Höhe weht. Lenken kannst du nur, indem du die Höhe mit dem passenden Wind suchst. Die Farben zeigen die Schichtung der Luft, blau ist eine Inversion.',
  scoop: 'Für feine Korrekturen gibt es die Schaufel: 200 g je Tipp aus der Sandmulde. Tippe einmal auf die Schaufel.',
  scoop2: 'Gut. Kleine Mengen reichen oft: Schon 1 kg ändert das Steigen spürbar, aber erst nach einigen Sekunden.',
  valve: 'Nach unten geht es mit dem Ventil: Es lässt Gas ab. Zieh den Regler nach unten und halte ihn zwei Sekunden. Solange du ziehst, läuft die Zeit 1×.',
  valve2: 'Der Ballon hat Gas verloren und wird sinken. Auch Gas kommt nicht zurück: Jede Höhenänderung kostet Sand oder Gas. Wer sparsam fährt, kommt weiter.',
  speed: 'Oben stellst du den Zeitraffer ein und hältst die Fahrt an. Der Knopf mit dem Ballon unten rechts blendet die Seitenansicht ein; unter 50 m erscheint sie von selbst.',
  rope: 'Das Schlepptau ist 50 m lang. Berührt es den Boden, trägt der Boden einen Teil seines Gewichts: Das fängt das Sinken ab und bremst die Fahrt. Wirf es jetzt aus. Es lässt sich nicht wieder einrollen.',
  land: 'Jetzt lande: Zieh das Ventil in kurzen Zügen und lass den Ballon sinken. Setz mit weniger als 1 m/s auf, dann ist es eine sanfte Landung. Sinkt er zu schnell, gib eine Schaufel Sand ab.',
  done: 'Gelandet. Das war deine erste Fahrt. In der Freien Fahrt wählst du Startplatz und Wetter selbst; in der Challenge warten Aufgaben mit Wertung.'},
 en: {intro: 'Welcome aboard. Your gas balloon is filled with hydrogen and is in equilibrium: it weighs exactly as much as the air it displaces. The ground crew is still holding it. At the bottom left you see it from the side.',
  sacks: 'These are your sandbags, 15 kg each. Tap a bag to empty it. The crew lets go as soon as the balloon is 30 kg lighter than the air.',
  go: 'The crew has let go and the balloon climbs. Releasing sand is the only way up, and what is gone does not come back.',
  inst: 'Your instruments are on the right: height above ground, below it the vario (climb and sink in m/s), track, sand and fill. The bar at the vario shows whether the balloon is accelerating.',
  prof: 'On the left is the vertical profile: the barbs show where the wind comes from and how strong it is at each height. You can only steer by finding the height with the right wind. The colours show how the air is layered; blue is an inversion.',
  scoop: 'For fine corrections there is the scoop: 200 g per tap from the sand trough. Tap the scoop once.',
  scoop2: 'Good. Small amounts are often enough: even 1 kg changes the climb noticeably, but only after a few seconds.',
  valve: 'The valve takes you down: it releases gas. Pull the slider down and hold it for two seconds. While you pull, time runs at 1×.',
  valve2: 'The balloon has lost gas and will sink. Gas does not come back either: every change of height costs sand or gas. Fly sparingly and you get farther.',
  speed: 'At the top you set the time factor and pause the flight. The button with the balloon at the bottom right shows the side view; below 50 m it appears by itself.',
  rope: 'The trail rope is 50 m long. When it touches the ground, the ground carries part of its weight: that stops the sink and slows the balloon. Deploy it now. It cannot be hauled in again.',
  land: 'Now land: pull the valve in short tugs and let the balloon sink. Touch down at less than 1 m/s for a gentle landing. If it sinks too fast, release a scoop of sand.',
  done: 'Landed. That was your first flight. In Free flight you choose launch site and weather yourself; in Challenge there are scored tasks.'}};
const TUT = {on: false, i: 0, vT: 0, mU0: 0,
  hide: ['box-sacks', 'box-trough', 'box-valve', 'box-rope', 'prof', 'inst', 'seg-speed', 'btn-set', 'corner', 'hint'],
  steps: [{k: 'intro'}, {k: 'sacks', show: ['box-sacks'], at: 'rack', done: () => B.go}, {k: 'go'}, {k: 'inst', show: ['inst']}, {k: 'prof', show: ['prof']},
    {k: 'scoop', show: ['box-trough'], at: 'scoop', done: () => B.mU < TUT.mU0 || B.sacks < TUT.s0}, {k: 'scoop2'}, {k: 'valve', show: ['box-valve'], at: 'valve', done: () => TUT.vT > 1.6}, {k: 'valve2'},
    {k: 'speed', show: ['seg-speed', 'corner'], at: 'seg-speed'}, {k: 'rope', show: ['box-rope'], at: 'rope', done: () => B.rope}, {k: 'land', at: 'valve', done: () => B.landed}, {k: 'done'}]};
function tutText(k){ return (TUT_TX[UI.lang] || TUT_TX.en)[k]; }
function tutShow(){
  const s = TUT.steps[TUT.i]; (s.show || []).forEach(id => { $(id).style.visibility = ''; $(id).style.pointerEvents = ''; });
  TUT.mU0 = B.mU; TUT.s0 = B.sacks; TUT.vT = 0;
  $('tut-text').textContent = tutText(s.k); $('tut-step').textContent = (TUT.i + 1) + ' / ' + TUT.steps.length; $('tut-next').hidden = !!s.done; $('tut-next').textContent = tr(TUT.i === TUT.steps.length - 1 ? 'close' : 'tut_next'); $('tut-skip').textContent = tr('tut_skip'); $('tut-skip').hidden = TUT.i === TUT.steps.length - 1;
  $('tut').hidden = false; $('tut-hand').hidden = !s.at;
}
function tutNext(){ if (TUT.i >= TUT.steps.length - 1){ tutEnd(true); return; } TUT.i++; tutShow(); }
function tutEnd(finished){
  if (!TUT.on) return; TUT.on = false; $('tut').hidden = true; $('tut-hand').hidden = true; TUT.hide.forEach(id => { $(id).style.visibility = ''; $(id).style.pointerEvents = ''; });
  if (finished) store.set('gb-tut', 1);
}
function tutTick(real){
  if (!TUT.on) return; if (STATE !== 'play' && STATE !== 'done'){ tutEnd(false); return; }
  const s = TUT.steps[TUT.i]; if (valve > 0) TUT.vT += real;
  if (s.at){ const r = $(s.at).getBoundingClientRect(), a = $('app').getBoundingClientRect(), h = $('tut-hand'); h.style.left = (r.left + r.width / 2 - a.left) + 'px'; h.style.top = Math.max(0, r.top - a.top + Math.min(r.height * 0.45, 40)) + 'px'; }
  if (s.done && s.done()) tutNext();
  else if (B.landed && s.k !== 'done' && s.k !== 'land'){ TUT.i = TUT.steps.length - 2; tutNext(); }          // früher gelandet: zum Abschluss springen
}
function tutStart(){
  UI.mode = 'free'; gbLeave(); clearGoals(); applyStart(BITTERFELD); TARGET = null; WZ = null; MDT = null; FLY = []; WX = null; newSim('free'); TER.on = false; resetRun();
  TUT.on = true; TUT.i = 0; TUT.hide.forEach(id => { $(id).style.visibility = 'hidden'; $(id).style.pointerEvents = 'none'; });
  setState('play'); startView(); tutShow();
}
$('m-tut').addEventListener('click', tutStart); $('tut-next').addEventListener('click', tutNext); $('tut-skip').addEventListener('click', () => tutEnd(false));

''')
f.rep("  pvTick(real); sideTick(real);","  pvTick(real); tutTick(real); sideTick(real);")
f.rep("function showMenu(){\n  gbLeave();","function showMenu(){\n  tutEnd(false); gbLeave();")
f.rep("const BUILD = '2026-10-10.2'","const BUILD = '2026-10-10.3'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v34'" in s; open(p,'w').write(s.replace("'v34'","'v35'"))
