"""Challan #9 "No Parking: Webb Telescope": the cop tickets James Webb for parking 15 lakh km away; it is at L2.

Opens in space on Webb's gold mirror, 15 lakh km lands -> pull out: Sun, Earth and L2 with a "P" sign -> home:
"Parking? Space mein?" -> whip back: Earth and Webb go round the Sun together, the two pulls (Sun, Earth) shown as
arrows -> Earth, the Moon's orbit and L2: four times farther -> snap home: "Free parking? Challan banta hai!" ->
"engine chalana padta hai" -> trombone, chai, end card -> comment -> subscribe -> teaser (a glowing spoon) -> crane to
the gold glint in the sky: the loop. Acting and camera come from tools/cycle2_beats.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import standard

DUR = 43.51
SPACE = [[0, 9.4], [11.55, 22.55]]
act, shots, T = standard(HERE, {"dur": DUR, "space": SPACE, "hook": "webb", "tease": "spoon", "home_start": False,
                                "screen": {"hook": "NO PARKING", "punch": "FREE?", "tease": "CHAMMACH"},
                                "extra_shots": [{"t": 42.1, "blend": 0.9, "look": [-2.2, 5.4, -6.5], "dir": [0.15, -0.25, 1], "dist": 8.0, "to": {"dist": 4.5}}]})
act["cop"]["duty"][0] = [0, 9.4]

nums = [
    {"value": 15, "fly": 1.2, "land": 1.5, "lock": 2.4, "out": 4.3, "rim": "#FFB703"},  # "पंद्रह लाख किलोमीटर"
    {"value": 4, "fly": 20.8, "land": 21.14, "lock": 21.9, "out": 22.4, "rim": "#4CC9F0"},  # "चार गुना"
]
space_shots = [
    {"t": 0, "look": "webb", "dir": [0.35, 0.25, 1], "dist": 5.2, "to": {"dist": 4.2}},  # the gold mirror
    {"t": 4.6, "blend": 1.6, "look": [0, 4.5, 0], "dir": [0, 0.02, 1], "dist": 34},  # Sun, Earth, L2 and the P sign
    {"t": 11.55, "look": [2.5, 4.5, 0], "dir": [0, 0.02, 1], "dist": 36},  # going round together
    {"t": 17.7, "blend": 1.0, "look": "earthL2", "dir": [0.05, 0.05, 1], "dist": 19},  # Moon's orbit vs L2
]

WORLD = r"""
// ---- Challan #9: a gold glint in the night sky (Webb) and a glowing spoon for the teaser; in space, Webb at L2
const skyWebb = new THREE.Sprite(haloMat("rgba(255,215,80,1)", "rgba(255,180,0,0)"));
const SKY_WEBB = [-2.2, 5.4, -7];
skyWebb.position.set(...SKY_WEBB);
const spoon = new THREE.Group();
const steel = glossy("#E6EAF2", { metalness: 0.9, roughness: 0.15 });
const bowl = new THREE.Mesh(new THREE.SphereGeometry(0.22, 20, 14), steel);
bowl.scale.set(1, 0.35, 1.4);
const handle = new THREE.Mesh(new THREE.CapsuleGeometry(0.04, 0.7, 4, 10), steel);
handle.rotation.x = Math.PI / 2;
handle.position.z = 0.62;
spoon.add(bowl, handle);
const spoonGlow = new THREE.Sprite(haloMat("rgba(190,220,255,0.9)", "rgba(150,190,255,0)"));
spoonGlow.scale.setScalar(2.2);
chairWorld.add(skyWebb, spoon, spoonGlow);
function skyAt(t) {
  const rise = outBack(seg(t, 37.4, 38.4), 1.1) * (1 - inOutSine(seg(t, 41.0, 41.6)));
  return { webb: SKY_WEBB, spoon: [2.2, lerp(1.0, 5.3, rise), -7] };
}

// space: the Sun at the top, Earth, the Moon's orbit, L2 below Earth; Webb (18 gold hexagons + sunshield) parked there
const epWorld = new THREE.Group();
const SUN_P = new THREE.Vector3(0, 15, 0);
const rig = new THREE.Group(); // everything that goes round the Sun together
rig.position.copy(SUN_P);
epWorld.add(rig);
const EARTH_L = new THREE.Vector3(0, -13, 0), L2_L = new THREE.Vector3(0, -19.4, 0); // in rig space (L2 ~4 Moon-distances out)
const bigSun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
bigSun.scale.setScalar(2.2);
bigSun.position.copy(SUN_P);
const bigHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
bigHalo.position.copy(SUN_P);
bigHalo.scale.setScalar(9);
epWorld.add(bigSun, bigHalo);
const eOrbit = new THREE.Mesh(new THREE.TorusGeometry(13, 0.05, 6, 240), new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false, transparent: true, opacity: 0.7 }));
eOrbit.position.copy(SUN_P);
epWorld.add(eOrbit);
const wEarth = makeEarth(1.3);
wEarth.position.copy(EARTH_L);
const mOrbit = new THREE.Mesh(new THREE.TorusGeometry(1.6, 0.04, 6, 120), new THREE.MeshBasicMaterial({ color: "#FFFFFF", toneMapped: false, transparent: true, opacity: 0.7 }));
mOrbit.position.copy(EARTH_L);
const wMoon = new THREE.Mesh(new THREE.IcosahedronGeometry(0.22, 3), glossy("#B4B8C6", { flatShading: true }));
rig.add(wEarth, mOrbit, wMoon);
// Webb
const webb = new THREE.Group();
const gold = new THREE.MeshPhysicalMaterial({ color: "#F2B632", metalness: 1, roughness: 0.18, clearcoat: 1, envMapIntensity: 1.6 });
const HEX = 0.19, hexGeo = new THREE.CylinderGeometry(HEX, HEX, 0.04, 6);
hexGeo.rotateX(Math.PI / 2);
const cells = [];
for (let q = -2; q <= 2; q++) for (let r = -2; r <= 2; r++) {
  const s = -q - r;
  if (Math.max(Math.abs(q), Math.abs(r), Math.abs(s)) > 2 || (q === 0 && r === 0)) continue;
  cells.push([HEX * 1.75 * (q + r / 2), HEX * 1.52 * r]);
}
cells.slice(0, 18).forEach(([x, y]) => {
  const h = new THREE.Mesh(hexGeo, gold);
  h.position.set(x, y + 0.75, 0.15);
  h.rotation.z = Math.PI / 6;
  webb.add(h);
});
const strutMat = glossy("#2A2A35");
for (const a of [0, 2.1, 4.2]) {
  const s = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 1.1, 6), strutMat);
  s.position.set(0.35 * Math.cos(a), 0.75 + 0.35 * Math.sin(a), 0.6);
  s.lookAt(0, 0.75, 1.2);
  s.rotateX(Math.PI / 2);
  webb.add(s);
}
const sec = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.03, 12), gold);
sec.rotation.x = Math.PI / 2;
sec.position.set(0, 0.75, 1.15);
webb.add(sec);
const shieldMat = new THREE.MeshPhysicalMaterial({ color: "#C9B8FF", metalness: 0.7, roughness: 0.25, side: THREE.DoubleSide });
const kite = new THREE.Shape();
kite.moveTo(-1.6, 0); kite.lineTo(0, 0.85); kite.lineTo(1.6, 0); kite.lineTo(0, -0.85); kite.lineTo(-1.6, 0);
for (let i = 0; i < 5; i++) {
  const layer = new THREE.Mesh(new THREE.ShapeGeometry(kite), shieldMat);
  layer.rotation.x = -Math.PI / 2;
  layer.position.y = -0.05 - 0.06 * i;
  layer.scale.setScalar(1 - 0.03 * i);
  webb.add(layer);
}
webb.position.copy(L2_L);
rig.add(webb);
// the "P" parking sign
const pc = document.createElement("canvas");
pc.width = pc.height = 256;
{
  const c = pc.getContext("2d");
  c.fillStyle = "#1E5BD8";
  c.beginPath(); c.roundRect(8, 8, 240, 240, 40); c.fill();
  c.strokeStyle = "#FFFFFF"; c.lineWidth = 12; c.beginPath(); c.roundRect(24, 24, 208, 208, 30); c.stroke();
  c.fillStyle = "#FFFFFF"; c.font = "bold 190px sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("P", 128, 140);
}
const pTex = new THREE.CanvasTexture(pc);
pTex.colorSpace = THREE.SRGBColorSpace;
const pSign = new THREE.Sprite(new THREE.SpriteMaterial({ map: pTex, toneMapped: false }));
pSign.position.copy(L2_L).add(new THREE.Vector3(2.2, 0.4, 0));
rig.add(pSign);
// pulls on Webb: toward the Sun (yellow) and toward Earth (blue)
const pullSun = new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0), new THREE.Vector3(), 3, 0xffd23f, 0.8, 0.55);
const pullEarth = new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0), new THREE.Vector3(), 2, 0x4cc9f0, 0.7, 0.5);
pullSun.position.copy(L2_L).add(new THREE.Vector3(-0.7, 0, 0));
pullEarth.position.copy(L2_L).add(new THREE.Vector3(0.7, 0, 0));
rig.add(pullSun, pullEarth);
// distance bars: Earth -> Moon (white) and Earth -> L2 (gold), drawn to the side
const barMoon = new THREE.Mesh(new RoundedBoxGeometry(0.22, 1, 0.22, 2, 0.08), glossy("#FFFFFF"));
const barL2 = new THREE.Mesh(new RoundedBoxGeometry(0.22, 1, 0.22, 2, 0.08), gold);
barMoon.geometry.translate(0, -0.5, 0);
barL2.geometry.translate(0, -0.5, 0);
barMoon.position.copy(EARTH_L).add(new THREE.Vector3(-2.2, 0, 0));
barL2.position.copy(EARTH_L).add(new THREE.Vector3(-1.6, 0, 0));
rig.add(barMoon, barL2);
const keyL = new THREE.DirectionalLight(0xfff1e0, 1.4);
keyL.position.set(3, 6, 8);
epWorld.add(keyL);
const rigAng = (t) => (t < 11.55 ? 0 : 0.3 * inOutSine(seg(t, 12.2, 17.4)));
const toWorld = (p, t) => p.clone().applyAxisAngle(new THREE.Vector3(0, 0, 1), rigAng(t)).add(SUN_P);
const FOCUS = {
  webb: (t) => toWorld(L2_L.clone().add(new THREE.Vector3(0, 0.4, 0)), t),
  earthL2: (t) => toWorld(EARTH_L.clone().add(new THREE.Vector3(-0.6, -3.2, 0)), t),
};

function episodeRender(t, name) {
  const sky = skyAt(t);
  skyWebb.scale.setScalar(1.2 * (1 + 0.15 * Math.sin(TAU * 1.5 * t)));
  spoon.visible = spoonGlow.visible = t > 37.3 && t < 41.7;
  spoon.position.set(...sky.spoon);
  spoon.rotation.set(0.6, 0.8 * t, 0.3);
  spoonGlow.position.copy(spoon.position);
  key.intensity = name === "chair" ? 2.0 : 1.5;
  key.color.set(name === "chair" ? "#e8ecff" : "#fff1e0");

  rig.rotation.z = rigAng(t);
  bigSun.rotation.y = 0.3 * t;
  wEarth.rotation.y = 0.4 * t;
  const ma = 0.8 * t;
  wMoon.position.copy(EARTH_L).add(new THREE.Vector3(1.6 * Math.cos(ma), 1.6 * Math.sin(ma), 0));
  // Webb: big in the close-up, shrinks to a dot-sized icon in the diagram
  const out = inOutSine(seg(t, 4.6, 6.2));
  webb.scale.setScalar(t < 11.55 ? lerp(1, 0.9, out) : 0.9);
  webb.rotation.set(0.2, 0.3 + 0.08 * Math.sin(TAU * t / 6), 0);
  const p = outBack(seg(t, 5.8, 6.3), 1.8) * (1 - seg(t, 17.4, 17.7));
  pSign.visible = p > 0.01;
  pSign.scale.setScalar(1.6 * p);
  const arr = seg(t, 13.2, 13.6) * (1 - seg(t, 17.3, 17.6));
  pullSun.visible = pullEarth.visible = arr > 0.01;
  pullSun.setLength(5 * arr + 0.001, 1.2 * arr + 0.001, 0.9 * arr + 0.001);
  pullEarth.setLength(3.2 * arr + 0.001, 1.0 * arr + 0.001, 0.8 * arr + 0.001);
  // the bars grow on "चाँद से लगभग चार गुना दूर"
  const bm = outBack(seg(t, 18.6, 19.1), 1.3), bl = outBack(seg(t, 21.1, 21.7), 1.3);
  barMoon.visible = bm > 0.01;
  barL2.visible = bl > 0.01;
  barMoon.scale.set(1, Math.max(0.001, 1.6 * bm), 1);
  barL2.scale.set(1, Math.max(0.001, 6.4 * bl), 1);
  mOrbit.visible = t > 17.6;
}
"""

build(HERE, {
    "title": 'Challan #9 "No Parking: Webb Telescope"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#3E2A6E", "#120A2A"], "space": ["#1B2348", "#070A18"], "alt": ["#3E2A6E", "#120A2A"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})
print("T", {k: v for k, v in T.items() if k in ("T", "C", "S", "Z", "P", "shock")})
