// Challan #2 "Wazan Ka Challan", built on Episode 1's scene. Episode 1's header follows.
// Challan: a cosmic traffic cop stops a guy sipping chai for "speeding" and his radar gun proves it,
// scale by scale (Earth's spin, the orbit, the galaxy), until he points it at himself.
// render(t) is a pure function of t (seconds); nothing reads the previous frame. Built for 9:16, recomposes for 16:9.
import * as THREE from "./vendor/three/three.module.min.js";
import { RoomEnvironment } from "./vendor/three/addons/RoomEnvironment.js";
import { FontLoader } from "./vendor/three/addons/FontLoader.js";
import { TextGeometry } from "./vendor/three/addons/TextGeometry.js";
import { RoundedBoxGeometry } from "./vendor/three/addons/RoundedBoxGeometry.js";


const host = window.__world;
const W = window.innerWidth || 1080;
const H = window.innerHeight || 1920;
const VERTICAL = H > W;
// device pixels per CSS pixel: 2 when the renderer captures 4K from the 1080x1920 layout
const DPR = window.devicePixelRatio || 1;
const K = (Math.min(W, H) / 1080) * DPR; // device-pixel scale for 2D drawing and point sizes

// ---------------------------------------------------------------- timing (dialogue track: assets/audio/lines.json)
// Challan #2 "Wazan Ka Challan": home -> the Moon (whip lands on "चाँद") -> Jupiter (on "Jupiter") -> snap home before "तो वहाँ सीधा jail!"
const DUR = 57.13;
const SW = { moon: 17.7, jupiter: 24.06, snap: 29.25 };
const WHIPS = [
  { c: SW.moon, b: 0.2, a: 0.18, dir: -1, k: 1 },
  { c: SW.jupiter, b: 0.2, a: 0.18, dir: -1, k: 1.1 },
  { c: SW.snap, b: 0.09, a: 0.12, dir: 1, k: 1.35 }, // snap back: the fastest move
];
const NUMS = [
  { value: 168, plus: false, fly: 2.42, land: 2.78, lock: 3.66, out: 5.95, rim: "#FF2D3D" }, // "एक सौ अड़सठ" on the chair
  { value: 28, plus: false, fly: 21.66, land: 22.01, lock: 22.45, out: 23.4, rim: "#8E9BB8" }, // "अट्ठाईस" on the Moon
  { value: 400, plus: true, fly: 26.66, land: 27.01, lock: 27.57, out: 29.05, rim: "#E8914A" }, // "चार सौ" on Jupiter
  { value: 168, plus: false, fly: 32.68, land: 33.03, lock: 33.91, out: 36.6, rim: "#34C759" }, // "एक सौ अड़सठ": mass, everywhere
];
const T_BEAM = 52.3; // the gun fires at the Moon rising for the teaser ("चाँद की FIR")
const T_BEAM_OFF = 54.5;
const T_TROMBONE = 37.35;
const T_END = 38.75; // end card
// speaking windows for lip flap (first to last word of each line)
const TALK = {
  cop: [[1.0, 5.9], [16.91, 17.43], [23.52, 24.74], [29.33, 31.05], [40.67, 47.67], [50.64, 54.45]],
  guy: [[6.25, 16.66], [17.73, 23.17], [25.09, 28.93], [31.35, 37.27], [47.97, 50.29], [54.76, 56.53]],
};

// ---------------------------------------------------------------- helpers
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const lerp = (a, b, x) => a + (b - a) * x;
const seg = (t, a, b) => clamp01((t - a) / (b - a));
const outBack = (x, s = 1.70158) => {
  const u = clamp01(x) - 1;
  return 1 + (s + 1) * u * u * u + s * u * u;
};
const outExpo = (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp01(x)));
const inCubic = (x) => clamp01(x) ** 3;
const inOutSine = (x) => 0.5 - 0.5 * Math.cos(Math.PI * clamp01(x));
const TAU = Math.PI * 2;
function mulberry32(a) {
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const gauss = (rnd) => {
  const u = Math.max(1e-6, rnd());
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * rnd());
};
const col = (h) => new THREE.Color(h);

function softDiscTexture(inner, outer, size = 256) {
  const c = document.createElement("canvas");
  c.width = c.height = size;
  const g = c.getContext("2d");
  const grad = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  grad.addColorStop(0, inner);
  grad.addColorStop(1, outer);
  g.fillStyle = grad;
  g.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
const shadowTex = softDiscTexture("rgba(40,10,20,0.55)", "rgba(40,10,20,0)");

// ---------------------------------------------------------------- renderer
const renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("w-canvas"),
  antialias: true,
  alpha: true,
  preserveDrawingBuffer: true,
});
renderer.setPixelRatio(DPR);
renderer.setSize(W, H, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.autoClear = false;
renderer.setClearColor(0x000000, 0);

const pmrem = new THREE.PMREMGenerator(renderer);
const envMap = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

const scene = new THREE.Scene();
scene.environment = envMap;
scene.environmentIntensity = 0.85;
const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 400);

const hemi = new THREE.HemisphereLight(0xffffff, 0x553344, 0.6);
const key = new THREE.DirectionalLight(0xfff1e0, 2.4);
key.position.set(-4, 7, 6);
const rim = new THREE.DirectionalLight(0xcfe8ff, 1.6);
rim.position.set(5, 3, -6);
scene.add(hemi, key, rim);

const glossy = (hex, extra = {}) =>
  new THREE.MeshPhysicalMaterial({
    color: hex,
    roughness: 0.32,
    metalness: 0,
    clearcoat: 1,
    clearcoatRoughness: 0.08,
    ...extra,
  });

// deterministic sine-noise field (Sun surface)
function landNoise(p) {
  return (
    Math.sin(p.x * 2.1 + 1.3) * Math.cos(p.y * 2.7 - 0.4) +
    0.7 * Math.sin(p.z * 3.1 + p.x * 1.2) +
    0.45 * Math.cos(p.y * 4.3 + p.z * 2.2 + 2.0) +
    0.3 * Math.sin((p.x + p.y + p.z) * 5.7)
  );
}
// Earth: low-poly icosphere; continents from rough lon/lat outlines so it reads as Earth at a glance
const LAND = [
  // Africa
  [[-17,15],[-17,21],[-13,28],[-9,32],[-6,35.8],[10,37],[11,33],[20,31],[32,31.5],[34,28],[38,18],[43,12],[51,11.5],[48,4],[40,-3],[40,-11],[35,-20],[35,-24],[32,-29],[27,-34],[20,-35],[18,-29],[14,-23],[12,-17],[13,-10],[9,-1],[9,4],[5,5],[-4,5],[-8,4.5],[-13,8]],
  // Madagascar
  [[44,-25],[47,-25],[50,-15],[49,-12],[44,-16]],
  // Eurasia (with Arabia and India)
  [[-9,38.7],[-9,43],[-1,46],[-4,48],[2,51],[5,53],[8,54],[8,57],[10,58],[5,59],[5,62],[14,67],[20,70],[28,71],[40,67],[44,68],[60,69],[70,73],[80,73],[100,77],[110,74],[130,71],[150,71],[170,70],[180,68],[180,65],[170,60],[163,58],[156,51],[156,57],[143,59],[141,53],[140,48],[135,43],[130,42.5],[129,35],[126,35],[126,38],[122,40],[121,37],[119,35],[122,31],[121,28],[117,23.5],[110,21],[108,21.5],[106,18],[109,12],[105,9],[103,10],[100,13],[99,9],[103,1.5],[100,3],[98,8],[98,16],[94,16],[92,22],[88,22],[80,15],[77,8],[73,16],[72,21],[67,24],[61,25],[57,25.5],[56,27],[50,30],[48,29.5],[50,25],[56,24],[59,22],[52,16],[43,13],[39,22],[35,28],[34,31],[35,36],[30,36.5],[27,37],[26,40],[23,40],[23,36.5],[20,40],[19,42],[13,45.5],[12,44],[16,41],[18,40],[16,38],[15,40],[10,44],[7,43.5],[3,43],[3.2,42],[0,39],[-2,36.7],[-5.6,36],[-9,37]],
  // Great Britain, Ireland
  [[-5,50],[1.5,51],[1.7,53],[-0.2,54],[-2,56],[-3,58.6],[-6,58],[-5.5,55],[-3,54],[-4.5,52.8],[-5,51.5]],
  [[-10,51.5],[-6,52],[-6,55],[-8,55.3],[-10,54]],
  // Japan, Borneo, Sumatra, New Guinea
  [[130,31],[135,34],[140,35],[142,40],[141.5,45],[145,44],[140,41],[136,37],[131,34]],
  [[109,1],[117,7],[119,5],[116,-4],[110,-3]],
  [[95,5.5],[98,4],[106,-6],[102,-4]],
  [[131,-1],[141,-2.6],[150,-10],[141,-9],[138,-8]],
  // Australia
  [[114,-22],[114,-34],[118,-35],[124,-34],[131,-31.5],[138,-35],[140,-38],[147,-39],[150,-37],[153,-31],[153,-25],[146,-19],[142,-10.7],[141,-17],[136,-15],[137,-12],[131,-11.5],[126,-14],[122,-18]],
  // North and Central America
  [[-168,65.5],[-163,70],[-156,71.3],[-141,69.6],[-128,70],[-115,68.5],[-100,68],[-94,70],[-85,69.5],[-82,66],[-87,64],[-93,61],[-94,58.7],[-90,57],[-82,55],[-79,52],[-79,57],[-77,61],[-73,62],[-64,60],[-61,56],[-56,52],[-60,48.5],[-66,49],[-64,45],[-67,44.5],[-70,43],[-70,41.5],[-74,40.5],[-76,37],[-75.5,35.2],[-78,33.8],[-81,31.5],[-80.5,28],[-80,25.2],[-81.5,25.5],[-83,29],[-85,29.7],[-89,30],[-94,29.5],[-97,27.5],[-97.5,22],[-95,18.5],[-91,18.5],[-90.5,21],[-87,21.5],[-88,16],[-84,15],[-83.5,11],[-81.5,9],[-79.5,9.5],[-77.5,8.5],[-80,7.3],[-83,8.3],[-86,11],[-88,13.2],[-92,14.5],[-96,15.7],[-105,19.5],[-105.7,22.5],[-109,25.7],[-112.7,31.7],[-114.5,30],[-110,23],[-112,24.5],[-115,28.5],[-117,32.5],[-120.6,34.5],[-124,40.5],[-124.5,48],[-130,54.5],[-136,58],[-145,60.3],[-152,59],[-158,56.5],[-164,54.8],[-157,58.5],[-162,60],[-165,62.5],[-166,64.5]],
  // Greenland
  [[-73,78],[-60,82],[-30,83.5],[-20,81],[-18,77],[-22,70],[-32,68],[-40,65],[-43,60],[-48,61],[-53,66],[-55,70],[-58,75.5],[-68,76.5]],
  // South America
  [[-77.5,8.5],[-71.5,12.4],[-64,10.7],[-60,8.5],[-52,5],[-50,0],[-44,-2.5],[-35,-5],[-35,-9],[-39,-15],[-41,-22],[-48,-25.5],[-53,-34],[-57,-36],[-57,-38.5],[-62,-39],[-65,-42],[-65,-47],[-69,-51],[-68.5,-55],[-72,-54],[-75,-50],[-73.5,-44],[-73.5,-37],[-71.5,-30],[-70.3,-18],[-76,-14],[-81,-6],[-80,-1],[-79.5,1.5],[-77.5,4],[-77.4,7]],
];
const DESERT = [
  [[-17,15],[-17,27],[-8,32],[10,33],[20,31],[32,31],[35,23],[38,17],[33,15],[15,14],[0,15]], // Sahara
  [[35,30],[48,30],[56,24],[58,21],[52,16],[43,13],[39,21]], // Arabia
  [[44,30],[62,25],[66,30],[60,37],[50,35]], // Iran
  [[12,-17],[25,-17],[28,-25],[20,-30],[15,-28]], // Kalahari
  [[115,-22],[122,-19],[135,-18],[142,-22],[140,-30],[131,-31],[120,-32],[116,-28]], // Australian outback
  [[90,38],[110,42],[112,45],[100,46],[90,44]], // Gobi
  [[-117,32],[-110,31],[-104,30],[-103,36],[-113,40],[-119,38]], // US southwest
];
function inPoly(lon, lat, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if (yi > lat !== yj > lat && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
// local +z is longitude EARTH_LON0; longitude grows toward +x (east), so the spin carries the surface rightwards
const EARTH_LON0 = 24.6;
function surfaceKind(m) {
  const lat = (Math.asin(Math.max(-1, Math.min(1, m.y))) * 180) / Math.PI;
  let lon = (Math.atan2(m.x, m.z) * 180) / Math.PI + EARTH_LON0;
  lon = ((((lon + 180) % 360) + 360) % 360) - 180;
  if (lat < -66 || lat > 80) return "ice";
  if (!LAND.some((p) => inPoly(lon, lat, p))) return "ocean";
  return DESERT.some((p) => inPoly(lon, lat, p)) ? "sand" : "land";
}
const EARTH_COLORS = { ocean: "#1E3A8A", land: "#34C759", sand: "#E8C07D", ice: "#F4FBFF" };
function paintLowPoly(geo, kindOf) {
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  for (let i = 0; i < pos.count; i += 3) {
    a.fromBufferAttribute(pos, i);
    b.fromBufferAttribute(pos, i + 1);
    c.fromBufferAttribute(pos, i + 2);
    const kind = kindOf(a.clone().add(b).add(c).divideScalar(3).normalize());
    const k = col(EARTH_COLORS[kind]);
    for (let j = 0; j < 3; j++) colors.set([k.r, k.g, k.b], (i + j) * 3);
  }
  geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  return geo;
}
const earthMaterial = () =>
  new THREE.MeshPhysicalMaterial({ vertexColors: true, flatShading: true, roughness: 0.55, clearcoat: 0.25, clearcoatRoughness: 0.25, envMapIntensity: 0.5 });
function makeEarth(radius) {
  return new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(radius, 12), surfaceKind), earthMaterial());
}


// ---------------------------------------------------------------- materials and rig helpers
const clay = (hex, extra = {}) =>
  new THREE.MeshPhysicalMaterial({
    color: hex,
    roughness: 0.8,
    metalness: 0,
    envMapIntensity: 0.4,
    specularIntensity: 0.25,
    ...extra,
  });

function capsuleBetween(a, b, r, mat) {
  const dir = new THREE.Vector3().subVectors(b, a);
  const len = dir.length();
  const m = new THREE.Mesh(new THREE.CapsuleGeometry(r, len, 8, 20), mat);
  m.position.copy(a).addScaledVector(dir, 0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
  return m;
}

function cylinderBetween(top, bottom, rTop, rBottom, mat) {
  const dir = new THREE.Vector3().subVectors(top, bottom);
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rTop, rBottom, dir.length(), 16), mat);
  m.position.copy(bottom).addScaledVector(dir, 0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
  return m;
}
// a unit capsule (straight part 1) stretched between two points each frame
function setSegment(mesh, a, b, r) {
  const d = new THREE.Vector3().subVectors(b, a);
  const len = d.length();
  mesh.position.copy(a).addScaledVector(d, 0.5);
  mesh.scale.set(1, (len + 2 * r) / (1 + 2 * r), 1);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
}

const GROUND_R = 3.6; // the chair sits on top of a small low-poly planet
const groundDrop = (x, z) => GROUND_R - Math.sqrt(Math.max(0, GROUND_R * GROUND_R - x * x - z * z));
const smooth = (a, b, x) => {
  const u = clamp01((x - a) / (b - a));
  return u * u * (3 - 2 * u);
};


// ---------------------------------------------------------------- keyed acting
// track(t, [[time, value, ease?], ...]): values are numbers or [x, y, z]; ease "back" overshoots into the key.
function track(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, v0] = keys[i];
    const [t1, v1, ease] = keys[i + 1];
    if (t < t1) {
      const x = ease === "back" ? outBack(seg(t, t0, t1), 1.4) : ease === "snap" ? outExpo(seg(t, t0, t1)) : inOutSine(seg(t, t0, t1));
      return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], x)) : lerp(v0, v1, x);
    }
  }
  return keys[keys.length - 1][1];
}
const V = (a) => new THREE.Vector3(a[0], a[1], a[2]);
const within = (t, wins) => wins.some(([a, b]) => t >= a && t < b);
// lip flap: two incommensurate sines so the mouth never repeats a pattern
const flap = (t) => clamp01(0.35 + 0.4 * Math.sin(t * 31) + 0.35 * Math.sin(t * 19.3 + 1.1));

// a kulhad: unglazed terracotta cup of chai
function makeKulhad() {
  const k = new THREE.Group();
  const terracotta = clay("#B5562F", { roughness: 0.92 });
  const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.1, 0.24, 28), terracotta);
  const lip = new THREE.Mesh(new THREE.TorusGeometry(0.145, 0.018, 8, 28), terracotta);
  lip.rotation.x = Math.PI / 2;
  lip.position.y = 0.12;
  const chai = new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.135, 0.01, 28), clay("#C68E5E", { roughness: 0.35 }));
  chai.position.y = 0.105;
  k.add(cup, lip, chai);
  return k;
}

// shared head pieces: skin sphere, ears, nose, eyes with lids and glints, brows, smile, open mouth
function makeFace(skin, { browMat, browR = 0.02, browLen = 0.1, noseR = 0.035 }) {
  const eyeMat = new THREE.MeshPhysicalMaterial({ color: "#1A1410", roughness: 0.25, clearcoat: 1 });
  const sparkle = new THREE.MeshBasicMaterial({ color: "#FFFFFF" });
  const mouthMat = clay("#5A2A1E");
  const head = new THREE.Group();
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.5, 48, 32), skin);
  skull.scale.set(1, 0.95, 0.95);
  head.add(skull);
  for (const sx of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), skin);
    ear.position.set(0.48 * sx, -0.02, 0);
    ear.scale.set(0.45, 0.75, 0.55);
    head.add(ear);
  }
  const nose = new THREE.Mesh(new THREE.SphereGeometry(noseR, 12, 10), skin);
  nose.position.set(0, -0.08, 0.47);
  head.add(nose);
  const eyes = [], lids = [], brows = [];
  for (const sx of [-1, 1]) {
    const eye = new THREE.Group();
    eye.position.set(0.18 * sx, -0.01, 0.425);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.075, 20, 16), eyeMat);
    ball.scale.set(0.85, 1.2, 0.5);
    const glint = new THREE.Mesh(new THREE.SphereGeometry(0.017, 10, 8), sparkle);
    glint.position.set(0.02, -0.012, 0.04);
    // eyelid: a skin hemisphere rotating over the eye (-PI/2 open, 0 half-closed, ~1.1 closed)
    const lid = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 10, 0, TAU, 0, Math.PI / 2), skin);
    lid.scale.set(0.075 * 0.85 * 1.15, 0.075 * 1.2 * 1.12, 0.075 * 0.5 * 1.3);
    eye.add(ball, glint, lid);
    head.add(eye);
    eyes.push(eye);
    lids.push(lid);
    const brow = new THREE.Group();
    brow.position.set(0.18 * sx, 0.15, 0.425);
    const bm = new THREE.Mesh(new THREE.CapsuleGeometry(browR, browLen, 6, 10), browMat);
    bm.rotation.z = Math.PI / 2;
    brow.add(bm);
    head.add(brow);
    brows.push(brow);
  }
  const smileGeo = new THREE.TorusGeometry(0.06, 0.012, 8, 20, Math.PI * 0.8);
  smileGeo.rotateZ(Math.PI * 0.1);
  const smile = new THREE.Mesh(smileGeo, mouthMat);
  smile.position.set(0, -0.2, 0.43);
  const mouthO = new THREE.Mesh(new THREE.SphereGeometry(0.045, 14, 10), mouthMat);
  mouthO.position.set(0, -0.21, 0.425);
  head.add(smile, mouthO);
  return { head, eyes, lids, brows, smile, mouthO };
}

// face state: lid angle, eye scale, brows [leftY, leftRot, rightY, rightRot], smile curve (1 smile, -1 frown), mouth open
function applyFace(f, { lid, eyeS = 1, brows = [0, 0, 0, 0], curve = 1, smileW = 1, open = 0 }) {
  f.lids.forEach((l) => (l.rotation.x = lid));
  f.eyes.forEach((e) => e.scale.setScalar(eyeS));
  f.brows[0].position.y = 0.15 + brows[0];
  f.brows[0].rotation.z = brows[1];
  f.brows[1].position.y = 0.15 + brows[2];
  f.brows[1].rotation.z = brows[3];
  f.smile.rotation.z = curve >= 0 ? Math.PI : 0;
  f.smile.position.y = curve >= 0 ? -0.2 : -0.25;
  const s = Math.max(0.001, 1 - clamp01(open));
  f.smile.scale.set(smileW * s, Math.max(0.001, Math.abs(curve)) * s, 1);
  f.mouthO.scale.set(0.001 + clamp01(open), 0.001 + 1.35 * clamp01(open), 0.4);
}

function makeArms(parent, sleeve, cuffMat, skin, shoulder) {
  const arms = [];
  for (let i = 0; i < 2; i++) {
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.095, 18, 14), skin);
    const upper = new THREE.Mesh(new THREE.CapsuleGeometry(0.115, 1, 8, 16), sleeve);
    const fore = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 1, 8, 16), sleeve);
    const cf = new THREE.Mesh(new THREE.CylinderGeometry(0.115, 0.115, 0.08, 18), cuffMat);
    parent.add(hand, upper, fore, cf);
    arms.push({ hand, upper, fore, cf });
  }
  // i = 0 left, 1 right; hand positions in the parent's space
  return function setArms(handL, handR, elbowOut = 0.2) {
    [handL, handR].forEach((hp, i) => {
      const sx = i ? 1 : -1;
      const a = shoulder(sx);
      const elbow = a.clone().lerp(hp, 0.5).add(new THREE.Vector3(elbowOut * sx, -0.2, -0.08));
      const wrist = elbow.clone().lerp(hp, 0.82);
      arms[i].hand.position.copy(hp);
      setSegment(arms[i].upper, a, elbow, 0.115);
      setSegment(arms[i].fore, elbow, wrist, 0.11);
      arms[i].cf.position.copy(wrist);
      arms[i].cf.quaternion.copy(arms[i].fore.quaternion);
    });
  };
}

// ---------------------------------------------------------------- the guy: designer-vinyl toy in his armchair
function makeGuy() {
  const skin = clay("#E8A87C");
  const hairMat = clay("#3B2416", { roughness: 0.7 });
  const hoodie = clay("#FF8A3D");
  const hoodieDeep = clay("#EE7428");
  const joggers = clay("#1E3A8A");
  const joggersDeep = clay("#172E6E");
  const sneaker = clay("#F6F5F0");
  const sole = clay("#34C759");
  const phones = clay("#2A2D34", { roughness: 0.55 });
  const sand = clay("#E8C07D", { roughness: 0.9 });
  const wood = clay("#8A5A35", { roughness: 0.5, envMapIntensity: 0.6 });
  const g = new THREE.Group();

  // mid-century armchair: sand upholstery, walnut frame, splayed tapered legs
  const chair = new THREE.Group();
  const base = new THREE.Mesh(new RoundedBoxGeometry(1.75, 0.08, 1.45, 4, 0.03), wood);
  base.position.set(0, 0.62, 0);
  const seat = new THREE.Mesh(new RoundedBoxGeometry(1.6, 0.3, 1.35, 5, 0.12), sand);
  seat.position.set(0, 0.81, 0.02);
  const back = new THREE.Mesh(new RoundedBoxGeometry(1.55, 1.1, 0.28, 5, 0.12), sand);
  back.position.set(0, 1.5, -0.66);
  back.rotation.x = -0.2;
  chair.add(base, seat, back);
  for (const sx of [-1, 1]) {
    const arm = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.06, 1.25, 4, 0.025), wood);
    arm.position.set(0.9 * sx, 1.3, -0.05);
    chair.add(arm);
    chair.add(cylinderBetween(new THREE.Vector3(0.9 * sx, 1.28, 0.45), new THREE.Vector3(0.9 * sx, 0.62, 0.45), 0.032, 0.032, wood));
    chair.add(cylinderBetween(new THREE.Vector3(0.9 * sx, 1.28, -0.55), new THREE.Vector3(0.9 * sx, 0.62, -0.5), 0.032, 0.032, wood));
    chair.add(cylinderBetween(new THREE.Vector3(0.6 * sx, 0.62, -0.62), new THREE.Vector3(0.62 * sx, 1.95, -0.9), 0.035, 0.035, wood));
    for (const sz of [-1, 1]) {
      const bx = 0.85 * sx, bz = 0.72 * sz;
      chair.add(cylinderBetween(new THREE.Vector3(0.75 * sx, 0.6, 0.6 * sz), new THREE.Vector3(bx, -0.16, bz), 0.045, 0.028, wood));
    }
  }
  g.add(chair);

  const fig = new THREE.Group();
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.36, 0.42, 10, 28), hoodie);
  torso.position.set(0, 1.56, -0.04);
  torso.scale.set(1.08, 1, 0.88);
  const pocket = new THREE.Mesh(new RoundedBoxGeometry(0.46, 0.2, 0.07, 4, 0.035), hoodieDeep);
  pocket.position.set(0, 1.38, 0.29);
  pocket.rotation.x = -0.15;
  const hood = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.1, 12, 28), hoodie);
  hood.position.set(0, 2.05, -0.1);
  hood.rotation.x = Math.PI / 2 - 0.35;
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.13, 0.2, 16), skin);
  neck.position.set(0, 2.16, 0);
  fig.add(torso, pocket, hood, neck);
  for (const sx of [-1, 1]) {
    fig.add(cylinderBetween(new THREE.Vector3(0.07 * sx, 2.02, 0.25), new THREE.Vector3(0.075 * sx, 1.8, 0.3), 0.014, 0.014, sneaker));
  }
  const bandGeo = new THREE.TorusGeometry(0.27, 0.035, 10, 40, Math.PI * 1.3);
  bandGeo.rotateZ(Math.PI * 0.85);
  bandGeo.rotateX(Math.PI / 2);
  const band = new THREE.Mesh(bandGeo, phones);
  band.position.set(0, 2.1, -0.02);
  band.rotation.x = 0.25;
  fig.add(band);
  for (const sx of [-1, 1]) {
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.105, 0.08, 24), phones);
    cup.rotation.z = Math.PI / 2;
    cup.position.set(0.25 * sx, 2.04, 0.12);
    fig.add(cup);
  }
  fig.add(capsuleBetween(new THREE.Vector3(-0.2, 1.16, 0), new THREE.Vector3(0.2, 1.16, 0), 0.25, joggers));
  for (const sx of [-1, 1]) {
    fig.add(capsuleBetween(new THREE.Vector3(0.2 * sx, 1.15, 0.05), new THREE.Vector3(0.22 * sx, 1.1, 0.64), 0.155, joggers));
    fig.add(capsuleBetween(new THREE.Vector3(0.22 * sx, 1.08, 0.68), new THREE.Vector3(0.23 * sx, 0.24, 0.78), 0.135, joggers));
    const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.08, 20), joggersDeep);
    cuff.position.set(0.23 * sx, 0.2, 0.78);
    const shoe = new THREE.Mesh(new RoundedBoxGeometry(0.25, 0.17, 0.44, 4, 0.07), sneaker);
    shoe.position.set(0.23 * sx, 0.05, 0.84);
    shoe.rotation.y = 0.12 * sx;
    const soleM = new THREE.Mesh(new RoundedBoxGeometry(0.27, 0.07, 0.46, 4, 0.03), sole);
    soleM.position.set(0.23 * sx, -0.07, 0.84);
    soleM.rotation.y = 0.12 * sx;
    fig.add(cuff, shoe, soleM);
  }

  const face = makeFace(skin, { browMat: clay("#3B2416") });
  const head = face.head;
  head.position.set(0, 2.62, 0);
  const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.53, 48, 24, 0, TAU, 0, 1.45), hairMat);
  hairCap.position.set(0, 0.02, -0.01);
  hairCap.rotation.x = -0.38;
  hairCap.scale.set(1, 0.96, 0.97);
  head.add(hairCap);
  const quiff = new THREE.Group();
  quiff.position.set(0.0, 0.36, 0.16);
  const wave = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 18), hairMat);
  wave.scale.set(0.27, 0.12, 0.25);
  wave.position.set(0.02, 0.07, 0.07);
  wave.rotation.x = -0.75;
  const crown = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 18), hairMat);
  crown.scale.set(0.3, 0.11, 0.26);
  crown.position.set(0, 0.04, -0.1);
  crown.rotation.x = -0.15;
  quiff.add(wave, crown);
  head.add(quiff);
  fig.add(head);

  const kulhad = makeKulhad();
  const kulhad2 = makeKulhad(); // the one he offers the cop; handed over by the caller
  fig.add(kulhad);
  const setArms = makeArms(fig, hoodie, hoodieDeep, skin, (sx) => new THREE.Vector3(0.38 * sx, 1.98, -0.02));
  const steam = [];
  const steamMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.6, transparent: true, opacity: 0.6 });
  for (let i = 0; i < 3; i++) {
    const s = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 10), steamMat.clone());
    steam.push(s);
    fig.add(s);
  }
  g.add(fig);

  const shGeo = new THREE.PlaneGeometry(3.2, 2.8, 16, 16);
  shGeo.rotateX(-Math.PI / 2);
  const sh = new THREE.Mesh(shGeo, new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false, toneMapped: false }));
  sh.position.set(0, 0.01, 0.1);
  g.add(sh);

  // ---- acting (guy-local positions; he faces +z, the cop stands to his front right)
  const REST_R = [0.16, 1.78, 0.6], SIP_R = [0.05, 2.3, 0.55], RAISE_R = [0.32, 2.3, 0.8], TOAST_R = [0.42, 2.6, 1.0];
  const REST_L = [-0.3, 1.3, 0.58], CHEST = [-0.06, 1.85, 0.36], POCKET = [-0.12, 1.45, 0.42], OFFER = [0.42, 2.0, 1.0];
  const DOWN = [-0.42, 1.12, 0.92], WAVE = [-0.36, 2.75, 0.7];
  const HAND_R = [[0, SIP_R], [0.95, SIP_R], [1.2, REST_R, "back"], [6.9, REST_R], [7.1, RAISE_R, "back"], [8.1, RAISE_R], [8.4, REST_R],
    [34.9, REST_R], [35.1, RAISE_R, "back"], [36.3, RAISE_R], [36.6, REST_R], [38.85, REST_R], [39.05, SIP_R], [39.7, SIP_R], [40.0, REST_R],
    [42.0, REST_R], [42.2, SIP_R], [43.0, SIP_R], [43.3, REST_R], [47.75, REST_R], [48.0, TOAST_R, "back"], [50.4, TOAST_R], [50.7, REST_R],
    [56.65, REST_R], [57.05, SIP_R]];
  const HAND_L = [[0, REST_L], [9.3, REST_L], [9.5, CHEST, "back"], [10.4, CHEST], [10.6, REST_L], [14.1, REST_L], [14.3, DOWN, "back"],
    [16.4, DOWN], [16.7, REST_L], [37.8, REST_L], [37.95, POCKET], [38.05, POCKET], [38.3, OFFER, "back"], [38.6, OFFER], [38.85, REST_L],
    [54.7, REST_L], [54.95, WAVE, "back"], [56.3, WAVE], [56.7, REST_L]];
  const LID = [[0, 1.1], [0.95, 1.1], [1.05, -1.75, "snap"], [1.6, -1.35], [5.9, -1.35], [6.2, -0.85], [29.2, -0.85], [31.3, -0.6], [37.3, -0.6],
    [37.4, 1.0], [37.8, 1.0], [38.0, 0.05], [38.95, 0.05], [39.05, 1.1], [39.7, 1.1], [40.0, 0.05], [42.1, 0.05], [42.2, 1.1], [43.0, 1.1],
    [43.3, -0.85], [47.8, -0.85], [48.0, -1.45], [50.4, -1.45], [50.7, -0.85], [56.6, -0.85], [57.0, 1.1]];
  const YAW = [[0, 0], [1.0, 0], [1.2, 0.55, "back"], [47.8, 0.55], [48.05, -0.35, "back"], [50.5, -0.35], [50.8, 0.55], [56.7, 0.55], [57.1, 0]];
  function pose(t, ti = t) {
    const breathe = Math.sin(TAU * ti / 1.5);
    const startle = Math.sin(Math.PI * seg(t, 1.0, 1.8)) * (t < 1.8 ? 1 : 0);
    const confused = smooth(1.7, 1.9, t) * (1 - smooth(5.8, 6.1, t));
    const smug = smooth(31.3, 31.6, t) * (1 - smooth(37.25, 37.4, t)) + smooth(16.85, 17.0, t) * (1 - smooth(17.5, 17.65, t));
    const laugh = smooth(37.35, 37.45, t) * (1 - smooth(37.85, 38.0, t));
    const sip = smooth(38.95, 39.05, t) * (1 - smooth(39.7, 39.9, t)) + smooth(42.1, 42.2, t) * (1 - smooth(43.0, 43.2, t))
      + (t < 0.95 ? 1 : 0) * (1 - smooth(0.93, 1.05, t)) + smooth(56.95, 57.05, t);
    const rise = smooth(55.5, 55.9, t) * (1 - smooth(56.6, 57.0, t)); // "मैं चला...": half out of the chair
    const dt = t - SW.snap;
    const wind = dt >= 0 && dt < 1.2 ? Math.exp(-((dt / 0.32) ** 2)) : 0;
    fig.position.y = 0.018 * breathe + 0.12 * startle + 0.03 * Math.abs(Math.sin(t * 22)) * laugh + 0.22 * rise;
    fig.position.z = 0.12 * rise;
    fig.rotation.x = 0.12 * rise;
    torso.scale.set(1.08 * (1 + 0.015 * breathe), 1 - 0.015 * breathe + 0.06 * startle, 0.88);
    head.rotation.y = track(t, YAW) + 0.06 * Math.sin(TAU * ti / 5);
    head.rotation.z = 0.06 * Math.sin(TAU * ti / 3) + 0.12 * confused - 0.08 * smug;
    head.rotation.x = -0.04 - 0.16 * sip - 0.12 * laugh + 0.04 * Math.sin(t * 22) * laugh;
    head.position.y = 2.62 + 0.012 * breathe;
    const talking = within(t, TALK.guy) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.45 * startle,
      brows: [0.05 * confused + 0.07 * startle, 0.22 * confused, -0.02 * confused + 0.05 * smug + 0.07 * startle, -0.3 * smug],
      curve: lerp(1, 0.3, confused),
      smileW: 1 + 0.5 * laugh + 0.15 * smug,
      open: Math.max(startle * 0.9, talking * 0.55, laugh * (0.5 + 0.4 * Math.abs(Math.sin(t * 22)))),
    });
    quiff.rotation.x = -0.55 * wind;
    quiff.scale.set(1 + 0.1 * wind, 1 - 0.45 * wind, 1 + 0.6 * wind);
    quiff.position.z = 0.16 - 0.14 * wind;
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR);
    kulhad.position.copy(hR).add(new THREE.Vector3(-0.02, 0.08, 0.04));
    kulhad.rotation.x = -0.8 * clamp01(sip);
    const kp = kulhad.position;
    steam.forEach((s, i) => {
      const p = (((ti / 1.5 + i / 3) % 1) + 1) % 1;
      s.position.set(kp.x + 0.04 * Math.sin(TAU * (p + i * 0.3)) - 0.9 * wind * p, kp.y + 0.18 + 0.55 * p, kp.z + 0.1 * p - 0.6 * wind * p);
      s.scale.set((0.5 + 1.1 * p) * (1 + 1.2 * wind), 0.5 + 1.1 * p, 0.5 + 1.1 * p);
      s.material.opacity = host.hideSteam ? 0 : 0.5 * Math.sin(Math.PI * p) * (1 - 0.7 * clamp01(sip));
    });
    return { handL: hL };
  }
  return { group: g, fig, pose, kulhad2 };
}

// ---------------------------------------------------------------- the cop: khaki, pot belly, moustache, beacon cap, radar gun
function makeCop() {
  const skin = clay("#C98B5E");
  const shirt = clay("#C9A66B");
  const shirtDeep = clay("#B08D57");
  const trousers = clay("#9C7A45");
  const leather = clay("#5A3A22", { roughness: 0.5 });
  const gold = new THREE.MeshPhysicalMaterial({ color: "#E0B040", roughness: 0.3, metalness: 0.8 });
  const black = clay("#1D1D22", { roughness: 0.4 });
  const hairDark = clay("#2B1A10");
  const g = new THREE.Group();
  const fig = new THREE.Group();
  for (const sx of [-1, 1]) {
    fig.add(capsuleBetween(new THREE.Vector3(0.2 * sx, 1.2, 0), new THREE.Vector3(0.2 * sx, 0.24, 0.02), 0.155, trousers));
    const shoe = new THREE.Mesh(new RoundedBoxGeometry(0.25, 0.15, 0.42, 4, 0.06), black);
    shoe.position.set(0.2 * sx, 0.07, 0.09);
    fig.add(shoe);
  }
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.43, 0.43, 0.12, 32), leather);
  belt.position.y = 1.3;
  belt.scale.z = 0.88;
  const buckle = new THREE.Mesh(new RoundedBoxGeometry(0.14, 0.1, 0.04, 3, 0.015), gold);
  buckle.position.set(0, 1.3, 0.39);
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.4, 0.5, 10, 28), shirt);
  torso.position.set(0, 1.78, 0);
  torso.scale.set(1.12, 1, 0.95);
  const belly = new THREE.Mesh(new THREE.SphereGeometry(0.37, 28, 20), shirt);
  belly.position.set(0, 1.52, 0.17);
  const badge = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.02, 16), gold);
  badge.rotation.x = Math.PI / 2;
  badge.position.set(-0.2, 2.0, 0.37);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.14, 0.2, 16), skin);
  neck.position.set(0, 2.3, 0);
  fig.add(belt, buckle, torso, belly, badge, neck);
  for (const sx of [-1, 1]) {
    const ep = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.05, 0.15, 2, 0.02), shirtDeep);
    ep.position.set(0.38 * sx, 2.22, 0);
    const pk = new THREE.Mesh(new RoundedBoxGeometry(0.15, 0.13, 0.04, 2, 0.015), shirtDeep);
    pk.position.set(0.18 * sx, 1.93, 0.36);
    fig.add(ep, pk);
  }

  const face = makeFace(skin, { browMat: hairDark, browR: 0.028, browLen: 0.13, noseR: 0.055 });
  const head = face.head;
  head.position.set(0, 2.82, 0);
  // a proud moustache: two curling halves
  const stache = new THREE.Group();
  stache.position.set(0, -0.14, 0.45);
  const halves = [];
  for (const sx of [-1, 1]) {
    const half = new THREE.Group();
    half.add(capsuleBetween(new THREE.Vector3(0.01 * sx, 0, 0), new THREE.Vector3(0.15 * sx, -0.02, -0.03), 0.04, hairDark));
    const curl = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 10), hairDark);
    curl.position.set(0.17 * sx, 0.03, -0.04);
    half.add(curl);
    stache.add(half);
    halves.push(half);
  }
  head.add(stache);
  // cap with a red band, black visor, gold badge and a beacon on top
  const cap = new THREE.Group();
  cap.position.set(0, 0.36, -0.02);
  const crownM = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.5, 0.26, 36), clay("#B8955A"));
  crownM.position.y = 0.1;
  const bandM = new THREE.Mesh(new THREE.CylinderGeometry(0.505, 0.505, 0.09, 36), clay("#C62828"));
  bandM.position.y = 0.0;
  const visor = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.03, 24, 1, false, -Math.PI / 2, Math.PI), black);
  visor.position.set(0, -0.04, 0.36);
  visor.scale.set(1.35, 1, 1.0);
  visor.rotation.x = 0.18;
  const capBadge = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 16), gold);
  capBadge.rotation.x = Math.PI / 2 - 0.1;
  capBadge.position.set(0, 0.1, 0.48);
  cap.add(crownM, bandM, visor, capBadge);
  const red = new THREE.MeshBasicMaterial({ color: "#FF2D3D", toneMapped: false });
  const blue = new THREE.MeshBasicMaterial({ color: "#2D7BFF", toneMapped: false });
  const bR = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12, 0, TAU, 0, Math.PI / 2), red);
  bR.position.set(-0.07, 0.23, 0);
  const bB = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12, 0, TAU, 0, Math.PI / 2), blue);
  bB.position.set(0.07, 0.23, 0);
  const lightR = new THREE.PointLight("#FF2D3D", 0, 6, 2);
  lightR.position.set(-0.3, 0.5, 0.4);
  const lightB = new THREE.PointLight("#2D7BFF", 0, 6, 2);
  lightB.position.set(0.3, 0.5, 0.4);
  cap.add(bR, bB, lightR, lightB);
  head.add(cap);
  const sweat = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 12), new THREE.MeshPhysicalMaterial({ color: "#8FD3FF", roughness: 0.1, clearcoat: 1, transparent: true, opacity: 0.9 }));
  sweat.scale.set(0.8, 1.3, 0.8);
  head.add(sweat);
  fig.add(head);

  // radar speed gun: body, nose, red lens, grip, rear screen with a live readout
  const gun = new THREE.Group();
  const gunMat = clay("#30343B", { roughness: 0.45 });
  const gBody = new THREE.Mesh(new RoundedBoxGeometry(0.17, 0.15, 0.4, 4, 0.04), gunMat);
  const gNose = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.14, 24), clay("#4A505A"));
  gNose.rotation.x = Math.PI / 2;
  gNose.position.z = 0.26;
  const lens = new THREE.Mesh(new THREE.CircleGeometry(0.07, 24), new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false }));
  lens.position.z = 0.335;
  const grip = new THREE.Mesh(new RoundedBoxGeometry(0.09, 0.22, 0.11, 3, 0.03), gunMat);
  grip.position.set(0, -0.15, -0.08);
  grip.rotation.x = 0.3;
  const stripe = new THREE.Mesh(new RoundedBoxGeometry(0.175, 0.03, 0.2, 2, 0.01), clay("#FFC21A"));
  stripe.position.set(0, 0.06, 0.05);
  const scrCanvas = document.createElement("canvas");
  scrCanvas.width = 512;
  scrCanvas.height = 192;
  const scrTex = new THREE.CanvasTexture(scrCanvas);
  scrTex.colorSpace = THREE.SRGBColorSpace;
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.15, 0.056), new THREE.MeshBasicMaterial({ map: scrTex, toneMapped: false }));
  screen.position.set(0, 0.02, -0.202);
  screen.rotation.y = Math.PI;
  gun.add(gBody, gNose, lens, grip, stripe, screen);
  fig.add(gun);
  const beam = new THREE.Mesh(
    new THREE.CylinderGeometry(0.035, 0.06, 1, 12, 1, true),
    new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }),
  );
  beam.geometry.translate(0, 0.5, 0);
  beam.geometry.rotateX(Math.PI / 2); // grows along +z from the lens
  beam.position.z = 0.34;
  gun.add(beam);
  const kulhadSlot = new THREE.Group(); // the kulhad lands here once he takes it
  fig.add(kulhadSlot);
  const setArms = makeArms(fig, shirt, shirtDeep, skin, (sx) => new THREE.Vector3(0.44 * sx, 2.1, 0));
  g.add(fig);
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.4), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false, toneMapped: false }));
  sh.rotation.x = -Math.PI / 2;
  sh.position.y = 0.01;
  g.add(sh);

  let lastScreen = "";
  function drawScreen(text, on) {
    const key = text + on;
    if (key === lastScreen) return;
    lastScreen = key;
    const c = scrCanvas.getContext("2d");
    c.fillStyle = "#0E1A12";
    c.fillRect(0, 0, 512, 192);
    if (on) {
      c.fillStyle = "#62FF8E";
      c.font = `bold ${Math.min(116, Math.floor(470 / (0.6 * text.length)))}px monospace`;
      c.textAlign = "center";
      c.textBaseline = "middle";
      c.fillText(text, 256, 100);
    }
    scrTex.needsUpdate = true;
  }

  // ---- acting (cop-local positions; he faces +z, the guy sits to his front left)
  const AIM = [0.3, 2.15, 0.72], UP = [0.34, 2.8, 0.42], BLOW = [0.5, 2.75, 0.32], LOW = [0.4, 1.55, 0.32];
  const HIP = [-0.5, 1.42, 0.12], STOP = [-0.42, 2.4, 0.62], TAKE = [-0.32, 1.98, 0.86], HOLD = [-0.22, 1.86, 0.62], SIP = [-0.06, 2.62, 0.55];
  const HAND_R = [[0, AIM], [30.4, AIM], [30.6, BLOW, "back"], [31.2, BLOW], [31.5, AIM], [37.3, AIM], [37.8, LOW], [40.45, LOW],
    [40.7, AIM, "back"], [51.9, AIM], [52.15, UP, "back"], [56.0, UP], [56.5, AIM]];
  const HAND_L = [[0, HIP], [0.95, HIP], [1.1, STOP, "back"], [2.6, STOP], [2.9, HIP], [38.4, HIP], [38.65, TAKE, "back"], [38.75, TAKE],
    [38.9, HOLD], [39.05, SIP], [39.7, SIP], [40.0, HOLD], [44.0, HOLD], [44.2, STOP, "back"], [45.1, STOP], [45.4, HOLD], [55.9, HOLD], [56.6, HIP]];
  const LID = [[0, -0.75], [16.85, -0.75], [16.95, -0.15], [17.6, -0.15], [29.25, -0.3], [33.0, -0.3], [33.05, -1.8, "snap"], [37.3, -1.8],
    [37.6, 0.35], [38.3, 0.35], [38.5, -0.9], [39.0, -0.9], [39.1, 1.1], [39.7, 1.1], [40.0, 0.05], [40.5, -0.75], [57.2, -0.75]];
  function pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal) {
    const breathe = Math.sin(TAU * ti / 1.7);
    const shout = Math.sin(Math.PI * seg(t, 1.0, 1.7)) * (t < 1.7 ? 1 : 0);
    const puzzled = smooth(16.85, 17.0, t) * (1 - smooth(17.5, 17.7, t));
    const smug = smooth(29.3, 29.5, t) * (1 - smooth(31.2, 31.4, t)) + smooth(50.6, 50.8, t) * (1 - smooth(54.4, 54.6, t));
    const shock = smooth(33.0, 33.1, t) * (1 - smooth(37.3, 37.5, t));
    const sad = smooth(37.3, 37.6, t) * (1 - smooth(38.2, 38.45, t));
    const sheepish = smooth(38.3, 38.5, t) * (1 - smooth(40.35, 40.55, t));
    const sip = smooth(39.0, 39.1, t) * (1 - smooth(39.7, 39.9, t));
    const toCam = smooth(40.45, 40.8, t) * (1 - smooth(47.75, 48.05, t));
    const stern = 1 - Math.max(smug, shock, sad, sheepish, puzzled);
    fig.position.y = 0.015 * breathe - 0.08 * sad + 0.08 * shout;
    fig.rotation.x = 0.1 * shout - 0.04 * sad;
    fig.rotation.y = 0.45 * toCam; // turns from the guy to the viewer
    torso.scale.set(1.12 * (1 + 0.02 * breathe), 1 - 0.02 * breathe - 0.05 * sad, 0.95);
    belly.scale.setScalar(1 + 0.03 * breathe);
    head.rotation.x = -0.03 + 0.28 * sad - 0.1 * shock - 0.15 * sip;
    head.rotation.z = 0.04 * Math.sin(TAU * ti / 3.4) + 0.1 * smug + 0.16 * puzzled;
    head.rotation.y = lerp(lerp(-0.25, 0, Math.max(shock, sad)), 0.1, toCam) + 0.05 * Math.sin(TAU * ti / 5);
    const talking = within(t, TALK.cop) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.5 * shock + 0.15 * puzzled,
      // stern: brows in a V; shock: high; sad: inner ends up; puzzled: one up, one down
      brows: [-0.02 * stern + 0.09 * shock + 0.02 * sad + 0.07 * puzzled, -0.3 * stern + 0.25 * sad + 0.2 * puzzled,
        -0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * smug - 0.02 * puzzled, 0.3 * stern - 0.25 * sad - 0.2 * smug + 0.1 * puzzled],
      curve: lerp(lerp(-0.6, 1, Math.max(smug, sheepish)), -1, sad),
      smileW: 1 + 0.2 * smug,
      open: Math.max(talking * 0.6, shock * 0.35 * (1 - talking)),
    });
    halves.forEach((h, i) => (h.rotation.z = (i ? 1 : -1) * (0.15 * stern + 0.25 * smug - 0.45 * sad)));
    if (host.copShout) {
      face.smile.scale.set(0.001, 0.001, 1);
      face.mouthO.position.y = -0.25;
      face.mouthO.scale.set(1.7, 1.9, 0.55);
    } else face.mouthO.position.y = -0.21;
    cap.rotation.z = 0.22 * sad + 0.08 * sheepish;
    cap.position.y = 0.36 - 0.03 * sad;
    // beacon: urgent while he is on duty (the stop, "jail", the subscribe challan, the loop back), dies with the trombone
    const onDuty = t < 6.2 || (t >= 29.25 && t < 31.3) || (t >= 40.45 && t < 47.8) || t >= 56.3;
    const fast = Math.sin(TAU * 3.2 * t) > 0 ? 1 : 0;
    const lazy = t > 38.4 ? 0.35 + 0.35 * Math.sin(TAU * 0.6 * t) : 0;
    const r = onDuty ? fast : lazy, b = onDuty ? 1 - fast : lazy * 0.8;
    bR.material.color.set("#FF2D3D").multiplyScalar(0.35 + 0.65 * r);
    bB.material.color.set("#2D7BFF").multiplyScalar(0.35 + 0.65 * b);
    lightR.intensity = 9 * r;
    lightB.intensity = 9 * b;
    const sw = seg(t, 33.5, 37.3);
    sweat.visible = t > 33.4 && t < 37.4;
    sweat.position.set(0.36, 0.18 - 0.3 * sw, 0.28);
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR, 0.24);
    gun.position.copy(hR).add(new THREE.Vector3(0, 0.08, 0.04));
    const sky = moonLocal.clone();
    const barrelUp = hR.clone().add(new THREE.Vector3(0, 2, 0.4));
    const down = hR.clone().add(new THREE.Vector3(0.1, -1.2, 1.2));
    const go = (a, b, t0, d = 0.25) => a.clone().lerp(b, outBack(seg(t, t0, t0 + d), 1.2));
    let target = guyHeadLocal.clone();
    if (t >= 30.45 && t < 31.45) target = go(guyHeadLocal, barrelUp, 30.45, 0.2);
    else if (t >= 37.3 && t < 40.45) target = go(guyHeadLocal, down, 37.3, 0.5);
    else if (t >= 40.45 && t < 51.95) target = go(down, camLocal, 40.45, 0.3);
    else if (t >= 51.95 && t < 56.4) target = go(camLocal, sky, 51.95, 0.3);
    else if (t >= 56.4) target = go(sky, guyHeadLocal, 56.4, 0.3);
    fig.updateMatrixWorld(true);
    gun.lookAt(fig.localToWorld(target.clone()));
    // the beam: fires at the Moon rising on "चाँद की FIR"
    const bl = seg(t, T_BEAM, T_BEAM + 0.3);
    beam.visible = t >= T_BEAM && t < T_BEAM_OFF;
    beam.scale.set(1, 1, 0.01 + 30 * outExpo(bl));
    beam.material.opacity = 0.9;
    // screen readout: the radar gun is in weight mode this episode
    if (host.gunScreen) drawScreen(host.gunScreen, true);
    else if (t < 2.78 || t >= 56.4) drawScreen("KG?", Math.floor(t * 3) % 2 === 0);
    else if (t < 3.66) drawScreen(Math.round(168 * seg(t, 2.78, 3.66)) + " KG", true);
    else if (t >= 40.45 && t < 51.95) drawScreen(t < 43.9 ? "COMMENT" : "SUBSCRIBE?", Math.floor(t * 3) % 2 === 0 || t < 43.9);
    else if (t >= 51.95) drawScreen("FIR!", true);
    else drawScreen("168 KG", true);
    return { handL: hL };
  }
  return { group: g, fig, pose, kulhadSlot, head };
}

// ---------------------------------------------------------------- the duo on their tiny planet
function makeDuo({ ground = true } = {}) {
  const duo = new THREE.Group();
  let cap = null;
  if (ground) {
    const capGeo = paintLowPoly(new THREE.IcosahedronGeometry(GROUND_R, 14), (m) => {
      const ang = Math.acos(Math.min(1, m.y));
      const wobble = 0.08 * Math.sin(m.x * 9 + 1.1) + 0.06 * Math.cos(m.z * 11 - 0.7);
      if (ang < 0.62 + wobble) return Math.sin(m.x * 14) * Math.cos(m.z * 12) > 0.55 && ang > 0.38 ? "sand" : "land";
      if (Math.hypot(m.x + 0.55, m.z + 0.62) < 0.2 + wobble) return "land";
      if (Math.hypot(m.x - 0.7, m.z + 0.35) < 0.14 + wobble) return "sand";
      if (Math.hypot(m.x - 0.2, m.z - 0.75) < 0.16 + wobble) return "land";
      return "ocean";
    });
    cap = new THREE.Mesh(capGeo, earthMaterial());
    cap.material.specularIntensity = 0.3;
    cap.material.clearcoat = 0.1;
    cap.material.color.setScalar(0.78);
    const pivot = new THREE.Group();
    pivot.position.y = -GROUND_R;
    pivot.add(cap);
    duo.add(pivot);
  }
  const guy = makeGuy();
  guy.group.position.set(-0.75, 0, 0);
  guy.group.rotation.y = 0.4;
  const cop = makeCop();
  cop.group.position.set(1.05, -groundDrop(1.05, 0.5) + 0.01, 0.5);
  cop.group.rotation.y = -0.55;
  duo.add(guy.group, cop.group);
  const k2 = guy.kulhad2;
  duo.add(k2);
  const tmp = new THREE.Vector3();
  const camWorld = new THREE.Vector3(0.6, 2.7, 9); // roughly where the camera sits for the to-camera shots
  function pose(t, ti = t) {
    duo.updateMatrixWorld(true);
    const guyHead = guy.group.localToWorld(new THREE.Vector3(0, 2.62, 0));
    const guyHeadLocal = cop.fig.worldToLocal(guyHead.clone());
    const selfHeadLocal = new THREE.Vector3(0, 2.82, 0);
    const camLocal = cop.fig.worldToLocal(duo.localToWorld(camWorld.clone()));
    const moonLocal = cop.fig.worldToLocal(duo.localToWorld(new THREE.Vector3(1.1, 4.7, -5)));
    const g = guy.pose(t, ti);
    const c = cop.pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal);
    duo.updateMatrixWorld(true);
    // kulhad #2: out of the hoodie pocket after the trombone, into the cop's hand; he keeps it till the loop
    k2.visible = t > 37.95 && t < 56.6;
    const from = guy.fig.localToWorld(g.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    const to = cop.fig.localToWorld(c.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    duo.worldToLocal(from);
    duo.worldToLocal(to);
    tmp.copy(t < 38.7 ? from : to);
    k2.position.copy(tmp);
    k2.scale.setScalar(outBack(seg(t, 37.95, 38.15), 2) * (1 - seg(t, 56.3, 56.6)));
    const copSip = smooth(39.0, 39.1, t) * (1 - smooth(39.7, 39.9, t));
    k2.rotation.set(-0.8 * (t >= 38.7 ? copSip : 0), t >= 38.7 ? -0.55 : 0.4, 0);
    if (cap) cap.rotation.x = -0.012 * t - 0.25 * inOutSine(seg(t, T_END, T_END + 1.7)) * (1 - inOutSine(seg(t, 40.4, 40.6)));
  }
  return { group: duo, pose };
}

// ---------------------------------------------------------------- worlds
const chairWorld = new THREE.Group();
const duo = makeDuo();
chairWorld.add(duo.group);
scene.add(chairWorld);

const earthWorld = new THREE.Group();
const earthTilt = new THREE.Group();
earthTilt.rotation.z = 0.41;
const earthSpin = new THREE.Group();
const earth = makeEarth(1.6);
earthSpin.add(earth);
// the same two, tiny, standing on the equator in Africa
const tinyDuo = makeDuo({ ground: false });
tinyDuo.group.scale.setScalar(0.09);
tinyDuo.group.position.set(0, 0, 1.6);
tinyDuo.group.rotation.x = Math.PI / 2;
earthSpin.add(tinyDuo.group);
earthTilt.add(earthSpin);
earthWorld.add(earthTilt);
const clouds = [];
const cloudMat = glossy("#FFFFFF", { roughness: 0.5, clearcoat: 0.4, flatShading: true });
for (let i = 0; i < 8; i++) {
  const cl = new THREE.Mesh(new THREE.IcosahedronGeometry(0.17 + 0.05 * (i % 3), 0), cloudMat);
  cl.scale.set(1.5, 0.6, 1);
  clouds.push(cl);
  earthWorld.add(cl);
}
scene.add(earthWorld);

// ---- Challan #2 worlds: the Moon (grey, cratered, the tiny duo standing on it) and Jupiter (banded, Great Red Spot)
Object.assign(EARTH_COLORS, {
  moonHi: "#B4B8C6", moonMid: "#8E93A4", moonMare: "#5E6376", crater: "#727789",
  jA: "#EBCB9E", jB: "#C4834E", jC: "#A85F33", jD: "#7E3F22", jE: "#D89A62", spot: "#B02E1A",
});
const rndC = mulberry32(5);
const CRATERS = Array.from({ length: 26 }, () => {
  const u = rndC() * 2 - 1, th = rndC() * TAU, s = Math.sqrt(1 - u * u);
  return { d: new THREE.Vector3(s * Math.cos(th), u, s * Math.sin(th)), r: 0.08 + 0.17 * rndC() };
});
function moonKind(m) {
  for (const c of CRATERS) {
    const a = m.angleTo(c.d);
    if (a < c.r * 0.55) return "crater";
    if (a < c.r) return "moonHi";
  }
  const n = landNoise(m.clone().multiplyScalar(1.6));
  return n > 0.9 ? "moonMare" : n > -0.2 ? "moonMid" : "moonHi";
}
function jupiterKind(m) {
  if (m.distanceTo(new THREE.Vector3(0.35, -0.3, 0.89).normalize()) < 0.24) return "spot";
  const lon = Math.atan2(m.z, m.x);
  const b = m.y * 5.2 + 0.18 * Math.sin(lon * 3 + m.y * 4);
  const k = ((Math.floor(b) % 5) + 5) % 5;
  return ["jA", "jC", "jE", "jD", "jB"][k];
}
function makeBody(radius, detail, kindOf) {
  const m = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(radius, detail), kindOf), earthMaterial());
  m.material.clearcoat = 0.1;
  return m;
}
const moonWorld = new THREE.Group();
const moonSpin = new THREE.Group();
moonSpin.add(makeBody(1.6, 10, moonKind));
const moonDuo = makeDuo({ ground: false });
moonDuo.group.scale.setScalar(0.11);
moonDuo.group.position.set(0, 1.6, 0);
moonSpin.add(moonDuo.group);
moonWorld.add(moonSpin);
scene.add(moonWorld);

const jupWorld = new THREE.Group();
const jupSpin = new THREE.Group();
jupSpin.rotation.z = 0.05;
jupSpin.add(makeBody(2.3, 16, jupiterKind));
const jupDuo = makeDuo({ ground: false });
jupDuo.group.scale.setScalar(0.1);
jupDuo.group.position.set(0, 2.3, 0);
jupSpin.add(jupDuo.group);
jupWorld.add(jupSpin);
scene.add(jupWorld);

// the Moon rising behind the home planet for the teaser ("अगला challan... चाँद की FIR")
const skyMoon = makeBody(0.9, 6, moonKind);
chairWorld.add(skyMoon);

// Orbit: glowing Sun, magenta orbit line, small Earth with a trail
const orbitWorld = new THREE.Group();
const sunGeo = new THREE.IcosahedronGeometry(1.15, 3);
{
  const p = sunGeo.attributes.position;
  const cs = new Float32Array(p.count * 3);
  const gold = col("#FFB703"), orange = col("#FB5607");
  const v = new THREE.Vector3();
  for (let i = 0; i < p.count; i += 3) {
    v.fromBufferAttribute(p, i).normalize();
    const k = gold.clone().lerp(orange, clamp01(0.5 + 0.5 * landNoise(v.multiplyScalar(1.7))));
    for (let j = 0; j < 3; j++) cs.set([k.r, k.g, k.b], (i + j) * 3);
  }
  sunGeo.setAttribute("color", new THREE.BufferAttribute(cs, 3));
}
const sun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
orbitWorld.add(sun);
const haloMat = (inner, outer) =>
  new THREE.SpriteMaterial({ map: softDiscTexture(inner, outer), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
const halo1 = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
const halo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.45)", "rgba(251,86,7,0)"));
orbitWorld.add(halo1, halo2);
const sunLight = new THREE.PointLight(0xffc46b, 60, 0, 2);
orbitWorld.add(sunLight);
const ORBIT_R = 4.4;
const orbitLine = new THREE.Mesh(
  new THREE.TorusGeometry(ORBIT_R, 0.03, 8, 200),
  new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false }),
);
orbitLine.rotation.x = Math.PI / 2;
orbitWorld.add(orbitLine);
const miniEarth = makeEarth(0.36);
orbitWorld.add(miniEarth);
const TRAIL = 26;
const trail = new THREE.InstancedMesh(
  new THREE.SphereGeometry(0.11, 12, 8),
  new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false, transparent: true, opacity: 0.85 }),
  TRAIL,
);
orbitWorld.add(trail);
scene.add(orbitWorld);

// Background stars shared by orbit and galaxy (500 points)
const rndS = mulberry32(7);
const STAR_N = 500;
const starPos = new Float32Array(STAR_N * 3);
const starCol = new Float32Array(STAR_N * 3);
for (let i = 0; i < STAR_N; i++) {
  const u = rndS() * 2 - 1, th = rndS() * TAU, r = 40 + rndS() * 30;
  const s = Math.sqrt(1 - u * u);
  starPos.set([r * s * Math.cos(th), r * u, r * s * Math.sin(th)], i * 3);
  const c = rndS() < 0.5 ? col("#FF4D9E") : col("#4CC9F0");
  c.lerp(col("#ffffff"), 0.6);
  starCol.set([c.r, c.g, c.b], i * 3);
}

// Points shader: soft round sprites; positions optionally rotated by a per-point angular speed
function makePointsMaterial(spin) {
  return new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uScale: { value: K }, uAlpha: { value: 1 } },
    vertexShader: `
      attribute float aSize;
      attribute float aR;
      attribute float aA;
      attribute float aW;
      uniform float uTime;
      uniform float uScale;
      varying vec3 vColor;
      void main() {
        vColor = color;
        vec3 p = position;
        ${spin ? "float a = aA + aW * uTime; p = vec3(cos(a) * aR, position.y, sin(a) * aR);" : ""}
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_PointSize = aSize * uScale * (40.0 / max(0.1, -mv.z));
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform float uAlpha;
      varying vec3 vColor;
      void main() {
        float d = length(gl_PointCoord - 0.5);
        float a = smoothstep(0.5, 0.0, d);
        gl_FragColor = vec4(vColor * a * a * uAlpha, a * uAlpha);
      }`,
    vertexColors: true,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
}
const starGeo = new THREE.BufferGeometry();
starGeo.setAttribute("position", new THREE.BufferAttribute(starPos, 3));
starGeo.setAttribute("color", new THREE.BufferAttribute(starCol, 3));
starGeo.setAttribute("aSize", new THREE.BufferAttribute(new Float32Array(STAR_N).map(() => 18 + rndS() * 30), 1));
const stars = new THREE.Points(starGeo, makePointsMaterial(false));
scene.add(stars);

// Galaxy: a grand-design spiral, 4,200 particles (with the 500 stars: 4,700 total):
// a bright bulge, two bright major arms, two fainter minor arms and a faint disc
const galaxyWorld = new THREE.Group();
const rndG = mulberry32(42);
const GAL_N = 4200;
const gPos = new Float32Array(GAL_N * 3), gCol = new Float32Array(GAL_N * 3);
const gSize = new Float32Array(GAL_N), gR = new Float32Array(GAL_N), gA = new Float32Array(GAL_N), gW = new Float32Array(GAL_N);
const pink = col("#FF4D9E"), teal = col("#4CC9F0"), coreC = col("#FFE9D6");
const omega = (r) => 0.9 / (0.6 + r * 0.55);
const GAL_EDGE = 7;
const WIND = 3.1; // log-spiral winding, about an 18 degree pitch
for (let i = 0; i < GAL_N; i++) {
  let r, a, y, c, size;
  if (i < 650) {
    // bulge
    r = Math.abs(gauss(rndG)) * 0.6;
    a = rndG() * TAU;
    y = gauss(rndG) * 0.32 * Math.exp(-r);
    c = coreC.clone().lerp(pink, rndG() * 0.25);
    size = 9 + rndG() * 14;
  } else if (i < 3750) {
    const major = i < 3050;
    const arm = major ? (i % 2) * Math.PI : Math.PI / 2 + (i % 2) * Math.PI;
    r = 0.7 + (GAL_EDGE - 0.7) * Math.pow(rndG(), major ? 1.05 : 0.9);
    const spread = (major ? 0.09 : 0.15) + 0.012 * r;
    a = arm + WIND * Math.log(r / 0.7) + gauss(rndG) * spread;
    r += gauss(rndG) * 0.08 * (0.5 + r / GAL_EDGE);
    y = gauss(rndG) * 0.07;
    c = (rndG() < 0.58 ? pink : teal).clone().lerp(coreC, Math.max(0, 0.55 - r * 0.11));
    if (!major) c.multiplyScalar(0.62);
    size = major ? 8 + rndG() * 16 : 6 + rndG() * 9;
  } else {
    // faint disc between the arms
    r = 0.8 + (GAL_EDGE + 0.6) * Math.sqrt(rndG());
    a = rndG() * TAU;
    y = gauss(rndG) * 0.08;
    c = pink.clone().lerp(teal, rndG()).multiplyScalar(0.18);
    size = 4 + rndG() * 5;
  }
  gR[i] = r;
  gA[i] = a;
  gW[i] = omega(r);
  gPos.set([Math.cos(a) * r, y, Math.sin(a) * r], i * 3);
  gCol.set([c.r, c.g, c.b], i * 3);
  gSize[i] = size;
}
const galGeo = new THREE.BufferGeometry();
galGeo.setAttribute("position", new THREE.BufferAttribute(gPos, 3));
galGeo.setAttribute("color", new THREE.BufferAttribute(gCol, 3));
galGeo.setAttribute("aSize", new THREE.BufferAttribute(gSize, 1));
galGeo.setAttribute("aR", new THREE.BufferAttribute(gR, 1));
galGeo.setAttribute("aA", new THREE.BufferAttribute(gA, 1));
galGeo.setAttribute("aW", new THREE.BufferAttribute(gW, 1));
const galMat = makePointsMaterial(true);
const galaxy = new THREE.Points(galGeo, galMat);
galaxy.frustumCulled = false;
galaxyWorld.add(galaxy);
const coreGlow = new THREE.Sprite(haloMat("rgba(255,233,214,0.4)", "rgba(255,77,158,0)"));
coreGlow.scale.setScalar(3.0);
galaxyWorld.add(coreGlow);
// the Sun: a small glowing yellow dot halfway out, on a thin ring that traces its path around the centre
const SUN_R = GAL_EDGE / 2, SUN_A = 2.2;
const sunDot = new THREE.Sprite(haloMat("rgba(255,236,120,1)", "rgba(255,200,0,0)"));
const sunCore = new THREE.Sprite(haloMat("rgba(255,255,235,1)", "rgba(255,230,90,0)"));
galaxyWorld.add(sunDot, sunCore);
const sunRing = new THREE.Mesh(
  new THREE.TorusGeometry(SUN_R, 0.022, 6, 256),
  new THREE.MeshBasicMaterial({ color: "#FFD23F", toneMapped: false, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false }),
);
sunRing.rotation.x = Math.PI / 2;
galaxyWorld.add(sunRing);
scene.add(galaxyWorld);


// ---------------------------------------------------------------- camera
const WORLDS = VERTICAL
  ? {
      moon: { dir: [0, 0.32, 1], dist: 8.6, shift: [0, 0.75] },
      jupiter: { dir: [0, 0.28, 1], dist: 12.2, shift: [0, 1.0] },
    }
  : {
      moon: { dir: [0, 0.32, 1], dist: 8.0, shift: [2.0, 0.1] },
      jupiter: { dir: [0, 0.28, 1], dist: 11, shift: [2.8, 0] },
    };
const up = new THREE.Vector3(0, 1, 0);

// chair-world shot list: [start, look-at, direction, distance]; a shot either cuts in or blends from the last one
const SHOTS_V = [
  { t: 0, look: [-0.45, 2.15, 0.2], dir: [0.3, 0.12, 1], dist: 5.6, to: { dist: 5.0 } }, // hook: the guy sipping, the gun pokes in
  { t: 1.0, look: [0.95, 2.45, 0.5], dir: [-0.4, 0.1, 1], dist: 4.8, to: { dist: 4.5 } }, // "रुको!": the cop
  { t: 2.5, blend: 0.4, look: [0.3, 2.75, 0.35], dir: [-0.15, 0.14, 1], dist: 8.2 }, // the 168 lands above the chair
  { t: 6.15, look: [0.1, 2.2, 0.25], dir: [0.06, 0.24, 1], dist: 10.2, to: { dist: 9.2 } }, // the guy explains: two-shot
  { t: 16.85, look: [1.0, 2.75, 0.5], dir: [-0.35, 0.08, 1], dist: 4.0 }, // "मतलब?"
  { t: SW.snap, look: [0.2, 2.2, 0.3], dir: [0.04, 0.22, 1], dist: 9.6 }, // back home
  { t: 29.95, blend: 0.5, look: [0.95, 2.6, 0.5], dir: [-0.4, 0.1, 1], dist: 5.0 }, // "jail!": smug cop, gunslinger blow
  { t: 31.3, look: [0.1, 2.45, 0.25], dir: [0.06, 0.2, 1], dist: 9.8 }, // the reversal: two-shot, room for the 168
  { t: 33.0, blend: 1.0, look: [1.0, 3.05, 0.5], dir: [-0.35, 0.08, 1], dist: 4.6 }, // push in on the cop's shock
  { t: 37.25, blend: 0.6, look: [1.0, 2.6, 0.5], dir: [-0.3, 0.05, 1], dist: 3.6 }, // trombone: his face
  { t: 37.95, look: [0.15, 2.1, 0.25], dir: [0.06, 0.22, 1], dist: 9.8 }, // chai together: two-shot
  { t: T_END, blend: 1.6, look: [0.15, 3.4, 0.25], dir: [0.06, 0.5, 1], dist: 12.5 }, // end card: crane up and back
  { t: 40.45, look: [1.05, 2.75, 0.75], dir: [0.12, 0.1, 1], dist: 4.4, to: { dist: 4.0 } }, // to camera: the subscribe challan
  { t: 47.8, look: [-0.55, 2.35, 0.3], dir: [-0.1, 0.1, 1], dist: 4.7 }, // the guy raises his kulhad to camera
  { t: 50.55, look: [0.15, 3.4, 0.0], dir: [0.08, 0.3, 1], dist: 12.0 }, // teaser: the Moon rises
  { t: 54.6, look: [-0.45, 2.15, 0.2], dir: [0.3, 0.12, 1], dist: 5.2, to: { dist: 5.6 } }, // back to the hook frame: the loop
];
const SHOTS_H = SHOTS_V.map((s) => ({ ...s, dist: s.dist * 0.62, to: s.to ? { dist: s.to.dist * 0.62 } : undefined }));
const SHOTS = VERTICAL ? SHOTS_V : SHOTS_H;

function shotAt(t) {
  let i = 0;
  while (i + 1 < SHOTS.length && t >= SHOTS[i + 1].t) i++;
  const s = SHOTS[i];
  const next = SHOTS[i + 1];
  const end = next ? next.t : DUR;
  let look = V(s.look), dir = V(s.dir).normalize(), dist = s.dist;
  if (s.to) dist = lerp(s.dist, s.to.dist, inOutSine(seg(t, s.t, end)));
  if (s.blend && i > 0) {
    const p = SHOTS[i - 1];
    const x = inOutSine(seg(t, s.t, s.t + s.blend));
    const pDist = p.to ? p.to.dist : p.dist;
    look = V(p.look).lerp(look, x);
    dir = V(p.dir).normalize().lerp(dir, x).normalize();
    dist = lerp(pDist, dist, x);
  }
  return { look, dir, dist };
}

function whipLevel(t) {
  let level = 0, dir = 0;
  for (const w of WHIPS) {
    let e = 0;
    if (t >= w.c - w.b && t < w.c) e = inCubic(seg(t, w.c - w.b, w.c));
    else if (t >= w.c && t < w.c + w.a) e = 1 - outExpo(seg(t, w.c, w.c + w.a));
    if (e * w.k > level) {
      level = e * w.k;
      dir = w.dir;
    }
  }
  return { level, dir };
}

function worldAt(t) {
  if (t < SW.moon) return "chair";
  if (t < SW.jupiter) return "moon";
  if (t < SW.snap) return "jupiter";
  return "chair";
}

// distance multiplier for the space worlds: arrive close, pull back with a soft overshoot, drift, rocket out on the whip
function distMul(t, name) {
  const s0 = SW[name];
  const s1 = name === "moon" ? SW.jupiter : SW.snap;
  const inn = lerp(0.32, 1, outBack(seg(t, s0, s0 + 0.6), 1.3));
  const drift = 1 + 0.03 * (t - s0);
  const out = name === "jupiter" ? lerp(1, 0.25, inCubic(seg(t, s1 - 0.09, s1))) : 1 + 3.2 * inCubic(seg(t, s1 - 0.2, s1));
  return inn * drift * out;
}

function placeCamera(t, name, whip) {
  let look, dir, dist;
  if (name === "chair") {
    ({ look, dir, dist } = shotAt(t));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 6));
    if (t < SW.snap) dist *= 1 + 3.2 * inCubic(seg(t, SW.moon - 0.2, SW.moon));
    else dist *= lerp(4.2, 1, outBack(seg(t, SW.snap, SW.snap + 0.55), 1.2));
  } else {
    const w = WORLDS[name];
    const m = distMul(t, name);
    dir = V(w.dir).applyAxisAngle(up, 0.06 * Math.sin(TAU * t / 7.5)).normalize();
    const right = new THREE.Vector3().crossVectors(up, dir).normalize();
    look = new THREE.Vector3().addScaledVector(right, w.shift[0] * Math.min(m, 1.6)).addScaledVector(up, w.shift[1] * Math.min(m, 1.6));
    dist = w.dist * m;
  }
  camera.position.copy(look).addScaledVector(dir, dist);
  camera.lookAt(look);
  camera.rotateZ(0.05 * whip.level * (whip.dir || 1));
  camera.fov = (VERTICAL ? 38 : 35) + 16 * whip.level;
  camera.updateProjectionMatrix();
}

// ---------------------------------------------------------------- 3D numbers (overlay scene)
const numScene = new THREE.Scene();
numScene.environment = envMap;
numScene.environmentIntensity = 1.0;
const numCam = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);
numCam.position.set(0, 0, 10);
const nKey = new THREE.DirectionalLight(0xffffff, 2.2);
nKey.position.set(-3, 4, 6);
numScene.add(nKey, new THREE.HemisphereLight(0xffffff, 0x444466, 0.5));
const faceMat = glossy("#FFFFFF", { roughness: 0.18, clearcoatRoughness: 0.04 });
const numGroup = new THREE.Group();
numScene.add(numGroup);
const numShadow = new THREE.Mesh(
  new THREE.PlaneGeometry(1, 1),
  new THREE.MeshBasicMaterial({ map: softDiscTexture("rgba(0,0,0,0.45)", "rgba(0,0,0,0)"), transparent: true, depthWrite: false, toneMapped: false }),
);
numScene.add(numShadow);
const NUM_POS = VERTICAL ? new THREE.Vector3(0, 1.78, 0) : new THREE.Vector3(1.5, 0.52, 0);
let glyphs = null;
let advance = null;
const slots = [];
const rimMats = NUMS.map((n) => glossy(n.rim, { roughness: 0.25 }));

function buildGlyphs(font) {
  glyphs = {};
  advance = {};
  for (const ch of "0123456789,+.") {
    const geo = new TextGeometry(ch, {
      font,
      size: 1,
      depth: 0.3,
      curveSegments: 8,
      bevelEnabled: true,
      bevelThickness: 0.05,
      bevelSize: 0.035,
      bevelSegments: 4,
    });
    geo.translate(0, 0, -0.15);
    glyphs[ch] = geo;
    advance[ch] = font.data.glyphs[ch].ha / font.data.resolution;
  }
  for (let i = 0; i < 9; i++) {
    const m = new THREE.Mesh(glyphs["0"], [faceMat, rimMats[0]]);
    slots.push(m);
    numGroup.add(m);
  }
}
const fmt = (v, dec = 0) => (dec ? v.toFixed(dec) : Math.round(v).toLocaleString("en-US"));
const strWidth = (s) => [...s].reduce((w, ch) => w + (ch === "," ? advance[ch] * 0.85 : advance[ch]), 0);

function renderNumber(t) {
  const n = NUMS.find((x) => t >= x.fly && t < x.out + 0.2);
  numGroup.visible = numShadow.visible = !!n;
  if (!n || !glyphs) return;
  const idx = NUMS.indexOf(n);
  // the counter races up and settles with a tiny overshoot
  const p = seg(t, n.fly, n.lock);
  const v = n.value * outBack(p, 0.45);
  const str = fmt(v, n.dec) + (n.plus && p > 0.55 ? "+" : "");
  const finalStr = fmt(n.value, n.dec) + (n.plus ? "+" : "");
  const size = Math.min(1.3, (VERTICAL ? 2.45 : 4.3) / strWidth(finalStr));
  const width = strWidth(str) * size;
  let x = -width / 2;
  slots.forEach((m, i) => {
    const ch = str[i];
    m.visible = !!ch;
    if (!ch) return;
    m.geometry = glyphs[ch];
    m.material[1] = rimMats[idx];
    m.scale.set(size, size, size);
    m.position.set(x, -0.36 * size, 0);
    x += (ch === "," ? advance[ch] * 0.85 : advance[ch]) * size;
  });
  // fly in (fast in), spin once and lock with a soft overshoot, then leave on the next whip
  const f = outExpo(seg(t, n.fly, n.land));
  const pos = (VERTICAL ? new THREE.Vector3(1.6, 3.6, -22) : new THREE.Vector3(4.5, 2.6, -22)).lerp(NUM_POS, f);
  const spin = outBack(seg(t, n.land, n.lock), 1.6);
  const leave = inCubic(seg(t, n.out, n.out + 0.2));
  pos.lerp(new THREE.Vector3(0, 0.3, -30), leave);
  numGroup.position.copy(pos);
  numGroup.rotation.set(0.25 * (1 - f), -TAU * (1 - spin) - 0.9 * (1 - f), 0);
  const punch = 1 + 0.14 * Math.exp(-14 * Math.max(0, t - n.land)) * (t >= n.land ? 1 : 0);
  numGroup.scale.setScalar(punch * (1 - 0.6 * leave));
  // soft baked shadow under the number, strongest once it lands
  numShadow.position.set(NUM_POS.x, NUM_POS.y - 0.62 * size - 0.12, -0.6);
  numShadow.scale.set((VERTICAL ? 2.8 : 4.6) * (0.6 + 0.4 * f), 0.5, 1);
  numShadow.material.opacity = 0.9 * f * (1 - leave);
}


// ---------------------------------------------------------------- speed lines
const lines = document.getElementById("w-lines");
const LW = Math.round(W * DPR), LH = Math.round(H * DPR);
lines.width = LW;
lines.height = LH;
const lctx = lines.getContext("2d");
const rndL = mulberry32(99);
const LINES = Array.from({ length: 110 }, () => ({ a: rndL() * TAU, ph: rndL(), sp: 0.8 + rndL() * 1.2, w: 1 + rndL() * 3 }));
function drawLines(t, whip) {
  lctx.clearRect(0, 0, LW, LH);
  if (whip.level < 0.02) return;
  const cx = LW / 2, cy = LH / 2, R = Math.hypot(cx, cy);
  lctx.lineCap = "round";
  for (const L of LINES) {
    // pull-back: streaks rush inward; snap-back: they burst outward
    let u = (L.ph + t * 3.2 * L.sp) % 1;
    if (whip.dir < 0) u = 1 - u;
    const r0 = R * (0.18 + 0.9 * u);
    const len = (90 + 320 * whip.level) * K * L.sp;
    const x0 = cx + Math.cos(L.a) * r0, y0 = cy + Math.sin(L.a) * r0;
    const x1 = cx + Math.cos(L.a) * (r0 + len), y1 = cy + Math.sin(L.a) * (r0 + len);
    lctx.strokeStyle = `rgba(255,255,255,${0.55 * Math.min(1, whip.level)})`;
    lctx.lineWidth = L.w * K * (0.6 + whip.level);
    lctx.beginPath();
    lctx.moveTo(x0, y0);
    lctx.lineTo(x1, y1);
    lctx.stroke();
  }
}


// ---------------------------------------------------------------- background
const BG = {
  chair: ["#FFD6A5", "#FF6B6B"],
  moon: ["#4A5275", "#141832"],
  jupiter: ["#F4B076", "#7A3418"],
};
const bgEl = document.getElementById("w-bg");
const policeEl = document.getElementById("w-police");
function bgAt(t) {
  // colours cross over inside each whip window
  const order = [[0, "chair"], [SW.moon, "moon"], [SW.jupiter, "jupiter"], [SW.snap, "chair"]];
  let from = BG.chair, to = BG.chair, x = 0;
  for (let i = 1; i < order.length; i++) {
    const [c, name] = order[i];
    const half = i === 3 ? 0.06 : 0.14;
    if (t >= c - half && t < c + half) {
      from = BG[order[i - 1][1]];
      to = BG[name];
      x = inOutSine(seg(t, c - half, c + half));
      break;
    }
    if (t >= c + half) from = to = BG[name];
  }
  const a = col(from[0]).lerp(col(to[0]), x), b = col(from[1]).lerp(col(to[1]), x);
  return [`#${a.getHexString()}`, `#${b.getHexString()}`];
}

// ---------------------------------------------------------------- render(t)
function render(t) {
  const whip = whipLevel(t);
  const name = worldAt(t);
  chairWorld.visible = name === "chair";
  earthWorld.visible = orbitWorld.visible = galaxyWorld.visible = false;
  moonWorld.visible = name === "moon";
  jupWorld.visible = name === "jupiter";
  stars.visible = name === "moon";

  if (name === "chair") duo.pose(t);
  // the Moon turns slowly under the tiny duo; Jupiter spins fast (its day is under 10 hours)
  moonSpin.rotation.set(0.35, 0.18 * (t - SW.moon) - 0.25, 0);
  if (name === "moon") moonDuo.pose(t);
  jupSpin.rotation.y = 0.45 * (t - SW.jupiter);
  if (name === "jupiter") jupDuo.pose(t);
  // the teaser's Moon climbs over the home planet's horizon
  const rise = outBack(seg(t, 50.7, 52.3), 1.1);
  skyMoon.visible = t > 50.6 && t < 54.7;
  skyMoon.position.set(1.1, lerp(-2.0, 4.7, rise), -5);
  skyMoon.rotation.y = 0.3 * t;
  stars.rotation.y = 0.03 * t;

  // background, the beacon's red/blue wash over the sky, camera, speed lines
  const [a, b] = bgAt(t);
  bgEl.style.background = VERTICAL
    ? `radial-gradient(130% 80% at 50% 42%, ${a} 0%, ${b} 80%)`
    : `radial-gradient(120% 120% at 32% 40%, ${a} 0%, ${b} 78%)`;
  const onDuty = name === "chair" && (t < 6.2 || (t >= 29.25 && t < 31.3) || (t >= 40.45 && t < 47.8) || t >= 56.3);
  const fast = Math.sin(TAU * 3.2 * t) > 0;
  policeEl.style.opacity = onDuty ? "0.55" : "0";
  policeEl.style.background = fast
    ? "radial-gradient(60% 40% at 15% 10%, rgba(255,45,61,0.75), rgba(255,45,61,0) 70%)"
    : "radial-gradient(60% 40% at 85% 10%, rgba(45,123,255,0.75), rgba(45,123,255,0) 70%)";
  placeCamera(t, name, whip);
  if (host.cameraOverride) host.cameraOverride(camera);
  drawLines(t, whip);

  renderer.clear();
  renderer.toneMappingExposure = name === "chair" ? 0.85 : 1.05;
  renderer.render(scene, camera);
  renderer.toneMappingExposure = 1.05;
  renderer.clearDepth();
  renderNumber(t);
  renderer.render(numScene, numCam);
}

host.render = render;
new FontLoader().load("assets/fonts/fredoka-700.typeface.json", (font) => {
  buildGlyphs(font);
  render(host.clock.t);
  host.ready();
});
render(host.clock.t);
