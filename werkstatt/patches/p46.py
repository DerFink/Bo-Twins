import sys, json, re
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add, tx_get, tx_set
f=F()
T62=open('/tmp/claude-0/gb18/teams62.json').read()
# ---------- Wetter: vor 2022 aus dem Open-Meteo-Archiv (ERA5) ----------
f.rep("  return (hist ? 'https://historical-forecast-api.open-meteo.com' : 'https://api.open-meteo.com') + '/v1/forecast?latitude=' + lat.toFixed(2)",
      "  return (hist ? (hist < Date.UTC(2022, 0, 1) ? 'https://archive-api.open-meteo.com/v1/archive' : 'https://historical-forecast-api.open-meteo.com/v1/forecast') : 'https://api.open-meteo.com/v1/forecast') + '?latitude=' + lat.toFixed(2)")   # vor 2022 (Gordon Bennett 2018): Reanalyse ERA5 aus dem Archiv
# ---------- Szenarien ----------
f.rep("const GB_TEAMS = [[","const GB_TEAMS69 = [[")
f.rep("const GB_BAN_NAMES = new Set(['Somaliland']);","""const GB_BAN_NAMES = new Set(['Somaliland']);
/* 62. Gordon Bennett 2018, Bern (offizielles Endergebnis). Teamnummern sind nur für die ersten vier belegt, sonst steht das Land allein. Die Landepunkte liegen
   in Richtung des genannten Ortes genau in der offiziellen Entfernung vom angenommenen Startplatz; für „Le Peyrat“ ist der Ort nicht eindeutig, deshalb ohne Punkt.
   Rang 15: Ergebnisseite AUS, Ergebnis-PDF USA; übernommen AUS. */
const GB_TEAMS62 = """+T62+""";
/* Szenarien der Meisterschaft (Wunsch Nutzer 26.10.2026). 2018: Startzeit 19:00 MESZ und Berner Allmend sind Annahmen; keine gesperrten Länder, Wasserlandung disqualifiziert. */
const GB_SC = {
  gb69: {id: 'gb69', start: {lat: 51 + 33.460 / 60, lon: 6 + 58.373 / 60, alt: 50, kind: 'gb'}, t0: Date.UTC(2026, 7, 29, 0, 45, 0), teams: GB_TEAMS69, ban: GB_BAN, banNames: GB_BAN_NAMES, routes: true, story: 'gb_story', save: 'gb-save69', list: 'gb-list69'},
  gb62: {id: 'gb62', start: {lat: 46.958, lon: 7.462, alt: 550, kind: 'gb'}, t0: Date.UTC(2018, 8, 28, 17, 0, 0), teams: GB_TEAMS62, ban: new Set(), banNames: new Set(), routes: false, story: 'gb62_story', save: 'gb-save62', list: 'gb-list62'}
};
let GB_TEAMS = GB_TEAMS69;
function gbUse(id){ const s = GB_SC[id] || GB_SC.gb69; GB.sc = s; GB.start = s.start; GB.t0 = s.t0; GB_TEAMS = s.teams;
  if (UI.gbsc !== s.id){ UI.gbsc = s.id; saveUI(); }
  if (GB.polys) GB.ban = GB.polys.filter(p => s.ban.has(p.id) || s.banNames.has(p.name)); }
gbUse(UI.gbsc);
/* Eigenes Team: frei wählbares Land (IOC-Kürzel) oder ohne Land, dann nur der Name (Wunsch Nutzer 26.10.2026, ersetzt JAM-1 CoolRidings) */
const GB_CTRY = ('ALB:AL,AND:AD,ARG:AR,ARM:AM,AUS:AU,AUT:AT,AZE:AZ,BEL:BE,BIH:BA,BLR:BY,BRA:BR,BUL:BG,CAN:CA,CHI:CL,CHN:CN,CRO:HR,CYP:CY,CZE:CZ,DEN:DK,EGY:EG,ESP:ES,EST:EE,FIN:FI,FRA:FR,GBR:GB,GEO:GE,GER:DE,GRE:GR,HUN:HU,INA:ID,IND:IN,IRL:IE,ISL:IS,ISR:IL,ITA:IT,JAM:JM,JPN:JP,KAZ:KZ,KOR:KR,LAT:LV,LIE:LI,LTU:LT,LUX:LU,MAR:MA,MAS:MY,MDA:MD,MEX:MX,MKD:MK,MLT:MT,MNE:ME,MON:MC,NED:NL,NOR:NO,NZL:NZ,PHI:PH,POL:PL,POR:PT,ROU:RO,RSA:ZA,RUS:RU,SGP:SG,SLO:SI,SMR:SM,SRB:RS,SUI:CH,SVK:SK,SWE:SE,THA:TH,TPE:TW,TUN:TN,TUR:TR,UAE:AE,UKR:UA,USA:US,VIE:VN').split(',').map(s => s.split(':'));
const flagOf = iso2 => iso2 ? String.fromCodePoint(...[...iso2].map(c => 0x1F1E6 + c.charCodeAt(0) - 65)) : '';
function ctryName(ioc){ const p = GB_CTRY.find(c => c[0] === ioc); if (!p) return ioc; try{ return new Intl.DisplayNames([UI.lang, 'en'], {type: 'region'}).of(p[1]); }catch(e){ return ioc; } }
function gbMe(){ const c = UI.ctry || '', p = GB_CTRY.find(x => x[0] === c); if (!p) return {code: '', flag: ''};
  return {code: c + '-' + (GB_TEAMS.filter(t => t[0].split('-')[0] === c).length + 1), flag: flagOf(p[1])}; }""")
# Ländergrenzen: Sperrliste je Szenario
f.rep("all.push({rings, box: [x0, y0, x1, y1], ban: GB_BAN.has(c.id) || GB_BAN_NAMES.has(c.name), name: c.name});","all.push({rings, box: [x0, y0, x1, y1], id: c.id, name: c.name});")
f.rep("  if (!all.some(p => p.ban)) return false;\n  GB.polys = all; GB.ban = all.filter(p => p.ban); return true;","  if (all.length < 100) return false;\n  GB.polys = all; gbUse(GB.sc.id); return true;")
# Speicherstände und Listen je Szenario
f.s=f.s.replace("store.get('gb-save69', null)","store.get(GB.sc.save, null)").replace("store.set('gb-save69',","store.set(GB.sc.save,")
f.rep("store.set('gb-list69', gbList().filter(","store.set(GB.sc.list, gbList().filter(")
f.rep("const gbList = () => { const a = store.get('gb-list69', []);","const gbList = sc => { const a = store.get((sc || GB.sc).list, []);")
f.rep("store.set('gb-list69', a.slice(0, 500));","store.set(GB.sc.list, a.slice(0, 500));")
assert 'gb-save69' not in f.s.replace("save: 'gb-save69'",'') and 'gb-list69' not in f.s.replace("list: 'gb-list69'",''), 'Reste'
# Auswertung
f.rep("  const ahead = GB_TEAMS.filter(t => t[2] > km).length, rank = GB.dq ? null : ahead + 1, name = (UI.name || '').trim() || 'Pilot';",
      "  const ahead = GB_TEAMS.filter(t => t[2] > km).length, rank = GB.dq ? null : ahead + 1, name = (UI.name || '').trim() || 'Pilot', me = gbMe(), nT = GB_TEAMS.length + 1;")
f.s=f.s.replace("tr('gb_of', {r: rank})","tr('gb_of', {r: rank, n: nT})")
f.rep("const e = {n: name, km:","const e = {n: (me.code ? me.code + ' · ' : '') + name, km:")
f.rep("onlineScore(Object.assign({c: 'gb69', p:","onlineScore(Object.assign({c: GB.sc.id, p:")
f.rep("cheerQ = GB.dq ? 0 : Math.max(0.1, 1 - ahead / 24);","cheerQ = GB.dq ? 0 : Math.max(0.1, 1 - ahead / nT);")
f.rep("list.splice(ahead, 0, {r: rank, team: 'JAM-1', who: 'CoolRidings · ' + name, km, me: true});","list.splice(ahead, 0, {r: rank, team: me.code ? me.flag + ' ' + me.code : '–', who: name, km, me: true});")
f.rep("me: GB.dq ? {team: 'JAM-1', who: 'CoolRidings · ' + name, km} : null};","me: GB.dq ? {team: me.code ? me.flag + ' ' + me.code : '–', who: name, km} : null};")
f.rep("tr('i-rank') ","tr('i-rank') ") if "tr('i-rank') " in f.s else None
f.rep("tg = tr('gb_story');","tg = tr(GB.sc.story);")
f.rep("$('sw-pv').hidden = k !== 'gb';","$('sw-pv').hidden = k !== 'gb' || !GB.sc.routes;")
# eigenes Team an der Karte
f.rep("function gbUndraw(){ GB.strips = [];","function gbUndraw(){ if (balMk.getTooltip()) balMk.unbindTooltip(); GB.strips = [];")
f.rep("  GB_TEAMS.forEach((t, i) => {\n    add(L.circleMarker(","  { const me = gbMe(); if (me.code) balMk.bindTooltip(me.flag + ' ' + me.code, {permanent: true, direction: 'right', offset: [14, -30], className: 'ptip gbtip'}); }\n  GB_TEAMS.forEach((t, i) => { if (t[5] == null) return;\n    add(L.circleMarker(")
# Bestenliste: zwei Reiter für die Rennen
f.rep('<button data-v="gb" data-i="gb_list"></button></div>','<button data-v="gb" data-i="gb_list"></button><button data-v="gb62" data-i="gb_list62"></button></div>')
f.rep("  if (scKind === 'gb'){                                    // Liste „69. Gordon Bennett“","  if (scKind === 'gb' || scKind === 'gb62'){ const sk = scKind, sc = sk === 'gb62' ? GB_SC.gb62 : GB_SC.gb69;   // Listen der Rennen")
f.rep("    let g = gbList(), gfail = false;\n    if (await onlineInit()){ try{ const r = await onlineCall('top&kind=gb'); if (Array.isArray(r)) g = r; else gfail = true; }catch(e){ gfail = true; } if (STATE !== 'scores' || scKind !== 'gb') return;",
      "    let g = gbList(sc), gfail = false;\n    if (await onlineInit()){ try{ const r = await onlineCall('top&kind=gb&c=' + sc.id); if (Array.isArray(r)) g = r; else gfail = true; }catch(e){ gfail = true; } if (STATE !== 'scores' || scKind !== sk) return;")
f.rep("e.dq ? 'DSQ' : tr('gb_of', {r: e.rank})], 'td'));","e.dq ? 'DSQ' : tr('gb_of', {r: e.rank, n: sc.teams.length + 1})], 'td'));")
f.rep("if (STATE !== 'scores' || scKind === 'gb') return; box.textContent = ''; }","if (STATE !== 'scores' || scKind !== 'chal') return; box.textContent = ''; }")
# Auswahlfenster
f.rep('  <div class="full" id="confirm" role="alertdialog" aria-modal="true" hidden>','''  <div class="full" id="gbsc" role="dialog" aria-modal="true" hidden>
    <div class="card">
      <h2 data-i="gbsc_t"></h2>
      <p class="note" data-i="gbsc_d"></p>
      <div id="gbsc-list"></div>
      <label class="gbsc-c"><span data-i="gbsc_ctry"></span><select id="gbsc-ctry"></select></label>
      <p class="note" data-i="gbsc_ctry_n"></p>
      <button class="sec" id="gbsc-no" data-i="back"></button>
    </div>
  </div>
  <div class="full" id="confirm" role="alertdialog" aria-modal="true" hidden>''')
f.rep("#confirm{z-index:1000}","""#confirm{z-index:1000}
#gbsc{z-index:950}
#gbsc .mbtn b{display:block;font-family:var(--num);font-size:19px}
#gbsc .mbtn span{display:block;font-size:13px;line-height:1.3;color:var(--mut)}
#gbsc .mbtn .res{color:var(--warn);margin-top:2px}
.gbsc-c{display:flex;align-items:center;gap:8px;margin-top:12px;font-size:14px}
.gbsc-c select{flex:1;min-width:0;min-height:40px;border-radius:10px;border:1px solid var(--line);background:#0d1626;color:var(--tx);font:inherit;padding:0 8px}""")
f.rep("""$('m-champ').addEventListener('click', async () => {
  const s = store.get(GB.sc.save, null);
  if (s && s.B && s.START && await confirmBox(tr('gb_resume_q', {km: nf(s.km || 0, 0), t: fmtT(s.B.t)}), tr('gb_resume'), tr('gb_new'))) return gbResume(s);
  if (!(await confirmBox(tr('gb_data'), tr('gb_go'), tr('back')))) return;
  UI.mode = 'champ'; saveUI(); prepareRun();
});""","""function gbScOpen(){                                   // Auswahl des Rennens und des eigenen Landes
  const box = $('gbsc-list'); box.textContent = '';
  Object.values(GB_SC).forEach(s => { const b = document.createElement('button'), sv = store.get(s.save, null), t = document.createElement('b'), d = document.createElement('span');
    b.className = 'mbtn'; t.textContent = tr(s.id + '_t'); d.textContent = tr(s.id + '_d'); b.append(t, d);
    if (sv && sv.B){ const r = document.createElement('span'); r.className = 'res'; r.textContent = tr('gbsc_res', {km: nf(sv.km || 0, 0), t: fmtT(sv.B.t)}); b.appendChild(r); }
    b.addEventListener('click', () => gbScGo(s.id)); box.appendChild(b); });
  const sel = $('gbsc-ctry'); sel.textContent = ''; sel.add(new Option(tr('gbsc_none'), ''));
  GB_CTRY.map(c => [c[0], ctryName(c[0]), flagOf(c[1])]).sort((a, b) => a[1].localeCompare(b[1], UI.lang)).forEach(c => sel.add(new Option(c[2] + ' ' + c[1] + ' (' + c[0] + ')', c[0])));
  sel.value = UI.ctry || ''; $('gbsc').hidden = false;
}
async function gbScGo(id){
  $('gbsc').hidden = true; gbUse(id);
  const s = store.get(GB.sc.save, null);
  if (s && s.B && s.START && await confirmBox(tr('gb_resume_q', {km: nf(s.km || 0, 0), t: fmtT(s.B.t)}), tr('gb_resume'), tr('gb_new'))) return gbResume(s);
  if (!(await confirmBox(tr('gb_data'), tr('gb_go'), tr('back')))) return;
  UI.mode = 'champ'; saveUI(); prepareRun();
}
$('m-champ').addEventListener('click', gbScOpen);
$('gbsc-no').addEventListener('click', () => { $('gbsc').hidden = true; });
$('gbsc-ctry').addEventListener('change', e => { UI.ctry = e.target.value; saveUI(); });""")
# ---------- Texte ----------
g=tx_get(f,'gb_of'); tx_set(f,'gb_of',[m.group(1).replace('24','{n}') for m in g])
tx_set(f,'m_champ_d',['Echte Gordon-Bennett-Rennen mit dem Wetter von damals nachfahren: 2026 ab Gladbeck, 2018 ab Bern. Inoffizielles Fan-Projekt.',
 'Fly real Gordon Bennett races with the weather of the day: 2026 from Gladbeck, 2018 from Bern. Unofficial fan project.',
 'Refaire de vraies courses Gordon Bennett avec la météo de l’époque : 2026 depuis Gladbeck, 2018 depuis Berne. Projet de fans non officiel.',
 'Przeleć prawdziwe wyścigi Gordona Bennetta z ówczesną pogodą: 2026 z Gladbeck, 2018 z Berna. Nieoficjalny projekt fanów.',
 'Zopakujte skutečné závody Gordona Bennetta s tehdejším počasím: 2026 z Gladbecku, 2018 z Bernu. Neoficiální fanouškovský projekt.',
 '以當時的天氣重飛真實的戈登·貝內特賽：2026 年自格拉德貝克、2018 年自伯恩起飛。非官方愛好者專案。',
 'Repite carreras Gordon Bennett reales con el tiempo de entonces: 2026 desde Gladbeck, 2018 desde Berna. Proyecto no oficial de aficionados.'])
tx_set(f,'gb_list',['Gordon Bennett 2026']*5+['戈登·貝內特 2026','Gordon Bennett 2026'])
tx_add(f,{
 'gb_list62':['Gordon Bennett 2018']*5+['戈登·貝內特 2018','Gordon Bennett 2018'],
 'gbsc_t':['Meisterschaft','Championship','Championnat','Mistrzostwa','Mistrovství','錦標賽','Campeonato'],
 'gbsc_d':['Fahre ein echtes Gordon-Bennett-Rennen mit dem Wetter von damals nach. Inoffizielles Fan-Projekt.','Fly a real Gordon Bennett race with the weather of the day. Unofficial fan project.','Refais une vraie course Gordon Bennett avec la météo de l’époque. Projet de fans non officiel.','Przeleć prawdziwy wyścig Gordona Bennetta z ówczesną pogodą. Nieoficjalny projekt fanów.','Zaleť si skutečný závod Gordona Bennetta s tehdejším počasím. Neoficiální fanouškovský projekt.','以當時的天氣重飛一場真實的戈登·貝內特賽。非官方愛好者專案。','Vuela una carrera Gordon Bennett real con el tiempo de entonces. Proyecto no oficial de aficionados.'],
 'gb69_t':['69. Gordon Bennett 2026','69th Gordon Bennett 2026','69e Gordon Bennett 2026','69. Gordon Bennett 2026','69. Gordon Bennett 2026','第 69 屆戈登·貝內特 2026','69.º Gordon Bennett 2026'],
 'gb69_d':['Start Gladbeck · 29.08.2026 · 23 Teams · Sieger 1555 km bis Finnland','Launch Gladbeck · 29 Aug 2026 · 23 teams · winner 1555 km to Finland','Départ Gladbeck · 29.08.2026 · 23 équipes · vainqueur 1555 km jusqu’en Finlande','Start Gladbeck · 29.08.2026 · 23 zespoły · zwycięzca 1555 km do Finlandii','Start Gladbeck · 29. 8. 2026 · 23 týmů · vítěz 1555 km do Finska','格拉德貝克起飛 · 2026/08/29 · 23 隊 · 冠軍 1555 公里至芬蘭','Salida Gladbeck · 29/08/2026 · 23 equipos · ganador 1555 km hasta Finlandia'],
 'gb62_t':['62. Gordon Bennett 2018','62nd Gordon Bennett 2018','62e Gordon Bennett 2018','62. Gordon Bennett 2018','62. Gordon Bennett 2018','第 62 屆戈登·貝內特 2018','62.º Gordon Bennett 2018'],
 'gb62_d':['Start Bern · 28.09.2018 · 20 Teams · Sieger 1145 km bis Polen, andere über die Alpen nach Italien oder nach Frankreich','Launch Bern · 28 Sep 2018 · 20 teams · winner 1145 km to Poland, others over the Alps to Italy or to France','Départ Berne · 28.09.2018 · 20 équipes · vainqueur 1145 km jusqu’en Pologne, d’autres par les Alpes vers l’Italie ou vers la France','Start Berno · 28.09.2018 · 20 zespołów · zwycięzca 1145 km do Polski, inni przez Alpy do Włoch lub do Francji','Start Bern · 28. 9. 2018 · 20 týmů · vítěz 1145 km do Polska, jiní přes Alpy do Itálie nebo do Francie','伯恩起飛 · 2018/09/28 · 20 隊 · 冠軍 1145 公里至波蘭，其他隊越過阿爾卑斯山到義大利或飛往法國','Salida Berna · 28/09/2018 · 20 equipos · ganador 1145 km hasta Polonia, otros por los Alpes a Italia o a Francia'],
 'gbsc_res':['Fortsetzen: {km} km, {t}','Resume: {km} km, {t}','Reprendre : {km} km, {t}','Kontynuuj: {km} km, {t}','Pokračovat: {km} km, {t}','繼續：{km} 公里，{t}','Continuar: {km} km, {t}'],
 'gbsc_ctry':['Land','Country','Pays','Kraj','Země','國家','País'],
 'gbsc_none':['ohne Land','no country','sans pays','bez kraju','bez země','不選國家','sin país'],
 'gbsc_ctry_n':['Mit Land startest du als nächstes Team dieses Landes, zum Beispiel GER-4, und das Kürzel steht an deinem Ballon. Ohne Land erscheint nur dein Name.','With a country you start as its next team, for example GER-4, and the code is shown at your balloon. Without a country only your name appears.','Avec un pays, tu pars comme sa prochaine équipe, par exemple GER-4, et le code s’affiche près de ton ballon. Sans pays, seul ton nom apparaît.','Z krajem startujesz jako jego kolejny zespół, np. GER-4, a skrót widać przy balonie. Bez kraju pojawia się tylko twoje imię.','Se zemí startuješ jako její další tým, např. GER-4, a zkratka je u tvého balonu. Bez země se zobrazí jen tvé jméno.','選了國家，你就以該國的下一隊出發，例如 GER-4，代碼顯示在你的氣球旁。不選國家則只顯示你的名字。','Con país sales como su siguiente equipo, por ejemplo GER-4, y el código aparece junto a tu globo. Sin país solo aparece tu nombre.'],
 'gb62_story':['Nachfahrt des 62. Coupe Aéronautique Gordon Bennett. 20 Teams sind am Abend des 28. September 2018 in Bern gestartet, du fährst als 21. Team hinterher. Startzeit (19 Uhr) und Startplatz (Berner Allmend) sind angenommen. Es gibt keine gesperrten Länder, eine Landung im Wasser disqualifiziert. Wer am weitesten vom Startplatz landet, gewinnt.',
  'Re-flight of the 62nd Coupe Aéronautique Gordon Bennett. 20 teams launched in Bern on the evening of 28 September 2018; you follow as the 21st team. Launch time (7 pm) and site (Bern Allmend) are assumed. No countries are closed; a landing in water disqualifies. Whoever lands farthest from the launch site wins.',
  'Reconstitution de la 62e Coupe Aéronautique Gordon Bennett. 20 équipes sont parties de Berne le soir du 28 septembre 2018 ; tu suis comme 21e équipe. L’heure (19 h) et le lieu de départ (Allmend de Berne) sont supposés. Aucun pays n’est interdit ; un atterrissage dans l’eau disqualifie. Le plus loin du départ gagne.',
  'Powtórka 62. Coupe Aéronautique Gordon Bennett. 20 zespołów wystartowało w Bernie wieczorem 28 września 2018; lecisz jako 21. zespół. Godzina (19:00) i miejsce startu (Berner Allmend) są przyjęte. Żaden kraj nie jest zamknięty; lądowanie w wodzie dyskwalifikuje. Wygrywa ten, kto wyląduje najdalej od startu.',
  'Opakování 62. Coupe Aéronautique Gordon Bennett. 20 týmů odstartovalo v Bernu večer 28. září 2018; letíš jako 21. tým. Čas (19:00) a místo startu (Berner Allmend) jsou předpokládané. Žádná země není uzavřena; přistání ve vodě diskvalifikuje. Vyhrává, kdo přistane nejdál od startu.',
  '重飛第 62 屆戈登·貝內特盃。20 隊於 2018 年 9 月 28 日晚間自伯恩起飛，你以第 21 隊跟隨。起飛時間（19 時）與地點（伯恩 Allmend）為假設。沒有封閉的國家；降落在水中即取消資格。離起飛點最遠者獲勝。',
  'Repetición de la 62.ª Coupe Aéronautique Gordon Bennett. 20 equipos salieron de Berna la tarde del 28 de septiembre de 2018; tú sigues como equipo 21. La hora (19:00) y el lugar de salida (Allmend de Berna) son supuestos. No hay países cerrados; aterrizar en el agua descalifica. Gana quien aterrice más lejos de la salida.']})
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-26.1', de: ['Meisterschaft mit Szenarien: Neu ist der 62. Gordon Bennett 2018 ab Bern, mit den 20 echten Teams und dem Wetter von damals (Reanalyse ERA5). Startzeit und Startplatz sind angenommen, gesperrte Länder gibt es keine. Ein Vorflug fehlt dort noch.', 'Statt „JAM-1 CoolRidings“ startest du mit deinem Namen; wer will, wählt ein Land und fährt dann zum Beispiel als GER-4.', 'Die Bestenliste hat einen eigenen Reiter für 2018.'],
  en: ['Championship with scenarios: new is the 62nd Gordon Bennett 2018 from Bern, with the 20 real teams and the weather of the day (ERA5 reanalysis). Launch time and site are assumed, no countries are closed. There is no pre-flight for it yet.', 'Instead of “JAM-1 CoolRidings” you fly under your own name; if you like, choose a country and fly as, for example, GER-4.', 'The high scores have their own tab for 2018.']},
""")
f.rep("const BUILD = '2026-10-13.1'","const BUILD = '2026-10-26.1'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v47'" in s; open(p,'w').write(s.replace("'v47'","'v48'"))
print('ok')
