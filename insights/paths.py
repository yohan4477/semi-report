# 경로 상수만 둔다. 예전엔 check_atoms.py가 이 역할을 겸해서, 그걸 지우면
# 생성기 여섯 개가 같이 죽는 구조였다. 상수는 상수 파일에 둔다.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MAN = os.path.join(HERE, 'manifest.json')
NOTES = os.path.join(HERE, 'notes')
CITES = os.path.join(HERE, 'cites.json')
TRACKS = os.path.join(HERE, 'tracks')
SYNTH = os.path.join(HERE, 'synth')
# 판단까지는 아닌 주제 정리본. 통합 인사이트에 인사이트와 나란히 실린다
DIGESTS = os.path.join(HERE, 'digests')
THESES = os.path.join(HERE, 'theses')
WORLD = os.path.join(HERE, 'world_path.txt')
