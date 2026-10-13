const C=require('./core.js');
const tab=C.buildAtm(C.SIM_WX);
function run(vol,pax,rust,env,free){
  const cfg=Object.assign({},C.DEFAULT_CFG,{vol,pax,rust,envKg:env,holdKg:0});
  const B=C.newBalloon(cfg,tab); const need=C.holdNeed(cfg,tab,B.Tg);
  C.dropKg(B,cfg,free); B.go=true; let maxH=0,w60=0,w300=0;
  for(let t=1;t<=1800;t++){ C.stepBalloon(B,cfg,tab,1,0); maxH=Math.max(maxH,B.h); if(t===60)w60=B.w; if(t===300)w300=B.w; if(B.landed)break; }
  return {vol,free,crewNeed250m:need, w_1min:w60.toFixed(2), w_5min:w300.toFixed(2), maxH_30min:Math.round(maxH), h_end:Math.round(B.h)};
}
for(const [v,p,r,e] of [[400,2,100,60],[1000,4,200,135]]) for(const f of [7.5,15,30]) console.log(JSON.stringify(run(v,p,r,e,f)));
