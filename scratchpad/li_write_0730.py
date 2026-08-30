import io, re

P = r'C:\Users\y\semianalysis\대시보드\소셜 신호 히스토리.html'
t = io.open(P, encoding='utf-8').read()

LI = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M7.1 9.2H4.7V19h2.4zM5.9 4.8a1.45 1.45 0 100 2.9 1.45 1.45 0 000-2.9zM19.3 13.4c0-2.9-1.6-4.4-3.7-4.4-1.7 0-2.4 1-2.8 1.6V9.2h-2.4V19h2.4v-5.2c0-1.4.6-2.2 1.8-2.2 1.1 0 1.6.8 1.6 2.2V19h2.4z"/></svg>'
YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1" y="4.5" width="22" height="15" rx="4" fill="#f00"/><path d="M10 9.2l5 2.8-5 2.8z" fill="#fff"/></svg>'
YTBADGE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="5" fill="#FF0000"/><path fill="#fff" d="M10 8.5v7l6-3.5z"/></svg>영상 &rarr;'
NLBADGE = None  # 뉴스레터 배지는 기존 파일에서 그대로 가져온다


def li_row(aid, text, arts=()):
    a = ''.join(f' <a class="art" href="{u}" target="_blank" rel="noopener">{label}</a>' for u, label in arts)
    return (f'<div class="row"><a class="rowmain" href="https://www.linkedin.com/feed/update/urn:li:activity:{aid}/"'
            f' target="_blank" rel="noopener"><span class="src">{LI}</span><span class="sn">{text}</span></a>{a}</div>')


def yt_row(url, text):
    return (f'<div class="row"><a class="rowmain" href="{url}" target="_blank" rel="noopener">'
            f'<span class="src">{YT}</span><span class="sn">{text}</span></a></div>')


def day(date, rows):
    return f'<div class="day"><h3>{date}</h3>' + ''.join(rows) + '</div>\n'


NL = 'https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters'
d0730 = day('2026-07-30', [
    li_row('7488579434934083584',
           'PCB 업계가 말하는 "M8·M9"는 파나소닉 메그트론(Megtron) 등급을 뜻하는 업계 은어다. 메그트론 4→8로 갈수록 유전손실(Df)이 낮아져 고주파에서 신호가 덜 깎이기 때문에, 이제는 파나소닉 제품이 아니라 EMC·두산이 만들어도 "M8급"이라 부른다. AI 서버 SerDes 속도가 계속 오르면서 고등급 동박적층판(CCL)이 하드웨어 공급망에서 가장 빡빡하고 빠르게 크는 병목 소재가 됐다. 첨부는 메그트론 4~8S 아웃가스 데이터(총질량손실 0.16→0.34%).'),
    li_row('7488356098895171584',
           '신규 뉴스레터 「The Wild Wild West Of LEGO Datacenters」 — 다들 모듈러라 말하는데 벤더 주장이 실제로 맞는지 검증했다. 저커버그의 천막 데이터센터, AWS 후디니, 모듈러 용량 60GW+ 추적, 벤더 지형도 전수 매핑, Vertiv의 MW당 콘텐츠 2배 상승.',
           arts=((NL, '뉴스레터 &rarr;'),)),
    li_row('7488349481403613184',
           '주간 팟캐스트 클립 「Trading Houses For Datacenters」 — 반도체 주가 조정 국면과 랩들의 움직임을 대비시킨 회차.',
           arts=(('https://youtu.be/kY64Mmo0mtc', YTBADGE),)),
    li_row('7488277540936269824',
           '시장은 2028년 WFE(반도체 장비 투자)를 $1,900~2,000억으로 보지만 SemiAnalysis는 $2,300억 이상을 본다. 근거는 캐파와 가격 두 축 — AMAT은 공장 바닥이 이미 준비돼 생산량 2배가 가능하다 하고 Lam은 4년새 생산능력을 거의 2배로, TEL은 FY2029까지 1.8배를 목표한다. 가격도 오른다: ASML이 2Q26 실적에서 인상을 시사, TSMC는 캐펙스 +15% 가이던스의 주요 원인으로 장비가 인플레를 지목, 중국 고객은 DUV +10%에 합의, TEL은 ~30% 인상을 논의 중이라는 채널 체크. 인상분은 거의 100% 장비사 매출총이익으로 남는다 — 협력사(Ichor 8~17%, Ultra Clean 11~21%)는 10년간 마진 밴드가 고정돼 가격 전가력이 없다. 10% 인상이면 장비사 마진은 역사적 고점보다 1~5%p 위.'),
])

d0729 = day('2026-07-29', [
    li_row('7487932851913564160',
           'AI로 만든 영상을 올렸다가 팔로워들에게 "무슨 일이냐", "괜찮냐", "링크드인 슬롭 아니냐"는 반응만 받았다. 정보성 신호는 없는 실험성 게시물.'),
])

d0728 = day('2026-07-28', [
    li_row('7487673418671300608',
           '밈 — 사람이 직접 올린 PR(GLM-4.5 FP8 MI355X SGLang 단일노드)과 에이전트가 자동으로 올린 PR([AgentX] vLLM DeepSeek-V4 GB300, 설명란 비어 있음)을 나란히 놓고 비꼰 것. 추론 프레임워크 저장소에 에이전트 생성 PR이 밀려드는 현상을 짚었다.'),
    li_row('7487612975202185216',
           'AMD가 OpenAI·Meta에 준 워런트는 보통 "지분 인센티브"로 설명되지만, 계산해 보면 컴퓨트 가격 자체를 되돌려주는 리베이트에 가깝고 OpenAI 기준 실효 할인율이 최대 105%까지 나온다. AMD 8-K상 워런트는 주가 구간별로 베스팅되며 상단 문턱이 $600, 행사가는 사실상 0인 $0.01이라 AMD 주가가 오를수록 되돌려주는 가치가 커진다. 전량 베스팅·행사 가정 시 실효 할인 85~105% — 고객에게 돈을 얹어주며 자사 주식으로 그 값을 치르는 구조다. 물량 약정이 주가를 밀어 올리면(이미 $520+) 괜찮은 거래지만, 아니면 순환 거래가 된다.',
           arts=(('https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing', '뉴스레터 &rarr;'),)),
    li_row('7487562579930664960',
           'ClusterMAX 팀이 일론 머스크와 저커버그에게 공개 농담 — "다음 네오클라우드 등급에 xAI와 Meta도 넣고 싶으니 개발용 클러스터를 5일만 빌려달라, 특히 쿠버네티스 운영이 규격에 맞는지 검증하고 싶다." 첨부 이미지는 ClusterMAX 시상대 그림과 xAI 매크로하드·Meta 템플 부지 항공사진.'),
])

d0727 = day('2026-07-27', [
    li_row('7487514788139466752',
           'CXMT 상장 첫날이 반도체 역사상 가장 기이했다 — 공모가 ¥8.66, 시초가 ¥49.50, 종가 ¥49로 +466%, 시가총액 약 $4,880억으로 인텔($4,650억)을 넘었다. 10년 전엔 존재하지도 않던 D램 회사다. SemiAnalysis는 지난달 딥다이브에서 키몬다의 잔해에서 세계 4위 D램 업체로 올라선 과정(기술 이전, 허페이의 인내 자본, IPO 셈법)을 이미 짚었다.',
           arts=(('https://lnkd.in/eDjsbYch', '뉴스레터 &rarr;'),)),
])

d0726 = day('2026-07-26', [
    li_row('7486888338415697920',
           '밈 — TSMC를 애니메이션 비행기로, 레거시 파운드리들을 그 아래 폭발하는 지상으로 그렸다. 본문은 물음표 하나뿐이고 댓글도 "질문이 너무 많다"는 반응.'),
])

anchor = '</div>\n<div class="day">'
i = t.find('<div class="day">')
assert i > 0
new = d0730 + d0729 + d0728 + d0727 + d0726
t2 = t[:i] + new + t[i:]

# stamp 갱신
old_stamp = re.search(r'<div class="stamp">.*?</div>', t2).group(0)
t2 = t2.replace(old_stamp,
                '<div class="stamp">2026-07-30 최신화 · 2026-02-25~ · LinkedIn 350건(한글 요약, 클릭 시 원문 이동) + YouTube 7건</div>', 1)

io.open(P, 'w', encoding='utf-8').write(t2)
print('inserted. div open/close:', t2.count('<div'), t2.count('</div>'))
print('rows now:', t2.count('class="row"'))
