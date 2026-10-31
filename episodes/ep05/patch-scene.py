"""Challan #5 "Venus ka Overtime": Inspector Sahab books Venus for a day that never ends; the Tapri wala explains why.

Night at home, Venus bright in the sky -> whip to Venus up close turning very slowly (243 days) -> pull up to its orbit, one
fast lap round the Sun (225 days: the day is longer than the year) -> back on Venus, the spin arrow runs backwards ->
on Venus's horizon the Sun rises in the west -> snap home: "a 243-day shift?!" -> trombone, chai, end card -> comment ->
subscribe callout -> teaser (red Mars rises) -> loop to frame 0. Data and world JS only; see tools/cycle2_patch.py.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../tools"))
from cycle2_patch import build

DUR = 40.92
SPACE = [[4.1, 22.7]]

guy = {
    "handR": [[0, "SIP_R"], [0.85, "SIP_R"], [1.1, "REST_R", "back"], [28.4, "REST_R"], [28.6, "SIP_R"], [29.2, "SIP_R"], [29.5, "REST_R"],
              [37.7, "REST_R"], [37.95, "RAISE_R", "back"], [40.2, "RAISE_R"], [40.6, "SIP_R"]],
    "handL": [[0, "REST_L"], [26.95, "REST_L"], [27.1, "POCKET"], [27.17, "POCKET"], [27.37, "OFFER", "back"], [27.6, "OFFER"],
              [27.85, "REST_L"]],
    "lid": [[0, 1.1], [0.85, 1.1], [0.95, -1.75, "snap"], [1.5, -1.3], [4.1, -0.85], [26.85, -0.85], [26.9, 1.0], [27.1, 1.0],
            [27.2, 0.05], [28.5, 0.05], [28.6, 1.1], [29.2, 1.1], [29.5, -0.85], [37.75, -0.85], [37.9, 0.05], [40.2, 0.05], [40.6, 1.1]],
    "yaw": [[0, 0], [0.95, 0], [1.15, 0.55, "back"], [40.4, 0.55], [40.8, 0]],
    "mood": {"startle": [0.9], "smug": [[22.8, 26.8], [37.75, 40.3]], "laugh": [[26.85, 27.15]], "sip": [[-1, 0.9], [28.6, 29.2], [40.6, 42]],
             "lookUp": [[1.5, 3.9], [33.4, 37.4]]},
}
cop = {
    "handR": [[0, "UP"], [26.9, "UP"], [27.3, "LOW"], [28.3, "LOW"], [28.55, "AIM", "back"], [33.3, "AIM"], [33.55, "UP", "back"], [DUR, "UP"]],
    "handL": [[0, "HIP"], [0.85, "HIP"], [1.0, "STOP", "back"], [2.6, "STOP"], [2.9, "HIP"], [24.2, "HIP"], [24.4, "STOP", "back"],
              [26.6, "STOP"], [26.9, "HIP"], [27.45, "HIP"], [27.6, "TAKE", "back"], [27.7, "TAKE"], [27.85, "HOLD"], [27.95, "SIP"],
              [28.3, "SIP"], [28.45, "HOLD"], [39.0, "HOLD"], [39.35, "HIP"]],
    "lid": [[0, -0.75], [22.75, -0.75], [22.9, -0.3], [24.85, -0.3], [24.95, -1.8, "snap"], [26.85, -1.8], [27.15, 0.35], [27.5, 0.35],
            [27.6, -0.9], [27.95, -0.9], [28.0, 1.1], [28.3, 1.1], [28.45, -0.75], [DUR, -0.75]],
    "aim": [[0, "venus"], [26.9, "down"], [28.45, "cam"], [33.4, "mars"], [37.7, "venus"]],
    "beam": [[0, 3.9], [33.6, 37.3], [38.7, 99]],
    "screen": [[0, "OVERTIME!", 1], [22.75, "SHIFT?", 0], [24.95, "243 DIN", 1], [26.85, "LEAVE?", 0], [28.45, "COMMENT", 0],
               [32.6, "SUBSCRIBE?", 1], [33.33, "MARS", 0], [37.7, "OVERTIME!", 1]],
    "duty": [[0, 4.1], [28.45, 33.4], [37.7, 99]],
    "lazyFrom": 27.6,
    "sweat": [25.0, 26.9],
    "mood": {"shout": [0.9], "hopeful": [[22.8, 24.85]], "shock": [[24.9, 26.85]], "sad": [[26.85, 27.5]], "sheepish": [[27.5, 28.45]],
             "sip": [[27.95, 28.35]], "toCam": [[28.45, 33.4]], "lookSky": [[-1, 4.1], [22.75, 24.4], [33.4, 37.4], [38.6, 99]]},
}
act = {"guy": guy, "cop": cop, "k2": {"pop": 27.05, "give": 27.65, "sipA": 27.95, "sipB": 28.35, "end": 39.0}, "alt": []}

nums = [
    {"value": 243, "fly": 6.6, "land": 6.91, "lock": 7.95, "out": 9.2, "rim": "#FFB703"},  # "दो सौ तैंतालीस दिन"
    {"value": 225, "fly": 12.1, "land": 12.41, "lock": 13.2, "out": 13.9, "rim": "#FF006E"},  # "दो सौ पच्चीस दिन"
]

CU_COP_AIM = {"look": [0.9, 2.75, 0.5], "dir": [-0.35, 0.02, 1]}
CU_COP = {"look": [1.0, 2.75, 0.5], "dir": [-0.35, 0.08, 1]}
CU_GUY = {"look": [-0.45, 2.3, 0.2], "dir": [0.3, 0.1, 1]}
shots = [
    {"t": 0, **CU_COP_AIM, "dist": 5.2, "to": {"dist": 4.6}},  # hook: radar gun on Venus
    {"t": 2.3, "blend": 0.5, "look": [-0.6, 3.6, -0.5], "dir": [0.1, -0.1, 1], "dist": 12.0},  # wide and low: Venus over them
    {"t": 22.7, "look": [0.2, 2.2, 0.3], "dir": [0.04, 0.22, 1], "dist": 9.6},  # back home
    {"t": 23.4, "blend": 0.6, **CU_COP, "dist": 4.8},  # "मतलब duty की एक shift..."
    {"t": 24.9, "blend": 0.8, "look": [1.0, 3.05, 0.5], "dir": [-0.35, 0.08, 1], "dist": 4.4},  # "...243 दिन की?!"
    {"t": 26.85, "blend": 0.4, "look": [1.0, 2.6, 0.5], "dir": [-0.3, 0.05, 1], "dist": 3.6},  # trombone: his face
    {"t": 27.05, "look": [0.15, 2.4, 0.2], "dir": [0.06, 0.3, 1], "dist": 11.0},  # chai together, end card
    {"t": 28.45, "look": [1.05, 2.75, 0.75], "dir": [0.12, 0.1, 1], "dist": 4.4, "to": {"dist": 4.0}},  # to camera
    {"t": 33.33, "look": [0.9, 3.6, -0.5], "dir": [-0.06, -0.1, 1], "dist": 12.0},  # teaser: Mars rises
    {"t": 37.7, **CU_GUY, "dist": 5.0, "to": {"dist": 4.7}},  # "साहब, आपकी shift ख़त्म हुई?"
    {"t": 39.4, **CU_COP_AIM, "dist": 5.6, "to": {"dist": 5.2}},  # the loop
]
space_shots = [
    {"t": 4.1, "look": "venus", "dir": [0, 0.2, 1], "dist": 9.0},  # Venus turning, slowly: 243
    {"t": 9.3, "blend": 1.6, "look": [0, 0, 0], "dir": [0, 1, 0.5], "dist": 40},  # "और साल?": up over the orbit
    {"t": 15.9, "look": "venus", "dir": [0.12, 0.25, 1], "dist": 8.5},  # the spin runs backwards
    {"t": 20.2, "blend": 0.7, "look": "venusTop", "dir": [0, 0.06, 1], "dist": 3.6},  # Venus's horizon: the Sun rises in the west
]

WORLD = r"""
// ---- Challan #5: Venus in the night sky (Mars rises for the teaser); in space, Venus up close and on its orbit
Object.assign(EARTH_COLORS, { vHi: "#F6E2B0", vMid: "#E8BE78", vLow: "#C98F4A", mRust: "#C1440E", mDust: "#E07A3F" });
const venusKind = (m) => {
  const n = Math.sin(m.y * 7.0 + 1.2 * Math.sin(m.x * 3.1 + m.z * 2.3)) + 0.35 * landNoise(m.clone().multiplyScalar(1.8));
  return n > 0.55 ? "vHi" : n > -0.45 ? "vMid" : "vLow";
};
const marsKind = (m) => (landNoise(m.clone().multiplyScalar(2.2)) > 0.3 ? "mDust" : "mRust");
const skyVenus = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(0.42, 3), venusKind), earthMaterial());
const skyVenusGlow = new THREE.Sprite(haloMat("rgba(255,240,200,0.75)", "rgba(255,240,200,0)"));
skyVenusGlow.scale.setScalar(3.4);
const SKY_VENUS = [-2.2, 5.9, -7];
skyVenus.position.set(...SKY_VENUS);
skyVenusGlow.position.set(SKY_VENUS[0], SKY_VENUS[1], SKY_VENUS[2] - 0.5);
const skyMars = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(0.36, 3), marsKind), earthMaterial());
const skyMarsGlow = new THREE.Sprite(haloMat("rgba(255,110,60,0.7)", "rgba(255,110,60,0)"));
chairWorld.add(skyVenus, skyVenusGlow, skyMars, skyMarsGlow);
function skyAt(t) {
  const rise = outBack(seg(t, 33.5, 34.4), 1.2) * (1 - inOutSine(seg(t, 37.3, 37.9)));
  return { venus: SKY_VENUS, mars: [2.4, lerp(1.0, 5.2, rise), -7] };
}

// space: the Sun at the centre, Venus on a magenta orbit; a flag on Venus shows how little it turns
const epWorld = new THREE.Group();
const vSun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
vSun.scale.setScalar(2.0);
const vHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
const vHalo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.45)", "rgba(251,86,7,0)"));
vHalo.scale.setScalar(8.5);
vHalo2.scale.setScalar(14);
const vLight = new THREE.PointLight(0xffd59a, 2.6, 0, 0);
epWorld.add(vSun, vHalo, vHalo2, vLight);
const V_R = 14;
const vOrbit = new THREE.Mesh(new THREE.TorusGeometry(V_R, 0.07, 8, 300), new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false }));
vOrbit.rotation.x = Math.PI / 2;
epWorld.add(vOrbit);
const venusSpin = new THREE.Group();
const venus = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(1.5, 10), venusKind), earthMaterial());
venusSpin.add(venus);
const flagMat = glossy("#FF2D3D", { roughness: 0.3 });
const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.7, 8), glossy("#FFFFFF"));
pole.position.set(0, 0, 1.5 + 0.33);
pole.rotation.x = Math.PI / 2;
const flag = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.22, 0.03, 2, 0.01), flagMat);
flag.position.set(0.18, 0.1, 1.5 + 0.6);
flag.rotation.y = Math.PI / 2;
venus.add(pole, flag);
epWorld.add(venusSpin);
// the spin arrow (red, backwards) round Venus's equator and the orbit arrow (yellow) along its path
const arcMat = new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false });
const spinArc = new THREE.Mesh(new THREE.TorusGeometry(2.0, 0.06, 8, 80, Math.PI * 1.3), arcMat);
spinArc.rotation.x = Math.PI / 2;
const spinHead = new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.42, 14), arcMat);
const spinArrow = new THREE.Group();
spinArrow.add(spinArc, spinHead);
epWorld.add(spinArrow);
const orbitArrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(), 2.6, 0xffd23f, 0.6, 0.42);
epWorld.add(orbitArrow);
// the trail Venus leaves on its fast lap
const V_TRAIL = 30;
const vTrail = new THREE.InstancedMesh(new THREE.SphereGeometry(0.3, 10, 8),
  new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false, transparent: true, opacity: 0.8 }), V_TRAIL);
epWorld.add(vTrail);
// the illustrative Sun that rises over Venus's western horizon
const riser = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
riser.scale.setScalar(0.28);
const riserHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.9)", "rgba(255,183,3,0)"));
epWorld.add(riser, riserHalo);
const venusAng = (t) => {
  // parked at the front (Sun behind the camera) except for one fast lap while he says "सिर्फ़ 225 दिन"
  const lap = inOutSine(seg(t, 11.3, 15.4));
  return Math.PI / 2 + TAU * lap + 0.01 * (t - 4.1);
};
const venusPos = (t) => { const a = venusAng(t); return new THREE.Vector3(Math.cos(a) * V_R, 0, -Math.sin(a) * V_R); };
const FOCUS = { venus: (t) => venusPos(t), venusTop: (t) => venusPos(t).add(new THREE.Vector3(0, 1.5, 0)) };
const dummy = new THREE.Object3D();

function episodeRender(t, name) {
  skyVenus.rotation.y = -0.05 * t;
  const sky = skyAt(t);
  skyMars.position.set(...sky.mars);
  skyMars.visible = skyMarsGlow.visible = t > 33.4 && t < 37.95;
  skyMarsGlow.position.set(sky.mars[0], sky.mars[1], sky.mars[2] - 0.5);
  skyMarsGlow.scale.setScalar(2.6);
  key.intensity = name === "chair" ? 2.0 : 1.4;
  key.color.set(name === "chair" ? "#e8ecff" : "#fff1e0");

  const vp = venusPos(t);
  venusSpin.position.copy(vp);
  venus.rotation.y = -0.35 - 0.04 * (t - 4.1); // backwards, and barely moving
  vSun.rotation.y = 0.3 * t;
  vOrbit.visible = t > 9.4 && t < 16.2; // the ring only for the orbit view
  // a short pink trail behind Venus during the lap
  const lapOn = seg(t, 11.3, 11.6) * (1 - seg(t, 15.4, 15.9));
  vTrail.visible = lapOn > 0.01;
  for (let i = 0; i < V_TRAIL; i++) {
    const p = venusPos(t - 0.035 * (i + 1));
    dummy.position.copy(p);
    dummy.scale.setScalar(lapOn * (1 - i / V_TRAIL));
    dummy.updateMatrix();
    vTrail.setMatrixAt(i, dummy.matrix);
  }
  vTrail.instanceMatrix.needsUpdate = true;
  // arrows: Venus spins clockwise seen from above (red) while it orbits anticlockwise (yellow)
  const arr = outBack(seg(t, 16.0, 16.5), 1.5) * (1 - seg(t, 20.0, 20.3));
  spinArrow.visible = orbitArrow.visible = arr > 0.01;
  spinArrow.position.copy(vp);
  spinArrow.scale.setScalar(arr);
  spinArrow.rotation.y = -1.2 * (t - 16.0);
  spinHead.position.set(2.0 * Math.cos(Math.PI * 1.3), 0, -2.0 * Math.sin(Math.PI * 1.3));
  spinHead.rotation.set(0, Math.PI * 1.3, -Math.PI / 2);
  const a = venusAng(t);
  orbitArrow.position.copy(vp).add(new THREE.Vector3(0, 2.3, 0));
  orbitArrow.setDirection(new THREE.Vector3(-Math.sin(a), 0, -Math.cos(a)));
  orbitArrow.setLength(2.6 * arr + 0.001, 0.6 * arr + 0.001, 0.42 * arr + 0.001);
  // sunrise in the west: up over the left of the horizon
  const rise = outBack(seg(t, 20.5, 21.6), 1.1);
  riser.visible = riserHalo.visible = t > 20.3;
  riser.position.copy(vp).add(new THREE.Vector3(-1.05, lerp(0.7, 1.85, rise), -0.9));
  riserHalo.position.copy(riser.position);
  riserHalo.scale.setScalar(1.6 * rise);
}
"""

build(HERE, {
    "title": 'Challan #5 "Venus ka Overtime"',
    "dur": DUR, "space": SPACE, "nums": nums, "act": act,
    "bg": {"home": ["#4B3A8C", "#140C33"], "space": ["#3B2448", "#120A20"], "alt": ["#4B3A8C", "#140C33"]},
    "shots": shots, "space_shots": space_shots, "world_js": WORLD, "exposure": [0.85, 0.8],
})
