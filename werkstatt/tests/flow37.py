from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':360,'height':720},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(800)
    print('1000 m³ Hinweis:', ev("$('hint').textContent"))
    ev("CFG=Object.assign({},CFG,{vol:400,pax:2,rust:100,envKg:60})"); ev("B=newBalloon(CFG,ATM)"); pg.wait_for_timeout(500)
    print('400 m³ Hinweis:', ev("$('hint').textContent"), '| Tutorialtext:', ev("tutText('sacks').slice(0,120)"))
    print('Fehler', errs); b.close()
