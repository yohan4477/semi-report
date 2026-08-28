# -*- coding: utf-8 -*-
"""통합 인사이트·통합 보고서 두 화면을 걷어낸 뒤 남는 참조를 정리한다.

원본(insights/synth·loop·briefs·debate, scratchpad/_biz_part*·_val_*·_fund_*)과
생성기는 그대로 둔다 — 언제든 다시 만들 수 있어야 한다. 여기서는 화면을 가리키는
링크와 공개 목록, 그리고 그 파일을 읽는 검사기만 손댄다.
"""
import io

PATCH = [
    # 공개 사이트 목록에서 뺀다
    ('scripts/gen_site.py',
     "    ('통합 인사이트.html', 'unified', '통합 인사이트', '🧩',",
     "    # 2026-08-28 두 화면을 걷었다. 원본과 생성기는 남아 있으니 다시 세울 때\n"
     "    # 이 줄을 되살린다.\n"
     "    # ('통합 인사이트.html', 'unified', '통합 인사이트', '🧩',"),
    ('scripts/gen_site.py',
     "    ('통합 보고서.html', 'report', '통합 보고서', '📑',",
     "    # ('통합 보고서.html', 'report', '통합 보고서', '📑',"),
    # 각도 지도에서 죽은 링크를 뺀다
    ('scratchpad/gen_angles_dashboard.py',
     "    o.append('<p class=\"note\">가로지르는 것만 추린 요약은 '\n"
     "             '<a href=\"통합 인사이트.html\">통합 인사이트</a>의 각도 층에 있다. '\n"
     "             '이 장은 항목 전체를 각도별로 펼친 쪽이다.</p>')\n",
     "    o.append('<p class=\"note\">이 장은 각도 항목 전체를 각도별로 펼친 것이다.</p>')\n"),
]

for f, a, b in PATCH:
    t = io.open(f, encoding='utf-8').read()
    if a not in t:
        print('   못 찾음:', f, a.strip()[:40])
        continue
    io.open(f, 'w', encoding='utf-8', newline='\n').write(t.replace(a, b, 1))
    print('고침:', f)
