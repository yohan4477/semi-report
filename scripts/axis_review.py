# -*- coding: utf-8 -*-
"""축 검토 — 이미 만든 카드를 다른 기준으로 다시 세워 보고 무엇이 겹치고 비는지 짚는다.

읽기 전용이다. 카드도 대시보드도 축 정의도 쓰지 않는다. 표준출력만 낸다.

  py -3.13 scripts/axis_review.py gen_realestate_dashboard
  py -3.13 scripts/axis_review.py gen_realestate_dashboard --axis region.json
"""
import hashlib
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import axis_lib as al  # noqa: E402


def receipt(root, module, axis):
    path = dict(al.card_modules(root)).get(module, '')
    h = ''
    if path and os.path.isfile(path):
        with io.open(path, 'rb') as f:
            h = hashlib.sha1(f.read()).hexdigest()[:8]
    return {'dashboard': module, 'hash': h, 'axis': axis}


def render(res, rc):
    out = ['%s · 카드 %d장' % (rc['dashboard'], res['cards']),
           '  축 [%s] %s — %s' % (res['axis'], res['shape'],
                                 ' / '.join(c['id'] for c in res['cells']) or '(칸 없음)')]
    for c in res['cells']:
        out.append('    %s  %d장' % (c['id'], c['n']))

    if 'overlap_declared' in res:
        # 선언된 축은 칸이 카드 자신의 section 에서 나오니 빈칸·잔여가 구조상 늘 0이다.
        # 겹침도 사람이 선언한 것이라 이름이 다르다 — 쓸모 있는 수는 이 둘뿐이다
        out.append('  선언된 다중 배치 %d · 쏠림 %s배'
                   % (len(res['overlap_declared']), res['skew']))
    else:
        out.append('  겹침 %d · 빈칸 %d · 잔여 %d장(%d%%) · 쏠림 %s배'
                   % (len(res['overlap']), len(res['empty']),
                      len(res['residual']), res['residual_pct'], res['skew']))

    if len(res['placement']) != res['cards']:
        out.append('  주의 — 배치 %d 대 카드 %d. 제목이 겹친다. 위 숫자들이 실제와 어긋나 있다'
                   % (len(res['placement']), res['cards']))

    for o in res['overlap']:
        out.append('    겹침  %s — %s' % (o['card'], ', '.join(o['cells'])))
    for o in res.get('overlap_declared') or ():
        out.append('    선언된 다중 배치  %s — %s' % (o['card'], ', '.join(o['cells'])))
    if res['empty']:
        out.append('    빈칸  %s' % ', '.join(res['empty']))
        out.append('          아직 안 쓴 것인지 원래 없는 것인지는 사람이 정한다')
    for t in res['residual'][:10]:
        out.append('    잔여  %s' % t)
    if len(res['residual']) > 10:
        out.append('    잔여  … 그리고 %d장 더' % (len(res['residual']) - 10))

    out.append('  — 영수증 — 생성기 %s · 칸 %d개'
               % (rc['hash'] or '(모름)', len(rc['axis']['cells'])))
    out.append('  배치')
    for title in sorted(res['placement']):
        cells = res['placement'][title]
        out.append('    %s  %s' % (title, ', '.join(cells) or '(없음)'))
    return '\n'.join(out)


def main(argv):
    if len(argv) < 2:
        print('쓰기: py -3.13 scripts/axis_review.py <생성기 모듈> [--axis 축.json]')
        print('모듈:', ', '.join(m for m, _ in al.card_modules(ROOT)))
        return 1
    module = argv[1]
    known = [m for m, _ in al.card_modules(ROOT)]
    if module not in known:
        print('그런 생성기가 없다: %s' % module)
        print('있는 것:', ', '.join(known))
        return 1
    cards = al.load_cards(ROOT, module)
    if '--axis' in argv:
        at = argv.index('--axis') + 1
        if at >= len(argv):
            print('--axis 뒤에 축 정의 파일 경로가 있어야 한다')
            return 1
        path = argv[at]
        if not os.path.isfile(path):
            print('축 정의 파일이 없다: %s' % path)
            return 1
        try:
            with io.open(path, encoding='utf-8') as f:
                axis = al.parse_axis(json.load(f))
        except ValueError as e:
            print('축 정의 파일을 읽을 수 없다 — JSON 이 아니거나 구조가 어긋났다: %s — %s'
                 % (path, e))
            return 1
        res = al.review(cards, axis)
    else:
        axis = al.declared_axis(cards)
        res = al.declared_review(cards)
    print(render(res, receipt(ROOT, module, axis)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
