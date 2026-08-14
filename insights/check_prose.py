# 문체 게이트 — 인사이트 문장이 읽히는 한국어인지 검사한다. 윤문은 하지 않는다.
# 설계: docs/superpowers/specs/2026-07-30-스킬-분할-구조화-design.md ④
# 규칙이 이미 스펙 문체 절에 표로 있어 결정론적으로 검사할 수 있다 — 에이전트 호출 0회.
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import notes_lib as nl

GLOSSARY = os.path.join(paths.ROOT, 'insights', 'views', 'glossary.json')


# 아래 둘은 원자 검사기(check_atoms)에 있던 것을 옮겨왔다. 원자를 걷어내면서
# 이 검사기가 같이 죽지 않도록 여기로 내린다.
def parse_synth(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.DOTALL)
    if not m:
        return None, text
    meta, body = {}, m.group(2)
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w+):\s*(.*)$', line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip()
        if v.startswith('['):
            v = [x.strip() for x in v.strip('[]').split(',') if x.strip()]
        meta[k] = v
    return meta, body


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r'^##\s+(.+?)\s*$', line)
        if h:
            cur = h.group(1)
            out[cur] = []
        elif cur and line.strip():
            out[cur].append(line.strip())
    return out

# 용어가 아니라 문장을 망가뜨리는 것들 — 어느 회사인지 모르면 문장이 성립하지 않고,
# 다른 분야 비유는 이 문서의 용어가 아니다
BANNED = ['벤더', '진영', '커스텀 실리콘', '헤지', '익스포저']

REF = re.compile(r'\(\s*A-\d{6}-\d{2}(?:\s*,\s*A-\d{6}-\d{2})*\s*\)')
FM = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def strip_refs(text):
    """인용과 frontmatter를 떨어낸 서술만 남긴다 — 검사 대상은 사람이 쓴 문장이다.
    (파일 L줄) 인용은 파일명이 통째로 들어 있어, 안 떼면 파일명 속 'HBM'을
    풀지 않은 용어로 잡는다."""
    text = FM.sub('', text or '')
    text = REF.sub('', text)
    return nl.CITE.sub('', text)


def sentences(text):
    parts = re.split(r'(?<=[.!?])\**\s+|\n+', text or '')
    return [p.strip() for p in parts if p.strip()]


def load_glossary():
    if not os.path.exists(GLOSSARY):
        return {}
    return {k: v for k, v in json.load(io.open(GLOSSARY, encoding='utf-8')).items()
            if not k.startswith('_')}


def check_banned(text, where):
    for w in BANNED:
        if w in text:
            add('FAIL', where, 'P1', '금지어 "%s" — 어느 회사인지 밝히거나 뜻을 그대로 쓴다' % w)


def check_glossary(text, where, gloss):
    """사전 용어는 첫 등장 문장에서 풀어야 한다. 둘째 등장부터는 그냥 쓴다."""
    for term, plain in sorted(gloss.items(), key=lambda kv: -len(kv[0])):
        first = None
        for s in sentences(text):
            if term in s:
                first = s
                break
        if first is None:
            continue
        plain_tail = (plain or '').split()[-1] if (plain or '').strip() else ''
        glossed = (re.search(re.escape(term) + r'\s*\(', first)
                   or (plain in first)
                   or (plain_tail and re.search(
                       re.escape(plain_tail) + r'\s*\([^)]*' + re.escape(term) + r'[^)]*\)', first)))
        if not glossed:
            add('FAIL', where, 'P2',
                '"%s" 첫 등장에 설명이 없다 — %s(%s) 형태로 풀거나 "%s"를 함께 쓴다'
                % (term, term, plain, plain))


TRANSLATIONESE = ['에 대한', '되어진', '로 인해', '에 있어서', '라고 할 수 있다']
SECTION_ORDER = ['주장', '그래서 무엇이 달라지나', '되돌릴 수 없는 지점', '근거',
                 '조건 충돌', '아직 모르는 것', '검토 후 무관']
MAXLEN = 160


def check_length(text, where):
    """긴 문장과 em dash로 절을 여러 개 이은 문장 — 읽는 사람이 숨 쉴 곳이 없다."""
    for s in sentences(text):
        if len(s) > MAXLEN:
            add('WARN', where, 'P3', '문장이 %d자 — 끊는다: %s…' % (len(s), s[:40]))
        if s.count('—') >= 2:
            add('WARN', where, 'P3', 'em dash가 2개 이상 — 문장을 끊는다: %s…' % s[:40])


def check_translationese(text, where):
    for pat in TRANSLATIONESE:
        if pat in text:
            add('WARN', where, 'P4', '번역투 "%s"' % pat)


def shingles(s):
    """정규화 2-gram — 조사·부호 차이를 무시하고 문장이 겹치는지 본다."""
    s = re.sub(r'[^0-9A-Za-z가-힣]', '', s or '')
    return {s[i:i + 2] for i in range(len(s) - 1)}


def check_dup_claim(sec, where):
    """주장이 「그래서」 항목 하나를 그대로 옮겨 쓴 경우는 중복이다."""
    claim = ' '.join(sec.get('주장') or [])
    a = shingles(claim)
    if not a:
        return
    for line in sec.get('그래서 무엇이 달라지나') or []:
        b = shingles(re.sub(r'^-\s*', '', line))
        if not b:
            continue
        overlap = len(a & b) / float(min(len(a), len(b)))
        if overlap >= 0.6:
            add('WARN', where, 'P5',
                '주장과 「그래서」 항목이 %.0f%% 겹친다 — 항목을 다른 각도로 쓰거나 지운다: %s…'
                % (overlap * 100, line[:40]))


def check_order(names, where):
    idx = [SECTION_ORDER.index(n) for n in names if n in SECTION_ORDER]
    if idx != sorted(idx):
        add('WARN', where, 'P6', '절 순서가 규정과 다르다: %s' % ' → '.join(names))


HEADLINE_MAX = 40
SUBHEAD_MAX = 60


def check_head(meta, sec, where):
    """P7 — 카드가 한 줄로 말하게 하는 두 필드.

    headline은 무엇에 관한 판단인지 주어를 담아 자립해야 하고(대상 없이 "승부는
    성능이 아니라 확보량에서 갈린다"고 쓰면 무엇의 승부인지 모른다), subhead는
    또 하나의 주장이 아니라 그 카드에 무엇이 들었는지 알려 주는 요약이다."""
    head = (meta.get('headline') or '').strip()
    sub = (meta.get('subhead') or '').strip()
    if not head:
        add('FAIL', where, 'P7', 'headline 없음 — 카드에 제목이 안 붙는다')
    elif len(head) > HEADLINE_MAX:
        add('WARN', where, 'P7', 'headline이 %d자 (%d자 이하로) — %s…'
            % (len(head), HEADLINE_MAX, head[:24]))
    if not sub:
        add('FAIL', where, 'P7', 'subhead 없음 — 제목 아래 요약 줄이 빈다')
    elif len(sub) > SUBHEAD_MAX:
        add('WARN', where, 'P7', 'subhead가 %d자 (%d자 이하로) — %s…'
            % (len(sub), SUBHEAD_MAX, sub[:24]))
    # subhead가 주장을 그대로 옮기면 요약이 아니라 반복이다
    claim = ' '.join(sec.get('주장') or [])
    if sub and claim:
        a, b = shingles(sub), shingles(claim)
        if a and b and len(a & b) / float(len(a)) >= 0.6:
            add('WARN', where, 'P7', 'subhead가 주장과 %.0f%% 겹친다 — 무엇이 들었는지 나열하는 쪽으로'
                % (100 * len(a & b) / float(len(a))))


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    gloss = load_glossary()
    files = sorted(glob.glob(os.path.join(paths.SYNTH, '*.md')))
    # 노트는 문체만 본다. 절 순서·headline 검사(P5~P7)는 인사이트 형식이라
    # 노트(주장/수치/추정)에 대면 있지도 않은 절을 없다고 잡는다
    notes = sorted(glob.glob(os.path.join(paths.NOTES, '*.md')))
    for p in notes:
        where = os.path.basename(p)
        body = strip_refs(io.open(p, encoding='utf-8').read())
        check_banned(body, where)
        check_glossary(body, where, gloss)
        check_length(body, where)
        check_translationese(body, where)

    # 정리본은 판단이 아니라 한 주제의 현재 상태를 묶은 것이라 절 구성이 다르다
    for p in sorted(glob.glob(os.path.join(paths.DIGESTS, '*.md'))):
        where = os.path.basename(p)
        raw = io.open(p, encoding='utf-8').read()
        body = strip_refs(raw)
        meta, _ = parse_synth(raw)
        check_banned(body, where)
        check_glossary(body, where, gloss)
        check_length(body, where)
        check_translationese(body, where)
        if not (meta or {}).get('headline'):
            add('FAIL', where, 'P7', 'headline 없음 — 카드에 제목이 안 붙는다')

    for p in files:
        where = os.path.basename(p)
        raw = io.open(p, encoding='utf-8').read()
        body = strip_refs(raw)
        meta, mdbody = parse_synth(raw)
        sec = sections(strip_refs(raw)) if meta else sections(body)
        names = [n for n in sec.keys()]
        check_banned(body, where)
        check_glossary(body, where, gloss)
        check_length(body, where)
        check_translationese(body, where)
        check_dup_claim(sec, where)
        check_order(names, where)
        check_head(meta or {}, sec, where)

    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    warns = len(findings) - fails
    per = {}
    for f in findings:
        per[f[1]] = per.get(f[1], 0) + (0 if f[0] == 'FAIL' else 1)
    print('요약: 인사이트 %d건 / 노트 %d장 / FAIL %d / WARN %d'
          % (len(files), len(notes), fails, warns))
    heavy = [k for k, v in per.items() if v > 5]
    if heavy:
        print('WARN 5건 초과: %s — 이 파일은 humanize-korean 스킬을 부를 계기다'
              % ', '.join(heavy))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
