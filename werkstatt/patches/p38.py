import sys
sys.path.insert(0,'/home/claude/w')
from ph import F,tx_add
f=F()
# ============ Rollhinweis: Klassenname kollidierte mit einer vorhandenen Regel („.more“), dadurch sprang das Fenster ============
f.rep(".shint{position:sticky;bottom:0;height:0;pointer-events:none;display:none;z-index:5}\n.more > .shint{display:block}",".shint{position:sticky;bottom:0;height:0;pointer-events:none;z-index:5;opacity:0;transition:opacity .25s}\n.scrl-more > .shint{opacity:1}\n.mcard,.sheet,.full .card,#result{overscroll-behavior:contain;overflow-anchor:none}")
f.rep(".shint i{position:absolute;left:-14px;right:-14px;bottom:-12px;height:44px;display:grid;place-items:end center;padding-bottom:5px;background:linear-gradient(rgba(10,16,25,0),rgba(10,16,25,.96) 62%)}",".shint i{position:absolute;left:50%;bottom:-6px;width:44px;height:24px;margin-left:-22px;display:grid;place-items:center;border-radius:12px;background:rgba(10,16,25,.9);border:1px solid var(--orb)}")
f.rep("function shintUpd(){ SHINT.forEach(el => el.classList.toggle('more', el.scrollHeight - el.clientHeight - el.scrollTop > 10)); }","function shintUpd(){ SHINT.forEach(el => { const rest = el.scrollHeight - el.clientHeight - el.scrollTop, on = el.classList.contains('scrl-more'); if (!on && rest > 28) el.classList.add('scrl-more'); else if (on && rest < 8) el.classList.remove('scrl-more'); }); }   // mit Abstand zwischen Ein und Aus, damit nichts flackert")
# ============ Fenster ein- und ausfahren (NFA-08) ============
f.rep('<canvas id="prof-cv" role="img" data-ia="prof_hint" aria-label="Vertikalprofil"></canvas>','<button class="hdl" id="prof-h" data-ia="fold_a" aria-label="ein- oder ausfahren"></button><canvas id="prof-cv" role="img" data-ia="prof_hint" aria-label="Vertikalprofil"></canvas>')
f.rep('        <div class="kv gasaid" hidden><span>ΔT K</span><b id="i-gast">–</b></div>\n      </div>','        <div class="kv gasaid" hidden><span>ΔT K</span><b id="i-gast">–</b></div>\n        <button class="hdl" id="inst-h" data-ia="fold_a" aria-label="ein- oder ausfahren"></button>\n      </div>')
f.rep('    <div class="panel">\n      <div class="box" id="box-sacks">','    <div class="panel">\n      <button class="hdl" id="panel-h" data-ia="fold_a" aria-label="ein- oder ausfahren"><span id="panel-sum"></span></button>\n      <div class="box" id="box-sacks">')
for a,b in [('<div class="kv"><span data-i="track">Fahrt</span>','<div class="kv x1"><span data-i="track">Fahrt</span>'),('<div class="kv tgt" hidden><span id="i-tlbl">','<div class="kv tgt x1" hidden><span id="i-tlbl">'),('<div class="kv tgt" hidden><span>→</span>','<div class="kv tgt x1" hidden><span>→</span>'),
 ('<div class="kv"><span data-i="time">Zeit</span>','<div class="kv x2"><span data-i="time">Zeit</span>'),('<div class="kv"><span data-i="dist">Weg</span>','<div class="kv x2"><span data-i="dist">Weg</span>'),('<div class="kv"><span data-i="sand">Sand</span><b id="n-total">','<div class="kv x2"><span data-i="sand">Sand</span><b id="n-total">'),
 ('<div class="kv"><span data-i="fill">Gas</span>','<div class="kv x1"><span data-i="fill">Gas</span>'),('<div class="kv"><span id="i-skyl">','<div class="kv x2"><span id="i-skyl">'),('<div class="kv"><span>°C</span><b id="i-temp">','<div class="kv x2"><span>°C</span><b id="i-temp">'),
 ('<div class="kv" id="row-wet" hidden>','<div class="kv x2" id="row-wet" hidden>'),('<div class="kv gasaid" hidden><span>m³</span>','<div class="kv gasaid x2" hidden><span>m³</span>'),('<div class="kv gasaid" hidden><span>ΔT K</span>','<div class="kv gasaid x2" hidden><span>ΔT K</span>')]: f.rep(a,b)
f.rep("#ofm-btn{right:0;top:230px;","""/* Fenster ein- und ausfahren (NFA-08): kleine Griffe am Rand */
.hdl{display:block;border:0;background:var(--pan2);color:var(--mut);padding:0;flex:none;position:relative}
.hdl::after{content:'';position:absolute;left:50%;top:50%;width:26px;height:4px;margin:-2px 0 0 -13px;border-radius:2px;background:#5d6f8f}
#prof-h{width:100%;height:16px;border-bottom:1px solid var(--line)}
#prof.shut{width:22px;height:86px;border-radius:0 0 12px 0}
#prof.shut canvas,#prof.shut #temp-btn{display:none}
#prof.shut #prof-h{height:100%;border:0}
#prof.shut #prof-h::after{width:4px;height:30px;margin:-15px 0 0 -2px}
#inst-h{width:calc(100% + 15px);height:15px;margin:3px -7px -6px -8px;border-top:1px solid var(--line)}
#inst.c1 .x2,#inst.c2 .x1,#inst.c2 .x2,#inst.c2 .lbl{display:none}
#panel-h{grid-column:1/-1;height:15px;margin:-6px -5px 0;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:center}
#panel-sum{display:none;font-family:var(--num);font-size:14px;color:var(--tx);padding-left:44px;white-space:nowrap}
.panel.shut > .box{display:none}
.panel.shut #panel-h{height:30px;margin-bottom:-6px;border-bottom:0}
.panel.shut #panel-sum{display:inline}
.panel.shut #panel-h::after{left:22px}
@media (orientation:landscape) and (max-height:560px){
  #panel-h{grid-column:auto;grid-row:1/-1;width:15px;height:auto;margin:-6px 0 -6px -5px;border-bottom:0;border-right:1px solid var(--line)}
  #panel-h::after{width:4px;height:26px;margin:-13px 0 0 -2px}
  .panel{grid-template-columns:15px 1.3fr 1fr 54px 50px}
  .panel.shut{width:22px;grid-template-columns:22px;padding-right:0}
  .panel.shut #panel-h{width:22px;height:auto;margin:-6px 0 -6px -5px}
  .panel.shut #panel-sum{display:none}
  .panel.shut #panel-h::after{left:50%}
}
#ofm-btn{right:0;top:230px;""")
tx_add(f,{'fold_a':['Fenster ein- oder ausfahren','Fold or unfold this panel','Replier ou déplier ce panneau','Zwiń lub rozwiń panel','Sbalit nebo rozbalit panel','收合或展開面板','Plegar o desplegar el panel'],
 'news_title':['Was ist neu','What’s new','Nouveautés','Co nowego','Co je nového','最新消息','Novedades']})
# ============ Ballonsymbol: Form nach Füllgrad (STE-29) ============
a=f.s.index("const balloonSVG = c => `"); b=f.s.index("\n",a)
f.s=f.s[:a]+r'''/* Ballonsymbol der Karte. f: Füllgrad 0 bis 1. Prall ist die Hülle rund; verliert sie Gas, sammelt es sich oben, und der untere Teil hängt schmal und schlaff (STE-29). */
const balloonSVG = (c, f) => { const s = Math.pow(1 - Math.max(0, Math.min(1, f == null ? 1 : f)), 0.7), nw = 5 - 3.2 * s, r = x => x.toFixed(1);
  return `<svg viewBox="0 0 44 54" width="44" height="54"><path d="M4 20C4 10 11 2 22 2C33 2 40 10 40 20C${r(40 - 15 * s)} ${r(28 - 2 * s)} ${r(34 - 9 * s)} 34.5 ${r(22 + nw)} 39L${r(22 - nw)} 39C${r(10 + 9 * s)} 34.5 ${r(4 + 15 * s)} ${r(28 - 2 * s)} 4 20z" fill="${c}" stroke="#0a1019" stroke-width="2" stroke-linejoin="round"/><path d="M22 2C16 7 ${r(14 + 5 * s)} 16 ${r(22 - nw)} 39M22 2C28 7 ${r(30 - 5 * s)} 16 ${r(22 + nw)} 39" fill="none" stroke="#0a1019" stroke-opacity=".35" stroke-width="1.6"/><path d="M${r(22 - nw)} 39L20 45M${r(22 + nw)} 39L24 45" stroke="#eef3fa" stroke-width="1.4"/><rect x="18" y="45" width="8" height="6" rx="1.5" fill="#eef3fa" stroke="#0a1019" stroke-width="1.5"/></svg>`; };'''+f.s[b:]
f.rep("  $('i-fill').textContent = nf(fillNow() * 100, 0) + ' %';","  $('i-fill').textContent = nf(fillNow() * 100, 0) + ' %';\n  { const q = Math.round(fillNow() * 20); if (q !== balMk._fq){ balMk._fq = q; balMk.setIcon(L.divIcon({className: 'mk', iconSize: [44, 54], iconAnchor: [22, 51], html: balloonSVG('#ff9f1c', q / 20)})); } }   // Symbol der Karte zeigt den Füllgrad\n  if (STATE === 'play' || STATE === 'done') $('panel-sum').textContent = tr('sand') + ' ' + nf(sandKg(B, CFG), 0) + ' kg · ' + tr('fill') + ' ' + nf(fillNow() * 100, 0) + ' %' + (B.rope ? ' · ' + tr('rope') : '');")
# ============ JS: Falten, Was ist neu ============
f.rep("/* ---------- Rollhinweis (NFA-07) ---------- */",r'''/* ---------- Fenster ein- und ausfahren (NFA-08): Vertikalprofil, Anzeigen (drei Längen) und Bedienfeld; die Wahl bleibt gespeichert ---------- */
const FOLD = Object.assign({p: 0, i: 0, b: 0}, store.get('gb-fold', {}));
function foldApply(save){
  $('prof').classList.toggle('shut', !!FOLD.p); $('inst').classList.toggle('c1', FOLD.i === 1); $('inst').classList.toggle('c2', FOLD.i === 2); document.querySelector('.panel').classList.toggle('shut', !!FOLD.b);
  if (save) store.set('gb-fold', FOLD); setTimeout(() => { try{ map.invalidateSize(); }catch(e){} }, 60);
}
$('prof-h').addEventListener('click', () => { FOLD.p = FOLD.p ? 0 : 1; foldApply(true); });
$('inst-h').addEventListener('click', () => { FOLD.i = (FOLD.i + 1) % 3; foldApply(true); });
$('panel-h').addEventListener('click', () => { FOLD.b = FOLD.b ? 0 : 1; foldApply(true); });
foldApply(false);

/* ---------- Was ist neu (INS-06): kurze Texte je Build für die Nutzer, der neueste zuerst. Deutsch und Englisch; andere Sprachen zeigen Englisch. ---------- */
const NEWS = [
 {b: '2026-10-11.1', de: ['Mehr Platz für die Karte: Vertikalprofil, Anzeigen und Bedienfeld lassen sich über die kleinen Griffe am Rand ein- und ausfahren. Die Anzeigen haben drei Längen; die kürzeste zeigt nur Höhe und Vario.', 'Das Ballonsymbol auf der Karte zeigt jetzt den Füllgrad: Verliert der Ballon Gas, wird die Hülle unten schmal.', 'Behoben: In langen Fenstern sprang der Inhalt beim Rollen.', 'Neu: diese Seite.'],
  en: ['More room for the map: the vertical profile, the instruments and the control panel fold away with the small handles at the edge. The instruments have three lengths; the shortest shows only height and vario.', 'The balloon symbol on the map now shows the fill: when the balloon loses gas, the envelope narrows at the bottom.', 'Fixed: in long windows the content jumped while scrolling.', 'New: this page.']},
 {b: '2026-10-10.7', de: ['Erste Fassung auf dem Server: gemeinsame Bestenliste mit Namen und Statistik in den Einstellungen, sobald der Dienst des Servers läuft.', 'Tutorial „Erste Fahrt“, neue Startseite mit ruhiger Melodie.', 'Temp-Diagramm mit Taupunkt unter dem Vertikalprofil, Seitenansicht mit Gelände, Lufträume als Schalter unter den Anzeigen.', 'Der Füllgrad der Hülle bestimmt den Luftwiderstand: Ein leerer Ballon fällt schnell.', 'Nach der Landung lässt sich der Weg auf der Karte ansehen.'],
  en: ['First version on the server: shared high scores with names and statistics in the settings as soon as the server’s service is running.', 'Tutorial “First flight”, new start page with a calm melody.', 'Sounding diagram with dew point below the vertical profile, side view with terrain, airspace as a switch below the instruments.', 'The fill of the envelope sets the drag: an empty balloon falls fast.', 'After landing you can view the track on the map.']}];
function newsOpen(){ const box = $('nw-rows'); box.textContent = ''; NEWS.forEach(n => { const h = document.createElement('h3'); h.textContent = 'Build ' + n.b; box.appendChild(h); (n[UI.lang] || n.en).forEach(t => { const p = document.createElement('p'); p.textContent = '• ' + t; box.appendChild(p); }); }); $('news').hidden = false; store.set('gb-news', BUILD); }
$('nw-btn').addEventListener('click', newsOpen); $('nw-close').addEventListener('click', () => { $('news').hidden = true; });
function newsAuto(){ const seen = store.get('gb-news', null); if (seen == null){ store.set('gb-news', BUILD); return; } if (seen !== BUILD && NEWS[0].b === BUILD && STATE === 'menu') newsOpen(); }   // nach einem Update einmal von selbst zeigen; bei der ersten Nutzung nicht

/* ---------- Rollhinweis (NFA-07) ---------- */''')
f.rep('<button class="sm" id="in-btn" data-i="in_title"></button>','<button class="sm" id="in-btn" data-i="in_title"></button><button class="sm" id="nw-btn" data-i="news_title"></button>')
f.rep('    <!-- Statistik für alle (SRV-07)','''    <!-- Was ist neu (INS-06) -->
    <div class="full" id="news" hidden>
      <div class="card">
        <h2 data-i="news_title"></h2>
        <div id="nw-rows"></div>
        <button class="sec" id="nw-close" data-i="close"></button>
      </div>
    </div>

    <!-- Statistik für alle (SRV-07)''')
f.rep("#stats{z-index:950}","#news{z-index:950}\n#news .card{width:min(480px,100%);max-height:calc(100% - 8px);overflow:auto;padding:14px;background:#0d1626}\n#nw-rows h3{margin:12px 0 4px;font-size:15px;color:var(--orb)}\n#nw-rows p{margin:0 0 5px;font-size:13.5px;line-height:1.4}\n#stats{z-index:950}")
f.rep("['.mcard', '#sheet', '#startwin .card', '#setup .card', '#info .card', '#chal .card', '#detail .card']","['.mcard', '#sheet', '#startwin .card', '#setup .card', '#info .card', '#chal .card', '#detail .card', '#news .card', '#stats .card']")
f.rep("  HERO.reset(); $('m-tut').classList.toggle('new', !store.get('gb-tut', 0)); setState('menu');","  HERO.reset(); $('m-tut').classList.toggle('new', !store.get('gb-tut', 0)); setState('menu'); setTimeout(() => { if (typeof newsAuto === 'function') newsAuto(); }, 1200);")
# Tutorial: alles ausgefahren
f.rep("  TUT.on = true; TUT.i = 0; TUT.hide.forEach(","  FOLD.p = 0; FOLD.i = 0; FOLD.b = 0; foldApply(false);                      // im Tutorial sind alle Fenster ausgefahren\n  TUT.on = true; TUT.i = 0; TUT.hide.forEach(")
f.rep("const BUILD = '2026-10-10.7'","const BUILD = '2026-10-11.1'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v39'" in s; open(p,'w').write(s.replace("'v39'","'v40'"))
