# -*- coding: utf-8 -*-
"""엔그램(N-gram 임베딩) 애니메이션 — FFN 과 나란히 놓고 견준다.

따로 그리면 「표에서 꺼낸다」가 FFN 과 같은 말로 들린다. 둘이 갈리는 지점은 하나뿐이다 —
**어디를 읽을지 언제 아느냐.** FFN 은 입력을 key 전부와 대 봐야 알고, 엔그램은 토큰 ID
만으로 먼저 안다. 그 차이가 표를 어느 메모리에 둘 수 있느냐까지 끌고 간다. 그래서 좌우
대비로 세웠다(규칙 — 도해, 조건과 결과가 어긋나는 자리는 좌우 대비).

값의 출처가 둘이라 화면에서 갈라 적는다. 토큰 ID 와 행 번호는 이 저장소에서 다시 돌리면
그대로 나오는 값이고, 표 크기·토큰당 읽는 양은 뉴스레터 변환본에서 가져온 값이다.
check_ui() 가 둘 다 밝혀져 있는지 본다.
"""
import io, os, re, sys, json

TRACE = os.path.join('data', 'ngram_trace.json')
FFN = os.path.join('data', 'ffn_trace.json')
OUT = os.path.join('대시보드', '애니메이션 — 엔그램.html')

W, H = 1040, 620
MID = W / 2.0
COLW = 460                 # 한 칸 폭
LX = MID - COLW - 16       # 왼쪽 칸 왼끝
RX = MID + 16              # 오른쪽 칸 왼끝
HEADY = 54                 # 칸 이름
INY = 112                  # 무엇을 들고 시작하나
ARROWY = 196               # 찾는 방법
TABY = 250                 # 표
TABH = 58
READY = 344                # 읽은 양
WHYY = 410                 # 그래서 어디에 두나
CAPY = 566
NCOL = 26                  # 표를 몇 칸으로 그리나
TBG = 3

T_HEAD = 1.8
T_IN = 3.6
T_WAY = 6.0
T_SCAN = 8.4               # 왼쪽이 표 전체를 훑는다
T_HIT = 12.0               # 둘 다 걸린 칸만 남는다
T_READ = 14.6              # 읽은 양이 적힌다
T_WHY = 17.2               # 그래서 어느 메모리에 두나
T_END = 21.4

CAPS = [
    '같은 일을 하는 둘이다 — 표에서 꺼내 잔차 스트림에 더한다',
    '열쇠로 드는 것이 다르다 — 이어지는 값이냐, 딱 떨어지는 번호냐',
    '찾는 법이 다르다. FFN 은 전부와 대 보고, 엔그램은 번지수를 계산한다',
    'FFN 은 어디가 걸릴지 알려면 표를 끝까지 훑어야 한다',
    '둘 다 결국 몇 칸만 쓴다 — 다른 것은 그 몇 칸을 언제 아느냐다',
    '읽어야 하는 양이 갈린다',
    '그래서 하나는 HBM 에 있어야 하고 하나는 DRAM 으로 나갈 수 있다',
]


def load_trace(path=TRACE):
    return json.load(io.open(path, encoding='utf-8'))


def load_ffn(path=FFN):
    return json.load(io.open(path, encoding='utf-8'))


def _screen_numbers(html):
    body = re.sub('<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    body = re.sub('<script[^>]*>.*?</script>', ' ', body, flags=re.S)
    return set(re.findall(r'-?\d+\.\d+', re.sub(r'<[^>]+>', ' ', body)))


def _cells(x0, n, w):
    step = (COLW - w) / float(n - 1)
    return [x0 + i * step for i in range(n)]


def svg_scene(tr, ft, uid='ngram', style=''):
    f = tr['from']
    rows = [l['row'] for l in tr['lookups'][:4]]
    lhit = sorted({(r * 7 + 3) % NCOL for r in rows})        # 왼쪽에서 살아남는 칸
    rhit = sorted({r % NCOL for r in rows})                  # 오른쪽에서 짚는 칸
    lxs, rxs = _cells(LX, NCOL, 12), _cells(RX, NCOL, 12)

    p = ['<svg id="%s" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet"%s '
         'role="img" aria-label="FFN 과 엔그램이 표에서 꺼내는 방식을 나란히 견준 장면">'
         % (uid, W, H, (' style="%s"' % style) if style else '')]
    p.append('<line class="divider" x1="%.1f" y1="36" x2="%.1f" y2="%d" opacity="0"/>'
             % (MID, MID, WHYY + 70))

    def col(x, side, head, keys, klabel, way, readn, why):
        """keys = [(글자, 진하기)]. 양쪽을 같은 크기 칸 한 줄로 그린다 — 하나는 벡터고
        하나는 토큰 ID 라 꼴까지 다르면 견줄 수가 없다(규칙 — 도해, 견줄 때는 같은 꼴)."""
        p.append('<text class="head %s" x="%.1f" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (side, x + COLW / 2, HEADY, head))
        kw, kg = 38, 6
        total = len(keys) * kw + (len(keys) - 1) * kg
        kx = x + (COLW - total) / 2.0
        p.append('<g class="inb %s" opacity="0">' % side)
        for i, (lab, dens) in enumerate(keys):
            cx = kx + i * (kw + kg)
            p.append('<rect class="keyc" x="%.1f" y="%d" width="%d" height="34" rx="5" '
                     'fill-opacity="%.3f"/>' % (cx, INY, kw, dens))
            p.append('<text x="%.1f" y="%d" text-anchor="middle">%s</text>'
                     % (cx + kw / 2.0, INY + 22, lab))
        p.append('<text class="klbl" x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                 % (x + COLW / 2, INY + 52, klabel))
        p.append('<text class="way %s" x="%.1f" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (side, x + COLW / 2, ARROWY, way))
        p.append('<text class="readn %s" x="%.1f" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (side, x + COLW / 2, READY, readn))
        p.append('<g class="whyb %s" opacity="0">'
                 '<rect x="%.1f" y="%d" width="%d" height="44" rx="8"/>'
                 '<text x="%.1f" y="%d" text-anchor="middle">%s</text></g>'
                 % (side, x + 30, WHYY, COLW - 60, x + COLW / 2, WHYY + 28, why))

    # 열쇠로 드는 것 — 같은 크기 칸으로 그리고 개수와 내용만 다르게 둔다
    vin = ft['in_preview'][:6]
    vmax = max(abs(v) for v in vin) or 1.0
    lkeys = [('%.1f' % v, 0.25 + 0.75 * abs(v) / vmax) for v in vin]
    rkeys = [(str(i), 1.0) for i in tr['tri_ids']]
    col(LX, 'L', 'FFN', lkeys,
        '벡터 ' + str(ft['d_model']) + '칸 중 ' + str(len(vin)) + '칸 — 값이 이어진다',
        '표 전체와 하나씩 대 본다',
        '표 전체를 읽는다 — 한 층 가중치 ' + format(ft['params']['ffn_per_layer'], ',') + '개',
        'HBM 에 있어야 한다')
    col(RX, 'R', '엔그램', rkeys,
        '토큰 ID ' + str(len(rkeys)) + '개 — 번호가 딱 떨어진다',
        '해시로 행 번호를 낸다',
        '짚은 행만 읽는다 — 토큰 자리 하나당 ' + str(f['deepseek_kib_per_token']) + ' KiB',
        'DRAM 으로 나갈 수 있다')

    # 표 — 왼쪽은 훑고, 오른쪽은 짚는다
    for i in range(NCOL):
        p.append('<rect class="lc%s" x="%.1f" y="%d" width="12" height="%d" rx="3" opacity="0"/>'
                 % (' lhit' if i in lhit else '', lxs[i], TABY, TABH))
        p.append('<rect class="rc%s" x="%.1f" y="%d" width="12" height="%d" rx="3" opacity="0"/>'
                 % (' rhit' if i in rhit else '', rxs[i], TABY, TABH))
    p.append('<rect class="scan" x="%.1f" y="%d" width="16" height="%d" rx="3" opacity="0"/>'
             % (LX, TABY - 4, TABH + 8))
    p.append('<text class="lbl lbl-l" x="%.1f" y="%d" text-anchor="middle" opacity="0">'
             '표 — 어디가 걸릴지는 다 대 봐야 안다</text>' % (LX + COLW / 2, TABY - 12))
    p.append('<text class="lbl lbl-r" x="%.1f" y="%d" text-anchor="middle" opacity="0">'
             '표 — 읽을 자리가 먼저 정해진다</text>' % (RX + COLW / 2, TABY - 12))

    for txt in CAPS:
        p.append('<text class="cap" x="%.1f" y="%d" text-anchor="middle" opacity="0">%s</text>'
                 % (MID, CAPY, txt))
    p.append('</svg>')
    return '\n'.join(p)


CSS = '''
:root{--ink-1:#1c1c1c;--ink-3:#8d8d8d;--bg-1:#fbfbfa;--bg-2:#efefee;--bg-3:#e0e0de;
  --hot:#1f7a5c;--hot-soft:#d9ede5;--cool:#8d8d8d}
@media (prefers-color-scheme:dark){:root{--ink-1:#ededec;--ink-3:#8f8f8f;
  --bg-1:#121212;--bg-2:#1e1e1e;--bg-3:#2c2c2c;--hot:#4fc39b;--hot-soft:#1b3a31}}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--bg-1);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
#wrap{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:14px}
svg{width:100%;height:100%}
text{fill:var(--ink-1);font-size:15px}
.divider{stroke:var(--bg-3);stroke-width:1.5;stroke-dasharray:5 5}
.head{font-size:19px;font-weight:800;letter-spacing:-.01em}
.whyb rect{fill:var(--bg-2);stroke:var(--ink-3)}
.keyc{fill:var(--hot);stroke:var(--ink-3)}
.klbl{font-size:12px;fill:var(--ink-3)}
.whyb.R rect{stroke:var(--hot);stroke-width:2}
.inb text{font-size:13px}
.whyb text{font-size:14px}
.way,.readn{font-size:13px;fill:var(--ink-3)}
.lc,.rc{fill:var(--bg-3)}
.lc.lhit,.rc.rhit{fill:var(--hot)}
.scan{fill:var(--hot);opacity:.35}
.lbl{font-size:12px;fill:var(--ink-3)}
.cap{font-size:17px;letter-spacing:-.01em}
#src{position:fixed;left:14px;bottom:10px;margin:0;font-size:11px;color:var(--ink-3);
  line-height:1.6;max-width:72%}
'''

EMBED_CSS = '''
#%(u)s{--hot:var(--accent,#1f7a5c);--hot-soft:var(--accent-soft,#d9ede5);
  --bg-2:var(--card,#f4f4f3);--bg-3:var(--line,#e0e0de);
  --ink-1:var(--ink,#1c1c1c);--ink-3:var(--ink-3,#8d8d8d)}
#%(u)s text{fill:var(--ink-1);font-size:15px}
#%(u)s .divider{stroke:var(--bg-3);stroke-width:1.5;stroke-dasharray:5 5}
#%(u)s .head{font-size:19px;font-weight:800}
#%(u)s .whyb rect{fill:var(--bg-2);stroke:var(--ink-3)}
#%(u)s .keyc{fill:var(--hot);stroke:var(--ink-3)}
#%(u)s .klbl{font-size:12px;fill:var(--ink-3)}
#%(u)s .whyb.R rect{stroke:var(--hot);stroke-width:2}
#%(u)s .inb text{font-size:13px}
#%(u)s .whyb text{font-size:14px}
#%(u)s .way,#%(u)s .readn{font-size:13px;fill:var(--ink-3)}
#%(u)s .lc,#%(u)s .rc{fill:var(--bg-3)}
#%(u)s .lc.lhit,#%(u)s .rc.rhit{fill:var(--hot)}
#%(u)s .scan{fill:var(--hot);opacity:.35}
#%(u)s .lbl{font-size:12px;fill:var(--ink-3)}
#%(u)s .cap{font-size:17px;letter-spacing:-.01em}
'''

JS = r'''
(function(){
var D=__DATA__;
var st=document.getElementById(D.uid);
var q=function(s){return [].slice.call(st.querySelectorAll(s));};
var heads=q('.head'),inb=q('.inb'),ways=q('.way'),readn=q('.readn'),whyb=q('.whyb');
var lc=q('.lc'),rc=q('.rc'),scan=q('.scan')[0],caps=q('.cap');
var divider=q('.divider')[0],lbll=q('.lbl-l')[0],lblr=q('.lbl-r')[0];
var T=D.t;
var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
function cl(v,a,b){return v<a?a:(v>b?b:v);}
function seg(t,a,b){return cl((t-a)/(b-a),0,1);}
function ease(u){return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;}
function set(e,k,v){if(e)e.setAttribute(k,v);}
function setAll(a,k,v){for(var i=0;i<a.length;i++)set(a[i],k,v);}

function capAt(t){
  if(t<T.in)return 0; if(t<T.way)return 1; if(t<T.scan)return 2;
  if(t<T.hit)return 3; if(t<T.read)return 4; if(t<T.why)return 5; return 6;
}

function frame(t){
  set(divider,'opacity',ease(seg(t,T.head,T.head+.8)).toFixed(3));
  setAll(heads,'opacity',ease(seg(t,0,T.head)).toFixed(3));
  setAll(inb,'opacity',ease(seg(t,T.in-.8,T.in)).toFixed(3));
  setAll(ways,'opacity',ease(seg(t,T.way-.8,T.way)).toFixed(3));
  var born=ease(seg(t,T.way,T.way+.8));
  set(lbll,'opacity',born.toFixed(3));set(lblr,'opacity',born.toFixed(3));
  // 왼쪽 — 훑는 빛이 표 전체를 지난다. 다 지난 뒤에야 걸린 칸이 드러난다
  var sc=seg(t,T.scan,T.hit);
  set(scan,'opacity',(sc>0&&sc<1?.35:0).toFixed(3));
  set(scan,'x',(D.lx+(D.colw-16)*sc).toFixed(1));
  var lhit=ease(seg(t,T.hit,T.hit+1.0));
  for(var i=0;i<lc.length;i++){
    var on=lc[i].classList.contains('lhit');
    var touched=sc>0?(i/(lc.length-1)<=sc?1:0):0;
    var base=born*(.25+.35*touched);
    set(lc[i],'opacity',(on?Math.max(base,lhit):base*(1-lhit*.6)).toFixed(3));
  }
  // 오른쪽 — 짚은 칸이 바로 켜진다. 훑는 일이 없다
  var rhit=ease(seg(t,T.way+.6,T.way+1.6));
  for(var i=0;i<rc.length;i++){
    var on=rc[i].classList.contains('rhit');
    set(rc[i],'opacity',(born*(on?Math.max(.25,rhit):.25)).toFixed(3));
  }
  setAll(readn,'opacity',ease(seg(t,T.read,T.read+.9)).toFixed(3));
  setAll(whyb,'opacity',ease(seg(t,T.why,T.why+.9)).toFixed(3));
  var ci=capAt(t);
  for(var c=0;c<caps.length;c++)set(caps[c],'opacity',c===ci?1:0);
}

if(still){frame(T.why+1.2);return;}
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
    data = {'uid': uid, 'lx': LX, 'colw': COLW,
            't': {'head': T_HEAD, 'in': T_IN, 'way': T_WAY, 'scan': T_SCAN,
                  'hit': T_HIT, 'read': T_READ, 'why': T_WHY, 'end': T_END}}
    return JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))


def embed(tr, ft, uid='ngram-scene', maxw=920):
    return ('<style>%s</style>\n%s\n<script>%s</script>'
            % (EMBED_CSS % {'u': uid},
               svg_scene(tr, ft, uid, style='max-width:%dpx' % maxw), scene_js(tr, uid)))


def render(tr, ft):
    f = tr['from']
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>애니메이션 — 엔그램과 FFN</title><style>%s</style></head><body>
<div id="wrap">%s</div>
<p id="src">FFN 가중치 개수는 %s 를 돌려 이 저장소에서 계산한 값이다.<br>
엔그램 수치는 SemiAnalysis 뉴스레터 변환본에서 가져왔다 — DeepSeek-V4.1-Flash 기준 표 %s
(%s GiB)를 층마다 %d행씩 읽어 토큰 자리 하나당 %s KiB, GPU 4장에 나누면 한 장당 %s KiB.</p>
<script>%s</script></body></html>''' % (
        CSS, svg_scene(tr, ft, 'ngram'), tr['model'],
        f['deepseek_table_params'], f['deepseek_table_gib'], f['deepseek_rows_per_layer'],
        f['deepseek_kib_per_token'], f['deepseek_kib_per_gpu'], scene_js(tr, 'ngram'))


def check_ui(html, tr, ft):
    known = set()
    # 왼쪽 열쇠 칸에 뜨는 값은 FFN 구운 값에서 온다
    for v in ft['in_preview']:
        known.add('%.1f' % v)
        known.add('%.2f' % v)
    for v in tr['from'].values():
        for n in re.findall(r'-?\d+\.\d+', str(v)):
            known.add(n)
        if isinstance(v, (int, float)):
            known.add('%.1f' % v)
    txt = html.replace(tr['model'], '(model)').replace('DeepSeek-V4.1-Flash', '(ds)')
    stray = _screen_numbers(txt) - known
    assert not stray, '규약 위반: 근거 없는 숫자가 화면에 있다 — %s' % sorted(stray)[:5]
    assert html.count('class="cap"') == len(CAPS), \
        '규약 위반: 자막이 %d개, 장면은 %d개다' % (html.count('class="cap"'), len(CAPS))
    assert 'function capAt' in html, '규약 위반: 어느 자막을 띄울지 정하는 자리가 없다'
    assert 'prefers-reduced-motion' in html, '규약 위반: 애니메이션을 줄이라는 설정을 안 본다'
    assert 'if(still){frame(' in html.replace(' ', ''), \
        '규약 위반: 줄이라고 한 사람에게 정지 화면을 안 준다'
    for banned, why in [('<button', '버튼'), ('class="stepdesc"', '설명 상자'),
                        ('class="dot"', '진행 점'), ('<h1', '머리말')]:
        assert banned not in html, '규약 위반: %s 을 두지 않는다 — 이 장은 한 장면이다' % why
    # 이 편은 대비가 요점이다 — 양쪽이 같은 항목으로 서 있어야 한다
    for cls, name in [('head', '칸 이름'), ('inb', '드는 것'), ('way', '찾는 법'),
                      ('readn', '읽는 양'), ('whyb', '어디에 두나')]:
        got = html.count('class="%s ' % cls)
        assert got == 2, '규약 위반: %s 이 %d개다 — 좌우 한 쌍이어야 한다' % (name, got)
    assert 'class="scan"' in html, '규약 위반: FFN 쪽이 표를 훑는 것이 안 보인다'
    assert html.count('lhit') >= 2 and html.count('rhit') >= 2, \
        '규약 위반: 양쪽 표에서 걸린 칸이 갈라져 있지 않다'
    # 값의 출처가 둘이라 화면이 갈라 적어야 한다
    assert '이 저장소에서 계산한' in html and '뉴스레터 변환본에서 가져왔다' in html, \
        '규약 위반: 계산한 값과 원문에서 가져온 값을 갈라 적지 않았다'


def selftest():
    tr, ft = load_trace(), load_ffn()
    good = render(tr, ft)
    check_ui(good, tr, ft)
    cases = [
        ('근거 없는 숫자 넣기', good.replace('</body>', '<p>9.87</p></body>', 1)),
        ('자막 하나 빼기', good.replace('class="cap"', 'class="x"', 1)),
        ('자막 고르는 자리 빼기', good.replace('function capAt', 'function xAt')),
        ('모션 설정 무시', good.replace('prefers-reduced-motion', 'xx')),
        ('정지 화면 빼기', good.replace('if(still){frame(', 'if(0){frame(')),
        ('버튼 두기', good.replace('</body>', '<button>다음</button></body>', 1)),
        ('한쪽 칸 이름 빼기', good.replace('class="head ', 'class="x ', 1)),
        ('한쪽 「읽는 양」 빼기', good.replace('class="readn ', 'class="x ', 1)),
        ('훑는 것 빼기', good.replace('class="scan"', 'class="x"')),
        ('출처 구분 지우기', good.replace('뉴스레터 변환본에서 가져왔다', '이다')),
    ]
    bites = 0
    for name, broken in cases:
        try:
            check_ui(broken, tr, ft)
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
        tr, ft = load_trace(), load_ffn()
        html = render(tr, ft)
        check_ui(html, tr, ft)
        io.open(OUT, 'w', encoding='utf-8').write(html)
        print('%s — 한 바퀴 %.1f초 · 좌우 대비' % (OUT, T_END))
