// node audit-shoot.js jobs.json report.json : screenshot each job and run audit.js in the page.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const AUDIT = fs.readFileSync(path.join(__dirname, 'audit.js'), 'utf8');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const report = {};
  for (const j of jobs) {
    const pg = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await pg.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(250);
    const issues = await pg.evaluate(`(${AUDIT})()`);
    await pg.screenshot({ path: j.out });
    await pg.screenshot({ path: j.out.replace(/\.png$/, '.jpg'), type: 'jpeg', quality: 90 });
    await pg.close();
    report[path.basename(j.out)] = issues;
    console.log((issues.length ? 'FAIL ' : 'ok   ') + path.basename(j.out));
    for (const x of issues) console.log('      ' + x);
  }
  fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 1));
  await browser.close();
})();
