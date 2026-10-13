const C=require('./core.js');const cfg=Object.assign({},C.DEFAULT_CFG);
function mk(hourSolar,lapse){const wx=JSON.parse(JSON.stringify(C.SIM_WX)); wx.layers=[[1e5,-lapse/1000]]; wx.t0=Date.UTC(2026,5,21,0,0)+hourSolar*3600e3-12.2946/15*3600e3; const tab=C.buildAtm(wx); return {tab,B:C.newBalloon(cfg,tab)};}
for(const hr of [7,12,2]){const {tab,B}=mk(hr,6.5); C.stepBalloon(B,cfg,tab,1,0); console.log('Start',hr,'Uhr: Trimmballast',B.trim.toFixed(1),'kg, Überschuss am Boden',B.free.toFixed(2),'kg, Gas−Luft',(B.Tg-C.atmAt(tab,0).T).toFixed(1),'K');}
// Selbststeuerung hält 500 m; Verbrauch je Stunde über 24 h
function day(start,hours,h){const {tab,B}=mk(start,6.5); let s0=C.sandKg(B,cfg),g0=B.gas, out=[];
  for(let t=0;t<hours*3600&&!B.landed;t++){ if(t%10===0)C.autopilot(B,cfg,tab,h); C.stepBalloon(B,cfg,tab,1,0);
    if(t%3600===3599){const a=C.atmAt(tab,B.h); const hr=(start+(t+1)/3600)%24; out.push(String(hr).padStart(2)+' Uhr: '+B.h.toFixed(0).padStart(4)+' m, Sonne '+(Math.asin(B.sun)*180/Math.PI).toFixed(0).padStart(3)+'°, Gas−Luft '+((B.Tg-a.T)>=0?'+':'')+(B.Tg-a.T).toFixed(1)+' K, Sand −'+(s0-C.sandKg(B,cfg)).toFixed(1).padStart(5)+' kg, Gas −'+(100*(1-B.gas/g0)).toFixed(1)+' %'); s0=C.sandKg(B,cfg); g0=B.gas;}}
  console.log(out.join('\n')); console.log('  Sand am Ende',C.sandKg(B,cfg).toFixed(0),'kg', B.landed?'GELANDET':'');}
day(12,24,500);
