// ---------------------------------------------------------------- camera
// worlds: hero centred and a little low in 9:16 (numbers above, captions below); left of centre in 16:9
const WORLDS = VERTICAL
  ? {
      earth: { dir: [0, 0.22, 1], dist: 10.5, shift: [0, 1.0] },
      orbit: { dir: [0, 0.5, 1], dist: 25, shift: [0, 2.2] },
      galaxy: { dir: [0, 0.577, 1], dist: 30, shift: [0, 2.6] },
    }
  : {
      earth: { dir: [0, 0.22, 1], dist: 9.2, shift: [2.15, -0.1] },
      orbit: { dir: [0, 0.5, 1], dist: 17, shift: [4.6, -0.6] },
      galaxy: { dir: [0, 0.577, 1], dist: 19.5, shift: [4.6, 0] },
    };
const up = new THREE.Vector3(0, 1, 0);

// chair-world shot list: [start, look-at, direction, distance]; a shot either cuts in or blends from the last one
const SHOTS_V = [
  { t: 0, look: [-0.45, 2.15, 0.2], dir: [0.3, 0.12, 1], dist: 5.6, to: { dist: 5.0 } }, // hook: the guy, the gun pokes in
  { t: 2.16, look: [0.95, 2.45, 0.5], dir: [-0.4, 0.1, 1], dist: 4.8, to: { dist: 4.4 } }, // "रुको!": the cop
  { t: 4.35, look: [0.1, 2.2, 0.25], dir: [0.06, 0.24, 1], dist: 10.2, to: { dist: 9.4 } }, // two-shot
  { t: 8.5, blend: 0.4, look: [0.3, 2.9, 0.3], dir: [0.06, 0.05, 1], dist: 9.4 }, // tilt up with the gun
  { t: SW.snap, look: [0.2, 2.2, 0.3], dir: [0.04, 0.22, 1], dist: 9.6 }, // back home
  { t: 21.0, blend: 1.0, look: [1.0, 2.65, 0.5], dir: [-0.35, 0.08, 1], dist: 4.4 }, // push in on the cop
  { t: 24.4, blend: 2.0, look: [1.0, 2.6, 0.5], dir: [-0.3, 0.05, 1], dist: 3.6 }, // trombone: hold on his face
  { t: 26.0, look: [0.15, 2.1, 0.25], dir: [0.06, 0.22, 1], dist: 9.8 }, // laugh: two-shot
  { t: T_END, blend: 2.3, look: [0.15, 3.4, 0.25], dir: [0.06, 0.5, 1], dist: 12.5 }, // end card: crane up and back
];
const SHOTS_H = SHOTS_V.map((s) => ({ ...s, dist: s.dist * 0.62, to: s.to ? { dist: s.to.dist * 0.62 } : undefined }));
const SHOTS = VERTICAL ? SHOTS_V : SHOTS_H;

function shotAt(t) {
  let i = 0;
  while (i + 1 < SHOTS.length && t >= SHOTS[i + 1].t) i++;
  const s = SHOTS[i];
  const next = SHOTS[i + 1];
  const end = next ? next.t : 31.3;
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
  if (t < SW.earth) return "chair";
  if (t < SW.orbit) return "earth";
  if (t < SW.galaxy) return "orbit";
  if (t < SW.snap) return "galaxy";
  return "chair";
}

// distance multiplier for the space worlds: arrive close, pull back with a soft overshoot, drift, rocket out on the whip
function distMul(t, name) {
  const s0 = SW[name];
  const s1 = name === "earth" ? SW.orbit : name === "orbit" ? SW.galaxy : SW.snap;
  const inn = lerp(0.32, 1, outBack(seg(t, s0, s0 + 0.6), 1.3));
  const drift = 1 + 0.045 * (t - s0);
  const out = name === "galaxy" ? lerp(1, 0.12, inCubic(seg(t, s1 - 0.09, s1))) : 1 + 3.2 * inCubic(seg(t, s1 - 0.2, s1));
  return inn * drift * out;
}

function placeCamera(t, name, whip) {
  let look, dir, dist;
  if (name === "chair") {
    ({ look, dir, dist } = shotAt(t));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 6));
    // leave on the first whip by rocketing back; arrive on the snap from far away
    if (t < SW.snap) dist *= 1 + 3.2 * inCubic(seg(t, SW.earth - 0.2, SW.earth));
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
