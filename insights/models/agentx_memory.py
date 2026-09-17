"""AgentX 메모리 모델 — HBM·DRAM·SSD 가 에이전틱 추론 처리량에 얼마나 들어가나.

원자료: insights/models/raw/agentx_memory.json
  rows    InferenceX GitHub Actions 요약 파일(bmk_agentic) 769행, 모델 8개
  tables  칩 규격(원문 인용) · 모델 파라미터 수(HF) · 정밀도별 바이트(우리 가정)

사슬은 이렇다.

  서버가 센 입력 토큰 = GPU 캐시에서 꺼낸 것 + 바깥 층(DRAM·SSD)에서 꺼낸 것 + 새로 계산한 것
  GPU 한 장 여유 HBM = 규격 용량 × 쓸 수 있는 비율 − 모델 가중치 ÷ 가중치를 나눠 든 GPU 수
  HBM 이 차는 지점 = GPU KV 사용률이 문턱을 처음 넘는 동시성
  세션 하나가 쓰는 HBM = 여유 HBM ÷ 그 지점에서 GPU 한 장이 받는 세션 수

마지막 값은 모델의 토큰당 KV 크기와 세션 길이를 함께 담는다. 같은 트레이스를
돌리므로 세션 길이는 모델끼리 같다고 보고, 모델 사이 차이를 KV 구조 차이로 읽는다.
"""
import agentx_frontier as AX

GB = 1e9


def chip(hw):
    """클러스터 이름(b200-nscale)에서 칩(b200)을 뗀다."""
    return (hw or '').split('-')[0]


def weights_gb_per_gpu(params_billion, bytes_per_param, shard_gpus):
    """가중치를 나눠 든 GPU 한 장에 올라가는 몫(GB)."""
    return params_billion * bytes_per_param / shard_gpus


def free_hbm_gb(hbm_gb, usable, weights_per_gpu):
    """KV 에 남는 HBM. 엔진이 따로 잡는 몫은 usable 로 뭉뚱그린다."""
    return hbm_gb * usable - weights_per_gpu


def serving_gpus(r):
    """한 노드 실행에서 요청을 받는 GPU 수. DP 어텐션이면 노드 여덟 장이 다 받는다."""
    return 8 if r['dp_attention'] == 'true' else int(r['tp'])


def cliff(rows, threshold):
    """동시성 오름차순에서 GPU KV 사용률이 threshold 를 처음 넘는 행."""
    for r in sorted(rows, key=lambda r: r['conc']):
        if (r.get('gpu_usage') or 0) >= threshold:
            return r
    return None


def gb_per_session(free_gb, conc, gpus):
    """HBM 이 찬 지점에서 세션 하나가 쓰는 HBM(GB)."""
    per_gpu = conc / gpus
    return free_gb / per_gpu if per_gpu > 0 and free_gb > 0 else None


def tier_shares(r):
    """입력 토큰을 출처 셋으로 나눈 비율. 서버가 센 값이 없으면 None."""
    tot = r.get('prompt_total')
    parts = [r.get('tok_gpu_hit'), r.get('tok_ext_hit'), r.get('tok_computed')]
    if not tot or any(p is None for p in parts):
        return None
    return [p / tot for p in parts]


def as_frontier_rows(rows):
    """요약 파일 행을 프런티어 함수가 읽는 꼴로 감싼다."""
    return [{'metrics': {'p90_intvty': r['p90_intvty'], 'tput_per_gpu': r['tput_per_gpu']}}
            for r in rows if r.get('p90_intvty') and r.get('tput_per_gpu')]


def frontier_ratio(on_rows, off_rows, s):
    """같은 사용자 속도 s 에서 내려놓기를 켠 곡선 ÷ 끈 곡선. 둘 다 잰 범위 안일 때만."""
    a = AX.at(AX.frontier(as_frontier_rows(off_rows)), s)
    b = AX.at(AX.frontier(as_frontier_rows(on_rows)), s)
    return None if not a or not b else b / a


def max_tput(rows):
    return max((r['tput_per_gpu'] for r in rows), default=None)
