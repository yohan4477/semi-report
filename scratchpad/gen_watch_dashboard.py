# -*- coding: utf-8 -*-
# 포트폴리오 워치 대시보드 생성. 보유 자산이 아니라 **보고 있는 대상**을 세우는 장이다.
# 설계는 docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md.
#
# 워치 줄은 insights/watch/<kind>/*.md 에 있고 여기서는 읽어서 카드로 굽기만 한다.
# 이 파일에 판단을 적지 않는다 — 적으면 같은 글이 두 벌이 되고 한쪽만 고친 날부터
# 어느 것이 맞는지 알 수 없게 된다.
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
sys.path.insert(0, os.path.join(dc.ROOT, 'insights'))
import watch_lib as wl  # noqa: E402
import watch_fig as wf  # noqa: E402

OUT = os.path.join(dc.ROOT, '대시보드', '포트폴리오 워치.html')
STAMP = '2026-08-31'

SECS = {
    'realestate': ('sec-area', '01', '권역 — 부동산',
                   '어느 권역을 왜 보고 있고, 무엇이 일어나면 판단이 바뀌나. '
                   '개별 물건이 아니라 권역이 한 줄이다'),
    'equity': ('sec-ticker', '02', '종목 — 주식',
               '보유가 아니라 관찰이다. 적정가를 재는 자리는 밸류에이션 쪽이고 '
               '여기는 「무엇을 기다리나」만 세운다'),
}
LABEL = {'realestate': '부동산 — 권역', 'equity': '주식 — 종목'}

# 트리거 표의 열은 어느 자산군이든 같다 — 어댑터가 자산군마다 값만 다르게 채운다.
# 「언제 것 · 성격」은 CLAUDE.md 가 값에 요구하는 두 열이라 어댑터 계약에 박혀 있다.
TRG_HEAD = ['무엇을', '지금 값', '걸리는 조건', '언제 것', '성격']

# 열쇠 앞머리를 도해 제목으로. 없으면 열쇠를 그대로 쓴다
TITLE = {'sale_idx': '매매가격지수', 'jeonse_idx': '전세가격지수',
         'jeonse_ratio': '전세가율 — 중위 매매가격 대비 전세가격',
         'supply_demand': '매매수급동향 — 100이 균형',
         'median': '서울 중위가격 — 매매와 전세'}

# 한 판에 겹칠 것. 단위가 같아 나란히 놓을 수 있는 짝이다. 판 위의 벌어짐은 차(差)이지
# 전세가율(比)이 아니다 — 전세가율은 따로 판이 있다. 값은 그 짝이 정한 이름으로 구분한다.
GROUP = {'median_sale': ('median', '매매'), 'median_jeonse': ('median', '전세')}


def trg_row(t):
    """트리거 한 줄을 표 행으로. 사건 줄은 어댑터가 안 채우므로 값 자리에 갈래를 적는다 —
    비워 두면 「아직 안 받아 온 값」과 「애초에 값이 아닌 것」이 화면에서 같아 보인다."""
    if t['kind'] == wl.KIND_EVENT:
        return [t['what'], '<i>사건</i>', t['cond'], '—', '사건']
    v = t['value']
    return [t['what'],
            '—' if v is None else str(v),
            t['cond'],
            t['as_of'] or '—',
            t['nature'] or '자리표시']


def figs_of(w):
    """트렌드 도해. 어댑터가 받은 metric 중 series 가 든 것만 그린다 — 어댑터가 붙기
    전에는 아무것도 안 선다(insight-figure 규칙 1을 배선으로 지킨다).

    트리거가 아니라 metric 전부를 본다. 전세지수처럼 트리거는 아니고 맥락으로만
    같이 보는 값이 있어서다.

    같은 단위끼리만 한 판에 둔다. 매매지수와 전세지수를 겹치면 세로 자 하나에 뜻이
    다른 두 값이 서서 어느 쪽이 움직인 건지 안 보인다. 열쇠 앞머리가 묶는 열쇠다 —
    sale_idx_강남구 · sale_idx_서초구 는 한 판, jeonse_idx_* 는 다른 판."""
    groups = {}
    for key, m in sorted((w.get('metrics') or {}).items()):
        if not m.get('series'):
            continue
        # 열쇠를 밑줄로 쪼개 어림하지 않는다 — supply_demand 처럼 밑줄이 든 이름에서
        # 깨진다. 어댑터가 실어 보낸 area 를 떼어 내 묶음 열쇠를 만든다.
        area = m.get('area') or ''
        base = key[:-(len(area) + 1)] if area and key.endswith('_' + area) else key
        # 겹칠 짝이면 판 열쇠를 바꾸고 선 이름도 그 짝이 정한 것으로 쓴다
        gkey, gname = GROUP.get(base, (base, area or base))
        groups.setdefault((gkey, m.get('unit') or ''), []).append((gname, m))
    out = []
    for (base, unit), items in groups.items():
        svg = wf.trend([(n, [tuple(x) for x in m['series']]) for n, m in items[:3]],
                       unit or '값', note=items[0][1].get('src', ''))
        if svg:
            out.append((0, TITLE.get(base, base), svg, items[0][1].get('src', '')))
    return out


def card(w):
    return {
        'section': SECS[w['kind']],
        'topic': ('market', w['topic']),
        'title': '%s — %s' % (w['target'], w['view']) if w.get('view') else w['target'],
        'gain': w['why'],
        'meta': [LABEL[w['kind']],
                 '보기 시작 <b>%s</b>' % w['opened'],
                 '마지막 확인 <b>%s</b>' % w['checked']],
        # 트리거 표가 맨 위다. 워치리스트에서 먼저 알아야 할 것은 근거가 아니라
        # 「지금 조건에 걸렸나」다(설계 §3).
        'lead_table': ('무엇이 일어나면 판단이 바뀌나', TRG_HEAD,
                       [trg_row(t) for t in w['triggers']]),
        'oneliner': w['judged'],
        'points': w['points'],
        'figs': figs_of(w),
        # 반대 근거는 「무엇이 — 왜」로 적혀 있다. 앞머리를 화자 자리에 넣는다.
        'clash': [tuple(c.split(' — ', 1)) if ' — ' in c else ('', c) for c in w['clash']],
    }


WATCHES = wl.load_all()
CARDS = [card(w) for w in WATCHES]
NVAL = sum(1 for w in WATCHES for t in w['triggers'] if t['kind'] == wl.KIND_VALUE)
NFILLED = sum(1 for w in WATCHES for t in w['triggers'] if t['value'] is not None)

HEADER = '''  <header>
    <p class="eyebrow">포트폴리오 — 무엇을 왜 보고 있나</p>
    <h1>포트폴리오 워치</h1>
  </header>'''

LEDE = ('<p class="lede"><b>보유 자산이 아닙니다.</b> 손익·비중·현금흐름은 이 장이 다루지 않습니다. '
        '보고 있는 대상마다 「왜 보나」와 「무엇이 일어나면 판단이 바뀌나」만 세웁니다. '
        '부동산은 <b>권역</b>, 주식은 <b>종목</b>이 한 줄입니다.</p>'
        '<p class="lede">트리거는 갈래가 둘입니다. <b>값</b>은 스크립트가 받아 채우고, '
        '<b>사건</b>은 공표가 날 때 사람이 갱신합니다. 값 트리거 %d개 중 <b>%d개</b>가 채워져 '
        '있습니다 — 성격이 <b>자리표시</b>인 줄은 아직 판단 근거가 아닙니다.</p>' % (NVAL, NFILLED))

META = ('''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>워치 <b>%d줄</b></span>
      <span>트리거 <b>%d개</b></span>
    </div>''' % (STAMP, len(CARDS), sum(len(w['triggers']) for w in WATCHES)))

FOOTER = (LEDE + META + '\n워치 줄은 <code>insights/watch/</code>, 수치는 '
          '<code>insights/watch/_metrics/</code>, 설계는 '
          '<code>docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md</code>, '
          '페이지 생성은 <code>scratchpad/gen_watch_dashboard.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

if __name__ == '__main__':
    dc.render(CARDS, '포트폴리오 워치', HEADER, FOOTER, OUT, page_slug='watch')
