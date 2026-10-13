const C=require('./core.js');const cfg=Object.assign({},C.DEFAULT_CFG);
const D=Math.cbrt(6*cfg.vol/Math.PI),A=Math.PI*D*D; console.log('Hülle: Durchmesser',D.toFixed(2),'m, Fläche',A.toFixed(0),'m², Flächengewicht',(cfg.envKg/A*1000).toFixed(0),'g/m²');
for(const [n,ms,lat,lon] of [['21.6. 12 Uhr Sonnenzeit Bitterfeld',Date.UTC(2026,5,21,12,0)-12.29/15*3600e3,51.62,12.29],['21.12. Mittag',Date.UTC(2026,11,21,12,0)-12.29/15*3600e3,51.62,12.29],['Sim-Start',C.simT0(12.29),51.62,12.29],['29.8. 02:45 MESZ Gladbeck',Date.UTC(2026,7,29,0,45),51.56,6.97],['29.8. 06:40 MESZ',Date.UTC(2026,7,29,4,40),51.56,6.97]]) console.log(' Sonnenhöhe',n+':',(Math.asin(C.sunSin(lat,lon,ms))*180/Math.PI).toFixed(1)+'°');
// Schweben in fester Höhe: Gleichgewichtstemperaturen
function hover(h,hourSolar,cloudAbove,cloudBelow,rain,T){
  const wx=JSON.parse(JSON.stringify(C.SIM_WX)); wx.layers=[[1e5,-0.0065]]; wx.t0=Date.UTC(2026,5,21,0,0)+hourSolar*3600e3-C.DEFAULT_CFG&&0||Date.UTC(2026,5,21,0,0)+hourSolar*3600e3-12.2946/15*3600e3;
  const tab=C.buildAtm(wx); tab.forEach((r,i)=>{const z=i*25; r.c=(cloudAbove&&z>h+300&&z<h+800)?1:(cloudBelow&&z<h-300&&z>h-800)?1:0;}); tab.rain=rain||0;
  const B=C.newBalloon(cfg,tab,C.loadout(cfg,tab)); B.air=true;B.go=true;B.h=h; B.gas*=0.90; const t0=B.t0;
  for(let t=0;t<(T||5400);t+=1){B.h=h;B.w=0;B.t0=t0-t*1000+0; C.stepBalloon(B,cfg,tab,1,0); B.Tg*=Math.pow(C.atmAt(tab,h).p/C.atmAt(tab,B.h).p,8.314462/28.83); B.h=h;B.w=0;}   // Uhrzeit festhalten
  const a=C.atmAt(tab,h); return {dTg:B.Tg-a.T,dTf:B.Tf-a.T,qSun:B.qSun/1000,qIR:B.qIR/1000,wet:B.wet,free:B.free};
}
const f=x=>(x>=0?'+':'')+x.toFixed(1);
console.log('Fall                                  | Hülle−Luft | Gas−Luft | Sonne kW | Wärmestr. kW | Auftrieb gegenüber Gas=Luft');
const base=hover(500,12,false,false,0); 
for(const [n,args] of [['Mittag, klar, 500 m',[500,12]],['Mittag, klar, 3000 m',[3000,12]],['Morgen 7 Uhr, klar, 500 m',[500,7]],['Mittag, Wolken darüber, 500 m',[500,12,true]],['Mittag, über Wolken, 3000 m',[3000,12,false,true]],['Nacht, klar, 500 m',[500,0]],['Nacht, klar, 3000 m',[3000,0]],['Nacht, Wolken darüber, 500 m',[500,0,true]]]){
  const r=hover(...args); console.log(n.padEnd(38)+'| '+f(r.dTf).padStart(7)+' K  | '+f(r.dTg).padStart(6)+' K | '+r.qSun.toFixed(1).padStart(7)+'  | '+f(r.qIR).padStart(9)+'    | '+f(r.dTg*4.05)+' kg'); }
// Regen
for(const mm of [0.5,2,8]){ let o=[]; for(const T of [300,900,1800,3600]){ o.push((T/60)+' min: '+hover(500,12,true,false,mm,T).wet.toFixed(1)+' kg'); } console.log('Regen',mm,'mm/h unter der Wolke:',o.join(', ')); }
console.log('über der Wolke bei Regen am Boden:',hover(3000,12,false,true,2,1800).wet.toFixed(1),'kg');
