# -*- coding: utf-8 -*-
"""원문 사실과 모형 입력 사이에 낀 판단을 한 자리에 모은다.

**왜 이 층이 따로 있나.** 케이스 파일 위쪽에는 이런 줄이 있다.

    FCF0 = (t['ocf']['val'] - t['capex']['val']) / B

산수처럼 보인다. 판단 넷이다 — 비현금 가산을 그대로 둘 것인가, 설비투자를 유지분과
성장분으로 가를 것인가, 리스를 셀 것인가, 잉여현금흐름을 이 정의로 잡을 것인가.
넷 다 어디에도 안 적혀 있었다. 판단이 계산 코드 한 줄에 숨으면 읽는 사람 눈에는
산수로 보이므로 리뷰가 안 걸린다. 2026-08-27에 주식보상비용이 그렇게 새어 나갔다.

**그래서 이 파일은 계산을 하지 않는다.** 값을 바꾸지도 않는다. 판단마다 줄 하나를
두고 다섯 칸을 적는다 — 이름 · 적용했나 · 값 · 근거 · 룰북 번호. 「미적용」 줄이
지워지지 않고 값이 붙은 채 남는 것이 이 표의 요점이다. 주식보상비용은 표에 줄조차
없어서 안 보였다.

**값은 손으로 안 적는다.** 전부 facts.json 에서 계산한다. 못 재는 것은 값을 지어내지
않고 상태를 `미측정`으로 둔다 — 안 잰 것을 잰 것처럼 적으면 이 표가 하려는 일이
무너진다.

검사기는 `insights/check_val.py` 가 이 표를 읽어서 돈다.
"""
import io
import json
import os
from datetime import datetime

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = 1e9

TICKERS = ('GOOGL', 'MSFT', 'NVDA', 'AMZN', 'META', 'AAPL')
NAMES = {'GOOGL': '알파벳', 'MSFT': '마이크로소프트', 'NVDA': '엔비디아',
         'AMZN': '아마존', 'META': '메타', 'AAPL': '애플'}

# 미적용 판단이 이 비중을 넘으면 본문에 문장으로 밝혀야 한다. 룰북 W9 가 정한 선이다.
THRESHOLD = 0.20

# 상태 셋. 「미측정」과 「미적용」을 가르는 것이 중요하다 — 앞은 값을 모르는 것이고
# 뒤는 값을 알면서 안 쓴 것이다. 섞으면 모르는 것이 정한 것으로 읽힌다.
APPLIED, SKIPPED, UNMEASURED = '적용', '미적용', '미측정'


def _facts(t):
    p = os.path.join(_root, 'insights', 'valuation', t, 'facts.json')
    return json.load(io.open(p, encoding='utf-8'))


def _row(key, name, state, affects, basis, rule, value=None, unit='', shown=None,
         note='', const=None):
    # const 는 케이스 파일에 박혀 있는 상수 이름이다. check_val 이 「근거 없이 박아 둔
    # 숫자」를 잡을 때, 이 표에 ours 로 등록된 것만 통과시키는 데 쓴다.
    return dict(key=key, name=name, state=state, affects=affects, basis=basis,
                rule=rule, value=value, unit=unit, const=const,
                shown=shown if shown is not None else
                (('%.1f%s' % (value, unit)) if value is not None else '—'),
                note=note)


def rows(t):
    """회사 하나의 조정 표. 값은 전부 facts.json 에서 온다."""
    d = _facts(t)
    s = d['sec']
    tt = s['ttm']
    out = []

    def v(k):
        return tt[k]['val'] / B if k in tt else None

    ocf, cap, sbc = v('ocf'), v('capex'), v('sbc')
    fcf = (ocf - cap) if (ocf is not None and cap is not None) else None

    # ── 1. 비현금 가산 ────────────────────────────────────────────
    # 회사가 임직원에게 새로 찍은 주식을 주고 그 가치를 비용으로 잡은 것이다.
    # 현금이 안 나가 영업현금흐름에 도로 더해져 있으므로 우리 기준값 안에 이미 있다.
    out.append(_row(
        'sbc', '주식보상비용을 도로 더한 채 둔다', SKIPPED,
        '기준 잉여현금흐름', 'sec', 'W9',
        value=(-sbc if sbc is not None else None), unit='억 달러',
        shown=('%.0f억 달러' % (-sbc * 10)) if sbc is not None else '—',
        note='빼면 주주 몫이 묽어지는 만큼이 반영되고, 두면 재투자 여력이 그대로 남는다. '
             '둘 다 서 있어 한쪽으로 안 정한다'))

    # ── 2. 세율 정제 ──────────────────────────────────────────────
    # 알파벳은 보유 지분(앤트로픽·스페이스X 등)을 공정가치로 다시 재 순이익에 태운다.
    # 현금이 아니라 평가액이라 세금이 그만큼 안 붙는데, 세전이익 분모에는 들어간다.
    fv, pre, tax = v('equity_fv_gain'), v('pretax_income'), v('tax_expense')
    # 두 값의 기간 끝이 어긋나면 못 견준다. 메타의 평가익 태그는 2022년이 마지막이라
    # 2026년 세전이익에서 빼면 네 해를 건너뛴 뺄셈이 된다 — check_val V2 가 잡았다.
    _fv_end = (tt.get('equity_fv_gain') or {}).get('end')
    _pre_end = (tt.get('pretax_income') or {}).get('end')
    _aligned = bool(_fv_end and _pre_end and abs(
        (datetime.strptime(_fv_end, '%Y-%m-%d')
         - datetime.strptime(_pre_end, '%Y-%m-%d')).days) <= 10)
    if fv and pre and tax and not _aligned:
        out.append(_row(
            'equity_fv_tax', '지분 평가익을 세전이익에서 안 뺀 실효세율을 쓴다', UNMEASURED,
            '할인율의 부채 절세효과', 'none', 'R3',
            value=None, shown='기간이 %s 대 %s 로 어긋난다' % (_fv_end, _pre_end),
            note='평가익 태그가 최근 기간에 안 나온다. 다른 기간의 값을 빼면 안 되므로 '
                 '재지 않는다'))
    elif fv and pre and tax and abs(fv) > 0 and (pre - fv) > 0:
        raw, cln = tax / pre, tax / (pre - fv)
        out.append(_row(
            'equity_fv_tax', '지분 평가익을 세전이익에서 안 뺀 실효세율을 쓴다', SKIPPED,
            '할인율의 부채 절세효과', 'sec', 'R3',
            value=(cln - raw) * 100, unit='%포인트',
            shown='%.1f%% 대신 %.1f%%' % (raw * 100, cln * 100),
            note='평가익 %.0f억 달러가 분모에 들어가 세율이 절반으로 보인다. '
                 '다만 부채 비중이 작아 할인율에 오는 폭은 0.1%%포인트 아래다'
                 % (fv * 10)))

    # ── 3. 주식수 기준 ────────────────────────────────────────────
    so = (s.get('shares_outstanding') or {}).get('val')
    sd = (s.get('shares_diluted') or {}).get('val')
    if so and sd:
        out.append(_row(
            'shares_basis', '주당가치를 발행주식수로 나눈다(희석 아님)', APPLIED,
            '주당가치', 'sec', 'W9',
            value=(sd / so - 1) * 100, unit='%',
            shown='희석이 %.1f%% 많다' % ((sd / so - 1) * 100),
            note='2번 항목과 같은 뿌리다 — 주식보상이 늘리는 주식 수가 여기로 온다'))

    # ── 4. 설비투자를 안 가른다 ───────────────────────────────────
    out.append(_row(
        'capex_split', '유지 설비투자와 성장 설비투자를 안 가른다', SKIPPED,
        '기준 잉여현금흐름', 'sec', 'R5·R6',
        value=None,
        shown='가를 근거 없음',
        note='공시가 둘을 나눠 내지 않는다. 감가상각을 유지분의 대용으로 쓰는 길이 '
             '있으나 규칙이 없어 안 쓴다'))

    # ── 5. 리스 상각 ──────────────────────────────────────────────
    lease = v('lease_amortization')
    out.append(_row(
        'lease', '리스자산 상각을 감가상각에 안 합친다', SKIPPED,
        '기준 잉여현금흐름', 'sec', 'W6',
        value=(-lease if lease is not None else None), unit='억 달러',
        shown=(('%.0f억 달러 (%s 기준)'
                % (-lease * 10, (tt.get('lease_amortization') or {}).get('end')))
               if lease is not None else '태그 없음'),
        note='합칠지가 회사마다 갈린다. 값만 받아 두고 안 쓴다. 기간을 함께 적는 것은 '
             '분기 공시가 끊긴 회사가 있어서다 — 쓰기로 하면 그때 기간부터 맞춘다'))

    # ── 6. 내용연수 ───────────────────────────────────────────────
    out.append(_row(
        'useful_life', '서버 내용연수 차이를 안 잰다', UNMEASURED,
        '상대가치 축의 선행 주가수익비율', 'none', 'W10',
        value=None, shown='안 쟀다',
        note='몇 년에 걸쳐 상각하느냐가 순이익을 움직이고 그 순이익이 배수에 들어간다'))

    # ── 7. 순부채 정의 ────────────────────────────────────────────
    out.append(_row(
        'net_debt_lt', '순부채에서 장기 투자자산을 안 뺀다', UNMEASURED,
        '주당가치', 'none', 'W6',
        value=None, shown='태그를 안 받는다',
        note='현금·유동 시장성증권까지만 뺀다. 비유동 투자자산은 받지 않아 크기를 모른다'))

    # ── 8·9. 우리가 고른 상수 ─────────────────────────────────────
    out.append(_row(
        'mrp', '시장위험프리미엄을 4.6%로 고정한다', APPLIED,
        '할인율', 'ours', 'W4',
        value=4.6, unit='%', shown='4.6%', const='MRP',
        note='관측이 아니라 우리가 고른 값이다. 알파벳 편에서 정하고 나머지에 옮겼다'))
    out.append(_row(
        'kd', '세전 타인자본비용을 4.5%로 고정한다', APPLIED,
        '할인율', 'ours', 'W4',
        value=4.5, unit='%', shown='4.5%', const='KD_PRE',
        note='출처를 안 적었다. 부채 비중이 작아 값이 거의 안 움직이지만 근거가 없는 '
             '것은 마찬가지다'))

    out += _consts(t)
    out += _observed(t)

    for r in out:
        r['ticker'] = t
        r['company'] = NAMES[t]
        # 기준 잉여현금흐름을 움직이는 줄만 비중을 잰다. 다른 축은 단위가 달라 못 견준다.
        r['share'] = (abs(r['value']) / fcf
                      if (r['value'] is not None and fcf and fcf > 0
                          and r['affects'] == '기준 잉여현금흐름' and r['unit'] == '억 달러')
                      else None)
    return out


# 케이스 파일에 값을 바로 적은 자리. 근거가 주석에만 있으면 리뷰가 안 걸리므로
# 여기에 줄로 세운다. check_val V3 이 이 목록에 없는 상수를 막는다.
_CONSTS = {
    'NVDA': [
        ('GUIDE_Q3', '1년차 기준점을 회사 3분기 가이던스로 잡는다', 'mkt',
         '1,080억 달러(중국 제외). 우리가 고른 값이 아니라 회사가 낸 값이다'),
        ('GUIDE_Q2', '가이던스를 직전 분기 실적에 붙여 읽는다', 'sec',
         '962.2억 달러. 회계연도 2027년 2분기 실적이다'),
        ('CONS_Y2', '2년차 성장률만 우리가 내려 잡는다', 'ours',
         '컨센서스가 2년차를 안 준다. 다음 회계연도 45.0%에서 30%로 내린 값이고 '
         '이 한 칸만 우리 가정이다'),
    ],
}


# 코퍼스에서 건져 올린 줄. SemiAnalysis 69편을 훑어 「공시 숫자가 회계 처리 선택 때문에
# 실제 경제와 어긋난다」는 관찰 열일곱 건을 모았고(2026-08-27), 그중 **우리 여섯 회사의
# 연결 재무제표 입력에 닿는 것**만 여기 세운다.
#
# 사업부 사이에서 옮겨 적는 이야기는 연결에서 씻기므로 뺐다 — 구글 클라우드 영업이익률
# 착시가 그 예다. 사기업(오픈AI·세레브라스·앤트로픽·스페이스X) 이야기도 뺐다. 우리가
# 그 회사를 재지 않는다.
#
# 넷 다 미측정이다. SEC 태그로 크기를 못 재기 때문이고, 못 재는 것을 잰 것처럼 적지
# 않는다. 표에 줄이 있는 것과 값이 있는 것은 다르다 — 줄만 있어도 다음에 눈에 걸린다.
_OBSERVED = {
    'GOOGL': [
        ('rev_gross', '완제품 시스템 판매를 총액으로 잡은 매출을 그대로 기준연도에 쓴다',
         '기준 매출과 성장 경로',
         '[260807] 제미나이는 끝났어도 GCP는 잘나간다 L154',
         '클라우드 대여 매출과 시스템 판매 매출이 한 줄에 섞여 있다. 성격이 달라 '
         '같은 성장률을 계속 곱하면 안 되는데 우리는 그렇게 하고 있다'),
        ('royalty_once', '일회성으로 인식했을 수 있는 로열티를 기준연도에서 안 뺀다',
         '기준 매출과 이익률',
         '[260528] 앤트로픽 성장과 베드락 믹스 L432',
         '필자는 가능성으로 적었고 공시가 따로 가르지 않는다. 크기를 모르므로 안 뺀다'),
        ('offbs_guarantee', '재무제표 밖 신용 보증을 순부채에 안 넣는다', '순부채',
         '[251128] TPUv7 L117',
         '임차인이 임대료를 못 낼 때 대신 내겠다는 약속이다. 발동 전에는 재무상태표에 '
         '안 잡히고 우리 순부채에도 안 들어간다'),
    ],
    'NVDA': [
        ('offbs_backstop', '우발채무로 남은 백스톱을 순부채에 안 넣는다', '순부채',
         '[260706] 엔비디아 GPU 부채 백스톱 L468',
         '발동 전까지 대차대조표 밖에 있다. 발동하면 우리 순부채가 그만큼 늘어난다'),
    ],
}


def _observed(t):
    return [_row(k, name, UNMEASURED, affects, 'semi', 'W11',
                 shown='안 쟀다', note='%s — %s' % (src, note))
            for k, name, affects, src, note in _OBSERVED.get(t, [])]


def _consts(t):
    return [_row('const_' + k.lower(), name, APPLIED, '경로 가정', basis, 'W9',
                 shown='케이스 파일 상수', const=k, note=note)
            for k, name, basis, note in _CONSTS.get(t, [])]


def unapplied(t):
    return [r for r in rows(t) if r['state'] != APPLIED]


def material(t, thr=THRESHOLD):
    """본문에 문장으로 밝혀야 하는 줄. 룰북 W9 의 20% 선을 넘은 미적용 항목이다."""
    return [r for r in unapplied(t) if r['share'] and r['share'] > thr]


def write_facts():
    """check_report 가 대조할 사실표."""
    L = ['# 조정 표 — 기계 대조용', '',
         '자동 생성이다. `python insights/valuation/adjust.py` 가 다시 쓴다.', '',
         '- 본문 명시 임계 %d%%' % (THRESHOLD * 100), '']
    for t in TICKERS:
        L += ['## %s (%s)' % (NAMES[t], t), '']
        for r in rows(t):
            L.append('- %s · %s · %s · 근거 %s · 룰북 %s%s'
                     % (r['name'], r['state'], r['shown'], r['basis'], r['rule'],
                        (' · 잉여현금흐름 대비 %.1f%%' % (r['share'] * 100))
                        if r['share'] else ''))
        m = material(t)
        L.append('- 본문에 밝혀야 하는 줄 %d개%s'
                 % (len(m), (': ' + ' · '.join(x['name'] for x in m)) if m else ''))
        L.append('')
    p = os.path.join(_root, 'scratchpad', 'adjust_facts.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p


def report():
    for t in TICKERS:
        print('\n== %s (%s)' % (NAMES[t], t))
        for r in rows(t):
            print('  %-4s %-34s %-16s %-8s %s'
                  % (r['state'], r['name'][:34], r['shown'], r['rule'],
                     ('%.0f%%' % (r['share'] * 100)) if r['share'] else ''))
        m = material(t)
        if m:
            print('  -> 본문 명시 필요: %s' % ' · '.join(x['name'] for x in m))


if __name__ == '__main__':
    report()
    print('\n사실표 ->', write_facts())
