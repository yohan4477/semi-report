# -*- coding: utf-8 -*-
"""AgentX 메모리 층의 도해 셋. 색은 회색만(확정 규칙 S2).

① 입력 토큰 출처 기둥 — 동시성마다 GPU 캐시·DRAM·새로 계산 세 칸
② 모델별 세션당 HBM — 가로 순위 막대, 범위 선
③ 내려놓기 넷의 처리량 — 나란한 세로 막대

값은 전부 _agentx_mem_tbl 이 check_agentx_memory 와 같은 함수로 낸 것이다.
좌표는 값에서 낸다 — 손으로 안 찍는다.
"""
import math

import _biz_fig as bf
import _agentx_mem_tbl as T

_svg, _lt = bf._svg, bf._lt
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'
NUM = '①②③④⑤⑥⑦⑧⑨'
SHADE = [(INK3, '.35'), (INK2, '.75'), (INK, '1')]      # GPU 캐시 · DRAM · 새로 계산


def _t(cx, y, s, cls='t-sm', anchor='middle'):
    return '<text x="%.1f" y="%.1f" text-anchor="%s" class="%s">%s</text>' % (cx, y, anchor, cls, s)


def _mark(x, y, n):
    return ('<circle cx="%.1f" cy="%.1f" r="10" fill="var(--paper)"/>%s'
            % (x, y, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    return ''.join(_lt(20, y + i * 21, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


def _swatch(x, y, k, label):
    fill, op = SHADE[k]
    return ('<rect x="%d" y="%d" width="14" height="14" fill="%s" fill-opacity="%s"/>' % (x, y, fill, op)
            + _lt(x + 20, y + 12, label, 't-sm', False))


# ── ① 입력 토큰 출처 ────────────────────────────────────────────────────
_CX0, _CW, _CY0, _CH = 70, 520, 56, 200


def _tiers():
    data = T.tier_sweep()
    n = len(data)
    slot = _CW / n
    bw = slot * 0.56
    out = ['<path d="M%d %d V%d H%d" stroke="var(--line)" stroke-width="1.2" fill="none"/>'
           % (_CX0, _CY0, _CY0 + _CH, _CX0 + _CW)]
    out += [_t(_CX0 - 8, _CY0 + _CH - _CH * v / 100 + 4, '%d%%' % v, 't-sm', 'end') for v in (0, 50, 100)]
    cliff_x = None
    for i, (r, s) in enumerate(data):
        tot = sum(s)
        x = _CX0 + slot * i + (slot - bw) / 2
        y = _CY0 + _CH
        for k in range(3):
            h = _CH * s[k] / tot
            fill, op = SHADE[k]
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%s"/>'
                       % (x, y - h, bw, h, fill, op))
            y -= h
        out.append(_t(x + bw / 2, _CY0 + _CH + 16, '%d' % r['conc']))
        if cliff_x is None and (r['gpu_usage'] or 0) >= 0.95:
            cliff_x = x - (slot - bw) / 2
    out.append('<path d="M%.1f %d V%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 4"/>'
               % (cliff_x, _CY0 - 6, _CY0 + _CH, INK3))
    out.append(_mark(cliff_x, _CY0 - 16, 1))
    return ''.join(out)


FIG_TIER = _svg(W, 390, '동시성을 올리면 GPU 캐시가 비고 DRAM 이 그 자리를 채운다', ''.join(
    [_lt(20, 26, '입력 토큰을 출처 셋으로 나눈 비율 · 가로 동시 세션 수 · DeepSeek V4 Pro · B200 · SGLang'),
     _tiers(),
     _t(_CX0 + _CW / 2, _CY0 + _CH + 36, '동시 세션 수'),
     _swatch(20, _CY0 + _CH + 52, 0, 'GPU 캐시에서'), _swatch(170, _CY0 + _CH + 52, 1, 'DRAM 에서'),
     _swatch(300, _CY0 + _CH + 52, 2, '새로 계산'),
     _legend(_CY0 + _CH + 92, ['GPU KV 사용률이 0.95 를 처음 넘은 동시성'])]
))


# ── ② 모델별 세션당 HBM (로그 눈금) ─────────────────────────────────────
_RX0, _RW = 210, 360
_LO, _HI = 1.0, 200.0


def _lx(v):
    return _RX0 + _RW * (math.log10(v) - math.log10(_LO)) / (math.log10(_HI) - math.log10(_LO))


def _sessions():
    rows = sorted(T.sessions(), key=lambda x: -x[1])
    out = ['<path d="M%d %d H%d" stroke="var(--line)" stroke-width="1.2"/>' % (_RX0, 60 + len(rows) * 40, _RX0 + _RW)]
    out += [_t(_lx(v), 60 + len(rows) * 40 + 16, '%g' % v) for v in (1, 10, 100)]
    for i, (m, med, lo, hi, n) in enumerate(rows):
        y = 56 + i * 40
        on = m == 'dsv4'
        out.append(_lt(20, y + 17, '%d' % (i + 1), 't-sm', on))
        out.append(_lt(38, y + 17, T.NAME[m], 't-sm', on))
        out.append('<rect x="%d" y="%d" width="%.1f" height="20" rx="3" fill="%s"/>'
                   % (_RX0, y + 2, _lx(med) - _RX0, INK if on else INK3))
        if hi > lo:
            out.append('<path d="M%.1f %d H%.1f" stroke="%s" stroke-width="1.4"/>' % (_lx(lo), y + 12, _lx(hi), INK))
        out.append(_lt(int(max(_lx(med), _lx(hi))) + 8, y + 17, '%.1f' % med, 't-sm', on))
    return ''.join(out)


FIG_SESS = _svg(W, 330, '세션 하나가 쓰는 HBM 은 모델에 따라 열 배 넘게 갈린다', ''.join(
    [_lt(20, 28, '세션당 HBM(GB) 중앙값 · 가로 로그 눈금 · 선은 설정 사이 범위'), _sessions()]
))


# ── ③ 내려놓기 넷 ──────────────────────────────────────────────────────
_BX0, _BW, _BY0, _BH = 90, 480, 56, 200
_ORDER = ['none', 'dram', 'nvme', 'dram+nvme']


def _ssd():
    by = T.ssd_rows()
    vals = [by[(o, 8)]['tput_per_gpu'] for o in _ORDER]
    top = 1200.0
    slot = _BW / len(vals)
    bw = slot * 0.5
    out = ['<path d="M%d %d V%d H%d" stroke="var(--line)" stroke-width="1.2" fill="none"/>'
           % (_BX0, _BY0, _BY0 + _BH, _BX0 + _BW)]
    out += [_t(_BX0 - 8, _BY0 + _BH - _BH * v / top + 4, '%s' % format(v, ','), 't-sm', 'end')
            for v in (0, 400, 800, 1200)]
    for i, (o, v) in enumerate(zip(_ORDER, vals)):
        x = _BX0 + slot * i + (slot - bw) / 2
        h = _BH * v / top
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                   % (x, _BY0 + _BH - h, bw, h, INK if o == 'nvme' else INK3))
        out.append(_t(x + bw / 2, _BY0 + _BH - h - 8, format(int(round(v)), ','), 't-sm'))
        out.append(_t(x + bw / 2, _BY0 + _BH + 18, T.OFF[o], 't-lab'))
    return ''.join(out)


FIG_SSD = _svg(W, 300, 'HBM 이 모자란 H100 에서 SSD 층이 DRAM 층만큼 처리량을 되살린다', ''.join(
    [_lt(20, 26, 'GPU 한 장 처리량(tok/s) · MiniMax M3 · H100 8장 · vLLM · 동시 세션 8'), _ssd()]
))
