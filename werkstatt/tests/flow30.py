from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); print('Build',ev('BUILD'),'| Neuigkeiten beim ersten Start von selbst:',not ev("$('news').hidden"))
    # Rollhinweis: Schrift und Lage des Menüs bleiben gleich
    a=ev("(()=>{const m=document.querySelector('.mcard'),s=getComputedStyle(m);return [s.fontSize,s.paddingLeft,m.classList.contains('scrl-more')]})()"); ev("document.querySelector('.mcard').scrollTop=9999"); pg.wait_for_timeout(700); b2=ev("(()=>{const m=document.querySelector('.mcard'),s=getComputedStyle(m);return [s.fontSize,s.paddingLeft,m.classList.contains('scrl-more'),m.scrollTop>0]})()"); print('Menü oben',a,'| unten',b2)
    ev("store.set('gb-news','2026-10-10.7'); showMenu()"); pg.wait_for_timeout(1800); print('nach Update von selbst:',not ev("$('news').hidden"),'|',ev("$('nw-rows').textContent")[:120]); pg.screenshot(path='j_news.png'); pg.click('#nw-close')
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500)
    for i in range(2): pg.click('#rack'); pg.wait_for_timeout(200)
    mh=lambda: ev("Math.round(document.querySelector('main').getBoundingClientRect().height)")
    print('Kartenhöhe offen',mh()); pg.screenshot(path='j_open.png')
    pg.click('#panel-h'); pg.wait_for_timeout(200); print(' Bedienfeld zu:',mh(),'|',ev("$('panel-sum').textContent")); pg.click('#prof-h'); pg.wait_for_timeout(200); print(' Profil zu, Breite',ev("Math.round($('prof').getBoundingClientRect().width)"))
    hh=lambda: ev("Math.round($('inst').getBoundingClientRect().height)"); q0=hh(); pg.click('#inst-h'); pg.wait_for_timeout(150); q1=hh(); pg.click('#inst-h'); pg.wait_for_timeout(150); q2=hh(); print(' Anzeigen Höhe voll/mittel/kurz',q0,q1,q2,'| Schalter Lufträume folgt:',ev("$('ofm-btn').style.top")); pg.screenshot(path='j_shut.png')
    print(' gespeichert:',ev("JSON.stringify(store.get('gb-fold'))")); pg.click('#inst-h'); pg.click('#panel-h'); pg.click('#prof-h'); pg.wait_for_timeout(200); print(' wieder offen:',mh(),hh())
    print('Symbol prall:',ev("balloonSVG('#f',1).match(/d=\"([^\"]+)\"/)[1]")); print('Symbol 40 %:',ev("balloonSVG('#f',0.4).match(/d=\"([^\"]+)\"/)[1]"))
    ev("B.gas*=0.45; B.h=800; B.air=true"); pg.wait_for_timeout(400); print('Füllgrad',ev('Math.round(fillNow()*100)'),'| Symbolstufe',ev('balMk._fq'))
    ev("document.body.insertAdjacentHTML('beforeend','<div id=demo style=\"position:fixed;left:110px;top:300px;z-index:9999;background:#234;padding:6px\">'+[1,.8,.6,.4,.2,0].map(f=>balloonSVG('#ff9f1c',f)).join('')+'</div>')"); pg.wait_for_timeout(200); pg.screenshot(path='j_icons.png',clip={'x':100,'y':290,'width':260,'height':80}); ev("$('demo').remove()")
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
    # Querformat
    b=p.chromium.launch(); c=b.new_context(viewport={'width':740,'height':360},locale='de-DE'); pg=c.new_page(); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev=lambda s: pg.evaluate(s)
    ev("store.set('gb-news',BUILD)"); pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500); mw=lambda: ev("Math.round(document.querySelector('main').getBoundingClientRect().width)")
    print('Querformat: Kartenbreite offen',mw()); pg.screenshot(path='j_land1.png'); pg.click('#panel-h'); pg.wait_for_timeout(250); print(' Bedienfeld zu',mw()); pg.screenshot(path='j_land2.png'); b.close()
