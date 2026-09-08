// 통합 보고서 첫 화면 — 최신순 목록과 태그 줄을 눈으로 본다.
//   node scratchpad/shot_replist.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve('대시보드/통합 보고서.html').replace(/\\/g, '/');
  const b = await chromium.launch();

  for (const [name, width] of [['desk', 1280], ['mobile', 390]]) {
    const pg = await b.newPage({ viewport: { width, height: 1100 } });
    await pg.goto('file:///' + file);
    await pg.waitForTimeout(300);

    const over = await pg.evaluate(function () {
      return document.documentElement.scrollWidth - document.documentElement.clientWidth;
    });
    const rows = await pg.$$eval('.rows .row', function (rs) {
      return rs.map(function (r) {
        return {
          tag: r.querySelector('.rtag').textContent,
          title: r.querySelector('.rtitle').textContent.slice(0, 40),
          meta: r.querySelector('.rmeta span').textContent
        };
      });
    });
    console.log(name, width, '가로 넘침', over, 'px · 줄', rows.length);
    if (name === 'desk') {
      rows.forEach(function (r) {
        console.log('   ', r.meta, '|', r.tag, '|', r.title);
      });
    }
    await pg.screenshot({ path: path.join(outdir, 'replist_' + name + '.png') });
    await pg.close();
  }
  await b.close();
})();
