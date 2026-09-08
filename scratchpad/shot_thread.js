// 주장 흐름 — 앞머리·도해·차례가 눈에 어떻게 서는지 본다.
//   node scratchpad/shot_thread.js <출력 폴더>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const outdir = process.argv[2];
  const file = path.resolve('대시보드/AI Engineer 주장 흐름.html').split(path.sep).join('/');
  const b = await chromium.launch();

  for (const [name, width] of [['desk', 1280], ['mobile', 390]]) {
    const pg = await b.newPage({ viewport: { width, height: 1400 } });
    await pg.goto('file:///' + file);
    await pg.waitForTimeout(300);
    const over = await pg.evaluate(function () {
      return document.documentElement.scrollWidth - document.documentElement.clientWidth;
    });
    const info = await pg.evaluate(function () {
      const secs = [].slice.call(document.querySelectorAll('.sec h3')).map(function (h) {
        return h.textContent.trim().slice(0, 30);
      });
      const svg = document.querySelector('.fig svg');
      const texts = [].slice.call(document.querySelectorAll('.fig svg text')).map(function (t) {
        const r = t.getBoundingClientRect();
        return { s: t.textContent.slice(0, 24), x: Math.round(r.x), y: Math.round(r.y),
                 w: Math.round(r.width), h: Math.round(r.height) };
      });
      return { secs: secs, box: svg ? svg.getBoundingClientRect().height : 0, texts: texts };
    });
    let hit = [];
    for (let i = 0; i < info.texts.length; i++) {
      for (let j = i + 1; j < info.texts.length; j++) {
        const a = info.texts[i], c = info.texts[j];
        if (a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h) {
          hit.push(a.s + ' ↔ ' + c.s);
        }
      }
    }
    console.log(name, width, '가로 넘침', over, 'px · 절', info.secs.length,
                '· 도해 높이', Math.round(info.box), '· 글자 겹침', hit.length);
    hit.slice(0, 6).forEach(function (h) { console.log('    겹침:', h); });
    await pg.screenshot({ path: path.join(outdir, 'thread_' + name + '.png') });
    await pg.close();
  }
  await b.close();
})();
