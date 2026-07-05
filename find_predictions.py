import sys

filename = '원본 해석/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md'
text = open(filename, encoding='utf-8').read()

out = open('predictions.txt', 'w', encoding='utf-8')

lines = text.split('\n')
for i, line in enumerate(lines):
    l_strip = line.strip()
    if l_strip and not l_strip.startswith('|') and not l_strip.startswith('style') and not l_strip.startswith('class'):
        # Check if line contains years or predictions keywords
        if any(keyword in line for keyword in ['2025', '2026', '2027', '2028', '년', '전망', '예상', '계획', '양산', '목표']):
            out.write(f"Line {i+1}: {line}\n")

out.close()
print("Done writing predictions.txt")
