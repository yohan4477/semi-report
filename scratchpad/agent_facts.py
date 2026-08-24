# -*- coding: utf-8 -*-
"""보고서에 쓰는 수를 파일에서 직접 센다.

손으로 적어 두면 스킬을 하나 더 깔았을 때 본문만 옛날 수로 남는다. 세는 대상은
이 컴퓨터의 실제 설정이다 — 저장소의 스킬 폴더, 사용자 홈의 플러그인 캐시,
settings.json. 못 찾으면 값을 지어내지 않고 None 을 돌려준다.
"""
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser('~')


def _read(p):
    try:
        return io.open(p, encoding='utf-8').read()
    except Exception:
        return ''


def skills():
    """저장소에서 걸리는 스킬마다 (이름, 본문 글자수, description 글자수)."""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, '.claude', 'skills', '*', 'SKILL.md'))):
        t = _read(p)
        if not t.startswith('---'):
            continue
        fm = t.split('---')[1]
        m = re.search(r'description:\s*(.*?)(?=\n\w+:|\Z)', fm, re.S)
        out.append((os.path.basename(os.path.dirname(p)), len(t),
                    len(m.group(1).strip()) if m else 0))
    return out


SKILLS = skills()
N_SKILL = len(SKILLS)
CH_BODY = sum(s[1] for s in SKILLS)
CH_DESC = sum(s[2] for s in SKILLS)
PCT_DESC = 100.0 * CH_DESC / CH_BODY if CH_BODY else 0
CH_ONE = CH_BODY // N_SKILL if N_SKILL else 0


def _plugin_root(market, name):
    base = os.path.join(HOME, '.claude', 'plugins', 'cache', market, name)
    if not os.path.isdir(base):
        return None
    kids = [os.path.join(base, d) for d in sorted(os.listdir(base))]
    kids = [k for k in kids if os.path.isdir(k)]
    return kids[-1] if kids else None


def plugin(market, name):
    """플러그인 상자 하나에 무엇이 몇 개 들었나. 없으면 None."""
    root = _plugin_root(market, name)
    if not root:
        return None
    mf = {}
    try:
        mf = json.loads(_read(os.path.join(root, '.claude-plugin', 'plugin.json')) or '{}')
    except ValueError:
        pass
    n = {}
    # 스킬은 폴더 하나가 하나, 명령·서브에이전트는 파일 하나가 하나다. 같은 명령을
    # .md 와 .toml 로 두 벌 두는 플러그인이 있어 .md 만 센다 — 파일 수를 그대로
    # 세면 명령이 두 배로 잡힌다.
    n['skills'] = len([d for d in os.listdir(os.path.join(root, 'skills'))
                       if os.path.isdir(os.path.join(root, 'skills', d))])         if os.path.isdir(os.path.join(root, 'skills')) else 0
    for d in ('commands', 'agents'):
        p = os.path.join(root, d)
        n[d] = len([f for f in os.listdir(p) if f.endswith('.md')]) if os.path.isdir(p) else 0
    # 훅은 두 자리에 적힐 수 있다 — 매니페스트 안이거나 hooks/ 폴더거나
    ev = list((mf.get('hooks') or {}).keys())
    hd = os.path.join(root, 'hooks')
    n['hooks'] = len(ev) or (len(os.listdir(hd)) if os.path.isdir(hd) else 0)
    n['hook_events'] = ev
    n['name'] = mf.get('name', name)
    return n


CAVEMAN = plugin('caveman', 'caveman')
SUPERPOWERS = plugin('claude-plugins-official', 'superpowers')


def _settings(p):
    try:
        return json.loads(_read(p) or '{}')
    except ValueError:
        return {}


_US = _settings(os.path.join(HOME, '.claude', 'settings.json'))
ENABLED = sorted((_US.get('enabledPlugins') or {}).keys())
HOOK_EVENTS = sorted((_US.get('hooks') or {}).keys())
_MCP = _settings(os.path.join(HOME, '.claude.json')).get('mcpServers') or {}
MCP = sorted(_MCP.keys())

_ALLOW = 0
for _p in ('.claude/settings.json', '.claude/settings.local.json'):
    _ALLOW += len((_settings(os.path.join(ROOT, _p)).get('permissions') or {}).get('allow') or [])
N_ALLOW = _ALLOW

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print('스킬 %d개 / 본문 %s자 / 설명 %s자 (%.1f%%)'
          % (N_SKILL, '{:,}'.format(CH_BODY), '{:,}'.format(CH_DESC), PCT_DESC))
    print('플러그인', ENABLED)
    print('caveman', CAVEMAN)
    print('superpowers', SUPERPOWERS)
    print('훅 이벤트', HOOK_EVENTS, '| MCP', MCP, '| 허용규칙', N_ALLOW)
