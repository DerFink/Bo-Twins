from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(3000)
    print('Build',ev('BUILD'),'| Meisterschaft-Text:',ev("document.querySelector('#m-champ > span').textContent"))
    r=ev("(()=>{const a=$('m-beer').getBoundingClientRect();return [Math.round(a.top),Math.round(a.bottom),innerHeight]})()"); print('Bier-Knopf Lage',r)
    pg.click('#m-beer'); pg.wait_for_timeout(200); print('Text:',ev("$('beer-text').textContent")); print(' Platzhalter',ev("$('beer-in').placeholder"),'| Link',ev("$('beer-go').href"),'| QR',ev("$('beer-cv').width"))
    pg.fill('#beer-in','5,5'); print(' 5,5 ->',ev("$('beer-go').href")); pg.fill('#beer-in','0.01'); print(' 0.01 ->',ev("$('beer-go').href")); pg.fill('#beer-in','abc'); print(' abc ->',ev("$('beer-go').href")); pg.fill('#beer-in','')
    pg.screenshot(path='b_beer.png'); pg.locator('#beer-cv').screenshot(path='b_qr.png'); pg.click('#beer-close')
    pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.wait_for_timeout(300)
    print('Aufgabe:',ev("$('sw-target').textContent")); print('Vorschau-Knöpfe:',ev("[...document.querySelectorAll('#sw-pv button')].map(x=>x.textContent)")); pg.screenshot(path='b_brief.png')
    pg.click('#sw-pv button[data-pv="max"]'); pg.wait_for_timeout(1500); print('Vorflug:',ev("$('pv-head').textContent"),'| läuft',ev('PV.play'),'| Startfenster zu',ev("$('startwin').hidden")); print(' ',ev("$('pv-read').textContent"))
    pg.wait_for_timeout(3000); print(' ',ev("$('pv-read').textContent")); ev("(()=>{const e=$('pv-pos');e.value=700;e.dispatchEvent(new Event('input'))})()"); print(' Regler 70 %:',ev("$('pv-read').textContent"),'| angehalten',not ev('PV.play')); print(' Hinweis:',ev("$('pv-leg').textContent")); pg.screenshot(path='b_pv.png')
    ev("(()=>{const e=$('pv-pos');e.value=1000;e.dispatchEvent(new Event('input'))})()"); print(' Ende:',ev("$('pv-read').textContent"))
    pg.click('#pv-close'); print(' zurück im Startfenster:',not ev("$('startwin').hidden"),ev("$('pv').hidden"),'Schichten entfernt',ev("PV.line===null"))
    pg.click('#sw-pv button[data-pv="kons"]'); pg.wait_for_timeout(500); print('Konservativ:',ev("$('pv-head').textContent")); pg.click('#pv-close')
    pg.click('#sw-go'); pg.wait_for_timeout(300); n=0
    while not ev('B.go') and n<12: pg.click('#rack'); n+=1; pg.wait_for_timeout(150)
    print('losgelassen nach',n,'Säcken')
    ev("window.__k=setInterval(()=>{ if(STATE==='play'&&!B.landed&&window.__hold){B.h=1200;B.w=0;} },5);window.__hold=true;0")
    pg.click('#seg-speed button[data-v="500"]'); pg.wait_for_timeout(6000); print('Fahrt bis',ev("fmtT(B.t)"),'Zwischenstände',ev('GB.snaps.length'),'km',ev('gbKm().toFixed(0)'))
    # Zeitbremse in Bodennähe
    ev("window.__hold=false; B.h=B.gnd+200; B.w=-0.6; 0"); t0=ev('B.t'); pg.wait_for_timeout(500); t1=ev('B.t'); print('Zeitbremse: %.0f s Spielzeit in 0,5 s (500x wären 250)'%(t1-t0),'| Hinweis',ev("$('toast').textContent") if ev("!!$('toast')") else '')
    ev("valve=1"); pg.wait_for_function("B.landed",timeout=60000); ev("valve=0"); pg.wait_for_timeout(600); tl=ev('B.t')
    print('gelandet bei',ev("fmtT(B.t)"),'| Zurück-Knopf sichtbar',not ev("$('r-rewind').hidden"),ev("$('r-rewind').textContent"),'| Liste',ev("gbList().length")); pg.screenshot(path='b_res.png')
    pg.click('#r-rewind'); pg.wait_for_timeout(500); print('zurückgespult auf',ev("fmtT(B.t)"),'(%.0f min zurück)'%((tl-ev('B.t'))/60),'| Zustand',ev('STATE'),'Pause',ev('PAUSED'),'gelandet',ev('B.landed'),'Höhe',ev('Math.round(B.h)'),'| Liste',ev("gbList().length"),'| Ergebnis zu',ev("$('result').hidden"))
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
