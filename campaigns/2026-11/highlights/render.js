// node render.js <out-dir> : Instagram Highlight covers + "Start here" Story frames
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const COVERS = ['start', 'tools', 'courses', 'protein', 'eatwell', 'data', 'festivals'];
const FRAMES = JSON.parse(fs.readFileSync(path.join(__dirname, 'start-here.json'), 'utf8'));
(async () => {
  let b; try { b = await chromium.launch(); } catch (e) { b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }); }
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(__dirname, 'hl.html'));
  for (const k of COVERS) { await p.evaluate(k => window.cover(k), k); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(80);
    await p.screenshot({ path: path.join(out, `cover-${k}.jpg`), type: 'jpeg', quality: 92 }); }
  for (const [i, f] of FRAMES.entries()) { await p.evaluate(f => window.frame(f), f); await p.evaluate(() => document.fonts.ready); await p.evaluate(f => window.frame(f), f); await p.waitForTimeout(80);
    await p.screenshot({ path: path.join(out, `start-here-${i + 1}.jpg`), type: 'jpeg', quality: 92 }); }
  await b.close(); console.log('done');
})().catch(e => { console.error(e); process.exit(1); });
