# -*- coding: utf-8 -*-
"""주간·월간 롤업 리포트를 소셜 히스토리와 SemiAnalysis 대시보드 상단에 스플라이스한다.

- 산문은 data/rollup_notes.json (사람이 씀, 판단이라 자동 생성 금지)
- 기간은 **링크드인 게시 시각**(URN 역산) 기준, 건수는 히스토리 day 그룹에서 계산
- 두 페이지 모두 <!--ROLLUP:START--> ~ <!--ROLLUP:END--> 사이만 갈아끼운다
- 렌더러·CSS는 scripts/rollup_lib.py 공용 (금융·미국주식 사관학교 대시보드와 한 벌)

사용: python scripts/gen_rollup.py
"""
import io, os, re, json, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rollup_lib as rl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
DASH = os.path.join(ROOT, '대시보드', 'SemiAnalysis 대시보드.html')
NOTES = os.path.join(ROOT, 'data', 'rollup_notes.json')


def day_counts(html):
    """{게시일: {'li': n, 'yt': n, 'all': n}} — 히스토리 day 그룹 기준"""
    out = {}
    for d, body in re.findall(r'<div class="day"><h3>(\d{4}-\d{2}-\d{2})</h3>(.*?)</div></div>', html, re.S):
        rows = re.findall(r'<a class="rowmain" href="([^"]+)"', body)
        li = sum(1 for u in rows if 'linkedin.com' in u)
        out[d] = {'li': li, 'yt': len(rows) - li, 'all': len(rows)}
    return out


def splice(path, anchor, block, indent=''):
    html = io.open(path, encoding='utf-8').read()
    html = re.sub(r'\n?  /\* rollup(:start)? \*/.*?(/\* rollup:end \*/\n)?(?=</style>)', '',
                  html, flags=re.S)
    html = html.replace('</style>', rl.CSS + '</style>', 1)
    if '<!--ROLLUP:START-->' not in html:
        assert anchor in html, 'anchor not found in %s' % path
        html = html.replace(anchor, indent + '<!--ROLLUP:START--><!--ROLLUP:END-->\n' + anchor, 1)
    html = re.sub(r'<!--ROLLUP:START-->.*?<!--ROLLUP:END-->',
                  lambda m: '<!--ROLLUP:START-->' + block + '<!--ROLLUP:END-->', html, flags=re.S)
    io.open(path, 'w', encoding='utf-8').write(html)
    print('%-28s div %d %d' % (os.path.basename(path), html.count('<div'), html.count('</div>')))


def main():
    notes = json.load(io.open(NOTES, encoding='utf-8'))
    counts = day_counts(io.open(HIST, encoding='utf-8').read())
    # 두 장의 기본값이 다르다(2026-08-21).
    #   · 소셜 신호 히스토리 — 접는다. 여기는 아카이브라 첫 화면이 타임라인이어야 한다
    #   · SemiAnalysis 대시보드 — 펼친다. 여기서는 롤업이 그 주의 요지 노릇을 한다
    # 접힌 요약 한 줄(show_desc)은 두 장 모두 뺀다 — 헤드라인과 같은 말을 두 번 읽게 된다.
    splice(HIST, '  <div class="tabbar">',
           rl.build(notes, counts, unit='건', open_current=False, show_desc=False), '  ')
    splice(DASH, '  <section id="social-section"',
           rl.build(notes, counts, unit='건', open_current=True, show_desc=False), '  ')
    print('reports: %d' % len(notes['reports']))


if __name__ == '__main__':
    main()
