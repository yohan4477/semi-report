# -*- coding: utf-8 -*-
"""AI Engineer 주장 흐름 — 시간순 한 줄기.

아카이브 부품(dash_common)을 안 쓴다. 저기는 카드가 쌓이는 장이라 최신순 목록과
태그로 고르게 돼 있는데, 이 장은 위에서 아래로 한 줄기를 읽는 장이라 고를 것이
순서가 아니다. 규약은 아래 check_ui() 가 생성 때 검사한다 — 규약을 우회하려고 나온
장이 규약 없는 장이 되면 다음 사람이 같은 자리를 다시 판다.

산출은 대시보드/ 바로 아래다. 대시보드/ai-engineer/ 안에 두면
dash_common._write_card_pages 가 카드 슬러그가 아닌 html 을 매 생성 때 지운다.

색으로 입장을 가르지 않는다. 어느 주장이 어느 편인지는 우리가 매긴 값이고, 이 장이
내놓는 근거는 나란히 놓인 두 인용뿐이다. 관계는 기호(● ↑ ✕)와 선꼴(실선·점선)로만
가른다.

옅게 내는 자리가 둘이라 클래스를 나눈다. faint 는 아무 데도 안 걸린 주장이고
(126줄 중 40%가 그렇다) 이것은 생성 때 박혀 거르개를 눌러도 안 바뀐다. off 는
조직 거르개가 지금 안 고른 줄이라 누를 때마다 붙었다 떨어진다. 한 클래스로 겸하면
조직을 한 번 누르는 순간 고립 표시가 통째로 지워진다.
"""
import io
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import aie_thread_lib as lib          # noqa: E402
import ui_bits                        # noqa: E402
from card_lib import slug             # noqa: E402

OUT = os.path.join(ROOT, '대시보드', 'AI Engineer 주장 흐름.html')

MARK = {'신규': '●', '동조': '↑', '엇갈림': '✕'}

CSS = '''<style>
  :root { --ink:#1a1a1a; --dim:#555; --pale:#999; --line:#ddd; --bg:#fbfbfa; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.7 -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
         word-break:keep-all; overflow-wrap:anywhere; }
  .wrap { max-width:860px; margin:0 auto; padding:28px 18px 80px; }
  h1 { font-size:24px; margin:0 0 6px; }
  .lede { color:var(--dim); margin:0 0 22px; }
  .filters { position:sticky; top:0; background:var(--bg); padding:10px 0;
             border-bottom:1px solid var(--line); z-index:2; }
  .chip { display:inline-block; border:1px solid var(--line); background:#fff;
          border-radius:999px; padding:4px 12px; margin:0 6px 6px 0; cursor:pointer;
          font-size:13px; color:var(--dim); }
  .chip[aria-pressed="true"] { border-color:var(--ink); color:var(--ink); }
  .row { display:grid; grid-template-columns:24px minmax(0,1fr); gap:10px;
         padding:14px 0; border-bottom:1px solid var(--line); }
  .row[hidden] { display:none; }
  .mark { color:var(--dim); text-align:center; }
  .when { font-size:12px; color:var(--pale); }
  .who { font-size:13px; color:var(--dim); }
  .claim { margin:3px 0 0; }
  .row.faint .claim, .row.faint .who,
  .row.off .claim, .row.off .who { color:var(--pale); }
  .row.off .mark, .row.off .tie { opacity:.45; }
  .tie { margin:8px 0 0; padding:8px 12px; border-left:2px solid var(--line);
         background:#fff; font-size:14px; }
  .tie.cross { border-left-style:dashed; }
  .tie b { font-weight:600; }
  .q { display:block; color:var(--dim); margin:2px 0; }
  a.card { color:inherit; text-decoration:none; border-bottom:1px solid var(--line); }
</style>'''


def check_ui(html, rows):
    """이 장의 규약. 어기면 생성이 멈춘다."""
    bad = []
    if '반박' in html:
        bad.append('관계 이름은 동조·엇갈림 둘뿐이다 — 「반박」이 화면에 났다')
    for hexcol in ('#c00', '#d00', '#b00', '#00c', 'red', 'blue', 'green'):
        if hexcol in html:
            bad.append('입장을 색으로 가르지 않는다 — %s' % hexcol)
    if html.count('class="claim"') != len(rows):
        bad.append('주장 줄 수가 재료와 다르다')
    if '신규만' not in html or '엇갈림만' not in html:
        bad.append('거르개 둘(신규만·엇갈림만)이 없다')
    if 'ai-engineer/' not in html:
        bad.append('줄에서 카드로 가는 주소가 없다')
    return bad


def build():
    """재료를 읽어 HTML 한 장을 돌려준다. 파일로 쓰지는 않는다."""
    rows = lib.load()
    hard = lib.validate(rows)
    if hard:
        raise SystemExit('재료 규약 FAIL\n  ' + '\n  '.join(hard))
    by_id = {r['id']: r for r in rows}
    tied = set()
    for r in rows:
        for rel in r['rel']:
            tied.add(r['id'])
            tied.add(rel['to'])
    orgs = sorted({r['org'] for r in rows})

    out = []
    for r in rows:
        kinds = {rel['kind'] for rel in r['rel']} or {'신규'}
        mark = MARK['엇갈림'] if '엇갈림' in kinds else (
            MARK['동조'] if '동조' in kinds else MARK['신규'])
        faint = '' if r['id'] in tied else ' faint'
        ties = []
        for rel in r['rel']:
            src = by_id[rel['to']]
            ties.append(
                '<div class="tie%s"><b>%s</b> · %s %s 에 걸린다'
                '<span class="q">%s</span><span class="q">%s</span></div>'
                % (' cross' if rel['kind'] == '엇갈림' else '', rel['kind'],
                   src['date'], esc(src['org']), esc(src['claim']), esc(r['claim'])))
        out.append(
            '<div class="row%s" data-kinds="%s" data-org="%s">'
            '<div class="mark">%s</div><div>'
            '<div class="when">%s</div>'
            '<div class="who">%s · %s</div>'
            '<p class="claim"><a class="card" href="ai-engineer/%s.html">%s</a></p>'
            '%s</div></div>'
            % (faint, ' '.join(sorted(kinds)), esc(r['org']), mark, r['date'],
               esc(r['org']), esc(r['speaker']), slug(title_of(r)), esc(r['claim']),
               ''.join(ties)))

    chips = ['<button class="chip" data-f="all" aria-pressed="true">전부</button>',
             '<button class="chip" data-f="신규">신규만</button>',
             '<button class="chip" data-f="엇갈림">엇갈림만</button>',
             '<button class="chip" data-f="동조">동조만</button>']
    chips += ['<button class="chip" data-org="%s">%s</button>' % (esc(o), esc(o))
              for o in orgs]

    html = ('<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>AI Engineer 주장 흐름</title>\n' + CSS + '\n'
            + ui_bits.OPEN_AT_TOP + '\n<div class="wrap">\n'
            '<a class="card" href="AI Engineer 대시보드.html">← AI Engineer</a>\n'
            '<h1>주장 흐름</h1>\n'
            '<p class="lede">발표 %d편에서 뽑은 주장 %d줄. 위가 오래된 것이다. '
            '뒤에 온 주장이 앞선 주장에 걸리면 그 자리에 두 인용을 나란히 둔다. '
            '아무 데도 안 걸린 주장은 옅게 뒀다.</p>\n'
            '<div class="filters">%s</div>\n%s\n</div>\n%s\n'
            % (len({r['talk'] for r in rows}), len(rows), ''.join(chips),
               '\n'.join(out), JS))
    return html


JS = '''<script>
(function () {
  var rows = [].slice.call(document.querySelectorAll('.row'));
  var kind = 'all', org = '';
  function paint() {
    rows.forEach(function (el) {
      var okK = kind === 'all' || el.dataset.kinds.split(' ').indexOf(kind) >= 0;
      var okO = !org || el.dataset.org === org;
      el.hidden = !okK;
      el.classList.toggle('off', okK && !okO);
    });
  }
  [].forEach.call(document.querySelectorAll('.chip'), function (b) {
    b.addEventListener('click', function () {
      if (b.dataset.f) { kind = b.dataset.f === kind ? 'all' : b.dataset.f; }
      else { org = b.dataset.org === org ? '' : b.dataset.org; }
      [].forEach.call(document.querySelectorAll('.chip'), function (o) {
        var on = (o.dataset.f && o.dataset.f === kind) || (o.dataset.org && o.dataset.org === org)
                 || (o.dataset.f === 'all' && kind === 'all' && !org);
        o.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      paint();
    });
  });
  paint();
})();
</script>'''


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


_TITLES = {}


def title_of(r):
    """카드 페이지 주소는 카드 제목의 슬러그다 — 변환본 프런트매터에서 읽는다."""
    talk = r['talk']
    if talk in _TITLES:
        return _TITLES[talk]
    got = talk
    for ln in (lib.md_lines(talk) or ())[:20]:
        if ln.startswith('title: '):
            got = ln[7:].strip()
            break
    _TITLES[talk] = got
    return got


def main():
    rows = lib.load()
    html = build()
    bad = check_ui(html, rows)
    for m in bad:
        print('FAIL ·', m)
    if bad:
        return 1
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('주장 %d줄 · 고립 %.0f%% -> %s'
          % (len(rows), lib.orphan_ratio(rows) * 100, os.path.basename(OUT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
