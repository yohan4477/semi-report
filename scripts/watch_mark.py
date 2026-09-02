# -*- coding: utf-8 -*-
"""「확인했다」를 기록하는 스크립트 — 정적 페이지에는 버튼을 못 둔다. 이 스크립트가
버튼이다.

포트폴리오 워치는 한 달에 한 번 열리고, 그 사이에 값이 뭐라고 있었는지는 안 남는다.
「지난 확인 이후」 화면(scratchpad/gen_watch_page.py)이 뭔가 비교하려면 「지난번에
어디까지 봤나」가 파일로 남아 있어야 한다 — 그 파일이 insights/watch/_seen.json 이다.

하는 일 둘.
  ① 지금 이 순간의 상태(값 트리거마다 wl.state_now, 법마다 지금 판)를 _seen.json 에
     스냅숏으로 찍는다.
  ② 모든 줄 md 파일의 frontmatter `checked:` 를 오늘 날짜로 바꾼다. notes_lib.parse_front
     로 읽어 본문을 다시 조립하면 사람이 쓴 줄바꿈·강조가 그 과정에서 뭉개질 수 있다 —
     그래서 frontmatter 그 한 줄만 정규식으로 바꾸고 나머지 텍스트는 안 건드린다.

  PYTHONIOENCODING=utf-8 python scripts/watch_mark.py --dry     무엇이 바뀔지만 본다
  PYTHONIOENCODING=utf-8 python scripts/watch_mark.py           실제로 찍는다(사람이 결정)

--dry 없이 실제로 찍는 것은 사람의 결정이다 — 이 스크립트를 만든 에이전트가 스스로
실행해 checked 날짜를 미리 당겨 놓지 않는다.
"""
import argparse
import datetime
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import watch_lib as wl  # noqa: E402

CHECKED_RE = re.compile(r'^(checked:\s*)\S+\s*$', re.M)


def _paths():
    return [p for p in sorted(glob.glob(os.path.join(wl.WATCH, '*', '*.md')))
            if os.path.basename(os.path.dirname(p)) != '_metrics']


def snapshot():
    """지금 상태를 _seen.json 이 쓰는 꼴로. 값은 wl.state_now 가 내는 표시
    (걸림·근접·멂·사람 판정·—) 그대로 적는다 — 화면·검사기와 다른 말을 지어내지 않는다."""
    value, laws = {}, {}
    for w in wl.load_all():
        for t in w['triggers']:
            if t['kind'] != wl.KIND_VALUE:
                continue
            st, _why = wl.state_now(t['cond'], t['series'])
            value['%s|%s' % (w['slug'], t['what'])] = st
        for _tg, name, seen_at in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            if not now or not seen_at:
                st = '—'
            else:
                st = '같다' if str(now) == seen_at else '걸림'
            laws[name] = st
    return value, laws


def main(dry=False):
    today = datetime.date.today().isoformat()
    value, laws = snapshot()
    data = {'checked': today, 'value': value, 'laws': laws}

    if dry:
        print('DRY: %s 에 값 %d개 · 법 %d개 스냅숏을 찍는다 (checked=%s)'
              % (wl.SEEN, len(value), len(laws), today))
    else:
        with io.open(wl.SEEN, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write('\n')

    for p in _paths():
        with io.open(p, encoding='utf-8') as f:
            text = f.read()
        new, n = CHECKED_RE.subn(r'\g<1>' + today, text, count=1)
        rel = os.path.relpath(p, ROOT)
        if n == 0:
            print('건너뜀(checked 줄이 없다): %s' % rel)
            continue
        if new == text:
            continue        # 이미 오늘 날짜다
        if dry:
            print('DRY: checked -> %s : %s' % (today, rel))
        else:
            with io.open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new)

    print('%s: 오늘(%s)로 확인을 기록했다' % ('DRY' if dry else 'OK', today))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry', action='store_true', help='무엇이 바뀔지만 본다, 안 쓴다')
    args = ap.parse_args()
    main(dry=args.dry)
