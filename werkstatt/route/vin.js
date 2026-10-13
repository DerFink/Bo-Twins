// Entfernung auf dem WGS84-Ellipsoid (Vincenty), in m
function geoDist(la1, lo1, la2, lo2){
  const a = 6378137, f = 1 / 298.257223563, b = a * (1 - f), R = Math.PI / 180;
  const U1 = Math.atan((1 - f) * Math.tan(la1 * R)), U2 = Math.atan((1 - f) * Math.tan(la2 * R)), L = (lo2 - lo1) * R;
  const sU1 = Math.sin(U1), cU1 = Math.cos(U1), sU2 = Math.sin(U2), cU2 = Math.cos(U2);
  let lam = L, sS = 0, cS = 1, sig = 0, cSqA = 1, c2SM = 0;
  for (let i = 0; i < 60; i++){
    const sL = Math.sin(lam), cL = Math.cos(lam);
    sS = Math.hypot(cU2 * sL, cU1 * sU2 - sU1 * cU2 * cL); if (sS === 0) return 0;
    cS = sU1 * sU2 + cU1 * cU2 * cL; sig = Math.atan2(sS, cS);
    const sA = cU1 * cU2 * sL / sS; cSqA = 1 - sA * sA; c2SM = cSqA ? cS - 2 * sU1 * sU2 / cSqA : 0;
    const C = f / 16 * cSqA * (4 + f * (4 - 3 * cSqA)), l2 = L + (1 - C) * f * sA * (sig + C * sS * (c2SM + C * cS * (-1 + 2 * c2SM * c2SM)));
    if (Math.abs(l2 - lam) < 1e-12){ lam = l2; break; } lam = l2;
  }
  const uSq = cSqA * (a * a - b * b) / (b * b), A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq))), Bq = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)));
  const dS = Bq * sS * (c2SM + Bq / 4 * (cS * (-1 + 2 * c2SM * c2SM) - Bq / 6 * c2SM * (-3 + 4 * sS * sS) * (-3 + 4 * c2SM * c2SM)));
  return b * A * (sig - dS);
}
