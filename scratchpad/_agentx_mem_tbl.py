# -*- coding: utf-8 -*-
"""AgentX 메모리 층의 표와 도해 재료. 셈은 insights/models/check_agentx_memory.py 와 같은
상수·함수로 한다 — 표와 검사기가 다른 길로 셈하면 한쪽만 고쳐진다.
"""
import collections
import os
import statistics
import sys

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'insights', 'models')
if _MODELS not in sys.path:
    sys.path.insert(0, _MODELS)
import agentx_memory as AM                                       # noqa: E402
import check_agentx_memory as CM                                 # noqa: E402

NAME = {'dsv4': 'DeepSeek V4 Pro', 'dsv41flash': 'DeepSeek V4.1 Flash', 'glm5.2': 'GLM-5.2',
        'kimik3': 'Kimi K3', 'minimaxm3': 'MiniMax M3', 'qwen3.5': 'Qwen3.5',
        'qwen3.8next': 'Qwen3.8 Flash Next'}
CHIP = {'h100': 'H100', 'h200': 'H200', 'b200': 'B200', 'b300': 'B300', 'gb200': 'GB200 NVL72',
        'gb300': 'GB300 NVL72', 'vr200': 'Vera Rubin NVL72', 'mi355x': 'MI355X'}
OFF = {'none': '끔', 'dram': 'DRAM', 'nvme': 'SSD', 'dram+nvme': 'DRAM+SSD'}


def tier_sweep():
    """DSv4 B200 SGLang 동시성 스윕 — 입력 토큰 출처."""
    rs = sorted([r for r in CM.ROWS if r['model'] == 'dsv4' and r['hw'] == 'b200-nscale'
                 and r['framework'] == 'sglang' and AM.tier_shares(r)], key=lambda r: r['conc'])
    return [(r, AM.tier_shares(r)) for r in rs]


def sessions():
    """설정마다 HBM 이 찬 지점의 세션당 HBM. check_agentx_memory 2절과 같은 길."""
    per = collections.defaultdict(list)
    keys = ['model', 'hw', 'framework', 'offload', 'precision', 'tp', 'dp_attention']
    for k, rs in CM.group([r for r in CM.ROWS if CM.single(r)], keys).items():
        m, hw, fw, off, prec, tp, dpa = k
        h = AM.chip(hw)
        if h not in CM.SPEC['rows'] or m not in CM.PARAMS['rows'] or prec not in CM.BYTES['rows'] or not tp:
            continue
        c = AM.cliff(rs, CM.CLIFF)
        if not c or c['conc'] <= 1:
            continue
        w = AM.weights_gb_per_gpu(CM.PARAMS['rows'][m][0], CM.BYTES['rows'][prec][0], int(tp))
        free = AM.free_hbm_gb(CM.spec(h, 'hbm_gb'), CM.USABLE, w)
        gps = AM.gb_per_session(free, c['conc'], AM.serving_gpus(c))
        if gps is not None:
            per[m].append(gps)
    return sorted(((m, statistics.median(v), min(v), max(v), len(v)) for m, v in per.items()),
                  key=lambda x: x[1])


def ssd_rows():
    rs = [r for r in CM.ROWS if r['model'] == 'minimaxm3' and r['hw'].startswith('h100')]
    return {(r['offload'], r['conc']): r for r in rs}


def dram_pairs():
    out = []
    keys3 = ['model', 'hw', 'framework', 'precision', 'tp']
    g3 = CM.group([r for r in CM.ROWS if CM.single(r)], keys3 + ['offload'])
    for k in sorted({kk[:-1] for kk in g3}, key=str):
        off, on = g3.get(k + ('none',)), g3.get(k + ('dram',))
        if not off or not on:
            continue
        cells = [(s, AM.frontier_ratio(on, off, s)) for s in (25, 50, 75, 100, 125)]
        cells = [(s, v) for s, v in cells if v]
        if cells:
            out.append((k, cells))
    return out


def spec_table():
    head = ['칩', 'HBM 용량', 'HBM 대역폭', 'CPU-GPU 연결', '호스트 메모리', '성격']
    body = []
    for h in ('h100', 'h200', 'b200', 'b300', 'gb200', 'gb300', 'vr200', 'mi355x'):
        s = lambda c: CM.spec(h, c)
        body.append([CHIP[h], '%dGB' % s('hbm_gb'),
                     '—' if s('hbm_tb_s') is None else '%gTB/s' % s('hbm_tb_s'),
                     '원문에 없음' if not s('link') else '%s %sGB/s' % (s('link'), format(s('link_gb_s'), ',')),
                     s('host_mem') or '원문에 없음', '원문 값'])
    return head, body


def tier_table():
    head = ['동시성', 'GPU 캐시에서', 'DRAM 에서', '새로 계산', 'GPU KV 사용률', 'DRAM KV 사용률', 'GPU 한 장 처리량']
    body = []
    for r, s in tier_sweep():
        body.append(['%d' % r['conc'], '%.1f%%' % (s[0] * 100), '%.1f%%' % (s[1] * 100),
                     '%.1f%%' % (s[2] * 100), '%.2f' % (r['gpu_usage'] or 0),
                     '—' if not r.get('cpu_tokens') else '%.2f' % (r['cpu_used_tokens'] / r['cpu_tokens']),
                     '%s tok/s' % format(int(round(r['tput_per_gpu'])), ',')])
    return head, body


def session_table():
    head = ['모델', '세션당 HBM 중앙값', '범위', '설정 수', '성격']
    return head, [[NAME[m], '%.1fGB' % med, '%.1f~%.1fGB' % (lo, hi), '%d' % n,
                   '모델이 낸 값 — 여유 HBM ÷ 찬 지점의 한 장 세션 수']
                  for m, med, lo, hi, n in sessions()]


def dram_table():
    head = ['모델', '칩', '엔진', '정밀도·TP', '같은 속도에서 켠 ÷ 끈']
    body = []
    for k, cells in dram_pairs():
        body.append([NAME[k[0]], CHIP[AM.chip(k[1])], k[2], '%s · TP%s' % (k[3].upper(), k[4]),
                     ' · '.join('%d TPS %.2f배' % (s, v) for s, v in cells)])
    return head, body


def ssd_table():
    head = ['내려놓기', '소프트웨어', '동시성', 'GPU 한 장 처리량', '첫 토큰 P90', 'GPU 캐시', '바깥 층', '새로 계산한 토큰']
    by = ssd_rows()
    body = []
    for off in ('none', 'dram', 'nvme', 'dram+nvme'):
        for c in (8, 10):
            r = by.get((off, c))
            if not r:
                continue
            s = AM.tier_shares(r)
            body.append([OFF[off], r['backend'] or '—', '%d' % c,
                         '%s tok/s' % format(int(round(r['tput_per_gpu'])), ','),
                         '%.0f초' % r['p90_ttft'], '%.1f%%' % (s[0] * 100), '%.1f%%' % (s[1] * 100),
                         format(r['tok_computed'], ',')])
    return head, body


TABLES = {
    'MEMSPEC': ('칩마다 HBM 과 CPU-GPU 연결 — 원문 규격', spec_table),
    'MEMTIER': ('DeepSeek V4 Pro · B200 · SGLang — 입력 토큰은 어디서 오나', tier_table),
    'MEMSESS': ('HBM 이 찬 지점에서 세션 하나가 쓰는 HBM — 모델별', session_table),
    'MEMDRAM': ('DRAM 내려놓기를 켠 곡선 ÷ 끈 곡선 — 같은 속도에서 잰 칸만', dram_table),
    'MEMSSD': ('MiniMax M3 · H100 8장 · vLLM — 내려놓기 넷', ssd_table),
}
