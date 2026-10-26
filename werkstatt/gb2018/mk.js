eval(require('fs').readFileSync('fit.js','utf8').split('const T=')[0]);
const S=[46.958,7.462];
const R=[["POL-2","Rękas, Bogdański",1145.29,"58h 28m","Ostróda, POL",53.696,19.965],["USA-2","Cayton, Smith",882.37,"56h 20m","bei Salerno, ITA",40.682,14.769],["GER-1","Zenge, Eimers",840.59,"66h 27m","Wolsztyn, POL",52.116,16.115],
["POL-1","Zapart, Borkowski",804.98,"50h 31m","Roccavivara, ITA",41.832,14.600],["FRA","Leys, Houver",722.93,"33h 54m","Labouheyre, FRA",44.213,-0.921],["SUI","Tièche, Sciboz",696.40,"36h 18m","Aire-sur-l'Adour, FRA",43.702,-0.263],
["FRA","Péterlé, Pelard",607.32,"32h 55m","Miramont-de-Guyenne, FRA",44.602,0.361],["SUI","Frieden, Hugi",603.12,"30h 52m","Casseneuil, FRA",44.443,0.622],["FRA","Decellières, Moine",593.48,"32h 08m","Villeneuve-sur-Lot, FRA",44.408,0.705],
["GER","Munz, Schlegel",546.58,"23h 23m","Agonac, FRA",45.293,0.750],["BEL","Peirsman, De Cock",541.72,"23h 57m","Le Peyrat, FRA",null,null],["USA","Sullivan, White",501.77,"22h 45m","Brive-la-Gaillarde, FRA",45.159,1.533],
["AUT","Lewetz, Wagner",457.79,"23h 35m","Pleaux, FRA",45.135,2.227],["GER","Zumrode, Hünekühl",411.69,"41h 47m","Issoudun, FRA",46.949,1.993],["AUS","Wilson, McCarron",409.26,"17h 27m","Pordenone, ITA",45.956,12.660],
["AUT","Stürzlinger, Herndl",366.84,"18h 21m","Treviso, ITA",45.666,12.243],["SUI","Gschwendtner, Krebs",333.46,"12h 03m","Bruneck, ITA",46.796,11.936],["JPN","Ichiyoshi, Hashimoto",326.65,"11h 51m","Montélimar, FRA",44.558,4.751],
["RUS","Tyukhtyaev, Sadkovskaya",148.55,"20h 45m","Verdabbio, SUI",46.267,9.157],["CZE","Smrčka, Vašíček",93.24,"11h 44m","Pontarlier, FRA",46.904,6.354]];
const rad=Math.PI/180;
function dest(la,lo,brg,dkm){const d=dkm/6371.0088,a=la*rad,b=lo*rad,t=brg*rad;const la2=Math.asin(Math.sin(a)*Math.cos(d)+Math.cos(a)*Math.sin(d)*Math.cos(t));const lo2=b+Math.atan2(Math.sin(t)*Math.sin(d)*Math.cos(a),Math.cos(d)-Math.sin(a)*Math.sin(la2));return [la2/rad,lo2/rad];}
function brg(a,b,c,d){const y=Math.sin((d-b)*rad)*Math.cos(c*rad),x=Math.cos(a*rad)*Math.sin(c*rad)-Math.sin(a*rad)*Math.cos(c*rad)*Math.cos((d-b)*rad);return Math.atan2(y,x)/rad;}
const out=R.map(t=>{if(t[5]==null)return t;const bb=brg(S[0],S[1],t[5],t[6]);let k=t[2];let p;for(let i=0;i<6;i++){p=dest(S[0],S[1],bb,k);k*=t[2]/(geoDist(S[0],S[1],p[0],p[1])/1000);}
 const off=geoDist(p[0],p[1],t[5],t[6])/1000; console.error(t[4].padEnd(26),'Abstand Punkt-Ort',off.toFixed(1),'km');return [t[0],t[1],t[2],t[3],t[4],+p[0].toFixed(4),+p[1].toFixed(4)];});
require('fs').writeFileSync('teams62.json',JSON.stringify(out));
