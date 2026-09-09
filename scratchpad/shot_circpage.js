// 순환금융 층 1절을 한 화면에 담아 찍는다 — 도해와 그 설명이 같이 보이는지 본다.
//   node scratchpad/shot_circpage.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

const PAGE = '대시보드/report/card-순환금융-총정리-파는-쪽이-사는-쪽에-돈을-빌려주면-그-고리는-어디서-끊기나.html';

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve(PAGE).split(path.sep).join('/');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 900, height: 1200 } });
  await pg.goto('file:///' + encodeURI(file));
  await pg.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
  await pg.waitForTimeout(300);
  const h = await pg.$('#circ-1');
  if (h) {
    await h.evaluate((el) => el.scrollIntoView({ block: 'start' }));
    await pg.waitForTimeout(200);
  }
  await pg.screenshot({ path: path.join(outdir, 'circ_sec1.png') });
  console.log('찍었다');
  await b.close();
})();
