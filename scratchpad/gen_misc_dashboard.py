# -*- coding: utf-8 -*-
# 기타 대시보드 — 다른 장에 자리가 없는 원문을 싣는 곳. 첫 재료는 JAX 스케일링 북
# (How To Scale Your Model, jax-ml.github.io/scaling-book) 열세 장이다.
#
# 카드 한 장 = 원문 한 장. 언더스탠딩 보고서 장과 같은 **보고서 형식**으로 쓴다 —
# 교재는 절이 앞에서 뒤로 굴러가므로 「핵심 포인트·숫자」로 가르면 순서가 사라진다.
# 파서·마크업·CSS는 AI Engineer 장 것을 빌려 쓴다(보고서 파서를 두 벌 두지 않는다).
#
# 카드 목록은 이 파일에 없다. `content/scaling-book/*.md` 한 편이 카드 한 장이고
# 섹션·주제칩·gain 은 그 글의 프런트매터에 있다. 도해는 `scratchpad/sb_figs/<slug>.py`
# 의 FIGS 사전에서 온다 — 파일 하나가 장 하나라 여럿이 동시에 써도 안 부딪친다.
#
# 다른 원문(책·긴 문서)을 이 장에 더 실을 때는 content/<이름>/ 폴더를 SOURCES 에 한 줄
# 더하고, 섹션 열쇠말을 SEC 에 세운다. 교재 순서로 읽는 장이라 newest_first 는 끈다.
import importlib
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import gen_aie_dashboard as aie   # noqa: E402  보고서 파서·CSS

OUT = os.path.join(dc.ROOT, '대시보드', '기타 대시보드.html')
STAMP = '2026-09-03'

# (content 아래 폴더, 도해 패키지, 원문 라벨)
SOURCES = [('scaling-book', 'sb_figs', 'How To Scale Your Model')]

# 섹션은 책의 읽는 순서다. 다른 원문이 들어오면 그 원문의 갈래를 아래에 잇는다.
SEC = {
    'basics':   ('sec-basics', '01', '하드웨어와 루프라인',
                 '연산·메모리·통신 셋 중 무엇이 시간을 먹나. TPU·GPU가 각각 어떻게 생겼나'),
    'parallel': ('sec-parallel', '02', '샤딩과 트랜스포머 계산',
                 '행렬을 칩 여럿에 어떻게 자르나. 트랜스포머 한 층이 FLOPs와 바이트를 얼마나 쓰나'),
    'train':    ('sec-train', '03', '학습 병렬화',
                 '데이터·텐서·파이프라인·전문가 병렬을 언제 섞나. LLaMA 3를 TPU에서 굴리면'),
    'infer':    ('sec-infer', '04', '추론과 서빙',
                 '프리필과 디코드가 왜 다르게 묶이나. KV 캐시가 어디까지 커지나'),
    'tools':    ('sec-tools', '05', '프로파일링 · JAX · 맺음',
                 '어디서 시간이 새는지 보는 법, JAX로 샤딩을 적는 법, 책이 남긴 것'),
}


def load_figs(pkg, slug):
    """scratchpad/<pkg>/<slug>.py 의 FIGS. 파일이 없으면 빈 사전 — 도해 없는 장도 선다."""
    mod = '%s.%s' % (pkg, slug.replace('-', '_'))
    try:
        m = importlib.import_module(mod)
    except ModuleNotFoundError as e:
        if e.name and e.name.endswith(slug.replace('-', '_')):
            return {}
        raise
    return dict(m.FIGS)


def build():
    cards, bad = [], []
    for folder, pkg, label in SOURCES:
        src_dir = os.path.join(dc.ROOT, 'content', folder)
        rel = 'content/%s/%%s' % folder
        for fn in sorted(os.listdir(src_dir)):
            if not fn.endswith('.md'):
                continue
            path = os.path.join(src_dir, fn)
            head_meta, _ = aie.front(io.open(path, encoding='utf-8').read().replace('\r\n', '\n'))
            if head_meta.get('format') != 'report':
                bad.append((fn, 'format이 report가 아니다'))
                continue
            slug = head_meta.get('slug') or fn[3:-3]
            figs = {slug: load_figs(pkg, slug)}
            meta, items, verdict = aie.parse_report(path, slug, figs=figs)
            why = ('본문 없음' if not items else
                   '한줄 코멘트 없음' if not verdict else
                   'section 열쇠말이 SEC에 없다: %r' % meta.get('section')
                   if meta.get('section') not in SEC else
                   'gain 없음' if not meta.get('gain') else
                   '도해 없음' if not any(k == 'fig' for k, _ in items) else '')
            if why:
                bad.append((fn, why))
                continue
            part = int(meta.get('part', '0'))
            cards.append({
                'section': SEC[meta['section']],
                'topic': ('market', meta.get('topic') or SEC[meta['section']][2]),
                'title': meta.get('title') or fn[:-3],
                'gain': meta['gain'],
                'meta': ['%s <b>Part %d</b>' % (label, part),
                         '발행 %s' % meta.get('date', ''),
                         'Google DeepMind · 제이컵 오스틴 외'],
                'report': items,
                'verdict': verdict,
                'figs': (),
                'links': [('한국어 정리 전문 ↗', dc.blob(rel % fn), ''),
                          ('원문 (영문) ↗', meta.get('source', ''), '')],
                '_order': part,
            })
    cards.sort(key=lambda c: c['_order'])
    print('  카드 %d장' % len(cards))
    for fn, why in bad:
        print('  ! 건너뜀 %s — %s' % (fn, why))
    assert cards, '올릴 글이 하나도 없다'
    return cards


INTRO_T = ('<p>다른 장에 자리가 없는 원문을 싣는 곳입니다. 지금은 구글 딥마인드 팀이 쓴 '
         '<b>How To Scale Your Model</b>(JAX 스케일링 북) 열세 장 중 %d장이 서 있습니다. '
         '원문 한 장이 카드 한 장이고, 책의 순서대로 서 있습니다 — 1부 루프라인부터 읽으면 '
         '뒤 장의 수식이 따라옵니다.</p>'
         '<p>맨 위 「한줄 코멘트」가 판단이고 그 아래가 거기까지 가는 걸음입니다. 숫자는 '
         '책에 적힌 것만 싣고, 칩 사양은 책이 인용한 공표치입니다.</p>')

if __name__ == '__main__':
    CARDS = build()
    INTRO = INTRO_T % len(CARDS)
    HEADER = '''  <header>
    <p class="eyebrow">기타 — 다른 장에 자리가 없는 원문</p>
    <h1>기타 대시보드</h1>
    <p class="lede">긴 원문 한 편을 장마다 <b>보고서</b>로 옮겨 담습니다. 지금은 JAX 스케일링 북 열세 장 중 %d장입니다.</p>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d편</b></span>
      <span>소스 <b>jax-ml.github.io/scaling-book</b></span>
    </div>
  </header>''' % (len(CARDS), STAMP, len(CARDS))
    FOOTER = ('원문은 공개 저장소(MIT)에 올라 있는 책입니다. 카드마다 원문 링크를 답니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_misc_dashboard.py</code>'
              '(공용 부품 <code>dash_common.py</code>, 보고서 파서 <code>gen_aie_dashboard.py</code>).')
    dc.render(CARDS, '기타 대시보드', HEADER, FOOTER, OUT,
              page_slug='misc',
              extra_css=aie.POST_CSS, intro=INTRO, newest_first=False)
