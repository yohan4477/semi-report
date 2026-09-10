"""하향 총액과 상향 단가를 잇는 모델을 대조한다.

값의 출처가 둘이라 표에서 갈라 적는다. 「프레임」은 다른 대화에서 받은 하향 틀의
값이고(`insights/frames/2026-09-10-dc-capex-topdown.md`), 나머지는 이 층 앞 네 글이
원문에서 뽑은 값이다. 프레임 값은 우리 코퍼스 대조를 안 거쳤다.

    PYTHONIOENCODING=utf-8 python insights/models/check_bridge.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                   # noqa: E402
from bridge_capex import (all_in_per_mw, blended_asp, chips_from_capex,  # noqa: E402
                          cumulative, gw_series,
                          gpu_capex, gpus_per_mw, gw_from_chips,
                          hbm_cost_per_mw, hbm_per_mw, implied_gw,
                          it_capex_per_mw, life_change, server_share,
                          total_range)

CAPEX = load_raw('capex')
TBL = load_raw('tables')
F = table(CAPEX, 'frame-capex')
S = table(CAPEX, 'frame-sheet')
SC = table(CAPEX, 'frame-scn')
LY = table(CAPEX, 'ground-layers')
G = table(CAPEX, 'ground-assump')
B = table(CAPEX, 'trinity-backstop')
X = table(CAPEX, 'spacex-econ')
AMD = table(TBL, 'amd-capex')

GPUS_PER_SERVER = 8


def f(k):
    return F['rows'][k][1]


def g(k):
    return G['rows'][k][1]


def sh(k):
    return S['rows'][k][1]


def _v_x(k):
    return X['rows'][k][1]


def sku(name, row):
    i = AMD['columns'].index(name)
    return AMD['rows'][row][i]


def main():
    fails = 0

    print('── 프레임이 낸 합산을 다시 낸다 ' + '─' * 34)
    lo, hi = total_range([(f('msft'), f('msft')),
                          (f('googl_lo'), f('googl_hi')),
                          (f('amzn'), f('amzn')),
                          (f('meta_lo'), f('meta_hi'))])
    ok = lo <= f('total_stated') <= hi
    fails += not ok
    print('  마이크로소프트 %g · 구글 %g~%g · 아마존 %g · 메타 %g~%g (십억 달러)'
          % (f('msft'), f('googl_lo'), f('googl_hi'), f('amzn'),
             f('meta_lo'), f('meta_hi')))
    print('  더하면 %g~%g 이고, 프레임이 적은 합산은 %g 다%s'
          % (lo, hi, f('total_stated'), '' if ok else '  FAIL'))
    print('  전부 프레임 값이다 — 회사 공시와 실적 콜에서 왔고 우리 원문에는 없다.')

    print()
    print('── 우리 원문이 그 틀의 빈칸에 넣는 값 ' + '─' * 28)
    kw_per_gpu = round(1000.0 / gpus_per_mw(2.10), 2)
    per_gpu = gpu_capex(sku('B200', 'server_cost'),
                        sku('B200', 'other_cluster_cost'), GPUS_PER_SERVER)
    it = it_capex_per_mw(2.10, per_gpu)
    print('  GPU 한 장이 끄는 전력 %.2fkW — GPU 금융 층이 우발채무에서 되짚은 값이다.'
          % kw_per_gpu)
    print('  메가와트당 GPU %s장. 원문에 없는 값이다.'
          % format(int(gpus_per_mw(2.10)), ','))
    print('  GPU 한 장의 선불 자본 $%s — 서버 값 $%s 에 망·저장·소프트웨어 $%s 를 더해'
          % (format(int(per_gpu), ','),
             format(sku('B200', 'server_cost'), ','),
             format(sku('B200', 'other_cluster_cost'), ',')))
    print('  여덟으로 나눈 값이다(추론 원가 모델의 B200 열).')
    print('  그러면 IT 자본지출이 메가와트당 $%.1f백만이다.' % it)

    print()
    print('── 시설·전력을 얹으면 메가와트당 얼마인가 ' + '─' * 24)
    print('%-16s %12s %14s %14s' % ('층', '시설·전력', 'IT', '합계'))
    rows = []
    for v in LY['rows'].values():
        name, flo, fhi = v[0], v[1], v[2]
        fhi = fhi if fhi is not None else flo
        rows.append((name, flo, fhi))
        print('%-16s %6.1f~%.1f M %10.1f M %8.1f~%.1f M'
              % (name, flo, fhi, it, all_in_per_mw(flo, it), all_in_per_mw(fhi, it)))
    span_lo = all_in_per_mw(min(r[1] for r in rows), it)
    span_hi = all_in_per_mw(max(r[2] for r in rows), it)
    print('  전체 폭 $%.1f~%.1f백만/MW 다. 회수 층이 쓴 전부 포함 단가는 $%g백만이다.'
          % (span_lo, span_hi, X['rows']['capex_per_gw'][1]))

    print()
    print('── 그러면 7,300억 달러는 몇 기가와트인가 ' + '─' * 24)
    print('%-28s %14s %12s' % ('무엇으로 나누나', 'MW당 자본', '신규 용량'))
    for label, per_mw in (('우리 단가 하한', span_lo),
                          ('우리 단가 상한', span_hi),
                          ('회수 층의 전부 포함 단가', X['rows']['capex_per_gw'][1])):
        print('%-28s %10.1f M %10.1f GW'
              % (label, per_mw, implied_gw(f('total_stated'), per_mw)))
    print('  프레임의 총액은 회사가 밝힌 돈이고, 나누는 단가는 우리 원문에서 왔다.')
    print('  둘을 곱해 만든 값이 아니라 남의 총액을 우리 자로 잰 것이다.')

    print()
    print('── 서버가 자본지출에서 차지하는 몫 ' + '─' * 30)
    for name, flo, fhi in rows:
        print('  %-14s %.0f~%.0f%%'
              % (name, server_share(it, fhi), server_share(it, flo)))
    print('  프레임은 구글 2분기에 서버가 %g%%, 데이터센터와 네트워크가 %g%% 라고 적었다.'
          % (f('googl_server_share'), f('googl_dc_share')))
    print('  마이크로소프트는 분기 자본지출의 약 %g%% 가 단기자산이라고 했다.'
          % f('msft_short_share'))
    print('  우리 단가로 낸 몫이 그 폭 안에 든다 — 서로 다른 길로 온 값이 겹친다.')

    print()
    print('── 내용연수를 15년에서 25년으로 바꾸면 ' + '─' * 26)
    c = life_change(g('wacc'), f('msft_life_old'), f('msft_life_new'))
    print('  자본비용 %g%% 에서 자본회수계수가 %.4f 에서 %.4f 로 내린다.'
          % (g('wacc'), c['old'], c['new']))
    print('  연 자본비가 %.0f%% 줄어 보인다. 자산이 달라진 것이 아니라 미는 기간이 늘었다.'
          % c['drop_pct'])
    print('  우리 원문의 지상 데이터센터 수명 가정은 %g년이다 — 프레임이 옮겨 간 %g년이'
          % (g('life_dc'), f('msft_life_new')))
    print('  아니라 옮겨 오기 전 값과 같다.')

    print()
    print('── 선지출 50퍼센트가 서는 자리 ' + '─' * 34)
    print('  프레임은 시설·전력을 차년도 가동분의 %g%% 만큼 미리 쓴다고 놓았다.'
          % f('prepay_share'))
    print('  모듈러 층의 공기가 그 근거다 — 현장시공은 착공에서 준비까지 18~24개월,')
    print('  허가까지 30~35개월이고 모듈러로 12~18개월이 된다. 공기가 짧아지면 같은')
    print('  자본이 더 늦게 나가므로 이 %g퍼센트도 따라 내려간다.' % f('prepay_share'))
    print('  IT 갱신 %g년은 우리 원문의 IT 장비 수명 %g년과 같다.'
          % (f('it_refresh_years'), g('life_it')))

    print()
    print('── 엑셀이 낸 2026년 항목과 우리 단가 ' + '─' * 28)
    kwg = 2.10
    per_gpu2 = gpu_capex(sku('B200', 'server_cost'),
                         sku('B200', 'other_cluster_cost'), GPUS_PER_SERVER)
    it2 = it_capex_per_mw(kwg, per_gpu2)
    print('  엑셀은 합산 %g십억 달러를 서버·칩 %g 과 데이터센터·전력·네트워크 %g 로 나눴다.'
          % (sh('total_2026'), sh('server_2026'), sh('dc_2026')))
    got = sh('server_2026') / sh('total_2026') * 100
    print('  서버 몫이 %.1f%% 다. 우리 단가로 낸 몫은 %.0f~%.0f%% 였다.'
          % (got, server_share(it2, 20.0), server_share(it2, 10.0)))

    print()
    print('── 용량을 세는 길 넷 ' + '─' * 44)
    print('%-30s %14s %12s' % ('무엇을 무엇으로 나누나', '단가', '신규 용량'))
    dc_lo = sh('dc_2026') / 20.0
    dc_hi = sh('dc_2026') / 10.0
    print('%-30s %10s %10.1f GW' % ('데이터센터·전력을 시설 단가 상한으로',
                                    '$20백만/MW', dc_lo))
    print('%-30s %10s %10.1f GW' % ('같은 값을 시설 단가 하한으로',
                                    '$10백만/MW', dc_hi))
    srv_gw = sh('server_2026') / it2
    print('%-30s %10.1f M %10.1f GW' % ('서버·칩을 우리 IT 단가로', it2, srv_gw))
    asp = blended_asp(sh('accel_capex'), sh('accel_units'))
    chip_gw = gw_from_chips(sh('accel_units'), kwg)
    print('%-30s %10s %10.1f GW' % ('엑셀의 가속기 대수에 칩당 전력을',
                                    '%.1f kW' % kwg, chip_gw))
    print('  앞의 셋은 14~29기가와트에 모이는데 넷째만 %.1f기가와트다.' % chip_gw)

    print()
    print('── 왜 넷째만 벌어지나 ' + '─' * 42)
    print('  엑셀의 블렌드 칩 값은 %.1f천 달러다(%g십억 ÷ %g백만 개).'
          % (asp, sh('accel_capex'), sh('accel_units')))
    print('  우리 GPU 한 장의 선불 자본은 %.1f천 달러다 — %.1f 배 차이다.'
          % (per_gpu2 / 1000, per_gpu2 / (asp * 1000)))
    print('  엑셀이 블랙웰 %g천, TPU %g천, 트레이니엄 %g천으로 섞었기 때문이다.'
          % (sh('asp_blackwell'), sh('asp_tpu'), sh('asp_trainium')))
    print('  자체 칩이 섞이면 같은 돈으로 칩을 두 배 산다. 그런데 그 칩들의 전력은')
    print('  엔비디아 랙 기준 %.2fkW 로 함께 세어져서 용량이 두 배로 나온다.' % kwg)
    print('  우리 %.2fkW 는 GB300 계약에서 되짚은 값이라 자체 칩에 그대로 못 댄다.' % kwg)
    n = chips_from_capex(sh('server_2026'), per_gpu2)
    print('  거꾸로 우리 단가로 서버·칩 %g십억을 나누면 칩이 %.1f백만 개다 — 엑셀의 %.1f 보다'
          % (sh('server_2026'), n, sh('accel_units')))
    print('  적다. 어느 쪽이 맞는지는 칩 믹스를 알아야 갈린다.')

    print()
    print('── HBM 이 메가와트에 얼마나 실리나 ' + '─' * 30)
    chips_mw = gpus_per_mw(kwg)
    for label, gb in (('블랙웰 블렌드', sh('hbm_blackwell_gb')),
                      ('루빈', sh('hbm_rubin_gb')),
                      ('구글 TPU', sh('hbm_tpu_gb'))):
        print('    %-12s 칩당 %gGB — 메가와트당 %.1fTB, 값으로 $%.2f백만'
              % (label, gb, hbm_per_mw(gb, chips_mw),
                 hbm_cost_per_mw(gb, chips_mw, sh('hbm_per_gb'))))
    print('  기가바이트당 %g달러는 엑셀의 블렌드 단가다. 메가와트당 HBM 값이'
          % sh('hbm_per_gb'))
    print('  IT 자본 $%.1f백만의 %.0f~%.0f%% 다.'
          % (it2, hbm_cost_per_mw(sh('hbm_blackwell_gb'), chips_mw,
                                  sh('hbm_per_gb')) / it2 * 100,
             hbm_cost_per_mw(sh('hbm_rubin_gb'), chips_mw,
                             sh('hbm_per_gb')) / it2 * 100))
    print('  엑셀은 HBM 이 가속기 자본지출의 %g%% 라고 냈다.' % sh('hbm_share'))

    print()
    print('── 조달 쪽은 어디서 갈리나 ' + '─' * 38)
    print('  엑셀은 2026년 자본지출이 영업현금흐름의 %.2f 배이고 잉여현금흐름이 %g십억,'
          % (sh('capex_to_ocf'), sh('fcf_2026')))
    print('  2028년에 추가 조달이 %g십억 달러 필요하다고 냈다.' % sh('gap_2028'))
    print('  GPU 금융 층은 그 돈을 빌릴 때 은행이 무엇을 보는지를 준다 — 담보인정비율')
    print('  70~80퍼센트, 부채상환비율 1.3배, 담보가 없으면 금리가 4.38퍼센트포인트 오른다.')

    print()
    print('── 케이스 셋을 우리 단가로 재면 ' + '─' * 34)
    print('%-8s %10s %10s %12s %14s' % ('케이스', '2026E', '2030E', '5년 누적', '누적 용량'))
    for k in ('capex_bear', 'capex_base', 'capex_bull'):
        r = SC['rows'][k]
        vals = r[1:6]
        cum = cumulative(vals)
        print('%-8s %8g십억 %8g십억 %10.1f십억 %10.0f GW'
              % (r[0], vals[0], vals[4], cum,
                 implied_gw(cum, _v_x('capex_per_gw'))))
    base = cumulative(SC['rows']['capex_base'][1:6])
    bear = cumulative(SC['rows']['capex_bear'][1:6])
    bull = cumulative(SC['rows']['capex_bull'][1:6])
    print('  세 케이스가 누적으로 %.0f~%.0f기가와트다. 위아래 폭이 기준의 %.0f퍼센트다.'
          % (implied_gw(bear, _v_x('capex_per_gw')),
             implied_gw(bull, _v_x('capex_per_gw')),
             (bull - bear) / base * 100))
    print('  지상 층의 원문은 2027년까지 세계 데이터센터가 새로 붙이는 발전 용량을')
    print('  약 106기가와트로 봤다(우주영문 L274). 빅4 다섯 해 누적이 그 자리에 선다.')

    print()
    print('── 케이스마다 갈리는 것은 용량이 아니라 조달이다 ' + '─' * 14)
    for k in ('gap_bear', 'gap_base', 'gap_bull'):
        r = SC['rows'][k]
        print('  %-16s 5년 합계 $%.1f십억' % (r[0], cumulative(r[1:6])))
    print('  세 케이스의 2026년 자본지출은 똑같이 %g십억이다 — 그 해는 이미 가이던스가'
          % SC['rows']['capex_base'][1])
    print('  나와 있어 레버가 안 붙는다. 갈리는 것은 2027년부터다.')

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
