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

# (페이지, 층 id, 재료 폴더) — 한 페이지에 성격이 다른 리포트 층이 여럿이면 층마다 재료가 다르다.
PAGES = [
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-report',
     os.path.join(ROOT, 'content', 'understanding', '피지컬AI')),
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-biz',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 알파벳 밸류에이션 층. 재료가 둘이다 — 산업 판단은 뉴스레터에서 오고 재무 숫자는
    # SEC 제출서류에서 온다. 후자는 JSON 이라 이 검사기가 못 읽으므로 googl_facts.md 로
    # 떨어뜨려 EXTRA 에 넣는다. 그 파일은 scratchpad/googl_cases.py 가 다시 쓴다.
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-val',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 모델 회사·칩 회사 정성 비교. 재무제표가 없는 회사가 대부분이라 값이 전부
    # 뉴스레터에서 온다.
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-ai',
     os.path.join(ROOT, 'content', 'newsletter')),
]

# 회사 사실(설립·조달·밸류)은 유튜브 원문이 아니라 회사 공식 사이트에서 온다. 그 조사 파일도
# 대조 대상에 넣는다 — 여기에도 없는 값이면 어디서 왔는지 사람이 대야 한다.
EXTRA = [os.path.join(ROOT, 'scratchpad', 'company_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'company_facts_B.md'),
         # SemiAnalysis 로봇 보고서의 재료 — 원문은 영어 클리핑이라 사실표로 대조한다
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_B.md'),
         # 알파벳 밸류에이션의 재무 숫자와 우리 계산 결과
         os.path.join(ROOT, 'scratchpad', 'googl_facts.md'),
         # 빅테크 여섯 비교의 계산 결과
         os.path.join(ROOT, 'scratchpad', 'peers_facts.md'),
         os.path.join(ROOT, 'scratchpad', 'nvda_facts.md')]

# 숫자로 읽히지만 대조할 값이 아닌 것들 — 연·월·일, 절 번호, 흔한 서수
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '2023', '2024', '2025', '2026', '0'}


def norm(t):
    """1,000 · 1000 · 1천 을 같은 자리에 놓기 위한 성긴 정규화."""
    return re.sub(r'[\s,]', '', t)


def corpus(d):
    out = []
    for base, _dirs, files in os.walk(d):
        for f in sorted(files):
            if f.endswith('.md'):
                out.append(io.open(os.path.join(base, f), encoding='utf-8').read())
    for f in EXTRA:
        if os.path.exists(f):
            out.append(io.open(f, encoding='utf-8').read())
    return norm('\n'.join(out))


def body(html, sec):
    """그 층의 글자만 — 태그와 스크립트를 걷는다."""
    h = io.open(html, encoding='utf-8').read()
    i = h.find('id="%s"' % sec)
    if i < 0:
        return ''
    seg = h[i:h.find('</section>', i)]
    seg = re.sub(r'<script.*?</script>', ' ', seg, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', seg)


def main():
    bad = 0
    for page, sec, src_dir in PAGES:
        if not os.path.exists(page):
            print('건너뜀 — 파일이 없다: %s' % page)
            continue
        text, src = body(page, sec), corpus(src_dir)
        if not text.strip():
            print('건너뜀 — 층이 아직 없다: %s' % sec)
            continue
        nums = []
        for m in re.finditer(r'\d[\d,\.]*', text):
            v = m.group(0).rstrip('.')
            if v in SKIP or len(norm(v)) < 2:
                continue
            nums.append((v, text[max(0, m.start() - 30):m.end() + 30]))
        # 한국식 단위로 옮긴 값은 원문 표기와 글자가 다르다(3억 9,700만 달러 ↔ $397M).
        # 바로 뒤에 원문 표기를 괄호로 병기했으면 출처가 붙은 것으로 본다.
        def sourced(v, c):
            if norm(v) in src:
                return True
            return bool(re.search(r'\(\$\s?[\d,\.]+\s?[MB]?\)', c))

        miss = [(v, c) for v, c in nums if not sourced(v, c)]
        name = os.path.basename(page) + ' / ' + sec
        for v, c in miss:
            print('확인 필요 %s — 원문에서 못 찾은 값 %s: …%s…'
                  % (name, v, ' '.join(c.split())))
        print('%s: 값 %d개 / 확인 필요 %d개' % (name, len(nums), len(miss)))
        bad += len(miss)
    print('요약: 확인 필요 %d건' % bad)


if __name__ == '__main__':
    main()
