# -*- coding: utf-8 -*-
"""AgentX 메모리 층의 원자료를 굳힌다 — 한 번 돌리는 스크립트.

입력: GitHub Actions 산출물 `bmk_agentic_*` 요약 파일(InferenceX, 실행 72개).
받는 법은 `gh api repos/SemiAnalysisAI/InferenceX/actions/runs/<run>/artifacts` 로
bmk_agentic 으로 시작하는 산출물을 받아 zip 안의 json 하나를 꺼낸다.

출력: insights/models/raw/agentx_memory.json. 값은 요약 파일 그대로 옮기고 고치지 않는다.
규격 표·파라미터 수는 아래 상수로 적었다 — 출처는 표마다 붙인다.

    PYTHONIOENCODING=utf-8 python scratchpad/build_agentx_memory_raw.py <bmk_rows.json>
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'insights', 'models', 'raw', 'agentx_memory.json')

C = 'input/clippings/'
N = 'content/newsletter/ai_infra/'
# (용량 GB, 대역폭 TB/s, CPU-GPU 연결, 연결 GB/s, 호스트 메모리, 인용)
SPEC = {
    'h100': [80, None, 'PCIe 5.0', 128, None,
             C + 'AMD vs NVIDIA Inference Benchmark Who Wins - Performance & Cost Per Million Tokens.md#L66 · '
             + C + 'InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590'],
    'h200': [144, 4.8, 'PCIe 5.0', 128, None,
             C + 'AMD vs NVIDIA Inference Benchmark Who Wins - Performance & Cost Per Million Tokens.md#L66 · '
             + C + 'Ultra-High Interactivity on NVIDIA GPUs - TileRT InferenceX.md#L111 (38.4TB/s ÷ 8)'],
    'b200': [180, 8, 'PCIe 5.0', 128, None,
             C + 'AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65 (2025-06-13, 180GB) · '
             + C + 'InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590 (2026-02-16, 192GB) · '
             + C + 'InferenceMAX™ Open Source Inference Benchmarking.md#L528'],
    'b300': [288, 8, 'PCIe 6.0', 256, None,
             C + 'Long Live the Short King Why 4-hi HBM Wins.md#L30 · '
             + C + 'AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65 · '
             + C + 'InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590'],
    'gb200': [192, 8, 'NVLink-C2C', 900, 'Grace LPDDR5X 480GB',
              N + 'memory/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md#L448 · '
              + C + 'CPUs are Back The Datacenter CPU Landscape in 2026.md#L314'],
    'gb300': [288, 8, 'NVLink-C2C', 900, 'Grace LPDDR5X 480GB',
              N + 'compute/[251128] TPUv7 - 구글, AI 반도체 왕좌에 도전장을 내밀다.md#L195 · '
              + C + 'CPUs are Back The Datacenter CPU Landscape in 2026.md#L314'],
    'vr200': [288, 22, 'NVLink-C2C', 1800, 'Vera LPDDR5X 1.5TB',
              N + 'compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md#L104·L137 · '
              + N + 'compute/[260209] CPU가 돌아왔다 - 2026년 데이터센터 CPU 판도.md#L503'],
    'mi355x': [288, 8, None, None, None,
               C + 'AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65 · '
               + C + 'InferenceMAX™ Open Source Inference Benchmarking.md#L528'],
}

# 전체 파라미터 수(십억). HF safetensors 메타데이터 total, 2026-09-17 읽음
PARAMS = {
    'dsv4': [1598.8, 'https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro'],
    'dsv41flash': [763.2, 'https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash'],
    'glm5.2': [753.3, 'https://huggingface.co/zai-org/GLM-5.2'],
    'kimik3': [2779.9, 'https://huggingface.co/moonshotai/Kimi-K3'],
    'minimaxm3': [427.0, 'https://huggingface.co/MiniMaxAI/MiniMax-M3'],
    'qwen3.5': [403.4, 'https://huggingface.co/Qwen/Qwen3.5-397B-A17B'],
    'qwen3.8next': [180.0, 'https://huggingface.co/Qwen/Qwen3.8-Flash-Next'],
}


def g(d, *path):
    for p in path:
        if not isinstance(d, dict):
            return None
        d = d.get(p)
    return d


def row(d):
    rm, sm = d.get('request_metrics') or {}, d.get('server_metrics') or {}
    lat = rm.get('latency') or {}
    return {
        'model': d.get('infmax_model_prefix'), 'hw': (d.get('hw') or '').replace('cluster:', ''),
        'framework': d.get('framework'), 'precision': d.get('precision'),
        'offload': d.get('kv_offloading'), 'backend': g(d, 'kv_offload_backend', 'name'),
        'tp': d.get('tp'), 'ep': d.get('ep'), 'dp_attention': str(d.get('dp_attention')).lower(),
        'multinode': str(d.get('is_multinode')).lower(), 'disagg': str(d.get('disagg')).lower(),
        'conc': d.get('conc'), 'run': d.get('_run'), 'image': d.get('image'),
        'dram_gb': d.get('allocated_cpu_dram_gb'), 'avg_power_w': d.get('avg_power_w'),
        'tput_per_gpu': g(rm, 'throughput', 'per_gpu', 'total_tput_tps'),
        'input_per_gpu': g(rm, 'throughput', 'per_gpu', 'input_tput_tps'),
        'output_per_gpu': g(rm, 'throughput', 'per_gpu', 'output_tput_tps'),
        'p90_intvty': g(lat, 'intvty', 'p90'), 'p90_ttft': g(lat, 'ttft', 'p90'),
        'gpu_usage': g(sm, 'kv_cache', 'gpu_usage_pct'), 'gpu_tokens': g(sm, 'kv_cache', 'gpu_total_tokens'),
        'cpu_used_tokens': g(sm, 'kv_cache', 'cpu_used_tokens'), 'cpu_tokens': g(sm, 'kv_cache', 'cpu_total_tokens'),
        'hit_gpu': g(sm, 'cache', 'gpu_cache_hit_rate'), 'hit_ext': g(sm, 'cache', 'external_cache_hit_rate'),
        'prompt_total': g(sm, 'tokens', 'prompt_total'),
        'tok_gpu_hit': g(sm, 'tokens', 'prompt_by_source', 'gpu_cache_hit'),
        'tok_ext_hit': g(sm, 'tokens', 'prompt_by_source', 'cpu_or_external_cache_hit'),
        'tok_computed': g(sm, 'tokens', 'prompt_by_source', 'computed'),
    }


def main(src):
    raw = json.loads(io.open(src, encoding='utf-8').read())
    rows = [row(d) for d in raw if isinstance(d, dict) and d.get('request_metrics')]
    rows = [r for r in rows if r['tput_per_gpu']]
    rows.sort(key=lambda r: (r['model'] or '', r['hw'], r['framework'] or '', r['offload'] or '',
                             str(r['tp']), r['conc'] or 0))
    out = {
        '_about': 'AgentX 메모리 층의 원자료. rows 는 InferenceX GitHub Actions 산출물 bmk_agentic 요약 파일을 칸만 골라 옮긴 것(값 안 고침).',
        '_읽는 법': 'hw 는 클러스터 이름(b200-nscale 등)이라 앞 토막이 칩이다. tok_* 는 서버가 출처별로 센 입력 토큰 수, gpu_usage 는 GPU KV 사용률 최댓값(0~1).',
        'sources': {
            'artifacts': {'title': 'InferenceX GitHub Actions bmk_agentic 산출물 (실행 72개)',
                          'publisher': 'SemiAnalysis InferenceX', 'url': 'https://github.com/SemiAnalysisAI/InferenceX/actions',
                          'published': '2026-08-03~2026-09-16', 'read_on': '2026-09-17'},
            'specs': {'title': 'SemiAnalysis 원문 — 시스템별 HBM·호스트 연결 규격',
                      'publisher': 'SemiAnalysis', 'url': 'scratchpad/agentx_spec_facts.md',
                      'published': '2025-06-13~2026-09-14', 'read_on': '2026-09-17'},
            'hf': {'title': 'Hugging Face 모델 카드 safetensors 메타데이터', 'publisher': 'Hugging Face',
                   'url': 'https://huggingface.co', 'published': '2026-09-17', 'read_on': '2026-09-17'},
        },
        'tables': [
            {'id': 'mem-spec', 'from': 'specs', 'read_on': '2026-09-17', 'redacted': [],
             'title': '칩별 HBM 용량·대역폭과 CPU-GPU 연결',
             'columns': ['hbm_gb', 'hbm_tb_s', 'link', 'link_gb_s', 'host_mem', 'cite'],
             'rows': SPEC},
            {'id': 'mem-params', 'from': 'hf', 'read_on': '2026-09-17', 'redacted': [],
             'title': '모델 전체 파라미터 수(십억)', 'columns': ['billion', 'url'], 'rows': PARAMS},
            {'id': 'mem-bytes', 'from': 'hf', 'read_on': '2026-09-17', 'redacted': [],
             'title': '정밀도별 파라미터당 바이트 — 블록 스케일 몫을 얹은 우리 가정',
             'columns': ['bytes'], 'rows': {'fp4': [0.53], 'fp8': [1.03], 'bf16': [2.0]}},
        ],
        'rows': rows,
    }
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    print('rows', len(rows), '->', OUT)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1])
