const C=require('./core.js');const cfg=Object.assign({},C.DEFAULT_CFG);
function mk(hourSolar,lapse,day){const wx=JSON.parse(JSON.stringify(C.SIM_WX)); if(lapse)wx.layers=[[1e5,-lapse/1000]]; if(hourSolar!=null)wx.t0=Date.UTC(2026,5,day||21,0,0)+hourSolar*3600e3-12.2946/15*3600e3; const tab=C.buildAtm(wx); return {tab,B:C.newBalloon(cfg,tab)};}
for(const [n,hr] of [['Sim-Morgen 7 Uhr',null],['Mittag',12],['Nacht 2 Uhr',2]]){const {tab,B}=mk(hr); const a=C.atmAt(tab,0); console.log('Am Startplatz,',n+': Gas−Luft',(B.Tg-a.T).toFixed(1),'K, Hülle−Luft',(B.Tf-a.T).toFixed(1),'K; nötiger Abwurf bis zum Loslassen',(30-(C.atmAt(tab,0).p*0.028964/(8.314462*a.T)*cfg.vol-B.gas*0.002016-(C.sandKg(B,cfg)+cfg.rust+cfg.equip+cfg.pax*cfg.paxKg))).toFixed(1),'kg');}
function fly(n,hr,lapse,kg,T,act){const {tab,B}=mk(hr,lapse); for(let i=0;i<kg*5;i++)C.dropScoop(B,cfg); const o=[]; let hmax=0;
  for(let t=0;t<=T&&!B.landed;t+=0.5){ if(act)act(B,t,tab); C.stepBalloon(B,cfg,tab,0.5,0); hmax=Math.max(hmax,B.h); if(t%1800===0&&t>0){const a=C.atmAt(tab,B.h); o.push(B.h.toFixed(0)+'m('+(B.Tg-a.T>=0?'+':'')+(B.Tg-a.T).toFixed(1)+'K)');} }
  console.log(n+': Gipfel '+hmax.toFixed(0)+' m | alle 30 min: '+o.join(' ')+(B.landed?' | gelandet nach '+(B.t/60).toFixed(0)+' min':'')+' | Sand übrig '+C.sandKg(B,cfg).toFixed(0)+' kg, Gas '+(100*B.gas/B.gas0).toFixed(1)+' %'); return B;}
fly('Sim-Morgen (7 Uhr), 31 kg ab, 4 h ohne Eingriff',null,null,31,4*3600);
fly('Mittag, Normalatmosphäre, 31 kg ab, 3 h',12,6.5,31,3*3600);
fly('Nacht 2 Uhr, Normalatmosphäre, 32 kg ab, 3 h',2,6.5,32,3*3600);
// Tag in die Nacht: Start 17 Uhr, mit einfachem Piloten: bei Sinken über 0,5 m/s unter 300 m eine Schaufel alle 10 s
let used=0; const B=fly('Start 17 Uhr über den Sonnenuntergang, 8 h, Pilot fängt unter 400 m ab',17,6.5,31,8*3600,(B,t)=>{ if(B.air&&B.h<400&&B.w<-0.3&&t%10===0){C.dropScoop(B,cfg);used+=0.2;} });
console.log(' dafür nachgeworfen:',used.toFixed(1),'kg');
