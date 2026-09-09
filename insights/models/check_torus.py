"""토러스 배선 모델을 원문 발표 표와 대조한다.

발표치는 그림 034 에서 읽어 `insights/models/raw/tpuv7.json` 에 옮긴 것이다.
값을 맞추려고 가정을 손대지 않는다. 대조가 끝나면 원문이 안 낸 값을 낸다 —
랙 모양을 바꾸면 광 트랜시버 부착률이 어떻게 움직이나.

    PYTHONIOENCODING=utf-8 python insights/models/check_torus.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                     # noqa: E402
from torus_attach import classify, rack, attach_rate   # noqa: E402

DIMS = (4, 4, 4)          # 랙 하나에 64장. 그림 034 가 「64 TPU Rack」이라고 적었다
KEY = {'꼭짓점': 'Corner', '모서리': 'Edge', '면': 'Face', '안쪽': 'Interior'}
KIND = {'copper': 'Copper Cables', 'pcb': 'PCB Traces',
        'optical': 'Optical Transceivers'}


def _published():
    """발표 표를 (자리 이름, 갈래) → (칩당, 랙 합계) 로 편다."""
    t = table(load_raw('tpuv7'), 'torus_attach_rates')
    out, total = {}, {}
    for row, vals in t['rows'].items():
        per, tot = float(vals[0]), float(vals[1])
        if row.startswith('Total'):
            total[row.split('—')[1].strip()] = (per, tot)
        else:
            head, kind = [s.strip() for s in row.split('—')]
            spot = head.split()[1]          # 「8 Interior TPUs」 → Interior
            out[(spot, kind)] = (per, tot)
    return out, total


def main():
    pub, pub_total = _published()
    groups = classify(DIMS)
    r = rack(DIMS)
    fails = 0

    print('── 자리마다 칩 수와 칩 한 장당 연결 (그림 034 재현) ' + '─' * 18)
    print('%-8s %6s %6s %10s %10s %8s' %
          ('자리', '모델', '발표', '갈래', '칩당 모델', '발표'))
    for k in sorted(groups, reverse=True):
        g = groups[k]
        name = KEY[g['name']]
        for kind_key, kind_en in KIND.items():
            want = pub.get((name, kind_en))
            got = g[kind_key]
            ok = want is not None and abs(got - want[0]) < 1e-9
            fails += not ok
            print('%-8s %6d %6s %10s %10d %8s%s'
                  % (name, g['chips'],
                     '—' if want is None else int(want[1] / max(want[0], 1))
                     if want[0] else g['chips'],
                     kind_en, got,
                     '—' if want is None else '%g' % want[0],
                     '' if ok else '  FAIL'))

    print()
    print('── 랙 합계 — 케이블은 반으로 나누고 트랜시버는 안 나눈다 ' + '─' * 12)
    print('%-16s %12s %12s %12s %12s' %
          ('갈래', '모델 합계', '발표 합계', '모델 칩당', '발표 칩당'))
    pairs = [('Copper Cable', r['copper_cables'], r['copper_per_chip']),
             ('PCB', r['pcb_traces'], r['pcb_per_chip']),
             ('Optical Transceivers', r['transceivers'], r['transceivers_per_chip'])]
    for name, tot, per in pairs:
        want = pub_total.get(name)
        ok = want is not None and abs(tot - want[1]) < 1e-9 and abs(per - want[0]) < 5e-3
        fails += not ok
        print('%-16s %12.0f %12s %12.2f %12s%s'
              % (name, tot, '—' if want is None else '%g' % want[1], per,
                 '—' if want is None else '%g' % want[0],
                 '' if ok else '  FAIL'))

    print()
    print('── 원문에 없는 값 — 랙 모양이 바뀌면 부착률이 어떻게 움직이나 ' + '─' * 6)
    print('원문은 4×4×4 하나만 냈다. 같은 규칙으로 다른 모양을 돌린다.')
    print('%-12s %7s %14s %14s %14s' %
          ('격자', '칩', '광 트랜시버', '칩당 트랜시버', '구리 케이블'))
    for dims in [(2, 2, 2), (4, 4, 4), (4, 4, 8), (8, 8, 8), (16, 16, 16)]:
        x = rack(dims)
        print('%-12s %7d %14.0f %14.2f %14.0f'
              % ('×'.join(map(str, dims)), x['chips'], x['transceivers'],
                 x['transceivers_per_chip'], x['copper_cables']))
    print()
    print('격자가 커지면 끝에 걸린 칩의 몫이 줄어 부착률이 내려간다.')
    print('4×4×4 에서 %.2f, 8×8×8 에서 %.2f, 16×16×16 에서 %.2f 다.'
          % (attach_rate((4, 4, 4)), attach_rate((8, 8, 8)), attach_rate((16, 16, 16))))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
