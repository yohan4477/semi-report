# -*- coding: utf-8 -*-
"""AI 비즈니스 리포트 전수 대조 — 재료로 선언한 뉴스레터가 본문에 다 나왔나.

insight-report §1 의 대조를 뉴스레터 코퍼스에 맞춘 것이다. 카드가 아니라
content/newsletter 변환본이 재료라 제목 대신 편마다 고른 고유어로 견준다.
"""
import os
if not os.path.exists('대시보드/통합 보고서.html'):
    raise SystemExit('건너뜀 — 통합 보고서 화면이 없다. 생성기를 돌리면 다시 생긴다')
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (편 이름, 그 편에만 나오는 말 여럿 중 하나라도 본문에 있으면 실린 것으로 본다)
MATERIAL = [
    ('260501 AI 가치 포착', ['SOCAMM', '와트당 자본지출', 'Opus 4.5']),
    ('260420 TCO·굿풋', ['굿풋']),
    ('260402 H100 임대 지수', ['H100 1년 계약 지수', '1.70달러']),
    ('260630 토큰 버짓팅', ['하드 캡', '워크데이']),
    ('260528 AWS 마진', ['베드락']),
    ('260708 앤트로픽 흑자', ['IPO', '9억 명']),
    ('260706 GPU 부채 백스톱', ['백스톱', '보증선']),
    ('260611 인텔 자본조달', ['인텔']),
    ('260702 메타 컴퓨트', ['코로케이션']),
    ('260709 메타 슈퍼인텔리전스', ['3,000명', '143억']),
    ('260107 RL 환경', ['데이터 파운드리', 'Surge']),
    ('250609 RL 스케일링', ['강화학습']),
    ('260616 RL 시스템', ['과제와 채점 기준']),
    ('260207 메모리 마니아', ['DDR5', 'HBM']),
    ('260626 전력망 제약', ['자가발전', 'BTM']),
    ('260303 가정 전기요금', ['ERCOT', '뉴저지']),
    ('260816 PJM 120억 달러', ['예비율 19.95', '120억 달러']),
    ('260729 레고 데이터센터', ['모듈러', '애빌린']),
    ('260521 EDA 시장', ['시놉시스', '케이던스']),
    ('260725 CUDA 모트', ['ATOM']),
    ('260824 AgentX InferenceXv3', ['AgentX', 'Dynamo']),
    ('260216 InferenceX v2', ['wideEP', 'MI355X']),
    ('260821 오픈 모델', ['파이어웍스', '40조']),
    ('260529 다크 아웃풋', ['다크 아웃풋', '유언장']),
    ('260807 스페이스X 10GW', ['90일', '120억 달러']),
    ('260807 GCP 반사이익', ['구글 클라우드', '제미나이']),
    ('260603 우주 데이터센터', ['우주 데이터센터']),
    ('260623 CXMT', ['CXMT', '키몬다']),
    ('260108 애플-TSMC', ['앵커', '240억 달러']),
    ('260425 코딩 어시스턴트', ['토크나이저', 'GPT-5.5']),
]


def main():
    h = io.open(os.path.join(ROOT, '대시보드', '통합 보고서.html'), encoding='utf-8').read()
    i = h.find('id="sec-biz"')
    txt = re.sub(r'<[^>]+>', ' ', h[i:h.find('</section>', i)])
    miss = [n for n, keys in MATERIAL if not any(k in txt for k in keys)]
    for n in miss:
        print('빠짐 %s' % n)
    print('요약: 재료 %d편 / 빠짐 %d편' % (len(MATERIAL), len(miss)))


if __name__ == '__main__':
    main()
