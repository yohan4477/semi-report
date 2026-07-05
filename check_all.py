import re

filename = '원본 해석/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md'
text = open(filename, encoding='utf-8').read()

# 1. Check difficulty emojis
emojis = ["🟢", "🟡", "🔴"]
found_emojis = [e for e in emojis if e in text]
print("1. Difficulty Emojis:", "Found" if found_emojis else "Pass", found_emojis)

# 2. Check diagram direction
directions = ["flowchart LR", "graph LR"]
found_directions = [d for d in directions if d in text]
print("2. LR Diagrams:", "Found" if found_directions else "Pass", found_directions)

# 3. Check unescaped tildes outside mermaid blocks
body = text
mermaid_blocks = re.findall(r'```mermaid.*?```', body, re.S)
for b in mermaid_blocks:
    body = body.replace(b, '')

unescaped_tildes = re.findall(r'(?<!\\)~', body)
print("3. Unescaped Tildes Outside Mermaid:", f"Found {len(unescaped_tildes)}" if unescaped_tildes else "Pass")

# 4. Check paragraph length <= 200 and ratio <= 30%
para = []
for l in body.split('\n'):
    l_strip = l.strip()
    if l_strip and not l_strip.startswith(('#','>','-','|','*','`','---','[')):
        para.append(l)

pc = sum(map(len, para))
tc = len(text)
long_lines = [l for l in para if len(l) > 200]
print(f"4. Paragraph Ratio: {pc*100/tc:.2f}% (Limit: 30%) | Long Lines: {len(long_lines)}")
