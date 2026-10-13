from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
JS_LINE = r"""
window.prallZ = () => { const Tex = B.Tg - atmAt(ATM, B.h).T; for (let z = 0; z < 9000; z += 10){ const a = atmAt(ATM, z); if (B.gas * R_GAS * (a.T + Tex) / a.p >= CFG.vol) return z; } return null; };
const _dp = drawProf; window.drawProf = drawProf = function(){ _dp(); const cv = $('prof-cv'), W = cv.clientWidth, H = cv.clientHeight, c = cv.getContext('2d');
  const top = Math.min(9000, Math.max(6000, Math.ceil((B.h + 300) / 1000) * 1000)), zb = Math.min(0, Math.floor(Math.min(B.gnd, B.h) / 500) * 500), y = z => H - 18 - (z - zb) / (top - zb) * (H - 40);
  const z = prallZ(); if (z == null) return; const Y = y(z); c.save(); c.setLineDash([5, 3]); c.strokeStyle = '#ffe14d'; c.lineWidth = 1.6; c.beginPath(); c.moveTo(27, Y); c.lineTo(W, Y); c.stroke(); c.setLineDash([]);
  c.fillStyle = '#ffe14d'; c.font = '600 11px "Barlow Condensed","Arial Narrow",sans-serif'; c.textAlign = 'right'; c.textAlign = 'left'; c.fillText('prall', 29, Y - 3); c.restore(); };
"""
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':360,'height':720},locale='de-DE',device_scale_factor=2); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2000); ev("store.set('gb-news',BUILD)")
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500)
    ev(JS_LINE)
    ev("B.go=true;B.air=true;B.h=900;B.w=0.8;setPaused(true)"); ev("(()=>{const a=atmAt(ATM,1700);B.gas=a.p*CFG.vol/(R_GAS*(a.T+(B.Tg-atmAt(ATM,B.h).T)));})()")
    pg.wait_for_timeout(500); ev("drawProf()"); print('prall bei', ev('prallZ()'), 'Füllgrad', ev('Math.round(fillNow()*100)'))
    pg.screenshot(path='n1.png')
    ev("B.h=prallZ()+5;B.full=true;updInst&&updInst()"); pg.wait_for_timeout(400); ev("toast('Prallhöhe erreicht');drawProf()"); pg.wait_for_timeout(300)
    pg.wait_for_timeout(300); pg.screenshot(path='n2.png'); b.close()
a=Image.open('n1.png'); bb=Image.open('n2.png'); out=Image.new('RGB',(a.width*2+30,a.height),(20,30,45)); out.paste(a,(0,0)); out.paste(bb,(a.width+30,0)); out.save('/mnt/user-data/outputs/Prallhoehe_Vorschlag2.png'); print('ok')
