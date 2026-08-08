# 종합 판단(insights/theses/*.md) 검사기.
#
# 기존 인사이트가 쓸모없어진 이유를 측정해 보니 셋이었다 — 한 문서 요약(29건 중 16건),
# 방어 서술이 본문 절반(13건), 주장에 연도 없음(15건). 그래서 종합 판단은 형식으로
# 그 셋을 막는다: 문서 3편 이상·최다 비중 50% 미만·시간표와 폐기 조건 필수.
import os, io, re, sys, json, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THESES = os.path.join(ROOT, 'insights', 'theses')
LI = os.path.join(ROOT, 'insights', 'views', 'li_signals.json')

MIN_DOCS = 3          # 두 편이면 대조가 아니라 재기술이다
MAX_TOP_SHARE = 50    # 한 문서가 절반을 넘으면 그 문서의 요약이다
NEED_SECTIONS = ['한 줄', '시간표', '종목 노출', '무엇이 나오면 이 판단을 버리나', '이 판단이 안 쥔 것']

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def load_atoms():
    man = {s['id']: s for s in json.load(io.open(os.path.join(ROOT, 'insights', 'manifest.json'),
                                                 encoding='utf-8'))['sources']}
    out = {}
    for f in glob.glob(os.path.join(ROOT, 'insights', 'atoms', '*.json')):
        d = json.load(io.open(f, encoding='utf-8'))
        date = man.get(d['source_id'], {}).get('date')
        for a in d['atoms']:
            out[a['id']] = (d['source_id'], date)
    return out


def main():
    atoms = load_atoms()
    li = {}
    if os.path.exists(LI):
        li = {s['id']: s for s in json.load(io.open(LI, encoding='utf-8'))['signals']}
    files = sorted(glob.glob(os.path.join(THESES, '*.md')))
    today = datetime.date.today()

    for p in files:
        name = os.path.basename(p)
        t = io.open(p, encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
        if not m:
            add('FAIL', name, 'T0', 'frontmatter가 없다')
            continue
        fm, body = m.group(1), m.group(2)

        # T1 — 인용 원자가 실재하고 frontmatter 목록 안에 있어야 한다
        declared = set(re.findall(r'A-\d{6}-\d{2}', re.search(r'^atoms: \[(.*?)\]$', fm, re.M).group(1))
                       if re.search(r'^atoms: \[(.*?)\]$', fm, re.M) else [])
        cited = set(re.findall(r'A-\d{6}-\d{2}', body))
        for a in sorted(cited - declared):
            add('FAIL', name, 'T1', '본문이 인용했는데 atoms 목록에 없다: %s' % a)
        for a in sorted(declared | cited):
            if a not in atoms:
                add('FAIL', name, 'T2', '존재하지 않는 원자: %s' % a)

        # T3 — 근거 문서 수와 쏠림
        docs = [atoms[a][0] for a in declared if a in atoms]
        uniq = set(docs)
        if len(uniq) < MIN_DOCS:
            add('FAIL', name, 'T3', '근거 문서 %d편 (최소 %d편)' % (len(uniq), MIN_DOCS))
        if docs:
            top = max(uniq, key=docs.count)
            share = round(docs.count(top) / len(docs) * 100)
            if share > MAX_TOP_SHARE:
                add('FAIL', name, 'T4', '한 문서가 근거의 %d%% (최대 %d%%) — %s'
                    % (share, MAX_TOP_SHARE, top.split(':')[-1][:34]))

        # T5 — 시간축. 날짜 없는 판단은 검증도 폐기도 못 한다
        dates = sorted({atoms[a][1] for a in declared if a in atoms and atoms[a][1]})
        if dates and (datetime.date.fromisoformat(dates[-1]) - datetime.date.fromisoformat(dates[0])).days < 90:
            add('WARN', name, 'T5', '근거 문서가 %s~%s로 3개월 안에 몰렸다' % (dates[0], dates[-1]))
        if not re.search(r'20\d\d년', body):
            add('FAIL', name, 'T6', '본문에 연도가 하나도 없다')

        # T7 — 필수 절
        heads = re.findall(r'^## (.+)$', body, re.M)
        for need in NEED_SECTIONS:
            if not any(need in h for h in heads):
                add('FAIL', name, 'T7', '「%s」 절이 없다' % need)

        # T8 — 종목 노출에 티커가 실제로 있어야 한다
        sec = re.search(r'^## 종목 노출.*?\n(.*?)(?=\n## |\Z)', body, re.S | re.M)
        if sec and len(re.findall(r'\|', sec.group(1))) < 12:
            add('FAIL', name, 'T8', '종목 노출 절에 표가 없다')

        # T9 — 링크드인 인용은 사용 가능한 것만
        for s in sorted(set(re.findall(r'L-\d{8}-\d{4}', body))):
            if s not in li:
                add('FAIL', name, 'T9', '존재하지 않는 링크드인 신호: %s' % s)
            elif not li[s]['usable']:
                add('FAIL', name, 'T9', '사용 불가 신호를 인용했다: %s (%s)' % (s, li[s]['kind']))

        # T10 — 유통기한
        rb = re.search(r'^review_by: (\d{4}-\d{2}-\d{2})$', fm, re.M)
        if not rb:
            add('FAIL', name, 'T10', 'review_by가 없다 — 판단에 유통기한을 박는다')
        elif datetime.date.fromisoformat(rb.group(1)) < today:
            add('WARN', name, 'T10', 'review_by %s가 지났다 — 다시 보거나 미룬다' % rb.group(1))

    for lv, where, rule, msg in findings:
        print('%s %s [%s] %s' % (lv, where, rule, msg))
    nf = sum(1 for f in findings if f[0] == 'FAIL')
    nw = len(findings) - nf
    print('요약: 종합 판단 %d건 / FAIL %d / WARN %d' % (len(files), nf, nw))
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
