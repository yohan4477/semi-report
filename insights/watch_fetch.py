# -*- coding: utf-8 -*-
"""워치 수치를 다시 받아 _metrics/ 에 쓴다.

이게 없던 동안 `_metrics/*.json` 은 손으로 돌린 결과였고 **다시 만드는 방법이 코드로
남아 있지 않았다.** 사람 기억이 그 사이를 메우고 있었다.

지키는 것 셋.
1. **줄어들면 안 쓴다.** 어댑터가 받은 열쇠 수가 지난번보다 적으면 덮어쓰지 않는다.
   응답이 반쯤 깨졌을 때 화면의 값이 통째로 사라지는 것을 막는 자리다.
2. **원자적으로 쓴다.** 임시 파일에 다 쓰고 옮긴다. 쓰다 죽으면 옛 파일이 남는다.
3. **소리를 낸다.** 어댑터가 던지면 그 대상만 건너뛰고 끝에 몇 개가 실패했는지 낸다.

    PYTHONIOENCODING=utf-8 python insights/watch_fetch.py            # 전부
    PYTHONIOENCODING=utf-8 python insights/watch_fetch.py 노도강      # 하나만
    PYTHONIOENCODING=utf-8 python insights/watch_fetch.py --dry       # 안 쓰고 보기만
"""
import io, os, sys, json, importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_lib as wl

ADAPTERS = os.path.join(wl.WATCH, 'adapters')


def adapter_for(kind):
    sys.path.insert(0, ADAPTERS)
    try:
        return importlib.import_module(kind)
    except ImportError:
        return None


def areas():
    p = os.path.join(wl.WATCH, '_areas.json')
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def write_atomic(path, obj, prev_n):
    """줄어들면 안 쓴다. 임시 파일에 다 쓰고 옮긴다."""
    if prev_n and len(obj) < prev_n:
        return False, '열쇠가 %d개에서 %d개로 줄었다 — 안 쓴다' % (prev_n, len(obj))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1) + '\n')
    os.replace(tmp, path)
    return True, '열쇠 %d개' % len(obj)


def main(only=None, dry=False):
    ar = areas()
    ok = fail = skip = 0
    for w in wl.load_all():
        if only and only not in (w['target'], w['slug']):
            continue
        mod = adapter_for(w['kind'])
        if mod is None:
            print('  건너뜀 %-22s 어댑터 %s.py 가 없다' % (w['slug'], w['kind']))
            skip += 1
            continue
        area = ar.get(w['target'])
        if area is None:
            print('  건너뜀 %-22s _areas.json 에 %s 가 없다' % (w['slug'], w['target']))
            skip += 1
            continue
        path = os.path.join(wl.METRICS, w['kind'], w['slug'] + '.json')
        prev_n = len(wl.metrics_of(w['kind'], w['slug']))
        try:
            got = mod.fetch(w['target'], area)
        except Exception as e:                       # noqa: BLE001 — 무엇이든 소리를 낸다
            print('  실패   %-22s %s: %s' % (w['slug'], type(e).__name__, e))
            fail += 1
            continue
        if dry:
            print('  (안 씀) %-21s 열쇠 %d개 (지금 %d개)' % (w['slug'], len(got), prev_n))
            ok += 1
            continue
        wrote, why = write_atomic(path, got, prev_n)
        print('  %s %-22s %s' % ('썼다  ' if wrote else '안 씀 ', w['slug'], why))
        ok += 1 if wrote else 0
        fail += 0 if wrote else 1
    print('\n요약: 쓴 것 %d / 실패 %d / 건너뜀 %d' % (ok, fail, skip))
    return fail


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not os.environ.get('REB_API_KEY'):
        print('경고: REB_API_KEY 가 없다 — 앞 몇 건만 오고 성격이 「공표(일부)」로 떨어진다\n')
    sys.exit(1 if main(args[0] if args else None, '--dry' in sys.argv) else 0)
