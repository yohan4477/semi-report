# 문서가 자기 본문에 갖고 있는 구조(계층·프로세스)를 문서마다 기록하고, 중복을 접는다.
#
# 왜 필요한가: 좌표(스택 8노드·프로세스 7단계)는 전역 축이라 문서 고유 구조를 못 담는다.
# 레고 문서의 3층 분류나 모듈화 사이클 5단계가 "데이터센터 / 건물 착공" 한 칸으로 접혔다.
# 그렇다고 문서마다 축을 만들면 사전이 문서 수만큼 늘어난다. 그래서 순서를 바꿨다 —
# 문서별로 있는 그대로 기록하고, **중복제거로 2편 이상이 공유하는 구조만** 승격 후보로 올린다.
#
# 저장: insights/views/structures.json  (검사기와 별개 — 원자 파일은 건드리지 않는다)
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca

STRUCT = os.path.join(ca.ROOT, 'insights', 'views', 'structures.json')
KINDS = ('hierarchy', 'process')


def load():
    if not os.path.exists(STRUCT):
        return {'docs': []}
    return json.load(io.open(STRUCT, encoding='utf-8'))


def norm_label(s):
    """라벨 비교용 정규화 — 공백·중점·괄호주석·조사성 접미를 떨어낸다."""
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = re.sub(r'[\s·∙,]+', '', s)
    return s.strip().lower()


KINDS_OF_DOC = ('quantitative', 'argument')


def validate(data, man_ids=None, atom_counts=None):
    """구조 기록 자체의 무결성. 반환: (오류 목록)"""
    errs = []
    seen = set()
    for d in data.get('docs', []):
        sid = d.get('source_id')
        if not sid:
            errs.append('source_id 없음')
            continue
        if sid in seen:
            errs.append('%s: 같은 문서가 두 번' % sid)
        seen.add(sid)
        if man_ids is not None and sid not in man_ids:
            errs.append('%s: manifest에 없는 source_id' % sid)
        kod = d.get('kind_of_doc', 'quantitative')
        if kod not in KINDS_OF_DOC:
            errs.append('%s: kind_of_doc이 %s 중 하나여야 함 (%s)'
                        % (sid, '|'.join(KINDS_OF_DOC), kod))
        if kod == 'argument':
            th = d.get('thesis') or {}
            if not th:
                errs.append('%s: argument 문서는 thesis가 있어야 한다' % sid)
            else:
                if not isinstance(th.get('line'), int):
                    errs.append('%s: thesis에 line(원문 줄 번호)이 없다' % sid)
                if not (th.get('claim') or '').strip():
                    errs.append('%s: thesis에 claim이 없다' % sid)
                if not (th.get('line_text') or '').strip():
                    errs.append('%s: thesis에 line_text(그 줄 원문)가 없다' % sid)
            # thesis가 원자의 우회로가 되지 않게 — 소급분(legacy_atoms)만 예외
            if (atom_counts or {}).get(sid) and not d.get('legacy_atoms'):
                errs.append('%s: argument 문서인데 원자가 %d개 있다 — 둘 중 하나만 둔다'
                            % (sid, atom_counts[sid]))
        for st in d.get('structures', []):
            where = '%s / %s' % (sid, st.get('name', '?'))
            if st.get('kind') not in KINDS:
                errs.append('%s: kind가 %s 중 하나여야 함 (%s)' % (where, '|'.join(KINDS), st.get('kind')))
            items = st.get('steps') if st.get('kind') == 'process' else st.get('levels')
            if not items or len(items) < 2:
                errs.append('%s: 항목이 2개 미만 — 구조가 아니다' % where)
            if not isinstance(st.get('line'), int):
                errs.append('%s: line(원문 줄 번호)이 없다' % where)
            if len({norm_label(x) for x in (items or [])}) != len(items or []):
                errs.append('%s: 항목 라벨 중복' % where)
    return errs


def _items(st):
    return st.get('steps') if st.get('kind') == 'process' else st.get('levels')


def jaccard(a, b):
    A = {norm_label(x) for x in a}
    B = {norm_label(x) for x in b}
    if not A or not B:
        return 0.0
    return len(A & B) / float(len(A | B))


def dedupe(data, threshold=0.4):
    """같은 kind끼리 문서를 가로질러 겹치는 구조 쌍을 찾는다.

    2편 이상이 같은 구조를 말하면 그것이 승격 후보다 — 한 문서만 말하는 구조는
    그 문서의 목차이고, 좌표로 올릴 근거가 없다(이게 이 스크립트의 존재 이유다)."""
    flat = []
    for d in data.get('docs', []):
        for st in d.get('structures', []):
            flat.append((d['source_id'], st))
    pairs = []
    for i, (sid_a, a) in enumerate(flat):
        for sid_b, b in flat[i + 1:]:
            if sid_a == sid_b or a.get('kind') != b.get('kind'):
                continue
            j = jaccard(_items(a), _items(b))
            if j >= threshold:
                pairs.append({'kind': a['kind'], 'jaccard': round(j, 2),
                              'a': (sid_a, a.get('name'), _items(a)),
                              'b': (sid_b, b.get('name'), _items(b)),
                              'shared': sorted({norm_label(x) for x in _items(a)} &
                                               {norm_label(x) for x in _items(b)})})
    pairs.sort(key=lambda p: -p['jaccard'])
    return flat, pairs


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    data = load()
    man_ids = {s['id'] for s in json.load(io.open(ca.MAN, encoding='utf-8'))['sources']}
    counts = {}
    for a in ca.load_atoms():
        counts[a['_source_id']] = counts.get(a['_source_id'], 0) + 1
    errs = validate(data, man_ids, counts)
    flat, pairs = dedupe(data)

    print('구조 기록: 문서 %d편 / 구조 %d개 (계층 %d · 프로세스 %d)'
          % (len(data.get('docs', [])), len(flat),
             sum(1 for _, s in flat if s['kind'] == 'hierarchy'),
             sum(1 for _, s in flat if s['kind'] == 'process')))
    if errs:
        print('')
        print('오류 %d건' % len(errs))
        for e in errs:
            print('  ' + e)
    print('')
    print('중복 후보 %d쌍  (문서를 가로질러 겹치는 구조 — 2편 이상이 말하면 승격 후보)' % len(pairs))
    for p in pairs:
        print('  %s  겹침 %.2f' % (p['kind'], p['jaccard']))
        print('    %s :: %s' % (p['a'][0].split(':')[-1][:34], ' → '.join(p['a'][2])))
        print('    %s :: %s' % (p['b'][0].split(':')[-1][:34], ' → '.join(p['b'][2])))
        print('    공유 항목: %s' % ', '.join(p['shared']))
    if not pairs and flat:
        print('  없음 — 지금 기록된 구조는 모두 한 문서에만 있다. 좌표로 올릴 근거가 아직 없다')
    print('')
    print('단독 구조 (승격 금지 — 그 문서의 목차다)')
    paired = {id(s) for p in pairs for s in ()}
    inpair = set()
    for p in pairs:
        inpair.add((p['a'][0], p['a'][1]))
        inpair.add((p['b'][0], p['b'][1]))
    for sid, st in flat:
        if (sid, st.get('name')) not in inpair:
            print('  %-10s %s :: %s' % (st['kind'], sid.split(':')[-1][:30],
                                        ' → '.join(_items(st))))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
