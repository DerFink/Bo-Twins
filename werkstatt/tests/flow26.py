from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
jj=json.loads(wx); H=jj['hourly']; N=len(H['time'])
RH={1000:78,975:80,950:84,925:90,900:96,850:97,800:70,700:35,600:30,500:22,400:18,300:15,250:12}
for L,v in RH.items(): H['relative_humidity_%dhPa'%L]=[v]*N; H['cloud_cover_%dhPa'%L]=[100 if L in (900,850) else 0]*N
H['relative_humidity_2m']=[75]*N; wx=json.dumps(jj)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':640},locale='de-DE',user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    print('Build',ev('BUILD'),'| Menü rollt, Pfeil sichtbar:',ev("document.querySelector('.mcard').classList.contains('more')"),'| Installationshinweis:',not ev("$('install').hidden"),'| Link im Menü verborgen solange Hinweis da:',ev("$('m-inst').hidden"))
    pg.screenshot(path='g_menu.png'); pg.click('#inst-later'); pg.wait_for_timeout(600); print(' nach „Später“: Hinweis weg',ev("$('install').hidden"),'| Link im Menü:',not ev("$('m-inst').hidden"),ev("$('m-inst').textContent"))
    ev("document.querySelector('.mcard').scrollTop=9999"); pg.wait_for_timeout(700); print(' ganz unten: Pfeil weg:',not ev("document.querySelector('.mcard').classList.contains('more')")); pg.screenshot(path='g_menu2.png'); ev("document.querySelector('.mcard').scrollTop=0")
    print('Abfrage Wetter enthält Feuchte:',ev("wxUrl(51,7,false).includes('relative_humidity_850hPa')"),'| einfache Abfrage ohne:',not ev("wxUrl(51,7,true).includes('relative_humidity')"),'| GPS',ev('GPS_AVG'))
    pg.click('#m-champ'); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(400)
    print('Taupunkt am Boden / 1500 m / 3000 m:',ev("[0,1500,3000].map(z=>{const a=atmAt(ATM,z);return a.d==null?null:(a.d-273.15).toFixed(1)+' ('+(a.T-273.15).toFixed(1)+')'})"))
    print('Profil-Tipp ändert nichts:',end=' '); box=pg.locator('#prof-cv').bounding_box(); pg.mouse.click(box['x']+20,box['y']+100); pg.wait_for_timeout(200); print(ev("$('stuve').hidden"),ev("$('prof').className"))
    pg.click('#temp-btn'); pg.wait_for_timeout(400); print('Temp offen:',not ev("$('stuve').hidden"),ev("$('temp-btn').classList.contains('on')")); pg.screenshot(path='g_temp.png'); pg.click('#stuve'); pg.wait_for_timeout(200); print(' zu:',ev("$('stuve').hidden"),not ev("$('temp-btn').classList.contains('on')"))
    n=0
    while not ev('B.go') and n<12: pg.click('#rack'); n+=1; pg.wait_for_timeout(150)
    pg.wait_for_timeout(500); ev("map.__userDrag()"); pg.wait_for_timeout(300); print('unter 50 m, Karte verschoben: Knopf „Ballon folgen“ verborgen:',ev("$('follow').hidden"),'folgt:',ev('follow'),'Seitenansicht:',not ev("$('side').hidden"))
    ev("showMenu()"); pg.wait_for_timeout(400)
    # Tutorial
    pg.click('#m-tut'); pg.wait_for_timeout(600); st=lambda: (ev('TUT.i+1'),ev("TUT.steps[TUT.i].k"),'Weiter grau' if ev("$('tut-next').disabled") else 'Weiter','Hand' if not ev("$('tut-hand').hidden") else '')
    print(st(), '| Knöpfe:',ev("[...document.querySelectorAll('#tut button')].map(b=>b.textContent)")); pg.click('#tut-next')
    while ev("TUT.steps[TUT.i].k")=='sacks': pg.click('#rack'); pg.wait_for_timeout(300)
    print(st()); pg.screenshot(path='g_tut3.png'); ev('UI.speed=10'); pg.wait_for_function('!$("tut-next").disabled',timeout=40000); ev('UI.speed=1'); pg.click('#tut-next'); print(st()); pg.click('#tut-next'); print(st()); pg.click('#tut-next'); print(st()); pg.screenshot(path='g_tut6.png')
    pg.click('#temp-btn'); pg.wait_for_timeout(400); print(st(),'| Sprechblase über dem Diagramm sichtbar:',ev("(()=>{const r=$('tut').getBoundingClientRect();return document.elementFromPoint(r.left+20,r.top+10).closest('#tut')!==null})()")); pg.screenshot(path='g_tut7.png'); pg.mouse.click(180,120); pg.wait_for_timeout(400); print(st())
    pg.click('#scoop'); pg.wait_for_timeout(300); print(st()); pg.click('#tut-next'); print(st()); ev("valve=0.6"); pg.wait_for_timeout(2200); ev("valve=0"); pg.wait_for_timeout(300); print(st()); pg.click('#tut-next'); print(st()); pg.click('#tut-next'); print(st(), ev("$('btn-set').style.visibility!=='hidden'")); pg.screenshot(path='g_tut13.png'); pg.click('#tut-next'); print(st())
    pg.click('#rope'); pg.wait_for_timeout(300); print(st()); pg.screenshot(path='g_tut15.png')
    ev("window.__v=setInterval(()=>{valve=B.landed?0:1},50);0"); pg.wait_for_function('B.landed',timeout=60000); ev("clearInterval(__v);valve=0"); pg.wait_for_timeout(500); print(st()); pg.click('#tut-next'); pg.wait_for_timeout(200); print('beendet',not ev('TUT.on'))
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
