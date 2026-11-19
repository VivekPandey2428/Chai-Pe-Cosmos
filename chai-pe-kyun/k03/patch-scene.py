"""Chai Pe Kyun? #3 "Chaand humare saath kyun chalta hai?": the Moon is so far away that its direction never changes.

v2 (virality pass): opens and ends on the night road (a mini Sahab on a scooter, the Moon behind him: "Inspector ka
pichha? Himmat toh dekho!") -> home: "about 3,84,000 km!" (3D number) -> the road again: trees and lamp posts race past,
the Moon stays put; sight lines: the tree line swings, the Moon line stays -> home: "Matlab chaand mera fan nahi hai?" ->
try it tonight -> comment bait (guess the Moon's speed), subscribe -> back on the road: "Sahab, chaand abhi bhi aapke
peeche hai..." with the next question as text only, looping into frame 0. Acting and camera: tools/cycle2_beats.kyun().
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import kyun, TWO

DUR = 34.15
SPACE = [[0, 5.86], [12.38, 18.55], [30.62, DUR]]  # the road: the hook, the explanation, and the loop back to frame 0
act, shots, T = kyun(HERE, {"dur": DUR, "space": SPACE, "screen": {"hook": "PICHHA?", "tease": "TAARE?"}, "tease_at": 30.75,
                         "extra_shots": [{"t": 9.35, "blend": 0.35, **TWO, "dist": 10.5}]})

nums = [{"value": 384000, "fly": 9.5, "land": 9.85, "lock": 10.8, "out": 12.25, "rim": "#C9D6FF"}]  # "about 3,84,000 km"
ROAD = {"look": [0.2, 2.7, 0], "dir": [0.22, 0.05, 1], "dist": 9.6}
space_shots = [
    {"t": 0, **ROAD, "to": {"dist": 9.0}},  # frame 0: the scooter, the Moon behind
    {"t": 12.38, **ROAD, "to": {"dist": 9.0}},
    {"t": 15.6, "blend": 0.9, "look": [0, 2.6, 0], "dir": [0, 1, 0.35], "dist": 14},  # from above: two sight lines
    {"t": 30.62, **ROAD, "to": {"dist": 9.0}},  # the loop: back to the frame-0 shot
]

WORLD = r"""
// ---- Chai Pe Kyun #3: the Moon over Sahab's shoulder at home; a night road with a scooter, trees, lamp posts
const skyMoon = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 4), glossy("#E6E9F2", { flatShading: true, roughness: 0.7 }));
const skyMoonGlow = new THREE.Sprite(haloMat("rgba(220,230,255,0.75)", "rgba(220,230,255,0)"));
skyMoon.position.set(2.6, 5.2, -7);
skyMoonGlow.position.copy(skyMoon.position);
skyMoonGlow.scale.setScalar(3.4);
chairWorld.add(skyMoon, skyMoonGlow);
function skyAt(t) { return { moon: skyMoon.position.toArray() }; }

const epWorld = new THREE.Group();
const road = new THREE.Mesh(new THREE.BoxGeometry(80, 0.1, 3), glossy("#3A3F55", { roughness: 0.8 }));
const grass = new THREE.Mesh(new THREE.BoxGeometry(80, 0.08, 30), glossy("#1F4A3C", { roughness: 0.9 }));
grass.position.y = -0.03;
const stripes = new THREE.InstancedMesh(new THREE.BoxGeometry(1.2, 0.02, 0.12), new THREE.MeshBasicMaterial({ color: "#FFE9A8" }), 20);
epWorld.add(grass, road, stripes);
// the scooter, standing still; the world slides past it
const scooter = new THREE.Group();
const body = new THREE.Mesh(new RoundedBoxGeometry(1.6, 0.5, 0.6, 3, 0.2), glossy("#FF3B5C"));
body.position.y = 0.6;
const front = new THREE.Mesh(new RoundedBoxGeometry(0.3, 1.0, 0.55, 3, 0.12), glossy("#FF3B5C"));
front.position.set(0.75, 0.95, 0);
const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.9, 8), glossy("#2A2A35"));
bar.rotation.x = Math.PI / 2;
bar.position.set(0.8, 1.5, 0);
const lamp = new THREE.Sprite(haloMat("rgba(255,240,180,1)", "rgba(255,240,180,0)"));
lamp.position.set(1.0, 1.15, 0);
lamp.scale.setScalar(0.8);
const WHEELS = [-0.55, 0.75].map((x) => {
  const w = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.12, 10, 24), glossy("#1D1D22"));
  w.position.set(x, 0.38, 0);
  scooter.add(w);
  return w;
});
scooter.add(body, front, bar, lamp);
const rider = makeCop();
rider.group.scale.setScalar(0.42);
rider.group.position.set(-0.15, 0.82, 0);
rider.group.rotation.y = Math.PI / 2;
scooter.add(rider.group);
epWorld.add(scooter);
// trees and lamp posts along the far side of the road
const SPEED = 9, SPAN = 48;
const PROPS = Array.from({ length: 10 }, (_, i) => {
  const g = new THREE.Group();
  if (i % 2 === 0) {
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, 1.4, 10), glossy("#7A4E2D"));
    trunk.position.y = 0.7;
    const top = new THREE.Mesh(new THREE.IcosahedronGeometry(0.9, 1), glossy("#3FAE6A", { flatShading: true }));
    top.position.y = 1.9;
    g.add(trunk, top);
  } else {
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 3, 8), glossy("#8C93A8"));
    pole.position.y = 1.5;
    const bulb = new THREE.Sprite(haloMat("rgba(255,220,140,1)", "rgba(255,200,100,0)"));
    bulb.position.y = 3.05;
    bulb.scale.setScalar(1.1);
    g.add(pole, bulb);
  }
  g.position.z = -2.4;
  epWorld.add(g);
  return { g, x0: i * (SPAN / 10) };
});
// the Moon: far up the sky, the same direction whatever happens
const MOON_P = new THREE.Vector3(-2.3, 6.0, -14);
const roadMoon = new THREE.Mesh(new THREE.IcosahedronGeometry(1.4, 4), glossy("#E6E9F2", { flatShading: true, roughness: 0.7 }));
roadMoon.position.copy(MOON_P);
const roadMoonGlow = new THREE.Sprite(haloMat("rgba(220,230,255,0.8)", "rgba(220,230,255,0)"));
roadMoonGlow.position.copy(MOON_P);
roadMoonGlow.scale.setScalar(7);
epWorld.add(roadMoon, roadMoonGlow);
// sight lines from the rider: to the Moon (stays) and to one tree (swings)
const lineMat = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, transparent: true, opacity: 0.95 });
const toMoon = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1, 8), lineMat("#BFD4FF"));
const toTree = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1, 8), lineMat("#7CFF9E"));
epWorld.add(toMoon, toTree);
const EYE = new THREE.Vector3(-0.15, 1.75, 0);
const UPV = new THREE.Vector3(0, 1, 0);
function lineBetween(m, a, b) {
  const d = b.clone().sub(a);
  m.position.copy(a).addScaledVector(d, 0.5);
  m.scale.set(1, d.length(), 1);
  m.quaternion.setFromUnitVectors(UPV, d.normalize());
}
const roadLight = new THREE.DirectionalLight(0xc8d6ff, 1.0);
roadLight.position.set(-3, 6, 5);
epWorld.add(roadLight);
const FOCUS = {};

function episodeRender(t, name) {
  const twinkle = t > 30.6 ? 1 : 0; // the next question (stars twinkle), as text over the last road shot
  skyMoon.rotation.y = 0.1 * t;
  stars.visible = true;
  stars.material.opacity = 0.8 + 0.2 * twinkle * Math.sin(TAU * 3 * t);
  // Sahab glances back at the Moon on the road ("पीछे-पीछे", "अभी भी आपके पीछे")
  const glance = Math.max(seg(t, 1.0, 1.3) * (1 - seg(t, 2.6, 2.9)), seg(t, 4.0, 4.3) * (1 - seg(t, 5.4, 5.7)), seg(t, 31.3, 31.6) * (1 - seg(t, 33.4, 33.8)));
  rider.group.rotation.y = Math.PI / 2 - 1.2 * inOutSine(glance);
  key.intensity = name === "chair" ? 1.7 : 1.4;
  key.color.set("#dfe6ff");

  // the road: everything near slides past; the Moon does not move
  const s = (t - 12.42) * SPEED;
  const st = new THREE.Object3D();
  for (let i = 0; i < 20; i++) {
    st.position.set((((i * 2.4 - s) % SPAN) + SPAN) % SPAN - SPAN / 2, 0.06, 0);
    st.updateMatrix();
    stripes.setMatrixAt(i, st.matrix);
  }
  stripes.instanceMatrix.needsUpdate = true;
  PROPS.forEach((p) => (p.g.position.x = (((p.x0 - s) % SPAN) + SPAN) % SPAN - SPAN / 2));
  WHEELS.forEach((w) => (w.rotation.z = -s / 0.4));
  scooter.position.y = 0.03 * Math.sin(TAU * 4 * t);
  // the sight lines appear on "...but something that far never changes direction" (16.0)
  const show = seg(t, 15.7, 16.1) * (t < 18.6 ? 1 : 0);
  toMoon.visible = toTree.visible = show > 0.01;
  const eye = EYE.clone().add(scooter.position);
  lineBetween(toMoon, eye, eye.clone().lerp(MOON_P, 0.92 * show));
  // follow the nearest tree that is still ahead (or just passed)
  const trees = PROPS.filter((p, i) => i % 2 === 0).map((p) => p.g);
  const tree = trees.reduce((a, b) => (Math.abs(b.position.x + 1) < Math.abs(a.position.x + 1) ? b : a));
  lineBetween(toTree, eye, eye.clone().lerp(tree.position.clone().add(new THREE.Vector3(0, 1.9, 0)), show));
}
"""

build(HERE, {
    "title": "Chai Pe Kyun #3: Chaand humare saath kyun chalta hai?",
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#2D3F8A", "#0B1030"], "space": ["#24346E", "#090D24"], "alt": ["#1A2156", "#05081A"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.9, 1.0],
})
# Indian grouping for the distance: 3,84,000
p = os.path.join(HERE, "assets/challan-scene.js")
js = open(p, encoding="utf-8").read().replace('toLocaleString("en-US")', 'toLocaleString("en-IN")')
open(p, "w", encoding="utf-8").write(js)

L = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
caps = [{"who": l["speaker"], "text": w["text"], "in": round(w["start"], 2), "out": round(w["end"], 2)} for l in L for w in l["words"]]
C, S, Z = T["C"], T["S"], T["Z"]
tags = [
    {"hook": True, "top": 300, "text": "Chaand pichha kyun karta?", "size": 110, "color": "#FFD23F", "in": 0.0, "out": 3.3},
    {"top": 300, "text": "INSPECTOR KA PICHHA?!", "size": 92, "color": "#FF4D5E", "in": 3.45, "out": 5.8},
    {"top": 330, "text": "Paas ka ped: tezi se peeche", "sub": "disha badal jaati hai", "color": "#7CFF9E", "in": 12.5, "out": 15.5},
    {"top": 330, "text": "Door ka chaand: disha same", "sub": "isliye saath chalta dikhta", "color": "#BFD4FF", "in": 15.7, "out": 18.5},
    {"top": 300, "text": "FAN NAHI HAI?!", "size": 96, "color": "#FF8FA3", "in": 18.7, "out": 20.8},
    {"top": 300, "text": "Aaj raat try karo!", "sub": "ped bhaagega, chaand wahin", "color": "#FFD23F", "in": 21.0, "out": 25.1},
    {"top": 300, "text": "Chaand ki speed?", "sub": "guess karo, comment karo!", "color": "#FFD23F", "in": C + 0.05, "out": S},
    {"top": 300, "text": "Subscribe karo", "sub": "roz ek naya sawaal", "in": S + 0.02, "out": round(S + 0.95, 2)},
    {"top": 300, "text": "Agla sawaal:", "sub": "taare tim-timate kyun?", "color": "#FFD23F", "in": 30.8, "out": 33.6},
]
json.dump({"title": "Chaand humare saath kyun chalta hai?", "duration": DUR, "scene_note": "Chai Pe Kyun? #3: why the Moon follows you.",
           "caps": [{"unit": "km", "label": "chaand itna door!", "in": 9.9, "out": 12.25}], "tags": tags, "captions": caps,
           "end": {"lines": [], "at": 99}}, open(os.path.join(HERE, "story.json"), "w"), ensure_ascii=False, indent=1)
print("T", {k: v for k, v in T.items() if k != "L"})
