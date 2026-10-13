from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; pg=b.new_page(viewport={'width':390,'height':844}); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    pg.click('#m-chal'); pg.click('#chal [data-task="wz"]'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
    ev("B.h=270;B.air=true;B.w=0;0"); pg.wait_for_timeout(300)
    print('Wind am Ballon',ev("(()=>{const a=atmAt(ATM,B.h);return Math.hypot(a.u,a.v).toFixed(1)})()"),'m/s, am Boden',ev("(()=>{const a=atmAt(ATM,5);return Math.hypot(a.u,a.v).toFixed(1)})()"),'| Höhe',ev('B.h.toFixed(0)'),'m, Fallzeit rund',ev('(B.h/9).toFixed(0)'),'s')
    ev("window.__d=[B.e,B.n];0"); pg.click('#mk-drop'); pg.wait_for_timeout(300)
    print('gleich nach dem Abwurf: im Fall',ev('FLY.length'),'| gelandet',ev('WZ.drops.length'),'| Säckchen übrig',ev('B.marks'),'| Abstand Säckchen–Ballon',ev("Math.hypot(FLY[0].e-B.e,FLY[0].n-B.n).toFixed(0)"),'m')
    pg.wait_for_timeout(12000); print('nach 12 s: Höhe Säckchen',ev("FLY[0]?FLY[0].z.toFixed(0):'-'"),'m | Abstand zum Ballon',ev("FLY[0]?Math.hypot(FLY[0].e-B.e,FLY[0].n-B.n).toFixed(0):'-'"),'m'); pg.screenshot(path='w_fly.png')
    pg.wait_for_function("WZ.drops.length===1",timeout=40000); pg.wait_for_timeout(200)
    print('Aufschlag: Abstand Landepunkt–Ballon jetzt',ev("Math.hypot(WZ.drops[0].e-B.e,WZ.drops[0].n-B.n).toFixed(0)"),'m | vom Abwurfort',ev("Math.hypot(WZ.drops[0].e-__d[0],WZ.drops[0].n-__d[1]).toFixed(0)"),'m | Meldung:',ev("$('toast').textContent"))
    # Zeitraffer 30x
    pg.click('#seg-speed button[data-v="30"]'); pg.click('#mk-drop'); pg.wait_for_function("WZ.drops.length===2",timeout=20000); print('mit 30×: gelandet, Abstand zum Ballon',ev("Math.hypot(WZ.drops[1].e-B.e,WZ.drops[1].n-B.n).toFixed(0)"),'m')
    # Landung, während ein Säckchen noch fällt
    pg.click('#seg-speed button[data-v="1"]'); ev("B.h=B.gnd+60;B.w=-2;B.gas*=0.9;0"); pg.click('#mk-drop'); pg.wait_for_function("STATE==='done'",timeout=60000)
    print('Landung des Ballons: gelandete Säckchen',ev('WZ.drops.length'),'| noch im Fall',ev('FLY.length'),'|',ev("$('r-extra').textContent")[:120])
    print('Fehler:',errs); b.close()
