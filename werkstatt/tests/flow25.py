from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    print('Build',ev('BUILD'),'| Menü:',ev("[...document.querySelectorAll('.mcard .mbtn')].map(x=>x.querySelector('b').textContent.trim()).join(' / ')"),'| Tutorial hervorgehoben:',ev("$('m-tut').classList.contains('new')"))
    r=ev("(()=>{const a=$('m-beer').getBoundingClientRect(),hh=$('hero').getBoundingClientRect(),m=document.querySelector('.mcard');return [Math.round(hh.height),Math.round(a.bottom),innerHeight,m.scrollHeight,m.clientHeight]})()"); print('Bildhöhe, Unterkante Bier-Knopf, Fensterhöhe, Menü Inhalt/sichtbar',r)
    pg.screenshot(path='f_menu1.png'); pg.wait_for_timeout(5000); pg.screenshot(path='f_menu2.png'); pg.wait_for_timeout(9500); pg.screenshot(path='f_menu3.png')
    pg.mouse.click(180,150); pg.wait_for_timeout(1500); print('Musik läuft:',ev("typeof SND.music"),)
    # Tutorial
    pg.click('#m-tut'); pg.wait_for_timeout(800); vis=lambda: ev("TUT.hide.filter(id=>$(id).style.visibility!=='hidden').join(',')")
    step=lambda: (ev('TUT.i+1'), ev("$('tut-text').textContent")[:70], 'sichtbar: '+vis(), 'Hand' if not ev("$('tut-hand').hidden") else '', 'Weiter' if not ev("$('tut-next').hidden") else 'wartet')
    print(step()); pg.screenshot(path='f_tut1.png'); pg.click('#tut-next'); pg.wait_for_timeout(300); print(step()); pg.screenshot(path='f_tut2.png')
    n=0
    while ev('TUT.i')==1 and n<8: pg.click('#rack'); n+=1; pg.wait_for_timeout(400)
    print(' Säcke',n); print(step()); pg.click('#seg-speed button[data-v="10"]',force=True) if False else ev('UI.speed=10'); pg.wait_for_function('!$("tut-next").hidden',timeout=30000); ev('UI.speed=1'); print(' Weiter erst ab 30 m: Höhe',ev('Math.round(B.h)')); pg.click('#tut-next'); print(step()); pg.click('#tut-next'); print(step()); pg.click('#tut-next'); print(step()); pg.screenshot(path='f_tut5.png')
    pg.click('#scoop'); pg.wait_for_timeout(400); print(step()); pg.click('#tut-next'); print(step())
    ev("valve=0.6"); pg.wait_for_timeout(2200); ev("valve=0"); pg.wait_for_timeout(300); print(step()); pg.click('#tut-next'); print(step()); pg.screenshot(path='f_tut9.png'); pg.click('#tut-next'); print(step())
    pg.click('#rope'); pg.wait_for_timeout(400); print(' Tau ohne Rückfrage:',ev('B.rope'),ev("$('confirm').hidden")); print(step())
    ev("window.__v=setInterval(()=>{valve=B.landed?0:1},50);0"); pg.click("#seg-speed button[data-v=\"10\"]"); pg.wait_for_function('B.landed',timeout=60000); ev("clearInterval(__v);valve=0"); pg.wait_for_timeout(600); print(step()); pg.screenshot(path='f_tut12.png'); pg.click('#tut-next'); pg.wait_for_timeout(300)
    print('beendet:',not ev('TUT.on'),'gemerkt:',ev("store.get('gb-tut',0)"),'| alles wieder sichtbar:',vis()==','.join(ev('TUT.hide')),'| Ergebnisfenster:',not ev("$('result').hidden"))
    ev("showMenu()"); pg.wait_for_timeout(500); print('Menü: Tutorial hervorgehoben:',ev("$('m-tut').classList.contains('new')"))
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
