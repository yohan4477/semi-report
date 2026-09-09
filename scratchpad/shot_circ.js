// 통합 보고서 순환금융 층의 도해를 하나씩 찍는다 — 겹침·넘침은 눈으로만 잡힌다.
//   node scratchpad/shot_circ.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

const PAGE = '대시보드/report/card-순환금융-총정리-파는-쪽이-사는-쪽에-돈을-빌려주면-그-고리는-어디서-끊기나.html';

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve(PAGE).split(path.sep).join('/');
  const b = await chromium.launch();

  for (const [name, width] of [['desk', 1280], ['mobile', 390]]) {
    const pg = await b.newPage({ viewport: { width, height: 1000 } });
    await pg.goto('file:///' + encodeURI(file));
    await pg.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
    await pg.waitForTimeout(300);

    const over = await pg.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(name, width, '가로 넘침', over, 'px');

    if (name === 'desk') {
      const figs = await pg.$$('.uc-fig');
      let k = 0;
      for (const f of figs) {
        k += 1;
        await f.scrollIntoViewIfNeeded();
        await f.screenshot({ path: path.join(outdir, 'circ_fig' + k + '.png') });
      }
      console.log('순환금융 층 도해', k, '장');
    }
    await pg.close();
  }
  await b.close();
})();
