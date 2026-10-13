const C=require('./core.js');const cfg=Object.assign({},C.DEFAULT_CFG);
for(const lv of [0,1,2]){let t=Date.now(),n=0,ok=0;for(let i=0;i<5;i++){const tab=C.buildAtm(C.randomWx(Math.random,false));const r=C.makeTarget(cfg,tab,lv,Math.random);n++;if(r)ok++;}console.log('Stufe',lv,'Mittel',((Date.now()-t)/n).toFixed(0),'ms',ok+'/'+n);}
let t=Date.now();const tab=C.buildAtm(C.randomWx(Math.random,false));C.makeCrosses(cfg,tab,Math.random);console.log('Wandziel',Date.now()-t,'ms');t=Date.now();C.bestDistance(cfg,tab,3600);console.log('MDT',Date.now()-t,'ms');
