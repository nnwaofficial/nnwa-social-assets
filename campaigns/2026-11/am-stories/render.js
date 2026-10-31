// node render.js <out-dir> [date ...]  -> 1080x1920 JPGs from am-stories.json via am.html
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const out = process.argv[2];
const only = process.argv.slice(3);
const specs = JSON.parse(fs.readFileSync(path.join(__dirname, 'am-stories.json'), 'utf8'));
(async () => {
  fs.mkdirSync(out, { recursive: true });
  let browser;
  try { browser = await chromium.launch(); }
  catch (e) { browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }); }
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'am.html'));
  for (const d of specs) {
    if (only.length && !only.includes(d.date)) continue;
    const m = await page.evaluate(d => window.build(d), d);
    await page.evaluate(() => document.fonts.ready);
    const m2 = await page.evaluate(d => window.build(d), d);
    await page.waitForTimeout(80);
    await page.screenshot({ path: path.join(out, d.file), type: 'jpeg', quality: 92 });
    console.log(d.file, 'content bottom', Math.round(m2.bottom), m2.bottom > 1420 ? 'TOO LOW' : 'ok');
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
