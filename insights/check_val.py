# -*- coding: utf-8 -*-
"""숫자 파이프라인 게이트.

**왜 필요한가.** 이 저장소에는 검사기가 여섯 있는데 여섯 다 산문만 본다. 정작 우리가
가장 자주 틀리는 자리는 숫자 쪽이었다. 2026-08-27까지 밸류에이션에서 나온 결함 다섯 중
검사기가 잡은 것은 하나도 없다 — 최근 12개월 값이 한 해 전 연간을 기저로 삼은 것,
재무상태표 날짜가 섞인 것, 할인율이 0.10으로 박혀 있는데 본문은 계산했다고 적은 것,
부호가 뒤집힌 것, 주식보상비용이 기준값에 통째로 들어가 있던 것. 넷은 사용자가 물어서
걸렸고 하나는 다른 값을 고치다 우연히 걸렸다.

**무엇을 보나.** 판단이 아니라 단언만 본다. 「주식보상비용을 빼야 하나」는 사람 몫이다.
「우리 기준값이 그 항목에 절반을 기대고 있는데 본문에 그 말이 없다」는 기계 몫이다.

    V1  조정 표의 미적용 항목이 임계를 넘었는데 본문에 안 나온다
    V2  최근 12개월 값들의 기간 끝이 서로 어긋난다
    V3  케이스 파일에 근거 없이 박아 둔 실수 상수가 있다
    V4  조정 표에 미측정으로 남은 줄 (WARN — 세어서 보이기만 한다)

조정 표는 `insights/valuation/adjust.py` 다. 이 검사기는 그 표를 읽을 뿐 판단을 더하지
않는다 — 판단이 코드로 새어 들어가면 이 검사기 자체가 다음 결함이 된다.

    PYTHONIOENCODING=utf-8 python insights/check_val.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights', 'valuation'))
import adjust                                                   # noqa: E402

DASH = os.path.join(ROOT, '대시보드', '통합 보고서.html')
CASES = os.path.join(ROOT, 'scratchpad')

# 기간 끝이 이만큼 넘게 벌어지면 서로 다른 시점을 한 비율에 넣은 것이다.
# 회사마다 분기 마감일이 며칠씩 달라 0일로는 못 잡는다.
DATE_TOL = 10

# 같은 계산에 함께 들어가는 값들. 이 안에서 기간이 어긋나면 서로 다른 시점을 한 비율에
# 넣은 것이다. 묶음 밖 태그는 공시 주기가 달라 뒤처질 수 있어 경고로만 낸다.
GROUPS = [
    # 지금 잉여현금흐름·마진에 실제로 들어가는 값만 묶는다. 받아만 두고 안 쓰는
    # 태그를 여기 넣으면 공시 주기 차이가 결함으로 둔갑한다.
    ('기간 값', ('revenue', 'ebit', 'ocf', 'capex', 'dna', 'sbc', 'net_income',
                'pretax_income', 'tax_expense')),
    ('재무상태표', ('cash', 'st_investments', 'lt_debt', 'st_debt',
                 'receivables', 'payables', 'inventory')),
]
LOOSE = ('cash_taxes_paid', 'equity_fv_gain', 'nonoperating',
         'lease_amortization')

# 미적용 항목이 본문에 나왔는지 볼 때 찾을 말. 표의 key 마다 후보 여럿을 두고
# 하나라도 있으면 통과다.
#
# **짧은 낱말을 쓰지 않는다.** 「리스」로 뒀더니 「애널리스트」에 열네 번 걸려 오탐으로
# 통과했다. 진짜 언급은 한 번뿐이었다. 다른 말에 안 묻히는 길이로 잡는다.
MENTION = {
    'sbc': ('주식보상',),
    'lease': ('리스자산', '금융리스', '리스 상각'),
    'capex_split': ('유지 설비투자', '유지분과 성장분'),
    'equity_fv_tax': ('지분 평가익', '평가익을'),
    'useful_life': ('내용연수',),
    'net_debt_lt': ('장기 투자자산',),
}

# 밸류에이션 절만 본다. 네 절짜리 문서에서 다른 절의 언급이 게이트를 통과시키면
# 「그 값을 쓴 자리에 밝혔다」가 아니라 「어딘가에 그 말이 있다」가 된다.
SECTION = 'sec-val'


def _text(path, section=None):
    if not os.path.exists(path):
        return ''
    h = io.open(path, encoding='utf-8').read()
    if section:
        m = re.search(r'id="%s"' % re.escape(section), h)
        if not m:
            return ''
        end = h.find('</section>', m.start())
        h = h[m.start():end if end > 0 else len(h)]
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))


def v1_material_disclosed(txt, out):
    """임계를 넘은 미적용 항목은 본문에 문장으로 있어야 한다 (룰북 W9)."""
    for t in adjust.TICKERS:
        for r in adjust.material(t):
            words = MENTION.get(r['key'])
            if words and not any(w in txt for w in words):
                out.append(('FAIL', 'V1',
                            '%s %s가 잉여현금흐름의 %.0f%%인데 밸류에이션 절에 '
                            '「%s」가 없다'
                            % (adjust.NAMES[t], r['name'], r['share'] * 100,
                               '」·「'.join(words))))


def v2_period_aligned(out):
    """한 계산에 함께 들어가는 값들의 기간이 맞나.

    파일 안 모든 태그를 한 줄에 세우지 않는다. 현금납부세액은 연간 공시만 있어 늘
    반년 뒤처지고, 그것은 결함이 아니라 공시 주기다. 잡아야 하는 것은 **같은 비율에
    함께 들어가는 값들**이 서로 다른 시점인 경우다 — 재무상태표 태그 하나가 한 해
    낡은 채 순현금에 들어갔던 것이 그 사고였다.
    """
    from datetime import datetime
    for t in adjust.TICKERS:
        p = os.path.join(ROOT, 'insights', 'valuation', t, 'facts.json')
        if not os.path.exists(p):
            out.append(('FAIL', 'V2', '%s facts.json 이 없다' % t))
            continue
        tt = json.load(io.open(p, encoding='utf-8'))['sec'].get('ttm', {})
        if not tt:
            out.append(('FAIL', 'V2', '%s 최근 12개월 값이 통째로 비었다' % t))
            continue
        for gname, keys in GROUPS:
            ends = {k: tt[k]['end'] for k in keys
                    if isinstance(tt.get(k), dict) and tt[k].get('end')}
            if len(ends) < 2:
                continue
            ds = {k: datetime.strptime(e, '%Y-%m-%d') for k, e in ends.items()}
            lo, hi = min(ds, key=lambda k: ds[k]), max(ds, key=lambda k: ds[k])
            gap = (ds[hi] - ds[lo]).days
            if gap > DATE_TOL:
                out.append(('FAIL', 'V2',
                            '%s %s 묶음의 기간이 %d일 벌어졌다 — %s(%s) 와 %s(%s)'
                            % (adjust.NAMES[t], gname, gap, lo, ends[lo], hi, ends[hi])))
        # 묶음 밖 태그가 낡은 것은 막지 않고 보이게만 둔다. 쓰는 자리에서 가드를 건다.
        base = (tt.get('revenue') or {}).get('end')
        if base:
            b = datetime.strptime(base, '%Y-%m-%d')
            for k in LOOSE:
                e = (tt.get(k) or {}).get('end')
                if e and (b - datetime.strptime(e, '%Y-%m-%d')).days > 200:
                    out.append(('WARN', 'V2', '%s %s 가 기준일보다 %d일 낡았다 — '
                                '쓰는 자리에서 기간을 맞춰 본다'
                                % (adjust.NAMES[t], k,
                                   (b - datetime.strptime(e, '%Y-%m-%d')).days)))
        # 낡은 잔액은 **계산에 들어가는 것만** 막는다. 순현금·운전자본에 들어가는 시점
        # 값이 한 해 낡은 채 실렸던 것이 그 사고였다. 받아만 두고 안 쓰는 태그(구매약정
        # 따위)까지 막으면 공시 주기가 결함으로 둔갑한다 — 리스 때 한 번 겪었다.
        used = set(GROUPS[1][1])
        unused_stale = []
        for k, x in tt.items():
            if not (isinstance(x, dict) and (x.get('stale_days') or 0) > DATE_TOL):
                continue
            if k in used:
                out.append(('FAIL', 'V2', '%s %s 가 기준일보다 %d일 낡았다'
                            % (adjust.NAMES[t], k, x['stale_days'])))
            else:
                unused_stale.append(k)
        # 안 쓰는 값이 낡은 것은 공시 주기 차이다. 회사마다 한 줄로 접는다 —
        # 줄줄이 세우면 없어지지 않는 경고가 쌓여 진짜 경고를 덮는다.
        if unused_stale:
            out.append(('INFO', 'V2', '%s 안 쓰는 값 %d개가 낡았다(%s)'
                        % (adjust.NAMES[t], len(unused_stale),
                           '·'.join(sorted(unused_stale)))))


# 모듈 최상단에서 대문자 이름에 소수 리터럴을 바로 붙인 자리. 계산에서 온 값은
# 오른쪽이 리터럴이 아니므로 안 걸린다. 연도 수 같은 정수도 안 본다 — 자릿수가 아니라
# 「근거 없이 고른 비율」을 찾는 것이다.
CONST = re.compile(r'^([A-Z][A-Z0-9_]*)\s*=\s*(\d+\.\d+)\s*(?:#.*)?$', re.M)


def v3_no_bare_constants(out):
    """케이스 파일에 박아 둔 실수는 조정 표에 ours 로 등록돼 있어야 한다."""
    # 근거가 무엇이든(회사 공시든 컨센서스든 우리 판단이든) 표에 줄이 있으면 통과다.
    # 막으려는 것은 「값이 어디서 왔는지 아무 데도 안 적힌 상수」다.
    known = {r['const'] for t in adjust.TICKERS for r in adjust.rows(t)
             if r.get('const')}
    for fn in sorted(os.listdir(CASES)):
        if not fn.endswith('_cases.py'):
            continue
        src = io.open(os.path.join(CASES, fn), encoding='utf-8').read()
        for name, lit in CONST.findall(src):
            if name not in known:
                out.append(('FAIL', 'V3',
                            '%s 의 %s = %s 가 조정 표에 없다 — 값을 어디서 골랐는지 '
                            'adjust.py 에 줄을 세운다' % (fn, name, lit)))


def v4_unmeasured(out):
    """**아직 안 잰** 줄만 센다. 「불가」는 안 센다.

    둘을 섞으면 표가 영영 안 줄어드는 할 일 목록이 된다. 공시가 안 갈라 못 재는 것을
    못 잰다고 확정하는 것도 결과이고, 그런 줄은 경고가 아니라 기록이다.
    """
    seen, blocked = {}, {}
    for t in adjust.TICKERS:
        for r in adjust.rows(t):
            if r['state'] == adjust.UNMEASURED:
                seen.setdefault(r['key'], set()).add(adjust.NAMES[t])
            elif r['state'] == adjust.BLOCKED:
                blocked.setdefault(r['key'], set()).add(adjust.NAMES[t])
    for k, who in sorted(seen.items()):
        out.append(('WARN', 'V4', '아직 안 쟀다: %s — %d곳(%s)'
                    % (k, len(who), '·'.join(sorted(who)))))
    if blocked:
        out.append(('INFO', 'V4', '공시로 못 재는 것으로 닫은 줄 %d종 · %d곳'
                    % (len(blocked), sum(len(v) for v in blocked.values()))))


def main():
    txt = _text(DASH, SECTION)
    out = []
    if not txt:
        out.append(('FAIL', 'V1',
                    '통합 보고서.html 의 %s 절을 못 읽었다' % SECTION))
    else:
        v1_material_disclosed(txt, out)
    v2_period_aligned(out)
    v3_no_bare_constants(out)
    v4_unmeasured(out)

    for lv, code, msg in out:
        print('%s [%s] %s' % (lv, code, msg))
    f = sum(1 for x in out if x[0] == 'FAIL')
    w = sum(1 for x in out if x[0] == 'WARN')
    i_ = sum(1 for x in out if x[0] == 'INFO')
    _rows = [r for t in adjust.TICKERS for r in adjust.rows(t)]
    _st = ' · '.join(
        '%s %d' % (k, sum(1 for r in _rows if r['state'] == k))
        for k in (adjust.APPLIED, adjust.SKIPPED, adjust.UNMEASURED, adjust.BLOCKED))
    n = len(_rows)
    print('\n요약: 회사 %d곳 / 조정 %d줄 (%s) / FAIL %d / WARN %d / INFO %d'
          % (len(adjust.TICKERS), n, _st, f, w, i_))
    return 1 if f else 0


if __name__ == '__main__':
    sys.exit(main())
