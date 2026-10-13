from playwright.sync_api import sync_playwright
import json, re, time, urllib.parse
stub=open('stub.js').read(); wx=open('wxmock.json').read(); FILE='file:///mnt/user-data/outputs/spiel/index.html'
M={'osm':'pitch','posts':[],'top':[{'n':'Anna','p':97,'c':'mid','l':None,'s':500,'at':1},{'n':'Ben','p':90,'c':'target','l':2,'s':480,'at':2}]}
def h(r):
    u=r.request.url
    if 'leaflet.min.js' in u: return r.fulfill(body=stub,content_type='application/javascript')
    if 'nominatim' in u: return r.fulfill(body=json.dumps({'name':'Roitzsch','address':{'village':'Roitzsch'}}),content_type='application/json')
    if '/v1/elevation' in u:
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query); return r.fulfill(body=json.dumps({'elevation':[80.0]*len(q['longitude'][0].split(','))}),content_type='application/json')
    if 'open-meteo' in u: return r.fulfill(body=wx,content_type='application/json')
    if 'overpass' in u:
        if M['osm']=='fail': return r.abort()
        q=urllib.parse.unquote_plus(r.request.post_data or ''); m=re.search(r'around:(\d+),([\d.]+),([\d.]+)',q); M['q']=q[:60]; rad,lat,lon=float(m.group(1)),float(m.group(2)),float(m.group(3))
        els=[{'type':'way','id':1,'center':{'lat':lat+0.002,'lon':lon+0.001},'tags':{'leisure':'pitch','name':'Sportplatz Musterdorf'}}] if M['osm']=='pitch' else []
        return r.fulfill(body=json.dumps({'elements':els}),content_type='application/json')
    if 'example.org' in u:
        if 'action=top' in u: return r.fulfill(body=json.dumps(M['top']),content_type='application/json',headers={'Access-Control-Allow-Origin':'*'})
        M['posts'].append((u.split('action=')[1], r.request.post_data)); return r.fulfill(body='{"ok":true}',content_type='application/json',headers={'Access-Control-Allow-Origin':'*'})
    if u.startswith('http'): return r.abort()
    r.continue_()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,locale='de-DE'); errs=[]
    ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('console: '+m.text) if m.type=='error' and 'ERR_' not in m.text and 'Failed to load' not in m.text else None)
    pg.route('**/*', h); pg.goto(FILE)
    ev("""()=>{window.__n=0;window.__g=[];const P=(window.AudioContext||window.webkitAudioContext).prototype;const o=P.createOscillator;P.createOscillator=function(){__n++;return o.call(this)};}""")
    pg.wait_for_timeout(500); print('Menü nach 0,5 s:',ev("getComputedStyle(document.querySelector('.mcard')).opacity")); pg.wait_for_timeout(2700); pg.screenshot(path='g0.png')
    print('Menü nach 3,2 s:',ev("getComputedStyle(document.querySelector('.mcard')).opacity"),'| Musik-Töne:',ev('__n'))
    pg.fill('#m-name','Erich'); pg.click('#m-chal'); pg.wait_for_timeout(200); print('Zustand',ev('STATE'),'| Aufgaben:',ev("[...document.querySelectorAll('#chal [data-task] b')].map(x=>x.textContent).join(' / ')")); pg.screenshot(path='g1.png')
    # ---- Zielfahren, aktuelles Wetter
    pg.click('#chal [data-task="target"]'); pg.click('#seg-level button[data-v="0"]'); pg.click('#seg-wx button[data-v="real"]'); pg.wait_for_timeout(100); pg.screenshot(path='g2.png')
    t0=time.time(); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Zielfahren bereit nach %.1f s'%(time.time()-t0)); pg.wait_for_timeout(400)
    print(' Ziel:',ev("$('sw-target').textContent")); print(' Wetter:',ev("$('sw-wx').textContent")[:120]); print(' Abfrage:',M.get('q'))
    for lvl in (1,2):
        pg.click('#sw-back'); pg.click(f'#seg-level button[data-v="{lvl}"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print(' Stufe',lvl,ev("(TARGET.dist/1000).toFixed(1)+' km, Suchradius '+Math.round(Math.max(250,Math.min(1200,0.15*TARGET.dist)))+' m, Versatz zum Sportplatz '+Math.round(TARGET.refMiss)+' m'"))
    M['osm']='fail'; pg.click('#sw-back'); t0=time.time(); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Kartendienst fällt aus: bereit nach %.1f s |'%(time.time()-t0),ev("$('sw-target').textContent")[-160:]); pg.screenshot(path='g3.png'); M['osm']='pitch'
    # ---- Wandziel, Simulation
    pg.click('#sw-back'); pg.click('#su-back'); pg.click('#chal [data-task="wz"]'); pg.wait_for_timeout(100); pg.screenshot(path='g4.png'); print('Wandziel: Startwahl verborgen',ev("$('su-startsel').hidden"),'| fester Start:',ev("$('su-startfix').textContent"))
    pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print(' ',ev("$('sw-tlbl').textContent"),':',ev("$('sw-target').textContent")); print('  Säckchen',ev('B.marks'),'Kreuze',ev('WZ.crosses.length'),'Start',ev("START.kind"),'| Sand',ev("$('sw-sand').textContent")[:40])
    w1=ev("(Math.atan2(-ATM[0].u,-ATM[0].v)*180/Math.PI+360)%360")
    pg.click('#sw-go'); pg.wait_for_timeout(300); print('  Knopf sichtbar',ev("!$('mk-drop').hidden"),'gesperrt am Boden',ev("$('mk-drop').disabled"),'| Ziel-Zeile:',ev("$('i-tlbl').textContent"),ev("$('i-tdist').textContent"))
    for i in range(4): pg.click('#rack')
    pg.click('#seg-speed button[data-v="10"]'); pg.wait_for_function("B.air",timeout=15000); pg.click('#seg-speed button[data-v="1"]')
    ev("(()=>{const c=WZ.crosses[0]; const q=markerFall(ATM,0,0,B.h,B.gnd); B.e=c.e-q[0]+8; B.n=c.n-q[1];})()"); pg.wait_for_timeout(150); pg.screenshot(path='g5.png'); pg.click('#mk-drop'); pg.wait_for_timeout(200)
    print('  Abwurf über Kreuz 1:',ev("$('toast').textContent"),'| übrig',ev('B.marks'),'| Zeile zeigt jetzt',ev("$('i-tlbl').textContent"))
    ev("B.e+=300"); pg.click('#mk-drop'); pg.wait_for_timeout(100); print('  zweiter Abwurf:',ev("$('toast').textContent"))
    ev("B.h=B.gnd+0.05;B.w=-0.4"); pg.wait_for_function("STATE==='done'",timeout=5000); pg.wait_for_timeout(200); pg.screenshot(path='g6.png')
    print('  Auswertung:',ev("$('r-head').textContent"),'|',ev("[...document.querySelectorAll('#r-extra .kv')].map(x=>x.children[0].textContent+': '+x.children[1].textContent).join('; ')"),'| Punkte',ev("$('r-pts').textContent"),'Platz',ev("$('r-rank').textContent"))
    # ---- neue Fahrt: anderer Wind
    pg.click('#again'); pg.wait_for_function("STATE==='brief'",timeout=20000); w2=ev("(Math.atan2(-ATM[0].u,-ATM[0].v)*180/Math.PI+360)%360"); print('Simulation: Bodenwind erste Fahrt %d°, zweite Fahrt %d°'%(w1,w2))
    # ---- MDT
    pg.click('#sw-back'); pg.click('#su-back'); pg.click('#chal [data-task="mdt"]'); t0=time.time(); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=30000); print('MDT bereit nach %.1f s |'%(time.time()-t0),ev("$('sw-target').textContent"),'| Bestweite',ev("(MDT.best.dist/1000).toFixed(1)+' km in '+MDT.best.h+' m'"))
    pg.click('#sw-go'); pg.wait_for_timeout(200); print('  Zeit sichtbar',ev("!$('timer').hidden"),ev("$('tm-val').textContent"),'| Zeile:',ev("$('i-tlbl').textContent"))
    for i in range(4): pg.click('#rack')
    pg.wait_for_function("B.t>5",timeout=8000); pg.screenshot(path='g7.png'); print('  läuft:',ev("$('tm-val').textContent"))
    ev("B.air=true;B.e=MDT.best.dist*0.8;B.n=0;B.t=10800+190;"); pg.wait_for_timeout(150); print('  Überzeit:',ev("$('tm-val').textContent"),ev("$('tm-val').style.color")); ev("B.h=B.gnd+0.05;B.w=-1.2"); pg.wait_for_function("STATE==='done'",timeout=5000); pg.wait_for_timeout(200); pg.screenshot(path='g8.png')
    print('  Auswertung:',ev("$('r-head').textContent"),'|',ev("[...document.querySelectorAll('#r-extra .kv')].map(x=>x.children[0].textContent+': '+x.children[1].textContent).join('; ')"),'| Punkte',ev("$('r-pts').textContent"),'|',ev("$('r-note').textContent"))
    # ---- MID
    pg.click('#r-menu'); pg.click('#m-chal'); pg.click('#chal [data-task="mid"]'); pg.wait_for_timeout(100); print('MID: Wetterwahl verborgen',ev("$('seg-wx').hidden"),'|',ev("$('su-wxmid').textContent")); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    print('  Sektoren bis 6000 m:',ev("(()=>{const s=new Set();for(let h=0;h<=6000;h+=25){const a=atmAt(ATM,h);s.add(Math.floor(((Math.atan2(-a.u,-a.v)*180/Math.PI+360)%360)/10)%36);}return s.size})()"),'von 36 |',ev("$('sw-target').textContent"),'| WX',ev('WX'))
    pg.click('#sw-go');
    for i in range(3): pg.click('#rack')
    pg.wait_for_function("B.t>3",timeout=8000); ev("B.air=true;B.e=350;B.n=0;B.t=3600+125;B.h=B.gnd+0.05;B.w=-2.0"); pg.wait_for_function("STATE==='done'",timeout=5000); pg.wait_for_timeout(200)
    print('  Auswertung:',ev("$('r-head').textContent"),'|',ev("[...document.querySelectorAll('#r-extra .kv')].map(x=>x.children[0].textContent+': '+x.children[1].textContent).join('; ')"),'| Punkte',ev("$('r-pts').textContent"))
    # ---- freie Fahrt: Rückmeldung zur Landung, Gasanzeige
    pg.click('#r-menu'); pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); print('Freie Fahrt: Startwahl sichtbar',ev("!$('su-startsel').hidden"),'| Punktezeile in der Auswertung:',end=' ')
    for v in (0.3,1.0,2.0,3.5):
        if ev("STATE")=='done': pg.click('#again'); pg.wait_for_function("STATE==='brief'",timeout=20000)
        pg.click('#sw-go'); pg.click('#rack'); pg.click('#rack'); pg.wait_for_function("B.t>2",timeout=8000); ev(f"B.air=true;B.h=B.gnd+0.03;B.w=-{v}"); pg.wait_for_function("STATE==='done'",timeout=5000); pg.wait_for_timeout(120)
        print(f"{v} m/s → {ev(chr(36)+'(\"r-head\").textContent')};",end=' ')
    print('| Punkte verborgen',ev("$('r-ptsrow').hidden"),'| Gas',ev("$('i-fill').textContent"))
    # ---- Bestenliste lokal und online
    pg.click('#r-menu'); pg.click('#m-score'); pg.wait_for_timeout(300); print('Bestenliste lokal:\n'+ev("[...document.querySelectorAll('table.sc tr')].map(r=>'  '+[...r.children].map(c=>c.textContent).join(' | ')).join('\\n')")); pg.screenshot(path='g9.png')
    pg.click('#sc-back'); ev("ONLINE.api='https://example.org/api.php'"); pg.click('#m-score'); pg.wait_for_timeout(500); print('Bestenliste online:',ev("[...document.querySelectorAll('table.sc tr')].slice(1).map(r=>[...r.children].map(c=>c.textContent).join(' | ')).join(' ; ')"))
    ev("onlineVisit(); onlineScore({n:'Erich',p:55,c:'wz',l:null,s:500,t:900,at:1})"); pg.wait_for_timeout(400); print('Meldungen an den Dienst:',[(a,(b or '')[:90]) for a,b in M['posts']])
    for l in ['en','fr','pl','cs','zh-TW','es','de']:
        pg.click('#lang-btn'); pg.click(f'#lang-list .lopt[data-c="{l}"]'); pg.wait_for_timeout(150); print(l,ev("[...document.querySelectorAll('table.sc tr')][0].textContent"),'|',ev("TX[UI.lang].ld_wild"))
    print('errors',errs)
    pg2=b.new_page(viewport={'width':844,'height':390},device_scale_factor=2,locale='de-DE'); e2=[]; pg2.on('pageerror',lambda e:e2.append(str(e))); pg2.route('**/*', h); pg2.goto(FILE); pg2.wait_for_timeout(2500); pg2.screenshot(path='h0.png')
    pg2.click('#m-chal'); pg2.click('#chal [data-task="mdt"]'); pg2.click('#seg-wx button[data-v="sim"]'); pg2.click('#su-go'); pg2.wait_for_function("STATE==='brief'",timeout=30000); pg2.click('#sw-go'); pg2.click('#rack'); pg2.click('#rack'); pg2.wait_for_timeout(1500); pg2.screenshot(path='h1.png'); print('quer errors',e2)
    b.close()
