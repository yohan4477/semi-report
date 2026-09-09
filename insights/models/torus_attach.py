"""3D 토러스 랙의 배선 부착률 모델 — TPU v7.

원문: input/clippings/TPUv7 Google Takes a Swing at the King.md (L278)
표 그림: 034 — Google TPU v7 3D Torus Connections Attach Rates

칩을 세제곱 격자에 놓고 3차원 토러스로 잇는다. 각 칩은 여섯 이웃(±x·±y·±z)과
연결된다. 연결 셋 가운데 무엇으로 잇는지가 칩이 어디 놓였느냐로 정해진다.

  기판 배선   같은 보드 위 이웃. 칩 자리와 무관하게 정해진 수만큼
  구리 케이블  랙 안 다른 보드의 이웃
  광 트랜시버  격자 끝에서 반대쪽 끝으로 되돌아가는 연결(토러스 닫힘)

되돌아가는 연결은 물리적으로 가장 멀어 광으로 간다. 그래서 칩의 좌표 가운데
격자 끝에 걸린 축이 몇 개냐가 곧 그 칩의 광 연결 수다.

세는 법에서 갈리는 자리가 하나 있다. 케이블과 기판 배선은 두 칩을 잇는 한
물건이라 랙 합계에서 반으로 나눈다. 트랜시버는 연결 양끝에 하나씩 붙는 부품이라
안 나눈다. 원문의 「TPU 한 장당 광 트랜시버 1.5개」가 이 차이에서 나온다.
"""
import itertools


LINKS_PER_CHIP = 6          # 3차원 토러스 — ±x·±y·±z
PCB_PER_CHIP = 2            # 같은 보드 위 이웃. 그림 034 가 네 자리 모두 2 로 적었다


def _boundary_axes(pos, dims):
    """이 칩의 좌표 가운데 격자 끝에 걸린 축의 수. 그만큼 되돌아가는 연결이 생긴다."""
    return sum(1 for p, n in zip(pos, dims) if n > 1 and p in (0, n - 1))


def classify(dims):
    """격자를 훑어 자리마다 칩 수를 센다. 자리 이름은 끝에 걸린 축 수로 정한다."""
    names = {0: '안쪽', 1: '면', 2: '모서리', 3: '꼭짓점'}
    out = {}
    for pos in itertools.product(*[range(n) for n in dims]):
        k = _boundary_axes(pos, dims)
        out.setdefault(k, {'name': names.get(k, '축 %d 개' % k), 'chips': 0})
        out[k]['chips'] += 1
    for k, v in out.items():
        v['optical'] = k                                   # 되돌아가는 연결 수
        v['pcb'] = PCB_PER_CHIP
        v['copper'] = LINKS_PER_CHIP - PCB_PER_CHIP - k    # 나머지가 구리
    return out


def rack(dims):
    """랙 하나의 합계. 케이블과 배선은 반으로 나누고 트랜시버는 안 나눈다."""
    groups = classify(dims)
    chips = 1
    for n in dims:
        chips *= n
    ends = {k: sum(g['chips'] * g[k] for g in groups.values())
            for k in ('copper', 'pcb', 'optical')}
    return {
        'chips': chips,
        'groups': groups,
        # 한 물건이 양끝을 잇는다 — 링크 수는 끝 수의 절반
        'copper_cables': ends['copper'] / 2,
        'pcb_traces': ends['pcb'] / 2,
        # 트랜시버는 끝마다 하나씩 붙는다 — 안 나눈다
        'transceivers': ends['optical'],
        'copper_per_chip': ends['copper'] / 2 / chips,
        'pcb_per_chip': ends['pcb'] / 2 / chips,
        'transceivers_per_chip': ends['optical'] / chips,
    }


def attach_rate(dims):
    """칩 한 장당 광 트랜시버 수. 이 모델이 답하는 값이다."""
    return rack(dims)['transceivers_per_chip']
