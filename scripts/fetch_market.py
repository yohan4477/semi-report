# -*- coding: utf-8 -*-
"""네이버 증권 모바일 API에서 시세·분기(연간)실적을 받아 insights/valuation/에 저장한다.

- 브라우저·로그인 불필요, 공개 JSON API를 그대로 두드린다(User-Agent·Referer만 필요)
- finance/quarter·finance/annual은 같은 모양(financeInfo.trTitleList·rowList)이라 파서 하나를 공유한다
- isConsensus "Y"(증권사 전망치)와 "N"(확정 실적)을 절대 섞으면 안 된다 — 밸류에이션이 통째로 틀어진다
- 검증 실패는 파일을 쓰지 않고 종료 코드 1로 죽는다. 조용히 틀린 값이 들어가는 게 최악이다
- 출력은 price.json/fundamentals.json/meta.json 세 파일로 쪼갠다. 바뀌는 주기가 다르기 때문이다
  (주가는 매 영업일, 실적은 발표 때만, 메타는 거의 안 바뀜) — 한 파일에 두면 주가 한 줄 때문에
  매일 커밋되면서 실적 diff까지 묻혀서 "무엇이 실제로 바뀌었나"가 안 보인다
- fetched_at을 뺀 나머지가 파일별로 기존 것과 같으면 그 파일만 건드리지 않는다

사용: PYTHONIOENCODING=utf-8 python scripts/fetch_market.py 005930
"""
import io
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALUATION_DIR = os.path.join(ROOT, "insights", "valuation")

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://m.stock.naver.com/",
}

KST = timezone(timedelta(hours=9))

# 상장주식수는 네이버 API 어디에도 명시 필드가 없다(integration의 marketValue는
# "조/억" 단위로 반올림돼 있어 역산하면 종목코드 하나만 틀려도 오차가 수만 주 난다).
# 그래서 확인된 값만 상수로 박아 둔다. 목록에 없는 종목은 shares 없이 나간다.
KNOWN_SHARES = {
    "005930": 5846278608,  # 삼성전자, 2026-08 기준
}


def fail(msg):
    """검증 실패 메시지를 stderr에 찍고 종료 코드 1로 죽는다. 호출 뒤로는 실행되지 않는다."""
    sys.stderr.write(f"[fetch_market] 실패: {msg}\n")
    sys.exit(1)


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        fail(f"HTTP 요청 실패 — {url} ({e})")
    except TimeoutError as e:
        fail(f"HTTP 요청 시간 초과 — {url} ({e})")
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        fail(f"JSON 파싱 실패 — {url} ({e})")


def parse_int(s):
    """쉼표 섞인 한글 숫자 문자열을 정수로. "-"나 빈 값은 None(그 키를 아예 빼기 위함)."""
    if s is None:
        return None
    s = str(s).strip()
    if s == "" or s == "-":
        return None
    s = s.replace(",", "")
    try:
        return int(s)
    except ValueError:
        return None


def extract_cell(raw):
    """columns[key] 값이 "66,853" 같은 문자열일 수도, {"value":"66,853","cx":null} 형태일 수도 있다."""
    if raw is None:
        return None
    if isinstance(raw, dict):
        return raw.get("value")
    return raw


def parse_finance_periods(finance_json):
    """finance/quarter·finance/annual 공용 파서. trTitleList 순서대로 기간 목록을 만든다."""
    info = finance_json.get("financeInfo") or {}
    tr_list = info.get("trTitleList") or []
    row_list = info.get("rowList") or []
    rows_by_title = {row.get("title"): (row.get("columns") or {}) for row in row_list}

    field_map = (
        ("매출액", "revenue_100m"),
        ("영업이익", "operating_profit_100m"),
        ("당기순이익", "net_income_100m"),
    )

    periods = []
    for tr in tr_list:
        key = tr.get("key")
        if not key:
            continue
        label = (tr.get("title") or "").rstrip(".")
        consensus = tr.get("isConsensus") == "Y"
        entry = {"key": key, "label": label, "consensus": consensus}
        for title_kr, field_name in field_map:
            cols = rows_by_title.get(title_kr, {})
            value = parse_int(extract_cell(cols.get(key)))
            if value is not None:
                entry[field_name] = value
        periods.append(entry)
    return periods


def resolve_change(basic):
    """compareToPreviousClosePrice엔 부호가 없다. compareToPreviousPrice.name으로 부호를 붙인다."""
    raw = parse_int(basic.get("compareToPreviousClosePrice"))
    if raw is None:
        return None
    direction = ((basic.get("compareToPreviousPrice") or {}).get("name") or "").upper()
    if direction == "FALLING":
        return -raw
    return raw


def load_json(path):
    """파일이 없거나 깨졌으면 None. 존재 비교는 여기서 하지 않는다(호출부 책임)."""
    if not os.path.exists(path):
        return None
    with io.open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return None


def same_ignoring_fetched_at(existing, new):
    if existing is None:
        return False
    a = dict(existing)
    a.pop("fetched_at", None)
    b = dict(new)
    b.pop("fetched_at", None)
    return a == b


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    if len(sys.argv) != 2:
        fail("종목코드를 하나만 인자로 넘겨라. 예: python scripts/fetch_market.py 005930")
    ticker = sys.argv[1].strip()
    if not ticker.isdigit():
        fail(f"종목코드가 숫자가 아니다: {ticker!r}")

    basic_url = f"https://m.stock.naver.com/api/stock/{ticker}/basic"
    quarter_url = f"https://m.stock.naver.com/api/stock/{ticker}/finance/quarter"
    annual_url = f"https://m.stock.naver.com/api/stock/{ticker}/finance/annual"

    basic = fetch_json(basic_url)
    quarter_json = fetch_json(quarter_url)
    annual_json = fetch_json(annual_url)

    name = basic.get("stockName")
    if not name:
        fail(f"stockName이 없다 — basic 응답 구조가 바뀐 것 같다: {basic_url}")

    close_price = parse_int(basic.get("closePrice"))
    if close_price is None:
        fail(f"closePrice가 없다 — basic 응답 구조가 바뀐 것 같다: {basic_url}")
    if not (1000 <= close_price <= 10_000_000):
        fail(f"closePrice({close_price})가 정상 범위(1,000~10,000,000원) 밖이다 — {basic_url}")

    quarters = parse_finance_periods(quarter_json)
    annuals = parse_finance_periods(annual_json)

    if len(quarters) < 4:
        fail(
            f"분기가 {len(quarters)}개뿐이다(4개 이상 필요) — "
            f"finance/quarter 응답 구조가 바뀐 것 같다: {quarter_url}"
        )
    if not any(not q["consensus"] for q in quarters):
        fail(
            f"확정(consensus:false) 분기가 하나도 없다 — 전부 컨센서스면 실적이 아니라 "
            f"전망치만 받은 것이다: {quarter_url}"
        )
    if not any("operating_profit_100m" in q for q in quarters):
        fail(
            f"어느 분기에도 영업이익 값이 없다 — '영업이익' 행 제목이 바뀌었거나 "
            f"rowList 구조가 바뀐 것 같다: {quarter_url}"
        )

    fetched_at = datetime.now(KST).isoformat()
    as_of = basic.get("localTradedAt")

    price_data = {
        "ticker": ticker,
        "fetched_at": fetched_at,
        "source": basic_url,
        "close": close_price,
        "change": resolve_change(basic),
        "as_of": as_of,
        "market_status": basic.get("marketStatus"),
    }
    fundamentals_data = {
        "ticker": ticker,
        "fetched_at": fetched_at,
        "sources": [quarter_url, annual_url],
        "unit": "억원",
        "quarters": quarters,
        "annuals": annuals,
    }

    # 종목 뒤섞임 방지 — price.json·fundamentals.json·meta.json이 서로 다른 파일이라도
    # 다 같은 ticker를 가리켜야 한다. 지금은 한 실행 안에서 같은 변수로 만들어 항상 참이지만,
    # 나중에 파일별로 따로 갱신하는 경로가 생기면 이 확인이 유일한 방어선이 된다.
    meta_ticker_check = ticker
    if not (price_data["ticker"] == fundamentals_data["ticker"] == meta_ticker_check):
        fail(
            "price.json/fundamentals.json/meta.json의 ticker가 서로 다르다 — "
            "종목이 섞였다. 이대로 쓰면 밸류에이션이 통째로 틀어진다"
        )

    out_dir = os.path.join(VALUATION_DIR, f"{ticker}-{name}")
    price_path = os.path.join(out_dir, "price.json")
    fundamentals_path = os.path.join(out_dir, "fundamentals.json")
    meta_path = os.path.join(out_dir, "meta.json")

    # 예전 한 파일 형식(market.json)의 잔재. 세 파일로 쪼갰으니 지운다.
    old_path = os.path.join(out_dir, "market.json")
    if os.path.exists(old_path):
        os.remove(old_path)

    results = []  # (파일명, 상태 문구)

    existing_price = load_json(price_path)
    if same_ignoring_fetched_at(existing_price, price_data):
        results.append(("price.json", "변화 없음"))
    else:
        write_json(price_path, price_data)
        as_of_date = (as_of or "")[:10]
        results.append(("price.json", f"갱신 ({close_price:,}원, {as_of_date})"))

    existing_fund = load_json(fundamentals_path)
    if same_ignoring_fetched_at(existing_fund, fundamentals_data):
        results.append(("fundamentals.json", "변화 없음"))
    else:
        write_json(fundamentals_path, fundamentals_data)
        results.append(
            ("fundamentals.json", f"갱신 (분기 {len(quarters)}개, 연간 {len(annuals)}개)")
        )

    # meta.json은 있으면 절대 덮어쓰지 않는다 — 메인 세션이 나중에 손으로 고칠 수 있는 파일이다.
    if os.path.exists(meta_path):
        results.append(("meta.json", "변화 없음"))
    else:
        shares = KNOWN_SHARES.get(ticker)
        shares_source = "constant" if shares is not None else "unavailable"
        meta_data = {
            "ticker": ticker,
            "name": name,
            "shares": shares,
            "shares_source": shares_source,
            "updated_at": datetime.now(KST).strftime("%Y-%m-%d"),
        }
        write_json(meta_path, meta_data)
        results.append(("meta.json", "생성"))

    width = max(len(fname) for fname, _ in results)
    for fname, status in results:
        print(f"{fname.ljust(width)}  {status}")


if __name__ == "__main__":
    main()
