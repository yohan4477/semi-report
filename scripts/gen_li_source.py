# -*- coding: utf-8 -*-
"""링크드인 게시물을 인용 가능한 원문 파일로 떨군다.

  py -3.13 scripts/gen_li_source.py   ->  content/linkedin/[YYMM] 링크드인 게시물.md

왜 필요한가: 통합 인사이트의 인용은 **원문 파일의 줄 번호**이고 cites.json이 그 줄의
해시를 잠근다. 링크드인 글은 지금까지 raw JSON 덤프와 소셜 신호 히스토리 HTML에만
있어서 노트가 source로 가리킬 대상이 없었다 — check_notes N1이 바로 FAIL을 냈다.

두 곳에서 모은다.
  raw/linkedin/linkedin_posts_raw.json   원문 전문(영어). 2026-03~07 수집분
  대시보드/소셜 신호 히스토리.html         우리가 쓴 한국어 요지. 그 뒤로 계속 들어온다
같은 urn이면 원문 전문을 본문으로 쓰고 요지는 머리에 붙인다.

**줄 번호가 인용 기준이라 앞줄이 밀리면 안 된다.** 그래서 월별 파일에 게시 시각
오름차순으로만 쌓는다 — 새 글은 그 달 파일 끝에 붙고, 지난 달 파일은 그대로다.
같은 이유로 이 파일들은 손으로 고치지 않는다.
"""
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import li_signal as ls  # noqa: E402  판정 규칙은 한 곳에만 둔다

RAW = os.path.join(ROOT, 'raw', 'linkedin', 'linkedin_posts_raw.json')
OUTDIR = os.path.join(ROOT, 'content', 'linkedin')

# 덤프 본문 머리에 붙는 UI 부스러기 — 게시물 번호·계정명·팔로워 수·상대시각
JUNK = re.compile(r'^(피드 게시물 번호 \d+|SemiAnalysis|팔로워 [\d,]+명|[^\n]{0,12}(시간|일|주|개월|년) ?•.*|\s*)$')


def kst(aid):
    """activity id 상위 비트가 밀리초 타임스탬프다. 상대 표기를 환산하지 않는다."""
    ms = int(aid) >> 22
    return datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=ms, hours=9)


def body_of(text):
    lines = text.split('\n')
    i = 0
    while i < len(lines) and JUNK.match(lines[i].strip()):
        i += 1
    out = '\n'.join(lines[i:]).strip()
    # 덤프 꼬리의 반응 수·번역 버튼 따위는 본문이 아니다
    out = re.split(r'\n(?:좋아요|댓글 \d+|번역 보기|더 보기)\s*$', out)[0]
    return out.strip()


def from_raw():
    if not os.path.isfile(RAW):
        return {}
    rows = {}
    for p in json.load(io.open(RAW, encoding='utf-8')):
        aid = p['urn'].split(':')[-1]
        b = body_of(p.get('text', ''))
        if b:
            rows[aid] = b
    return rows


def collect():
    hist = io.open(ls.HIST, encoding='utf-8').read()
    pub = ls.publish_dates()
    raw = from_raw()
    rows, seen = {}, set()

    for m in re.finditer(r'urn:li:activity:(\d+)/"[^>]*>(.*?)</a>', hist, re.S):
        aid, title = m.group(1), ls.clean(m.group(2))
        if aid in seen:
            continue
        seen.add(aid)
        seg = hist[m.end():m.end() + 3000]
        dm = re.search(r'<div class="d">(.*?)</div>', seg, re.S)
        nl = re.search(r'newsletter\.semianalysis\.com/p/([a-z0-9-]+)', seg[:2000])
        rows[aid] = {'aid': aid, 'gist': title, 'desc': ls.clean(dm.group(1)) if dm else '',
                     'slug': nl.group(1) if nl else None, 'body': raw.get(aid, '')}

    for aid, body in raw.items():
        if aid not in rows:
            rows[aid] = {'aid': aid, 'gist': '', 'desc': '', 'slug': None, 'body': body}

    out = []
    for r in rows.values():
        t = kst(r['aid'])
        posted = t.strftime('%Y-%m-%d')
        text = ' '.join([r['gist'], r['desc'], r['body'][:1200]])
        kind, usable, basis, lag, push = ls.classify(text, r['slug'], posted, pub)
        r.update({'t': t, 'posted': posted, 'kind': kind, 'usable': usable,
                  'basis': basis, 'lag': lag, 'push': push,
                  'id': 'L-' + posted.replace('-', '') + '-' + r['aid'][-4:]})
        out.append(r)
    out.sort(key=lambda r: r['t'])
    return out


def write_month(ym, rows):
    path = os.path.join(OUTDIR, '[%s] 링크드인 게시물.md' % ym)
    L = ['---',
         'title: "링크드인 게시물 20%s-%s"' % (ym[:2], ym[2:]),
         # 매니페스트가 읽는 날짜다. 묶음 파일이라 그 달 1일로 둔다
         'published: 20%s-%s-01' % (ym[:2], ym[2:]),
         'corpus: li',
         'source: "raw/linkedin/linkedin_posts_raw.json · 대시보드/소셜 신호 히스토리.html"',
         'generator: "scripts/gen_li_source.py"',
         'count: %d' % len(rows),
         '---',
         '',
         '<!-- 생성물이다. 손으로 고치지 않는다. 게시 시각 오름차순으로만 쌓이므로',
         '     새 글이 들어와도 앞줄의 줄 번호는 밀리지 않는다 — 인용이 그 줄에 걸려 있다. -->',
         '']
    for r in rows:
        L.append('## %s · %s' % (r['id'], r['t'].strftime('%Y-%m-%d %H:%M KST')))
        L.append('')
        meta = ['kind: %s' % r['kind'], 'usable: %s' % ('yes' if r['usable'] else 'no')]
        if r['push']:
            meta.append('push: yes')
        L.append('- ' + ' · '.join(meta))
        base = '기준일 %s' % r['basis']
        if r['slug']:
            base += ' (뉴스레터 %s 발행일)' % r['slug']
            if r['lag'] is not None:
                base += ' · 게시까지 %d일' % r['lag']
        else:
            base += ' (게시일)'
        L.append('- ' + base)
        L.append('- https://www.linkedin.com/feed/update/urn:li:activity:%s/' % r['aid'])
        L.append('')
        if r['gist']:
            L.append('요지 — %s' % r['gist'])
            L.append('')
        if r['body']:
            for para in [p.strip() for p in r['body'].split('\n') if p.strip()]:
                L.append(para)
                L.append('')
        elif r['desc']:
            L.append(r['desc'])
            L.append('')
    io.open(path, 'w', encoding='utf-8').write('\n'.join(L))
    return path


def main():
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    rows = collect()
    months = {}
    for r in rows:
        months.setdefault(r['t'].strftime('%y%m'), []).append(r)
    n_body = sum(1 for r in rows if r['body'])
    for ym in sorted(months):
        p = write_month(ym, months[ym])
        print('  %s  %3d건 -> %s' % (ym, len(months[ym]), os.path.basename(p)))
    print('링크드인 원문 %d건 (원문 전문 %d · 요지만 %d) · 월 %d개'
          % (len(rows), n_body, len(rows) - n_body, len(months)))
    print('  사용 가능 %d · 재홍보·홍보(push) %d'
          % (sum(1 for r in rows if r['usable']), sum(1 for r in rows if r['push'])))


if __name__ == '__main__':
    main()
