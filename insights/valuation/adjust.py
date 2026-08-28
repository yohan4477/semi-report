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

# 상태 넷. 나누는 이유가 각각 다르다.
#   적용   값을 알고 모형에 넣었다
#   미적용 값을 알면서 안 넣었다. 왜 안 넣는지가 근거 칸에 있다
#   미측정 **아직** 안 쟀다. 재면 잴 수 있다 — 열린 일이다
#   불가   재봤는데 공시로 못 잰다. **닫힌 일이다**
# 「미측정」과 「불가」를 안 가르면 표가 영영 안 줄어드는 할 일 목록이 된다. 못 재는
# 것을 못 잰다고 확정하는 것도 결과다.
APPLIED, SKIPPED, UNMEASURED, BLOCKED = '적용', '미적용', '미측정', '불가'


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
            'equity_fv_tax', '지분 평가익을 세전이익에서 안 뺀 실효세율을 쓴다', BLOCKED,
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

    # ── 4. 설비투자를 안 나눈다 ───────────────────────────────────
    out.append(_row(
        'capex_split', '유지 설비투자와 성장 설비투자를 안 나눈다', SKIPPED,
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
    out += _useful_life(t)

    # ── 7. 순부채 정의 ────────────────────────────────────────────
    lt, nm = v('lt_investments'), v('nonmarketable_equity')
    _ltv = lt if (lt is not None and not tt['lt_investments'].get('stale_days')) else None
    _nmv = nm if (nm is not None and not tt['nonmarketable_equity'].get('stale_days')) else None
    # 둘은 포함 관계다 — 알파벳은 비시장성 지분이 장기 투자자산 안에 든다. 더하지 않고
    # 넓은 쪽이 최신이면 그것을, 아니면 좁은 쪽을 쓴다.
    _wide = _ltv if _ltv is not None else _nmv
    _lab = '장기 투자자산' if _ltv is not None else '비시장성 지분'
    out.append(_row(
        'net_debt_lt', '순부채에서 장기 투자자산을 안 뺀다',
        SKIPPED if _wide is not None else BLOCKED,
        '주당가치', 'sec' if _wide is not None else 'none', 'W6',
        value=_wide, unit='억 달러',
        shown=('%s %.0f억 달러' % (_lab, _wide * 10)) if _wide is not None
              else '최신 태그가 없다',
        note=('현금과 유동 시장성증권까지만 뺀다. 이 금액은 영업과 무관한 자산이라 '
              '더하자는 주장이 서지만, 팔 수 있는 값이 장부가와 다르고 팔면 세금이 '
              '붙어 그대로 못 더한다. 크기를 밝히고 안 넣는다')
             if _wide is not None else
             '두 태그 모두 손익 기준일에 최신 값이 없다'))

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
    out += _gross_trace(d, t)
    out += _offbs(d, t, fcf)

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
        ('royalty_once', '일회성으로 인식했을 수 있는 로열티를 기준연도에서 안 뺀다',
         '기준 매출과 이익률',
         '[260528] 앤트로픽 성장과 베드락 믹스 L432',
         '필자가 가능성으로 적었고 공시가 매출을 그렇게 안 나눈다. 재봤고 못 재는 것으로 '
         '닫는다 — 회사가 항목을 새로 가르기 전에는 방법이 없다'),
    ],
    'NVDA': [
    ],
}


# 서버 내용연수. XBRL 태그가 아니라 10-K 유의적 회계정책 주석의 문장이라 값을 여기 적고
# accession 을 함께 남긴다. 2026-08-27 에 여섯 회사 10-K 를 읽어 뽑았고, 아마존·메타의
# 손익 영향 수치는 원문에서 직접 확인했다.
#
# **이 표가 말하는 것 하나** — 같은 해(2025년) 같은 자산군에서 두 회사가 **반대로** 갔다.
# 아마존은 인공지능 때문에 기술이 빨리 낡는다며 6년에서 5년으로 줄여 이익을 깎았고,
# 메타는 5.5년으로 늘려 이익을 키웠다. 주당 영향은 메타 +1.00달러, 아마존 -0.10달러다.
# 우리 상대가치 축은 컨센서스 주당순이익으로 내므로 이 선택이 그대로 배수에 들어간다.
_USEFUL_LIFE = {
    'GOOGL': ('6년', '서버와 네트워크 장비를 묶어 6년', None,
              '10-K FY2025 · 0001652044-26-000018'),
    'MSFT': ('2~6년', '서버와 네트워크 장비를 묶어 2~6년', None,
             '10-K FY2026 · 0001193125-26-323660'),
    'NVDA': (None, '서버를 따로 안 구분한다. 장비 전체가 2~7년', None,
             '10-K FY2026 · 0001045810-26-000021'),
    'AMZN': ('5년', '일부 서버·네트워크 장비를 6년에서 5년으로 줄였다(2025-01-01부터)',
             (1.4, -1.0, -0.10), '10-K FY2025 · 0001018724-26-000004'),
    'META': ('5.5년', '대다수 서버·네트워크 자산을 5.5년으로 늘렸다(2025-01-01부터)',
             (-2.92, 2.59, 1.00), '10-K FY2025 · 0001628280-26-003942'),
    'AAPL': (None, '자산군별 내용연수를 공시하지 않는다', None,
             '10-K FY2025 · 0000320193-25-000079'),
}


def _useful_life(t):
    life, how, impact, src = _USEFUL_LIFE[t]
    note = '%s — %s' % (src, how)
    if impact:
        dep, ni, eps = impact
        # 본문이 찍는 형태 그대로 적는다. 자릿수가 다르면 check_report 가 못 찾는다.
        def _b(v):
            v = abs(v) * 10
            return ('%.1f' % v).rstrip('0').rstrip('.') + '억 달러'
        note += ('. 바꾼 해 손익 영향을 회사가 밝혔다 — 감가상각비 %s %s · 순이익 %s %s · '
                 '주당 %.2f달러 %s'
                 % (_b(dep), '늘었다' if dep > 0 else '줄었다',
                    _b(ni), '늘었다' if ni > 0 else '줄었다',
                    abs(eps), '붙었다' if eps > 0 else '깎였다'))
    return [_row('useful_life',
                 '서버 내용연수가 회사마다 다른 것을 배수 비교에서 안 고른다',
                 SKIPPED if life else BLOCKED,
                 '상대가치 축의 선행 주가수익비율', 'sec' if life else 'none', 'W10',
                 shown=life or '공시 안 함', note=note)]



# 재무제표 밖에 있는 약속. 순부채에 **안 더한다** — 더하면 두 번 틀린다.
#   보증 최대노출은 「최대」다. 발동해야 돈이 나가고, 기대손실이 아니다.
#   구매약정은 받을 물건·용역이 맞물려 있어 빚이 아니다.
# 그래도 줄은 세운다. 우리가 순현금 회사라고 부르는 근거가 재무상태표 안쪽만 본 것이라면,
# 바깥에 얼마가 있는지는 적어 두어야 그 말의 뜻이 정해진다.
_OFFBS_SRC = {
    'GOOGL': '[251128] TPUv7 L117 — 임차인이 임대료를 못 낼 때 대신 내겠다는 약속',
    'NVDA': '[260706] 엔비디아 GPU 부채 백스톱 L468 — 발동 전까지 대차대조표 밖에 있다',
}


def _offbs(d, t, fcf):
    tt = d['sec']['ttm']
    out = []
    g = tt.get('guarantee_max')
    if g:
        net_cash = -((tt.get('lt_debt', {}).get('val', 0)
                      + tt.get('st_debt', {}).get('val', 0)
                      - tt.get('cash', {}).get('val', 0)
                      - tt.get('st_investments', {}).get('val', 0)) / B)
        out.append(_row(
            'offbs_guarantee', '보증 최대노출을 순부채에 안 넣는다', SKIPPED,
            '순부채', 'sec', 'W11',
            value=-g['val'] / B, unit='억 달러',
            shown='%.0f억 달러 (%s 기준)' % (-g['val'] / B * 10, g['end']),
            note='%s. 「최대」라 기대손실이 아니고 발동해야 돈이 나가므로 더하지 않는다. '
                 '다만 우리가 더하는 순현금 %.0f억 달러의 %.1f배다'
                 % (_OFFBS_SRC.get(t, '공시 주석'), net_cash * 10,
                    (g['val'] / B) / net_cash if net_cash > 0 else 0)))
    # 구매약정. 알파벳은 이 태그를 잔액이 아니라 기간 값으로 낸다 — 자릿수째로 오해할
    # 자리라 값을 안 쓰고 왜 못 쓰는지만 남긴다.
    # 최근 12개월 값이 안 만들어지는 항목이라 원자료를 본다. concepts 를 보면
    # 연간 기저가 없는 회사가 통째로 빠진다 — 알파벳이 그랬다.
    rawp = (d.get('raw') or {}).get('purchase_long') or []
    if rawp:
        last = rawp[-1]
        out.append(_row(
            'purchase_commit', '장기 구매약정을 순부채에 안 넣는다', BLOCKED,
            '순부채', 'sec', 'W11',
            shown='%s 값이라 잔액이 아니다' % last['kind'],
            note='가장 최근 관측은 %s~%s 에 %.0f억 달러다. start 가 붙은 %s 값이라 '
                 '「남아 있는 약정」이 아니라 그 구간에 쌓인 금액이고, 잔액처럼 더하면 '
                 '자릿수째로 틀린다. 관측이 %d건뿐이라 최근 12개월 값도 못 만든다. '
                 '주석을 읽지 않아 무엇을 담는 수치인지도 아직 모른다'
                 % (last['start'], last['end'], last['val'] / B * 10, last['kind'],
                    len(rawp))))
    return out



# 총액 인식이 연결에 남기는 흔적을 실제로 찾아본 줄. 알파벳만 대상이다 —
# 완제품 시스템 판매가 섞였다는 관찰이 그 회사에만 있다(260807 GCP 편 L154).
#
# **크기는 여전히 못 잰다.** 공시가 클라우드 대여와 시스템 판매를 안 나눈다. 잴 수 있는
# 것은 「원가를 함께 지는 매출이 늘면 눌리는」 매출총이익률의 방향 하나다. 안 눌렸다고
# 없는 것이 아니다 — 연결 규모에 견줘 작거나 마진이 높다는 뜻이고, 그 구분을 적는다.
_TRACE_ON = ('GOOGL',)


def _gross_trace(d, t):
    if t not in _TRACE_ON:
        return []
    gm = d.get('gross_margin') or []
    if len(gm) < 4:
        return [_row('rev_gross', '완제품 시스템 판매가 총액으로 섞인 매출을 그대로 쓴다',
                     UNMEASURED, '기준 매출과 성장 경로', 'none', 'W11',
                     shown='계열이 짧아 못 본다')]
    first, last = gm[0], gm[-1]
    delta = (last['margin'] - first['margin']) * 100
    return [_row(
        'rev_gross', '완제품 시스템 판매가 총액으로 섞인 매출을 그대로 쓴다',
        BLOCKED, '기준 매출과 성장 경로', 'semi', 'W11',
        value=delta, unit='%포인트',
        shown='매출총이익률 %.1f%% → %.1f%% (%+.1f%%포인트)'
              % (first['margin'] * 100, last['margin'] * 100, delta),
        note='[260807] 제미나이는 끝났어도 GCP는 잘나간다 L154 — 크기는 공시가 안 '
             '갈라 못 잰다. %s부터 %s까지 %d분기를 봤고 이익률이 %s. 총액 매출이 크게 '
             '섞였다면 눌려야 하는 방향인데 %s'
             % (first['end'], last['end'], len(gm),
                '올랐다' if delta > 0 else '내렸다',
                '안 눌렸다 — 연결 규모에 견줘 작거나 마진이 높다는 뜻이다' if delta > 0
                else '눌렸다 — 다른 원인과 가릴 수 없으므로 단정하지 않는다'))]


def _observed(t):
    return [_row(k, name, BLOCKED, affects, 'semi', 'W11',
                 shown='공시로 못 잰다', note='%s — %s' % (src, note))
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
            # 줄의 근거 문장에도 값이 들어 있다. 본문이 그 값을 찍으므로 함께 적는다
            if r.get('note'):
                L.append('  - %s' % r['note'])
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
