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
TRACKS = os.path.join(HERE, 'tracks')
SYNTH = os.path.join(HERE, 'synth')
# 판단까지는 아닌 주제 브리핑. 통합 인사이트에서 인사이트보다 앞에 선다
BRIEFS = os.path.join(HERE, 'briefs')
THESES = os.path.join(HERE, 'theses')
WORLD = os.path.join(HERE, 'world_path.txt')
# 돈 고리 여덟 편. 교차 인사이트(어긋남 하나)와 절 구성이 달라 디렉터리를 가른다
LOOP = os.path.join(HERE, 'loop')
