import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# Musik leiser
f.rep("mus.g.gain.value = 0.3; mus.g.connect(master);","mus.g.gain.value = 0.16; mus.g.connect(master);")
f.rep("g.setValueAtTime(0.3, t0); g.setValueAtTime(0.3, t0 + 8); g.linearRampToValueAtTime(0.14, t0 + 14);","g.setValueAtTime(0.16, t0); g.setValueAtTime(0.16, t0 + 8); g.linearRampToValueAtTime(0.07, t0 + 14);")
# Online-Dienst: liegt neben der App ein Dienst (api/api.php), wird er benutzt; sonst bleibt alles auf dem Gerät
f.rep("const ONLINE = {api: ''};                                  // zum Beispiel 'https://example.org/gasballon/api.php'",
"""const ONLINE = {api: '', probe: './api/api.php', ready: null};   // api wird gesetzt, sobald der Dienst neben der App antwortet (auf GitHub gibt es keinen, dort bleibt alles auf dem Gerät)
function onlineInit(){
  if (ONLINE.ready) return ONLINE.ready;
  ONLINE.ready = (async () => {
    if (!/^https?:$/.test(location.protocol)) return false;
    const ac = new AbortController(), to = setTimeout(() => ac.abort(), 5000);
    try{ const r = await fetch(ONLINE.probe + '?action=ping', {signal: ac.signal, cache: 'no-store'}); if (!r.ok) return false; const j = await r.json(); if (j && j.ok === true){ ONLINE.api = ONLINE.probe; return true; } return false; }
    catch(e){ return false; } finally { clearTimeout(to); }
  })();
  ONLINE.ready.then(ok => { if (!ok) setTimeout(() => { if (!ONLINE.api) ONLINE.ready = null; }, 60000); });   // ohne Antwort später noch einmal versuchen
  return ONLINE.ready;
}""")
f.rep("    const r = await fetch(ONLINE.api + '?action=' + action, body ?","    const r = await fetch(ONLINE.api + '?action=' + action, body ? ")
f.rep("function onlineScore(e){ if (ONLINE.api) onlineCall('score', Object.assign({id: uid(), build: BUILD}, e)).catch(() => {}); }",
"function onlineScore(e){ onlineInit().then(ok => { if (ok) onlineCall('score', Object.assign({id: uid(), build: BUILD}, e)).catch(() => {}); }); }\nfunction onlineUnscore(at){ onlineInit().then(ok => { if (ok && at) onlineCall('unscore', {id: uid(), at}).catch(() => {}); }); }")
f.rep("applyLang(); applyTiles(); renderSand(true); showMenu(); onlineVisit();","applyLang(); applyTiles(); renderSand(true); showMenu(); onlineInit().then(ok => { if (ok) onlineVisit(); });")
# Listen
f.rep("  if (scKind === 'gb'){                                    // Liste „69. Gordon Bennett“: alle Fahrten dieses Geräts, auch mehrere je Spieler\n    const g = gbList();",
"  if (scKind === 'gb'){                                    // Liste „69. Gordon Bennett“: mit Dienst alle Fahrten aller Spieler, sonst die dieses Geräts\n    let g = gbList(), gfail = false;\n    if (await onlineInit()){ try{ const r = await onlineCall('top&kind=gb'); if (Array.isArray(r)) g = r; else gfail = true; }catch(e){ gfail = true; } if (STATE !== 'scores' || scKind !== 'gb') return; box.textContent = ''; }\n    if (gfail){ const q = document.createElement('p'); q.className = 'note'; q.textContent = tr('sc_online_fail'); box.appendChild(q); }")
f.rep("  if (ONLINE.api){ try{ const r = await onlineTop();","  if (await onlineInit()){ try{ const r = await onlineTop();")
f.rep("if (STATE !== 'scores') return; box.textContent = ''; }\n  if (fail)","if (STATE !== 'scores' || scKind === 'gb') return; box.textContent = ''; }\n  if (fail)")
f.rep("  store.set('gb-list69', gbList().filter(e => e.at !== GB.lastAt));","  store.set('gb-list69', gbList().filter(e => e.at !== GB.lastAt)); onlineUnscore(GB.lastAt);")
f.rep("const BUILD = '2026-10-09.9'","const BUILD = '2026-10-09.10'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read()
a="  if (url.origin === location.origin) { e.respondWith(shell(req)); return; }"; assert s.count(a)==1
s=s.replace(a,"  if (url.origin === location.origin && url.pathname.includes('/api/')) return;   // Dienst für die Bestenliste: immer direkt ins Netz, nie aus dem Zwischenspeicher\n"+a).replace("'v31'","'v32'"); open(p,'w').write(s)
