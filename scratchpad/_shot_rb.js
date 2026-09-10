// RocketBlocks 글 한 장을 위·중·아래로 찍는다.
//   node scratchpad/_shot_rb.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = '대시보드/rocketblocks/market-entry-three-answers.html';
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 900, height: 1100 } });
  await pg.goto('file:///' + path.resolve(file).split(path.sep).join('/'));
  await pg.waitForTimeout(300);
  for (const [name, sel] of [['head', 'header'], ['b3', '#b3'], ['b6', '#b6'], ['b8', '#b8']]) {
    const el = await pg.$(sel);
    await el.scrollIntoViewIfNeeded();
    await pg.waitForTimeout(120);
    await pg.screenshot({ path: 'scratchpad/_rb_' + name + '.png' });
  }
  const idx = '대시보드/RocketBlocks 대시보드.html';
  await pg.goto('file:///' + path.resolve(idx).split(path.sep).join('/'));
  await pg.screenshot({ path: 'scratchpad/_rb_idx.png' });
  console.log('ok');
  await b.close();
})();
