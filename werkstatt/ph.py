# Hilfen für die Umbauskripte: Datei laden, Textstellen eindeutig ersetzen, speichern
P='/mnt/user-data/outputs/spiel/index.html'
class F:
    def __init__(self): self.s=open(P,encoding='utf-8').read()
    def rep(self,a,b,cnt=1):
        assert self.s.count(a)==cnt,(a[:100],self.s.count(a)); self.s=self.s.replace(a,b)
    def block(self,start,end,new):
        assert self.s.count(start)==1,(start[:80],self.s.count(start)); a=self.s.index(start); b=self.s.index(end,a+len(start)); self.s=self.s[:a]+new+self.s[b:]
    def line(self,prefix,new):
        L=self.s.split('\n'); idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
        assert len(idx)==1,(prefix,len(idx)); L[idx[0]]=new; self.s='\n'.join(L)
    def save(self):
        open(P,'w',encoding='utf-8').write(self.s)
        s=self.s; core=s[s.index('/*CORE-START*/'):s.index('/*CORE-END*/')]
        names='dragArea,dropKg,M_AIR,M_H2,G0,holdNeed,autopilot,holdAlt,sunSin,simT0,cloudInfo,radEnv,DEFAULT_CFG,SIM_WX,buildAtm,atmAt,loadout,newBalloon,sandKg,refill,dropSack,dropScoop,stepBalloon,R_GAS,wxUrl,wxParse,buildAtmFromHour,wxTabAt,lerpTab,planFlight,makeTarget,scoreLanding,scoreRadius,osmQuery,osmClass,pickPlace,mDist,OSM,randomWx,makeCrosses,markerFall,scoreMarker,scoreCrosses,bestDistance,scoreMdt,scoreMid,landClass,WZ_R,windDirTo,TARGET_KM'
        open('/home/claude/w/core.js','w').write(core+'\nmodule.exports={'+names+'};\n')
        open('/home/claude/w/all.js','w').write(s[s.index('<script>\n/* ====')+9:s.rindex('</script>')])

import re as _re
LANGS=['de','en','fr','pl','cs','zh','es']
def _txpos(s):
    pos=[m.start() for m in _re.finditer(r"gb_story:'",s)]; assert len(pos)==7,len(pos); return pos
def tx_add(f,d):
    """d: {key:[7 Texte]} – neue Schlüssel in alle Sprachen"""
    pos=_txpos(f.s)
    for i in range(6,-1,-1):
        add=''.join("%s:'%s', "%(k,v[i].replace("\\","\\\\").replace("'","\\'")) for k,v in d.items()); f.s=f.s[:pos[i]]+add+f.s[pos[i]:]
def tx_get(f,key):
    ms=list(_re.finditer(r"(?<![a-z_0-9])"+key+r":'((?:[^'\\]|\\.)*)'",f.s)); return ms
def tx_set(f,key,vals):
    ms=tx_get(f,key); assert len(ms)==7,(key,len(ms))
    for m,v in sorted(zip(ms,vals),key=lambda x:-x[0].start()):
        f.s=f.s[:m.start(1)]+v.replace("\\","\\\\").replace("'","\\'")+f.s[m.end(1):]
