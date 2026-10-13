from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
src=open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0]
exec(src); h1=h
def h(r):
    u=r.request.url
    if u.startswith('http://127.0.0.1:8765/'): return r.continue_()
    return h1(r)
URL='http://127.0.0.1:8765/'
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(URL); pg.wait_for_timeout(3000)
    print('Build',ev('BUILD'),'| Dienst erkannt:',ev('ONLINE.api'),'| Service Worker:',ev("navigator.serviceWorker.getRegistration().then(r=>!!r)"))
    ev("$('m-name').value='Erich'; $('m-name').dispatchEvent(new Event('input'))")
    ev("onlineScore({n:'Erich',p:91,c:'target',l:2,s:333.3,t:1200,at:Date.now()})"); ev("onlineScore({n:'Erich',km:1234.56,rank:9,dq:null,t:120000,at:777,c:'gb69',p:1235})"); ev("onlineScore({n:'Pech',km:800,rank:null,dq:'water',t:90000,at:778,c:'gb69',p:800})"); pg.wait_for_timeout(800)
    pg.click('#m-score'); pg.wait_for_timeout(1200); print('Liste Challenge:',ev("[...document.querySelectorAll('#sc-list tr')].map(r=>r.textContent).join(' | ')"))
    pg.click('#sc-kind button[data-v="gb"]'); pg.wait_for_timeout(1200); print('Liste Gordon Bennett:',ev("[...document.querySelectorAll('#sc-list tr')].map(r=>r.textContent).join(' | ')")); pg.screenshot(path='d_gb.png')
    ev("onlineUnscore(778)"); pg.wait_for_timeout(600); pg.click('#sc-kind button[data-v="chal"]'); pg.wait_for_timeout(500); pg.click('#sc-kind button[data-v="gb"]'); pg.wait_for_timeout(1000); print('nach Zurückziehen:',ev("[...document.querySelectorAll('#sc-list tr')].map(r=>r.textContent).join(' | ')"))
    # zweites Gerät
    c2=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); p2=c2.new_page(); p2.route('**/*', h); p2.goto(URL); p2.wait_for_timeout(3000); p2.click('#m-score'); p2.wait_for_timeout(1200)
    print('zweites Gerät sieht:',p2.evaluate("[...document.querySelectorAll('#sc-list tr')].map(r=>r.textContent).join(' | ')"))
    # Dienst weg
    pg.route('**/api/**', lambda r: r.abort()); pg.click('#sc-kind button[data-v="chal"]'); pg.wait_for_timeout(1200); print('Dienst nicht erreichbar:',ev("$('sc-list').textContent")[:120])
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
