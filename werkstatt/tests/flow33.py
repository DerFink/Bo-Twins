from playwright.sync_api import sync_playwright
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':360,'height':700},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(400)
    ev("window.LOG=[];const o=SND.valve;SND.valve=function(v){o.call(SND,v)};B.go=true;B.air=true;B.h=900;SIDE.user=true")
    ev("window.SPY=[];const st=AudioParam.prototype.setTargetAtTime;AudioParam.prototype.setTargetAtTime=function(v,t,k){SPY.push(v);try{return st.call(this,v,t,k)}catch(e){return this}}")
    ev("SPY.length=0;SND.valve(0.5)"); print('voll: Zischen-Pegel',ev('SPY[0]'),'leer?',ev('gasEmpty()'))
    ev("B.gas=0;SPY.length=0;SND.valve(0.5)"); print('leer: Zischen-Pegel',ev('SPY[0]'),'leer?',ev('gasEmpty()'),'Füllgrad',ev('fillNow()'))
    ev("valve=0.5;SIDE.puff.length=0"); pg.wait_for_timeout(700); print('Gaswolken bei leerer Hülle:',ev('SIDE.puff.length'),'Fehler',errs); b.close()
