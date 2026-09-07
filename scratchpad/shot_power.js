// 통합 보고서 전력 층의 도해를 하나씩 찍는다 — 겹침·넘침은 눈으로만 잡힌다.
//   node scratchpad/shot_power.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve('대시보드/통합 보고서.html').replace(/\\/g, '/');
  const b = await chromium.launch();

  for (const [name, width] of [['desk', 1280], ['mobile', 390]]) {
    const pg = await b.newPage({ viewport: { width, height: 1000 } });
    await pg.goto('file:///' + file);
    const tile = await pg.$('button.stile[data-sec="sec-power"]');
    if (tile) { await tile.click(); await pg.waitForTimeout(300); }
    await pg.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
    await pg.waitForTimeout(200);

    const over = await pg.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(name, width, '가로 넘침', over, 'px');

    if (name === 'desk') {
      const sec = await pg.$('#sec-power');
      const figs = sec ? await sec.$$('.uc-fig') : [];
      let k = 0;
      for (const f of figs) {
        k += 1;
        await f.scrollIntoViewIfNeeded();
        await f.screenshot({ path: path.join(outdir, `power_fig${k}.png`) });
      }
      console.log('전력 층 도해', k, '장');
    }
    await pg.close();
  }
  await b.close();
})();
