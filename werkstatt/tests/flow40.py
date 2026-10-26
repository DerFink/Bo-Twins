from playwright.sync_api import sync_playwright
import json
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
MODE={'v':'nogeo'}
def arch(u):
    jj=json.loads(hist(u))
    for k in list(jj['hourly']):
        if k.startswith('geopotential') or (MODE['v']=='bad' and 'hPa' in k): jj['hourly'][k]=[None]*len(jj['hourly'][k])
    return json.dumps(jj)
h1=h
def h(r):
    if 'archive-api.open-meteo' in r.request.url: return r.fulfill(body=arch(r.request.url),content_type='application/json')
    return h1(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':720},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev("store.set('gb-news',BUILD)")
    def go():
        pg.click('#m-champ'); pg.wait_for_timeout(200); pg.click('#gbsc-list .mbtn:nth-child(2)'); pg.wait_for_timeout(200); pg.click('#cf-ok'); pg.wait_for_timeout(5000)
    go(); print('ohne Höhen:',ev('STATE'),'| Schichten',ev("WX&&WX.hours[0].pts.length"),'| Wind in 1500 m',ev("(()=>{const a=atmAt(ATM,1500);return Math.hypot(a.u,a.v).toFixed(1)})()"))
    ev("showMenu()"); pg.wait_for_timeout(300); MODE['v']='bad'; go(); print('ganz ohne Höhendaten:',ev('STATE'),'|',ev("$('toast').textContent"))
    print('Fehler',errs); b.close()
