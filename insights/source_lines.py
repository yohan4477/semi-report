# -*- coding: utf-8 -*-
"""원문 하나에서 줄을 뽑는다. 갈래별 차이가 전부 여기 있다.

색인 주소는 갈래와 무관하게 `경로#L123` 하나다. 「123번째 줄」이 무엇인지만
갈래마다 다르다.

  .md    파일의 물리 줄 그대로
  .json  메르 클리핑. 본문이 text 문자열 하나에 들어 있어 물리 줄이 14개뿐이고
         그 안에 105줄이 escape 로 접혀 있다. text 를 펴서 그 줄을 쓴다

이 파일이 서기 전에는 줄을 읽는 코드가 gen_index·gen_times·q·check_index 넷에
흩어져 있었다. 넷 다 「파일을 열어 한 줄씩」을 가정했고 메르에서 그 가정이 깨진다.
한 곳만 고치면 나머지 셋이 조용히 어긋나므로 모았다.
"""
import io
import json
import os

MARKDOWN = '.md'
CLIPPING = '.json'


def known(rel):
    return os.path.splitext(rel)[1].lower() in (MARKDOWN, CLIPPING)


def _full(root, rel):
    return os.path.join(root, rel.replace('/', os.sep))


def lines(root, rel):
    path = _full(root, rel)
    if not os.path.isfile(path):
        return []
    if os.path.splitext(rel)[1].lower() == CLIPPING:
        try:
            with io.open(path, encoding='utf-8') as f:
                body = json.load(f).get('text') or ''
        except (ValueError, AttributeError):
            return []
        return body.split('\n') if body else []
    with io.open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    if not text:
        return []
    out = text.split('\n')
    if out and out[-1] == '':
        out.pop()
    return out


def count(root, rel):
    return len(lines(root, rel))


def line_at(root, rel, n):
    got = lines(root, rel)
    if n < 1 or n > len(got):
        return ''
    return got[n - 1].strip()
