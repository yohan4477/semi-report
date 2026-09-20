# -*- coding: utf-8 -*-
"""엔그램(N-gram 임베딩) 애니메이션이 쓸 값을 굽는다.

어텐션·FFN 과 사정이 다르다. 그쪽은 모델을 돌려 실제 값을 뽑았는데, 엔그램 층을 가진
모델(DeepSeek-V4.1-Flash·LongCat·Qwen3.8-Flash-Next)은 여기서 돌릴 수 있는 크기가
아니다. 그래서 둘로 갈라 굽는다.

  ① 재현할 수 있는 것 — 토큰 ID 와 해시로 나오는 행 번호. 문장을 실제 토크나이저로
     자르고, 뉴스레터가 적은 방식(접미사 n-gram 을 곱셈 해싱하고 XOR 로 섞는다)을
     그대로 구현해 행 번호를 낸다. 여기 나오는 숫자는 이 파일을 돌리면 그대로 다시 나온다.
  ② 원문에서 가져오는 것 — 표 크기·토큰당 읽는 양·조회 개수. 출처는
     content/newsletter/ai_infra/memory/[260918] Engram … 변환본이고, 그 값을 그대로 적는다.

②를 ①처럼 보이게 하면 안 된다. 화면과 캡션이 어느 쪽인지 밝히고, from 필드에 출처를
같이 적어 둔다.
"""
import io, os, sys, json

OUT = os.path.join('data', 'ngram_trace.json')
ATTN = os.path.join('data', 'attn_trace.json')
MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
TABLE_ROWS = 1 << 20      # 설명용 표 크기. 행 번호가 이 안으로 떨어진다
N_BI, N_TRI = 8, 8        # 큐원이 쓰는 개수 — 바이그램 8 · 트라이그램 8 (원문)
SHOW_ROWS = 40            # 표를 몇 칸으로 그려 보일까

# 원문에서 그대로 가져오는 값. 계산해 낸 것이 아니라는 표시로 따로 담는다.
FROM_SOURCE = {
    'ref': 'content/newsletter/ai_infra/memory/[260918] Engram 임베딩과 DRAM·SSD 오프로딩 공동설계.md',
    'deepseek_table_params': '196.6B',
    'deepseek_table_gib': 188.8,
    'deepseek_rows_per_layer': 24,
    'deepseek_kib_per_token': 12.4,
    'deepseek_kib_per_gpu': 3.1,
    'qwen_table_params': '51.2B',
    'qwen_rows_per_token': 16,
    'qwen_kib_per_token': 5,
}


def mix(h):
    """곱셈 해싱 + XOR 섞기. 원문이 적은 방식을 그대로 옮긴 것이다."""
    h = (h * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 29
    h = (h * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    h ^= h >> 32
    return h


def row_of(ids, salt):
    h = mix(salt)
    for i in ids:
        h = mix(h ^ (i + 0x9E3779B9))
    return h % TABLE_ROWS


def validate(tr):
    assert len(tr['ids']) == len(tr['tokens']), '토큰과 ID 수가 같아야 한다'
    assert len(tr['lookups']) == N_BI + N_TRI, \
        '조회가 %d개여야 한다 (바이그램 %d · 트라이그램 %d)' % (N_BI + N_TRI, N_BI, N_TRI)
    for lk in tr['lookups']:
        assert 0 <= lk['row'] < tr['table_rows'], '행 번호가 표 밖이다'
        assert len(lk['ids']) in (2, 3), '접미사 n-gram 은 2~3 토큰이다'
    assert len(set(l['row'] for l in tr['lookups'])) >= 2, \
        '행 번호가 전부 같으면 해시가 안 도는 것이다'
    assert tr['from']['ref'], '원문에서 가져온 값의 출처가 비어 있다'
    return True


def build_trace():
    from transformers import AutoTokenizer
    at = json.load(io.open(ATTN, encoding='utf-8'))
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    ids = tok(at['sentence'])['input_ids']
    pos = at['query_pos']
    bi = ids[pos - 1:pos + 1]          # 접미사 2-gram
    tri = ids[pos - 2:pos + 1]         # 접미사 3-gram
    lookups = ([{'kind': 'bi', 'ids': bi, 'salt': k, 'row': row_of(bi, k)}
                for k in range(N_BI)]
               + [{'kind': 'tri', 'ids': tri, 'salt': k, 'row': row_of(tri, k)}
                  for k in range(N_TRI)])
    return {
        'model': MODEL_ID,
        'sentence': at['sentence'],
        'tokens': at['tokens'],
        'ids': ids,
        'query_pos': pos,
        'bi_ids': bi,
        'tri_ids': tri,
        'table_rows': TABLE_ROWS,
        'show_rows': SHOW_ROWS,
        'lookups': lookups,
        'hash_note': '곱셈 해싱 + XOR 섞기. 설명을 위해 원문이 적은 방식대로 구현한 것이지 '
                     '그 모델이 쓰는 해시 그대로는 아니다.',
        'from': FROM_SOURCE,
    }


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    tr = build_trace()
    validate(tr)
    os.makedirs('data', exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(tr, ensure_ascii=False, indent=1))
    print('접미사 2-gram %s · 3-gram %s' % (tr['bi_ids'], tr['tri_ids']))
    print('조회 %d개 · 행 번호 앞 6개 %s'
          % (len(tr['lookups']), [l['row'] for l in tr['lookups'][:6]]))
