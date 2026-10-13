from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    print('BUILD',ev('BUILD'),'Route max km',ev('GB_ROUTES.max.km'),'Punkte',ev('GB_ROUTES.max.log.length'))
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(400)
    ev("B.go=true;B.air=true;B.h=900;SIDE.user=true;setPaused(true);window.G0=B.gas")
    fs=[1,0.8,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
    ev("(()=>{const d=document.createElement('div');d.id='strip';d.style.cssText='position:fixed;left:0;top:0;z-index:99999;background:#1d4a6b;padding:6px;display:flex;gap:2px';d.innerHTML=%s.map(f=>balloonSVG('#ff9f1c',f)).join('');document.body.appendChild(d)})()" % fs)
    pg.screenshot(path='m_icons.png',clip={'x':0,'y':0,'width':360,'height':70}); ev("$('strip').remove()")
    from PIL import Image
    ims=[]
    for f in fs:
        ev("B.gas=window.G0*%s"%f); pg.wait_for_timeout(350)
        r=ev("(()=>{const q=$('side').getBoundingClientRect();return [q.left,q.top,q.width,q.height]})()")
        pg.screenshot(path='l_tmp.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); ims.append(Image.open('l_tmp.png').copy()); print(f, ev('Math.round(fillNow()*100)'))
    W=sum(i.width for i in ims[:5]); H=ims[0].height; out=Image.new('RGB',(W,H*2))
    x=0
    for k,i in enumerate(ims[:5]): out.paste(i,(x,0)); x+=i.width
    x=0
    for k,i in enumerate(ims[5:]): out.paste(i,(x,H)); x+=i.width
    out.save('m_side.png'); print('Fehler',errs); b.close()
