# -*- coding: utf-8 -*-
"""링크드인 글을 페이지가 스스로 받는 응답에서 읽는다 — 날마다 새 스크립트를 짜지 않으려고 둔 고정 도구.

  python scripts/li_fetch.py company semianalysis --since 2026-09-25
  python scripts/li_fetch.py person wei-li-a93561b --since 2026-09-01 --known "C:/Users/y/clippings/linkedin/Wei Li"

company: 회사 피드가 부르는 voyagerFeedDashOrganizationalPageUpdates JSON 을 CDP Network 로 엿듣는다.
         우리가 따로 부르는 API 는 없다(사람이 스크롤할 때와 같은 요청만 나간다). 본문 전문·재공유 원글·
         이미지 원본 주소가 JSON 에 다 있어서 「더보기」 클릭도 스크린샷도 필요 없다.
person:  인물 활동 페이지는 2026-10 기준 SDUI(서버 렌더 RSC)라 JSON 이 없다. 본문은 화면 카드에서,
         활동 ID 는 문서 속 피드 순서 목록에서 가져와 순서로 짝짓고 상대 시각 라벨로 짝마다 검증한다.
         RSC 안 본문은 지연 참조($Lbd5)로 조각나 있어 직접 파싱하지 않는다(2026-10-02 시험에서 21편 중 19편 깨짐).

산출: C:/Users/y/clippings/linkedin/_runs/<대상>/<오늘>/posts.json + img/<id>_<n>.<ext> (원본 해상도)
화면에는 새 글만 한 줄씩 찍는다. 전문은 posts.json 에서 필요한 것만 연다.
새 글 판별 — company: 소셜 신호 히스토리 + data/li_excluded.json, person: --known 폴더 안 activity ID.
"""
import argparse, base64, bisect, datetime, glob, io, json, os, re, sys, time, urllib.parse, urllib.request
from websocket import create_connection

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDP = 'http://127.0.0.1:9222'
RUNS = 'C:/Users/y/clippings/linkedin/_runs'
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
EXCL = os.path.join(ROOT, 'data', 'li_excluded.json')
KST = datetime.timedelta(hours=9)


def kst(aid):
    return (datetime.datetime.utcfromtimestamp((int(aid) >> 22) / 1000) + KST).strftime('%Y-%m-%d %H:%M')


class Tab:
    def __init__(self, url):
        req = urllib.request.Request(CDP + '/json/new?' + urllib.parse.quote(url, safe=':/?=&%'), method='PUT')
        self.t = json.loads(urllib.request.urlopen(req).read())
        self.ws = create_connection(self.t['webSocketDebuggerUrl'], suppress_origin=True, timeout=60)
        self.mid = 0
        self.events = []

    def send(self, m, p=None):
        self.mid += 1
        self.ws.send(json.dumps({'id': self.mid, 'method': m, 'params': p or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get('id') == self.mid:
                return r
            self.events.append(r)

    def ev(self, js):
        r = self.send('Runtime.evaluate', {'expression': js, 'returnByValue': True, 'awaitPromise': True})
        return r.get('result', {}).get('result', {}).get('value')

    def pump(self, sec):
        self.ws.settimeout(0.3)
        end = time.time() + sec
        while time.time() < end:
            try:
                self.events.append(json.loads(self.ws.recv()))
            except Exception:
                pass
        self.ws.settimeout(60)

    def body(self, rid):
        b = self.send('Network.getResponseBody', {'requestId': rid}).get('result', {})
        s = b.get('body', '')
        return base64.b64decode(s).decode('utf-8', 'replace') if b.get('base64Encoded') else s

    def close(self):
        try:
            urllib.request.urlopen(CDP + '/json/close/' + self.t['id'])
        except Exception:
            pass


def responses(tab, pred):
    """다 받은(loadingFinished) 응답 중 pred(url, type) 를 만족하는 것의 (url, body). 한 번 준 것은 다시 안 준다.
    아직 받는 중인 응답은 다음 부름으로 미룬다 — 스트리밍 RSC 는 도착 직후 본문이 비어 있다."""
    tab.pending = getattr(tab, 'pending', {})
    done = set()
    rest = []
    for e in tab.events:
        m = e.get('method')
        if m == 'Network.responseReceived':
            r = e['params']['response']
            if pred(r['url'], e['params'].get('type')):
                tab.pending[e['params']['requestId']] = r['url']
        elif m in ('Network.loadingFinished', 'Network.loadingFailed'):
            done.add(e['params']['requestId'])
        else:
            rest.append(e)
    tab.events = rest
    tab.finished = getattr(tab, 'finished', set()) | done
    out = []
    for rid in [k for k in tab.pending if k in tab.finished]:
        u = tab.pending.pop(rid)
        try:
            out.append((u, tab.body(rid)))
        except Exception:
            pass
    return out


# ---------- company: voyager JSON ----------

def best_image(vi):
    arts = vi.get('artifacts') or []
    if not arts or not vi.get('rootUrl'):
        return None
    a = max(arts, key=lambda x: x.get('width') or 0)
    return {'url': vi['rootUrl'] + a['fileIdentifyingUrlPathSegment'], 'w': a.get('width'), 'h': a.get('height')}


def walk_images(o, acc):
    if isinstance(o, dict):
        if o.get('$type') == 'com.linkedin.common.VectorImage' or ('artifacts' in o and 'rootUrl' in o):
            b = best_image(o)
            if b and b['url'] not in [x['url'] for x in acc]:
                acc.append(b)
            return
        for v in o.values():
            walk_images(v, acc)
    elif isinstance(o, list):
        for v in o:
            walk_images(v, acc)


def urls_in(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('url', 'actionTarget', 'transcribedDocumentUrl', 'manifestUrl') and isinstance(v, str) and v.startswith('http'):
                if v not in acc:
                    acc.append(v)
            else:
                urls_in(v, acc)
    elif isinstance(o, list):
        for v in o:
            urls_in(v, acc)


def txt(o):
    return ((o or {}).get('text') or {}).get('text', '') if isinstance(o, dict) else ''


def parse_update(u, byurn):
    md = u.get('metadata') or {}
    m = re.search(r'activity:(\d{19})', md.get('backendUrn', '') or u.get('entityUrn', ''))
    if not m:
        return None
    content = u.get('content') or {}
    kinds = sorted(k.replace('Component', '') for k, v in content.items() if v and not k.startswith('$'))
    imgs = []
    walk_images({k: v for k, v in content.items() if k != 'articleComponent' or True}, imgs)
    imgs = [i for i in imgs if 'profile-displayphoto' not in i['url'] and 'company-logo' not in i['url']]
    links = []
    for a in ((u.get('commentary') or {}).get('text') or {}).get('attributesV2') or []:
        urls_in(a, links)
    art = content.get('articleComponent') or {}
    if art:
        urls_in({'n': art.get('navigationContext')}, links)
    doc = content.get('documentComponent') or {}
    rs = u.get('resharedUpdate') or byurn.get(u.get('*resharedUpdate') or '')
    reshare = None
    if rs:
        reshare = {'actor': txt({'text': (rs.get('actor') or {}).get('name')}),
                   'text': txt(rs.get('commentary')),
                   'id': (re.search(r'activity:(\d{19})', (rs.get('metadata') or {}).get('backendUrn', '')) or [None, None])[1]}
        ri = []
        walk_images(rs.get('content') or {}, ri)
        imgs += [i for i in ri if 'profile-displayphoto' not in i['url'] and 'company-logo' not in i['url']]
    return {'id': m.group(1), 'kst': kst(m.group(1)),
            'actor': ((u.get('actor') or {}).get('name') or {}).get('text', ''),
            'text': txt(u.get('commentary')), 'kinds': kinds, 'images': imgs, 'links': links,
            'article': txt({'text': art.get('title')}) if art else '',
            'doc': {'title': doc.get('document', {}).get('title', ''), 'urls': (lambda a: (urls_in(doc, a), a)[1])([])} if doc else None,
            'video': 'linkedInVideo' in kinds, 'reshare': reshare, 'yt': []}


def collect_company(tab, since_ms, max_rounds):
    posts = {}

    def harvest():
        for u, b in responses(tab, lambda url, t: 'OrganizationalPageUpdates' in url or 'organizationalPageUrn' in urllib.parse.unquote(url)):
            try:
                inc = json.loads(b).get('included') or []
            except Exception:
                continue
            byurn = {x.get('entityUrn'): x for x in inc if x.get('entityUrn')}
            for x in inc:
                if (x.get('$type') or '').endswith('feed.Update'):
                    p = parse_update(x, byurn)
                    if p and (p['id'] not in posts or len(p['text']) > len(posts[p['id']]['text'])):
                        posts[p['id']] = p

    tab.send('Network.enable', {'maxResourceBufferSize': 50_000_000, 'maxTotalBufferSize': 300_000_000})
    tab.send('Page.reload')
    tab.pump(10)
    tab.ev("(function(){var b=[].slice.call(document.querySelectorAll('button,[role=button]')).find(function(x){return /정렬 기준/.test(x.innerText||'')}); if(b&&b.getAttribute('aria-expanded')!=='true')b.click(); return 1;})()")
    tab.pump(1.5)
    tab.ev("(function(){var o=[].slice.call(document.querySelectorAll('[role=option]')).find(function(x){return (x.innerText||'').trim()==='최근'}); if(o)o.click(); return 1;})()")
    tab.pump(4)
    stall, last = 0, -1
    for i in range(max_rounds):
        harvest()
        oldest = min((int(k) >> 22 for k in posts), default=0)
        if oldest and oldest < since_ms and i > 2:
            break
        stall = stall + 1 if len(posts) == last else 0
        last = len(posts)
        if stall >= 6:
            break
        tab.ev('window.scrollBy(0,2600)')
        tab.pump(2.0)
    harvest()
    return posts


def youtube_links(tab, aid):
    tab.send('Page.navigate', {'url': 'https://www.linkedin.com/feed/update/urn:li:activity:%s/' % aid})
    tab.pump(6)
    out = []
    for _ in range(2):
        tab.ev('window.scrollBy(0,1500)')
        tab.pump(2.2)
        out = tab.ev("JSON.stringify([...new Set([].slice.call(document.querySelectorAll('a[href*=\"youtube\"],a[href*=\"youtu.be\"]')).map(a=>a.href))])")
        out = json.loads(out or '[]')
        if out:
            break
    return out


# ---------- person: SDUI 화면 + 문서 속 순서 목록 ----------
# 본문은 화면(main [role=listitem])에 전문이 있지만 활동 ID 가 없다. 문서(RSC)에는 피드 순서대로 된
# 항목 ID(updateUrnActivityUrn)가 피드 순서대로 있다. 둘을 순서로 짝짓고, 카드의 상대 시각(「2일」「1주」)이 ID 시각과
# 맞는지 짝마다 확인한다 — 어긋나는 첫 자리에서 짝짓기를 멈춘다(엉뚱한 ID 를 붙이느니 덜 받는다).

JS_ITEMS = r"""(async()=>{
for(const b of document.querySelectorAll('main [role=listitem] button')){const t=(b.innerText||'').trim();if(/^…/.test(t)&&/더보기/.test(t))b.click();}
await new Promise(r=>setTimeout(r,1200));
return JSON.stringify([...document.querySelectorAll('main [role=listitem]')].filter(li=>/^피드 게시물/.test(li.innerText.trim())).map(li=>({t:li.innerText,
 key:(((li.getAttribute('componentkey')||'').match(/^update-card-focus(.+?)FeedType_/)||[])[1]||''),vid:li.querySelectorAll('video').length,
 doc:!!li.querySelector('iframe[src*="native-document"]'),
 imgs:[...li.querySelectorAll('img')].map(i=>{let best=i.currentSrc||i.src,bw=0;(i.srcset||'').split(',').forEach(p=>{const m=p.trim().match(/^(\S+)\s+(\d+)w$/);if(m&&+m[2]>bw){bw=+m[2];best=m[1]}});
  return [i.naturalWidth,i.naturalHeight,i.alt||'',best]}),
 links:[...li.querySelectorAll('a[href]')].map(a=>a.href).filter(h=>!/linkedin\.com\/(in|company|search|feed\/hashtag)\//.test(h))})))})()"""


def feed_order(body):
    """피드 항목의 활동 ID 를 나온 순서대로. 퍼간 글도 퍼간 쪽 ID 가 잡힌다(원글 ID 는 reactionState 쪽에 있다)."""
    out = []
    for m in re.finditer(r'updateUrnActivityUrn[^0-9]{0,80}?(\d{19})', body):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


def rel_ok(label, aid, now_ms):
    """카드의 상대 시각 라벨이 ID 시각과 맞나. 라벨을 못 읽으면 True(판정 보류)."""
    m = re.match(r'(\d+)\s*(분|시간|일|주|개월|년)', label)
    if not m:
        return True
    n, u = int(m.group(1)), m.group(2)
    age = (now_ms - (int(aid) >> 22)) / 86400000
    # 링크드인은 내림으로 적는다 — 211일 전 글이 「6개월」(2026-10-02 Peccatiello 에서 걸렸다)
    lo, hi = {'분': (0, 1.1), '시간': (0, 1.1), '일': (n - 0.6, n + 1.6), '주': (7 * n - 1, 7 * n + 8),
              '개월': (30 * n - 3, 31 * (n + 1) + 3), '년': (365 * n - 15, 365 * (n + 1) + 15)}[u]
    return lo <= age <= hi


def parse_item(t):
    """화면 카드 글을 퍼감 여부·원저자·시각 라벨·본문·링크 카드로 가른다(scratchpad/_wl_fetch.py 에서 옮김)."""
    lines = [l.rstrip() for l in t.split('\n')]
    if lines and lines[0].strip() == '피드 게시물':
        lines = lines[1:]
    ne = [l for l in lines if l.strip()]
    repost = bool(ne and '님이 퍼감' in ne[0])
    author = ne[1].strip() if repost and len(ne) > 1 else ''
    ti, label = None, ''
    for i, l in enumerate(lines[:30]):
        if re.match(r'^\d+\s*\S+\s*(•|·)', l.strip()) and i > 0:
            ti, label = i, l.strip()
            break
    start = ti + 1 if ti is not None else 0
    end = len(lines)
    for i in range(start, len(lines)):
        s = lines[i].strip()
        if s == '번역 표시' or re.match(r'^반응 \d+', s) or s == '추천':
            end = i
            break
    body = lines[start:end]
    while body and (not body[0].strip() or body[0].strip() == '팔로우'):
        body.pop(0)
    card = []
    if end < len(lines) and lines[end].strip() == '번역 표시':
        for l in lines[end + 1:]:
            s = l.strip()
            if re.match(r'^반응 \d+', s) or s == '추천':
                break
            if s and s not in card:
                card.append(s)
    text = re.sub(r'\n?\s*…\s*더보기\s*$', '', '\n'.join(body)).strip()
    text = re.sub(r'\n{3,}', '\n\n', text)
    hdr = ' / '.join(l.strip() for l in lines[:ti or 0] if l.strip())[:200]
    return repost, author, label, text, card, hdr


def good_img(w, h, alt, src):
    if not src or 'media.licdn.com/dms/image' not in src:
        return False
    if re.search(r'profile-|company-logo|articleshare|comment-image|ghost|emoji', src) or '프로필 보기' in alt:
        return False
    return min(w, h) >= 200 and max(w, h) >= 400


class Blocked(Exception):
    pass


def guard(tab):
    """로그인 벽·요청 과다 화면이면 멈춘다 — 여러 사람을 이어 돌릴 때 계정을 지키려고."""
    href = tab.ev('location.href') or ''
    if re.search(r'login|authwall|checkpoint|uas/', href):
        raise Blocked(href)
    if tab.ev("/요청이 너무 많|Too Many Requests|unusual activity|비정상적인 활동/i.test(document.body.innerText.slice(0,3000))"):
        raise Blocked('rate limit/unusual activity page')


def index_ids(body):
    """본문 속 활동 ID 위치를 한 번만 색인한다 — 카드마다 다시 훑지 않으려고."""
    # 글에 따라 ID 가 activity·ugcPost·share 셋 중 하나로만 나온다(Damodaran 은 ugcPost) — 셋 다 색인한다
    pos, ids = [], []
    for m in re.finditer(r'(activity|ugcPost|share):(\d{19})', body):
        pos.append(m.start())
        ids.append(m.group(1) + ':' + m.group(2))
    return pos, ids


def id_for_key(bodies, key, label='', now_ms=0, W=3000):
    """카드 고유 키(update-card-focus<키>FeedType_…)가 나오는 모든 자리 앞뒤 W자 안에서 가장 많이 나오는 활동 ID.
    Bob Elliott 시험: 제 ID 2,228회, 다음 후보 107회. 앞 40자리만 세면 이웃 글과 차이가 안 벌어진다.
    블로그 링크가 붙은 긴 글(Damodaran)은 이웃 ID 가 비슷하게 섞인다 — 카드 라벨 시각에 맞는 후보만 남겨 고른다."""
    if not key:
        return None
    cnt = {}
    for body, (pos, ids) in bodies:
        for m in re.finditer(re.escape(key), body):
            lo = bisect.bisect_left(pos, m.start() - W)
            hi = bisect.bisect_right(pos, m.start() + W)
            for a in ids[lo:hi]:
                cnt[a] = cnt.get(a, 0) + 1
    if now_ms and label:
        cnt = {a: c for a, c in cnt.items() if rel_ok(label, a.split(':')[1], now_ms)}
    if not cnt:
        return None
    top = sorted(cnt.items(), key=lambda x: -x[1])
    if len(top) > 1 and top[0][1] < 2 * top[1][1]:
        return None
    return top[0][0]


def collect_person(tab, since_ms, max_rounds):
    order, cards = [], []          # 둘 다 피드 순서. order=활동 ID, cards=화면 카드(본문 앞 80자로 중복 제거)
    seen_cards = set()
    bodies = []

    def harvest():
        for u, b in responses(tab, lambda url, t: '/recent-activity/' in url or 'pagers.profile.ActivityDetail' in url):
            if re.fullmatch(r'[A-Za-z0-9+/=\s]+', b[:2000] or '-'):
                try:
                    b = base64.b64decode(b + '==').decode('utf-8', 'replace')
                except Exception:
                    pass
            bodies.append((b, index_ids(b)))
            for x in feed_order(b):
                if x not in order:
                    order.append(x)
        for it in json.loads(tab.ev(JS_ITEMS) or '[]'):
            # 직함 줄이 긴 사람은 앞 160자가 카드마다 같다(Bob Elliott) — 고유 키로 가린다
            key = it.get('key') or re.sub(r'\s+', ' ', it['t'])[:600]
            if key not in seen_cards:
                seen_cards.add(key)
                cards.append(it)

    tab.send('Network.enable', {'maxResourceBufferSize': 80_000_000, 'maxTotalBufferSize': 300_000_000})
    tab.send('Page.reload')
    tab.pump(10)
    guard(tab)
    stall, last = 0, -1
    for i in range(max_rounds):
        harvest()
        oldest = min((int(k) >> 22 for k in order), default=0)
        if oldest and oldest < since_ms and i > 2:
            break
        stall = stall + 1 if (len(order), len(cards)) == last else 0
        if stall >= 3:
            break
        last = (len(order), len(cards))
        if stall >= 6:
            break
        # 이 페이지는 안쪽 컨테이너가 스크롤한다 — window.scrollBy 는 안 먹는다. 마지막 카드를 화면에 들인다
        tab.ev("var l=[...document.querySelectorAll('main [role=listitem]')].filter(x=>/^피드 게시물/.test(x.innerText.trim()));if(l.length)l[l.length-1].scrollIntoView();1")
        tab.pump(4.0)
    tab.pump(8.0)   # 마지막 쪽 응답이 다 오기 전에 끝나면 그 쪽 카드가 통째로 못 붙는다(Peccatiello 카드 50 · 순서 40)
    harvest()
    now_ms = int(time.time() * 1000)
    posts = {}
    lost = 0
    for k, it in enumerate(cards):
        repost, author, label, text, card, hdr = parse_item(it['t'])
        urn = id_for_key(bodies, it.get('key'), label, now_ms)
        kind, aid = urn.split(':') if urn else (None, None)
        if not aid or not rel_ok(label, aid, now_ms):
            lost += 1
            if os.environ.get('LI_DEBUG'):
                print('LOST', k, repr(label[:10]), 'key' if it.get('key') else 'nokey', aid and kst(aid), text[:40].replace('\n', ' '))
            continue
        imgs, urls = [], set()
        for w, h, alt, src in it['imgs']:
            if good_img(w, h, alt, src) and src not in urls:
                urls.add(src)
                imgs.append({'url': src, 'w': w, 'h': h})
        posts[aid] = {'id': aid, 'kst': kst(aid), 'text': text, 'images': imgs,
                      'kinds': ['repost'] if repost else [], 'links': sorted(set(it['links'])),
                      'article': ' / '.join(card[:3]), 'doc': {'urls': []} if it['doc'] else None,
                      'video': bool(it['vid']), 'reshare': {'actor': author, 'text': '', 'id': None} if repost else None,
                      'yt': [], 'label': label, 'hdr': hdr, 'urn_kind': kind}
    print('순서 목록 %d · 화면 카드 %d · 짝 %d · 못 붙임 %d' % (len(order), len(cards), len(posts), lost))
    return posts


# ---------- 공통 ----------

def known_company():
    k = set(re.findall(r'activity:(\d+)', open(HIST, encoding='utf-8').read()))
    k |= {r['id'] for r in json.load(open(EXCL, encoding='utf-8'))}
    return k


def known_dir(d):
    # 파일 이름의 [끝 4자리]로는 판별하지 않는다 — 2026-10-02 시험에서 49편 중 5편이 남의 파일에 걸렸다
    ids = set()
    for f in glob.glob(os.path.join(d, '*.md')):
        ids |= set(re.findall(r'(?:activity|ugcPost|share):(\d{19})', open(f, encoding='utf-8').read()))
    return ids


def download(posts, imgdir, base=0):
    os.makedirs(imgdir, exist_ok=True)
    for p in posts:
        for n, im in enumerate(p['images']):
            try:
                req = urllib.request.Request(im['url'], headers={'User-Agent': 'Mozilla/5.0'})
                r = urllib.request.urlopen(req, timeout=30)
                ext = {'image/png': 'png', 'image/gif': 'gif', 'image/webp': 'webp'}.get(r.headers.get_content_type(), 'jpg')
                fn = os.path.join(imgdir, '%s_%d.%s' % (p['id'], n + base, ext))
                open(fn, 'wb').write(r.read())
                im['file'] = fn
            except Exception as e:
                im['err'] = str(e)[:80]


def safe(s):
    return re.sub(r'[\\/:*?"<>|\r\n\t\x00-\x1f]', '', s).strip().rstrip('.')


def write_clips(posts, d, author, corpus):
    """인물 클리핑 md 를 Wei Li 폴더 꼴로 쓴다(frontmatter + 본문 + 그림 링크). 이미 있는 ID 는 건너뛴다."""
    have = known_dir(d)
    # 같은 글이 activity ID 와 ugcPost ID 로 두 번 잡힐 수 있다 — 날짜+제목이 같은 파일이 있으면 건너뛴다
    seen = {os.path.basename(f)[:10] + os.path.basename(f)[11:51] for f in glob.glob(os.path.join(d, '20*.md'))}
    n = 0
    for p in posts:
        if p['id'] in have:
            continue
        first0 = next((l.strip() for l in p['text'].split('\n') if l.strip()), '(본문 없음)')
        if p['kst'][:10] + safe(first0[:40]) in seen:
            continue
        repost = bool(p.get('reshare'))
        media = ['_img/' + os.path.basename(i['file']) for i in p['images'] if i.get('file')]
        if p['video']:
            media.append('video')
        body = p['text']
        if p.get('article'):
            body += '\n\n> 링크 카드: ' + p['article']
        if p.get('yt'):
            body += '\n\n' + '\n'.join('유튜브: ' + u for u in p['yt'])
        pics = [m for m in media if m != 'video']
        if pics:
            body += '\n\n' + '\n'.join('![](%s)' % m for m in pics)
        first = next((l.strip() for l in p['text'].split('\n') if l.strip()), '(본문 없음)')
        date = p['kst'][:10]
        who = ((p['reshare'] or {}).get('actor') or author) if repost else author
        fm = ['---', 'title: "%s"' % first[:60].replace('"', "'"),
              'source: "https://www.linkedin.com/feed/update/urn:li:%s:%s/"' % (p.get('urn_kind') or 'activity', p['id']),
              'author: "%s"' % who.replace('"', "'")]
        if repost:
            fm.append('reposted_by: "%s"' % author)
        fm += ['published: %s' % date, 'posted_kst: "%s"' % p['kst'], 'kind: %s' % ('repost' if repost else 'own'),
               'corpus: %s' % corpus, 'media: ' + json.dumps(media, ensure_ascii=False), '---']
        fn = os.path.join(d, '%s %s [%s].md' % (date, safe(first[:40]), p['id'][-4:]))
        open(fn, 'w', encoding='utf-8').write('\n'.join(fm) + '\n\n' + body.strip() + '\n')
        n += 1
    return n


def write_index(d, author, slug, corpus):
    rows = []
    for f in glob.glob(os.path.join(d, '*.md')):
        b = os.path.basename(f)
        if b.startswith('_'):
            continue
        t = open(f, encoding='utf-8').read()
        head, body = t.split('\n---\n', 1)
        g = lambda k: (re.search(r'^' + k + r': (.*)$', head, re.M) or [None, ''])[1].strip()
        media = g('media')
        m = []
        if media.count('_img/'):
            m.append('그림 %d' % media.count('_img/'))
        if 'video' in media:
            m.append('영상')
        rows.append((g('posted_kst').strip('"'), g('kind'), g('title').strip('"'), len(body.strip()), ', '.join(m), b[:-3]))
    rows.sort(reverse=True)
    own = sum(1 for r in rows if r[1] == 'own')
    out = ['---', 'title: "%s — 링크드인 게시물 색인"' % author,
           'source: "https://www.linkedin.com/in/%s/recent-activity/all/"' % slug,
           'count: %d' % len(rows), 'own: %d' % own, 'repost: %d' % (len(rows) - own),
           'clipped: %s' % datetime.date.today().isoformat(), 'corpus: %s' % corpus, '---', '',
           '<!-- scripts/li_fetch.py 가 쓴다. 게시 시각은 activity URN 에서 풀어낸 KST. -->', '',
           '| 게시(KST) | 종류 | 제목 | 글자 | 매체 | 파일 |', '|---|---|---|---|---|---|']
    for kst_, kind, title, n, m, fn in rows:
        out.append('| %s | %s | %s | %d | %s | [[%s]] |' % (kst_, '본인' if kind == 'own' else '퍼온 글', title.replace('|', '/'), n, m, fn))
    open(os.path.join(d, '_색인.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['company', 'person'])
    ap.add_argument('slug')
    ap.add_argument('--since', required=True, help='YYYY-MM-DD (KST). 이보다 오래된 글이 보이면 스크롤을 멈춘다')
    ap.add_argument('--known', help='person: 이미 받은 클리핑 폴더')
    ap.add_argument('--all', action='store_true', help='이미 아는 글도 posts.json 에 남긴다')
    ap.add_argument('--no-img', action='store_true')
    ap.add_argument('--rounds', type=int, default=120)
    ap.add_argument('--write', help='person: 클리핑 폴더. 새 글을 md 로 쓰고 그림은 <폴더>/_img, 색인을 다시 만든다(--known 기본값도 이 폴더)')
    ap.add_argument('--author', help='--write 와 함께. 폴더 이름과 같은 표기')
    ap.add_argument('--corpus', help='--write 와 함께. 예: li-peccatiello')
    a = ap.parse_args()
    if a.write:
        os.makedirs(a.write, exist_ok=True)
        a.known = a.known or a.write
    since_ms = int((datetime.datetime.strptime(a.since, '%Y-%m-%d') - KST).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
    if a.mode == 'company':
        url = 'https://www.linkedin.com/company/%s/posts/?feedView=all' % a.slug
    else:
        url = 'https://www.linkedin.com/in/%s/recent-activity/all/' % a.slug
    tab = Tab(url)
    try:
        posts = (collect_company if a.mode == 'company' else collect_person)(tab, since_ms, a.rounds)
        rows = sorted((p for p in posts.values() if (int(p['id']) >> 22) >= since_ms), key=lambda p: -int(p['id']))
        if a.mode == 'company':
            kn = known_company()
            for p in rows:
                p['new'] = p['id'] not in kn
        else:
            ids = known_dir(a.known) if a.known else set()
            for p in rows:
                p['new'] = p['id'] not in ids
        new = [p for p in rows if p['new']]
        for p in new:
            if p['video']:
                p['yt'] = youtube_links(tab, p['id'])
    finally:
        tab.close()
    outdir = os.path.join(RUNS, a.slug, datetime.date.today().isoformat())
    os.makedirs(outdir, exist_ok=True)
    keep = rows if a.all else new
    if not a.no_img:
        if a.write:
            download(new, os.path.join(a.write, '_img'), base=1)
        else:
            download(keep, os.path.join(outdir, 'img'))
    if a.write:
        w = write_clips(new, a.write, a.author or a.slug, a.corpus or 'li-' + a.slug)
        total = write_index(a.write, a.author or a.slug, a.slug, a.corpus or 'li-' + a.slug)
        print('wrote %d md, index %d -> %s' % (w, total, a.write))
    json.dump(keep, open(os.path.join(outdir, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('seen %d (since %s), new %d -> %s' % (len(rows), a.since, len(new), os.path.join(outdir, 'posts.json')))
    hdrs = [p.get('hdr') for p in rows if p.get('hdr') and not p.get('reshare')]
    if hdrs:
        print('HDR', max(set(hdrs), key=hdrs.count))
    for p in new:
        flags = ''.join(['I%d' % len(p['images']) if p['images'] else '', ' V' if p['video'] else '',
                         ' D' if p.get('doc') else '', ' R:' + (p['reshare'] or {}).get('actor', '')[:20] if p['reshare'] else '',
                         ' YT' if p['yt'] else ''])
        print('%s %s %4d %-12s %s' % (p['kst'], p['id'], len(p['text']), flags.strip(), p['text'][:70].replace('\n', ' ')))


if __name__ == '__main__':
    main()
