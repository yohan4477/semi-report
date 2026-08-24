#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""소셜 신호 히스토리를 「발화 기록」 타임라인 꼴로 만든다.

붙이는 것 셋 — 모두 여러 번 돌려도 결과가 같다.
  ① 행 라벨  밈·채용·팟캐스트·뉴스레터·재홍보. 라벨이 붙은 줄이 건너뛸 줄이고,
     라벨 없는 줄이 실질 신호다(그 줄만 점이 크고 파랗다).
  ② 행 날짜  「08-20」을 각 줄 앞에 박는다. 날짜별 <h3>는 DOM에 남기되 눈에서 감춘다 —
     gen_bmirror.py 와 li_signal.py 가 그 h3 로 날짜 그룹을 찾는다.
  ③ 월 머리  「2026년 8월 · 13일」을 그 달 첫 날짜 그룹 앞에 세운다.

**span 은 행 끝에 넣고 CSS order 로 앞에 그린다.** </a> 바로 뒤에 넣으면
gen_li_source.py 가 링크를 찾는 고정 창(seg[:2000])이 밀려 뉴스레터 slug 가 잘린다.
행 여는 태그(`<div class="row">`)에도 손대지 않는다 — gen_bmirror.py 의 행 정규식이
`<div class="row"><a class="rowmain"` 를 그대로 요구한다. 그래서 실질 신호 줄은
클래스가 아니라 `:has()` 로 가른다.

사용: PYTHONIOENCODING=utf-8 python scripts/stamp_li_kind.py
linkedin-update 로 새 글을 넣은 뒤 돌린다.
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'insights'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import li_signal as ls

HIST = os.path.join('대시보드', '소셜 신호 히스토리.html')
LEDGER = os.path.join('data', 'li_excluded.json')

# 라벨은 카드 첫머리의 표지로만 붙인다. li_signal 의 배제 정규식을 그대로 쓰면 안 된다 —
# 그쪽은 인용 자격을 가리려고 넓게 걸어 둔 것이라, 「구독자에게 답을 줬다」가 행사로,
# 「이번 주 팟캐스트에 나온다」가 팟캐스트로 잡혀 실질 신호에 건너뛰라는 딱지가 붙는다.
# 뉴스레터·재홍보만 li_signal 판정을 쓴다 — 그건 링크와 발행일로 갈리므로 틀리지 않는다.
MEME = re.compile(r'^밈\b|^밈\s*[—:·]|풍자 글이다|농담이다|한 줄짜리 농담|밈이다|밈성')
HIRE = re.compile(r'채용 공고|채용한다는|모집한다는|뽑는다는 공고|채용한다고')
CAST = re.compile(r'^팟캐스트|^주간 팟캐스트|^SemiAnalysis Weekly|^위클리 팟캐스트'
                  r'|^SemiAnalysis 주간 팟캐스트')
NEWS = {'신규 발행 알림', '뉴스레터 링크(발행일 미상)'}
DAY = re.compile(r'^<h3>(\d{4})-(\d\d)-(\d\d)</h3>')
ROW = re.compile(r'(<div class="row"><a class="rowmain" href="([^"]+)".*?</a>)(.*?)(</div>)', re.S)
CSS = """/*TLOG-START*/
.day{margin:0; border-left:2px solid var(--line); padding-left:14px;}
.day h3{position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden;
  clip:rect(0 0 0 0); white-space:nowrap; border:0;}
.day .row{position:relative; border-top:none; padding:9px 0;}
.day .row::before{content:''; position:absolute; left:-21px; top:15px; width:7px; height:7px;
  border-radius:50%; background:var(--sub); box-shadow:0 0 0 3px var(--bg);}
.day .row:not(:has(> .kind))::before{width:9px; height:9px; left:-22px; top:14px;
  background:var(--accent);}
.row > .d{order:-3; flex:none; font-variant-numeric:tabular-nums; font-weight:850;
  font-size:.82rem; color:var(--ink); margin-top:1px;}
.day a.rowmain{flex-basis:100%;}
.row > .tt{order:-1; flex:1 1 auto; min-width:0; font-size:.92rem; font-weight:800;
  color:var(--ink); line-height:1.45; overflow-wrap:anywhere;}
.row > .kind{order:-2; flex:none; font-size:.68rem; font-weight:850; letter-spacing:.02em;
  padding:1px 8px; border-radius:999px; border:1px solid var(--line); color:var(--sub);
  margin-top:2px; white-space:nowrap;}
.row > .kind.k-뉴스레터{border-color:var(--accent); color:var(--accent);}
.row > .kind.k-재홍보{border-color:#c2504a; color:#c2504a;}
:root[data-theme="dark"] .row > .kind.k-재홍보{border-color:#e08b85; color:#e08b85;}
.tlog-m{margin:26px 0 8px; font-size:.74rem; font-weight:850; letter-spacing:.05em;
  color:var(--sub);}
.tlog-m:first-of-type{margin-top:8px;}
/*TLOG-END*/"""


def label(text, kind):
    if kind == '재홍보':
        return '재홍보'
    if kind in NEWS:
        return '뉴스레터'
    if MEME.search(text):
        return '밈'
    if HIRE.search(text):
        return '채용'
    if CAST.search(text):
        return '팟캐스트'
    return None


def drop_hires(s):
    """채용 공고 행을 히스토리에서 뺀다.

    뺀 활동 ID 는 대장(data/li_excluded.json)에 반드시 남긴다 — linkedin-update 는
    「이 ID 가 히스토리에 있나」로 새 글을 가리므로, 대장이 없으면 지운 공고를
    다음 실행 때마다 새 글로 다시 잡아 넣는다.
    """
    led = []
    if os.path.exists(LEDGER):
        led = json.loads(io.open(LEDGER, encoding='utf-8').read())
    known = set(r['id'] for r in led)
    dropped = []

    def one(m):
        head, href, tail, close = m.groups()
        sn = re.search(r'<span class="sn">(.*?)</span>', head, re.S)
        text = ls.clean(sn.group(1)) if sn else ''
        if not (HIRE.search(text) or 'k-채용' in tail):
            return m.group(0)
        aid = re.search(r'activity:(\d+)', href)
        if aid and aid.group(1) not in known:
            known.add(aid.group(1))
            led.append({'id': aid.group(1), 'date': ls.urn_date(aid.group(1)),
                        'kind': '채용', 'sn': text})
        dropped.append(1)
        return ''

    s = ROW.sub(one, s)

    # 행이 다 빠져 머리만 남은 날짜 그룹은 그 그룹만 걷어낸다(뒤따르는 내용은 남긴다)
    parts = s.split('<div class="day">')
    out = [parts[0]]
    for seg in parts[1:]:
        e = re.match(r'^<h3>\d{4}-\d\d-\d\d</h3></div>', seg)
        if e:
            out.append(seg[e.end():])
            continue
        out.append('<div class="day">' + seg)
    s = ''.join(out)

    led.sort(key=lambda r: r['id'])
    io.open(LEDGER, 'w', encoding='utf-8').write(
        json.dumps(led, ensure_ascii=False, indent=1) + chr(10))
    return s, len(dropped), len(led)


def main():
    s = io.open(HIST, encoding='utf-8').read()
    s, ndrop, nled = drop_hires(s)
    pub = ls.publish_dates()
    s = re.sub(r'<p class="tlog-m">[^<]*</p>', '', s)
    n, days = {}, 0

    parts = s.split('<div class="day">')
    months = {}
    for seg in parts[1:]:
        d = DAY.match(seg)
        if d:
            months[d.group(1) + d.group(2)] = months.get(d.group(1) + d.group(2), 0) + 1

    out, seen = [parts[0]], set()
    for seg in parts[1:]:
        d = DAY.match(seg)
        if not d:
            out.append('<div class="day">' + seg)
            continue
        days += 1
        y, mm, dd = d.groups()

        def one(m):
            head, href, tail, close = m.groups()
            tail = re.sub(r'<span class="(?:kind|d)[^"]*"[^>]*>[^<]*</span>', '', tail)
            aid = re.search(r'activity:(\d+)', href)
            tail += '<span class="d">%s-%s</span>' % (mm, dd)
            if aid:
                text = ls.clean(re.search(r'<span class="sn">(.*?)</span>', head, re.S).group(1))
                nl = re.search(r'newsletter\.semianalysis\.com/p/([a-z0-9-]+)', head + tail)
                kind = ls.classify(text, nl.group(1) if nl else None,
                                   ls.urn_date(aid.group(1)), pub)[0]
                lab = label(text, kind)
                if lab:
                    n[lab] = n.get(lab, 0) + 1
                    tail += '<span class="kind k-%s">%s</span>' % (lab, lab)
            return head + tail + close

        seg = ROW.sub(one, seg)
        key = y + mm
        if key not in seen:
            seen.add(key)
            out.append('<p class="tlog-m">%s년 %d월 · %d일</p>' % (y, int(mm), months[key]))
        out.append('<div class="day">' + seg)

    s = ''.join(out)
    s = re.sub('/[*]TLOG-START[*]/.*?/[*]TLOG-END[*]/' + chr(10) + '?', '', s, flags=re.S)
    s = s.replace('</style>', CSS + '\n</style>', 1)
    cnt = len(re.findall(r'class="rowmain" href="https://www\.linkedin\.com', s))
    s = re.sub(r'LinkedIn \d+건', 'LinkedIn %d건' % cnt, s)
    io.open(HIST, 'w', encoding='utf-8').write(s)
    print('날짜 그룹 %d · 월 머리 %d · LinkedIn %d건 · 라벨 %d개 · %s'
          % (days, len(seen), cnt, sum(n.values()),
             ' '.join('%s %d' % kv for kv in sorted(n.items()))))
    print('채용 제외 %d행 · 대장 누적 %d건 (%s)' % (ndrop, nled, LEDGER))


if __name__ == '__main__':
    main()
