"""모델 층 검사기 — 모델이 늘어날 때 갈릴 자리를 문다.

모델을 하나 세울 때는 안 걸리는데 셋이 되면 걸리는 것들이 있다. 월을 720시간으로
세는 글과 730시간으로 세는 글이 한 화면에 서고, 원자료 파일이 여럿이 되고, 어떤
모델은 원자료를 안 읽고 코드에 값을 박는다. 그 셋을 여기서 막는다.

    PYTHONIOENCODING=utf-8 python insights/check_model.py
    PYTHONIOENCODING=utf-8 python insights/check_model.py --selftest
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, 'insights', 'models')
RAW = os.path.join(MODELS, 'raw')

findings = []


def add(level, rule, msg):
    findings.append((level, rule, msg))


# ── M1. 월 시간을 코드에 박지 않는다 ───────────────────────────────────
# 글마다 다르다. 720 과 730 이 코드 안에 상수로 서면 부르는 자리에서 어느 쪽인지
# 안 보이고, 두 모델을 이으면 1.4% 가 조용히 어긋난다.
_HOURS = re.compile(r'(?<![\d.])7[23]0(?![\d.])')


def _code_lines(src):
    """문서화 문자열과 주석을 걷고 남은 코드만. 설명에 적은 720 을 물면 안 된다.

    한 줄 안에서 열고 닫는 설명글도 있으므로, 줄을 통째로 버리지 말고 따옴표
    바깥에 남은 글자만 모은다.
    """
    marks = (chr(39) * 3, chr(34) * 3)
    out, in_doc, quote = [], False, ""
    for i, line in enumerate(src.splitlines(), 1):
        rest, code = line, ""
        while rest:
            if in_doc:
                j = rest.find(quote)
                if j < 0:
                    rest = ""
                    break
                rest, in_doc = rest[j + 3:], False
                continue
            hits = [x for x in (rest.find(marks[0]), rest.find(marks[1])) if x >= 0]
            if not hits:
                code += rest
                break
            k = min(hits)
            code += rest[:k]
            quote, rest, in_doc = rest[k:k + 3], rest[k + 3:], True
        code = code.split("#")[0]
        if code.strip():
            out.append((i, code))
    return out


def check_hours():
    for p in sorted(glob.glob(os.path.join(MODELS, '*.py'))):
        name = os.path.basename(p)
        if name.startswith('check_'):
            continue                      # 검사기는 발표치를 그대로 적는 자리다
        src = io.open(p, encoding='utf-8').read()
        for i, line in _code_lines(src):
            if not _HOURS.search(line):
                continue
            if 'HOURS_PER_MONTH' in line or 'hours_per_month' in line:
                continue
            add('FAIL', 'M1',
                '%s:%d 월 시간을 코드에 박았다 — 인자로 받는다: %s'
                % (name, i, line.strip()[:60]))


# ── M2. 원자료 파일마다 출처가 붙어 있나 ───────────────────────────────
# 값이 어느 글 몇 번 그림에서 왔는지, 언제 읽었는지가 없으면 다시 열 자리를 못 찾는다.
_NEED = ('title', 'publisher', 'url', 'published')


def check_raw():
    files = sorted(glob.glob(os.path.join(RAW, '*.json')))
    if not files:
        add('FAIL', 'M2', 'insights/models/raw 에 원자료가 없다')
    for p in files:
        name = os.path.basename(p)
        d = json.loads(io.open(p, encoding='utf-8').read())
        srcs = d.get('sources') or {'_': d.get('source') or {}}
        for key, s in srcs.items():
            miss = [k for k in _NEED if not s.get(k)]
            if miss:
                add('FAIL', 'M2', '%s [%s] 출처가 없다: %s'
                    % (name, key, '·'.join(miss)))
        for t in d.get('tables', []):
            if not t.get('read_on') and not any(
                    s.get('read_on') for s in srcs.values()):
                add('FAIL', 'M2', '%s [%s] 언제 읽었는지가 없다'
                    % (name, t.get('id', '?')))
            if 'redacted' not in t:
                add('WARN', 'M2', '%s [%s] 가려진 칸 목록이 없다 — 없으면 [] 로 적는다'
                    % (name, t.get('id', '?')))


# ── M3. 모델은 원자료를 읽는다 ─────────────────────────────────────────
# 그림에서 읽은 값을 코드에 다시 적으면 원자료와 코드가 갈린다. 검사기(check_*)는
# 발표치를 적는 자리라 뺀다.
def check_reads_raw():
    for p in sorted(glob.glob(os.path.join(MODELS, 'check_*.py'))):
        src = io.open(p, encoding='utf-8').read()
        name = os.path.basename(p)
        if 'load_raw' in src or 'raw' in src.lower():
            continue
        add('WARN', 'M3', '%s 가 원자료를 안 읽는다 — 값이 코드에 박혀 있을 수 있다' % name)


# ── M4. 모델마다 검사기가 있나 ────────────────────────────────────────
def check_paired():
    mods = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(MODELS, '*.py'))}
    for m in sorted(mods):
        if m.startswith('check_') or m in ('common', '__init__'):
            continue
        if not any(c.startswith('check_') and m.split('_')[0] in c for c in mods):
            add('FAIL', 'M4', '%s.py 에 짝이 되는 검사기가 없다' % m)


def selftest():
    """규칙이 결함을 실제로 무는지 본다. 안 물면 규칙이 아니라 장식이다."""
    ok = True
    cases = [
        ('M1 박은 상수', 'x = cost / 730\n', True),
        ('M1 인자로 받음', 'x = cost / hours_per_month\n', False),
        ('M1 주석', '# 월을 730시간으로 센다\n', False),
        ('M1 설명글', chr(34) * 3 + '월을 720시간으로 센다' + chr(34) * 3 + '\n', False),
    ]
    for name, case_src, want in cases:
        got = any(_HOURS.search(l) and 'hours_per_month' not in l
                  for _i, l in _code_lines(case_src))
        if got != want:
            print('선테스트 실패 — %s' % name)
            ok = False
    print('선테스트 %s' % ('OK' if ok else 'FAIL'))
    return 0 if ok else 1


def main():
    if '--selftest' in sys.argv:
        return selftest()
    check_hours()
    check_raw()
    check_reads_raw()
    check_paired()
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    for level, rule, msg in findings:
        print('%s %s %s' % (level, rule, msg))
    models = len([p for p in glob.glob(os.path.join(MODELS, '*.py'))
                  if not os.path.basename(p).startswith('check_')
                  and os.path.basename(p) != 'common.py'])
    print('\n요약: 모델 %d개 / 원자료 %d개 / FAIL %d / WARN %d'
          % (models, len(glob.glob(os.path.join(RAW, '*.json'))), fails,
             len(findings) - fails))
    return 1 if fails else 0


if __name__ == '__main__':
    raise SystemExit(main())
