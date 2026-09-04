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

# 「청약 제도」줄만 — policy 어댑터가 주는 법 판 위에 subscription 어댑터의 청약홈
# 공고 수치를 얹어 같은 _metrics/policy/청약 제도.json 에 쓴다. 다른 정책 줄(임대차
# 제도 등)은 청약홈과 무관하니 슬러그로 딱 이 하나만 짚는다.
SUBSCRIPTION_SLUG = '청약 제도'
# 「정비사업」줄도 같은 꼴 — 법 판(도시정비법·주택법) 위에 rebuild 어댑터가 긁은
# 정비사업 정보몽땅(서울)·경기도 온누리(성남) 사업장 목록을 얹는다(2026-09-04)
REBUILD_SLUG = '정비사업'


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
        # 부동산은 권역 사전이 필요하고 종목은 티커면 된다. 어댑터가 무엇을 받는지는
        # 갈래가 정한다 — 종목에 권역 사전을 물으면 영영 건너뛴다
        if w['kind'] == 'policy':
            # 정책은 조문이 아니라 시행일자를 받는다 — 「내가 본 뒤에 바뀌었나」만 센다
            if not w.get('laws'):
                print('  건너뜀 %-22s laws 가 비어 있다' % w['slug'])
                skip += 1
                continue
            area, key = None, w['target']
        elif w['kind'] == 'realestate':
            area = ar.get(w['target'])
            if area is None:
                print('  건너뜀 %-22s _areas.json 에 %s 가 없다' % (w['slug'], w['target']))
                skip += 1
                continue
            key = w['target']
        else:
            area, key = None, (w['ticker'] or w['target'])
        path = os.path.join(wl.METRICS, w['kind'], w['slug'] + '.json')
        prev_n = len(wl.metrics_of(w['kind'], w['slug']))
        try:
            got = (mod.fetch(key, area, laws=[(a, b) for a, b, _c in w['laws']])
                   if w['kind'] == 'policy' else mod.fetch(key, area))
        except Exception as e:                       # noqa: BLE001 — 무엇이든 소리를 낸다
            print('  실패   %-22s %s: %s' % (w['slug'], type(e).__name__, e))
            fail += 1
            continue
        # 청약 제도 줄만 — 법 판(got) 위에 청약홈 공고 수치를 얹는다. 열쇠가 없거나
        # 실패해도 policy 것은 그대로 남으니 실패로 세지 않는다(경고 한 줄만).
        if w['kind'] == 'policy' and w['slug'] == SUBSCRIPTION_SLUG:
            sub = adapter_for('subscription')
            if sub is None:
                print('  경고   %-22s subscription.py 어댑터가 없다 — 법 판만 쓴다' % w['slug'])
            else:
                try:
                    sub_got = sub.fetch(w['target'])
                except Exception as e:                # noqa: BLE001
                    sub_got = {}
                    print('  경고   %-22s 청약홈 수치를 못 얻었다: %s: %s'
                          % (w['slug'], type(e).__name__, e))
                if sub_got:
                    got.update(sub_got)
                    rate_err = getattr(sub.fetch, 'rate_error', None)
                    if rate_err:
                        print('  경고   %-22s 경쟁률(15098905)을 못 얻었다: %s'
                              % (w['slug'], rate_err))
                else:
                    print('  경고   %-22s 청약홈 수치 없음 — %s'
                          % (w['slug'], getattr(sub.fetch, 'last_error', None) or '사유 불명'))
        if w['kind'] == 'policy' and w['slug'] == REBUILD_SLUG:
            rb = adapter_for('rebuild')
            if rb is None:
                print('  경고   %-22s rebuild.py 어댑터가 없다 — 법 판만 쓴다' % w['slug'])
            else:
                try:
                    rb_got = rb.fetch(w['target'])
                except Exception as e:                # noqa: BLE001
                    rb_got = {}
                    print('  경고   %-22s 정비사업 목록을 못 얻었다: %s: %s'
                          % (w['slug'], type(e).__name__, e))
                if rb_got:
                    got.update(rb_got)
                    err = getattr(rb.fetch, 'last_error', None)
                    if err:
                        print('  경고   %-22s 한쪽 원천이 빠졌다: %s' % (w['slug'], err))
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
