// 링크드인 흐름 장을 눈으로 보기 위한 촬영. 도해가 섹션 타일 안에 있어서
// shot_figs.js 로는 못 찍는다 — 타일을 먼저 누르고 접힌 것을 전부 편 뒤 찍는다.
//   node scratchpad/shot_liflow.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve('대시보드/링크드인 흐름.html').replace(/\\/g, '/');
  const b = await chromium.launch();

  for (const [name, width] of [['desk', 1280], ['mobile', 390]]) {
    const pg = await b.newPage({ viewport: { width, height: 1000 } });
    await pg.goto('file:///' + file);
    const tile = await pg.$('button.stile[data-sec="sec-li-flow"]');
    if (tile) { await tile.click(); await pg.waitForTimeout(300); }
    await pg.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
    await pg.waitForTimeout(200);

    await pg.screenshot({ path: path.join(outdir, `liflow_${name}_full.png`), fullPage: true });

    // 가로로 밀리면 안 된다(확정 규칙 4절 「모바일」)
    const over = await pg.evaluate(() =>
      document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(name, width, '가로 넘침', over, 'px');

    if (name === 'desk') {
      const figs = await pg.$$('.uc-fig');
      let k = 0;
      for (const f of figs) {
        k += 1;
        await f.scrollIntoViewIfNeeded();
        await f.screenshot({ path: path.join(outdir, `liflow_fig${k}.png`) });
      }
      console.log('도해', k, '장');
    }
    await pg.close();
  }
  await b.close();
})();
