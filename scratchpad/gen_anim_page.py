# -*- coding: utf-8 -*-
"""어텐션 애니메이션 장 생성기. 아카이브 부품(dash_common)을 안 쓴다.

왜 따로 짰나. 아카이브는 카드가 쌓이는 장의 부품이고 이 장은 카드가 없다 — 한 계산을
일곱 단계로 늦춰 보이는 것이 전부다. 접힘·타일·목록이 그 사이를 막는다.

규약은 check_ui() 가 생성 때 검사한다. 화면에 뜨는 숫자는 전부 data/attn_trace.json 에
있어야 한다 — 그리는 쪽이 값을 지어내지 못하게 막는 자리다.
"""
import io, os, re, sys, json

TRACE = os.path.join('data', 'attn_trace.json')
OUT = os.path.join('대시보드', '애니메이션 — 어텐션.html')

STEPS = [
    ('sentence', '이 자리에서 다음 토큰을 만든다 — 그러려면 앞선 토큰들을 얼마나 볼지 정해야 한다'),
    ('query',    '지금 토큰이 무엇을 찾는지가 Q다 — 이 자리 것 하나뿐이다'),
    ('keys',     '앞선 토큰마다 K가 이미 캐시에 있다 — 새로 만들지 않는다'),
    ('score',    'Q와 K를 왼쪽부터 하나씩 곱해 점수를 낸다 — 막대가 그 점수다'),
    ('softmax',  '점수를 합 1의 비율로 바꾼다 — 이제 막대는 어느 토큰을 얼마나 볼지의 몫이다'),
    ('mix',      '그 비율대로 V를 섞는다 — 많이 보기로 한 토큰의 V가 많이 들어간다'),
    ('out',      '섞인 결과 하나가 이 자리의 어텐션 출력이다'),
]

BW, BG, BX = 62, 10, 70      # K 칸 폭 · 사이 · 왼쪽 시작
QY, KY = 44, 150             # Q 상자 윗변 · K 칸 윗변
BASE, MAXH = 300, 78         # 막대 바닥 · 최대 높이
VY = 330                     # V 칸 윗변


def load_trace(path=TRACE):
    return json.load(io.open(path, encoding='utf-8'))


def _screen_numbers(html):
    """화면에 뜬 숫자를 전부 긁는다.

    사람이 읽는 글자만 본다 — 태그 속성(data-raw 같은 것)도, style·script 안 숫자
    (line-height:1.6 같은 것)도 화면 글자가 아니다.
    """
    body = re.sub('<style[^>]*>.*?</style>', ' ', html, flags=re.S)
    body = re.sub('<script[^>]*>.*?</script>', ' ', body, flags=re.S)
    return set(re.findall(r'-?\d+\.\d+', re.sub(r'<[^>]+>', ' ', body)))


def svg_board(tr):
    m = tr['query_pos'] + 1
    soft, raw = tr['scores_softmax'], tr['scores_raw']
    top = max(soft)
    lo, hi = min(raw), max(raw)
    span = (hi - lo) or 1.0
    w = BX + m * (BW + BG) + 150
    p = ['<svg viewBox="0 0 %d 400" role="img" aria-label="어텐션 계산 한 번">' % w]

    # ② Q — 지금 토큰 것 하나
    qx = BX + tr['query_pos'] * (BW + BG)
    p.append('<g class="fade" data-show="1">'
             '<rect x="%d" y="%d" width="%d" height="42" rx="6" fill="var(--bg-3)" '
             'stroke="var(--hot)" stroke-width="2"/>'
             '<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="var(--ink-1)">Q</text>'
             '<text x="%d" y="%d" font-size="10" text-anchor="middle" fill="var(--ink-3)">%.2f</text>'
             '</g>' % (qx, QY, BW, qx + BW // 2, QY + 19, qx + BW // 2, QY + 34,
                       tr['q_preview'][0]))

    # ③ K — 앞선 토큰마다 하나
    for j in range(m):
        x = BX + j * (BW + BG)
        p.append('<g class="kcell fade" data-show="2">'
                 '<rect x="%d" y="%d" width="%d" height="40" rx="5" fill="var(--bg-2)" '
                 'stroke="var(--ink-3)"/>'
                 '<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="var(--ink-1)">K</text>'
                 '<text x="%d" y="%d" font-size="10" text-anchor="middle" fill="var(--ink-3)">%.2f</text>'
                 '</g>' % (x, KY, BW, x + BW // 2, KY + 17, x + BW // 2, KY + 32,
                           tr['k_preview'][j][0]))
        p.append('<text x="%d" y="%d" font-size="11" text-anchor="middle" fill="var(--ink-3)">%s</text>'
                 % (x + BW // 2, KY + 56, (tr['tokens'][j].strip() or '_')[:4]))

    # ④⑤ 점수 막대 — 스텝 3 은 원점수, 스텝 4 부터 비율
    for j in range(m):
        x = BX + j * (BW + BG)
        h_raw = int(6 + MAXH * (raw[j] - lo) / span)
        h_soft = int(6 + MAXH * soft[j] / top)
        hot = ' data-top="1"' if soft[j] == top else ''
        p.append('<rect class="bar" data-show="3"%s x="%d" y="%d" width="%d" height="0" '
                 'rx="3" fill="var(--bg-3)" stroke="var(--ink-3)" data-raw="%d" data-soft="%d"/>'
                 % (hot, x + 8, BASE, BW - 16, h_raw, h_soft))
        p.append('<text class="softval fade" data-show="4" x="%d" y="%d" font-size="10" '
                 'text-anchor="middle" fill="var(--ink-3)">%.2f</text>'
                 % (x + BW // 2, BASE + 15, soft[j]))

    # ⑥ V — 비율만큼 진하게
    for j in range(m):
        x = BX + j * (BW + BG)
        op = 0.12 + 0.88 * soft[j] / top
        p.append('<g class="vcell fade" data-show="5">'
                 '<rect x="%d" y="%d" width="%d" height="34" rx="5" fill="var(--hot)" '
                 'fill-opacity="%.3f" stroke="var(--ink-3)"/>'
                 '<text x="%d" y="%d" font-size="11" text-anchor="middle" fill="var(--ink-1)">V</text>'
                 '</g>' % (x, VY, BW, op, x + BW // 2, VY + 22))

    # ⑦ 출력 — 섞인 결과 하나
    ox = BX + m * (BW + BG) + 16
    p.append('<g id="out-box" class="fade" data-show="6">'
             '<rect x="%d" y="%d" width="%d" height="34" rx="6" fill="var(--bg-3)" '
             'stroke="var(--hot)" stroke-width="2"/>'
             '<text x="%d" y="%d" font-size="11" text-anchor="middle" fill="var(--ink-1)">출력 %.2f</text>'
             '</g>' % (ox, VY, BW + 56, ox + (BW + 56) // 2, VY + 22, tr['out_preview'][0]))
    p.append('</svg>')
    return '\n'.join(p)


CSS = '''
:root{--ink-1:#222;--ink-3:#8a8a8a;--bg-1:#fafafa;--bg-2:#f4f4f4;--bg-3:#e6e6e6;--hot:#2f8f6b}
@media (prefers-color-scheme:dark){:root{--ink-1:#e8e8e8;--ink-3:#9a9a9a;
  --bg-1:#181818;--bg-2:#202020;--bg-3:#2a2a2a}}
*{box-sizing:border-box}
html,body{margin:0;overflow-x:hidden;background:var(--bg-1);color:var(--ink-1);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:22px 16px 48px}
h1{font-size:19px;margin:0 0 6px;letter-spacing:-.01em}
.meta{font-size:12px;color:var(--ink-3);margin:0 0 16px;line-height:1.6}
.sent{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 14px}
.tk{padding:5px 9px;border:1px solid var(--ink-3);border-radius:6px;font-size:13px;
  background:var(--bg-2);transition:border-color .25s ease,background .25s ease}
.tk.q{border-color:var(--hot);border-width:2px;background:var(--bg-3);font-weight:700}
svg{width:100%;height:auto;display:block}
.stepdesc{display:none;font-size:14px;line-height:1.7;margin:0}
.bar{transition:height .35s ease,y .35s ease,fill .3s ease}
.fade{opacity:0;transition:opacity .35s ease}
.desc{min-height:52px;margin-top:10px;padding:12px 14px;background:var(--bg-2);
  border-radius:8px;border:1px solid var(--bg-3)}
.ctl{display:flex;gap:7px;margin-top:12px;flex-wrap:wrap}
button{font:inherit;font-size:13px;padding:7px 13px;border:1px solid var(--ink-3);
  border-radius:6px;background:var(--bg-2);color:var(--ink-1);cursor:pointer}
button:hover{background:var(--bg-3)}
.dots{display:flex;gap:5px;margin-top:12px}
.dot{width:22px;height:4px;border-radius:2px;background:var(--bg-3);transition:background .25s}
'''

STEP_CSS = '\n'.join(
    '[data-step="%d"] .stepdesc[data-i="%d"]{display:block}' % (i, i)
    for i in range(len(STEPS))) + '\n' + '\n'.join(
    '[data-step="%d"] [data-show="%d"]{opacity:1}' % (i, s)
    for i in range(len(STEPS)) for s in range(0, i + 1)) + '\n' + '\n'.join(
    '[data-step="%d"] .dot[data-i="%d"]{background:var(--hot)}' % (i, d)
    for i in range(len(STEPS)) for d in range(0, i + 1))

JS = '''
(function(){var st=document.getElementById('stage'),n=%d,i=0,t=null,sweep=null;
function setBar(r,v,hot){r.setAttribute('height',v);r.setAttribute('y',%d-v);
  r.setAttribute('fill',hot?'var(--hot)':'var(--bg-3)');}
function go(k){i=Math.max(0,Math.min(n-1,k));st.setAttribute('data-step',i);
  if(sweep){clearTimeout(sweep);sweep=null;}
  var bars=st.querySelectorAll('.bar');
  if(i<3){for(var a=0;a<bars.length;a++)setBar(bars[a],0,false);return;}
  if(i===3){var j=0;(function next(){if(j>=bars.length){sweep=null;return;}
    setBar(bars[j],+bars[j].getAttribute('data-raw'),false);j++;
    sweep=setTimeout(next,350);})();return;}
  for(var b=0;b<bars.length;b++){var r=bars[b];
    setBar(r,+r.getAttribute('data-soft'),!!r.getAttribute('data-top'));}}
function stop(){if(t){clearInterval(t);t=null;}}
document.getElementById('btn-next').onclick=function(){stop();go(i+1)};
document.getElementById('btn-prev').onclick=function(){stop();go(i-1)};
document.getElementById('btn-reset').onclick=function(){stop();go(0)};
document.getElementById('btn-pause').onclick=stop;
go(0);
t=setInterval(function(){if(i>=n-1){stop();}else{go(i+1);}},2200);})();
'''


def render(tr):
    tks = ''.join(
        '<span class="tk%s">%s</span>' % (' q' if i == tr['query_pos'] else '',
                                          t.strip() or '_')
        for i, t in enumerate(tr['tokens']))
    descs = ''.join('<p class="stepdesc" data-i="%d">%s</p>' % (i, d)
                    for i, (_k, d) in enumerate(STEPS))
    dots = ''.join('<span class="dot" data-i="%d"></span>' % i for i in range(len(STEPS)))
    return '''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>애니메이션 — 어텐션</title><style>%s
%s</style></head><body><div class="wrap" id="stage" data-step="0">
<h1>어텐션 계산 한 번을 일곱 걸음으로</h1>
<p class="meta">%s · %d층 %d번 헤드 — 「%s」 자리가 앞 명사를 가장 세게 되짚는 헤드로 골랐다.<br>
화면에 뜨는 값은 그 모델을 실제로 돌려 뽑은 것이다.</p>
<div class="sent">%s</div>
%s
<div class="desc">%s</div>
<div class="dots">%s</div>
<div class="ctl">
<button type="button" id="btn-prev">이전</button>
<button type="button" id="btn-next">다음</button>
<button type="button" id="btn-pause">자동재생 멈춤</button>
<button type="button" id="btn-reset">처음부터</button></div>
</div><script>%s</script></body></html>''' % (
        CSS, STEP_CSS, tr['model'], tr['layer'], tr['head'],
        tr['tokens'][tr['query_pos']].strip(), tks, svg_board(tr), descs, dots,
        JS % (len(STEPS), BASE))


def check_ui(html, tr):
    m = tr['query_pos'] + 1
    n_desc = html.count('class="stepdesc"')
    assert n_desc == len(STEPS), '규약 위반: 설명 줄이 %d개, 스텝은 %d개다' % (n_desc, len(STEPS))
    for i, (key, _d) in enumerate(STEPS):
        assert '[data-step="%d"]' % i in html, \
            '규약 위반: 스텝 %d(%s)에 대응하는 상태가 없다' % (i, key)
    known = set()
    vals = (tr['scores_raw'] + tr['scores_softmax'] + tr['q_preview'] + tr['out_preview']
            + [v for row in tr['k_preview'] + tr['v_preview'] for v in row])
    for v in vals:
        known.add('%.2f' % v)
        known.add('%.3f' % v)
    # 모델 이름(Qwen2.5-0.5B)에 든 숫자는 값이 아니라 이름의 일부다
    stray = _screen_numbers(html.replace(tr['model'], '(model)')) - known
    assert not stray, '규약 위반: 구운 값에 없는 숫자가 화면에 있다 — %s' % sorted(stray)[:5]
    assert 'id="btn-pause"' in html, '규약 위반: 자동재생을 멈출 버튼이 없다'
    flat = html.replace(' ', '')
    assert 'overflow-x:hidden' in flat, '규약 위반: 가로 스크롤을 막는 선언이 없다'
    assert 'width:100%' in flat and 'viewBox' in html, '규약 위반: 판이 폭에 맞춰 안 줄어든다'
    assert html.count('class="kcell') == m, '규약 위반: K 칸이 %d개다 (기대 %d)' % (
        html.count('class="kcell'), m)
    assert html.count('class="bar"') == m, '규약 위반: 막대가 %d개다 (기대 %d)' % (
        html.count('class="bar"'), m)
    assert html.count('class="vcell') == m, '규약 위반: V 칸이 %d개다 (기대 %d)' % (
        html.count('class="vcell'), m)
    assert 'id="out-box"' in html, '규약 위반: 어텐션 출력 상자가 없다'


def selftest():
    tr = load_trace()
    good = render(tr)
    check_ui(good, tr)
    cases = [
        ('설명 줄 빼기', good.replace('class="stepdesc"', 'class="x"', 1)),
        ('스텝 상태 빼기', good.replace('[data-step="3"]', '[data-step="99"]')),
        ('없는 숫자 넣기', good.replace('</body>', '<p>9.87</p></body>', 1)),
        ('멈춤 버튼 빼기', good.replace('id="btn-pause"', 'id="x"', 1)),
        ('가로 스크롤 허용', good.replace('overflow-x:hidden', 'overflow-x:auto', 1)),
        ('K 칸 빼기', good.replace('class="kcell', 'class="x', 1)),
        ('막대 빼기', good.replace('class="bar"', 'class="x"', 1)),
        ('V 칸 빼기', good.replace('class="vcell', 'class="x', 1)),
        ('출력 상자 빼기', good.replace('id="out-box"', 'id="x"', 1)),
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
        print('%s — 스텝 %d개 · 토큰 %d개 · 막대 %d개'
              % (OUT, len(STEPS), len(tr['tokens']), tr['query_pos'] + 1))
