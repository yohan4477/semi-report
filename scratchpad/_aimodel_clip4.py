# AI 모델 층 — 영문 클리핑이 빠진 네 편을 받는다 (2026-10-02). clip_articles.py 의 CDP·EXTRACT 를 그대로 쓴다
import sys, os, json, time, datetime
sys.path.insert(0, 'scratchpad')
import clip_articles as ca
import html2text

SLUGS = ['scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data',
         'rl-environments-and-rl-for-science',
         'h100-vs-gb200-nvl72-training-benchmarks',
         'the-coding-assistant-breakdown-more']
h = html2text.HTML2Text(); h.body_width = 0; h.ignore_images = False; h.wrap_links = False
cdp = ca.CDP(ca.get_tab())
for slug in SLUGS:
    cdp.call('Page.navigate', {'url': ca.BASE + slug})
    time.sleep(9)
    d = json.loads(cdp.js(ca.EXTRACT))
    if d.get('error') or not d.get('title'):
        print('FAIL', slug, d.get('error')); continue
    if d['paywalled'] or d['text_len'] < 6000:
        print('PAYWALL', slug, d['text_len']); continue
    fname = os.path.join(ca.OUT_DIR, ca.sanitize(d['title']) + '.md')
    if os.path.exists(fname):
        print('EXISTS', fname); continue
    fm = ['---', 'title: "%s"' % d['title'], 'source: "%s%s"' % (ca.BASE, slug), 'author:'] + \
         ['  - "[[%s]]"' % a for a in (d['authors'] or ['SemiAnalysis'])] + \
         ['published: %s' % d['published'], 'created: %s' % datetime.date.today().isoformat(),
          'description: "%s"' % d['subtitle'][:300].replace('"', "'"), 'tags:', '  - "clippings"', '---', '']
    open(fname, 'w', encoding='utf-8').write('\n'.join(fm) + h.handle(d['html']))
    print('OK', d['published'], d['text_len'], os.path.basename(fname))
cdp.ws.close()
