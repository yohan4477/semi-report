# -*- coding: utf-8 -*-
import json, time, sys, io, os, urllib.request
sys.path.insert(0, os.path.join(os.getcwd(), 'scratchpad'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from clip_naver import CDP
req = urllib.request.Request('http://127.0.0.1:9222/json/new?about:blank', method='PUT')
c = CDP(json.loads(urllib.request.urlopen(req).read()))
c.call('Page.navigate', {'url': 'https://contents.premium.naver.com/usa/nasdaq'})
time.sleep(9)
for i in range(4):
    c.js('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2.5)
raw = c.js(r"""(function(){
  var out=[], seen={};
  document.querySelectorAll('a[href*="/contents/"]').forEach(function(a){
    var m=a.href.match(/\/contents\/(\d{6})/); if(!m) return;
    if(seen[a.href]) return; seen[a.href]=1;
    var t=(a.innerText||'').replace(/\s+/g,' ').trim();
    out.push({url:a.href, d:m[1], t:t.slice(0,120)});
  });
  return JSON.stringify(out);
})()""")
c.ws.close()
rows = json.loads(raw or '[]')
rows.sort(key=lambda r: r['d'], reverse=True)
io.open('scratchpad/naver_list.json', 'w', encoding='utf-8').write(json.dumps(rows, ensure_ascii=False, indent=1))
for r in rows[:40]:
    print(r['d'], '|', r['t'][:80])
print('total', len(rows))
