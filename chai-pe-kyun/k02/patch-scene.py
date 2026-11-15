"""Chai Pe Kyun? #2 "Shaam ko suraj laal kyun?": at sunset, light crosses far more air and loses its blue on the way.

Sunset at home, a big orange Sun on the horizon -> side view of Earth and its air layer: a short straight beam at noon,
a long slanting beam at sunset, blue dots peeling off it so only red-orange arrives -> home: "the blue got off on the
way!" -> comment, subscribe, teaser (night falls, the Moon rises), loop. Acting and camera: tools/cycle2_beats.kyun().
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import kyun

DUR = 33.85
SPACE = [[7.18, 17.72]]
act, shots, T = kyun(HERE, {"dur": DUR, "space": SPACE, "screen": {"hook": "LAAL?", "tease": "CHAAND?"}, "alt": [[27.1, 31.0]]})
# the punchline: "नीले का तो challan बनता है!" - the radar gun reads CHALLAN
act["cop"]["screen"] = sorted(act["cop"]["screen"] + [[17.9, "CHALLAN!", 1], [21.3, "LAAL?", 0]], key=lambda k: k[0])

nums = [{"value": 40, "fly": 10.62, "land": 10.92, "lock": 11.7, "out": 12.25, "rim": "#FF8A3D"}]  # "लगभग चालीस गुना"

space_shots = [
    {"t": 7.18, "look": [0, 0, 0], "dir": [0, 0.05, 1], "dist": 24},  # Earth's air layer, noon and sunset beams
    {"t": 12.3, "blend": 1.0, "look": [-1.0, -0.3, 0], "dir": [0.05, 0.08, 1], "dist": 21},  # blue gets off the long beam
]

WORLD = r"""
// ---- Chai Pe Kyun #2: a low orange Sun at home (the Moon rises for the teaser); Earth's air and two sunbeams
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,120,40,0.95)", "rgba(255,80,20,0)"));
const skyMoon = new THREE.Mesh(new THREE.IcosahedronGeometry(0.45, 4), glossy("#C9CEDC", { flatShading: true, roughness: 0.7 }));
const skyMoonGlow = new THREE.Sprite(haloMat("rgba(220,230,255,0.6)", "rgba(220,230,255,0)"));
chairWorld.add(skySun, skySunHalo, skyMoon, skyMoonGlow);
function skyAt(t) { return {}; }

const epWorld = new THREE.Group();
const EARTH_C = new THREE.Vector3(0, -3.56, 0), ER = 2.8, AR = 4.6;
const bigEarth = makeEarth(ER);
bigEarth.position.copy(EARTH_C);
const air = new THREE.Mesh(new THREE.SphereGeometry(AR, 64, 32), new THREE.MeshBasicMaterial({ color: "#8FD0FF", transparent: true, opacity: 0.34, depthWrite: false, toneMapped: false }));
air.position.copy(EARTH_C);
const OBS = new THREE.Vector3(0, -0.76, 0); // where we stand, on top of the Earth
const you = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.5, 12), glossy("#FFD23F"));
you.position.copy(OBS).add(new THREE.Vector3(0, 0.25, 0));
epWorld.add(air, bigEarth, you);
const glowMat = (c, o) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, transparent: true, opacity: o, blending: THREE.AdditiveBlending, depthWrite: false });
// noon: straight down through a thin layer of air
const noonSun = new THREE.Sprite(haloMat("rgba(255,250,220,1)", "rgba(255,230,150,0)"));
noonSun.position.set(0, 2.5, 0);
noonSun.scale.setScalar(3);
const noonBeam = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 1, 12), glowMat("#FFFBE6", 0.9));
epWorld.add(noonSun, noonBeam);
// sunset: a long slanting path through the air
const SET_FROM = new THREE.Vector3(-3.9, -0.6, 0);
const setSun = new THREE.Sprite(haloMat("rgba(255,170,80,1)", "rgba(255,120,40,0)"));
setSun.position.copy(SET_FROM);
setSun.scale.setScalar(2.6);
const SEGS = 14;
const setBeam = Array.from({ length: SEGS }, (_, i) => {
  const u = (i + 0.5) / SEGS;
  const c = new THREE.Color("#FFF8E8").lerp(new THREE.Color("#FF3A00"), Math.pow(u, 0.7));
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 1, 10), new THREE.MeshBasicMaterial({ color: c, toneMapped: false, depthTest: false }));
  m.renderOrder = 5;
  m.rotation.z = Math.atan2(OBS.y - SET_FROM.y, OBS.x - SET_FROM.x) - Math.PI / 2;
  m.userData.u = u;
  epWorld.add(m);
  return m;
});
epWorld.add(setSun);
const arrive = new THREE.Sprite(haloMat("rgba(255,110,30,1)", "rgba(255,80,20,0)"));
arrive.position.copy(OBS);
epWorld.add(arrive);
const rndP = mulberry32(29);
const PHOT = Array.from({ length: 26 }, (_, i) => {
  const blue = i % 2 === 0;
  const s = new THREE.Sprite(haloMat(blue ? "rgba(80,170,255,1)" : "rgba(255,140,60,1)", "rgba(0,0,0,0)"));
  s.scale.setScalar(blue ? 1.15 : 0.6);
  epWorld.add(s);
  const a = (rndP() < 0.5 ? 1 : -1) * (0.6 + 0.9 * rndP());
  return { s, blue, ph: i / 26, out: 0.25 + 0.5 * rndP(), dir: new THREE.Vector3(0.3, Math.sin(a), Math.cos(a) * 0.6) };
});
const FOCUS = {};

function episodeRender(t, name) {
  const night = mood(t, ACT.alt, 0.6);
  skySun.position.set(-2.6, 2.6 - 3.5 * night, -7);
  skySun.scale.setScalar(1.25);
  skySun.rotation.y = 0.3 * t;
  skySun.material.color.setRGB(1, 0.7, 0.55);
  skySunHalo.position.copy(skySun.position);
  skySunHalo.scale.setScalar(7.5 * (1 - 0.6 * night));
  // the Moon rises for the teaser and fades out in place (it must not slide down past Sahab)
  const rise = outBack(seg(t, 27.3, 28.3), 1.2);
  const fade = 1 - seg(t, 30.7, 31.2);
  skyMoon.visible = skyMoonGlow.visible = rise > 0.01 && fade > 0.01;
  skyMoon.position.set(2.2, lerp(1.0, 5.4, rise), -7);
  skyMoon.scale.setScalar(Math.max(0.001, fade));
  skyMoonGlow.material.opacity = fade;
  skyMoonGlow.position.copy(skyMoon.position);
  skyMoonGlow.scale.setScalar(2.6);
  if (name === "chair") stars.visible = night > 0.3;
  key.intensity = name === "chair" ? lerp(2.2, 1.6, night) : 1.6;
  key.color.set(name === "chair" ? (night > 0.5 ? "#e8ecff" : "#ffc89a") : "#fff1e0");

  bigEarth.rotation.y = 0.05 * t;
  // the noon beam for comparison, the sunset beam on "शाम को धूप तिरछी" (both stay through "40 गुना")
  const noon = outExpo(seg(t, 7.3, 7.8)) * (1 - seg(t, 12.1, 12.4));
  noonSun.visible = noonBeam.visible = noon > 0.01;
  const top = new THREE.Vector3(0, 2.3, 0);
  noonBeam.position.copy(top).lerp(OBS, 0.5 * noon);
  noonBeam.scale.set(1, top.distanceTo(OBS) * noon + 0.001, 1);
  noonBeam.position.y = top.y - (top.y - OBS.y) * noon * 0.5;
  const set = outExpo(seg(t, 7.9, 8.8));
  setSun.visible = set > 0.01;
  const len = SET_FROM.distanceTo(OBS);
  const dir = OBS.clone().sub(SET_FROM).normalize();
  setBeam.forEach((m) => {
    const u = m.userData.u;
    m.visible = set > u;
    m.position.copy(SET_FROM).addScaledVector(dir, len * u);
    m.scale.set(1, len / SEGS + 0.02, 1);
  });
  // photons ride the sunset beam; the blue ones are knocked out of it on the way ("नीला ... उतर जाता है")
  const pOn = t > 12.3 && t < 17.8;
  const arr = seg(t, 15.9, 16.4);
  arrive.visible = arr > 0.01 && t < 17.8;
  arrive.scale.setScalar(2.6 * arr * (1 + 0.08 * Math.sin(TAU * 2 * t)));
  PHOT.forEach((p) => {
    p.s.visible = pOn && p.blue; // the beam itself carries the warm colours; warm sprites piled on it read as white
    if (!pOn) return;
    const u = (((t - 12.3) / 2.2 + p.ph) % 1 + 1) % 1;
    const along = SET_FROM.clone().addScaledVector(dir, len * u);
    if (p.blue && u > p.out) p.s.position.copy(SET_FROM).addScaledVector(dir, len * p.out).addScaledVector(p.dir, (u - p.out) * 4);
    else p.s.position.copy(along);
    p.s.material.opacity = p.blue && u > p.out ? 1 - seg(u, p.out, p.out + 0.3) : 1;
  });
}
"""

build(HERE, {
    "title": "Chai Pe Kyun #2: Shaam ko suraj laal kyun?",
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#FF9E6B", "#5A2A6E"], "space": ["#1B2348", "#070A18"], "alt": ["#3E2A6E", "#120A2A"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 1.0],
})

L = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
caps = [{"who": l["speaker"], "text": w["text"], "in": round(w["start"], 2), "out": round(w["end"], 2)} for l in L for w in l["words"]]
C, S, Z = T["C"], T["S"], T["Z"]
tags = [
    {"hook": True, "top": 300, "text": "Suraj laal kyun?", "size": 120, "color": "#FFD23F", "in": 0.0, "out": 2.9},
    {"top": 330, "text": "Shaam: tirchhi dhoop", "sub": "dopahar: seedhi", "color": "#FFB385", "in": 7.4, "out": 10.5},
    {"top": 330, "text": "Neela raaste mein utar gaya", "sub": "sirf laal-narangi pahuncha", "color": "#FFB385", "in": 14.5, "out": 17.6},
    {"top": 300, "text": "NEELE KA CHALLAN!", "size": 96, "color": "#FF4D5E", "in": 17.9, "out": 21.2},
    {"top": 300, "text": "Mars = LAAL planet", "sub": "wahan sunset kis rang ka? Comment!", "color": "#FFD23F", "in": C + 0.05, "out": S},
    {"top": 300, "text": "Subscribe karo", "sub": "roz ek naya sawaal", "in": S + 0.02, "out": round(S + 0.95, 2)},
    {"top": 300, "text": "Agla sawaal:", "sub": "chaand saath kyun chalta hai?", "color": "#FFD23F", "in": round(S + 1.0, 2), "out": 30.9},
]
json.dump({"title": "Shaam ko suraj laal kyun?", "duration": DUR, "scene_note": "Chai Pe Kyun? #2: why the Sun is red at sunset.",
           "caps": [{"unit": "GUNA", "label": "dopahar se zyada hawa!", "in": 10.95, "out": 12.2}], "tags": tags, "captions": caps, "end": {"lines": [], "at": 99}}, open(os.path.join(HERE, "story.json"), "w"),
          ensure_ascii=False, indent=1)
print("T", {k: v for k, v in T.items() if k != "L"})
