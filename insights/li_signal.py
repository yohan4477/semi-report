# 링크드인 글을 시간축에 쓸 수 있는 신호와 못 쓰는 것으로 나눈다.
#
# 왜 필요한가: 게시일은 정보의 날짜가 아니다. SemiAnalysis는 몇 달 전 뉴스레터를
# 다시 홍보하기도 하고(최장 +74일), 밈·팟캐스트·채용 글도 같은 피드에 섞인다.
# 게시일을 그대로 시간축에 걸면 「2026-07에 확인된 사실」이 실제로는 5월 자료가 된다.
#
# 규칙
#   1) 뉴스레터 링크가 있으면 기준일은 그 원문의 발행일이다. 게시일이 아니다.
#   2) 시차가 LAG_MAX일을 넘으면 재홍보로 본다 — 새 정보가 아니므로 시간축에서 뺀다.
#   3) 링크가 없으면 게시일을 정보 날짜로 인정한다. 배제 목록(밈·행사·채용·방송·
#      과거 회고)에 걸리지 않으면 전부 인용 후보다 — 「수치가 있나」로는 안 나눈다.
#   4) 재홍보와 행사·홍보는 시간축에서 빼되 **버리지는 않는다**(push=True).
#      「몇 달 전 글을 지금 다시 민다」는 새 사실은 아니어도 지금 무엇을 밀고 있나의 신호다.
#      이 축은 usable과 별개다 — 근거로 인용하지 않고, 무엇이 반복되는지를 볼 때만 쓴다.
import io, os, re, sys, json, html, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
CLIPS = os.path.join(ROOT, 'input', 'clippings')
OUT = os.path.join(ROOT, 'insights', 'views', 'li_signals.json')
LAG_MAX = 15   # 이 날짜를 넘겨 올린 뉴스레터 홍보는 새 정보로 세지 않는다

# 배제 목록 — 여기 걸리면 근거로 못 쓴다. 걸리지 않으면 전부 인용 후보다.
# 「수치가 있나」로 자동 판정하지 않는다. 기계가 「새 사실인가」를 못 나눈다는 것을
# 논평·서술 137건이 증명했다 — 밈과 InP 레이저 글이 같은 칸에 앉아 있었다.
#
# 라운드 2: 정규식이 한국어 표지만 잡아서 233건 중 약 13%가 새서 usable로 남았다 —
# 게시물 원문(영어)이거나, 요지가 한국어라도 밈/패러디를 부르는 낱말이 달랐다(패러디·유머).
# 아래 영어 대안은 실제 raw/linkedin_posts_raw.json·content/linkedin 원문에서 반복 확인된
# 표현만 담았다 — has_video처럼 「형식이 영상·팟캐스트다」라는 이유만으로는 안 뺀다. AMD
# MI355X InferenceX 비교(밈 영상 자막에 수치 주장)와 구글 TPU ICI 토폴로지 글은 여전히
# usable이어야 한다 — 둘 다 이미 카드가 인용 중이다.
MEME = re.compile(r'밈\s*[—:-]|[—:-]\s*밈\b|밈:|농담|풍자|짤|패러디|유머|업무 무관|실질 정보 없음')
EVENT = re.compile(
    r'모임|컨퍼런스|콘퍼런스|행사|웨비나|구독|초청|등록에 승인|참가 안내'
    r'|fireside chat|join us (?:for|at)|we.?ll be (?:hosting|presenting|joining)'
    r'|please register|register (?:at|here|now|below|to join)', re.I)
HIRE = re.compile(r'채용|합류|모집|팔로우|계정을 열|구독을 권')
# 채용 글은 실제 표본에서 전부 한국어 공고문(요지에 "채용 공고" 등)이라 영어 대안을
# 추가할 근거가 없었다 — "career"·"apply" 등은 실제 usable 표본에서 무관한 문맥에만
# 나왔다(예: "이 한 시간이 커리어에 도움" · "엔지니어링 재능을 apply했다").
BROADCAST = re.compile(r'팟캐스트|Podcast|에피소드|Ep\.|출연|방송 자막|(?i:Episode\s*#?\d)')
PAST = re.compile(r'작년|지난해|20(1\d|2[0-4])년|당시|그때|돌아보면|회고')


def urn_date(aid):
    """activity id 상위 비트가 밀리초 타임스탬프 — 게시일을 추정 없이 얻는다.

    **여기는 UTC 다. scripts/gen_li_source.py 의 kst() 는 같은 id 를 KST(+9h)로
    읽는다.** 그래서 한국 시각 00~09시 글은 이 파일의 basis_date 와 원문 마크다운의
    기준일이 하루 어긋난다. 한쪽만 고치면 두 파일을 날짜로 잇던 자리가 조용히
    깨진다 — 고치려면 kst() 와 같이 고친다.

    날짜로 게시물을 가리키지 않는 것이 더 안전하다. basis_date 는 뉴스레터 링크가
    있으면 그 원문 발행일로 덮어써지므로 애초에 게시물 식별자가 아니다.
    게시물을 가리켜야 하면 activity 번호를 쓴다(notes_lib.li_activity)."""
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

    **배제 판정이다.** 배제 목록에 걸리지 않으면 전부 인용 후보다. 고를 사람은
    글 쓰는 쪽이고, 기계는 배제된 줄을 인용하면 막는 일만 한다(check_axes L1).

    has_video는 판정에 쓰지 않는다 — 영상 자막 속 사실(예: AMD MI355X InferenceX
    주장)을 이미 카드가 인용하고 있어, 영상이라는 이유만으로 배제하면 안 된다.
    호출부가 넘기므로 시그니처는 유지한다.

    반환: (kind, usable, basis_date, lag_days, push)
    """
    if slug:
        src = pub.get(slug)
        if src is None:
            return '뉴스레터 링크(발행일 미상)', False, posted, None, False
        lag = (datetime.date.fromisoformat(posted) - datetime.date.fromisoformat(src)).days
        if lag > LAG_MAX:
            return '재홍보', False, src, lag, True
        # 원본 뉴스레터가 있으니 그쪽을 인용한다. 링크드인은 인용 대상이 아니다
        return '신규 발행 알림', False, src, lag, False
    if MEME.search(text):
        return '밈·농담', False, posted, None, True
    if EVENT.search(text):
        return '행사·모임', False, posted, None, True
    if HIRE.search(text):
        return '채용·권유', False, posted, None, True
    if BROADCAST.search(text):
        return '방송·팟캐스트', False, posted, None, True
    if PAST.search(text):
        return '과거 회고', False, posted, None, False
    return '자체 발화', True, posted, None, False


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
                 'usable_kinds': ['자체 발화'],
                 'push_kinds': ['재홍보', '밈·농담', '행사·모임', '채용·권유', '방송·팟캐스트']},
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
