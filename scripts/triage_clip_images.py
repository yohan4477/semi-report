"""클리핑 이미지를 크기만 보고 1차로 가른다. 그림을 열지 않는다.

substack 주소 끝에 원본 픽셀 크기가 박혀 있다(..._2300x1380.png).
표는 행이 쌓여 세로로 길고 폭이 넓다. 차트는 넓적하다. 로고·인물
사진은 작다. 이 셋을 크기만으로 갈라, 사람이나 모델이 실제로 볼
장수를 줄이는 것이 목적이다.

판정은 확정이 아니라 후보다. 2차(모델이 보는 단계)로 넘길 것만
고르는 체다.

    PYTHONIOENCODING=utf-8 python scripts/triage_clip_images.py
    PYTHONIOENCODING=utf-8 python scripts/triage_clip_images.py --list 표후보
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "input" / "clippings"
OUT = ROOT / "input" / "clip-images-triage.json"

IMG_RE = re.compile(r"!\[[^\]]*\]\((https://substackcdn\.com/[^)]+)\)")
SIZE_RE = re.compile(r"_(\d{2,5})x(\d{2,5})\.(png|jpe?g|webp|gif)", re.I)


def classify(w: int, h: int) -> str:
    """작은 것은 장식, 넓적한 것은 차트, 세로로 선 것은 표 후보."""
    px = w * h
    ratio = w / h if h else 0

    if px < 200_000:
        return "장식"          # 로고·아바타·아이콘. 볼 값어치 없다
    if ratio >= 2.2:
        return "넓은띠"        # 배너·타임라인. 표일 가능성 낮다
    if ratio <= 1.35:
        return "표후보"        # 행이 쌓인 꼴. 엑셀 표가 여기 있다
    return "차트후보"          # 1.35~2.2. 막대·선 그래프의 통상 비율


def main() -> int:
    want = None
    if "--list" in sys.argv:
        want = sys.argv[sys.argv.index("--list") + 1]

    rows = []
    unknown = 0
    for md in sorted(SRC.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for seq, cdn in enumerate(IMG_RE.findall(text), 1):
            m = SIZE_RE.search(cdn)
            if not m:
                unknown += 1
                continue
            w, h = int(m.group(1)), int(m.group(2))
            rows.append({
                "clip": md.stem,
                "seq": seq,
                "w": w,
                "h": h,
                "kind": classify(w, h),
                "url": cdn,
            })

    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    counts = Counter(r["kind"] for r in rows)
    print(f"이미지 {len(rows)} (크기 못 읽음 {unknown})")
    for kind, n in counts.most_common():
        print(f"  {kind:6} {n:5}  {n * 100 // max(len(rows), 1):2}%")

    if want:
        print()
        per = Counter(r["clip"] for r in rows if r["kind"] == want)
        print(f"[{want}] 많은 클리핑 20편")
        for clip, n in per.most_common(20):
            print(f"  {n:3}  {clip[:70]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
