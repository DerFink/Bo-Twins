import sys
sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
f.rep("#rope b{font-family:var(--num);font-size:11px;font-weight:600;min-height:14px;white-space:nowrap}","#rope b{font-family:var(--num);font-size:11px;font-weight:600;min-height:14px;white-space:pre;text-align:center;line-height:1.15}")
f.rep("nf(B.ropeOn / CFG.ropeKgM) + ' m · −' + nf(B.ropeOn, 1) + ' kg'","nf(B.ropeOn / CFG.ropeKgM) + ' m\\n−' + nf(B.ropeOn, 1) + ' kg'")
f.rep("#c64{position:absolute;inset:0;","@media (max-height:500px){.mbar{display:none}}\n#c64{position:absolute;inset:0;")
f.save()
