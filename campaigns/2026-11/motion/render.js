// Render NNWA motion reels: node render.js <out-dir> [slug ...] [--stills t1,t2,...]
// Loads reel.html, builds each reel from reels.json, steps window.seek(t) at 30 fps and pipes JPEG frames to ffmpeg.
// Silent by design: add a track from Instagram's licensed library in the app if wanted.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const HERE = __dirname;
const args = process.argv.slice(2);
const out = args.shift();
let stills = null;
const si = args.indexOf('--stills');
if (si >= 0) { stills = args[si + 1].split(',').map(Number); args.splice(si, 2); }
const spec = JSON.parse(fs.readFileSync(path.join(HERE, 'reels.json'), 'utf8'));
const slugs = args.length ? args : Object.keys(spec).filter(k => !k.startsWith('_'));

(async () => {
  fs.mkdirSync(out, { recursive: true });
  let browser;
  try { browser = await chromium.launch(); }
  catch (e) { browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }); }
  for (const slug of slugs) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto('file://' + path.join(HERE, 'reel.html'));
    const total = await page.evaluate(s => window.build(s), spec[slug]);
    await page.evaluate(() => window.ready());
    if (stills) {
      for (const t of stills) {
        await page.evaluate(t => window.seek(t), t);
        await page.screenshot({ path: path.join(out, `${slug}-t${t}.jpg`), type: 'jpeg', quality: 85 });
      }
      console.log(slug, 'stills, total', total.toFixed(2));
      await page.close();
      continue;
    }
    const file = path.join(out, slug + '.mp4');
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', file],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(total * FPS);
    for (let f = 0; f < n; f++) {
      await page.evaluate(t => window.seek(t), f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
    console.log('wrote', file, n, 'frames', total.toFixed(2) + 's');
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
