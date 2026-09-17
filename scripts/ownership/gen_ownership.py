"""지분 대시보드 — data/ownership/hanwha.json 을 읽어 대시보드/지분 대시보드.html 한 장으로 굽는다.

HTML 은 생성물이다. 화면은 app.css·app.js, 판단은 build.py, 검사는 check_own.py.
check_own 이 FAIL 이면 굽지 않는다.

  python scripts/ownership/collect.py      # DART 정기보고서(뒤값)
  python scripts/ownership/collect_ftc.py  # 공정위 대규모기업집단현황공시(정본)
  python scripts/ownership/build.py
  python scripts/ownership/gen_ownership.py
"""
import html, json, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import check_own  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / '대시보드' / '지분 대시보드.html'


def main():
    d = json.loads((ROOT / 'data' / 'ownership' / 'hanwha.json').read_text(encoding='utf-8'))
    fails = check_own.validate(d)
    if fails:
        sys.exit('check_own FAIL — 굽지 않는다:\n' + '\n'.join(fails))
    d['start'] = '한화'
    corps = [n for n in d['nodes'] if n['kind'] == 'corp' and not n.get('foreign')]
    listed = [n for n in corps if n.get('stock')]
    src = d['source']
    e = html.escape

    moved = []
    for ed in d['edges']:
        lt = ed.get('later')
        if lt and lt['moved']:
            moved.append((ed['from'], ed['to'], ed['pct'], lt))
    moved_rows = ''.join(
        f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{p:g}%</td><td>{lt['pct']:g}%</td>"
        f"<td><a href=\"{e(lt['url'])}\" target=\"_blank\" rel=\"noopener\">{e(lt['asof'])}</a></td></tr>"
        for a, b, p, lt in moved)
    # 일가 직접 지분 — 사람 × 회사. 판의 나무는 최대주주 선 하나만 그려서 일가가 여러 곳을 나눠 쥔 모양이 안 보인다
    fam = d['family']
    order = {'동일인': 0}
    fam = sorted(fam, key=lambda x: (order.get(next(n['rel'] for n in d['nodes'] if n['id'] == x), 1), x))
    fcos = {}
    for ed in d['edges']:
        if ed['from'] in fam:
            fcos.setdefault(ed['to'], 0)
            fcos[ed['to']] += ed['pct']
    cols = sorted(fcos, key=lambda c: -fcos[c])
    cell = {(ed['from'], ed['to']): ed['pct'] for ed in d['edges'] if ed['from'] in fam}
    rel = {n['id']: ('동일인' if n.get('rel') == '동일인' else '친족') for n in d['nodes'] if n['kind'] == 'person'}
    fam_table = ('<div class="tw"><table><tr><th></th>' + ''.join(f'<th>{e(c)}</th>' for c in cols) + '</tr>' +
                 ''.join(f'<tr><th>{e(f)} <span class="r">{rel[f]}</span></th>' +
                         ''.join(f'<td>{cell[(f, c)]:g}%</td>' if (f, c) in cell else '<td class="z">·</td>' for c in cols) +
                         '</tr>' for f in fam) +
                 '<tr class="sum"><th>일가 합</th>' + ''.join(f'<td>{round(fcos[c], 2):g}%</td>' for c in cols) +
                 '</tr></table></div>')
    names = ''.join(f'<option value="{e(n["name"])}">' for n in d['nodes'])

    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>지분 대시보드 · {e(d['group'])}</title>
<style>{(HERE / 'app.css').read_text(encoding='utf-8')}</style></head>
<body><div class="wrap">
<h1>{e(d['group'])} 지분 사슬</h1>
<p class="meta">국내 계열사 <b>{len(corps)}곳</b> · 상장 <b>{len(listed)}곳</b> · 동일인측 지분 선 <b>{len(d['edges'])}개</b><br>
출처 <a href="{e(src['url'])}" target="_blank" rel="noopener">{e(src['label'])}</a>, {e(src['basis'])}, {e(src['rcept_dt'][:4])}-{e(src['rcept_dt'][4:6])}-{e(src['rcept_dt'][6:])} 접수</p>
<section class="fam">
<h2>일가가 직접 가진 지분 (보통주)</h2>
{fam_table}
</section>
<div class="bar">
<button id="b-listed" type="button">상장사까지 펼치기</button>
<button id="b-all" type="button">모두 펼치기</button>
<input id="q" list="names" placeholder="회사·사람 이름" aria-label="이름으로 찾기">
<datalist id="names">{names}</datalist>
</div>
<div class="legend">
<span><svg width="34" height="8"><path d="M0 4H34" stroke="#9aa1ab" stroke-width="2.6"/></svg>최대 동일인측 주주 50% 이상</span>
<span><svg width="34" height="8"><path d="M0 4H34" stroke="#9aa1ab" stroke-width="1.8"/></svg>30~50%</span>
<span><svg width="34" height="8"><path d="M0 4H34" stroke="#9aa1ab" stroke-width="1.1"/></svg>30% 미만</span>
<span><svg width="34" height="8"><path d="M0 4H34" stroke="#9aa1ab" stroke-width="1.1" stroke-dasharray="4 3"/></svg>상자를 고르면 그 밖의 동일인측 지분(1% 이상)</span>
<span>숫자 칸을 누르면 아래 계열사가 펼쳐진다</span>
</div>
<div class="main">
<div class="board" id="board"></div>
<aside class="panel" id="panel" aria-live="polite"></aside>
</div>
<section class="notes">
<h2>지정일 뒤 정기보고서에서 달라진 지분</h2>
{f'<div class="tw"><table><tr><th>주주</th><th>회사</th><th>지정일</th><th>정기보고서</th><th>기준일</th></tr>{moved_rows}</table></div>' if moved else '<p>없음</p>'}
<p>순환출자 고리 {len(d['cycles'])}개. 지분율은 보통주 기준이고, 우선주를 합친 값은 회사 칸에 따로 적었다.</p>
</section>
</div>
<script>window.OWN={json.dumps(d, ensure_ascii=False, separators=(',', ':'))};</script>
<script>{(HERE / 'app.js').read_text(encoding='utf-8')}</script>
</body></html>
"""
    OUT.write_text(page, encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)} {len(page) // 1024}KB')


if __name__ == '__main__':
    main()
