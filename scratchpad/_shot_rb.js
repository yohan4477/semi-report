// RocketBlocks 대본 한 장을 막마다 찍는다.
//   node scratchpad/_shot_rb.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = '대시보드/rocketblocks/market-entry-three-answers.html';
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 900, height: 1100 } });
  await pg.goto('file:///' + path.resolve(file).split(path.sep).join('/'));
  await pg.waitForTimeout(300);
  for (const [name, sel] of [['head', 'header'], ['a1', '#a1'], ['a3', '#a3'],
                             ['a4', '#a4'], ['a5', '#a5'], ['x', '#x'], ['e', '#e']]) {
    const el = await pg.$(sel);
    await el.scrollIntoViewIfNeeded();
    await pg.waitForTimeout(120);
    await pg.screenshot({ path: 'scratchpad/_rb_' + name + '.png' });
  }
  // 좁은 폭에서 이름 칸이 접히는지
  await pg.setViewportSize({ width: 400, height: 900 });
  const el = await pg.$('#a1');
  await el.scrollIntoViewIfNeeded();
  await pg.waitForTimeout(200);
  await pg.screenshot({ path: 'scratchpad/_rb_narrow.png' });
  console.log('ok');
  await b.close();
})();
