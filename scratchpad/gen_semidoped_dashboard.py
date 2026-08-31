# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — 회차 하나를 여러 눈으로 설명하게 하고 그대로 싣는다.

카드 한 장이 「회차 × 뷰」다. 본문은 우리가 쓴 글이 아니라 다른 모델(Gemini)
에게 물어 받은 답이고, 문장을 고치지 않는다. 원본은 insights/frames/ 에 있다.

  물어 오기   py -3.13 scripts/gem_views.py <원문 md> <회차 링크>
  대조        py -3.13 insights/check_frame.py
  이 화면     py -3.13 scratchpad/gen_semidoped_dashboard.py

이 장은 구조 게이트에서 뺐다(check_struct STRICT · check_fig STRICT_FIG). 받은 글에
우리 규칙(앞머리·목차·물음 절·성격 열)을 댈 자리가 아니다 — 규칙을 지운 것이 아니라
연결을 끊은 것이다.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))

import dash_common as dc  # noqa: E402
import frame_view  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', 'Semi Doped 대시보드.html')
SRC = 'content/understanding/Semi Doped/'
BLOB = 'https://github.com/johnn8n/semianalysis/blob/main/'


def blob(p):
    return BLOB + p.replace(' ', '%20')


# 회차 하나에 뷰 둘. 뷰마다 카드 한 장이고, 본문은 받은 답을 그대로 싣는다
EPISODES = [
    # 제목은 우리가 새로 짓지 않는다. 그 회차가 달고 나온 이름을 한국어로 옮기고,
    # 원제는 메타 줄에 그대로 남긴다
    ('2026-08-27-openai-jalapeno', '오픈AI 의 할라페뇨라는 느낌',
     "OpenAI's Jalapeño Feeling", '2026-08-27',
     'https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling'),
    ('2026-08-24-grok-bots-cpu', 'Grok 봇과 에이전틱 AI 에서 CPU 가 쓰이는 방식',
     'Grok Bots and How CPUs are used in Agentic AI', '2026-08-24',
     'https://daily.semidoped.com/p/new-episode-grok-bots-and-how-cpus'),
]

# 섹션이 회차다. 회차 제목 아래 뷰 카드 둘이 나란히 선다.
#
# 통합 뷰는 아예 안 묻는다 — 2026-08-31 에 할라페뇨 세 뷰를 대조해 보니 통합 뷰가
# 혼자 가진 대목이 하나도 없었다. 절 아홉 중 여섯이 세 뷰에 다 있었고(설계 철학·NUMA
# 로컬 HBM·다크 실리콘·9개월 테이프아웃·범용 벤치마크·SRAM 영역 침투), 전략 뷰의 제언과
# 통합 뷰의 제언은 관전 포인트 둘이 같은 말이었다.
# 카드 이름은 누가 본 것인지로 단다 — 「전략 뷰」는 무엇을 담았는지 안 말한다
VIEWS = [
    ('strategy', '경영전략 컨설턴트 검토', '시니어 경영전략 컨설턴트에게 물었다'),
    ('tech', '업계 기술 전문가 검토', '시니어 업계 기술 전문가에게 물었다'),
]


import re  # noqa: E402


def _paras(md):
    return [t.strip() for t in md.split(chr(10) * 2) if t.strip()]


def _first_prose(md):
    """제목·표·도식을 건너뛴 첫 줄글 한 도막. 카드 앞면에 세울 자리다."""
    for t in _paras(md):
        for ln in t.split(chr(10)):
            # 목록 표시만 걷는다. 굵은 글씨(**핵심 요약:**)의 별표까지 걷으면 짝이 깨져
            # 앞면에 별표가 그대로 남는다
            ln = re.sub(r'^\s*[-*]\s+', '', ln.strip())
            if ln.startswith(('#', '|', '`', '>')):
                continue
            if len(re.findall(r'[가-힣]', ln)) >= 20:
                return ln
    return ''


def plain(md):
    """문단 하나를 카드 앞면에 세울 줄글로. 굵은 글씨 표시만 걷고 글자는 그대로 둔다.

    frame_view.lead_of 는 굵은 글씨로 시작하는 줄을 통째로 건너뛴다 — 「**요약하자면,**」
    으로 시작하는 문단이 앞면에서 통째로 사라진다.
    """
    lines = []
    for ln in md.split(chr(10)):
        t = ln.strip()
        # 제목 노릇만 하는 굵은 글씨 한 줄(**[요약 및 컨설턴트 제언]**)은 앞면에 안 세운다
        if t.startswith('**') and t.endswith('**') and len(t) < 44:
            continue
        lines.append(t)
    t = ' '.join(lines)
    t = re.sub(r'\*\*(.+?)\*\*', r'\g<1>', t).replace('`', '')
    return re.sub(r'\s+', ' ', t).strip()


def head_html(date, en_title):
    """섹션 머리 아래 한 줄 — 회차에 붙는 것은 여기 한 번만 선다.

    진행자·업로드 날짜·원제는 뷰가 달라도 같은 값이다. 카드마다 달면 같은 줄이 넷이 된다.
    앞머리 상자는 없앴다 — 통합 뷰를 걷으면서 그 글이 사라졌고, 전략·기술 뷰는 저마다
    자기 앞머리를 카드 안에 그대로 갖고 있다.
    """
    meta = ['Austin · Vik Sekar <b>Semi Doped 공동 진행</b>',
            '업로드 %s' % date, '원제 %s' % en_title]
    return '<p class="sd-meta">%s</p>' % ' · '.join(meta)


def make_card(slug, ep_title, en_title, date, url, kind, view_title, asked, num,
              path=None, tag=''):
    """뷰 하나가 카드 한 장이다. 회차 하나에 카드 둘이 한 섹션에 선다.

    받은 글을 상자에 나눠 담지 않는다 — 카드 안에 상자를 하나 더 그리면 쓸 폭이 줄고
    카드 속 카드처럼 읽힌다. 몸은 한 덩어리로 흐르고, 앞면에 세울 첫 줄글만 위로 뽑는다.
    """
    path = path or os.path.join(ROOT, 'insights', 'frames', '%s-%s.md' % (slug, kind))
    md = frame_view.body_of(path)
    front = _first_prose(md)
    rp = _paras(md)
    # 앞면에 세운 줄글은 몸에서 걷는다. 맨 앞 두 문단 안에 있을 때만 — 제목 아래 문단을
    # 빼면 그 제목이 자기 글을 잃는다. 굵은 글씨 제목 한 줄(**…요약**)이 먼저 서고 그
    # 다음 문단이 줄글인 판이 많아 첫 문단만 보면 못 걷는다
    cut = None
    for i, para in enumerate(rp[:2]):
        if front and plain(front) in plain(para) and not para.lstrip().startswith('#'):
            cut = i
            break
    # 걷은 문단 자리만 원문에서 도려낸다. 문단으로 쪼갰다 다시 이으면 조각마다 strip 이
    # 걸려 **도식 줄의 들여쓰기가 사라진다** — 칸 정렬이 무너져 표가 표로 안 읽힌다
    # (2026-08-31 「폐쇄형 대 개방형」 표가 그렇게 아스키로 떨어졌다)
    rest = md
    if cut is not None:
        at = md.find(rp[cut])
        if at >= 0:
            rest = (md[:at] + md[at + len(rp[cut]):]).strip()
    return {
        'id': 'sd-%s-%s%s' % (slug, kind, '-' + tag.split()[0].lower() if tag else ''),
        'section': ('sd-%s' % slug, num, ep_title,
                    '한 회차를 눈을 바꿔 설명하게 하고 받은 글을 그대로 싣는다'),
        # 제목에 회차를 다시 안 적는다 — 섹션 머리가 바로 위에서 그 말을 한다.
        # 대신 앵커를 따로 준다. 이름이 짧아 다른 회차 카드와 겹친다
        # 같은 회차에 모델이 둘이면 제목에 모델 이름만 붙여 가른다
        'title': '%s — %s' % (view_title, tag) if tag else view_title,
        'anchor': 'sd-%s-%s%s' % (slug, kind, '-' + tag.split()[0].lower() if tag else ''),
        'gain': plain(front)[:150],
        # 회차에 붙는 줄(진행자·업로드·원제)은 섹션 머리 아래에 한 번 선다. 카드에 남는
        # 것은 뷰마다 다른 것 — 어느 모델이 썼나. 「받은 그대로 · 미검증」은 그 줄에 붙여
        # 카드 안에 남긴다. 이 카드 본문이 인용이라는 표이고, check_frame 이 그 표로
        # 인용 카드를 유출 검사에서 뺀다 — 카드 밖으로 옮기면 인용이 유출로 잡힌다
        'meta': ['모델 %s · 받은 그대로 · 미검증' % frame_view.model_of(path)],
        'links': [('요약본', blob(SRC + '%s.md' % slug), ''),
                  ('원문(Semi Doped)', url, 'ghost')],
        # 앞면에 세운 문단을 한줄 코멘트로 또 세우지 않는다
        'verdict': '',
        'report': [('raw', '<div class="fv-b">%s</div>' % frame_view.to_html(rest))],
    }


# 회차를 바깥 고리로 돈다 — 한 회차의 뷰 둘이 한 섹션에 모인다
CARDS = [make_card(slug, t, en, d, u, kind, vt, asked, '%02d' % (i + 1),
                   tag='Gemini 3.1 Pro')
         for i, (slug, t, en, d, u) in enumerate(EPISODES)
         for kind, vt, asked in VIEWS]

# 같은 프롬프트를 다른 모델에 넣어 본 답도 같은 섹션에 세운다. 가르는 것은 제목의
# 모델 이름뿐이다 — 무엇이 달라지는지는 나란히 놓고 읽어야 보인다(2026-08-31 실험)
EXP = os.path.join(ROOT, 'insights', 'frames', 'exp')
for i, (slug, t, en, d, u) in enumerate(EPISODES):
    for kind, vt, asked in VIEWS:
        f = os.path.join(EXP, '%s-%s-opus.md' % (slug, kind))
        if os.path.exists(f):
            CARDS.append(make_card(slug, t, en, d, u, kind, vt, asked,
                                   '%02d' % (i + 1), path=f, tag='Claude Opus 5'))


# 섹션 머리 아래 앞머리 — 늘 펴져 있고 그 아래에 뷰 카드가 이어 선다.
# sec_top 이 아니라 sec_fig 다. sec_top 은 「밸류에이션 · 개별 포스트」 버튼을 만들어
# 앞머리와 카드를 갈라 놓는다 — 앞머리는 고를 대상이 아니라 먼저 읽는 글이다
SEC_LEAD = {'sd-%s' % slug: head_html(d, en)
            for slug, _t, en, d, _u in EPISODES}


CSS = '''
/* 제목 링크 — 누르면 이 장으로 오지만 글자는 제목 그대로다 */
h1 a.h-home { color:inherit; text-decoration:none; }
h1 a.h-home:hover { text-decoration:underline; }
/* 밸류체인 도식 — 칸이 어디로 옮겨 가는지 두 줄로 */
.uc-rep pre.vc { margin:12px 0; padding:12px 14px; border:1px solid var(--line);
  border-radius:8px; background:var(--surface); overflow-x:auto;
  font: 400 .74rem/1.9 ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--ink-2); }

/* 다른 각도 상자 — 카드 발치에 접어 둔다 */
.uc-rep details.ang { margin:18px 0 0; border:1px solid var(--line); border-radius:8px;
  background:var(--surface); }
.uc-rep details.ang > summary { cursor:pointer; padding:10px 13px; font-size:.8rem;
  font-weight:800; color:var(--ink-2); list-style:none; }
.uc-rep details.ang > summary::-webkit-details-marker { display:none; }
.uc-rep details.ang > summary::before { content:"▸ "; color:var(--ink-3); }
.uc-rep details.ang[open] > summary::before { content:"▾ "; }
.uc-rep details.ang > summary span { font-weight:400; color:var(--ink-3); font-size:.72rem; }
.uc-rep .ang-s { padding:0 13px 8px; }
.uc-rep .ang-h { margin:0 0 4px; font-size:.78rem; font-weight:800; color:var(--ink); }
.uc-rep .ang-h i { font-style:normal; font-weight:400; font-size:.72rem; color:var(--ink-3);
  margin-left:7px; }
.uc-rep .ang-s ul { margin:0; padding:0 0 0 14px; }
.uc-rep .ang-s li { font-size:.78rem; line-height:1.7; color:var(--ink-2); margin:0 0 4px; }
.uc-rep .ang-m { margin:0; padding:10px 13px; border-top:1px solid var(--line);
  font-size:.78rem; line-height:1.7; color:var(--ink-2); }
/* 본문을 들여쓰지 않는다. 카드 안에 상자를 하나 더 그리면 쓸 폭이 그만큼 줄고,
   받은 글이 카드 속 카드처럼 읽힌다 — 여기서 카드는 뷰 하나다 */
.uc-body > .uc-rep { margin-left:0; padding-left:0; border-left:0; }
.uc-rep .fv-b { padding:0; }
/* 절 제목 앞의 노드 이름 — 번호가 노드마다 다시 시작하므로 어느 노드의 몇째인지를
   제목이 스스로 말해야 한다 */
.uc-rep h3 .h-node { display:block; font-size:.72rem; font-weight:700; line-height:1.6;
  color:var(--ink-3); opacity:.8; letter-spacing:.02em; }
/* 목차 — 번호가 ①②③ 이라 불릿을 쓰지 않는다. 마커가 둘이면 어느 쪽이 항목인지
   흐려지고, 들여쓰기만 두 번 먹는다. 줄 간격도 본문만큼 벌리지 않는다 —
   목차는 읽는 글이 아니라 한눈에 훑는 표다 */
.uc-rep .uc-toc { margin:2px 0 18px; padding:10px 12px; border:1px solid var(--line);
  border-radius:8px; background:var(--surface); }
.uc-rep .uc-toc .uc-label { margin:0 0 7px; }
.uc-rep .uc-toc .tg { display:flex; gap:10px; align-items:baseline; padding:3px 0; }
.uc-rep .uc-toc .tg-k { flex:0 0 4.6em; font-size:.82rem; font-weight:800;
  line-height:1.5; color:var(--ink); }
.uc-rep .uc-toc .tg-f { flex:0 0 4.6em; font-size:.7rem; font-weight:700;
  line-height:1.75; color:var(--ink-3); opacity:.72; }
.uc-rep .uc-toc ul { flex:1; margin:0; padding:0; list-style:none; }
.uc-rep .uc-toc li { font-size:.84rem; line-height:1.5; color:var(--ink-2);
  padding:1px 0; }
.uc-rep .uc-toc li b { color:var(--ink); font-weight:700; margin-right:4px; }
@media (max-width:520px) {
  .uc-rep .uc-toc .tg { display:block; }
  .uc-rep .uc-toc .tg-f { display:inline-block; margin-left:6px; }
}
/* 목차 안의 축 — 절이 셋을 넘는 마디는 그 안에서 한 번 더 갈린다 */
.uc-rep .uc-toc li.tg-ax { padding:1px 0 2px; }
.uc-rep .uc-toc li.tg-ax > span { display:block; font-size:.72rem;
  font-weight:700; color:var(--ink-3); opacity:.85; }
.uc-rep .uc-toc li.tg-ax > ul { margin:0 0 0 10px; }
.uc-rep .uc-toc .tg-a { font-size:.74rem; font-weight:700; color:var(--ink-3);
  opacity:.85; }
/* 목차 맨 위 사슬 — 목표 → 시도 → 성과 → 한계 */
.uc-rep .uc-toc .tg-chain { margin:0 0 8px; padding:0 0 7px;
  border-bottom:1px solid var(--line); font-size:.78rem; line-height:1.6; }
.uc-rep .uc-toc .tg-chain b { font-weight:800; color:var(--ink); }
.uc-rep .uc-toc .tg-chain i { font-style:normal; color:var(--ink-3); padding:0 1px; }

/* 회차에 붙는 줄 — 섹션 머리 아래 한 줄 */
.sd-meta { margin:0 0 14px; font-size:.76rem; line-height:1.7; color:var(--ink-3); }
.sd-meta b { color:var(--ink-2); font-weight:700; }
'''

# 제목을 누르면 이 장으로 온다. 파일 이름으로 걸면 gen_site 가 공개 주소(/semidoped)로
# 바꿔 준다 — 손으로 두 주소를 적지 않는다
HEADER = '''<h1><a class="h-home" href="Semi Doped 대시보드.html">🎙️ Semi Doped</a></h1>
<p class="lede">daily.semidoped.com 전사본을 카드로 옮긴다. 원문은 전부 무료라
잠그지 않는다. 카드 한 장이 원문 한 편이고, 목차가 그 편을 무슨 방법으로 나눴는지를
먼저 보인다.</p>'''

FOOTER = ('<p>생성물이다. 고칠 것은 <code>scratchpad/gen_semidoped_dashboard.py</code> 다. '
          '원문은 <a href="https://daily.semidoped.com">daily.semidoped.com</a>.</p>')


def main():
    dc.check_links(CARDS)
    dc.check_labels(CARDS)
    # 카드를 눌러도 새 페이지로 안 간다 — 자리에서 펼친다. 회차 한 편이 카드 한 장이라
    # 목록에서 펼치는 것으로 충분하고, 페이지가 따로 나면 주소가 둘로 갈린다
    dc.render(CARDS, 'Semi Doped 대시보드', HEADER, FOOTER, OUT,
              sec_fig=SEC_LEAD,
              extra_css=frame_view.CSS + CSS, newest_first=True)


if __name__ == '__main__':
    main()
