# -*- coding: utf-8 -*-
"""보고서 층의 차례와 절 번호 — 규약 하나, 코드 하나.

CPO 층과 선단 패키징 층이 저마다 `toc_html` 을 들고 있다가 넷을 따로 고쳐야 했다
(2026-09-05). 다음 층이 또 복사하면 또 갈린다. 그래서 여기 하나만 둔다.

규약 (2026-09-05 확정)

    번호      대단원은 「1. 2. 3.」, 그 아래 절은 ①②③.
              CLAUDE.md 「번호는 층마다 다르다」. 거꾸로 붙어 있던 것을 이날 뒤집었다
    한 줄에    절 하나. 「·」로 이으면 절 제목 안의 대시와 섞여 한 문장으로 읽힌다
    들여쓰기   머리글 0 · 대단원 6px · 절 16px. 세 층이 왼쪽 끝에 나란히 서면 눈이 층을 못 센다
    색        본문 잉크. 브라우저 기본 파랑은 회색 판에서 그 자리만 튄다
    밑줄      없다. hover 에만. 눌리는 자리는 커서가 말한다

    CSS 는 이 파일의 `CSS` 다 — 보고서 장 밖(메르·링크드인 흐름 층)에서도 같은 차례를
    쓰므로 규약과 붙여 둔다. 안 물리면 차례가 맨 글씨로 나온다(2026-09-08 두 흐름 장이
    그랬다).
    새 층은 `toc_html` 과 `sec_title` 을 부르기만 한다 — 직접 짜지 않는다.
    안 부르고 손으로 짠 층은 `check_toc` 가 문다.
"""
import re

# 표지·차례의 붓. 이 층을 쓰는 장은 extra_css 에 이것을 반드시 넣는다.
CSS = """
  /* 보고서 표지 — 한 층에 글이 둘이라 어디서 끊기는지가 보여야 한다.
     번호·제목·바탕·기간을 한 덩이로 세우고, 다음 보고서 앞에 굵은 선을 둔다. */
  .rep-head{margin:8px 0 18px;padding:18px 20px;border:1px solid var(--line);
            border-left:5px solid var(--accent);border-radius:12px;
            background:var(--accent-soft)}
  .rep-head .rn{display:block;font-size:11px;font-weight:850;letter-spacing:.08em;
                color:var(--accent-ink)}
  .rep-head h2{margin:6px 0 8px;font-size:21px;line-height:1.35}
  .rep-head .rm{margin:0;font-size:12.5px;line-height:1.7;color:var(--ink-2)}
  .rep-head .rm b{color:var(--ink)}
  .rep-cut{margin:38px 0 0;border:0;border-top:3px solid var(--line)}
  /* rep-toc 는 절 차례, rep-note 는 안내문. 규약 검사(check_toc)가 앞엣것만 본다 */
  .rep-toc,.rep-note{margin:0 0 18px;padding:14px 16px;border:1px dashed var(--line);
           border-radius:12px;font-size:13px;line-height:1.85}
  .rep-note a{font-weight:700;color:var(--ink);text-decoration:none}
  .rep-note a:hover{text-decoration:underline}
  .rep-toc .tl{display:block;margin-bottom:2px}
  .rep-toc .tg{display:block;margin-top:12px;padding-left:6px;font-size:12.5px;color:var(--ink-2)}
  /* 층마다 들여쓴다 — 머리글 · 묶음 이름 · 절 목록이 눈으로 갈린다 */
  .rep-toc .tt{display:block;padding-left:16px}
  /* 차례 링크가 브라우저 기본 파랑으로 나와 회색 판에서 튀었다(2026-09-05).
     색은 본문 잉크로 두고 밑줄만 옅게 — 눌리는 자리인 것은 밑줄이 말한다 */
  .rep-toc a{font-weight:700;color:var(--ink);text-decoration:none}
  .rep-toc a:hover{text-decoration:underline;text-decoration-color:var(--ink-3);
                   text-underline-offset:3px}
"""


def circ(n):
    """절 번호 ①②③. 스무 개를 넘으면 그냥 숫자다 — 유니코드에 동그라미가 스물까지다."""
    return chr(0x2460 + n - 1) if 1 <= n <= 20 else str(n)


_OLDNUM = re.compile(r'^(?:\d+\.|[①-⑳])\s*')


def sec_title(n, title):
    """본문 절 제목. 목차와 같은 함수에서 나와야 번호가 안 어긋난다.

    옛 층은 제목 문자열에 「1. 」이 박혀 있다. 번호는 여기서만 붙이므로 걷고 다시 단다."""
    return '%s %s' % (circ(n), _OLDNUM.sub('', title))


def toc_html(anchor, lead, groups, titles):
    """차례 한 덩어리.

    anchor  앵커 접두어. 'pkg' 면 링크가 #pkg-1
    lead    머리글 한 줄. 이 층이 물음을 몇 묶음으로 따라가는지
    groups  [(대단원 이름, 첫 절, 끝 절)] — 이름에 번호를 붙이지 않는다. 여기서 센다
    titles  절 제목 목록. groups 의 끝 절 번호와 길이가 같아야 한다
    """
    assert groups and groups[-1][2] == len(titles), (groups, len(titles))
    parts = ['<p class="rep-toc"><b class="tl">%s</b>' % lead]
    for k, (name, a, b) in enumerate(groups, 1):
        links = '<br>'.join('<a href="#%s-%d">%s %s</a>' % (anchor, i, circ(i), titles[i - 1])
                            for i in range(a, b + 1))
        parts.append('<b class="tg">%d. %s</b><span class="tt">%s</span>' % (k, name, links))
    return ''.join(parts) + '</p>'


_TOC = re.compile(r'<p class="rep-toc">(.*?)</p>', re.S)
_TG = re.compile(r'<b class="tg">(\d+)\.\s')
_LINK = re.compile(r'<a href="#[a-z]+-\d+">(.)')
_CIRC = set(chr(0x2460 + i) for i in range(20))


def check_toc(html):
    """만들어진 페이지의 차례가 규약대로인가. 손으로 짠 층을 잡는다.

    돌려주는 것은 어긋난 것들의 목록이다. 비어 있으면 통과.
    """
    bad = []
    for k, block in enumerate(_TOC.findall(html), 1):
        if 'class="tg"' not in block:
            bad.append('차례 %d: 대단원(class="tg")이 없다 — toc_html 을 안 썼다' % k)
            continue
        nums = [int(x) for x in _TG.findall(block)]
        if nums != list(range(1, len(nums) + 1)):
            bad.append('차례 %d: 대단원 번호가 1부터 이어지지 않는다 %s' % (k, nums))
        heads = _LINK.findall(block)
        if not heads:
            bad.append('차례 %d: 절 링크가 없다' % k)
        elif any(h not in _CIRC for h in heads):
            bad.append('차례 %d: 절 번호가 동그라미가 아니다 %s'
                       % (k, [h for h in heads if h not in _CIRC][:3]))
        if re.search(r'</a>\s*(?:&nbsp;|\s)*·', block):
            bad.append('차례 %d: 절을 「·」로 이었다 — 한 줄에 하나씩' % k)
    return bad
