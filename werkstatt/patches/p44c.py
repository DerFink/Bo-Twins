import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("as soon as the balloon is 30 kg lighter than the air.',","as soon as the balloon is 30 kg lighter than the air. With the small handle at its edge you can shrink this control panel to see more of the map.',")
f.rep("The bar at the vario shows whether the balloon is accelerating.',","The bar at the vario shows whether the balloon is accelerating. With the small handle at the bottom you fold the instruments to three lengths; the shortest shows only height and vario.',")
f.rep("const NEWS = [\n","""const NEWS = [
 {b: '2026-10-12.2', de: ['Autopilot: Der Knopf „AP“ unter dem Tau hält die Höhe beim Einschalten auf ±5 m und gibt dafür selbst Sand oder Gas ab. Darunter wählst du, ob er die Höhe über NN oder über Grund hält. Er schaltet sich aus, sobald du selbst Sand gibst oder am Ventil ziehst, wenn der Sand die Landereserve erreicht oder wenn Gas abgelassen werden müsste, der Füllgrad aber unter 40 % liegt. Die Sollhöhe steht als violette Linie im Vertikalprofil.', 'Tutorial: Hinweise, dass sich Anzeigen und Bedienfeld über ihre Griffe einklappen lassen.'],
  en: ['Autopilot: the “AP” button below the trail rope holds the altitude at the moment you switch it on to ±5 m, releasing sand or gas by itself. Below it you choose altitude above sea level or above ground. It switches off as soon as you release sand or pull the valve yourself, when the sand reaches the landing reserve, or when gas would have to be released while the fill is below 40 %. The target altitude is a violet line in the vertical profile.', 'Tutorial: notes that the instruments and the control panel fold away with their handles.']},
""")
f.rep("const BUILD = '2026-10-12.1'","const BUILD = '2026-10-12.2'")
f.save()
p='/mnt/user-data/outputs/spiel/sw.js'; s=open(p).read(); assert "'v45'" in s; open(p,'w').write(s.replace("'v45'","'v46'"))
