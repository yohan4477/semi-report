// 모바일 폭(390px)에서 페이지가 옆으로 밀리는지 Playwright 로 잰다.
//   node scratchpad/check_scroll.js <html 경로> [<html 경로> …]
// 옆으로 밀리는 장은 「경로  scrollWidth > innerWidth」 한 줄을 내고 종료 코드 1.
// 정적 검사로는 못 본다 — 표 5열이 390px 에서 어떻게 접히는지는 브라우저만 안다.
// 2026-09-02 Semi Doped 글 페이지에서 표가 한 글자씩 세로로 늘어진 것을 눈으로 보고 세웠다.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const files = process.argv.slice(2);
  if (!files.length) { console.error('html 경로를 준다'); process.exit(2); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  let bad = 0;
  for (const f of files) {
    const url = 'file:///' + path.resolve(f).replace(/\\/g, '/');
    await page.goto(url);
    const r = await page.evaluate(() => ({
      sw: document.documentElement.scrollWidth, iw: window.innerWidth,
    }));
    if (r.sw > r.iw + 1) { console.log(`FAIL ${f}  scrollWidth ${r.sw} > innerWidth ${r.iw}`); bad++; }
    else console.log(`OK   ${f}`);
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
