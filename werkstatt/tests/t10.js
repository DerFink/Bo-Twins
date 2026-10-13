const C=require('./core.js');
const dd=(a,b)=>((b-a+540)%360)-180;
for(const full of [false,true]){
  let turns=[],t6=[],rev=[],cover=0,N=400,layers=[];
  for(let k=0;k<N;k++){ const wx=C.randomWx(Math.random,full); let acc=0,a3=0,ch=0,last=null; const seen=new Set();
    for(let i=1;i<wx.wind.length-1;i++){ const d=dd(wx.wind[i-1][1],wx.wind[i][1]); acc+=d; if(wx.wind[i][0]===3000)a3=acc; seen.add(Math.floor(wx.wind[i][1]/10)); if(Math.abs(d)>12){ch++;} }
    turns.push(Math.abs(a3)); t6.push(Math.abs(acc)); layers.push(ch); if(seen.size===36)cover++; }
  const s=a=>{a=[...a].sort((x,y)=>x-y);return a[0].toFixed(0)+' / '+a[a.length>>1].toFixed(0)+' / '+a[a.length-1].toFixed(0)};
  console.log(full?'MID':'Simulation','| Drehung bis 3000 m (min/Median/max):',s(turns),'| bis 6000 m:',s(t6),'| 100-m-Stufen mit über 12° Drehung:',s(layers),'| alle 36 Sektoren:',cover+'/'+N);
}
const wx=C.randomWx(); console.log('Beispiel:',wx.wind.filter(w=>w[0]%500===0).map(w=>w[0]+':'+w[1].toFixed(0)+'°/'+w[2].toFixed(1)).join('  '));
