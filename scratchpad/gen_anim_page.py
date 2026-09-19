# -*- coding: utf-8 -*-
"""어텐션 애니메이션 장 생성기. 대시보드 부품을 아무것도 안 쓴다.

왜 틀을 걷었나. 처음에는 버튼·설명 상자·진행 점을 붙인 「단계 넘기는 화면」으로 만들었는데
그건 애니메이션이 아니라 슬라이드였다. 어텐션은 한 번에 흐르는 계산이라 걸음을 사람이
끊어 넘기면 흐름이 안 보인다. 머리말·토큰 칩·설명 상자·버튼·진행 점을 전부 걷고 시계
하나로 도는 한 장면으로 다시 세웠다.

남은 규약은 다섯이고 check_ui() 가 생성 때 본다. 지어낸 숫자가 못 샌다 · 자막이 장면마다
하나다 · 안 움직이게 설정한 사람에게는 정지 화면을 준다 · 틀(버튼·머리말·설명 상자·진행
점)을 안 세운다 · 칸 수가 구운 값과 맞는다.
"""
import io, os, re, sys, json

TRACE = os.path.join('data', 'attn_trace.json')
OUT = os.path.join('대시보드', '애니메이션 — 어텐션.html')

# ── 판 좌표 ─────────────────────────────────────────────────
W, H = 1000, 620
TOKY = 64            # 문장 줄
QY = 180             # Q 칩이 내려와 머무는 높이
KY = 292             # K 칸
BARBASE = 452        # 막대 바닥
BARMAX = 118         # 막대 최대 높이
VY = 486             # V 칸
CAPY = 578           # 자막
CW, CGAP = 74, 9     # 칸 폭 · 사이

# ── 시계 (초) ───────────────────────────────────────────────
T_TOK = 2.4
T_Q = 4.4
T_SCAN = 6.2
SCAN_STEP = 0.85

CAPS = [
    '「그것은」이 무엇을 가리키는지 찾는 중이다',
    '지금 이 자리가 무엇을 찾는가 — 그것이 Q 하나다',
    '앞선 토큰마다 K 가 이미 남아 있다',
    'Q 를 K 하나하나에 대 본다 — 닮은 만큼 점수가 선다',
    '점수를 합이 1 인 비율로 바꾼다',
    '그 비율만큼 V 를 섞는다',
    '섞여 나온 하나 — 이 자리의 어텐션 출력이다',
]


def load_trace(path=TRACE):
    return json.load(io.open(path, encoding='utf-8'))


def _screen_numbers(html):
    """사람이 읽는 글자 속 숫자만. style·script 안과 태그 속성은 화면 글자가 아니다."""
    body = re.sub('<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    body = re.sub('<script[^>]*>.*?</script>', ' ', body, flags=re.S)
    return set(re.findall(r'-?\d+\.\d+', re.sub(r'<[^>]+>', ' ', body)))


def layout(tr):
    n = len(tr['tokens'])
    total = n * CW + (n - 1) * CGAP
    x0 = (W - total) / 2.0
    return tr['query_pos'] + 1, n, [x0 + i * (CW + CGAP) for i in range(n)]


def timings(m):
    t_soft = T_SCAN + m * SCAN_STEP + 0.6
    t_v = t_soft + 2.6
    t_out = t_v + 2.4
    return {'tok': T_TOK, 'q': T_Q, 'scan': T_SCAN, 'step': SCAN_STEP,
            'soft': t_soft, 'v': t_v, 'out': t_out, 'end': t_out + 4.2}


def svg_scene(tr, uid='stage', style=''):
    """장면 SVG 한 덩이. uid 를 갈라 주면 한 페이지에 여럿 세울 수 있다."""
    m, n, xs = layout(tr)
    p = ['<svg id="%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet"%s '
         'role="img" aria-label="어텐션 계산 한 번이 흐르는 장면">'
         % (uid, W, H, (' style="%s"' % style) if style else '')]
    p.append(('<defs><linearGradient id="beam-%s" x1="0" y1="0" x2="0" y2="1">'
              '<stop offset="0" stop-color="var(--hot)" stop-opacity=".1"/>'
              '<stop offset="1" stop-color="var(--hot)" stop-opacity=".95"/>'
              '</linearGradient></defs>') % uid)
    for i, t in enumerate(tr['tokens']):
        cls = 'tok' + (' tokq' if i == tr['query_pos'] else '')
        p.append('<g class="%s" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="38" rx="7"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                 % (cls, xs[i], TOKY, CW, xs[i] + CW / 2, TOKY + 25, t.strip() or '·'))
    p.append('<line class="beam" x1="0" y1="0" x2="0" y2="0" stroke="url(#beam-%s)" '
             'stroke-width="3" stroke-linecap="round" opacity="0"/>' % uid)
    for j in range(m):
        p.append('<g class="kc" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="40" rx="7"/>'
                 '<text class="kk" x="%.1f" y="%d" text-anchor="middle">K</text>'
                 '<text class="kv" x="%.1f" y="%d" text-anchor="middle">%.2f</text></g>'
                 % (xs[j], KY, CW, xs[j] + CW / 2, KY + 17,
                    xs[j] + CW / 2, KY + 32, tr['k_preview'][j][0]))
    for j in range(m):
        p.append('<rect class="bar" x="%.1f" y="%d" width="%d" height="0" rx="4"/>'
                 % (xs[j] + 11, BARBASE, CW - 22))
        p.append('<text class="bv" x="%.1f" y="%d" text-anchor="middle" opacity="0">%.2f</text>'
                 % (xs[j] + CW / 2, BARBASE + 17, tr['scores_softmax'][j]))
    for j in range(m):
        p.append('<g class="vc" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="34" rx="7"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">V</text></g>'
                 % (xs[j], VY, CW, xs[j] + CW / 2, VY + 23))
    for _j in range(m):
        p.append('<circle class="flow" r="4" opacity="0"/>')
    ox = xs[m - 1] + CW + 40
    p.append('<g class="outb" opacity="0">'
             '<rect x="%.1f" y="%d" width="140" height="34" rx="8"/>'
             '<text x="%.1f" y="%d" text-anchor="middle">출력 %.2f</text></g>'
             % (ox, VY, ox + 70, VY + 23, tr['out_preview'][0]))
    for txt in CAPS:
        p.append('<text class="cap" x="%d" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (W // 2, CAPY, txt))
    p.append('</svg>')
    return '\n'.join(p), ox


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
.outb rect{fill:var(--bg-2);stroke:var(--hot);stroke-width:2}
.outb text{font-size:14px}
.flow{fill:var(--hot)}
.cap{font-size:17px;letter-spacing:-.01em}
#src{position:fixed;left:14px;bottom:10px;margin:0;font-size:11px;color:var(--ink-3)}
'''

JS = r'''
(function(){
var D=__DATA__;
var st=document.getElementById(D.uid);
var q=function(s){return [].slice.call(st.querySelectorAll(s));};
var toks=q('.tok'),kcs=q('.kc'),bars=q('.bar'),bvs=q('.bv'),vcs=q('.vc'),flows=q('.flow');
var beam=q('.beam')[0],out=q('.outb')[0],caps=q('.cap');
var T=D.t,m=D.m,xs=D.xs,cw=D.cw;
var topw=Math.max.apply(null,D.bars.map(function(b){return b.w;}));
var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
function cl(v,a,b){return v<a?a:(v>b?b:v);}
function seg(t,a,b){return cl((t-a)/(b-a),0,1);}
function ease(u){return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;}
function set(e,k,v){e.setAttribute(k,v);}

var qbox=document.createElementNS('http://www.w3.org/2000/svg','g');
qbox.setAttribute('opacity','0');
qbox.innerHTML='<rect width="'+cw+'" height="40" rx="7" fill="var(--hot-soft)" '+
  'stroke="var(--hot)" stroke-width="2"/>'+
  '<text x="'+(cw/2)+'" y="17" text-anchor="middle" font-size="13">Q</text>'+
  '<text x="'+(cw/2)+'" y="32" text-anchor="middle" font-size="11" fill="var(--ink-3)">'+
  D.qv+'</text>';
st.appendChild(qbox);

function capAt(t){
  // 자막이 뜨는 구간은 그 장면이 실제로 도는 구간과 맞춘다. 예전에는 둘이 1초도 안
  // 떠 있어 읽기 전에 넘어갔다.
  if(t<T.tok)return 0; if(t<T.q-.6)return 1; if(t<T.scan)return 2;
  if(t<T.soft)return 3; if(t<T.v)return 4; if(t<T.out)return 5; return 6;
}

function frame(t){
  var per=T.tok/toks.length;
  for(var i=0;i<toks.length;i++){
    var u=ease(seg(t,i*per,i*per+.6));
    set(toks[i],'opacity',u.toFixed(3));
  }
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
  for(var j=0;j<kcs.length;j++)set(kcs[j],'opacity',ease(seg(t,T.q-1.0+j*.09,T.q-.3+j*.09)).toFixed(3));
  for(var j=0;j<m;j++){
    var b=D.bars[j],h=0;
    if(t>=T.scan&&t<T.soft)h=b.raw*ease(seg(t,T.scan+j*T.step,T.scan+j*T.step+.6));
    else if(t>=T.soft)h=b.raw+(b.soft-b.raw)*ease(seg(t,T.soft,T.soft+1.4));
    set(bars[j],'height',h.toFixed(1));set(bars[j],'y',(D.barbase-h).toFixed(1));
    if(t>=T.soft&&b.top)bars[j].classList.add('hot');else bars[j].classList.remove('hot');
    set(bvs[j],'opacity',ease(seg(t,T.soft+.6,T.soft+1.5)).toFixed(3));
  }
  for(var j=0;j<m;j++){
    var uv=ease(seg(t,T.v+j*.08,T.v+j*.08+.7));
    set(vcs[j],'opacity',uv.toFixed(3));
    vcs[j].querySelector('rect').setAttribute(
      'fill-opacity',((.12+.88*D.bars[j].w/topw)*uv).toFixed(3));
    var uf=seg(t,T.out-.8+j*.08,T.out+1.2);
    set(flows[j],'opacity',(uf>0&&uf<1?(.3+.7*D.bars[j].w/topw):0).toFixed(3));
    set(flows[j],'cx',(xs[j]+cw/2+(D.ox+70-xs[j]-cw/2)*ease(uf)).toFixed(1));
    set(flows[j],'cy',(D.vy+17).toFixed(1));
  }
  set(out,'opacity',ease(seg(t,T.out+.7,T.out+1.5)).toFixed(3));
  var ci=capAt(t);
  for(var c=0;c<caps.length;c++)set(caps[c],'opacity',c===ci?1:0);
}

if(still){frame(T.out+1.6);return;}
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


def scene_js(tr, uid, ox):
    """그 장면을 돌리는 시계. uid 로 자기 SVG 만 잡으니 한 페이지에 여럿 서도 안 섞인다."""
    m, n, xs = layout(tr)
    soft, raw = tr['scores_softmax'], tr['scores_raw']
    top = max(soft)
    lo, hi = min(raw), max(raw)
    span = (hi - lo) or 1.0
    data = {
        'uid': uid,
        'm': m, 'xs': xs, 'cw': CW, 'qx': xs[tr['query_pos']],
        'toky': TOKY, 'qy': QY, 'ky': KY, 'barbase': BARBASE, 'vy': VY, 'ox': ox,
        'qv': '%.2f' % tr['q_preview'][0],
        'bars': [{'raw': round(10 + BARMAX * (raw[j] - lo) / span, 1),
                  'soft': round(10 + BARMAX * soft[j] / top, 1),
                  'w': soft[j], 'top': soft[j] == top} for j in range(m)],
        't': timings(m),
    }
    return JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))


# 카드 안에 넣을 때 쓰는 붓. 전면 화면용 CSS 는 :root 를 건드리므로 그대로 못 쓴다 —
# 이쪽은 그 SVG 안으로만 범위를 좁히고 색은 대시보드 변수에서 받는다.
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
#%(u)s .outb rect{fill:var(--bg-2);stroke:var(--hot);stroke-width:2}
#%(u)s .outb text{font-size:14px}
#%(u)s .flow{fill:var(--hot)}
#%(u)s .cap{font-size:17px;letter-spacing:-.01em}
'''


def embed(tr, uid='attn-scene', maxw=900):
    """카드 그림 자리에 그대로 넣는 한 덩이 — 스타일·장면·시계가 같이 간다."""
    scene, ox = svg_scene(tr, uid, style='max-width:%dpx' % maxw)
    return ('<style>%s</style>\n%s\n<script>%s</script>'
            % (EMBED_CSS % {'u': uid}, scene, scene_js(tr, uid, ox)))


def render(tr):
    scene, ox = svg_scene(tr)
    js = scene_js(tr, 'stage', ox)
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>애니메이션 — 어텐션</title><style>%s</style></head><body>
<div id="wrap">%s</div>
<p id="src">%s · %d층 %d번 헤드 — 「%s」 자리에서 잰 실제 값이다</p>
<script>%s</script></body></html>''' % (
        CSS, scene, tr['model'], tr['layer'], tr['head'],
        tr['tokens'][tr['query_pos']].strip(), js)


def check_ui(html, tr):
    m = tr['query_pos'] + 1
    known = set()
    vals = (tr['scores_raw'] + tr['scores_softmax'] + tr['q_preview'] + tr['out_preview']
            + [v for row in tr['k_preview'] + tr['v_preview'] for v in row])
    for v in vals:
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
    for cls, name in [('kc', 'K'), ('bar', '막대'), ('vc', 'V'), ('flow', '알갱이')]:
        got = html.count('class="%s"' % cls)
        assert got == m, '규약 위반: %s 칸이 %d개다 (기대 %d)' % (name, got, m)


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
        ('머리말 두기', good.replace('<div id="wrap">', '<h1>어텐션</h1><div id="wrap">', 1)),
        ('K 칸 빼기', good.replace('class="kc"', 'class="x"', 1)),
        ('알갱이 빼기', good.replace('class="flow"', 'class="x"', 1)),
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
        m = tr['query_pos'] + 1
        print('%s — 한 바퀴 %.1f초 · 칸 %d개' % (OUT, timings(m)['end'], m))
