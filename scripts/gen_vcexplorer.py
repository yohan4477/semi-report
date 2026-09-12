# -*- coding: utf-8 -*-
"""밸류체인 탐색기 — data/valuechain 을 읽어 한 장짜리 HTML 로 굽는다.

원본은 JSON 이다. HTML 은 생성물이니 손으로 고치지 않는다.
  entities.json / sources.json / methods.json        전역
  chains/<사슬>/relationships.json                    지속적인 관계. 숫자를 박지 않는다
  chains/<사슬>/observations.json                     시점별 값. 분모·기준일·근거등급이 붙는다
  chains/<사슬>/claims.json · hypotheses.json
  chains/<사슬>/projects.json                         프로젝트 맥락. 식구를 두르는 테두리, 상자 아님
  chains/<사슬>/bom/*.json · financials/*.json

화면(CSS·앱)은 scripts/vcexplorer/app.css·app.js 다. 이 파일은 데이터를 읽어 굽기만 한다.

어느 회사도 코드에 박지 않는다. 실리는 사슬은 chains/ 아래 chain.json 이 있는 디렉터리
전부이고(check_vc.shipped_chains), 시작 회사는 관계가 가장 많은 엔티티에서 고른다.
굽기 전에 check_vc.validate() 를 돌려 FAIL 이면 굽지 않는다.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_vc  # noqa: E402  실리는 사슬 목록과 발행 전 검사를 같이 쓴다


def ship_list():
    u"""화면에 싣는 사슬 — chains/ 아래 chain.json 이 있는 디렉터리 전부.
    회사 이름을 코드에 박지 않는다. 안 실을 사슬은 chain.json 을 안 둔다."""
    return check_vc.shipped_chains()


# 라이브러리는 저장소 안 scripts/vcexplorer/vendor/ 의 파일을 HTML 에 그대로 넣는다.
# CDN 을 부르면 오프라인·CDN 장애 때 빈 화면이다. 판본은 vendor/README.md
VENDOR_JS = ['react_18.3.1_umd_react.production.min.js',
             'react-dom_18.3.1_umd_react-dom.production.min.js',
             'reactflow_11.11.4_dist_umd_index.js']
VENDOR_CSS = 'reactflow_11.11.4_dist_style.css'

TEMPLATE = u'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>밸류체인 탐색기</title>
<style>__RFCSS__</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&display=swap">
<style>__CSS__</style>
</head><body>
<div id="root"></div>
__SCRIPTS__
<script>window.__VC__ = __DATA__;</script>
<script>__APP__</script>
</body></html>
'''

HERE = os.path.dirname(os.path.abspath(__file__))


def _read(name):
    with io.open(os.path.join(HERE, 'vcexplorer', name), encoding='utf-8') as f:
        return f.read()


# 화면의 CSS 와 앱은 scripts/vcexplorer/ 의 실제 파일이다. 파이썬 문자열에 박아 두면
# 편집기가 JS 로 읽지 못하고 이스케이프가 두 겹이 된다
CSS = _read('app.css')

# 앱은 네 장이다 — 데이터 색인 / 자리 잡기 / 그래프 세우기 / 화면. 번호 순으로 이어 붙이고
# 한 함수 안에 감싼다. 장마다 첫 두 줄은 이름과 한 줄 설명이다
APP_PARTS = ['10_data.js', '20_layout.js', '30_graph.js', '40_ui.js']


def _app():
    lines = []
    for name in APP_PARTS:
        rows = _read(name).split('\n')
        if rows and rows[-1] == '':
            rows.pop()
        lines.extend(rows[2:])          # 첫 두 줄은 장 이름과 설명
    return '\n(function(){\n' + '\n'.join(lines) + '\n})();\n'


APP = _app()


def load(*parts):
    p = os.path.join(DATA, *parts)
    if not os.path.exists(p):
        return None
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def by_id(rows):
    return dict((r['id'], r) for r in (rows or []))


def read_dir(base, sub):
    d = os.path.join(base, sub)
    out = {}
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.json'):
                with io.open(os.path.join(d, fn), encoding='utf-8') as f:
                    out[fn[:-5]] = json.load(f)
    return out


def build():
    db = {'entities': by_id(load('entities.json')),
          'sources': by_id(load('sources.json')),
          'methods': by_id(load('methods.json')),
          # SEC 에 등록된 업종. scripts/fetch_sec_sector.py 가 받아 둔다
          'sec': load('sec_sector.json') or {},
          'chains': {}}
    cdir = os.path.join(DATA, 'chains')
    for ck in ship_list():
        base = os.path.join(cdir, ck)
        db['chains'][ck] = {
            'projects': load('chains', ck, 'projects.json') or [],
            'relationships': load('chains', ck, 'relationships.json') or [],
            'observations': load('chains', ck, 'observations.json') or [],
            'claims': load('chains', ck, 'claims.json') or [],
            'hypotheses': load('chains', ck, 'hypotheses.json') or [],
            'meta': load('chains', ck, 'chain.json') or {},
            'classifications': load('chains', ck, 'classifications.json')
                               or {'supply_sources': [], 'revenue_types': []},
            'bom': read_dir(base, 'bom'),
            'financials': read_dir(base, 'financials'),
        }
    # 실은 사슬이 쓰는 엔티티만 내보낸다
    used = set()
    for c in db['chains'].values():
        for r in c['relationships']:
            used.add(r['source_entity'])
            used.add(r['target_entity'])
        for x in c['hypotheses']:
            used.add(x['anon_company_id'])
            used.add(x['candidate_company_id'])
    db['entities'] = dict((k, v) for k, v in db['entities'].items() if k in used)

    payload = json.dumps(db, ensure_ascii=False, separators=(',', ':'))
    vend = os.path.join(HERE, 'vcexplorer', 'vendor')

    def vf(name):
        with io.open(os.path.join(vend, name), encoding='utf-8') as f:
            return f.read()
    scripts = '\n'.join('<script>%s</script>' % vf(n) for n in VENDOR_JS)
    html = (TEMPLATE
            .replace('__RFCSS__', vf(VENDOR_CSS))
            .replace('__CSS__', CSS)
            .replace('__SCRIPTS__', scripts)
            .replace('__DATA__', payload)
            .replace('__APP__', APP))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    return OUT, db


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    # 발행을 막는 검사 — 데이터 규약이 어긋나면 굽지 않는다. 화면이 잘못 그리지 않게
    # 하려면 검증된 상자·선만 넘긴다(프레임워크 §1)
    fails, debt, st = check_vc.validate()
    if fails:
        for f in fails[:40]:
            print(f)
        print(u'검사 FAIL %d — 굽지 않는다. data 와 생성기를 같이 고친다' % len(fails))
        sys.exit(1)
    p, db = build()
    n = sum(len(c['relationships']) for c in db['chains'].values())
    print('%s\n사슬 %d · 엔티티 %d · 관계 %d · 출처 %d'
          % (p, len(db['chains']), len(db['entities']), n, len(db['sources'])))
