function geoDist(la1, lo1, la2, lo2){
  const a = 6378137, f = 1 / 298.257223563, b = a * (1 - f), R = Math.PI / 180;
  const U1 = Math.atan((1 - f) * Math.tan(la1 * R)), U2 = Math.atan((1 - f) * Math.tan(la2 * R)), L = (lo2 - lo1) * R;
  const sU1 = Math.sin(U1), cU1 = Math.cos(U1), sU2 = Math.sin(U2), cU2 = Math.cos(U2);
  let lam = L, sS = 0, cS = 1, sig = 0, cSqA = 1, c2SM = 0;
  for (let i = 0; i < 60; i++){ const sL = Math.sin(lam), cL = Math.cos(lam);
    sS = Math.hypot(cU2 * sL, cU1 * sU2 - sU1 * cU2 * cL); if (sS === 0) return 0;
    cS = sU1 * sU2 + cU1 * cU2 * cL; sig = Math.atan2(sS, cS);
    const sA = cU1 * cU2 * sL / sS; cSqA = 1 - sA * sA; c2SM = cSqA ? cS - 2 * sU1 * sU2 / cSqA : 0;
    const C = f / 16 * cSqA * (4 + f * (4 - 3 * cSqA)), l2 = L + (1 - C) * f * sA * (sig + C * sS * (c2SM + C * cS * (-1 + 2 * c2SM * c2SM)));
    if (Math.abs(l2 - lam) < 1e-12){ lam = l2; break; } lam = l2; }
  const uSq = cSqA * (a * a - b * b) / (b * b), A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq))), Bq = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)));
  return b * A * (sig - Bq * sS * (c2SM + Bq / 4 * (cS * (-1 + 2 * c2SM * c2SM) - Bq / 6 * c2SM * (-3 + 4 * sS * sS) * (-3 + 4 * c2SM * c2SM))));
}
const T=[["Ostróda",1145.29,53.696,19.965],["Salerno",882.37,40.682,14.769],["Wolsztyn",840.59,52.116,16.115],["Roccavivara",804.98,41.832,14.600],["Labouheyre",722.93,44.213,-0.921],["Aire-sur-l'Adour",696.40,43.702,-0.263],["Miramont-de-Guyenne",607.32,44.602,0.361],["Casseneuil",603.12,44.443,0.622],["Villeneuve-sur-Lot",593.48,44.408,0.705],["Agonac",546.58,45.293,0.750],["Le Peyrat(09)",541.72,42.955,1.920],["Peyrat-le-Château",541.72,45.815,1.772],["Brive",501.77,45.159,1.533],["Pleaux",457.79,45.135,2.227],["Issoudun",411.69,46.949,1.993],["Pordenone",409.26,45.956,12.660],["Treviso",366.84,45.666,12.243],["Bruneck",333.46,46.796,11.936],["Montélimar",326.65,44.558,4.751],["Verdabbio",148.55,46.267,9.157],["Pontarlier",93.24,46.904,6.354]];
const S=[46.958,7.462];
let best=null;for(let la=46.85;la<=47.05;la+=0.002)for(let lo=7.30;lo<=7.62;lo+=0.003){let e=0;for(const t of T){if(t[0].startsWith('Le Peyrat')||t[0].startsWith('Peyrat'))continue;const d=geoDist(la,lo,t[2],t[3])/1000-t[1];e+=d*d;}if(!best||e<best.e)best={la,lo,e};}
console.log('Fit Start',best.la.toFixed(3),best.lo.toFixed(3),'rms',Math.sqrt(best.e/19).toFixed(1),'km; Abstand zur Allmend',(geoDist(best.la,best.lo,S[0],S[1])/1000).toFixed(1),'km');
for(const t of T) console.log(t[0].padEnd(22),t[1],'Allmend:',(geoDist(S[0],S[1],t[2],t[3])/1000).toFixed(1),'Fit:',(geoDist(best.la,best.lo,t[2],t[3])/1000).toFixed(1));
