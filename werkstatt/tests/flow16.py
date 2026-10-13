from playwright.sync_api import sync_playwright
import json, urllib.parse, re
exec(open('flow7.py').read().split("with sync_playwright()")[0])
# Wetter mit Wolkendecke 900 bis 800 hPa und Regen
j=json.loads(wx); n=len(j['hourly']['time'])
for L in [1000,975,950,925,900,850,800,700,600,500,400,300,250]: j['hourly']['cloud_cover_%dhPa'%L]=[100 if L in (900,850,800) else 0]*n
j['hourly']['precipitation']=[2.0]*n; j['hourly']['cloud_cover']=[100]*n; wxc=json.dumps(j); MODE={'wx':'cloud'}; REQ=[]
h0=h
def h(r):
    u=r.request.url
    if 'api.open-meteo.com/v1/forecast' in u:
        REQ.append('cloud_cover_850hPa' in u)
        if MODE['wx']=='reject' and 'cloud_cover' in u: return r.fulfill(status=400,body='{"error":true}',content_type='application/json')
        return r.fulfill(body=wxc if MODE['wx']=='cloud' else wx,content_type='application/json')
    return h0(r)
GEO="""(() => { let id=0, timers={}; navigator.geolocation.watchPosition=(ok,err,o)=>{ const k=++id; let n=0; timers[k]=setInterval(()=>{ n++; ok({coords:{latitude:52.5, longitude:13.4, accuracy:n<3?80:8, altitude:40}}); },1000); return k; }; navigator.geolocation.clearWatch=k=>{ clearInterval(timers[k]); }; })()"""
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':390,'height':844},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev(GEO)
    # GPS-Countdown
    pg.click('#m-free'); pg.click('#st-gps'); pg.wait_for_timeout(1200); print('GPS Suche:',ev("[$('gps-n').textContent,$('gps-cap').textContent,$('su-go').disabled]"))
    pg.wait_for_timeout(4000); print('GPS Mittelung:',ev("[$('gps-n').textContent,$('gps-cap').textContent]")); pg.screenshot(path='g_gps.png')
    t=pg.evaluate("performance.now()"); pg.wait_for_function("$('gps-big').hidden",timeout=15000); print('fertig: Countdown weg, Start',ev("START.kind"),'| Weiter frei',not ev("$('su-go').disabled"))
    pg.click('#st-def')
    # echtes Wetter mit Wolken und Regen
    pg.click('#seg-wx button[data-v="real"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    print('Abfrage mit Wolken:',REQ[-1],'| Startfenster:',ev("$('sw-wx').textContent")[:210])
    print('Wolken: Basis',ev("cloudInfo(ATM).base"),'m, Obergrenze',ev("cloudInfo(ATM).top"),'m über Startplatz; Regen',ev("ATM.rain"),'mm/h')
    pg.click('#sw-go'); pg.wait_for_timeout(300); pg.click('#rack'); pg.click('#rack'); pg.click('#rack'); pg.wait_for_timeout(1500)
    print('Anzeige nach dem Start:',ev("[$('i-skyl').textContent,$('i-sky').textContent,$('toast').textContent]"))
    pg.click('#seg-speed button[data-v="30"]'); pg.wait_for_timeout(6000); print('nach 3 min Spielzeit im Regen:',ev("[B.h.toFixed(0)+' m',$('i-wet').textContent,!$('row-wet').hidden,B.free.toFixed(1)]")); pg.screenshot(path='g_rain.png')
    pg.click('#seg-speed button[data-v="1"]'); ev("B.h=2900;B.w=0;0"); pg.wait_for_timeout(1200); print('über den Wolken:',ev("[B.h.toFixed(0)+' m',cloudInfo(ATM).rainTop,$('i-skyl').textContent,$('i-sky').textContent,B.rain,$('i-wet').textContent]"))
    ev("showMenu()")
    # Dienst lehnt die erweiterte Abfrage ab
    MODE['wx']='reject'; REQ.clear(); pg.click('#m-free'); pg.evaluate("store.set('gb-wx2',null)"); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    print('erweiterte Abfrage abgelehnt: Abfragen',REQ,'| echtes Wetter geladen',ev('!!WX'),'| Wolken',ev("cloudInfo(ATM).up[0]"))
    ev("showMenu()")
    # Simulation
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Simulation:',ev("$('sw-wx').textContent")[:60]); pg.click('#sw-go'); pg.wait_for_timeout(500)
    print(' Anzeige:',ev("[$('i-skyl').textContent,$('i-sky').textContent]"),'| Gas−Luft am Start',ev("(B.Tg-atmAt(ATM,0).T).toFixed(1)"),'K | Hinweis:',ev("$('hint').textContent")[-28:]); pg.screenshot(path='g_sim.png')
    print('Fehler:',errs); b.close()
