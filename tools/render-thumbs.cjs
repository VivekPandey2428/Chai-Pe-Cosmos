// Renders an episode's thumbnails: hero layer (transparent) -> anchors -> layout template -> PNG + JPG.
// usage: node tools/render-thumbs.cjs http://127.0.0.1:8765 thumbs/ep01.json
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const [base, epPath] = process.argv.slice(2);
const ep = JSON.parse(fs.readFileSync(epPath, "utf8"));
const id = path.basename(epPath, ".json");
(async () => {
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  for (const [format, f] of Object.entries(ep.formats)) {
    const [w, h] = f.size;
    const hero = await browser.newPage({ viewport: { width: w, height: h } });
    hero.on("pageerror", (e) => console.log("hero error", e.message));
    await hero.goto(`${base}/thumb-hero.html?ep=${epPath}&format=${format}`);
    await hero.waitForFunction(() => window.__done === true, null, { timeout: 120000 });
    const heroPng = `thumbs/out/${id}-hero-${format}.png`;
    await hero.screenshot({ path: heroPng, omitBackground: true });
    fs.writeFileSync(`thumbs/out/${id}-anchors-${format}.json`, JSON.stringify(await hero.evaluate(() => window.__anchors)));
    await hero.close();
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    page.on("pageerror", (e) => console.log("layout error", e.message));
    await page.goto(`${base}/thumb.html?ep=${epPath}&format=${format}&hero=${heroPng}&anchors=thumbs/out/${id}-anchors-${format}.json`);
    await page.waitForFunction(() => window.__done === true, null, { timeout: 60000 });
    await page.screenshot({ path: `thumbs/out/${id}-thumb-${format}.png` });
    await page.screenshot({ path: `thumbs/out/${id}-thumb-${format}.jpg`, type: "jpeg", quality: 92 });
    await page.close();
    console.log("rendered", format);
  }
  await browser.close();
})();
