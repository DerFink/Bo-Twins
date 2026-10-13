from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0]); h1=h
def h(r):
    u=r.request.url
    return r.continue_() if u.startswith('http://127.0.0.1:8765/') else h1(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); c.route('**/*', h); pg.goto('http://127.0.0.1:8765/'); pg.wait_for_timeout(6000)
    print('Service Worker aktiv:',ev("navigator.serviceWorker.getRegistration().then(r=>r&&r.active?r.active.state:String(r&&(r.installing||r.waiting)&&'lädt'))"),'| Zwischenspeicher:',ev("caches.keys()"))
    print('App-Dateien gespeichert:',ev("caches.open('gb-shell-v38').then(c=>c.keys()).then(k=>k.map(r=>r.url.split('/').pop()||'/'))"))
    pg.reload(); pg.wait_for_timeout(3000); print('nach Neuladen vom Service Worker gesteuert:',ev("!!navigator.serviceWorker.controller"),'| Dienst weiter erreichbar:',ev("onlineCall('ping').then(r=>r.ok)"),'| api im Zwischenspeicher:',ev("caches.open('gb-shell-v38').then(c=>c.keys()).then(k=>k.some(r=>r.url.includes('/api/')))"))
    c.set_offline(True); pg.reload(); pg.wait_for_timeout(3500); print('ohne Netz: App startet:',ev("typeof BUILD==='string' && BUILD"),'| Zustand',ev('STATE')); c.set_offline(False)
    print('Fehler:',[e for e in errs if 'countries-50m' not in e][:3]); b.close()
