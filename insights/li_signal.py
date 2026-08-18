# 링크드인 글을 시간축에 쓸 수 있는 신호와 못 쓰는 것으로 가른다.
#
# 왜 필요한가: 게시일은 정보의 날짜가 아니다. SemiAnalysis는 몇 달 전 뉴스레터를
# 다시 홍보하기도 하고(최장 +74일), 밈·팟캐스트·채용 글도 같은 피드에 섞인다.
# 게시일을 그대로 시간축에 걸면 「2026-07에 확인된 사실」이 실제로는 5월 자료가 된다.
#
# 규칙
#   1) 뉴스레터 링크가 있으면 기준일은 그 원문의 발행일이다. 게시일이 아니다.
#   2) 시차가 LAG_MAX일을 넘으면 재홍보로 본다 — 새 정보가 아니므로 시간축에서 뺀다.
#   3) 링크가 없으면 게시일을 정보 날짜로 인정하되, 수치가 박힌 자체 발화만 근거로 쓴다.
#      밈·행사·팟캐스트·채용·과거 회고는 신호가 아니다.
#   4) 재홍보와 행사·홍보는 시간축에서 빼되 **버리지는 않는다**(push=True).
#      「몇 달 전 글을 지금 다시 민다」는 새 사실은 아니어도 지금 무엇을 밀고 있나의 신호다.
#      이 축은 usable과 별개다 — 근거로 인용하지 않고, 무엇이 반복되는지를 볼 때만 쓴다.
import io, os, re, sys, json, html, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
CLIPS = os.path.join(ROOT, 'input', 'clippings')
OUT = os.path.join(ROOT, 'insights', 'views', 'li_signals.json')
LAG_MAX = 15   # 이 날짜를 넘겨 올린 뉴스레터 홍보는 새 정보로 세지 않는다

NUM = re.compile(r'\d+(?:\.\d+)?\s?(?:GW|MW|kW|억|조|%|배|TB/s|GB|nm|kV|달러|\$|명)')
# 제품·모델명끼리 우열을 매기는 주장 — 수치 단위가 없어도 판단 재료다.
# 예: "MI355X의 vLLM이 B200의 vLLM보다 낫다" / "X outperforms Y" / "X beats Y"
COMPARE = re.compile(
    r'보다\s*(?:더\s*)?(?:낫다|나은|앞선다|앞섰다|앞서는|빠르다|빠른|빨랐다|우수하다|우세하다|우위)'
    r'|is\s+(?:much\s+|far\s+)?better\s+than|outperforms?|outperformed'
    r'|\bbeats?\b'
    , re.I)
PROMO = re.compile(r'팟캐스트|Podcast|에피소드|Ep\.|채용|합류|모집|컨퍼런스|콘퍼런스|행사|웨비나|구독|밈 —|밈-')
PAST = re.compile(r'작년|지난해|20(1\d|2[0-4])년|당시|그때|돌아보면')


def urn_date(aid):
    """activity id 상위 비트가 밀리초 타임스탬프 — 게시일을 추정 없이 얻는다"""
    return datetime.datetime.utcfromtimestamp((int(aid) >> 22) / 1000).strftime('%Y-%m-%d')


def clean(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


def publish_dates():
    out = {}
    for name in os.listdir(CLIPS):
        if not name.endswith('.md'):
            continue
        head = io.open(os.path.join(CLIPS, name), encoding='utf-8').read()[:1500]
        s = re.search(r'source: "https://newsletter\.semianalysis\.com/p/([a-z0-9-]+)"', head)
        d = re.search(r'^published: (\d{4}-\d{2}-\d{2})', head, re.M)
        if s and d:
            out[s.group(1)] = d.group(1)
    return out


def classify(text, slug, posted, pub, has_video=False):
    """게시물 하나의 자격 판정. 이 규칙은 여기 한 벌만 둔다 —
    scripts/gen_li_source.py도 이 함수를 부른다.

    반환: (kind, usable, basis_date, lag_days, push)
    """
    if slug:
        src = pub.get(slug)
        if src is None:
            return '뉴스레터 링크(발행일 미상)', False, posted, None, False
        lag = (datetime.date.fromisoformat(posted) - datetime.date.fromisoformat(src)).days
        if lag > LAG_MAX:
            return '재홍보', False, src, lag, True
        return '신규 발행 알림', True, src, lag, False
    if PROMO.search(text) or has_video:
        return '행사·홍보', False, posted, None, True
    if NUM.search(text):
        return '수치 있는 자체 발화', True, posted, None, False
    if COMPARE.search(text):
        return '제품 비교 주장', True, posted, None, False
    if PAST.search(text):
        return '과거 회고', False, posted, None, False
    return '논평·서술', False, posted, None, False


def build():
    hist = io.open(HIST, encoding='utf-8').read()
    pub = publish_dates()
    rows, seen = [], set()
    for m in re.finditer(r'urn:li:activity:(\d+)/"[^>]*>(.*?)</a>', hist, re.S):
        aid, title = m.group(1), clean(m.group(2))
        if aid in seen:
            continue
        seen.add(aid)
        seg = hist[m.end():m.end() + 3000]
        dm = re.search(r'<div class="d">(.*?)</div>', seg, re.S)
        desc = clean(dm.group(1)) if dm else ''
        nl = re.search(r'newsletter\.semianalysis\.com/p/([a-z0-9-]+)', seg[:2000])
        slug = nl.group(1) if nl else None
        posted = urn_date(aid)
        text = title + ' ' + desc

        kind, usable, basis, lag, push = classify(
            text, slug, posted, pub, has_video='youtu' in seg[:2000])
        src = pub.get(slug) if slug else None

        rows.append({'id': 'L-' + posted.replace('-', '') + '-' + aid[-4:],
                     'activity': aid, 'posted': posted, 'slug': slug, 'source_date': src,
                     'lag_days': lag, 'kind': kind, 'usable': usable, 'push': push,
                     'basis_date': basis,
                     'title': title[:400], 'desc': desc[:900],
                     'url': 'https://www.linkedin.com/feed/update/urn:li:activity:%s/' % aid})

    rows.sort(key=lambda r: r['basis_date'], reverse=True)
    data = {
        'note': ('링크드인 글의 시간축 자격. 기준일(basis_date)은 뉴스레터 링크가 있으면 그 원문 발행일, '
                 '없으면 게시일이다. usable=true인 것만 판단의 근거로 인용한다. '
                 'push=true는 새 사실은 아니지만 「지금 무엇을 다시 미나」를 보는 별도 축이다.'),
        'rule': {'lag_max_days': LAG_MAX,
                 'usable_kinds': ['신규 발행 알림', '수치 있는 자체 발화', '제품 비교 주장'],
                 'push_kinds': ['재홍보', '행사·홍보']},
        'generated_from': '대시보드/소셜 신호 히스토리.html',
        'counts': dict(collections.Counter(r['kind'] for r in rows)),
        'signals': rows,
    }
    json.dump(data, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('OK: 링크드인 %d건 -> %s' % (len(rows), OUT))
    for k, v in sorted(data['counts'].items(), key=lambda kv: -kv[1]):
        print('   %-22s %3d%s' % (k, v, '  (사용 가능)' if k in data['rule']['usable_kinds'] else ''))
    print('   사용 가능 합계 %d건 · 다시 미는 글(push) %d건'
          % (sum(1 for r in rows if r['usable']), sum(1 for r in rows if r['push'])))
    return data


if __name__ == '__main__':
    build()
