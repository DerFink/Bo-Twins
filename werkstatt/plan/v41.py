import openpyxl, copy
exec(open('v19.py').read().split("# ---------------- Deckblatt")[0].replace("0.19.xlsx","0.41.xlsx").replace("0.18.xlsx","0.40.xlsx").replace("Version 0.19","Version 0.41").replace("Nutzer 08.10.2026","Nutzer 11.10.2026"))
BLD='2026-10-11.1'
ws=wb['Deckblatt']; ws['B4']='0.41'; ws['B6']=ws['B6'].value.replace('Build 2026-10-10.7',f'Build {BLD}')
ws=wb['Anforderungen']; rows=rows_of(ws,5,10)
def app(key,txt,src=None):
    r=rows[idx(rows,key)]; r[3]=(r[3] or '')+' '+txt; r[7]=(r[7] or '')+'; '+N+(': '+src if src else '')
app('NFA-07','Fehler behoben: Der Hinweis benutzte einen Klassennamen, der schon vergeben war; dadurch änderten sich beim Rollen Schrift und Abstand des Fensters und der Inhalt sprang. Der Pfeil ist jetzt ein kleines Zeichen ohne Farbverlauf und schaltet mit Abstand zwischen Ein und Aus.','Fund „Darstellung zappelt“')
def ins(pre,row):
    i=max(k for k,r in enumerate(rows) if str(r[0]).startswith(pre+'-'))+1; rows.insert(i,row)
ins('NFA',['NFA-08','Nichtfunktional','Fenster ein- und ausfahren','Vertikalprofil, Anzeigen und Bedienfeld (Sand, Ventil, Tau) haben am Rand einen kleinen Griff. Das Profil fährt zu einem schmalen Streifen ein, das Bedienfeld zu einer Zeile mit Sand und Füllgrad (im Querformat zu einem Streifen), die Anzeigen haben drei Längen: alles, kurz (Höhe, Vario, Fahrt, Ziel, Füllgrad) und kürzest (Höhe und Vario). Die Wahl bleibt gespeichert; im Tutorial ist alles ausgefahren.','Mit eingefahrenen Fenstern ist deutlich mehr Karte zu sehen; ein Tipp auf den Griff holt das Fenster zurück.','Soll','Umgesetzt',N+': Feedback „Bildschirm zu voll, Gelände kaum zu sehen“',None,'Basis'])
ins('STE',['STE-29','Steuerung und Physik','Ballonsymbol zeigt den Füllgrad','Das Ballonsymbol auf der Karte folgt dem Füllgrad in Schritten von 5 %: prall ist die Hülle rund, mit weniger Gas wird sie unten schmal. Die Seitenansicht zeigt die Form schon seit STE-28.','Bei 50 % Füllgrad ist die Hülle des Symbols unten sichtbar schmaler.','Kann','Umgesetzt',N,None,'Basis'])
ins('INS',['INS-06','Installation','Seite „Was ist neu“','In den Einstellungen zeigt „Was ist neu“ je Build kurze Texte für die Nutzer, der neueste zuerst, ab Build 2026-10-10.7. Nach einem Update öffnet sich die Seite einmal von selbst; bei der ersten Nutzung nicht. Deutsch und Englisch.','Nach einem Update erscheint die Seite einmal und nennt die Änderungen.','Soll','Umgesetzt',N+': Bei jedem Build schreibt Claude zusätzlich zum Plan einen kurzen Nutzertext',None,'Basis'])
def fixA(v,r): v[8]=f'=COUNTIF(Tests!$C$5:$C$300,"*"&A{r}&"*")'
put(ws,5,rows,10,4,fixA); ws['A2']=ws['A2'].value.replace('2026-10-10.7',BLD)
ws=wb['Tests']; rows=rows_of(ws,5,15)
r=rows[idx(rows,'T-40')]; r[2]=r[2]+', NFA-08, STE-29'; r[5]=r[5]+'; Profil, Anzeigen und Bedienfeld über die Griffe ein- und ausfahren, auch im Querformat; Gas ablassen und das Ballonsymbol beobachten'; r[6]=r[6]+'; eingefahren ist mehr Karte zu sehen; das Symbol wird mit weniger Gas unten schmal'
r[11]=(r[11] or '')+f' Build {BLD}: Kartenhöhe 497 px offen, 614 px mit eingefahrenem Bedienfeld (Bildschirm 360 × 700); Anzeigen 232 / 142 / 93 px; Querformat Kartenbreite 410 auf 718 px. Symbol bei 50 % geprüft.'
r=rows[idx(rows,'T-41')]; r[2]=r[2]+', INS-06'; r[11]=(r[11] or '')+f' Build {BLD}: Menü springt beim Rollen nicht mehr (Schrift und Abstand unverändert); „Was ist neu“ öffnet nach einem Update von selbst.'
put(ws,5,rows,15,4)
ws=wb['Änderungen']; r=ws.max_row+1
for c,v in enumerate(['0.41','11.10.2026',f'Build {BLD}: Fenster ein- und ausfahren (NFA-08). Springen der Fenster beim Rollen behoben (NFA-07). Ballonsymbol zeigt den Füllgrad (STE-29). Seite „Was ist neu“ (INS-06). Querformat: Seitenansicht und Knöpfe versetzt. Dienst mit Selbsttest (action=check).','Nutzer 11.10.2026'],1):
    ws.cell(r,c).value=v; ws.cell(r,c)._style=copy.copy(ws.cell(r-1,c)._style)
ws.row_dimensions[r].height=None; ws.auto_filter.ref=f'A3:D{r}'
wb.save(OUT); print('gespeichert',OUT)
