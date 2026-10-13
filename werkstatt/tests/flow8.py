from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(1800)
    pg.click('#m-chal'); pg.click('#chal [data-task="wz"]'); pg.click('#seg-wx button[data-v="sim"]'); out=[]
    for i in range(6):
        pg.click('#su-go' if i==0 else '#again') if i==0 else None
        if i>0: pg.click('#sw-back'); pg.click('#su-go')
        pg.wait_for_function("STATE==='brief'",timeout=20000)
        out.append(ev("Math.round((Math.atan2(-ATM[0].u,-ATM[0].v)*180/Math.PI+360)%360)+'°'+(WX?' echt':' sim')+' K'+WZ.crosses.length"))
    print('Wandziel, sechs Starts in der Simulation:',out, errs); b.close()
