# -*- coding: utf-8 -*-
# 수도리무브 — 로보틱스·피지컬 AI 해설 아카이브.
# 채널(sudoremove) 하나를 통째로 받는 장이 아니라 **로봇 모델을 다루는 주제**를 받는 장이다.
# 공개 웹 에세이(sudoremove.com)와 유튜브 해설이 같은 페이지에 선다.
# 카드는 이 파일 CARDS에 적고 재실행하면 페이지가 다시 만들어진다.
# 마크업·CSS·첫 화면 규약은 dash_common 머리말에 있다.
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc

OUT = os.path.join(dc.ROOT, '대시보드', '수도리무브 대시보드.html')
blob = dc.blob

STAMP = '2026-08-23'
BASE = 'content/understanding/피지컬AI/'
VID = 'https://youtu.be/-sa8-SxgrVU'
PAPER = 'https://arxiv.org/abs/2603.08122'

WHO_YT = 'sudoremove <b>JB · JC</b>'
WHO_ESSAY = 'sudoremove <b>박종현</b>'

# 섹션은 여기 한 곳에서만 정한다. 카드 파일은 문자열 id만 쓰고(예: 'sec-model')
# 로더가 이 표로 푼다 — 카드 서른 장이 각자 섹션 튜플을 베껴 들고 있으면 번호가 어긋난다.
SECTIONS = [
    ('sec-base', '01', '피지컬 AI 기초',
     '용어의 층위, 범용화 조건, 그리고 데이터가 없다는 사실'),
    ('sec-model', '02', '모델과 회사',
     '같은 데이터 병목을 서로 다른 자리에서 푸는 회사들'),
    ('sec-world', '03', '월드모델',
     '영상을 만드는 모델이 로봇의 훈련장이 되는 길'),
    ('sec-hand', '04', '로봇 손과 하드웨어',
     '모델이 아무리 좋아도 잡지 못하면 아무것도 안 된다'),
    ('sec-biz', '05', '회사와 산업',
     '누가 돈을 받고 누가 망했나'),
    ('sec-field', '06', '현장과 실습',
     '학회·전시장·해커톤에서 직접 보고 만져 본 기록'),
]
SEC = {s[0]: s for s in SECTIONS}
SEC_ORDER = [s[0] for s in SECTIONS]

SEC_MODEL = SEC['sec-model']
SEC_BASE = SEC['sec-base']

NOTE_YT = ('유튜브 자동 자막 전문을 <b>요약</b>한 카드입니다. 자동 인식이라 회사·모델 이름이 '
           '흔들리는 대목이 있어 영상 설명란과 논문으로 맞춰 적었습니다. 자막은 Sharpa를 '
           '「셰파」와 「샤파」로 번갈아 받아 적고 설명란 목차에도 Sherpa가 한 번 나오는데, '
           '논문 링크 표기를 따라 <b>Sharpa</b>로 통일했습니다. 이 회사가 로봇 손을 만들어 왔다는 '
           '것은 이 편이 아니라 같은 채널의 「로봇 손 직접 다 써보고 알려 드림」(2026-06-21)과 '
           '「CES 로봇 리뷰」(2026-01-14)에서 다룹니다. 숫자는 진행자가 말한 것을 그대로 옮겼고 '
           '따로 검증하지 않았습니다. 투자 추천이 아닙니다.')
NOTE_ESSAY = ('sudoremove.com 공개 웹 에세이를 <b>요약</b>한 카드입니다. 원문 전문을 다시 싣지 '
              '않습니다. 숫자는 필자가 적은 것을 옮겼고 따로 검증하지 않았습니다. '
              '투자 추천이 아닙니다.')

ESSAY_META = [WHO_ESSAY, '2026-03-19', '공개 웹 에세이', 'sudoremove.com']


def elinks(name, url):
    return [('📄 변환본', blob(BASE + name + '.md'), ''),
            ('🔗 원문(sudoremove.com)', url, 'secondary')]


# ── 그림 ──────────────────────────────────────────────────────────────
# 말로 읽으면 순서가 안 잡히는 대목만 그린다. 무엇이 무엇을 먹어서 무엇을 내놓는지를
# 상자와 화살표로만 그린다. 색은 .uc-fig 붓(card_lib.FIG_CSS)을 그대로 받는다.
# 좌표를 손으로 적는 일이 잦아 상자·글씨를 함수로 뽑았다 — 글자가 상자 밖으로 나가는지는
# 브라우저에서 getBBox 로 잰다(눈으로만 보면 다크모드에서 놓친다).


def _r(x, y, w, h, st='var(--ink-3)', sw=1.5, extra=''):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, st, sw, extra))


def _t(cx, y, s, cls='t-lab'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _lt(x, y, s, cls='t-sm', bold=True):
    return ('<text x="%d" y="%d" class="%s"%s>%s</text>'
            % (x, y, cls, ' style="font-weight:850"' if bold else '', s))


def _a(x1, y1, x2, y2, dash=False):
    return ('<path d="M%d %d L%d %d" class="flow"%s/>'
            % (x1, y1, x2, y2, ' style="stroke-dasharray:5 4"' if dash else ''))


def _box(x, y, w, h, lines, st='var(--ink-3)', sw=1.5):
    """상자 하나 + 가운데 정렬한 줄들. 첫 줄은 t-lab, 나머지는 t-sm."""
    cx, out = x + w // 2, [_r(x, y, w, h, st, sw)]
    n = len(lines)
    top = y + (h - (n - 1) * 16) // 2 + 5
    for i, s in enumerate(lines):
        out.append(_t(cx, top + i * 16, s, 't-lab' if i == 0 else 't-sm'))
    return ''.join(out)


def _svg(w, h, label, body):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>'
            % (w, h, label, body))


# 넓은 정의와 좁은 정의를 가르는 선 — 「Physical AI의 정의」 카드
FIG_DEF = _svg(640, 246, 'Physical AI의 넓은 정의와 좁은 정의', ''.join([
    _t(155, 28, '넓게 잡으면 여기까지', 't-sm'),
    _t(485, 28, '좁게 잡으면 이것만', 't-sm'),
    '<path d="M320 40 L320 208" stroke="var(--ink-3)" stroke-width="2" '
    'stroke-dasharray="6 5" fill="none"/>',
    _box(30, 48, 250, 44, ['자율주행']),
    _box(30, 104, 250, 44, ['드론']),
    _box(30, 160, 250, 44, ['디지털 트윈']),
    _box(360, 48, 250, 44, ['π0 · Helix — 빨래 개기'], 'var(--accent)', 1.8),
    _box(360, 104, 250, 44, ['Figure AI — 비닐 포장 1시간'], 'var(--accent)', 1.8),
    _box(360, 160, 250, 44, ['보스턴 다이내믹스 — LBM'], 'var(--accent)', 1.8),
    _t(320, 224, '경계선 — RT-2 (2023년 7월)', 't-sm'),
    _t(155, 240, '규칙 기반으로 이미 하던 것', 't-sm'),
    _t(485, 240, '규칙 기반으로는 못 하던 것', 't-sm'),
]))

# 계보 한 줄과 세 이름의 층위 — 「VLA · LBM · RFM」 카드
FIG_TERMS = _svg(640, 236, 'VLA와 LBM과 RFM의 층위', ''.join([
    _lt(20, 26, '계보는 한 줄이다'),
    _box(20, 38, 130, 46, ['LLM', '텍스트']),
    _box(180, 38, 130, 46, ['VLM', '시각 + 언어']),
    _box(340, 38, 130, 46, ['VLA', '+ 행동']),
    _box(500, 38, 130, 46, ['VTLA', '+ 촉각']),
    _a(152, 61, 178, 61), _a(312, 61, 338, 61), _a(472, 61, 498, 61),
    _lt(20, 112, '이름 셋의 층위는 다르다'),
    _r(140, 122, 360, 100, 'var(--accent)', 1.8),
    _t(320, 142, 'RFM — 여러 환경 · 여러 과제를 한 모델이', 't-sm'),
    _box(160, 154, 155, 52, ['VLA', '입력 쪽에서 부른 이름']),
    _box(325, 154, 155, 52, ['LBM', '출력 쪽에서 부른 이름']),
    _a(405, 86, 405, 120, True),
]))

# 비전이 걸어간 길과 로보틱스가 걷는 길 — 「비전 AI가 걸어간 길」 카드
FIG_PATH = _svg(640, 248, '비전 AI의 수렴과 로보틱스의 수렴', ''.join([
    _lt(20, 26, '비전 AI — 이미 지나간 길'),
    _box(20, 36, 250, 48, ['분류 · 검출 · 분할', '과제마다 따로']),
    _box(390, 36, 230, 48, ['통합 VLM 하나']),
    _a(272, 60, 388, 60),
    _lt(20, 116, '로보틱스 — 지금 걷는 길'),
    _box(20, 126, 250, 48, ['과제별 특화 모델', '환경이 바뀌면 무너진다'], 'var(--accent)', 1.8),
    _box(390, 126, 230, 48, ['범용 RFM'], 'var(--accent)', 1.8),
    _a(272, 150, 388, 150),
    _box(20, 196, 190, 44, ['사전학습 VLM 백본'], 'var(--line)', 1.3),
    _box(225, 196, 190, 44, ['교차 embodiment 데이터'], 'var(--line)', 1.3),
    _box(430, 196, 190, 44, ['스케일링 법칙'], 'var(--line)', 1.3),
    _a(115, 194, 115, 176), _a(320, 194, 320, 176), _a(525, 194, 525, 176),
]))

# 병목 셋과 뚫으려는 경로 다섯 — 「행동 데이터는 인터넷에 없다」 카드
FIG_PATHS5 = _svg(640, 268, '행동 데이터 병목과 다섯 경로', ''.join([
    _box(90, 14, 460, 50, ['막는 것 셋',
                           '데이터가 없다 · 평가가 비싸다 · 하드웨어가 덜 됐다'],
         'var(--accent)', 1.8),
    _a(320, 64, 320, 84),
    '<path d="M60 84 L580 84" stroke="var(--ink-3)" stroke-width="1.4" fill="none"/>',
    ] + [_a(x, 84, x, 100) for x in (68, 194, 320, 446, 572)] + [
    _box(9, 100, 118, 76, ['텔레오퍼레이션', '사람이 장비를 걸치고', '로봇을 조종']),
    _box(135, 100, 118, 76, ['UMI', '집게를 사람이 들고', '로봇 없이 수집']),
    _box(261, 100, 118, 76, ['시뮬레이션', 'Isaac GR00T가', '합성 데이터 생성']),
    _box(387, 100, 118, 76, ['커뮤니티', 'HuggingFace가', '하드웨어까지 개방']),
    _box(513, 100, 118, 76, ['월드모델 + IDM', '레이블 없는 영상에서', '행동을 역산']),
    ] + [_a(x, 176, x, 196) for x in (68, 194, 320, 446, 572)] + [
    _r(90, 196, 460, 46, 'var(--line)', 1.3, ' stroke-dasharray="6 5"'),
    _t(320, 216, '다섯 가운데 무엇도 규모 문제를 푼다고 입증되지 않았다', 't-sm'),
    _t(320, 232, '이 글이 닫는 자리다', 't-sm'),
]))


# 다섯 편이 세 갈래로 갈린다 — 「GTC 열흘 전」 카드
FIG_GTC = _svg(640, 250, '같은 재료에서 갈린 세 갈래', ''.join([
    _box(170, 12, 300, 44, ['같은 재료', '사람 1인칭 영상']),
    _a(300, 56, 130, 94), _a(320, 56, 320, 94), _a(340, 56, 510, 94),
    _box(10, 96, 200, 90, ['월드모델', 'DreamDojo', '사람 영상 4만 시간',
                           '잠재행동을 자기지도로']),
    _box(220, 96, 200, 90, ['VLA', 'SONIC · EgoScale', '손 관절값 2만 시간',
                            '마노스 장갑으로 뽑음'], 'var(--accent)', 1.8),
    _box(430, 96, 200, 90, ['비디오 액션모델', 'DreamZero', 'Cosmos Policy',
                            '영상 생성 모델을 파인튜닝']),
    _a(110, 186, 110, 198), _a(530, 186, 530, 198),
    _box(10, 198, 200, 44, ['월드모델 안 성공률이', '실제보다 높다'], 'var(--line)', 1.3),
    _box(430, 198, 200, 44, ['GB200 두 대로 7Hz', '반응이 못 따라간다'], 'var(--line)', 1.3),
]))

# 300년과 170년은 같은 자가 아니다 — 「Dyna-2」 카드
FIG_YEARS = _svg(640, 232, 'Rhoda 300년과 Dyna-2 170년의 성격 차이', ''.join([
    '<path d="M320 34 L320 178" stroke="var(--ink-3)" stroke-width="2" '
    'stroke-dasharray="6 5" fill="none"/>',
    _box(20, 26, 270, 152, ['Rhoda AI — 웹 비디오 300년', '인터넷에 이미 있던 영상',
                            '로봇 손이 나오지 않는다', '로봇 데이터는 11시간만',
                            '성공률 숫자 없음']),
    _box(350, 26, 270, 152, ['Dyna-2 — 사람 영상 170년', '100만 시간, 벤더가 새로 찍음',
                             '손목을 6DOF로 좌표화하려고', '로봇 파인튜닝 성공률',
                             '20%에서 53%로'], 'var(--accent)', 1.8),
    _t(320, 198, '세는 대상이 다르다 — 「년」이라는 단위만 같다', 't-sm'),
    _t(320, 216, '하나는 주워 온 영상, 하나는 쓰려고 찍은 영상', 't-sm'),
]))

# 로봇을 쓰느냐 안 쓰느냐 — 「로봇 데이터 없이」 카드
FIG_3CO = _svg(640, 236, '데이터를 모으는 두 갈래', ''.join([
    _lt(20, 24, 'Sunday Robotics · Generalist AI — 로봇 없이 모은다'),
    _box(20, 34, 180, 52, ['사람이 글로브를 낀다'], 'var(--accent)', 1.8),
    _box(230, 34, 180, 52, ['영상 + 손 좌표'], 'var(--accent)', 1.8),
    _box(440, 34, 180, 52, ['리타게팅해 로봇으로'], 'var(--accent)', 1.8),
    _a(202, 60, 228, 60), _a(412, 60, 438, 60),
    _lt(20, 122, 'Physical Intelligence — 로봇을 써서 모은다'),
    _box(20, 132, 180, 52, ['사람이 로봇을 조종']),
    _box(230, 132, 180, 52, ['로봇 데이터']),
    _box(440, 132, 180, 52, ['지도학습 + 강화학습']),
    _a(202, 158, 228, 158), _a(412, 158, 438, 158),
    _t(320, 208, '제목의 「없이」는 위 두 회사에만 맞는다', 't-sm'),
    _t(320, 226, '아래 한 회사는 로봇을 그대로 쓴다', 't-sm'),
]))

# 손 넷을 같은 자로 — 「Sharpa는 로봇 손 회사였다」 카드
FIG_HANDS = _svg(640, 202, '로봇 손 넷의 실측 비교', ''.join([
    _lt(12, 22, '손 넷을 같은 자로 잰다'),
    _box(12, 32, 148, 120, ['Wuji', '600g · 15N', '값 비공개',
                            '초경량, 파지 지름', '40분 과열, V2 나옴']),
    _box(168, 32, 148, 120, ['Sharpa', '1.2kg · 20N', '5만 달러',
                             '엄지 5자유도', '촉각 530픽셀'], 'var(--accent)', 1.8),
    _box(324, 32, 148, 120, ['Tesollo', '870g', '7,500달러',
                             '20 · 15자유도', '촉각은 선택 옵션']),
    _box(480, 32, 148, 120, ['Alex', '40N — 넷 중 최강', 'RealWorld 독점',
                             '전완부 액추에이터', '100g 변화 감지']),
    _t(320, 178, 'Sharpa 한 개 값이 Tesollo의 여섯 배가 넘는다', 't-sm'),
    _t(320, 194, '손 하나가 로봇 상체보다 비쌀 때도 있다', 't-sm'),
]))

FIG_WHO = (
    '<svg viewBox="0 0 640 250" role="img" '
    'aria-label="Rhoda AI와 Sharpa는 서로 다른 회사다">'
    '<rect x="160" y="14" width="320" height="46" rx="9" fill="none" '
    'stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="320" y="34" text-anchor="middle" class="t-lab">둘이 같이 걸린 병목</text>'
    '<text x="320" y="50" text-anchor="middle" class="t-sm">로봇 데이터가 인터넷에 없다</text>'
    '<path d="M280 60 L172 92" class="flow"/>'
    '<path d="M360 60 L468 92" class="flow"/>'
    '<rect x="20" y="96" width="280" height="134" rx="10" fill="none" '
    'stroke="var(--accent)" stroke-width="1.6"/>'
    '<text x="160" y="121" text-anchor="middle" class="t-lab">Rhoda AI</text>'
    '<text x="160" y="139" text-anchor="middle" class="t-sm">스텔스에서 2026년 3월 등장</text>'
    '<text x="160" y="155" text-anchor="middle" class="t-sm">조달 4억 5천만 달러</text>'
    '<path d="M36 168 L284 168" stroke="var(--line)" stroke-width="1" fill="none"/>'
    '<text x="160" y="190" text-anchor="middle" class="t-sm">다음 장면을 상상해</text>'
    '<text x="160" y="206" text-anchor="middle" class="t-sm">행동을 거꾸로 계산</text>'
    '<text x="160" y="222" text-anchor="middle" class="t-sm">논문 없음 · 데모만</text>'
    '<rect x="340" y="96" width="280" height="134" rx="10" fill="none" '
    'stroke="var(--accent)" stroke-width="1.6"/>'
    '<text x="480" y="121" text-anchor="middle" class="t-lab">Sharpa</text>'
    '<text x="480" y="139" text-anchor="middle" class="t-sm">로봇 손을 만드는 회사</text>'
    '<text x="480" y="155" text-anchor="middle" class="t-sm">엔비디아 GTC 2026 부스</text>'
    '<path d="M356 168 L604 168" stroke="var(--line)" stroke-width="1" fill="none"/>'
    '<text x="480" y="190" text-anchor="middle" class="t-sm">어려운 동작을 반사로</text>'
    '<text x="480" y="206" text-anchor="middle" class="t-sm">미리 구워 둔다</text>'
    '<text x="480" y="222" text-anchor="middle" class="t-sm">논문 MoDE-VLA</text>'
    '</svg>')

FIG_DVA = (
    '<svg viewBox="0 0 640 300" role="img" '
    'aria-label="VLA와 Rhoda DVA의 경로 대조">'
    # 위 칸 — 지금까지의 VLA
    '<rect x="6" y="22" width="628" height="96" rx="10" fill="none" '
    'stroke="var(--line)" stroke-width="1.2"/>'
    '<text x="20" y="42" class="t-sm" style="font-weight:850">VLA — 지금 보이는 것만 본다</text>'
    '<rect x="26" y="54" width="160" height="48" rx="8" fill="none" stroke="var(--line)" stroke-width="1.4"/>'
    '<text x="106" y="74" text-anchor="middle" class="t-lab">지금 이미지 + 말</text>'
    '<text x="106" y="90" text-anchor="middle" class="t-sm">한 장면</text>'
    '<rect x="232" y="54" width="160" height="48" rx="8" fill="none" stroke="var(--line)" stroke-width="1.4"/>'
    '<text x="312" y="74" text-anchor="middle" class="t-lab">VLA 모델</text>'
    '<text x="312" y="90" text-anchor="middle" class="t-sm">한 모델이 통째로</text>'
    '<rect x="438" y="54" width="150" height="48" rx="8" fill="none" stroke="var(--line)" stroke-width="1.4"/>'
    '<text x="513" y="82" text-anchor="middle" class="t-lab">관절 명령</text>'
    '<path d="M188 78 L230 78" class="flow"/>'
    '<path d="M394 78 L436 78" class="flow"/>'
    # 아래 칸 — Rhoda
    '<rect x="6" y="132" width="628" height="160" rx="10" fill="none" '
    'stroke="var(--accent)" stroke-width="1.4" stroke-opacity=".55"/>'
    '<text x="20" y="152" class="t-sm" style="font-weight:850">'
    'Rhoda DVA — 지나간 장면을 전부 들고 다음 장면을 상상한다</text>'
    '<rect x="26" y="164" width="164" height="46" rx="8" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="108" y="186" text-anchor="middle" class="t-lab">지나간 프레임 전부</text>'
    '<text x="108" y="202" text-anchor="middle" class="t-sm">KV 캐시</text>'
    '<rect x="236" y="164" width="156" height="46" rx="8" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="314" y="186" text-anchor="middle" class="t-lab">비디오 모델</text>'
    '<text x="314" y="202" text-anchor="middle" class="t-sm">다음 프레임 예측</text>'
    '<rect x="438" y="164" width="150" height="46" rx="8" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="513" y="192" text-anchor="middle" class="t-lab">다음 프레임</text>'
    '<path d="M190 187 L234 187" class="flow"/>'
    '<path d="M392 187 L436 187" class="flow"/>'
    '<path d="M513 210 L513 230" class="flow"/>'
    '<rect x="26" y="232" width="164" height="46" rx="8" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="108" y="260" text-anchor="middle" class="t-lab">로봇 실행</text>'
    '<rect x="236" y="232" width="156" height="46" rx="8" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="314" y="260" text-anchor="middle" class="t-lab">관절 명령</text>'
    '<rect x="438" y="232" width="150" height="46" rx="8" fill="none" stroke="var(--accent)" stroke-width="1.8"/>'
    '<text x="513" y="252" text-anchor="middle" class="t-lab">인버스 다이내믹스</text>'
    '<text x="513" y="268" text-anchor="middle" class="t-sm">장면에서 행동 역산</text>'
    '<path d="M436 255 L394 255" class="flow"/>'
    '<path d="M234 255 L192 255" class="flow"/>'
    '<path d="M108 230 L108 212" class="flow" style="stroke-dasharray:5 4"/>'
    '<text x="120" y="226" class="t-sm">새 프레임이 쌓인다</text>'
    '</svg>')

FIG_SHARPA = (
    '<svg viewBox="0 0 640 270" role="img" '
    'aria-label="Sharpa의 두 층 구조">'
    '<rect x="210" y="16" width="220" height="46" rx="9" fill="none" stroke="var(--line)" stroke-width="1.5"/>'
    '<text x="320" y="37" text-anchor="middle" class="t-lab">사람 조종자</text>'
    '<text x="320" y="53" text-anchor="middle" class="t-sm">외골격 · 햅틱 · 발 페달 3개</text>'
    '<path d="M272 62 L165 96" class="flow"/>'
    '<path d="M370 62 L482 96" class="flow"/>'
    '<rect x="20" y="100" width="250" height="66" rx="9" fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>'
    '<text x="145" y="122" text-anchor="middle" class="t-lab">판단 — 무엇을 할 차례인가</text>'
    '<text x="145" y="138" text-anchor="middle" class="t-sm">VLA · 조종 데이터를 흉내 내 배운다</text>'
    '<text x="145" y="154" text-anchor="middle" class="t-sm">출력 하나가 「스킬 켜기」</text>'
    '<rect x="390" y="100" width="230" height="66" rx="9" fill="none" stroke="var(--accent)" stroke-width="1.8"/>'
    '<text x="505" y="122" text-anchor="middle" class="t-lab">반사 — 몸에 익어 바로 나가는 동작</text>'
    '<text x="505" y="138" text-anchor="middle" class="t-sm">강화학습으로 미리 구워 둔 정책</text>'
    '<text x="505" y="154" text-anchor="middle" class="t-sm">쥐기 · 축 기준 돌리기</text>'
    '<path d="M272 133 L388 133" class="flow"/>'
    '<text x="330" y="126" text-anchor="middle" class="t-sm">스킬 켜기 신호</text>'
    '<rect x="240" y="206" width="170" height="44" rx="9" fill="none" stroke="var(--line)" stroke-width="1.5"/>'
    '<text x="325" y="233" text-anchor="middle" class="t-lab">로봇 손</text>'
    '<path d="M145 166 L282 204" class="flow"/>'
    '<path d="M505 166 L370 204" class="flow"/>'
    '</svg>')


CARDS = [{
    'section': SEC_MODEL,
    'topic': ('infra', '모델 아키텍처'),
    'title': 'Rhoda AI는 VLA를 버렸고 Sharpa는 손안 조작만 따로 구웠다',
    'gain': '스텔스에서 나온 로봇 회사 둘이 같은 주에 공개한 방법을 나란히 놓고 봅니다. '
            '한쪽은 다음 장면을 상상해 행동을 역산하고, 다른 쪽은 사람이 조종하기 어려운 '
            '동작만 강화학습으로 미리 구워 둡니다. 두 방법이 각각 어떤 숫자를 내놓았는지, '
            '그리고 무엇을 안 밝혔는지까지.',
    'date': '2026-03-16',
    'meta': [WHO_YT, '2026-03-16', '23분', 'YouTube'],
    'links': [('▶ 원본 영상', VID, ''),
              ('📄 자막 기반 변환본',
               blob(BASE + '[260316] Rhoda AI 비디오 액션 모델과 Sharpa 손안 조작.md'), 'secondary'),
              ('📎 Sharpa MoDE-VLA 논문', PAPER, 'secondary')],
    'slim_oneliner': (
        '<b>서로 다른 회사 둘</b>을 한 편에서 견준다. Rhoda AI는 스텔스에서 막 나온 로봇 회사이고, '
        'Sharpa는 로봇 손을 만들어 온 회사다. Rhoda는 VLA(Vision-Language-Action, 시각·언어·행동 '
        '통합 모델)로는 범용성에 못 닿는다고 보고, 웹 비디오로 학습한 생성 모델이 다음 프레임을 '
        '예측하면 그 프레임을 역산해 관절 명령을 뽑는 방식을 택했다. Sharpa는 엔비디아 GTC 부스에서 '
        '사과 깎기를 걸고, 사람이 조종하기 가장 어려운 손안 조작만 강화학습 정책으로 미리 구워 발 '
        '페달에 붙였다. 진행자들은 어느 쪽이 맞는지 판정하지 않는다.'),
    'slim_points': [
        '<b>Rhoda의 학습량은 한쪽으로 심하게 쏠려 있다.</b> 웹 비디오 300년치로 사전학습한 다음 로봇 '
        '데이터는 11시간만 얹었다고 주장한다. 진행자들은 300년이라는 단위 자체가 이상하다고 먼저 짚는다.',
        '<b>다음 프레임을 시간 순서대로 하나씩 예측한다.</b> 보통의 비디오 생성은 정해진 길이의 영상을 '
        '양방향으로 만드는데, 이쪽은 지나간 프레임을 KV 캐시로 들고 가면서 LLM의 다음 토큰 예측처럼 '
        '다음 장면을 잇는다.',
        '<b>행동은 그 장면에서 거꾸로 계산해 나온다.</b> 비디오 모델은 그림만 그릴 줄 알지 관절은 '
        '모른다. 인버스 다이내믹스 모델(지금 장면과 다음 장면 두 장을 받아 그 사이를 만든 관절 '
        '움직임을 되짚는 모델)이 그 차이를 관절 명령으로 옮기고, 두 모델이 번갈아 돌아간다. '
        '지금 실행하는 행동은 앞서 예측해 둔 것이다.',
        '<b>야바위 데모가 시각 기억의 증거로 나온다.</b> 컵 아래 물건을 감추고 섞는 작업은 지금 이미지만 '
        '보는 VLA로는 원리상 못 푼다. Rhoda 쪽은 지나간 프레임을 전부 들고 있어 어느 컵인지 기억한다.',
        '<b>말을 안 쓰고 영상이 프롬프트 구실을 한다.</b> 사람이 몸으로 한 번 보여 주면 로봇이 따라 한다. '
        'LLM의 퓨샷 프롬프팅에서 예시가 하던 일을 영상이 대신하는 셈이다.',
        '<b>Rhoda는 정량 지표를 하나도 안 냈다.</b> 모델 파라미터도 초당 프레임 수도 밝히지 않았고 '
        '데모만 공개했다. 진행자 한 명은 "그냥 정량적인 거는 이게 다였어"라고 말한다.',
        '<b>Sharpa는 손안 조작만 떼어 강화학습으로 풀었다.</b> 적당한 힘으로 쥐는 데에는 정답 데이터가 '
        '없어 사람 시범으로 못 가르친다. 그래서 PPO(Proximal Policy Optimization, 잘한 행동 쪽으로 '
        '정책을 조금씩 미는 강화학습 방법)로 아이작 랩(엔비디아의 로봇 시뮬레이터. 로봇 수천 대를 '
        '동시에 돌린다)에서 정책 둘을 굽는다. 조종자는 발 페달 세 개로 그 스킬을 켜고, 모방학습 '
        '단계에서 페달을 누른 시점까지 배워 VLA의 출력 하나가 스킬 켜기가 된다.',
        '<b>효과는 성공률보다 데이터 수율에서 크게 드러난다.</b> 텔레오퍼레이션(사람이 장비를 걸치고 '
        '로봇을 직접 조종하는 것)만으로는 90회 중 31회만 학습에 쓸 수 있는데, 강화학습 정책을 켜면 '
        '89%가 쓸 만해진다. 사과 깎기 성공률 자체는 30%이고 π0 베이스라인은 0%다.',
    ],
    'figs': [
        (0, '두 회사는 무엇이 다른가', FIG_WHO,
         '<b>Rhoda AI</b>와 <b>Sharpa</b>는 서로 다른 회사다. 데이터를 모을 길이 막혔다는 사정은 '
         '같은데 푸는 자리가 갈린다. Rhoda는 학습 재료를 웹 비디오로 갈아 끼웠고, Sharpa는 사람이 '
         '조종하다 실패하는 구간만 기계에 넘겼다. 아래 두 그림이 각각의 속을 연다.'),
        (3, 'Rhoda는 어디를 갈아 끼웠나', FIG_DVA,
         '위 칸이 지금까지의 VLA다. 지금 이미지와 말을 한 모델에 넣어 관절 명령을 바로 낸다. '
         '아래 칸이 Rhoda다. <b>비디오 모델</b>이 다음 장면을 그리고, <b>인버스 다이내믹스</b>가 '
         '그 장면에서 행동을 거꾸로 계산한다. 실행한 결과가 프레임으로 다시 쌓여 다음 상상의 '
         '재료가 되고, 그 누적분이 야바위를 푸는 기억이다.'),
        (7, 'Sharpa는 반사에 해당하는 동작만 떼어 냈다', FIG_SHARPA,
         '사람이 몸 쓰는 방식을 그대로 옮겼다. <b>판단</b>은 무엇을 할 차례인지 정하는 몫이고, '
         '<b>반사</b>는 숙달돼서 생각하지 않고 나가는 동작이다. 오른손으로 사과를 깎는 동작은 VLA가 '
         '흉내 내 배우고, 손가락으로는 조종이 안 되는 쥐기와 돌리기는 강화학습 정책이 맡는다. 발 페달이 '
         '그 정책을 켜는 스위치이고, 페달을 누른 시점까지 VLA가 배워 나중에는 스스로 켠다. '
         '이 구조가 조종 성공률을 <b>90회 중 31회에서 89%로</b> 끌어올렸다.'),
    ],
    'slim_stats': [('300년 / 11시간', 'Rhoda의 웹 비디오 사전학습량과 로봇 데이터량'),
                   ('90회 중 31회', '순수 텔레오퍼레이션으로 건진 학습 데이터'),
                   ('89%', '강화학습 스킬을 켜고 조종했을 때의 수율'),
                   ('30% / 0%', 'Sharpa 사과 깎기 성공률과 π0 베이스라인')],
    'points': [
        '<b>규모부터 이례적이다.</b> Rhoda AI는 처음 보는 회사인데 4억 5천만 달러를 조달했고 '
        '밸류에이션이 11억 7천만 달러다. 시리즈 B로 1억 6천5백만 달러를 받은 Sunday Robotics보다 '
        '밸류에이션이 높다. 진행자들은 투자를 더 받는 것이 더 좋은 회사라는 뜻은 아니라고 선을 긋는다.',
        '<b>실시간을 어떻게 벌었는지가 공개 자료의 자랑거리다.</b> 비디오 생성은 느린데 로봇 제어는 '
        '실시간이어야 한다. 두 모델이 1초 안에서 교차하도록 짜고, 예측한 행동을 한 구간 뒤에 실행한다. '
        '진행자들은 이것을 리얼타임 청킹을 학습 단계로 끌어올린 것으로 읽는다.',
        '<b>예측과 실제가 어긋날 때의 처리는 안 나와 있다.</b> 공개 자료에 그림 한 장뿐이고 방법이 '
        '적혀 있지 않다. 진행자들이 가장 궁금해한 대목이다.',
        '<b>Sharpa의 조종 장비는 외골격에 햅틱 피드백과 발 페달을 붙였다.</b> 손가락으로는 흉내 내기 '
        '어려운 움직임을 사람이 직접 조종하면 실패가 잦아, 그 구간만 기계에 넘긴 구조다.',
        '<b>힘과 촉각은 뒤에서 주입한다.</b> π0 백본이 촉각 입력을 받지 않아, 액션 토큰이 나온 뒤에 '
        '관절 토크와 손끝 촉각 센서를 받는 작은 MoE 트랜스포머를 따로 학습해 잔차로 얹는다. '
        '진행자 한 명은 이 부분이 왜 필요한지 논문만으로는 모르겠다며 스킬 위계 쪽을 주된 기여로 본다.',
        '<b>사람의 반사 동작에 견준다.</b> 숙달된 사람이 생각하지 않고 하는 동작을 미리 구워 둔 스킬로 '
        '읽고, 손가락을 여섯 개 일곱 개로 늘리거나 전용 하드웨어를 붙여 사람이 못 하는 스킬을 만들 수도 '
        '있다는 상상까지 나아간다.',
    ],
    'stats': [('4억 5천만 달러', 'Rhoda AI 조달액'),
              ('11억 7천만 달러', 'Rhoda AI 밸류에이션'),
              ('1억 6천5백만 달러', 'Sunday Robotics 시리즈 B'),
              ('페달 3개', 'Sharpa 조종자가 강화학습 스킬을 켜는 입력')],
    'table': ('두 접근의 대조',
              ['', 'Rhoda AI (DVA)', 'Sharpa (MoDE-VLA)'],
              [['행동을 만드는 경로', '다음 프레임 상상 후 역산', 'VLA 액션 토큰에 힘·촉각 잔차 주입'],
               ['어려운 동작', '비디오 모델이 통째로 감당', '반사로 쓸 스킬을 미리 구움'],
               ['언어', '안 씀(영상이 프롬프트)', 'VLA 안에 있음'],
               ['데이터 병목을 푸는 자리', '웹 비디오 사전학습', '조종 수율 31/90에서 89%로'],
               ['공개된 정량 지표', '없음', '표 하나(30%, π0 0%)']]),
    'quote': '이게 정답이 아닐 수도 있죠. 근데 이게 됐다라는 걸 보여줬다는게 나는 굉장히 중요한 거 같아요.',
    'clash': [
        ('같은 채널 「Action Data Scaling 문제」',
         '기초 4강은 데이터를 모으는 경로 다섯을 늘어놓고 <b>어느 것도 스케일 문제를 푼다고 '
         '입증되지 않았다</b>고 닫는다. Rhoda의 웹 비디오 사전학습은 그 경로 가운데 월드모델과 '
         '역동역학 모델을 쓰는 다섯 번째의 변형인데, 이번 편에서도 성공률 숫자가 나오지 않았다. '
         '경로가 바뀐 것이지 입증이 된 것은 아니다.'),
        ('미국주식 사관학교 — VLA가 병목을 푸는 중이라는 전제',
         '<b>「로봇은 인건비가 아니라 설비투자 예산에서 팔린다」(2026-07-20)</b>는 VLA 모델과 영상 '
         '사전학습·시뮬레이션이 물리 데이터 부족을 <b>풀고 있다</b>는 전제 위에서 로봇 시장 규모를 '
         '추산한다. 이번 편의 두 회사는 그 전제에 각각 다르게 선다. Rhoda는 VLA로는 범용성에 못 닿는다며 '
         '아예 갈아탔고, Sharpa는 VLA를 쓰되 어려운 구간을 떼어냈다. 병목이 풀리는 중이라는 진술은 '
         '아직 방법이 정해지지 않았다는 뜻이기도 하다.'),
        ('성공률 30%를 어떻게 읽을 것인가',
         '사과 깎기 성공 판정 기준이 논문 밖에서는 확인되지 않는다. 베이스라인이 0%라는 대비가 커 보여도 '
         '<b>실험 표가 하나뿐</b>이고, 진행자들도 GTC 부스에서 실제로 그 시연을 할지 확신하지 않는다.'),
    ],
    'note': NOTE_YT,
}, {
    'section': SEC_BASE,
    'topic': ('infra', '용어 정의'),
    'title': 'Physical AI를 좁게 정의해야 하는 이유',
    'figs': [(2, '선을 어디에 긋는가', FIG_DEF,
              '왼쪽은 넓은 정의에만 드는 것들이다. 규칙과 모듈로 이미 10년 넘게 하던 일이라 '
              '이것까지 묶으면 새 이름을 붙일 이유가 없어진다. 오른쪽은 규칙 기반으로는 못 하던 '
              '일들이고, 필자는 <b>RT-2</b>가 나온 2023년 7월을 그 선으로 잡는다.')],
    'gain': '이 말을 넓게 쓰면 자율주행과 드론까지 들어와 10년 전 로보틱스와 구분이 안 됩니다. '
            '어디에 선을 그어야 하는지, 그 선을 언제 넘었는지.',
    'date': '2026-03-19',
    'meta': ESSAY_META,
    'links': elinks('Physical AI의 정의',
                    'https://sudoremove.com/knowledge/essays/fundamentals/definition/'),
    'oneliner': ('필자는 Physical AI를 "VLA(Vision-Language-Action, 시각·언어·행동 통합) 모델을 '
                 'end-to-end로 써서 규칙 기반으로는 불가능했던 범용 물리 작업을 해내는 시스템"으로 '
                 '좁게 잡자고 주장한다. 넓게 잡으면 이미 10년 전부터 있던 것들과 구분이 사라진다.'),
    'points': [
        '<b>용어의 출처는 엔비디아다.</b> 젠슨 황이 GTC 2024에서 꺼냈고 "로보틱스의 ChatGPT 순간이 곧 '
        '온다"고 예고했다.',
        '<b>경계선은 2023년 7월 RT-2다.</b> 구글 딥마인드가 웹 데이터와 로봇 데이터를 함께 학습하며 '
        '로봇의 동작을 언어 토큰처럼 다뤘다. 학습에 없던 물체로의 일반화, 추론을 거친 명령 수행, '
        '다단계 계획이 이때부터 열렸다.',
        '<b>증거는 예전엔 안 되던 작업이 된다는 것이다.</b> Physical Intelligence의 π0와 Figure의 '
        'Helix가 빨래 개기를 자율로 해냈다. 형태가 매번 달라지는 변형체라 로보틱스의 성배로 불리던 '
        '작업이다.',
        '<b>고전 로보틱스 진영도 넘어왔다.</b> 모듈형 구조와 MPC(모델 예측 제어)를 쓰던 보스턴 '
        '다이내믹스가 디퓨전 트랜스포머 기반 LBM(Large Behavior Model)을 만들고 있다.',
        '<b>이름만 바뀐 것이 아니라는 주장이다.</b> LLM·VLM 학습에서 넘어온 세계 지식을 물려받아, '
        '명시적으로 프로그래밍하지 않은 새 물체도 다룬다는 점을 근거로 든다.',
    ],
    'stats': [('2024', '젠슨 황이 GTC에서 용어를 꺼낸 해'),
              ('2023년 7월', '필자가 경계선으로 잡은 RT-2 공개 시점'),
              ('1시간', 'Figure AI가 무른 비닐 포장을 연속으로 다룬 시간')],
    'table': ('고전 로보틱스와 Physical AI',
              ['', '고전 로보틱스', 'Physical AI'],
              [['구조', '모듈형(인지·계획·제어 분리)', 'end-to-end 단일 모델'],
               ['동작 규정', '규칙 기반', '데이터 기반'],
               ['적용 범위', '도메인 한정', '범용'],
               ['사전 지식', '없음(직접 설계)', 'LLM·VLM에서 상속']]),
    'quote': '로보틱스의 ChatGPT 순간이 곧 온다.',
    'clash': [
        ('보스턴 다이내믹스의 전환을 어디까지 읽을 수 있나',
         '한 회사의 구조 변경을 업계 전체의 패러다임 이동 신호로 읽는 것은 <b>필자의 해석</b>이다. '
         '원문도 이를 추정으로 밝힌다.'),
        ('좁은 정의는 회사를 걸러 내는 잣대가 아니다',
         '정의를 좁히면 자율주행과 드론이 빠지는데, 이 분류는 <b>기술 계보를 가르는 것</b>이지 어느 '
         '시장이 더 크다는 판단이 아니다. 같은 페이지의 다른 카드가 시장 규모를 다룰 때 이 선을 '
         '그대로 옮겨 쓰면 안 된다.'),
    ],
    'note': NOTE_ESSAY,
}, {
    'section': SEC_BASE,
    'topic': ('infra', '용어 정의'),
    'title': 'VLA · LBM · RFM은 같은 말이 아니다',
    'figs': [(2, '한 줄로 이어진 계보와, 층위가 다른 이름 셋', FIG_TERMS,
              '위는 무엇을 입력으로 더해 왔는지의 순서다. 아래가 헷갈리는 대목인데, '
              '<b>VLA</b>와 <b>LBM</b>은 사실상 같은 것을 입력 쪽과 출력 쪽에서 각각 부른 '
              '이름이고, <b>RFM</b>은 그보다 한 칸 위에서 「여러 환경과 여러 과제를 한 모델이 '
              '감당한다」는 뜻이다. 계보의 VLA 자리가 아래 그림으로 이어진다.')],
    'gain': '뒤섞여 쓰이는 세 단어의 층위를 갈라 놓습니다. 그리고 언어에서 통한 방법이 '
            '몸에서는 왜 그대로 안 통하는지.',
    'date': '2026-03-19',
    'meta': ESSAY_META,
    'links': elinks('RFM & VLA란 무엇인가',
                    'https://sudoremove.com/knowledge/essays/fundamentals/what-is-rfm-vla/'),
    'oneliner': ('LLM에서 VLM으로, 다시 VLA로 이어지는 계보를 한 줄로 세우고 세 용어의 층위를 가른다. '
                 '언어에서 LLM이 해낸 범용화를 로봇의 몸에서 되풀이하려는 시도인데, 행동 데이터는 '
                 '인터넷에 없다는 점이 그 경로를 막는다.'),
    'points': [
        '<b>계보는 한 줄이다.</b> LLM(텍스트)에서 VLM(시각과 언어)으로, 다시 VLA(시각·언어·행동)로 '
        '이어진다. 최근에는 촉각을 더한 VTLA까지 나온다.',
        '<b>세 용어의 층위가 다르다.</b> VLA는 시각 인지·언어 지시·모터 동작을 한 모델에 넣은 것, '
        'LBM은 사실상 같은 것을 행동 출력 쪽에서 부르는 이름, RFM(Robot Foundation Model)은 그보다 위 '
        '개념으로 여러 환경과 여러 과제를 한 모델이 감당한다는 뜻이다.',
        '<b>특화형이 무너지는 지점이 있다.</b> 물체 형태가 매번 달라지는 빨래 개기, 쥐는 힘과 접촉 '
        '방식을 상황마다 조절해야 하는 무른 물건 다루기가 그렇다.',
        '<b>범용 로봇이 갖춰야 할 것은 세계 지식이다.</b> 물건은 떨어지고 물은 마르며 사람 말에는 '
        '생략된 맥락이 있다는 것을, 로봇이 별도 학습 없이 이미 알고 있어야 한다는 발상이다.',
        '<b>병목은 데이터의 존재 자체다.</b> 로봇이 물건을 집고 문을 열고 빨래를 개는 데이터는 '
        '인터넷에 없다. 텍스트를 인터넷 규모로 긁어 성공한 LLM의 경로를 그대로 밟을 수 없는 이유다.',
    ],
    'stats': [('3단계', 'LLM에서 VLM을 거쳐 VLA로 이어지는 계보'),
              ('VTLA', '촉각을 더해 최근 나온 네 번째 이름')],
    'quote': '언어의 LLM을 몸에서 되풀이한다.',
    'clash': [
        ('층위를 갈라도 회사들은 뒤섞어 쓴다',
         '필자가 정리한 구분은 <b>읽는 사람을 위한 정리</b>이고, 제품 발표에서는 같은 모델을 '
         'LBM이라고도 RFM이라고도 부른다. 이름으로 기술을 가르려 하면 어긋난다.'),
        ('같은 채널 「Rhoda AI」 편',
         'VLA를 계보의 도착점처럼 세워 두는 이 정리와 달리, 2026년 3월 편에서는 <b>VLA로는 범용성에 '
         '못 닿는다</b>며 비디오 생성으로 갈아탄 회사가 나온다. 계보가 한 줄이라는 서술은 다섯 달 만에 '
         '갈래를 하나 더 받았다.'),
    ],
    'note': NOTE_ESSAY,
}, {
    'section': SEC_BASE,
    'topic': ('infra', '전환 조건'),
    'title': '비전 AI가 걸어간 길을 로보틱스가 다시 걷는다',
    'figs': [(1, '같은 모양의 수렴이 두 번', FIG_PATH,
              '위는 이미 일어난 일이다. 분류·검출·분할마다 따로 있던 모델이 통합 VLM 하나로 '
              '모였다. 아래가 지금 벌어지는 일이고, 필자는 같은 모양으로 본다. 맨 아래 셋은 '
              '아래 화살표를 실제로 밀고 있는 것들이다 — 이 셋이 없으면 수렴은 비유로만 남는다.')],
    'gain': '과제별 특화 모델이 통합 모델로 수렴한 전례가 로봇에서 되풀이될 조건 셋. '
            '그리고 지금 어디까지 왔는지를 데이터셋 숫자로.',
    'date': '2026-03-19',
    'meta': ESSAY_META,
    'links': elinks('Specialist에서 Generalist로',
                    'https://sudoremove.com/knowledge/essays/fundamentals/specialist-to-generalist/'),
    'oneliner': ('분류·검출·분할마다 따로 있던 비전 모델이 통합 VLM 하나로 수렴한 경로를 로보틱스가 '
                 '그대로 밟고 있다고 본다. 그 전환을 떠받치는 조건으로 사전학습 VLM 백본, 교차 '
                 'embodiment 데이터셋, 스케일링 법칙 셋을 든다.'),
    'points': [
        '<b>특화형과 범용형의 차이가 환경에서 갈린다.</b> 특화형은 통제된 조건에서 성능이 높지만 환경이 '
        '조금만 달라져도 무너진다. 범용형은 학습에 없던 상황을 zero-shot(사전 예시 없이)이나 '
        'few-shot(예시 몇 개만으로) 처리한다.',
        '<b>조건 하나는 사전학습 VLM 백본이다.</b> PaliGemma·Qwen-VL·SmolVLM이 인터넷 규모 학습에서 '
        '얻은 상식을 이미 갖고 있어, 로봇이 기초부터 배울 필요가 없어졌다.',
        '<b>조건 둘은 교차 embodiment 데이터셋이다.</b> 서로 다른 로봇에서 모은 데이터를 함께 쓴다. '
        'Open X-Embodiment는 로봇 22종 이상, 과제 527개, 에피소드 100만 건을 넘는다.',
        '<b>조건 셋은 스케일링 법칙이다.</b> 모델이 커지고 데이터가 다양해질수록 일반화가 좋아진다는 '
        'LLM의 경험칙이 로봇에도 적용될 것으로 본다.',
        '<b>일반화 사례가 이미 나와 있다.</b> π0.5는 학습에 없던 환경에 적응하고, GR00T는 서로 다른 '
        '하드웨어를 오가며, SmolVLA는 4.5억 파라미터로 범용 수준의 성능을 낸다.',
        '<b>당분간의 절충은 파인튜닝이다.</b> 넓은 기반 모델에 과제별 미세조정을 얹어 특화형의 정밀도와 '
        '범용형의 유연성을 같이 가져간다. 웹 데이터·시뮬레이션·로봇 데이터를 함께 학습해 미세조정조차 '
        '필요 없게 만드는 것이 지향점이다.',
    ],
    'stats': [('22종 · 527과제 · 100만+', 'Open X-Embodiment 규모'),
              ('7종 · 500+ · 7만 6천', 'DROID 규모'),
              ('4.5억', 'SmolVLA 파라미터 수'),
              ('15종', '데이터셋이 포괄하는 휴머노이드 설계 수')],
    'table': ('교차 embodiment 데이터셋',
              ['데이터셋', '로봇 종류', '과제 수', '에피소드'],
              [['Open X-Embodiment', '22종 이상', '527', '100만+'],
               ['DROID', '7종', '500+', '7만 6천'],
               ['BridgeData V2', '1종', '13', '6만']]),
    'quote': '비전 AI가 걸어간 길.',
    'clash': [
        ('전례가 있다는 것이 되풀이된다는 뜻은 아니다',
         '비전 AI의 수렴을 로봇의 미래 지도로 쓰는 것이 이 글의 논법인데, 비전은 <b>인터넷에 이미 쌓인 '
         '이미지</b>로 스케일을 얻었다. 같은 채널의 4강이 못 박듯 행동 데이터는 그렇게 쌓여 있지 않다.'),
        ('에피소드 100만 건은 텍스트 규모가 아니다',
         'Open X-Embodiment가 이 분야에서 가장 큰 축인데도 <b>100만 건 단위</b>다. LLM이 다룬 토큰 '
         '규모와 견주면 스케일링 법칙을 그대로 옮겨 붙일 근거가 아직 얇다.'),
    ],
    'note': NOTE_ESSAY,
}, {
    'section': SEC_BASE,
    'topic': ('infra', '데이터 병목'),
    'title': '행동 데이터는 인터넷에 없다 — 이를 뚫으려는 다섯 경로',
    'figs': [(2, '병목 셋에서 갈라진 다섯 경로', FIG_PATHS5,
              '맨 위가 막는 것이고 다섯 갈래가 뚫으려는 방법이다. 갈래마다 무엇을 대신 쓰는지가 '
              '다르다 — 사람의 시간, 로봇 없는 도구, 시뮬레이터, 오픈소스, 그리고 인터넷에 이미 '
              '쌓인 영상이다. 맨 아래 점선이 이 글의 결론인데, 다섯 가운데 어느 것도 아직 '
              '입증되지 않았다.')],
    'gain': 'VLA가 LLM처럼 규모로 성능을 얻지 못하는 이유 셋과, 데이터를 모으려는 경로 다섯. '
            '테슬라가 조종자에게 건 신체 조건까지.',
    'date': '2026-03-19',
    'meta': ESSAY_META,
    'links': elinks('Action Data Scaling 문제',
                    'https://sudoremove.com/knowledge/essays/fundamentals/scaling-problem/'),
    'oneliner': ('행동 데이터가 인터넷에 없다는 사실, 실물 로봇을 돌려야 하는 평가 비용, 촉각 센싱과 '
                 '하드웨어 제조의 미완성이 규모 확대를 막는다고 정리한다. 이를 뚫으려는 수집 경로 '
                 '다섯을 늘어놓되 어느 쪽도 정답으로 판명되지 않았다고 닫는다.'),
    'points': [
        '<b>막는 것 하나는 데이터가 없다는 사실이다.</b> 행동 데이터는 인터넷에 존재하지 않는다. '
        '텍스트처럼 이미 쌓여 있는 것을 긁어오는 방식이 통하지 않고 물리적으로 직접 모아야 한다.',
        '<b>막는 것 둘은 평가 비용이다.</b> 실물 로봇을 돌려야 성능을 알 수 있고 하드웨어가 부서질 위험 '
        '때문에 자동 벤치마크를 못 돌린다. 개발 반복 속도가 여기서 직접 깎인다.',
        '<b>경로 하나는 텔레오퍼레이션이다.</b> 테슬라는 옵티머스 학습용 조종자를 시급 48달러에 뽑았고 '
        '키 170~180cm, 하루 7시간 이상 보행, 13kg 운반이라는 신체 조건을 걸었다. VR 장비를 오래 쓰면 '
        '피로와 멀미가 와서 조종 시간 자체가 한계다.',
        '<b>경로 둘은 UMI다.</b> 로봇 없이 사람이 들고 다니는 집게로 조작 데이터를 모으고, 그 데이터를 '
        '다른 로봇 플랫폼으로 옮긴다.',
        '<b>경로 셋은 시뮬레이션이다.</b> 엔비디아 Isaac GR00T가 합성 데이터를 만든다. 시뮬레이션과 '
        '현실의 차이를 메우는 것이 관건이다.',
        '<b>경로 넷은 커뮤니티다.</b> HuggingFace가 하드웨어와 소프트웨어를 오픈소스로 풀고 '
        '데이터·모델을 한곳에 모은다. SmolVLA가 그 가능성의 증거로 제시된다.',
        '<b>경로 다섯은 월드모델과 역동역학 모델이다.</b> 1X Technologies가 레이블 없는 영상에서 행동을 '
        '역으로 뽑아낸다. 인터넷에 쌓인 사람 행동 영상을 데이터원으로 바꾸려는 시도다.',
        '<b>결론은 미정이다.</b> 다섯 경로 가운데 어느 것도 규모 문제를 푼다고 입증되지 않았다.',
    ],
    'stats': [('시급 48달러', '테슬라 옵티머스 학습용 조종자 임금'),
              ('170~180cm', '조종자 신체 조건 중 키'),
              ('13kg', '조종자에게 요구한 운반 중량'),
              ('5개', '필자가 정리한 데이터 수집 경로 수')],
    'table': ('LLM과 VLA의 대조',
              ['', 'LLM', 'VLA'],
              [['데이터원', '인터넷(사실상 무한)', '실물 로봇 동작(제한)'],
               ['수집 비용', '낮음', '높음'],
               ['평가', '자동', '실물 로봇 필요']]),
    'quote': '인터넷에 없는 데이터.',
    'clash': [
        ('같은 채널 「Rhoda AI」 편이 다섯 번째 경로를 밀고 나갔다',
         '2026년 3월 편의 Rhoda AI는 <b>웹 비디오 300년치</b>로 사전학습하고 로봇 데이터를 11시간만 '
         '얹었다고 주장한다. 이 글이 미정으로 남긴 경로가 같은 달에 자금 4억 5천만 달러를 받아 '
         '제품이 됐다. 다만 성공률 숫자는 여전히 공개되지 않았다.'),
        ('조종자 조건은 채용 공고이지 병목의 크기가 아니다',
         '시급 48달러와 신체 조건은 <b>한 회사의 채용 문서</b>에서 나온 값이다. 이것으로 산업 전체의 '
         '데이터 수집 단가를 추산하면 표본이 하나다.'),
    ],
    'note': NOTE_ESSAY,
}]

# ── 카드 파일 모으기 ──────────────────────────────────────────────────
# 영상 하나 = 파일 하나(scratchpad/cards_sudo/<영상ID>.py 안의 CARD).
# 서른 장을 이 파일 하나에 쌓으면 손을 못 댄다. 위 CARDS는 처음 다섯 장이고,
# 나머지는 여기서 긁어 모은다. 카드 파일은 섹션을 문자열 id로만 적는다.
import glob as _glob

# 카드 파일은 dict 하나만 들고 있고 그림은 여기서 붙인다 — 상자·화살표 helper 가 이 파일에만
# 있어서, 카드 파일마다 SVG 를 베껴 넣으면 좌표 규칙이 갈라진다. 열쇠는 영상 ID다.
EXTRA_FIGS = {
    '0i5gjyiG3Rc': [(3, '같은 재료에서 갈린 세 갈래', FIG_GTC,
                     '다섯 편이 쓴 재료는 같다. 갈라지는 자리는 그 영상을 무엇으로 바꾸느냐다 — '
                     '<b>월드모델</b>은 다음 장면을 그리고, <b>VLA</b>는 손가락 관절값을 직접 뽑고, '
                     '<b>비디오 액션모델</b>은 영상 생성 모델을 통째로 파인튜닝한다. 아래 점선 둘은 '
                     '각 갈래가 지금 치르는 값이다.')],
    'cG_eCvQoZOw': [(2, '300년과 170년은 같은 자가 아니다', FIG_YEARS,
                     '두 회사 다 「몇 년치」로 데이터 규모를 말하는데 세는 대상이 다르다. '
                     'Rhoda 쪽은 <b>인터넷에 이미 있던 영상</b>이라 로봇 손이 나오지 않고, Dyna-2 쪽은 '
                     '<b>손목 좌표를 뽑으려고 새로 찍은 영상</b>이다. 단위가 같다고 견줄 수 있는 것은 '
                     '아니다.')],
    'vQ6ckZEyqbY': [(3, '로봇을 쓰느냐 안 쓰느냐', FIG_3CO,
                     '위 두 회사는 사람이 장치를 끼고 움직인 것을 찍어 로봇 관절값으로 옮겨 심는다. '
                     '아래 한 회사는 사람이 로봇을 직접 조종한 데이터를 그대로 쓴다. '
                     '<b>제목의 「없이」가 갈라지는 자리</b>가 여기다.')],
    '7iwWNj1yg9g': [(3, '손 넷을 같은 자로 잰다', FIG_HANDS,
                     '자유도만 놓고 고르면 Sharpa가 앞서는데, 무게와 값을 같이 놓으면 순위가 흔들린다. '
                     'Tesollo는 값이 <b>6분의 1</b>이면서 웬만한 과제를 해내고, Alex는 손끝 힘이 '
                     '<b>40N</b>으로 가장 세다. 어느 손이 좋은지는 무엇을 시키느냐로 갈린다.')],
}

CARDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards_sudo')


def load_extra():
    out = []
    for p in sorted(_glob.glob(os.path.join(CARDS_DIR, '*.py'))):
        if os.path.basename(p).startswith('_'):
            continue
        ns = {}
        exec(compile(io.open(p, encoding='utf-8').read(), p, 'exec'), ns)
        c = ns.get('CARD')
        assert isinstance(c, dict), '%s 에 CARD dict 가 없다' % p
        assert c.get('date'), '%s 에 date 가 없다 — 섹션 안 정렬 기준이다' % p
        sid = c['section']
        assert sid in SEC, '%s 의 섹션 id를 모른다: %r' % (p, sid)
        c['section'] = SEC[sid]
        f = EXTRA_FIGS.get(os.path.basename(p)[:-3])
        if f:
            c['figs'] = f
        out.append(c)
    return out


def order(cards):
    """섹션은 SEC_ORDER 순서로, 섹션 안은 업로드일 역순(최신이 위)."""
    idx = {c['section'][0]: SEC_ORDER.index(c['section'][0]) for c in cards}
    return sorted(cards, key=lambda c: (idx[c['section'][0]],
                                        [-int(x) for x in (c.get('date') or '0-0-0').split('-')]))


CARDS = order(CARDS + load_extra())

HEADER = '''  <header>
    <p class="eyebrow">sudoremove — 로보틱스 · 피지컬 AI 해설</p>
    <h1>수도리무브</h1>
  </header>'''

META = '''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d건</b></span>
      <span>원문 기간 <b>2026-03-16 ~ 03-19</b></span>
      <span>소스 <b>sudoremove.com · YouTube</b></span>
    </div>''' % (STAMP, len(CARDS))

LEDE = ('<p class="lede">로봇이 몸으로 하는 일을 학습으로 푸는 흐름을 따라가는 페이지입니다. '
        '공개 웹 에세이와 유튜브 해설을 같이 담고, 원문은 싣지 않고 <b>요약과 대조만</b> 남깁니다. '
        '카드마다 반론을 붙여 한 편만 읽고 결론이 나지 않게 했습니다.</p>')

FOOTER = (LEDE + META + '\n제3자 해설 요약 아카이브 · 원문은 싣지 않습니다. 투자 추천이 아닙니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_sudoremove_dashboard.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

if __name__ == '__main__':
    dc.render(CARDS, '수도리무브 — 로보틱스 · 피지컬 AI', HEADER, FOOTER, OUT)
