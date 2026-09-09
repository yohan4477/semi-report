"""추론 지연 모델 — 지연·처리량·동시 사용자·토큰당 원가를 한 항등식으로 잇는다.

원문: input/clippings/AMD vs NVIDIA Inference Benchmark Who Wins ... .md (L94~L98)
원문이 공표한 식은 하나다.

    E2E 지연 = 첫 토큰까지 시간 + 출력 토큰 수 × 토큰 사이 시간

이 식만으로 세 가지가 더 나온다. 원문은 그 셋을 안 냈다.

  ① 대화 속도   토큰 사이 시간의 역수. 사용자가 초당 몇 글자를 받나
  ② 동시 사용자  리틀의 법칙 — 처리량 × 지연 = 시스템 안에 든 요청 수
  ③ 토큰당 원가  GPU 시간당 원가를 처리량으로 나눈다

②가 이 모델의 알맹이다. 벤치마크가 「150초 지연에서 초당 1,000토큰」이라고 말할 때
그 뒤에 GPU 한 장이 동시에 몇 사람을 붙들고 있는지는 안 적힌다. 리틀의 법칙이 그것을
낸다 — 처리량과 지연을 곱하면 시스템 안에 든 요청 수가 된다.

세 값은 원문의 TCO 모델(inference_tco.py)과 물려 돌아간다. 시간당 원가는 거기서 온다.
"""


def e2e_latency_s(ttft_s, out_tokens, tbot_s):
    """원문이 공표한 식 그대로. 첫 토큰까지 기다리고, 나머지를 한 톨씩 받는다."""
    return ttft_s + out_tokens * tbot_s


def tbot_from_e2e(e2e_s, out_tokens, ttft_s):
    """지연 목표에서 토큰 사이 시간을 거꾸로 푼다."""
    return (e2e_s - ttft_s) / out_tokens


def interactivity(tbot_s):
    """사용자가 느끼는 속도. 초당 몇 토큰이 흘러나오나."""
    return 1.0 / tbot_s


def concurrency_per_gpu(tokens_per_s_per_gpu, out_tokens, e2e_s):
    """리틀의 법칙 — GPU 한 장이 동시에 붙들고 있는 요청 수.

    시스템 안에 든 요청 수 = 도착률 × 머무는 시간이다. 도착률은 초당 처리 토큰을
    요청당 출력 토큰으로 나눈 값이고, 머무는 시간이 E2E 지연이다.
    """
    requests_per_s = tokens_per_s_per_gpu / out_tokens
    return requests_per_s * e2e_s


def cost_per_million_tokens(hourly_per_gpu, tokens_per_s_per_gpu):
    """GPU 시간당 원가를 처리량으로 나눈다. 낮을수록 좋다."""
    return hourly_per_gpu / 3600.0 / tokens_per_s_per_gpu * 1_000_000


def throughput_for_cost(hourly_per_gpu, target_per_mtok):
    """토큰당 원가 목표를 맞추려면 초당 몇 토큰을 내야 하나. 거꾸로 푼 값이다."""
    return hourly_per_gpu / 3600.0 / target_per_mtok * 1_000_000


def profile(tokens_per_s_per_gpu, out_tokens, e2e_s, hourly_per_gpu, ttft_s=0.0):
    """한 운영점의 값 넷을 한꺼번에. ttft 를 모르면 0 으로 두고 그렇다고 밝힌다."""
    tbot = tbot_from_e2e(e2e_s, out_tokens, ttft_s)
    return {
        'tbot_s': tbot,
        'interactivity_tok_s': interactivity(tbot),
        'concurrency_per_gpu': concurrency_per_gpu(tokens_per_s_per_gpu, out_tokens, e2e_s),
        'cost_per_mtok': cost_per_million_tokens(hourly_per_gpu, tokens_per_s_per_gpu),
    }
