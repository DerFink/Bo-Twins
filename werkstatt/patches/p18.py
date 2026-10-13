import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. Unterer Rand: Inhalt bleibt über den Systemtasten ----------
# Ohne viewport-fit=cover hält der Browser die Seite selbst aus dem Bereich der Systemleisten heraus; mit cover hing das von den
# gemeldeten Randabständen ab, die manche Android-Geräte in der installierten App mit 0 melden.
f.rep('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">','<meta name="viewport" content="width=device-width, initial-scale=1">')
f.rep('<meta name="mobile-web-app-capable" content="yes">\n','')
f.rep('<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">','<meta name="apple-mobile-web-app-status-bar-style" content="black">')
f.rep("#app{position:relative;width:100%;height:100vh;height:100dvh;","#app{position:relative;width:100%;height:100vh;height:100dvh;height:var(--apph,100dvh);")
f.rep("/* ---------- Installation als App (INS-04) ----------","""/* Höhe der App = sichtbare Höhe des Fensters, damit unten nichts hinter den Systemtasten oder der Adressleiste liegt */
function fitApp(){ const h = (window.visualViewport && visualViewport.height) || window.innerHeight; if (h > 100) document.documentElement.style.setProperty('--apph', Math.floor(Math.min(h, window.innerHeight || h)) + 'px'); if (typeof map !== 'undefined' && map.invalidateSize) map.invalidateSize(); }
fitApp(); window.addEventListener('resize', fitApp); window.addEventListener('orientationchange', () => setTimeout(fitApp, 300)); if (window.visualViewport) visualViewport.addEventListener('resize', fitApp);

/* ---------- Installation als App (INS-04) ----------""")
# ---------- 2. Knopf „Hauptmenü“ oben links, außerhalb des Hauptmenüs immer sichtbar ----------
f.rep('''      <div class="brand">
        <svg width="22"''','''      <button class="iconbtn" id="btn-menu" data-ia="menu" aria-label="Hauptmenü"><svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 11.5L12 4l8.5 7.5M6 10v9.5h4.2V14h3.6v5.5H18V10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      <div class="brand">
        <svg width="22"''')
f.rep("#app.inmenu #seg-speed{visibility:hidden}","#app.inmenu #seg-speed{visibility:hidden}\n#app.home #btn-menu{display:none}\n#app:not(.home) .brand svg{display:none}\n@media (max-width:440px){#app:not(.home) .brand{display:none}}")
f.rep("function setState(s){ STATE = s;","function setState(s){ STATE = s; $('app').classList.toggle('home', s === 'menu');")
f.rep("""$('set-menu').addEventListener('click', async () => {
  if (STATE === 'play' && B.air && !(await confirmBox(tr('cf_menu'), tr('cf_menu_ok')))) return;
  openSheet(false); showMenu();
});""","""async function goMenu(){                                   // Fahrt abbrechen und zurück ins Hauptmenü; in der Luft mit Rückfrage
  if (STATE === 'menu') return;
  if (STATE === 'play' && B.air && !B.landed && !(await confirmBox(tr('cf_menu'), tr('cf_menu_ok')))) return;
  if (typeof gpsStop === 'function') gpsStop();
  openSheet(false); $('result').hidden = true; showMenu();
}
$('set-menu').addEventListener('click', goMenu);
$('btn-menu').addEventListener('click', goMenu);""")
f.rep("const BUILD = '2026-10-08.12';","const BUILD = '2026-10-08.13';")
f.save()
