"""클리핑 md 안의 substackcdn 이미지를 원본 해상도로 내려받는다.

CDN 주소 안에 원본 S3 주소가 URL 인코딩돼 박혀 있다. 그것을 풀어
w_1456 축소본이 아니라 원본(2300x1380 등)을 받는다. 표 그림은 글자를
읽어야 하므로 해상도가 곧 정보다.

저장 위치: input/clip-images/<클리핑 파일명>/NNN_<uuid>_<WxH>.<ext>
같은 이름 파일이 이미 있으면 건너뛴다. 여러 번 돌려도 안전하다.
"""
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "input" / "clippings"
DST = ROOT / "input" / "clip-images"

IMG_RE = re.compile(r"!\[[^\]]*\]\((https://substackcdn\.com/[^)]+)\)")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"


def original_url(cdn_url: str) -> str:
    """CDN 주소에서 안에 박힌 원본 주소를 꺼낸다. 없으면 그대로 돌려준다."""
    idx = cdn_url.find("/https%3A%2F%2F")
    if idx == -1:
        return cdn_url
    return urllib.parse.unquote(cdn_url[idx + 1:])


def safe_name(url: str, seq: int) -> str:
    tail = url.rsplit("/", 1)[-1].split("?")[0]
    tail = re.sub(r"[^A-Za-z0-9._-]", "_", tail)[:120]
    return f"{seq:03d}_{tail}"


def fetch(url: str, out: Path) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    out.write_bytes(data)
    return len(data)


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(SRC.glob("*.md"))
    if only:
        files = [f for f in files if only.lower() in f.name.lower()]

    total = skipped = ok = fail = 0
    fails: list[str] = []

    for md in files:
        urls = IMG_RE.findall(md.read_text(encoding="utf-8", errors="ignore"))
        if not urls:
            continue
        outdir = DST / re.sub(r"[^\w가-힣 .,()&+-]", "_", md.stem)[:120]
        outdir.mkdir(parents=True, exist_ok=True)
        for seq, cdn in enumerate(urls, 1):
            total += 1
            url = original_url(cdn)
            out = outdir / safe_name(url, seq)
            if out.exists() and out.stat().st_size > 0:
                skipped += 1
                continue
            try:
                fetch(url, out)
                ok += 1
            except Exception as exc:  # noqa: BLE001
                fail += 1
                fails.append(f"{md.stem} #{seq}: {type(exc).__name__}")
                time.sleep(1)

    print(f"대상 {total} / 새로받음 {ok} / 이미있음 {skipped} / 실패 {fail}")
    for line in fails[:10]:
        print("  실패:", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
