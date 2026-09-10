# -*- coding: utf-8 -*-
"""RocketBlocks 장 — 페이지 껍데기와 두 줄기 블록.

이 장의 규약은 한 가지다. 모의면접 한 대목은 **발화**와 **해설** 두 줄기를
갖는다. 발화만 실으면 녹취록이고 해설만 실으면 교과서다. 발화는 가라앉은
바탕(--sunk) 블록, 해설은 맨 본문으로 둬서 읽는 사람이 「누가 한 말」과
「우리가 붙인 판단」을 색으로 가른다.

색은 감시 장(gen_watch_page) 팔레트를 그대로 받는다 — 새 시각 언어를 안 만든다.
"""
import html as _html

CSS = """
:root{
  --paper:#F3F5F7; --surface:#FFFFFF; --sunk:#E8ECF0;
  --ink:#101418; --ink-2:#4A5560; --ink-3:#7C8791;
  --line:#DDE2E7; --accent:#2B63D6;
  --good:#1F7A5C; --miss:#D6412B;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0F1418; --surface:#171D22; --sunk:#1E262C;
  --ink:#E9EDF0; --ink-2:#AAB4BC; --ink-3:#7C8791;
  --line:#263038; --accent:#5C8CE0;
  --good:#57B393; --miss:#E0704A;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 15px/1.7 "IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  font-variant-numeric:tabular-nums}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
a:hover{border-bottom-color:var(--ink)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{max-width:860px;margin:0 auto;padding:0 22px 90px}
header{padding:34px 0 0}
h1{font-size:23px;font-weight:700;letter-spacing:-.01em;margin:0}
.meta{font-size:12.5px;color:var(--ink-3);margin:6px 0 0}
.lede{color:var(--ink-2);margin:14px 0 0;max-width:66ch}
.back{display:inline-block;margin:24px 0 0;font-size:.82rem;font-weight:600;
  color:var(--ink-3);border-bottom:0}
.back:hover{color:var(--ink)}

/* 앞머리 상자 — 물음·바탕·읽는 법. 한줄 코멘트는 결론만 담고 나머지는 여기로 */
.lead{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;margin:20px 0 0}
.lead dt{font-size:11.5px;font-weight:850;color:var(--ink-3);letter-spacing:.04em}
.lead dd{margin:3px 0 12px;max-width:64ch}
.lead dd:last-child{margin-bottom:0}

/* 차례 — 한 줄에 절 하나 */
.toc{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:16px 20px;margin:18px 0 0;font-size:14px}
.toc ol{margin:0;padding-left:1.3em}
.toc li{margin:4px 0}
.toc a{border-bottom:0;color:var(--ink-2)}
.toc a:hover{color:var(--ink);border-bottom:1px solid var(--line)}

/* 대목 */
.beat{margin:44px 0 0;scroll-margin-top:18px}
.beat h2{font-size:19px;font-weight:700;margin:0;letter-spacing:-.01em}
.beat .watch{font-size:13px;color:var(--ink-3);margin:6px 0 0}
.beat p{max-width:66ch}

/* 대본 — 이 장의 본체. 턴이 끊기지 않게 바탕을 깔지 않고 왼쪽 띠로만 가른다.
   말한 사람 이름은 줄 위가 아니라 왼쪽 칸에 둔다 — 위에 얹으면 턴마다 줄이
   하나씩 늘어 대본이 두 배로 길어 보인다 */
.script{margin:18px 0 0}
.act{display:flex;align-items:center;gap:12px;margin:34px 0 14px}
.act:first-child{margin-top:18px}
.act-n{font-size:11.5px;font-weight:850;letter-spacing:.06em;color:var(--ink-3);
  white-space:nowrap}
.act-r{flex:1;height:1px;background:var(--line)}
.turn{display:grid;grid-template-columns:64px 1fr;gap:0 14px;margin:12px 0}
.turn .who{font-size:11.5px;font-weight:850;letter-spacing:.03em;padding-top:4px;
  text-align:right;color:var(--ink-3)}
.turn .line{border-left:3px solid var(--line);padding-left:14px;max-width:62ch}
.turn.q .line{border-left-color:var(--ink-3);color:var(--ink-2)}
.turn.a .line{border-left-color:var(--accent)}
.turn .line p{margin:0 0 10px}
.turn .line p:last-child{margin-bottom:0}
/* 지문 — 말이 아니라 그 자리에서 벌어진 일 */
.dir{grid-column:2;font-size:13px;color:var(--ink-3);font-style:italic;
  padding-left:17px;margin:10px 0}
/* 해설 — 대본을 끊고 들어오는 자리라 들여쓰고 이름을 붙인다 */
.note{margin:16px 0 0 78px;padding:12px 16px;background:var(--sunk);
  border-radius:10px;font-size:13.5px;max-width:60ch}
.note b{display:block;font-size:11px;font-weight:850;letter-spacing:.04em;
  color:var(--ink-3);margin-bottom:4px}
.note p{margin:0 0 8px}
.note p:last-child{margin-bottom:0}
@media (max-width:640px){
  .turn{grid-template-columns:1fr;gap:2px}
  .turn .who{text-align:left;padding-top:0}
  .dir{grid-column:1}
  .note{margin-left:0}
}

/* 발화 줄기 — 가라앉은 바탕. 지원자와 면접관은 왼쪽 띠 색으로 가른다 */
.said{background:var(--sunk);border-radius:12px;padding:4px 18px;margin:16px 0 0}
.sp{margin:14px 0;padding-left:14px;border-left:3px solid var(--line);
  font-size:14.5px;color:var(--ink-2)}
.sp b{display:block;font-size:11.5px;font-weight:850;letter-spacing:.04em;
  color:var(--ink-3);margin-bottom:2px}
.sp-i{border-left-color:var(--ink-3)}
.sp-c{border-left-color:var(--accent)}

/* 해설 줄기 — 맨 본문. 바탕을 안 깐다 */
.gloss{margin:18px 0 0}
.gloss p{margin:12px 0 0}
.gloss p:first-child{margin-top:0}

/* 요약 노트 — 케이스마다 하나. 대본을 다 읽고 손에 남길 것만 담는다.
   해설(.note)과 달리 테두리를 두른다 — 흐름을 끊고 들어오는 자리가 아니라
   다시 찾아올 자리다 */
.memo{border:1px solid var(--line);border-radius:12px;background:var(--surface);
  padding:6px 22px 22px;margin:18px 0 0}
.memo section{margin:22px 0 0}
.memo h3{font-size:12px;font-weight:850;letter-spacing:.05em;color:var(--ink-3);
  margin:0 0 10px}
.memo p{margin:0 0 10px;max-width:62ch}
.memo p:last-child{margin-bottom:0}
.memo table{margin-top:0}
/* 그대로 쓸 문장 — 따옴표 대신 왼쪽 띠로 세운다 */
.lines{margin:0;padding:0;list-style:none}
.lines li{border-left:3px solid var(--accent);padding:2px 0 2px 14px;margin:0 0 12px;
  max-width:60ch}
.lines li:last-child{margin-bottom:0}
.lines em{display:block;font-style:normal;font-size:12.5px;color:var(--ink-3);
  margin-top:3px}
/* 계산 골격 — 한 줄로 늘어놓는 곱셈 */
.chain{font-family:"IBM Plex Mono","IBM Plex Sans KR",monospace;font-size:13px;
  background:var(--sunk);border-radius:8px;padding:12px 14px;overflow-x:auto;
  white-space:nowrap;margin:0}

/* 판정 줄 — 잘한 수·빠진 수 */
.calls{margin:16px 0 0;padding:0;list-style:none;font-size:14px}
.calls li{margin:7px 0;padding-left:22px;position:relative;max-width:64ch}
.calls li::before{position:absolute;left:0;font-weight:850}
.calls .ok::before{content:"○";color:var(--good)}
.calls .mid::before{content:"△";color:var(--ink-3)}
.calls .no::before{content:"×";color:var(--miss)}

/* 표 */
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:18px 0 0}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;
  vertical-align:top}
th{font-size:11.5px;font-weight:850;color:var(--ink-3);letter-spacing:.03em;
  white-space:nowrap}
td.n{text-align:right;white-space:nowrap}
.tw{overflow-x:auto}

/* 도해 */
figure{margin:22px 0 0}
figure svg{display:block;width:100%;height:auto;background:var(--surface);
  border:1px solid var(--line);border-radius:12px}
figcaption{font-size:12.5px;color:var(--ink-3);margin:8px 0 0;max-width:64ch}
.t-lab{font-size:12.5px;font-weight:800;fill:var(--ink)}
.t-sm{font-size:11.5px;fill:var(--ink-2)}
.flow{stroke:var(--ink-3);stroke-width:1.5;marker-end:url(#ah)}

/* 목록 장 */
.rows{margin:20px 0 0;border-top:1px solid var(--line)}
.row{display:block;padding:14px 2px;border-bottom:1px solid var(--line);
  border-left:0;border-right:0;border-top:0}
.row:hover{background:var(--surface)}
.r-t{font-size:15.5px;font-weight:600}
.r-m{font-size:12.5px;color:var(--ink-3);margin:4px 0 0}
.tag{display:inline-block;font-size:11px;font-weight:700;color:var(--ink-3);
  border:1px solid var(--line);border-radius:999px;padding:2px 9px;margin-right:6px}
"""

AH = ('<svg width="0" height="0" style="position:absolute"><defs>'
      '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
      'markerHeight="7" orient="auto-start-reverse">'
      '<path d="M0 0 L10 5 L0 10 z" fill="var(--ink-3)"/></marker></defs></svg>')


def esc(s):
    return _html.escape(s, quote=False)


def page(title, body, desc=''):
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s</style></head><body>%s%s'
            '<div class="wrap">%s</div></body></html>'
            % (esc(title),
               '<meta name="description" content="%s">' % esc(desc) if desc else '',
               CSS, AH, '', body))


def act(name):
    """막 구분. 대목 이름 하나와 가로줄."""
    return '<div class="act"><span class="act-n">%s</span><i class="act-r"></i></div>' % esc(name)


def turn(who, *paras):
    """대본 한 턴. who 는 '면접관' 또는 '지원자'."""
    cls = 'q' if who == '면접관' else 'a'
    return ('<div class="turn %s"><div class="who">%s</div><div class="line">%s</div></div>'
            % (cls, esc(who), ''.join('<p>%s</p>' % esc(p) for p in paras)))


def direction(text):
    """지문 — 말이 아니라 그 자리에서 벌어진 일."""
    return '<div class="turn"><div class="dir">%s</div></div>' % esc(text)


def note(*paras):
    """해설. 대본을 끊고 들어오므로 짧게 둔다."""
    return ('<div class="note"><b>해설</b>%s</div>'
            % ''.join('<p>%s</p>' % esc(p) for p in paras))


def script(blocks):
    return '<div class="script">%s</div>' % ''.join(blocks)


def memo(blocks):
    """요약 노트. blocks 는 (소제목, html) 목록."""
    body = ''.join('<section><h3>%s</h3>%s</section>' % (esc(t), h) for t, h in blocks)
    return '<div class="memo">%s</div>' % body


def lines(items):
    """그대로 쓸 문장. items 는 (문장, 언제 쓰나) 목록."""
    return ('<ul class="lines">%s</ul>'
            % ''.join('<li>%s<em>%s</em></li>' % (esc(a), esc(b)) for a, b in items))


def chain(text):
    """계산 골격 한 줄."""
    return '<p class="chain">%s</p>' % esc(text)


def said(turns):
    """발화 줄기. turns 는 ('면접관'|'지원자', 글) 목록."""
    out = []
    for who, text in turns:
        cls = 'sp-i' if who == '면접관' else 'sp-c'
        out.append('<p class="sp %s"><b>%s</b>%s</p>' % (cls, esc(who), esc(text)))
    return '<div class="said">%s</div>' % ''.join(out)


def gloss(paras):
    return '<div class="gloss">%s</div>' % ''.join('<p>%s</p>' % esc(p) for p in paras)


def calls(items):
    """판정 줄. items 는 ('ok'|'no', 글) 목록."""
    return ('<ul class="calls">%s</ul>'
            % ''.join('<li class="%s">%s</li>' % (k, esc(v)) for k, v in items))


def fig(svg, caption):
    return '<figure>%s<figcaption>%s</figcaption></figure>' % (svg, esc(caption))


def table(head, rows, numcols=()):
    th = ''.join('<th>%s</th>' % esc(h) for h in head)
    tr = []
    for r in rows:
        tds = ''.join('<td%s>%s</td>' % (' class="n"' if i in numcols else '', esc(str(c)))
                      for i, c in enumerate(r))
        tr.append('<tr>%s</tr>' % tds)
    return ('<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody>'
            '</table></div>' % (th, ''.join(tr)))


def beat(num, name, watch, blocks):
    return ('<section class="beat" id="b%d"><h2>%d. %s</h2>'
            '<p class="watch">%s</p>%s</section>'
            % (num, num, esc(name), esc(watch), ''.join(blocks)))
