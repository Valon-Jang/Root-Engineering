import { chromium } from 'playwright';
import fs from 'node:fs';

const outDir = 'out';
fs.mkdirSync(outDir, { recursive: true });
const target = 'https://www.dyson.ie/events/unveiled-2026';
const media = new Map();
const add = (url, type, source) => {
  if (!url) return;
  if (/\.(mp4|m3u8|mpd)(\?|$)/i.test(url) || /video|brightcove|akamai|cloudfront|mux|vimeo/i.test(url) || type === 'media') {
    media.set(url, { url, type, source });
  }
};

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36'
});
const page = await context.newPage();
page.on('request', req => add(req.url(), req.resourceType(), 'request'));
page.on('response', res => add(res.url(), res.request().resourceType(), 'response'));

await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 120000 });
for (const label of ['Accept all', 'Accept All', 'Allow all', 'I agree']) {
  try {
    const b = page.getByRole('button', { name: new RegExp(label, 'i') }).first();
    if (await b.isVisible({ timeout: 1500 })) { await b.click(); break; }
  } catch {}
}

const r3 = page.getByText(/R3 Nurovi Spot\+Scrub/i).first();
try {
  await r3.scrollIntoViewIfNeeded({ timeout: 20000 });
  await page.waitForTimeout(5000);
} catch {}

for (let y = 0; y < await page.evaluate(() => document.body.scrollHeight); y += 850) {
  await page.evaluate(v => window.scrollTo(0, v), y);
  await page.waitForTimeout(400);
}
await page.waitForTimeout(4000);

const domData = await page.evaluate(() => {
  const abs = x => { try { return new URL(x, location.href).href; } catch { return x; } };
  const videos = [...document.querySelectorAll('video')].map((v, i) => ({
    i,
    src: abs(v.currentSrc || v.src || ''),
    poster: abs(v.poster || ''),
    autoplay: v.autoplay,
    muted: v.muted,
    sources: [...v.querySelectorAll('source')].map(s => ({ src: abs(s.src), type: s.type })),
    attrs: Object.fromEntries([...v.attributes].map(a => [a.name, a.value]))
  }));
  const iframes = [...document.querySelectorAll('iframe')].map((f, i) => ({ i, src: abs(f.src), title: f.title }));
  const resources = performance.getEntriesByType('resource').map(r => r.name).filter(x => /\.(mp4|m3u8|mpd)(\?|$)/i.test(x) || /video|brightcove|akamai|cloudfront|mux/i.test(x));
  let r3html = '';
  const nodes = [...document.querySelectorAll('h1,h2,h3,h4,p,div,section')];
  const hit = nodes.find(n => /R3 Nurovi Spot\+Scrub/i.test(n.textContent || '') && (n.textContent || '').length < 1500);
  if (hit) {
    let p = hit;
    for (let i=0; i<4 && p.parentElement; i++) p = p.parentElement;
    r3html = p.outerHTML.slice(0, 120000);
  }
  return { videos, iframes, resources, r3html };
});

for (const v of domData.videos) {
  add(v.src, 'video-dom', 'dom');
  for (const s of v.sources) add(s.src, s.type, 'source-dom');
}
for (const r of domData.resources) add(r, 'performance', 'performance');

fs.writeFileSync(`${outDir}/media.json`, JSON.stringify([...media.values()], null, 2));
fs.writeFileSync(`${outDir}/dom.json`, JSON.stringify({ videos: domData.videos, iframes: domData.iframes }, null, 2));
fs.writeFileSync(`${outDir}/r3.html`, domData.r3html);
fs.writeFileSync(`${outDir}/page.html`, await page.content());
await page.screenshot({ path: `${outDir}/r3-page.png`, fullPage: true });
console.log('VIDEOS', JSON.stringify(domData.videos, null, 2));
console.log('IFRAMES', JSON.stringify(domData.iframes, null, 2));
console.log('MEDIA_URLS');
for (const m of media.values()) console.log(m.url);
await browser.close();
