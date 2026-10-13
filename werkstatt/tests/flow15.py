from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
FAKE="""(v => { const of = window.fetch; window.__f = 0; window.fetch = (u, o) => String(u).includes('index.html') ? (window.__f++, Promise.resolve(new Response("x const BUILD = '" + v + "'; y"))) : of(u, o); })"""
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    def page():
        c=b.new_context(viewport={'width':390,'height':844},locale='de-DE'); pg=c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); return pg
    pg=page(); ev=lambda s: pg.evaluate(s)
    ev(FAKE+"(BUILD)"); ev("UPDATE.check(true)"); pg.wait_for_timeout(300); print('gleiche Version auf dem Server: Fenster',not ev("$('confirm').hidden"))
    ev(FAKE+"('2026-10-08.14')"); ev("UPDATE.check(true)"); pg.wait_for_timeout(300); print('ältere Version auf dem Server: Fenster',not ev("$('confirm').hidden"))
    ev(FAKE+"('2026-12-01.1')"); ev("UPDATE.check(true)"); pg.wait_for_timeout(300)
    print('neuere Version: Fenster',not ev("$('confirm').hidden"),'|',ev("$('cf-text').textContent"),'| Knöpfe:',ev("[$('cf-ok').textContent,$('cf-no').textContent]")); pg.screenshot(path='u_win.png')
    pg.click('#cf-no'); ev("UPDATE.check(true)"); pg.wait_for_timeout(300); print('nach „Später“ erneut geprüft: Fenster',not ev("$('confirm').hidden"))
    pg.context.close()
    # während der Fahrt
    pg=page(); ev=lambda s: pg.evaluate(s)
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
    ev(FAKE+"('2026-11-01.1')"); ev("UPDATE.check(true)"); pg.wait_for_timeout(300); print('in der Fahrt: Fenster',not ev("$('confirm').hidden"))
    pg.click('#btn-menu'); pg.wait_for_timeout(300); print('zurück im Menü: Fenster',not ev("$('confirm').hidden"),'|',ev("$('cf-text').textContent"))
    ev("window.__r=0; reloadApp=async()=>{window.__r++}; 0")
    pg.click('#cf-ok'); pg.wait_for_timeout(300); print('„Version aktualisieren“ löst das Neuladen aus:',ev('window.__r')==1)
    pg.evaluate("openSheet(true)"); print('Hinweis:',pg.evaluate("document.querySelector('[data-i=about3]').textContent")); pg.evaluate("document.querySelector('[data-i=about3]').scrollIntoView()")
    pg.evaluate("$('cf-no').textContent"); print('Rückfrage sonst: Knopf heißt',pg.evaluate("(confirmBox('x','ok'), $('cf-no').textContent)"))
    print('Fehler:',errs); b.close()
