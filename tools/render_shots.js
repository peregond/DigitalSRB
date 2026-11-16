// Renders every tools/shots/*.html to a PNG next to it. Usage: node tools/render_shots.js <dir> <width> <height> <scale>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [dir, w, h, s] = [process.argv[2], +process.argv[3], +process.argv[4], +process.argv[5]];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: s });
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html'))) {
    await page.goto('file://' + path.resolve(dir, f), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    await page.screenshot({ path: path.resolve(dir, f.replace('.html', '.png')), omitBackground: process.argv[6] === 'transparent' });
  }
  await browser.close();
})();
