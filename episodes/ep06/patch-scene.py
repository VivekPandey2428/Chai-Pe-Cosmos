"""Challan #6 "Mars pe Illegal Construction": Inspector Sahab finds a 22 km "building" on Mars; it is Olympus Mons.

Opens on Mars with the beacon wash and 22 km at frame 0 -> snap home (night, Mars red in the sky): "volcano hai!" ->
whip back to Mars: Everest pops up beside it (2.5x) -> lava piles up in one spot and the volcano grows (the crust
does not move) -> snap home: "तो इसको गिराओ!" -> Maharashtra-sized; a toy bulldozer pops up -> trombone, chai, end card
-> comment -> subscribe callout -> teaser (a late dawn Sun) -> crane up to Mars: the loop to frame 0.
Data and world JS only; see tools/cycle2_patch.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build

DUR = 40.15
SPACE = [[0, 4.82], [10.95, 19.85]]

guy = {
    "handR": [[0, "REST_R"], [4.85, "REST_R"], [5.1, "SKY_R", "back"], [7.3, "SKY_R"], [7.6, "REST_R"], [21.2, "REST_R"],
              [21.45, "TOAST_R", "back"], [24.4, "TOAST_R"], [24.7, "REST_R"], [27.8, "REST_R"], [28.0, "SIP_R"], [28.6, "SIP_R"],
              [28.9, "REST_R"], [36.7, "REST_R"], [36.95, "SKY_R", "back"], [38.4, "SKY_R"], [38.7, "REST_R"]],
    "handL": [[0, "REST_L"], [26.35, "REST_L"], [26.5, "POCKET"], [26.57, "POCKET"], [26.77, "OFFER", "back"], [27.0, "OFFER"],
              [27.25, "REST_L"]],
    "lid": [[0, -0.85], [4.9, -0.85], [5.0, 0.05], [5.6, 0.05], [5.8, -0.85], [21.1, -0.85], [21.3, 0.05], [22.0, 0.05], [22.2, -0.85],
            [26.25, -0.85], [26.3, 1.0], [26.5, 1.0], [26.6, 0.05], [27.8, 0.05], [28.0, 1.1], [28.6, 1.1], [28.9, -0.85], [DUR, -0.85]],
    "yaw": [[0, 0.55], [DUR, 0.55]],
    "mood": {"smug": [[4.9, 9.3], [36.7, 39.4]], "laugh": [[21.15, 22.0], [24.6, 26.2], [26.25, 26.6]], "sip": [[28.0, 28.6]],
             "lookUp": [[5.1, 7.4], [32.6, 36.3], [36.9, 38.5]]},
}
cop = {
    "handR": [[0, "UP"], [21.0, "UP"], [21.25, "AIM", "back"], [26.3, "AIM"], [26.7, "LOW"], [27.75, "LOW"], [28.0, "AIM", "back"],
              [32.4, "AIM"], [32.65, "UP", "back"], [DUR, "UP"]],
    "handL": [[0, "HIP"], [19.9, "HIP"], [20.05, "STOP", "back"], [20.9, "STOP"], [21.2, "HIP"], [26.85, "HIP"], [27.0, "TAKE", "back"],
              [27.1, "TAKE"], [27.25, "HOLD"], [27.35, "SIP"], [27.75, "SIP"], [27.85, "HOLD"], [39.4, "HOLD"], [39.8, "HIP"]],
    "lid": [[0, -0.75], [9.5, -0.75], [9.6, -1.6, "snap"], [10.8, -1.6], [11.0, -0.75], [25.35, -0.75], [25.45, -1.8, "snap"],
            [26.25, -1.8], [26.55, 0.35], [26.9, 0.35], [27.0, -0.9], [27.35, -0.9], [27.4, 1.1], [27.75, 1.1], [27.85, -0.75], [DUR, -0.75]],
    "aim": [[0, "mars"], [21.1, "guy"], [26.3, "down"], [27.85, "cam"], [32.5, "sun"], [36.7, "mars"]],
    "beam": [[4.85, 9.4], [19.9, 21.0], [32.8, 36.2], [38.2, 99]],
    "screen": [[0, "22 KM!", 1], [9.5, "EVEREST?", 0], [19.9, "GIRAO!", 1], [22.9, "600 KM", 0], [26.25, "FAIL", 0], [27.85, "COMMENT", 0],
               [31.75, "SUBSCRIBE?", 1], [32.5, "LATE!", 1], [36.7, "22 KM!", 1]],
    "duty": [[0, 4.85], [19.9, 21.1], [27.85, 32.6], [38.2, 99]],
    "lazyFrom": 27.0,
    "sweat": [25.5, 26.3],
    "mood": {"shout": [19.95], "shock": [[9.55, 10.8], [25.4, 26.25]], "sad": [[26.25, 26.9]], "sheepish": [[26.9, 27.85]],
             "sip": [[27.35, 27.75]], "toCam": [[27.85, 32.5]], "lookSky": [[4.85, 9.4], [32.5, 36.3], [38.2, 99]]},
}
act = {"guy": guy, "cop": cop, "k2": {"pop": 26.45, "give": 27.05, "sipA": 27.35, "sipB": 27.75, "end": 39.4}, "alt": [[32.6, 36.4]]}

nums = [
    {"value": 22, "fly": 1.25, "land": 1.58, "lock": 2.4, "out": 4.5, "rim": "#FB5607"},  # "बाईस किलोमीटर"
    {"value": 2.5, "dec": 1, "fly": 11.5, "land": 11.88, "lock": 12.6, "out": 13.2, "rim": "#4CC9F0"},  # "ढाई गुना"
]

CU_COP = {"look": [1.0, 2.75, 0.5], "dir": [-0.35, 0.08, 1]}
CU_GUY = {"look": [-0.45, 2.3, 0.2], "dir": [0.3, 0.1, 1]}
shots = [
    {"t": 0, **CU_GUY, "dist": 5.0},  # (in space until 4.82)
    {"t": 4.82, **CU_GUY, "dist": 5.0, "to": {"dist": 4.6}},  # "Building नहीं साहब, volcano है!"
    {"t": 7.6, "blend": 0.6, "look": [0.9, 3.6, -0.5], "dir": [-0.06, -0.1, 1], "dist": 12.0},  # Mars red in the sky
    {"t": 9.45, **CU_COP, "dist": 4.6},  # "Everest से भी बड़ा?"
    {"t": 19.85, **CU_COP, "dist": 4.8},  # "तो इसको गिराओ!"
    {"t": 21.1, **CU_GUY, "dist": 5.0},  # "साहब, ये लगभग पूरे महाराष्ट्र जितना बड़ा है!"
    {"t": 23.0, "blend": 0.6, "look": [0.6, 2.0, 0.5], "dir": [0.04, 0.22, 1], "dist": 10.0},  # two-shot: the bulldozer pops up
    {"t": 25.4, "blend": 0.6, "look": [1.0, 3.0, 0.5], "dir": [-0.35, 0.08, 1], "dist": 4.6},  # it dawns on him
    {"t": 26.25, "blend": 0.4, "look": [1.0, 2.6, 0.5], "dir": [-0.3, 0.05, 1], "dist": 3.6},  # trombone
    {"t": 26.45, "look": [0.15, 2.4, 0.2], "dir": [0.06, 0.3, 1], "dist": 11.0},  # chai together, end card
    {"t": 27.85, "look": [1.05, 2.75, 0.75], "dir": [0.12, 0.1, 1], "dist": 4.4, "to": {"dist": 4.0}},  # to camera
    {"t": 32.5, "look": [-0.6, 3.2, -0.3], "dir": [0.1, 0.12, 1], "dist": 12.0},  # teaser: the Sun, late
    {"t": 36.65, **CU_GUY, "dist": 5.0},  # "साहब, permission Mars से ही ले लो..."
    {"t": 38.2, "blend": 1.2, "look": [1.9, 5.0, -6.5], "dir": [-0.15, -0.25, 1], "dist": 9.0, "to": {"dist": 4.5}},  # crane to Mars: loop
]
space_shots = [
    {"t": 0, "look": [0, 2.05, 0], "dir": [0, 0.3, 1], "dist": 4.2, "to": {"dist": 3.6}},  # hook: the "building"
    {"t": 10.95, "look": [0.6, 1.95, 0], "dir": [0, 0.12, 1], "dist": 4.4},  # Everest beside it
    {"t": 13.2, "blend": 1.0, "look": [0.3, 2.0, 0], "dir": [0, 0.3, 1], "dist": 4.0},
    {"t": 17.2, "blend": 1.2, "look": [0, 1.6, 0], "dir": [0.2, 0.35, 1], "dist": 5.5},  # the whole planet, the volcano growing
]

WORLD = r"""
// ---- Challan #6: Mars in the night sky (a late Sun for the teaser), a toy bulldozer; in space, Mars with Olympus Mons
Object.assign(EARTH_COLORS, { mRust: "#A8380C", mDust: "#C8602E", mDark: "#7A280A", mIce: "#F4FBFF", mVolc: "#C0562A", mCald: "#6E2410" });
const OLY = new THREE.Vector3(0, 1, 0), OLY_A = 0.42, OLY_H = 0.42, M_R = 2.0;
const marsKind = (m) => {
  const a = m.angleTo(OLY);
  if (a < 0.06) return "mCald";
  if (a < OLY_A) return "mVolc";
  if (Math.abs(m.z) > 0.92) return "mIce";
  const n = landNoise(m.clone().multiplyScalar(2.2));
  return n > 0.9 ? "mDark" : n > 0.0 ? "mDust" : "mRust";
};
const skyMars = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(0.45, 3), marsKind), earthMaterial());
const skyMarsGlow = new THREE.Sprite(haloMat("rgba(255,110,60,0.7)", "rgba(255,110,60,0)"));
skyMarsGlow.scale.setScalar(3.0);
const SKY_MARS = [2.0, 5.4, -7];
skyMars.position.set(...SKY_MARS);
skyMarsGlow.position.set(SKY_MARS[0], SKY_MARS[1], SKY_MARS[2] - 0.5);
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
chairWorld.add(skyMars, skyMarsGlow, skySun, skySunHalo);
// a toy bulldozer by the cop's boots
const dozer = new THREE.Group();
const yellow = glossy("#FFC300", { roughness: 0.3 }), dark = glossy("#2A2A35", { roughness: 0.5 }), glass = glossy("#8FD3FF", { roughness: 0.1 });
const dBody = new THREE.Mesh(new RoundedBoxGeometry(0.6, 0.28, 0.4, 2, 0.05), yellow);
dBody.position.y = 0.26;
const dCab = new THREE.Mesh(new RoundedBoxGeometry(0.28, 0.26, 0.34, 2, 0.04), glass);
dCab.position.set(-0.1, 0.52, 0);
const dRoof = new THREE.Mesh(new RoundedBoxGeometry(0.32, 0.05, 0.38, 2, 0.02), yellow);
dRoof.position.set(-0.1, 0.67, 0);
const dBlade = new THREE.Mesh(new RoundedBoxGeometry(0.08, 0.3, 0.56, 2, 0.02), dark);
dBlade.position.set(0.4, 0.17, 0);
dBlade.rotation.z = -0.2;
const dTrackL = new THREE.Mesh(new RoundedBoxGeometry(0.64, 0.14, 0.1, 2, 0.05), dark);
dTrackL.position.set(0, 0.08, 0.2);
const dTrackR = dTrackL.clone();
dTrackR.position.z = -0.2;
dozer.add(dBody, dCab, dRoof, dBlade, dTrackL, dTrackR);
const DOZER = [1.0, -groundDrop(1.0, 1.9) - 0.02, 1.9];
dozer.position.set(...DOZER);
dozer.rotation.y = -2.0;
chairWorld.add(dozer);
function skyAt(t) {
  const rise = outBack(seg(t, 33.6, 35.0), 1.1) * (1 - inOutSine(seg(t, 36.4, 37.0)));
  return { mars: SKY_MARS, sun: [-3.0, lerp(-1.0, 3.4, rise), -7] };
}

// space: Mars with Olympus Mons (exaggerated), Everest beside it for scale, lava piling up in one place
const epWorld = new THREE.Group();
const marsGeo = paintLowPoly(new THREE.IcosahedronGeometry(M_R, 24), marsKind);
const mPos = marsGeo.attributes.position;
const mBase = new Float32Array(mPos.array.length);
const mBump = new Float32Array(mPos.count);
{
  const v = new THREE.Vector3();
  for (let i = 0; i < mPos.count; i++) {
    v.fromBufferAttribute(mPos, i).normalize();
    mBase.set([v.x, v.y, v.z], i * 3);
    const a = v.angleTo(OLY);
    let p = a < OLY_A ? Math.cos((Math.PI / 2) * a / OLY_A) ** 1.4 : 0;
    if (a < 0.06) p -= 0.22 * (1 - a / 0.06);
    mBump[i] = p;
  }
}
let lastH = -1;
function setVolcano(h) {
  if (Math.abs(h - lastH) < 1e-4) return;
  lastH = h;
  for (let i = 0; i < mPos.count; i++) {
    const r = M_R + OLY_H * h * mBump[i];
    mPos.setXYZ(i, mBase[i * 3] * r, mBase[i * 3 + 1] * r, mBase[i * 3 + 2] * r);
  }
  mPos.needsUpdate = true;
  marsGeo.computeVertexNormals();
}
const mars = new THREE.Mesh(marsGeo, earthMaterial());
epWorld.add(mars);
// Everest at the same scale: 22 km / 2.5
const EV = OLY.clone().applyAxisAngle(new THREE.Vector3(0, 0, -1), 0.55).normalize();
const everest = new THREE.Group();
const evRock = new THREE.Mesh(new THREE.ConeGeometry(0.14, OLY_H / 2.5 + 0.02, 7), glossy("#6E7280", { flatShading: true, roughness: 0.6 }));
evRock.position.y = (OLY_H / 2.5 + 0.02) / 2 - 0.01;
const evSnow = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.07, 7), glossy("#FFFFFF", { flatShading: true }));
evSnow.position.y = OLY_H / 2.5 - 0.02;
everest.add(evRock, evSnow);
everest.position.copy(EV).multiplyScalar(M_R - 0.01);
everest.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), EV);
epWorld.add(everest);
// lava: glowing blobs well up at the summit and run down the flanks
const lavaMat = new THREE.MeshBasicMaterial({ color: "#FF7A1A", toneMapped: false });
const LAVA = Array.from({ length: 12 }, (_, i) => {
  const m = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8), lavaMat);
  epWorld.add(m);
  return { m, az: (i / 12) * TAU, ph: (i * 0.37) % 1 };
});
const lavaGlow = new THREE.Sprite(haloMat("rgba(255,120,30,0.9)", "rgba(255,80,0,0)"));
epWorld.add(lavaGlow);
const volcH = (t) => (t < 15.5 ? 1 : lerp(1, 0.3, inOutSine(seg(t, 15.5, 15.85))) + 0.7 * inOutSine(seg(t, 16.0, 19.4)));
const FOCUS = {};
const qT = new THREE.Quaternion();

function episodeRender(t, name) {
  skyMars.rotation.y = 0.1 * t;
  const sky = skyAt(t);
  skySun.position.set(...sky.sun);
  skySun.scale.setScalar(0.9);
  skySun.rotation.y = 0.4 * t;
  skySun.visible = skySunHalo.visible = t > 33.5 && t < 37.1;
  skySunHalo.position.copy(skySun.position);
  skySunHalo.scale.setScalar(4.2);
  const dawn = mood(t, ACT.alt, 0.6);
  key.intensity = name === "chair" ? lerp(2.0, 2.4, dawn) : 1.5;
  key.color.set(name === "chair" && dawn < 0.5 ? "#e8ecff" : "#fff1e0");
  // the bulldozer: pops up on "Bulldozer", sinks away with the trombone
  const dz = outBack(seg(t, 24.6, 24.95), 1.8) * (1 - inCubic(seg(t, 26.3, 26.6)));
  dozer.visible = dz > 0.01;
  dozer.scale.setScalar(1.6 * dz);
  dozer.position.y = DOZER[1] + 0.04 * Math.abs(Math.sin(t * 18)) * dz;

  // Mars: a slow sway; the volcano drops back and regrows while the lava piles up
  mars.rotation.y = everest.rotation.y = 0;
  epWorld.rotation.y = 0.15 * Math.sin(TAU * t / 14);
  const h = volcH(t);
  setVolcano(h);
  const ev = outBack(seg(t, 11.1, 11.5), 1.8) * (1 - seg(t, 15.3, 15.6));
  everest.visible = ev > 0.01;
  everest.scale.setScalar(Math.max(0.001, ev));
  const summit = OLY.clone().multiplyScalar(M_R + OLY_H * h * 0.78);
  const lavaOn = t > 15.6 && t < 19.7;
  lavaGlow.visible = lavaOn;
  lavaGlow.position.copy(summit);
  lavaGlow.scale.setScalar(0.9 + 0.15 * Math.sin(TAU * 2 * t));
  const side = new THREE.Vector3().crossVectors(OLY, new THREE.Vector3(1, 0, 0)).normalize();
  for (const L of LAVA) {
    L.m.visible = lavaOn;
    if (!lavaOn) continue;
    const u = (((t - 15.6) / 1.3 + L.ph) % 1 + 1) % 1;
    const a = OLY_A * 0.95 * u; // angle away from the summit, down the flank
    const axis = side.clone().applyAxisAngle(OLY, L.az);
    const dir = OLY.clone().applyAxisAngle(axis, a);
    const ang = dir.angleTo(OLY);
    const p = ang < OLY_A ? Math.cos((Math.PI / 2) * ang / OLY_A) ** 1.4 : 0;
    L.m.position.copy(dir).multiplyScalar(M_R + OLY_H * h * p + 0.04);
    L.m.scale.setScalar(1.2 * (1 - 0.6 * u));
  }
}
"""

build(HERE, {
    "title": 'Challan #6 "Mars pe Illegal Construction"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#3E2A6E", "#120A2A"], "space": ["#5A2A3A", "#1A0A16"], "alt": ["#FFB385", "#7A2E5C"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 0.8],
})
