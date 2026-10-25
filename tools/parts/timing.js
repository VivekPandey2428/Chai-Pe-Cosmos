const host = window.__world;
const W = window.innerWidth || 1080;
const H = window.innerHeight || 1920;
const VERTICAL = H > W;
const K = Math.min(W, H) / 1080; // pixel scale for 2D drawing and point sizes

// ---------------------------------------------------------------- timing (dialogue track: assets/audio/lines.json)
// whips land on "Earth", "Sun", "galaxy"; the snap back follows the last "हज़ार!"
const SW = { earth: 9.18, orbit: 12.47, galaxy: 16.15, snap: 20.3 };
const WHIPS = [
  { c: SW.earth, b: 0.2, a: 0.18, dir: -1, k: 1 },
  { c: SW.orbit, b: 0.2, a: 0.18, dir: -1, k: 1 },
  { c: SW.galaxy, b: 0.22, a: 0.2, dir: -1, k: 1.15 },
  { c: SW.snap, b: 0.09, a: 0.12, dir: 1, k: 1.35 }, // snap back: the fastest move
];
const NUMS = [
  { value: 1670, plus: false, fly: 10.55, land: 10.9, lock: 11.38, out: 12.27, rim: "#00B4D8" }, // "सत्रह सौ"
  { value: 107000, plus: false, fly: 13.75, land: 14.1, lock: 15.22, out: 15.95, rim: "#FF006E" }, // "एक लाख सात हज़ार"
  { value: 720000, plus: true, fly: 17.9, land: 18.27, lock: 19.55, out: 20.1, rim: "#FF4D9E" }, // "सात लाख बीस हज़ार"
  { value: 720000, plus: true, fly: 20.95, land: 21.25, lock: 21.75, out: 26.5, rim: "#FF2D3D" }, // the gun on the cop himself
];
const T_SUN_WORD = 12.6;
const T_BEAM = 8.85; // the gun fires into the sky on "बैठे हो?"
const T_SELF_BEEP = 21.25; // the gun reads the cop
const T_END = 29.0; // end card
// speaking windows for lip flap
const TALK = {
  cop: [[1.28, 4.4], [8.1, 8.98], [9.22, 12.5], [12.5, 15.86], [15.95, 20.19], [22.2, 23.32], [23.56, 24.36]],
  guy: [[5.39, 6.11], [6.19, 8.03], [26.96, 28.96]],
};
