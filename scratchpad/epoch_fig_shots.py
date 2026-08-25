# -*- coding: utf-8 -*-
"""Epoch AI 장의 도해 — 원문에 화면 캡처로 실린 그림을 한국어 인라인 SVG로 다시 짠다.

원문 여섯 장 가운데 넷은 채용 사이트·정부 안내문의 화면 캡처이고, 하나는 옛 책에
실린 삽화다. 캡처를 픽셀로 흉내 내지 않는다 — 그 화면이 담은 내용을 상자와 목록으로
다시 짠다. 로고와 브랜드 표시는 그리지 않고, 어느 회사의 어떤 공고인지는 글자로 밝힌다.
공고 문구는 원문 그림에 보이는 것만 옮긴다.

부품과 한 벌(선 굵기·색·글자 class)은 scratchpad/epoch_fig.py 를 그대로 쓴다.
검사는 scratchpad/check_fig.py.
"""
import math

import epoch_fig as ef

SX, SW = 16, 608                      # 화면 테두리의 왼쪽 끝과 너비
TX = SX + 18                          # 화면 안 글자의 왼쪽 맞춤 자리
GOOD = 'var(--fig-good,#2f8f6b)'


# ── 화면을 다시 짜는 부품 ────────────────────────────────────────────────
def txt(x, y, s, cls='t-sm', style='', anchor=None, fs=None):
    """글자 한 줄. class 없는 <text>는 두지 않는다(한 벌 규칙)."""
    st = style
    if fs:
        st = ('font-size:%spx;' % fs) + st
    a = ' text-anchor="%s"' % anchor if anchor else ''
    return ('<text x="%d" y="%d" class="%s"%s%s>%s</text>'
            % (x, y, cls, a, ' style="%s"' % st if st else '', ef.esc(s)))


def line_fit(s, fs, limit):
    """글자 폭을 재서 화면 밖으로 나가면 그 자리에서 멈춘다."""
    assert ef.w(s, fs) < limit, '줄이 화면을 넘는다(%.0f px): %s' % (ef.w(s, fs), s)
    return s


def screen(y, h):
    """공고·안내문 한 화면을 감싸는 테두리."""
    return '<rect x="%d" y="%d" width="%d" height="%d" rx="10" class="bx"/>' % (SX, y, SW, h)


def sec(y, s):
    """절 제목 — 원문 화면이 파란 세로 막대로 표시하던 자리."""
    return ('<rect x="%d" y="%d" width="4" height="14" rx="2" fill="%s"/>'
            % (TX, y - 12, GOOD)) + txt(TX + 12, y, s, 't-lab')


def rule(y):
    return ('<path d="M%d %d L%d %d" stroke="var(--line,#d8d8d8)" stroke-width="1" '
            'fill="none"/>' % (SX + 16, y, SX + SW - 16, y))


def rows(y, lines, step=19, x=TX, cls='t-sm'):
    """목록 여러 줄. 마지막 줄의 기준선을 함께 돌려준다."""
    o = []
    for s in lines:
        o.append(txt(x, y, line_fit(s, 13.5, SX + SW - 8 - x), cls))
        y += step
    return o, y - step


def notes(y, lines):
    """판 아래 주석. 폭을 넘는 줄은 잘라서 다음 줄로 내린다."""
    flat = []
    for s in lines:
        flat += ef.wrap_lines(s, 636 - SX, 13)
    return [ef.lab(SX, y + 18 * i, t, fs=13) for i, t in enumerate(flat)]


# ── ① 딥시크 데이터센터 직무 공고 ────────────────────────────────────────
def cn_shot_dc():
    """스타트업이 자체 데이터센터를 짓기 시작했다는 증거로 원문이 실은 공고 화면."""
    o = [ef.lab(SX, 22, '딥시크가 채용 사이트에 올린 공고 화면. 글자는 한국어로 옮겼다', fs=13)]
    o.append(screen(34, 346))
    o.append(txt(TX, 66, 'IDC 설계기획 엔지니어', 't-lab', fs=15))
    o.append('<rect x="502" y="48" width="100" height="28" rx="14" fill="%s"/>' % GOOD)
    o.append(txt(552, 66, '직무 지원', 't-sm', style='font-weight:850;fill:#fff',
                 anchor='middle'))
    o.append(txt(TX, 90, '정규직 · 기타 · DeepSeek · 저장성 항저우시', 't-sm t-axis'))
    o.append(rule(108))
    o.append(sec(132, '직무 설명'))
    o.append(txt(TX, 158, '담당 업무 — 당신이 맡을 일', 't-sm', style='font-weight:850'))
    body, _ = rows(178, [
        '1. 데이터센터 단지·전산실 기획과 기반시설 아키텍처 설계에 참여한다',
        '2. 전력·냉각·랙·네트워크 기반시설 방안을 심의하고 최적화한다',
        '3. 액체냉각·고밀도 배전·모듈러 건설·지능형 운영 등 새 기술 노선을 연구·평가한다',
        '4. 설계 규범·기술 표준·장비 선정 전략·용량 계획안을 낸다',
        '5. 설계원·장비 제조사·건설팀·운영팀과 함께 프로젝트 인도를 밀고 나간다',
        '6. 세계 데이터센터·AI 기반시설 업계 동향을 연구해 건설 기준을 계속 다듬는다',
        '7. 비용·신뢰성·에너지 효율·확장성 지표를 따로 분석하고 방안을 최적화한다'])
    o += body
    o.append(txt(TX, 308, '자격 요건 — 갖추길 바라는 것', 't-sm', style='font-weight:850'))
    body2, _ = rows(328, [
        '1. 학사 이상, 경력 무관, 전기/공조/환경/토목 등 관련 전공',
        '2. 탄탄한 공학 기초 지식과 시스템적 사고력. 기술 규범·도면을 읽으면 가산점',
        '3. 강한 논리 분석력과 문제 분해 능력'])
    o += body2
    o += notes(402, ['빌린 서버가 아니라 지을 건물을 두고 뽑는 자리다 — 전력·냉각·랙·용량 계획이 '
                     '담당 업무에 들어 있다',
                     '경력을 묻지 않는다. 「경력 무관」이 자격 요건 첫 줄에 그대로 적혀 있다'])
    return ef.svg(428, ''.join(o))


# ── ② Z.ai 미국 시장 개척 직무 공고 ──────────────────────────────────────
def cn_shot_bd():
    """누구에게 파는가가 적힌 공고. 표적은 포춘 글로벌 500대 기업이다."""
    o = [ef.lab(SX, 22, 'Z.ai(지푸)가 올린 미국 시장 개척 직무 공고 화면', fs=13)]
    o.append(screen(34, 182))
    o.append(txt(TX, 66, 'Business Development—America', 't-lab', fs=15))
    o.append(txt(TX, 90, '베이징 · 정규직 · 인터넷 / 전자 / 온라인게임', 't-sm t-axis'))
    o.append(rule(108))
    o.append(sec(132, '직무 설명'))
    body, _ = rows(160, [
        '1. 포춘 글로벌 500대 다국적 기업을 겨냥한 Zhipu AI LLM 제품 사업을 넓힌다.',
        '   생성형 AI 솔루션 컨설팅을 제공해 다국적 기업의 생성형 AI 전환을 앞당긴다.',
        '   고객과 장기간 이어질 전략적 파트너십을 맺는다.'], step=18)
    o += body
    key, _h = ef.box(SX, 234, SW, '이 자리가 노리는 고객',
                     ['포춘 글로벌 500대 다국적 기업 — 미국 시장 개척 직무가 여기를 겨냥한다'],
                     key=True)
    o.append(key)
    o += notes(303, ['제목도 본문도 영어로 적힌 공고다. 중국 안에서 뽑되 파는 곳은 미국이라는 뜻이다',
                     'Z.ai는 정부기관과 국유기업도 표적 고객으로 적어 두고 있다'])
    return ef.svg(330, ''.join(o))


# ── ③ 딥시크 Agent Harness R&D Engineer 공고 ────────────────────────────
def cn_shot_agent():
    """영어가 많이 섞여 있어 중국어를 몰라도 무슨 일인지 읽히는 공고.

    그래서 영어로 적힌 말은 옮기지 않고 그대로 둔다 — 옮기면 이 그림의 요지가 사라진다."""
    o = [ef.lab(SX, 22, '딥시크 「Agent Harness R&D Engineer」 공고 화면. 영어로 적힌 말은 '
                        '원문 그대로 뒀다', fs=13)]
    o.append(screen(34, 340))
    o.append(sec(62, '팀 사명'))
    o.append('<rect x="%d" y="76" width="252" height="34" rx="8" class="bx-key"/>' % TX)
    o.append(txt(TX + 126, 98, 'Model + Harness = Agent', 't-lab', fs=13, anchor='middle'))
    body, _ = rows(130, [
        'DeepSeek 의 최전선 모델 능력을 앞서가는 Agent 제품으로 바꾸는 중이다.',
        '모델 자체를 뺀 나머지 모든 일이 Harness 의 범주다.',
        'Harness 팀에서 엔지니어·연구원·프로덕트 매니저와 함께 DeepSeek 데스크톱 Agent',
        '제품 연구개발 전 과정에 참여하고, DeepSeek 이 Harness 를 이해하는 방식을 정한다.'],
        step=18)
    o += body
    o.append(sec(214, '주요 담당 업무'))
    body2, _ = rows(236, [
        '· DeepSeek Harness 제품의 기술 아키텍처와 기술 선정 설계에 참여한다.',
        '· DeepSeek Harness 제품을 개발한다.',
        '· 연구원과 함께 Harness 영역의 최전선 혁신을 정의하고 구현한다.',
        '· 모델 학습팀 엔지니어·연구원과 깊이 협력해 모델과 Harness 가 함께 진화하도록,',
        '  Harness 쪽에서 모델과의 깊은 정합을 이룬다.',
        '· 사내 실제 업무를 Harness 제품과 모델 능력 학습의 피드백원으로 삼아 고쳐 나간다.',
        '· 팀이 모은 사용자 피드백을 분석하고 Harness 사용자 커뮤니티 유지를 돕는다.',
        '· 프로젝트 관리 관련 업무를 돕는다.'])
    o += body2
    o += notes(396, ['Model·Harness·Agent·DeepSeek 은 원문에도 영어다. 중국어를 못 읽어도 무슨 '
                     '일인지 대강 읽힌다',
                     '스타트업 공고는 이렇게 LLM과 그 위의 제품에 좁게 몰려 있다'])
    return ef.svg(422, ''.join(o))


# ── ④ 미국 고용평등위원회 안내문 ─────────────────────────────────────────
def cn_shot_law():
    """경력 연수로 지원자를 거르면 법에 걸릴 수 있다는 대목."""
    o = [ef.lab(SX, 22, '미국 고용평등위원회(EEOC)가 낸 안내문 화면', fs=13)]
    o.append(screen(34, 222))
    o.append(txt(TX, 66, 'Job Advertisements — 채용 광고', 't-lab', fs=15))
    o.append(rule(86))
    body, _ = rows(112, [
        '고용주가 지원자의 인종·피부색·종교·성별(트랜스젠더 정체성·성적 지향·임신 포함),',
        '출신 국가, 나이(만 40세 이상), 장애, 유전 정보를 이유로 어느 쪽을 선호하거나',
        '지원을 단념시키는 채용 광고를 내는 것은 위법이다.'], step=18)
    o += body
    key, _h = ef.box(SX + 16, 172, SW - 32, '예를 들어', [
        '「여성」이나 「최근 대학 졸업자」를 찾는 구인 광고는 남성과 40세 넘는 사람의',
        '지원을 단념시킬 수 있고, 법을 어길 수 있다.'], key=True)
    o.append(key)
    o += notes(278, ['경력이 아니라 신졸을 겨냥해 뽑는 방식이 미국에서는 이 대목에 걸릴 수 있다',
                     '중국 랩은 요구 최소 경력 평균이 1.6년, 미국 랩은 5.5년이다'])
    return ef.svg(304, ''.join(o))


# ── ⑤ 클라크의 정지궤도 통신위성 셋 ──────────────────────────────────────
# 위성도 범위도 셋이다. 개수가 곧 값이라 다른 개수를 그리면 그림이 거짓이 된다.
EX, EY, ER = 320, 200, 38             # 지구
ORX, ORY = 270, 118                   # 정지궤도 타원
SATS = (-95, 30, 160)                 # 위성 셋이 앉은 각도


def _on(r_x, r_y, deg):
    return (EX + r_x * math.cos(math.radians(deg)), EY + r_y * math.sin(math.radians(deg)))


def _arc(r, a0, a1):
    x0, y0 = _on(r, r, a0)
    x1, y1 = _on(r, r, a1)
    big = 1 if abs(a1 - a0) > 180 else 0
    return 'M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f' % (x0, y0, r, r, big, x1, y1)


def _beam(sx, sy, deg, up):
    """위성과 지표면을 잇는 전파 링크. up이면 지상에서 위성으로 올라간다."""
    gx, gy = _on(ER, ER, deg)
    if up:
        # 화살촉이 위성 동그라미에 먹히지 않게 11px 앞에서 끊는다
        dx, dy = sx - gx, sy - gy
        d = math.hypot(dx, dy)
        a, b = (gx, gy), (sx - dx / d * 11, sy - dy / d * 11)
    else:
        a, b = (sx, sy), (gx, gy)
    return ('<path d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="3" '
            'marker-end="url(#fig-arrow-a)"/>' % (a[0], a[1], b[0], b[1], GOOD))


def clarke_sat():
    pos = [_on(ORX, ORY, d) for d in SATS]
    o = []
    # 범례 — 선 세 벌의 뜻을 판 위쪽에서 밝힌다
    o.append('<path d="M16 18 L36 18" fill="none" stroke="%s" stroke-width="3" '
             'marker-end="url(#fig-arrow-a)"/>' % GOOD)
    o.append(ef.lab(42, 22, '지상에서 올라간 신호를 위성이 내려 쏜다', fs=13))
    o.append(ef.arrow('svc', [(310, 18), (330, 18)]))
    o.append(ef.lab(336, 22, '위성끼리 신호를 넘긴다', fs=13))
    o.append('<path d="M16 36 L36 36" fill="none" stroke="%s" stroke-width="6" '
             'opacity=".38" stroke-linecap="round"/>' % GOOD)
    o.append(ef.lab(42, 40, '위성 하나가 덮는 범위 — 반구 하나', fs=13))
    # 정지궤도 — 값이 아니라 기준선이라 점선 1.2다
    o.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="var(--ink-3)" '
             'stroke-width="1.8" stroke-dasharray="6 4"/>' % (EX, EY, ORX, ORY))
    # 지구
    o.append('<circle cx="%d" cy="%d" r="%d" fill="var(--fig-body,rgba(127,127,127,.30))" '
             'stroke="var(--ink-3)" stroke-width="1"/>' % (EX, EY, ER))
    o.append(txt(EX, EY + 4, '지구', 't-lab', anchor='middle'))
    # 각 위성이 덮는 반구 — 반지름을 달리해 셋이 겹치는 것이 보이게 한다
    for r, deg in zip((52, 66, 80), SATS):
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="6" opacity=".38" '
                 'stroke-linecap="round"/>' % (_arc(r, deg - 90, deg + 90), GOOD))
    # 위성끼리 잇는 중계 링크
    for i in range(3):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % 3]
        o.append('<path d="M%.1f %.1f L%.1f %.1f" class="flow-svc"/>' % (x1, y1, x2, y2))
    # 지상 링크 — 하나는 올라가고 둘은 내려온다
    for (sx, sy), deg, up in zip(pos, SATS, (False, False, True)):
        o.append(_beam(sx, sy, deg, up))
    for (sx, sy) in pos:
        o.append('<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (sx, sy, GOOD))
    o.append(txt(297, 64, '중계 위성', 't-role', anchor='middle'))
    o.append(txt(554, 285, '중계 위성', 't-role', anchor='middle'))
    o.append(txt(52, 274, '중계 위성', 't-role', anchor='middle'))
    o.append(txt(EX, 332, '정지궤도 — 적도 위 고정된 자리', 't-role', anchor='middle'))
    o += notes(352, ['지상 송신소에서 올라간 라디오·TV·전화 신호를 위성 셋이 나눠 다시 뿌린다',
                     '위성 하나가 반구 하나를 내려다본다. 적도 위 고정된 자리에 셋을 두면 '
                     '빈 곳이 거의 없다',
                     '아서 C. 클라크가 내놓은 구상이다. 실제로 이렇게 되기까지 약 19년이 걸렸다'])
    return ef.svg(398, ''.join(o))


FIGS = {
    'cn_shot_dc': cn_shot_dc,
    'cn_shot_bd': cn_shot_bd,
    'cn_shot_agent': cn_shot_agent,
    'cn_shot_law': cn_shot_law,
    'clarke_sat': clarke_sat,
}
