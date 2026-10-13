const R=require('./gbroute.js'),C=R.C;
const dir=q=>((Math.atan2(-q.u,-q.v)*180/Math.PI+360)%360).toFixed(0).padStart(3)+'/'+Math.hypot(q.u,q.v).toFixed(0).padStart(2);
const Hs=[100,300,600,1000,1500,2000,2500,3000,4000,5000,6000];
console.log('Wind (aus Grad / m/s) am Startplatz je Hoehe ueber Start; Spalten: Stunde nach Start 0,3,6,9,12');
for(const h of Hs){let s='';for(const th of [0,3,6,9,12]){s+=' '+dir(C.atmAt(R.column(R.START[0],R.START[1],R.T0+th*3600e3),h));}console.log(String(h).padStart(5),s);}
console.log('\nDrift in fester Hoehe (ohne Ballonphysik), Position nach 12/24/36/48/60 h, km vom Start');
for(const h of Hs){let lat=R.START[0],lon=R.START[1],s='';for(let t=0;t<60*3600;t+=600){const a=C.atmAt(R.column(lat,lon,R.T0+t*1000),h);lat+=a.v*600/111320;lon+=a.u*600/(111320*Math.cos(lat*Math.PI/180));if((t+600)%(12*3600)===0)s+='  '+lat.toFixed(1)+'/'+lon.toFixed(1)+' '+(R.geoDist(R.START[0],R.START[1],lat,lon)/1000).toFixed(0).padStart(4);}console.log(String(h).padStart(5),s);}
// entlang der Siegerspur: welche Hoehe traegt in Spurrichtung?
const W=[[51.56,6.97],[54.0,11.0],[54.7,12.6],[55.3,15.0],[56.5,18.5],[57.6,20.6],[58.8,22.6],[59.6,24.4],[60.5,25.5]];
console.log('\nEntlang der Siegerspur: Kurs zum naechsten Punkt und Windrichtung-wohin je Hoehe (Stunde geschaetzt bei 12 m/s)');
let t=0;for(let i=0;i<W.length-1;i++){const a=W[i],b=W[i+1];const crs=(Math.atan2((b[1]-a[1])*Math.cos(a[0]*Math.PI/180),b[0]-a[0])*180/Math.PI+360)%360;
 for(const tt of [t, t*1.5]){let s='';for(const h of Hs){const q=C.atmAt(R.column(a[0],a[1],R.T0+tt*1000),h);s+=' '+((Math.atan2(q.u,q.v)*180/Math.PI+360)%360).toFixed(0).padStart(3)+'/'+Math.hypot(q.u,q.v).toFixed(0).padStart(2);}
 console.log(a.join('/').padEnd(11),'Kurs',crs.toFixed(0).padStart(3),'t',(tt/3600).toFixed(0).padStart(2)+'h',s);}
 t+=R.geoDist(a[0],a[1],b[0],b[1])/12;}
console.log('Hoehen:',Hs.join(' '));
