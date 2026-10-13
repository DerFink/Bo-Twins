from playwright.sync_api import sync_playwright
import json, urllib.parse, datetime
exec(open('flow17.py').read().split(chr(10)+'with sync_playwright() as p:')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':360,'height':740},locale='de-DE'); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h); pg.goto(FILE); pg.wait_for_timeout(3000)
    print('Build',ev('BUILD'))
    pg.click('#m-free'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(500)
    print('Hinweis:',ev("$('hint').textContent"),'| Seitenansicht am Boden sichtbar:',not ev("$('side').hidden"),'| Füllgrad-Zeile:',ev("$('i-fill').parentElement.textContent"))
    pg.click('#rack'); pg.wait_for_timeout(400); pg.screenshot(path='e_start.png'); pg.click('#rack'); pg.wait_for_timeout(2500)
    print('losgelassen',ev('B.go'),'Sandteilchen in der Seitenansicht',ev('SIDE.sand.length'))
    pg.click('#seg-speed button[data-v="10"]'); pg.wait_for_timeout(4000); print('Höhe',ev('Math.round(B.h)'),'Seitenansicht über 50 m:',not ev("$('side').hidden"))
    pg.click('#side-btn'); pg.wait_for_timeout(300); print(' nach Knopf sichtbar:',not ev("$('side').hidden")); pg.screenshot(path='e_high.png'); pg.click('#side'); pg.wait_for_timeout(200); print(' nach Antippen verborgen:',ev("$('side').hidden"))
    # Stüve
    box=pg.locator('#prof').bounding_box(); pg.click('#temp-btn'); pg.wait_for_timeout(400); print('Stüve offen:',not ev("$('stuve').hidden"),); pg.screenshot(path='e_stuve.png')
    pg.click('#stuve'); pg.wait_for_timeout(200); print(' geschlossen:',ev("$('stuve').hidden")); pass
    ev("$('prof').classList.remove('big')")
    # Detail
    ev("balMk.fire('click')"); pg.wait_for_timeout(300); print('Detail:',ev("[...document.querySelectorAll('#dt-rows .kv')].map(x=>x.children[0].textContent+' '+x.children[1].textContent).join(' | ')")); pg.screenshot(path='e_detail.png'); pg.click('#detail'); print(' geschlossen:',ev("$('detail').hidden"))
    # Ventil: sinken bis unter 50 m, Tau
    pg.click('#rope'); pg.wait_for_timeout(300); print('Tau-Rückfrage:',ev("$('cf-text').textContent")); pg.click('#cf-no'); print(' abgebrochen, Tau draußen:',ev('B.rope')); pg.click('#rope'); pg.click('#cf-ok'); pg.wait_for_timeout(200); print(' bestätigt:',ev('B.rope')); pg.click('#rope'); pg.wait_for_timeout(200); print(' zweiter Tipp:',ev('B.rope'),'|',ev("document.querySelector('#toast')?document.querySelector('#toast').textContent:''"))
    ev("SIDE.user=null; B.h=B.gnd+38; B.w=-0.4; valve=0.5"); pg.click('#seg-speed button[data-v="1"]'); pg.wait_for_timeout(1200); print('unter 50 m sichtbar:',not ev("$('side').hidden"),'Gaswolken',ev('SIDE.puff.length'),'Tau liegt auf kg',ev('B.ropeOn.toFixed(1)')); pg.screenshot(path='e_low.png'); ev("valve=0")
    pg.wait_for_timeout(1500); pg.click('#rv-btn'); pg.wait_for_timeout(400); print('Rückblick:',ev("$('rv-read').textContent")); print(' ',ev("$('rv-why').textContent")); pg.screenshot(path='e_rev.png'); pg.click('#rv-close')
    # Einstellungen
    pg.click('#btn-set'); pg.wait_for_timeout(300); pg.click('#seg-ofm button[data-v="1"]'); pg.wait_for_timeout(200); print('Lufträume ein:',ev('UI.ofm'),ev('!!OFM.layer'),'|',ev("__layers.filter(l=>l.kind==='tile'&&l.added).length"),'Kachelebenen'); pg.click('#in-btn'); pg.wait_for_timeout(300); print('Karten und Daten:',ev("[...document.querySelectorAll('#in-rows h3')].map(x=>x.textContent).join(', ')")); pg.screenshot(path='e_info.png',full_page=False); pg.click('#in-close')
    print('Fehler:',[e for e in errs if 'countries-50m' not in e]); b.close()
