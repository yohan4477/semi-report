# -*- coding: utf-8 -*-
u"""밸류체인 그림 값 검사 — report_figs.json 의 숫자가 조사 보고서 본문에 있나, 워터폴 산수가 맞나.

  PYTHONIOENCODING=utf-8 python scripts/check_vcfigs.py

F1 값이 보고서 본문에 없다      F2 start − Σsteps ≠ end      F3 히트맵 점수가 1~5 밖
F4 report 경로가 실재하지 않는다   F5 시나리오 막대가 5개 미만
"""
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def nums_in(text):
    out = set()
    for m in re.finditer(r'\d[\d,]*\.?\d*', text):
        t = m.group(0).replace(',', '')
        try:
            out.add(round(float(t), 3))
        except ValueError:
            pass
    return out


def main():
    fails = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'data', 'valuechain', 'chains', '*', 'report_figs.json'))):
        cid = os.path.basename(os.path.dirname(p))
        fg = json.load(io.open(p, encoding='utf-8'))
        rp = os.path.join(ROOT, fg.get('report') or '')
        if not fg.get('report') or not os.path.exists(rp):
            print(u'FAIL F4 %s report 경로가 없다: %s' % (cid, fg.get('report')))
            fails += 1
            continue
        body = io.open(rp, encoding='utf-8').read()
        have = nums_in(body)
        vals = []
        u = fg.get('unit') or {}
        if u.get('steps'):
            vals.append(('unit.start', u['start']['value']))
            vals += [('unit.step %s' % s['label'], s['value']) for s in u['steps']]
            vals.append(('unit.end', u['end']['value']))
            diff = float(u['start']['value']) - sum(float(s['value']) for s in u['steps']) - float(u['end']['value'])
            if abs(diff) > max(1.0, 0.01 * float(u['start']['value'])):
                print(u'FAIL F2 %s 워터폴 산수가 안 맞는다: start − Σsteps − end = %g' % (cid, diff))
                fails += 1
        pl = fg.get('pool') or {}
        if pl.get('cost'):
            vals += [('pool.cost %s' % s['label'], s['value']) for s in pl['cost']]
            vals.append(('pool.price', pl['price']['value']))
        sc = fg.get('scenario') or {}
        if sc.get('bars'):
            vals += [('scenario %s' % b['label'], abs(float(b['value']))) for b in sc['bars']]
            if len(sc['bars']) < 5:
                print(u'FAIL F5 %s 시나리오 막대 %d개 — 다섯은 돼야 한다' % (cid, len(sc['bars'])))
                fails += 1
        for r in (fg.get('heat') or {}).get('rows') or []:
            for k in ('sub', 'lead', 'geo'):
                if not (1 <= int(r[k]) <= 5):
                    print(u'FAIL F3 %s 히트맵 점수 밖: %s %s=%s' % (cid, r['item'], k, r[k]))
                    fails += 1
        for name, v in vals:
            v = round(float(v), 3)
            ok = v in have or (v >= 1000 and round(v / 1000.0, 3) in have) or (v >= 100 and round(v / 100.0, 3) in have) or (v >= 1e6 and round(v / 1e6, 3) in have)
            if not ok:
                print(u'FAIL F1 %s 값 %s=%g 가 보고서 본문에 없다' % (cid, name, v))
                fails += 1
        print(u'%s · 값 %d개' % (cid, len(vals)))
    print(u'요약: FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
