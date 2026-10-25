// Renders brand/cover-2560x1440.png and brand/avatar-800x800.png from still.html (served over http for ES modules).
const { chromium } = require("playwright");
const base = process.argv[2];
(async () => {
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
for (const [mode, w, h] of [["cover", 2560, 1440], ["avatar", 800, 800]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.log("pageerror", e.message));
  await page.goto(`${base}/still.html?mode=${mode}`);
  await page.waitForFunction(() => window.__done === true, null, { timeout: 120000 });
  await page.screenshot({ path: `brand/${mode === "cover" ? "cover-2560x1440" : "avatar-800x800"}.png` });
  await page.close();
  console.log("rendered", mode);
}
await browser.close();
})();
