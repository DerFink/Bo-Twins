from playwright.sync_api import sync_playwright
import urllib.parse
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':720},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev("store.set('gb-news',BUILD)")
    pg.click('#m-champ'); pg.wait_for_timeout(200); pg.click('#gbsc-list .mbtn:nth-child(1)'); pg.wait_for_timeout(200); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    print('2026:',ev("[GB.sc.id,START.lat.toFixed(3),GB_TEAMS.length,GB.ban.length,$('sw-pv').hidden]"),REQ[-1].split('?')[0],'|',ev("$('sw-target').textContent")[:60])
    pg.click('#sw-go'); pg.wait_for_timeout(300); pg.click('#rack'); pg.click('#rack'); pg.click('#rack'); pg.wait_for_timeout(800)
    pg.click('#gb-save'); pg.wait_for_timeout(200); print('gespeichert unter gb-save69:',ev("!!store.get('gb-save69')"),'gb-save62:',ev("!!store.get('gb-save62')"))
    ev("showMenu()"); pg.wait_for_timeout(300); pg.click('#m-champ'); pg.wait_for_timeout(200); print('Fortsetzen-Zeile:',ev("[...document.querySelectorAll('#gbsc-list .res')].map(x=>x.textContent)"))
    print('Fehler',errs); b.close()
