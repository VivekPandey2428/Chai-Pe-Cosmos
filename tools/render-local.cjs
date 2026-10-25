// Renders a HyperFrames-style episode without the HyperFrames CLI: serves the folder, opens the world composition
// in headless Chromium, seeks window.__timelines.world frame by frame and pipes screenshots into ffmpeg.
// Usage: node tools/render-local.cjs <episode-dir> <out.mp4> [--width 720] [--fps 30] [--from 0] [--to END] [--stills t1,t2,...]
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const http = require("http");
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const dir = path.resolve(args[0]);
const out = path.resolve(args[1]);
const width = parseInt(opt("--width", "1080"), 10);
const height = Math.round((width * 16) / 9);
const fps = parseInt(opt("--fps", "30"), 10);
const stills = opt("--stills", null);

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".woff2": "font/woff2",
  ".png": "image/png", ".jpg": "image/jpeg", ".wav": "audio/wav", ".mp3": "audio/mpeg" };
// the composition references assets relative to the project root, so serve it at the root
const comp = fs.readFileSync(path.join(dir, "compositions/world.html"), "utf8");
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split("?")[0]);
  if (url === "/" || url === "/__world.html") {
    res.writeHead(200, { "content-type": "text/html" });
    return res.end(comp);
  }
  const f = path.join(dir, url);
  if (!f.startsWith(dir) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const port = server.address().port;
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.log("pageerror", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.log("console", m.text()); });
  await page.goto(`http://127.0.0.1:${port}/__world.html`);
  await page.waitForFunction(() => window.__hf && window.__hf.buildReady && window.__hf.buildReady.world, null, { timeout: 60000 });
  await page.evaluate(() => window.__hf.buildReady.world);
  await page.evaluate(() => document.fonts.ready);
  const dur = await page.evaluate(() => window.__world.duration);
  const seek = (t) => page.evaluate((t) => { window.__timelines.world.seek(t, false); }, t);

  if (stills) {
    for (const t of stills.split(",").map(Number)) {
      await seek(t);
      await page.screenshot({ path: out.replace(/\.(png|mp4)$/, "") + `-${t.toFixed(2)}.png` });
    }
  } else {
    const from = parseFloat(opt("--from", "0"));
    const to = parseFloat(opt("--to", String(dur)));
    const n = Math.round((to - from) * fps);
    const ff = spawn("ffmpeg", ["-y", "-v", "error", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "png", "-i", "-",
      "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await seek(from + i / fps);
      const buf = await page.screenshot({ type: "png" });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
      if (i % 60 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await new Promise((r) => ff.on("close", r));
  }
  await browser.close();
  server.close();
  console.log("done", out);
})();
