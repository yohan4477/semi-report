# -*- coding: utf-8 -*-
"""슬림 포인트가 자막 원문에 실제로 있는지 대조한다.

요약을 다시 요약하면서 근거가 흐려지는 걸 막으려고 둔 검사기다.
카드의 slim_* 텍스트에서 숫자와 따옴표 인용, 고유명사 후보를 뽑아
그 편 자막(scratchpad/yt_subs/<영상ID>.txt)에 나오는지 본다.

  py -3.13 scratchpad/check_slim.py            전체
  py -3.13 scratchpad/check_slim.py 용인        제목에 그 말이 든 카드만

자막은 자동 인식이라 표기가 흔들린다. 그래서 숫자는 자릿수만 맞으면 통과로 보고,
쉼표·공백·조사는 지운 뒤 비교한다. FAIL이 뜨면 사람이 그 줄을 직접 확인한다.
"""
import difflib, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scratchpad'))
import gen_realestate_dashboard as g

SUBS = os.path.join(ROOT, 'scratchpad', 'yt_subs')
STRIP = re.compile(r'<[^>]+>')
NUM = re.compile(r'\d[\d,\.]*')
# 자막에 그대로 나올 리 없는 우리 쪽 표기
SKIP_NUM = {'1', '2', '3', '4', '5', '10', '100'}


def norm(t):
    return re.sub(r'[\s,]', '', t)


# 전문용어는 쉬운 말로 바꾸지 않고 첫 등장에 괄호로 푼다(korean-readability 규칙).
# 슬림으로 줄이면서 이 괄호가 빠지는 일이 잦아 여기서 잡는다
GLOSS_TERMS = [
    '정주 인구', '용적률', '연담화', '도정법', '도시정비법', '장특공제', '장기보유특별공제',
    '대항력', '최우선변제권', '토지거래허가', '감정평가', '공공기여', '재초환', 'PF', 'DSR',
    '구분등기', '공유지분', '필터링', 'PIR', '락인', 'OSC', '모듈러', '점용허가', '제척기간',
    '자금조달계획서', '일몰제', '도급계약', '산출내역서', '유치권', '매수청구', '완충녹지',
    '부담부 증여', '차용증', '거래사례비교법', '분양가 상한제', '후분양', '인구집중유발시설',
    '공정시장가액비율', '공시가격 현실화율', '토지임대부', '전매제한', '지목', '과소필지',
]


def gloss_missing(card):
    """슬림 텍스트에 나온 전문용어 중 괄호 설명이 안 붙은 것"""
    body = ' '.join([card.get('slim_oneliner', '')] + list(card['slim_points']))
    body = STRIP.sub('', body)
    out = []
    for t in GLOSS_TERMS:
        i = body.find(t)
        if i < 0:
            continue
        tail = body[i + len(t):i + len(t) + 60]
        if tail.lstrip().startswith('(') or '(' in body[max(0, i - 30):i]:
            continue
        out.append(t)
    return out


def best_ratio(q, sub):
    """자막에서 이 인용과 가장 비슷한 대목의 유사도. 창을 겹쳐 훑는다"""
    best, step, win = 0.0, max(4, len(q) // 2), len(q) * 2
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(q)
    for i in range(0, max(1, len(sub) - win), step):
        sm.set_seq1(sub[i:i + win])
        if sm.real_quick_ratio() <= best or sm.quick_ratio() <= best:
            continue
        best = max(best, sm.ratio())
    return best


def vid_of(card):
    for _lab, url, _cls in card['links']:
        if 'youtu' in url:
            return url.rsplit('/', 1)[-1]
    return None


def check(card):
    vid = vid_of(card)
    path = os.path.join(SUBS, (vid or '') + '.txt')
    if not vid or not os.path.exists(path):
        return ['자막 없음(%s) — 대조 못 함' % vid], []
    sub = norm(io.open(path, encoding='utf-8').read())
    bad, warn = [], []
    body = ' '.join([card.get('slim_oneliner', '')] + list(card['slim_points'])
                    + [v for v, _l in card.get('slim_stats', [])])
    body = STRIP.sub('', body)
    # 숫자는 표기가 달라질 수 있다(3.4 ↔ 3억 4천, 130~140 ↔ 130, 140). 사람이 볼 경고로만 둔다
    for n in set(NUM.findall(body)):
        if n in SKIP_NUM or len(n.replace(',', '').replace('.', '')) < 2:
            continue
        if norm(n) in sub or norm(n.split('.')[0]) in sub:
            continue
        warn.append('숫자 "%s" 는 자막에서 그대로 못 찾음(표기 차이일 수 있음)' % n)
    # 따옴표는 화자가 한 말로 읽힌다. 다만 자동 자막은 오인식이 많아 완전 일치를 요구할 수 없다.
    # 그래서 가장 비슷한 대목과의 유사도로 본다 — 많이 다르면 우리가 지어낸 문장일 가능성이 크다
    quotes = []
    for item in [card.get('slim_oneliner', '')] + list(card['slim_points']):
        item = STRIP.sub('', item)
        if item.count('"') % 2:      # 짝이 안 맞으면 따옴표 범위를 믿을 수 없다
            continue
        quotes += re.findall(r'"([^"]{6,60})"', item)
    for q in quotes:
        nq = norm(q)
        if nq in sub:
            continue
        r = best_ratio(nq, sub)
        if r < 0.55:
            bad.append('인용 "%s" 가 자막에 없다(유사도 %.2f)' % (q[:40], r))
        elif r < 0.8:
            warn.append('인용 "%s" 가 자막과 조금 다르다(유사도 %.2f)' % (q[:40], r))
    return bad, warn


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    fails = 0
    for c in g.CARDS:
        if not c.get('slim_points'):
            continue
        if want and want not in c['title']:
            continue
        bad, warn = check(c)
        miss = gloss_missing(c)
        if miss:
            warn.append('괄호 설명이 없는 용어: ' + ', '.join(miss))
        mark = 'FAIL' if bad else ('warn' if warn else 'OK  ')
        print('%s %s' % (mark, c['title']))
        for b in bad:
            print('       ! %s' % b)
        for w in warn:
            print('       ~ %s' % w)
        fails += bool(bad)
    print('\nFAIL %d건 (! = 고쳐야 함, ~ = 사람이 확인)' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
