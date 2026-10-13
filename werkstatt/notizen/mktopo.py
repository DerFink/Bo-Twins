# Kleine Test-Topologie mit Transform und Delta-Kodierung: Deutschland (276), Polen (616), Russland (643) mit gemeinsamer Grenze bei 24° Ost
import json
sc=[0.01,0.01]; tr=[0,40]
q=lambda lon,lat:[round((lon-tr[0])/sc[0]),round((lat-tr[1])/sc[1])]
def arc(pts):
    out=[];px=py=0
    for lon,lat in pts:
        x,y=q(lon,lat); out.append([x-px,y-py]); px,py=x,y
    return out
arcs=[arc([(5,47),(15,47),(15,56),(5,56),(5,47)]),            # 0 Deutschland geschlossen
      arc([(24,49),(15,49),(15,56),(24,56)]),                  # 1 Polen West/Süd/Nord (offen)
      arc([(24,56),(24,49)]),                                  # 2 gemeinsame Grenze Polen–Russland, von Nord nach Süd
      arc([(24,56),(24,62),(45,62),(45,49),(24,49)])]          # 3 Russland Rest
topo={'type':'Topology','objects':{'countries':{'type':'GeometryCollection','geometries':[
  {'type':'Polygon','id':'276','properties':{'name':'Germany'},'arcs':[[0]]},
  {'type':'Polygon','id':'616','properties':{'name':'Poland'},'arcs':[[1,2]]},
  {'type':'MultiPolygon','id':'643','properties':{'name':'Russia'},'arcs':[[[3,-3]]]}]}},
  'arcs':arcs,'transform':{'scale':sc,'translate':tr}}
json.dump(topo,open('topomock.json','w'))
