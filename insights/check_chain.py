# -*- coding: utf-8 -*-
"""체인 추출물 — 줄 주소가 실재하는 줄을 가리키나, 사슬이 사슬 꼴인가.

    PYTHONIOENCODING=utf-8 python insights/check_chain.py

왜 있나 — 체인 카드는 「어느 단계에 누가 있고 어디가 병목인가」를 말한다. 그 말의 근거는
씨모어 전사 원문 한 줄뿐이라, 줄 주소가 빗나가면 카드 전체가 근거 없는 주장이 된다.
2026-09-09 첫 추출에서 서브에이전트 열 기가 저마다 줄을 셌으므로 기계가 전수로 짚는다.

규약
  C1  L숫자~L숫자(또는 L숫자) 꼴이어야 한다. 떨어진 대목은 쉼표로 잇는다
      — 「L71~L72, L107~L115」. 구간마다 따로 검사한다
  C2  그 줄이 원문 파일에 실재해야 한다 (파일 끝 넘기면 FAIL)
  C3  가리킨 구간이 전부 빈 줄이면 FAIL
  C4  companies 의 name 이 그 구간 어딘가에 나와야 한다 (raw_name 도 본다) — 확인 필요
  C5  stages 의 order 가 1부터 빈틈없이 이어져야 한다
  C6  bottleneck 은 high|mid|low|"" 넷뿐. high 면 bottleneck_why 와 bottleneck_lines 가 있어야 한다
  C7  chains 가 비지 않았으면 stages 가 둘 이상이어야 한다 (사슬은 마디가 둘부터)

C4 는 자동 자막이 이름을 뭉개는 일이 잦아 FAIL 이 아니라 「확인 필요」로 센다.
"""
import glob, io, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(ROOT, 'insights', 'chains', 'extract', '*.json')
RAWDIR = os.path.join(ROOT, 'content', 'understanding', '채널 씨모어', 'raw')

LINE_RE = re.compile(r'^L(\d+)(?:~L(\d+))?$')
_cache = {}


def raw_lines(slug):
    if slug not in _cache:
        p = os.path.join(RAWDIR, slug + '.md')
        if not os.path.exists(p):
            _cache[slug] = None
        else:
            _cache[slug] = io.open(p, encoding='utf-8').read().split('\n')
    return _cache[slug]


def span(lines, ref):
    """줄 주소를 실제 텍스트로 편다. (본문, 사유) — 사유가 있으면 결함.

    떨어진 대목은 쉼표로 이어 짚는다. 원문이 같은 회사를 앞뒤로 나눠 말하는 일이 잦다
    (제약 병목 회차는 단계 설명과 병목 판정이 예순 줄 떨어져 있다). 구간마다 따로 본다."""
    if not (ref or '').strip():
        return None, 'C1 줄 주소가 비었다'
    out = []
    for part in ref.split(','):
        m = LINE_RE.match(part.strip())
        if not m:
            return None, 'C1 꼴이 아니다: %r' % ref
        a = int(m.group(1))
        b = int(m.group(2) or m.group(1))
        if a < 1 or b < a:
            return None, 'C1 번호가 거꾸로거나 0이다: %s' % part.strip()
        if b > len(lines):
            return None, 'C2 파일은 %d줄인데 %s 를 가리킨다' % (len(lines), part.strip())
        out.append('\n'.join(lines[a - 1:b]))
    body = '\n'.join(out)
    if not body.strip():
        return None, 'C3 빈 줄만 가리킨다: %s' % ref
    return body, None


fail, warn, ok, files, chains, stages_n = [], [], 0, 0, 0, 0
for path in sorted(glob.glob(EXTRACT)):
    files += 1
    name = os.path.basename(path)
    try:
        d = json.load(io.open(path, encoding='utf-8'))
    except Exception as e:
        fail.append((name, '', 'JSON 을 못 읽는다: %s' % e))
        continue
    slug = d.get('slug') or name[:-5]
    lines = raw_lines(slug)
    if lines is None:
        fail.append((name, '', '원문 %s.md 가 없다' % slug))
        continue

    def cite(ref, where):
        global ok
        if not ref:
            return
        body, why = span(lines, ref)
        if why:
            fail.append((name, where, why))
        else:
            ok += 1
        return body

    for ci, ch in enumerate(d.get('chains') or []):
        chains += 1
        tag = '%s#%d' % (ch.get('chain_name', '?'), ci + 1)
        cite(ch.get('chain_lines'), tag)
        st = ch.get('stages') or []
        if len(st) < 2:
            fail.append((name, tag, 'C7 마디가 %d개다 — 사슬이 아니다' % len(st)))
        orders = [s.get('order') for s in st]
        if orders != list(range(1, len(st) + 1)):
            fail.append((name, tag, 'C5 order 가 1..%d 가 아니다: %s' % (len(st), orders)))
        for s in st:
            stages_n += 1
            w = '%s/%s' % (tag, s.get('name', '?'))
            cite(s.get('lines'), w)
            bn = s.get('bottleneck', '')
            if bn not in ('high', 'mid', 'low', ''):
                fail.append((name, w, 'C6 bottleneck 값이 %r' % bn))
            if bn == 'high':
                if not (s.get('bottleneck_why') or '').strip():
                    fail.append((name, w, 'C6 high 인데 이유가 없다'))
                if not (s.get('bottleneck_lines') or '').strip():
                    fail.append((name, w, 'C6 high 인데 줄 주소가 없다'))
                cite(s.get('bottleneck_lines'), w + '(병목)')
            for c in s.get('companies') or []:
                body = cite(c.get('lines'), w + '/' + c.get('name', '?'))
                if body:
                    nm = (c.get('name') or '').strip()
                    rn = (c.get('raw_name') or '').strip()
                    if nm and nm not in body and (not rn or rn not in body):
                        warn.append((name, w, 'C4 「%s」가 그 줄에 없다 (%s)' % (nm, c.get('lines'))))

for f in fail:
    print('FAIL %s [%s] %s' % f)
for w in warn:
    print('확인필요 %s [%s] %s' % w)
print('---')
print('파일 %d · 체인 %d · 마디 %d · 짚은 줄 %d · FAIL %d · 확인필요 %d'
      % (files, chains, stages_n, ok, len(fail), len(warn)))
sys.exit(1 if fail else 0)
