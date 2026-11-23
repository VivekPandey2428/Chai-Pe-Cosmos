"""Chai Pe Kyun? #4 "Taare tim-timate kyun?": starlight is jolted by moving warm and cold air; planets, being little
discs, barely twinkle.

Night at home, one star winking at Sahab ("Mujhe signal de raha hai kya?") -> "Aankh nahi maar raha sahab, hawa naach
rahi hai!" -> side view: a far star (40 lakh crore km, as text), its thin ray wobbling through drifting warm and cold
air bubbles down to an eye; the star flickers -> home: "Hawa ka challan banta hai!" -> the try-it: a steady planet
beside the twinkling star -> comment bait (brightest star? Dhruv tara? it's Sirius), subscribe -> "Sahab, dekho... phir
aankh maari!" with the next question as text only, looping into frame 0. Acting and camera: tools/cycle2_beats.kyun().
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build
from cycle2_beats import kyun, SKY_LOW

DUR = 33.88
SPACE = [[7.72, 15.55]]
act, shots, T = kyun(HERE, {"dur": DUR, "space": SPACE, "screen": {"hook": "WINK?", "tease": "TAARE?"}, "tease_at": 30.85,
                         # the try-it: a wide shot of the sky, the planet steady beside the twinkling star
                         "extra_shots": [{"t": 19.85, "blend": 0.5, **SKY_LOW, "dist": 11.5, "to": {"dist": 10.8}}]})
# the punchline: "हवा का challan बनता है!" - the radar gun reads CHALLAN
act["cop"]["screen"] = sorted(act["cop"]["screen"] + [[15.7, "CHALLAN!", 1], [19.8, "WINK?", 0]], key=lambda k: k[0])

space_shots = [{"t": 7.72, "look": [0, 1.0, 0], "dir": [0, 0.05, 1], "dist": 26, "to": {"dist": 24}}]

WORLD = r"""
// ---- Chai Pe Kyun #4: a winking star and a steady planet in the home sky; in the lab, a star's ray through moving air
const heroStar = new THREE.Sprite(haloMat("rgba(255,255,255,1)", "rgba(190,215,255,0)"));
const heroCore = new THREE.Sprite(haloMat("rgba(255,255,255,1)", "rgba(255,255,255,0)"));
const HERO = [-2.3, 5.4, -7];
heroStar.position.set(...HERO);
heroCore.position.set(...HERO);
const planet = new THREE.Mesh(new THREE.IcosahedronGeometry(0.22, 3), new THREE.MeshBasicMaterial({ color: "#FFE2B0", toneMapped: false }));
const planetGlow = new THREE.Sprite(haloMat("rgba(255,226,176,0.8)", "rgba(255,226,176,0)"));
const PLANET = [2.0, 4.9, -7];
planet.position.set(...PLANET);
planetGlow.position.set(...PLANET);
planetGlow.scale.setScalar(1.3);
// rings that point them out during the try-it
const ringMat = (c) => new THREE.MeshBasicMaterial({ color: c, toneMapped: false, transparent: true, opacity: 0.9, side: THREE.DoubleSide });
const starRing = new THREE.Mesh(new THREE.RingGeometry(0.62, 0.7, 40), ringMat("#7FD8FF"));
const planetRing = new THREE.Mesh(new THREE.RingGeometry(0.62, 0.7, 40), ringMat("#FFD23F"));
starRing.position.set(...HERO);
planetRing.position.set(...PLANET);
chairWorld.add(heroStar, heroCore, planet, planetGlow, starRing, planetRing);
function skyAt(t) { return { star: HERO }; }
// the twinkle: fast irregular flicker, plus a big "wink" on the jokes
const WINKS = [0.9, 2.1, 32.4];
function twinkle(t, k = 1) {
  const f = 0.62 + 0.38 * Math.abs(Math.sin(13.1 * t) * Math.sin(7.7 * t + 1.3) + 0.4 * Math.sin(23.3 * t));
  const w = WINKS.reduce((m, a) => Math.max(m, 1 - Math.min(1, Math.abs(t - a) / 0.18)), 0);
  return Math.max(0.08, lerp(1, f, k) * (1 - 0.9 * w));
}

const epWorld = new THREE.Group();
const STAR_P = new THREE.Vector3(0, 6.4, 0), EYE_P = new THREE.Vector3(0, -5.0, 0), AIR_TOP = 3.2, AIR_BOT = -1.4;
const farStar = new THREE.Sprite(haloMat("rgba(255,255,255,1)", "rgba(190,215,255,0)"));
farStar.position.copy(STAR_P);
epWorld.add(farStar);
// the air: warm and cold bubbles drifting sideways
const rndB = mulberry32(41);
const BUBBLES = Array.from({ length: 22 }, (_, i) => {
  const warm = i % 2 === 0;
  const r = 0.7 + 0.8 * rndB();
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), new THREE.MeshBasicMaterial({ color: warm ? "#FF9E6B" : "#5FB4FF", transparent: true, opacity: 0.22, depthWrite: false, toneMapped: false }));
  epWorld.add(m);
  return { m, x0: -6 + 12 * rndB(), y: AIR_BOT + 0.4 + (AIR_TOP - AIR_BOT - 0.8) * rndB(), v: (0.6 + 0.9 * rndB()) * (rndB() < 0.5 ? 1 : -1) };
});
const airBand = new THREE.Mesh(new THREE.BoxGeometry(14, AIR_TOP - AIR_BOT, 0.1), new THREE.MeshBasicMaterial({ color: "#7FC8FF", transparent: true, opacity: 0.08, depthWrite: false }));
airBand.position.y = (AIR_TOP + AIR_BOT) / 2;
airBand.position.z = -1.5;
epWorld.add(airBand);
// the eye looking up
const eye = new THREE.Group();
const white = new THREE.Mesh(new THREE.SphereGeometry(0.75, 32, 20), glossy("#FFFFFF", { roughness: 0.3 }));
const iris = new THREE.Mesh(new THREE.SphereGeometry(0.42, 24, 16), glossy("#3A2A1E", { roughness: 0.2 }));
iris.position.set(0, 0.42, 0.42);
const lidTop = new THREE.Mesh(new THREE.SphereGeometry(0.8, 32, 16, 0, TAU, 0, Math.PI / 2), clay("#C98B5E"));
eye.add(white, iris, lidTop);
eye.position.copy(EYE_P);
epWorld.add(eye);
// the ray: thin segments, straight in space, wobbling inside the air
const SEG = 48;
const rayMat = new THREE.MeshBasicMaterial({ color: "#FFFBE6", toneMapped: false });
const RAY = Array.from({ length: SEG }, () => {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1, 8), rayMat);
  epWorld.add(m);
  return m;
});
const UPV = new THREE.Vector3(0, 1, 0);
function lineBetween(m, a, b) {
  const d = b.clone().sub(a);
  m.position.copy(a).addScaledVector(d, 0.5);
  m.scale.set(1, d.length(), 1);
  m.quaternion.setFromUnitVectors(UPV, d.normalize());
}
const seen = new THREE.Sprite(haloMat("rgba(255,255,255,1)", "rgba(190,215,255,0)"));
epWorld.add(seen);
const labLight = new THREE.DirectionalLight(0xffffff, 1.3);
labLight.position.set(2, 4, 6);
epWorld.add(labLight);
const FOCUS = {};

function episodeRender(t, name) {
  if (name === "chair") {
    stars.visible = true;
    stars.material.opacity = 0.55 + 0.45 * Math.abs(Math.sin(5.3 * t) * Math.sin(3.1 * t + 0.7));
  }
  key.intensity = name === "chair" ? 1.7 : 1.4;
  key.color.set("#dfe6ff");
  const tw = twinkle(t);
  heroStar.scale.setScalar(2.6 * tw);
  heroCore.scale.setScalar(0.9 * tw);
  heroStar.material.color.setHSL(0.6 - 0.12 * Math.abs(Math.sin(9.7 * t)), 0.6, 0.85);
  planetGlow.scale.setScalar(1.3 + 0.02 * Math.sin(2 * t)); // steady
  const point = outBack(seg(t, 20.0, 20.4), 1.3) * (1 - seg(t, 25.1, 25.4));
  starRing.visible = planetRing.visible = point > 0.01;
  starRing.scale.setScalar(point);
  planetRing.scale.setScalar(point);
  starRing.lookAt(camera.position);
  planetRing.lookAt(camera.position);

  // lab: the bubbles appear on "हवा गरम-ठंडी होकर हिलती रहती है" (10.0); the ray wobbles once they move
  const air = seg(t, 9.9, 10.5);
  BUBBLES.forEach((b) => {
    b.m.visible = air > 0.01;
    b.m.material.opacity = 0.22 * air;
    b.m.position.set(((b.x0 + b.v * (t - 7.7) + 7) % 14 + 14) % 14 - 7, b.y + 0.15 * Math.sin(2 * t + b.x0), 0);
  });
  const ray = outExpo(seg(t, 7.85, 8.6)); // the ray travels down from the star
  const wob = 0.55 * seg(t, 10.2, 10.8) + 0.35 * seg(t, 12.6, 13.0); // stronger on "रोशनी झटके खाती है"
  const pts = [];
  for (let i = 0; i <= SEG; i++) {
    const u = i / SEG;
    const y = lerp(STAR_P.y, lerp(STAR_P.y, EYE_P.y + 0.6, 1), u);
    const inAir = smoothstep(AIR_TOP + 0.2, AIR_TOP - 0.6, y) * smoothstep(AIR_BOT - 0.2, AIR_BOT + 0.6, y);
    const below = y < AIR_BOT ? 1 : 0;
    const x = wob * (inAir * Math.sin(7.3 * t + 2.1 * y) * Math.sin(3.7 * t + 1.3 * y) + below * 0.6 * Math.sin(5.1 * t) * smoothstep(EYE_P.y + 0.6, AIR_BOT, y));
    pts.push(new THREE.Vector3(x, y, 0.2));
  }
  RAY.forEach((m, i) => {
    const u = (i + 1) / SEG;
    m.visible = u <= ray;
    if (m.visible) lineBetween(m, pts[i], pts[i + 1]);
  });
  // what the eye sees: the star, flickering and jumping a little
  const ftw = wob > 0.05 ? twinkle(t, Math.min(1, wob * 1.6)) : 1;
  farStar.scale.setScalar(2.2 * ftw);
  seen.visible = ray > 0.98;
  seen.scale.setScalar(0.9 * ftw);
  seen.position.set(EYE_P.x + 1.6 + 0.25 * wob * Math.sin(11 * t), EYE_P.y + 1.4 + 0.2 * wob * Math.cos(9 * t), 0.4);
}
function smoothstep(a, b, x) {
  const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return k * k * (3 - 2 * k);
}
"""

build(HERE, {
    "title": "Chai Pe Kyun #4: Taare tim-timate kyun?",
    "dur": DUR, "space": SPACE, "nums": [], "act": act,
    "bg": {"home": ["#24317A", "#070B22"], "space": ["#1B2348", "#070A18"], "alt": ["#24317A", "#070B22"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.9, 1.0],
})

L = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
caps = [{"who": l["speaker"], "text": w["text"], "in": round(w["start"], 2), "out": round(w["end"], 2)} for l in L for w in l["words"]]
C, S = T["C"], T["S"]
tags = [
    {"hook": True, "top": 300, "text": "Taara aankh maar raha?!", "size": 104, "color": "#FFD23F", "in": 0.0, "out": 3.2},
    {"top": 300, "text": "Taara: 40 lakh crore km door", "sub": "bas ek chhota sa point", "color": "#BFD4FF", "in": 7.9, "out": 9.95},
    {"top": 300, "text": "Garam-thandi hawa hilti hai", "sub": "roshni ka raasta mudta hai", "color": "#FFB385", "in": 10.1, "out": 12.55},
    {"top": 300, "text": "Roshni jhatke khaati hai", "sub": "isliye TIM-TIM!", "color": "#7FD8FF", "in": 12.7, "out": 15.45},
    {"top": 300, "text": "HAWA KA CHALLAN!", "size": 96, "color": "#FF4D5E", "in": 18.1, "out": 19.8},
    {"top": 300, "text": "Planet timtimata nahi!", "sub": "taara: hilta  ·  planet: steady", "color": "#FFD23F", "in": 20.0, "out": 22.45},
    {"top": 300, "text": "Aaj raat try karo!", "sub": "jo point nahi hilta, woh planet", "color": "#FFD23F", "in": 22.55, "out": 25.3},
    {"top": 300, "text": "Sabse chamakdaar taara?", "sub": "Dhruv tara? Comment karo!", "color": "#FFD23F", "in": C + 0.05, "out": S},
    {"top": 300, "text": "Subscribe karo", "sub": "roz ek naya sawaal", "in": S + 0.02, "out": round(S + 0.95, 2)},
    {"top": 300, "text": "Agla sawaal:", "sub": "din mein taare kahan jaate hain?", "color": "#FFD23F", "in": 30.9, "out": 33.3},
]
json.dump({"title": "Taare tim-timate kyun?", "duration": DUR, "scene_note": "Chai Pe Kyun? #4: why stars twinkle (and planets don't).",
           "caps": [], "tags": tags, "captions": caps, "end": {"lines": [], "at": 99}}, open(os.path.join(HERE, "story.json"), "w"),
          ensure_ascii=False, indent=1)
print("T", {k: v for k, v in T.items() if k != "L"})
