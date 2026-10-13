# Werkstatt Gasballon-Simulator

Arbeitswerkzeuge, mit denen die App gebaut und geprüft wird. Nicht Teil der App, nicht veröffentlichen.
Stand: Build 2026-10-12.2, Projektplan 0.49 (13.10.2026). Liegt öffentlich im Repository Bo-Twins; keine Zugangsdaten eintragen.

## Ordner
- `ph.py`: Patch-Helfer. `F()` lädt `index.html`, `rep(alt, neu)` ersetzt eine Stelle, die genau einmal vorkommen muss, `save()` schreibt die Datei und exportiert den Rechenkern (zwischen `/*CORE-START*/` und `/*CORE-END*/`) nach `core.js` für die Tests in Node. `tx_add` fügt Texte in alle 7 Sprachen ein. Pfad `P` oben in der Datei anpassen.
- `patches/`: Umbauskripte der Builds der Reihe nach (p14 bis p44c). Zum Nachlesen, was wann geändert wurde; nicht erneut ausführen.
- `plan/`: Skripte, die den Projektplan fortschreiben. `v19.py` enthält die Grundfunktionen (`rows_of`, `put`, `idx`), jedes `vNN.py` erzeugt aus Version NN−1 die Version NN. Danach `recalc.py` (LibreOffice) für die Formeln.
- `tests/`: Playwright-Abläufe in Python (`flowNN.py`; der Kopf von `flow17.py` stellt die Kartenattrappe `stub2.js` und die Wetter- und Geländeattrappen `wxmock.json`, `topomock.json` bereit) und Node-Tests des Rechenkerns (`tNN.js`, `aptest.js` für den Autopiloten).
- `route/`: Routensuche der Meisterschaft. `gb69-wetter.bin.gz` ist das Wetterpaket des 69. Gordon Bennett (Open-Meteo, CC BY 4.0; Raster 1° × 1,5°, 72 h, 13 Druckflächen). `gbroute.js` rechnet mit der Physik der App, `grun.js` startet Suchläufe (Modus `y`: angelehnt an die Siegerspur). In der App stecken `route_y1.json` (KI-optimiert, 1733 km) und `route_kons.json` (konservativ, 1059 km).
- `server/`: Quellen des Serverdienstes (`api.php`, `config.php` mit leeren Zugangsdaten) und die Anleitungen aus dem Serverpaket.
- `notizen/`: Sammelliste offener Findings, Entwurfsseiten (z. B. Füllgrad-Vorschläge), Erzeuger der Testdaten.

## Ablauf eines Builds
1. Findings sammeln, Entwürfe zeigen, Freigabe abwarten.
2. Patch-Skript schreiben und ausführen; `BUILD` in `index.html` und `VER` in `sw.js` erhöhen; Eintrag in `NEWS`.
3. Tests: Node-Tests des Kerns, betroffene Playwright-Abläufe, Bilder ansehen.
4. Serverpaket packen (`index.html`, `sw.js` in `gasballon/`), Projektplan fortschreiben.
5. Nutzer testet auf GitHub, dann auf dem Server.
