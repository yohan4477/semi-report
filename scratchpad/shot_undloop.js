// 언더스탠딩 고리 도해 한 장만 찍는다 — 번호와 범례가 겹치지 않는지 눈으로 본다.
//   node scratchpad/shot_undloop.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

const PAGE = '대시보드/understanding/card-번-돈이-중국-밖으로-나가지-않기-시작했다.html';

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve(PAGE).split(path.sep).join('/');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 1000 } });
  await pg.goto('file:///' + encodeURI(file));
  await pg.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
  await pg.waitForTimeout(300);
  const figs = await pg.$$('figure');
  let k = 0;
  for (const f of figs) {
    k += 1;
    await f.scrollIntoViewIfNeeded();
    await f.screenshot({ path: path.join(outdir, 'und_fig' + k + '.png') });
  }
  console.log('도해', k, '장');
  await b.close();
})();
