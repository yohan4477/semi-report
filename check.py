import re

filename = '원본 해석/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md'
lines = open(filename, encoding='utf-8').read().split('\n')

for i, line in enumerate(lines):
    # check if it's a paragraph line (doesn't start with '#','>','-','|','*','`','---','[' and is not empty)
    l_strip = line.strip()
    if l_strip and not l_strip.startswith(('#','>','-','|','*','`','---','[')):
        if len(line) > 200:
            print(f'Line {i+1} ({len(line)} chars): {line}')
