from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
src=open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0]
exec(src); h1=h; LOG=[]
def h(r):
    u=r.request.url
    if u.startswith('http://127.0.0.1:8765/'):
        if 'action=' in u: LOG.append(u.split('action=')[1]+(' '+(r.request.post_data or '')[-12:] if r.request.post_data else ''))
        return r.continue_()
    return h1(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto('http://127.0.0.1:8765/'); pg.wait_for_timeout(3500)
    print('Build',ev('BUILD'),'| Dienst:',ev('ONLINE.api'),'| Service Worker:',ev("navigator.serviceWorker.getRegistration().then(r=>!!r)"))
    pg.click('#btn-set'); pg.wait_for_timeout(300); print('Statistik-Knopf sichtbar:',not ev("$('sx-btn').hidden")); pg.click('#sx-btn'); pg.wait_for_timeout(1200)
    print(ev("[...document.querySelectorAll('#sx-rows .kv')].map(x=>x.children[0].textContent+': '+x.children[1].textContent).join(' | ')")); print(ev("$('sx-note').textContent")); pg.screenshot(path='i_stats.png'); pg.click('#sx-close')
    pg.wait_for_timeout(61000); print('Meldungen an den Dienst:',LOG)
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
