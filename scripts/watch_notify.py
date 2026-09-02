# -*- coding: utf-8 -*-
"""워치 알림 — 봇이 지난번에 알린 상태와 지금 상태를 견줘 「새로 걸린 것」만 낸다.

포트폴리오 워치(insights/watch/*.md)는 그 자체로 지금 상태를 보여 준다
(scratchpad/gen_watch_page.py 의 fired()). 하지만 그건 매달 같은 조건이 계속 걸려
있어도 계속 「걸림」이라고만 말할 뿐, 이번 달에 "새로" 걸렸는지는 모른다. 이 스크립트가
그 자리를 채운다 — 이전 실행이 insights/watch/_notified.json 에 남긴 상태와 지금 상태를
비교해서 달라진 것만 골라낸다.

**_notified.json 과 _seen.json 은 다른 파일이다 — 섞으면 안 된다.** _seen.json 은
「사람이 마지막으로 이 줄을 읽고 확인한 상태」이고 scripts/watch_mark.py 만 쓴다 —
사람이 카드를 열어 「봤다」고 표시할 때만 움직인다. 이 스크립트(봇)는 그 파일을
읽지도 쓰지도 않는다. 봇이 매달 자동으로 _seen.json 을 덮어쓰면 대시보드의
「지난 확인 이후 무엇이 바뀌었나」가 사람이 실제로 보지 않았는데도 리셋된다 —
알림을 보낸 것과 사람이 그걸 읽은 것은 서로 다른 시점이고, 하나로 두면 "봇이 알렸다"가
"사람이 확인했다"를 대신해 버린다. 그래서 봇은 자기 몫의 기준선을
insights/watch/_notified.json 에 따로 둔다 — 꼴은 같지만(checked 대신 notified 키)
주체와 갱신 시점이 다른 별개의 파일이다.

_notified.json 의 꼴:
    {"notified": "YYYY-MM-DD",
     "value": {"<slug>|<트리거 무엇을>": "걸림|근접|평온|—"},
     "laws": {"<법 이름>": "<지금 판 YYYY-MM-DD>"}}

파일이 아직 없거나 어떤 열쇠가 그 안에 없으면 "이전에 확인한 적이 없다"로 본다 —
비교할 기준이 없으므로 그 열쇠는 이번엔 "새로 걸렸다"로 세지 않고 조용히 기준선만
남긴다. 처음 실행할 때(또는 워치 줄을 새로 추가했을 때) 이미 걸려 있던 조건을 전부
"새로 걸린 것"으로 쏟아내면 그게 소음이 된다 — 대시보드를 열면 이미 보이는 것들이다.

이 스크립트는 insights/watch/_notified.json 을 읽고 실행 끝에 다시 쓴다. 커밋은
워크플로(.github/workflows/watch.yml)가 한다 — gen_watch_page.py 산출물과 같은
커밋에 묶는다.
"""
import io
import os
import sys
import json
import argparse
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import watch_lib as wl  # noqa: E402

NOTIFIED_PATH = os.path.join(ROOT, 'insights', 'watch', '_notified.json')

# 저장소 밖으로 나가는 값은 넷뿐이다 — state_now() 가 내는 다섯 가지 표시를 이 넷으로
# 접는다. '사람 판정'(조건을 기계가 못 읽는다)은 걸림·근접이 될 수 없으니 '평온'으로
# 둔다 — 신호가 아니라는 뜻만 남으면 된다.
COARSE = {'걸림': '걸림', '근접': '근접', '멂': '평온', '사람 판정': '평온', '—': '—'}

# scripts/gen_site.py 의 PAGES 에서 슬러그를 확인했다 — ('포트폴리오 워치.html', 'watch', ...)
DASHBOARD_URL = 'https://insight-dashboard.com/watch'


def kst_today():
    """워크플로가 KST 로 도니 날짜도 KST 로 잰다 — market.yml 의 TZ=Asia/Seoul 관례."""
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date()


def load_notified():
    if not os.path.exists(NOTIFIED_PATH):
        return {'notified': None, 'value': {}, 'laws': {}}
    with io.open(NOTIFIED_PATH, encoding='utf-8') as f:
        d = json.load(f)
    d.setdefault('value', {})
    d.setdefault('laws', {})
    return d


def save_notified(d):
    with io.open(NOTIFIED_PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def title_of(w):
    """gen_watch_page.py 의 title_of() 와 같은 규칙 — 그 파일은 동시에 다른 작업이
    고치고 있어 임포트하지 않고 여기서 그대로 되풀이한다."""
    return '%s — %s' % (w['target'], w['view']) if w.get('view') else w['target']


def collect():
    """지금 상태를 읽어 (새 기준선, 새로 걸린 것, 새로 근접, 풀린 것, 법 개정) 을 낸다."""
    old = load_notified()
    new_value, new_laws = {}, {}
    fired, near, resolved, law_changes = [], [], [], []

    for w in wl.load_all():
        t9 = title_of(w)
        for t in w['triggers']:
            if t['kind'] != wl.KIND_VALUE:
                continue
            key = '%s|%s' % (w['slug'], t['what'])
            st, why = wl.state_now(t['cond'], t['series'])
            cur = COARSE.get(st, '평온')
            new_value[key] = cur
            prev = old['value'].get(key)
            row = (t9, t['what'], t['value'], t['unit'], t['cond'], t['as_of'] or '—', why)
            if prev is None:
                continue  # 기준선이 없다 — 이번엔 세지 않고 조용히 채운다
            if prev != '걸림' and cur == '걸림':
                fired.append(row)
            elif prev not in ('걸림', '근접') and cur == '근접':
                near.append(row)
            elif prev in ('걸림', '근접') and cur not in ('걸림', '근접'):
                resolved.append(row)

        for _tgt, name, _seen_in_md in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now_val = m.get('value')
            if now_val:
                new_laws[name] = now_val
                prev_law = old['laws'].get(name)
                if prev_law is not None and str(prev_law) != str(now_val):
                    law_changes.append((name, now_val, prev_law))
            elif name in old['laws']:
                new_laws[name] = old['laws'][name]  # 이번엔 못 받았다 — 기존 값을 지키지 않는다면 사라진다

    new_notified = {'notified': kst_today().isoformat(), 'value': new_value, 'laws': new_laws}
    return new_notified, fired, near, resolved, law_changes


def fmt_row(row):
    t9, what, val, unit, cond, as_of, why = row
    val_s = '—' if val is None else ('%s%s' % (val, unit) if unit else str(val))
    return '- **%s** — %s — 지금 %s · 조건 %s · %s (%s)' % (
        t9, what, val_s, cond, as_of, why)


def fmt_law(row):
    name, now_val, prev_val = row
    return '- **%s** — 지금 판 %s (전에 본 판 %s)' % (name, now_val, prev_val)


def build_report(fired, near, resolved, law_changes):
    month = kst_today().strftime('%Y-%m')
    title = '워치 — 새로 걸린 것 %d · 새로 근접 %d · 풀린 %d (%s)' % (
        len(fired), len(near), len(resolved), month)

    if not fired and not near and not law_changes:
        return title, ''

    parts = [title, '']
    if fired:
        parts.append('## 새로 걸린 것')
        parts += [fmt_row(r) for r in fired]
        parts.append('')
    if near:
        parts.append('## 새로 근접')
        parts += [fmt_row(r) for r in near]
        parts.append('')
    if law_changes:
        parts.append('## 법 개정')
        parts += [fmt_law(r) for r in law_changes]
        parts.append('')
    if resolved:
        parts.append('## 풀린 것')
        parts += [fmt_row(r) for r in resolved]
        parts.append('')
    parts.append('화면: %s' % DASHBOARD_URL)
    return title, '\n'.join(parts).rstrip() + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title-only', action='store_true',
                     help='제목 줄만 낸다 — 이슈 제목으로 쓸 때')
    args = ap.parse_args()

    new_notified, fired, near, resolved, law_changes = collect()
    title, body = build_report(fired, near, resolved, law_changes)
    save_notified(new_notified)

    if args.title_only:
        if body:
            print(title)
        return

    if body:
        sys.stdout.write(body)


if __name__ == '__main__':
    main()
