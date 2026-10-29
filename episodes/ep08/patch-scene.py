"""Challan #8 "Saturn ka Swimming Pool": someone wants a pool for Saturn; it would float (density 0.69 < water's 1).

Opens in space: Saturn hangs over a giant pool and is lowered in, where it floats -> home: "this big... floats?" ->
whip back: 0.69 lands, Saturn bobbing -> Earth (5.5) is dropped in and sinks -> snap home: "permit de deta hoon" ->
"the pool has to be bigger than Saturn" -> trombone, chai, end card -> comment -> subscribe -> teaser (a gold glint:
Webb) -> crane to Saturn in the sky: the loop. Acting and camera come from tools/cycle2_beats.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import standard

DUR = 41.8
SPACE = [[0, 7.05], [9.85, 22.88]]
act, shots, T = standard(HERE, {"dur": DUR, "space": SPACE, "hook": "saturn", "tease": "webb", "home_start": False,
                                "screen": {"hook": "ILLEGAL!", "punch": "POOL?", "tease": "WEBB"},
                                "extra_shots": [{"t": 40.4, "blend": 1.0, "look": [1.9, 5.2, -6.5], "dir": [-0.15, -0.25, 1], "dist": 9.0, "to": {"dist": 5.0}}]})
act["cop"]["duty"][0] = [0, 7.05]  # the beacon wash over the pool at the start

nums = [
    {"value": 0.69, "dec": 2, "fly": 11.0, "land": 11.29, "lock": 12.4, "out": 13.7, "rim": "#4CC9F0"},  # "zero point छह नौ"
    {"value": 5.5, "dec": 1, "fly": 19.5, "land": 19.81, "lock": 20.8, "out": 21.7, "rim": "#34C759"},  # "पाँच point पाँच"
]
space_shots = [
    {"t": 0, "look": [0, 1.6, 0], "dir": [0, 0.55, 1], "dist": 27, "to": {"dist": 24}},  # Saturn over the pool
    {"t": 9.85, "look": [0, 0.4, 0], "dir": [0.25, 0.5, 1], "dist": 21},  # floating, 0.69
    {"t": 16.0, "blend": 1.0, "look": [-2.8, 1.2, 0], "dir": [0.15, 0.45, 1], "dist": 20},  # room for Earth
]

WORLD = r"""
// ---- Challan #8: Saturn in the night sky (a gold glint for the teaser); in space, a giant pool, Saturn floats, Earth sinks
const makeSaturn = (r) => {
  const g = new THREE.Group();
  Object.assign(EARTH_COLORS, { sA: "#F2D9A4", sB: "#E3BC7A", sC: "#C9965A", sD: "#F7E7C4" });
  const ball = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(r, 6), (m) => {
    const b = Math.sin(m.y * 11 + 0.6 * Math.sin(m.x * 4));
    return b > 0.6 ? "sD" : b > 0 ? "sA" : b > -0.6 ? "sB" : "sC";
  }), earthMaterial());
  const ring = new THREE.Mesh(new THREE.RingGeometry(r * 1.35, r * 2.1, 72, 1),
    new THREE.MeshBasicMaterial({ color: "#EADBB8", side: THREE.DoubleSide, transparent: true, opacity: 0.85, toneMapped: false }));
  const gap = new THREE.Mesh(new THREE.RingGeometry(r * 1.72, r * 1.78, 72, 1),
    new THREE.MeshBasicMaterial({ color: "#7A6040", side: THREE.DoubleSide, toneMapped: false }));
  ring.rotation.x = gap.rotation.x = Math.PI / 2 - 0.38;
  g.add(ball, ring, gap);
  g.userData.ball = ball;
  return g;
};
const skySat = makeSaturn(0.42);
const SKY_SAT = [2.0, 5.4, -7];
skySat.position.set(...SKY_SAT);
const webbGlint = new THREE.Sprite(haloMat("rgba(255,215,80,1)", "rgba(255,180,0,0)"));
chairWorld.add(skySat, webbGlint);
function skyAt(t) {
  const rise = outBack(seg(t, 34.8, 35.8), 1.1) * (1 - inOutSine(seg(t, 38.4, 39.0)));
  return { saturn: SKY_SAT, webb: [-2.3, lerp(1.5, 5.6, rise), -7] };
}

// space: the pool (water box with a tiled rim), Saturn lowered in and floating ~70% under, Earth dropped and sinking
const epWorld = new THREE.Group();
const POOL_W = 22, POOL_D = 13, POOL_H = 3.2;
const water = new THREE.Mesh(new THREE.BoxGeometry(POOL_W, POOL_H, POOL_D),
  new THREE.MeshPhysicalMaterial({ color: "#2E9BF0", transparent: true, opacity: 0.55, roughness: 0.1, clearcoat: 1, depthWrite: false }));
water.position.y = -POOL_H / 2;
const floor = new THREE.Mesh(new THREE.BoxGeometry(POOL_W, 0.2, POOL_D), glossy("#7FD8FF", { roughness: 0.4 }));
floor.position.y = -POOL_H - 0.1;
const tile = glossy("#F4FBFF", { roughness: 0.3 });
const rims = [[POOL_W + 0.8, 0.35, 0.4, 0, POOL_D / 2 + 0.2], [POOL_W + 0.8, 0.35, 0.4, 0, -POOL_D / 2 - 0.2],
  [0.4, 0.35, POOL_D, POOL_W / 2 + 0.2, 0], [0.4, 0.35, POOL_D, -POOL_W / 2 - 0.2, 0]].map(([w, h, d, x, z]) => {
  const m = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 2, 0.08), tile);
  m.position.set(x, 0.05, z);
  return m;
});
const ladder = new THREE.Group();
for (const x of [-0.25, 0.25]) {
  const rail = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.04, 8, 20, Math.PI), glossy("#D8DDE6", { metalness: 0.8, roughness: 0.2 }));
  rail.position.set(x, 0.2, 0);
  rail.rotation.y = Math.PI / 2;
  ladder.add(rail);
}
ladder.position.set(POOL_W / 2 - 1.2, 0, POOL_D / 2 + 0.2);
epWorld.add(water, floor, ladder, ...rims);
const bigSat = makeSaturn(2.1);
epWorld.add(bigSat);
const sinkEarth = makeEarth(1.0);
epWorld.add(sinkEarth);
const DROPS = Array.from({ length: 16 }, (_, i) => {
  const d = new THREE.Mesh(new THREE.SphereGeometry(0.13, 10, 8), glossy("#BFEAFF", { roughness: 0.1, transparent: true, opacity: 0.9 }));
  epWorld.add(d);
  return { d, a: (i / 16) * TAU, v: 0.8 + 0.5 * ((i * 7) % 5) / 5 };
});
const sunL = new THREE.DirectionalLight(0xfff1e0, 1.2);
sunL.position.set(-4, 8, 6);
epWorld.add(sunL);
const FOCUS = {};
function splash(t, t0, at, size) {
  const u = seg(t, t0, t0 + 0.9);
  return u > 0 && u < 1 ? { u, at, size } : null;
}

function episodeRender(t, name) {
  skySat.rotation.y = 0.15 * t;
  const sky = skyAt(t);
  webbGlint.visible = t > 34.7 && t < 39.1;
  webbGlint.position.set(...sky.webb);
  webbGlint.scale.setScalar(1.3 * (1 + 0.15 * Math.sin(TAU * 2 * t)));
  key.intensity = name === "chair" ? 2.0 : 2.0;
  key.color.set(name === "chair" ? "#e8ecff" : "#fff1e0");

  // Saturn: hangs at y 5.5, lowered on "तैर जाएगा" (4.6-6.3), then floats a quarter-radius under the waterline and bobs
  const FLOAT = -0.25 * 2.1;
  const lower = inOutSine(seg(t, 4.6, 6.3));
  const bob = 0.12 * Math.sin(TAU * t / 2.2) * seg(t, 6.0, 6.8);
  bigSat.position.set(0, lerp(5.5, FLOAT, lower) + bob + (t < 4.6 ? 0.15 * Math.sin(TAU * t / 3) : 0), 0);
  bigSat.rotation.y = 0.12 * t;
  bigSat.rotation.z = 0.05 * Math.sin(TAU * t / 2.2);
  // Earth: appears above on "तो Earth भी तैरेगी?", drops on "सीधा", sinks to the floor
  const eIn = outBack(seg(t, 16.3, 16.8), 1.6);
  const drop = inCubic(seg(t, 21.2, 21.6));
  const sink = outExpo(seg(t, 21.6, 22.6));
  sinkEarth.visible = t > 16.3;
  sinkEarth.scale.setScalar(Math.max(0.001, eIn));
  sinkEarth.position.set(-6.0, lerp(4.0, 0, drop) + lerp(0, -POOL_H + 0.85, sink), 0.6);
  sinkEarth.rotation.y = 0.3 * t;
  // splashes when each body hits the water
  const sp = splash(t, 5.5, new THREE.Vector3(0, 0, 0), 2.2) || splash(t, 21.6, new THREE.Vector3(-6.0, 0, 0.6), 1.0);
  DROPS.forEach((D) => {
    D.d.visible = !!sp;
    if (!sp) return;
    const r = sp.size * (0.6 + 1.4 * sp.u) * D.v;
    D.d.position.set(sp.at.x + Math.cos(D.a) * r, 0.2 + sp.size * 1.6 * sp.u * (1 - sp.u) * 2 * D.v, sp.at.z + Math.sin(D.a) * r * 0.6);
    D.d.scale.setScalar(sp.size * 0.8 * (1 - sp.u));
  });
}
"""

build(HERE, {
    "title": 'Challan #8 "Saturn ka Swimming Pool"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#3E2A6E", "#120A2A"], "space": ["#24406E", "#0B1530"], "alt": ["#3E2A6E", "#120A2A"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 0.95],
})
print("T", {k: v for k, v in T.items() if k in ("T", "C", "S", "Z", "P", "shock")})
