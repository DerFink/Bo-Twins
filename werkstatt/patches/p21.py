import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. Hinweis: nicht kommerziell, privater Gebrauch ----------
f.rep('    <p class="note" data-i="about2"></p>','    <p class="note" data-i="about3"></p>\n    <p class="note" data-i="about2"></p>')
# ---------- 2. Fenster „Neue Version“ ----------
f.rep("function confirmBox(text, okLabel){ $('cf-text').textContent = text; $('cf-ok').textContent = okLabel; $('confirm').hidden = false;","function confirmBox(text, okLabel, noLabel){ $('cf-text').textContent = text; $('cf-ok').textContent = okLabel; $('cf-no').textContent = noLabel || tr('cancel'); $('confirm').hidden = false;")
f.block("$('reload').addEventListener('click', async () => {","/* Höhe der App = sichtbare Höhe",
"""async function reloadApp(){                               // Service Worker und Zwischenspeicher der App verwerfen, dann neu laden
  try{ if ('serviceWorker' in navigator){ for (const r of await navigator.serviceWorker.getRegistrations()) if (r.scope.endsWith('/spiel/') || r.scope === new URL('./', location.href).href) await r.unregister(); }
       if (window.caches){ for (const k of await caches.keys()) if (k.startsWith('gb-shell')) await caches.delete(k); } }catch(e){}
  location.reload();
}
$('reload').addEventListener('click', reloadApp);

/* ---------- Neue Version (INS-05) ----------
   Die App liest die Build-Nummer der Datei auf dem Server und vergleicht sie mit der laufenden: kurz nach dem Start, wenn die App wieder in den
   Vordergrund kommt und alle 30 Minuten. Liegt dort eine neuere, erscheint ein Fenster mit „Version aktualisieren“ und „Später“.
   Während einer Fahrt stört es nicht; es kommt, sobald die Fahrt zu Ende ist. Nach „Später“ meldet es sich beim nächsten Start wieder. */
const UPDATE = (() => {
  let found = null, last = 0, later = null, open = false;
  const num = v => String(v).split(/[^0-9]+/).filter(Boolean).map(Number);
  const newer = (a, b) => { const x = num(a), y = num(b); for (let i = 0; i < Math.max(x.length, y.length); i++){ const d = (x[i] || 0) - (y[i] || 0); if (d) return d > 0; } return false; };
  async function check(force){
    if (location.protocol !== 'https:' && !force) return;
    if (!force && Date.now() - last < 60000) return; last = Date.now();
    try{
      const r = await fetch(new URL('./index.html', location.href).href + '?v=' + Date.now(), {cache: 'no-store'}); if (!r.ok) return;
      const m = /const BUILD = '([^']+)'/.exec(await r.text()); if (m && newer(m[1], BUILD)) found = m[1];
    }catch(e){}
    show();
  }
  async function show(){
    if (!found || found === later || open || STATE === 'play' || STATE === 'busy' || !$('confirm').hidden) return;
    open = true; const ok = await confirmBox(tr('upd_text', {neu: found, alt: BUILD}), tr('upd_ok'), tr('upd_later')); open = false;
    if (ok) reloadApp(); else later = found;
  }
  setTimeout(check, 5000); setInterval(check, 30 * 60000);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') check(); });
  return { check, show };
})();

""")
f.rep("if (typeof INSTALL !== 'undefined') INSTALL.show(); }","if (typeof INSTALL !== 'undefined') INSTALL.show(); if (typeof UPDATE !== 'undefined') UPDATE.show(); }")
T={'de':("about3:'Diese App ist nicht kommerziell und nur für den privaten Gebrauch bestimmt. Nutzung auf eigene Verantwortung, ohne Gewähr.'","upd_text:'Eine neue Version ist verfügbar: {neu}. Auf diesem Gerät läuft {alt}.'","upd_ok:'Version aktualisieren'","upd_later:'Später'"),
 'en':("about3:'This app is non-commercial and intended for private use only. Use at your own risk, without warranty.'","upd_text:'A new version is available: {neu}. This device is running {alt}.'","upd_ok:'Update version'","upd_later:'Later'"),
 'fr':("about3:'Cette application est non commerciale et réservée à un usage privé. Utilisation à vos propres risques, sans garantie.'","upd_text:'Une nouvelle version est disponible : {neu}. Cet appareil utilise la version {alt}.'","upd_ok:'Mettre à jour la version'","upd_later:'Plus tard'"),
 'pl':("about3:'Ta aplikacja jest niekomercyjna i przeznaczona wyłącznie do użytku prywatnego. Korzystanie na własną odpowiedzialność, bez gwarancji.'","upd_text:'Dostępna jest nowa wersja: {neu}. Na tym urządzeniu działa {alt}.'","upd_ok:'Zaktualizuj wersję'","upd_later:'Później'"),
 'cs':("about3:'Tato aplikace je nekomerční a určena pouze pro soukromé použití. Používání na vlastní odpovědnost, bez záruky.'","upd_text:'Je k dispozici nová verze: {neu}. Na tomto zařízení běží {alt}.'","upd_ok:'Aktualizovat verzi'","upd_later:'Později'"),
 'zh-TW':("about3:'本 App 為非商業用途，僅供個人使用。使用風險自負，不提供任何保證。'","upd_text:'有新版本可用：{neu}。此裝置目前執行的是 {alt}。'","upd_ok:'更新版本'","upd_later:'稍後'"),
 'es':("about3:'Esta aplicación no es comercial y está destinada únicamente al uso privado. Uso bajo tu propia responsabilidad, sin garantía.'","upd_text:'Hay una nueva versión disponible: {neu}. En este dispositivo se ejecuta {alt}.'","upd_ok:'Actualizar versión'","upd_later:'Más tarde'")}
order=['de','en','fr','pl','cs','zh-TW','es']; it=iter(order); n=[0]
def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[next(it)])+m.group(2)
f.s=re.sub(r"(hold_go:'[^']*')( \})",r,f.s); assert n[0]==7,n
f.rep("const BUILD = '2026-10-09.1';","const BUILD = '2026-10-09.2';")
f.save()
