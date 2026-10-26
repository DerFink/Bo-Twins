# Gasballon-Simulator: Stand und Arbeitsweise

Stand 13.10.2026 · Build **2026-10-26.4** (Service Worker `v51`) · Projektplan **0.52**

## Wo die App läuft
- Test: https://derfink.github.io/Bo-Twins/spiel/ (GitHub-Repository derfink/Bo-Twins, Ordner `spiel/`)
- Server: https://cloud.aerarium.de/gasballon/ (Synology-NAS). Der Serverdienst für Bestenliste, Statistik und Admin-Mails (`api/api.php`) braucht PHP 8 mit pdo_sqlite. Stand 10.10.: Der Server liefert dafür „500“, PHP ist dort noch nicht eingerichtet. Ohne PHP läuft die App vollständig, nur ohne gemeinsame Bestenliste.

## Arbeitsweise (vereinbart)
- Erst prüfen und fragen, erst nach Freigabe bauen. Ziel: weniger Rechenaufwand.
- Bei Darstellungen vorab Bilder oder Entwürfe zeigen.
- Findings sammeln und in einem Sammel-Patch umsetzen.
- Jeder Build: neue `BUILD`-Nummer in `index.html`, `VER` in `sw.js` erhöhen, Eintrag in „Was ist neu“ (de/en), kurzer Text für den Nutzer, Projektplan fortschreiben, Serverpaket `Gasballon_Server_Build_<build>.zip`.
- Updates: zuerst `index.html` und `sw.js` auf GitHub testen, dann dieselben Dateien auf den Server. `api/config.php` und `api/data/` auf dem Server nie überschreiben.
- Antworten auf Deutsch, Ergebnis zuerst, knapp, ehrlich über Ungetestetes.

## Aufbau der App
- Eine Datei `index.html` (HTML, CSS, JavaScript, rund 430 kB), Karte mit Leaflet 1.9.4 und OpenStreetMap, Service Worker `sw.js` für den Start ohne Netz, `manifest.json` und Symbole für die Installation als Web-App. 7 Sprachen (de, en, fr, pl, cs, zh-TW, es); lange Texte nur de/en.
- Rechenkern zwischen `/*CORE-START*/` und `/*CORE-END*/`: Atmosphäre, Ballonphysik (`stepBalloon`), Füllgrad und Widerstand (`dragArea`), Sonne, Nachtabkühlung, Regen, Schlepptau, Selbststeuerung (`autopilot` für Vergleichsfahrten, `holdAlt` für den Autopiloten des Spielers), Ziele und Wertung. Wird für Tests nach `core.js` exportiert.
- Wetter: Open-Meteo (CC BY 4.0) für den Ort des Ballons, 13 Druckflächen mit Temperatur, Wind, Bewölkung, Feuchte; Gelände über Open-Meteo-Höhenmodell; Lufträume optional über open flightmaps.
- Serverdienst `api/api.php` (PHP 8, SQLite) mit Selbsttest `?action=check`; Anleitung `INSTALLATION_Synology.txt` im Serverpaket.

## Spielarten
- **Freie Fahrt:** Startplatz (Karte, GPS, Bitterfeld) und Wetter (echt oder Simulation) wählbar.
- **Challenge:** Zielfahren (Landezone 100 m Durchmesser), Wandziel, Max- und Min-Distance.
- **Meisterschaft:** Szenarien zur Auswahl. 62. Gordon Bennett 2018 ab Bern (20 Teams, Wetter ERA5 aus dem Open-Meteo-Archiv, Start 19:00 MESZ Berner Allmend angenommen, keine gesperrten Länder, noch ohne Vorflug; Daten in `werkstatt/notizen/gb2018_daten.md`) und Nachfahrt des 69. Gordon Bennett (Start Gladbeck, 29.08.2026), „inoffizielles Fan-Projekt“. Gesperrte Länder mit rotem 10-km-Rand, offizielle Landepunkte, Vorflug „KI-optimiert“ (1733 km über die Ostsee nach Finnland) und „Konservativ“ (1059 km), eigene Bestenliste.
- Tutorial „Erste Fahrt“ (16 Schritte), Rückblick auf die Fahrt, Seitenansicht unter 50 m, Temp-Diagramm (Skew-T), Prallhöhen-Linie, Autopilot (±5 m, NN oder über Grund).

## Wichtige Entscheidungen
- Richtige Physik ist der Kern und bleibt. Ballon: 1000 m³ Wasserstoff, Hülle 135 kg, Sandsäcke je 15 kg, Sandmulde mit 200-g-Schaufel; Crew lässt erst bei mindestens 30 kg Auftriebsüberschuss los.
- Landung härter als 2,5 m/s = disqualifiziert (alle gewerteten Aufgaben und Meisterschaft).
- Füllgrad statt Gas in % in den Anzeigen; Hüllenform: bis 50 % Pilzform, darunter schmaler, unter 20 % flatternde Hülle (Wahl 11.10.).
- Autopilot: aus bei eigenem Eingriff, Sand unter 6 kg je 100 m³ Hülle oder Füllgrad unter 40 %; überall erlaubt, ausblendbar über `AP_HIDE`.
- Meisterschaft: offizielle Sperrflächen und Spuren zurückgestellt. Eigenes Team: Name, Land frei wählbar oder ohne Land (dann nur der Name); mit Land z. B. GER-4 (seit 26.10.2026, ersetzt JAM-1 CoolRidings).
- Ballonbild (seit 26.10.2026, Entwurf B2): silberne Hülle, oranges Rautennetz mit fünf Reihen, Ventil, Füllansatz, Lastring, Korb mit Sandsäcken; dieselbe Zeichnung (balGeo/balloonSVG/balDraw) für App-Symbol, Logo, Karte, Seitenansicht und Startseite. Werkzeuge in `werkstatt/ballonbild/`.
- „Was ist neu“: nach einem Update nur ein Satz, die Liste öffnet sich nicht von selbst; Schließen-Knopf immer sichtbar.
- App ist nicht kommerziell, nur für den privaten Gebrauch.

## Offen
- Build 2026-10-26.4 auf den Server: `index.html`, `sw.js`, die vier Symbole und `api/api.php` ersetzen.
- Gordon Bennett 2018 ist gesperrt („in Vorbereitung“): Das Open-Meteo-Archiv liefert für 2018 keine Werte in der Höhe (alle null). Plan: ERA5 auf Druckflächen über Copernicus (Konto des Nutzers, Download per Formular, GRIB), daraus Wetterpaket für App und Vorflug. Freischalten über `ready` in `GB_SC.gb62`.
- PHP auf dem Server einrichten, dann `…/gasballon/api/api.php?action=check` prüfen.
- Am Handy prüfen: Autopilot, Prallhöhe, Hüllenform, Melodie; restliche Basis-Tests im Blatt `Abnahme_Basis` (T-06, T-15 bis T-20, T-22 bis T-24, T-26 bis T-30, T-36, T-40, T-41).
- Rückmeldung erfahrener Gasballonpiloten zu Sonne, Nacht und Regen (OP-46).
- Sicherheit Serverdienst (vorgeschlagen, nicht freigegeben): Selbsttest nur mit Schlüssel, Admin-Schlüssel nicht in der Adresszeile, Namensanzeige prüfen.
- Vorschlag Text im Vorflug: „Aus rund 19.000 durchgerechneten Fahrtstunden ausgewählt, angelehnt an die Spur des Siegers“ (nicht freigegeben).
- Ideen: Szenario Alpen mit lokalen Windsystemen; Verfolgerfahrzeug auf der Karte.

## Wo was liegt
- App-Dateien und Serverpaket: beim Nutzer (zuletzt geliefert: Build 2026-10-12.2, Plan 0.49) und auf GitHub (`spiel/`).
- Werkzeuge (Patch-Helfer, Tests, Routensuche mit Wetterpaket, Plan-Skripte, Server-Quellen): auf GitHub im Ordner `werkstatt/` von Bo-Twins (öffentlich, ohne Zugangsdaten; seit 13.10.2026), Erklärung in `werkstatt/LIESMICH_WERKSTATT.md`. Claude hat Schreibzugriff auf das Repository.
- Auftrag für die Bo-Twins-App (Beschleunigung, Klappfenster, Füllgrad, Taupunkt): `BoTwins_Uebernahme_aus_Simulator.md`.
- Nächstes Vorhaben: Luftschiff-Simulator mit Baukasten und Auslegungsrechner, eigener Chat im Projekt; gemeinsamer Kern mit dem Gasballon geplant, noch nicht begonnen.
