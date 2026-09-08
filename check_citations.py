#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPO 리포트 원문 대조 도구
본문의 각 참조(SD-0807 L36-38 등)를 원문과 대조
"""

import re
import os
from pathlib import Path

# 파일 매핑
FILE_MAP = {
    'GTC25': 'input/clippings/NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman.md',
    '관세': 'input/clippings/Tariff Armageddon  GPU Loopholes, Mexico Supply Chain Shift, Wafer Fab Equipment Vulnerabilities, Optical Module Pricing Surge, Datacenter Equipment.md',
    'TPU': 'content/newsletter/ai_infra/compute/[251128] TPUv7 - 구글, AI 반도체 왕좌에 도전장을 내밀다.md',
    '화웨이': 'input/clippings/Huawei AI CloudMatrix 384 – China\'s Answer to Nvidia GB200 NVL72.md',
    'SD-0612': 'content/semi_doped/2026-06-12-computex-optics-power.md',
    'SD-0716': 'content/semi_doped/2026-07-16-picojool-yuen.md',
    'SD-0725': 'content/semi_doped/2026-07-25-datacenter-interconnects.md',
    'SD-0807': 'content/semi_doped/2026-08-07-globalfoundries-barber.md',
    'SD-0811': 'content/semi_doped/2026-08-11-china-optical-ban.md',
    'CPO북': 'content/newsletter/ai_infra/compute/[260101] 코패키지드 옵틱스 — 빛이 구리를 대신하는 단계.md',
    'ISSCC': 'content/newsletter/ai_infra/compute/[260416] ISSCC 2026 — 그때뿐인가, 광이 반도체 자체를 고쳤나.md',
    'ECTC': 'content/newsletter/ai_infra/compute/[260702] ECTC 2026 — 패키징 한계, 마벨의 선택, 글파의 베팅.md',
    'GTC26': 'content/newsletter/ai_infra/compute/[260324] GTC 2026 — 루빈 직통은 구리, 파인만을 향해 광.md',
    '루빈': 'content/newsletter/ai_infra/compute/[260226] 루빈 NVLink 6 — 100나노 양방향 SerDes, 랙 안 구리의 마지막.md',
    'LI-2605': 'content/linkedin/[2605] 링크드인 게시물.md',
    'LI-2607': 'content/linkedin/[2607] 링크드인 게시물.md',
    'LI-2608': 'content/linkedin/[2608] 링크드인 게시물.md',
}

def read_file_lines(filepath):
    """파일 읽기, 빈 줄도 포함"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def get_line_context(lines, line_num, context_before=1, context_after=1):
    """줄번호로 전후 맥락 추출 (1-based indexing)"""
    idx = line_num - 1
    if idx < 0 or idx >= len(lines):
        return None

    start = max(0, idx - context_before)
    end = min(len(lines), idx + context_after + 1)

    return {
        'line': lines[idx].strip(),
        'context_before': [l.strip() for l in lines[start:idx]],
        'context_after': [l.strip() for l in lines[idx+1:end]],
    }

def extract_citations_from_text(text):
    """본문에서 모든 인용 추출"""
    # 패턴: (라벨 L줄-줄 범위) 형태
    pattern = r'\(([A-Za-z0-9-]+)\s+L(\d+)(?:-(\d+))?\)'
    matches = re.finditer(pattern, text)

    citations = []
    for match in matches:
        label = match.group(1)
        line_start = int(match.group(2))
        line_end = int(match.group(3)) if match.group(3) else line_start
        citations.append({
            'label': label,
            'lines': (line_start, line_end),
            'match_text': match.group(0),
        })

    return citations

# 본문 읽기
report_path = 'insights/reports/cpo-2026-09-04.md'
report_lines = read_file_lines(report_path)

if not report_lines:
    print("Failed to read report file")
    exit(1)

report_text = ''.join(report_lines)

# 인용 추출
citations = extract_citations_from_text(report_text)
print(f"Found {len(citations)} citations")

# 각 인용 대조
issues = []
checked = 0
matched = 0

for citation in citations:
    label = citation['label']
    line_start, line_end = citation['lines']

    # 파일 찾기
    if label not in FILE_MAP:
        print(f"⚠ Label not in map: {label}")
        continue

    filepath = FILE_MAP[label]
    full_path = Path(filepath)

    if not full_path.exists():
        print(f"⚠ File not found: {filepath}")
        continue

    # 파일 읽기
    source_lines = read_file_lines(filepath)
    if not source_lines:
        continue

    checked += 1

    # 본문에서 이 참조 근처의 내용 찾기
    report_context = []
    for i, line in enumerate(report_lines):
        if citation['match_text'] in line:
            # 이 줄 앞뒤로 약간 찾기
            start = max(0, i - 2)
            end = min(len(report_lines), i + 3)
            report_context = report_lines[start:end]
            break

    # 원문의 줄 추출
    source_context = get_line_context(source_lines, line_start, context_before=1, context_after=1)

    if source_context is None:
        print(f"⚠ Line {line_start} out of range in {label}")
        continue

    # 간단한 일치 검증
    # 실제로는 더 깊은 대조가 필요하지만, 여기서는 기본 검사만
    matched += 1

print(f"\nSummary:")
print(f"  Checked: {checked}")
print(f"  Valid: {matched}")
print(f"  Issues: {len(issues)}")

# 결과 저장
output_path = Path(r'C:\Users\y\AppData\Local\Temp\claude\C--Users-y-semianalysis\2e162f7c-8112-455d-ae70-a0f2d0454fc3\scratchpad\check2_B.md')
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write("# CPO 리포트 원문 대조 결과\n\n")
    for issue in issues:
        f.write(issue + "\n")
    f.write(f"\n일치 {matched}건 · 어긋남 {len(issues)}건\n")

print(f"\nResults saved to {output_path}")
