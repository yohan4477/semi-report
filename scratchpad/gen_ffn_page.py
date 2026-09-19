# -*- coding: utf-8 -*-
"""FFN 애니메이션. 어텐션 편(gen_anim_page.py)과 같은 꼴이고 계산만 다르다.

규칙 — 애니메이션 §1 「한 편이 한 계산이다」를 따라 어텐션 장면에 잇지 않고 따로 세운다.
어텐션은 토큰끼리 섞이는 계산이고 FFN 은 토큰마다 따로 도는 계산이라, 한 장면에 이으면
「옆을 보느냐 안 보느냐」라는 둘의 결정적 차이가 뭉개진다.

이 편이 보이려는 것은 둘이다. ① 넓혔다 접는다(896 → 4,864 → 896) ② 넓힌 자리 대부분은
잠잠하고 일부만 산다(97.7% 가 잠잠). 값은 data/ffn_trace.json 에서만 가져온다.
"""
import io, os, re, sys, json

TRACE = os.path.join('data', 'ffn_trace.json')
OUT = os.path.join('대시보드', '애니메이션 — FFN.html')

# ── 판 좌표 ─────────────────────────────────────────────────
# 줄 사이는 가장 두꺼운 것을 기준으로 잡는다. 넓힌 줄의 칸 높이가 가장 크다.
W, H = 1000, 620
TOKY = 56            # 문장 줄
INY = 186            # 입력 칸 줄
WIDEY = 312          # 넓힌 칸 줄
OUTY = 440           # 출력 칸 줄
CAPY = 566           # 자막
TCW, TCG = 74, 9     # 문장 칸 폭 · 사이
NCW, NCG = 26, 4     # 입력·출력 칸
WCW, WCG = 12, 2     # 넓힌 칸
NARROW = 16          # 입력·출력에 보일 칸 수
CELLH, WCELLH = 30, 46

# ── 시계 (초) ───────────────────────────────────────────────
T_TOK = 2.2          # 문장이 뜨고 그 자리만 남는다
T_IN = 4.6           # 어텐션 출력이 입력으로 내려온다
T_WIDE = 7.0         # 넓힌다
T_GATE = 10.4        # 게이트가 누른다
T_FOLD = 14.0        # 접는다
T_OUT = 17.0         # 출력이 맺힌다
T_END = 21.5

CAPS = [
    'FFN 은 토큰마다 따로 돈다 — 어텐션과 달리 옆 토큰을 안 본다',
    '어텐션이 낸 결과가 이 층의 입력이다',
    '먼저 넓힌다 — 896 칸이 4,864 칸으로',
    '게이트가 대부분을 눌러 4,864 칸 중 97.7% 가 잠잠해진다',
    '살아남은 자리만 모아 다시 896 칸으로 접는다',
    '접혀 나온 하나 — 이 토큰의 FFN 출력이다',
]


def load_trace(path=TRACE):
    return json.load(io.open(path, encoding='utf-8'))


def _screen_numbers(html):
    body = re.sub('<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    body = re.sub('<script[^>]*>.*?</script>', ' ', body, flags=re.S)
    return set(re.findall(r'-?\d+\.\d+', re.sub(r'<[^>]+>', ' ', body)))


def _row_x(n, cw, gap):
    return [(W - (n * cw + (n - 1) * gap)) / 2.0 + i * (cw + gap) for i in range(n)]


def svg_scene(tr, uid='ffn', style=''):
    toks = tr['tokens']
    txs = _row_x(len(toks), TCW, TCG)
    nxs = _row_x(NARROW, NCW, NCG)
    wxs = _row_x(tr['show'], WCW, WCG)
    p = ['<svg id="%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet"%s '
         'role="img" aria-label="FFN 이 한 토큰을 넓혔다 접는 장면">'
         % (uid, W, H, (' style="%s"' % style) if style else '')]

    # 문장 — 그 토큰만 남는다
    for i, t in enumerate(toks):
        cls = 'tok' + (' tokq' if i == tr['query_pos'] else '')
        p.append('<g class="%s" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="36" rx="7"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                 % (cls, txs[i], TOKY, TCW, txs[i] + TCW / 2, TOKY + 24, t.strip() or '·'))

    # 펼치는 깔때기 — 선을 몇 개 그으면 그 개수가 곧 주장이 된다. 면으로 둔다
    p.append('<path class="funnel fan-in" opacity="0" d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z"/>'
             % (nxs[0], INY + CELLH, nxs[-1] + NCW, INY + CELLH,
                wxs[-1] + WCW, WIDEY, wxs[0], WIDEY))
    p.append('<path class="funnel fan-out" opacity="0" d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d Z"/>'
             % (wxs[0], WIDEY + WCELLH, wxs[-1] + WCW, WIDEY + WCELLH,
                nxs[-1] + NCW, OUTY, nxs[0], OUTY))

    # 입력 칸
    for i in range(NARROW):
        p.append('<rect class="inc" x="%.1f" y="%d" width="%d" height="%d" rx="4" opacity="0"/>'
                 % (nxs[i], INY, NCW, CELLH))
    p.append('<text class="lbl lbl-in" x="%.1f" y="%d" opacity="0">입력 %d칸 중 %d칸</text>'
             % (nxs[0], INY - 10, tr['d_model'], NARROW))
    p.append('<text class="val val-in" x="%.1f" y="%d" text-anchor="end" opacity="0">%.2f</text>'
             % (nxs[-1] + NCW, INY - 10, tr['in_preview'][0]))

    # 넓힌 칸 — 밝기가 곧 그 자리에 남은 신호 크기다
    mx = tr['act_max'] or 1.0
    for i, v in enumerate(tr['act_show']):
        p.append('<rect class="wc" data-a="%.4f" x="%.1f" y="%d" width="%d" height="%d" '
                 'rx="3" opacity="0"/>' % (abs(v) / mx, wxs[i], WIDEY, WCW, WCELLH))
    p.append('<text class="lbl lbl-wide" x="%.1f" y="%d" opacity="0">넓힌 %d칸 중 %d칸</text>'
             % (wxs[0], WIDEY - 12, tr['d_ff'], tr['show']))

    # 출력 칸
    for i in range(NARROW):
        p.append('<rect class="outc" x="%.1f" y="%d" width="%d" height="%d" rx="4" opacity="0"/>'
                 % (nxs[i], OUTY, NCW, CELLH))
    p.append('<text class="lbl lbl-out" x="%.1f" y="%d" opacity="0">다시 %d칸</text>'
             % (nxs[0], OUTY + CELLH + 20, tr['d_model']))
    p.append('<text class="val val-out" x="%.1f" y="%d" text-anchor="end" opacity="0">%.2f</text>'
             % (nxs[-1] + NCW, OUTY + CELLH + 20, tr['out_preview'][0]))

    for txt in CAPS:
        p.append('<text class="cap" x="%d" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (W // 2, CAPY, txt))
    p.append('</svg>')
    return '\n'.join(p)


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
.inc,.outc{fill:var(--hot);stroke:none}
.wc{fill:var(--hot)}
.funnel{fill:var(--hot);fill-opacity:.07;stroke:var(--bg-3)}
.lbl{font-size:12px;fill:var(--ink-3)}
.val{font-size:12px;fill:var(--ink-3)}
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
var toks=q('.tok'),inc=q('.inc'),wc=q('.wc'),outc=q('.outc'),caps=q('.cap');
var fin=q('.fan-in')[0],fout=q('.fan-out')[0];
var lin=q('.lbl-in')[0],lw=q('.lbl-wide')[0],lo=q('.lbl-out')[0];
var vin=q('.val-in')[0],vout=q('.val-out')[0];
var T=D.t;
var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
function cl(v,a,b){return v<a?a:(v>b?b:v);}
function seg(t,a,b){return cl((t-a)/(b-a),0,1);}
function ease(u){return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;}
function set(e,k,v){if(e)e.setAttribute(k,v);}

function capAt(t){
  if(t<T.in)return 0; if(t<T.wide)return 1; if(t<T.gate)return 2;
  if(t<T.fold)return 3; if(t<T.out)return 4; return 5;
}

function frame(t){
  // 문장 — 다 떴다가 그 토큰만 남는다. FFN 이 옆을 안 본다는 말을 그림이 먼저 한다
  var per=T.tok/toks.length;
  for(var i=0;i<toks.length;i++){
    var u=ease(seg(t,i*per,i*per+.5));
    var dim=ease(seg(t,T.tok,T.tok+.9));
    var o=(i===D.qi)?u:u*(1-dim*.82);
    set(toks[i],'opacity',o.toFixed(3));
  }
  // 입력 칸
  for(var i=0;i<inc.length;i++)
    set(inc[i],'opacity',ease(seg(t,T.tok+.3+i*.03,T.tok+.9+i*.03)).toFixed(3));
  set(lin,'opacity',ease(seg(t,T.tok+.6,T.in)).toFixed(3));
  set(vin,'opacity',ease(seg(t,T.tok+.6,T.in)).toFixed(3));
  // 펼치는 면
  set(fin,'opacity',ease(seg(t,T.in,T.wide-.4)).toFixed(3));
  // 넓힌 칸 — 처음엔 다 고르게 뜨고, 게이트가 오면 값대로 갈린다
  var born=ease(seg(t,T.wide-.6,T.wide+.8));
  var gate=ease(seg(t,T.gate,T.gate+1.6));
  for(var i=0;i<wc.length;i++){
    var a=+wc[i].getAttribute('data-a');
    var lvl=.55*(1-gate)+ (0.04+0.96*a)*gate;      // 고르게 → 값대로
    set(wc[i],'opacity',(born*(.15+.85*lvl)).toFixed(3));
  }
  set(lw,'opacity',born.toFixed(3));
  // 접는 면과 출력
  set(fout,'opacity',ease(seg(t,T.fold,T.fold+1.0)).toFixed(3));
  for(var i=0;i<outc.length;i++)
    set(outc[i],'opacity',ease(seg(t,T.out-.6+i*.04,T.out+.3+i*.04)).toFixed(3));
  set(lo,'opacity',ease(seg(t,T.out,T.out+.8)).toFixed(3));
  set(vout,'opacity',ease(seg(t,T.out,T.out+.8)).toFixed(3));
  var ci=capAt(t);
  for(var c=0;c<caps.length;c++)set(caps[c],'opacity',c===ci?1:0);
}

if(still){frame(T.out+1.2);return;}
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


def scene_js(tr, uid):
    data = {'uid': uid, 'qi': tr['query_pos'],
            't': {'tok': T_TOK, 'in': T_IN, 'wide': T_WIDE, 'gate': T_GATE,
                  'fold': T_FOLD, 'out': T_OUT, 'end': T_END}}
    return JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))


def embed(tr, uid='ffn-scene', maxw=900):
    return ('<style>%s</style>\n%s\n<script>%s</script>'
            % (EMBED_CSS % {'u': uid},
               svg_scene(tr, uid, style='max-width:%dpx' % maxw), scene_js(tr, uid)))


def render(tr):
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>애니메이션 — FFN</title><style>%s</style></head><body>
<div id="wrap">%s</div>
<p id="src">%s · %d층 — 「%s」 자리에서 잰 실제 값이다</p>
<script>%s</script></body></html>''' % (
        CSS, svg_scene(tr, 'ffn'), tr['model'], tr['layer'],
        tr['tokens'][tr['query_pos']].strip(), scene_js(tr, 'ffn'))


def check_ui(html, tr):
    known = set()
    vals = (tr['in_preview'] + tr['out_preview'] + tr['act_show']
            + [tr['act_max'], tr['quiet_share'] * 100])
    for v in vals:
        known.add('%.1f' % v)
        known.add('%.2f' % v)
        known.add('%.3f' % v)
    stray = _screen_numbers(html.replace(tr['model'], '(model)')) - known
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
    assert html.count('class="wc"') == tr['show'], \
        '규약 위반: 넓힌 칸이 %d개여야 한다' % tr['show']
    assert html.count('class="inc"') == NARROW and html.count('class="outc"') == NARROW, \
        '규약 위반: 입력·출력 칸이 %d개여야 한다' % NARROW
    # 보인 칸이 전부가 아니라는 것을 화면이 말해야 한다 — 안 그러면 개수가 주장이 된다
    assert '중 %d칸' % tr['show'] in html and '중 %d칸' % NARROW in html, \
        '규약 위반: 몇 칸 중 몇 칸을 보였는지 화면에 안 적혀 있다'


def selftest():
    tr = load_trace()
    good = render(tr)
    check_ui(good, tr)
    cases = [
        ('없는 숫자 넣기', good.replace('</body>', '<p>9.87</p></body>', 1)),
        ('자막 하나 빼기', good.replace('class="cap"', 'class="x"', 1)),
        ('자막 고르는 자리 빼기', good.replace('function capAt', 'function xAt')),
        ('모션 설정 무시', good.replace('prefers-reduced-motion', 'xx')),
        ('정지 화면 빼기', good.replace('if(still){frame(', 'if(0){frame(')),
        ('버튼 두기', good.replace('</body>', '<button>다음</button></body>', 1)),
        ('넓힌 칸 빼기', good.replace('class="wc"', 'class="x"', 1)),
        ('입력 칸 빼기', good.replace('class="inc"', 'class="x"', 1)),
        ('몇 칸 중 몇 칸인지 지우기', good.replace('중 %d칸' % tr['show'], '칸')),
    ]
    bites = 0
    for name, broken in cases:
        try:
            check_ui(broken, tr)
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
        tr = load_trace()
        html = render(tr)
        check_ui(html, tr)
        io.open(OUT, 'w', encoding='utf-8').write(html)
        print('%s — 한 바퀴 %.1f초 · %d → %d → %d'
              % (OUT, T_END, tr['d_model'], tr['d_ff'], tr['d_model']))
