from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
GEO="""(() => { let id=0, timers={}; navigator.geolocation.watchPosition=(ok,err,o)=>{ const k=++id; let n=0; timers[k]=setInterval(()=>{ n++; ok({coords:{latitude:52.5+1e-6*n, longitude:13.4, accuracy:n<3?80:8, altitude:40}}); },1000); return k; }; navigator.geolocation.clearWatch=k=>{ clearInterval(timers[k]); delete timers[k]; window.__cleared=(window.__cleared||0)+1; }; })()"""
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; pg=b.new_page(viewport={'width':390,'height':844}); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev(GEO)
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]')
    print('vorher:',ev("$('st-info').textContent"),'| Weiter gesperrt:',ev("$('su-go').disabled"))
    pg.click('#st-gps'); pg.wait_for_timeout(1500)
    print('nach GPS-Tipp:',ev("$('st-info').textContent"),'| Weiter gesperrt:',ev("$('su-go').disabled"))
    ev("$('su-go').click()"); pg.wait_for_timeout(400); print('Weiter angetippt -> Zustand:',ev('STATE'))
    pg.wait_for_timeout(6000); print('nach 8 s:',ev("$('st-info').textContent"),'| gesperrt:',ev("$('su-go').disabled"))
    pg.wait_for_timeout(12500); print('nach 20 s:',ev("$('st-info').textContent"),'| gesperrt:',ev("$('su-go').disabled"),'| Start:',ev("START.lat.toFixed(4)+' '+START.kind"))
    pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(600)
    ev("B.h=1200;0"); pg.wait_for_timeout(2500); print('Fahrt: Ballon bei',ev("START.lat.toFixed(4)+' / Abstand vom Start '+Math.hypot(B.e,B.n).toFixed(0)+' m'"))
    pg.screenshot(path='n_play.png')
    # abbrechen: GPS antippen, dann zurück -> Suche beendet, Weiter frei
    ev("showMenu()"); pg.click('#m-free'); c0=ev("window.__cleared||0"); pg.click('#st-gps'); pg.wait_for_timeout(500); pg.click('#st-def'); print('GPS, dann Bitterfeld:',ev("$('st-info').textContent"),'| gesperrt:',ev("$('su-go').disabled"),'| Suche beendet:',ev("(window.__cleared||0)")>c0)
    pg.wait_for_timeout(18000); print('18 s später Start noch:',ev("START.kind+' '+START.lat.toFixed(4)"))
    ev("openSheet(true)"); pg.wait_for_timeout(300); ev("document.querySelector('[data-i=lg_title]').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path='n_leg.png')
    print('Fehler:',errs); b.close()
