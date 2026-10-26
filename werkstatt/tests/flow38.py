from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
h1=h
def h(r):
    u=r.request.url
    if 'archive-api.open-meteo' in u:
        REQ.append(u); return r.fulfill(body=hist(u),content_type='application/json')
    return h1(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':720},locale='de-DE',device_scale_factor=2); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(2500); ev("store.set('gb-news',BUILD)")
    print('Menütext:',ev("$('m-champ').textContent")[:110])
    ev("$('m-name').value='Erich'; $('m-name').dispatchEvent(new Event('input'))")
    pg.click('#m-champ'); pg.wait_for_timeout(300); pg.screenshot(path='/mnt/user-data/outputs/Szenario_Auswahl.png')
    print('Karten:',ev("[...document.querySelectorAll('#gbsc-list .mbtn b')].map(x=>x.textContent)"),'| Länder',ev("$('gbsc-ctry').options.length"),ev("[...$('gbsc-ctry').options].slice(0,4).map(o=>o.text)"))
    pg.select_option('#gbsc-ctry','GER'); print('Land gespeichert:',ev("UI.ctry"))
    pg.click('#gbsc-list .mbtn:nth-child(2)'); pg.wait_for_timeout(200); print('Rückfrage:',ev("$('cf-text').textContent")[:60]); pg.click('#cf-ok'); pg.wait_for_function("STATE==='brief'",timeout=20000)
    print('Szenario',ev("GB.sc.id"),'Start',ev("[START.lat,START.lon]"),'Teams',ev("GB_TEAMS.length"),'Sperrflächen',ev("GB.ban.length"),'Vorflug versteckt',ev("$('sw-pv').hidden"))
    print('Wetterabruf:',REQ[-1].split('?')[0],urllib.parse.parse_qs(urllib.parse.urlparse(REQ[-1]).query)['start_date'])
    print('Geschichte:',ev("$('sw-target').textContent")[:140])
    print('Landepunkte an Land:',ev("GB_TEAMS.filter(t=>t[5]!=null).map(t=>gbOnLand(t[5],t[6])?1:0).join('')"))
    pg.click('#sw-go'); pg.wait_for_timeout(500); pg.screenshot(path='r_map.png')
    print('Tooltip am Ballon:',ev("balMk.getTooltip()&&balMk.getTooltip().getContent()"))
    res=ev("(()=>{B.landed=true;B.vLand=1;const rows=[];const r=gbResult(rows);return [r.list.find(x=>x.me),r.list.length,$('r-head').textContent]})()")
    print('Auswertung:',res,'| Liste 2018:',ev("store.get('gb-list62')"),'| Liste 2026:',ev("store.get('gb-list69')"))
    ev("showScores()"); pg.wait_for_timeout(300); pg.click('#sc-kind button[data-v=gb62]'); pg.wait_for_timeout(500); pg.screenshot(path='r_scores.png')
    print('Bestenliste 2018:',ev("$('sc-list').textContent")[:120])
    ev("gbUse('gb69')"); print('zurück auf 2026:',ev("[GB.sc.id,GB_TEAMS.length,GB.ban.length]"))
    print('Fehler',errs); b.close()
