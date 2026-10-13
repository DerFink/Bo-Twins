import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. Vertikalbeschleunigung ----------
f.rep("    B.w = 0; B.h = B.gnd; return;","    B.w = 0; B.acc = 0; B.h = B.gnd; return;")
f.rep("  B.w += (G0 * free - k * B.w * Math.abs(B.w)) / mEff * dt;","  B.acc = (G0 * free - k * B.w * Math.abs(B.w)) / mEff;                    // m/s², Vertikalbeschleunigung (Anzeige am Vario)\n  B.w += B.acc * dt;")
f.rep('<div class="kv"><span>m/s</span><b id="i-vario">0,0</b></div>','<div class="kv" id="row-vario"><i id="i-acc" aria-hidden="true"></i><span>m/s</span><b id="i-vario">0,0</b></div>')
f.rep("#inst #i-vario{font-size:17px}","""#inst #i-vario{font-size:17px}
/* Balken der Vertikalbeschleunigung links neben dem Vario: wächst von der Mitte der Zeile nach oben (grün) oder nach unten (rot); bei 0 unsichtbar */
#row-vario{position:relative}
#i-acc{position:absolute;left:-6px;width:4px;height:0;border-radius:2px;pointer-events:none}
#i-acc.up{bottom:50%;background:var(--up)} #i-acc.dn{top:50%;background:var(--dn)}""")
f.rep("  const v = $('i-vario'); v.textContent = fmtV(B.w);","""  { const ac = (B.landed || !(agl > 0)) ? 0 : (B.acc || 0), el = $('i-acc'), px = Math.abs(ac) < 0.002 ? 0 : Math.max(2, Math.round(26 * Math.min(1, Math.sqrt(Math.abs(ac) / ACC_FULL))));   // Wurzelskala: kleine Werte bleiben sichtbar
    el.className = ac > 0 ? 'up' : 'dn'; el.style.height = px + 'px'; }
  const v = $('i-vario'); v.textContent = fmtV(B.w);""")
f.rep("const BUILD = '2026-10-08.10';","const BUILD = '2026-10-08.11';\nconst ACC_FULL = 0.25;   // m/s², Vertikalbeschleunigung, bei der der Balken am Vario voll ausschlägt (ein Sack von 15 kg ergibt rund 0,08)")
f.rep('    <p class="note lg"><i style="background:#ff9f1c;height:3px"></i><span data-i="lg_balloon"></span></p>','    <p class="note lg"><i style="background:#ff9f1c;height:3px"></i><span data-i="lg_balloon"></span></p>\n    <p class="note lg"><i style="background:linear-gradient(#5fe3a1 50%,#ff6e5f 50%);width:5px;height:16px;margin:0 5px"></i><span data-i="lg_acc"></span></p>')

# ---------- 2. Installationshinweis für Android und iOS ----------
f.rep('<link rel="apple-touch-icon" href="icon-192.png">','<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="Gasballon">')
f.rep('  <div id="toast" role="status" aria-live="polite"></div>','''  <!-- Hinweis zur Installation als App (Android: Installationsdialog des Browsers; iPhone und iPad: Anleitung für Safari) -->
  <div class="card" id="install" hidden>
    <img src="icon-192.png" alt="" width="40" height="40">
    <div class="itx"><b data-i="inst_t"></b><span id="inst-d"></span></div>
    <div class="ibt"><button class="sm" id="inst-later" data-i="inst_later"></button><button class="sm pri2" id="inst-ok" data-i="inst_ok"></button></div>
  </div>
  <div id="toast" role="status" aria-live="polite"></div>''')
f.rep("#toast.on{opacity:1;","""#install{position:absolute;left:8px;right:8px;bottom:max(8px,env(safe-area-inset-bottom));z-index:870;margin:0 auto;max-width:560px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;padding:10px 12px;background:rgba(13,22,38,.97);box-shadow:0 12px 30px rgba(0,0,0,.5)}
#install[hidden]{display:none}
#install img{flex:none;border-radius:9px}
#install .itx{flex:1;min-width:150px} #install .itx b{display:block;font-size:15px} #install .itx span{display:block;font-size:12.5px;color:var(--mut);line-height:1.35}
#install .ibt{display:flex;gap:8px;margin-left:auto}
button.pri2{background:var(--orb);border-color:var(--orb);color:#0a1019;font-weight:600}
#toast.on{opacity:1;""")
f.rep('<button class="sm" id="reload" data-i="reload"></button></p>','<button class="sm" id="reload" data-i="reload"></button> <button class="sm" id="inst-set" data-i="inst_set" hidden></button></p>')
f.rep("if (s !== 'play'){ SND.valve(0); SND.drag(0); setPaused(false); } SND.music(musicWanted()); }","if (s !== 'play'){ SND.valve(0); SND.drag(0); setPaused(false); } SND.music(musicWanted()); if (typeof INSTALL !== 'undefined') INSTALL.show(); }")
f.rep("if ('serviceWorker' in navigator && location.protocol === 'https:'){","""/* ---------- Installation als App (INS-04) ----------
   Android und Chrome am Rechner melden mit beforeinstallprompt, dass sich die App installieren lässt; „Installieren“ öffnet dann den Dialog des Browsers.
   iPhone und iPad kennen das nicht: Dort zeigt der Hinweis die Schritte in Safari. „Später“ blendet den Hinweis für 7 Tage aus. In der installierten App erscheint er nicht. */
const INSTALL = (() => {
  let ev = null, steps = false, forced = false;
  const ua = navigator.userAgent || '';
  const ios = /iphone|ipad|ipod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const android = /android/i.test(ua);
  const standalone = () => (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  const snoozed = () => Date.now() < store.get('gb-inst-later', 0);
  const possible = () => !standalone() && (!!ev || ios || android);
  function show(){
    const on = possible() && STATE === 'menu' && (forced || !snoozed());
    $('install').hidden = !on; $('inst-set').hidden = !possible();
    if (!on) return;
    $('inst-d').textContent = steps ? tr(ios ? 'inst_ios' : 'inst_other') : tr('inst_d');
    $('inst-ok').hidden = steps; $('inst-later').textContent = tr(steps ? 'close' : 'inst_later');
  }
  window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); ev = e; steps = false; show(); });
  window.addEventListener('appinstalled', () => { ev = null; forced = false; show(); toast(tr('inst_done')); });
  $('inst-ok').addEventListener('click', async () => {
    if (ev){ const e = ev; ev = null; try{ e.prompt(); await e.userChoice; }catch(x){} forced = false; store.set('gb-inst-later', Date.now() + 7 * 864e5); show(); }
    else { steps = true; show(); }
  });
  $('inst-later').addEventListener('click', () => { store.set('gb-inst-later', Date.now() + 7 * 864e5); steps = false; forced = false; show(); });
  $('inst-set').addEventListener('click', () => { forced = true; steps = !ev; openSheet(false); if (STATE !== 'menu') toast(tr(ios ? 'inst_ios' : ev ? 'inst_d' : 'inst_other')); if (STATE === 'menu') show(); else if (ev) $('inst-ok').click(); });
  return { show };
})();
INSTALL.show();

if ('serviceWorker' in navigator && location.protocol === 'https:'){""")
T={'de':("lg_acc:'Balken am Vario: Beschleunigung nach oben grün, nach unten rot; je länger, desto stärker'","inst_t:'Als App installieren'","inst_d:'Dann startet das Spiel vom Startbildschirm, auch ohne Netz.'","inst_ok:'Installieren'","inst_later:'Später'","inst_ios:'Auf iPhone und iPad in Safari: auf „Teilen“ tippen (Quadrat mit Pfeil nach oben), dann „Zum Home-Bildschirm“ wählen und mit „Hinzufügen“ bestätigen.'","inst_other:'Im Menü des Browsers (⋮) „App installieren“ oder „Zum Startbildschirm hinzufügen“ wählen.'","inst_done:'App installiert'","inst_set:'Zum Startbildschirm'"),
 'en':("lg_acc:'Bar at the vario: acceleration upwards green, downwards red; the longer, the stronger'","inst_t:'Install as an app'","inst_d:'The game then starts from the home screen, even without a connection.'","inst_ok:'Install'","inst_later:'Later'","inst_ios:'On iPhone and iPad in Safari: tap “Share” (square with an arrow pointing up), choose “Add to Home Screen” and confirm with “Add”.'","inst_other:'In the browser menu (⋮) choose “Install app” or “Add to Home screen”.'","inst_done:'App installed'","inst_set:'Add to home screen'"),
 'fr':("lg_acc:'Barre près du vario : accélération vers le haut en vert, vers le bas en rouge ; plus elle est longue, plus elle est forte'","inst_t:'Installer comme application'","inst_d:'Le jeu démarre alors depuis l’écran d’accueil, même sans réseau.'","inst_ok:'Installer'","inst_later:'Plus tard'","inst_ios:'Sur iPhone et iPad dans Safari : touchez « Partager » (carré avec une flèche vers le haut), choisissez « Sur l’écran d’accueil » puis confirmez avec « Ajouter ».'","inst_other:'Dans le menu du navigateur (⋮), choisissez « Installer l’application » ou « Ajouter à l’écran d’accueil ».'","inst_done:'Application installée'","inst_set:'Sur l’écran d’accueil'"),
 'pl':("lg_acc:'Słupek przy wariometrze: przyspieszenie w górę zielone, w dół czerwone; im dłuższy, tym silniejsze'","inst_t:'Zainstaluj jako aplikację'","inst_d:'Gra uruchamia się wtedy z ekranu głównego, także bez sieci.'","inst_ok:'Zainstaluj'","inst_later:'Później'","inst_ios:'Na iPhonie i iPadzie w Safari: dotknij „Udostępnij” (kwadrat ze strzałką w górę), wybierz „Do ekranu początkowego” i potwierdź przyciskiem „Dodaj”.'","inst_other:'W menu przeglądarki (⋮) wybierz „Zainstaluj aplikację” lub „Dodaj do ekranu głównego”.'","inst_done:'Aplikacja zainstalowana'","inst_set:'Do ekranu głównego'"),
 'cs':("lg_acc:'Sloupec u variometru: zrychlení nahoru zeleně, dolů červeně; čím delší, tím silnější'","inst_t:'Nainstalovat jako aplikaci'","inst_d:'Hra se pak spouští z domovské obrazovky, i bez připojení.'","inst_ok:'Nainstalovat'","inst_later:'Později'","inst_ios:'Na iPhonu a iPadu v Safari: klepněte na „Sdílet“ (čtverec se šipkou nahoru), zvolte „Přidat na plochu“ a potvrďte tlačítkem „Přidat“.'","inst_other:'V nabídce prohlížeče (⋮) zvolte „Instalovat aplikaci“ nebo „Přidat na plochu“.'","inst_done:'Aplikace nainstalována'","inst_set:'Na domovskou obrazovku'"),
 'zh-TW':("lg_acc:'升降表旁的長條：向上加速為綠色，向下為紅色；越長表示越強'","inst_t:'安裝為 App'","inst_d:'之後可從主畫面啟動遊戲，沒有網路也能開啟。'","inst_ok:'安裝'","inst_later:'稍後'","inst_ios:'在 iPhone 和 iPad 的 Safari 中：點一下「分享」（帶向上箭頭的方框），選擇「加入主畫面」，再點「加入」確認。'","inst_other:'在瀏覽器選單（⋮）中選擇「安裝應用程式」或「加到主畫面」。'","inst_done:'App 已安裝'","inst_set:'加入主畫面'"),
 'es':("lg_acc:'Barra junto al variómetro: aceleración hacia arriba en verde, hacia abajo en rojo; cuanto más larga, más fuerte'","inst_t:'Instalar como aplicación'","inst_d:'El juego se inicia entonces desde la pantalla de inicio, también sin conexión.'","inst_ok:'Instalar'","inst_later:'Más tarde'","inst_ios:'En iPhone y iPad con Safari: toca «Compartir» (cuadrado con una flecha hacia arriba), elige «Añadir a pantalla de inicio» y confirma con «Añadir».'","inst_other:'En el menú del navegador (⋮) elige «Instalar aplicación» o «Añadir a pantalla de inicio».'","inst_done:'Aplicación instalada'","inst_set:'A la pantalla de inicio'")}
order=['de','en','fr','pl','cs','zh-TW','es']; it=iter(order); n=[0]
def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[next(it)])+m.group(2)
f.s=re.sub(r"(toast_valve:'[^']*')( \})",r,f.s); assert n[0]==7
f.save()
