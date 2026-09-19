# -*- coding: utf-8 -*-
"""어텐션 애니메이션이 쓸 실제 값을 모델에서 한 번 뽑아 굽는다.

브라우저에서 모델을 돌리지 않는다. 화면에 뜨는 숫자는 전부 이 파일이 낸 JSON 에 있어야
한다(도해 규칙 1 — 원문에 없는 값을 그리지 않는다). 그래서 굽는 자리와 그리는 자리를
갈라 두고, 그리는 쪽(gen_anim_page.py)은 이 JSON 말고 아무 데서도 숫자를 못 가져온다.
"""
import io, os, sys, json, math

OUT = os.path.join('data', 'attn_trace.json')
MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
SENTENCE = '사료를 열었는데 그것이 눅눅했다'
MAX_TOKENS = 12
PREVIEW = 8


def validate(tr):
    """구운 값이 그림이 기대하는 꼴인가. 어기면 굽기가 실패한다."""
    n = len(tr['tokens'])
    assert 2 <= n <= MAX_TOKENS, '토큰이 %d개다 — %d개를 넘으면 막대가 화면에 안 들어간다' % (n, MAX_TOKENS)
    assert 0 <= tr['noun_pos'] < tr['query_pos'] < n, '보는 자리가 앞 명사보다 뒤에 있어야 한다'
    m = tr['query_pos'] + 1
    assert len(tr['scores_raw']) == m, '점수 길이가 보는 자리까지여야 한다'
    assert len(tr['scores_softmax']) == m, '소프트맥스 길이가 점수와 같아야 한다'
    assert abs(sum(tr['scores_softmax']) - 1.0) < 1e-4, '소프트맥스 합이 1이 아니다'
    assert len(tr['q_preview']) == PREVIEW, 'Q 미리보기가 %d개여야 한다' % PREVIEW
    for row in tr['k_preview'] + tr['v_preview']:
        assert len(row) == PREVIEW, 'K·V 미리보기가 %d개여야 한다' % PREVIEW
    assert len(tr['k_preview']) == m and len(tr['v_preview']) == m, 'K·V 줄 수가 점수와 같아야 한다'
    assert len(tr['out_preview']) == PREVIEW, '출력 미리보기가 %d개여야 한다' % PREVIEW
    assert tr['picked_weight'] == max(tr['scores_softmax']), \
        '고른 헤드의 근거 값이 소프트맥스 최댓값과 달라선 안 된다'
    return True


def pick_head(attns, query_pos, noun_pos):
    """보는 자리가 앞 명사를 가장 세게 되짚는 (층, 헤드)를 고른다.

    층·헤드를 사람이 고르면 「그렇게 보이는 것만 골랐다」는 말을 듣는다. 기준을 코드에
    박아 두고 그 기준과 값을 JSON 에 같이 남긴다.
    """
    best = (-1, -1, -1.0)
    for li, a in enumerate(attns):                 # a: (1, heads, seq, seq)
        w = a[0, :, query_pos, noun_pos]           # 헤드마다 그 자리 → 명사 가중치
        for hi in range(w.shape[0]):
            v = float(w[hi])
            if v > best[2]:
                best = (li, hi, v)
    return best


def build_trace():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32, attn_implementation='eager')
    model.eval()

    enc = tok(SENTENCE, return_tensors='pt')
    ids = enc['input_ids'][0]
    tokens = [tok.decode([int(i)]) for i in ids]
    assert len(tokens) <= MAX_TOKENS, \
        '토큰이 %d개다 — SENTENCE 를 줄여 다시 뽑는다: %s' % (len(tokens), tokens)

    # 보는 자리와 되짚을 앞 명사. 문장을 바꾸면 이 두 줄을 같이 고친다.
    query_pos = max(i for i, t in enumerate(tokens) if '그것' in t)
    noun_pos = max(i for i, t in enumerate(tokens[:query_pos]) if '료' in t or '사' in t)

    with torch.no_grad():
        out = model(**enc, output_attentions=True, output_hidden_states=True)
    layer, head, picked = pick_head(out.attentions, query_pos, noun_pos)

    # 그 층·헤드의 Q·K·V 를 직접 다시 만든다. 어텐션 가중치만으로는 Q·K 를 못 보인다.
    hs = out.hidden_states[layer][0]               # (seq, hidden)
    attn = model.model.layers[layer].self_attn
    ln = model.model.layers[layer].input_layernorm
    x = ln(hs)
    n_heads = model.config.num_attention_heads
    n_kv = getattr(model.config, 'num_key_value_heads', n_heads)
    dim = model.config.hidden_size // n_heads
    kv_head = head // (n_heads // n_kv)            # GQA — 여러 Q 헤드가 K·V 하나를 나눠 쓴다

    q = attn.q_proj(x).view(-1, n_heads, dim)[:, head, :]
    k = attn.k_proj(x).view(-1, n_kv, dim)[:, kv_head, :]
    v = attn.v_proj(x).view(-1, n_kv, dim)[:, kv_head, :]

    m = query_pos + 1
    raw = [float(torch.dot(q[query_pos], k[j]) / math.sqrt(dim)) for j in range(m)]
    soft = [float(w) for w in out.attentions[layer][0, head, query_pos, :m]]
    soft = [w / sum(soft) for w in soft]           # 잘라 썼으니 합을 다시 1로
    outv = [sum(soft[j] * float(v[j][d]) for j in range(m)) for d in range(PREVIEW)]

    return {
        'model': MODEL_ID,
        'sentence': SENTENCE,
        'tokens': tokens,
        'query_pos': query_pos,
        'noun_pos': noun_pos,
        'layer': layer,
        'head': head,
        'picked_weight': max(soft),
        'picked_by': '보는 자리가 앞 명사 토큰에 준 가중치가 가장 큰 층·헤드',
        'dim': dim,
        'scores_raw': raw,
        'scores_softmax': soft,
        'q_preview': [float(x) for x in q[query_pos][:PREVIEW]],
        'k_preview': [[float(x) for x in k[j][:PREVIEW]] for j in range(m)],
        'v_preview': [[float(x) for x in v[j][:PREVIEW]] for j in range(m)],
        'out_preview': outv,
    }


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    tr = build_trace()
    validate(tr)
    os.makedirs('data', exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(tr, ensure_ascii=False, indent=1))
    print('토큰 %d개 · %d층 %d번 헤드 · 그 자리가 「%s」에 준 가중치 %.3f'
          % (len(tr['tokens']), tr['layer'], tr['head'],
             tr['tokens'][tr['noun_pos']], tr['picked_weight']))
