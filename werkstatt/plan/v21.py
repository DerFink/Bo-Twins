import openpyxl, copy
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill, Font
exec(open('v19.py').read().split("# ---------------- Deckblatt")[0].replace("0.19.xlsx","0.21.xlsx").replace("0.18.xlsx","0.20.xlsx").replace("Version 0.19","Version 0.21"))
BLD='2026-10-08.10'
ws=wb['Deckblatt']; ws['B4']='0.21'; ws['B5']='08.10.2026'
ws['B6']=ws['B6'].value.replace('Build 2026-10-08.9',f'Build {BLD}')
for c in (1,2): ws.cell(25,c)._style=copy.copy(ws.cell(20,c)._style)
ws['A25']='Testfälle am Rechner geprüft (Handy offen)'; ws['B25']='=COUNTIF(Tests!K5:K300,"Am Rechner geprüft")'
ws['A28']=(ws['A28'].value or '')+' Teststatus „Am Rechner geprüft“ heißt: Die Logik ist am Rechner mit Beispieldaten geprüft; der Test am Handy steht noch aus. „Bestanden“ trägt der Projektinhaber nach dem Test am Handy ein; danach kann die Anforderung von „Umgesetzt“ auf „Erledigt“ gehen.'

ws=wb['Anforderungen']; rows=rows_of(ws,5,9)
def a(key,**kw):
    m={'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}; r=rows[idx(rows,key)]
    for k,v in kw.items(): r[m[k]]=v
a('SPI-01',D='Der Start lässt sich auf drei Arten setzen: Wunschort durch Antippen der Karte, Standort des Handys (GPS) oder Standardplatz in Bitterfeld. Beim GPS-Start fragt die App die Standortfreigabe ab, wartet auf einen brauchbaren Fix (besser als 30 m) und mittelt die Position etwa 15 Sekunden. Solange gewartet und gemittelt wird, ist „Weiter“ gesperrt, damit die Fahrt nicht am vorherigen Startplatz beginnt und der Ballon später auf den GPS-Ort springt. Wer in dieser Zeit einen anderen Startplatz wählt oder die Vorbereitung verlässt, beendet die GPS-Suche. Ohne Freigabe oder Fix bleiben Karte und Standardplatz.',
  E='Alle drei Startarten setzen Karte und Ballon an den gewählten Ort; während der GPS-Suche lässt sich die Fahrt nicht beginnen; der Ballon springt in der Fahrt nie auf einen anderen Ort; ohne GPS gelingt der Start per Karte oder am Standardplatz.',H=N+': Fehler behoben (Ballon sprang nach dem Start auf den GPS-Ort)')
a('STE-17',D=rows[idx(rows,'STE-17')][3].replace('die Schichtung ist farbig gekennzeichnet, Inversionen sind hervorgehoben.','die Schichtung ist farbig gekennzeichnet: blau für Inversion, grün für sehr stabil, grau für gewöhnlich, rot für labil; Inversionen sind zusätzlich als blaues Band hervorgehoben.'),H=N+': Farben geändert (vorher rot, gelb, grau, blau)')
a('MET-06',D='Vor der Runde lässt sich wählen, ob mit den realen Wetterdaten des Startorts oder mit einer simulierten Atmosphäre gespielt wird. In der Simulation kommt der Wind nach jedem Start aus einer anderen Richtung und wechselt mit der Höhe häufig und in unregelmäßigen Abständen die Richtung: Vom Boden bis 3000 m dreht er um 150° bis 270°, darüber um weitere 30° bis 110°. Bodenwerte und Inversion sind ebenfalls zufällig.',
  E='Beide Arten lassen sich wählen; mehrere Starts in der Simulation zeigen unterschiedliche Windrichtungen; zwischen Boden und 3000 m dreht der Wind um mindestens 150° und höchstens 270°.',H=N+'; vorher 80° bis 200° bis 6000 m')
def fixA(v,r): v[8]=f'=COUNTIF(Tests!$C$5:$C$300,"*"&A{r}&"*")'
put(ws,5,rows,9,4,fixA)
ws['A2']=ws['A2'].value.replace('2026-10-08.9',BLD)

ws=wb['Parameter']; ds=[copy.copy(ws.cell(40,c)._style) for c in range(1,5)]; r0=ws.max_row+1
for k,v in enumerate([('Simulation: Drehung des Windes vom Boden bis 3000 m','150 bis 270','°','Vorgabe Nutzer 08.10.2026: bis 270° bei 3000 m; Untergrenze Vorschlag Claude (MET-06)'),('Simulation: weitere Drehung von 3000 bis 6000 m','30 bis 110','°','Vorschlag Claude; in der Aufgabe MID 130 bis 170, damit alle Richtungen vorkommen (AUF-08)')]):
    for c,x in enumerate(v,1): ws.cell(r0+k,c).value=x; ws.cell(r0+k,c)._style=copy.copy(ds[c-1])

# ---------------- Tests: Vorprüfung am Rechner eintragen
ws=wb['Tests']; rows=rows_of(ws,5,14)
r=rows[idx(rows,'T-01')]; r[5]='Start nacheinander per GPS, per Wunschort auf der Karte und am Standardplatz Bitterfeld setzen; nach dem Antippen von GPS sofort „Weiter“ versuchen; während der GPS-Suche einmal Bitterfeld wählen; einmal ohne Fix (Innenraum) wiederholen'
r[6]='Der Ballon steht jeweils am gewählten Ort (bei GPS innerhalb der Genauigkeit); während der GPS-Suche ist „Weiter“ gesperrt und der Ballon springt in der Fahrt nicht; ohne Fix gelingt der Start per Karte oder am Standardplatz'
r=rows[idx(rows,'T-24')]; r[6]='Beide Arten starten; die Anzeige nennt die aktive Art; in der Simulation kommt der Wind jedes Mal aus einer anderen Richtung und dreht bis 3000 m um 150° bis 270°'
r=rows[idx(rows,'T-08')]; r[6]=r[6].replace('und die Inversion,','und die Inversion (blau; sehr stabil grün, gewöhnlich grau, labil rot),')
D='08.10.2026'; P='Claude (Rechner)'; G='Am Rechner geprüft'; H=' Am Handy offen: '
res={
 'T-03':(G,'Ablauf Start, Fahrt, Landung, Auswertung, neue Fahrt im Browser fehlerfrei, in allen vier Aufgaben und der freien Fahrt.'+H+'Bedienung mit dem Finger.'),
 'T-05':(G,'Sack 15,0 kg und Schaufel 0,20 kg zählen richtig; Tau-Knopf und Ventil wirken.'+H+'Treffsicherheit der Knöpfe.'),
 'T-06':(G,'Testskript: 2 kg Sand heben den Ballon ab (0,2 m/s nach 20 s); mit 30 kg steigt er auf 312 m, die pralle Hülle bläst ab, danach sinkt er ohne weiteren Ballast und landet nach 12 min mit 0,47 m/s; Ventil voll offen: 95 % des Gases in 24 s.'+H+'Spielgefühl.'),
 'T-07':(G,'Testskript: 10 min Westwind 3 m/s ergeben 1800 m nach Osten, 10 min Nordwind 6 m/s in der oberen Schicht 3600 m nach Süden.'),
 'T-08':(G,'Alle Werte sichtbar und laufend aktualisiert; Gas mit einer Nachkommastelle; Profil mit den neuen Farben.'+H+'Lesbarkeit auf dem kleinen Bildschirm.'),
 'T-09':(G,'Ziele in 2,2 / 4,0 / 9,1 km (einfach / mittel / schwer), jeweils mit Kreis, Entfernung und Richtung; 45 berechnete Ziele liegen im Bereich der Stufe.'),
 'T-10':(G,'Testskript: Zielberechnung je Stufe in 3 bis 25 ms; Vergleichsfahrten 11 bis 52 min.'+H+'Zeitmessung (Grenzwert 3 s).'),
 'T-11':(G,'Mit nachgestelltem Kartendienst: Sportplatz wird Ziel; bei Ausfall erscheint sofort die Meldung und eine freie Landezone.'+H+'echter Dienst Overpass, Wartezeit, Flugmodus.'),
 'T-12':(G,'0 / 100 / 300 / 500 m Abstand bei 2,5 km Ziel: 100 / 100 / 50 / 0 Punkte; harte Landung in der Zone: 50; Kreis auf der Karte 100 m.'),
 'T-17':(G,'Alle Texte in sieben Sprachen vorhanden; Umschalten wirkt in Bestenliste und Auswertung.'+H+'Durchsicht der Texte (T-28).'),
 'T-22':(G,'Testskript: Auftrieb 1155 kg, Trimmballast 604,8 kg = 39 Säcke + 19,8 kg Mulde; Ballon steht 2 min im Gleichgewicht.'),
 'T-23':(G,'Testskript: Mulde wird aus einem Sack nachgefüllt, sobald weniger als ein Sack darin ist (15,0 auf 29,8 kg, 38 auf 37 Säcke).'+H+'Darstellung der Säcke.'),
 'T-24':(G,'Beide Arten starten (echtes Wetter nachgestellt); 400 Zufallswinde: Drehung bis 3000 m 151° bis 270°, Median 213°.'+H+'echter Wetterdienst.'),
 'T-27':(G,'Startbild im Rahmen in Hoch-, Quer- und Tablet-Format; Untermenü mit vier Aufgaben.'+H+'Rückfrage bei „Übernehmen und neu starten“ (in diesem Build nicht erneut geprüft).'),
 'T-29':(G,'Tau: Aufsetzen aus 2 m/s Sinken mit 1,83 statt 2,39 m/s; bei 4 m/s Wind und 40 m am Boden 0,4 m/s Fahrt; Abbremsen über rund 30 s.'+H+'Schleifgeräusch und Musik hören.'),
 'T-31':(G,'3 Target Cross, 3 Säckchen; Abwurf 9 m neben Kreuz 1 ergibt 94 Punkte für das Kreuz, 145 m neben Kreuz 2 ergibt 0; Gesamt 31.'),
 'T-32':(G,'Zeit läuft von 03:00:00 herunter und zeigt Überzeit rot; 90,2 von 112,8 km und 3 min zu spät ergeben 80 − 3 = 77 Punkte.'),
 'T-33':(G,'Alle 36 Windsektoren bis 6000 m; 350 m Abstand und 2 min Abweichung ergeben 97 Punkte.'),
 'T-34':(G,'Vier Rückmeldungen an den Grenzen 0,5 / 1,5 / 2,8 m/s richtig; Bestenliste mit Rang, Name, Punkte, Challenge für alle Aufgaben.'),
 'T-01':('Geplant','Am Rechner mit nachgestelltem Empfänger geprüft: „Weiter“ ist während der Suche gesperrt, der Ballon springt nicht. Der Test braucht ein echtes GPS.'),
 'T-14':('Geplant','Nur mit Beispieldaten geprüft; der echte Wetterdienst lässt sich am Rechner nicht erreichen.'),
 'T-13':('Blockiert','Das Chaserfahrzeug ist noch nicht gebaut (KRT-02 offen).'),
 'T-25':('Blockiert','Der zweite Ballon ist noch nicht gebaut (KI-01 offen).'),
 'T-35':('Blockiert','Es gibt noch keinen Server und keinen Online-Dienst (OP-34).'),
}
for k,(st,txt) in res.items():
    r=rows[idx(rows,k)]; r[10]=st; r[11]=f'Build {BLD}: '+txt
    if st==G: r[12]=D; r[13]=P
put(ws,5,rows,14,4)
ws['A2']='Jede Muss-Anforderung hat mindestens einen Testfall. „Am Rechner geprüft“: Claude hat die Logik am Rechner mit Beispieldaten geprüft, das Ergebnis steht in Spalte L; der Test am Handy steht noch aus. „Bestanden“, Messwerte, Datum und Prüfer trägt der Projektinhaber nach dem Test am Handy ein.'
dv=ws.data_validations.dataValidation[0]; dv.formula1='"Geplant,Am Rechner geprüft,Bestanden,Nicht bestanden,Blockiert"'
ws.conditional_formatting.add('K5:K85',CellIsRule(operator='equal',formula=['"Am Rechner geprüft"'],fill=PatternFill('solid',start_color='DDEBF7',end_color='DDEBF7'),font=Font(color='1F4E78')))
ws.column_dimensions['K'].width=max(ws.column_dimensions['K'].width or 0,19); ws.column_dimensions['L'].width=max(ws.column_dimensions['L'].width or 0,48)

ws=wb['Änderungen']; r=ws.max_row+1
for c,v in enumerate(['0.21','08.10.2026',f'Build {BLD}: Fehler behoben, bei dem der Ballon nach dem Start auf den GPS-Ort sprang; „Weiter“ wartet jetzt auf den Standort (SPI-01, T-01). Simulation mit mehr Richtungswechseln, 150° bis 270° Drehung bis 3000 m (MET-06, T-24). Farben im Vertikalprofil: blau Inversion, grün sehr stabil, grau gewöhnlich, rot labil (STE-17). Testplan: neuer Status „Am Rechner geprüft“ mit Ergebnis für 19 Testfälle, 3 Testfälle blockiert; neue Kennzahl auf dem Deckblatt.','Claude'],1):
    ws.cell(r,c).value=v; ws.cell(r,c)._style=copy.copy(ws.cell(r-1,c)._style)
ws.row_dimensions[r].height=None; ws.auto_filter.ref=f'A3:D{r}'
wb.save(OUT); print('gespeichert')
