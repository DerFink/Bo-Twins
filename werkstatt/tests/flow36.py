from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':780,'height':360},locale='de-DE',device_scale_factor=2); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(800)
    pg.screenshot(path='p_ap_quer.png')
    ev("tutStart()"); pg.wait_for_timeout(800); print('Tutorial: AP versteckt', ev("$('ap-btn').hidden"), 'Fehler', errs); b.close()
