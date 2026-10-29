"""Challan #7 "Late-Latif Suraj": Inspector Sahab books the Sun for arriving 8 min 20 s late; light takes time to travel.

Dawn at home, the gun on the Sun, 8 min 20 s lands -> whip to space: light pulses race from the Sun down to Earth with a
stopwatch -> the Sun switches off but its last light is still on the way, Earth stays lit until it lands -> Earth and
Moon: moonlight arrives in 1.3 s -> snap home: "तो मैं तो अभी का हूँ!" -> "nanoseconds old" -> trombone, chai, end
card -> comment -> subscribe -> teaser (Saturn rises) -> loop. Acting and camera come from tools/cycle2_beats.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import standard

DUR = 42.94
SPACE = [[4.75, 22.68]]
act, shots, T = standard(HERE, {"dur": DUR, "space": SPACE, "hook": "sun", "tease": "saturn", "alt": [[35.6, 39.6]],
                                "screen": {"hook": "LATE!", "punch": "10 ns", "tease": "SATURN"}})
act["guy"]["mood"]["lookUp"].append([1.5, 4.5])

nums = [
    {"value": 8, "fly": 1.9, "land": 2.2, "lock": 3.1, "out": 4.45, "rim": "#FFB703"},  # "आठ minute बीस second"
    {"value": 1.3, "dec": 1, "fly": 20.3, "land": 20.64, "lock": 21.6, "out": 22.45, "rim": "#4CC9F0"},  # "एक point तीन second"
]
space_shots = [
    {"t": 4.75, "look": [0, 0.6, 0], "dir": [0, 0.08, 1], "dist": 35},  # the Sun up top, Earth below, light on its way
    {"t": 13.8, "blend": 0.8, "look": [0, 0.3, 0], "dir": [0.1, 0.12, 1], "dist": 33},
    {"t": 17.75, "blend": 0.9, "look": [1.6, -8.6, 0], "dir": [0.05, 0.25, 1], "dist": 10.5},  # Earth and the Moon
]

WORLD = r"""
// ---- Challan #7: a low dawn Sun at home (Saturn rises for the teaser); in space, light travelling Sun -> Earth -> Moon
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
const skySunHalo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.45)", "rgba(251,86,7,0)"));
const SKY_SUN = [-2.6, 4.4, -7];
const saturnSky = new THREE.Group();
const satBall = new THREE.Mesh(new THREE.IcosahedronGeometry(0.42, 3), glossy("#E9C98B", { flatShading: true, roughness: 0.45 }));
const satRing = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.95, 48), new THREE.MeshBasicMaterial({ color: "#F2DFB5", side: THREE.DoubleSide, toneMapped: false, transparent: true, opacity: 0.9 }));
satRing.rotation.x = Math.PI / 2 - 0.45;
saturnSky.add(satBall, satRing);
chairWorld.add(skySun, skySunHalo, skySunHalo2, saturnSky);
function skyAt(t) {
  const rise = outBack(seg(t, 35.8, 36.9), 1.1) * (1 - inOutSine(seg(t, 39.4, 40.0)));
  return { sun: SKY_SUN, saturn: [2.2, lerp(1.0, 5.4, rise), -7] };
}

// space: the Sun high, Earth far below, a dotted light path, pulses, a stopwatch; the Moon beside Earth
const epWorld = new THREE.Group();
const SUN_P = new THREE.Vector3(0, 9, 0), EARTH_P = new THREE.Vector3(0, -9, 0), MOON_P = new THREE.Vector3(3.6, -8.2, 0);
const bigSun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
bigSun.scale.setScalar(2.2);
bigSun.position.copy(SUN_P);
const bigHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
bigHalo.position.copy(SUN_P);
bigHalo.scale.setScalar(9);
const lEarth = makeEarth(1.7);
lEarth.position.copy(EARTH_P);
const lMoon = new THREE.Mesh(new THREE.IcosahedronGeometry(0.5, 4), glossy("#B4B8C6", { flatShading: true, roughness: 0.7 }));
lMoon.position.copy(MOON_P);
const moonGlow = new THREE.Sprite(haloMat("rgba(220,230,255,0.6)", "rgba(220,230,255,0)"));
moonGlow.position.copy(MOON_P);
const earthLight = new THREE.PointLight(0xfff1d0, 0, 0, 0);
earthLight.position.set(0, -3, 6);
epWorld.add(bigSun, bigHalo, lEarth, lMoon, moonGlow, earthLight);
const mPulse = new THREE.Sprite(haloMat("rgba(225,235,255,1)", "rgba(200,220,255,0)"));
mPulse.scale.setScalar(0.9);
epWorld.add(mPulse);
// dotted path
const dots = new THREE.InstancedMesh(new THREE.SphereGeometry(0.05, 8, 6), new THREE.MeshBasicMaterial({ color: "#FFE9A8", toneMapped: false }), 40);
{
  const o = new THREE.Object3D();
  for (let i = 0; i < 40; i++) {
    o.position.copy(SUN_P).lerp(EARTH_P, (i + 0.5) / 40);
    o.updateMatrix();
    dots.setMatrixAt(i, o.matrix);
  }
}
epWorld.add(dots);
// light pulses with short trails (a pulse takes 3.6 s on screen = 8 min 20 s)
const PULSES = Array.from({ length: 3 }, () => {
  const g = new THREE.Group();
  const head = new THREE.Sprite(haloMat("rgba(255,250,220,1)", "rgba(255,220,120,0)"));
  head.scale.setScalar(1.6);
  g.add(head);
  for (let k = 1; k <= 6; k++) {
    const s = new THREE.Sprite(haloMat("rgba(255,230,150,0.8)", "rgba(255,220,120,0)"));
    s.scale.setScalar(1.3 - 0.17 * k);
    s.position.y = 0.32 * k;
    g.add(s);
  }
  epWorld.add(g);
  return g;
});
// stopwatch beside the path
const watch = new THREE.Group();
const face = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.15, 0.18, 40), glossy("#FFFFFF", { roughness: 0.3 }));
face.rotation.x = Math.PI / 2;
const rimW = new THREE.Mesh(new THREE.TorusGeometry(1.18, 0.11, 10, 40), glossy("#FF2D3D", { roughness: 0.3 }));
const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 0.3, 14), glossy("#FF2D3D"));
knob.position.y = 1.42;
const hand = new THREE.Mesh(new RoundedBoxGeometry(0.08, 0.95, 0.06, 2, 0.02), glossy("#2A1530"));
hand.geometry.translate(0, 0.42, 0);
hand.position.z = 0.12;
const ticks = new THREE.InstancedMesh(new RoundedBoxGeometry(0.05, 0.16, 0.04, 1, 0.01), glossy("#2A1530"), 12);
{
  const o = new THREE.Object3D();
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * TAU;
    o.position.set(Math.sin(a) * 0.95, Math.cos(a) * 0.95, 0.1);
    o.rotation.set(0, 0, -a);
    o.updateMatrix();
    ticks.setMatrixAt(i, o.matrix);
  }
}
watch.add(face, rimW, knob, hand, ticks);
watch.position.set(3.4, 0.5, 0.5);
epWorld.add(watch);
const FOCUS = {};
const PULSE_S = 3.6;
const T_OFF = 14.36; // "अभी बुझ जाए"
const T_ARRIVE = T_OFF + PULSE_S; // the last light reaches Earth

function episodeRender(t, name) {
  const sky = skyAt(t);
  skySun.position.set(...sky.sun);
  skySun.rotation.y = 0.4 * t;
  skySunHalo.position.copy(skySun.position);
  skySunHalo2.position.copy(skySun.position);
  skySunHalo.scale.setScalar(4.2 * (1 + 0.04 * Math.sin(TAU * t)));
  skySunHalo2.scale.setScalar(7.5);
  saturnSky.position.set(...sky.saturn);
  saturnSky.visible = t > 35.7 && t < 40.1;
  saturnSky.rotation.y = 0.2 * t;
  const dusk = mood(t, ACT.alt, 0.6);
  if (name === "chair") stars.visible = dusk > 0.3;
  key.intensity = name === "chair" ? lerp(2.3, 1.9, dusk) : 1.6;
  key.color.set(dusk > 0.5 ? "#e8ecff" : "#fff1e0");

  // space: the Sun is "on" except between T_OFF and 17.75; pulses leave every 1.2 s while it shines
  const off = t >= T_OFF && t < 17.75;
  const dim = off ? 1 - outExpo(seg(t, T_OFF, T_OFF + 0.25)) : seg(t, 17.75, 18.1);
  bigSun.material.color.setScalar(0.15 + 0.85 * dim);
  bigHalo.material.opacity = dim;
  bigSun.scale.setScalar(2.2 * (0.9 + 0.1 * dim));
  PULSES.forEach((p, i) => {
    // pulse i left at the latest launch time <= t on its own 3.6 s cycle; no launches while the Sun is off
    const cyc = PULSE_S, ph = i * 1.2;
    let launch = Math.floor((t - 4.75 - ph) / cyc) * cyc + 4.75 + ph;
    if (launch >= T_OFF && launch < 17.75) launch = -99;
    const u = (t - launch) / cyc;
    p.visible = t < 17.75 && u >= 0 && u < 1 && launch > 0;
    p.position.copy(SUN_P).lerp(EARTH_P, u);
  });
  // Earth stays lit until the last light lands, then goes dark until the Sun is back
  const dark = t >= T_ARRIVE - 0.2 && t < 17.9 ? 1 : 0;
  lEarth.material.color.setScalar(dark ? 0.25 : 1);
  earthLight.intensity = 0;
  lEarth.rotation.y = 0.12 * t;
  watch.visible = t < 13.9;
  hand.rotation.z = -TAU * ((t - 4.75) / PULSE_S);
  // the Moon: its light reaches Earth in 1.3 s ("एक point तीन second")
  lMoon.rotation.y = 0.1 * t;
  moonGlow.scale.setScalar(1.6);
  const mu = ((t - 20.64) / 1.3) % 1;
  mPulse.visible = t >= 20.64 && t < 22.6;
  mPulse.position.copy(MOON_P).lerp(EARTH_P.clone().add(new THREE.Vector3(1.2, 1.1, 0)), mu);
}
"""

build(HERE, {
    "title": 'Challan #7 "Late-Latif Suraj"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#FFB385", "#7A2E5C"], "space": ["#1B2348", "#070A18"], "alt": ["#4B3A8C", "#140C33"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})
print("T", {k: v for k, v in T.items() if k in ("T", "C", "S", "Z", "P", "shock")})
