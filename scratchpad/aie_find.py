# -*- coding: utf-8 -*-
"""받아 둔 자막 전부를 가로질러 찾는다.

한 편을 처리할 때마다 그 편 자막만 읽으면 「어느 발표가 이 이야기를 했더라」를
영영 못 찾는다. 자막은 1,152편이 이미 `scratchpad/yt_subs/*.txt` 에 있는데 찾을
길이 없었다. 이 도구가 그 자리를 맡는다.

대장(`_aie_subs.json`)에 오른 1,057편 중 1,055편이 여기 있다. 나머지 둘은
유튜브에 자막 자체가 없어(`err: NO_SUB`) 받을 것이 없다. 대장 밖 97편도 함께
들어 있고 그런 편은 소속·날짜가 비어 나온다.

대시보드에 카드로 오른 것은 그중 81편이다. 나머지가 「카드없음」으로 나오는 것은
빠뜨려서가 아니라 처음부터 고르지 않았기 때문이다.

  py -3.13 scratchpad/aie_find.py "context graph"
  py -3.13 scratchpad/aie_find.py "eval" --org OpenAI --per 3
  py -3.13 scratchpad/aie_find.py "cache" --status todo --count
  py -3.13 scratchpad/aie_find.py --list --year 2026 --org Google

옵션
  --org NAME    소속으로 거른다(부분 일치, 대소문자 무시)
  --year YYYY   연도로 거른다
  --status S    report | num | none | done | todo  (아래 「상태」 참조)
  --and A,B     쉼표로 나눈 낱말이 **모두** 나오는 편만
  --word        낱말 경계에 맞춰 찾는다(부분어 배제)
  --re          패턴을 정규식 그대로 쓴다
  --count       조각을 빼고 편마다 적중 수만
  --list        패턴 없이 목록만
  --per N       한 편에서 보일 조각 수 (기본 2)
  --limit N     보일 편 수 (기본 20, 0이면 전부)
  --ctx N       조각 앞뒤 글자 수 (기본 90)

상태 — 자막이 어디까지 갔나
  report  카드가 보고서로 옮겨졌다
  num     카드는 있는데 아직 옛 번호글이다
  none    카드가 없다
  done    report 와 같다
  todo    num + none
  뒤에 `+표` 가 붙으면 `scratchpad/aie_facts/<ID>.md` 가 있다는 뜻이다.

찾는 자리는 `yt_subs/*.txt` 뿐이다. 같은 폴더의 `.vtt` 는 같은 말이 시간표와
함께 두 번 들어 있어 걸러 낸다 — 넣으면 적중 수가 두 배로 부풀고 조각도 깨진다.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBS = os.path.join(ROOT, 'scratchpad', 'yt_subs')
FACTS = os.path.join(ROOT, 'scratchpad', 'aie_facts')
LEDGER = os.path.join(ROOT, 'scratchpad', '_aie_subs.json')
CARDS = os.path.join(ROOT, 'content', 'understanding', 'AI Engineer')


def meta():
    """영상 ID 마다 대장·카드·사실표를 한 자리에 모은다."""
    out = {}
    if os.path.exists(LEDGER):
        for vid, row in json.load(io.open(LEDGER, encoding='utf-8')).items():
            out[vid] = {'title': row.get('title') or '', 'org': row.get('org') or '',
                        'speaker': row.get('speaker') or '', 'date': row.get('date') or '',
                        'ko': '', 'state': 'none'}
    if os.path.isdir(CARDS):
        for fn in sorted(os.listdir(CARDS)):
            if not fn.endswith('.md'):
                continue
            head = io.open(os.path.join(CARDS, fn), encoding='utf-8').read(1400)
            src = re.search(r'^source: *(\S+)', head, re.M)
            if not src:
                continue
            vid = src.group(1).rsplit('/', 1)[-1].split('?')[0]
            row = out.setdefault(vid, {'title': '', 'org': '', 'speaker': '',
                                       'date': '', 'ko': '', 'state': 'none'})
            ttl = re.search(r'^title: *(.+)', head, re.M)
            row['ko'] = (ttl.group(1).strip() if ttl else fn[:-3])
            row['state'] = 'report' if re.search(r'^format: *report', head, re.M) else 'num'
    for vid, row in out.items():
        row['facts'] = os.path.exists(os.path.join(FACTS, vid + '.md'))
    return out


def keep(row, org, year, state):
    if org and org.lower() not in (row.get('org') or '').lower():
        return False
    if year and not (row.get('date') or '').startswith(year):
        return False
    if state:
        s = row.get('state', 'none')
        if state == 'done':
            return s == 'report'
        if state == 'todo':
            return s in ('num', 'none')
        return s == state
    return True


def label(vid, row):
    mark = {'report': '보고서', 'num': '번호글', 'none': '카드없음'}[row.get('state', 'none')]
    if row.get('facts'):
        mark += '+표'
    name = row.get('ko') or row.get('title') or '(대장에 없음)'
    return '%-11s  %-10s  %-16s %-9s %s' % (
        vid, row.get('date') or '', (row.get('org') or '')[:16], mark, name[:70])


def snip(text, m, ctx):
    a, b = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
    s = text[a:b].replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return ('…' if a else '') + s + ('…' if b < len(text) else '')


def main(argv):
    args, opt = [], {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith('--'):
            key = a[2:]
            if key in ('count', 'list', 'word', 're'):
                opt[key] = True
            else:
                i += 1
                opt[key] = argv[i] if i < len(argv) else ''
        else:
            args.append(a)
        i += 1

    listing = opt.get('list')
    if not args and not listing:
        print(__doc__)
        return 0

    pat = args[0] if args else ''
    also = [t.strip() for t in (opt.get('and') or '').split(',') if t.strip()]
    per = int(opt.get('per', 2))
    limit = int(opt.get('limit', 20))
    ctx = int(opt.get('ctx', 90))
    org, year, state = opt.get('org'), opt.get('year'), opt.get('status')

    info = meta()
    if listing:
        rows = [(info[v].get('date') or '', v) for v in info if keep(info[v], org, year, state)]
        rows.sort(reverse=True)
        for _, v in (rows if not limit else rows[:limit]):
            print(label(v, info[v]))
        print('\n%d편' % len(rows))
        return 0

    body = pat if opt.get('re') else re.escape(pat)
    if opt.get('word'):
        body = r'\b%s\b' % body
    rx = re.compile(body, re.I)
    extra = [re.compile(re.escape(t), re.I) for t in also]

    hits = []
    for fn in sorted(os.listdir(SUBS)):
        if not fn.endswith('.txt'):
            continue
        vid = fn[:-4]
        row = info.setdefault(vid, {'title': '', 'org': '', 'speaker': '', 'date': '',
                                    'ko': '', 'state': 'none', 'facts': False})
        if not keep(row, org, year, state):
            continue
        text = io.open(os.path.join(SUBS, fn), encoding='utf-8', errors='replace').read()
        ms = list(rx.finditer(text))
        if not ms:
            continue
        if extra and not all(r.search(text) for r in extra):
            continue
        hits.append((len(ms), vid, text, ms))

    hits.sort(key=lambda h: (-h[0], h[1]))
    shown = hits if not limit else hits[:limit]
    for n, vid, text, ms in shown:
        print('%s   [%d]' % (label(vid, info[vid]), n))
        if not opt.get('count'):
            for m in ms[:per]:
                print('    %s' % snip(text, m, ctx))
            print('')
    print('%d편 적중 / 조각 %d개%s' % (len(hits), sum(h[0] for h in hits),
                                    '' if len(shown) == len(hits) else ' (%d편만 보임)' % len(shown)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
