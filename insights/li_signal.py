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
import io, os, re, sys, json, html, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
CLIPS = os.path.join(ROOT, 'input', 'clippings')
OUT = os.path.join(ROOT, 'insights', 'views', 'li_signals.json')
LAG_MAX = 15   # 이 날짜를 넘겨 올린 뉴스레터 홍보는 새 정보로 세지 않는다

NUM = re.compile(r'\d+(?:\.\d+)?\s?(?:GW|MW|kW|억|조|%|배|TB/s|GB|nm|kV|달러|\$|명)')
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

        if slug:
            src = pub.get(slug)
            lag = ((datetime.date.fromisoformat(posted) - datetime.date.fromisoformat(src)).days
                   if src else None)
            if src is None:
                kind, usable, basis = '뉴스레터 링크(발행일 미상)', False, posted
            elif lag > LAG_MAX:
                kind, usable, basis = '재홍보', False, src
            else:
                kind, usable, basis = '신규 발행 알림', True, src
        else:
            src, lag = None, None
            if PROMO.search(text) or 'youtu' in seg[:2000]:
                kind, usable, basis = '행사·홍보', False, posted
            elif NUM.search(text):
                kind, usable, basis = '수치 있는 자체 발화', True, posted
            elif PAST.search(text):
                kind, usable, basis = '과거 회고', False, posted
            else:
                kind, usable, basis = '논평·서술', False, posted

        rows.append({'id': 'L-' + posted.replace('-', '') + '-' + aid[-4:],
                     'activity': aid, 'posted': posted, 'slug': slug, 'source_date': src,
                     'lag_days': lag, 'kind': kind, 'usable': usable, 'basis_date': basis,
                     'title': title[:400], 'desc': desc[:900],
                     'url': 'https://www.linkedin.com/feed/update/urn:li:activity:%s/' % aid})

    rows.sort(key=lambda r: r['basis_date'], reverse=True)
    data = {
        'note': ('링크드인 글의 시간축 자격. 기준일(basis_date)은 뉴스레터 링크가 있으면 그 원문 발행일, '
                 '없으면 게시일이다. usable=true인 것만 판단의 근거로 인용한다.'),
        'rule': {'lag_max_days': LAG_MAX,
                 'usable_kinds': ['신규 발행 알림', '수치 있는 자체 발화']},
        'generated_from': '대시보드/소셜 신호 히스토리.html',
        'counts': dict(collections.Counter(r['kind'] for r in rows)),
        'signals': rows,
    }
    json.dump(data, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('OK: 링크드인 %d건 -> %s' % (len(rows), OUT))
    for k, v in sorted(data['counts'].items(), key=lambda kv: -kv[1]):
        print('   %-22s %3d%s' % (k, v, '  (사용 가능)' if k in data['rule']['usable_kinds'] else ''))
    print('   사용 가능 합계 %d건' % sum(1 for r in rows if r['usable']))
    return data


if __name__ == '__main__':
    build()
