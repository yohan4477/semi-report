"""소스별로 아직 처리하지 않은 영상이 몇 편인지 센다.

이미 처리한 영상은 content/·insights/ 안 파일에서 11자리 영상 ID로 찾는다
(frontmatter `vid:` 또는 본문의 youtu.be·watch?v= 링크).
유튜브 RSS 는 채널마다 최근 15편만 준다 — 매일 돌리는 것을 전제로 한다.

  PYTHONIOENCODING=utf-8 python scripts/count_new.py
  PYTHONIOENCODING=utf-8 python scripts/count_new.py --kakao   # 카톡으로 보낸다
"""
import argparse
import glob
import re
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 이름 -> 유튜브 채널 ID
CHANNELS = {
    "언더스탠딩": "UCIUni4ScRp4mqPXsxy62L5w",
    "Semi Doped": "UCqIzK82kDT3zpA5OcPDg3Rg",
    "AI Engineer": "UCLKPca3kwwd-B59HNr-_lvA",
    "SemiAnalysis 팟캐스트": "UCf_KhBXw5TIV0A7butjgFhg",
    "채널 씨모어": "UCeoGAFzUkVQ9RgLKDdFmUZw",
}

ID_RE = re.compile(r"(?:vid:\s*|youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})")


def processed_ids():
    seen = set()
    for pat in ("content/**/*.md", "insights/**/*.md", "input/**/*.md"):
        for f in glob.glob(pat, recursive=True):
            try:
                seen.update(ID_RE.findall(open(f, encoding="utf-8").read()))
            except (OSError, UnicodeDecodeError):
                continue
    return seen


def _raw(url):
    """먼저 브라우저에 묻는다 — 파이썬으로 몰아 부르면 유튜브가 채널을 막는다."""
    import cdp_fetch

    if cdp_fetch.ensure_chrome():
        return cdp_fetch.fetch(url)
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=30
    ).read().decode("utf-8", "replace")


def feed(channel_id, tries=4):
    """유튜브가 곧잘 404를 던진다 — 간격을 늘려 가며 다시 묻는다."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    last = None
    for attempt in range(tries):
        try:
            raw = _raw(url)
            out = []
            for entry in re.findall(r"<entry>(.*?)</entry>", raw, re.S):
                vid = re.search(r"<yt:videoId>(.*?)</yt:videoId>", entry)
                title = re.search(r"<title>(.*?)</title>", entry)
                pub = re.search(r"<published>(.*?)</published>", entry)
                if vid and title and pub:
                    out.append((pub.group(1)[:10], vid.group(1), title.group(1)))
            return sorted(out, reverse=True)
        except Exception as exc:  # noqa: BLE001 - 네트워크 예외 종류가 여럿이다
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kakao", action="store_true", help="결과를 카카오톡으로 보낸다")
    args = ap.parse_args()

    sys.path.insert(0, "scripts")
    done = processed_ids()
    got = {}
    # 유튜브는 몰아서 부르면 채널을 통째로 막는다. 실패한 채널만 뜸을 들여 다시 묻는다
    for rnd in range(3):
        left = [(n, c) for n, c in CHANNELS.items() if n not in got]
        if not left:
            break
        if rnd:
            print(f"{len(left)}개 채널 재시도 — {60 * rnd}초 쉰다")
            time.sleep(60 * rnd)
        for name, cid in left:
            try:
                got[name] = feed(cid)
            except Exception as exc:  # noqa: BLE001
                got[name] = f"피드를 못 읽었다 ({type(exc).__name__})"
        got = {n: v for n, v in got.items() if isinstance(v, list)}

    sources, total = [], 0
    for name in CHANNELS:
        items = got.get(name)
        if items is None:
            sources.append((name, "피드를 못 읽었다"))
            continue
        new = [i for i in items if i[1] not in done]
        total += len(new)
        sources.append((name, new))

    # 전부 실패하면 0편짜리 장이 멀쩡한 장을 덮어쓴다. 그럴 바엔 아무것도 안 한다
    if not got:
        print("모든 채널이 막혔다. 목록도 안 고치고 카톡도 안 보낸다.")
        return 1

    sys.path.insert(0, "scripts")
    import gen_newsrc_page

    path = gen_newsrc_page.write(sources, total)
    print(f"목록 -> {path}")

    tally = " · ".join(
        f"{n} {len(v)}" if isinstance(v, list) else f"{n} 실패" for n, v in sources)
    failed = [n for n, v in sources if not isinstance(v, list)]
    # 실패한 채널을 뺀 채로 합계만 보내면 적게 나온 수를 사실로 읽는다
    head = f"[아직 처리 안 한 것 {total}편]"
    if failed:
        head = f"[아직 처리 안 한 것 {total}편 이상]"
    msg = f"{head}\n{tally}\n\n"
    if failed:
        msg += f"{'·'.join(failed)} 는 못 셌다. 합계에 안 들어갔다.\n\n"
    msg += "말풍선을 누르면 목록이 열린다."
    print(msg)
    if args.kakao:
        import kakao_send

        kakao_send.send(msg, gen_newsrc_page.PUBLIC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
