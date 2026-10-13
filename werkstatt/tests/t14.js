const C=require('./core.js');
function run(name,cfgX,hour,layers,rain,cloud,sacks,T=1800){
  const cfg=Object.assign({},C.DEFAULT_CFG,cfgX); const wx=JSON.parse(JSON.stringify(C.SIM_WX)); wx.layers=layers; wx.t0=Date.UTC(2026,7,29,0,0)+hour*3600e3-6.97/15*3600e3; wx.lat=51.56; wx.lon=6.97;
  const tab=C.buildAtm(wx); if(cloud) tab.forEach((r,i)=>{const z=i*25; r.c=(z>=cloud[0]&&z<=cloud[1])?1:0;}); tab.rain=rain||0;
  const B=C.newBalloon(cfg,tab); for(let i=0;i<sacks;i++)C.dropSack(B,cfg);
  let hmax=0,tGo=null,o=[]; for(let t=0;t<T&&!B.landed;t+=0.25){C.stepBalloon(B,cfg,tab,0.25,0); if(B.go&&tGo==null)tGo=t; hmax=Math.max(hmax,B.h); if(t%300===0&&t>0)o.push(B.h.toFixed(0));}
  console.log(name.padEnd(46)+'| '+sacks+' Säcke: '+(B.go?'los':'GEHALTEN (frei '+B.free.toFixed(1)+' kg)')+' | Gipfel '+hmax.toFixed(0).padStart(4)+' m | alle 5 min: '+o.join(' ')+(B.landed?' | wieder am Boden nach '+(B.t/60).toFixed(0)+' min':'')+(B.wet>1?' | Wasser '+B.wet.toFixed(0)+' kg':''));
}
const GBc={vol:1000,rust:200,equip:90,pax:2,paxKg:80}, std=[[1e5,-0.0065]], inv=[[300,0.020],[1e5,-0.0065]], inv2=[[150,0.040],[1e5,-0.0065]];
for(const s of [2,3,4]){
 run('Nacht 02:45, Normalatmosphäre',GBc,2.75,std,0,null,s);
 run('Nacht, Bodeninversion +6 K bis 300 m',GBc,2.75,inv,0,null,s);
 run('Nacht, scharfe Inversion +6 K bis 150 m',GBc,2.75,inv2,0,null,s);
 run('Nacht, bedeckt ab 800 m, Regen 1 mm/h',GBc,2.75,std,1,[800,2000],s);
 run('Nacht, bedeckt, Regen 4 mm/h',GBc,2.75,std,4,[800,2000],s);
 run('Tag 10 Uhr, bedeckt, Regen 2 mm/h (4 Pers.)',{},10,std,2,[800,2000],s);
 console.log('');
}
