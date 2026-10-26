from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':720},locale='de-DE',device_scale_factor=2); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev("store.set('gb-news',BUILD)")
    pg.click('#m-champ'); pg.wait_for_timeout(300); pg.screenshot(path='/mnt/user-data/outputs/Szenario_Auswahl_gesperrt.png')
    pg.click('#gbsc-list .mbtn:nth-child(2)',force=True); pg.wait_for_timeout(300); print('nach Tipp auf 2018: Fenster offen',not ev("$('gbsc').hidden"),'STATE',ev('STATE'))
    pg.click('#gbsc-list .mbtn:nth-child(1)'); pg.wait_for_timeout(200); print('2026 Rückfrage:',ev("$('cf-text').textContent")[:40]); print('Fehler',errs); b.close()
