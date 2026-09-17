"""DART OpenAPI 얇은 호출기 — 키는 저장소 .env 의 DART_API_KEY, 응답은 data/ownership/raw/ 에 캐시."""
import io, json, os, sys, time, urllib.parse, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'data' / 'ownership' / 'raw'
BASE = 'https://opendart.fss.or.kr/api/'


def _key():
    for line in (ROOT / '.env').read_text(encoding='utf-8').splitlines():
        if line.startswith('DART_API_KEY='):
            return line.split('=', 1)[1].strip()
    sys.exit('DART_API_KEY 없음 (.env)')


def get(endpoint, **params):
    """json 엔드포인트 호출. 같은 인자면 캐시를 돌려준다."""
    tag = endpoint + '_' + '_'.join(f'{k}-{v}' for k, v in sorted(params.items()))
    cache = RAW / (tag + '.json')
    if cache.exists():
        return json.loads(cache.read_text(encoding='utf-8'))
    q = urllib.parse.urlencode({'crtfc_key': _key(), **params})
    with urllib.request.urlopen(BASE + endpoint + '.json?' + q, timeout=30) as r:
        data = json.load(r)
    time.sleep(0.2)
    if data.get('status') in ('000', '013'):  # 013 = 조회 데이터 없음, 이것도 캐시
        cache.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    return data


def corp_codes():
    """고유번호 전체 목록 [(corp_code, corp_name, stock_code)]."""
    cache = RAW / 'corpCode.json'
    if not cache.exists():
        with urllib.request.urlopen(BASE + 'corpCode.xml?crtfc_key=' + _key(), timeout=60) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        import xml.etree.ElementTree as ET
        root = ET.fromstring(z.read(z.namelist()[0]))
        rows = [(e.findtext('corp_code'), e.findtext('corp_name'), (e.findtext('stock_code') or '').strip())
                for e in root.iter('list')]
        cache.write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
    return json.loads(cache.read_text(encoding='utf-8'))


if __name__ == '__main__':
    rows = corp_codes()
    hits = [r for r in rows if '한화' in r[1]]
    print(len(rows), 'corps;', len(hits), 'with 한화')
    for r in hits:
        print(r)


def document(rcept_no):
    """공시 원문(zip 안 xml들)을 raw/doc_<접수번호>/ 에 풀고 파일 경로 목록을 돌려준다."""
    d = RAW / f'doc_{rcept_no}'
    if not d.exists():
        with urllib.request.urlopen(BASE + f'document.xml?crtfc_key={_key()}&rcept_no={rcept_no}', timeout=60) as r:
            z = zipfile.ZipFile(io.BytesIO(r.read()))
        d.mkdir(parents=True)
        z.extractall(d)
        time.sleep(0.2)
    return sorted(d.iterdir())
