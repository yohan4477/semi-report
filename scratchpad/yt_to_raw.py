# -*- coding: utf-8 -*-
"""유튜브 자막(content/semi_doped/youtube/*.md)을 raw/ 정본 꼴로 옮긴다.

    py -3.13 scratchpad/yt_to_raw.py <youtube 파일 이름(확장자 빼고)> <새 slug>

자막은 줄마다 여섯 낱말쯤에서 끊긴다. 화자가 바뀌는 표시(&gt;&gt;)를 경계로
한 발언을 한 줄로 잇는다. 인용에 붙는 (L줄번호)가 그 발언을 가리키게 된다.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YT = os.path.join(ROOT, 'content', 'semi_doped', 'youtube')
RAW = os.path.join(ROOT, 'content', 'semi_doped', 'raw')

ENT = [('&gt;', '>'), ('&lt;', '<'), ('&quot;', '"'), ('&#39;', "'"), ('&nbsp;', ' '), ('&amp;', '&')]


def unescape(s):
    for a, b in ENT:
        s = s.replace(a, b)
    return s


def main():
    name, slug = sys.argv[1], sys.argv[2]
    src = io.open(os.path.join(YT, name + '.md'), encoding='utf-8').read()
    parts = src.split('---\n')
    fm = parts[1]
    body = unescape('---\n'.join(parts[2:]))

    turns, cur = [], []
    for line in body.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('>>'):
            if cur:
                turns.append(' '.join(cur))
            cur = [line.lstrip('> ').strip()]
        else:
            cur.append(line)
    if cur:
        turns.append(' '.join(cur))
    turns = [re.sub(r'\s+', ' ', t).strip() for t in turns if t.strip()]
    note = '유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄.'

    if len(turns) < 5:  # 화자 바뀜 표시가 없는 자막 — 문장 넷씩 묶는다
        flat = re.sub(r'\s+', ' ', body.replace('\n', ' ')).strip()
        sents = re.findall(r'[^.!?]+[.!?]+|[^.!?]+$', flat)
        sents = [x.strip() for x in sents if x.strip()]
        turns = [' '.join(sents[i:i + 4]) for i in range(0, len(sents), 4)]
        note = '유튜브 자막에서 옮긴 전사. 화자 표시가 없어 문장 넷씩 한 줄.'

    meta = dict(re.findall(r'^(\w+): (.*)$', fm, re.M))
    out = ['---',
           'source: ' + meta.get('source', ''),
           'title: ' + meta.get('title', ''),
           'date: ' + meta.get('date', ''),
           'kind: transcript',
           'note: ' + note,
           '---', '']
    out += [t + '\n' for t in turns]
    io.open(os.path.join(RAW, slug + '.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print('%s  발언 %d개' % (slug, len(turns)))


if __name__ == '__main__':
    main()
