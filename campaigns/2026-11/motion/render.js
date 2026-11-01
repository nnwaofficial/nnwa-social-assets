// Render NNWA motion reels: node render.js <out-dir> [slug ...] [--stills t1,t2,...]
// Loads reel.html, builds each reel from reels.json, steps window.seek(t) at 30 fps and pipes JPEG frames to ffmpeg.
// Sound: audio.py synthesises an original 120 BPM track plus haptic SFX from window.events(), muxed at -14 LUFS.
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
const KEY = { '2026-11-04-reel-500g': 'C', '2026-11-12-reel-oil': 'D', '2026-11-18-reel-sources': 'F', '2026-11-22-reel-breakfasts': 'G', '2026-11-25-reel-move': 'A', '2026-11-29-reel-recap': 'E' };
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
    const silent = path.join(out, slug + '.silent.mp4');
    const evf = path.join(out, slug + '.events.json'), wav = path.join(out, slug + '.wav');
    fs.writeFileSync(evf, JSON.stringify(await page.evaluate(() => window.events())));
    require('child_process').execFileSync('python3', [path.join(HERE, 'audio.py'), evf, total.toFixed(3), wav, KEY[slug] || 'C'], { stdio: 'inherit' });
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', silent],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(total * FPS);
    for (let f = 0; f < n; f++) {
      await page.evaluate(t => window.seek(t), f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
    require('child_process').execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', silent, '-i', wav,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-maxrate', '10M', '-bufsize', '20M', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.1',
      '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', file], { stdio: 'inherit' });
    fs.unlinkSync(silent);
    console.log('wrote', file, n, 'frames', total.toFixed(2) + 's');
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
