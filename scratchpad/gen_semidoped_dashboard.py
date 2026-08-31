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
    # 제목은 우리가 새로 짓지 않는다. 그 회차가 달고 나온 이름을 한국어로 옮기고,
    # 원제는 메타 줄에 그대로 남긴다
    ('2026-08-27-openai-jalapeno', '오픈AI 의 할라페뇨라는 느낌',
     "OpenAI's Jalapeño Feeling", '2026-08-27',
     'https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling'),
    ('2026-08-24-grok-bots-cpu', 'Grok 봇과 에이전틱 AI 에서 CPU 가 쓰이는 방식',
     'Grok Bots and How CPUs are used in Agentic AI', '2026-08-24',
     'https://daily.semidoped.com/p/new-episode-grok-bots-and-how-cpus'),
]

# 섹션이 회차다. 회차 제목 아래 뷰 카드 셋이 나란히 선다
VIEWS = [
    ('strategy', '전략 뷰', '시니어 전략 컨설턴트에게 물었다'),
    ('tech', '기술 뷰', '시니어 업계 기술 전문가에게 물었다'),
    ('merged', '통합 뷰', '시니어 애널리스트에게 두 뷰를 합쳐 달라고 물었다'),
]


def view_html(slug, kind, view_title, asked):
    """뷰 하나를 카드 상자로. 꼬리에 붙은 요약·제언은 상자 맨 위로 올린다.

    받은 글에서 그 대목이 맨 끝에 서면, 접힌 카드에서 먼저 보이는 자리에 배경 설명이
    오고 결론이 스크롤 끝에 숨는다. 문장은 안 고치고 자리만 옮긴다.
    """
    md = frame_view.body_of(os.path.join(
        ROOT, 'insights', 'frames', '%s-%s.md' % (slug, kind)))
    summ, rest = frame_view.split_summary(md)
    top = ('<div class="vc-sum">%s</div>' % frame_view.to_html(summ)) if summ else ''
    return ('<section class="vc">'
            '<p class="vc-h">%s<span>%s · 받은 그대로 · 미검증</span></p>'
            '%s<div class="fv-b">%s</div></section>'
            % (view_title, asked, top, frame_view.to_html(rest)))


def make_card(slug, ep_title, en_title, date, url, num):
    """회차 한 편이 카드 한 장이다. 누르면 앞머리가 먼저 서고 그 아래 뷰 카드가 선다."""
    lead_md = frame_view.body_of(os.path.join(
        ROOT, 'insights', 'frames', '%s-strategy.md' % slug))
    intro = frame_view.intro_of(lead_md)
    body = ''.join(view_html(slug, kind, vt, asked) for kind, vt, asked in VIEWS)
    return {
        'id': 'sd-%s' % slug,
        'section': ('sd-ep', '01', '회차',
                    '한 회차를 눈을 바꿔 설명하게 하고 받은 글을 그대로 싣는다'),
        'title': ep_title,
        'gain': frame_view.lead_of(lead_md)[:150],
        'meta': ['Austin · Vik Sekar <b>Semi Doped 공동 진행</b>',
                 '업로드 %s' % date, '원제 %s' % en_title,
                 'Gemini 3.1 Pro', '받은 그대로 · 미검증'],
        'links': [('요약본', blob(SRC + '%s.md' % slug), ''),
                  ('원문(Semi Doped)', url, 'ghost')],
        # 앞머리는 본문 맨 위 상자에 한 번만 선다 — 한줄 코멘트로도 세우면 같은 글이 두 번
        # 읽힌다. 접힌 목록에 서는 gain 만 그 첫 문장을 쓴다
        'verdict': '',
        'report': [('raw', '<div class="fv-b vc-intro">%s</div>%s'
                    % (frame_view.to_html(intro), body))],
    }


# 회차 한 편에 카드 한 장. 뷰 셋은 그 카드 안에 상자로 선다
CARDS = [make_card(slug, t, en, d, u, '%02d' % (i + 1))
         for i, (slug, t, en, d, u) in enumerate(EPISODES)]


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

/* 회차 앞머리 — 뷰 카드보다 먼저 선다. 이 회차가 무엇을 다루나 */
.uc-rep .vc-intro { padding:0 0 6px; }
.uc-rep .vc-intro p { font-size:.86rem; }
/* 뷰 카드 — 한 회차 아래 뷰마다 한 장 */
.uc-rep section.vc { margin:16px 0; border:1px solid var(--line); border-radius:10px;
  background:var(--surface); }
.uc-rep section.vc .vc-h { margin:0; padding:11px 14px 9px; border-bottom:1px solid var(--line);
  font-size:.88rem; font-weight:800; color:var(--ink); }
.uc-rep section.vc .vc-h span { display:block; margin-top:2px; font-weight:400;
  font-size:.72rem; color:var(--ink-3); }
/* 받은 글 꼬리의 요약·제언을 여기로 올린다 — 뷰 카드에서 먼저 읽히는 자리 */
.uc-rep .vc-sum { margin:12px 14px 0; padding:10px 12px; border-left:3px solid var(--ink-3);
  border-radius:0 6px 6px 0; background:var(--sunk); }
.uc-rep .vc-sum p { margin:6px 0; font-size:.82rem; line-height:1.75; color:var(--ink-2); }
.uc-rep .vc-sum p.fv-h { margin:0 0 4px; font-weight:800; color:var(--ink); }
.uc-rep .vc-sum ul { margin:6px 0; padding-left:18px; }
.uc-rep .vc-sum li { font-size:.82rem; line-height:1.75; color:var(--ink-2); }
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
    # 카드를 눌러도 새 페이지로 안 간다 — 자리에서 펼친다. 회차 한 편이 카드 한 장이라
    # 목록에서 펼치는 것으로 충분하고, 페이지가 따로 나면 주소가 둘로 갈린다
    dc.render(CARDS, 'Semi Doped 대시보드', HEADER, FOOTER, OUT,
              extra_css=frame_view.CSS + CSS, newest_first=True)


if __name__ == '__main__':
    main()
