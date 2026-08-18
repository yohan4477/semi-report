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

# 금지어 목록은 2026-08-17에 걷어냈다. 낱말을 세는 방식은 「서진영」을 진영으로 잡는 식의
# 오탐을 계속 냈고, 정작 글을 망가뜨리는 밀도·누락은 못 잡았다. 대신 P8~P11로 옮겼다.

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


def check_density(text, where):
    """P8~P11 — 낱말이 아니라 밀도를 본다.

    금지어를 세던 자리를 대신한다. 2026-08-17 건강 대시보드를 쓰면서 드러난 것들이다.
    대시 14개, 「A가 아니라 B」 대구 14회, 문장 속 볼드가 그대로 나갔는데 검사기는
    전부 통과시켰다. 낱말이 아니라 되풀이가 글을 AI 문장으로 만든다."""
    paras = [p for p in (text or '').split('\n') if p.strip()]
    if not paras:
        return
    dash = text.count('—')
    if dash > len(paras) * 0.5:
        add('WARN', where, 'P8',
            'em dash가 %d개 (문단 %d개) — 쉼표·괄호·문장 분리로 바꾼다' % (dash, len(paras)))
    contrast = len(re.findall(r'[가-힣]\s*(?:가|이)\s+아니라', text))
    if contrast > 2:
        add('WARN', where, 'P9',
            '「A가 아니라 B」 대구가 %d회 — 문서당 2회까지다' % contrast)
    for s in sentences(text):
        if s.count(',') >= 4:
            add('WARN', where, 'P11',
                '한 문장에 절이 %d개 — 논지 하나만 남기고 끊는다: %s…' % (s.count(',') + 1, s[:40]))
    check_vague(text, where)
    check_figure(text, where)



# P14 — 돈·값을 은유 주어로 세운 문장. 「돈이 도는 자리가 …로 옮겨 간다」처럼 쓰면
# 매끄럽게 읽히는데 무엇이 실제로 움직이는지가 없다. 매출인지 이익인지 주문인지,
# 누구 것인지가 빠진다. 2026-08-18에 「돈이 도는 자리가 다이 바깥의 메모리
# 인터페이스와 광 연결로 옮겨 가고 있다」를 그대로 내보내 사용자가 잡아냈다.
# 앞서 같은 자리에 있던 「값을 받는 자리」를 고치면서 다른 은유로 바꾼 것이 원인이다.
# 은유를 다른 은유로 바꾸는 것은 수정이 아니다 — 주체와 돈의 종류를 이름으로 댄다.
BANNED_FIGURE = [
    (r'돈이 (도는|돌아가는|흐르는|몰리는|모이는)', '무엇이 늘어나는지 이름을 댄다 — 매출·수주·이익 중 무엇인가'),
    (r'값을 받아\s?가', '누가 무엇을 파는지로 쓴다 — 「돈을 번다」·「매출로 들어온다」'),
    (r'값을 받는 자리', '무엇을 파는 자리인지 쓴다'),
    (r'돈이 되는 자리', '무엇을 팔아 얼마를 버는 자리인지 쓴다'),
]


def check_figure(text, where):
    """P14 — 은유로 주어를 대신한 자리. 검사기가 잡아 다시 못 나가게 한다."""
    for pat, fix in BANNED_FIGURE:
        for m in re.finditer(pat, text):
            at = max(0, m.start() - 20)
            snip = ' '.join(text[at:m.end() + 30].split())
            add('FAIL', where, 'P14',
                '은유가 주어 자리에 있다 — %s: …%s…' % (fix, snip))


# 무엇을 먹는지·마시는지 안 밝히고 「먹으면」으로 넘어가는 조건절. 2026-08-17에
# "GLP-1은 먹으면 장에서 나오는 호르몬이다"를 그대로 내보냈다. 읽는 사람은 무엇을
# 먹어야 나오는지 알 수 없다. 앞 15자 안에 목적어(을/를)가 있으면 통과시킨다.
# 「맞으면」은 들어맞다·주사 맞다로 갈려 오탐이 크다. 뜻이 하나인 둘만 본다.
INGEST = re.compile(r'(?<![가-힣])(먹|마시)으?면')
# 정도만 말하고 값을 안 대는 주장. 같은 문장에 숫자가 있으면 통과시킨다.
DEGREE = re.compile(r'(훨씬|크게|상당히|대폭|급격히)\s*[가-힣]{0,4}?'
                    r'(늘|줄|올라|떨어|커지|작아지|높아|낮아|많아|적어)')


def check_vague(text, where):
    """P12·P13 — 문장은 매끄러운데 뜻이 안 닿는 자리를 잡는다.

    검사기가 밀도(P8~P11)만 보던 동안, 조건이 빠진 결론과 값이 없는 정도 주장은
    그대로 나갔다. 둘 다 사람이 읽다가 "그래서 뭘?"이라고 되묻게 되는 자리다."""
    for s in sentences(text):
        for m in INGEST.finditer(s):
            # 목적어(을/를)만 인정한다. 「GLP-1은 먹으면」처럼 주어가 앞에 있어도
            # 무엇을 먹는지는 여전히 빠져 있다 — 그게 이 규칙을 만든 사건이었다.
            head = s[:m.start()]
            if '을 ' in head or '를 ' in head or head[-1:] in ('을', '를'):
                continue
            add('WARN', where, 'P12',
                '「%s」 앞에 무엇을 먹는지가 없다 — 조건을 밝힌다: %s…'
                % (m.group(0), s[:44]))
        if DEGREE.search(s) and not re.search(r'\d', s):
            add('WARN', where, 'P13',
                '정도만 말하고 값이 없다 — 숫자를 대거나 무엇에 견줘 큰지 쓴다: %s…' % s[:44])


def check_bold(raw, where):
    """P10 — 문장 속 볼드. 태그를 떼기 전 원본에서 센다.

    항목 머리말 볼드는 스캔을 돕지만, 한 문단에서 두 번을 넘으면 강조가 강조를 지운다."""
    bold = raw.count('<b>') + raw.count('<strong>')
    blocks = raw.count('<li') + raw.count('<p ') + raw.count('<p>')
    if blocks and bold > blocks * 2:
        add('WARN', where, 'P10',
            '볼드 %d개 / 문단·항목 %d개 — 항목 머리말만 남기고 본문 안 강조는 뺀다' % (bold, blocks))


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


DASH_DIR = os.path.join(paths.ROOT, '대시보드')

# 금지어를 걷어내면서 DASH_BACKLOG도 같이 없앴다. 대시보드에서 나오는 지적은 전부
# WARN이라 예외 목록을 둘 이유가 사라졌다.

# 대시보드 산문에서 걷어내야 하는 것. 눈에 보이는 글만 남긴다.
_TAGBLOCK = re.compile(r'<(script|style|svg)\b.*?</\1>', re.S | re.I)
_TAG = re.compile(r'<[^>]+>')
_ENT = [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&#39;', "'"),
        ('&nbsp;', ' ')]


# 페이지 안내(「같은 영상에서 나온 카드」·「읽는 순서」)는 다른 자리에 있는 카드 제목을
# 그대로 되풀이한다. 산문이 아니라 길잡이다. 그대로 세면 제목 하나가 문서에 여러 번
# 있는 것으로 잡혀 밀도 규칙이 헛돈다 — 2026-08-18에 P9 대구가 2회에서 5회로 뛴 원인이
# 이것이었다. script를 통째로 빼는 이유(같은 문장을 두 번 잡는다)와 같다.
_ECHO_CLASSES = ('uc-kin', 'course')


def _drop_block(raw, cls):
    """class="…cls…"를 단 <div>를 여는 태그부터 짝이 맞는 </div>까지 통째로 지운다.

    안에 <div>가 겹쳐 있어서 정규식으로는 끝을 못 찾는다. 깊이를 세서 끊는다."""
    out, at = [], 0
    key = 'class="%s' % cls
    while True:
        i = raw.find(key, at)
        if i < 0:
            out.append(raw[at:])
            return ''.join(out)
        start = raw.rfind('<div', 0, i)
        if start < 0:
            out.append(raw[at:i + len(key)])
            at = i + len(key)
            continue
        out.append(raw[at:start])
        depth, j = 0, start
        while j < len(raw):
            if raw.startswith('<div', j):
                depth += 1
                j += 4
            elif raw.startswith('</div>', j):
                depth -= 1
                j += 6
                if depth == 0:
                    break
            else:
                j += 1
        at = j


def dashboard_text(path):
    """대시보드 HTML에서 화면에 보이는 한글 문장만 뽑는다.

    script는 통째로 뺀다 — 모달 데이터(JSON)가 거기 있는데, 그건 이 검사기가
    이미 노트·인사이트에서 본 문장이 아니라 파이썬 생성기가 만든 원본이라
    같은 문장을 두 번 잡는다. 표의 숫자 칸은 문장이 아니라서 저절로 걸러진다."""
    raw = io.open(path, encoding='utf-8').read()
    raw = _TAGBLOCK.sub(' ', raw)
    for _cls in _ECHO_CLASSES:
        raw = _drop_block(raw, _cls)
    raw = _TAG.sub('\n', raw)
    for a, b in _ENT:
        raw = raw.replace(a, b)
    out = []
    for line in raw.split('\n'):
        line = line.strip()
        # 한글이 두 글자도 없으면 숫자 칸이거나 라벨이다. 문장 규칙을 대지 않는다.
        if len(re.findall(r'[가-힣]', line)) < 2:
            continue
        out.append(line)
    return '\n'.join(out)


def check_dashboards(gloss):
    """대시보드도 문체 게이트에 넣는다.

    왜 뒤늦게 넣나: 이 검사기가 insights/ 아래 세 곳만 보고 있어서, 같은 사람이
    같은 날 쓴 문장이라도 대시보드에 쓰면 번역투가 그대로 나갔다. 실제로
    회계사 대시보드에 em dash가 95개 쌓이고 나서야 사람 눈에 걸렸다.

    용어 사전(P2)은 대지 않는다. 대시보드는 카드마다 독립해 읽히는 화면이라
    「첫 등장」이라는 개념이 문서와 다르다."""
    paths_ = sorted(glob.glob(os.path.join(DASH_DIR, '*.html')))
    for p in paths_:
        where = os.path.basename(p)
        body = dashboard_text(p)
        check_density(body, where)
        check_length(body, where)
        check_translationese(body, where)
        # 볼드는 태그를 떼기 전 원본에서 센다
        check_bold(io.open(p, encoding='utf-8').read(), where)
    return paths_


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
        check_density(body, where)
        check_glossary(body, where, gloss)
        check_length(body, where)
        check_translationese(body, where)

    # 브리핑은 판단이 아니라 한 주제의 현재 상태를 묶은 것이라 절 구성이 다르다
    for p in sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md'))):
        where = os.path.basename(p)
        raw = io.open(p, encoding='utf-8').read()
        body = strip_refs(raw)
        meta, _ = parse_synth(raw)
        check_density(body, where)
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
        check_density(body, where)
        check_glossary(body, where, gloss)
        check_length(body, where)
        check_translationese(body, where)
        check_dup_claim(sec, where)
        check_order(names, where)
        check_head(meta or {}, sec, where)

    dashes = check_dashboards(gloss)

    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    warns = len(findings) - fails
    # 「WARN 5건 초과 → humanize-korean」 줄은 2026-08-17에 걷어냈다. 다섯 장이 상시
    # 초과 상태라 늘 켜져 있었고, 늘 켜진 신호는 신호가 아니다. 윤문을 부를 계기는
    # 개별 규칙(P8~P11)이 무엇을 몇 개 잡았는지로 판단한다.
    print('요약: 인사이트 %d건 / 노트 %d장 / 대시보드 %d장 / FAIL %d / WARN %d'
          % (len(files), len(notes), len(dashes), fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
