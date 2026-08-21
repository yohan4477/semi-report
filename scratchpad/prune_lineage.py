# -*- coding: utf-8 -*-
# 계보 마디 가지치기.
#
# extract_lineage.py가 뽑은 절 후보에는 과다검출이 섞여 있다. 본문에 FP4가 한 번
# 스치면 정밀도 궤도로 끌려오는 탓에 「전력 예산과 BOM」·「데이터센터 램프업」 같은
# 절이 들어왔다. 계보 마디의 조건은 하나다 — 절 제목 자체가 기전(機轉)을 말할 것.
# 벤치마크 결과·비용 비교·공급망은 그 기전이 낳은 값이지 기전이 아니다.
#
# 규칙만으로 안 갈리는 자리가 남아 예외 목록을 둔다. 「정적 컴파일의 대가」는 값이
# 아니라 마디이고(빠른 대신 무엇을 냈나), 「Day 0 참사」는 마디가 아니라 사건이다.
import os, re, json, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'C:/Users/y/semianalysis'

# 제목에서 기전을 가리키는 표지. 궤도 판정도 제목으로만 다시 한다.
# si에서 '비동기'를 뺐다 — 「동기식에서 비동기식으로」는 실리콘이 아니라 학습 계보다.
HEAD_RAILS = [
 ('attn', '어텐션', 'MLA|GQA|MQA|MHA|어텐션|attention|DeltaNet|KDA|Delta Attention|RoPE|KV 캐시|CSA|HCA|AFD|선형'),
 ('moe',  '전문가',  'MoE|전문가|부하 분산|Quantile|MegaMoE|LatentMoE|WideEP|Wide EP'),
 ('dec',  '디코딩',  'MTP|투기|추측 디코딩|speculative|멀티토큰|멀티 토큰|multi-token'),
 ('prec', '정밀도',  'FP4|FP8|FP16|BF16|INT8|NVFP4|MXFP4|양자화|quantiz|희소성|sparsit|정밀도|숫자 포맷|비트|LUT|압축'),
 ('si',   '실리콘',  '텐서 코어|텐서코어|tensor core|MMA|TMA|DSMEM|SMEM|LDGSTS|Volta|Turing|Ampere|Hopper|Blackwell|CDNA|마이크로아키텍처|UArch|PTX|SASS|프로그래밍 모델'),
 ('serve','서빙',    '분리형|disagg|프리필|prefill|PD |배칭|prefix 캐시|캐시 계층|커널|엔진|서빙 전략'),
 ('train','학습',    '강화학습|\\bRL\\b|롤아웃|온폴리시|오프폴리시|정책|보상|사전학습|미드트레이닝|GRPO|PPO|동기식|비동기식|환경'),
]
HEAD_RAILS = [(k, ko, re.compile(p, re.I)) for k, ko, p in HEAD_RAILS]

# 제목이 이걸로 끝나면 값(결과)이지 기전이 아니다.
VALUE_ONLY = re.compile('벤치마크|성능 비교|비용 비교|TCO|전력 예산|BOM|램프업|공급망|스펙|시장|권고'
                        '|트러블슈팅|방법론|개요|서론|결론|미리보기|현황|요약|로드맵|사례 연구'
                        '|숨은 전제|소요량|추이|참사|과소약속|성능$|성능 \\(')

# 규칙이 못 가르는 자리. 제목 앞부분으로 맞춘다.
FORCE_KEEP = [
 'MTP(멀티토큰예측)와 Anthropic Fast Mode',      # 경제학이 붙었을 뿐 MTP는 디코딩 계보 마디
 'TileRT 개발이 느린 이유',                       # 빠른 대신 무엇을 냈나 — 대가 마디
]
FORCE_DROP = [
 'Helios 스케일업·스케일아웃 토폴로지',            # 여기 '라우팅'은 NIC 라우팅, 전문가 라우팅이 아니다
 'TileRT란 무엇인가 - 타일과 워프',               # 같은 문서의 '지속형 엔진 커널' 마디와 겹친다
 'AMD 조합성(Composability) 문제',              # 제품 비판이지 기전 변화가 아니다
 'AMD AI 엔지니어 보상',                        # 여기 '보상'은 연봉이다. RL 보상과 같은 글자를 쓴 남
 '5세대 텐서 코어 MMA: 처리량 분석',              # 마이크로벤치마크 측정값이지 기전 변화가 아니다
 'MMA 지연시간과 In-flight',                    # 같음
 '소프트웨어 사용 경험',                          # 도구 사용기지 기전 변화가 아니다
]

raw = json.load(open(ROOT + '/scratchpad/lineage_raw.json', encoding='utf-8'))
keep, drop = [], []
for r in raw:
    head = r['head']
    rails = [k for k, ko, p in HEAD_RAILS if p.search(head)]
    forced_keep = any(head.startswith(x) for x in FORCE_KEEP)
    forced_drop = any(head.startswith(x) for x in FORCE_DROP)
    ok = bool(rails) and not VALUE_ONLY.search(head)
    if (ok or forced_keep) and not forced_drop:
        if not rails:                       # 예외로 살린 절도 궤도는 있어야 한다
            rails = r['rails'][:1]
        r2 = dict(r); r2['rails'] = rails
        keep.append(r2)
    else:
        drop.append((head, r['rails']))

json.dump(keep, open(ROOT + '/scratchpad/lineage_nodes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
c = Counter(k for r in keep for k in r['rails'])
print('남김:', len(keep), '| 버림:', len(drop), '| 문서:', len({r['doc'] for r in keep}))
print('궤도별:', dict(c)); print()
for r in keep:
    print('%s  %-16s %s' % (r['date'], '/'.join(r['rails']), r['head'][:66]))
