from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; pg=b.new_page(viewport={'width':390,'height':844}); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    for speed in (10,30,100):
        ev("showMenu()"); pg.click('#m-chal'); pg.click('#chal [data-task="wz"]'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
        ev("window.__k=setInterval(()=>{ if(STATE==='play'&&!B.landed){B.h=270;B.w=0;B.air=true;B.go=true;} },5); B.h=270;B.air=true;B.go=true; 0"); pg.wait_for_timeout(300)
        pg.click(f'#seg-speed button[data-v="{speed}"]'); out=[]
        n=ev("B.marks")
        for i in range(n):
            ev("window.__t0=B.t; window.__r0=performance.now(); window.__n0=WZ.drops.length; window.__p0=[B.e,B.n]; 0"); pg.click('#mk-drop')
            pg.wait_for_function("WZ.drops.length>window.__n0",timeout=12000)
            out.append(ev("(()=>{const d=WZ.drops[WZ.drops.length-1];return 'Fall '+(B.t-__t0).toFixed(1)+' s Spielzeit, '+((performance.now()-__r0)/1000).toFixed(1)+' s echt, Landepunkt '+Math.hypot(d.e-B.e,d.n-B.n).toFixed(0)+' m vom Ballon, '+Math.hypot(d.e-__p0[0],d.n-__p0[1]).toFixed(0)+' m vom Abwurfort'})()"))
            pg.wait_for_timeout(700)
        print(f'{speed}×, Abwurf aus 270 m (Soll 30 s Spielzeit):'); [print('   Wurf',i+1,':',o) for i,o in enumerate(out)]
        print('   Wind am Ballon / am Boden:',ev("(()=>{const a=atmAt(ATM,270),g=atmAt(ATM,10);return Math.hypot(a.u,a.v).toFixed(1)+' m/s aus '+((Math.atan2(-a.u,-a.v)*180/Math.PI+360)%360).toFixed(0)+'° / '+Math.hypot(g.u,g.v).toFixed(1)+' m/s aus '+((Math.atan2(-g.u,-g.v)*180/Math.PI+360)%360).toFixed(0)+'°'})()"))
        ev("clearInterval(window.__k)")
    print('Fehler:',errs); b.close()
