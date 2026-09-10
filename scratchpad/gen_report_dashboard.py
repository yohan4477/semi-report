# -*- coding: utf-8 -*-
# 통합 보고서 — 카드 여러 장을 한 물음으로 꿴 글 한 편을 싣는 장.
#
# 카드로 쪼개지 않는다. 카드 장(수도리무브 대시보드 등)이 원문 한 편씩을 답한다면
# 여기는 그 답들을 이어 붙인 한 편이다. 그림은 원본 생성기에서 가져다 쓴다 —
# 여기서 다시 그리면 한쪽만 고쳐지는 사고가 난다.
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 본문은 층마다 갈라 둔다 — 경로를 세운 뒤라야 어디서 실행해도 잡힌다
import _cpo_part1  # noqa: E402
import _cpo_fig  # noqa: E402
import _pkg_part1  # noqa: E402
import _pkg_fig  # noqa: E402
import _rep_toc  # noqa: E402
import _rate_part1  # noqa: E402
import _rate_fig  # noqa: E402
import _mem_part1  # noqa: E402
import _power_part1  # noqa: E402
import _circ_part1  # noqa: E402
import _mem_fig  # noqa: E402
import _trump_part1  # noqa: E402
import _harness_part1  # noqa: E402
import _harness_fig  # noqa: E402
import _model_part1  # noqa: E402
import dash_common as dc
from card_lib import fig_html

OUT = os.path.join(dc.ROOT, '대시보드', '통합 보고서.html')
STAMP = '2026-08-24'



# 층 안의 표 — 열이 많아 가로로 넘치면 스스로 스크롤한다.
# 걷어 낸 _biz_part3 에 있던 것을 여기로 옮겼다(2026-09-06)
TABLE_CSS = """
  .biz-tw{overflow-x:auto;margin:14px 0 18px}
  .biz-t{border-collapse:collapse;font-size:13px;line-height:1.65;min-width:640px}
  .biz-t caption{caption-side:top;text-align:left;font-size:12.5px;color:var(--ink-2);
                 padding:0 0 8px;line-height:1.7}
  .biz-t th,.biz-t td{border:1px solid var(--line);padding:7px 10px;vertical-align:top}
  .biz-t thead th{background:var(--accent-soft);font-weight:850;white-space:nowrap}
  .biz-t tbody td:first-child{font-weight:800;white-space:nowrap}
"""

REPORT_CSS = TABLE_CSS + """
  /* 보고서 접기. 제목을 누르면 그 보고서가 통째로 나온다. 타일을 누르면 먼저
     보고서 제목 둘이 보이고, 거기서 볼 것을 고른다. */
  .rrep{margin:0 0 12px}
  .rrep > summary{list-style:none;cursor:pointer}
  .rrep > summary::-webkit-details-marker{display:none}
  .rrep > summary .rep-head{margin:0;position:relative;padding-left:34px;
                            transition:border-color .12s}
  .rrep > summary .rep-head::before{content:"▸";position:absolute;left:16px;top:20px;
                                    color:var(--accent);font-size:15px;font-weight:800}
  .rrep[open] > summary .rep-head::before{content:"▾"}
  .rrep > summary:hover .rep-head{border-color:var(--accent)}
  .rrep > summary .rep-head h2{text-decoration:underline;text-underline-offset:3px;
                               text-decoration-thickness:1px;
                               text-decoration-color:var(--line)}
  .rrep > summary:hover .rep-head h2{text-decoration-color:var(--accent)}
  .rrep-b{padding-top:10px}

  /* 연도별 경로표. 재무 모형은 왼쪽에서 오른쪽으로 읽으므로 연도를 가로축에 둔다
     (회계사 대시보드 규칙 3절). 열 폭은 colgroup 에만 준다 — th 에도 주면 둘을 합쳐
     계산해 첫 열 글자가 다음 열과 포개진다. 좁은 화면에서는 표만 가로로 스크롤한다. */
  .yt-wrap{overflow-x:auto;margin:2px 0 6px;-webkit-overflow-scrolling:touch}
  .yt{border-collapse:collapse;table-layout:fixed;font-size:11.5px;
      font-variant-numeric:tabular-nums;min-width:100%}
  .yt th,.yt td{padding:4px 6px;border-bottom:1px solid var(--line);text-align:right;
                white-space:nowrap}
  .yt thead th{font-size:10.5px;font-weight:850;color:var(--ink-3);
               border-bottom:1.5px solid var(--ink-3)}
  .yt th[scope="row"]{text-align:left;font-weight:800;color:var(--ink-2);
                      position:sticky;left:0;background:var(--card,var(--surface,#fff))}
  /* 구간은 선으로만 나눈다. 한 구간만 칠하면 그 구간이 다른 성격의 값처럼 읽힌다 */
  .yt .cut{border-left:2px solid var(--ink-3)}
  .yt tr.hi td,.yt tr.hi th[scope="row"]{font-weight:850;color:var(--ink)}
  .yt-memo{margin:0 0 10px;font-size:10px;line-height:1.5;color:var(--ink-3)}

  /* ── 계산기 표. 원문이 실은 것이 스프레드시트라 그 꼴을 지킨다 ──────────
     머리 띠 · 줄무늬 · 숫자 오른쪽 정렬 · 합계 줄 굵게. 색은 강조색 하나만 쓰고
     그것도 머리 띠와 합계 줄에만 둔다 — 칸마다 칠하면 어느 값이 중요한지 안 보인다.
     어긋난 칸(모델과 발표치가 다른 줄)만 왼쪽에 굵은 선을 세운다. */
  .xls{margin:2px 0 4px}
  .xlt{display:block;font-size:11.5px;font-weight:850;color:var(--ink);
       padding:6px 10px;border:1px solid var(--ink-3);border-bottom:none;
       border-radius:8px 8px 0 0;background:var(--sunk,#f3f4f6)}
  .xlw{overflow-x:auto;-webkit-overflow-scrolling:touch;
       border:1px solid var(--ink-3);border-radius:0 0 8px 8px}
  .xl{border-collapse:collapse;font-size:11px;min-width:100%;
      font-variant-numeric:tabular-nums}
  .xl th,.xl td{padding:5px 9px;border-bottom:1px solid var(--line);white-space:nowrap}
  /* 머리 칸 정렬은 그 열이 숫자 열인지가 정한다(.num). 자리로 정하면 「복원 방식」
     같은 글자 열의 머리만 오른쪽에 붙어 아래 칸과 어긋난다 */
  .xl thead th{font-size:10.5px;font-weight:850;color:var(--ink);text-align:left;
               background:var(--sunk,#f3f4f6);
               border-bottom:1.5px solid var(--ink-3);position:sticky;top:0}
  .xl thead th.num{text-align:right}
  .xl tbody tr:nth-child(even){background:rgba(127,127,127,.055)}
  .xl td{text-align:left}
  .xl td:first-child{color:var(--ink)}
  /* 둘째 열이 「수량·단위」인 표가 있어 흐리게 두는데, 숫자 열이면 값이므로
     흐리게 하지 않는다 — SKU 표의 첫 값 열이 통째로 흐려졌다(2026-09-09) */
  .xl td:nth-child(2):not(.num){color:var(--ink-3)}
  .xl td.num{text-align:right;font-weight:600;color:var(--ink)}
  .xl tr.sum td{font-weight:850;color:var(--ink);
                border-top:1.5px solid var(--ink-3);background:rgba(127,127,127,.09)}
  /* 원문이 검은 막대로 지운 칸. 빈칸으로 두면 0 으로 읽히므로 칠해서 「모르는 값」
     임을 눈에 보이게 한다. 원문 표의 검은 막대와 같은 자리다 */
  .xl td.red{background:var(--ink-2);opacity:.62}
  .xl tr.off td:first-child{box-shadow:inset 3px 0 0 var(--accent)}
  .xl tr.off td.num{color:var(--ink);font-weight:850}
  /* 추정 배지. 원문 값이 아니라 우리가 고른 가정 위에 선 대목임을 그 자리에서 밝힌다.
     문단 맨 앞과 표 머리 띠에만 붙인다 — 값마다 붙이면 배지가 배경이 된다 */
  .tag-est{display:inline-block;margin-right:6px;padding:1px 7px;border-radius:9px;
           font-size:10px;font-weight:850;letter-spacing:.02em;
           color:var(--paper,#fff);background:var(--ink-2);vertical-align:2px}
  .xlt .tag-est{vertical-align:1px}
  .xl-memo{margin:4px 0 12px;font-size:10.5px;line-height:1.55;color:var(--ink-3)}

  /* ── 수식 블록. 원문이 공표한 식을 기호까지 그대로 낸다 ─────────────────
     왼쪽에 이름, 오른쪽에 식. 등호를 세로로 맞춰 눈이 한 줄로 훑게 한다. */
  .eqbox{border:1px solid var(--ink-3);border-radius:10px;margin:6px 0 12px;
         overflow:hidden}
  .eqhead{display:flex;justify-content:space-between;align-items:baseline;gap:8px;
          padding:7px 10px;background:var(--sunk,#f3f4f6);
          border-bottom:1.5px solid var(--ink-3);font-size:11.5px}
  .eqsrc{font-size:10px;color:var(--ink-3);font-weight:700;white-space:nowrap}
  .eqrow{display:grid;grid-template-columns:minmax(96px,150px) 1fr;gap:10px;
         padding:7px 10px;border-bottom:1px solid var(--line);align-items:baseline}
  .eqrow:last-of-type{border-bottom:none}
  .eqlhs{font-size:11.5px;font-weight:850;color:var(--ink);text-align:right}
  .eqrhs{font-size:12px;color:var(--ink);line-height:1.55;
         font-variant-numeric:tabular-nums;word-break:keep-all}
  .eqop{color:var(--ink-3);font-weight:800;margin-right:4px}
  .eqrhs sub{font-size:.72em;color:var(--ink-2)}
  .eqrhs sup{font-size:.72em}
  .eqnote{margin-top:3px;font-size:10.5px;color:var(--ink-3);line-height:1.5}
  .eqterms{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
           gap:2px 14px;padding:8px 10px;border-top:1.5px solid var(--line);
           background:rgba(127,127,127,.045)}
  .eqterm{font-size:10.5px;color:var(--ink-2);line-height:1.6}
  .eqsym{display:inline-block;min-width:64px;font-weight:850;color:var(--ink)}
  .eqcode{padding:6px 10px;border-top:1px solid var(--line);font-size:10px;
          color:var(--ink-3)}
  @media (max-width:520px){
    .eqrow{grid-template-columns:1fr;gap:2px}
    .eqlhs{text-align:left}
  }

  /* 결론을 두 축으로 가른 판. 왼쪽은 우리가 값을 내는 축, 오른쪽은 시장가를 정답으로
     놓고 되돌리는 축이다. 좁은 화면에서는 세로로 쌓인다.
     두 판은 배경도 테두리도 같다 — 한쪽에 강조색을 깔면 그쪽이 결론처럼 읽힌다.
     나누는 것은 제목(DCF · Reverse-DCF)이지 색이 아니다. */
  .vh2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 8px}
  .vh-ax{padding:8px 10px;border:1px solid var(--line);border-radius:10px}
  .vh-ax > .k{display:block;margin-bottom:7px}
  .vh-ax > .k .en{display:block;font-size:15px;font-weight:850;letter-spacing:.01em;
                  color:var(--ink);line-height:1.2}
  .vh-ax > .k .ko{display:block;font-size:11px;font-weight:700;color:var(--ink-3);
                  line-height:1.4;margin-top:2px}
  .vh-ax .lead{margin:0 0 6px;font-size:11.5px;line-height:1.45;color:var(--ink)}
  .vh-ax .lead b{font-weight:850}
  .vh-ax .top{display:flex;gap:6px;margin-bottom:6px}
  .vh-ax .top div{flex:1;text-align:center;padding:5px 2px;border:1px solid var(--line);
                  border-radius:7px;background:var(--card,var(--surface,#fff))}
  .vh-ax .top .n{display:block;font-size:10px;font-weight:850;color:var(--ink-3)}
  .vh-ax .top .p{display:block;font-size:16px;font-weight:850;color:var(--ink);
                 font-variant-numeric:tabular-nums;line-height:1.3}
  .vh-ax .top .g{display:block;font-size:10.5px;font-weight:800;color:var(--ink-2);
                 font-variant-numeric:tabular-nums}
  .vh-ln{display:flex;justify-content:space-between;gap:7px;padding:1px 0;
         font-size:11px;line-height:1.4;border-top:1px dashed var(--line)}
  .vh-ln:first-of-type{border-top:0}
  .vh-ln .a{color:var(--ink-2);min-width:0}
  .vh-ln .b{color:var(--ink);font-weight:800;text-align:right;white-space:nowrap;
            font-variant-numeric:tabular-nums}
  .vh-ln.sub .a{padding-left:9px;color:var(--ink-3);font-weight:400}
  .vh-ln.sub .b{font-weight:700}
  @media(max-width:560px){ .vh2{grid-template-columns:1fr} }

  /* 알파벳 편 머리 결론 — 스크롤 없이 한 화면에 들어가야 한다.
     표 둘로는 캡션·헤더까지 스무 줄이 넘어 첫 화면을 넘겼다. 값만 남긴 격자로 바꾼다.
     배경 토큰은 --card 가 없는 장이 있어(통합 보고서가 그렇다) --surface 로 되짚는다. */
  .vhero{margin:6px 0 18px;padding:11px 13px;border:1px solid var(--line);
         border-radius:12px;background:var(--card,var(--surface,#fff))}
  .vhero .vh-l{font-size:11px;font-weight:850;letter-spacing:.06em;color:var(--ink-3);
               text-transform:uppercase;margin:0 0 8px}
  .vhero .vh-say{margin:0 0 8px;font-size:13.5px;line-height:1.5;color:var(--ink)}
  .vhero .vh-say b{color:var(--accent)}
  .vh-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 12px}
  .vh-c{padding:9px 10px;border:1px solid var(--line);border-radius:9px;text-align:center}
  .vh-c.now{border-color:var(--accent);background:var(--accent-soft)}
  .vh-c .k{display:block;font-size:10.5px;font-weight:850;color:var(--ink-3);
           letter-spacing:.04em}
  .vh-c .v{display:block;font-size:19px;font-weight:850;line-height:1.25;margin-top:3px;
           font-variant-numeric:tabular-nums;color:var(--ink)}
  .vh-c .d{display:block;font-size:11.5px;font-weight:800;margin-top:1px;color:var(--ink-2);
           font-variant-numeric:tabular-nums}
  .vh-rev{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 10px}
  .vh-r{padding:8px 10px;border:1px dashed var(--line);border-radius:9px}
  .vh-r .k{display:block;font-size:10.5px;font-weight:850;color:var(--ink-3);
           letter-spacing:.04em;margin-bottom:2px}
  .vh-r .t{display:block;font-size:12.5px;line-height:1.5;color:var(--ink)}
  .vh-r .t b{font-variant-numeric:tabular-nums}
  .vh-foot{margin:0;font-size:11.5px;line-height:1.55;color:var(--ink-2)}
  .vh-foot a{font-weight:800}
  @media(max-width:640px){
    .vh-grid{grid-template-columns:repeat(2,1fr)}
    .vh-rev{grid-template-columns:1fr}
    .vh-c .v{font-size:17px}
  }

  /* 시계열 도해의 기준금리 한 줄에만 쓰는 색. 확정 규칙 S2 는 회색만인데, 선이 셋을
     넘으면 회색만으로는 안 갈려서 둔 예외다(2026-09-06). --fig-amber 는 epoch 도해
     안에서만 사는 변수라 여기서는 안 먹었다 — 이 장에서 쓸 것을 따로 정의한다 */
  :root{--rate-amber:#b8860b}
  @media (prefers-color-scheme:dark){:root{--rate-amber:#e0a84a}}
  [data-theme="dark"]{--rate-amber:#e0a84a}
  [data-theme="light"]{--rate-amber:#b8860b}
""" + _rep_toc.CSS + """
"""


def report_cpo_html(head=True):
    """CPO 총정리 — 한 편. 본문은 insights/reports/cpo-2026-09-04.md 원본에서 읽는다."""
    h = [_cpo_part1.HEAD_CPO] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="cpo-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _cpo_part1.report_cpo(sec, p, fig)
    return ''.join(h)


def report_pkg_html(head=True):
    """선단 패키징 총정리 — 한 편. 본문은 insights/reports/pkg-2026-09-05.md 원본에서 읽는다."""
    h = [_pkg_part1.HEAD_PKG] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="pkg-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _pkg_part1.report_pkg(sec, p, fig)
    return ''.join(h)


def report_rate_html(head=True):
    """금리·물가 총정리 — 한 편. 본문은 insights/reports/rate-2026-09-05.md 원본에서 읽는다."""
    h = [_rate_part1.HEAD_RATE] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="rate-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _rate_part1.report_rate(sec, p, fig)
    return ''.join(h)


def _report_model_html(head_html, fn, anchor, head=True):
    """모델링 섹션의 층 둘이 같은 꼴이라 한 함수로 낸다."""
    h = [head_html] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="%s-%d">%s</h3>' % (anchor, n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    fn(sec, p, fig)
    return ''.join(h)


def report_model_cluster_html(head=True):
    """클러스터 총소유비용. 본문은 insights/reports/model-cluster-2026-09-09.md."""
    return _report_model_html(_model_part1.HEAD_CLUSTER, _model_part1.report_cluster,
                              'model-cluster', head)


def report_model_infer_html(head=True):
    """추론 원가. 본문은 insights/reports/model-infer-2026-09-09.md."""
    return _report_model_html(_model_part1.HEAD_INFER, _model_part1.report_infer,
                              'model-infer', head)


def report_model_pjm_html(head=True):
    """PJM 용량 경매. 본문은 insights/reports/model-pjm-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_PJM, _model_part1.report_pjm,
                              'model-pjm', head)


def report_model_roof_html(head=True):
    """웨이퍼 루프라인. 본문은 insights/reports/model-roofline-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_ROOF, _model_part1.report_roof,
                              'model-roof', head)


def report_model_lat_html(head=True):
    """추론 지연. 본문은 insights/reports/model-latency-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_LAT, _model_part1.report_lat,
                              'model-lat', head)


def report_model_torus_html(head=True):
    """토러스 배선. 본문은 insights/reports/model-torus-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_TORUS, _model_part1.report_torus,
                              'model-torus', head)


def report_model_lego_html(head=True):
    """모듈러 자본지출. 본문은 insights/reports/model-lego-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_LEGO, _model_part1.report_lego,
                              'model-lego', head)


def report_model_grd_html(head=True):
    """지상 데이터센터 자본. 본문은 insights/reports/model-ground-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_GRD, _model_part1.report_grd,
                              'model-grd', head)


def report_model_trn_html(head=True):
    """GPU 금융. 본문은 insights/reports/model-trinity-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_TRN, _model_part1.report_trn,
                              'model-trn', head)


def report_model_sx_html(head=True):
    """회수 기간. 본문은 insights/reports/model-payback-2026-09-10.md."""
    return _report_model_html(_model_part1.HEAD_SX, _model_part1.report_sx,
                              'model-sx', head)


def report_trump_html(head=True):
    """트럼프 총정리 — 한 편. 본문은 insights/reports/trump-2026-09-06.md 원본에서 읽는다."""
    h = [_trump_part1.HEAD_TRUMP] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="trump-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _trump_part1.report_trump(sec, p, fig)
    return ''.join(h)


def report_mem_html(head=True):
    """메모리 총정리 — 한 편. 본문은 insights/reports/mem-2026-09-06.md 원본에서 읽는다."""
    h = [_mem_part1.HEAD_MEM] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="mem-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _mem_part1.report_mem(sec, p, fig)
    return ''.join(h)


def report_harness_html(head=True):
    """하네스·스킬 총정리 — 한 편. 본문은 insights/reports/harness-2026-09-08.md 원본에서 읽는다."""
    h = [_harness_part1.HEAD_HARNESS] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="harness-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _harness_part1.report_harness(sec, p, fig)
    return ''.join(h)


def report_power_html(head=True):
    """전력 총정리 — 한 편. 본문은 insights/reports/power-2026-09-07.md 원본에서 읽는다."""
    h = [_power_part1.HEAD_POWER] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="power-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _power_part1.report_power(sec, p, fig)
    return ''.join(h)


def report_circ_html(head=True):
    """순환금융 총정리 — 한 편. 본문은 insights/reports/circ-2026-09-09.md 원본에서 읽는다."""
    h = [_circ_part1.HEAD_CIRC] if head else []
    n = [0]

    def sec(title):
        n[0] += 1
        h.append('<h3 id="circ-%d">%s</h3>' % (n[0], title))

    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))
    _circ_part1.report_circ(sec, p, fig)
    return ''.join(h)


HEADER = '''  <header>
    <p class="eyebrow">여러 편을 한 물음으로 꿴 글</p>
    <h1>통합 보고서</h1>
  </header>'''

LEDE = ('<p class="lede">카드 장이 원문 한 편씩을 답한다면, 이 장은 그 답들을 이어 붙입니다. '
        '지금 실린 것은 여덟입니다 — <b>CPO</b>(광학을 칩 옆까지 끌어온 방식)는 빛이 '
        '데이터센터 어디까지 들어왔는지를, <b>선단 패키징</b>은 다이 하나로 못 만들게 된 뒤 '
        '무엇이 그 일을 대신했는지를, <b>금리·물가</b>는 연준이 내렸는데 왜 장기금리는 '
        '올랐는지를, <b>메모리</b>는 40년 만에 모자란데 왜 만드는 회사 손에 안 남는지를, '
        '<b>트럼프</b>는 무엇을 걸어 무엇을 받아냈는지를, <b>전력</b>은 계통에 막힌 값을 '
        '누가 냈는지를, <b>하네스·스킬</b>은 모델 안에 있던 판단이 바깥으로 걷혀 나간 뒤 '
        '그 값을 누가 냈는지를, <b>순환금융</b>은 파는 쪽이 사는 쪽에 돈을 빌려주는 '
        '고리가 어디서 끊기는지를 묻습니다. 본문은 <code>insights/reports/</code> 의 '
        '원본에서 읽어 옵니다.</p>')

META_ROW = '''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>바탕 <b>SemiAnalysis 37편 · Semi Doped 6회차 · 메르 35편 · 해설 35편 · 링크드인 3개월</b></span>
      <span>보고서 <b>8편</b></span>
    </div>''' % STAMP

FOOTER = (LEDE + META_ROW
          + '\n제3자 해설을 우리가 종합한 글입니다. 투자 추천이 아닙니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_report_dashboard.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

# check_fig.py 가 걷어 가는 목록. 보고서 층 도해는 CARDS 에 없어서 여기 안 적으면
# 검사를 통째로 빠져나간다. 캡션까지 각 층의 CAPTION 이 정본이다
REPORT_FIGS = ([(0, t, svg, '') for t, svg, _c in _cpo_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _pkg_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _rate_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _mem_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _power_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _trump_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _harness_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _circ_part1.CAPTION.values()]
               + [(0, t, svg, '') for t, svg, _c in _model_part1.CAPTION.values()])


# ── 층 일곱을 카드로 세운다 ─────────────────────────────────────────────
# 2026-09-09 이전에는 층이 전부 「카드 없는 고정 층」이었다. 그러면 첫 화면에 목록이
# 빈칸으로 서고 층은 목록 위 링크 한 줄로만 보인다 — 어느 것이 새로 들어왔는지 안 읽힌다.
# 대시보드 규약은 어느 장이든 첫 화면이 최신순 이름 목록이므로(dash_common.render),
# 층 하나를 카드 하나로 옮긴다. **섹션 id 는 sec-* 그대로 둔다** — check_report 가
# 그 id 로 층의 글자를 잘라 숫자를 대조하고, 층마다 재료가 달라 한 칸에 섞으면 안 된다.
#
# 카드 하나에 섹션 하나라 태그 줄과 목록이 1:1 이다. 층이 열을 넘어가면 그때 갈래로
# 묶는다 — 지금 묶으면 check_report 의 재료 칸이 한 덩어리가 된다.
LAYERS = [
    # 모델링 섹션 — 카드 둘이 한 섹션에 선다. 재료도 어긋난 자리도 달라 한 글로
    # 묶으면 절이 열넷이 된다. 섹션 id 가 같으면 dash_common 이 한 <section> 으로 묶는다
    ('sec-model', '모델링', '2026-09-09',
     '클러스터 총소유비용 — 발표된 계산기를 다시 세우면 굿풋에서 어긋난다',
     'SemiAnalysis 영문 1편 · 표 그림 4장',
     '총소유비용은 달러까지 맞는데 그 안의 굿풋 표가 자기 공표 수식과 어긋난다',
     report_model_cluster_html),
    ('sec-model', '모델링', '2026-09-09',
     '추론 원가 — AMD 는 빌리면 엔비디아에 지고, 사서 쓰면 작업에 따라 이긴다',
     'SemiAnalysis 영문 1편 · 표 그림 3장',
     '원문은 임대 시세로만 답했는데, 같은 데이터를 소유 기준으로 풀면 답이 뒤집힌다',
     report_model_infer_html),
    ('sec-model', '모델링', '2026-09-10',
     'PJM 용량 경매 — 모델링 가정 하나가 6,600만 명의 전기요금이 되는 길',
     'SemiAnalysis 영문 1편의 본문 값',
     '공급곡선이 끝에서 수직이라, 요구 용량을 조금만 낮춰도 값이 반토막 난다',
     report_model_pjm_html),
    ('sec-model', '모델링', '2026-09-10',
     '웨이퍼 한 장짜리 칩 — 면적은 이기고 둘레는 지는 자리',
     'SemiAnalysis 영문 1편의 본문 값',
     '데이터가 나가는 통로는 면적이 아니라 가장자리에 붙는다',
     report_model_roof_html),
    ('sec-model', '모델링', '2026-09-10',
     '추론 지연 — 「150초에 초당 1,000토큰」이 실제로 무엇을 뜻하나',
     'SemiAnalysis 영문 2편의 본문 값',
     '원문이 낸 식 하나에서 대화 속도와 동시 요청과 토큰당 원가가 따라 나온다',
     report_model_lat_html),
    ('sec-model', '모델링', '2026-09-10',
     '토러스 배선 — 랙이 커지면 칩 한 장에 붙는 광 부품이 준다',
     'SemiAnalysis 영문 1편 · 표 그림 1장',
     '칩이 놓인 자리가 배선을 정하고, 거기서 나온 부착률은 랙 크기에 매여 있다',
     report_model_torus_html),
    ('sec-model', '모델링', '2026-09-10',
     '모듈러 데이터센터 — 8퍼센트가 인건비에서 나온다는 생각이 틀린 자리',
     'SemiAnalysis 영문 1편의 본문 값',
     '현장 시간은 62퍼센트가 주는데 값은 8퍼센트만 준다',
     report_model_lego_html),
    ('sec-model', '모델링', '2026-09-10',
     '지상 데이터센터 자본 — 전력을 어렵게 끌수록 매출의 몇 할이 자본으로 가나',
     'SemiAnalysis 영문 1편의 본문 값',
     '자본과 전기만으로 매출의 3분의 1이 나가고, 그 나머지로 GPU 값을 대야 한다',
     report_model_grd_html),
    ('sec-model', '모델링', '2026-09-10',
     'GPU 금융 — 바닥값을 깔아 주면 이익이 어디로 가나',
     'SemiAnalysis 영문 1편의 본문 값',
     '바닥값을 받으면 청구가의 18퍼센트를 떼 주고, 안 받으면 이익률에서 9퍼센트포인트가 깎인다',
     report_model_trn_html),
    ('sec-model', '모델링', '2026-09-10',
     '회수 기간 — 기가와트당 500억 달러를 1년에 갚는다는 말이 서는 자리',
     'SemiAnalysis 영문 1편의 본문 값',
     '그 1년은 매출에서 비용을 빼기 전의 값이다',
     report_model_sx_html),
    ('sec-circ', '순환금융', '2026-09-09',
     '순환금융 총정리 — 파는 쪽이 사는 쪽에 돈을 빌려주면, 그 고리는 어디서 끊기나',
     'SemiAnalysis 12편 · 메르 6편',
     '지분과 보증과 계약이 한 고리 위에 겹쳐 있어 어느 마디가 약한지가 안 보인다',
     report_circ_html),
    ('sec-harness', '하네스·스킬', '2026-09-08',
     '하네스·스킬 총정리 — 판단을 모델에서 걷어 낸 열두 달, 그 값을 누가 냈나',
     'AI Engineer 발표 16편 · SemiAnalysis 2편',
     '모델 안에 있던 판단이 바깥으로 걷혀 나간 뒤 같은 해 세 답이 서로를 반박한다',
     report_harness_html),
    ('sec-power', '전력', '2026-09-07',
     '전력 총정리 — 데이터센터가 계통에 막힌 뒤, 그 값을 누가 냈나',
     'SemiAnalysis 12편 · 팟캐스트 1회차 · 전략 판 1회차',
     '경매와 요금제를 거쳐 그 값이 결국 어느 청구서에 실렸나',
     report_power_html),
    ('sec-trump', '트럼프', '2026-09-06',
     '트럼프 총정리 — 무엇을 걸어 무엇을 받아냈고, 한국은 그 순서 어디에서 값을 냈나',
     '메르 47편',
     '위협하고 미루고 거래하고 청구하는 순서가 되풀이되고, 한국은 그 끝에서 값을 낸다',
     report_trump_html),
    ('sec-mem', '메모리', '2026-09-06',
     '메모리 총정리 — 40년 만에 모자란데 왜 만드는 회사가 안 웃나',
     'SemiAnalysis 5편 · 링크드인 3개월 · 해설 11편',
     '값은 오르는데 만드는 회사 손에 안 남는 자리를 원가와 계약 쪽에서 짚는다',
     report_mem_html),
    ('sec-rate', '금리·물가', '2026-09-05',
     '금리·물가 총정리 — 연준이 내렸는데 왜 장기금리는 올랐고, 누가 그것을 다르게 읽나',
     '메르 24편 · 해설 17편',
     '같은 값을 놓고 필자마다 다르게 읽는 자리를 맞대 놓았다',
     report_rate_html),
    ('sec-pkg', '선단 패키징', '2026-09-05',
     '선단 패키징 총정리 — 다이 하나로 못 만들게 된 뒤 무엇이 그 자리를 대신했나',
     'SemiAnalysis 9편 · Semi Doped 1회차 · 영문 클리핑 2편',
     '인터포저·EMIB·하이브리드 본딩이 저마다 무엇을 대신하고 무엇을 못 하나',
     report_pkg_html),
    ('sec-cpo', 'CPO', '2026-09-04',
     'CPO 총정리 — 빛이 구리를 어디까지 밀어냈고, 누가 그 자리에 서 있나',
     'SemiAnalysis 9편 · Semi Doped 5회차 · 링크드인 4개월',
     '광학이 칩 옆까지 온 뒤 모듈·스위치·트랜시버 회사의 자리가 어떻게 갈렸나',
     report_cpo_html),
]


def cards():
    """층 하나 = 카드 하나. 본문은 층 함수가 머리 없이 낸 HTML 을 그대로 끼운다."""
    out = []
    for i, (sid, tag, day, title, base, gain, fn) in enumerate(LAYERS, 1):
        out.append({
            'section': (sid, '%02d' % i, tag, base),
            'title': title,
            'gain': gain,
            'meta': [day, base],
            # ('raw', …) 는 층 HTML 을 그대로 끼우는 자리다. 층은 자기 차례와 절 번호를
            # _rep_toc 로 이미 붙여 놓았으므로 카드 쪽에서 다시 세우지 않는다
            'report': [('raw', fn(head=False))],
        })
    return out


if __name__ == '__main__':
    dc.render(cards(), '통합 보고서', HEADER, FOOTER, OUT,
              page_slug='report',
              extra_css=REPORT_CSS)

    # 차례 규약(_rep_toc)을 손으로 우회한 층이 있나. 있으면 커밋 사슬을 끊는다
    _bad = _rep_toc.check_toc(io.open(OUT, encoding="utf-8").read())
    if _bad:
        raise SystemExit('차례 규약 위반\n  ' + '\n  '.join(_bad))
    print("  차례 규약 OK")
