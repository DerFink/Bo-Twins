from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; pg=b.new_page(viewport={'width':360,'height':740}); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    vis=lambda: ev("getComputedStyle($('btn-menu')).display!=='none'")
    print('Hauptmenü: Knopf sichtbar',vis(),'| Höhe App',ev("$('app').getBoundingClientRect().height"),'von',ev('innerHeight'))
    pg.click('#m-free'); print('Vorbereitung: Knopf',vis()); pg.click('#btn-menu'); print(' -> Zustand',ev('STATE'))
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Startfenster: Knopf',vis()); pg.click('#sw-go'); pg.wait_for_timeout(400)
    r=ev("(()=>{const a=$('btn-menu').getBoundingClientRect(),s=$('seg-speed').getBoundingClientRect(),t=$('btn-set').getBoundingClientRect(),p=document.querySelector('.panel').getBoundingClientRect();return [Math.round(a.left),Math.round(a.right),Math.round(s.left),Math.round(t.right),Math.round(p.bottom),innerWidth,innerHeight]})()")
    print('Fahrt: Knopf',vis(),'| Knopf x',r[0],'bis',r[1],'| Zeitraffer ab',r[2],'| Einstellungen bis',r[3],'von',r[5],'| Unterkante Bedienfeld',r[4],'von',r[6])
    pg.screenshot(path='k_play.png')
    pg.click('#btn-menu'); pg.wait_for_timeout(200); print('am Boden angetippt -> Zustand',ev('STATE'),'(ohne Rückfrage)')
    pg.click('#m-free'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); ev("dropSack(B,CFG);dropSack(B,CFG);B.h=200;B.air=true;0"); pg.wait_for_timeout(800)
    print('in der Luft:',ev('B.air')); pg.click('#btn-menu'); pg.wait_for_timeout(200); print(' Rückfrage sichtbar',not ev("$('confirm').hidden"),ev("$('cf-text').textContent")); pg.click('#cf-no'); pg.wait_for_timeout(200); print(' abgebrochen -> Zustand',ev('STATE'))
    pg.click('#btn-menu'); pg.click('#cf-ok'); pg.wait_for_timeout(300); print(' bestätigt -> Zustand',ev('STATE'),'| Knopf',vis())
    pg.set_viewport_size({'width':360,'height':600}); pg.wait_for_timeout(300); print('Fenster kleiner (600): Höhe App',ev("$('app').getBoundingClientRect().height"))
    print('Fehler:',errs); b.close()
