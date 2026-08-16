# -*- coding: utf-8 -*-
# 미국주식 사관학교(네이버 프리미엄) 여러 편을 한 번에 클리핑 → 로컬 볼트에만 저장.
# 유료 구독 콘텐츠라 공개 저장소엔 커밋 금지 — 공개엔 요약만.
import json, time, sys, io, os, re, datetime, urllib.request

sys.path.insert(0, os.path.join(os.getcwd(), 'scratchpad'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from clip_naver import CDP, EXTRACT

VAULT = r"C:\Users\y\semi_docs\Clippings\미국주식 사관학교"
URLS = [
    'https://contents.premium.naver.com/usa/nasdaq/contents/260302154215384ia',
    'https://contents.premium.naver.com/usa/nasdaq/contents/260420133218168yx',
    'https://contents.premium.naver.com/usa/nasdaq/contents/260429130220884jr',
    'https://contents.premium.naver.com/usa/nasdaq/contents/260703131526618hl',
    'https://contents.premium.naver.com/usa/nasdaq/contents/260710024312597hb',
]

def pub_from_url(u):
    m = re.search(r'/contents/(\d{6})', u)
    return '20%s-%s-%s' % (m.group(1)[:2], m.group(1)[2:4], m.group(1)[4:6]) if m else ''


def sanitize(n):
    return re.sub(r'[\\/:*?"<>|]', '', n).strip()[:150]


req = urllib.request.Request('http://127.0.0.1:9222/json/new?about:blank', method='PUT')
cdp = CDP(json.loads(urllib.request.urlopen(req).read()))
os.makedirs(VAULT, exist_ok=True)
out = []
for u in URLS:
    cdp.call('Page.navigate', {'url': u})
    time.sleep(9)
    d = json.loads(cdp.js(EXTRACT))
    pub = pub_from_url(u)
    ok = (not d['paywalled']) and d['text_len'] > 1500
    print('%s | %s | len=%d | paywalled=%s | %s' % (pub, 'OK ' if ok else 'FAIL', d['text_len'], d['paywalled'], d['og_title']))
    if not ok:
        continue
    fm = ['---', 'title: "%s"' % d['og_title'], 'source: "%s"' % u,
          'author:', '  - "[[카레라]]"', '  - "[[미국주식 사관학교]]"',
          'published: %s' % pub, 'created: %s' % datetime.date.today().isoformat(),
          'tags:', '  - "clippings"', '  - "naver-premium"', '---', '']
    f = os.path.join(VAULT, sanitize(d['og_title']) + '.md')
    io.open(f, 'w', encoding='utf-8').write('\n'.join(fm) + '# ' + d['og_title'] + '\n\n' + d['text'])
    # 요약 작성용으로 본문만 따로 — 메인 세션이 읽을 파일
    io.open(os.path.join('scratchpad', 'naver_%s.txt' % pub.replace('-', '')), 'w', encoding='utf-8').write(
        d['og_title'] + '\n\n' + d['text'])
    out.append({'url': u, 'pub': pub, 'title': d['og_title'], 'len': d['text_len'], 'vault': f})
cdp.ws.close()
json.dump(out, io.open(os.path.join('scratchpad', 'naver_batch.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nsaved', len(out), 'of', len(URLS))
