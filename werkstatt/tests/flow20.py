from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(3000)
    print('Menü:',ev("[...document.querySelectorAll('.mcard .mbtn')].map(x=>x.querySelector('b').textContent.trim()+' — '+x.querySelector(':scope > span').textContent)"),'|',ev("document.querySelector('.mhint').textContent")); pg.screenshot(path='r_menu.png')
    # Simulation: Anzeige, Profil, Rückblick
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
    print('Hinweis:',ev("$('hint').textContent"),'| Himmel:',ev("[$('i-skyl').textContent,$('i-sky').textContent,$('i-temp').textContent]"),'| Rückblick-Knopf vor dem Abheben sichtbar:',not ev("$('rv-btn').hidden"))
    pg.click('#rack'); pg.click('#rack'); pg.click('#seg-speed button[data-v="30"]'); pg.wait_for_timeout(5000)
    for i in range(20): pg.click('#scoop') if ev("!!$('scoop')") else None
    pg.wait_for_timeout(3000); ev("valve=0.4"); pg.wait_for_timeout(250); ev("valve=0"); pg.wait_for_timeout(9000)
    print('Aufzeichnung:',ev("REC.t.length"),'Sätze, bis',ev("fmtT(B.t)"),'| Knopf sichtbar',not ev("$('rv-btn').hidden"))
    pg.click('#rv-btn'); pg.wait_for_timeout(300); print('Rückblick offen, angehalten:',ev('PAUSED'),'|',ev("$('rv-read').textContent")); print(' ',ev("$('rv-why').textContent")); pg.screenshot(path='r_rev.png')
    box=pg.locator('#rv-cv').bounding_box(); pg.mouse.click(box['x']+box['width']*0.45, box['y']+60); pg.wait_for_timeout(150); print(' Zeiger gesetzt:',ev("$('rv-read').textContent")[:70]); print(' ',ev("$('rv-why').textContent"))
    pg.click('#rv-span button[data-v="0"]'); pg.wait_for_timeout(150); pg.click('#rv-close'); print(' geschlossen, läuft weiter:',not ev('PAUSED')); pg.screenshot(path='r_play.png')
    ev("showMenu()")
    # Meisterschaft: Zeitraffer
    pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
    r=ev("(()=>{const s=$('seg-speed').getBoundingClientRect(),t=$('btn-set').getBoundingClientRect(),m=$('btn-menu').getBoundingClientRect();return [Math.round(m.right),Math.round(s.left),Math.round(s.right),Math.round(t.left),innerWidth]})()")
    print('Meisterschaft Kopf:',ev("[...document.querySelectorAll('#seg-speed button')].filter(x=>getComputedStyle(x).display!=='none').map(x=>x.textContent.trim()||'II')"),'| Menü bis',r[0],'Zeitraffer',r[1],'bis',r[2],'Einstellungen ab',r[3],'Breite',r[4])
    print(' Hinweis:',ev("$('hint').textContent"),'| Himmel',ev("[$('i-skyl').textContent,$('i-sky').textContent,$('i-temp').textContent]"))
    n=0
    while not ev('B.go') and n<12: pg.click('#rack'); n+=1; pg.wait_for_timeout(150)
    print(' losgelassen nach',n,'Säcken'); ev("window.__k=setInterval(()=>{ if(STATE==='play'&&!B.landed){B.h=1200;B.w=0;} },5);0")
    pg.click('#seg-speed button[data-v="500"]'); t0=ev('B.t'); pg.wait_for_timeout(1000); t1=ev('B.t'); pg.dispatch_event('#btn-500','pointerdown',{'pointerId':1}); pg.wait_for_timeout(1000); t2=ev('B.t'); pg.dispatch_event('#btn-500','pointerup',{'pointerId':1}); pg.wait_for_timeout(1000); t3=ev('B.t')
    print(' 500× fest: %.0f s/s | 1000× gedrückt: %.0f s/s | danach wieder: %.0f s/s'%(t1-t0,t2-t1,t3-t2),'| Uhr',ev("[$('tm-val').textContent,$('i-sky').textContent]")); pg.screenshot(path='r_gb.png')
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
