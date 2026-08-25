# -*- coding: utf-8 -*-
# AI Engineer 대시보드 — 컨퍼런스 발표 한 편이 카드 한 장이다.
#
# 다른 장과 다른 것이 하나 있다. 카드를 「핵심 포인트 · 주요 숫자 · 인용」으로 갈라 쓰지 않고,
# 메르 블로그처럼 **한 생각에 번호 하나**를 매겨 죽 늘어놓는다. 발표는 논지가 앞에서 뒤로
# 굴러가는 글이라, 조각으로 갈라 놓으면 「그래서 앞의 것이 뒤에 어떻게 걸리나」가 사라진다.
#
# 본문은 이 파일에 적지 않는다. `content/understanding/AI Engineer/*.md` 한 편이 카드 한 장이고,
# 이 파일은 그 글을 어느 섹션에 세우고 접힌 채로 뭐라고 소개할지(gain)만 정한다.
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc

OUT = os.path.join(dc.ROOT, '대시보드', 'AI Engineer 대시보드.html')
SRC_DIR = os.path.join(dc.ROOT, 'content', 'understanding', 'AI Engineer')
REL = 'content/understanding/AI Engineer/%s'

STAMP = '2026-08-26'

SEC_AGENT = ('sec-agent', '01', '에이전트 만들기 · 운영',
             '데모에서 운영으로 넘어갈 때 무엇이 먼저 깨지나. 붙잡는 쪽이 만든 장치들')
SEC_TRAIN = ('sec-train', '02', '모델 훈련 · 후속 학습',
             '배포한 뒤에도 모델이 더 배우게 하려면 무엇을 모아야 하나')
SEC_EVAL = ('sec-eval', '03', '평가 · 결과물 품질',
            '정답이 없는 일을 어떻게 채점하나. 취향을 숫자로 바꾸는 자리')


# 글 한 편이 카드 한 장. body는 md에서 읽는다 — 여기에는 자리와 소개만 적는다.
POSTS = [
    {'file': '2025-04-01-블룸버그-에이전트-확장.md',
     'section': SEC_AGENT,
     'topic': ('market', '에이전트 · 운영'),
     'vid': 'b2GqTDWtg6s'},
    {'file': '2026-07-31-일하면서-배우는-에이전트.md',
     'section': SEC_TRAIN,
     'topic': ('tech', '포스트트레이닝 · 강화학습'),
     'vid': 'k35LeKZEhiE'},
    {'file': '2026-07-31-AI-슬롭을-끝내는-법.md',
     'section': SEC_EVAL,
     'topic': ('tech', '평가 · 보상 모델'),
     'vid': 'lCBf9slCanI'},
]

# 접힌 채로 고르는 기준. 글이 무엇을 알려 주는지를 사람이 쓴다 — 첫 문단을 잘라 쓰지 않는다.
GAIN = {
    'b2GqTDWtg6s': '리서치 애널리스트용 에이전트를 400명·50개 팀이 매일 고쳐 내보내며 겪은 것. '
                   '「최근 5개 분기」에서 글자 하나가 빠져 월간 값이 분기 값으로 나간 사고, 위에서 '
                   '에이전트를 바꾸면 아래가 흔들린다고 미리 가정하고 방어막부터 치는 순서, '
                   '가드레일을 언제 팀마다 두지 말고 수평으로 떼어낼지.',
    'k35LeKZEhiE': '훈련 스택이 쥐고 있던 것을 한 겹씩 바깥으로 내주는 순서. 한 턴짜리 문답에서 '
                   '합성 환경으로, 남의 하니스로, 배포 뒤 자기개선으로 넘어갈 때마다 무엇을 놓고 '
                   '무엇을 얻나. 네트워크 탓에 도구 호출 10%가 실패하자 모델이 답을 점점 짧게 '
                   '내놓은 사례가 왜 리워드 해킹과 같은 문제인지도 나온다.',
    'lCBf9slCanI': '디자인·글쓰기·성격처럼 정답이 없는 일을 채점할 수 있는 것으로 쪼개는 방법. '
                   '수학에서는 여러 답의 평균이 정답에 가까워지는데 취향에서는 그 평균이 슬롭이 되는 '
                   '이유와, 전문가끼리 판단이 갈릴 때 그것을 나쁜 데이터로 버릴지 좋은 데이터로 남길지 '
                   '가르는 기준.',
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
    assert items, '번호글이 하나도 없다: %s' % path
    assert verdict, '한줄 코멘트가 없다: %s' % path
    return meta, items, verdict


def dur_ko(s):
    """길이 표기를 한 벌로 맞춘다 — 「16:30」도 「18분 20초」도 들어온다."""
    m = re.match(r'^(\d+):(\d{2})$', (s or '').strip())
    if not m:
        return s or ''
    mm, ss = int(m.group(1)), int(m.group(2))
    return '%d분 %d초' % (mm, ss) if ss else '%d분' % mm


def build():
    cards = []
    for p in POSTS:
        path = os.path.join(SRC_DIR, p['file'])
        meta, items, verdict = parse(path)
        url = meta.get('source') or ('https://youtu.be/' + p['vid'])
        dur = dur_ko(meta.get('dur', ''))
        cards.append({
            'section': p['section'],
            'topic': p['topic'],
            'title': meta.get('title') or p['file'][:-3],
            'gain': GAIN.get(p['vid'], ''),
            'meta': ['%s <b>%s</b>' % (meta.get('speaker', ''), meta.get('org', '')),
                     '발표 %s' % meta.get('date', ''),
                     dur,
                     meta.get('channel', 'AI Engineer')],
            'post': items,
            'verdict': verdict,
            'links': [('번호글 전문 ↗', dc.blob(REL % p['file']), ''),
                      ('발표 영상 ↗', url, '')],
        })
        print('  %-46s 번호 %2d개' % (p['file'][:46], len(items)))
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
  /* 한줄 코멘트 — 글쓴이의 판단이 한 줄로 서는 자리 */
  .uc-verdict{margin:18px 0 0;padding:13px 15px;border-radius:12px;
              border:1px solid var(--line);background:var(--sunk,rgba(127,127,127,.06));
              font-size:.93rem;line-height:1.65;color:var(--ink)}
  .uc-verdict b{color:var(--ink-3);font-size:.78rem;letter-spacing:.04em;margin-right:6px}
  @media (max-width:520px){
    .uc-post>li{padding-left:30px}
    .uc-post>li::before{width:23px}
  }
'''

INTRO = ('<p>발표 한 편이 카드 한 장입니다. 다른 장과 달리 <b>핵심 포인트로 갈라 쓰지 않고</b> '
         '한 생각에 번호 하나를 매겨 순서대로 늘어놓았습니다 — 발표는 앞의 말이 뒤에 걸리는 '
         '글이라 조각으로 나누면 그 걸림이 사라집니다. 맨 끝의 「한줄 코멘트」가 이 글의 판단입니다.</p>'
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
