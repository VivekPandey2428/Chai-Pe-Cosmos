"""Challan #10 "Wazan Ka Challan 2: Ek Chammach": a callback to #2; a teaspoon of neutron star on the weighing scale.

Opens at home: a glowing teaspoon on a bathroom scale, the display goes haywire, 100 crore+ tonnes lands -> whip to a
pulsar (beams sweeping) -> a big star collapses into it, then a city grid beside it for scale -> snap home: "chammach
wapas karo!" -> "uthaoge kaise?": he tries, the planet tilts -> trombone, chai, end card -> comment -> subscribe ->
teaser ("aap batao!", a glowing question mark) -> loop to the spoon. Acting and camera come from tools/cycle2_beats.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import standard

DUR = 34.05
SPACE = [[5.6, 17.38]]
act, shots, T = standard(HERE, {"dur": DUR, "space": SPACE, "hook": "spoon", "tease": "ask", "low": ["spoon"], "beam": True,
                                "screen": {"hook": "100 CR TON", "punch": "HEAVY!", "tease": "AAP?"},
                                "extra_shots": [{"t": 19.8, "look": [0.4, 1.7, 0.9], "dir": [0.1, 0.35, 1], "dist": 7.5}, {"t": 1.9, "blend": 0.5, "look": [0.2, 1.3, 1.2], "dir": [0.05, 0.55, 1], "dist": 6.5}]})
# "उठाओगे कैसे?": he bends for the spoon with his free hand and strains
hl = act["cop"]["handL"]
hl += [[19.3, "HIP"], [19.6, [0.05, 0.95, 1.05], "back"], [20.9, [0.05, 1.0, 1.05]], [21.15, "HIP"]]
hl.sort(key=lambda k: k[0])
act["cop"]["mood"]["confused"].append([19.5, 20.95])

nums = [
    {"value": 100, "plus": True, "fly": 1.7, "land": 2.04, "lock": 3.0, "out": 5.3, "rim": "#B983FF"},  # "सौ करोड़ टन से ज़्यादा"
]
space_shots = [
    {"t": 5.6, "look": [0, 0, 0], "dir": [0.2, 0.25, 1], "dist": 9},  # the pulsar, beams sweeping
    {"t": 11.8, "blend": 0.6, "look": [0, 0, 0], "dir": [0.1, 0.2, 1], "dist": 16},  # the big star before it died
    {"t": 15.3, "blend": 0.9, "look": [0.7, -0.35, 0], "dir": [0.1, 0.55, 1], "dist": 6.0},  # a city for scale
]

WORLD = r"""
// ---- Challan #10: a bathroom scale with a glowing teaspoon at home, a "?" for the teaser; in space, a pulsar
const SCALE = [0.15, -groundDrop(0.15, 1.75) + 0.02, 1.75];
const scaleG = new THREE.Group();
const sBody = new THREE.Mesh(new RoundedBoxGeometry(0.95, 0.13, 0.75, 3, 0.05), glossy("#F4FBFF", { roughness: 0.25 }));
sBody.position.y = 0.065;
const sc = document.createElement("canvas");
sc.width = 256; sc.height = 96;
const sTex = new THREE.CanvasTexture(sc);
sTex.colorSpace = THREE.SRGBColorSpace;
const sDisp = new THREE.Mesh(new THREE.PlaneGeometry(0.42, 0.16), new THREE.MeshBasicMaterial({ map: sTex, toneMapped: false }));
sDisp.rotation.x = -Math.PI / 2;
sDisp.position.set(0, 0.135, 0.2);
let lastDisp = "";
function drawDisp(text, red) {
  if (text + red === lastDisp) return;
  lastDisp = text + red;
  const c = sc.getContext("2d");
  c.fillStyle = "#0E1A12"; c.fillRect(0, 0, 256, 96);
  c.fillStyle = red ? "#FF4D4D" : "#62FF8E";
  c.font = `bold ${Math.min(72, Math.floor(420 / text.length))}px monospace`;
  c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(text, 128, 50);
  sTex.needsUpdate = true;
}
const spoonG = new THREE.Group();
const steel = glossy("#E6EAF2", { metalness: 0.9, roughness: 0.15 });
const bowl = new THREE.Mesh(new THREE.SphereGeometry(0.11, 20, 14), steel);
bowl.scale.set(1, 0.35, 1.4);
const handle = new THREE.Mesh(new THREE.CapsuleGeometry(0.02, 0.36, 4, 10), steel);
handle.rotation.x = Math.PI / 2;
handle.position.z = 0.3;
const goo = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 10), new THREE.MeshBasicMaterial({ color: "#D9E8FF", toneMapped: false }));
goo.scale.set(1, 0.4, 1.2);
goo.position.y = 0.02;
spoonG.add(bowl, handle, goo);
spoonG.position.set(-0.1, 0.17, -0.1);
spoonG.rotation.y = 0.5;
const spoonGlow = new THREE.Sprite(haloMat("rgba(190,220,255,0.95)", "rgba(150,190,255,0)"));
spoonGlow.scale.setScalar(0.9);
spoonGlow.position.copy(spoonG.position).add(new THREE.Vector3(0, 0.05, 0));
scaleG.add(sBody, sDisp, spoonG, spoonGlow);
scaleG.position.set(...SCALE);
chairWorld.add(scaleG);
const qc = document.createElement("canvas");
qc.width = qc.height = 256;
{
  const c = qc.getContext("2d");
  c.fillStyle = "#FFD23F"; c.font = "bold 220px sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("?", 128, 140);
}
const qTex = new THREE.CanvasTexture(qc);
qTex.colorSpace = THREE.SRGBColorSpace;
const qMark = new THREE.Sprite(new THREE.SpriteMaterial({ map: qTex, toneMapped: false, transparent: true }));
const qGlow = new THREE.Sprite(haloMat("rgba(255,210,63,0.7)", "rgba(255,210,63,0)"));
chairWorld.add(qGlow, qMark);
function skyAt(t) {
  const rise = outBack(seg(t, 27.5, 28.4), 1.3) * (1 - inOutSine(seg(t, 29.9, 30.4)));
  return { spoon: [SCALE[0] - 0.1, SCALE[1] + 0.2, SCALE[2] - 0.1], ask: [0.4, lerp(1.0, 5.2, rise), -6] };
}

// space: a pulsar (tiny, blinding, two sweeping beams), the big star it came from, and a city grid for scale
const epWorld = new THREE.Group();
const ns = new THREE.Mesh(new THREE.IcosahedronGeometry(0.5, 4), new THREE.MeshBasicMaterial({ color: "#E8F1FF", toneMapped: false }));
const nsHalo = new THREE.Sprite(haloMat("rgba(170,200,255,1)", "rgba(120,150,255,0)"));
nsHalo.scale.setScalar(3.2);
const beamMat = new THREE.MeshBasicMaterial({ color: "#9FC2FF", toneMapped: false, transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
const beams = new THREE.Group();
for (const s of [1, -1]) {
  const b = new THREE.Mesh(new THREE.ConeGeometry(0.9, 9, 24, 1, true), beamMat);
  b.geometry.translate(0, -4.5, 0);
  b.rotation.x = s > 0 ? Math.PI : 0;
  beams.add(b);
}
beams.rotation.z = 0.5;
const spinAxis = new THREE.Group();
spinAxis.add(beams);
const giant = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const giantHalo = new THREE.Sprite(haloMat("rgba(255,90,40,0.8)", "rgba(255,60,20,0)"));
const flash = new THREE.Sprite(haloMat("rgba(255,255,255,1)", "rgba(200,220,255,0)"));
// the city: a disc of little buildings the same width as the star
const city = new THREE.Group();
const ground = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.03, 40), glossy("#3A3F55", { roughness: 0.8 }));
city.add(ground);
const rndC = mulberry32(31);
const bld = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), glossy("#C9D6FF", { roughness: 0.4 }), 90);
{
  const o = new THREE.Object3D();
  let n = 0;
  for (let gx = -5; gx <= 5; gx++) for (let gz = -5; gz <= 5; gz++) {
    const x = gx * 0.105, z = gz * 0.105;
    if (Math.hypot(x, z) > 0.56 || n >= 90 || (gx % 3 === 0) || (gz % 3 === 0)) continue;
    const h = 0.03 + 0.12 * rndC() * rndC();
    o.position.set(x, 0.015 + h / 2, z);
    o.scale.set(0.07, h, 0.07);
    o.updateMatrix();
    bld.setMatrixAt(n++, o.matrix);
  }
  bld.count = n;
}
city.add(bld);
city.position.set(1.35, -0.55, 0);
epWorld.add(giantHalo, giant, ns, nsHalo, spinAxis, flash, city);
const FOCUS = {};

function episodeRender(t, name) {
  // home: the scale's display panics while the spoon is on it; it shakes when the cop tries to lift it
  const sky = skyAt(t);
  const hook = t < 5.6 || t > 32.0;
  drawDisp(hook ? (Math.floor(t * 6) % 2 ? "ERROR" : "999999") : t > 19.4 && t < 21.0 ? "HEAVY!" : "ERROR", hook || (t > 19.4 && t < 21.0));
  spoonGlow.scale.setScalar(0.9 * (1 + 0.15 * Math.sin(TAU * 3 * t)));
  const strain = smooth(19.6, 19.9, t) * (1 - smooth(20.9, 21.2, t));
  scaleG.position.x = SCALE[0] + 0.02 * Math.sin(t * 60) * strain;
  chairWorld.rotation.z = -0.07 * strain; // the whole little planet tips toward the spoon
  qMark.visible = qGlow.visible = t > 27.4 && t < 30.5;
  qMark.position.set(...sky.ask);
  qMark.scale.setScalar(1.6);
  qGlow.position.copy(qMark.position);
  qGlow.scale.setScalar(3.0);
  key.intensity = name === "chair" ? 2.0 : 1.0;
  key.color.set(name === "chair" ? "#e8ecff" : "#fff1e0");

  // space: the pulsar spins fast; from 11.9 the big star is shown, collapses at 13.1 (flash) back into the pulsar
  const gOn = t >= 11.9 && t < 13.25;
  const collapse = inCubic(seg(t, 12.6, 13.15));
  giant.visible = giantHalo.visible = gOn;
  giant.scale.setScalar(lerp(3.2, 0.3, collapse) * outBack(seg(t, 11.9, 12.2), 1.2));
  giant.rotation.y = 0.2 * t;
  giant.material.color.setRGB(1, lerp(0.55, 1, collapse), lerp(0.4, 1, collapse));
  giantHalo.scale.setScalar(lerp(11, 1, collapse));
  const fl = seg(t, 13.1, 13.6);
  flash.visible = fl > 0 && fl < 1;
  flash.scale.setScalar(14 * Math.sin(Math.PI * fl));
  const nsOn = !gOn;
  ns.visible = nsHalo.visible = spinAxis.visible = nsOn;
  spinAxis.rotation.y = TAU * 1.6 * t; // fast spin, the beams sweep like a lighthouse
  nsHalo.scale.setScalar(3.2 * (1 + 0.08 * Math.sin(TAU * 4 * t)));
  const cityOn = outBack(seg(t, 15.4, 15.9), 1.4);
  city.visible = cityOn > 0.01;
  city.scale.setScalar(Math.max(0.001, cityOn));
}
"""

build(HERE, {
    "title": 'Challan #10 "Wazan Ka Challan 2: Ek Chammach"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#3E2A6E", "#120A2A"], "space": ["#141030", "#05040E"], "alt": ["#3E2A6E", "#120A2A"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})
print("T", {k: v for k, v in T.items() if k in ("T", "C", "S", "Z", "P", "shock")})
