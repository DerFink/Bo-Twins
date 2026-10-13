from playwright.sync_api import sync_playwright
import json, urllib.parse, gzip, struct, array
exec(open('flow7.py').read().split("with sync_playwright()")[0])
base=json.loads(wx); n=72; CNT={'n':0,'limited':0}
def h2(r):
    u=r.request.url
    if 'historical-forecast-api' in u:
        CNT['n']+=1
        if CNT['n']==3 and not CNT['limited']: CNT['limited']=1; return r.fulfill(status=429,body='{"error":true,"reason":"Minutely API request limit exceeded. Please try again in one minute."}',content_type='application/json')
        q=urllib.parse.parse_qs(urllib.parse.urlparse(u).query); la=q['latitude'][0].split(','); lo=q['longitude'][0].split(','); out=[]
        for a,b in zip(la,lo):
            jj={'latitude':float(a),'longitude':float(b),'elevation':round(100+float(a)),'hourly':{k:v[:n] for k,v in base['hourly'].items()}}
            jj['hourly']['time']=['2026-08-%02dT%02d:00'%(29+i//24,i%24) for i in range(n)]; jj['hourly']['precipitation']=[0.3]*n; jj['hourly']['cloud_cover']=[55]*n
            jj['hourly']['temperature_2m']=[float(a)-40+float(b)/10]*n
            out.append(jj)
        return r.fulfill(body=json.dumps(out),content_type='application/json')
    return h(r)
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]; c=b.new_context(viewport={'width':390,'height':844},locale='de-DE',accept_downloads=True); pg=c.new_page(); ev=lambda s: pg.evaluate(s)
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.route('**/*', h2); pg.goto(FILE); pg.wait_for_timeout(2500)
    # Fallgeräusch
    pg.click('#m-chal'); pg.click('#chal [data-task="wz"]'); pg.click('#seg-wx button[data-v="sim"]'); pg.click('#su-go'); pg.wait_for_function("STATE==='brief'",timeout=20000); pg.click('#sw-go'); pg.wait_for_timeout(300)
    ev("window.__osc=0; const O=AudioContext.prototype.createOscillator; AudioContext.prototype.createOscillator=function(){window.__osc++; return O.call(this)}; B.h=180;B.air=true;B.go=true;0")
    pg.click('#mk-drop'); pg.wait_for_timeout(1500); print('Säckchen fällt: Töne erzeugt',ev('window.__osc')>=2,'| im Fall',ev('FLY.length'),'| Resthöhe',ev("(FLY[0].z/FLY[0].z0).toFixed(2)"))
    pg.click('#btn-pause'); pg.wait_for_timeout(200); pg.click('#btn-pause'); pg.click('#seg-speed button[data-v="30"]'); pg.wait_for_function("WZ.drops.length===1",timeout=20000); print('gelandet:',ev("$('toast').textContent"))
    ev("showMenu()")
    # Wetterpaket
    ev("(()=>{const st=window.setTimeout; window.setTimeout=(f,ms,...a)=>st(f,ms/200,...a)})()")
    ev("openSheet(true)"); ev("$('wxp-btn').scrollIntoView()"); pg.click('#wxp-btn'); pg.wait_for_timeout(200); print('Rückfrage:',ev("$('cf-text').textContent")[:110])
    with pg.expect_download(timeout=110000) as d: pg.click('#cf-ok')
    path=d.value.path(); name=d.value.suggested_filename; pg.wait_for_timeout(300); print('Datei:',name,'| Abrufe',CNT['n'],'| Meldung:',ev("$('wxp-info').textContent"))
    raw=open(path,'rb').read(); 
    if name.endswith('.gz'): raw=gzip.decompress(raw)
    assert raw[:6]==b'GBWX1\n'; hl=struct.unpack('<I',raw[6:10])[0]; head=json.loads(raw[10:10+hl]); data=array.array('h'); data.frombytes(raw[10+hl:])
    nP=len(head['lats'])*len(head['lons']); print('Kopf:',{k:head[k] for k in ('nT','rec','levels','fields','extra')},'| Orte',nP,'| Werte',len(data),'soll',nP*head['nT']*head['rec'],'| ungepackt %.1f MB, Datei %.2f MB'%(len(raw)/1e6,len(open(path,'rb').read())/1e6))
    rec=head['rec']; nT=head['nT']
    def val(ip,k,lev,fld): return data[(ip*nT+k)*rec+lev*5+fld]
    ip=5*len(head['lons'])+7; la=head['lats'][5]; lo=head['lons'][7]
    print('Ort',la,lo,': Höhe',val(ip,0,0,0),'(soll',round(100+la),') | T Boden',val(ip,0,0,1)/10,'(soll',round(la-40+lo/10,1),') | 850 hPa (Fläche 6): z',val(ip,10,6,0),'T',val(ip,10,6,1)/10,'u',val(ip,10,6,2)/10,'v',val(ip,10,6,3)/10,'Wolke',val(ip,10,6,4))
    k=10; H=base['hourly']; import math
    sp=H['wind_speed_850hPa'][k]; dd=H['wind_direction_850hPa'][k]; print('  Beispieldaten 850 hPa: z',H['geopotential_height_850hPa'][k],'T',H['temperature_850hPa'][k],'u',round(-sp*math.sin(math.radians(dd)),1),'v',round(-sp*math.cos(math.radians(dd)),1))
    o=(ip*nT+k)*rec+13*5; print('  Zusatz: Druck',data[o]/10+1000,'(Beispiel',H['surface_pressure'][k],') Niederschlag',data[o+1]/10,'Bedeckung',data[o+2])
    print('Fehler:',errs); b.close()
