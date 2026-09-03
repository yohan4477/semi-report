# -*- coding: utf-8 -*-
"""Semi Doped 전략 판 — 『글과 도해 — 확정 규칙』 중 기계가 잴 수 있는 것을 아홉 편에 댄다.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/check_semidoped.py

글(insights/semidoped/*-strategy.md)과 화면(대시보드/semidoped/*.html)을 같이 본다.
gen_semidoped.py 가 끝에서 부르므로 FAIL 이 있으면 생성이 멈춘다. 규칙 번호는 문서 7절과 같다.

  G1 길이 5,500~6,500자(공백 포함, (L) 걷고)        G2 절 다섯~일곱, 마지막 절은 「말하지 않은 것」
  G3 여는 문단에 「(이하 진행자A)」, Vik 이 말하면 V 도  G4 「둘이다·셋이다」로 열고 ①이 없는 문단 (WARN)
  G5 영문 인용 — 따옴표 안이 영어                     G6 번역체 낱말 — 값이 움직·자리가 열리·몫·N 단
  G7 방법 이름 — MECE·프로세스·부분 나눔·대비 가 절 제목에  G8 frontmatter fixed · people 에 [[이름]]
  S1 화면에 (L줄) 남음 · 화자 상자 · 차례 · 15px       S2 도해 색 — 회색 아닌 색(채도 있는 hex)
  S3 도해가 절 머리(「N.」)에만 있고 문단 앞이 아님 (WARN) S4 글마다 도해 하나 이상
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANES = os.path.join(ROOT, 'insights', 'semidoped')
PAGES = os.path.join(ROOT, '대시보드', 'semidoped')
META = os.path.join(ROOT, 'content', 'understanding', 'Semi Doped')

BAD = [(r'값이 움직', '값이 움직인다'), (r'(자리|시장|수요|기회)[가이] 열리', '자리가 열린다'),
       (r'(?<![가-힣])몫', '몫'), (r'(아래|위|세|두|다섯|여러|그) 단(?=[ 을이에의로,.)])', '공급망 층을 「단」으로')]
METHOD = ['MECE', '프로세스', '부분 나눔', '대비', '밸류체인 분석', '인과 사슬']
GRAY_OK = re.compile(r'#(?:[0-9a-f]{3}|[0-9a-f]{6})\b', re.I)


def is_gray(hexs):
    h = hexs.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16)
    return max(r, g, b) - min(r, g, b) <= 40


def check(slug, out):
    lane = os.path.join(LANES, slug + '-strategy.md')
    page = os.path.join(PAGES, slug + '.html')
    meta = os.path.join(META, slug + '.md')
    s = io.open(lane, encoding='utf-8').read()
    fm, body = s.split('---', 2)[1], s.split('---', 2)[2]
    fail = lambda code, msg: out.append(('FAIL', slug, code, msg))
    warn = lambda code, msg: out.append(('WARN', slug, code, msg))

    n = len(re.sub(r'\(L[^)]*\)', '', body).strip())
    if not 5500 <= n <= 6500:
        fail('G1', '글자 %d — 5,500~6,500 밖' % n)
    secs = re.findall(r'^## (\d+)\. (.*)$', body, re.M)
    if not 5 <= len(secs) <= 7:
        fail('G2', '절 %d' % len(secs))
    if secs and '말하지 않은 것' not in secs[-1][1]:
        fail('G2', '마지막 절이 「말하지 않은 것」이 아니다: %s' % secs[-1][1][:30])
    lead = body.split('## 1.')[0]
    # 진행자가 한 사람인 회차가 있다(WEKA 편은 Vik 단독) — 그 진행자가 본문에 나올 때만 요구한다
    if re.search(r'Austin', body) and '(이하 진행자A)' not in lead:
        fail('G3', 'Austin 이 말하는데 여는 문단에 「(이하 진행자A)」가 없다')
    if re.search(r'\bVik\b', body) and '(이하 진행자V)' not in lead:
        fail('G3', 'Vik 이 말하는데 여는 문단에 「(이하 진행자V)」가 없다')
    for para in body.split('\n\n'):
        # 「이 셋이다」처럼 앞 문단의 ①②③을 되가리키는 것은 새 나열이 아니다
        if re.search(r'(?<!이 )(?<!그 )(둘|셋|넷|다섯|여섯)(이다|로 갈|로 나뉘|이 있다|을 들었다)\.', para) and '①' not in para:
            warn('G4', '「N이다」로 열고 ①이 없다: %s…' % para.strip()[:40])
    for q in re.findall(r'"([^"\n]{12,})"', body):
        if len(re.findall(r'[A-Za-z]', q)) > len(q) * 0.6:
            fail('G5', '영문 인용: "%s…"' % q[:40])
    for pat, name in BAD:
        for m in re.finditer(pat, body):
            fail('G6', '번역체 「%s」: …%s…' % (name, body[max(0, m.start() - 18):m.end() + 12].replace('\n', ' ')))
    for _, title in secs:
        for w in METHOD:
            if w in title:
                fail('G7', '절 제목에 방법 이름 「%s」: %s' % (w, title))
    if 'MECE' in body:
        fail('G7', '본문에 MECE')
    if not re.search(r'^fixed:', fm, re.M):
        fail('G8', 'frontmatter 에 fixed 가 없다 — 대조를 안 거쳤다')
    mm = io.open(meta, encoding='utf-8').read() if os.path.exists(meta) else ''
    if '[[' not in mm.split('---', 2)[1]:
        fail('G8', '회차 frontmatter people 에 [[이름]]이 없다')

    if not os.path.exists(page):
        fail('S1', '화면이 없다: %s' % page)
        return
    h = io.open(page, encoding='utf-8').read()
    if re.search(r'\(L\d', h):
        fail('S1', '화면에 (L줄) 이 남았다')
    for need, name in [('class="whobox"', '화자 상자'), ('>차례<', '차례'), ('class="pn', '이름 색'), ('font-size:15px', '본문 15px')]:
        if need not in h:
            fail('S1', '화면에 %s 가 없다' % name)
    figs = re.findall(r'<figure class="uc-fig".*?</figure>', h, re.S)
    if not figs:
        fail('S4', '도해가 없다')
    for f in figs:
        title = re.search(r'fig-title">([^<]*)<', f)
        for hx in set(GRAY_OK.findall(re.sub(r'<style.*?</style>', '', f, flags=re.S))):
            if not is_gray(hx):
                fail('S2', '도해 「%s」에 회색 아닌 색 %s' % (title.group(1) if title else '?', hx))
    return len(figs)


def main():
    out, nfig, slugs = [], 0, []
    for lane in sorted(glob.glob(os.path.join(LANES, '*-strategy.md'))):
        slug = os.path.basename(lane)[:-len('-strategy.md')]
        slugs.append(slug)
        nfig += check(slug, out) or 0
    # S3 — 도해 열쇠가 절 머리(「N.」)뿐인 것
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import semidoped_figs
    for (slug, lane), figs in semidoped_figs.FIGS.items():
        for key, title, _svg, _cap in figs:
            if '|' not in key:
                out.append(('WARN', slug, 'S3', '도해 「%s」가 절 머리에 있다 — 문단 앞으로' % title))
    for lv, slug, code, msg in out:
        print('%s %s [%s] %s' % (lv, slug[:16], code, msg))
    nf = sum(1 for o in out if o[0] == 'FAIL')
    nw = sum(1 for o in out if o[0] == 'WARN')
    print('요약: 글 %d편 / 도해 %d장 / FAIL %d / WARN %d' % (len(slugs), nfig, nf, nw))
    return nf


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
