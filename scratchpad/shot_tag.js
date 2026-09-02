// 목록 첫 줄과 글 페이지 판 머리를 찍는다 — 꼬리표(한글패치) 확인용.
// node scratchpad/shot_tag.js <출력 폴더> <slug>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, slug] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const url = (p) => 'file:///' + path.resolve(p).split(path.sep).join('/');
  await pg.goto(url('대시보드/Semi Doped 대시보드.html'));
  const row = await pg.$('a.row[href*="' + slug + '"]');
  await row.scrollIntoViewIfNeeded();
  await pg.screenshot({ path: path.join(out, 'tag_index.png'), clip: { x: 0, y: 200, width: 1280, height: 420 } });
  await pg.goto(url('대시보드/semidoped/' + slug + '.html'));
  await pg.screenshot({ path: path.join(out, 'tag_post.png'), clip: { x: 0, y: 0, width: 1280, height: 420 } });
  await b.close();
  console.log('shots');
})();
