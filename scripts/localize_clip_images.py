"""뉴스레터 클리핑 md 의 substackcdn 이미지를 원본으로 받아 md 옆에 두고 링크를 로컬로 바꾼다.

클리핑을 오프라인에서도 그림째 읽게 하려는 것이다. 받은 그림은
<클리핑 폴더>/_img/<클리핑 파일명>/NNN_<원본 파일명> 에 둔다.
input/clip-images 에 같은 파일이 이미 있으면 내려받지 않고 복사한다.

원래 CDN 주소는 버리지 않고 이미지 제목 자리에 남긴다:
    ![](https://substackcdn.com/...)  →  ![](<_img/stem/001_x.png> "https://substackcdn.com/...")
fetch_clip_images·triage_clip_images 의 IMG_RE 가 두 꼴을 다 읽는다.
여러 번 돌려도 안전하다 — 이미 바꾼 링크는 건드리지 않는다.

    python scripts/localize_clip_images.py --since 2026
"""
import argparse
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "insights"))
import paths  # noqa: E402

SRC = paths.CLIP_SEMI
CACHE = ROOT / "input" / "clip-images"
RAW_RE = re.compile(r"!\[([^\]]*)\]\((https://substackcdn\.com/[^)\s]+)\)")
ANY_RE = re.compile(r'!\[[^\]]*\]\((?:<[^>]+> ")?(https://substackcdn\.com/[^)"\s]+)"?\)')
PUB_RE = re.compile(r"^published:\s*(\d{4})", re.M)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"


def original_url(cdn_url: str) -> str:
    idx = cdn_url.find("/https%3A%2F%2F")
    return urllib.parse.unquote(cdn_url[idx + 1:]) if idx != -1 else cdn_url


def safe_name(url: str, seq: int) -> str:
    tail = url.rsplit("/", 1)[-1].split("?")[0]
    tail = re.sub(r"[^A-Za-z0-9._-]", "_", tail)[:120]
    return f"{seq:03d}_{tail}"


def dir_name(stem: str) -> str:
    return re.sub(r"[^\w가-힣 .,()&+-]", "_", stem)[:120]


def fetch(url: str, out: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if not data:
        raise ValueError("빈 응답")
    out.write_bytes(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=int, default=2026, help="published 연도 하한")
    ap.add_argument("--only", help="파일명에 이 글자가 든 것만")
    a = ap.parse_args()

    docs = pages = got = copied = have = fail = 0
    fails: list[str] = []
    for md in sorted(SRC.glob("*.md")):
        if a.only and a.only.lower() not in md.name.lower():
            continue
        text = md.read_text(encoding="utf-8")
        m = PUB_RE.search(text)
        if not m or int(m.group(1)) < a.since:
            continue
        # 순번은 IMG_RE 순서(바꾼 것·안 바꾼 것 섞여도)와 같아야 input/clip-images 와 맞는다
        urls = ANY_RE.findall(text)
        if not urls:
            continue
        docs += 1
        sub = dir_name(md.stem)
        outdir = SRC / "_img" / sub
        outdir.mkdir(parents=True, exist_ok=True)
        local: dict[int, str] = {}
        for seq, cdn in enumerate(urls, 1):
            pages += 1
            name = safe_name(original_url(cdn), seq)
            out = outdir / name
            if not (out.exists() and out.stat().st_size > 0):
                cached = CACHE / sub / name
                try:
                    if cached.exists() and cached.stat().st_size > 0:
                        shutil.copyfile(cached, out)
                        copied += 1
                    else:
                        try:
                            fetch(original_url(cdn), out)
                        except Exception:  # noqa: BLE001  원본이 지워진 그림은 CDN 축소본으로
                            fetch(cdn, out)
                        got += 1
                except Exception as exc:  # noqa: BLE001
                    fail += 1
                    fails.append(f"{md.stem} #{seq}: {type(exc).__name__}")
                    time.sleep(1)
                    continue
            else:
                have += 1
            local[seq] = f"_img/{sub}/{name}"

        counter = iter(range(1, len(urls) + 1))

        def repl(mm: re.Match) -> str:
            seq = next(counter)
            whole = mm.group(0)
            if seq not in local or not RAW_RE.fullmatch(whole):
                return whole
            alt, cdn = RAW_RE.fullmatch(whole).groups()
            return f'![{alt}](<{local[seq]}> "{cdn}")'

        new = re.sub(ANY_RE, repl, text)
        if new != text:
            md.write_text(new, encoding="utf-8")

    print(f"문서 {docs} / 그림 {pages} / 새로받음 {got} / 복사 {copied} / 이미있음 {have} / 실패 {fail}")
    for line in fails[:15]:
        print("  실패:", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
