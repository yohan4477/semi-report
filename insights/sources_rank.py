# -*- coding: utf-8 -*-
"""출처 등급 — 이 숫자에 대해 누가 1차 관측자인가.

**등급은 출처 속성이 아니라 (출처 × 주제) 속성이다.** SemiAnalysis가 한국 부동산
세제를 말하면 1차가 아니고, 전 한국은행 국장이 HBM 수율을 말해도 1차가 아니다.
전역 순위표를 만들면 그게 첫 오답이 된다.

  관측  직접 재거나 현장에서 본 것 — 벤치마크·전력 계측, 정책 내부 경험, 본인 발언
  해석  1차 자료를 읽고 푸는 쪽 — 공시 분석, 통계 해설
  전달  남의 말을 옮기는 쪽 — 방송 발언 인용, 출처를 안 밝힌 총계

**등급이 결론을 정하지 않는다.** 관측이 해석을 항상 이기지도 않는다 — 보증 카드에서
SemiAnalysis는 수익률 25.4% 대 40.7%를 재고 회계사는 장부 밖 의무 3조 달러를 센다.
둘은 같은 것을 두고 싸우는 게 아니라 다른 것을 센다. 등급은 「누가 더 가까이서 봤나」를
글에 쓰게 만드는 재료지, 판정이 아니다.

모르면 낮게 잡는다 — 표에 없는 (출처, 섹션) 짝은 전부 전달이다.
"""

OBS, INT, REL = '관측', '해석', '전달'
MARK = {OBS: '●', INT: '◑', REL: '○'}
SLUG = {OBS: 'obs', INT: 'int', REL: 'rel'}
ORDER = (OBS, INT, REL)

# (경로 접두어, 부르는 이름, {섹션: 등급}, 그 밖의 섹션 기본값)
# 접두어가 긴 것이 먼저 맞는다.
SOURCES = [
    ('content/newsletter/ai_infra', 'SemiAnalysis 뉴스레터',
     {'chip': OBS, 'power': OBS, 'model': OBS, 'biz': OBS, 'winner': OBS}, REL),
    ('content/newsletter/ai_models', 'SemiAnalysis 뉴스레터',
     {'model': OBS, 'chip': OBS, 'biz': INT}, REL),
    ('content/newsletter/semiconductors', 'SemiAnalysis 뉴스레터',
     {'chip': OBS, 'power': OBS, 'model': OBS, 'biz': OBS}, REL),
    ('content/podcast', 'SemiAnalysis 팟캐스트',
     {'chip': OBS, 'power': OBS, 'model': OBS, 'biz': OBS}, REL),
    # 본인이 쓴 게시물이라 발언 자체는 1차다. 카드화는 나중에 한다
    ('content/linkedin', 'SemiAnalysis 게시물', {}, OBS),
    ('content/understanding/류상철 국장', '류상철 · 전 한국은행 국장',
     {'market': OBS, 'energy': INT}, REL),
    ('content/understanding/권효재 대표', '권효재 · COR에너지인사이트 대표',
     {'energy': OBS, 'power': INT}, REL),
    # 기자는 취재로 1차를 물어 온다 — 담당 영역에서는 관측이고 그 밖은 해석이다.
    # 순위는 TIER 가 따로 매긴다(전 한국은행 국장 다음).
    ('content/understanding/김상훈 기자', '김상훈 기자',
     {'market': OBS, 'chip': INT}, REL),
    ('content/understanding/백종훈 기자', '백종훈 기자',
     {'chip': OBS}, REL),
    ('content/understanding/손진석 기자', '손진석 기자',
     {'market': OBS, 'energy': INT}, REL),
    # 공시를 직접 읽어 센다 — 3조 달러 오프발란스가 그렇게 나온 숫자다
    ('content/understanding/회계사', '엘곰 · 회계사',
     {'biz': INT}, REL),
    ('content/understanding/부동산', '부동산 해설',
     {'estate_price': INT, 'estate_project': INT, 'estate_supply': INT}, REL),
    ('content/understanding/언더스탠딩 백브리핑', '언더스탠딩 백브리핑',
     {'energy': INT}, REL),
    ('content/understanding/빌 애크먼', '빌 애크먼',
     {'market': OBS}, REL),
    # 남의 말을 옮기는 자리가 많다 — 아이스먼 CNBC 발언, 산출 주체 없는 8,000억 달러
    ('content/understanding/미국주식 사관학교', '미국주식 사관학교', {}, REL),
    ('content/understanding/이선엽 대표', '이선엽 · AFW파트너스 대표', {}, REL),
]

DEFAULT = REL

# 우선순위 — 등급과 다른 축이다.
# 등급(관측·해석·전달)은 그 숫자에서 얼마나 가까운가를 잰다.
# 우선순위는 둘이 같은 것을 두고 부딪칠 때 누구를 먼저 두는가다.
# 기자를 관측으로만 적으면 SemiAnalysis 와 같은 급이 되어 순서가 사라진다.
# 숫자가 작을수록 앞선다. 표에 없으면 9다.
TIER = {
    'SemiAnalysis 뉴스레터': 1,
    'SemiAnalysis 팟캐스트': 1,
    'SemiAnalysis 게시물': 1,
    '류상철 · 전 한국은행 국장': 1,
    '김상훈 기자': 2,
    '백종훈 기자': 2,
    '손진석 기자': 2,
}
TIER_DEFAULT = 9


def tier_of(path):
    name, _bysec, _d = source_of(path)
    return TIER.get(name, TIER_DEFAULT)


def _norm(p):
    return (p or '').replace('\\', '/')


def source_of(path):
    """(부르는 이름, 섹션별 등급표, 기본 등급) — 접두어가 긴 것이 먼저 맞는다."""
    p = _norm(path)
    best = None
    for pref, name, bysec, dflt in SOURCES:
        if p.startswith(pref) and (best is None or len(pref) > len(best[0])):
            best = (pref, name, bysec, dflt)
    if not best:
        return None, {}, DEFAULT
    return best[1], best[2], best[3]


def rank_of(path, section):
    name, bysec, dflt = source_of(path)
    return bysec.get(section, dflt)


def mark_of(path, section):
    return MARK[rank_of(path, section)]


def tally(paths, section):
    """등급별 편수 — 합류도 칸이 무엇으로 서 있는지를 세는 데 쓴다."""
    out = dict((r, 0) for r in ORDER)
    for p in paths:
        out[rank_of(p, section)] += 1
    return out
