# -*- coding: utf-8 -*-
"""경량 색인 검사기 — `scratchpad/aie_index/*.md` 가 규격을 지켰나.

  PYTHONIOENCODING=utf-8 python scratchpad/check_aieidx.py

색인은 하이쿠가 만든다. 사실표와 달리 인용이 없어 사람이 눈으로 대조할 자리가 없고,
그래서 **꼴이라도 기계가 물어야 한다.** 실제로 시험 두 편에서 목록에 없는 태그(`설계`)가
한 번 새어 나왔다 — 규격에 적어 두는 것만으로는 안 막힌다.

무는 것
  I1 frontmatter 다섯 열쇠(vid·speaker·org·tags·numbers·demo)가 다 있나
  I2 vid 가 파일 이름과 같나
  I3 tags 가 열두 낱말 안에 있나, 하나에서 셋인가
  I4 numbers·demo 가 있음/없음 둘 중 하나인가
  I5 절 셋(무엇을 다루나·값·이 편이 쓸모 있어 보이는 자리)이 다 있나
  I6 「무엇을 다루나」가 세 줄인가
  I7 영어 인용이 새어 들어왔나 — 따옴표에 든 영문 여덟 낱말 이상
  I8 판단어가 들어갔나 — 중요하다·인상적·놀랍다·뛰어나다·훌륭
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'scratchpad', 'aie_index')

TAGS = {'에이전트', '평가', '인프라', '코드', '검색·기억', '음성·영상',
        '학습', '제품·조직', '데이터', '보안', '버티컬', '기타'}
KEYS = ['vid', 'speaker', 'org', 'tags', 'numbers', 'demo']
SECS = ['## 무엇을 다루나', '## 값', '## 이 편이 쓸모 있어 보이는 자리']
JUDGE = re.compile(r'중요하다|중요한 자리|인상적|놀랍|뛰어나|훌륭|대단')
QUOTE = re.compile(r'["“”]([A-Za-z][^"“”]{40,})["“”]')


def check(path):
    name = os.path.basename(path)[:-3]
    s = io.open(path, encoding='utf-8').read()
    out = []
    m = re.match(r'---\n(.*?)\n---\n(.*)$', s, re.S)
    if not m:
        return ['I1 frontmatter 가 없다']
    head, body = m.group(1), m.group(2)
    meta = {}
    for line in head.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    for k in KEYS:
        if k not in meta:
            out.append('I1 열쇠 %s 가 없다' % k)
    if meta.get('vid') != name:
        out.append('I2 vid 가 파일 이름과 다르다: %s' % meta.get('vid'))
    tags = [t.strip() for t in meta.get('tags', '').split(',') if t.strip()]
    if not 1 <= len(tags) <= 3:
        out.append('I3 태그가 %d 개다' % len(tags))
    for t in tags:
        if t not in TAGS:
            out.append('I3 목록에 없는 태그: %s' % t)
    for k in ('numbers', 'demo'):
        if meta.get(k) not in ('있음', '없음'):
            out.append('I4 %s 가 있음/없음이 아니다: %s' % (k, meta.get(k)))
    for sec in SECS:
        if sec not in body:
            out.append('I5 절이 없다: %s' % sec)
    if SECS[0] in body and SECS[1] in body:
        seg = body.split(SECS[0])[1].split(SECS[1])[0]
        lines = [l for l in seg.strip().split('\n') if l.strip()]
        if len(lines) != 3:
            out.append('I6 「무엇을 다루나」가 %d 줄이다' % len(lines))
    q = QUOTE.search(body)
    if q:
        out.append('I7 영어 인용이 들어갔다: %s…' % q.group(1)[:40])
    for j in JUDGE.finditer(body):
        tail = body[j.end():j.end() + 20]
        if re.search(r'말한다|밝힌다|짚는다|한다고', tail):
            continue  # 발표자에게 돌린 자리는 색인의 판단이 아니다
        out.append('I8 판단어: %s' % j.group(0))
    return out


def main():
    if not os.path.isdir(DIR):
        print('색인 폴더가 없다'); return
    files = sorted(f for f in os.listdir(DIR) if f.endswith('.md'))
    bad = 0
    for f in files:
        errs = check(os.path.join(DIR, f))
        if errs:
            bad += 1
            for e in errs:
                print('FAIL %-14s %s' % (f[:-3], e))
    print('요약: 색인 %d장 / FAIL %d장' % (len(files), bad))


if __name__ == '__main__':
    main()
