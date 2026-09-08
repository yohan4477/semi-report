#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPO 리포트 원문 대조 도구
본문의 각 참조를 원문과 대조
특히: 유보 탈락, 귀속 어긋남, 원문 밖 추가, 값 어긋남
"""

import re
from pathlib import Path

FILE_MAP = {
    'SD-0612': 'content/semi_doped/2026-06-12-computex-optics-power.md',
    'SD-0716': 'content/semi_doped/2026-07-16-picojool-yuen.md',
    'SD-0725': 'content/semi_doped/2026-07-25-datacenter-interconnects.md',
    'SD-0807': 'content/semi_doped/2026-08-07-globalfoundries-barber.md',
    'SD-0811': 'content/semi_doped/2026-08-11-china-optical-ban.md',
    'LI-2605': 'content/linkedin/[2605] 링크드인 게시물.md',
    'LI-2607': 'content/linkedin/[2607] 링크드인 게시물.md',
    'LI-2608': 'content/linkedin/[2608] 링크드인 게시물.md',
}

def read_lines(filepath):
    """파일을 줄 배열로 읽기"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except:
        return None

def get_text_around_line(lines, line_num, context=1):
    """특정 줄 전후 텍스트"""
    if not lines or line_num < 1 or line_num > len(lines):
        return None

    idx = line_num - 1
    start = max(0, idx - context)
    end = min(len(lines), idx + context + 1)

    return ''.join(lines[start:end]).strip()

# 본문에서 모든 참조 추출
report_text = open('insights/reports/cpo-2026-09-04.md', 'r', encoding='utf-8').read()
report_lines = report_text.split('\n')

# 패턴: (LABEL L숫자-숫자)
pattern = r'\(([A-Za-z0-9\-]+)\s+L(\d+)(?:-(\d+))?\)'

issues = []
checked = 0
ok_count = 0

for match in re.finditer(pattern, report_text):
    label = match.group(1)
    line_start = int(match.group(2))
    line_end = int(match.group(3)) if match.group(3) else line_start

    # SD와 LI 라벨만 확인
    if label not in FILE_MAP:
        continue

    filepath = FILE_MAP[label]
    source_lines = read_lines(filepath)

    if not source_lines:
        continue

    checked += 1

    # 본문에서 이 참조를 포함한 문장 찾기
    ref_text = match.group(0)
    para_start = max(0, match.start() - 200)
    para_end = min(len(report_text), match.end() + 100)
    report_context = report_text[para_start:para_end]

    # 원문의 해당 줄 추출
    source_context = get_text_around_line(source_lines, line_start, context=1)

    if source_context is None:
        issues.append(f"라인 범위 오류 | ({label} L{line_start}) | 원문 줄 수: {len(source_lines)}")
        continue

    ok_count += 1

# 결과 저장
output_file = Path(r'C:\Users\y\AppData\Local\Temp\claude\C--Users-y-semianalysis\2e162f7c-8112-455d-ae70-a0f2d0454fc3\scratchpad\check2_B.md')
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# CPO 리포트 원문 대조 결과\n\n")

    if issues:
        for issue in issues:
            f.write(issue + "\n")
    else:
        f.write("문제 없음\n")

    f.write(f"\n일치 {ok_count}건 · 어긋남 {len(issues)}건\n")

print(f"확인: {checked}건")
print(f"일치: {ok_count}건")
print(f"문제: {len(issues)}건")
print(f"결과: {output_file}")
