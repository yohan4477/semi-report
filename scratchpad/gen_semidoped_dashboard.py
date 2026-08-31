# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — 회차 하나를 여러 눈으로 설명하게 하고 그대로 싣는다.

카드 한 장이 「회차 × 뷰」다. 본문은 우리가 쓴 글이 아니라 다른 모델(Gemini 3.1 Pro)
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


# 회차 하나에 뷰 셋. 뷰마다 카드 한 장이고, 본문은 받은 답을 그대로 싣는다
EPISODES = [
    ('2026-08-27-openai-jalapeno', '오픈AI 할라페뇨', '2026-08-27',
     'https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling'),
    ('2026-08-24-grok-bots-cpu', 'Grok bots 와 에이전틱 CPU', '2026-08-24',
     'https://daily.semidoped.com/p/new-episode-grok-bots-and-how-cpus'),
]

# 뷰마다 섹션 하나. 같은 눈으로 본 글끼리 모아 두어야 회차를 건너 견줄 수 있다
VIEWS = [
    ('strategy', '전략 뷰', '전략 컨설턴트에게 물었다',
     ('sd-strategy', '01', '전략 뷰', '전략 컨설턴트에게 회차를 설명하게 했다')),
    ('tech', '기술 뷰', '업계 기술 전문가에게 물었다',
     ('sd-tech', '02', '기술 뷰', '업계 기술 전문가에게 회차를 설명하게 했다')),
    ('merged', '통합 뷰', '두 뷰를 합쳐 달라고 물었다',
     ('sd-merged', '03', '통합 뷰', '앞의 두 뷰를 넣고 합쳐 달라고 했다')),
]


def make_card(slug, ep_title, date, url, kind, view_title, asked, section):
    md = frame_view.body_of(os.path.join(
        ROOT, 'insights', 'frames', '%s-%s.md' % (slug, kind)))
    return {
        'id': 'sd-%s-%s' % (slug, kind),
        'section': section,
        'title': '%s — %s' % (ep_title, view_title),
        'gain': '%s. 받은 글을 고치지 않고 그대로 싣는다.' % asked,
        'meta': ['Austin · Vik Sekar <b>Semi Doped 공동 진행</b>',
                 '업로드 %s' % date, 'Gemini 3.1 Pro', '받은 그대로 · 미검증'],
        'links': [('요약본', blob(SRC + '%s.md' % slug), ''),
                  ('원문(Semi Doped)', url, 'ghost')],
        'verdict': '%s 받은 답을 그대로 싣는다. 원문이 받쳐 주는지는 '
                   'insights/check_frame.py 가 따로 센다.' % asked,
        'report': [('raw', '<div class="fv-b">%s</div>' % frame_view.to_html(md))],
    }


# 섹션이 뷰라서 뷰를 바깥 고리로 돈다 — 전략 뷰 카드가 먼저 모이고 그다음이 기술 뷰다
CARDS = [make_card(slug, t, d, u, kind, vt, asked, sec)
         for kind, vt, asked, sec in VIEWS
         for slug, t, d, u in EPISODES]

CSS = '''
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
/* 한줄 코멘트가 머리다. 그 아래를 한 칸 들여써서 나머지가 그 머리에 딸린 것으로
   보이게 한다 — 나란히 서면 코멘트가 여러 문단 중 하나로 읽힌다 */
.uc-body > .uc-verdict { margin-bottom:12px; }
/* 딱지 뒤에서 줄을 바꾼다 — 딱지와 글이 한 문장처럼 붙어 읽히지 않게 */
.uc-body > .uc-verdict > b:first-child { display:block; margin-bottom:5px;
  font-size:.74rem; color:var(--ink-3); letter-spacing:.02em; }
.uc-body > .uc-rep { margin-left:14px; padding-left:14px;
  border-left:2px solid var(--line); }
@media (max-width:520px) {
  .uc-body > .uc-rep { margin-left:6px; padding-left:10px; }
}
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
'''

HEADER = '''<h1>🎙️ Semi Doped</h1>
<p class="lede">daily.semidoped.com 전사본을 카드로 옮긴다. 원문은 전부 무료라
잠그지 않는다. 카드 한 장이 원문 한 편이고, 목차가 그 편을 무슨 방법으로 나눴는지를
먼저 보인다.</p>'''

FOOTER = ('<p>생성물이다. 고칠 것은 <code>scratchpad/gen_semidoped_dashboard.py</code> 다. '
          '원문은 <a href="https://daily.semidoped.com">daily.semidoped.com</a>.</p>')


def main():
    dc.check_links(CARDS)
    dc.check_labels(CARDS)
    dc.render(CARDS, 'Semi Doped 대시보드', HEADER, FOOTER, OUT,
              page_slug='semidoped',
              extra_css=frame_view.CSS + CSS, newest_first=True)


if __name__ == '__main__':
    main()
