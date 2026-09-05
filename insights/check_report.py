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
import glob
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
    # 자금조달 층. 재료가 각도 파일이지만 각도의 값은 전부 뉴스레터 네 편에서 온 것이라
    # 대조 대상은 같다 — 각도를 거쳐 온 값이 원문에 없으면 각도가 틀린 것이다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-fund',
     os.path.join(ROOT, 'content', 'newsletter')),
    # CPO 층(2026-09-04). 재료가 뉴스레터 아홉 편 + Semi Doped 다섯 회차 + 영문 클리핑 넷 +
    # 링크드인 셋이다. 뉴스레터 밖의 것은 파일로 EXTRA 에 올린다 — 폴더째 넣으면 이 층과 무관한
    # 회차의 값이 다른 층의 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-cpo',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 선단 패키징 층(2026-09-05). 재료가 뉴스레터 아홉 편 + Semi Doped 한 회차 + 영문 클리핑 둘이다.
    # 뉴스레터 밖의 셋만 파일로 EXTRA 에 올린다 — 폴더째 넣으면 이 층과 무관한 회차의 값이
    # 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-pkg',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 금리·물가 층(2026-09-05). 재료가 회계사·미국주식 사관학교·류상철·김상훈·박소연에
    # 흩어져 있어 공통 폴더가 content/understanding 인데 그것을 통째로 넣으면 540편이
    # 알리바이가 된다. 그래서 폴더 없이 RATE_EXTRA 에 파일을 하나씩 적는다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-rate', None),
]

_SD = os.path.join(ROOT, 'content', 'understanding', 'Semi Doped')
_CLIP = os.path.join(ROOT, 'input', 'clippings')
_LI = os.path.join(ROOT, 'content', 'linkedin')
CPO_EXTRA = [os.path.join(_SD, f + '.md') for f in
             ('2026-06-12-computex-optics-power', '2026-07-16-picojool-yuen',
              '2026-07-25-datacenter-interconnects', '2026-08-07-globalfoundries-barber',
              '2026-08-11-china-optical-ban')] + [
    os.path.join(_CLIP, 'NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, '
                 'Jensen Math, Feynman.md'),
    os.path.join(_CLIP, 'Tariff Armageddon  GPU Loopholes, Mexico Supply Chain Shift, Wafer Fab Equipment '
                 'Vulnerabilities, Optical Module Pricing Surge, Datacenter Equipment.md'),
] + glob.glob(os.path.join(_CLIP, 'Huawei AI CloudMatrix 384*.md')) + glob.glob(
    os.path.join(_CLIP, 'Co-Packaged Optics (CPO) Book*.md')) + [
    os.path.join(_LI, '[2605] 링크드인 게시물.md'), os.path.join(_LI, '[2607] 링크드인 게시물.md'),
    os.path.join(_LI, '[2608] 링크드인 게시물.md'), os.path.join(_LI, '[2609] 링크드인 게시물.md')]

# 선단 패키징 층의 뉴스레터 밖 재료 셋
PKG_EXTRA = [os.path.join(ROOT, 'insights', 'semidoped', '2026-06-19-advanced-packaging-strategy.md'),
             os.path.join(_CLIP, 'EMIB-T Roadmap, Custom HBM, HBM4 Packaging Challenges, '
                          'Microfluidic Cooling, Photonic Interconnects, and More.md'),
             os.path.join(_CLIP, 'CPUs are Back The Datacenter CPU Landscape in 2026.md')]

# 금리·물가 층의 재료 마흔. 폴더째 넣지 않고 파일을 하나씩 적는다 — content/understanding 은
# 540편이라 통째로 넣으면 이 층과 무관한 편이 알리바이가 된다. EXTRA 는 확장자를 안 가려
# 읽으므로 메르 클리핑과 사슬(json)도 그대로 대조 대상이 된다
RATE_EXTRA = [os.path.join(ROOT, *p.split('/')) for p in (
    'input/clippings/mer/223873166379.json',
    'input/clippings/mer/223887755561.json',
    'input/clippings/mer/223931247450.json',
    'input/clippings/mer/223954627912.json',
    'input/clippings/mer/224032232941.json',
    'input/clippings/mer/224031770885.json',
    'input/clippings/mer/224095422334.json',
    'input/clippings/mer/224100335488.json',
    'input/clippings/mer/224153982515.json',
    'input/clippings/mer/224167473277.json',
    'input/clippings/mer/224179162516.json',
    'input/clippings/mer/224260820330.json',
    'input/clippings/mer/224292480472.json',
    'input/clippings/mer/224292701545.json',
    'input/clippings/mer/224356110315.json',
    'input/clippings/mer/224366267736.json',
    'input/clippings/mer/224369325535.json',
    'input/clippings/mer/224376966792.json',
    'input/clippings/mer/224380392566.json',
    'input/clippings/mer/224381241715.json',
    'input/clippings/mer/224381744094.json',
    'input/clippings/mer/224382901516.json',
    'input/clippings/mer/224384006179.json',
    'input/clippings/mer/224392077639.json',
    'content/understanding/류상철 국장/경제 교과서 틀렸다 - 물가 때문에 금리 인상해도 주가 오른다.md',
    'content/understanding/언더스탠딩 보고서/2026-08-24-물가-신호를-무시하면-10년이-녹는다.md',
    'content/understanding/미국주식 사관학교/[260115] 기준금리는 내렸는데 10년물은 그대로다 - 물타기는 TLT가 아니라 단기채로.md',
    'content/understanding/미국주식 사관학교/[260318] 인하 논쟁 - 물가가 안 죽었다 대 안 내리면 경기가 먼저 깨진다.md',
    'content/understanding/미국주식 사관학교/[260424] 채권이 주식을 지켜주던 20년은 예외였다 - 갈림길은 물가 3%.md',
    'content/understanding/미국주식 사관학교/[260608] 인상 소나기를 정통으로 맞는 건 중기채다 - 충격이 꽂히는 자리와 가격 반응은 다르다.md',
    'content/understanding/미국주식 사관학교/[260823] 국채가 밀리는 동안 지방채는 물량이 안 늘었다 - 고금리 뉴노멀에서 남는 채권 셋.md',
    'content/understanding/미국주식 사관학교/[260830] 워시는 파월과 다르다, 물가 2%가 찍혀야 움직인다 - 잭슨홀 조정을 저가매수 신호로 읽으면 안 되는 이유.md',
    'content/understanding/회계사/[260802] 채권 자경단, 동결 속에서 30년물 금리를 5.27%로 밀어올리다 - 엘곰.md',
    'content/understanding/회계사/[260819] 30년물이 19년 만의 고점을 찍은 이유 - 엘곰.md',
    'content/understanding/미국주식 사관학교/[260821] 재무부가 바이백을 두 배로 늘렸는데 하루 만에 되돌아왔다 - 30년물 금리와 매수자 교체.md',
    'content/understanding/김상훈 기자/[260806] 엔화를 지켜준 게 아니라 국채를 못 팔게 했다 - 미일 공동개입의 진짜 청구서 - 김상훈.md',
    'content/understanding/박소연 이사/[260806] 금리 방향이 바뀔 때마다 잘하던 방식이 먼저 무너졌다 - 철도채에서 LTCM까지 - 박소연.md',
    'insights/flows/mer/rate_cpi.json',
    'insights/flows/mer/rate_0818.json',
    'insights/debate/issue-2026-08-28-금리와-AI설비투자-무엇이-앞에-서나.md',
)]

# 회사 사실(설립·조달·밸류)은 유튜브 원문이 아니라 회사 공식 사이트에서 온다. 그 조사 파일도
# 대조 대상에 넣는다 — 여기에도 없는 값이면 어디서 왔는지 사람이 대야 한다.
EXTRA = [os.path.join(ROOT, 'scratchpad', 'company_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'company_facts_B.md'),
         # SemiAnalysis 로봇 보고서의 재료 — 원문은 영어 클리핑이라 사실표로 대조한다
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_B.md'),
         # 알파벳 밸류에이션의 재무 숫자와 우리 계산 결과
         os.path.join(ROOT, 'scratchpad', 'googl_facts.md'),
         # 원문 사실과 모형 입력 사이에 낀 판단 — insights/valuation/adjust.py 가 쓴다
         os.path.join(ROOT, 'scratchpad', 'adjust_facts.md'),
         # 빅테크 여섯 비교의 계산 결과
         os.path.join(ROOT, 'scratchpad', 'peers_facts.md'),
         os.path.join(ROOT, 'scratchpad', 'nvda_facts.md')] + CPO_EXTRA + PKG_EXTRA + RATE_EXTRA

# 숫자로 읽히지만 대조할 값이 아닌 것들 — 연·월·일, 절 번호, 흔한 서수
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '2023', '2024', '2025', '2026', '0'}


def norm(t):
    """1,000 · 1000 · 1천 을 같은 자리에 놓기 위한 성긴 정규화."""
    return re.sub(r'[\s,]', '', t)


def corpus(d):
    """재료 글자를 한 덩어리로. d 가 None 이면 EXTRA 에 적은 파일만 본다.

    폴더를 통째로 넣으면 그 층과 무관한 편의 값이 알리바이가 된다. 재료가 여러 폴더에
    흩어진 층(금리·물가는 회계사·미주사·류상철·김상훈·박소연에 걸쳐 있다)은 폴더 대신
    파일을 하나씩 적는다. EXTRA 는 확장자를 안 가려서 json 도 글자로 읽는다.
    """
    out = []
    for base, _dirs, files in os.walk(d) if d else []:
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
