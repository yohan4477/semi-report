# 경로 상수만 둔다. 예전엔 check_atoms.py가 이 역할을 겸해서, 그걸 지우면
# 생성기 여섯 개가 같이 죽는 구조였다. 상수는 상수 파일에 둔다.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAN = os.path.join(HERE, 'manifest.json')
NOTES = os.path.join(HERE, 'notes')
CITES = os.path.join(HERE, 'cites.json')
# 개체 사전은 사람이 검토해 커밋하고, 색인은 그것으로 만든 생성물이다
ENTITIES = os.path.join(HERE, 'entities.json')
INDEX = os.path.join(HERE, 'index.json')
# 가리키는 때는 색인에서 파생된 생성물이다 — 색인이 가리키는 줄만 판정한다
TIMES = os.path.join(HERE, 'times.json')
TRACKS = os.path.join(HERE, 'tracks')
SYNTH = os.path.join(HERE, 'synth')
# 판단까지는 아닌 주제 브리핑. 통합 인사이트에서 인사이트보다 앞에 선다
BRIEFS = os.path.join(HERE, 'briefs')
THESES = os.path.join(HERE, 'theses')
WORLD = os.path.join(HERE, 'world_path.txt')
# 돈 고리 여덟 편. 교차 인사이트(어긋남 하나)와 절 구성이 달라 디렉터리를 가른다
LOOP = os.path.join(HERE, 'loop')
# 쟁점 — 같은 물음에 화자들이 갈린 자리. 화자 말은 인용이고 진행자 말은 판단이라
# 절 구성이 교차 인사이트와 다르다
# 각도 — 원문 한 편을 여러 글과 합칠 수 있는 꼴로 가른 것. 대상·때가 붙는 열쇠다
ANGLES = os.path.join(HERE, 'angles')

DEBATE = os.path.join(HERE, 'debate')

# 클리핑 원문은 저장소 밖에 있다(2026-10-01). 노트·색인·인용이 쓰는 주소는 옛 꼴
# `input/clippings/...` 그대로 두는 열쇠이고, 디스크를 열 때만 아래로 바꾼다.
#   input/clippings/mer/*       -> CLIP_ROOT/mer/*
#   input/clippings/*           -> CLIP_ROOT/semianalysis/*
#   input/linkedin/한주성/*     -> CLIP_ROOT/linkedin/한주성/*
from pathlib import Path

CLIP_ROOT = Path(r"C:\Users\y\clippings")
CLIP_SEMI = CLIP_ROOT / "semianalysis"
CLIP_MER = CLIP_ROOT / "mer"
CLIP_LINKEDIN = CLIP_ROOT / "linkedin"

_VIRTUAL = (
    ('input/clippings/mer', CLIP_MER),
    ('input/clippings', CLIP_SEMI),
    ('input/linkedin', CLIP_LINKEDIN),
)


def _is_repo(root):
    return os.path.normcase(os.path.abspath(str(root))) == os.path.normcase(ROOT)


def locate(root, rel):
    """열쇠 주소(rel, 슬래시)를 디스크 경로로. 저장소 루트가 아닌 root(테스트의 tmp)는 그대로 붙인다."""
    r = rel.replace(os.sep, '/')
    if _is_repo(root):
        for pre, real in _VIRTUAL:
            if r == pre or r.startswith(pre + '/'):
                return os.path.join(str(real), *r[len(pre):].strip('/').split('/')) if r != pre else str(real)
    return os.path.join(str(root), r.replace('/', os.sep))


def virtual(root, path):
    """locate 의 거꾸로. 디스크 경로 -> 열쇠 주소(슬래시)."""
    p = os.path.abspath(str(path))
    if _is_repo(root):
        for pre, real in _VIRTUAL:
            base = os.path.normcase(os.path.abspath(str(real)))
            if os.path.normcase(p).startswith(base + os.sep):
                return pre + '/' + p[len(base) + 1:].replace(os.sep, '/')
    return os.path.relpath(p, str(root)).replace(os.sep, '/')
