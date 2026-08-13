/**
 * insight-dashboard.com 비밀번호 게이트 (Cloudflare Pages Functions).
 *
 * PROTECTED 경로는 쿠키 검증을 통과하기 전에는 next() 를 호출하지 않는다.
 * 즉 잠긴 문서의 HTML 은 인증 전에 클라이언트로 아예 나가지 않는다.
 *
 * 비밀번호는 저장소에 두지 않는다. Cloudflare Pages 프로젝트의
 * Settings > Variables and secrets 에 SITE_PASSWORD 를 secret 으로 등록해야 한다.
 */

const PROTECTED = new Set(['/semianalysis', '/usa-academy']);
const COOKIE = 'ida_auth';
const MAX_AGE = 60 * 60 * 24 * 30; // 30일

function normalize(pathname) {
  const p = pathname.replace(/\.html$/, '').replace(/\/+$/, '');
  return p === '' ? '/' : p;
}

async function tokenFor(password) {
  const bytes = new TextEncoder().encode('ida.v1:' + password);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)]
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

/** 길이·내용 모두 상수 시간 비교 (타이밍으로 정답을 되짚지 못하게). */
function safeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function readCookie(header, name) {
  if (!header) return null;
  for (const part of header.split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return null;
}

function loginPage(path, failed) {
  return `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>비밀번호 필요</title>
<style>
  :root {
    --bg:#fbfbf9; --fg:#1b1b19; --sub:#6c6a63; --line:#e5e3dc; --card:#fff; --accent:#b4522b;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg:#16161a; --fg:#eceae4; --sub:#9b988f; --line:#2c2c32; --card:#1e1e23; --accent:#e08a5f;
    }
  }
  :root[data-theme="dark"] {
    --bg:#16161a; --fg:#eceae4; --sub:#9b988f; --line:#2c2c32; --card:#1e1e23; --accent:#e08a5f;
  }
  * { box-sizing:border-box; }
  body {
    margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
    background:var(--bg); color:var(--fg); padding:24px;
    font-family:-apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  .box {
    width:100%; max-width:360px; background:var(--card);
    border:1px solid var(--line); border-radius:16px; padding:30px 28px 26px;
  }
  .ico { font-size:1.6rem; }
  h1 { font-size:1.12rem; letter-spacing:-.01em; margin:.7rem 0 .35rem; }
  p.sub { color:var(--sub); font-size:.86rem; line-height:1.6; margin:0 0 1.4rem; }
  input {
    width:100%; padding:11px 13px; font-size:.95rem; color:var(--fg);
    background:var(--bg); border:1px solid var(--line); border-radius:9px; outline:none;
  }
  input:focus { border-color:var(--accent); }
  button {
    width:100%; margin-top:10px; padding:11px; font-size:.93rem; font-weight:700;
    color:#fff; background:var(--accent); border:0; border-radius:9px; cursor:pointer;
  }
  .err { margin-top:11px; color:#c0392b; font-size:.83rem; }
  .hint { margin-top:16px; text-align:center; color:var(--sub); font-size:.74rem; opacity:.42; }
  .back { display:block; margin-top:18px; text-align:center; color:var(--sub); font-size:.8rem; }
</style>
</head>
<body>
  <form class="box" method="POST" action="${path}">
    <div class="ico">🔒</div>
    <h1>비밀번호가 필요한 문서입니다</h1>
    <p class="sub">비공개 아카이브입니다. 비밀번호를 입력하면 30일간 유지됩니다.</p>
    <input type="password" name="pw" placeholder="비밀번호" autofocus autocomplete="current-password">
    <button type="submit">들어가기</button>
    ${failed ? '<div class="err">비밀번호가 맞지 않습니다.</div>' : ''}
    <div class="hint">비밀번호는 주인님에게 물어보세요</div>
    <a class="back" href="/">← 목록으로</a>
  </form>
</body>
</html>`;
}

function htmlResponse(body, status) {
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    },
  });
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const path = normalize(url.pathname);

  if (!PROTECTED.has(path)) return next();

  const password = env.SITE_PASSWORD;
  if (!password) {
    return htmlResponse('SITE_PASSWORD 환경변수가 설정되지 않았습니다.', 500);
  }
  const expected = await tokenFor(password);

  if (request.method === 'POST') {
    const form = await request.formData();
    if (safeEqual(String(form.get('pw') ?? ''), password)) {
      return new Response(null, {
        status: 303,
        headers: {
          Location: path,
          'Set-Cookie': `${COOKIE}=${expected}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${MAX_AGE}`,
          'Cache-Control': 'no-store',
        },
      });
    }
    return htmlResponse(loginPage(path, true), 401);
  }

  if (safeEqual(readCookie(request.headers.get('Cookie'), COOKIE) ?? '', expected)) {
    const res = await next();
    const out = new Response(res.body, res);
    out.headers.set('Cache-Control', 'private, no-store');
    out.headers.set('X-Robots-Tag', 'noindex');
    return out;
  }

  return htmlResponse(loginPage(path, false), 401);
}
