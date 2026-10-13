from playwright.sync_api import sync_playwright
import json, urllib.parse
exec(open('flow7.py').read().split("with sync_playwright()")[0])
IOS='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
AND='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    def page(ua,vp={'width':390,'height':844}):
        c=b.new_context(user_agent=ua,viewport=vp,locale='de-DE'); pg=c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2800); return pg
    # Android mit Installationsdialog
    pg=page(AND); ev=lambda s: pg.evaluate(s)
    print('Android ohne Meldung des Browsers: Hinweis sichtbar',not ev("$('install').hidden"),'|',ev("$('inst-d').textContent"))
    ev("window.__p=0; const e=new Event('beforeinstallprompt'); e.prompt=()=>{window.__p++}; e.userChoice=Promise.resolve({outcome:'accepted'}); window.dispatchEvent(e); 0")
    pg.wait_for_timeout(200); pg.screenshot(path='i_and.png'); pg.click('#inst-ok'); pg.wait_for_timeout(300)
    print('Android: Dialog des Browsers geöffnet',ev('window.__p'),'| Hinweis danach sichtbar',not ev("$('install').hidden"))
    pg.context.close()
    # iOS
    pg=page(IOS); ev=lambda s: pg.evaluate(s)
    print('iOS: Hinweis sichtbar',not ev("$('install').hidden"),'|',ev("$('inst-d').textContent")); pg.click('#inst-ok'); pg.wait_for_timeout(200); pg.screenshot(path='i_ios.png')
    print('iOS nach „Installieren“:',ev("$('inst-d').textContent"),'| Knöpfe:',ev("[$('inst-ok').hidden,$('inst-later').textContent]"))
    pg.click('#inst-later'); print('iOS geschlossen: sichtbar',not ev("$('install').hidden")); pg.reload(); pg.wait_for_timeout(2500); print('iOS nach Neuladen (7 Tage Ruhe): sichtbar',not ev("$('install').hidden"),'| Knopf in den Einstellungen sichtbar',not ev("$('inst-set').hidden"))
    ev("openSheet(true)"); pg.click('#inst-set'); pg.wait_for_timeout(200); print('über Einstellungen wieder geöffnet:',not ev("$('install').hidden"),ev("$('inst-d').textContent")[:40])
    pg.click('#inst-later'); pg.click('#m-free'); print('in der Vorbereitung sichtbar',not ev("$('install').hidden"))
    # Beschleunigungsbalken
    pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500)
    out=[('am Boden',ev("[$('i-acc').className,$('i-acc').style.height]"))]
    ev("dropSack(B,CFG);dropSack(B,CFG);0"); pg.wait_for_timeout(2500); out.append(('30 kg ab, '+ev("(B.acc).toFixed(3)")+' m/s²',ev("[$('i-acc').className,$('i-acc').style.height]"))); pg.screenshot(path='i_up.png')
    ev("B.h=600;B.w=0;B.gas*=0.97;0"); pg.wait_for_timeout(1200); out.append(('Gas weg, '+ev("(B.acc).toFixed(3)")+' m/s²',ev("[$('i-acc').className,$('i-acc').style.height]"))); pg.screenshot(path='i_dn.png')
    pg.wait_for_timeout(15000); out.append(('Sinken gleichmäßig, '+ev("(B.acc).toFixed(3)")+' m/s², w '+ev("B.w.toFixed(2)"),ev("[$('i-acc').className,$('i-acc').style.height]")))
    for o in out: print(' Balken',o)
    pg.context.close()
    # installierte App
    c=b.new_context(user_agent=IOS,viewport={'width':390,'height':844}); pg=c.new_page(); pg.add_init_script("Object.defineProperty(navigator,'standalone',{get:()=>true})"); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    print('installierte App: Hinweis sichtbar',not pg.evaluate("$('install').hidden"),'| Knopf sichtbar',not pg.evaluate("$('inst-set').hidden"))
    # Rechner ohne Installationsmöglichkeit
    pg=page('Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',{'width':1200,'height':800}); print('Rechner ohne Meldung: sichtbar',not pg.evaluate("$('install').hidden"))
    print('Fehler:',errs); b.close()
