# -*- coding: utf-8 -*-
"""메르 흐름도의 자료 구조와 검사.

흐름도는 두 겹이다. 메르 글은 한 편이 이미 사슬이라서(앞 글 요약 번호 → 새 사건 →
메커니즘 → 부작용 → 관전포인트 → 한줄 코멘트) 한 번 읽어 둘 다 뽑는다.

  글 안(intra)  한 편이 작은 개념도다. 마디는 그 편의 단계이고 카드 본문에 들어간다.
  글 사이(inter) 편마다 `lift`로 표시한 마디 한둘만 시간축에 서고 화살표가 편을 가로지른다.

마디 역할(role)은 여섯이다 — 메르 글이 실제로 그렇게 굴러간다.
  bg      배경. 앞 글에서 이어받은 전제
  event   날짜가 박힌 일. 「8/19 재무부가 1회 바이백 한도를 20억→40억달러로」
  mech    메커니즘 한 단계. 「장기채 물량이 준다 ⇒ 귀해진다 ⇒ 값이 올라 금리가 내린다」
  risk    부작용·반대 방향. 「단기채로 갈아타 만기가 짧아진다」
  watch   관전포인트. 나중에 맞았는지 볼 수 있는 분기점
  verdict 한줄 코멘트. 그 편의 결론

kind는 그 마디가 사실인지 판단인지다 — event/bg는 event, 나머지는 claim으로 적는다.
화살표(edge)는 마디 사이의 관계다.
  cause      앞이 뒤를 낳는다
  update     뒤 글이 앞 판단을 고친다(A/S)
  contradict 뒤가 앞과 어긋난다

**없는 값을 그리지 않는다.** 마디마다 원문 글번호(src)와 그 글에 실제로 있는 구절(quote)을
달고, 이 파일의 check()가 원문과 대조한다. 대조에 실패하면 화면에 올리지 않는다.
"""
import json, io, os, re, glob, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'input', 'clippings', 'mer')
FLOW = os.path.join(ROOT, 'insights', 'flows', 'mer')

LANES = [
    ('rate', '미국 금리 · 재무부'),
    ('fx', '환율 · 물가 · 한국은행'),
    ('krx', '국장 수급 · 제도'),
    ('semi', '반도체'),
    ('ai', 'AI · 전력'),
    ('comm', '원자재 · 에너지'),
    ('geo', '지정학 · 통상'),
]
LANE_ID = {k for k, _ in LANES}
KINDS = {'event', 'claim'}
ROLES = {'bg', 'event', 'mech', 'risk', 'watch', 'verdict'}
EDGES = {'cause', 'update', 'contradict'}


def load_posts():
    out = {}
    for p in glob.glob(os.path.join(SRC, '*.json')):
        d = json.load(io.open(p, encoding='utf-8'))
        out[d['no']] = d
    return out


def norm(s):
    return re.sub(r'\s+', '', s or '')


def load_flow():
    """마디 id는 파일 안에서만 유일하면 된다 — 불러올 때 파일 이름을 앞에 붙여 갈라놓는다.
    사슬 하나가 파일 하나라 a1·b1 같은 짧은 id를 그대로 쓸 수 있다."""
    nodes, edges = [], []
    for p in sorted(glob.glob(os.path.join(FLOW, '*.json'))):
        d = json.load(io.open(p, encoding='utf-8'))
        key = os.path.basename(p)[:-5]
        for n in d.get('nodes', []):
            n = dict(n, id='%s:%s' % (key, n['id']), thread=d.get('thread', ''))
            nodes.append(n)
        # 다른 사슬의 마디를 가리킬 때는 파일 이름까지 적는다(rate_0818:a5). 콜론이 있으면
        # 이미 갈라진 이름이라 그대로 둔다 — 사슬끼리 잇는 화살표가 이걸로 붙는다.
        def q(v):
            return v if ':' in v else '%s:%s' % (key, v)
        for e in d.get('edges', []):
            edges.append(dict(e, **{'from': q(e['from']), 'to': q(e['to'])}))
    return nodes, edges


def check(nodes, edges, posts):
    """FAIL 목록을 돌려준다. 빈 목록이라야 화면에 올린다."""
    bad = []
    ids = {}
    for n in nodes:
        i = n.get('id')
        if not i:
            bad.append(('노드에 id 없음', json.dumps(n, ensure_ascii=False)[:70]))
            continue
        if i in ids:
            bad.append(('id 중복', i))
        ids[i] = n
        if n.get('lane') not in LANE_ID:
            bad.append(('레인 모름', '%s %s' % (i, n.get('lane'))))
        if n.get('kind') not in KINDS:
            bad.append(('마디 종류 모름', '%s %s' % (i, n.get('kind'))))
        if n.get('role') not in ROLES:
            bad.append(('마디 역할 모름', '%s %s' % (i, n.get('role'))))
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', n.get('date') or ''):
            bad.append(('날짜 형식', '%s %s' % (i, n.get('date'))))
        src = n.get('src')
        if src not in posts:
            bad.append(('원문 글번호 없음', '%s %s' % (i, src)))
            continue
        q, text = norm(n.get('quote')), norm(posts[src]['text'])
        if not q:
            bad.append(('인용 없음', i))
        elif q not in text:
            r = difflib.SequenceMatcher(None, q, text).find_longest_match(0, len(q), 0, len(text))
            if r.size / max(len(q), 1) < 0.8:
                bad.append(('인용이 원문에 없다', '%s | %s' % (i, (n.get('quote') or '')[:40])))
        ac = (n.get('actor') or '').strip()
        if not ac:
            bad.append(('마디에 주체(actor)가 없다', i))
        # 주체는 사람·기관·시장 참가자여야 한다. 「개입 구조」·「전환 제도」처럼 없는 행위자를
        # 세우면 「누가 무엇을 했나」가 아니라 분류가 되어 그림이 안 읽힌다.
        elif ac.endswith(('구조', '제도', '배분', '밸류에이션', '잔액', '효과', '방식', '체계')):
            bad.append(('주체가 행위자가 아니다', '%s %s' % (i, ac)))
        lb = (n.get('label') or '').strip()
        if len(lb) > 24:
            bad.append(('마디 이름이 길다(24자 초과)', '%s %s' % (i, lb)))
        # 마디 이름은 단어로 끝낸다 — 상자 안에 문장을 넣으면 눈이 읽느라 그림을 못 본다
        if lb and (lb[-1] in '?!.,' or lb.endswith(('다', '까', '나', '냐', '지', '요',
                                                    '음', '함', '됨', '임'))):
            bad.append(('마디 이름이 단어로 안 끝난다', '%s %s' % (i, lb)))
    # 편마다 통합 흐름도로 올려보내는 마디가 있어야 두 겹이 이어진다.
    # **사슬마다** 센다 — 한 글을 두 사슬이 같이 인용하면 합계로 세면 안 된다.
    lifted = {}
    for n in nodes:
        if n.get('src'):
            key = (n['id'].split(':')[0], n['src'])
            lifted.setdefault(key, 0)
            lifted[key] += 1 if n.get('lift') else 0
    for (thread, src), k in lifted.items():
        if k == 0:
            bad.append(('통합 흐름도로 올릴 마디(lift)가 없다', '%s %s' % (thread, src)))
        elif k > 2:
            bad.append(('한 편에서 올린 마디가 셋 이상이다', '%s %s %d개' % (thread, src, k)))
    for e in edges:
        for k in ('from', 'to'):
            if e.get(k) not in ids:
                bad.append(('화살표가 없는 마디를 가리킨다', '%s→%s' % (e.get('from'), e.get('to'))))
        if e.get('kind') not in EDGES:
            bad.append(('화살표 종류 모름', str(e.get('kind'))))
        if not (e.get('why') or '').strip():
            bad.append(('화살표에 근거 문장 없음', '%s→%s' % (e.get('from'), e.get('to'))))
        a, b = ids.get(e.get('from')), ids.get(e.get('to'))
        if a and b and a['date'] > b['date']:
            bad.append(('화살표가 시간을 거스른다', '%s→%s' % (e['from'], e['to'])))
    return bad


if __name__ == '__main__':
    posts = load_posts()
    nodes, edges = load_flow()
    bad = check(nodes, edges, posts)
    print('마디 %d · 화살표 %d · 원문 %d편' % (len(nodes), len(edges), len(posts)))
    for why, what in bad:
        print('FAIL %s | %s' % (why, what))
    print('FAIL %d' % len(bad))
    raise SystemExit(1 if bad else 0)
