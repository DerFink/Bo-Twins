from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':720},locale='de-DE',device_scale_factor=2); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500)
    ev("store.set('gb-news','2026-10-26.3')"); ev("showMenu()"); pg.wait_for_timeout(1800)
    print('nach Update: Liste offen',not ev("$('news').hidden"),'| Hinweis',ev("$('toast').textContent"))
    pg.screenshot(path='s_menu.png')
    ev("newsOpen()"); pg.wait_for_timeout(300); pg.screenshot(path='s_news.png'); ev("$('news').hidden=true")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v=\"sim\"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500)
    ev("B.go=true;B.air=true;B.h=30;SIDE.user=true;setPaused(true);window.G0=B.gas"); ims=[]
    for f in [1,0.6,0.4,0.2,0.05]:
        ev("B.gas=window.G0*%s"%f); pg.wait_for_timeout(300); r=ev("(()=>{const q=$('side').getBoundingClientRect();return [q.left,q.top,q.width,q.height]})()")
        pg.screenshot(path='l_tmp.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('l_tmp.png').copy())
    W=sum(i.width for i in ims); o=Image.new('RGB',(W,ims[0].height)); x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width
    o.save('s_side.png'); ev("B.gas=window.G0;B.h=400;SIDE.user=false;$('side').hidden=true"); pg.wait_for_timeout(500)
    pg.screenshot(path='s_map.png',clip={'x':100,'y':250,'width':160,'height':200})
    print('Fehler',errs); b.close()
