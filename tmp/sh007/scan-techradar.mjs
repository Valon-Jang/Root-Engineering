import { chromium } from 'playwright';
import fs from 'node:fs';
const out='out'; fs.mkdirSync(out,{recursive:true});
const target='https://www.techradar.com/home/robot-vacuums/itll-light-up-your-home-like-a-bowling-alley-dysons-new-nurovi-robot-vacuum-has-a-uv-light-to-show-up-invisible-spills-and-im-not-sure-im-ready-to-see-whats-on-my-floors';
const media=new Map();
const add=(url,type,source)=>{ if(!url)return; if(/\.(mp4|m3u8|mpd|webm)(\?|$)/i.test(url)||/(jwplayer|jwp|video|brightcove|vimeo|youtube|futr|futurecdn|cloudfront|akamai|mux)/i.test(url)||type==='media') media.set(url,{url,type,source}); };
const browser=await chromium.launch({headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000},userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36'});
const page=await context.newPage();
page.on('request',r=>add(r.url(),r.resourceType(),'request'));
page.on('response',r=>add(r.url(),r.request().resourceType(),'response'));
await page.goto(target,{waitUntil:'domcontentloaded',timeout:120000});
for(const label of ['Accept all','Accept All','I Accept','Agree','Allow all']){try{const b=page.getByRole('button',{name:new RegExp(label,'i')}).first();if(await b.isVisible({timeout:1200})){await b.click();break;}}catch{}}
await page.waitForTimeout(3000);
for(let y=0;y<await page.evaluate(()=>document.body.scrollHeight);y+=700){await page.evaluate(v=>scrollTo(0,v),y);await page.waitForTimeout(250);}
for(const sel of ['button[aria-label*="play" i]','.jw-icon-playback','.vjs-big-play-button','button[class*="play" i]']){try{for(const b of await page.locator(sel).all()){if(await b.isVisible()){await b.click({timeout:2000}).catch(()=>{});await page.waitForTimeout(2500);}}}catch{}}
await page.waitForTimeout(4000);
const dom=await page.evaluate(()=>{const abs=x=>{try{return new URL(x,location.href).href}catch{return x}};return {
 videos:[...document.querySelectorAll('video')].map((v,i)=>({i,src:abs(v.currentSrc||v.src||''),poster:abs(v.poster||''),outer:v.outerHTML.slice(0,4000)})),
 iframes:[...document.querySelectorAll('iframe')].map((f,i)=>({i,src:abs(f.src),title:f.title,outer:f.outerHTML.slice(0,3000)})),
 scripts:[...document.scripts].map(s=>s.src||s.textContent||'').filter(x=>/(jwplayer|jwp|video|mp4|m3u8|youtube|brightcove)/i.test(x)).slice(0,200)
};});
for(const v of dom.videos)add(v.src,'video-dom','dom');
for(const f of dom.iframes)add(f.src,'iframe','dom');
for(const r of await page.evaluate(()=>performance.getEntriesByType('resource').map(x=>x.name))) add(r,'performance','perf');
fs.writeFileSync(`${out}/media.json`,JSON.stringify([...media.values()],null,2));
fs.writeFileSync(`${out}/dom.json`,JSON.stringify(dom,null,2));
fs.writeFileSync(`${out}/page.html`,await page.content());
console.log('VIDEOS',JSON.stringify(dom.videos,null,2));
console.log('IFRAMES',JSON.stringify(dom.iframes,null,2));
console.log('MEDIA'); for(const m of media.values())console.log(m.url);
await browser.close();
