# -*- coding: utf-8 -*-
"""관리자 대시보드 — 세 갈래가 데이터를 어떻게 처리하는지 한 장에.

  py -3.13 scripts/gen_admin.py   ->  대시보드/관리자 대시보드.html

룰 원본은 README·CLAUDE.md·LINKEDIN_RULES.md와 스킬 셋이다. 이 파일은 그것을
다시 쓰지 않고 **어느 룰이 어느 단계에 걸리는지**만 모아 놓는다. 룰이 바뀌면
아래 LANES를 고치고 다시 돌린다. 공개 사이트에는 잠금(/admin)으로 나간다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'insights'))
import style  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, '대시보드', '관리자 대시보드.html')

# 단계 — 세 갈래가 공유하는 뼈대. 이 순서로 행이 만들어진다
STAGES = [
    ('① 소스', '무엇이 들어오나'),
    ('② 가공', '무엇으로 바뀌나'),
    ('③ 집필 룰', '쓸 때 지키는 것'),
    ('④ 검사', '무엇이 푸시를 막나'),
    ('⑤ 생성', '어느 스크립트가 화면을 만드나'),
    ('⑥ 발행', '어디로 나가나'),
]

# 갈래 — (키, 이모지, 이름, 한 줄, 룰 원본)
LANES = [
    ('unified', '🧩', '통합 인사이트',
     '문서를 가로질러야 보이는 판단만. 문서 한 편 요약은 여기 안 온다.',
     'insight-note · insight-review 스킬'),
    ('topic', '🏠', '주제 대시보드 4장',
     '부동산 · 금융 · 미주사 · AI·인프라·에너지. 제3자 해설 한 편 = 카드 한 장.',
     'insight-upload 스킬 · scripts/card_lib.py'),
    ('semi', '📊', 'SemiAnalysis 대시보드',
     '카드 체계가 아니다. 소셜 신호·뉴스레터·클러스터 판단으로 짜인 다른 구조.',
     'LINKEDIN_RULES.md · semianalysis-newsletter 스킬'),
]

# CELLS[stage_index][lane_key] = (실물 목록, 룰 목록)
# 실물은 파일·명령, 룰은 그 단계에서만 걸리는 것. 세 갈래 공통은 아래 COMMON으로 뺀다
CELLS = [
    # ① 소스
    {
        'unified': (
            ['content/newsletter/**', 'input/clippings/**', 'content/understanding/**'],
            ['<b>줄 번호가 인용의 기준이다.</b> 원문이 바뀌면 <code>cites.json</code>의 줄 해시가 어긋나 검사기가 잡는다.',
             'manifest에 원문이 없으면 노트를 쓰지 않고 멈춘다 — 변환 파이프라인 쪽 문제다.'],
        ),
        'topic': (
            ['py -3.13 scratchpad/ytsub.py &lt;영상ID&gt;', 'py -3.13 scratchpad/clip_one.py &lt;URL&gt; &lt;YYYYMMDD&gt;',
             'content/understanding/&lt;주제 또는 화자&gt;/'],
            ['<b>유튜브는 자막 전문을 받는다.</b> 설명란 요약으로 때우지 않는다.',
             '네이버 프리미엄 유료 텍스트는 CDP 크롬으로 파싱하고 <b>원문은 로컬에만</b> 둔다. 공개엔 요약만.'],
        ),
        'semi': (
            ['CDP 크롬 9222 (chrome-semianalysis 프로필)', 'input/clippings/', 'raw/linkedin/'],
            ['LinkedIn은 <b>「최근」 정렬로 바꾼 뒤</b> 스크롤한다. 기본값 「인기순」은 오래된 글을 섞어 새 글을 굶긴다.',
             '뉴스레터는 <code>paywalled:false</code>이고 <code>text_len</code>이 6000을 훨씬 넘어야 한다. <b>부분 클립으로 변환하지 않는다</b> — 세션이 만료된 것이다.',
             '웹소켓은 <code>suppress_origin=True</code>, 크롬은 <code>--remote-allow-origins=*</code> 없으면 403.'],
        ),
    },
    # ② 가공
    {
        'unified': (
            ['insights/notes/&lt;yymmdd&gt;-&lt;슬러그&gt;.md', 'insights/synth/cross-*.md',
             'insights/briefs/*-지금-상태.md', 'insights/tracks/*.md'],
            ['<b>문서 하나에 노트 하나.</b> 여러 문서를 한 노트에 눌러 담으면 요약의 요약이 된다 — 원자 체계를 폐기한 이유다.',
             '노트는 3KB 이하(N5 WARN). 넘으면 서술 단계에서 원문을 다시 읽는 편이 낫다는 신호다.',
             '노트는 문서가 말한 것만 담는다. <b>티커·수혜/피해·전망은 서술에서</b> 한다.',
             '교차는 노트 층에서 일어난다 — 노트 전량이 한 콜에 들어간다.'],
        ),
        'topic': (
            ['생성기의 <code>CARDS</code> 목록에 dict 추가', 'scripts/card_lib.py (스키마 한 벌)',
             'slim_oneliner · slim_points 6~8 · slim_stats 4'],
            ['<b>채널이 아니라 주제로 고른다.</b> 같은 채널이라도 주제가 다르면 다른 페이지다.',
             '<b>슬림 포인트는 자막 전문에서 직접 뽑는다.</b> 카드에 쓴 문장이나 요약 md를 다시 줄이면 「누가 무엇을」이 빠지면서 뜻이 뒤집힌다(용인 편).',
             '<code>slim_*</code>는 렌더링 선택이라 <code>points</code>·<code>table</code>·<code>stats</code>·<code>clash</code> 원본은 카드에 그대로 남긴다.'],
        ),
        'semi': (
            ['대시보드/소셜 신호 히스토리.html (손으로 편집)',
             'semianalysis-transformer 에이전트', 'content/newsletter/**'],
            ['<b>여기는 카드 체계가 아니다.</b> <code>insight-upload</code> 대상이 아니고 지금 형태를 그대로 둔다.',
             '히스토리 카드 <code>&lt;span class="sn"&gt;</code>의 <b>첫 문장은 이 글이 무슨 뜻인지</b>를 말한다. 원문 논증을 중간부터 옮기지 않는다 — 미러가 이 문장을 카드 제목으로 쓴다.',
             '뉴스레터 변환은 길고 토큰을 많이 먹으니 <b>서브에이전트에 위임</b>해 메인 컨텍스트를 지킨다.'],
        ),
    },
    # ③ 집필 룰
    {
        'unified': (
            ['insight-review 스킬 「집필 계약」', 'check_prose.py의 SECTION_ORDER'],
            ['<b>카드 하나 = 어긋남 하나.</b> 쌍의 양쪽은 같은 층위여야 한다. 「그리고」로 두 쌍을 이으면 그 자리가 쪼갤 자리다.',
             '<code>## 주장</code> 문단의 부품과 순서 — ① 쌍의 양쪽을 실명으로 ② 어긋남의 주체를 하나로 ③ 양쪽의 값에 각각 인용 ④ 이 카드가 정하는 것.',
             '<b>역방향 읽기</b> — 주장 문단을 가리고 나머지 절만 읽어 주장을 다시 뽑는다. 다르면 <b>사례가 맞다</b>. 사례를 빼서 주장에 맞추는 게 결함 유형 1이다.',
             '<b>한 회차에 한두 장만 뽑는다.</b> 6장 배치 생산이 「카드끼리 겹친다」의 직접 원인이었다.',
             '인용은 문장 끝 마침표 앞, 앞에 공백. 화면에는 <code>L123</code>만 남고 문서명은 tooltip으로 들어간다.'],
        ),
        'topic': (
            ['insight-upload 스킬 「카드 형식」', 'korean-readability 스킬'],
            ['<b>gain</b> 필수 — 접힌 채로 고르는 기준이다. 옛 언더스탠딩 카드엔 이게 없어 제목만 보고 골라야 했다.',
             '<b>clash(반론·충돌) 필수</b> — 한 편만 읽고 결론 내리지 않게 다른 편이나 SemiAnalysis 코퍼스와 어긋나는 지점을 박는다. 수익 사례가 전면에 나올수록 길게.',
             '<b>stats는 본문에 나온 숫자만.</b> 추정치를 만들지 않는다. quote는 원문 그대로, 다듬지 않는다.',
             '표는 비교 대상이 둘 이상일 때만. <b>탭으로 나누지 말고 한 화면에 나란히</b> 둔다.',
             '따옴표는 화자가 한 말로 읽힌다 — <b>자막에 있는 말만</b> 넣는다.'],
        ),
        'semi': (
            ['LINKEDIN_RULES.md §2 필터 · §5.6'],
            ['<b>제외</b> — 채용 공고, 행사·웨비나 홍보, 수상·기념, 내용 없는 구독 유도. <b>포함</b> — 시장·기술 분석, 숫자·차트, 공급망·기업 동향.',
             '제외한 것도 대장에 제목 한 줄 + <code>제외(사유)</code>로 남긴다. 재처리를 막는 유일한 장치다.',
             '이미 대장에 있는 게시물은 건너뛴다(URN 또는 날짜+첫 줄로 식별) — 재수집이 전체 재처리가 되지 않게.'],
        ),
    },
    # ④ 검사
    {
        'unified': (
            ['check_notes N1~N7', 'check_prose P1~P7', 'check_read R1~R12', 'check_cite C1', 'check_fresh F1~F3'],
            ['<b>다섯을 다 돌린다.</b> 앞의 셋만 돌려 푸시한 이력이 있다 — 2026-08-15에 <code>check_read</code> FAIL 0으로 통과했는데 <code>check_cite</code> 확인필요 6건과 <code>check_fresh</code> FAIL 3건을 달고 나갔다.',
             '<code>check_notes</code> FAIL이면 여기서 멈춘다. <b>줄 번호를 손으로 맞추지 말고</b> 그 문서를 재추출한다.',
             '<code>check_prose</code> FAIL은 <b>용어를 지우지 말고 괄호로 푼다.</b> 지웠다가 되돌린 이력이 있다.',
             '<code>check_cite</code> 확인필요는 기계가 절반만 본 것이다. <b>원문 줄을 열어 사람이 확인한다</b> — 숫자가 그 줄에 있어도 뜻이 다를 수 있다.',
             '<code>check_fresh</code> F1은 날짜만 미루지 않는다. 안 바뀐다고 판단했으면 <b>그 판단의 근거를 본문에</b> 쓴다.'],
        ),
        'topic': (
            ['py -3.13 scratchpad/check_slim.py'],
            ['<b>FAIL</b> — 따옴표 인용이 자막에 없다(유사도 0.55 미만). 자동 자막은 오인식이 많아 완전 일치가 아니라 유사도로 본다.',
             '<b>경고</b> — 숫자를 자막에서 못 찾았다. 3.4억 ↔ 3억 4천 같은 표기 차이일 수 있어 사람이 본다.',
             '<b>경고</b> — 전문용어에 괄호 설명이 없다(<code>GLOSS_TERMS</code>). 새 용어를 쓰면 그 목록에 추가한다.'],
        ),
        'semi': (
            ['전용 검사기 없음'],
            ['게이트는 수집 쪽에 있다 — <code>text_len &gt; 6000</code>, <code>paywalled:false</code>.',
             '<b>여기가 이 갈래의 약한 고리다.</b> 노트·카드와 달리 기계가 문장을 보지 않는다. 첫 문장 규칙(§5.6)과 필터는 사람이 지킨다.'],
        ),
    },
    # ⑤ 생성
    {
        'unified': (
            ['insights/gen_insightview.py', 'insights/gen_entity_board.py musk', 'insights/gen_map.py',
             'insights/gen_manifest.py · coverage.py'],
            ['클러스터·좌표를 건드렸으면 <code>refresh_provenance.py</code> → <code>validate_insights.py</code> → <code>gen_dashboard.py</code>·<code>gen_map.py</code>.',
             '공유 CSS는 <code>insights/style.py</code>의 <code>BASE</code>다. <b>페이지마다 토큰을 새로 정하지 않는다.</b>'],
        ),
        'topic': (
            ['scratchpad/gen_realestate_dashboard.py', 'scratchpad/gen_usa_dashboard.py',
             'scratchpad/gen_finance_dashboard.py', 'scripts/add_card.py --section sec-ai'],
            ['<b>AI·인프라·에너지만 생성기가 없다.</b> 카드 dict를 파일 하나에 담아 <code>add_card.py</code>로 끼워 넣는다.',
             '섹션 순서는 각 생성기의 <code>SEC_ORDER</code>가 정한다. <b>섹션 번호는 손대지 않는다</b> — 다시 매겨진다.',
             '<code>scratchpad/dash_common.py</code>가 <code>언더스탠딩 대시보드.html</code>의 <code>&lt;style&gt;</code>을 CSS 원본으로 읽는다. <b>파일명을 바꾸지 않는다</b>(표시 이름만 AI·인프라·에너지).',
             '옛 형식 카드 26장은 <b>소급 변환하지 않는다.</b> 한동안 두 형식이 섞인다.'],
        ),
        'semi': (
            ['py scripts/gen_bmirror.py [일수=14]', 'py scripts/gen_rollup.py'],
            ['<b>자동은 ① 소셜 신호뿐이다.</b> 히스토리 최근 N일을 파싱해 미러로 다시 깐다 — <code>linkedin-update</code>로 히스토리를 갱신한 뒤 돌리면 동기된다.',
             '<b>②~④는 손으로 고친다</b> — 뉴스레터 최근분, 클러스터 종합 판단, 기업 익스포저. 「대시보드 HTML은 생성물」 원칙의 예외가 여기다.',
             'NVIDIA 1차 신호는 <code>gen_bmirror.py</code>의 <code>NVROWS</code>에 날짜별로 직접 적는다.'],
        ),
    },
    # ⑥ 발행
    {
        'unified': (
            ['대시보드/통합 인사이트.html', 'site 슬러그 <code>/unified</code> 🔒'],
            ['공개 도메인에서는 <b>잠금</b>이다 — <code>functions/_middleware.js</code>의 <code>PROTECTED</code>.'],
        ),
        'topic': (
            ['py scripts/update_card_ledger.py', 'py scripts/gen_site.py',
             '<code>/realestate</code> <code>/finance</code> <code>/understanding</code> 공개 · <code>/usa-academy</code> 🔒'],
            ['<b>카드를 올렸으면 주간·월간 리포트도 같이 손본다.</b> 산문은 사람이 쓴다 — <code>data/rollup_notes*.json</code>. 기간 기준은 <b>매체 업로드일</b>이지 처리한 날이 아니다.',
             '<code>update_card_ledger.py</code>를 건너뛰면 NEW 배지가 안 붙는다. 기준은 영상 업로드일이 아니라 <b>카드가 사이트에 처음 올라온 날</b>이고 그 날짜는 대장에만 있다.',
             '<b>리포트 한 편 때문에 페이지를 새로 만들지 않는다</b> — 주제 대시보드의 섹션으로 넣는다. 그렇게 늘어난 게 19장이었다.'],
        ),
        'semi': (
            ['site 슬러그 <code>/semianalysis</code> 🔒'],
            ['LinkedIn 배치를 돌린 뒤 <b>소셜 신호 히스토리와 이 대시보드 둘 다</b> 갱신한다.',
             '주제 대시보드에는 <b>해당 주제 신호만</b> 골라 반영한다.'],
        ),
    },
]

# 세 갈래가 함께 지키는 것 — 갈래별 표에 세 번 적지 않는다
COMMON = [
    ('푸시 전 한 방', 'py -3.13 scripts/build_all.py',
     '생성기 전부와 검사기 다섯을 순서대로 돌리고 하나라도 실패하면 종료 코드 1이다. <code>--check</code>는 검사만.'),
    ('FAIL 0', '다섯 검사기 전부',
     'FAIL이 남은 채로 푸시하지 않는다. 검사기가 <b>못 잡는 것</b>도 안다 — 숫자는 맞는데 뜻이 다른 경우(68,928달러가 배선 값인지 백플레인 값인지)는 원문 줄을 열어야 한다.'),
    ('용어', '남기고 괄호로 푼다',
     '전문용어를 쉬운 말로 치환하지 않는다. 첫 등장에 괄호로 푼다 — 용적률(대지면적 대비 지을 수 있는 총 바닥면적의 비율).'),
    ('일반론 금지', '숫자 · 명명된 주체 · 비직관',
     '「중요하다」·「주목된다」는 쓰지 않는다.'),
    ('생성물', '대시보드 HTML은 손으로 고치지 않는다',
     '고칠 것은 <code>insights/</code> 아래 원본과 <code>gen_*.py</code>다. <b>예외는 SemiAnalysis ②~④와 소셜 신호 히스토리</b> — 이 둘만 손으로 쓴다.'),
    ('커밋', '의미 단위마다 바로',
     '몰아서 하지 않는다. <code>main</code>에 푸시하면 Cloudflare Pages가 <code>gen_site.py</code>를 돌려 자동 배포한다.'),
    ('인코딩', 'PYTHONIOENCODING=utf-8',
     '콘솔이 cp949라 파이썬 실행에 붙인다.'),
]

CSS = r'''
  .lede2{color:var(--sub);font-size:var(--t-body);margin:10px 0 0;max-width:70ch}
  /* 공통 밴드 — 갈래별 표에 같은 말을 세 번 적지 않으려고 위로 뺐다 */
  .common{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin:18px 0 0}
  .cm{border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:12px 14px;box-shadow:var(--shadow)}
  .cm b{display:block;font-size:var(--t-lbl);font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);margin:0 0 5px}
  .cm .w{display:block;font-size:var(--t-body);font-weight:800;color:var(--ink);margin:0 0 4px}
  .cm p{margin:0;font-size:var(--t-meta);color:var(--sub)}

  /* 매트릭스 — 행은 단계, 열은 갈래. 비교 대상이라 탭으로 나누지 않는다 */
  .mx{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:14px 0 0}
  .lane{border:1px solid var(--line);border-top:3px solid var(--ac);border-radius:var(--r);
        background:var(--card);padding:13px 15px;box-shadow:var(--shadow);position:sticky;top:0;z-index:2}
  .lane .nm{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:0;display:flex;gap:8px;align-items:baseline}
  .lane .nm span{font-size:19px}
  .lane p{margin:6px 0 0;font-size:var(--t-meta);color:var(--sub)}
  .lane .rl{margin:8px 0 0;font-size:var(--t-lbl);font-weight:700;color:var(--ac);
            font-family:ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:0}

  .band{grid-column:1/-1;display:flex;align-items:baseline;gap:10px;margin:16px 0 -2px;
        padding:0 2px 7px;border-bottom:1px solid var(--line)}
  .band b{font-size:var(--t-body);font-weight:850;color:var(--ink);letter-spacing:-.01em}
  .band i{font-style:normal;font-size:var(--t-meta);color:var(--faint)}

  .cell{border:1px solid var(--line);border-left:3px solid var(--ac);border-radius:0 var(--r) var(--r) 0;
        background:var(--card);padding:12px 14px;box-shadow:var(--shadow)}
  .cell .lb{display:none;font-size:var(--t-lbl);font-weight:800;color:var(--ac);margin:0 0 6px}
  .thing{display:block;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:var(--t-meta);
         color:var(--sub);background:var(--sunk);border-radius:6px;padding:5px 8px;margin:0 0 4px;
         word-break:break-word}
  .cell ul{margin:9px 0 0;padding:0;list-style:none}
  .cell li{font-size:var(--t-meta);color:var(--sub);margin:0 0 7px;padding-left:11px;position:relative}
  .cell li:last-child{margin-bottom:0}
  .cell li::before{content:"";position:absolute;left:0;top:.62em;width:4px;height:4px;border-radius:50%;background:var(--line)}
  .cell li b{color:var(--ink);font-weight:700}
  .cell code{font-size:.9em}

  /* 좁은 화면 — 열이 무너지면 단계별로 세 갈래가 위아래로 붙는다.
     그래서 셀마다 어느 갈래인지 이름을 되살린다 */
  @media (max-width:860px){
    .mx{grid-template-columns:1fr}
    .lane{position:static}
    .cell .lb{display:block}
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


def cell_html(lane_key, lane_name, ac, things, rules):
    t = ''.join('<span class="thing">%s</span>' % x for x in things)
    r = ''.join('<li>%s</li>' % x for x in rules)
    return ('<div class="cell" style="--ac:%s">'
            '<p class="lb">%s</p>%s<ul>%s</ul></div>' % (ac, lane_name, t, r))


ACCENT = {'unified': '#2563eb', 'topic': '#0f9d76', 'semi': '#b4522b'}


def main():
    out = [HEAD % (style.BASE, CSS)]
    out.append('<header>'
               '<p class="eyebrow">관리자 · 비공개</p>'
               '<h1>데이터 처리 지도</h1>'
               '<p class="lede">대시보드는 세 갈래로 나뉘고 갈래마다 소스·집필 룰·검사기가 다르다. '
               '룰 문서를 다 읽지 않고도 <b>어느 룰이 어느 단계에 걸리는지</b> 보라고 만든 장이다.</p>'
               '<p class="lede2">행은 단계, 열은 갈래다. 세 갈래가 함께 지키는 것은 아래 공통 밴드에 한 번만 적었다.</p>'
               '<div class="meta"><span>룰 원본 · README.md · CLAUDE.md · LINKEDIN_RULES.md · '
               '.claude/skills/</span><span>생성 · scripts/gen_admin.py</span></div>'
               '</header>')

    out.append('<h3 class="sec">세 갈래가 함께 지키는 것</h3><div class="common">')
    for lbl, word, desc in COMMON:
        out.append('<div class="cm"><b>%s</b><span class="w">%s</span><p>%s</p></div>' % (lbl, word, desc))
    out.append('</div>')

    out.append('<h3 class="sec">갈래 × 단계</h3><div class="mx">')
    for key, emo, name, one, rule_src in LANES:
        out.append('<div class="lane" style="--ac:%s"><p class="nm"><span>%s</span>%s</p>'
                   '<p>%s</p><p class="rl">%s</p></div>' % (ACCENT[key], emo, name, one, rule_src))
    for i, (stg, note) in enumerate(STAGES):
        out.append('<div class="band"><b>%s</b><i>%s</i></div>' % (stg, note))
        for key, emo, name, _one, _src in LANES:
            things, rules = CELLS[i][key]
            out.append(cell_html(key, '%s %s' % (emo, name), ACCENT[key], things, rules))
    out.append('</div>')

    out.append('<footer>이 장은 룰의 원본이 아니라 <b>색인</b>이다. 룰이 바뀌면 원본 문서를 먼저 고치고 '
               '<code>scripts/gen_admin.py</code>의 <code>CELLS</code>를 맞춘 뒤 다시 만든다. '
               '공개 도메인에서는 <code>/admin</code>으로 잠겨 나간다.</footer>')
    out.append('</main></body></html>')

    html = '\n'.join(out)
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print('관리자 대시보드 — 갈래 %d · 단계 %d · 셀 %d  ->  %s'
          % (len(LANES), len(STAGES), len(LANES) * len(STAGES), os.path.basename(OUT)))


if __name__ == '__main__':
    main()
