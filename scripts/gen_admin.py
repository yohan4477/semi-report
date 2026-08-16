# -*- coding: utf-8 -*-
"""관리자 대시보드 — 세 갈래가 데이터를 어떻게 처리하는지 흐름도로.

  py -3.13 scripts/gen_admin.py   ->  대시보드/관리자 대시보드.html

룰 원본은 README·CLAUDE.md·LINKEDIN_RULES.md와 스킬 셋이다. 이 파일은 그것을
다시 쓰지 않고 **어느 룰이 어느 단계에 걸리는지**만 모아 놓는다. 룰이 바뀌면
아래 LANES를 고치고 다시 돌린다. 공개 사이트에는 잠금(/admin)으로 나간다.

한 갈래 = 흐름도 한 장. 단계 상자가 위에서 아래로 이어지고, 상자마다
실물(파일·명령)과 그 단계에서만 걸리는 룰이 함께 있다. 표를 따로 두지 않는다 —
같은 사실을 두 곳에 적으면 반드시 한쪽이 낡는다.

  kind: src 들어오는 것 · work 가공물 · gate 막는 것 · gen 스크립트 · out 화면
"""
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'insights'))
import style  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, '대시보드', '관리자 대시보드.html')

ACCENT = {'unified': '#2563eb', 'topic': '#0f9d76', 'semi': '#b4522b'}
# 노드 왼쪽 띠 — 들어오는 것 · 가공물 · 막는 것 · 스크립트 · 화면을 색으로 가른다
KIND_COLOR = {'src': '#8892a3', 'work': '#6366f1', 'gate': '#ea580c', 'gen': '#0f9d76', 'out': '#b4522b'}
KIND_NAME = [('src', '원문 — 밖에서 들어온다'), ('work', '가공물 — 우리가 만든다'),
             ('gate', '게이트 — 여기서 막힌다'), ('gen', '스크립트 — 화면을 만든다'),
             ('out', '화면 — 나가는 것')]

# 갈래 — (키, 이모지, 이름, 한 줄, 룰 원본, [단계])
# 단계 = (이름, kind, 한 줄 요지, [(노드 이름, 실물)], [룰])
LANES = [
 ('unified', '🧩', '통합 인사이트',
  '문서를 가로질러야 보이는 판단만. 문서 한 편 요약은 여기 안 온다.',
  'insight-note · insight-review 스킬',
  [
   ('① 원문', 'src', '줄 번호가 인용의 기준이다',
    [('뉴스레터 변환본', 'content/newsletter/**'),
     ('미변환 클리핑', 'input/clippings/**'),
     ('제3자 해설 요약', 'content/understanding/**'),
     ('링크드인 월별 묶음', 'content/linkedin/[YYMM] 링크드인 게시물.md')],
    ['원문이 바뀌면 <code>insights/cites.json</code>의 줄 해시가 어긋나 검사기가 잡는다.',
     'manifest에 원문이 없으면 노트를 쓰지 않고 <b>멈춘다</b> — 변환 파이프라인 쪽 문제다.',
     '링크드인은 <code>scripts/gen_li_source.py</code>가 떨군다. <b>게시 시각 오름차순으로만 쌓여</b> 새 글이 들어와도 앞줄의 줄 번호가 밀리지 않는다 — 그래서 손으로 고치지 않는다.']),

   ('①.5 링크드인 자격', 'gate', '게시일은 정보의 날짜가 아니다 · insights/li_signal.py',
    [('신호 자격 판정', 'insights/views/li_signals.json')],
    ['기준일(<code>basis_date</code>)은 뉴스레터 링크가 있으면 <b>그 원문 발행일</b>이다. 게시일이 아니다 — 최장 74일 차이가 났다.',
     '시차가 <code>LAG_MAX</code> 15일을 넘으면 재홍보로 본다. 새 정보가 아니므로 <b>시간축에서 뺀다</b>.',
     '링크가 없으면 게시일을 인정하되 <b>수치가 박힌 자체 발화만</b> 근거로 쓴다. 밈·행사·팟캐스트·채용·과거 회고는 신호가 아니다.',
     '<b><code>push=true</code>는 버리는 게 아니라 다른 축이다.</b> 재홍보·행사 글은 근거로 인용하지 않지만 「지금 무엇을 다시 미나」를 볼 때 쓴다.',
     '게시 시각은 activity URN 상위 비트에서 뽑는다 — 「2주 전」 같은 상대 표기를 환산하지 않는다.']),

   ('② 노트', 'work', '문서 1편 = 노트 1장 · insight-note 스킬',
    [('문서 노트', 'insights/notes/&lt;yymmdd&gt;-&lt;슬러그&gt;.md')],
    ['<b>압축을 두 번 하지 않는다.</b> 여러 문서를 한 노트에 눌러 담으면 요약의 요약이 된다 — 원자 체계를 폐기한 이유다.',
     '한 장 3KB 이하(N5 WARN). 넘으면 서술 단계에서 원문을 다시 읽는 편이 낫다는 신호다.',
     '<b>조건 없는 수치는 적지 않는다.</b> 언제·어디서·누구 기준인지 없으면 나중에 반대 결론이 나온다(N6 FAIL).',
     '노트는 문서가 말한 것만 담는다. <b>티커·수혜/피해·전망은 서술에서</b> 한다.',
     '문장을 쪼개지 않는다. 논증이 살아 있어야 「왜 그렇게 말했나」가 남는다.']),

   ('③ 서술', 'work', '노트 전량을 한 콜에 읽고 쓴다 · insight-review 스킬',
    [('교차 인사이트', 'insights/synth/cross-*.md'),
     ('현황 브리핑', 'insights/briefs/*-지금-상태.md'),
     ('주체 추적', 'insights/tracks/*.md')],
    ['<b>카드 하나 = 어긋남 하나.</b> 쌍의 양쪽은 같은 층위여야 한다. 「그리고」로 두 쌍을 이으면 그 자리가 쪼갤 자리다.',
     '<code>## 주장</code> 문단의 부품과 순서 — ① 쌍의 양쪽을 실명으로 ② 어긋남의 주체를 하나로 ③ 양쪽의 값에 각각 인용 ④ 이 카드가 정하는 것.',
     '<b>역방향 읽기</b> — 주장 문단을 가리고 나머지 절만 읽어 주장을 다시 뽑는다. 다르면 <b>사례가 맞다</b>. 사례를 빼서 주장에 맞추는 게 결함 유형 1이다.',
     '<b>한 회차에 한두 장만 뽑는다.</b> 6장 배치 생산이 「카드끼리 겹친다」의 직접 원인이었다.',
     '인용은 문장 끝 마침표 앞, 앞에 공백. 화면에는 <code>L123</code>만 남고 문서명은 tooltip으로 들어간다.',
     '절 순서는 <code>check_prose.py</code>의 <code>SECTION_ORDER</code>가 정한다.']),

   ('④ 검사', 'gate', '다섯 다 FAIL 0이어야 푸시한다',
    [('노트·인용 무결성', 'check_notes.py  N1~N7'),
     ('문체·용어·절 순서', 'check_prose.py  P1~P7'),
     ('읽히는가', 'check_read.py  R1~R12'),
     ('숫자와 원문 대조', 'check_cite.py  C1'),
     ('아직 지금 이야기인가', 'check_fresh.py  F1~F3')],
    ['<b>앞의 셋만 돌리지 않는다.</b> 2026-08-15에 그렇게 푸시해서 <code>check_cite</code> 확인필요 6건과 <code>check_fresh</code> FAIL 3건이 그대로 나갔다.',
     '<code>check_notes</code> FAIL이면 여기서 멈춘다. <b>줄 번호를 손으로 맞추지 말고</b> 그 문서를 재추출한다.',
     '<code>check_prose</code> FAIL은 <b>용어를 지우지 말고 괄호로 푼다.</b> 지웠다가 되돌린 이력이 있다.',
     '<code>check_cite</code> 확인필요는 기계가 절반만 본 것이다. <b>원문 줄을 열어 사람이 확인한다</b> — 숫자가 그 줄에 있어도 뜻이 다를 수 있다.',
     '<code>check_fresh</code> F1은 날짜만 미루지 않는다. 안 바뀐다고 판단했으면 <b>그 판단의 근거를 본문에</b> 쓴다.']),

   ('⑤ 생성', 'gen', '공유 CSS는 insights/style.py의 BASE 하나',
    [('통합 인사이트', 'insights/gen_insightview.py'),
     ('주체 보드', 'insights/gen_entity_board.py musk'),
     ('지도', 'insights/gen_map.py')],
    ['클러스터·좌표를 건드렸으면 <code>refresh_provenance.py</code> → <code>validate_insights.py</code> → <code>gen_map.py</code>. <b>클러스터는 인사이트 지도만 쓴다</b> — 통합 인사이트는 노트에서 나온다.',
     '<b>페이지마다 CSS 토큰을 새로 정하지 않는다.</b>']),

   ('⑥ 화면', 'out', '',
    [('통합 인사이트.html', '/unified 🔒'),
     ('추적 - 일론 머스크.html', ''),
     ('인사이트 지도.html', '')],
    ['문장 옆 줄번호를 누르면 근거가 된 <b>원문 그 줄</b>로 간다.']),
  ]),

 ('topic', '🏠', '주제 대시보드 4장',
  '부동산 · 금융 · 미주사 · AI·인프라·에너지. 제3자 해설 한 편 = 카드 한 장.',
  'insight-upload 스킬 · scripts/card_lib.py',
  [
   ('① 원문', 'src', '유튜브는 자막 전문. 설명란 요약으로 때우지 않는다',
    [('유튜브 자막', 'scratchpad/ytsub.py &lt;영상ID&gt;'),
     ('네이버 프리미엄', 'scratchpad/clip_one.py &lt;URL&gt; &lt;YYYYMMDD&gt;')],
    ['네이버 프리미엄은 CDP 크롬으로 파싱하고 <b>유료 원문은 로컬에만</b> 둔다. 공개엔 요약만 싣는다.']),

   ('② 요약본', 'work', '주제 또는 화자 폴더에 마크다운으로 남긴다',
    [('해설 요약', 'content/understanding/&lt;주제 또는 화자&gt;/')],
    ['채널별·주제별 폴더가 섞여 있다 — <b>주제 축으로 모으는 중</b>이다.']),

   ('③ 카드', 'work', '채널이 아니라 주제로 고른다 · insight-upload 스킬',
    [('카드 dict', 'scripts/card_lib.py — 스키마 한 벌'),
     ('슬림 필드', 'slim_oneliner · slim_points 6~8 · slim_stats 4')],
    ['<b>gain 필수</b> — 접힌 채로 고르는 기준이다. 옛 언더스탠딩 카드엔 이게 없어 제목만 보고 골라야 했다.',
     '<b>clash(반론·충돌) 필수</b> — 한 편만 읽고 결론 내리지 않게 다른 편이나 SemiAnalysis 코퍼스와 어긋나는 지점을 박는다. 수익 사례가 전면에 나올수록 길게.',
     '<b>stats는 본문에 나온 숫자만.</b> 추정치를 만들지 않는다. quote는 원문 그대로, 다듬지 않는다.',
     '표는 비교 대상이 둘 이상일 때만. <b>탭으로 나누지 말고 한 화면에 나란히</b> 둔다.',
     '<b>슬림 포인트는 자막 전문에서 직접 뽑는다.</b> 요약을 또 요약하면 「누가 무엇을」이 빠지면서 뜻이 뒤집힌다(용인 편).',
     '<code>slim_*</code>는 렌더링 선택이라 <code>points</code>·<code>table</code>·<code>stats</code>·<code>clash</code> 원본은 카드에 그대로 남긴다.']),

   ('④ 검사', 'gate', '따옴표는 자막에 있는 말만',
    [('슬림 ↔ 자막 대조', 'scratchpad/check_slim.py')],
    ['<b>FAIL</b> — 따옴표 인용이 자막에 없다(유사도 0.55 미만). 자동 자막은 오인식이 많아 완전 일치가 아니라 유사도로 본다.',
     '<b>경고</b> — 숫자를 자막에서 못 찾았다. 3.4억 ↔ 3억 4천 같은 표기 차이일 수 있어 사람이 본다.',
     '<b>경고</b> — 전문용어에 괄호 설명이 없다(<code>GLOSS_TERMS</code>). 새 용어를 쓰면 그 목록에 추가한다.']),

   ('⑤ 생성', 'gen', '섹션 번호는 손대지 않는다 — SEC_ORDER가 다시 매긴다',
    [('부동산', 'scratchpad/gen_realestate_dashboard.py'),
     ('금융', 'scratchpad/gen_finance_dashboard.py'),
     ('미주사', 'scratchpad/gen_usa_dashboard.py'),
     ('AI·인프라·에너지 — 생성기 없음', 'scripts/add_card.py --section sec-ai')],
    ['<code>scratchpad/dash_common.py</code>가 <code>언더스탠딩 대시보드.html</code>의 <code>&lt;style&gt;</code>을 CSS 원본으로 읽는다. <b>파일명을 바꾸지 않는다</b>(표시 이름만 AI·인프라·에너지).',
     '옛 형식 카드 26장은 <b>소급 변환하지 않는다.</b> 한동안 두 형식이 섞인다.']),

   ('⑥ 롤업', 'work', '카드를 올렸으면 리포트도 같이 손본다',
    [('주간·월간 리포트', 'data/rollup_notes_*.json'),
     ('SemiAnalysis 쪽 재배치', 'scripts/gen_rollup.py')],
    ['<b>산문은 사람이 쓴다</b> — 판단이라 자동 생성하지 않는다.',
     '각 리포트에 <b><code>desc</code>(접힌 채로 읽는 한 줄)</b>를 반드시 넣는다.',
     '기간 기준은 <b>매체 업로드일</b>이지 우리가 처리한 날이 아니다.',
     '새 편이 기존 판단을 뒤집으면 <code>items</code>를 고친다. 덧붙이기만 하지 않는다.']),

   ('⑦ 화면', 'out', '',
    [('부동산 대시보드.html', '/realestate'),
     ('금융 대시보드.html', '/finance'),
     ('언더스탠딩 대시보드.html', '/understanding'),
     ('미국주식 사관학교 대시보드.html', '/usa-academy 🔒')],
    ['종목이 언급돼도 <b>추천이 아니다.</b> 가격·타이밍은 이 체계에 없다.']),
  ]),

 ('semi', '📊', 'SemiAnalysis 대시보드',
  '카드 체계가 아니다. 소셜 신호·뉴스레터·클러스터 판단으로 짜인 다른 구조.',
  'LINKEDIN_RULES.md · semianalysis-newsletter 스킬',
  [
   ('① 원문', 'src', '전용 프로필 chrome-semianalysis 하나로 둘 다 로그인',
    [('LinkedIn 게시물', 'CDP 크롬 9222 · 「최근」 정렬'),
     ('뉴스레터 전문', 'semianalysis-newsletter 스킬'),
     ('YouTube 신호', '')],
    ['<b>「최근」으로 바꾼 뒤</b> 스크롤한다. 기본값 「인기순」은 오래된 글을 섞어 새 글을 굶긴다.',
     '웹소켓은 <code>suppress_origin=True</code>, 크롬은 <code>--remote-allow-origins=*</code> 없으면 403이다.']),

   ('② 게이트', 'gate', '이 갈래엔 문장 검사기가 없다 — 막는 곳은 여기뿐이다',
    [('게시물 필터', '채용·행사·수상·구독유도 제외'),
     ('페이월 통과 확인', 'text_len &gt; 6000 · paywalled:false')],
    ['<b>포함</b> — 시장·기술 분석, 숫자·차트가 담긴 것, 공급망·기업 동향 신호.',
     '제외한 것도 대장에 제목 한 줄 + <code>제외(사유)</code>로 남긴다. 재처리를 막는 유일한 장치다.',
     '이미 대장에 있는 게시물은 건너뛴다(URN 또는 날짜+첫 줄로 식별).',
     '<b>부분 클립으로 변환하지 않는다</b> — <code>text_len</code>이 작으면 구독 세션이 만료된 것이다.']),

   ('③ 적재', 'work', '카드 체계가 아니다 — insight-upload 대상이 아니다',
    [('소셜 신호 히스토리', '대시보드/소셜 신호 히스토리.html · 손으로'),
     ('뉴스레터 변환', 'input/clippings → transformer → content/newsletter/**')],
    ['히스토리 카드 <code>&lt;span class="sn"&gt;</code>의 <b>첫 문장은 이 글이 무슨 뜻인지</b>를 말한다. 원문 논증을 중간부터 옮기지 않는다 — 미러가 이 문장을 카드 제목으로 쓴다.',
     '용어는 남기고 첫 등장에 괄호로 푼다(프로브 카드·ATE·SoC·전공정/후공정 등).',
     '뉴스레터 변환은 길고 토큰을 많이 먹으니 <b>서브에이전트에 위임</b>해 메인 컨텍스트를 지킨다.']),

   ('④ 생성', 'gen', '자동은 ① 소셜 신호뿐이다',
    [('① 미러 재생성', 'scripts/gen_bmirror.py [일수=14]'),
     ('롤업 재배치', 'scripts/gen_rollup.py')],
    ['히스토리 최근 N일을 파싱해 다시 깐다 — <code>linkedin-update</code>로 히스토리를 갱신한 뒤 돌리면 동기된다.',
     'NVIDIA 1차 신호는 <code>gen_bmirror.py</code>의 <code>NVROWS</code>에 날짜별로 직접 적는다.']),

   ('⑤ 손편집', 'work', '「대시보드 HTML은 생성물」 원칙의 예외가 여기다',
    [('② 뉴스레터 최근분', ''),
     ('③ 클러스터 종합 판단', ''),
     ('④ 기업 익스포저', '')],
    ['이 셋과 소셜 신호 히스토리만 손으로 쓴다. 나머지 대시보드는 전부 생성물이다.',
     '주제 대시보드에는 <b>해당 주제 신호만</b> 골라 반영한다.']),

   ('⑥ 화면', 'out', '',
    [('SemiAnalysis 대시보드.html', '/semianalysis 🔒')],
    ['점수판을 두지 않는다.']),
  ]),
]

# 발행은 세 갈래가 같은 길을 쓴다 — 흐름도 꼬리에 공통으로 붙인다
TAIL = ('⑦ 발행', 'gen', '세 갈래가 같은 길을 쓴다',
        [('NEW 배지 기준일', 'scripts/update_card_ledger.py'),
         ('사이트 빌드', 'scripts/gen_site.py')],
        ['<code>update_card_ledger.py</code>를 건너뛰면 NEW 배지가 안 붙는다. 기준은 업로드일이 아니라 <b>사이트에 처음 올라온 날</b>이고 그 날짜는 대장에만 있다.',
         '<b>리포트 한 편 때문에 페이지를 새로 만들지 않는다</b> — 주제 대시보드의 섹션으로 넣는다. 그렇게 늘어난 게 19장이었다.',
         '<code>main</code>에 푸시하면 Cloudflare Pages가 <code>gen_site.py</code>를 돌려 자동 배포한다.'])

# 세 갈래가 함께 지키는 것 — 흐름도 셋에 세 번 적지 않는다
COMMON = [
    ('푸시 전 한 방', 'py -3.13 scripts/build_all.py',
     '생성기 전부와 검사기 다섯을 순서대로 돌리고 하나라도 실패하면 종료 코드 1이다. <code>--check</code>는 검사만.'),
    ('FAIL 0', '검사기가 못 잡는 것도 안다',
     '숫자는 맞는데 뜻이 다른 경우(68,928달러가 배선 값인지 백플레인 값인지)는 기계가 모른다. 원문 줄을 열어야 한다.'),
    ('용어', '남기고 괄호로 푼다',
     '전문용어를 쉬운 말로 치환하지 않는다 — 용적률(대지면적 대비 지을 수 있는 총 바닥면적의 비율).'),
    ('일반론 금지', '숫자 · 명명된 주체 · 비직관',
     '「중요하다」·「주목된다」는 쓰지 않는다.'),
    ('커밋', '의미 단위마다 바로',
     '몰아서 하지 않는다. 단계마다 승인을 묻지 않고 판단해서 진행한다.'),
    ('인코딩', 'PYTHONIOENCODING=utf-8',
     '콘솔이 cp949라 파이썬 실행에 붙인다.'),
]

CSS = r'''
  .lede2{color:var(--sub);font-size:var(--t-body);margin:10px 0 0;max-width:70ch}
  .common{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin:18px 0 0}
  .cm{border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:12px 14px;box-shadow:var(--shadow)}
  .cm b{display:block;font-size:var(--t-lbl);font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);margin:0 0 5px}
  .cm .w{display:block;font-size:var(--t-body);font-weight:800;color:var(--ink);margin:0 0 4px}
  .cm p{margin:0;font-size:var(--t-meta);color:var(--sub)}

  /* 범례 — 상자 색이 무엇을 뜻하는지 */
  .lg{display:flex;flex-wrap:wrap;gap:6px 16px;margin:14px 0 0;padding:10px 13px;
      border:1px solid var(--line);border-radius:10px;background:var(--sunk)}
  .lg span{display:inline-flex;align-items:center;gap:7px;font-size:var(--t-lbl);font-weight:700;color:var(--sub)}
  .lg i{width:11px;height:11px;border-radius:3px;background:var(--k);flex:none}

  /* 갈래로 건너뛰는 링크 — 탭이 아니라 앵커다 */
  .jump{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
  .jump a{flex:1 1 200px;border:1px solid var(--line);border-left:4px solid var(--ac);border-radius:0 10px 10px 0;
          background:var(--card);padding:10px 13px;text-decoration:none;box-shadow:var(--shadow)}
  .jump a:hover{border-color:var(--ac)}
  .jump .t{display:block;font-size:var(--t-body);font-weight:850;color:var(--ink);letter-spacing:-.01em}
  .jump .s{display:block;margin:2px 0 0;font-size:var(--t-lbl);color:var(--faint)}

  /* 흐름도 한 장 = 갈래 하나 */
  .lane{margin:34px 0 0;padding-top:22px;border-top:1px solid var(--line)}
  .lane:first-of-type{border-top:0}
  .lh{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 11px;margin:0 0 3px}
  .lh .em{font-size:22px;line-height:1}
  .lh h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.025em;margin:0;color:var(--ink)}
  .lh .rl{font-size:var(--t-lbl);font-weight:700;color:var(--ac);
          font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
  .lane>.one{margin:0 0 12px;font-size:var(--t-body);color:var(--sub);max-width:70ch}

  /* 단계 상자 — 왼쪽에 단계 이름, 오른쪽에 실물과 룰 */
  .fs{border:1px solid var(--line);border-radius:11px;background:var(--card);
      padding:12px 14px;box-shadow:var(--shadow)}
  .fs>.sh{display:flex;flex-wrap:wrap;align-items:baseline;gap:5px 10px;margin:0 0 9px}
  .fs>.sh b{font-size:var(--t-body);font-weight:850;color:var(--ink);letter-spacing:-.01em}
  .fs>.sh i{font-style:normal;font-size:var(--t-meta);color:var(--sub)}
  .fnn{display:flex;flex-wrap:wrap;gap:8px}
  .fn{flex:1 1 210px;min-width:0;border:1px solid var(--line);border-left:3px solid var(--nc);
      border-radius:0 8px 8px 0;background:var(--sunk);padding:8px 10px}
  .fn .nn{display:block;font-size:var(--t-meta);font-weight:800;color:var(--ink)}
  .fn .ns{display:block;margin:3px 0 0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
          font-size:var(--t-lbl);color:var(--faint);word-break:break-word}
  .fs ul{margin:10px 0 0;padding:0;list-style:none}
  .fs li{font-size:var(--t-meta);color:var(--sub);margin:0 0 6px;padding-left:12px;position:relative}
  .fs li:last-child{margin-bottom:0}
  .fs li::before{content:"";position:absolute;left:0;top:.62em;width:4px;height:4px;border-radius:50%;background:var(--line)}
  .fs li b{color:var(--ink);font-weight:700}
  .fs code{font-size:.9em}

  /* 막는 단계는 색으로 갈라 놓는다 */
  .fs[data-kind="gate"]{border-color:#ea580c;background:#fff7ed}
  .fs[data-kind="gate"]>.sh b,.fs[data-kind="gate"]>.sh i{color:#9a3412}
  .fs[data-kind="gate"] .fn{background:#fff}
  .fs[data-kind="gate"] li{color:#7c2d12}
  .fs[data-kind="gate"] li b{color:#7c2d12}
  @media (prefers-color-scheme:dark){
    .fs[data-kind="gate"]{border-color:#c2410c;background:#2a1509}
    .fs[data-kind="gate"]>.sh b,.fs[data-kind="gate"]>.sh i{color:#fdba74}
    .fs[data-kind="gate"] .fn{background:#1f1710}
    .fs[data-kind="gate"] li,.fs[data-kind="gate"] li b{color:#f3c9a8}
  }

  .arw{height:22px;display:flex;align-items:center;justify-content:center;
       color:var(--ac);font-size:12px;line-height:1;opacity:.7}

  @media (max-width:860px){
    .fn{flex:1 1 100%}
    .jump a{flex:1 1 100%}
  }
'''

HEAD = '''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>관리자 — 데이터 처리 지도</title>
<style>%s%s</style>
</head><body><main class="wrap">
'''


def stage_html(stg, kind, note, nodes, rules):
    n = ''.join('<div class="fn" style="--nc:%s"><span class="nn">%s</span>%s</div>'
                % (KIND_COLOR[kind], nm, '<span class="ns">%s</span>' % sub if sub else '')
                for nm, sub in nodes)
    r = ''.join('<li>%s</li>' % x for x in rules)
    return ('<div class="fs" data-kind="%s"><p class="sh"><b>%s</b>%s</p>'
            '<div class="fnn">%s</div>%s</div>'
            % (kind, stg, '<i>%s</i>' % note if note else '', n,
               '<ul>%s</ul>' % r if r else ''))


def main():
    out = [HEAD % (style.BASE, CSS)]
    out.append('<header>'
               '<p class="eyebrow">관리자 · 비공개</p>'
               '<h1>데이터 처리 지도</h1>'
               '<p class="lede">대시보드는 세 갈래로 나뉘고 갈래마다 소스·집필 룰·검사기가 다르다. '
               '룰 문서를 다 읽지 않고도 <b>어느 룰이 어느 단계에 걸리는지</b> 보라고 만든 장이다.</p>'
               '<p class="lede2">갈래마다 흐름도 한 장이다. 원문이 어디로 들어와 무엇을 거쳐 어느 화면으로 '
               '나가는지 위에서 아래로 읽고, 상자 안에 그 단계에서만 걸리는 룰이 있다.</p>'
               '<div class="meta"><span>룰 원본 · README.md · CLAUDE.md · LINKEDIN_RULES.md · '
               '.claude/skills/</span><span>생성 · scripts/gen_admin.py</span></div>'
               '</header>')

    out.append('<h3 class="sec">세 갈래가 함께 지키는 것</h3><div class="common">')
    for lbl, word, desc in COMMON:
        out.append('<div class="cm"><b>%s</b><span class="w">%s</span><p>%s</p></div>' % (lbl, word, desc))
    out.append('</div>')

    out.append('<div class="lg">')
    for k, nm in KIND_NAME:
        out.append('<span style="--k:%s"><i></i>%s</span>' % (KIND_COLOR[k], nm))
    out.append('</div>')

    out.append('<div class="jump">')
    for key, emo, name, one, _src, stages in LANES:
        out.append('<a href="#%s" style="--ac:%s"><span class="t">%s %s</span>'
                   '<span class="s">단계 %d</span></a>'
                   % (key, ACCENT[key], emo, name, len(stages) + 1))
    out.append('</div>')

    for key, emo, name, one, rule_src, stages in LANES:
        out.append('<section class="lane" id="%s" style="--ac:%s">' % (key, ACCENT[key]))
        out.append('<div class="lh"><span class="em">%s</span><h2>%s</h2>'
                   '<span class="rl">%s</span></div>' % (emo, name, rule_src))
        out.append('<p class="one">%s</p>' % one)
        for j, st in enumerate(stages + [TAIL]):
            if j:
                out.append('<div class="arw" aria-hidden="true">▼</div>')
            out.append(stage_html(*st))
        out.append('</section>')

    out.append('<footer>이 장은 룰의 원본이 아니라 <b>색인</b>이다. 룰이 바뀌면 원본 문서를 먼저 고치고 '
               '<code>scripts/gen_admin.py</code>의 <code>LANES</code>를 맞춘 뒤 다시 만든다. '
               'insight-dashboard.com에서는 <code>/admin</code>으로 잠겨 나간다.</footer>')
    out.append('</main></body></html>')

    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    n = sum(len(l[5]) + 1 for l in LANES)
    print('관리자 대시보드 — 갈래 %d · 단계 %d  ->  %s' % (len(LANES), n, os.path.basename(OUT)))


if __name__ == '__main__':
    main()
