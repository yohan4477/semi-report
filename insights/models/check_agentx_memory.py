"""AgentX 메모리 모델 — 원자료에서 드라이버 값을 다시 내고 본문이 기대는 성질을 문다.

원자료는 `insights/models/raw/agentx_memory.json` 이 정본이다. 여기 찍히는 값이 본문
숫자의 대조 재료(model_facts.md)가 된다. FAIL 은 본문 주장이 원자료와 어긋날 때만 낸다.

    PYTHONIOENCODING=utf-8 python insights/models/check_agentx_memory.py
"""
import collections
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                        # noqa: E402
import agentx_memory as AM                                               # noqa: E402

RAW = load_raw('agentx_memory')
SPEC = table(RAW, 'mem-spec')
PARAMS = table(RAW, 'mem-params')
BYTES = table(RAW, 'mem-bytes')
ROWS = RAW['rows']

USABLE = 0.9        # 엔진이 KV 에 넘기는 HBM 비율 — vLLM·SGLang 기본값 근처로 둔 우리 가정
CLIFF = 0.95        # GPU KV 사용률이 이 값을 넘으면 찼다고 본다


def spec(h, col):
    return SPEC['rows'][h][SPEC['columns'].index(col)]


def single(r):
    return r['multinode'] != 'true' and r['disagg'] != 'true'


def group(rows, keys):
    g = collections.defaultdict(list)
    for r in rows:
        g[tuple(r[k] for k in keys)].append(r)
    return g


def main():
    fails = 0

    # ── 1. 입력 토큰은 어디서 오나 ─────────────────────────────────────────
    print('── 1. 입력 토큰의 출처 — DSv4 B200 SGLang (b200-nscale) ' + '─' * 14)
    sw = sorted([r for r in ROWS if r['model'] == 'dsv4' and r['hw'] == 'b200-nscale'
                 and r['framework'] == 'sglang' and AM.tier_shares(r)], key=lambda r: r['conc'])
    for r in sw:
        s = AM.tier_shares(r)
        print('  동시성 %4d  %-5s GPU %5.1f%% · 바깥 %5.1f%% · 계산 %5.1f%% | GPU KV %.2f · DRAM KV %s | %6.0f tok/s'
              % (r['conc'], r['offload'], s[0] * 100, s[1] * 100, s[2] * 100, r['gpu_usage'] or 0,
                 '-' if not r.get('cpu_tokens') else '%.2f' % (r['cpu_used_tokens'] / r['cpu_tokens']),
                 r['tput_per_gpu']))
    top = sw[-1]
    print('  동시성 %d 입력 %.2f억 토큰 = GPU %.2f억 + 바깥 %.2f억 + 계산 %.2f억 · DRAM KV %s/%s 토큰'
          % (top['conc'], top['prompt_total'] / 1e8, top['tok_gpu_hit'] / 1e8, top['tok_ext_hit'] / 1e8,
             top['tok_computed'] / 1e8, format(top['cpu_used_tokens'], ','), format(top['cpu_tokens'], ',')))
    shares = [AM.tier_shares(r) for r in ROWS if AM.tier_shares(r)]
    sums = [sum(s) for s in shares]
    comp = sorted(s[2] for s in shares)
    out_share = sorted(r['output_per_gpu'] / r['tput_per_gpu'] for r in ROWS if r.get('output_per_gpu'))
    print('  서버가 출처를 센 행 %d개 — 새로 계산한 비중 중앙값 %.1f%% (사분위 %.1f~%.1f%%), 출력 토큰 비중 중앙값 %.2f%%'
          % (len(shares), statistics.median(comp) * 100, comp[len(comp) // 4] * 100,
             comp[3 * len(comp) // 4] * 100, statistics.median(out_share) * 100))
    bad = sum(1 for x in sums if not 0.9 <= x <= 1.12)
    print('  세 출처 합이 입력의 90~112%% 밖인 행 %d개 (페이지 단위로 세어 넘친다)' % bad)
    ok = bad <= len(sums) * 0.1
    fails += not ok
    print('  합이 맞는 행이 90%% 이상%s' % ('' if ok else '  FAIL'))

    # ── 2. HBM 이 차는 지점과 세션 하나의 HBM ────────────────────────────
    print()
    print('── 2. HBM 이 차는 지점 — 한 노드 실행 ' + '─' * 30)
    per_model = collections.defaultdict(list)
    keys = ['model', 'hw', 'framework', 'offload', 'precision', 'tp', 'dp_attention']
    for k, rs in sorted(group([r for r in ROWS if single(r)], keys).items(), key=lambda x: str(x[0])):
        m, hw, fw, off, prec, tp, dpa = k
        h = AM.chip(hw)
        if h not in SPEC['rows'] or m not in PARAMS['rows'] or prec not in BYTES['rows'] or not tp:
            continue
        c = AM.cliff(rs, CLIFF)
        if not c or c['conc'] <= 1:
            continue
        w = AM.weights_gb_per_gpu(PARAMS['rows'][m][0], BYTES['rows'][prec][0], int(tp))
        free = AM.free_hbm_gb(spec(h, 'hbm_gb'), USABLE, w)
        n = AM.serving_gpus(c)
        gps = AM.gb_per_session(free, c['conc'], n)
        if gps is None:
            continue
        per_model[m].append(gps)
        print('  %-11s %-6s %-12s %-5s %-4s TP%-2s | HBM %3dGB 가중치 %5.1fGB 여유 %5.1fGB | 찬 동시성 %4d · 한 장 %5.2f세션 · 세션당 %5.1fGB'
              % (m, h, fw[:12], off, prec, tp, spec(h, 'hbm_gb'), w, free, c['conc'], c['conc'] / n, gps))
    print()
    print('  모델별 세션당 HBM (GB) — 중앙값 · 범위 · 설정 수')
    med = {}
    for m, v in sorted(per_model.items(), key=lambda x: statistics.median(x[1])):
        med[m] = statistics.median(v)
        print('    %-11s %6.1f · %5.1f~%5.1f · %d' % (m, med[m], min(v), max(v), len(v)))
    order = ['dsv4', 'minimaxm3', 'glm5.2']
    ok = all(m in med for m in order) and med['dsv4'] < med['minimaxm3'] < med['glm5.2']
    fails += not ok
    print('  DSv4 < MiniMax M3 < GLM-5.2 순서%s' % ('' if ok else '  FAIL'))
    ratio = med['glm5.2'] / med['dsv4']
    print('  GLM-5.2 ÷ DSv4 = %.1f배' % ratio)

    print()
    print('── 2-B. 같은 모델, HBM 만 다를 때 — Qwen3.5 FP4 TP2 ' + '─' * 16)
    q = {}
    for h in ('b200', 'b300'):
        rs = [r for r in ROWS if single(r) and r['model'] == 'qwen3.5' and AM.chip(r['hw']) == h
              and r['precision'] == 'fp4' and str(r['tp']) == '2' and r['offload'] == 'dram']
        c = AM.cliff(rs, CLIFF)
        w = AM.weights_gb_per_gpu(PARAMS['rows']['qwen3.5'][0], BYTES['rows']['fp4'][0], 2)
        q[h] = (AM.free_hbm_gb(spec(h, 'hbm_gb'), USABLE, w), c['conc'] / 2)
        print('  %s  여유 HBM %.1fGB · 찬 지점 한 장 %.1f세션' % (h, q[h][0], q[h][1]))
    fr, sr = q['b300'][0] / q['b200'][0], q['b300'][1] / q['b200'][1]
    print('  여유 HBM %.2f배 → 세션 %.2f배 · 탄력성 %.2f' % (fr, sr, sr / fr))
    ok = sr >= fr * 0.9
    fails += not ok
    print('  세션이 여유 HBM 만큼은 는다%s' % ('' if ok else '  FAIL'))
    raw_ratio = spec('b300', 'hbm_gb') / spec('b200', 'hbm_gb')
    print('  규격 용량으로는 %.2f배 — 가중치가 고정으로 빠져 여유분은 %.2f배가 된다' % (raw_ratio, fr))

    # ── 3. DRAM 을 켜면 같은 속도에서 ─────────────────────────────────────
    print()
    print('── 3. DRAM 내려놓기 켠 곡선 ÷ 끈 곡선 — 같은 사용자 속도 ' + '─' * 12)
    gains = []
    keys3 = ['model', 'hw', 'framework', 'precision', 'tp']
    g3 = group([r for r in ROWS if single(r)], keys3 + ['offload'])
    for k in sorted({kk[:-1] for kk in g3}, key=str):
        off, on = g3.get(k + ('none',)), g3.get(k + ('dram',))
        if not off or not on:
            continue
        cells = []
        for s in (25, 50, 75, 100, 125):
            v = AM.frontier_ratio(on, off, s)
            if v:
                cells.append('%d TPS %.2f' % (s, v))
                gains.append(v)
        print('  %-11s %-14s %-13s %-4s TP%-2s 끈 최대 %7.0f · 켠 최대 %7.0f tok/s | %s'
              % (k[0], k[1], (k[2] or '')[:13], k[3], k[4], AM.max_tput(off), AM.max_tput(on),
                 ' · '.join(cells) or '같은 속도 구간 없음'))
    print('  같은 속도에서 잰 칸 %d개 · 켠 ÷ 끈 중앙값 %.2f · 범위 %.2f~%.2f'
          % (len(gains), statistics.median(gains), min(gains), max(gains)))

    # ── 4. SSD ─────────────────────────────────────────────────────────
    print()
    print('── 4. MiniMax M3 H100 vLLM — 내려놓기 없음·DRAM·SSD·DRAM+SSD ' + '─' * 8)
    ssd = [r for r in ROWS if r['model'] == 'minimaxm3' and r['hw'].startswith('h100')]
    by = {}
    for r in sorted(ssd, key=lambda r: (r['offload'], r['conc'])):
        by[(r['offload'], r['conc'])] = r
        s = AM.tier_shares(r)
        print('  %-9s %-11s 동시성 %2d | %5.0f tok/s · P90 %4.1f TPS · 첫 토큰 P90 %5.0f초 | GPU %4.1f%% · 바깥 %4.1f%% · 계산 %s토큰'
              % (r['offload'], r['backend'] or '-', r['conc'], r['tput_per_gpu'], r['p90_intvty'] or 0,
                 r['p90_ttft'] or 0, s[0] * 100, s[1] * 100, format(r['tok_computed'], ',')))
    n8, d8, s8 = by[('none', 8)], by[('dram', 8)], by[('nvme', 8)]
    print('  동시성 8: SSD ÷ DRAM 처리량 %.2f · 없음 ÷ DRAM %.2f · 계산 토큰 없음 ÷ SSD %.1f배'
          % (s8['tput_per_gpu'] / d8['tput_per_gpu'], n8['tput_per_gpu'] / d8['tput_per_gpu'],
             n8['tok_computed'] / s8['tok_computed']))
    ok = s8['tput_per_gpu'] >= 0.9 * d8['tput_per_gpu'] and n8['tput_per_gpu'] < 0.5 * d8['tput_per_gpu']
    fails += not ok
    print('  SSD 가 DRAM 의 90%% 이상 · 없음은 절반 아래%s' % ('' if ok else '  FAIL'))

    # ── 5. 연결 방식별로 DRAM 이 맡은 적중 ──────────────────────────────
    print()
    print('── 5. CPU-GPU 연결 방식별 바깥 층 적중 최댓값 — 엔진이 같이 달라 인과 아님 ' + '─' * 2)
    link = collections.defaultdict(list)
    for r in ROWS:
        h = AM.chip(r['hw'])
        if r['offload'] in ('dram',) and h in SPEC['rows'] and r.get('hit_ext') is not None:
            link[(spec(h, 'link') or '원문에 없음', h)].append(r['hit_ext'])
    for (ln, h), v in sorted(link.items(), key=lambda x: str(x[0])):
        print('  %-12s %-6s 행 %3d · 바깥 적중 최댓값 %5.1f%% · 중앙값 %4.1f%%'
              % (ln, h, len(v), max(v) * 100, statistics.median(v) * 100))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
