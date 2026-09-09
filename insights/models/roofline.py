"""루프라인 모델 — 칩이 연산에 막히나 메모리에 막히나.

원문: input/clippings/Cerebras — Faster Tokens Please.md (L215~L231)

성능은 둘 중 낮은 쪽에 걸린다. 초당 낼 수 있는 연산량과, 초당 나르는 바이트에
그 바이트가 낳는 연산량을 곱한 값이다.

    실현 연산량 = min(최대 연산량, 대역폭 × 산술 강도)

산술 강도는 바이트 하나가 몇 번의 연산을 낳느냐다. 행렬 곱셈이면 원문이 공표한
식이 있다.

    연산량 = 2·M·N·K
    바이트 = (M·K + K·N + M·N) × 원소당 바이트
    산술 강도 = 연산량 ÷ 바이트

정사각이면 M=N=K=n 이라 산술 강도가 (2/3)·(n/b) 로 줄어든다. 크기에 비례한다.

두 선이 만나는 자리를 능선이라 부른다. 능선 왼쪽은 메모리에 막히고 오른쪽은
연산에 막힌다. 능선의 위치는 최대 연산량을 대역폭으로 나눈 값이다 — 칩의 성격을
한 숫자로 줄인 것이다.
"""


def flops(m, n, k):
    """행렬 곱셈 한 번의 연산량. 곱하고 더하니 2를 곱한다."""
    return 2 * m * n * k


def bytes_moved(m, n, k, bytes_per_element):
    """읽고 쓰는 바이트. 입력 둘과 출력 하나가 전부 메모리를 거친다고 본다."""
    return (m * k + k * n + m * n) * bytes_per_element


def arithmetic_intensity(m, n, k, bytes_per_element):
    """바이트 하나가 낳는 연산 수."""
    return flops(m, n, k) / bytes_moved(m, n, k, bytes_per_element)


def square_intensity(n, bytes_per_element):
    """정사각 행렬이면 (2/3)·(n/b) 로 줄어든다. 원문이 공표한 축약형이다."""
    return (2.0 / 3.0) * n / bytes_per_element


def ridge_point(peak_flops, bandwidth_bytes_per_s):
    """능선 — 여기보다 산술 강도가 낮으면 메모리에, 높으면 연산에 막힌다."""
    return peak_flops / bandwidth_bytes_per_s


def implied_bandwidth(peak_flops, ridge):
    """능선과 최대 연산량이 주어졌을 때의 대역폭. 거꾸로 푼 값이다."""
    return peak_flops / ridge


def achieved_flops(peak_flops, bandwidth_bytes_per_s, intensity):
    """실현 연산량. 둘 중 낮은 쪽에 걸린다."""
    return min(peak_flops, bandwidth_bytes_per_s * intensity)


def bound_by(peak_flops, bandwidth_bytes_per_s, intensity):
    """어디에 막혔나."""
    return '연산' if intensity >= ridge_point(peak_flops, bandwidth_bytes_per_s) \
        else '메모리'


def shoreline_density(bandwidth_bytes_per_s, side_mm):
    """가장자리 1밀리미터가 나르는 바이트. 네모 칩이면 둘레는 네 변이다.

    칩 밖으로 데이터를 빼는 통로는 가장자리에 붙는다. 그래서 대역폭은 면적이
    아니라 둘레에 매인다 — 웨이퍼처럼 커도 둘레는 변 길이에 비례할 뿐이다.
    """
    return bandwidth_bytes_per_s / (4.0 * side_mm)


def power_density(watts, side_mm):
    """제곱센티미터당 와트. 열을 뽑아낼 수 있느냐를 정하는 값이다."""
    area_cm2 = (side_mm / 10.0) ** 2
    return watts / area_cm2


def area_mm2(side_mm):
    return side_mm * side_mm
