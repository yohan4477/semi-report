# -*- coding: utf-8 -*-
# AI Engineer 대시보드 — 컨퍼런스 발표 한 편이 카드 한 장이다.
#
# 만드는 규칙은 docs/AI Engineer 대시보드 — 만드는 규칙.md 가 정본이다.
# 카드를 쓰거나 도해를 붙이기 전에 그 문서를 연다 — 구조화(앞머리·축·비교표·한계)가
# 거기 있다.
#
# 다른 장과 다른 것이 하나 있다. 카드를 「핵심 포인트 · 주요 숫자 · 인용」으로 갈라 쓰지 않고,
# 메르 블로그처럼 **한 생각에 번호 하나**를 매겨 죽 늘어놓는다. 발표는 논지가 앞에서 뒤로
# 굴러가는 글이라, 조각으로 갈라 놓으면 「그래서 앞의 것이 뒤에 어떻게 걸리나」가 사라진다.
#
# 카드 목록을 이 파일에 적지 않는다. `content/understanding/AI Engineer/*.md` 한 편이
# 카드 한 장이고, 어느 섹션에 설지·주제칩·gain 까지 전부 그 글의 프런트매터에 있다.
# 글을 새로 넣고 이 파일을 다시 돌리면 카드가 는다.
#
# 프런트매터 필수 키
#   title date source speaker org channel dur section topic gain
#   section 은 아래 SEC 의 열쇠말 하나다. 없는 열쇠말을 적으면 생성이 멈춘다.
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import aie_figs                 # noqa: E402  번호글에 끼우는 도해

OUT = os.path.join(dc.ROOT, '대시보드', 'AI Engineer 대시보드.html')
SRC_DIR = os.path.join(dc.ROOT, 'content', 'understanding', 'AI Engineer')
REL = 'content/understanding/AI Engineer/%s'

STAMP = '2026-08-26'

# 섹션은 「무엇을 만드는 이야기인가」로 나눈다. 회사로 나누지 않는다 —
# 같은 회사가 훈련 이야기도 하고 제품 이야기도 하는데 회사로 묶으면 그게 한 칸에 뭉친다.
SEC = {
    'agent':   ('sec-agent', '01', '에이전트 만들기 · 운영',
                '데모에서 운영으로 넘어갈 때 무엇이 먼저 깨지나. 붙잡는 쪽이 만든 장치들'),
    'code':    ('sec-code', '02', '코딩 에이전트 · 개발 도구',
                '코드를 대신 쓰는 쪽이 무엇에서 막히나. 사람이 어디까지 쥐고 있어야 하나'),
    'rag':     ('sec-rag', '03', '검색 · 컨텍스트 · 기억',
                '모델에 무엇을 얼마나 넣어 주나. 찾아오는 일과 기억하는 일이 갈리는 자리'),
    'train':   ('sec-train', '04', '모델 훈련 · 후속 학습',
                '배포한 뒤에도 모델이 더 배우게 하려면 무엇을 모아야 하나'),
    'eval':    ('sec-eval', '05', '평가 · 결과물 품질',
                '정답이 없는 일을 어떻게 채점하나. 취향을 숫자로 바꾸는 자리'),
    'infra':   ('sec-infra', '06', '서빙 · 비용 · 인프라',
                '토큰을 싸게 많이 내보내는 일. 지연과 값이 부딪히는 자리'),
    'voice':   ('sec-voice', '07', '음성 · 멀티모달',
                '말로 주고받는 것이 글로 주고받는 것과 어디서 갈리나'),
    'product': ('sec-product', '08', '제품 · 조직 · 도입',
                '만든 것을 회사 안에 어떻게 들이나. 조직이 먼저 바뀌는 대목'),
}

# 한 섹션에 서른 장이 넘으면 목록이 아니라 벽이 된다. 갈래로 나누고 읽는 차례를 정해
# 섹션 머리에 세운다 — 카드 자체도 이 차례대로 선다(날짜순이 아니다).
# {섹션 열쇠말: [(갈래 이름, 한 줄, [영상 ID …]), …]}. 목록에 없는 카드는 갈래 뒤에 날짜순으로 붙는다.
TRACKS = {
    'agent': [
        ('먼저 읽을 것', '무엇이 먼저 깨지고, 왜 모델 탓이 아닌가',
         ['m24UKZomm7k', 'BInpv7lGp1o', 'R30col3UPUg', '3_gYbhABcAE']),
        ('하네스와 상태', '한 번의 부름을 넘어가는 것을 무엇이 쥐고 있나',
         ['shRR1e2HXMk', '8txf05vVVl4', 'j_TKDweOsYE', '9QebvrrY3KY',
          'aqW68Is_Kj4', 'CEvIs9y1uog', '9fubhllmsBU', 'pMggiOb18tc']),
        ('도구와 연결', '무엇을 쥐여 주나. 도구를 몇 개까지 두나',
         ['WJjInLeaJjo', '0n3MKk7r60w', 'RkVILz06y08', 'v3Fr2JR47KA',
          '_xIwFcnHqp4', 'Q3NreEAdKMc', 'VGN22pPpb-8']),
        ('운영에서 지키는 것', '권한·사고·규모. 터진 뒤에 무엇을 할 수 있나',
         ['rbjWzZK2LU0', 'Lc8zRh9muoY', '7gujZrJ9L5I', 'GdvKNwMcfd0',
          'abvQEhvRI_c', 'HT4l0DeP69I', 'b2GqTDWtg6s', '6lTxD_oUjXQ']),
        ('사람과 함께', '어디서 사람이 끼어들고 무엇을 보여 주나',
         ['fmZWvE7yDZo', 'HN-F-OQe6j0', 'ClWD8OEYgp8', 'iQ5xldZ9StU']),
    ],
    'rag': [
        ('먼저 읽을 것', '언제 그래프가 값을 하고 언제 안 하나',
         ['LLuKshphGOE', '-tgQa8Fzf80']),
        ('무엇을 담나', '사실 말고 지난 판단과 기억을 넣으면 무엇이 달라지나',
         ['Q0VkgCyNVUg', 'B9h9ovW5H9U']),
        ('만든 뒤에 남는 일', '재지 않으면 무엇이 잘못됐는지도 모른다',
         ['ROfHHJmumcc', 'c5qJHr3DnT4']),
    ],
    'eval': [
        ('먼저 읽을 것', '왜 재나, 그리고 어디까지 온 판인가',
         ['FB-MLPhL9Ms', 'a4BV0gGmXgA', 'nxokqOq1imY', 'Ubwb6NzegyA']),
        ('채점을 어떻게 짜나', '정답이 없는 일에 점수를 붙이는 법',
         ['6d60zVdcCV4', 'lCBf9slCanI', '0vphxNt4wyk', 'FWEInOtngmM']),
        ('자취를 보는 일', '내보낸 뒤에 남는 기록으로 무엇을 하나',
         ['XBaznoTRDFI', 'JsCCrBF7F1g', '_fQ7Z_Wfouk', '9HbzAWnKbo4']),
        ('값을 줄이는 일', '작은 것으로 같은 데까지 가기',
         ['pP_dSNz_EdQ', 'fWXJM-J0ZB8']),
        ('안전과 명세', '두드려 보고, 지킬 것을 글로 못 박기',
         ['JhJKgRAmfIU', 'J4vPq2i0QzE', '8rABwKRsec4']),
    ],
    'infra': [
        ('먼저 읽을 것', '무엇이 값과 속도를 정하나',
         ['Y2qc0UhDSnc', 'GJX19pNhmSw', 'lyL5QhgIOxc']),
        ('기기 위로 내리기', '밖으로 안 보내고 그 자리에서 돌리기',
         ['owH1f0N-keY', '_gVFUEdhCyI', 'Lm8BLHkxiAo', 'l614N5W60ls']),
        ('도구를 잇는 바닥', '무엇을 어디로 어떻게 흘려보내나',
         ['CD6R4Wf3jnY', '0NHCyq8bBcM']),
        ('실행 자리를 바꾼다', '도는 자리와 만드는 방식 자체를 다시 짜기',
         ['SKDJo2CopRs', 'RmS5s6Wbin4', 'r305-aQTaU0']),
    ],
}

# 영상 ID -> (섹션 열쇠말, 갈래 차례, 갈래 안 차례). 카드를 세우는 열쇠이자 검사용이다.
TRACK_POS = {vid: (sec, ti, vi)
             for sec, tl in TRACKS.items()
             for ti, (_lab, _sub, vids) in enumerate(tl)
             for vi, vid in enumerate(vids)}


KO_NUM = {2: '둘', 3: '셋', 4: '넷', 5: '다섯', 6: '여섯', 7: '일곱'}


def read_guide(sec_key, cards):
    """섹션 머리에 서는 「읽는 차례」. 갈래 이름과 그 안의 차례를 카드 앵커로 잇는다.

    안내만 두고 카드는 날짜순으로 두면 차례를 짚어 줘도 아래에서 찾아야 한다.
    그래서 카드도 이 차례로 세운다 — 여기 적힌 순서가 곧 화면 순서다."""
    by_vid = {c['_vid']: c for c in cards}
    out, n = [], 0
    for lab, sub, vids in TRACKS[sec_key]:
        got = [by_vid[v] for v in vids if v in by_vid]
        if not got:
            continue
        n += len(got)
        items = ''.join('<li><a href="#%s">%s</a></li>'
                        % (dc.slug(c['title']), esc(c['title'].split(' — ')[0]))
                        for c in got)
        out.append('<li><b>%s</b><span>%s</span><ol>%s</ol></li>' % (lab, esc(sub), items))
    miss = [c for c in cards if c['_vid'] not in TRACK_POS]
    tail = ('<p class="rd-tail">아직 갈래에 안 넣은 %d편은 아래 맨 뒤에 날짜순으로 붙어 있습니다.</p>'
            % len(miss)) if miss else ''
    return ('<details class="rd-guide" open><summary class="rd-sum">읽는 차례 — 갈래 %s</summary>'
            '<p class="rd-lede">%d편입니다. <b>카드도 이 차례로 서 있습니다</b> — '
            '위에서부터 읽으면 앞이 뒤를 받칩니다.</p>'
            '<ol class="rd-tracks">%s</ol>%s</details>'
            % (KO_NUM[len(TRACKS[sec_key])], n, ''.join(out), tail))


VERDICT_RE = re.compile(r'^한줄\s*코멘트[.,]?\s*(.+)$')
NUM_RE = re.compile(r'^(\d{1,3})\.\s+(.*)$')


def front(text):
    """맨 위 YAML 프런트매터를 얕게 읽는다. 값은 전부 문자열로 본다."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end < 0:
        return {}, text
    head, body = text[3:end], text[end + 4:]
    meta = {}
    for line in head.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body.lstrip('\n')


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def dur_ko(s):
    """길이 표기를 한 벌로 맞춘다 — 「16:30」도 「18분 20초」도 들어온다."""
    m = re.match(r'^(\d+):(\d{2})$', (s or '').strip())
    if not m:
        return s or ''
    mm, ss = int(m.group(1)), int(m.group(2))
    return '%d분 %d초' % (mm, ss) if ss else '%d분' % mm


def parse(path):
    """번호글 md 한 편 → (프런트매터, 번호글 목록, 한줄 코멘트)."""
    raw = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    meta, body = front(raw)
    items, verdict, expect = [], '', 1
    for para in re.split(r'\n\s*\n', body):
        t = ' '.join(para.split()).strip()
        if not t:
            continue
        m = VERDICT_RE.match(t)
        if m:
            verdict = esc(m.group(1))
            continue
        m = NUM_RE.match(t)
        if not m:
            continue
        n = int(m.group(1))
        # 번호가 튀면 사람이 봐야 한다 — 화면에서는 순서대로 다시 매겨지므로 조용히 어긋난다
        if n != expect:
            print('  ! %s 번호가 %d에서 %d로 튄다' % (os.path.basename(path), expect, n))
            expect = n
        items.append(esc(m.group(2)))
        expect += 1
    return meta, items, verdict


H_RE = re.compile(r'^##\s+(.*)$')
FIG_RE = re.compile(r'^\[\[fig:([a-z0-9_-]+)\]\]$')
BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
# 역참조는 raw 문자열이라야 한다. 따옴표 안의 \1은 8진 이스케이프라
# 제어문자 하나가 되고, 굵게 표시한 글이 통째로 사라진다(87곳이 그렇게 먹혔다)
BOLD_TO = r'<b>\1</b>'


def _terms(para):
    """용어 덩어리 → [(이름, 설명)].

    괄호로 풀던 것을 여기로 내렸다. 본문 한복판에 설명을 끼우면 문장이 길어지고
    읽는 눈이 한 번 끊긴다. 본문에는 별표 표시만 남기고 설명은 글 아래에 모은다.
    """
    out = []
    for line in para.strip().splitlines():
        line = line.strip()
        if not line.startswith('*'):
            continue
        name, _, desc = line[1:].partition('—')
        name, desc = name.strip(), desc.strip()
        assert name and desc, '용어 줄이 「*이름 — 설명」 꼴이 아니다: %r' % line
        out.append((esc(name), BOLD_RE.sub(BOLD_TO, esc(desc))))
    assert out, '용어 덩어리가 비었다'
    return out


def _mark(text, names):
    """본문 속 별표 표시를 용어 표시로 바꾼다.

    선언한 이름만 바꾼다. 그래야 뒤에 붙는 조사가 표시 안으로 딸려 들어가지 않고,
    선언 안 한 별표는 아래 assert에 걸린다."""
    # 검사가 먼저다. 치환한 결과 안에도 별표가 들어가므로 뒤에 재면 내가 넣은 것을 잡는다
    for m in re.finditer('[*]([^ *]+)', text):
        tail = text[m.start() + 1:]
        assert any(tail.startswith(n) for n in names),             '용어로 선언 안 한 별표가 있다: %r' % m.group(0)
    for name in sorted(names, key=len, reverse=True):
        text = re.sub('[*]' + re.escape(name),
                      '<span class="rf-term"><i>*</i>%s</span>' % name, text)
    return text


def _table(para, names=()):
    """마크다운 표 한 덩어리 → (제목, 머리, 행들).

    목록을 상자로 그리지 않기로 하면서 생긴 자리다. 이름과 한 줄 설명이 짝지어
    늘어서는 것은 그림이 아니라 표다 — 도해는 무엇을 주고 무엇을 받는지가 보일 때만 쓴다.
    """
    cap, head, rows = '', [], []
    for line in para.strip().splitlines():
        line = line.strip()
        if line.startswith('표:'):
            cap = esc(line[2:].strip())
            continue
        if not line.startswith('|'):
            continue
        cells = [_mark(BOLD_RE.sub(BOLD_TO, esc(c.strip())), names)
                 for c in line.strip('|').split('|')]
        if all(set(c) <= set('-: ') for c in cells):
            continue            # |---|---| 구분줄
        if head:
            rows.append(cells)
        else:
            head = cells
    assert head and rows, '표에 머리나 행이 없다: %r' % para[:40]
    return cap, head, rows


def parse_report(path, vid, figs=None):
    """보고서 형식 md 한 편 → (프런트매터, 블록 목록, 한줄 코멘트).

    번호글과 달리 절 제목(`## `)·문단·그림 부름(`[[fig:이름]]`)이 섞여 흐른다.
    그림은 `figs[영상ID][이름]`에서 꺼낸다 — 이름이 없으면 생성을 멈춘다.
    figs를 안 주면 `aie_figs.RFIGS`를 쓴다. 다른 장이 이 파서를 빌려 쓸 때
    자기 그림 사전을 넘긴다 — 언더스탠딩 보고서 장이 그렇게 쓴다.
    """
    raw = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    meta, body = front(raw)
    have = (aie_figs.RFIGS if figs is None else figs).get(vid, {})
    blocks, verdict, used = [], '', set()
    paras = re.split(r'\n\s*\n', body)
    # 용어는 본문보다 먼저 읽는다 — 이름을 알아야 본문의 별표를 제대로 짚는다
    terms = []
    for para in paras:
        if para.strip().startswith('용어'):
            terms = _terms(para)
    names = [n for n, _ in terms]
    for para in paras:
        if para.strip().startswith('용어'):
            continue
        t = ' '.join(para.split()).strip()
        if not t:
            continue
        m = VERDICT_RE.match(t)
        if m:
            # 굵게는 여기서도 먹여야 한다. esc만 거치면 별표가 글자 그대로 화면에 나간다
            verdict = BOLD_RE.sub(BOLD_TO, esc(m.group(1)))
            # 용어 표시는 안 거친다. 남은 별표가 있으면 그대로 나가므로 멈춘다
            assert '*' not in verdict, '한줄 코멘트에 별표가 남았다 — 용어는 본문에서 짚는다'
            continue
        if para.lstrip().startswith('|') or para.lstrip().startswith('표:'):
            blocks.append(('tbl', _table(para, names)))
            continue
        m = H_RE.match(t)
        if m:
            blocks.append(('h', esc(m.group(1))))
            continue
        m = FIG_RE.match(t)
        if m:
            key = m.group(1)
            assert key in have, '%s — 그림 %r가 aie_figs.RFIGS에 없다' % (os.path.basename(path), key)
            blocks.append(('fig', have[key]))
            used.add(key)
            continue
        blocks.append(('p', _mark(BOLD_RE.sub(BOLD_TO, esc(t)), names)))
    if terms:
        # 선언만 하고 본문에서 한 번도 안 짚은 용어는 아래 설명만 떠 있게 된다
        # 표는 (제목, 머리, 행들)이다. 머리 칸에서 용어를 처음 짚는 경우가 있어 셋 다 본다
        body_html = ' '.join(
            v if k == 'p' else ' '.join([v[0]] + list(v[1]) + [c for r in v[2] for c in r])
            for k, v in blocks if k in ('p', 'tbl'))
        for n, _ in terms:
            if ('>%s</span>' % n) not in body_html:
                print('  ! %s — 용어 %r를 본문에서 안 짚는다' % (os.path.basename(path), n))
        blocks.append(('terms', terms))
    for key in sorted(set(have) - used):
        print('  ! %s — 그림 %r를 본문에서 안 부른다' % (os.path.basename(path), key))
    return meta, blocks, verdict


def vid_of(url):
    return (url or '').rsplit('/', 1)[-1].split('?')[0]


def build():
    cards, bad = [], []
    for fn in sorted(os.listdir(SRC_DIR)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(SRC_DIR, fn)
        # 형식이 둘이다. 논지가 앞뒤로 걸리는 발표는 번호글로, 구조를 설명하는
        # 발표는 그림을 앞세운 보고서로 간다. 어느 쪽인지는 프런트매터가 정한다.
        head_meta, _ = front(io.open(path, encoding='utf-8').read().replace('\r\n', '\n'))
        is_report = head_meta.get('format') == 'report'
        if is_report:
            meta, items, verdict = parse_report(path, vid_of(head_meta.get('source', '')))
        else:
            meta, items, verdict = parse(path)
        # 덜 된 글은 화면에 올리지 않는다 — 번호글이나 한줄 코멘트가 비면 건너뛰고 적어 둔다
        why = (('본문 없음' if is_report else '번호글 없음') if not items else
               '한줄 코멘트 없음' if not verdict else
               'section 열쇠말이 SEC에 없다: %r' % meta.get('section') if meta.get('section') not in SEC else
               'gain 없음' if not meta.get('gain') else '')
        if why:
            bad.append((fn, why))
            continue
        cards.append({
            'section': SEC[meta['section']],
            'topic': ('market' if meta['section'] in ('product', 'infra') else 'tech',
                      meta.get('topic') or SEC[meta['section']][2]),
            'title': meta.get('title') or fn[:-3],
            'gain': meta['gain'],
            'meta': ['%s <b>%s</b>' % (meta.get('speaker', ''), meta.get('org', '')),
                     '발표 %s' % meta.get('date', ''),
                     dur_ko(meta.get('dur', '')),
                     meta.get('channel', 'AI Engineer')],
            ('report' if is_report else 'post'): items,
            'verdict': verdict,
            # 번호글은 한 줄에 한 생각이라 전체가 어떻게 맞물리는지가 안 잡힌다.
            # 그 한 장을 aie_figs가 갖고 있고 영상 ID로 붙인다.
            'figs': () if is_report else aie_figs.FIGS.get(vid_of(meta.get('source', '')), ()),
            'links': [('%s 전문 ↗' % ('보고서' if is_report else '번호글'),
                       dc.blob(REL % fn), ''),
                      ('발표 영상 ↗', meta.get('source', ''), '')],
            '_date': meta.get('date', ''),
            '_vid': vid_of(meta.get('source', '')),
            '_sec': meta['section'],
        })
    cards.sort(key=lambda c: c['_date'], reverse=True)
    # 섹션 차례는 SEC에 적은 번호다. 날짜로 두면 섹션 순서가 새 글이 들어올 때마다 바뀐다.
    cards.sort(key=lambda c: (c['section'][1],
                              TRACK_POS.get(c['_vid'], ('', 99, 99))[1:]))
    for key in TRACKS:
        listed = {v for _l, _s, vs in TRACKS[key] for v in vs}
        have = {c['_vid'] for c in cards if c['_sec'] == key}
        ghost = listed - have
        assert not ghost, '갈래에 없는 영상 ID가 적혀 있다: %s' % sorted(ghost)
    print('  카드 %d장' % len(cards))
    for fn, why in bad:
        print('  ! 건너뜀 %s — %s' % (fn, why))
    assert cards, '올릴 글이 하나도 없다'
    return cards


# 번호글 전용 CSS. 카드 본문 안에서만 쓰는 규칙이라 이 장에서만 붙인다.
POST_CSS = '''
  /* 번호글 — 한 생각에 번호 하나. 번호를 왼쪽에 떼어 놓고 글을 들여 쓴다 */
  .uc-post{list-style:none;margin:14px 0 0;padding:0;counter-reset:mp}
  .uc-post>li{counter-increment:mp;position:relative;padding:0 0 0 38px;margin:0 0 13px;
              font-size:.95rem;line-height:1.72;color:var(--ink-2)}
  .uc-post>li::before{content:counter(mp) ".";position:absolute;left:0;top:0;
              width:30px;text-align:right;font-variant-numeric:tabular-nums;
              font-weight:800;font-size:.82rem;line-height:1.98;color:var(--ink-3)}
  .uc-post>li:last-child{margin-bottom:0}
  /* 한줄 코멘트 — 글쓴이의 판단이 한 줄로 서는 자리. 번호글 위에 선다 */
  .uc-verdict{margin:14px 0 4px;padding:13px 15px;border-radius:12px;
              border:1px solid var(--line);background:var(--sunk,rgba(127,127,127,.06));
              font-size:.93rem;line-height:1.65;color:var(--ink)}
  .uc-verdict b{color:var(--ink-3);font-size:.78rem;letter-spacing:.04em;margin-right:6px}
  @media (max-width:520px){
    .uc-post>li{padding-left:30px}
    .uc-post>li::before{width:23px}
  }
  /* 보고서 — 절 제목과 문단이 섞여 흐른다. 번호글과 같은 카드 안에서 쓴다 */
  .uc-rep{margin:14px 0 0}
  .uc-rep h3{margin:26px 0 10px;font-size:1.02rem;line-height:1.45;font-weight:800;
             color:var(--ink);letter-spacing:-.01em}
  .uc-rep h3:first-child{margin-top:4px}
  .uc-rep p{margin:0 0 13px;font-size:.95rem;line-height:1.78;color:var(--ink-2)}
  .uc-rep p:last-child{margin-bottom:0}
  .uc-rep .uc-fig{margin:18px 0}
  /* 판은 520px까지만 넓힌다. 자리가 그보다 넓으면 배율이 1이라 판 안 글자가
     본문과 같은 .95rem으로 그려지고, 좁으면 판이 줄어든다. 어느 쪽이든 옆으로
     스크롤하지 않는다 — 776으로 내보내던 때는 창이 조금만 좁아도 밀렸다 */
  .ucard .uc-fig svg.epoch{width:100%;max-width:520px;margin:0 auto}
  /* HTML로 짠 판(.rfig). SVG는 판이 줄면 글자도 같이 줄어 본문과 어긋난다 —
     휴대폰에서 자리가 300px이면 520 판이 0.6배가 되고 글자가 9px로 앉았다.
     여기서는 글자가 본문과 같은 .95rem으로 고정이고, 좁아지면 칸이 아래로 쌓인다.
     기준은 화면 폭이 아니라 카드 안 자리다 — 그래서 컨테이너 질의를 쓴다 */
  .uc-fig .rfig{container-type:inline-size;margin:2px 0}
  .rfig .rf-row + .rf-row{margin-top:20px}
  .rfig .rf-cap{margin:0 0 10px;font-size:.95rem;font-weight:800;color:var(--ink-3)}
  .rfig .rf-pair{display:flex;align-items:stretch;gap:10px}
  .rfig .rf-box{flex:1 1 0;min-width:0;border:1px solid var(--ink-3);border-radius:10px;
                padding:12px 10px;background:var(--surface,#fff);text-align:center}
  .rfig .rf-box b{display:block;font-size:.95rem;font-weight:800;color:var(--ink);margin-bottom:5px}
  .rfig .rf-box span{display:block;font-size:.95rem;line-height:1.7;color:var(--ink)}
  .rfig .rf-empty{border-style:dashed}
  .rfig .rf-empty b,.rfig .rf-empty span{color:var(--ink-3)}
  .rfig .rf-harness{background:var(--epoch-wrapbg);border-color:var(--epoch-teal);border-width:1.6px}
  .rfig .rf-model{background:var(--sunk,rgba(127,127,127,.10))}
  .rfig .rf-msgs{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;
                 justify-content:center;gap:18px}
  /* 오가는 말이 없는 대비 판에서는 가운데가 늘면 안 된다 — 두 칸 사이에
     139px짜리 빈 곳이 생겼다. 비었으면 자리를 안 차지하게 둔다 */
  .rfig .rf-msgs:empty{flex:0 0 18px}
  .rfig .rf-msg{display:flex;align-items:center;gap:9px}
  .rfig .rf-msg em{flex:0 0 auto;font-style:normal;font-size:.95rem;line-height:1.45;color:var(--ink-3)}
  .rfig .rf-msg em b{display:block;font-weight:800;color:var(--ink-2)}
  .rfig .rf-msg em span{display:block;font-weight:600}
  .rfig .rf-msg.is-back em{text-align:right}
  /* 선은 받는 쪽 끝에 화살촉이 붙는다. 방향이 글자에도 선에도 있어야 안 헷갈린다 —
     라벨만 가운데 띄워 두면 둘 다 하네스가 하는 말로 읽힌다 */
  .rfig .rf-track{flex:1 1 auto;min-width:32px;height:0;align-self:center;position:relative;
                  border-top:2px solid var(--epoch-teal)}
  .rfig .rf-track::after{content:'';position:absolute;top:-6px;right:-1px;width:0;height:0;
                  border-top:6px solid transparent;border-bottom:6px solid transparent;
                  border-left:9px solid var(--epoch-teal)}
  .rfig .rf-track.is-back::after{right:auto;left:-1px;border-left:0;
                  border-right:9px solid var(--epoch-teal)}
  /* 흐름 판 — 칸을 늘어놓고 사이마다 화살표. 좁아지면 아래로 쌓인다 */
  .rfig .rf-chain{display:flex;align-items:stretch;gap:7px}
  .rfig .rf-step{flex:0 0 auto;align-self:center;width:0;height:0;
            border-top:6px solid transparent;border-bottom:6px solid transparent;
            border-left:9px solid var(--epoch-teal)}
  /* 칸을 잇는 것이 이름을 가진 것(프로토콜 등)일 때 화살표 위에 붙인다 */
  .rfig .rf-link{flex:0 0 auto;align-self:center;display:flex;flex-direction:column;
            align-items:center;gap:3px}
  .rfig .rf-link em{font-style:normal;font-size:.95rem;font-weight:700;color:var(--ink-3);
            white-space:nowrap}
  /* 여럿이 하나로 모이는 판에서 왼쪽에 쌓이는 입구들 */
  .rfig .rf-stack{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:6px}
  .rfig .rf-stack .rf-box{flex:0 0 auto;padding:8px}
  /* 마지막 칸이 처음으로 돌아가는 표시. 판 아래를 가로지르는 선과 왼쪽 화살촉 */
  .rfig .rf-loop{position:relative;margin:9px 0 2px;height:0;
            border-top:2px dashed var(--epoch-teal)}
  .rfig .rf-loop::after{content:'';position:absolute;top:-6px;left:-1px;width:0;height:0;
            border-top:6px solid transparent;border-bottom:6px solid transparent;
            border-right:9px solid var(--epoch-teal)}
  .rfig .rf-loop em{position:absolute;top:-11px;left:50%;transform:translateX(-50%);
            padding:0 8px;background:var(--surface,#fff);font-style:normal;
            font-size:.95rem;font-weight:700;color:var(--ink-3);white-space:nowrap}
  .rfig .rf-legend{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:14px}
  .rfig .rf-legend span{display:flex;align-items:center;gap:7px;font-size:.95rem;color:var(--ink-3)}
  .rfig .rf-sw{width:14px;height:14px;border-radius:4px;border:1px solid var(--ink-3);flex:0 0 auto}
  .rfig .rf-sw.rf-harness{background:var(--epoch-wrapbg);border-color:var(--epoch-teal)}
  .rfig .rf-sw.rf-model{background:var(--sunk,rgba(127,127,127,.10))}
  /* 시퀀스 판. 레인이 열이고 걸음이 행이다. SVG로 그리면 좁은 화면에서 글자까지
     같이 줄어서 CSS 그리드로 짠다 — 여기 글자도 본문과 같은 .95rem 고정이다 */
  .rfig .rq{display:grid;grid-template-columns:repeat(3,1fr);column-gap:0;
            align-items:center;position:relative}
  .rfig .rq-actor{align-self:start;text-align:center;font-size:.95rem;font-weight:800;
            color:var(--ink);border:1px solid var(--ink-3);border-radius:9px;padding:9px 4px;
            margin:0 4px;background:var(--surface,#fff)}
  .rfig .rq-actor.rf-harness{background:var(--epoch-wrapbg);border-color:var(--epoch-teal);border-width:1.6px}
  .rfig .rq-actor.rf-model{background:var(--sunk,rgba(127,127,127,.10))}
  .rfig .rq-actor.rf-human{background:var(--epoch-keybg)}
  /* 생명선 — 레인 한가운데로 내려가는 점선. 걸음 뒤에 깔린다 */
  .rfig .rq-life{width:0;justify-self:center;align-self:stretch;
            border-left:1px dashed var(--ink-3);opacity:.5}
  /* 말은 제 화살표 바로 위에 같은 열을 걸치고 앉는다. 보내는 쪽으로 붙여
     어느 레인에서 나온 말인지 자리로 보이게 한다 */
  .rfig .rq-lab{margin:16px 2px 5px;font-size:.95rem;line-height:1.6;font-weight:600;
            color:var(--ink-2);text-align:left}
  .rfig .rq-lab.is-back{text-align:right}
  /* 보내는 레인 한가운데에서 받는 레인 한가운데까지. 두 열을 걸친 칸에서
     양옆을 25%씩 미는 것이 정확히 그 자리다 */
  .rfig .rq-arrow{height:0;margin:2px 25% 10px;border-top:2px solid var(--epoch-teal);
            position:relative;align-self:center}
  .rfig .rq-arrow::after{content:'';position:absolute;top:-6px;right:-1px;width:0;height:0;
            border-top:6px solid transparent;border-bottom:6px solid transparent;
            border-left:9px solid var(--epoch-teal)}
  .rfig .rq-arrow.is-back::after{right:auto;left:-1px;border-left:0;
            border-right:9px solid var(--epoch-teal)}
  /* 자기 호출 — 하네스가 저 혼자 하는 걸음이다. 벌어지는 일을 칸 안에 적는다.
     빈 칸을 두고 글을 그 위에 얹으면 그 칸이 무엇을 하는 자리인지가 안 보인다 */
  .rfig .rq-self{justify-self:center;max-width:76%;margin:16px 0 10px;padding:11px 14px;
            border:2px solid var(--epoch-teal);border-radius:9px;background:var(--epoch-wrapbg);
            font-size:.95rem;line-height:1.6;font-weight:600;color:var(--ink-2);text-align:center}
  @container (max-width:430px){
    .rfig .rf-pair,.rfig .rf-chain{flex-direction:column;align-items:stretch}
    .rfig .rf-step{align-self:center;border-left:6px solid transparent;
            border-right:6px solid transparent;border-top:9px solid var(--epoch-teal);
            border-bottom:0}
    /* 칸이 세로로 쌓이면 선은 뜻을 잃는다. 선을 숨기고 이름만 남긴다 —
       「하네스가 시킨다」·「모델이 돌려준다」가 글자에 이미 들어 있다 */
    .rfig .rf-msgs{gap:12px}
    .rfig .rf-track{display:none}
    .rfig .rf-msg{justify-content:center}
    .rfig .rf-msg em,.rfig .rf-msg.is-back em{text-align:center}
    /* 레인 이름이 좁아지면 줄바꿈으로 버틴다. 열을 접으면 시퀀스가 아니게 된다 */
    .rfig .rq-actor{padding:8px 2px;margin:0 2px}
    .rfig .rq-lab{margin-top:14px}
  }
  /* 카드 안 글자는 한 값이다. 본문·판·판 제목·캡션·표까지 전부 .95rem이고
     층은 굵기와 색으로만 나눈다 — 크기로 가르면 자리마다 값이 갈린다 */
  .ucard .uc-fig .fig-title{font-size:.95rem;letter-spacing:0;text-transform:none}
  .ucard .uc-fig figcaption{font-size:.95rem;line-height:1.78}
  .uc-rep .uc-label{font-size:.95rem;letter-spacing:0;text-transform:none}
  /* 용어 — 본문에는 별표 표시만 남기고 설명은 글 아래에 모은다.
     괄호로 풀면 문장이 길어지고 읽는 눈이 그 자리에서 한 번 끊긴다 */
  .uc-rep .rf-term{font-weight:700;color:var(--ink)}
  .uc-rep .rf-term i{font-style:normal;font-weight:800;color:var(--epoch-teal);margin-right:1px}
  .uc-rep .rf-terms{margin:26px 0 0;padding:14px 15px;border-radius:12px;
            border:1px solid var(--line);background:var(--sunk,rgba(127,127,127,.06))}
  .uc-rep .rf-terms dl{margin:0}
  .uc-rep .rf-terms dt{margin:12px 0 2px;font-size:.95rem;font-weight:800;color:var(--ink)}
  .uc-rep .rf-terms dl>dt:first-of-type{margin-top:0}
  .uc-rep .rf-terms dt i{font-style:normal;color:var(--epoch-teal);margin-right:2px}
  .uc-rep .rf-terms dd{margin:0;font-size:.95rem;line-height:1.7;color:var(--ink-2)}
  .ucard .uc-verdict{font-size:.95rem}
  .uc-rep .tbl-wrap{overflow-x:visible}
  .uc-rep .uc-tbl{font-size:.95rem;min-width:0}
  .uc-rep .uc-tbl th{font-size:.95rem;letter-spacing:0;text-transform:none}
  /* 설명 칸까지 굵게 두면 표만 본문보다 무겁게 읽힌다 */
  .uc-rep .uc-tbl td:nth-child(2){font-weight:400;color:var(--ink-2)}
  /* 첫 칸이 안 접히면 좁은 자리에서 표가 카드 밖으로 밀린다 —
     「매달린 툴 호출」 한 칸 때문에 표가 311px로 벌어졌다 */
  .uc-rep .uc-tbl td:first-child{white-space:normal}
  /* 좁은 자리에서는 표가 칸 여백만으로도 넘친다. 세 열짜리 표가 295px 자리에서
     300px로 벌어졌다 — 여백을 조이고 긴 낱말도 끊는다. 기준은 화면이 아니라
     카드 안 자리라 .uc-rep 을 컨테이너로 삼는다 */
  .uc-rep{container-type:inline-size}
  @container (max-width:430px){
    .uc-rep .uc-tbl th,.uc-rep .uc-tbl td{padding:8px 7px}
    .uc-rep .uc-tbl{word-break:break-word}
  }

  /* 읽는 차례 — 섹션 머리 바로 아래. 갈래 이름과 그 안의 순서를 카드 앵커로 잇는다 */
  .rd-guide{margin:0 0 22px;padding:16px 18px;border:1px solid var(--line);
            border-radius:14px;background:var(--sunk,rgba(127,127,127,.05))}
  .rd-sum{cursor:pointer;font-size:.95rem;color:var(--ink);list-style:none}
  .rd-sum::-webkit-details-marker{display:none}
  .rd-sum::before{content:'▾ ';color:var(--epoch-teal)}
  .rd-guide:not([open]) .rd-sum::before{content:'▸ '}
  .rd-lede{margin:10px 0 14px;font-size:.92rem;line-height:1.6;color:var(--ink-2)}
  .rd-tracks{list-style:none;margin:0;padding:0;display:grid;gap:14px;
             grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
  .rd-tracks>li{counter-increment:rt;min-width:0}
  .rd-tracks{counter-reset:rt}
  .rd-tracks>li>b{display:block;font-size:.95rem;color:var(--ink)}
  .rd-tracks>li>b::before{content:counter(rt) ". ";color:var(--epoch-teal);
                          font-variant-numeric:tabular-nums}
  .rd-tracks>li>span{display:block;margin:2px 0 7px;font-size:.85rem;
                     line-height:1.5;color:var(--ink-3)}
  .rd-tracks ol{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}
  .rd-tracks ol li{padding:0 0 0 10px;margin:0 0 5px;font-size:.88rem;line-height:1.5}
  .rd-tracks ol a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid transparent}
  .rd-tracks ol a:hover{color:var(--epoch-teal);border-bottom-color:var(--epoch-teal)}
  .rd-tail{margin:13px 0 0;font-size:.85rem;color:var(--ink-3)}
''' + aie_figs.FIG_CSS

INTRO = ('<p>발표 한 편이 카드 한 장입니다. 글의 형식은 둘입니다. 논지가 앞의 말에서 뒤의 말로 '
         '굴러가는 발표는 <b>한 생각에 번호 하나</b>를 매겨 늘어놓고, 구조를 설명하는 발표는 '
         '<b>그림을 앞세운 보고서</b>로 씁니다. 어느 쪽이든 맨 위의 「한줄 코멘트」가 판단이고 '
         '그 아래가 거기까지 가는 걸음입니다.</p>'
         '<p>자막 전문에서 옮겼고, 발표자가 자기 회사를 파는 대목은 그렇다고 밝혀 두었습니다. '
         '숫자는 발표에 나온 것만 싣습니다.</p>')

if __name__ == '__main__':
    CARDS = build()
    HEADER = '''  <header>
    <p class="eyebrow">AI Engineer — 컨퍼런스 발표 아카이브</p>
    <h1>AI Engineer</h1>
    <p class="lede">에이전트를 실제로 굴려 본 사람들이 무엇에서 막혔고 무엇으로 뚫었는지. 발표 한 편을 <b>번호글</b>로 옮겨 담습니다.</p>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d편</b></span>
      <span>소스 <b>youtube.com/@aidotengineer</b></span>
    </div>
  </header>''' % (STAMP, len(CARDS))
    FOOTER = ('AI Engineer 컨퍼런스 발표 번역·정리 아카이브 · 원문 영상 링크를 카드마다 답니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_aie_dashboard.py</code>'
              '(공용 부품 <code>dash_common.py</code>).')
    dc.render(CARDS, 'AI Engineer', HEADER, FOOTER, OUT,
              extra_css=POST_CSS, intro=INTRO,
              sec_fig={SEC[k][0]: read_guide(k, [c for c in CARDS if c['_sec'] == k])
                       for k in TRACKS})
