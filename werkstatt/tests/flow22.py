from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(3000)
    print('Build',ev('BUILD'),'| Namenshinweis:',ev("document.querySelector('.mhint').textContent"))
    print('Wertung: 40 m',ev('scoreLanding(40,0.5,3000)'),'| 60 m',ev('scoreLanding(60,0.5,3000)'),'| 300 m',ev('scoreLanding(300,0.5,3000)'),'| 40 m mit 2,4 m/s',ev('scoreLanding(40,2.4,3000)'),'| 40 m mit 2,6 m/s',ev('scoreLanding(40,2.6,3000)'),'| Kreis',ev('ZONE_R'))
    pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.wait_for_timeout(300)
    print('Aufgabe:',ev("$('sw-target').textContent")[:170]); print('Streifen:',ev('GB.strips.length'),'Gewicht bei Zoom 13 (px):',ev("GB.strips.length?Math.round(2*11000/(156543.03392*Math.cos(GB.strips[0].lat*Math.PI/180)/Math.pow(2,13))):0"))
    pg.click('#sw-go'); pg.wait_for_timeout(300); print('Platz-Zeile vor dem Start sichtbar:',not ev("$('row-rank').hidden")); n=0
    while not ev('B.go') and n<12: pg.click('#rack'); n+=1; pg.wait_for_timeout(150)
    pg.wait_for_timeout(300); print('nach dem Loslassen:',ev("$('row-rank').textContent"))
    ev("window.__k=setInterval(()=>{ if(STATE==='play'&&!B.landed&&window.__hold){B.h=1200;B.w=0;} },5);window.__hold=true;0"); pg.click('#seg-speed button[data-v="500"]')
    for i in range(4): pg.wait_for_timeout(9000); print(' ',ev("fmtT(B.t)"),ev('gbKm().toFixed(0)'),'km →',ev("$('i-rank').textContent"))
    pg.screenshot(path='c_play.png')
    ev("window.__hold=false; B.h=B.gnd+3; B.w=-3.2; 0"); pg.wait_for_function("B.landed",timeout=30000); pg.wait_for_timeout(500); print('harte Landung:',ev('B.vLand.toFixed(1)'),'|',ev("$('r-head').textContent"),'| Liste',ev("JSON.stringify(gbList().map(e=>[e.km,e.dq]))")); pg.screenshot(path='c_res.png')
    ev("showMenu()"); pg.wait_for_timeout(300)
    # Zielfahren mit harter Landung
    pg.click('#m-chal'); pg.wait_for_timeout(300); ev("document.querySelector('[data-task=\"target\"]')&&document.querySelector('[data-task=\"target\"]').click()"); pg.wait_for_timeout(300)
    print('Zustand',ev('STATE'),ev('UI.mode'))
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
