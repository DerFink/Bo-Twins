from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(400)
    ev("B.go=true;B.air=true;B.h=900;B.gas=B.gas*0.02;SIDE.user=true;setPaused(true)"); pg.wait_for_timeout(600)
    r=ev("(()=>{const q=$('side').getBoundingClientRect();return [q.left,q.top,q.width,q.height,$('side').hidden]})()"); print(r, ev('Math.round(fillNow()*100)'))
    pg.screenshot(path='k_wurst.png',clip={'x':r[0],'y':r[1],'width':r[2],'height':r[3]}); b.close()
