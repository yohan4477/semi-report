# -*- coding: utf-8 -*-
# How To Scale Your Model (jax-ml.github.io/scaling-book) 열세 장을 마크다운으로 받는다.
# 산출: content/scaling-book/원문/NN-slug.md — 본문(article)만, 내비·각주 스크립트는 걷는다.
import io, os, re, sys, urllib.request
import html2text
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'content', 'scaling-book', '원문')
BASE = 'https://jax-ml.github.io/scaling-book/'
CH = ['index', 'roofline', 'tpus', 'sharding', 'transformers', 'training',
      'applied-training', 'inference', 'applied-inference', 'profiling',
      'jax-stuff', 'conclusion', 'gpus']

h = html2text.HTML2Text()
h.body_width = 0
h.ignore_images = False
h.ignore_links = False
h.mark_code = True

for i, slug in enumerate(CH):
    url = BASE + ('' if slug == 'index' else slug)
    raw = urllib.request.urlopen(url, timeout=60).read().decode('utf-8')
    soup = BeautifulSoup(raw, 'html.parser')
    for t in soup(['script', 'style', 'nav', 'header', 'footer']):
        t.decompose()
    art = soup.find('article') or soup.find('d-article') or soup.body
    for t in art.select('d-byline, .giscus, #giscus, d-contents, .contents'):
        t.decompose()
    md = h.handle(str(art))
    md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
    title = (soup.title.string or slug).split('|')[0].strip()
    head = '---\ntitle: %s\nurl: %s\npart: %d\nslug: %s\n---\n\n' % (title, url, i, slug)
    path = os.path.join(OUT, '%02d-%s.md' % (i, slug))
    io.open(path, 'w', encoding='utf-8').write(head + md)
    print('%02d %-18s %6d자  %s' % (i, slug, len(md), title))
