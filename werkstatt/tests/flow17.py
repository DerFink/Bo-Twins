from playwright.sync_api import sync_playwright
import json, urllib.parse, re, datetime
exec(open('flow7.py').read().split("with sync_playwright()")[0]); stub=open('stub2.js').read()
topo=open('topomock.json').read(); j=json.loads(wx); n=len(j['hourly']['time'])
REQ=[]; NET={'wx':True,'topo':True}
def hist(u):
    q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query); d0=datetime.datetime.fromisoformat(q['start_date'][0]); jj=json.loads(wx)
    jj['hourly']['time']=[(d0+datetime.timedelta(hours=i)).strftime('%Y-%m-%dT%H:%M') for i in range(n)]; jj['latitude']=float(q['latitude'][0]); jj['longitude']=float(q['longitude'][0]); return json.dumps(jj)
h0=h
def h(r):
    u=r.request.url
    if 'historical-forecast-api' in u:
        REQ.append(u)
        return r.fulfill(body=hist(u),content_type='application/json') if NET['wx'] else r.abort()
    if 'countries-50m.json' in u:
        if 'jsdelivr' in u and NET['topo']: return r.fulfill(body=topo,content_type='application/json')
        return r.abort()
    return h0(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':390,'height':844},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('console: '+m.text) if m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text else None)
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    print('Menü:',ev("[...document.querySelectorAll('.mcard .mbtn b')].map(x=>x.textContent)"))
    ev("$('m-name').value='Erich'; $('m-name').dispatchEvent(new Event('input'))")
    pg.click('#m-champ'); pg.wait_for_timeout(200); print('Hinweis vor dem Start:',ev("$('cf-text').textContent")[:120],ev("[$('cf-ok').textContent,$('cf-no').textContent]"))
    pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    q=urllib.parse.parse_qs(urllib.parse.urlparse(REQ[0]).query); print('Wetterabruf:',REQ[0].split('/v1')[0],q['start_date'],q['end_date'],q['latitude'],q['longitude'],'| Wolken dabei:', 'cloud_cover_850hPa' in REQ[0])
    print('Startfenster:',ev("$('sw-target').textContent")[:90],'|',ev("$('sw-start').textContent"),'|',ev("$('sw-bal').textContent"),'|',ev("$('sw-sand').textContent")[:40]); pg.screenshot(path='b_brief.png')
    print('Sperrflächen auf der Karte:',ev("GB.ban.length"),'| Ebenen',ev("GB.layers.length"),'| Sonne',ev("(Math.asin(radEnv(B,ATM).s)*180/Math.PI).toFixed(0)"),'° | Gas−Luft',ev("(B.Tg-atmAt(ATM,0).T).toFixed(1)"))
    pg.click('#sw-go'); pg.wait_for_timeout(400); print('Kopf:',ev("[...document.querySelectorAll('#seg-speed button')].filter(x=>getComputedStyle(x).display!=='none').map(x=>x.textContent.trim()||'II')"),'| Uhr',ev("[$('tm-lbl').textContent,$('tm-val').textContent]"),'| Speichern sichtbar',not ev("$('gb-save').hidden"))
    pg.click('#rack'); pg.click('#rack'); pg.click('#rack'); pg.wait_for_timeout(1500); print('abgehoben:',ev("B.go"),ev("B.h.toFixed(0)"),'m')
    # 500× nur solange gedrückt
    t0=ev("B.t"); pg.dispatch_event('#btn-500','pointerdown',{'pointerId':1}); pg.wait_for_timeout(1000); t1=ev("B.t"); pg.dispatch_event('#btn-500','pointerup',{'pointerId':1}); pg.wait_for_timeout(1000); t2=ev("B.t")
    print('500× gedrückt: %.0f s Spielzeit in 1 s; losgelassen: %.0f s in 1 s'%(t1-t0,t2-t1)); pg.screenshot(path='b_play.png')
    # weite Strecke: Bezugspunkt nachziehen, Entfernung prüfen
    ev("window.__hold=setInterval(()=>{ if(STATE==='play'&&!B.landed&&window.__keep){B.h=1500;B.w=0;} },5); window.__keep=true; B.h=1500;B.w=0;ATM.forEach(r=>{r.u=30;r.v=8}); wxTick=()=>{}; 0"); pg.dispatch_event('#btn-500','pointerdown',{'pointerId':1}); pg.wait_for_function("B.t>3600*6 || B.landed",timeout=60000); pg.dispatch_event('#btn-500','pointerup',{'pointerId':1})
    ev("setPaused(true)"); print('nach 6 h mit 31 m/s: Entfernung laut App',ev("gbKm().toFixed(1)"),'km | Bezugspunkt',ev("START.lat.toFixed(3)+' / '+START.lon.toFixed(3)"),'| Position',ev("gbPos().map(x=>x.toFixed(3)).join(' / ')"),'| Weg',ev("(B.dist/1000).toFixed(0)"),'km | gelandet',ev('B.landed'),'| Höhe',ev('B.h.toFixed(0)'))
    print(' Anzeige Start:',ev("[$('i-tlbl').textContent,$('i-tdist').textContent]"),'| Sperrzone:',ev("[!$('row-zone').hidden,$('i-zone').textContent,(GB.zone/1000).toFixed(0)]"))
    # Speichern und Fortsetzen
    ev("setPaused(false)"); pg.click('#gb-save'); pg.wait_for_timeout(200); sv=ev("(()=>{const s=store.get('gb-save69');return [s.km.toFixed(1),s.B.t.toFixed(0),s.path.length,JSON.stringify(s).length]})()"); print('gespeichert (km, t, Wegpunkte, Bytes):',sv,'|',ev("$('toast').textContent"))
    pos=ev("gbPos()"); pg.click('#btn-menu'); pg.wait_for_timeout(200); print('Menü-Rückfrage:',ev("$('cf-text').textContent")); pg.click('#cf-ok'); pg.wait_for_timeout(300); print(' Zustand',ev('STATE'),'| Ballon-Einstellung zurück:',ev("CFG.pax"),'Personen')
    pg.click('#m-champ'); pg.wait_for_timeout(200); print('Fortsetzen?',ev("$('cf-text').textContent"),ev("[$('cf-ok').textContent,$('cf-no').textContent]")); pg.click('#cf-ok'); pg.wait_for_function("STATE==='play'",timeout=20000); pg.wait_for_timeout(300)
    pos2=ev("gbPos()"); print('fortgesetzt: Position gleich',abs(pos[0]-pos2[0])<1e-6 and abs(pos[1]-pos2[1])<1e-6,'| angehalten',ev('PAUSED'),'| t',ev('B.t.toFixed(0)'),'| km',ev('gbKm().toFixed(1)'),'| Personen',ev('CFG.pax'),'| Wetterabruf am Ort:',urllib.parse.parse_qs(urllib.parse.urlparse(REQ[-1]).query)['start_date'],ev("$('toast').textContent"))
    # 30-Minuten-Frage
    ev("setPaused(false); GB.playS=1799.9; 0"); pg.wait_for_timeout(600); print('30-min-Frage:',not ev("$('confirm').hidden"),ev("$('cf-text').textContent"),'| angehalten',ev('PAUSED')); pg.click('#cf-no'); pg.wait_for_timeout(200)
    # Sperrzone: Annäherung an 24° Ost (Testgrenze)
    ev("(()=>{ const la=52, lo=23.55; START={lat:la,lon:lo,alt:START.alt,kind:'gb'}; B.e=0;B.n=0;B.lat0=la;B.lon0=lo; ATM.forEach(r=>{r.u=20;r.v=0}); GB.chkAt=-1e9; GB.warned=0; })()"); ev("B.h=1500;B.w=0;0")
    pg.wait_for_function("GB.zone!=null && GB.zone<31000",timeout=20000); print('Annäherung:',ev("[$('toast').textContent,$('i-zone').textContent,!$('row-zone').hidden]"))
    pg.click('#seg-speed button[data-v="100"]'); pg.wait_for_function("STATE==='done'",timeout=30000); pg.wait_for_timeout(300)
    print('Sperrzone erreicht:',ev("$('r-head').textContent"),'| Länge beim Abbruch',ev("gbPos()[1].toFixed(3)"),'(Grenze 24,000; 10 km = 0,146°) |',ev("$('r-extra').textContent")[:60]); pg.screenshot(path='b_dq.png')
    print(' Liste im Fenster:',ev("document.querySelectorAll('#r-list tr').length"),'Zeilen, eigene:',ev("document.querySelector('#r-list tr.me').textContent"),'| Spielstand gelöscht',ev("store.get('gb-save69',null)===null"))
    # Reguläre Landung an Land und im Wasser
    def land(lat,lon,label):
        ev('window.__keep=false'); pg.click('#again'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(200)
        ev(f"(()=>{{ START={{lat:{lat},lon:{lon},alt:START.alt,kind:'gb'}}; B.e=0;B.n=0;B.lat0={lat};B.lon0={lon}; B.go=true;B.air=true;B.h=B.gnd+0.03;B.w=-0.4; }})()"); pg.wait_for_function("STATE==='done'",timeout=10000); pg.wait_for_timeout(200)
        print(label+':',ev("$('r-head').textContent"),'|',ev("$('r-extra').textContent")[:80],'|',ev("$('r-note').textContent")[:110])
    land(55.0,23.0,'Landung in Polen bei 55 N 23 O'); pg.screenshot(path='b_res.png')
    print(' Rang in der Liste:',ev("[...document.querySelectorAll('#r-list tr')].findIndex(r=>r.className==='me')+1"),'| Zeile:',ev("document.querySelector('#r-list tr.me').textContent"),'| Linien/Marken der echten Teams:',ev("GB.layers.length-GB.ban.length"))
    land(57.5,20.0,'Landung in der Ostsee')
    land(60.5,23.9,'Landung bei 60,5 N 23,9 O (im Puffer)')
    pg.click('#r-menu'); pg.click('#m-score'); pg.click('#sc-kind button[data-v="gb"]'); pg.wait_for_timeout(200); print('Liste 69. Gordon Bennett:',ev("[...document.querySelectorAll('#sc-list tr')].map(r=>[...r.children].map(c=>c.textContent).join(' | '))"))
    pg.click('#sc-back')
    # ohne Grenzdaten / ohne Wetter
    ev("GB.polys=null;GB.ban=null;0"); NET['topo']=False; pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='menu'",timeout=20000); print('ohne Grenzdaten:',ev("$('toast').textContent"))
    NET['topo']=True; NET['wx']=False; pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='menu'",timeout=30000); print('ohne Wetter:',ev("$('toast').textContent"))
    # andere Spielart danach unverändert
    NET['wx']=True; pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Freie Fahrt danach:',ev("$('sw-bal').textContent")[:40],'| Aufgabe',ev('TASK()'),'| rote Flächen',ev('GB.layers.length'))
    print('Fehler:',errs); b.close()
