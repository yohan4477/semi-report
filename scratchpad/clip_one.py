# -*- coding: utf-8 -*-
# 카레라 유료글 한 편 클리핑 → scratchpad/naver_<YYYYMMDD>.txt (로컬 전용, 커밋 금지)
import json, time, sys, io, os, urllib.request
sys.path.insert(0, os.path.join(os.getcwd(), 'scratchpad'))
from clip_naver import CDP, EXTRACT
url, day = sys.argv[1], sys.argv[2]
req = urllib.request.Request('http://127.0.0.1:9222/json/new?about:blank', method='PUT')
c = CDP(json.loads(urllib.request.urlopen(req).read()))
c.call('Page.navigate', {'url': url})
time.sleep(11)
d = json.loads(c.js(EXTRACT))
c.ws.close()
out = os.path.join('scratchpad', 'naver_%s.txt' % day)
io.open(out, 'w', encoding='utf-8').write(d['text'])
print(d['og_title'], '| len', d['text_len'], '| paywalled', d['paywalled'], '->', out)
