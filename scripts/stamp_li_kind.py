#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""소셜 신호 히스토리의 각 행에 「무슨 글인가」 라벨을 붙인다.
밈·행사·채용·팟캐스트·뉴스레터 홍보를 실질 신호와 같은 무게로 늘어놓으면 걸러 읽을 수
없다. 라벨은 insights/li_signal.classify 가 정하므로 content/linkedin 의 kind 와 항상 같다.
「자체 발화」(실질 신호)에는 아무것도 붙이지 않는다 — 라벨이 붙은 줄이 건너뛸 줄이다.

라벨은 <a class="rowmain"> **뒤에** 넣고 CSS order 로 앞에 그린다. 앞에 넣으면
gen_bmirror.py 의 행 정규식(`<div class="row"><a class="rowmain"`)이 깨진다.

사용: PYTHONIOENCODING=utf-8 python scripts/stamp_li_kind.py
linkedin-update 로 히스토리에 새 글을 넣은 뒤 다시 돌리면 된다(여러 번 돌려도 같다).
"""
import io, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'insights'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import li_signal as ls

HIST = os.path.join('대시보드', '소셜 신호 히스토리.html')

# 라벨은 카드 첫머리의 표지로만 붙인다. li_signal 의 배제 정규식을 그대로 쓰면 안 된다 —
# 그쪽은 인용 자격을 가리려고 넓게 걸어 둔 것이라, 「구독자에게 답을 줬다」가 행사로,
# 「이번 주 팟캐스트에 나온다」가 팟캐스트로 잡혀 실질 신호에 건너뛰라는 딱지가 붙는다.
# 실제로 그렇게 붙여 봤더니 채용 33장·행사 13장·회고 13장 중 상당수가 오라벨이었다.
# 뉴스레터·재홍보만 li_signal 판정을 쓴다 — 그건 링크와 발행일로 갈리므로 틀리지 않는다.
MEME = re.compile(r'^밈|^밈\s*[—:·]|풍자 글이다|농담이다|한 줄짜리 농담|밈이다|밈성')
HIRE = re.compile(r'채용 공고|채용한다는|모집한다는|뽑는다는 공고|채용한다고')
CAST = re.compile(r'^팟캐스트|^주간 팟캐스트|^SemiAnalysis Weekly|^위클리 팟캐스트'
                  r'|^SemiAnalysis 주간 팟캐스트')
NEWS = {'신규 발행 알림', '뉴스레터 링크(발행일 미상)'}
CSS = ('.row > .kind{order:-1; flex:none; font-size:.68rem; font-weight:700; letter-spacing:.02em;'
       ' color:var(--sub); border:1px solid var(--line); border-radius:5px; padding:1px 6px;'
       ' margin-top:2px; white-space:nowrap;}')
ROW = re.compile(r'(<div class="row"><a class="rowmain" href="([^"]+)".*?</a>)(.*?)(</div>)', re.S)


def label(text, kind):
    if kind == '재홍보':
        return '재홍보'
    if kind in NEWS:
        return '뉴스레터'
    if MEME.search(text):
        return '밈'
    if HIRE.search(text):
        return '채용'
    if CAST.search(text):
        return '팟캐스트'
    return None


def main():
    s = io.open(HIST, encoding='utf-8').read()
    pub = ls.publish_dates()
    n = {}

    def one(m):
        head, href, tail, close = m.groups()
        tail = re.sub(r'<span class="kind">[^<]*</span>', '', tail)
        aid = re.search(r'activity:(\d+)', href)
        if aid:
            text = ls.clean(re.search(r'<span class="sn">(.*?)</span>', head, re.S).group(1))
            nl = re.search(r'newsletter\.semianalysis\.com/p/([a-z0-9-]+)', head + tail)
            kind = ls.classify(text, nl.group(1) if nl else None,
                               ls.urn_date(aid.group(1)), pub)[0]
            lab = label(text, kind)
            if lab:
                n[lab] = n.get(lab, 0) + 1
                # 행 **끝**에 붙인다. </a> 바로 뒤에 넣으면 gen_li_source 가 링크를
                # 찾는 고정 창(seg[:2000])이 밀려 뉴스레터 slug 가 잘린다.
                tail = tail + '<span class="kind">%s</span>' % lab
        return head + tail + close

    s = ROW.sub(one, s)
    if '.row > .kind{' not in s:
        s = s.replace('.row > .relb{', CSS + chr(10) + '.row > .relb{', 1)
    io.open(HIST, 'w', encoding='utf-8').write(s)
    print('라벨 %d개 · %s' % (sum(n.values()), ' '.join('%s %d' % kv for kv in sorted(n.items()))))


if __name__ == '__main__':
    main()
