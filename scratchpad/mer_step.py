# -*- coding: utf-8 -*-
"""사슬 하나를 한 편씩 넘겨 보는 층.

한 걸음 = 원문 한 편. 넘기면 그 편이 무엇을 더했는지가 주체별로 뜬다. 여섯 달을
한눈에 훑는 데는 주체 x 시간 표가 낫고, 한 편씩 따라가는 데는 이 층이 낫다 — 표는
접어서 이 아래에 같이 둔다.

**걸음은 좌우로 넘어간다.** 페이지 스크롤을 가로채지 않는다 — 카드 안에서 옆으로
미는 것과 페이지를 내리는 것이 갈려 있어야 카드를 지나쳐 읽을 수 있다. 화살표 단추,
키보드 좌우, 점 클릭, 손가락으로 밀기 넷 다 받는다. JS는 페이지에 한 벌만 나간다.
"""
from mer_map_svg import esc

BLOG = 'https://blog.naver.com/ranto28/%s'

CSS = """
/* ── 한 편씩 넘겨 보는 층 ── */
/* 이 페이지에는 --fig-* 토큰이 없다. 페이지가 이미 갖고 있는 색으로 이어 붙인다 —
   다크모드가 따라오는 것도 그 토큰들이 이미 하고 있다 */
.mtd{margin:14px 0 4px;--mtd-h:min(80vh,760px);--fig-bg:var(--sunk,#eef1f5);--fig-bxbg:var(--surface,#fff);
  --fig-good:var(--good,#16a34a);--fig-keybg:var(--good-soft,#e8f6ec)}
.mtd-bar{display:flex;align-items:center;gap:10px;
  margin:8px 0 6px;padding:8px 10px;border:1px solid var(--line);border-radius:10px;
  background:var(--fig-bg)}
.mtd-now{flex:1 1 auto;min-width:0;font-size:12px;color:var(--ink-3);line-height:1.4;
  height:35px;overflow:hidden}
.mtd-now b{display:block;font-size:12.5px;font-weight:850;color:var(--ink)}
.mtd-now span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mtd-dots{flex:0 0 auto;display:flex;gap:5px}
.mtd-dot{width:8px;height:8px;padding:0;border:0;border-radius:50%;background:var(--line);
  cursor:pointer}
.mtd-dot.on{background:var(--fig-good)}
/* 좌우 단추. 끝에 닿으면 흐려지고 눌러도 안 넘어간다 */
.mtd-nav{flex:0 0 auto;display:flex;gap:6px}
.mtd-go{width:30px;height:30px;padding:0;border:1px solid var(--line);border-radius:8px;
  background:var(--fig-bxbg);color:var(--ink-2);font-size:14px;line-height:1;cursor:pointer}
.mtd-go:hover{border-color:var(--fig-good);color:var(--fig-good)}
.mtd-go[disabled]{opacity:.35;cursor:default}
.mtd-go[disabled]:hover{border-color:var(--line);color:var(--ink-2)}
/* 판은 제자리에 서 있고 걸음이 옆으로 지나간다. 페이지 스크롤은 건드리지 않는다 */
.mtd-view{overflow:hidden;border:1px solid var(--line);border-radius:10px;
  background:var(--fig-bxbg);touch-action:pan-y}
.mtd-track{display:flex;align-items:stretch;will-change:transform;
  transition:transform .32s cubic-bezier(.22,.61,.36,1)}
/* 한 걸음이 판 폭을 다 쓴다. 긴 편은 그 칸 안에서만 내려 본다 */
.mtd-step{flex:0 0 100%;max-width:100%;min-width:0;margin:0;padding:0;box-sizing:border-box;
  max-height:var(--mtd-h);overflow-y:auto;overscroll-behavior:contain}
.mtd-line{display:flex;border-bottom:1px solid var(--line)}
.mtd-line:last-child{border-bottom:0}
.mtd-who{flex:0 0 124px;padding:10px 11px;background:var(--fig-bg,#f6f7f8);
  border-right:1px solid var(--line);font-size:12px;font-weight:850;color:var(--ink);
  line-height:1.35}
.mtd-who i{display:block;font-style:normal;font-weight:600;font-size:10.5px;
  color:var(--ink-3);margin-top:3px;line-height:1.4}
.mtd-what{flex:1 1 auto;min-width:0;padding:10px 12px;font-size:12.5px;
  color:var(--ink-2);line-height:1.55}
.mtd-what div+div{margin-top:7px}
.mtd-what em{font-style:normal;font-weight:800;color:var(--ink)}
.mtd-what q{display:block;quotes:none;font-size:11.5px;color:var(--ink-3);margin-top:1px}
.mtd-what u{text-decoration:none;font-size:11px;font-weight:700;color:var(--fig-good)}
.mtd-off .mtd-who{opacity:.45}
.mtd-more{font-size:11px;font-weight:700;color:var(--ink-3)}
.mtd-mine .mtd-who{color:var(--fig-good,#2f8f6b);background:var(--fig-keybg,#d8f0e6)}
.mtd-mine .mtd-who i{color:var(--fig-good)}
@media (max-width:560px){
  /* 폰에서는 주체 칸을 옆에 세울 자리가 없다. 124px을 떼 주면 내용이 230px로
     좁아져 문장이 다섯 줄씩 접힌다. 주체를 색 띠로 위에 올리고 내용이 폭을 다 쓴다 */
  .mtd-line{display:block}
  .mtd-who{padding:6px 10px;border-right:0;border-bottom:1px solid var(--line)}
  .mtd-who i{display:inline;margin:0 0 0 7px}
  .mtd-what{padding:9px 10px}
  /* 바는 단추 줄과 날짜 줄로 나눈다 — 셋이 한 줄에 서면 제목이 세 줄로 접힌다 */
  .mtd-bar{flex-wrap:wrap;gap:8px}
  .mtd-now{order:3;flex:1 0 100%;margin-top:1px}
  .mtd-dots{flex:1 1 auto;justify-content:center}
}
.mtd .mp-box{transition:opacity .3s}
.mtd.lit .mp-box{opacity:.28}
.mtd.lit .mp-box.on{opacity:1}

"""

JS = """
<script>
(function(){
  function steps(root){ return root.querySelectorAll('.mtd-step'); }
  // 주체 줄의 높이를 편끼리 맞춘다. 편마다 쓴 양이 달라 같은 주체가 위아래로
  // 튀면 넘길 때 눈이 줄을 다시 찾아야 한다 — 가장 긴 편에 나머지를 맞춘다
  function sync(root){
    var st = steps(root);
    if (!st.length || !root.querySelector('.mtd-view').clientWidth) return false;
    var n = st[0].querySelectorAll('.mtd-line').length, hs = [], k, j;
    for (j = 0; j < st.length; j++)
      st[j].querySelectorAll('.mtd-line').forEach(function(l){ l.style.height = ''; });
    for (k = 0; k < n; k++){
      var h = 0;
      for (j = 0; j < st.length; j++){
        var l = st[j].querySelectorAll('.mtd-line')[k];
        if (l) h = Math.max(h, l.getBoundingClientRect().height);
      }
      hs.push(Math.ceil(h));
    }
    for (j = 0; j < st.length; j++)
      st[j].querySelectorAll('.mtd-line').forEach(function(l, k2){
        l.style.height = hs[k2] + 'px'; });
    return true;
  }
  function go(root, i, quiet){
    var st = steps(root), n = st.length;
    i = Math.max(0, Math.min(n - 1, i));
    if (+root.dataset.i === i) return;
    root.dataset.i = i;
    root.querySelector('.mtd-track').style.transform = 'translateX(' + (-i * 100) + '%)';
    root.querySelector('.mtd-now').innerHTML = st[i].dataset.now;
    root.querySelectorAll('.mtd-dot').forEach(function(d, k){
      d.classList.toggle('on', k === i); });
    root.querySelector('.mtd-prev').disabled = (i === 0);
    root.querySelector('.mtd-next').disabled = (i === n - 1);
    // 지도에 불을 켠다 — 이 편에 실제로 나온 주체만
    var on = (st[i].dataset.on || '').split('|');
    root.classList.add('lit');
    root.querySelectorAll('.mp-box').forEach(function(b){
      b.classList.toggle('on', on.indexOf(b.dataset.a) >= 0); });
    // 줄 높이가 편끼리 같으므로 스크롤 자리를 그대로 물려주면 같은 주체가
    // 같은 높이에 선다. 0으로 되돌리면 그 정렬이 깨진다
    st[i].scrollTop = +root.dataset.sc || 0;
    if (!quiet) root.focus({preventScroll: true});
  }
  document.addEventListener('click', function(e){
    var d = e.target.closest('.mtd-dot');
    if (d) { go(d.closest('.mtd'), +d.dataset.go); return; }
    var g = e.target.closest('.mtd-go');
    if (!g || g.disabled) return;
    var root = g.closest('.mtd');
    go(root, +root.dataset.i + (+g.dataset.d));
  });
  document.addEventListener('keydown', function(e){
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var root = e.target.closest && e.target.closest('.mtd');
    if (!root) return;
    e.preventDefault();
    go(root, +root.dataset.i + (e.key === 'ArrowRight' ? 1 : -1));
  });
  // 손가락으로 밀기. 세로로 미는 것은 페이지 스크롤이므로 가로가 우세할 때만 넘긴다
  var x0 = 0, y0 = 0, tr = null;
  document.addEventListener('touchstart', function(e){
    tr = e.target.closest('.mtd-view') ? e.target.closest('.mtd') : null;
    if (!tr) return;
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
  }, {passive: true});
  document.addEventListener('touchend', function(e){
    if (!tr) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 42 && Math.abs(dx) > Math.abs(dy))
      go(tr, +tr.dataset.i + (dx < 0 ? 1 : -1), true);
    tr = null;
  }, {passive: true});
  // 지금 편을 내린 만큼을 기억해 다음 편에 물려준다
  document.addEventListener('scroll', function(e){
    var st = e.target.classList && e.target.classList.contains('mtd-step') ? e.target : null;
    if (!st) return;
    var root = st.closest('.mtd');
    if (st === steps(root)[+root.dataset.i]) root.dataset.sc = st.scrollTop;
  }, true);
  function boot(){
    document.querySelectorAll('.mtd').forEach(function(r){
      var first = !r.dataset.on1;
      if (!sync(r)) return;                 // 접혀 있으면 재 볼 수 없다. 펼칠 때 다시
      r.dataset.on1 = '1';
      if (first){ r.dataset.i = -1; go(r, 0, true); }
    });
  }
  var rt;
  window.addEventListener('resize', function(){
    clearTimeout(rt); rt = setTimeout(boot, 120); });
  document.addEventListener('click', function(e){
    if (e.target.closest('.uc-head, summary')) setTimeout(boot, 80);
  });
  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
</script>
"""








def steps(key, nodes, posts, mp):
    """한 걸음 = 원문 한 편. 걸음마다 그 편에 나온 주체와 마디를 담는다.

    **주체 줄은 편마다 달라지지 않는다.** 그 편에 안 나온 주체도 빈 칸으로 세운다 —
    줄이 사라지면 넘길 때마다 세로축이 흔들려 「이 편에서 이 주체가 조용했다」와
    「그 주체가 이 사슬에 없다」가 구분되지 않는다. 사슬 하나의 주체는 대여섯이라
    빈 줄을 다 세워도 판이 넘치지 않는다."""
    mine = [n for n in nodes if n['id'].startswith(key + ':')]
    actors = mp.get('actors') or {}
    order = list(mp.get('stackOrder') or actors)
    order += [a for a in actors if a not in order]
    by_src = {}
    for n in mine:
        by_src.setdefault(n['src'], []).append(n)
    # 사슬 전체를 관통하는 주체 축. 지도 순서가 먼저, 지도에 없는 주체는 편수 많은
    # 순으로 뒤에, 필자 판단은 맨 아래
    cnt = {}
    for n in mine:
        a = n.get('col', '')
        if a:
            cnt[a] = cnt.get(a, 0) + 1
    axis = [a for a in order if a in cnt and not a.startswith('메르')]
    axis += [a for a in sorted(cnt, key=lambda a: (-cnt[a], a))
             if a not in axis and not a.startswith('메르')]
    axis += [a for a in order if a in cnt and a.startswith('메르')]
    axis += [a for a in sorted(cnt) if a.startswith('메르') and a not in axis]
    out = []
    for src in sorted(by_src, key=lambda s: (posts[s]['date'], s)):
        ns = by_src[src]
        groups = [(a, [n for n in ns if n.get('col') == a]) for a in axis]
        out.append({'src': src, 'date': posts[src]['date'],
                    'title': posts[src]['title'], 'groups': groups})
    return out


def _line(n):
    """칸에 깔 한 줄. 풀이가 있으면 그것을, 없으면 인용을 낫표로 묶어 쓴다.

    **자르지 않는다.** 글자 수로 자르면 말끝이 「…」로 끝나 무슨 말인지 남지 않는다.
    풀이는 길어야 134자다 — 판이 그만큼 길어지는 편이 뜻이 잘리는 것보다 낫다."""
    t = (n.get('detail') or '').strip()
    if t:
        return t
    t = (n.get('quote') or '').strip()
    return ('「%s」' % t) if t else ''


def render(fig, sts, role, label, uid, with_js=False):
    """걸음. fig를 주면 그 위에 함께 서고, 빈 문자열이면 걸음만 선다."""
    dots = ''.join('<button class="mtd-dot%s" data-go="%d" aria-label="%d번째 편"></button>'
                   % (' on' if i == 0 else '', i, i + 1) for i in range(len(sts)))
    panes = []
    for st in sts:
        lines = []
        for a, ns in st['groups']:
            mine = a.startswith('메르')
            who = '이 사슬을 두고 필자가 한 말' if mine else role.get(a, '')
            what = ''.join(
                '<div><em>%s</em>%s<q>%s</q></div>'
                % (esc(n['label']),
                   (' <u>%s</u>' % esc(' · '.join(n['nums'][:2]))) if n.get('nums') else '',
                   esc(_line(n)))
                for n in sorted(ns, key=lambda n: (not n.get('lift'), n['id']))[:3])
            # 세 마디를 넘기면 판이 그 한 칸에 끌려간다. 몇이 남았는지는 적는다
            if len(ns) > 3:
                what += '<div class="mtd-more">그 밖에 %d마디</div>' % (len(ns) - 3)
            # 이 편에 안 나온 주체도 줄은 선다. 칸은 비워 둔다 — 빈 칸이 곧
            # 「이번엔 조용했다」다. 말로 적으면 줄마다 같은 문장이 반복된다
            lines.append('<div class="mtd-line%s%s"><div class="mtd-who">%s<i>%s</i></div>'
                         '<div class="mtd-what">%s</div></div>'
                         % (' mtd-mine' if mine else '',
                            '' if ns else ' mtd-off', esc(a), esc(who), what))
        now = ('<b>%s</b><span>%s</span>' % (esc(st['date']), esc(st['title'])))
        panes.append('<section class="mtd-step" data-now="%s" data-on="%s">%s</section>'
                     % (esc(now), esc('|'.join(a for a, ns in st['groups'] if ns)),
                        ''.join(lines)))
    nav = ('<div class="mtd-nav">'
           '<button class="mtd-go mtd-prev" data-d="-1" aria-label="앞 편">‹</button>'
           '<button class="mtd-go mtd-next" data-d="1" aria-label="다음 편">›</button>'
           '</div>')
    return ('<div class="mtd" id="%s" data-i="0" tabindex="0">%s'
            '<div class="mtd-bar">'
            '<div class="mtd-now"></div><div class="mtd-dots">%s</div>%s'
            '</div><div class="mtd-view"><div class="mtd-track">%s</div></div>'
            '<p class="mp-note">%s</p></div>%s'
            % (uid, fig, dots, nav, ''.join(panes), esc(label), JS if with_js else ''))
