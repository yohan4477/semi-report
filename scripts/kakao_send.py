"""카카오톡 「나에게 보내기」 전송기.

준비(최초 1회):
  1) https://developers.kakao.com 애플리케이션 추가
  2) 앱 설정 > 플랫폼 > Web > 사이트 도메인에 http://localhost 등록
  3) 카카오 로그인 활성화 ON, Redirect URI 에 http://localhost/oauth 등록
  4) 동의항목에서 「카카오톡 메시지 전송(talk_message)」 사용 설정
  5) 환경변수 KAKAO_REST_KEY 에 REST API 키를 넣고 `python scripts/kakao_send.py --auth`

토큰은 저장소 밖(~/.kakao_token.json)에 둔다. refresh_token 은 60일, access_token 은 6시간.

사용:
  python scripts/kakao_send.py --file 보낼내용.md
  echo "본문" | python scripts/kakao_send.py
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN_PATH = Path.home() / ".kakao_token.json"
REDIRECT_URI = "http://localhost/oauth"
TEXT_LIMIT = 190  # 텍스트 템플릿 text 상한 200자, 여유 10자
DEFAULT_LINK = "none"  # 말풍선에 링크를 안 붙인다


def rest_key():
    key = os.environ.get("KAKAO_REST_KEY")
    if not key:
        sys.exit("KAKAO_REST_KEY 환경변수가 없다.")
    return key


SECRET_PATH = Path.home() / ".kakao_secret"


def with_secret(data):
    """클라이언트 시크릿이 켜진 앱은 토큰 요청에 코드를 함께 보내야 한다."""
    secret = os.environ.get("KAKAO_CLIENT_SECRET")
    if not secret and SECRET_PATH.exists():
        secret = SECRET_PATH.read_text(encoding="utf-8").strip()
    if secret:
        data = dict(data, client_secret=secret)
    return data


def post(url, data, headers=None):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers or {})
    req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def auth(code=None):
    key = rest_key()
    params = urllib.parse.urlencode({
        "client_id": key,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "talk_message",
    })
    if not code:
        print("아래 주소를 브라우저에 붙여 동의하고, 되돌아온 주소의 code= 값을 붙여넣는다.\n")
        print(f"https://kauth.kakao.com/oauth/authorize?{params}\n")
        code = input("code: ").strip()
    tok = post("https://kauth.kakao.com/oauth/token", with_secret({
        "grant_type": "authorization_code",
        "client_id": key,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }))
    save_token(tok)
    print(f"토큰 저장: {TOKEN_PATH}")


def save_token(tok):
    tok["obtained_at"] = int(time.time())
    TOKEN_PATH.write_text(json.dumps(tok, ensure_ascii=False), encoding="utf-8")
    try:
        os.chmod(TOKEN_PATH, 0o600)
    except OSError:
        pass


def access_token():
    if not TOKEN_PATH.exists():
        sys.exit("토큰이 없다. `python scripts/kakao_send.py --auth` 먼저.")
    tok = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    age = int(time.time()) - tok.get("obtained_at", 0)
    if age < tok.get("expires_in", 21600) - 300:
        return tok["access_token"]
    fresh = post("https://kauth.kakao.com/oauth/token", with_secret({
        "grant_type": "refresh_token",
        "client_id": rest_key(),
        "refresh_token": tok["refresh_token"],
    }))
    fresh.setdefault("refresh_token", tok["refresh_token"])
    save_token(fresh)
    return fresh["access_token"]


def chunks(text, limit=TEXT_LIMIT):
    out, buf = [], ""
    for line in text.splitlines():
        while len(line) > limit:
            if buf:
                out.append(buf)
                buf = ""
            out.append(line[:limit])
            line = line[limit:]
        if len(buf) + len(line) + 1 > limit:
            out.append(buf)
            buf = line
        else:
            buf = f"{buf}\n{line}" if buf else line
    if buf.strip():
        out.append(buf)
    return out


def send(text, link=DEFAULT_LINK):
    token = access_token()
    parts = chunks(text)
    for i, part in enumerate(parts, 1):
        head = f"({i}/{len(parts)})\n" if len(parts) > 1 else ""
        payload = {
            "object_type": "text",
            "text": head + part,
            # link 를 비우면 말풍선을 눌러도 아무 데도 가지 않는다
            "link": {} if link in (None, "", "none") else {"web_url": link, "mobile_web_url": link},
        }
        res = post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send",
            {"template_object": json.dumps(payload, ensure_ascii=False)},
            {"Authorization": f"Bearer {token}"},
        )
        if res.get("result_code") != 0:
            sys.exit(f"전송 실패: {res}")
    print(f"전송 완료 — {len(parts)}건")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth", action="store_true", help="최초 토큰 발급")
    ap.add_argument("--code", help="동의 후 돌아온 주소의 code 값 (붙이면 대화 없이 교환)")
    ap.add_argument("--file", help="보낼 텍스트 파일")
    ap.add_argument("--link", default=DEFAULT_LINK, help="말풍선에 붙는 링크")
    args = ap.parse_args()
    if args.auth or args.code:
        auth(args.code)
        return
    text = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
    if not text.strip():
        sys.exit("보낼 내용이 비었다.")
    send(text.strip(), args.link)


if __name__ == "__main__":
    main()
