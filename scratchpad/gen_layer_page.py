# -*- coding: utf-8 -*-
"""트랜스포머 한 층 — 어텐션과 FFN 을 한 장면으로 잇는다.

처음에는 규칙 — 애니메이션 §1(한 편이 한 계산이다)을 따라 둘을 따로 세웠다. 그런데
따로 보면 둘을 잇는 대목이 빠진다 — FFN 의 입력이 어텐션의 출력이라는 것, 그래서 한
층이 「섞고 나서 다듬는」 두 걸음이라는 것이 안 보인다. 그래서 규칙을 고쳤다(§1 은 이제
「한 편이 한 층이다」).

장면은 두 막이다. 1막에서 어텐션이 돌아 출력 하나가 맺히고, 그 상자가 그대로 위로
올라가 2막의 입력이 된다. 어텐션 쪽 칸들은 그때 물러난다 — 같은 화면에 다 두면 무엇을
보라는 건지 알 수 없다.

값은 두 JSON 에서만 가져온다 — data/attn_trace.json 과 data/ffn_trace.json 이고,
둘 다 같은 층·같은 자리에서 잰 것이다.
"""
import io, os, re, sys, json

ATTN = os.path.join('data', 'attn_trace.json')
FFN = os.path.join('data', 'ffn_trace.json')
OUT = os.path.join('대시보드', '애니메이션 — 한 층.html')

# ── 판 좌표 ─────────────────────────────────────────────────
# 1막과 2막이 같은 자리를 나눠 쓴다. 1막이 물러난 뒤에 2막이 들어오므로 줄이 겹쳐도
# 되지만, 문장 줄과 자막은 둘 다 쓰므로 그 둘만 고정이다.
W, H = 1000, 640
TOKY = 52            # 문장 줄 (두 막 공용)
CAPY = 596           # 자막 (두 막 공용)
# 1막 — 어텐션
QY = 150
KY = 252
BARBASE = 430
BARMAX = 108
VY = 462
# 2막 — FFN
INY = 168            # 어텐션 출력 상자가 올라와 서는 자리
WIDEY = 300
OUTY = 438
TCW, TCG = 74, 9     # 문장 칸
CW, CG = 74, 9       # 어텐션 칸
NCW, NCG = 26, 4     # FFN 입력·출력 칸
WCW, WCG = 12, 2     # FFN 넓힌 칸
NARROW = 16
CELLH, WCELLH = 30, 46

# ── 시계 (초) ───────────────────────────────────────────────
T_TOK = 2.2
T_Q = 4.2
T_SCAN = 6.0
SCAN_STEP = 0.8
T_SOFT = None        # build() 가 채운다
T_V = T_MIX = T_AOUT = None
T_HAND = T_WIDE = T_GATE = T_FOLD = T_FOUT = T_END = None

CAPS = [
    '「그것은」이 무엇을 가리키는지 찾는 중이다',
    '지금 이 자리가 무엇을 찾는가 — 그것이 Q 하나다',
    '앞선 토큰마다 K 가 이미 남아 있다',
    'Q 를 K 하나하나에 대 본다 — 닮은 만큼 점수가 선다',
    '점수를 합이 1 인 비율로 바꾼다',
    '그 비율을 가중치로 V 를 가중평균한다',
    '여기까지가 어텐션이다 — 앞선 토큰들을 섞어 하나로 모았다',
    '그 결과가 그대로 FFN 의 입력이 된다',
    '먼저 넓힌다 — 896 칸이 4,864 칸으로',
    '게이트가 대부분을 눌러 4,864 칸 중 97.7% 가 잠잠해진다',
    '살아남은 자리만 모아 다시 896 칸으로 접는다',
    '섞고 다듬었다 — 여기까지가 한 층이고, 이것이 층마다 되풀이된다',
]


def load():
    return (json.load(io.open(ATTN, encoding='utf-8')),
            json.load(io.open(FFN, encoding='utf-8')))


def _screen_numbers(html):
    body = re.sub('<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    body = re.sub('<script[^>]*>.*?</script>', ' ', body, flags=re.S)
    return set(re.findall(r'-?\d+\.\d+', re.sub(r'<[^>]+>', ' ', body)))


def _row_x(n, cw, gap):
    return [(W - (n * cw + (n - 1) * gap)) / 2.0 + i * (cw + gap) for i in range(n)]


def timings(m):
    global T_SOFT, T_V, T_MIX, T_AOUT, T_HAND, T_WIDE, T_GATE, T_FOLD, T_FOUT, T_END
    T_SOFT = T_SCAN + m * SCAN_STEP + 0.6
    T_V = T_SOFT + 2.4
    T_MIX = T_V + 2.2
    T_AOUT = T_MIX + 2.0          # 어텐션 출력이 맺힌다
    T_HAND = T_AOUT + 2.2         # 1막이 물러나고 출력이 위로 올라간다
    T_WIDE = T_HAND + 2.4
    T_GATE = T_WIDE + 3.0
    T_FOLD = T_GATE + 3.2
    T_FOUT = T_FOLD + 2.4
    T_END = T_FOUT + 3.4
    return {'tok': T_TOK, 'q': T_Q, 'scan': T_SCAN, 'step': SCAN_STEP, 'soft': T_SOFT,
            'v': T_V, 'mix': T_MIX, 'aout': T_AOUT, 'hand': T_HAND, 'wide': T_WIDE,
            'gate': T_GATE, 'fold': T_FOLD, 'fout': T_FOUT, 'end': T_END}


def svg_scene(at, ft, uid='layer', style=''):
    m = at['query_pos'] + 1
    toks = at['tokens']
    txs = _row_x(len(toks), TCW, TCG)
    axs = _row_x(m, CW, CG)[:]                     # 어텐션 칸은 앞 m 개만 쓴다
    nxs = _row_x(NARROW, NCW, NCG)
    wxs = _row_x(ft['show'], WCW, WCG)
    soft, raw = at['scores_softmax'], at['scores_raw']
    top = max(soft)
    lo, hi = min(raw), max(raw)
    span = (hi - lo) or 1.0

    p = ['<svg id="%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet"%s '
         'role="img" aria-label="트랜스포머 한 층이 어텐션에서 FFN 으로 이어지는 장면">'
         % (uid, W, H, (' style="%s"' % style) if style else '')]
    p.append(('<defs><linearGradient id="beam-%s" x1="0" y1="0" x2="0" y2="1">'
              '<stop offset="0" stop-color="var(--hot)" stop-opacity=".1"/>'
              '<stop offset="1" stop-color="var(--hot)" stop-opacity=".95"/>'
              '</linearGradient></defs>') % uid)

    # 문장 — 두 막 공용
    for i, t in enumerate(toks):
        cls = 'tok' + (' tokq' if i == at['query_pos'] else '')
        p.append('<g class="%s" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="36" rx="7"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                 % (cls, txs[i], TOKY, TCW, txs[i] + TCW / 2, TOKY + 24, t.strip() or '·'))

    # ── 1막 — 어텐션. act1 을 통째로 물러나게 하려고 한 겹에 담는다
    p.append('<g class="act1">')
    p.append('<line class="beam" x1="0" y1="0" x2="0" y2="0" stroke="url(#beam-%s)" '
             'stroke-width="3" stroke-linecap="round" opacity="0"/>' % uid)
    for j in range(m):
        p.append('<g class="kc" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="40" rx="7"/>'
                 '<text class="kk" x="%.1f" y="%d" text-anchor="middle">K</text>'
                 '<text class="kv" x="%.1f" y="%d" text-anchor="middle">%.2f</text></g>'
                 % (axs[j], KY, CW, axs[j] + CW / 2, KY + 17,
                    axs[j] + CW / 2, KY + 32, at['k_preview'][j][0]))
    for j in range(m):
        h_raw = int(8 + BARMAX * (raw[j] - lo) / span)
        h_soft = int(8 + BARMAX * soft[j] / top)
        hot = ' data-top="1"' if soft[j] == top else ''
        p.append('<rect class="bar" data-show="3"%s x="%.1f" y="%d" width="%d" height="0" '
                 'rx="4" data-raw="%d" data-soft="%d"/>'
                 % (hot, axs[j] + 11, BARBASE, CW - 22, h_raw, h_soft))
        p.append('<text class="bv" x="%.1f" y="%d" text-anchor="middle" opacity="0">%.2f</text>'
                 % (axs[j] + CW / 2, BARBASE + 21, soft[j]))
    for j in range(m):
        p.append('<g class="vc" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="34" rx="7"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">V</text></g>'
                 % (axs[j], VY, CW, axs[j] + CW / 2, VY + 23))
    for _j in range(m):
        p.append('<circle class="flow" r="4" opacity="0"/>')
    p.append('</g>')

    # 어텐션 출력 상자 — 1막의 끝이자 2막의 입력. 한 물건이 자리를 옮긴다
    p.append('<g class="hand" opacity="0" transform="translate(0,0)">'
             '<rect x="%.1f" y="%d" width="150" height="34" rx="8"/>'
             '<text x="%.1f" y="%d" text-anchor="middle">어텐션 출력 %.2f</text></g>'
             % (axs[m - 1] + CW + 30, VY, axs[m - 1] + CW + 105, VY + 23,
                at['out_preview'][0]))

    # ── 2막 — FFN
    p.append('<g class="act2">')
    p.append('<path class="funnel fan-in" opacity="0" d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z"/>'
             % (nxs[0], INY + CELLH, nxs[-1] + NCW, INY + CELLH,
                wxs[-1] + WCW, WIDEY, wxs[0], WIDEY))
    p.append('<path class="funnel fan-out" opacity="0" d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z"/>'
             % (wxs[0], WIDEY + WCELLH, wxs[-1] + WCW, WIDEY + WCELLH,
                nxs[-1] + NCW, OUTY, nxs[0], OUTY))
    for i in range(NARROW):
        p.append('<rect class="inc" x="%.1f" y="%d" width="%d" height="%d" rx="4" opacity="0"/>'
                 % (nxs[i], INY, NCW, CELLH))
    p.append('<text class="lbl lbl-in" x="%.1f" y="%d" opacity="0">입력 %d칸 중 %d칸</text>'
             % (nxs[0], INY + CELLH + 18, ft['d_model'], NARROW))
    mx = ft['act_max'] or 1.0
    for i, v in enumerate(ft['act_show']):
        p.append('<rect class="wc" data-a="%.4f" x="%.1f" y="%d" width="%d" height="%d" '
                 'rx="3" opacity="0"/>' % (abs(v) / mx, wxs[i], WIDEY, WCW, WCELLH))
    p.append('<text class="lbl lbl-wide" x="%.1f" y="%d" opacity="0">넓힌 %d칸 중 %d칸</text>'
             % (wxs[0], WIDEY - 12, ft['d_ff'], ft['show']))
    for i in range(NARROW):
        p.append('<rect class="outc" x="%.1f" y="%d" width="%d" height="%d" rx="4" opacity="0"/>'
                 % (nxs[i], OUTY, NCW, CELLH))
    p.append('<text class="lbl lbl-out" x="%.1f" y="%d" opacity="0">다시 %d칸</text>'
             % (nxs[0], OUTY + CELLH + 20, ft['d_model']))
    p.append('<text class="val val-out" x="%.1f" y="%d" text-anchor="end" opacity="0">%.2f</text>'
             % (nxs[-1] + NCW, OUTY + CELLH + 20, ft['out_preview'][0]))
    p.append('</g>')

    for txt in CAPS:
        p.append('<text class="cap" x="%d" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (W // 2, CAPY, txt))
    p.append('</svg>')
    return '\n'.join(p), axs, nxs


CSS = '''
:root{--ink-1:#1c1c1c;--ink-3:#8d8d8d;--bg-1:#fbfbfa;--bg-2:#efefee;--bg-3:#e0e0de;
  --hot:#1f7a5c;--hot-soft:#d9ede5}
@media (prefers-color-scheme:dark){:root{--ink-1:#ededec;--ink-3:#8f8f8f;
  --bg-1:#121212;--bg-2:#1e1e1e;--bg-3:#2c2c2c;--hot:#4fc39b;--hot-soft:#1b3a31}}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--bg-1);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:14px}
svg{width:100%;height:100%}
text{fill:var(--ink-1);font-size:15px}
.tok rect{fill:var(--bg-2);stroke:var(--bg-3)}
.tokq rect{fill:var(--hot-soft);stroke:var(--hot);stroke-width:2}
.kc rect{fill:var(--bg-2);stroke:var(--bg-3)}
.kc .kk{font-size:13px}
.kc .kv{font-size:11px;fill:var(--ink-3)}
.bar{fill:var(--bg-3)}
.bar.hot{fill:var(--hot)}
.bv{font-size:12px;fill:var(--ink-3)}
.vc rect{fill:var(--hot)}
.vc text{font-size:13px}
.hand rect{fill:var(--bg-2);stroke:var(--hot);stroke-width:2}
.hand text{font-size:13px}
.flow{fill:var(--hot)}
.inc,.outc{fill:var(--hot);stroke:none}
.wc{fill:var(--hot)}
.funnel{fill:var(--hot);fill-opacity:.07;stroke:var(--bg-3)}
.lbl,.val{font-size:12px;fill:var(--ink-3)}
.cap{font-size:17px;letter-spacing:-.01em}
#src{position:fixed;left:14px;bottom:10px;margin:0;font-size:11px;color:var(--ink-3)}
'''

EMBED_CSS = '''
#%(u)s{--hot:var(--accent,#1f7a5c);--hot-soft:var(--accent-soft,#d9ede5);
  --bg-2:var(--card,#f4f4f3);--bg-3:var(--line,#e0e0de);
  --ink-1:var(--ink,#1c1c1c);--ink-3:var(--ink-3,#8d8d8d)}
#%(u)s text{fill:var(--ink-1);font-size:15px}
#%(u)s .tok rect{fill:var(--bg-2);stroke:var(--bg-3)}
#%(u)s .tokq rect{fill:var(--hot-soft);stroke:var(--hot);stroke-width:2}
#%(u)s .kc rect{fill:var(--bg-2);stroke:var(--bg-3)}
#%(u)s .kc .kk{font-size:13px}
#%(u)s .kc .kv{font-size:11px;fill:var(--ink-3)}
#%(u)s .bar{fill:var(--bg-3)}
#%(u)s .bar.hot{fill:var(--hot)}
#%(u)s .bv{font-size:12px;fill:var(--ink-3)}
#%(u)s .vc rect{fill:var(--hot)}
#%(u)s .vc text{font-size:13px}
#%(u)s .hand rect{fill:var(--bg-2);stroke:var(--hot);stroke-width:2}
#%(u)s .hand text{font-size:13px}
#%(u)s .flow{fill:var(--hot)}
#%(u)s .inc,#%(u)s .outc{fill:var(--hot);stroke:none}
#%(u)s .wc{fill:var(--hot)}
#%(u)s .funnel{fill:var(--hot);fill-opacity:.07;stroke:var(--bg-3)}
#%(u)s .lbl,#%(u)s .val{font-size:12px;fill:var(--ink-3)}
#%(u)s .cap{font-size:17px;letter-spacing:-.01em}
'''

JS = r'''
(function(){
var D=__DATA__;
var st=document.getElementById(D.uid);
var q=function(s){return [].slice.call(st.querySelectorAll(s));};
var toks=q('.tok'),kcs=q('.kc'),bars=q('.bar'),bvs=q('.bv'),vcs=q('.vc'),flows=q('.flow');
var beam=q('.beam')[0],hand=q('.hand')[0],act1=q('.act1')[0];
var inc=q('.inc'),wc=q('.wc'),outc=q('.outc'),caps=q('.cap');
var fin=q('.fan-in')[0],fout=q('.fan-out')[0];
var lin=q('.lbl-in')[0],lw=q('.lbl-wide')[0],lo=q('.lbl-out')[0],vout=q('.val-out')[0];
var T=D.t,m=D.m,xs=D.xs,cw=D.cw;
var topw=Math.max.apply(null,D.bars.map(function(b){return b.w;}));
var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
function cl(v,a,b){return v<a?a:(v>b?b:v);}
function seg(t,a,b){return cl((t-a)/(b-a),0,1);}
function ease(u){return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;}
function set(e,k,v){if(e)e.setAttribute(k,v);}

var qbox=document.createElementNS('http://www.w3.org/2000/svg','g');
qbox.setAttribute('opacity','0');
qbox.innerHTML='<rect width="'+cw+'" height="40" rx="7" fill="var(--hot-soft)" '+
  'stroke="var(--hot)" stroke-width="2"/>'+
  '<text x="'+(cw/2)+'" y="17" text-anchor="middle" font-size="13">Q</text>'+
  '<text x="'+(cw/2)+'" y="32" text-anchor="middle" font-size="11" fill="var(--ink-3)">'+
  D.qv+'</text>';
act1.appendChild(qbox);

function capAt(t){
  if(t<T.tok)return 0; if(t<T.q-.6)return 1; if(t<T.scan)return 2;
  if(t<T.soft)return 3; if(t<T.v)return 4; if(t<T.mix)return 5;
  if(t<T.hand)return 6; if(t<T.wide)return 7; if(t<T.gate)return 8;
  if(t<T.fold)return 9; if(t<T.fout)return 10; return 11;
}

function frame(t){
  // 문장 — 두 막 내내 서 있다. 2막에서는 그 토큰만 남는다(FFN 은 옆을 안 본다)
  var per=T.tok/toks.length;
  var solo=ease(seg(t,T.hand,T.hand+1.0));
  for(var i=0;i<toks.length;i++){
    var u=ease(seg(t,i*per,i*per+.6));
    var o=(i===D.qi)?u:u*(1-solo*.82);
    set(toks[i],'opacity',o.toFixed(3));
  }
  // 1막 전체 — 넘겨준 뒤 물러난다
  set(act1,'opacity',(1-ease(seg(t,T.aout+.8,T.hand))).toFixed(3));

  var uq=ease(seg(t,T.tok,T.q));
  var qx=D.qx,qy=D.toky+(D.qy-D.toky)*uq;
  var scanning=t>=T.scan&&t<T.soft;
  if(scanning){
    var k=cl(Math.floor((t-T.scan)/T.step),0,m-1);
    var fr=cl((t-T.scan)/T.step-k,0,1);
    qx=xs[k]+(xs[cl(k+1,0,m-1)]-xs[k])*ease(fr);
    qy=D.qy;
    set(beam,'opacity',(1-Math.abs(fr-.5)*1.5).toFixed(2));
    set(beam,'x1',(qx+cw/2).toFixed(1));set(beam,'y1',D.qy+40);
    set(beam,'x2',(xs[k]+cw/2).toFixed(1));set(beam,'y2',D.ky);
  }else{
    set(beam,'opacity',0);
    if(t>=T.soft){qx=xs[m-1];qy=D.qy;}
  }
  set(qbox,'opacity',uq.toFixed(3));
  set(qbox,'transform','translate('+qx.toFixed(1)+','+qy.toFixed(1)+')');
  for(var j=0;j<kcs.length;j++)
    set(kcs[j],'opacity',ease(seg(t,T.q-1.0+j*.09,T.q-.3+j*.09)).toFixed(3));
  for(var j=0;j<m;j++){
    var b=D.bars[j],h=0;
    if(t>=T.scan&&t<T.soft)h=b.raw*ease(seg(t,T.scan+j*T.step,T.scan+j*T.step+.6));
    else if(t>=T.soft)h=b.raw+(b.soft-b.raw)*ease(seg(t,T.soft,T.soft+1.4));
    set(bars[j],'height',h.toFixed(1));set(bars[j],'y',(D.barbase-h).toFixed(1));
    if(t>=T.soft&&b.top)bars[j].classList.add('hot');else bars[j].classList.remove('hot');
    set(bvs[j],'opacity',ease(seg(t,T.soft+.6,T.soft+1.5)).toFixed(3));
    var uv=ease(seg(t,T.v+j*.08,T.v+j*.08+.7));
    set(vcs[j],'opacity',uv.toFixed(3));
    vcs[j].querySelector('rect').setAttribute(
      'fill-opacity',((.12+.88*D.bars[j].w/topw)*uv).toFixed(3));
    var uf=seg(t,T.mix-.8+j*.08,T.mix+1.2);
    set(flows[j],'opacity',(uf>0&&uf<1?(.3+.7*D.bars[j].w/topw):0).toFixed(3));
    set(flows[j],'cx',(xs[j]+cw/2+(D.hx-xs[j]-cw/2)*ease(uf)).toFixed(1));
    set(flows[j],'cy',(D.vy+17).toFixed(1));
  }
  // 넘겨주기 — 어텐션 출력 상자가 그대로 위로 올라가 FFN 입력 자리에 선다
  var uh=ease(seg(t,T.aout,T.aout+1.0));
  var mv=ease(seg(t,T.aout+1.0,T.hand));
  set(hand,'opacity',(uh*(1-ease(seg(t,T.wide-.6,T.wide)))).toFixed(3));
  set(hand,'transform','translate('+((D.inx-D.hx0)*mv).toFixed(1)+','
    +((D.iny-D.vy)*mv).toFixed(1)+')');
  // 2막
  for(var i=0;i<inc.length;i++)
    set(inc[i],'opacity',ease(seg(t,T.hand+.2+i*.03,T.hand+.8+i*.03)).toFixed(3));
  set(lin,'opacity',ease(seg(t,T.hand+.4,T.wide-.4)).toFixed(3));
  set(fin,'opacity',ease(seg(t,T.hand+.8,T.wide-.2)).toFixed(3));
  var born=ease(seg(t,T.wide-.6,T.wide+.8));
  var gate=ease(seg(t,T.gate,T.gate+1.8));
  for(var i=0;i<wc.length;i++){
    var a=+wc[i].getAttribute('data-a');
    var lvl=.55*(1-gate)+(0.04+0.96*a)*gate;
    set(wc[i],'opacity',(born*(.15+.85*lvl)).toFixed(3));
  }
  set(lw,'opacity',born.toFixed(3));
  set(fout,'opacity',ease(seg(t,T.fold,T.fold+1.0)).toFixed(3));
  for(var i=0;i<outc.length;i++)
    set(outc[i],'opacity',ease(seg(t,T.fout-.6+i*.04,T.fout+.3+i*.04)).toFixed(3));
  set(lo,'opacity',ease(seg(t,T.fout,T.fout+.8)).toFixed(3));
  set(vout,'opacity',ease(seg(t,T.fout,T.fout+.8)).toFixed(3));
  var ci=capAt(t);
  for(var c=0;c<caps.length;c++)set(caps[c],'opacity',c===ci?1:0);
}

if(still){frame(T.fout+1.2);return;}
var t0=null;
function loop(ts){
  if(t0===null)t0=ts;
  var t=(ts-t0)/1000;
  if(t>T.end){t0=ts;t=0;}
  frame(t);requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
'''


def scene_js(at, ft, uid, axs, nxs):
    m = at['query_pos'] + 1
    soft, raw = at['scores_softmax'], at['scores_raw']
    top = max(soft)
    lo, hi = min(raw), max(raw)
    span = (hi - lo) or 1.0
    hx0 = axs[m - 1] + CW + 30
    data = {
        'uid': uid, 'm': m, 'xs': axs, 'cw': CW, 'qi': at['query_pos'],
        'qx': axs[at['query_pos']] if at['query_pos'] < len(axs) else axs[-1],
        'toky': TOKY, 'qy': QY, 'ky': KY, 'barbase': BARBASE, 'vy': VY,
        'hx0': hx0, 'hx': hx0 + 75,
        # 넘긴 상자는 입력 칸 줄 위에 앉는다 — 칸 위에 얹으면 글자가 뭉갠다
        'inx': (W - 150) / 2.0, 'iny': INY - 58,
        'qv': '%.2f' % at['q_preview'][0],
        'bars': [{'raw': round(8 + BARMAX * (raw[j] - lo) / span, 1),
                  'soft': round(8 + BARMAX * soft[j] / top, 1),
                  'w': soft[j], 'top': soft[j] == top} for j in range(m)],
        't': timings(m),
    }
    return JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))


def embed(at, ft, uid='layer-scene', maxw=900):
    scene, axs, nxs = svg_scene(at, ft, uid, style='max-width:%dpx' % maxw)
    return ('<style>%s</style>\n%s\n<script>%s</script>'
            % (EMBED_CSS % {'u': uid}, scene, scene_js(at, ft, uid, axs, nxs)))


def render(at, ft):
    scene, axs, nxs = svg_scene(at, ft, 'layer')
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>애니메이션 — 트랜스포머 한 층</title><style>%s</style></head><body>
<div id="wrap">%s</div>
<p id="src">%s · %d층 %d번 헤드 — 「%s」 자리에서 잰 실제 값이다</p>
<script>%s</script></body></html>''' % (
        CSS, scene, at['model'], at['layer'], at['head'],
        at['tokens'][at['query_pos']].strip(), scene_js(at, ft, 'layer', axs, nxs))


def check_ui(html, at, ft):
    m = at['query_pos'] + 1
    known = set()
    vals = (at['scores_raw'] + at['scores_softmax'] + at['q_preview'] + at['out_preview']
            + [v for row in at['k_preview'] + at['v_preview'] for v in row]
            + ft['in_preview'] + ft['out_preview'] + ft['act_show']
            + [ft['act_max'], ft['quiet_share'] * 100])
    for v in vals:
        known.add('%.1f' % v)
        known.add('%.2f' % v)
        known.add('%.3f' % v)
    stray = _screen_numbers(html.replace(at['model'], '(model)')) - known
    assert not stray, '규약 위반: 구운 값에 없는 숫자가 화면에 있다 — %s' % sorted(stray)[:5]
    assert html.count('class="cap"') == len(CAPS), \
        '규약 위반: 자막이 %d개, 장면은 %d개다' % (html.count('class="cap"'), len(CAPS))
    assert 'function capAt' in html, '규약 위반: 어느 자막을 띄울지 정하는 자리가 없다'
    assert 'prefers-reduced-motion' in html, '규약 위반: 애니메이션을 줄이라는 설정을 안 본다'
    assert 'if(still){frame(' in html.replace(' ', ''), \
        '규약 위반: 줄이라고 한 사람에게 정지 화면을 안 준다'
    for banned, why in [('<button', '버튼'), ('class="stepdesc"', '설명 상자'),
                        ('class="dot"', '진행 점'), ('<h1', '머리말')]:
        assert banned not in html, '규약 위반: %s 을 두지 않는다 — 이 장은 한 장면이다' % why
    for cls, name, want in [('kc', 'K', m), ('bar', '막대', m), ('vc', 'V', m),
                            ('wc', '넓힌 칸', ft['show']),
                            ('inc', 'FFN 입력 칸', NARROW), ('outc', 'FFN 출력 칸', NARROW)]:
        got = html.count('class="%s"' % cls)
        assert got == want, '규약 위반: %s 이 %d개다 (기대 %d)' % (name, got, want)
    # 두 막을 잇는 물건이 하나 있어야 한다 — 이 장의 요점이다
    assert html.count('class="hand"') == 1, \
        '규약 위반: 어텐션 출력을 FFN 입력으로 넘기는 상자가 없다'
    assert '중 %d칸' % ft['show'] in html and '중 %d칸' % NARROW in html, \
        '규약 위반: 몇 칸 중 몇 칸을 보였는지 화면에 안 적혀 있다'


def selftest():
    at, ft = load()
    good = render(at, ft)
    check_ui(good, at, ft)
    cases = [
        ('없는 숫자 넣기', good.replace('</body>', '<p>9.87</p></body>', 1)),
        ('자막 하나 빼기', good.replace('class="cap"', 'class="x"', 1)),
        ('자막 고르는 자리 빼기', good.replace('function capAt', 'function xAt')),
        ('모션 설정 무시', good.replace('prefers-reduced-motion', 'xx')),
        ('정지 화면 빼기', good.replace('if(still){frame(', 'if(0){frame(')),
        ('버튼 두기', good.replace('</body>', '<button>다음</button></body>', 1)),
        ('K 칸 빼기', good.replace('class="kc"', 'class="x"', 1)),
        ('넓힌 칸 빼기', good.replace('class="wc"', 'class="x"', 1)),
        ('넘겨주는 상자 빼기', good.replace('class="hand"', 'class="x"', 1)),
        ('몇 칸 중 몇 칸인지 지우기', good.replace('중 %d칸' % ft['show'], '칸')),
    ]
    bites = 0
    for name, broken in cases:
        try:
            check_ui(broken, at, ft)
        except AssertionError:
            bites += 1
        else:
            print('FAIL 결함을 안 물었다 —', name)
    print('selftest: 규약 %d개 중 %d개가 결함을 물었다' % (len(cases), bites))
    assert bites == len(cases)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if '--selftest' in sys.argv:
        selftest()
    else:
        at, ft = load()
        html = render(at, ft)
        check_ui(html, at, ft)
        io.open(OUT, 'w', encoding='utf-8').write(html)
        print('%s — 한 바퀴 %.1f초 · 자막 %d개'
              % (OUT, timings(at['query_pos'] + 1)['end'], len(CAPS)))
