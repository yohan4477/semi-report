# -*- coding: utf-8 -*-
# 언더스탠딩 「부동산」 재생목록을 기준으로 처리 대기 목록을 만든다.
# 재생목록은 최신순(1번이 가장 최근)이라 그 순서를 그대로 대기 순서로 쓴다.
#   재생목록 스냅샷 -> content/understanding/_재생목록 부동산.tsv
#   대기 목록      -> content/understanding/_대기 목록.md
# 처리 완료 판정은 DONE(영상 ID -> 결과물 파일명)에 적힌 것만 인정한다.
import io, json, os, subprocess, sys, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYLIST = 'https://www.youtube.com/playlist?list=PL142diDwvogYmYEZwdN9kUXIBi9E6nXde'
TSV = os.path.join(ROOT, 'content', 'understanding', '_재생목록 부동산.tsv')
MD = os.path.join(ROOT, 'content', 'understanding', '_대기 목록.md')
TOP = 30  # 대기 목록 md에 펼쳐 적을 최신 미처리 편수

# 처리 완료 — 영상 ID: (처리일, 결과물 경로)
DONE = {
    'ug2iyPwtQdI': ('2026-08-09', '부동산/[260708] 아파트 공사비가 오른 이유 셋 - 100년 아파트는 화장실 배관에 달렸다 - 최도영.md'),
    'S_ZZxVbwK8o': ('2026-07-29', '부동산/[260729] 한국 보유세는 정말 낮은가 - 같은 집에 각 도시 세제를 붙여봤다 (1부).md'),
    'sQG-R3l6_3o': ('2026-07-30', '부동산/[260730] 전세와 거래세가 시장을 잠근다 - 필터링이 안 돌아간다 (2부).md'),
    'FhhB5GnElRg': ('2026-06-20', '부동산/[260620] 싱가포르 주택 모델 - 공급·연금·세금 세 축과 한국이 못 하는 이유.md'),
    'R840lTdtCSw': ('2026-08-04', '부동산/[260804] 일본 지방 땅값이 오르는 곳은 전부 기업을 끼고 있다 - 박상준.md'),
    'UbB0U966PLw': ('2026-08-09', '부동산/[260304] 공급 절벽은 통계 차이였다 - 같은 서울에 4천호와 3만호 - 장순원.md'),
    'YHVxAsU5Y0M': ('2026-08-09', '부동산/[260529] 20년 장기전세 첫 만기 - 계약대로 나가라와 갈 데가 없다 사이 - 장순원.md'),
    '8E2JxYShT9A': ('2026-08-09', '부동산/[260407] 땅값은 직선이 아니라 2차 함수 - 호재가 아니라 정주 인구를 보고 산다 - 김종율.md'),
    # 아래 5편은 처리해 놓고 여기 적지 않아 대기열에 남아 있던 것들이다
    'GvjknPowMsk': ('2026-08-13', '부동산/[260106] 용인에 공장이 와도 사람은 동탄에 산다 - 전기는 묻으면 되지만 물은 답이 없다 - 김시덕.md'),
    '6CNYmb_cohA': ('2026-08-09', '부동산/[260409] 상가·오피스를 집으로 바꾸기 - 평당 500만 원이면 차라리 새로 짓는다 - 장순원.md'),
    'WuKhGefGpSA': ('2026-08-09', '부동산/[260420] 착공 앞두고 시공사를 갈아치우면 - 성남 상대원2구역과 두 건의 선례 - 장순원.md'),
    '2BR4uXFZ2rY': ('2026-08-09', '부동산/[260424] 부모가 준 전세금까지 타고 올라간다 - 자금조달계획서가 국세청으로 가는 길 (2부) - 이장원.md'),
    'uJlfke5FMrM': ('2026-08-09', '부동산/[260424] 장특공제 축소는 비실거주 1주택을 겨냥한다 - 보유 공제를 깎는 두 시나리오 - 백종훈.md'),
    'sVUTmmjuZ6s': ('2026-08-14', '부동산/[260810] 300평 펜트하우스에 걸린 공공복리 - 성수동 삼표 부지와 국토부 심의 - 장순원.md'),
    'yXupZjctWjM': ('2026-08-14', '부동산/[260720] 한 동만 빼고 재건축 - 대지지분이 커도 감정가는 시세를 따라간다 - 장순원.md'),
    'dCDjXzOojdU': ('2026-08-14', '부동산/[260629] 조합장 성과급은 왜 매번 부결되나 - 계약이 없어서다 - 장순원.md'),
    'poF9rvBW5PM': ('2026-08-14', '부동산/[260609] 토지비를 0으로 만드는 상상 - 도로 위, 물 위, 그리고 잠깐 쓰는 집 - 최상희.md'),
    'NBImj7DXYyE': ('2026-08-14', '부동산/[260501] 전세사기 3분의 1 보장법 - 국가가 처음 돈을 대지만 구멍은 남았다 - 백종훈.md'),
    'UUq7EDvjbqY': ('2026-08-14', '부동산/[260423] 시골집 하나에 세금 8억 - 양도세 중과 부활 앞 네 갈래 선택 (1부) - 이장원.md'),
    'yTc15fSbXqo': ('2026-08-14', '부동산/[260326] 4.2평 아파트를 짓는 이유 - 아현1구역 공유지분 900가구를 끌어안는 법 - 장순원.md'),
    'Vfpfkvvmy9U': ('2026-08-14', '부동산/[260323] 3억 4천만 원짜리 마곡 아파트 - 토지임대부가 다시 나온 이유 - 백종훈.md'),
}
# 재생목록 밖에서 사용자가 직접 던진 편(있으면 여기 적어 대기 목록 위에 붙인다)
EXTRA = []


def fetch():
    cmd = ['py', '-3.13', '-m', 'yt_dlp', '--flat-playlist', '-J',
           '--extractor-args', 'youtube:lang=ko', PLAYLIST]
    raw = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8', 'replace')
    return json.loads(raw)


def hhmm(sec):
    if not sec:
        return ''
    m = int(sec) // 60
    return '%d분' % m


def main():
    d = fetch()
    rows = []
    for i, e in enumerate(d.get('entries') or []):
        vid = e.get('id')
        if not vid:
            continue
        rows.append((i + 1, vid, (e.get('title') or '').replace('\t', ' '), hhmm(e.get('duration'))))

    with io.open(TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('순번\t영상ID\t제목\t길이\t상태\n')
        for n, vid, t, dur in rows:
            f.write('%d\t%s\t%s\t%s\t%s\n' % (n, vid, t, dur, 'DONE' if vid in DONE else ''))

    todo = [r for r in rows if r[1] not in DONE][:TOP]
    today = datetime.date.today().isoformat()

    L = []
    L.append('# 제3자 해설 처리 대기 목록 — 부동산\n')
    L.append('기준은 언더스탠딩 **「부동산」 재생목록**입니다(최신순, 1번이 가장 최근). '
             '전체 스냅샷은 `_재생목록 부동산.tsv`에 있고, 아래 표는 그중 **아직 처리하지 않은 최신 %d편**입니다.\n' % TOP)
    L.append('- 재생목록: %s\n' % PLAYLIST)
    L.append('- 스냅샷 갱신 · 이 문서 재생성: `python scratchpad/gen_understanding_queue.py` '
             '(처리 완료는 그 파일 `DONE`에 영상 ID를 적어야 반영됩니다)\n')
    in_pl = sum(1 for r in rows if r[1] in DONE)
    L.append('- 재생목록 총 **%d편** / 그중 처리 완료 **%d편** / 미처리 **%d편** '
             '(재생목록 밖에서 처리한 편이 %d건 더 있어 아래 완료 표는 %d행입니다)\n'
             % (len(rows), in_pl, len(rows) - in_pl, len(DONE) - in_pl, len(DONE)))
    L.append('\n**운영 약속**: 사용자가 "업데이트 해"라고 하면 이 스크립트를 다시 돌려 스냅샷을 갱신한 뒤, '
             '**"최신순으로 이걸로 처리할까요?"라고 먼저 묻고** 답을 받은 다음에 요약에 들어갑니다.\n')
    L.append('\n**처리 규칙**: 유튜브는 길이·토큰과 무관하게 **자막 전문 기반 요약**이 기본입니다. '
             '결과물은 `content/understanding/부동산/`, 카드는 `대시보드/부동산 대시보드.html`'
             '(생성기 `scratchpad/gen_realestate_dashboard.py`)로 갑니다.\n')

    if EXTRA:
        L.append('\n## 재생목록 밖 — 사용자 직접 지목\n')
        L.append('\n| 제목 | 링크 |\n|---|---|\n')
        for t, u in EXTRA:
            L.append('| %s | %s |\n' % (t, u))

    L.append('\n## 미처리 최신 %d편 (재생목록 순서)\n' % len(todo))
    L.append('\n| # | 제목 | 길이 | 링크 |\n|---|---|---|---|\n')
    for n, vid, t, dur in todo:
        L.append('| %d | %s | %s | https://youtu.be/%s |\n' % (n, t, dur, vid))

    L.append('\n## 처리 완료\n')
    L.append('\n| 처리일 | 영상 | 결과물 |\n|---|---|---|\n')
    for vid, (day, path) in sorted(DONE.items(), key=lambda kv: kv[1][0], reverse=True):
        L.append('| %s | https://youtu.be/%s | `%s` |\n' % (day, vid, path))

    L.append('\n<sub>스냅샷 갱신일 %s · 재생목록 제목은 YouTube가 주는 표기라 영어로 번역돼 오는 편이 섞여 있습니다.</sub>\n' % today)

    with io.open(MD, 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(L))

    print('OK: 재생목록 %d편 / 완료 %d / 미처리 %d -> %s, %s'
          % (len(rows), len(DONE), len(rows) - sum(1 for r in rows if r[1] in DONE), TSV, MD))


if __name__ == '__main__':
    main()
