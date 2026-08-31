# -*- coding: utf-8 -*-
"""프레임 답이 원문 안에 있나 — 남의 모델이 준 틀을 재료로 쓰기 전에 거른다.

`insights/frames/*.md` 는 다른 모델(Gemini 등)에게 같은 원문을 주고 각도를 바꿔 받은
답이다. **재료가 아니라 프레임 후보**다. 2026-08-30 에 세 답을 손으로 재 봤더니 이랬다.

  전략 판   각주 셋이 원문에 없는 인용이었다(「Semi Doped 도 …지적한다」)
  기술 판   사양의 대부분이 원문 밖이었고, 해법과 네트워크는 원문과 **반대**였다
            (원문은 HBM 을 조각내 전담시키는 NUMA, 답은 분산 온칩 SRAM 에 KV 캐시 핀닝.
             원문은 Tomahawk 6 · ESUN 스케일업, 답은 PCIe Gen6 · RoCEv2 스케일아웃)

손으로 재는 데 시간이 다 갔다. 그 일을 여기서 한다.

  PYTHONIOENCODING=utf-8 python insights/check_frame.py
  PYTHONIOENCODING=utf-8 python insights/check_frame.py 할라페뇨    이름에 그 말이 든 것만

보는 것 둘이다.

  F1  프레임 답에 든 이름·수치가 원문에 있나       (없으면 목록으로 낸다. FAIL 아님)
  F2  원문에 없는 그 이름이 카드 화면에 들어갔나   (들어갔으면 FAIL — 미검증이 샜다)

F1 이 FAIL 이 아닌 이유는, 프레임 답은 원래 원문 밖 말을 하라고 시킨 것이기 때문이다.
막아야 하는 것은 그 말이 **표시 없이 카드로 새는 것**이고 그게 F2 다.
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8', line_buffering=True)
FRAME_DIR = os.path.join(paths.ROOT, 'insights', 'frames')
DASH_DIR = os.path.join(paths.ROOT, '대시보드')

# 뽑을 것 — 영문 고유명사·약어와 단위 붙은 수. 이 둘이 검증할 수 있는 주장이다
NAME = re.compile(r'\b[A-Z][A-Za-z0-9]{2,}(?:\s?[A-Z][A-Za-z0-9]+)?\b')
NUM = re.compile(r'\d[\d,\.]*\s*(?:W|nm|GB|Gb|TB|MB|%|배|억|조|달러|개월|년|시간)')
# 대조에서 뺄 말 — 이 저장소·틀 이야기라 원문에 있을 이유가 없다
SKIP_NAME = {
    'Gemini', 'Chrome', 'Semi', 'Doped', 'OpenAI', 'MECE', 'Executive', 'Summary',
    'BCG', 'McKinsey', 'Bain', 'Jalapeño', 'Impact', 'Map', 'Option', 'Core',
    'Thesis', 'Strategic', 'Intent', 'Industry', 'Implications', 'Risks',
}
TAGBLOCK = re.compile(r'<(script|style|svg)\b.*?</\1>', re.S | re.I)
TAG = re.compile(r'<[^>]+>')
# 받은 글을 그대로 실은 자리. 접힌 상자(details.fv)든 카드 본문 전체(div.fv-b)든
# 남의 글을 인용한 것이라 유출로 세지 않는다 — 2026-08-31 에 카드가 뷰 하나를
# 통째로 싣는 꼴로 바뀌면서 본문 전체가 인용이 됐다
QUOTE_BOX = re.compile(r'<details class="fv">.*?</details>'
                       r'|<div class="fv-b">.*?</div>\s*(?=<div class="uc-links"|\Z)', re.S)


def meta(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}, text
    out = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            out[k.strip()] = v.strip()
    return out, text[m.end():]


def claims(body):
    """검증할 수 있는 주장만 뽑는다 — 이름과 수."""
    out = []
    for m in NAME.finditer(body):
        s = m.group(0).strip()
        if s in SKIP_NAME or len(s) < 3:
            continue
        out.append(s)
    out += [re.sub(r'\s+', '', m.group(0)) for m in NUM.finditer(body)]
    seen, uniq = set(), []
    for c in out:
        if c.lower() not in seen:
            seen.add(c.lower())
            uniq.append(c)
    return uniq


def flat(s):
    return re.sub(r'[\s,]', '', s or '')


CARD = re.compile(r'<div class="ucard[^"]*"[^>]*>(.*?)(?=<div class="ucard|<footer|\Z)', re.S)


def cards_of(slug):
    """그 원문으로 만든 카드만 고른다.

    처음에는 대시보드 전체를 봤더니 「CUDA」가 알고리즘 계보에 있다는 이유로 FAIL 이
    났다. 그 카드는 이 원문과 아무 상관이 없다 — 미검증이 샜는지는 **그 원문으로 만든
    카드 안에서만** 물을 수 있다. 카드는 요약본 링크로 찾는다."""
    out = []
    for p in sorted(glob.glob(os.path.join(DASH_DIR, '*.html'))):
        raw = io.open(p, encoding='utf-8').read()
        if slug not in raw:
            continue
        for m in CARD.finditer(raw):
            block = m.group(0)
            # 메타에 「받은 그대로」가 붙은 카드는 앞면(요지·한줄)까지 다 인용이다.
            # 그런 카드를 유출로 세면 인용을 실을 수 없는 검사기가 된다(2026-08-31)
            if slug in block and '받은 그대로' in block:
                continue
            if slug in block:
                # 「받은 그대로」 상자는 남의 글을 인용한 자리다. 우리가 한 주장이 아니라
                # 유출로 세지 않는다 — 상자 머리에 미검증이라고 적혀 있다(2026-08-31)
                block = QUOTE_BOX.sub(' ', block)
                out.append((os.path.basename(p), flat(TAG.sub(' ', TAGBLOCK.sub(' ', block)))))
    return out


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ''
    files = sorted(glob.glob(os.path.join(FRAME_DIR, '*.md')))
    fails = missing = 0
    for p in files:
        name = os.path.basename(p)
        if want and want not in name:
            continue
        head, body = meta(io.open(p, encoding='utf-8').read())
        src = os.path.join(paths.ROOT, head.get('source', ''))
        if not head.get('source') or not os.path.exists(src):
            print('FAIL %s [F0] source 가 없거나 그 파일이 없다' % name, file=OUT)
            fails += 1
            continue
        srcflat = flat(io.open(src, encoding='utf-8').read())
        # used  카드가 실제로 가져다 쓴 것
        # named 카드가 「안 가져왔다」고 이름을 댄 것 — 언급은 새는 것이 아니다.
        #       2026-08-30 에 이 검사기가 제 몫을 했다. 「안 가져온 것」 목록에 적은
        #       550W·1.5~1.9배·RoCEv2 를 미검증 유출로 잡았다 — 규칙이 옳고 자리가 달랐다
        used = head.get('used', '') + ' ' + head.get('named', '')
        out_of_source = [c for c in claims(body) if flat(c) not in srcflat]
        missing += len(out_of_source)
        print('%s  %s · 원문 밖 %d개'
              % (name, head.get('kind', '?'), len(out_of_source)), file=OUT)
        if out_of_source:
            print('   F1 원문에 없다: %s' % ' · '.join(out_of_source[:24]), file=OUT)
        # F2 — 원문에 없는 말이 그 원문의 카드에 들어갔나
        slug = os.path.splitext(os.path.basename(head['source']))[0]
        dashes = cards_of(slug)
        if not dashes:
            print('   F2 아직 카드가 없다 — 새는지 볼 자리가 없다', file=OUT)
        for c in out_of_source:
            if len(flat(c)) < 4:
                continue          # 너무 짧은 토막은 우연히 걸린다
            for where, text in dashes:
                if flat(c) in text and flat(c) not in flat(used):
                    print('FAIL %s [F2] 원문에 없는 「%s」가 %s 의 그 카드에 들어갔다'
                          % (name, c, where), file=OUT)
                    fails += 1
    print('\n요약: 프레임 %d편 / FAIL %d / 원문 밖 주장 %d개'
          % (len(files), fails, missing), file=OUT)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
