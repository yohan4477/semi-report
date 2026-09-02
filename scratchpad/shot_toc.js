// 목차 링크를 눌렀을 때 절 머리가 화면 위에 잘리지 않고 서는지 찍는다.
//   node scratchpad/shot_toc.js <html> <out_dir> [width]
// 각 목차 링크를 차례로 눌러 <out_dir>/toc_<n>_<width>.png 을 남기고, 절 제목의 위 끝 y 를 찍는다.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [file, outDir, w] = process.argv.slice(2);
  const width = parseInt(w || '1280', 10);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height: width < 600 ? 844 : 900 } });
  await page.goto('file:///' + path.resolve(file).replace(/\\/g, '/'));
  const n = await page.locator('nav.toc a').count();
  for (let i = 0; i < n; i++) {
    const a = page.locator('nav.toc a').nth(i);
    const href = await a.getAttribute('href');
    await a.click();
    await page.waitForTimeout(150);
    const top = await page.evaluate((h) => {
      const el = document.querySelector(h);
      return el ? Math.round(el.getBoundingClientRect().top) : null;
    }, href);
    console.log(`${href}  heading top y=${top}`);
    await page.screenshot({ path: path.join(outDir, `toc_${i + 1}_${width}.png`) });
    await page.evaluate(() => window.scrollTo(0, 0));
  }
  await browser.close();
})();
