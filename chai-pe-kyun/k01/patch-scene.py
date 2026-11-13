"""Chai Pe Kyun? #1 "Aasmaan neela kyun hai?": sunlight holds every colour; air scatters blue the most.

A bright blue sky at home, both looking up -> a prism splits a white sunbeam into a rainbow -> air particles knock the
blue light every which way while red and yellow fly straight on -> home: "the whole sky fills with blue!" -> the try-it
beat: a glass of milky water and a torch, glowing blue from the side -> comment, subscribe, teaser (the sky warms), loop.
Acting and camera: tools/cycle2_beats.kyun(); machinery: tools/cycle2_patch.py. Also writes story.json from the lines.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import kyun

DUR = 34.2
SPACE = [[4.35, 14.6], [17.2, 22.75]]
act, shots, T = kyun(HERE, {"dur": DUR, "space": SPACE, "screen": {"hook": "NEELA?", "tease": "LAAL?"}, "alt": [[27.4, 32.0]]})

space_shots = [
    {"t": 4.35, "look": [0.8, 0, 0], "dir": [0, 0.15, 1], "dist": 11},  # the prism and the rainbow
    {"t": 9.3, "look": [0, 0, 0], "dir": [0.1, 0.2, 1], "dist": 12},  # air particles scatter blue
    {"t": 17.2, "look": [-0.6, 0.0, 0], "dir": [0.15, 0.2, 1], "dist": 10},  # milky water and a torch
]

WORLD = r"""
// ---- Chai Pe Kyun #1: a daytime Sun at home; in the lab, a prism, scattering air, and a glass of milky water
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,240,200,0.9)", "rgba(255,240,200,0)"));
skySun.position.set(-2.8, 5.6, -7);
skySun.scale.setScalar(0.8);
skySunHalo.position.copy(skySun.position);
skySunHalo.scale.setScalar(4.5);
chairWorld.add(skySun, skySunHalo);
function skyAt(t) { return {}; }

const epWorld = new THREE.Group();
const glow = (hex) => new THREE.MeshBasicMaterial({ color: hex, toneMapped: false });
// A: the prism
const prismG = new THREE.Group();
const beamIn = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 1, 12), glow("#FFFFFF"));
beamIn.rotation.z = Math.PI / 2;
const prism = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 1.8, 3), new THREE.MeshPhysicalMaterial({ color: "#E8F6FF", transmission: 0.6, roughness: 0.05, thickness: 1, clearcoat: 1, transparent: true, opacity: 0.75 }));
prism.rotation.x = Math.PI / 2;
const RAINBOW = ["#FF3B3B", "#FF8C1A", "#FFE14D", "#4CD964", "#2E86FF", "#8A4DFF"];
const fan = RAINBOW.map((c, i) => {
  const b = new THREE.Mesh(new THREE.BoxGeometry(1, 0.14, 0.14), glow(c));
  b.geometry.translate(0.5, 0, 0);
  b.rotation.z = -0.12 - 0.07 * i;
  b.position.set(0.6, 0, 0);
  prismG.add(b);
  return b;
});
prismG.add(beamIn, prism);
epWorld.add(prismG);
// B: air particles and light
const airG = new THREE.Group();
const rndA = mulberry32(17);
const MOL = Array.from({ length: 34 }, () => {
  const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.16, 1), glossy("#DDE6F5", { roughness: 0.4 }));
  m.position.set(-5 + 10 * rndA(), -3 + 6 * rndA(), -1 + 2 * rndA());
  airG.add(m);
  return m;
});
const PHOT = Array.from({ length: 30 }, (_, i) => {
  const c = ["#2E86FF", "#FF3B3B", "#FFE14D"][i % 3];
  const s = new THREE.Sprite(haloMat(c === "#2E86FF" ? "rgba(70,150,255,1)" : c === "#FF3B3B" ? "rgba(255,80,80,1)" : "rgba(255,225,80,1)", "rgba(0,0,0,0)"));
  s.scale.setScalar(0.85);
  airG.add(s);
  const a = rndA() * TAU;
  return { s, blue: i % 3 === 0, y: -2.6 + 5.2 * rndA(), ph: rndA(), hit: -2 + 4 * rndA(), dir: new THREE.Vector3(Math.cos(a), Math.sin(a), 0.4 * (rndA() - 0.5)) };
});
epWorld.add(airG);
// C: milky water and a torch
const milkG = new THREE.Group();
const glass = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 0.85, 2.6, 32, 1, true), new THREE.MeshPhysicalMaterial({ color: "#FFFFFF", transparent: true, opacity: 0.25, roughness: 0.05, side: THREE.DoubleSide }));
const water = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.82, 2.1, 32), new THREE.MeshPhysicalMaterial({ color: "#F4F8FF", transparent: true, opacity: 0.6, roughness: 0.3 }));
water.position.y = -0.22;
const torch = new THREE.Group();
const tBody = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 1.2, 16), glossy("#2A2A35"));
tBody.rotation.z = Math.PI / 2;
const tHead = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.24, 0.35, 16), glossy("#FFC300"));
tHead.rotation.z = Math.PI / 2;
tHead.position.x = 0.7;
torch.add(tBody, tHead);
torch.position.set(-3.2, -0.2, 0);
const tBeam = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.55, 1, 20, 1, true), new THREE.MeshBasicMaterial({ color: "#FFF6D0", toneMapped: false, transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
tBeam.geometry.translate(0, 0.5, 0);
tBeam.rotation.z = -Math.PI / 2;
tBeam.position.set(-2.3, -0.2, 0);
const blueGlow = new THREE.Sprite(haloMat("rgba(60,140,255,1)", "rgba(60,140,255,0)"));
blueGlow.position.set(0, -0.2, 0.6);
const orangeGlow = new THREE.Sprite(haloMat("rgba(255,160,60,0.9)", "rgba(255,140,40,0)"));
orangeGlow.position.set(1.6, -0.2, 0);
milkG.add(water, glass, torch, tBeam, blueGlow, orangeGlow);
epWorld.add(milkG);
const labLight = new THREE.DirectionalLight(0xffffff, 1.2);
labLight.position.set(2, 4, 6);
epWorld.add(labLight);
const FOCUS = {};

function episodeRender(t, name) {
  const dusk = mood(t, ACT.alt, 0.6);
  skySun.position.y = 5.6 - 3.0 * dusk;
  skySunHalo.position.copy(skySun.position);
  skySun.rotation.y = 0.3 * t;
  key.intensity = 2.3;
  key.color.set(dusk > 0.5 ? "#ffd2a8" : "#fff1e0");
  if (name === "chair") stars.visible = false;
  // A
  prismG.visible = t >= 4.3 && t < 9.3;
  const bin = outExpo(seg(t, 4.5, 5.2));
  beamIn.scale.set(1, 6 * bin + 0.001, 1);
  beamIn.position.set(-6 + 3 * bin - 0.6, 0, 0);
  prism.rotation.y = 0.2 * Math.sin(TAU * t / 6);
  const f = outExpo(seg(t, 7.0, 7.6)); // "धूप में सारे रंग छुपे हैं"
  fan.forEach((b) => (b.scale.set(6 * f + 0.001, 1, 1), (b.visible = f > 0.01)));
  // B
  airG.visible = t >= 9.3 && t < 14.6;
  MOL.forEach((m, i) => m.position.setY(m.position.y + 0.002 * Math.sin(t * 3 + i)));
  PHOT.forEach((p) => {
    const u = (((t - 9.3) / 2.2 + p.ph) % 1 + 1) % 1;
    const x = -6 + 12 * u;
    if (p.blue && x > p.hit) {
      const k = x - p.hit;
      p.s.position.set(p.hit, p.y, 0).addScaledVector(p.dir, k * 1.1);
    } else p.s.position.set(x, p.y, 0);
  });
  // C
  milkG.visible = t >= 17.2 && t < 22.8;
  const on = outExpo(seg(t, 19.3, 19.6)); // "torch मारो"
  tBeam.scale.set(1, 4.6 * on + 0.001, 1);
  tBeam.visible = on > 0.01;
  const side = seg(t, 20.3, 20.9); // "side से नीला"
  blueGlow.visible = orangeGlow.visible = on > 0.01;
  blueGlow.scale.setScalar(0.6 + 4.2 * side);
  orangeGlow.scale.setScalar(1.6 * on);
  water.material.color.set(side > 0.5 ? "#9CC8FF" : "#F4F8FF");
  milkG.rotation.y = 0.25 * Math.sin(TAU * t / 8);
}
"""

build(HERE, {
    "title": "Chai Pe Kyun #1: Aasmaan neela kyun hai?",
    "dur": DUR, "space": SPACE, "nums": [], "act": act,
    "bg": {"home": ["#9FDBFF", "#2E86DE"], "space": ["#1B2348", "#070A18"], "alt": ["#FFB385", "#7A2E5C"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})

# story.json: captions from the phrase timings, plus the on-screen tags
L = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
caps = [{"who": l["speaker"], "text": w["text"], "in": round(w["start"], 2), "out": round(w["end"], 2)} for l in L for w in l["words"]]
C, S, Z = T["C"], T["S"], T["Z"]
tags = [
    {"hook": True, "top": 300, "text": "Aasmaan neela kyun?", "size": 120, "color": "#FFD23F", "in": 0.0, "out": 2.9},
    {"top": 330, "text": "Dhoop = saare rang", "sub": "safed roshni mein rainbow", "in": 7.1, "out": 9.15},
    {"top": 330, "text": "Neela sabse zyada bikharta", "sub": "isliye aasmaan neela", "color": "#7FD8FF", "in": 11.2, "out": 14.5},
    {"top": 330, "text": "Ghar pe try karo!", "sub": "paani + 2 boond doodh + torch", "color": "#FFD23F", "in": 17.3, "out": 22.6},
    {"top": 300, "text": "Chaand pe aasmaan?", "sub": "kis rang ka? Comment karo!", "color": "#FFD23F", "in": C + 0.05, "out": S},
    {"top": 300, "text": "Subscribe karo", "sub": "roz ek naya sawaal", "in": S + 0.02, "out": round(S + 0.95, 2)},
    {"top": 300, "text": "Agla sawaal:", "sub": "shaam ko suraj laal kyun?", "color": "#FFD23F", "in": round(S + 1.0, 2), "out": 31.7},
]
json.dump({"title": "Aasmaan neela kyun hai?", "duration": DUR, "scene_note": "Chai Pe Kyun? #1: why the sky is blue.",
           "caps": [], "tags": tags, "captions": caps, "end": {"lines": [], "at": 99}}, open(os.path.join(HERE, "story.json"), "w"),
          ensure_ascii=False, indent=1)
print("T", {k: v for k, v in T.items() if k != "L"})
