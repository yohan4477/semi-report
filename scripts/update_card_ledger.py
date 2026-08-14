# -*- coding: utf-8 -*-
"""카드가 사이트에 처음 올라온 날 대장을 갱신한다.

영상 업로드일이 아니라 "인사이트에 올라온 날"이 기준이라, 그 날짜를 따로 들고 있어야 한다.
처음 보는 카드는 git 이력에서 그 카드가 대시보드 파일에 처음 등장한 커밋 날짜를 캐고,
못 찾으면 오늘로 잡는다. 한 번 기록된 날짜는 다시 건드리지 않는다.

로컬에서 돌리고 결과 JSON을 커밋한다 — Cloudflare 빌드는 이 파일을 읽기만 한다.
대시보드를 새로 생성한 뒤 커밋 전에 실행하면 된다.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_site import PAGES, SRC, ROOT  # noqa: E402

LEDGER = ROOT / 'data' / 'site_card_first_seen.json'
CARD_ID = re.compile(r'<h2 id="(card-[^"]+)"')
# 다른 대시보드의 카드를 그대로 옮겨 담는 페이지. NEW 기준은 원래 페이지에 올라온 날이라
# 여기서 새로 날짜를 잡으면 옛 카드가 전부 새 카드로 보인다
COPY_SLUGS = {'unified'}


def git_first_seen(rel_path: str, needle: str) -> str | None:
    """해당 문자열이 그 파일에 처음 들어온 커밋 날짜 (pickaxe)."""
    try:
        out = subprocess.run(
            ['git', 'log', '--reverse', '--format=%ad', '--date=short',
             '-S', needle, '--', rel_path],
            cwd=ROOT, capture_output=True, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    lines = out.stdout.decode('utf-8', 'replace').split('\n')
    for line in lines:
        line = line.strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', line):
            return line
    return None


def main():
    today = date.today().isoformat()
    ledger = json.loads(LEDGER.read_text(encoding='utf-8')) if LEDGER.exists() else {}

    added = dropped = 0
    # 원본 페이지를 먼저 처리해야 복사본이 그 날짜를 물려받는다
    pages = sorted(PAGES, key=lambda p: p[1] in COPY_SLUGS)
    for src, slug, *_ in pages:
        path = SRC / src
        ids = CARD_ID.findall(path.read_text(encoding='utf-8'))
        if not ids:
            continue  # 카드 단위가 없는 대시보드(SemiAnalysis)는 건너뛴다

        book = ledger.setdefault(slug, {})
        rel = f'대시보드/{src}'
        origin = {}
        if slug in COPY_SLUGS:
            for other, seen in ledger.items():
                if other == slug:
                    continue
                for cid, day in seen.items():
                    if cid not in origin or day < origin[cid]:
                        origin[cid] = day
        for cid in ids:
            if cid in book:
                continue
            book[cid] = origin.get(cid) or git_first_seen(rel, cid) or today
            added += 1
            print(f'  + {slug}/{cid[:44]} -> {book[cid]}')

        for gone in [k for k in book if k not in ids]:
            del book[gone]
            dropped += 1

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=1, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    total = sum(len(v) for v in ledger.values())
    print(f'\n신규 {added} / 삭제 {dropped} / 전체 {total}  -> {LEDGER}')


if __name__ == '__main__':
    main()
