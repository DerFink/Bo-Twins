import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ---- Leere Hülle: Am Ventil strömt nichts mehr aus, also kein Zischen und keine Gaswolken ----
f.rep("    valve(v){ // Zischen folgt der Öffnung; ab 30 % kommt das Flattern des Stoffs im Gasstrom dazu","    valve(v){ // Zischen folgt der Öffnung; ab 30 % kommt das Flattern des Stoffs im Gasstrom dazu\n      if (v > 0 && gasEmpty()) v = 0;                                   // leere Hülle: Es strömt nichts mehr aus")
f.rep("function fillNow(){","function gasEmpty(){ try { return fillNow() < 0.005; } catch (e){ return false; } }   // Füllgrad zeigt 0 %\nfunction fillNow(){")
f.rep("  if (valve > 0 && on){ SIDE.pacc","  if (valve > 0 && on && !gasEmpty()){ SIDE.pacc")
f.rep("    const adv = simDt;\n","    const adv = simDt;\n    if (valve > 0 && gasEmpty()) SND.valve(valve);                                      // läuft die Hülle bei gezogener Leine leer, verstummt das Zischen\n")
f.rep("'Meisterschaft, Vorflug „KI-optimiert“: neue Route tief über die Ostsee bis nach Finnland.'],","'Meisterschaft, Vorflug „KI-optimiert“: neue Route tief über die Ostsee bis nach Finnland.', 'Ist die Hülle leer, zischt das Ventil nicht mehr.'],")
f.rep("new route low across the Baltic Sea to Finland.']},","new route low across the Baltic Sea to Finland.', 'With an empty envelope the valve no longer hisses.']},")
f.save()
