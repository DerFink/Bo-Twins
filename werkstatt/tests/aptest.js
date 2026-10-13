const R=require('./gbroute.js'),C=require('./core.js');
function run(hours, P){
  const S=R.start(); R.advance(S,[950,1050],2*3600,{ban:0}); const B=S.B, hT=1000, s0=C.sandKg(B,R.cfg), g0=B.gas;
  let dmax=0,sum=0,n=0,out=0,nS=0,nG=0, tab=S.tab, lat=S.lat, lon=S.lon;
  for(let t=0;t<hours*3600;t++){
    if(t%600===0){ lat+=B.n/111320; lon+=B.e/(111320*Math.cos(lat*Math.PI/180)); B.e=0;B.n=0; tab=R.column(lat,lon,R.T0+B.t*1000); B.gnd=Math.max(0,R.elevAt(lat,lon)-R.ZREF); }
    if(t%2===0){ const r=C.holdAlt(B,R.cfg,tab,hT,null,P); if(r.sand) nS++; if(r.gas) nG++; }
    C.stepBalloon(B,R.cfg,tab,1,0);
    if(t>600){ const d=Math.abs(B.h-hT); dmax=Math.max(dmax,d); sum+=d; n++; if(d>5) out++; }
    if(B.landed) break;
  }
  return {Stunden:hours, Sand_kg:(s0-C.sandKg(B,R.cfg)).toFixed(1), Gas_pct:(100*(g0-B.gas)/B.gas0).toFixed(1), Abw_max:dmax.toFixed(1), Abw_mittel:(sum/n).toFixed(1), Anteil_ausserhalb_5m:(100*out/n).toFixed(1)+'%', Sandgaben:nS, Gasgaben:nG, gelandet:B.landed};
}
for (const P of JSON.parse(process.argv[2])) console.log(JSON.stringify(P), JSON.stringify(run(+process.argv[3]||4,P)));
