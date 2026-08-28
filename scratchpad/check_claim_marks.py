# -*- coding: utf-8 -*-
"""보고서 층에서 「누가 한 말인가」와 「언제 것인가」가 문장까지 살아 넘어왔나.

각도 파일은 항목마다 성격(사실·추정·전망·가정·제안·계획·발언·개념)과 때를 단다.
보고서로 옮기면서 그 둘이 빠지면 저자 추정이 사실로 굳는다 — 각도 체계가 막으려던
바로 그 사고가 마지막 한 걸음에서 난다. 문장 단위로 센다.

  PYTHONIOENCODING=utf-8 python scratchpad/check_claim_marks.py sec-fund
"""
import os
if not os.path.exists('대시보드/통합 보고서.html'):
    raise SystemExit('건너뜀 — 통합 보고서 화면이 없다. 생성기를 돌리면 다시 생긴다')
import io
import re
import sys

SRC = re.compile(r'추정|전망|봅니다|보입니다|제안|가정|계획|밝혔|말했|따르면|것으로 |라는 것이')
WHEN = re.compile(r'20\d\d년|20\d\d-\d\d|\d분기|[1-4]Q|올해|지금|현재|말까지|미래|앞으로')
NUM = re.compile(r'\d')


def main(sec):
    h = io.open('대시보드/통합 보고서.html', encoding='utf-8').read()
    i = h.index('id="%s"' % sec)
    seg = re.sub(r'<[^>]+>', '', h[i:h.index('</section>', i)])
    sents = [s.strip() for s in re.split(r'(?<=다)\.\s+|\n', seg) if len(s.strip()) > 25]
    claim = [s for s in sents if NUM.search(s)]
    no_src = [s for s in claim if not SRC.search(s)]
    no_when = [s for s in claim if not WHEN.search(s)]
    print('%s · 문장 %d · 수를 든 문장 %d' % (sec, len(sents), len(claim)))
    print('  말한 주체가 안 붙은 문장 %d' % len(no_src))
    print('  때가 안 붙은 문장 %d' % len(no_when))
    for s in no_when[:6]:
        print('    때 없음 —', s[:78])
    for s in no_src[:6]:
        print('    주체 없음 —', s[:78])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'sec-fund')
