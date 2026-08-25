# -*- coding: utf-8 -*-
# AI Engineer 대시보드 — 컨퍼런스 발표 한 편이 카드 한 장이다.
#
# 다른 장과 다른 것이 하나 있다. 카드를 「핵심 포인트 · 주요 숫자 · 인용」으로 갈라 쓰지 않고,
# 메르 블로그처럼 **한 생각에 번호 하나**를 매겨 죽 늘어놓는다. 발표는 논지가 앞에서 뒤로
# 굴러가는 글이라, 조각으로 갈라 놓으면 「그래서 앞의 것이 뒤에 어떻게 걸리나」가 사라진다.
#
# 카드 목록을 이 파일에 적지 않는다. `content/understanding/AI Engineer/*.md` 한 편이
# 카드 한 장이고, 어느 섹션에 설지·주제칩·gain 까지 전부 그 글의 프런트매터에 있다.
# 글을 새로 넣고 이 파일을 다시 돌리면 카드가 는다.
#
# 프런트매터 필수 키
#   title date source speaker org channel dur section topic gain
#   section 은 아래 SEC 의 열쇠말 하나다. 없는 열쇠말을 적으면 생성이 멈춘다.
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import aie_figs                 # noqa: E402  번호글에 끼우는 도해

OUT = os.path.join(dc.ROOT, '대시보드', 'AI Engineer 대시보드.html')
SRC_DIR = os.path.join(dc.ROOT, 'content', 'understanding', 'AI Engineer')
REL = 'content/understanding/AI Engineer/%s'

STAMP = '2026-08-26'

# 섹션은 「무엇을 만드는 이야기인가」로 가른다. 회사로 가르지 않는다 —
# 같은 회사가 훈련 이야기도 하고 제품 이야기도 하는데 회사로 묶으면 그게 한 칸에 뭉친다.
SEC = {
    'agent':   ('sec-agent', '01', '에이전트 만들기 · 운영',
                '데모에서 운영으로 넘어갈 때 무엇이 먼저 깨지나. 붙잡는 쪽이 만든 장치들'),
    'code':    ('sec-code', '02', '코딩 에이전트 · 개발 도구',
                '코드를 대신 쓰는 쪽이 무엇에서 막히나. 사람이 어디까지 쥐고 있어야 하나'),
    'rag':     ('sec-rag', '03', '검색 · 컨텍스트 · 기억',
                '모델에 무엇을 얼마나 넣어 주나. 찾아오는 일과 기억하는 일이 갈리는 자리'),
    'train':   ('sec-train', '04', '모델 훈련 · 후속 학습',
                '배포한 뒤에도 모델이 더 배우게 하려면 무엇을 모아야 하나'),
    'eval':    ('sec-eval', '05', '평가 · 결과물 품질',
                '정답이 없는 일을 어떻게 채점하나. 취향을 숫자로 바꾸는 자리'),
    'infra':   ('sec-infra', '06', '서빙 · 비용 · 인프라',
                '토큰을 싸게 많이 내보내는 일. 지연과 값이 부딪히는 자리'),
    'voice':   ('sec-voice', '07', '음성 · 멀티모달',
                '말로 주고받는 것이 글로 주고받는 것과 어디서 갈리나'),
    'product': ('sec-product', '08', '제품 · 조직 · 도입',
                '만든 것을 회사 안에 어떻게 들이나. 조직이 먼저 바뀌는 대목'),
}

VERDICT_RE = re.compile(r'^한줄\s*코멘트[.,]?\s*(.+)$')
NUM_RE = re.compile(r'^(\d{1,3})\.\s+(.*)$')


def front(text):
    """맨 위 YAML 프런트매터를 얕게 읽는다. 값은 전부 문자열로 본다."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end < 0:
        return {}, text
    head, body = text[3:end], text[end + 4:]
    meta = {}
    for line in head.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body.lstrip('\n')


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def dur_ko(s):
    """길이 표기를 한 벌로 맞춘다 — 「16:30」도 「18분 20초」도 들어온다."""
    m = re.match(r'^(\d+):(\d{2})$', (s or '').strip())
    if not m:
        return s or ''
    mm, ss = int(m.group(1)), int(m.group(2))
    return '%d분 %d초' % (mm, ss) if ss else '%d분' % mm


def parse(path):
    """번호글 md 한 편 → (프런트매터, 번호글 목록, 한줄 코멘트)."""
    raw = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    meta, body = front(raw)
    items, verdict, expect = [], '', 1
    for para in re.split(r'\n\s*\n', body):
        t = ' '.join(para.split()).strip()
        if not t:
            continue
        m = VERDICT_RE.match(t)
        if m:
            verdict = esc(m.group(1))
            continue
        m = NUM_RE.match(t)
        if not m:
            continue
        n = int(m.group(1))
        # 번호가 튀면 사람이 봐야 한다 — 화면에서는 순서대로 다시 매겨지므로 조용히 어긋난다
        if n != expect:
            print('  ! %s 번호가 %d에서 %d로 튄다' % (os.path.basename(path), expect, n))
            expect = n
        items.append(esc(m.group(2)))
        expect += 1
    return meta, items, verdict


H_RE = re.compile(r'^##\s+(.*)$')
FIG_RE = re.compile(r'^\[\[fig:([a-z0-9_-]+)\]\]$')
BOLD_RE = re.compile(r'\*\*(.+?)\*\*')


def parse_report(path, vid):
    """보고서 형식 md 한 편 → (프런트매터, 블록 목록, 한줄 코멘트).

    번호글과 달리 절 제목(`## `)·문단·그림 부름(`[[fig:이름]]`)이 섞여 흐른다.
    그림은 `aie_figs.RFIGS[영상ID][이름]`에서 꺼낸다 — 이름이 없으면 생성을 멈춘다.
    """
    raw = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    meta, body = front(raw)
    have = aie_figs.RFIGS.get(vid, {})
    blocks, verdict, used = [], '', set()
    for para in re.split(r'\n\s*\n', body):
        t = ' '.join(para.split()).strip()
        if not t:
            continue
        m = VERDICT_RE.match(t)
        if m:
            verdict = esc(m.group(1))
            continue
        m = H_RE.match(t)
        if m:
            blocks.append(('h', esc(m.group(1))))
            continue
        m = FIG_RE.match(t)
        if m:
            key = m.group(1)
            assert key in have, '%s — 그림 %r가 aie_figs.RFIGS에 없다' % (os.path.basename(path), key)
            blocks.append(('fig', have[key]))
            used.add(key)
            continue
        blocks.append(('p', BOLD_RE.sub(r'<b>\1</b>', esc(t))))
    for key in sorted(set(have) - used):
        print('  ! %s — 그림 %r를 본문에서 안 부른다' % (os.path.basename(path), key))
    return meta, blocks, verdict


def vid_of(url):
    return (url or '').rsplit('/', 1)[-1].split('?')[0]


def build():
    cards, bad = [], []
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(SRC_DIR, fn)
        # 형식이 둘이다. 논지가 앞뒤로 걸리는 발표는 번호글로, 구조를 설명하는
        # 발표는 그림을 앞세운 보고서로 간다. 어느 쪽인지는 프런트매터가 정한다.
        head_meta, _ = front(io.open(path, encoding='utf-8').read().replace('\r\n', '\n'))
        is_report = head_meta.get('format') == 'report'
        if is_report:
            meta, items, verdict = parse_report(path, vid_of(head_meta.get('source', '')))
        else:
            meta, items, verdict = parse(path)
        # 덜 된 글은 화면에 올리지 않는다 — 번호글이나 한줄 코멘트가 비면 건너뛰고 적어 둔다
        why = (('본문 없음' if is_report else '번호글 없음') if not items else
               '한줄 코멘트 없음' if not verdict else
               'section 열쇠말이 SEC에 없다: %r' % meta.get('section') if meta.get('section') not in SEC else
               'gain 없음' if not meta.get('gain') else '')
        if why:
            bad.append((fn, why))
            continue
        cards.append({
            'section': SEC[meta['section']],
            'topic': ('market' if meta['section'] in ('product', 'infra') else 'tech',
                      meta.get('topic') or SEC[meta['section']][2]),
            'title': meta.get('title') or fn[:-3],
            'gain': meta['gain'],
            'meta': ['%s <b>%s</b>' % (meta.get('speaker', ''), meta.get('org', '')),
                     '발표 %s' % meta.get('date', ''),
                     dur_ko(meta.get('dur', '')),
                     meta.get('channel', 'AI Engineer')],
            ('report' if is_report else 'post'): items,
            'verdict': verdict,
            # 번호글은 한 줄에 한 생각이라 전체가 어떻게 맞물리는지가 안 잡힌다.
            # 그 한 장을 aie_figs가 갖고 있고 영상 ID로 붙인다.
            'figs': () if is_report else aie_figs.FIGS.get(vid_of(meta.get('source', '')), ()),
            'links': [('번호글 전문 ↗', dc.blob(REL % fn), ''),
                      ('발표 영상 ↗', meta.get('source', ''), '')],
            '_date': meta.get('date', ''),
        })
    cards.sort(key=lambda c: c['_date'], reverse=True)
    print('  카드 %d장' % len(cards))
    for fn, why in bad:
        print('  ! 건너뜀 %s — %s' % (fn, why))
    assert cards, '올릴 글이 하나도 없다'
    return cards


# 번호글 전용 CSS. 카드 본문 안에서만 쓰는 규칙이라 이 장에서만 붙인다.
POST_CSS = '''
  /* 번호글 — 한 생각에 번호 하나. 번호를 왼쪽에 떼어 놓고 글을 들여 쓴다 */
  .uc-post{list-style:none;margin:14px 0 0;padding:0;counter-reset:mp}
  .uc-post>li{counter-increment:mp;position:relative;padding:0 0 0 38px;margin:0 0 13px;
              font-size:.95rem;line-height:1.72;color:var(--ink-2)}
  .uc-post>li::before{content:counter(mp) ".";position:absolute;left:0;top:0;
              width:30px;text-align:right;font-variant-numeric:tabular-nums;
              font-weight:800;font-size:.82rem;line-height:1.98;color:var(--ink-3)}
  .uc-post>li:last-child{margin-bottom:0}
  /* 한줄 코멘트 — 글쓴이의 판단이 한 줄로 서는 자리. 번호글 위에 선다 */
  .uc-verdict{margin:14px 0 4px;padding:13px 15px;border-radius:12px;
              border:1px solid var(--line);background:var(--sunk,rgba(127,127,127,.06));
              font-size:.93rem;line-height:1.65;color:var(--ink)}
  .uc-verdict b{color:var(--ink-3);font-size:.78rem;letter-spacing:.04em;margin-right:6px}
  @media (max-width:520px){
    .uc-post>li{padding-left:30px}
    .uc-post>li::before{width:23px}
  }
  /* 보고서 — 절 제목과 문단이 섞여 흐른다. 번호글과 같은 카드 안에서 쓴다 */
  .uc-rep{margin:14px 0 0}
  .uc-rep h3{margin:26px 0 10px;font-size:1.02rem;line-height:1.45;font-weight:800;
             color:var(--ink);letter-spacing:-.01em}
  .uc-rep h3:first-child{margin-top:4px}
  .uc-rep p{margin:0 0 13px;font-size:.95rem;line-height:1.78;color:var(--ink-2)}
  .uc-rep p:last-child{margin-bottom:0}
  .uc-rep .uc-fig{margin:18px 0}
''' + aie_figs.FIG_CSS

INTRO = ('<p>발표 한 편이 카드 한 장입니다. 글의 형식은 둘입니다. 논지가 앞의 말에서 뒤의 말로 '
         '굴러가는 발표는 <b>한 생각에 번호 하나</b>를 매겨 늘어놓고, 구조를 설명하는 발표는 '
         '<b>그림을 앞세운 보고서</b>로 씁니다. 어느 쪽이든 맨 위의 「한줄 코멘트」가 판단이고 '
         '그 아래가 거기까지 가는 걸음입니다.</p>'
         '<p>자막 전문에서 옮겼고, 발표자가 자기 회사를 파는 대목은 그렇다고 밝혀 두었습니다. '
         '숫자는 발표에 나온 것만 싣습니다.</p>')

if __name__ == '__main__':
    CARDS = build()
    HEADER = '''  <header>
    <p class="eyebrow">AI Engineer — 컨퍼런스 발표 아카이브</p>
    <h1>AI Engineer</h1>
    <p class="lede">에이전트를 실제로 굴려 본 사람들이 무엇에서 막혔고 무엇으로 뚫었는지. 발표 한 편을 <b>번호글</b>로 옮겨 담습니다.</p>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d편</b></span>
      <span>소스 <b>youtube.com/@aidotengineer</b></span>
    </div>
  </header>''' % (STAMP, len(CARDS))
    FOOTER = ('AI Engineer 컨퍼런스 발표 번역·정리 아카이브 · 원문 영상 링크를 카드마다 답니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_aie_dashboard.py</code>'
              '(공용 부품 <code>dash_common.py</code>).')
    dc.render(CARDS, 'AI Engineer', HEADER, FOOTER, OUT,
              extra_css=POST_CSS, intro=INTRO, newest_first=True)
