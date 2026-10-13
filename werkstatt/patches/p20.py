import re,sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---------- 1. Bodencrew hält den Ballon, bis er deutlich leichter als Luft ist ----------
f.rep("  markKg: 0.07 ","  holdKg: 30,      // kg Auftriebsüberschuss, ab dem die Bodencrew den Ballon loslässt (Vorgabe Nutzer: rund 30 kg, zwei Säcke)\n  markKg: 0.07 ")
f.rep("  B.free = free;\n","""  B.free = free;
  if (!B.air && !B.go){                                                    // Start (STE-22): Die Bodencrew hält den Ballon am Boden fest, bis er eindeutig leichter als Luft ist
    if (free < (cfg.holdKg || 0)){ B.held = true; B.Tg = B.Tf = a.T; B.w = 0; B.acc = 0; B.h = B.gnd; return; }
    B.go = true; B.held = false;
  }
""")
f.rep("  if (B.h <= 0 && !B.air && hSoll > 0){ dropKg(B, cfg, Math.max(need, 2)); return; }","  if (B.h <= 0 && !B.air && hSoll > 0){ dropKg(B, cfg, Math.max(need, 2, B.go ? 0 : (cfg.holdKg || 0) + 1 - B.free)); return; }   // am Start so viel, dass die Bodencrew loslässt")
f.rep("  else if (agl <= 0 && !B.air && !B.landed){ hint.hidden = false; hint.textContent = tr('hint_start'); }","""  else if (agl <= 0 && !B.air && !B.landed && !B.go){ hint.hidden = false; hint.textContent = tr('hint_hold', {kg: nf(CFG.holdKg), rest: nf(Math.max(0, CFG.holdKg - (B.free || 0)), 1)}); heldSeen = true; }
  else if (heldSeen && B.go){ heldSeen = false; hint.hidden = true; toast(tr('hold_go')); }""")
f.rep("function updInst(","let heldSeen = false;\nfunction updInst(")
T={'de':("hint_hold:'Die Bodencrew hält den Ballon, bis er {kg} kg leichter als Luft ist (zwei Säcke). Noch {rest} kg abwerfen.'","hold_go:'Die Crew lässt los'"),
 'en':("hint_hold:'The ground crew holds the balloon until it is {kg} kg lighter than air (two bags). Drop another {rest} kg.'","hold_go:'The crew lets go'"),
 'fr':("hint_hold:'L’équipe au sol retient le ballon jusqu’à ce qu’il soit plus léger que l’air de {kg} kg (deux sacs). Encore {rest} kg à lâcher.'","hold_go:'L’équipe lâche le ballon'"),
 'pl':("hint_hold:'Obsługa naziemna trzyma balon, aż będzie o {kg} kg lżejszy od powietrza (dwa worki). Zrzuć jeszcze {rest} kg.'","hold_go:'Obsługa puszcza balon'"),
 'cs':("hint_hold:'Pozemní posádka drží balon, dokud není o {kg} kg lehčí než vzduch (dva pytle). Shoďte ještě {rest} kg.'","hold_go:'Posádka pouští balon'"),
 'zh-TW':("hint_hold:'地勤人員會拉住氣球，直到它比空氣輕 {kg} 公斤（兩袋沙）。還需拋下 {rest} 公斤。'","hold_go:'地勤放手了'"),
 'es':("hint_hold:'El equipo de tierra sujeta el globo hasta que sea {kg} kg más ligero que el aire (dos sacos). Suelta otros {rest} kg.'","hold_go:'El equipo suelta el globo'")}
order=['de','en','fr','pl','cs','zh-TW','es']; it=iter(order); n=[0]
def r(m): n[0]+=1; return m.group(1)+', '+', '.join(T[next(it)])+m.group(2)
f.s=re.sub(r"(inst_set:'[^']*')( \})",r,f.s); assert n[0]==7,n

# ---------- 2. Karte: eigenes Zoomen des Spielers bleibt erhalten ----------
f.rep("map.on('dragstart', () => { follow = false; introUntil = 0; if (STATE === 'play') $('follow').hidden = false; });","""// Alle Kartenbewegungen des Programms laufen über diese Aufrufe und sind dabei gekennzeichnet. Zoomt der Spieler selbst (Finger, Mausrad),
// stellt die Kamera den Ausschnitt nicht mehr von sich aus neu ein; sie hält nur noch den Ballon in der Mitte, bis „Zentrieren“ angetippt wird.
let autoMove = 0, userZoom = false;
['setView', 'flyTo', 'fitBounds', 'panTo'].forEach(k => { const o = map[k].bind(map); map[k] = (...a) => { autoMove++; try{ return o(...a); } finally { autoMove--; } }; });
map.on('zoomstart', () => { if (autoMove || STATE !== 'play') return; userZoom = true; introUntil = 0; $('follow').hidden = false; });
map.on('dragstart', () => { follow = false; introUntil = 0; if (STATE === 'play') $('follow').hidden = false; });""")
f.rep("$('follow').addEventListener('click', () => { follow = true; introUntil = 0;","$('follow').addEventListener('click', () => { follow = true; userZoom = false; introUntil = 0;")
f.rep("  follow = true; $('follow').hidden = true; $('result').hidden = true;","  follow = true; userZoom = false; $('follow').hidden = true; $('result').hidden = true;")
f.rep("  if (np && np.zoom && Math.hypot(np.e - B.e, np.n - B.n) < (wz ? 2500 : 8000)){","  if (!userZoom && np && np.zoom && Math.hypot(np.e - B.e, np.n - B.n) < (wz ? 2500 : 8000)){")
f.rep("setTimeout(() => { if (STATE === 'play' && !B.air) map.flyTo(","setTimeout(() => { if (STATE === 'play' && !B.air && !userZoom && follow && introUntil) map.flyTo(")
f.rep("const BUILD = '2026-10-08.14';","const BUILD = '2026-10-09.1';")
f.save()
