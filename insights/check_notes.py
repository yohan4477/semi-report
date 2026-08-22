# 노트와 서술의 인용을 검사한다. 원자 검사기(C1~C21)를 대신하되 실제로
# 인용한 줄만 본다 — 모든 문장을 미리 분해해 두지 않아서 훨씬 싸다.
import io, os, re, sys, json, glob
import paths
import notes_lib as nl

MAXKB = 3.0

# -- N9 : 회사 이름은 정본 하나로만 --------------------------------------
# actors 는 문서를 회사로 잇는 열쇠다. 같은 회사가 「엔비디아」와 「NVIDIA」로 나뉘면
# 교차 인사이트가 한 회사를 둘로 세고 둘 다 근거가 얇아진다. 2026-08-23에 노트에서
# 갈라져 있던 25종을 합치고 이 검사를 걸었다. 표는 insights/actor_alias.json.
ALIAS = {k: v for k, v in
         json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'actor_alias.json'), encoding='utf-8')).items()
         if not k.startswith('_')}


def check_actors(path, meta):
    out = []
    raw = (meta.get('actors') or '').strip()
    if not (raw.startswith('[') and raw.endswith(']')):
        return out
    for a in raw[1:-1].split(','):
        a = a.strip().strip('"')
        if a in ALIAS:
            out.append(('FAIL', path, 'N9',
                        'actors 에 별칭을 썼다 -- %s 는 %s 로 적는다' % (a, ALIAS[a])))
    return out

NUM = re.compile(r'\d')
ROW = re.compile(r'^\s*-\s+(.+)$', re.M)

# ── N8 — 숫자를 말하는 문장은 자기 인용을 갖는다 ──────────────────────────
# N7 은 문단 단위라, 인용 붙은 문장 옆에 인용 없는 숫자 문장이 붙어 있으면
# 못 본다. check_cite 는 인용한 줄만 보므로 인용이 아예 없는 문장을 못 본다.
# 그 틈으로 같은 결함이 네 편에서 두 번 통과했다. 문장 단위로 다시 센다.
#
# 문장 자르기를 「다. 」로 하면 안 된다. 인용이 붙은 문장은 전부 「).」로
# 끝나서, 인용 문장 다음 문장이 통째로 앞 문장에 붙어 인용을 물려받는다.
# 실제로 사람이 그렇게 훑고 「8건 → 0건」이라 보고했는데 2건이 남아 있었다.
# 마침표 뒤 공백으로만 자른다.
SENT8 = re.compile(r'(?<=[.])\s+')
# 인용 표지 — (라벨 L12) 와 (L529) 둘 다. notes_lib.CITE 는 라벨이 3자
# 이상이라야 잡아서 맨 뒤 되풀이 인용 (L529) 를 놓친다
MARK8 = re.compile(r'\([^()]*L\d')
STRIP8 = re.compile(r'\([^()]*L\d[^()]*\)')
# 제품 이름 속 숫자는 잰 값이 아니다 — B200 · NVL72 · H200 · GPT-4 · HBM4E.
# 단위가 붙은 64TB/s · 800G · 5.3kW 는 잰 값이므로 남긴다(숫자가 앞에 온다)
NAME8 = re.compile(r'[A-Za-z]-?\d[\dA-Za-z.]*')
NUM8 = re.compile(r'\d[\d,]*(?:\.\d+)?')


def figures_of(s):
    """문장이 들고 있는 잰 값들. 인용 표지와 제품 이름은 뺀다."""
    return set(NUM8.findall(NAME8.sub(' ', STRIP8.sub(' ', s))))


def sentences_of(body):
    """본문을 문장으로 자른다. 제목 줄은 마침표가 없어 다음 문장에 들러붙으므로
    먼저 버리고, 표 줄과 목록 표지도 걷어 낸다."""
    for line in body.split('\n'):
        t = line.strip()
        if not t or t.startswith('#') or t.startswith('|'):
            continue
        t = re.sub(r'^[-*]\s+', '', t)
        for s in SENT8.split(t):
            s = s.strip()
            if s:
                yield s


def check_uncited_figures(path, body):
    """인용 없이 숫자를 말하는 문장을 찾는다.

    면제 둘. ① 앞서 인용된 문장이 이미 내놓은 값을 되짚는 문장 — 「같은 줄이」
    「이 1.7배는」처럼 가리키는 경우와, 「33%와 30%를 한 숫자로 묶어 쓰면 안
    된다」처럼 필자가 자기 판단을 얹는 경우가 여기 든다. 새 값을 나르지 않으니
    붙일 인용도 없다. ② 제품 이름 속 숫자(figures_of 가 이미 걷어 낸다)."""
    out, seen = [], set()
    for s in sentences_of(body):
        figs = figures_of(s)
        if MARK8.search(s):
            seen |= figs
            continue
        if figs - seen:
            out.append(('WARN', path, 'N8',
                        '숫자를 말하는데 이 문장에 인용이 없다: %s' % s[:46]))
    return out


def check_file(path, text, lock):
    out = []
    meta, body = nl.parse_front(text)
    src = nl.sources_of(meta)
    if not src:
        out.append(('FAIL', path, 'N1', 'frontmatter에 source/sources가 없다'))
        return out
    for s in src:
        if not os.path.isfile(nl.abspath(s['file'])):
            out.append(('FAIL', path, 'N1', '원문이 없다: %s' % s['file']))

    for r in nl.cite_refs(body, src):
        if not r['ok']:
            out.append(('FAIL', path, 'N2', '라벨을 못 푼다: %s' % r['label']))
            continue
        ap = nl.abspath(r['file'])
        for n in r['lines']:
            h = nl.line_hash(ap, n)
            if h is None:
                out.append(('FAIL', path, 'N3',
                            '%s에 %d번 줄이 없다' % (r['file'], n)))
                continue
            key = '%s#L%d' % (r['file'], n)
            old = (lock.get(key) or {}).get('sha1')
            if old and old != h:
                out.append(('WARN', path, 'N4',
                            '원문이 바뀌었다 — 다시 볼 것: %s' % key))
            lock[key] = {'sha1': h}

    # 3KB 상한은 노트에만 건다. 추적·인사이트 서술은 원래 길다
    if '/notes/' in path and len(text.encode('utf-8')) > MAXKB * 1024:
        out.append(('WARN', path, 'N5',
                    '노트가 %.1fKB — %.0fKB를 넘으면 원문을 다시 읽는 편이 낫다'
                    % (len(text.encode('utf-8')) / 1024.0, MAXKB)))

    out += check_actors(path, meta)

    m = re.search(r'^## 수치\s*\n(.*?)(?=\n## |\Z)', body, re.S | re.M)
    if m:
        for row in ROW.findall(m.group(1)):
            if not nl.CITE.search(row):
                out.append(('FAIL', path, 'N6', '수치에 인용이 없다: %s' % row[:40]))

    for para in re.split(r'\n\s*\n', body):
        p = para.strip()
        if p.startswith('#') or p.startswith('-') or len(p) < 40:
            continue
        if NUM.search(p) and not nl.CITE.search(p):
            out.append(('WARN', path, 'N7', '숫자가 있는데 인용이 없다: %s' % p[:40]))

    # N8 은 고리 글에만 건다. 옛 글 41장은 흡수되는 대로 지워지므로 나가는
    # 길에 다시 훑을 이유가 없다
    if '/loop/' in path:
        out += check_uncited_figures(path, body)
    return out


def main(write_lock=True):
    lock = {}
    if os.path.isfile(paths.CITES):
        lock = json.load(io.open(paths.CITES, encoding='utf-8'))
    findings, n = [], 0
    # synth·theses는 Task 5(참조 치환)가 끝난 뒤에 넣는다. 지금 넣으면
    # sources: frontmatter가 없어 전부 N1 FAIL이 난다
    for d in (paths.NOTES, paths.TRACKS, paths.SYNTH, paths.THESES, paths.BRIEFS, paths.LOOP):
        for p in sorted(glob.glob(os.path.join(d, '*.md'))):
            n += 1
            rel = os.path.relpath(p, paths.ROOT).replace(os.sep, '/')
            findings += check_file(rel, io.open(p, encoding='utf-8').read(), lock)
    for lv, where, rule, msg in findings:
        print('%s %s [%s] %s' % (lv, os.path.basename(where), rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    warns = len(findings) - fails
    print('요약: 문서 %d편 / FAIL %d / WARN %d' % (n, fails, warns))
    if write_lock:
        json.dump(lock, io.open(paths.CITES, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1, sort_keys=True)
    return fails


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
