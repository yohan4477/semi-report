# -*- coding: utf-8 -*-
"""보고서 「모델 총정리」 층의 수식 블록.

원문이 공표한 식을 그대로 낸다. 옮겨 적으면서 기호를 바꾸지 않는다 —
기호를 우리 말로 갈면 원문과 대조할 수 없다. 대신 기호마다 뜻을 붙인다.

각 식에는 우리 코드 어디가 그 식을 계산하는지 적는다. 글과 코드가 갈리면
그 줄이 먼저 눈에 띈다.
"""

# (묶음 제목, 출처, [(왼쪽, 오른쪽, 각주)], [(기호, 뜻)], 코드 자리)
EQ = {
    # ── 클러스터 TCO. 원문 L92·L96·L98 ────────────────────────────────
    'TCO': (
        '월 총비용은 여덟 항의 합이다',
        '클러스터영문 L92·L96·L98',
        [('TCO<sub>$/클러스터·월</sub>',
          'GPU + 저장 + 네트워크 + 컨트롤플레인 + 지원 + 굿풋 + 설치 + 디버깅', ''),
         ('GPU<sub>$/월</sub>', '$<sub>GPU·시간</sub> × #GPU × 720<sub>시간/월</sub>',
          '월을 720시간으로 센다'),
         ('저장<sub>$/월</sub>', '$<sub>GiB·월</sub> × #GiB', ''),
         ('컨트롤플레인<sub>$/월</sub>',
          '$<sub>VM·시간</sub> × #VM × 720<sub>시간/월</sub>', ''),
         ('지원<sub>$/월</sub>', '%할증 × (GPU + 저장 + 네트워크 + 컨트롤플레인)',
          '굿풋·설치·디버깅에는 안 붙는다'),
         ('굿풋<sub>$/월</sub>',
          'G<sub>chkpt-cold</sub> | G<sub>chkpt-hot</sub> | G<sub>tolerant</sub>',
          '복원 방식에 따라 셋 중 하나. 아래에서 편다'),
         ('설치<sub>$/월</sub>', '엔지니어비 × t<sub>설치</sub> ÷ t<sub>계약</sub>',
          '3년 계약이면 36으로 나눈다'),
         ('디버깅<sub>$/월</sub>',
          '엔지니어비 × t<sub>디버깅</sub> + %클러스터시간 × GPU<sub>$/월</sub>', '')],
        [],
        'insights/models/gpu_cluster_tco.py · TcoInputs'),

    # ── 굿풋 셋. 원문 L131·L143 을 기호까지 그대로 ──────────────────────
    'GOOD': (
        '고장이 원가로 바뀌는 식은 셋이다',
        '클러스터영문 L131·L143',
        [('G<sub>chkpt-cold</sub>',
          '[(t<sub>id</sub> + t<sub>chkpt</sub>/2) + t<sub>init</sub> + t<sub>repair</sub>] '
          '× j<sub>size</sub> × #failures × $<sub>GPU-hr</sub>',
          '작업이 수리를 기다린다. 원문이 최악이라고 부른 경우다'),
         ('G<sub>chkpt-hot</sub>',
          '{[(t<sub>id</sub> + t<sub>chkpt</sub>/2) + t<sub>init</sub>] × j<sub>size</sub> '
          '+ t<sub>repair</sub> × b<sub>radius</sub>} × #failures × $<sub>GPU-hr</sub>',
          '수리 시간에는 폭발 반경만 곱한다'),
         ('G<sub>tolerant</sub>',
          '[(t<sub>id</sub> + t<sub>failover</sub>) × j<sub>size</sub> '
          '+ t<sub>repair</sub> × b<sub>radius</sub>] × #failures × $<sub>GPU-hr</sub>',
          '체크포인트 손실이 없다. 작업이 계속 돈다'),
         ('클러스터 MTBF', 'GPU MTBF ÷ 클러스터 장수',
          '원문 L110. 클수록 고장 사이가 짧아진다'),
         ('#failures', '720<sub>시간/월</sub> ÷ 클러스터 MTBF', '')],
        [('t<sub>id</sub>', '고장을 알아차리기까지 걸리는 시간'),
         ('t<sub>chkpt</sub>', '체크포인트 주기. 평균 손실은 그 절반이다'),
         ('t<sub>init</sub>', '작업을 다시 띄우는 시간'),
         ('t<sub>repair</sub>', '노드를 고치거나 바꾸는 시간(MTTR)'),
         ('t<sub>failover</sub>', '뜨거운 예비 노드로 넘어가는 시간'),
         ('b<sub>radius</sub>', '폭발 반경. 한 번 고장에 함께 내려앉는 최소 단위'),
         ('j<sub>size</sub>', '평균 작업 크기'),
         ('$<sub>GPU-hr</sub>', 'GPU 한 장을 한 시간 쓰는 값')],
        'insights/models/gpu_cluster_tco.py · goodput_lost_gpu_hours'),

    # ── 추론 원가. 원문 L442·L446 과 표 그림 049·050 에서 읽어 세운 것 ──
    'INF': (
        '서버 값이 시간당 단가가 되는 식',
        'AMD영문 L442·L446 + 그림 049·050',
        [('선불<sub>서버당</sub>', '서버 값 + 서비스·망·저장·소프트웨어', ''),
         ('월 자본비', '선불 × r ÷ [1 − (1 + r)<sup>−n</sup>]',
          'r = WACC ÷ 12, n = 4년 × 12. 단순히 48로 나누는 것이 아니다'),
         ('전기<sub>kW·월</sub>',
          '$<sub>kWh</sub> × 730<sub>시간/월</sub> × 가동률 × PUE',
          '이 글은 월을 730시간으로 센다. 앞 글의 클러스터 원가 글은 720시간이다'),
         ('호스팅<sub>서버·월</sub>', '(전기<sub>kW·월</sub> + 코로케이션<sub>kW·월</sub>)'
          ' × 서버 전력<sub>kW</sub>', ''),
         ('운영비<sub>서버·월</sub>', '호스팅 + 상면 인건비 + 회선', ''),
         ('$<sub>GPU-시간</sub>', '(월 자본비 + 월 운영비) ÷ (8 × 730)',
          '서버 한 대에 GPU 여덟 장'),
         ('$<sub>백만 토큰</sub>',
          '$<sub>GPU-시간</sub> ÷ (초당 토큰 × 3,600) × 1,000,000',
          '원문은 이 값을 곡선으로만 냈다. 이 글은 여기까지 안 갔다')],
        [('WACC', '가중평균자본비용. 빌린 돈과 자기 돈을 섞어 조달할 때 붙는 연 할인율'),
         ('PUE', '전력사용효율. IT 장비 1와트를 쓰려고 실제로 끌어오는 전력의 배수'),
         ('가동률', '장비가 실제로 돌아간 시간의 몫. 전기는 이만큼만 쓴다')],
        'insights/models/inference_tco.py · levelized_monthly · Opex'),

    # ── 우리가 세운 식 둘. 원문에 없다 ──────────────────────────────────
    'OURS': (
        '원문에 없고 이 글이 세운 식 둘',
        '우리 계산',
        [('상대 처리량', '손익분기 임대료 ÷ 기준 SKU 임대료',
          '토큰당 원가가 같아지려면 시간당 값의 비율이 처리량 비율과 같아야 한다'),
         ('소유 문턱', '$<sub>GPU-시간</sub> ÷ 기준 SKU $<sub>GPU-시간</sub>',
          '빌리는 값이 아니라 자기 TCO 로 견줄 때 넘어야 할 처리량 비율')],
        [],
        'insights/models/inference_tco.py · implied_throughput_ratio'),
}


def eq_html(key):
    """수식 한 묶음. 왼쪽에 이름, 오른쪽에 식, 아래에 기호 뜻."""
    title, src, rows, terms, code = EQ[key]
    h = ['<div class="eqbox">',
         '<div class="eqhead"><b>%s</b><span class="eqsrc">%s</span></div>' % (title, src)]
    for lhs, rhs, note in rows:
        h.append('<div class="eqrow"><div class="eqlhs">%s</div>'
                 '<div class="eqrhs"><span class="eqop">=</span> %s%s</div></div>'
                 % (lhs, rhs,
                    '<div class="eqnote">%s</div>' % note if note else ''))
    if terms:
        h.append('<div class="eqterms">')
        for sym, mean in terms:
            h.append('<div class="eqterm"><span class="eqsym">%s</span>%s</div>'
                     % (sym, mean))
        h.append('</div>')
    h.append('<div class="eqcode">계산하는 자리 — <code>%s</code></div>' % code)
    h.append('</div>')
    return ''.join(h)


def all_text():
    """수식에 든 숫자를 글자로. 사실표가 받아 check_report 의 대조 재료로 쓴다."""
    out = []
    for key, (title, src, rows, terms, code) in EQ.items():
        out.append('### 수식 %s — %s (%s)' % (key, title, src))
        for lhs, rhs, note in rows:
            plain = (lhs + ' = ' + rhs + (' — ' + note if note else ''))
            for a, b in (('<sub>', '_'), ('</sub>', ''), ('<sup>', '^'), ('</sup>', '')):
                plain = plain.replace(a, b)
            out.append(plain)
        out.append('')
    return '\n'.join(out)
