from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0]); stub=open('stub2.js').read()
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':390,'height':844},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    pg.click('#m-chal'); pg.click('#chal [data-task="target"]'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(600)
    print('Start:',ev("$('hint').textContent")); pg.screenshot(path='h_hold.png')
    pg.click('#rack'); pg.wait_for_timeout(500); print('ein Sack:',ev("$('hint').textContent"),'| Höhe',ev('B.h'),'| Weg',ev('Math.hypot(B.e,B.n).toFixed(1)'),'| Balken',ev("$('i-acc').style.height"))
    pg.click('#rack'); pg.wait_for_timeout(700); print('zwei Säcke: Hinweis sichtbar',not ev("$('hint').hidden"),'| Meldung:',ev("$('toast').textContent"),'| los',ev('B.go'),'| Steigen',ev('B.w.toFixed(2)'))
    # Kamera: während der Einführung selbst zoomen
    n0=ev("JSON.stringify(__calls)"); ev("__map.__userZoom()"); pg.wait_for_timeout(2500)
    print('Zoom des Spielers während der Einführung: userZoom',ev('userZoom'),'| Kartenfahrt danach gestartet:',ev("__calls.flyTo"),'| Knopf Zentrieren sichtbar',not ev("$('follow').hidden"))
    ev("B.h=300;B.air=true;0"); pg.wait_for_timeout(500); a=ev("__calls.setView"); pg.wait_for_timeout(1500); bq=ev("__calls.setView"); pa=ev("__calls.panTo")
    print('in der Fahrt nach eigenem Zoom: Zoom-Eingriffe der Kamera in 1,5 s:',bq-a,'| Ballon bleibt in der Mitte (panTo-Aufrufe):',pa>0)
    pg.click('#follow'); pg.wait_for_timeout(300); a=ev("__calls.setView"); pg.wait_for_timeout(1000); print('nach „Zentrieren“: Kamera stellt wieder selbst ein:',ev("__calls.setView")-a>0,'| userZoom',ev('userZoom'))
    print('Fehler:',errs); b.close()
