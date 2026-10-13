from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    for name,vp in [('m_hoch',{'width':390,'height':844}),('m_quer',{'width':844,'height':390}),('m_tab',{'width':1024,'height':768})]:
        pg=b.new_page(viewport=vp); pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(3200); pg.screenshot(path=name+'.png')
        if name=='m_hoch':
            ev=lambda s: pg.evaluate(s)
            pg.click('#m-chal'); pg.wait_for_timeout(300); pg.screenshot(path='m_chal.png')
            pg.click('#chal [data-task="target"]'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000)
            print('Ziel',ev("Math.round(TARGET.dist)+' m, Punkteradius '+scoreRadius(TARGET.dist)+', Zone '+tgtCore.getRadius()"))
            pg.wait_for_timeout(500); pg.screenshot(path='m_brief.png'); pg.click('#sw-go'); pg.wait_for_timeout(400)
            # Fahrt: Sand abwerfen, steigen, dann Tau raus und in Bodennähe schleppen
            ev("for(let i=0;i<3;i++) dropScoop(B,CFG); 0");
            pg.wait_for_timeout(1500); pg.click('#rope'); pg.wait_for_timeout(300)
            ev("B.h=B.gnd+25; B.w=0; 0"); pg.wait_for_timeout(1500)
            print('Tau',ev("[$('n-rope').textContent,B.ropeOn.toFixed(1),B.gs.toFixed(2),Math.hypot(atmAt(ATM,B.h).u,atmAt(ATM,B.h).v).toFixed(2),B.lag,$('i-track').textContent]"))
            pg.screenshot(path='m_play.png')
        pg.close()
    print('Fehler:',errs); b.close()
