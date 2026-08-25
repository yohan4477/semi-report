# -*- coding: utf-8 -*-
"""AI Engineer 채널 자막을 통째로 받아 둔다.

  py -3.13 scratchpad/aie_clip.py            # 소속 상위 순서로 전부
  py -3.13 scratchpad/aie_clip.py 60         # 60편만

결과는 scratchpad/yt_subs/<ID>.txt(전문)과 scratchpad/_aie_subs.json(대장).
이미 받은 것은 건너뛴다. 유튜브가 429를 던지면 기다렸다가 다시 집는다 —
한 번에 다 받으려다 막히면 그 뒤가 통째로 밀리므로 천천히 가는 쪽을 택한다.

순서는 소속이 많은 쪽부터다. 같은 회사 발표가 여러 편이면 그 회사가 무엇을
반복해서 말하는지가 먼저 잡히기 때문이다.
"""
import collections, csv, io, json, os, random, sys, time, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

spec = importlib.util.spec_from_file_location(
    'ytsub', os.path.join(ROOT, 'scratchpad', 'ytsub.py'))
ytsub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ytsub)

LIST = os.path.join(ROOT, 'scratchpad', 'aie_list.csv')
OUT = os.path.join(ROOT, 'scratchpad', 'yt_subs')
LEDGER = os.path.join(ROOT, 'scratchpad', '_aie_subs.json')

GAP = 2.0          # 한 편 받고 쉬는 시간(초)
BACKOFF = 90       # 429를 만나면 쉬는 시간. 만날 때마다 늘린다
MAX_BACKOFF = 900


def rows():
    return list(csv.DictReader(io.open(LIST, encoding='utf-8-sig')))


def ordered():
    """소속이 많은 회사부터. 소속을 못 적은 편은 맨 뒤로 민다."""
    rs = rows()
    cnt = collections.Counter(r['소속'] for r in rs if r['소속'])
    def key(r):
        org = r['소속']
        # 같은 회사끼리는 최신 발표가 먼저다
        return (-cnt.get(org, 0), org, r['날짜'] and (10 ** 9 - int(r['날짜'].replace('-', ''))))
    return sorted(rs, key=key)


def vid_of(row):
    return row['링크'].rsplit('/', 1)[-1]


def main(limit=0):
    led = {}
    if os.path.exists(LEDGER):
        led = json.load(io.open(LEDGER, encoding='utf-8'))
    todo = ordered()
    if limit:
        todo = todo[:limit]
    back = BACKOFF
    done = fail = skip = 0
    for n, r in enumerate(todo, 1):
        vid = vid_of(r)
        txt = os.path.join(OUT, vid + '.txt')
        if os.path.exists(txt) and led.get(vid, {}).get('chars'):
            skip += 1
            continue
        tries = 0
        while True:
            tries += 1
            try:
                rc = ytsub.main(vid, 'en')
            except Exception as e:                     # noqa: BLE001
                rc, e_ = 1, str(e)[:120]
            else:
                e_ = ''
            if rc == 0 and os.path.exists(txt):
                chars = len(io.open(txt, encoding='utf-8').read())
                led[vid] = {'id': vid, 'title': r['원제목'], 'org': r['소속'],
                            'speaker': r['발표자'], 'date': r['날짜'], 'chars': chars}
                done += 1
                print('%4d/%d  ok   %s %5d자  %-22s %s'
                      % (n, len(todo), vid, chars, (r['소속'] or '-')[:22], r['제목'][:44]))
                break
            # 자막이 아예 없는 편도 있다 — 세 번 집어 보고 없으면 없는 대로 적어 둔다
            if tries >= 3:
                led[vid] = {'id': vid, 'title': r['원제목'], 'org': r['소속'],
                            'date': r['날짜'], 'chars': 0, 'err': e_ or 'NO_SUB'}
                fail += 1
                print('%4d/%d  FAIL %s  %s' % (n, len(todo), vid, r['제목'][:50]))
                break
            time.sleep(back + random.random() * 10)
            back = min(back * 2, MAX_BACKOFF)
        if n % 10 == 0:
            io.open(LEDGER, 'w', encoding='utf-8').write(
                json.dumps(led, ensure_ascii=False, indent=1))
        time.sleep(GAP + random.random())
    io.open(LEDGER, 'w', encoding='utf-8').write(
        json.dumps(led, ensure_ascii=False, indent=1))
    print('\n받음 %d · 건너뜀 %d · 실패 %d · 대장 %d편' % (done, skip, fail, len(led)))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
