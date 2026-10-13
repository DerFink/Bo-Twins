const C=require('./core.js');const cfg=Object.assign({},C.DEFAULT_CFG);
for(const f of [1,.7,.5,.2,.1,0]) process.stdout.write(`f=${f}: ${C.dragArea(cfg,f).toFixed(1)} m2  `); console.log();
const tab=C.buildAtm(C.SIM_WX);
// normaler Flug: Aufstieg, dann Gas ganz ablassen aus 3000 m
function run(gasFrac){const B=C.newBalloon(cfg,tab);let t=0;while(!B.go&&t<50){C.dropSack(B,cfg);C.stepBalloon(B,cfg,tab,1,0);t++;}
 for(let i=0;i<4000&&B.h<3000;i++){ if(i%20==0&&B.w<1.5)C.dropSack(B,cfg); C.stepBalloon(B,cfg,tab,0.25,0);} 
 B.gas*=gasFrac; let vmax=0,fill=0; for(let i=0;i<40000&&!B.landed;i++){C.stepBalloon(B,cfg,tab,0.1,0); if(-B.w>vmax){vmax=-B.w;fill=B.fill;}} return [vmax.toFixed(1),(fill*100).toFixed(0),B.landed,B.vLand.toFixed(1)];}
for(const g of [1,0.8,0.5,0.2,0.05,0]) console.log('Gasrest',g,'-> größtes Sinken m/s, Füllgrad %, gelandet, Aufsetzen',run(g).join(' | '));
// Normalfahrt: Vergleich Steigrate bei +30 kg prall
const B=C.newBalloon(cfg,tab);let n=0;while(!B.go&&n<20){C.dropSack(B,cfg);C.stepBalloon(B,cfg,tab,1,0);n++;} for(let i=0;i<600;i++)C.stepBalloon(B,cfg,tab,0.25,0); console.log('Start: Säcke',n,'w nach 150 s',B.w.toFixed(2),'h',B.h.toFixed(0),'fill',B.fill.toFixed(3));
