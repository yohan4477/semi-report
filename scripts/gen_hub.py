# Yomianalysis — 전체 입구 한 장.
#
# 왜 있나: 대시보드가 19개까지 늘어나면서 "어디로 들어가야 하는지"를 아는 페이지가 없어졌다.
# 2026-08-09에 11개로 줄이면서 입구를 하나 세웠다. 여기만 북마크하면 된다.
#
# 예외 하나: 「관리자 대시보드」는 여기에 넣지 않는다. 읽을거리가 아니라 룰 색인이고
# 공개 사이트에서 /admin 으로 잠겨 나간다(gen_admin.py · gen_site.py).
# 규칙: 페이지를 새로 만들면 반드시 아래 TOPICS에 한 줄 넣는다. 여기에 없는 페이지는
# 사실상 없는 페이지다. 반대로, 리포트 한 편 때문에 페이지를 새로 만들지 않는다
# (REPORT_RULES.md 참조 — 그렇게 늘어난 게 19개였다).
import os, io, re, sys, urllib.parse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'insights'))
import style

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, '대시보드', 'Yomianalysis.html')
import ui_bits


# 2026-08-09부터 claude.ai 아티팩트를 쓰지 않는다. 정본은 GitHub Pages 하나다 —
# 두 벌을 두면 한쪽이 몇 주씩 낡고, 아티팩트는 도구로 지울 수도 없다.
P = 'https://yohan4477.github.io/semi-report/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/'


def pg(name):
    return P + urllib.parse.quote(name)

# (이모지, 이름, 주소, 한 줄, [배지])  — 배지는 그 페이지가 무엇을 근거로 삼는지다
TOPICS = [
    ('🔬', '반도체 · AI · 인프라',
     '칩에서 전력망까지. 이 저장소의 본진이고, 새 소스는 대부분 여기로 들어온다.',
     [
      ('🧭', 'SemiAnalysis 대시보드', pg('SemiAnalysis 대시보드.html'),
       '소셜·영상 신호, 뉴스레터 최근분, 클러스터 종합 판단, 회사별 걸린 정도까지 한 화면에',
       ['SemiAnalysis']),
      ('🧩', '통합 인사이트', pg('통합 인사이트.html'),
       'AI 판 · AI 밖 · 부동산 세 묶음. 노트를 한 번에 읽어야 보이는 것만 실었고, 문장 옆 줄번호를 누르면 근거가 된 원문 줄로 간다',
       ['SemiAnalysis', '제3자 해설', '노트 검사기']),
      ('🗺️', '인사이트 지도', pg('인사이트 지도.html'),
       '좌표가 있는 클러스터를 스크롤하며 따라가는 지도',
       ['SemiAnalysis']),
      ('🧩', '개념 지도', pg('개념 지도 — LLM 계층·병렬화.html'),
       '학습·추론에서 모델 계층, 병렬화, GPU 랙까지 구조를 한 장에',
       ['SemiAnalysis']),
      ('📖', '모델 가이드', pg('모델 가이드.html'),
       'AI 모델을 처음 보는 사람이 순서대로 읽는 장. 토큰과 학습 세 단계부터 시작해 값이 어디서 붙고 누가 버는지까지, 카드마다 그림을 같이 붙였다',
       ['SemiAnalysis', '제3자 해설']),
      ('🧬', '알고리즘 계보', pg('알고리즘 계보.html'),
       '무엇이 무엇을 갈아치웠고 그 대가로 무엇을 냈는지를 궤도 일곱으로 세운 장. 어텐션·전문가·디코딩·학습·정밀도·실리콘·서빙 순서이고, 약속을 못 지키고 낙오한 갈래도 그대로 싣는다',
       ['SemiAnalysis']),
      ('🚀', '추적 · 일론 머스크', pg('추적 - 일론 머스크.html'),
       '스페이스X·xAI·Colossus·APR Energy가 지금 어디쯤인지. 부지 지도는 시점 탭으로 용량이 언제 늘었는지 보여준다',
       ['SemiAnalysis', 'LinkedIn']),
      ('🗂️', '소셜 신호 히스토리', pg('소셜 신호 히스토리.html'),
       'LinkedIn·YouTube 신호 전체 아카이브. SemiAnalysis 대시보드 ①이 여기를 비춘다',
       ['LinkedIn', 'YouTube']),
      ('📊', '임팩트 타임라인', pg('소스 타임라인.html'),
       '이벤트 하나가 어디까지 번지는지를 가지로 그린다. 2차 파급까지만 — 3차는 추측이다',
       ['LinkedIn']),
      ('⚡', '산업/시장 인사이트', pg('산업시장 대시보드.html'),
       '같은 주제를 국내 해설 쪽에서 본 것. 데이터센터 전력·에너지 수급·중동 유가에 금리·환율까지',
       ['제3자 해설']),
      ('📚', '용어사전', pg('용어사전.html'),
       '읽다 막히는 말을 하나씩 푸는 장. 카드 하나가 용어 하나이고, 그 말이 가리키는 물건이 실제로 어떻게 도는지를 그림으로 같이 단다',
       ['SemiAnalysis']),
      ('🔒', '언더스탠딩 프리미엄', pg('언더스탠딩 프리미엄 대시보드.html'),
       '네이버 프리미엄 구독물 요약. 전기요금 구조와 원유 다변화, 호남 반도체 산단',
       ['제3자 해설']),
     ]),
    ('🏠', '부동산',
     '채널을 가리지 않고 부동산 주제만 모은다.',
     [
      ('🏠', '부동산 인사이트', pg('부동산 대시보드.html'),
       '공급·세제·건설 원가·토지. 유튜브는 자막 전문 기반 요약이다',
       ['제3자 해설']),
     ]),
    ('🩺', '건강',
     '몸에서 실제로 벌어지는 일. 카드 단위가 영상이 아니라 주제다.',
     [
      ('🩺', '건강 인사이트', pg('건강 대시보드.html'),
       '만성 염증·대사·수면. 해부도를 함께 그렸고 진단이나 처방이 아니다',
       ['제3자 해설']),
     ]),
]

# 채널 단위로 만들어 둔 아카이브. 주제 축으로 옮기는 중이라 따로 세워 둔다
LEGACY = [
    ('🎓', '미국주식 사관학교', pg('미국주식 사관학교 대시보드.html'),
     '네이버 프리미엄 유료 채널 요약. 종목이 나오지만 추천이 아니고 가격 검증도 없다'),
    ('🎖️', '이선엽 시황', pg('이선엽 시황 대시보드.html'),
     '삼프로TV 유료 클럽의 실시간 텍스트 시황을 주제별로 묶었다. 종목이 나오지만 추천이 아니다'),
    ('🧮', '20년차 회계사가 남긴 모든 것', pg('회계사 대시보드.html'),
     '네이버 프리미엄 유료 채널 요약. DCF 방법론 네 편과 삼성전자 평가 세 편이고 종목 추천이 아니다'),
]

CSS = r'''
  .tp{margin:44px 0 0;padding-top:26px;border-top:1px solid var(--line)}
  .tp:first-of-type{border-top:0;padding-top:8px;margin-top:26px}
  .tph{display:flex;align-items:baseline;gap:10px;margin:0}
  .tpe{font-size:24px;line-height:1}
  .tph h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:0}
  .tph .n{font-size:var(--t-lbl);font-weight:800;color:var(--faint);font-variant-numeric:tabular-nums}
  .tp>p{font-size:var(--t-body);color:var(--sub);margin:6px 0 0;max-width:64ch}
  .cards{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));margin-top:14px}
  .pc{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);
      border-left:3px solid var(--accent);border-radius:var(--r);padding:13px 15px;box-shadow:var(--shadow);
      transition:transform .12s cubic-bezier(.32,.72,0,1),border-color .12s}
  .pc:hover{transform:translateY(-1px);border-color:var(--accent)}
  .pc:active{transform:scale(.995)}
  .pct{display:flex;align-items:baseline;gap:7px}
  .pct .e{font-size:15px;line-height:1}
  .pct b{font-size:var(--t-lead);font-weight:800;letter-spacing:-.01em}
  .pc p{font-size:var(--t-body);color:var(--sub);margin:5px 0 0;line-height:1.55}
  .bd{margin:8px 0 0;display:flex;flex-wrap:wrap;gap:5px}
  .bd i{font-style:normal;font-size:var(--t-lbl);font-weight:800;padding:2px 8px;border-radius:999px;
        background:var(--sunk);color:var(--faint)}
  .bd i.semi{background:var(--soft);color:var(--accent2)}
  .bd i.warn{background:#f6ecda;color:#9a5b12}
  @media (prefers-color-scheme:dark){.bd i.warn{background:#2a2113;color:#d79a4e}}
  .rule{background:var(--soft);border-left:3px solid var(--accent);border-radius:0 var(--r) var(--r) 0;
        padding:12px 16px;margin:26px 0 0;font-size:var(--t-body);line-height:1.6}
  .rule b{color:var(--accent2)}
  @media (max-width:640px){
    .cards{grid-template-columns:1fr}
    .pc{padding:14px 15px}
  }
'''


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def card(e, name, href, note, badges=()):
    b = ''
    if badges:
        b = '<p class="bd">%s</p>' % ''.join(
            '<i class="%s">%s</i>' % ('semi' if x == 'SemiAnalysis' else
                                      'warn' if x == '미발행' else '', esc(x))
            for x in badges)
    return ('<a class="pc" href="%s"><span class="pct"><span class="e">%s</span>'
            '<b>%s</b></span><p>%s</p>%s</a>'
            % (esc(href), e, esc(name), esc(note), b))


def sec_id(name):
    """묶음 하나를 지목하는 주소. 이름에서 뽑는다 — 순번으로 매기면 묶음이 하나 끼는 날
    남이 받아 둔 링크가 다른 묶음을 가리킨다."""
    return 'sec-' + re.sub(r'[^0-9A-Za-z가-힣]+', '-', name).strip('-')


def build():
    blocks = []
    for emoji, name, lede, pages in TOPICS:
        blocks.append(
            '<section class="tp" id="%s"><div class="tph"><span class="tpe">%s</span>'
            '<h2>%s</h2><span class="n">%d장</span>%s</div><p>%s</p>'
            '<div class="cards">%s</div></section>'
            % (sec_id(name), emoji, esc(name), len(pages), ui_bits.copy_btn(sec_id(name)),
               esc(lede), ''.join(card(*p) for p in pages)))
    blocks.append(
        '<section class="tp" id="sec-소스별-아카이브"><div class="tph">'
        '<span class="tpe">📼</span>'
        '<h2>소스별 아카이브</h2><span class="n">%d장</span>%s</div>'
        '<p>주제가 아니라 채널로 묶여 있는 것들이다. 한 채널이 여러 주제를 다루면 '
        '읽는 사람이 골라내야 해서, 위의 주제 쪽으로 옮기는 중이다.</p>'
        '<div class="cards">%s</div></section>'
        % (len(LEGACY), ui_bits.copy_btn('sec-소스별-아카이브'),
           ''.join(card(*p) for p in LEGACY)))

    n = sum(len(p) for _, _, _, p in TOPICS) + len(LEGACY)
    html = TMPL.replace('__CSS__', style.BASE + CSS) \
               .replace('__BLOCKS__', ''.join(blocks)) \
               .replace('__N__', str(n)) \
               .replace('__T__', str(len(TOPICS))) \
               .replace('__L__', str(len(LEGACY)))
    io.open(OUT, 'w', encoding='utf-8').write(html + ui_bits.COPY_JS + ui_bits.TOP_BTN)
    print('OK: %d장 -> %s' % (n, OUT))


TMPL = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yomianalysis</title>
<style>__CSS__</style>
<div class="wrap">
<header>
  <p class="eyebrow">Yomianalysis</p>
  <h1>어디로 들어갈까</h1>
</header>
__BLOCKS__
<div class="rule"><b>페이지를 늘리지 않는 규칙.</b> 리포트 한 편이나 릴리스 하나 때문에
대시보드를 새로 만들지 않습니다. 주제 대시보드의 한 섹션으로 넣고 원문을 링크합니다 —
2026-08-09에 19장을 11장으로 줄인 이유가 그것이었습니다.</div>
<footer>
<p class="lede">SemiAnalysis 뉴스레터와 LinkedIn·YouTube 신호, 그리고 제3자 해설을
  한국어로 옮기고 엮은 것들입니다. 여기만 북마크하면 됩니다 — 나머지는 이 페이지에서 닿습니다.</p>
<div class="meta"><span>페이지 __N__장</span><span>주제 __T__ · 소스 아카이브 __L__</span></div>
이 저장소는 public입니다. 종목이 언급되더라도 투자 추천이 아니며,
가격·밸류에이션·타이밍은 이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
