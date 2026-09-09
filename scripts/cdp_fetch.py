# -*- coding: utf-8 -*-
"""CDP 크롬으로 URL 본문을 받아 온다.

유튜브 RSS 를 파이썬에서 몰아 부르면 채널을 통째로 404 로 막는다. 클리핑에서 쓰던
방식 그대로 진짜 브라우저에 물어보면 막히지 않는다. 크롬이 없으면 조용히 띄운다.
"""
import json
import os
import subprocess
import time
import urllib.request

PORT = 9223
PROFILE = os.path.expanduser(r"~\.claude\chrome-kakao")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def _alive():
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
        return True
    except Exception:  # noqa: BLE001
        return False


def ensure_chrome(headless=True):
    if _alive():
        return True
    if not os.path.exists(CHROME):
        return False
    args = [CHROME, f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}", "--no-first-run", "--no-default-browser-check",
            "about:blank"]
    if headless:
        args.insert(1, "--headless=new")
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(20):
        time.sleep(1)
        if _alive():
            return True
    return False


def fetch(url, timeout=30):
    """브라우저 안에서 fetch 한 본문 문자열. 실패하면 예외를 올린다.

    받을 곳과 같은 출처로 탭을 먼저 옮긴다 — 다른 출처에서 부르면 CORS 가 막는다.
    """
    import urllib.parse

    import websocket  # 지연 임포트 — 이 길을 안 탈 때는 필요 없다

    parts = urllib.parse.urlsplit(url)
    origin = f"{parts.scheme}://{parts.netloc}/"

    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=5).read())
    tab = next(t for t in tabs if t.get("type") == "page")
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=timeout + 10)
    try:
        if not tab.get("url", "").startswith(origin):
            ws.send(json.dumps({"id": 90, "method": "Page.navigate",
                                "params": {"url": origin}}))
            deadline = time.time() + timeout
            while time.time() < deadline:
                if json.loads(ws.recv()).get("id") == 90:
                    break
            time.sleep(2)
        expr = (f"fetch({json.dumps(url)}, {{credentials:'omit'}})"
                ".then(function(r){return r.ok ? r.text() : 'HTTP '+r.status})")
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                            "params": {"expression": expr, "awaitPromise": True,
                                       "returnByValue": True}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(ws.recv())
            if msg.get("id") == 1:
                res = msg["result"]["result"]
                if "value" not in res:
                    raise RuntimeError(str(res)[:200])
                body = res["value"]
                if isinstance(body, str) and body.startswith("HTTP "):
                    raise RuntimeError(body)
                return body
        raise TimeoutError("CDP 응답 없음")
    finally:
        ws.close()
