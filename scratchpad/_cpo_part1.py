# -*- coding: utf-8 -*-
"""보고서 ⑥ — CPO(공동패키지 광학) 총정리. 본문은 insights/reports/cpo-2026-09-04.md 에서 읽는다.

앞의 층 다섯은 산문을 파이썬 문자열로 들고 있었다. 이 층은 본문을 마크다운 원본에 두고
여기서 HTML 로 바꾼다 — 한국어로 다시 쓰기(확정 규칙 §6 4.5)와 전사 대조가 원본 파일을
문단째 다루기 때문이다. 대시보드 HTML 은 생성물이고 고칠 것은 그 원본이다.

원본 규약
  ## N. 제목          절. 번호는 여기서 다시 센다(목차와 본문이 같은 함수에서 나온다)
  [[fig:이름]]        도해. _cpo_fig 의 FIG_이름 과 아래 CAPTION 의 캡션을 붙인다
  | … |               표 — 첫 줄이 머리, 둘째 줄이 구분선
  (라벨 L12)          출처 표기. 화면에서는 걷는다(확정 규칙 S1)
"""
import io
import os
import re

import _cpo_fig as cf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'cpo-2026-09-04.md')

HEAD_CPO = (
    '<div class="rep-head"><span class="rn">보고서 ⑥</span>'
    '<h2 id="rep-cpo">CPO 총정리 — 빛이 구리를 어디까지 밀어냈고, 누가 그 자리에 서 있나</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 뉴스레터 9편 · Semi Doped 5회차 · 링크드인 게시물</b> · '
    '원문 기간 <b>2025-03 ~ 2026-09</b> · 유료 뉴스레터 원문<br>'
    '광 트랜시버·CPO·OCS 를 다룬 원문을 한데 놓고, 빛이 데이터센터 어디까지 들어왔고 어디서 '
    '막혔는지를 묻습니다. 분량 제한 없이 썼습니다.</p></div>')

# 절 묶음 — 목차를 접는 단위. 절 번호는 원본 순서다.
GROUPS = [('① 왜 빛인가', 1, 4), ('② 어디부터 쓰이나', 5, 9), ('③ 누가 서 있고 무엇이 남았나', 10, 12)]

# 도해 캡션. 값 판단은 캡션에, 판 위에는 대상만(확정 규칙 §3).
CAPTION = {
    'MAP': ('데이터센터 연결 세 층과 구리·광의 경계', cf.FIG_MAP,
            '왼쪽 층일수록 연결 개수가 많고 오른쪽 층일수록 거리가 멉니다. 빛은 오른쪽 두 층에는 '
            '들어와 있고 맨 왼쪽 랙 안에는 아직 없습니다. 이 글은 그 경계가 어디로 움직이는지를 '
            '따라갑니다. 층 셋은 Semi Doped 진행자의 구분이고 값은 없습니다.'),
    'REACH': ('신호 증폭 없는 직결 구리가 닿는 거리', cf.FIG_REACH,
              '글로벌파운드리 Tom Barber 가 든 값입니다(2026-08). 레인 속도가 두 배가 될 때마다 '
              '거리가 반으로 줍니다. SemiAnalysis 는 200G 에서 2m, PicoJool 은 3~4m 라고 했으니 '
              '케이블 종류에 따라 다르지만, 400G 에서 랙 안이 안 닿는다는 결론은 셋이 같습니다.'),
    'LADDER': ('플러거블에서 CPO까지 — 전기 경로가 짧아질수록 손실과 전력이 준다', cf.FIG_LADDER,
               '같은 스위치 칩에서 광엔진까지의 거리만 다릅니다. 손실과 비트당 전력은 Barber 의 값'
               '(2026-08)입니다. 선 길이는 전기가 가야 하는 거리의 순서만 보이고 실제 거리에 비례하지 않습니다.'),
    'MODULE': ('광 트랜시버 한 개를 세 주체가 나눠 만든다', cf.FIG_MODULE,
               '줄마다 같은 모듈을 그렸고 짙은 칸이 그 줄의 회사가 맡는 부품입니다. 반도체는 미국, '
               '레이저는 미국 공장, 조립은 중국계 회사의 중국·태국 공장입니다(Semi Doped 2026-08-11, '
               'SemiAnalysis 2025-04). 광섬유 연결부는 어느 줄도 짙지 않습니다 — 원문이 주체를 안 댔습니다.'),
    'POWER': ('800G 한 개 — 트랜시버와 CPO 광엔진의 전력', cf.FIG_POWER,
              'SemiAnalysis 추정(2026-01)입니다. 800G DSP 트랜시버 한 개는 16~17W, 같은 800G 를 CPO 광엔진과 '
              '외부 레이저로 내면 4~5W 입니다. 막대 높이는 값에 비례하고 범위는 위 끝입니다.'),
    'SHARE': ('광 부품이 차지하는 비중 — 클러스터에서 모듈까지', cf.FIG_SHARE,
              '기둥 하나가 100% 입니다. 클러스터 총비용에서 네트워킹이 15%(옅은 조각)이고, 그 네트워킹 안에서 '
              '트랜시버가 60%(짙은 조각)입니다. 전력도 같은 짝입니다 — 네트워킹 9%, 그 안에서 트랜시버 45%. '
              '짙은 조각의 % 는 옅은 조각 기준이고, 클러스터 대비 몇 % 인지는 원문이 안 적어서 곱하지 않았습니다. '
              '오른쪽 둘은 트랜시버 한 개 안에서 DSP 가 차지하는 것으로, 전력의 약 절반과 자재비의 20~30%'
              '(위 끝 높이)입니다. 전부 SemiAnalysis 추정(2026-01, GB300 NVL72 3층망 기준)입니다.'),
    'COST': ('광 부품값은 절반인데 클러스터 총비용은 3~7%만 준다', cf.FIG_COST,
             'SemiAnalysis 추정(2026-01)입니다. 왼쪽은 Q3450 급 스위치 한 대에 드는 광 부품값으로, '
             '트랜시버로 채우면 7만 2천 달러, CPO 광엔진 원가는 3만 5천~4만 달러인데 스위치 회사가 '
             '60% 마진을 얹으면 8만~9만 달러가 됩니다(점선). 범위 값은 위 끝 높이로 그렸습니다. '
             '오른쪽은 클러스터 총비용 기준 절감폭입니다.'),
    'RACK': ('루빈 울트라 NVL576 랙 지출 — HBM 을 깎자 스케일업 네트워킹이 세 배', cf.FIG_RACK,
             'SemiAnalysis 링크드인 게시물(2026-09-02)의 값입니다. 엔비디아가 루빈 울트라의 HBM 을 HBM4E 12단에서 '
             'HBM4 8단으로 깎자 랙 지출에서 메모리는 40% 에서 28% 로 내려가고 스케일업 네트워킹(NVL576 NPO 구성)은 '
             '4% 에서 12% 로 오릅니다. 두 조각 밖의 나머지는 원문이 안 나눠 비워 뒀습니다.'),
    'ROADMAP': ('엔비디아 스케일업 — 어디까지 구리인가', cf.FIG_ROADMAP,
                'GTC 2026 에서 확인된 로드맵(2026-03)과 그 뒤 연기 소식(2026-07)입니다. 랙 안은 세 세대 '
                '내내 구리이고 CPO 는 랙과 랙 사이에만 들어옵니다. 파인만 랙 안이 구리인지는 엔비디아 '
                '기술 블로그와 젠슨 황의 말이 갈려 물음표로 뒀습니다. 카이버 NVL144 는 2028년으로 밀렸고 '
                'CPO NVSwitch 는 파인만까지 없습니다.'),
    'THREE': ('랙 하나를 넘는 스케일업 — 세 회사의 세 답', cf.FIG_THREE,
              '엔비디아는 랙 하나 안에서 구리로 끝내고, 화웨이는 트랜시버를 6,912개 넣어 랙 16개를 묶고, '
              '구글은 큐브 64개 안은 구리·경계는 광과 OCS 로 9,216개까지 갑니다. 전력 두 값은 단위가 '
              '다릅니다(랙 대 슈퍼노드). 칩 수도 다릅니다. SemiAnalysis 2025-04 · 2025-11 값입니다.'),
    'CHAIN': ('엔비디아 CPO 공급망 다섯 단계 — 단계마다 이미 소수다', cf.FIG_CHAIN,
              'SemiAnalysis 가 세운 다섯 단계(2026-01)를 끝에서 끝까지 그렸습니다. 상자 안 이름은 원문이 '
              '유력 공급사로 적은 곳만이고 순서는 원문 그대로입니다. 짙은 칸이 FAU 인 것은 이 글의 '
              '판단입니다 — 검사가 가닥당 10~15분 수작업이라 가장 막힌 자리입니다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\bL\d[^()]*)\)')


def _strip(s):
    """(라벨 L12) 를 걷고 마크다운 굵게를 <b> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
         '<caption>값은 그 회사가 공표했거나 SemiAnalysis 가 적은 것이고, 빈칸은 원문에 없는 자리입니다. '
         '「언제 것」은 원문 발행일이며 「회사 주장」은 그 회사 사람이 말한 값입니다.</caption>',
         '<thead><tr>' + ''.join('<th>%s</th>' % _strip(c) for c in head) + '</tr></thead><tbody>']
    for r in body:
        h.append('<tr>' + ''.join('<td>%s</td>' % _strip(c) for c in r) + '</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def load():
    """원본을 (kind, payload) 목록으로. kind ∈ lead·sec·p·fig·table."""
    txt = io.open(SRC, encoding='utf-8').read()
    if txt.startswith('---'):
        txt = txt.split('---', 2)[2]
    out, para, tbl = [], [], []

    def flush():
        if para:
            out.append(('p', ' '.join(para)))
            para.clear()
        if tbl:
            out.append(('table', list(tbl)))
            tbl.clear()

    for line in txt.split('\n'):
        s = line.rstrip()
        if s.startswith('## '):
            flush()
            out.append(('sec', re.sub(r'^\d+\.\s*', '', s[3:]).strip()))
        elif s.startswith('[[fig:'):
            flush()
            out.append(('fig', s[6:].rstrip(']').strip()))
        elif s.startswith('|'):
            if para:
                flush()
            tbl.append(s)
        elif not s:
            flush()
        elif s.startswith('#'):
            continue
        else:
            para.append(s.strip())
    flush()
    return out


def toc_html(titles):
    parts = ['<p class="rep-toc"><b>이 층은 물음 하나를 세 묶음으로 따라갑니다 — '
             '왜 빛인가, 어디부터 쓰이나, 누가 서 있고 무엇이 남았나.</b><br>']
    for name, a, b in GROUPS:
        links = ' · '.join('<a href="#cpo-%d">%d %s</a>' % (i, i, titles[i - 1]) for i in range(a, b + 1))
        parts.append('<b>%s</b> %s<br>' % (name, links))
    parts[-1] = parts[-1][:-4]
    return ''.join(parts) + '</p>'


def report_cpo(sec, p, fig):
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig') and not toc_done:
            p(toc_html(titles))
            toc_done = True
        if k == 'sec':
            sec('%d. %s' % (titles.index(v) + 1, v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'table':
            p(_table(v))
    return titles
