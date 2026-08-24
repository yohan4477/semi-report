# -*- coding: utf-8 -*-
"""통합 보고서의 숫자가 원문에 있나 — 대시보드 산문용 대조기.

check_cite 는 insights/ 아래 글만 본다. 통합 보고서는 카드에서 뽑아 쓴 숫자가
문단에 흩어져 있어서 그 대조가 비어 있었다. 여기서 본문 글자에 든 수를 전부 뽑아
바탕이 되는 원문(content/understanding/피지컬AI/*.md)에 그 수가 있는지 센다.

  PYTHONIOENCODING=utf-8 python insights/check_report.py

숫자 하나가 여러 꼴로 적히므로(1천만·10밀리언·1,000만) 정규화해서 견준다.
못 찾은 값은 FAIL 이 아니라 **확인 필요**로 낸다 — 원문이 「열흘」처럼 한글로만
적어 둔 경우가 있어 사람이 봐야 갈린다.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'),
     os.path.join(ROOT, 'content', 'understanding', '피지컬AI')),
]

# 숫자로 읽히지만 대조할 값이 아닌 것들 — 연·월·일, 절 번호, 흔한 서수
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '2023', '2024', '2025', '2026', '0'}


def norm(t):
    """1,000 · 1000 · 1천 을 같은 자리에 놓기 위한 성긴 정규화."""
    return re.sub(r'[\s,]', '', t)


def corpus(d):
    out = []
    for f in sorted(os.listdir(d)):
        if f.endswith('.md'):
            out.append(io.open(os.path.join(d, f), encoding='utf-8').read())
    return norm('\n'.join(out))


def body(html):
    """보고서 층의 글자만 — 태그와 스크립트를 걷는다."""
    h = io.open(html, encoding='utf-8').read()
    i = h.find('id="sec-report"')
    if i < 0:
        return ''
    seg = h[i:h.find('</section>', i)]
    seg = re.sub(r'<script.*?</script>', ' ', seg, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', seg)


def main():
    bad = 0
    for page, src_dir in PAGES:
        if not os.path.exists(page):
            print('건너뜀 — 파일이 없다: %s' % page)
            continue
        text, src = body(page), corpus(src_dir)
        nums = []
        for m in re.finditer(r'\d[\d,\.]*', text):
            v = m.group(0).rstrip('.')
            if v in SKIP or len(norm(v)) < 2:
                continue
            nums.append((v, text[max(0, m.start() - 30):m.end() + 30]))
        miss = [(v, c) for v, c in nums if norm(v) not in src]
        name = os.path.basename(page)
        for v, c in miss:
            print('확인 필요 %s — 원문에서 못 찾은 값 %s: …%s…'
                  % (name, v, ' '.join(c.split())))
        print('%s: 값 %d개 / 확인 필요 %d개' % (name, len(nums), len(miss)))
        bad += len(miss)
    print('요약: 확인 필요 %d건' % bad)


if __name__ == '__main__':
    main()
