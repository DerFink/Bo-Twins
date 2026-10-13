from playwright.sync_api import sync_playwright
import json
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
hb=h; SLOW={'on':True}
def h(r):
    u=r.request.url
    if 'overpass' in u and SLOW['on']:
        import time; time.sleep(2.5)
    return hb(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); print('Build',ev('BUILD'))
    print('Wetterabruf:',ev("wxUrl(51.624583,12.294567,false).match(/latitude=[^&]+&longitude=[^&]+/)[0]"))
    pg.click('#btn-set'); pg.wait_for_timeout(300); print('Einstellungen: Wetterpaket sichtbar:',ev("$('wxp-btn').offsetParent!==null"),'| „Was ist neu“ neben „Neueste Version laden“:',ev("$('nw-btn').parentElement===$('reload').parentElement")); pg.click('#nw-btn'); pg.wait_for_timeout(200); print(' ',ev("$('nw-rows').textContent")[:90]); pg.click('#nw-close'); ev("openSheet(false)")
    # Zielfahren mit langsamer Ortssuche
    import time
    pg.click('#m-chal'); pg.wait_for_timeout(200); pg.click('#chal [data-task="target"]'); pg.wait_for_timeout(200); pg.click('#seg-wx button[data-v="sim"]'); t0=time.time(); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); t1=time.time()
    print('Zielfahren: Startfenster nach %.1f s | Ziel: %s'%(t1-t0,ev("$('sw-target').textContent")[:150]))
    pg.wait_for_function("TARGET&&TARGET.place&&!TARGET.place.pending",timeout=20000); print(' nach %.1f s: %s'%(time.time()-t0,ev("$('sw-target').textContent")[:150]))
    ev("showMenu()"); pg.wait_for_timeout(300); pg.click('#m-chal'); pg.wait_for_timeout(200); pg.click('#chal [data-task="target"]'); pg.wait_for_timeout(200); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); d0=ev('TARGET.dist'); pg.click('#sw-go'); pg.wait_for_timeout(3500); print(' sofort losgefahren: Ziel bleibt unverändert:',abs(ev('TARGET.dist')-d0)<0.01,'| Zustand',ev('STATE'),ev("JSON.stringify(TARGET.place)"))
    # Wurst
    ev("B.h=600;B.air=true;B.go=true;B.gas=B.gas*0.03;SIDE.user=true"); pg.wait_for_timeout(500); print('Füllgrad',ev('Math.round(fillNow()*100)'),'| Symbol Wurst:',ev("balloonSVG('#f',0.03).includes('M19 4')")); pg.screenshot(path='k_wurst.png',clip={'x':0,'y':380,'width':200,'height':240})
    ev("showMenu()"); pg.wait_for_timeout(300)
    pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Meisterschaft: Abschnitte',ev('GB.segs.length'),'davon gezeichnet',ev('GB.strips.length'))
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
