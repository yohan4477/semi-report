# -*- coding: utf-8 -*-
"""모델링 대시보드 — 발표된 계산을 다시 세운 층만 모은 장.

통합 보고서 안 한 섹션으로 있던 것을 2026-09-10 에 떼어 냈다. 층이 열하나로 늘어
한 섹션에 다 들어가지 않았고, 이 장은 다른 층과 재료가 다르다 — 남이 낸 계산기와
그 안의 값을 코드로 다시 세우고 어긋난 칸을 남기는 것이 이 장의 일이다.

카드 한 장이 층 하나다. 본문은 `insights/reports/model-*.md` 가 갖고, 표는
`scratchpad/_capex_tbl.py`·`_model_tbl.py` 가, 도해는 `_capex_fig.py`·`_model_fig.py`
가 낸다. 층 HTML 을 만드는 함수는 `gen_report_dashboard` 에 그대로 두었다 —
두 장이 같은 함수를 쓰므로 한쪽만 고쳐지는 사고가 안 난다.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_model_dashboard.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc          # noqa: E402
import gen_report_dashboard as rp  # noqa: E402
import _rep_toc                    # noqa: E402
import _xlsx_card                  # noqa: E402  받은 엑셀 부록

OUT = os.path.join(dc.ROOT, '대시보드', '모델링 대시보드.html')

HEADER = ('발표된 계산을 다시 세운다. 리서치 회사가 낸 표와 다른 모델이 낸 엑셀을 '
          '옮겨 적는 대신 그 계산을 코드로 다시 세우고, 발표치와 칸 단위로 대조해 '
          '어긋난 자리를 남긴다. 값의 출처는 셋이다 — 원문 글자(줄 번호로 인용), '
          '원문이 실은 표 그림(몇 번 그림인지 밝힌다), 우리 모델이 낸 값(표의 「성격」 '
          '열이 셋을 나눈다).')

FOOTER = ('모델 코드는 <code>insights/models/</code> 에 있고 검사기가 매번 발표치와 '
          '대조한다. 원자료는 <code>insights/models/raw/*.json</code> 이 정본이고, '
          '본문은 <code>insights/reports/model-*.md</code> 다. 이 화면은 생성물이라 '
          '손으로 고치지 않는다.')

# 섹션은 「무엇을 재는 모델인가」로 나눈다. 원문으로 가르지 않는다 — 같은 원문이
# 원가도 물리도 말하는데 원문으로 묶으면 그게 한 칸에 뭉친다.
SEC = {
    'sec-cost': ('01', '원가와 값',
                 '빌려 쓸 때와 사서 쓸 때의 원가, 그리고 그 답이 어디서 뒤집히나'),
    'sec-phys': ('02', '물건과 물리',
                 '칩과 배선과 대역폭 — 돈이 아니라 물건의 수를 세는 자리'),
    'sec-dc': ('03', '데이터센터 자본',
               '메가와트당 얼마가 들고 그 자본이 매출에서 얼마를 먹나'),
    'sec-fin': ('04', '자금 조달',
                '누가 그 돈을 빌려주고, 바닥값과 담보가 이익을 어디로 옮기나'),
    'sec-meet': ('05', '남의 모델과 맞대기',
                 '밖에서 받은 하향 모델의 빈칸에 우리 단가를 넣으면 무엇이 나오나'),
}

# (섹션, 날짜, 제목, 바탕, 한줄, 층 함수)
LAYERS = [
    ('sec-meet', '2026-09-10',
     '받은 엑셀 — 시트 그대로 보기',
     '밖에서 받은 엑셀 3개 · 숫자를 안 고쳤다',
     '우리가 다시 세운 계산이 아니라 남이 낸 표를 그대로 펴 놓은 부록이다',
     _xlsx_card.card_html),
    ('sec-meet', '2026-09-10',
     '자본에서 웨이퍼까지 — 빅4가 쓰는 돈이 세계 파운드리의 10.8퍼센트가 된다',
     'SemiAnalysis 영문 1편의 계수 · 앞 층들의 단가 · 하향 모델의 총액',
     '기가와트당 웨이퍼 35만 4,000장이라는 계수 하나가 돈과 실리콘을 잇는다',
     rp.report_model_waf_html),
    ('sec-meet', '2026-09-10',
     '빅4 자본지출 7,325억 달러 — 우리 단가로 나누면 신규 14~30기가와트다',
     '밖에서 받은 하향 모델 1편(엑셀 3개) · 앞 네 층의 원문 값',
     '돈만 세는 모델과 단가만 있는 모델을 나눠 보면 용량이 나온다',
     rp.report_model_br_html),
    ('sec-dc', '2026-09-10',
     '모듈러 데이터센터 원가 — 메가와트당 8퍼센트 싼데 인건비는 그 5분의 1이다',
     'SemiAnalysis 영문 1편의 본문 값',
     '현장 시간은 62퍼센트가 주는데 원가는 8퍼센트만 준다',
     rp.report_model_lego_html),
    ('sec-dc', '2026-09-10',
     '데이터센터 메가와트당 자본 — 전력을 어디서 끄느냐로 매출의 12~22퍼센트가 자본으로 간다',
     'SemiAnalysis 영문 1편의 본문 값',
     '자본과 전기만으로 매출의 3분의 1이 나가고, 남는 것으로 GPU 를 사야 한다',
     rp.report_model_grd_html),
    ('sec-fin', '2026-09-10',
     'GPU 임대 바닥값(엔비디아 백스톱) — 깔아 준 대가로 청구가의 18퍼센트를 가져간다',
     'SemiAnalysis 영문 1편의 본문 값',
     '바닥값을 받으면 청구가의 18퍼센트를 떼 주고, 안 받으면 이익률에서 9퍼센트포인트가 깎인다',
     rp.report_model_trn_html),
    ('sec-fin', '2026-09-10',
     '컴퓨트 자본 회수 기간 — 「1년」은 비용을 빼기 전 셈이고 빼면 1.32년이다',
     'SemiAnalysis 영문 1편의 본문 값',
     '그 1년은 매출에서 비용을 빼기 전의 셈이다',
     rp.report_model_sx_html),
    ('sec-fin', '2026-09-10',
     'PJM 용량 경매 — 겨울 성능 가정 하나가 두 해 120억 달러 요금이 됐다',
     'SemiAnalysis 영문 1편의 본문 값',
     '공급곡선이 끝에서 수직이라, 요구 용량을 조금만 낮춰도 낙찰가가 반토막 난다',
     rp.report_model_pjm_html),
    ('sec-phys', '2026-09-10',
     '웨이퍼 한 장짜리 칩(세레브라스) — 면적은 462배인데 바깥으로 나가는 통로는 안 는다',
     'SemiAnalysis 영문 1편의 본문 값',
     '데이터가 나가는 통로는 면적이 아니라 가장자리에 붙는다',
     rp.report_model_roof_html),
    ('sec-cost', '2026-09-10',
     '추론 지연 150초 — 그 안에서 대화 속도와 동시 요청과 토큰당 원가를 꺼낸다',
     'SemiAnalysis 영문 2편의 본문 값',
     '원문이 낸 식 하나에서 대화 속도와 동시 요청과 토큰당 원가가 따라 나온다',
     rp.report_model_lat_html),
    ('sec-phys', '2026-09-10',
     'TPU 토러스 배선 — 칩 한 장에 광 트랜시버 1.5개, 격자를 키우면 절반이 된다',
     'SemiAnalysis 영문 1편 · 표 그림 1장',
     '칩이 놓인 자리가 배선을 정하고, 거기서 나온 부착률은 랙 크기에 매여 있다',
     rp.report_model_torus_html),
    ('sec-cost', '2026-09-09',
     'GPU 클러스터 총소유비용 계산기 재현 — 표는 달러까지 맞고 굿풋 세 칸이 공표 수식과 어긋난다',
     'SemiAnalysis 영문 1편 · 표 그림 4장',
     '총소유비용은 달러까지 맞는데 그 안의 굿풋 표가 자기 공표 수식과 어긋난다',
     rp.report_model_cluster_html),
    ('sec-cost', '2026-09-09',
     '추론 원가 AMD 대 엔비디아 — 빌리면 지고 사서 쓰면 작업에 따라 이긴다',
     'SemiAnalysis 영문 1편 · 표 그림 3장',
     '원문은 임대 시세로만 답했는데, 같은 데이터를 소유 기준으로 풀면 답이 뒤집힌다',
     rp.report_model_infer_html),
]


def cards():
    """층 하나 = 카드 하나. 본문은 층 함수가 머리 없이 낸 HTML 을 그대로 끼운다."""
    out = []
    for i, (sid, day, title, base, gain, fn) in enumerate(LAYERS, 1):
        num, tag, _desc = SEC[sid]
        out.append({
            'section': (sid, num, tag, _desc),
            'title': title,
            'gain': gain,
            'meta': [day, base],
            'report': [('raw', fn(head=False))],
        })
    return out


if __name__ == '__main__':
    dc.render(cards(), '모델링', HEADER, FOOTER, OUT,
              page_slug='model',
              extra_css=rp.REPORT_CSS)

    _bad = _rep_toc.check_toc(io.open(OUT, encoding='utf-8').read())
    if _bad:
        raise SystemExit('차례 규약 위반\n  ' + '\n  '.join(_bad))
    print('  차례 규약 OK')
