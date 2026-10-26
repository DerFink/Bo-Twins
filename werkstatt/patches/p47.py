import sys
sys.path.insert(0,'/home/claude/w')
from ph import F, tx_add
f=F()
# ---- Druckflächen ohne Höhe (Archiv ERA5, Gordon Bennett 2018): Höhe hydrostatisch vom Boden aus rechnen ----
f.rep("""      const lay = z => {""","""      let p0 = g('surface_pressure'); p0 = p0 != null ? p0 * 100 : null;
      let zP = elev, pP = p0, tP = g('temperature_2m') + 273.15;              // letzte Stützstelle für die Höhenformel, beginnend am Boden
      const lay = z => {""")
f.rep("""        const z = g('geopotential_height_' + L + 'hPa'), T = g('temperature_' + L + 'hPa'), sp = g('wind_speed_' + L + 'hPa'), d = g('wind_direction_' + L + 'hPa');""",
"""        let z = g('geopotential_height_' + L + 'hPa'); const T = g('temperature_' + L + 'hPa'), sp = g('wind_speed_' + L + 'hPa'), d = g('wind_direction_' + L + 'hPa'), pL = L * 100;
        if (z == null && T != null && pP != null && pL < pP) z = zP + R_GAS * (tP + T + 273.15) / 2 / (G0 * M_AIR) * Math.log(pP / pL);   // barometrische Höhenformel, mittlere Temperatur der Schicht
        if (z != null && T != null && pP != null && pL < pP){ zP = z; pP = pL; tP = T + 273.15; }""")
f.rep("""      let p0 = g('surface_pressure'); p0 = p0 != null ? p0 * 100 : null;
      if (p0 == null){""","""      if (p0 == null){""")
# ---- Grund des Fehlschlags merken und nennen ----
f.rep("async function loadWx(lat, lon, useCache, hist){","let WX_ERR = '';\nasync function loadWx(lat, lon, useCache, hist){")
f.rep("  }catch(e){\n    if (!useCache) return null;","  }catch(e){\n    WX_ERR = e && e.name === 'AbortError' ? 'timeout' : e && /^http/.test(e.message) ? e.message : e && e.message === 'parse' ? 'data' : 'net';\n    if (!useCache) return null;")
f.s=f.s.replace("if (!m){ showMenu(); toast(tr('gb_nowx')); return; }","if (!m){ showMenu(); toast(tr('gb_nowx') + ' (' + tr('wxerr_' + (/^http/.test(WX_ERR) ? 'http' : WX_ERR || 'net'), {c: WX_ERR.replace('http ', '')}) + ')'); return; }")
tx_add(f,{
 'wxerr_net':['keine Verbindung zum Wetterdienst','no connection to the weather service','pas de connexion au service météo','brak połączenia z serwisem pogody','žádné spojení s meteoslužbou','無法連線氣象服務','sin conexión con el servicio meteorológico'],
 'wxerr_timeout':['Wetterdienst antwortet zu langsam','weather service too slow','service météo trop lent','serwis pogody odpowiada zbyt wolno','meteoslužba odpovídá příliš pomalu','氣象服務回應太慢','el servicio meteorológico tarda demasiado'],
 'wxerr_http':['Wetterdienst lehnt ab, Code {c}','weather service refused, code {c}','service météo refuse, code {c}','serwis pogody odmawia, kod {c}','meteoslužba odmítá, kód {c}','氣象服務拒絕，代碼 {c}','el servicio meteorológico rechaza, código {c}'],
 'wxerr_data':['Antwort ohne brauchbare Höhenwerte','reply without usable upper-air data','réponse sans données d’altitude exploitables','odpowiedź bez użytecznych danych wysokościowych','odpověď bez použitelných výškových dat','回應缺少可用的高空資料','respuesta sin datos de altura utilizables']})
f.rep("const NEWS = [\n {b: '2026-10-26.1', de: [","const NEWS = [\n {b: '2026-10-26.2', de: ['Behoben: Der Gordon Bennett 2018 brach beim Laden des Wetters ab, weil das Archiv die Höhe der Luftschichten nicht mitliefert. Die App rechnet sie jetzt selbst aus Luftdruck und Temperatur. Scheitert das Wetter, nennt die Meldung den Grund.'],\n  en: ['Fixed: the Gordon Bennett 2018 stopped while loading the weather because the archive does not supply the height of the air layers. The app now computes it from pressure and temperature. If the weather fails, the message names the reason.']},\n {b: '2026-10-26.1', de: [")
f.rep("const BUILD = '2026-10-26.1'","const BUILD = '2026-10-26.2'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v48'" in s; open(p,'w').write(s.replace("'v48'","'v49'"))
print('ok')
