# -*- coding: utf-8 -*-
"""FFN 애니메이션이 쓸 실제 값을 모델에서 한 번 뽑아 굽는다.

어텐션 쪽(attn_trace.py)과 같은 원칙이다 — 브라우저에서 모델을 돌리지 않고, 화면에
뜨는 숫자는 전부 이 파일이 낸 JSON 에 있어야 한다.

무엇을 재나. Qwen2 의 FFN 은 SwiGLU 다 — 같은 입력을 게이트·업 두 갈래로 넓히고,
게이트 쪽에 SiLU 를 먹여 업 쪽과 곱한 뒤, 다시 원래 폭으로 접는다. 그래서 「넓혔다
접는다」와 「대부분이 눌리고 일부만 산다」 둘을 같이 보일 수 있다.

validate() 가 마지막에 한 가지를 못 박는다 — 여기서 직접 계산한 결과가 모델이 낸
MLP 출력과 같아야 한다. 그 단언이 통과해야 화면이 참이 된다.
"""
import io, os, sys, json

OUT = os.path.join('data', 'ffn_trace.json')
ATTN = os.path.join('data', 'attn_trace.json')
MODEL_ID = 'Qwen/Qwen2.5-0.5B-Instruct'
SHOW = 64          # 화면에 보일 칸 수. 넓은 층에서 이만큼만 골라 보인다
TOPN = 6           # 가장 세게 켜진 자리 몇 개를 따로 적는다
PREVIEW = 8


def validate(tr):
    assert tr['d_model'] > 0 and tr['d_ff'] > tr['d_model'], \
        'FFN 은 원래 폭보다 넓혀야 한다 (%d → %d)' % (tr['d_model'], tr['d_ff'])
    assert len(tr['show_idx']) == SHOW, '보일 칸이 %d개여야 한다' % SHOW
    assert len(tr['act_show']) == SHOW, '보일 칸의 값도 같은 수여야 한다'
    assert len(tr['in_preview']) == PREVIEW and len(tr['out_preview']) == PREVIEW, \
        '입력·출력 미리보기가 %d개여야 한다' % PREVIEW
    assert len(tr['top']) == TOPN, '가장 센 자리가 %d개여야 한다' % TOPN
    assert 0.0 < tr['quiet_share'] < 1.0, '잠잠한 자리 비율이 0과 1 사이여야 한다'
    assert tr['max_err'] < 1e-4, \
        '여기서 계산한 FFN 출력이 모델 것과 다르다 (최대 %.2e)' % tr['max_err']
    return True


def build_trace():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    at = json.load(io.open(ATTN, encoding='utf-8'))
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32, attn_implementation='eager')
    model.eval()

    enc = tok(at['sentence'], return_tensors='pt')
    layer = at['layer']
    pos = at['query_pos']
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
        # 그 층의 FFN 입력 — 어텐션을 더한 뒤 정규화한 것이다
        hs_next = out.hidden_states[layer + 1][0]      # 그 층을 지난 결과
        blk = model.model.layers[layer]
        x = blk.post_attention_layernorm(hs_next)[pos]
        mlp = blk.mlp
        gate = mlp.gate_proj(x)
        up = mlp.up_proj(x)
        act = torch.nn.functional.silu(gate) * up      # 살아남은 신호
        y = mlp.down_proj(act)
        ref = mlp(x.unsqueeze(0))[0]                   # 모델이 직접 낸 것
        err = float((y - ref).abs().max())

    d_ff = int(act.shape[0])
    d_model = int(x.shape[0])
    mag = act.abs()
    thr = float(mag.max()) * 0.1                       # 최댓값의 10% 아래를 잠잠하다고 본다
    quiet = int((mag < thr).sum())
    step = d_ff // SHOW
    idx = [i * step for i in range(SHOW)]
    topv, topi = torch.topk(mag, TOPN)
    return {
        'model': MODEL_ID,
        'sentence': at['sentence'],
        'tokens': at['tokens'],
        'query_pos': pos,
        'layer': layer,
        'd_model': d_model,
        'd_ff': d_ff,
        'show': SHOW,
        'show_idx': idx,
        'act_show': [float(act[i]) for i in idx],
        'act_max': float(mag.max()),
        'quiet_thr': thr,
        'quiet_share': quiet / float(d_ff),
        'top': [{'i': int(topi[k]), 'v': float(act[int(topi[k])])} for k in range(TOPN)],
        'in_preview': [float(v) for v in x[:PREVIEW]],
        'out_preview': [float(v) for v in y[:PREVIEW]],
        'max_err': err,
        # 「왜 넓히나」를 말하려면 그 값이 얼마인지도 영수증이 있어야 한다.
        # config 에서 바로 세어 둔다 — 화면에 적는 숫자는 여기서만 가져온다.
        'params': {
            'n_layers': int(model.config.num_hidden_layers),
            'ffn_per_layer': 3 * d_model * int(model.config.intermediate_size),
            'attn_per_layer': (2 * d_model * d_model
                               + 2 * int(model.config.num_key_value_heads)
                               * (d_model // int(model.config.num_attention_heads)) * d_model),
            'ffn_share': 0.0,     # 아래에서 채운다
        },
    }


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    tr = build_trace()
    p = tr['params']
    p['ffn_share'] = p['ffn_per_layer'] / float(p['ffn_per_layer'] + p['attn_per_layer'])
    validate(tr)
    os.makedirs('data', exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(tr, ensure_ascii=False, indent=1))
    print('%d층 · %d → %d → %d · 잠잠한 자리 %.1f%% · 모델과의 차이 %.1e'
          % (tr['layer'], tr['d_model'], tr['d_ff'], tr['d_model'],
             tr['quiet_share'] * 100, tr['max_err']))
    print('층 안 가중치 — FFN {:,} · 어텐션 {:,} · FFN 몫 {:.0f}%'.format(
        p['ffn_per_layer'], p['attn_per_layer'], p['ffn_share'] * 100))
