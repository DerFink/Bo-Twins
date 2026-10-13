# Gesammelte Findings für den nächsten Sammel-Patch (Stand nach Build 2026-10-12.2)

1. Start: Die Bodencrew lässt los ab mindestens 30 kg Auftriebsüberschuss (fest, „zwei Säcke“). Soll vom Volumen abhängen: je angefangene 500 m³ ein Sack (400 m³: 1 Sack = 15 kg, 1000 m³: 2 Säcke = 30 kg, 1500 m³: 3 Säcke). Die zweite Bedingung (praller Ballon steigt bis 250 m über Grund, in Inversionen mehr) bleibt. Tutorialtext „30 kg“ muss den tatsächlichen Wert nennen.
   Gerechnet (werkstatt/tests/sack.js, simuliertes Wetter): 400 m³ mit 15 kg steigt auf 376 m, 1000 m³ mit 30 kg auf 312 m; 400 m³ braucht für 250 m nur 11 kg, 1000 m³ 27 kg. Mit festen 30 kg stiege der 400er auf 640 m.
