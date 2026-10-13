// Beispieldaten für das Wettermodell: 72 Stunden ab heute 0 UTC; der Wind dreht je Stunde um 10 Grad und nimmt zu
const lv=[1000,975,950,925,900,850,800,700,600,500,400,300,250], zz=[110,320,540,760,990,1460,1950,3010,4200,5570,7180,9160,10360], TT=[11,9.5,8,9,7.5,4,1,-5,-12,-22,-34,-48,-55];
const H={time:[],temperature_2m:[],wind_speed_10m:[],wind_direction_10m:[],surface_pressure:[]}; const d0=new Date(); d0.setUTCHours(0,0,0,0);
for(let h=0;h<72;h++){const d=new Date(d0.getTime()+h*3600e3);H.time.push(d.toISOString().slice(0,16));H.temperature_2m.push(12);H.wind_speed_10m.push(3+h*0.05);H.wind_direction_10m.push((210+h*10)%360);H.surface_pressure.push(1003.2);
 lv.forEach((L,i)=>{for(const [k,v] of [['temperature',TT[i]],['wind_speed',4+i*1.5+h*0.05],['wind_direction',(220+i*9+h*10)%360],['geopotential_height',zz[i]]]){(H[k+'_'+L+'hPa']=H[k+'_'+L+'hPa']||[]).push(v);}});}
require('fs').writeFileSync('wxmock.json',JSON.stringify({latitude:51.62,longitude:12.30,elevation:80,hourly:H}));
