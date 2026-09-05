// 통합 보고서의 선단 패키징 층(#sec-pkg) 도해를 한 장씩, 그리고 층 머리를 데스크톱·모바일로 찍는다.
// node scratchpad/shot_cpo.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [outdir] = process.argv.slice(2);
  const html = path.resolve('대시보드/통합 보고서.html');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await pg.goto('file:///' + html.replace(/\\/g, '/'));
  // 접힌 층을 편다
  await pg.evaluate(() => {
    document.querySelectorAll('details').forEach(d => { d.open = true; });
    const s = document.querySelector('#sec-pkg');
    if (s) {
      s.querySelectorAll('[hidden]').forEach(e => { e.hidden = false; });
      let e = s;
      while (e) { e.hidden = false; if (e.style) e.style.display = ''; e = e.parentElement; }
      s.querySelectorAll('.rrep').forEach(d => { d.open = true; });
    }
  });
  const figs = await pg.$$('#sec-pkg .uc-fig');
  let k = 0;
  for (const f of figs) {
    k += 1;
    await f.scrollIntoViewIfNeeded();
    await f.screenshot({ path: path.join(outdir, `pkg_fig_${k}.png`) });
  }
  const head = await pg.$('#rep-pkg');
  if (head) {
    await head.scrollIntoViewIfNeeded();
    await pg.screenshot({ path: path.join(outdir, 'pkg_head_1280.png'), clip: { x: 0, y: 0, width: 1280, height: 900 } });
  }
  const tbl = await pg.$('#sec-pkg table.biz-t');
  if (tbl) { await tbl.scrollIntoViewIfNeeded(); await tbl.screenshot({ path: path.join(outdir, 'pkg_table.png') }); }
  await pg.setViewportSize({ width: 390, height: 844 });
  if (head) {
    await head.scrollIntoViewIfNeeded();
    await pg.screenshot({ path: path.join(outdir, 'pkg_head_390.png'), clip: { x: 0, y: 0, width: 390, height: 844 } });
  }
  const sw = await pg.evaluate(() => document.documentElement.scrollWidth);
  console.log('도해', k, '장 · 390px scrollWidth', sw);
  await b.close();
})();
