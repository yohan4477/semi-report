# 두 페이지가 같은 스케일을 쓴다 — 규칙을 두 벌 두면 반드시 어긋난다.
# 여기 있는 것: 토큰·리셋·헤더·근거 상자·원자 카드·푸터, 그리고 모바일 토큰 재정의.
# 페이지 고유 규칙(사슬·레일·좌표 막대 등)은 각 생성기가 자기 <style>에 이어 붙인다.
BASE = r'''
  :root{--bg:#f7f8fa;--card:#fff;--ink:#1a2233;--sub:#5b6577;--faint:#8892a3;--line:#e3e7ee;--accent:#2563eb;--accent2:#1e40af;--soft:#eaf1fe;--sunk:#eef1f5;--shadow:0 1px 2px rgba(26,34,51,.05);
        /* 글자·간격은 여기서만 정한다. 모바일은 이 값만 바꾼다 — 규칙을 두 벌 두면 어긋난다 */
        --t-lbl:10.5px;--t-meta:12px;--t-body:13.5px;--t-lead:14.5px;--t-h2:19px;
        --r:12px;--pad:16px 20px;--gap:12px}
  @media (prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#7e8798;--line:#2a3140;--accent:#7aa5f8;--accent2:#9ab8fa;--soft:#1e2a44;--sunk:#242b38;--shadow:none}}
  *{box-sizing:border-box}
  html{font-size:100%}
  body{font-size:1rem;background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.64;margin:0;padding:0 20px 80px}
  .wrap{max-width:900px;margin:0 auto}
  header{padding:52px 0 6px}
  .eyebrow{font-size:var(--t-meta);font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
  h1{font-size:clamp(28px,6vw,44px);font-weight:850;letter-spacing:-.035em;margin:0}
  h1::after{content:"";display:block;width:52px;height:3px;background:var(--accent);margin-top:14px;border-radius:2px}
  .lede{color:var(--sub);font-size:var(--t-lead);margin:16px 0 0;max-width:64ch}
  .meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:var(--t-meta);color:var(--faint)}
  h3.sec{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:48px 0 4px;padding-top:24px;border-top:1px solid var(--line)}
  h4.sub2{font-size:var(--t-body);font-weight:800;color:var(--sub);margin:22px 0 8px}
  .ev{border:1px solid var(--line);border-radius:var(--r);background:var(--sunk);margin:14px 0 0}
  .ev>summary{cursor:pointer;padding:10px 13px;font-size:var(--t-meta);color:var(--sub);list-style:none}
  .ev>summary::-webkit-details-marker{display:none}
  .ev>summary::before{content:"▸ ";color:var(--faint)}
  .ev[open]>summary::before{content:"▾ "}
  .ev>summary b{color:var(--ink)}
  .ev .atom{padding:11px 13px;border-top:1px solid var(--line)}
  .axnote{font-size:var(--t-body);color:var(--sub);margin:0 0 14px;max-width:64ch}
  .atom{border-top:1px solid var(--line);padding:11px 0}
  .atom:first-of-type{border-top:0}
  .aid{font-size:var(--t-lbl);font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums}
  .atag{font-size:var(--t-lbl);font-weight:800;padding:1px 7px;border-radius:999px;margin-left:6px;background:var(--sunk);color:var(--faint)}
  .aclaim{font-size:var(--t-body);color:var(--ink);margin:3px 0 4px}
  .kv{font-size:var(--t-meta);color:var(--sub);margin:0 0 3px}
  .kv span{color:var(--faint)}
  .src{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:var(--t-meta);color:var(--sub);background:var(--sunk);
       border-left:2px solid var(--line);border-radius:0 6px 6px 0;padding:7px 9px;margin:5px 0 0;white-space:pre-wrap;word-break:break-word}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;background:var(--sunk);padding:1px 4px;border-radius:4px}
  .maplink{color:var(--accent);font-weight:700;text-decoration:none}
  .maplink:hover{text-decoration:underline}
  footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);font-size:var(--t-meta);color:var(--faint)}
  /* ── 모바일 — 값이 아니라 토큰만 바꾼다. 규칙을 두 벌 두면 반드시 어긋난다 ── */
  @media (max-width:640px){
    :root{--t-lbl:11.5px;--t-meta:12.5px;--t-body:14px;--t-lead:14.5px;--t-h2:17.5px;--pad:16px 15px}
    body{padding:0 14px 64px;line-height:1.66}
    .wrap{max-width:100%}
    header{padding:34px 0 4px}
    h1{font-size:clamp(26px,7.5vw,34px);letter-spacing:-.03em}
    .meta{gap:5px 14px}
    .ev>summary,.ev .atom{padding:13px 14px;min-height:44px}
    .atag{padding:2px 8px}
  }

'''
