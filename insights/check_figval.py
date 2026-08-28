# -*- coding: utf-8 -*-
"""도해에 든 값이 원문에 있나 — 손으로 그린 그림만 값을 지어낼 수 있다.

카드 본문은 원문 md 를 그대로 렌더링하므로 값이 새로 생길 자리가 없다. 반면 도해는
사람이 SVG 로 짠 것이라 원문에 없는 수가 들어갈 수 있고, 그게 insight-figure 규칙 1이
막으려는 사고다. 실제로 통합 보고서에서 축 눈금 하나($1.50)가 그렇게 들어갔다가
check_report 에 걸렸다 — 그 대조를 원문 하나짜리 카드 쪽에도 붙인다.

지금은 **확인 필요만 센다.** FAIL 을 안 낸다 — 도해에는 좌표·개수처럼 값이 아닌 수가
섞여 있어서, 사람이 한 번 훑기 전에 게이트로 세우면 규칙이 죽는다.

  PYTHONIOENCODING=utf-8 python insights/check_figval.py
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scratchpad'))
import paths  # noqa: E402

SRC_DIR = os.path.join(paths.ROOT, 'content', 'understanding', 'AI Engineer')
TEXT_RE = re.compile(r'<text[^>]*>([^<]*)<')
NUM_RE = re.compile(r'\d[\d,\.]*')
# 도해 글자에 섞이는 값 아닌 수 — 순번·연차 표기·흔한 한 자리
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '10',
        '2023', '2024', '2025', '2026'}


def digits(s):
    return re.sub(r'[^0-9]', '', s or '')


def norm(s):
    """쉼표만 떼고 남긴다. 숫자를 다 이어 붙이면 「4.8」이 「…4, 8…」에 우연히 걸린다 —
    첫 판이 그렇게 느슨해서 도해 한 줄만 잡고 나머지 둘을 놓쳤다."""
    return (s or '').replace(',', '')


def src_by_vid():
    """영상 ID -> 원문 md 본문. source: 줄의 유튜브 주소에서 ID를 딴다."""
    out = {}
    for p in sorted(glob.glob(os.path.join(SRC_DIR, '*.md'))):
        t = io.open(p, encoding='utf-8').read()
        m = re.search(r'^source:\s*\S*?([A-Za-z0-9_-]{11})\s*$', t, re.M)
        if m:
            out[m.group(1)] = (os.path.basename(p), t)
    return out


def fig_nums(markup):
    """그림 글자에 적힌 값. 좌표·클래스는 태그 안이라 안 걸린다.

    이 장의 도해는 SVG 가 아니라 HTML div 로 짠 것이 많다. 둘 다 읽는다 —
    SVG 면 <text> 안만, HTML 이면 태그를 떼고 남은 글자를 본다.
    """
    m = markup or ''
    if '<text' in m:
        chunks = TEXT_RE.findall(m)
    else:
        chunks = re.sub(r'<[^>]+>', ' ', m).split()
    out = set()
    for s in chunks:
        for n in NUM_RE.findall(s):
            if n.strip('.,') not in SKIP and len(digits(n)) >= 2:
                out.add(n.strip('.,'))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    import aie_figs  # noqa: E402  scratchpad 에 있다
    src = src_by_vid()
    books = [('RFIGS', getattr(aie_figs, 'RFIGS', {})),
             ('FIGS', getattr(aie_figs, 'FIGS', {}))]
    need = shown = 0
    for book, table in books:
        for vid, figs in sorted(table.items()):
            if vid not in src:
                print('건너뜀 — 원문을 못 찾음: %s (%s)' % (vid, book))
                continue
            name, text = src[vid]
            body = norm(text)
            items = figs.items() if isinstance(figs, dict) else \
                [(str(i), f) for i, f in enumerate(figs)]
            for key, fig in items:
                svg = fig[1] if isinstance(fig, (tuple, list)) and len(fig) > 1 \
                    else str(fig)
                for n in sorted(fig_nums(svg)):
                    shown += 1
                    if norm(n) not in body:
                        need += 1
                        print('확인 필요 %s [%s] 도해 값 "%s" 가 원문에 없다'
                              % (name[:44], key, n))
    print('\n요약: 도해 값 %d개 / 확인 필요 %d개' % (shown, need))
    return 0


if __name__ == '__main__':
    sys.exit(main())
