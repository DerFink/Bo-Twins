import sys
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add
f=F()
f.rep("routes: false, story: 'gb62_story'","routes: false, ready: false, story: 'gb62_story'")   # gesperrt, bis ein Wetterpaket aus ERA5 (Copernicus) vorliegt: das Open-Meteo-Archiv liefert für 2018 keine Höhenwerte
f.rep("    b.addEventListener('click', () => gbScGo(s.id)); box.appendChild(b); });",
"""    if (s.ready === false){ const r = document.createElement('span'); r.className = 'res'; r.textContent = tr('gbsc_prep'); b.appendChild(r); b.disabled = true; b.classList.add('off'); }
    else b.addEventListener('click', () => gbScGo(s.id));
    box.appendChild(b); });""")
f.rep("#gbsc .mbtn .res{color:var(--warn);margin-top:2px}","#gbsc .mbtn .res{color:var(--warn);margin-top:2px}\n#gbsc .mbtn.off{opacity:.55;cursor:default}")
f.rep("async function gbScGo(id){\n  $('gbsc').hidden = true; gbUse(id);","async function gbScGo(id){\n  if (GB_SC[id] && GB_SC[id].ready === false) return;\n  $('gbsc').hidden = true; gbUse(id);")
tx_add(f,{'gbsc_prep':['In Vorbereitung: Das Wetter von 2018 in der Höhe fehlt noch.','In preparation: the 2018 upper-air weather is still missing.','En préparation : la météo en altitude de 2018 manque encore.','W przygotowaniu: brakuje jeszcze danych wysokościowych z 2018 r.','Připravuje se: výšková data počasí z roku 2018 zatím chybí.','準備中：2018 年的高空天氣資料尚未取得。','En preparación: aún faltan los datos de altura de 2018.']})
f.rep("const NEWS = [\n {b: '2026-10-26.2', de: [","const NEWS = [\n {b: '2026-10-26.3', de: ['Der Gordon Bennett 2018 ist vorerst gesperrt: Für 2018 fehlt das Wetter in der Höhe. Er kommt wieder, sobald ein Wetterpaket aus der Reanalyse ERA5 vorliegt.'],\n  en: ['The Gordon Bennett 2018 is locked for now: the upper-air weather for 2018 is missing. It returns once a weather package from the ERA5 reanalysis is ready.']},\n {b: '2026-10-26.2', de: [")
f.rep("const BUILD = '2026-10-26.2'","const BUILD = '2026-10-26.3'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v49'" in s; open(p,'w').write(s.replace("'v49'","'v50'"))
print('ok')
