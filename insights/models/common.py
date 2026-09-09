"""모델 여럿이 같이 쓰는 뼈대.

모델을 하나씩 세울 때마다 같은 함수를 다시 쓰다가 값이 갈렸다 — 클러스터 글은
월을 720시간으로 세고 추론 글은 730시간으로 센다. 시간 상수를 모델마다 박아 두면
어느 쪽 값인지 부르는 자리에서 안 보인다. 그래서 시간은 인자로 받고, 기본값을 두지
않는다.

원자료는 `insights/models/raw/` 의 JSON 이 정본이다. 모델은 그 파일을 읽고, 그림에서
읽은 값을 코드에 다시 적지 않는다.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, 'insights', 'models', 'raw')

MONTHS_PER_YEAR = 12


def load_raw(name):
    """원자료 JSON 하나를 읽는다. 이름은 확장자 없이."""
    p = os.path.join(RAW, name + '.json')
    return json.loads(io.open(p, encoding='utf-8').read())


def table(raw, table_id):
    """원자료에서 표 하나를 꺼낸다. 없으면 어떤 표가 있는지 알려 준다."""
    for t in raw.get('tables', []):
        if t.get('id') == table_id:
            return t
    have = ', '.join(t.get('id', '?') for t in raw.get('tables', []))
    raise KeyError('그런 표가 없다: %s (있는 것: %s)' % (table_id, have))


def col(t, name):
    """표의 열 하나를 이름으로 꺼낸다. 행 이름 → 그 열의 값."""
    i = t['columns'].index(name)
    return {k: (v[i] if isinstance(v, list) else v) for k, v in t['rows'].items()}


def levelized_monthly(principal, wacc_annual, years):
    """선불액을 내용연수에 걸쳐 매달 같은 금액으로 편다.

    자본비용이 붙는 원리금 균등 상환이다. 단순 나눗셈이 아니라서 WACC 13.25%,
    4년이면 원금의 약 1.29배를 갚는다.
    """
    r = wacc_annual / MONTHS_PER_YEAR
    n = years * MONTHS_PER_YEAR
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def implied_rate(principal, monthly_payment, years, lo=0.0, hi=1.0):
    """발표된 월 상환액에서 실제 쓰인 할인율을 역산한다.

    표에 찍힌 값이 반올림된 표시값일 때, 여러 대상이 한 값으로 모이면 그것이
    실제 값이다. 추론 원가 표에서 13.3%가 13.25%였던 자리가 이 함수로 나왔다.
    """
    for _ in range(200):
        mid = (lo + hi) / 2
        if levelized_monthly(principal, mid, years) < monthly_payment:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def hourly_from_monthly(monthly, units, hours_per_month):
    """월 비용을 단위당 시간당 값으로. 시간은 반드시 받는다 — 글마다 다르다."""
    return monthly / units / hours_per_month


def per_million_tokens(hourly, tokens_per_sec):
    """시간당 값을 처리량으로 나눠 백만 토큰당 원가로. 낮을수록 좋다."""
    return hourly / (tokens_per_sec * 3600) * 1_000_000


def ratio_threshold(a_hourly, b_hourly):
    """b 를 1 로 놓았을 때 a 가 넘어야 하는 처리량 비율.

    토큰당 원가가 같아지려면 시간당 값의 비율이 처리량 비율과 같아야 한다.
    """
    return a_hourly / b_hourly


class Compare(object):
    """발표치와 모델값을 칸마다 대조한다. 어긋난 칸을 지우지 않고 세운다."""

    def __init__(self, name):
        self.name = name
        self.rows = []

    def add(self, label, got, want, tol):
        ok = want is None or abs(got - want) <= tol
        self.rows.append((label, got, want, tol, ok))
        return ok

    @property
    def fails(self):
        return [r for r in self.rows if not r[4]]

    def report(self, out=None):
        lines = ['── %s ' % self.name + '─' * max(0, 60 - len(self.name))]
        for label, got, want, _tol, ok in self.rows:
            mark = '' if ok else '  FAIL'
            w = '—' if want is None else ('%,.4f' % want).replace(',', ',')
            lines.append('%-34s %14.4f %14s%s' % (label, got, w, mark))
        lines.append('  어긋난 칸: %d / %d' % (len(self.fails), len(self.rows)))
        text = '\n'.join(lines)
        if out is not None:
            out.write(text + '\n')
        return text
