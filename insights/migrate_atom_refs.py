# 일회용. 인사이트·thesis의 (A-xxx) 참조를 (파일 L줄) 인용으로 바꾸고
# sources: frontmatter를 채운다. 사람이 쓴 산문은 건드리지 않는다.
import io, os, re, sys, json, glob
import paths

REF = re.compile(r'\((A-[0-9A-Za-z-]+(?:\s*,\s*A-[0-9A-Za-z-]+)*)\)')


def atom_index():
    idx = {}
    for p in glob.glob(os.path.join(paths.ROOT, 'insights', 'atoms', '*.json')):
        d = json.load(io.open(p, encoding='utf-8'))
        doc = d['path'].replace('\\', '/')
        for a in d['atoms']:
            idx[a['id']] = (doc, a.get('line') or 1)
    return idx


def _label(doc):
    return os.path.basename(doc).rsplit('.md', 1)[0]


def convert(text, index):
    used = []

    def one(m):
        ids = [x.strip() for x in m.group(1).split(',')]
        groups, order = {}, []
        for i in ids:
            if i not in index:
                return m.group(0)          # 하나라도 모르면 통째로 둔다
            doc, line = index[i]
            if doc not in groups:
                groups[doc] = []
                order.append(doc)
            groups[doc].append(line)
        for doc in order:
            if doc not in used:
                used.append(doc)
        # 문서마다 괄호를 따로 연다. 한 괄호에 두 문서를 넣으면 「(냉각 L370,
        # 베라루빈 L456)」이 되어, 읽는 쪽이 L456을 앞 문서 줄로 붙인다
        return ' '.join(
            '(%s %s)' % (_label(doc), ', '.join('L%d' % n for n in groups[doc]))
            for doc in order)

    return REF.sub(one, text), used


def _inject_sources(head, docs):
    if 'sources:' in head or not docs:
        return head
    rows = '\n'.join('  - {file: "%s", note: ""}' % d for d in docs)
    return head.rstrip() + '\nsources:\n' + rows


def main(dry_run=False):
    idx = atom_index()
    n = 0
    for d in (paths.SYNTH, paths.THESES):
        for p in sorted(glob.glob(os.path.join(d, '*.md'))):
            t = io.open(p, encoding='utf-8').read()
            m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
            if not m:
                continue
            head, body = m.group(1), m.group(2)
            new_body, used = convert(body, idx)
            if new_body == body:
                continue
            out = '---\n%s\n---\n%s' % (_inject_sources(head, used), new_body)
            if not dry_run:
                io.open(p, 'w', encoding='utf-8').write(out)
            n += 1
            print('%s%s — 원문 %d편' % ('[dry] ' if dry_run else '', os.path.basename(p), len(used)))
    print('고친 파일 %d개' % n)
    return n


if __name__ == '__main__':
    main('--dry-run' in sys.argv)
