# -*- coding: utf-8 -*-
# 계보 재료 추출기.
#
# mermaid는 못 쓴다 — 알고리즘 17편의 도해 660개 중 화살표에 사유 라벨이 붙은 건 5개뿐이다.
# 나머지는 구성도(무엇이 무엇으로 이뤄졌나)라 "왜 갈아탔나"가 없다.
# 그래서 문서 공통 골격인 `## N. 제목` 절과 그 아래 `📌 핵심` 불릿을 단위로 뽑는다.
#
# 산출: scratchpad/lineage_raw.json — 절 단위 레코드. 각 레코드가 계보 마디 후보 하나.
import os, re, json, glob, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = 'C:/Users/y/semianalysis'
NL = ROOT + '/content/newsletter'

# 밀도 표지. RL 어휘를 뺐더니 강화학습 문서 3편이 통째로 탈락했다 — 학습 쪽 계보는
# 어텐션·MoE 어휘를 안 쓴다. 궤도가 다르면 어휘도 다르다는 걸 놓친 실수다.
DENS = re.compile('MLA|GQA|MQA|MoE|전문가 혼합|FP8|FP4|어텐션|양자화|디코딩|KV 캐시|라우팅'
                  '|강화학습|롤아웃|온폴리시|오프폴리시|보상 해킹|사전학습|미드트레이닝', re.I)

# 궤도별 표지. 절이 어느 궤도에 속하는지 이걸로 가른다.
RAILS = [
 ('attn', '어텐션', 'MLA|GQA|MQA|MHA|어텐션|attention|DeltaNet|KDA|RoPE|KV 캐시|선형 어텐션|CSA|HCA|슬라이딩'),
 ('moe',  '전문가',  'MoE|전문가|라우팅|expert|부하 분산|load balanc|Quantile|MegaMoE|LatentMoE'),
 ('dec',  '디코딩',  'MTP|투기|speculative|멀티 토큰|multi-token|디코딩|드래프트|draft'),
 ('prec', '정밀도',  'FP4|FP8|FP16|BF16|FP32|INT8|NVFP4|MXFP4|양자화|quantiz|희소|sparsit|정밀도'),
 ('si',   '실리콘',  '텐서 코어|텐서코어|tensor core|MMA|TMA|비동기|Volta|Turing|Ampere|Hopper|Blackwell|명령어|PTX|SASS'),
 ('serve','서빙',    '프리필|prefill|디코드 분리|disaggregat|배칭|batching|prefix 캐시|캐시 계층|스케줄'),
 ('train','학습',    '강화학습|\\bRL\\b|롤아웃|rollout|온폴리시|오프폴리시|on-policy|off-policy|정책 지연|PipelineRL'
                     '|보상|reward|사전학습|미드트레이닝|학습기|생성기|환경'),
]
RAILS = [(k, ko, re.compile(p, re.I)) for k, ko, p in RAILS]

# 변화를 말하는 문장의 표지. 이게 없는 절은 계보가 아니라 설명이다.
CHANGE = re.compile('바꾸|바뀌|갈아|대체|→|에서 .{0,12}(으로|로)\\b|세대|진화|계보|이전에는|기존|도입|폐기|포기|버리|넘어|대신|개선|극복|한계|문제|트레이드오프|대가|희생')

SECT = re.compile('^## (\\d+)\\. (.+)$', re.M)
BULLET = re.compile('^- (.+)$', re.M)

out = []
for path in sorted(glob.glob(NL + '/**/*.md', recursive=True)):
    txt = open(path, encoding='utf-8').read()
    if len(DENS.findall(txt)) <= 15:
        continue
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    date = re.search('\\[(\\d{6})\\]', os.path.basename(path)).group(1)
    marks = list(SECT.finditer(txt))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(txt)
        body = txt[m.start():end]
        head = m.group(2).strip()
        # 절 안에서 📌 핵심 블록만 취한다 (도해·표 제외)
        core = ''
        km = re.search('\\*\\*📌 핵심:\\*\\*(.*?)(?:\\n---|\\n```|\\Z)', body, re.S)
        if km:
            core = km.group(1)
        bullets = [b.strip() for b in BULLET.findall(core)]
        hay = head + ' ' + ' '.join(bullets)
        rails = [k for k, ko, p in RAILS if len(p.findall(hay)) >= 2]
        if not rails or not bullets:
            continue
        if not CHANGE.search(hay):
            continue
        out.append({'doc': rel, 'date': date, 'sec': m.group(1), 'head': head,
                    'rails': rails, 'nb': len(bullets), 'bullets': bullets})

out.sort(key=lambda r: (r['date'], int(r['sec'])))
json.dump(out, open(ROOT + '/scratchpad/lineage_raw.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

from collections import Counter
c = Counter(k for r in out for k in r['rails'])
print('절 후보:', len(out), '| 문서:', len({r['doc'] for r in out}))
print('궤도별:', dict(c))
print()
for r in out:
    print('%s  %-14s %-56s %s' % (r['date'], '/'.join(r['rails']), r['head'][:56], r['doc'].split('/')[-1][:30]))
