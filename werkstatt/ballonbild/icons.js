const fs=require('fs');const s=fs.readFileSync('/mnt/user-data/outputs/spiel/index.html','utf8');
const grab=n=>{const i=s.indexOf('function '+n+'(');let d=0,j=s.indexOf('{',i);for(let k=j;;k++){if(s[k]=='{')d++;else if(s[k]=='}'){d--;if(!d)return s.slice(i,k+1);}}};
const bl=s.slice(s.indexOf('const BAL = {'),s.indexOf('function balDraw('));
eval(grab('hullProf')+'\n'+bl+'\nglobalThis.balloonSVG=balloonSVG;');
const inner=balloonSVG('',1,{w:100,k:1.3}).replace(/^<svg[^>]*>/,'').replace(/<\/svg>$/,'');
const mk=(size,pad,rx)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="${-pad} ${-pad+3} ${100+2*pad} ${100+2*pad}"><rect x="${-pad-50}" y="${-pad-50}" width="${200+4*pad}" height="${200+4*pad}" fill="#0e1726"/><g transform="translate(50 ${50-3}) scale(${(100)/118}) translate(-50 -58)">${inner}</g></svg>`;
fs.writeFileSync('i_std.svg',mk(512,16));fs.writeFileSync('i_mask.svg',mk(512,34));
