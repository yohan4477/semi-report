# -*- coding: utf-8 -*-
# 언더스탠딩 보고서 — 한두 시간짜리 방송 한 편이 카드 한 장이다.
#
# 다른 장과 다른 것이 하나 있다. 「핵심 포인트·주요 숫자·인용」으로 갈라 쓰지 않고
# 절 제목과 문단이 섞여 흐르는 **보고서**로 쓴다. 긴 방송은 논지가 앞에서 뒤로 굴러가는데,
# 조각으로 갈라 놓으면 「그래서 앞의 것이 뒤에 어떻게 걸리나」가 사라진다.
#
# 카드 목록을 이 파일에 적지 않는다. `content/understanding/언더스탠딩 보고서/*.md`
# 한 편이 카드 한 장이고, 어느 섹션에 설지·주제칩·gain 까지 전부 그 글의 프런트매터에 있다.
# 글을 새로 넣고 이 파일을 다시 돌리면 카드가 는다.
#
# 프런트매터 필수 키
#   title date source speaker org channel dur section topic gain format
#   format 은 report 하나뿐이다 — 이 장은 보고서만 싣는다.
#   section 은 아래 SEC 의 열쇠말 하나다. 없는 열쇠말을 적으면 생성이 멈춘다.
#
# 파서·마크업·CSS는 AI Engineer 장이 갖고 있는 것을 그대로 빌려 쓴다. 두 장이 한 벌로
# 보여야 하고, 보고서 파서를 두 벌 두면 한쪽만 고쳐지는 사고가 난다.
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import gen_aie_dashboard as aie   # noqa: E402  보고서 파서·CSS
import und_figs                   # noqa: E402  본문에 끼우는 도해

OUT = os.path.join(dc.ROOT, '대시보드', '언더스탠딩 보고서 대시보드.html')
SRC_DIR = os.path.join(dc.ROOT, 'content', 'understanding', '언더스탠딩 보고서')
REL = 'content/understanding/언더스탠딩 보고서/%s'

STAMP = '2026-08-26'

# 섹션은 「무엇을 재는 이야기인가」로 나눈다. 출연자로 가르지 않는다 —
# 같은 사람이 금리 이야기도 하고 산업 이야기도 하는데 사람으로 묶으면 그게 한 칸에 뭉친다.
SEC = {
    'macro':  ('sec-macro', '01', '물가 · 금리 · 통화',
               '무엇이 물가를 밀어 올리고, 그것이 금리와 환율을 어디로 미는가'),
    'asset':  ('sec-asset', '02', '자산배분 · 포트폴리오',
               '국면마다 어느 자산이 먼저 움직이나. 무엇을 기준으로 갈아타나'),
    'credit': ('sec-credit', '03', '채권 · 크레딧',
               '만기와 등급을 어떻게 고르나. 값이 어디서 갈리나'),
    'equity': ('sec-equity', '04', '주식 · 밸류에이션',
               '값이 이익에서 오나 배수에서 오나'),
    'geo':    ('sec-geo', '05', '정책 · 지정학',
               '정부와 중앙은행이 무엇을 정했고 그것이 어느 숫자를 움직이나'),
    'industry': ('sec-industry', '06', '산업 · 기업',
                 '한 산업의 병목이 어디에 있고 누가 그 자리를 쥐나'),
}


def build():
    cards, bad = [], []
    if not os.path.isdir(SRC_DIR):
        os.makedirs(SRC_DIR, exist_ok=True)
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(SRC_DIR, fn)
        head_meta, _ = aie.front(io.open(path, encoding='utf-8').read().replace('\r\n', '\n'))
        if head_meta.get('format') != 'report':
            bad.append((fn, 'format이 report가 아니다 — 이 장은 보고서만 싣는다'))
            continue
        vid = aie.vid_of(head_meta.get('source', ''))
        meta, items, verdict = aie.parse_report(path, vid, figs=und_figs.RFIGS)
        why = ('본문 없음' if not items else
               '한줄 코멘트 없음' if not verdict else
               'section 열쇠말이 SEC에 없다: %r' % meta.get('section')
               if meta.get('section') not in SEC else
               'gain 없음' if not meta.get('gain') else '')
        if why:
            bad.append((fn, why))
            continue
        cards.append({
            'section': SEC[meta['section']],
            'topic': ('market', meta.get('topic') or SEC[meta['section']][2]),
            'title': meta.get('title') or fn[:-3],
            'gain': meta['gain'],
            'meta': ['%s <b>%s</b>' % (meta.get('speaker', ''), meta.get('org', '')),
                     '방송 %s' % meta.get('date', ''),
                     aie.dur_ko(meta.get('dur', '')),
                     meta.get('channel', '언더스탠딩')],
            'report': items,
            'verdict': verdict,
            'figs': (),
            'links': [('보고서 전문 ↗', dc.blob(REL % fn), ''),
                      ('방송 영상 ↗', meta.get('source', ''), '')],
            '_date': meta.get('date', ''),
        })
    cards.sort(key=lambda c: c['_date'], reverse=True)
    print('  카드 %d장' % len(cards))
    for fn, why in bad:
        print('  ! 건너뜀 %s — %s' % (fn, why))
    assert cards, '올릴 글이 하나도 없다'
    return cards


INTRO = ('<p>방송 한 편이 카드 한 장입니다. 한두 시간짜리 이야기를 <b>절로 나눈 보고서</b>로 '
         '옮겨 담습니다. 맨 위의 「한줄 코멘트」가 판단이고 그 아래가 거기까지 가는 걸음입니다.</p>'
         '<p>자막 전문에서 옮겼습니다. 숫자는 방송에 나온 것만 싣고, 출연자의 전망과 '
         '이미 벌어진 일은 문장에서 갈라 둡니다. 종목 추천이 아닙니다.</p>')

if __name__ == '__main__':
    CARDS = build()
    HEADER = '''  <header>
    <p class="eyebrow">언더스탠딩 — 장편 방송 보고서</p>
    <h1>언더스탠딩 보고서</h1>
    <p class="lede">한두 시간짜리 방송 한 편을 <b>보고서</b>로 옮겨 담습니다. 무엇을 근거로 그렇게 봤는지가 남습니다.</p>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d편</b></span>
      <span>소스 <b>youtube.com/@understanding.</b></span>
    </div>
  </header>''' % (STAMP, len(CARDS))
    FOOTER = ('언더스탠딩 방송 정리 아카이브 · 원문 영상 링크를 카드마다 답니다. 종목 추천이 아닙니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_undreport_dashboard.py</code>'
              '(공용 부품 <code>dash_common.py</code>, 보고서 파서 <code>gen_aie_dashboard.py</code>).')
    dc.render(CARDS, '언더스탠딩 보고서', HEADER, FOOTER, OUT,
              page_slug='und-report',
              extra_css=aie.POST_CSS, intro=INTRO, newest_first=True)
