// 글 페이지의 도해(.uc-fig)를 하나씩 PNG 로 찍는다 — 눈으로 보는 확인용.
// node scratchpad/shot_figs.js <html 경로> <출력 폴더> <접두어>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, outdir, prefix] = process.argv.slice(2);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await pg.goto('file:///' + path.resolve(html).replace(/\\/g, '/'));
  const figs = await pg.$$('.uc-fig');
  let k = 0;
  for (const f of figs) {
    k += 1;
    await f.screenshot({ path: path.join(outdir, `${prefix}_${k}.png`) });
  }
  // 본문의 이름 색 — 첫 절 머리 근처를 한 장
  const h2 = await pg.$('.lane h2');
  if (h2) {
    await h2.scrollIntoViewIfNeeded();
    await pg.screenshot({ path: path.join(outdir, `${prefix}_body.png`), clip: { x: 0, y: 0, width: 1280, height: 700 } });
  }
  console.log(prefix, '도해', k, '장');
  await b.close();
})();
