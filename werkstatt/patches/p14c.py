import sys; sys.path.insert(0,'/home/claude/w')
from ph import F
f=F()
# ================= CSS: Hauptmenü im Stil der App =================
f.block("#menu{z-index:850;padding:0;background:#352879}",".note.lg{display:flex;","""#menu{z-index:850;padding:0;background:#0a1019}
#menubg{position:absolute;inset:0;width:100%;height:100%}
.mcard{position:relative;width:min(340px,calc(100% - 24px));max-height:calc(100% - 16px);overflow:auto;padding:14px;background:rgba(13,22,38,.94);border:1px solid var(--line);border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.45)}
.mcard h1{margin:0 0 6px;font-family:var(--num);font-size:28px;font-weight:700;letter-spacing:.02em}
/* Das Menü erscheint nach einer Sekunde und wird weich eingeblendet */
.mcard.boot{animation:menuin .6s ease-out 1s both}
@keyframes menuin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.mname{display:flex;align-items:center;gap:8px;margin-top:2px;font-size:12.5px;color:var(--mut)}
.mname input{flex:1;min-width:0;min-height:40px;padding:0 10px;border-radius:10px;border:1px solid var(--line);background:var(--pan);font-size:16px;color:var(--tx)}
""")
f.block(".mbtn{display:block;","#result .big b{","""#scores,#chal{z-index:860}
.mbtn{display:block;width:100%;text-align:left;margin-top:8px;padding:8px 12px;border-radius:12px;border:1px solid var(--line);background:var(--pan2)}
.mbtn b{display:block;font-size:16px;font-weight:600}
.mbtn span{display:block;font-size:12.5px;color:var(--mut);line-height:1.3;margin-top:1px}
.mbtn em{float:right;font-style:normal;font-size:11px;color:var(--mut);border:1px solid var(--line);border-radius:8px;padding:1px 7px;margin-left:8px}
.mbtn:disabled{opacity:.55;cursor:default}
.mbtn:not(:disabled):active{background:#22355a}
/* Ecke unten rechts auf der Karte: Zeit für MDT und MID, Abwurfknopf für die Säckchen (Wandziel) */
#corner{right:8px;bottom:26px;display:flex;flex-direction:column;align-items:flex-end;gap:6px}
#timer{padding:5px 10px 6px;text-align:right}
#timer span{display:block;font-size:11px;color:var(--mut);line-height:1.1}
#timer b{font-family:var(--num);font-size:24px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.05}
#mk-drop{display:flex;align-items:center;gap:6px;min-height:52px;padding:0 12px 0 10px;border-radius:14px;border:2px solid #ff7ad9;background:#3a1633;touch-action:manipulation}
#mk-drop b{font-family:var(--num);font-size:24px;font-weight:700}
#mk-drop:active{background:#5a2350}
#mk-drop:disabled{opacity:.45}
""")
f.rep("#scores{z-index:860}\n","")
f.rep("#scores .card{width:min(420px,100%)}","#scores .card{width:min(420px,100%);display:flex;flex-direction:column}\n#sc-list{flex:1;min-height:0;max-height:min(62vh,560px);overflow:auto;-webkit-overflow-scrolling:touch}\ntable.sc th{position:sticky;top:0;background:#0d1626}")
f.line("#follow{right:8px;bottom:26px;","#follow{left:8px;bottom:26px;min-height:40px;padding:0 13px;border-radius:12px;border:1px solid var(--orb);background:var(--orb);color:#1a1000;font-weight:600;font-size:14px}")
f.rep(".flash{animation-duration:.01s}.mcard.boot{animation:none}}",".flash{animation-duration:.01s}.mcard.boot{animation:none}}")
# ================= HTML =================
f.rep('<canvas id="c64" aria-hidden="true"></canvas>','<canvas id="menubg" aria-hidden="true"></canvas>')
f.rep("    <!-- Hauptmenü mit bewegtem Hintergrund im Stil der Heimcomputer der 80er -->","    <!-- Hauptmenü im Stil der App, dahinter ein ruhig bewegtes Bild: ein Ballon, der Sand abwirft, steigt und wieder sinkt -->")
f.rep('<div class="kv tgt" hidden><span data-i="tgt">Ziel</span><b id="i-tdist">–</b></div>','<div class="kv tgt" hidden><span id="i-tlbl"></span><b id="i-tdist">–</b></div>')
f.rep('      <button class="ov" id="follow" hidden data-i="follow">Ballon folgen</button>\n','''      <button class="ov" id="follow" hidden data-i="follow">Ballon folgen</button>
      <div class="ov" id="corner">
        <div class="card" id="timer" hidden><span data-i="tm_left"></span><b id="tm-val">00:00:00</b></div>
        <button id="mk-drop" hidden data-ia="mk_a" aria-label="Säckchen abwerfen"><svg width="22" height="28" viewBox="0 0 22 28" aria-hidden="true"><path d="M7 3h8l-1.5 5c4.5 2.5 6.5 7 6.5 11 0 4.5-3.5 7-9 7s-9-2.500-9-7c0-4 2-8.500 6.500-11z" fill="#ff7ad9" stroke="#0a1019" stroke-width="1.500"/><path d="M6.500 8h9" stroke="#0a1019" stroke-width="2"/></svg><b id="mk-n">0</b></button>
      </div>
''')
f.block('        <h2 data-i="landed">Gelandet</h2>','        <div class="kv"><span data-i="r_sink">','''        <h2 id="r-head"></h2>
        <div class="kv big" id="r-ptsrow" hidden><span data-i="r_pts"></span><b id="r-pts">–</b></div>
        <div id="r-extra"></div>
        <div class="kv" id="r-rankrow" hidden><span data-i="r_rank"></span><b id="r-rank">–</b></div>
''')
f.rep('        <p class="note tgtres" hidden data-i="r_best"></p>','        <p class="note" id="r-note" hidden></p>')
f.block('        <div id="su-task" hidden>','        <button class="pri" id="su-go" data-i="next"></button>','''        <div id="su-task" hidden>
          <div class="task"><span id="su-tdesc"></span></div>
          <div id="su-levelbox">
            <h4 data-i="su_level"></h4>
            <div class="seg wide" id="seg-level"><button data-v="0" data-i="lv_easy"></button><button data-v="1" data-i="lv_mid"></button><button data-v="2" data-i="lv_hard"></button></div>
          </div>
        </div>
        <h4 data-i="su_start"></h4>
        <div id="su-startsel">
          <div class="lbl" id="st-info"></div>
          <div class="btns" style="margin-top:8px">
            <button class="sm" id="st-map" data-i="st_map"></button>
            <button class="sm" id="st-gps" data-i="st_gps"></button>
            <button class="sm" id="st-def" data-i="st_bitt"></button>
          </div>
        </div>
        <div class="lbl" id="su-startfix" hidden data-i="su_fix"></div>
        <h4 data-i="su_wx"></h4>
        <div class="seg wide" id="seg-wx"><button data-v="real" data-i="wx_real"></button><button data-v="sim" data-i="wx_sim"></button></div>
        <div class="lbl" id="su-wxmid" hidden data-i="su_wx_mid"></div>
''')
f.rep('''    <!-- Startfenster: kurze Zusammenfassung vor jeder Fahrt -->''','''    <!-- Challenge: Auswahl der Aufgabe -->
    <div class="full" id="chal" hidden>
      <div class="card">
        <h2 data-i="m_chal"></h2>
        <button class="mbtn" data-task="target"><b data-i="task_target"></b><span data-i="task_target_d"></span></button>
        <button class="mbtn" data-task="wz"><b data-i="task_wz"></b><span data-i="task_wz_d"></span></button>
        <button class="mbtn" data-task="mdt"><b data-i="task_mdt"></b><span data-i="task_mdt_d"></span></button>
        <button class="mbtn" data-task="mid"><b data-i="task_mid"></b><span data-i="task_mid_d"></span></button>
        <button class="sec" id="ch-back" data-i="back"></button>
      </div>
    </div>

    <!-- Startfenster: kurze Zusammenfassung vor jeder Fahrt -->''')
f.rep('<dt data-i="sw_target"></dt><dd id="sw-target"></dd>','<dt id="sw-tlbl"></dt><dd id="sw-target"></dd>')
f.rep('.task span{display:block;font-size:12.5px;color:var(--mut);line-height:1.35;margin-top:2px}','.task span{display:block;font-size:13px;color:var(--tx);line-height:1.4}')
f.save(); print('ok')
