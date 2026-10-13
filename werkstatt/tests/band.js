const R=require('./gbroute.js'),C=R.C;
function run(bw,hold){ const S=R.start(); R.advance(S,[900,1100],2*3600,{ban:0}); // aufsteigen, einpendeln
  const s0=C.sandKg(S.B,R.cfg), g0=S.B.gas, h0=1000; let dmax=0,sum=0,n=0,out=0;
  for(let t=0;t<hold;t+=60){ R.advance(S,[h0-bw,h0+bw],60,{ban:0}); const d=Math.abs(S.B.h-h0); dmax=Math.max(dmax,d); sum+=d; n++; if(d>bw+2) out++; if(!S.ok) break; }
  return {band:bw, Sand_kg:(s0-C.sandKg(S.B,R.cfg)).toFixed(0), Gas_pct:(100*(g0-S.B.gas)/S.B.gas0).toFixed(1), Abw_max:dmax.toFixed(0), Abw_mittel:(sum/n).toFixed(0), Minuten_ausserhalb:out, ok:S.ok, why:S.why};}
for(const bw of [5,15,30]) console.log(JSON.stringify(run(bw,10*3600)));
