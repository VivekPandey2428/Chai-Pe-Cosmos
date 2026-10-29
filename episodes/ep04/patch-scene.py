"""Challan #4 "Suraj ka Bijli ka Bill": Inspector Sahab bills the Sun for its power; the Tapri wala explains fusion.

Home is daytime with the Sun in the sky -> the Sun up close, hydrogen fusing into helium (whip on "Fusion!") -> snap home
on "तो bill तो बनता है!" -> a sunbeam grows a tea bush next to the chair ("चाय की पत्ती भी इसी धूप से उगी है") ->
trombone, chai, end card -> comment question -> subscribe callout -> teaser (dusk, Venus appears) -> loop to frame 0.
Data and world JS only; the machinery is tools/cycle2_patch.py. Run after tools/build-dialogue-ep.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build

DUR = 39.37
SPACE = [[13.55, 19.25]]

guy = {
    "handR": [[0, "SIP_R"], [0.85, "SIP_R"], [1.1, "REST_R", "back"], [8.9, "REST_R"], [9.15, "RAISE_R", "back"], [10.9, "RAISE_R"],
              [11.2, "REST_R"], [22.3, "REST_R"], [22.55, "TOAST_R", "back"], [25.4, "TOAST_R"], [25.7, "REST_R"], [27.4, "REST_R"],
              [27.6, "SIP_R"], [28.2, "SIP_R"], [28.5, "REST_R"], [35.95, "REST_R"], [38.7, "REST_R"], [39.0, "SIP_R"]],
    "handL": [[0, "REST_L"], [25.8, "REST_L"], [25.95, "POCKET"], [26.02, "POCKET"], [26.22, "OFFER", "back"], [26.45, "OFFER"],
              [26.7, "REST_L"], [36.0, "REST_L"], [36.3, "OFFER", "back"], [38.3, "OFFER"], [38.7, "REST_L"]],
    "lid": [[0, 1.1], [0.85, 1.1], [0.95, -1.75, "snap"], [1.5, -1.3], [7.2, -1.3], [7.4, -0.6], [11.1, -0.6], [11.3, -0.85],
            [21.6, -0.85], [21.8, 0.05], [22.5, 0.05], [22.7, -0.85], [25.7, -0.85], [25.75, 1.0], [25.95, 1.0], [26.05, 0.05],
            [27.5, 0.05], [27.6, 1.1], [28.2, 1.1], [28.5, -0.85], [36.0, -0.85], [36.2, -0.6], [38.6, -0.6], [38.9, -0.85],
            [39.0, 1.1]],
    "yaw": [[0, 0], [0.95, 0], [1.15, 0.55, "back"], [38.8, 0.55], [39.2, 0]],
    "mood": {"startle": [0.9], "smug": [[7.3, 11.1], [36.0, 38.7]], "laugh": [[21.6, 22.5], [25.75, 26.1]],
             "sip": [[-1, 0.9], [27.6, 28.2], [39.0, 40]], "lookUp": [[1.5, 3.8], [32.0, 35.5]]},
}
cop = {
    "handR": [[0, "UP"], [7.2, "UP"], [7.45, "AIM", "back"], [11.2, "AIM"], [11.45, "UP", "back"], [21.5, "UP"], [21.75, "AIM", "back"],
              [25.75, "AIM"], [26.2, "LOW"], [27.1, "LOW"], [27.35, "AIM", "back"], [31.8, "AIM"], [32.05, "UP", "back"], [DUR, "UP"]],
    "handL": [[0, "HIP"], [0.85, "HIP"], [1.0, "STOP", "back"], [2.4, "STOP"], [2.7, "HIP"], [6.1, "HIP"], [6.3, "STOP", "back"],
              [7.0, "STOP"], [7.25, "HIP"], [26.35, "HIP"], [26.5, "TAKE", "back"], [26.6, "TAKE"], [26.75, "HOLD"], [26.9, "SIP"],
              [27.15, "SIP"], [27.25, "HOLD"], [38.9, "HOLD"], [39.3, "HIP"]],
    "lid": [[0, -0.75], [24.5, -0.75], [24.6, -1.8, "snap"], [25.7, -1.8], [26.0, 0.35], [26.35, 0.35], [26.5, -0.9], [26.85, -0.9],
            [26.9, 1.1], [27.15, 1.1], [27.25, -0.75], [DUR, -0.75]],
    "aim": [[0, "sun"], [7.25, "guy"], [11.25, "sun"], [21.55, "guy"], [25.75, "down"], [27.15, "cam"], [31.85, "venus"], [35.9, "sun"]],
    "beam": [[0, 7.1], [19.3, 21.5], [32.2, 35.5], [37.6, 99]],
    "screen": [[0, "BILL!", 1], [7.2, "6 LAKH+", 0], [11.3, "?!", 0], [19.3, "BILL!", 1], [24.6, "ERROR", 1], [25.75, "0 Rs", 0],
               [27.2, "COMMENT", 0], [31.1, "SUBSCRIBE?", 1], [31.85, "VENUS", 0], [35.9, "BILL!", 1]],
    "duty": [[0, 13.55], [19.25, 21.6], [27.2, 32.1], [35.9, 99]],
    "lazyFrom": 26.5,
    "sweat": [24.7, 25.8],
    "mood": {"shout": [0.9, 6.3], "confused": [[11.3, 13.5]], "smug": [[19.3, 21.5]], "shock": [[24.6, 25.7]], "sad": [[25.7, 26.35]],
             "sheepish": [[26.35, 27.15]], "sip": [[26.9, 27.2]], "toCam": [[27.15, 32.1]],
             "lookSky": [[-1, 7.2], [11.3, 13.5], [31.9, 35.6], [37.6, 99]]},
}
act = {"guy": guy, "cop": cop, "k2": {"pop": 25.95, "give": 26.55, "sipA": 26.9, "sipB": 27.2, "end": 38.9}, "alt": [[31.9, 35.7]]}

nums = [
    {"value": 6, "plus": True, "fly": 3.95, "land": 4.34, "lock": 5.3, "out": 6.9, "rim": "#FFB703"},  # "छह लाख साल की बिजली"
    {"value": 60, "fly": 15.5, "land": 15.89, "lock": 16.75, "out": 18.9, "rim": "#FB5607"},  # "साठ करोड़ टन"
]

CU_COP_AIM = {"look": [0.9, 2.75, 0.5], "dir": [-0.35, 0.02, 1]}
CU_COP = {"look": [1.0, 2.75, 0.5], "dir": [-0.35, 0.08, 1]}
CU_GUY = {"look": [-0.45, 2.3, 0.2], "dir": [0.3, 0.1, 1]}
SKY_WIDE = {"look": [0.3, 3.6, -0.5], "dir": [0.06, -0.1, 1], "dist": 12.0}
shots = [
    {"t": 0, **CU_COP_AIM, "dist": 5.2, "to": {"dist": 4.6}},  # hook: radar gun on the Sun
    {"t": 3.8, "blend": 0.5, "look": [-0.6, 3.6, -0.5], "dir": [0.1, -0.08, 1], "dist": 12.0},  # wide and low: the Sun above them, room for 6+
    {"t": 7.2, **CU_GUY, "dist": 5.0, "to": {"dist": 4.6}},  # "सही पकड़ा साहब"
    {"t": 11.3, **CU_COP, "dist": 4.8},  # "इतनी बिजली आती कहाँ से?"
    {"t": 19.25, "look": [0.2, 2.2, 0.3], "dir": [0.04, 0.22, 1], "dist": 9.6},  # back home
    {"t": 19.6, "blend": 0.5, **CU_COP, "dist": 4.6},  # "तो bill तो बनता है!"
    {"t": 21.6, "look": [-1.3, 2.0, 0.4], "dir": [0.32, 0.16, 1], "dist": 8.6},  # the sunbeam grows a tea bush
    {"t": 24.5, "blend": 0.6, "look": [1.0, 3.0, 0.5], "dir": [-0.35, 0.08, 1], "dist": 4.6},  # it dawns on him
    {"t": 25.75, "blend": 0.4, "look": [1.0, 2.6, 0.5], "dir": [-0.3, 0.05, 1], "dist": 3.6},  # trombone: his face
    {"t": 25.95, "look": [0.15, 2.4, 0.2], "dir": [0.06, 0.3, 1], "dist": 11.0},  # chai together, end card
    {"t": 27.15, "look": [1.05, 2.75, 0.75], "dir": [0.12, 0.1, 1], "dist": 4.4, "to": {"dist": 4.0}},  # to camera: comment, subscribe
    {"t": 31.85, **SKY_WIDE},  # teaser: dusk, Venus comes out
    {"t": 35.9, **CU_GUY, "dist": 5.0, "to": {"dist": 4.7}},  # "साहब, bill पे sign तो करा लो..."
    {"t": 37.6, **CU_COP_AIM, "dist": 5.6, "to": {"dist": 5.2}},  # the loop: back to frame 0
]
space_shots = [
    {"t": 13.55, "look": [0, 0.4, 0], "dir": [0, 0.22, 1], "dist": 17.0},  # the Sun, fusion sparking on its face
    {"t": 15.3, "blend": 0.9, "look": [0.4, 0.6, 2.6], "dir": [0.3, 0.12, 1], "dist": 8.5},  # in close: H + H -> He, the 60
    {"t": 17.7, "blend": 1.0, "look": [0, 0.6, 0], "dir": [-0.22, 0.3, 1], "dist": 16.0},
]

WORLD = r"""
// ---- Challan #4: a Sun in the home sky, a tea bush its beam grows, Venus for the teaser; the Sun up close with fusion
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
const skySunHalo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.45)", "rgba(251,86,7,0)"));
const SKY_SUN = [-2.6, 5.5, -7];
const skyVenus = new THREE.Mesh(new THREE.IcosahedronGeometry(0.3, 3), glossy("#F6E2B0", { roughness: 0.4, flatShading: true }));
const skyVenusGlow = new THREE.Sprite(haloMat("rgba(255,240,200,0.8)", "rgba(255,240,200,0)"));
const SKY_VENUS = [2.0, 5.6, -7];
chairWorld.add(skySun, skySunHalo, skySunHalo2, skyVenus, skyVenusGlow);
// the tea bush by the armchair: a clump of glossy leaves the sunbeam brings up
const BUSH = [-2.0, -groundDrop(-2.0, 0.9) - 0.02, 0.9];
const bush = new THREE.Group();
bush.position.set(...BUSH);
bush.scale.setScalar(1.7);
const leafMat = glossy("#2FA84F", { roughness: 0.35, flatShading: true });
const leafMat2 = glossy("#5BD06E", { roughness: 0.35, flatShading: true });
const rndB = mulberry32(11);
const leaves = [];
for (let i = 0; i < 14; i++) {
  const lf = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16, 0), i % 3 ? leafMat : leafMat2);
  const a = rndB() * TAU, r = 0.12 + 0.28 * rndB(), h = 0.12 + 0.5 * rndB();
  lf.userData.home = new THREE.Vector3(r * Math.cos(a), h, r * Math.sin(a));
  lf.scale.set(1.0, 0.45, 1.6);
  lf.rotation.set(rndB(), a, 0.3 * rndB());
  leaves.push(lf);
  bush.add(lf);
}
chairWorld.add(bush);
const sunbeam = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.9, 1, 20, 1, true),
  new THREE.MeshBasicMaterial({ color: "#FFD23F", toneMapped: false, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
chairWorld.add(sunbeam);
function skyAt(t) {
  const set = inOutSine(seg(t, 31.9, 33.0)) * (1 - inOutSine(seg(t, 35.6, 36.4))); // the Sun dips for the teaser
  return { sun: [SKY_SUN[0], SKY_SUN[1] - 4.5 * set, SKY_SUN[2]], venus: SKY_VENUS };
}

// the Sun up close: churning low-poly surface, halos, and fusion: two hydrogen nuclei meet, flash, and a helium nucleus flies off
const epWorld = new THREE.Group();
const bigSun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
bigSun.scale.setScalar(2.1);
const bigHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.9)", "rgba(255,183,3,0)"));
const bigHalo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.5)", "rgba(251,86,7,0)"));
bigHalo.scale.setScalar(9.5);
bigHalo2.scale.setScalar(16);
epWorld.add(bigHalo2, bigHalo, bigSun);
const hMat = new THREE.MeshPhysicalMaterial({ color: "#4CC9F0", emissive: "#1E7FB0", emissiveIntensity: 0.9, roughness: 0.2, clearcoat: 1 });
const heMat = new THREE.MeshPhysicalMaterial({ color: "#FFE66D", emissive: "#FFB703", emissiveIntensity: 1.1, roughness: 0.2, clearcoat: 1 });
const rndF = mulberry32(23);
const FUSE = Array.from({ length: 9 }, (_, i) => {
  const th = -0.9 + 1.8 * rndF(), ph = -0.55 + 1.1 * rndF();
  const at = new THREE.Vector3(Math.sin(th) * Math.cos(ph), Math.sin(ph), Math.cos(th) * Math.cos(ph)).multiplyScalar(2.75);
  const side = new THREE.Vector3(Math.cos(th), 0, -Math.sin(th)).multiplyScalar(0.55);
  const h1 = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 12), hMat);
  const h2 = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 12), hMat);
  const he = new THREE.Mesh(new THREE.SphereGeometry(0.3, 18, 14), heMat);
  const flash = new THREE.Sprite(haloMat("rgba(255,255,240,1)", "rgba(255,240,180,0)"));
  epWorld.add(h1, h2, he, flash);
  return { at, side, h1, h2, he, flash, ph: i / 9 + 0.05 * rndF(), out: at.clone().normalize() };
});
const sunLight2 = new THREE.PointLight(0xffc46b, 80, 0, 2);
sunLight2.position.set(0, 0, 3.5);
epWorld.add(sunLight2);
const FOCUS = {};

function episodeRender(t, name) {
  // home sky: the Sun (dips at dusk for the teaser), Venus comes out, stars only at dusk
  const sky = skyAt(t);
  skySun.position.set(...sky.sun);
  skySun.scale.setScalar(1.0);
  skySun.rotation.y = 0.4 * t;
  skySunHalo.position.copy(skySun.position);
  skySunHalo2.position.copy(skySun.position);
  skySunHalo.scale.setScalar(4.2 * (1 + 0.04 * Math.sin(TAU * t)));
  skySunHalo2.scale.setScalar(7.5);
  const dusk = mood(t, ACT.alt, 0.6);
  skyVenus.visible = skyVenusGlow.visible = dusk > 0.01;
  skyVenus.position.set(...SKY_VENUS);
  skyVenus.scale.setScalar(outBack(seg(t, 32.6, 33.2), 1.6) * (1 - seg(t, 35.4, 35.8)));
  skyVenusGlow.position.copy(skyVenus.position);
  skyVenusGlow.scale.setScalar(2.4 * dusk);
  if (name === "chair") stars.visible = dusk > 0.3;
  key.intensity = name === "chair" ? lerp(2.6, 1.9, dusk) : 2.4;
  key.color.set(dusk > 0.5 ? "#e8ecff" : "#fff1e0");
  // "चाय की पत्ती भी इसी धूप से उगी है": a beam from the Sun, and the bush grows leaf by leaf
  const beamOn = seg(t, 21.8, 22.3) * (1 - seg(t, 25.5, 25.9));
  sunbeam.visible = beamOn > 0.01;
  const top = V(sky.sun), bot = V(BUSH).add(new THREE.Vector3(0, 0.3, 0));
  sunbeam.position.copy(top).lerp(bot, 0.5);
  sunbeam.scale.set(1, top.distanceTo(bot), 1);
  sunbeam.quaternion.setFromUnitVectors(up, tmpV.copy(top).sub(bot).normalize());
  sunbeam.material.opacity = 0.32 * beamOn * (0.85 + 0.15 * Math.sin(TAU * 2 * t));
  leaves.forEach((lf, i) => {
    const g = outBack(seg(t, 22.0 + 0.09 * i, 22.5 + 0.09 * i), 2.0);
    lf.position.copy(lf.userData.home).multiplyScalar(0.3 + 0.7 * g);
    lf.visible = g > 0.01;
    lf.scale.set(1.0 * g, 0.45 * g, 1.6 * g);
  });
  bush.rotation.y = 0.15 * Math.sin(TAU * t / 4);

  // the Sun up close
  bigSun.rotation.y = 0.05 * t;
  bigSun.rotation.x = 0.03 * t;
  bigHalo.scale.setScalar(9.5 * (1 + 0.03 * Math.sin(TAU * 1.3 * t)));
  for (const f of FUSE) {
    const u = (((t - 13.55) / 1.7 + f.ph) % 1 + 1) % 1; // each site loops every 1.7 s
    const meet = seg(u, 0, 0.45), boom = seg(u, 0.45, 0.6), fly = seg(u, 0.5, 1);
    const pre = u < 0.47;
    f.h1.visible = f.h2.visible = pre;
    f.h1.position.copy(f.at).addScaledVector(f.side, 1 - inCubic(meet));
    f.h2.position.copy(f.at).addScaledVector(f.side, -(1 - inCubic(meet)));
    f.flash.visible = boom > 0 && boom < 1;
    f.flash.position.copy(f.at);
    f.flash.scale.setScalar(2.6 * Math.sin(Math.PI * boom));
    f.he.visible = !pre;
    f.he.position.copy(f.at).addScaledVector(f.out, 1.6 * outExpo(fly));
    f.he.scale.setScalar(outBack(seg(u, 0.47, 0.6), 2) * (1 - seg(u, 0.85, 1)));
  }
}
"""

build(HERE, {
    "title": 'Challan #4 "Suraj ka Bijli ka Bill"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#FFD6A5", "#FF6B6B"], "space": ["#4A1530", "#1A0718"], "alt": ["#B4588C", "#2A1846"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})
