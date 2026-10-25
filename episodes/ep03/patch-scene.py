"""Turns Episode 1's scene (assets/challan-scene.js, copied here) into Challan #3 "Chand ki FIR".

Only the episode-specific blocks are replaced: timing, both characters' keyed acting, the kulhad hand-off, a night
version of the home world (Moon in the sky, stars, a dawn Sun for the teaser), the Earth-Moon space world (orbit,
Apollo laser, tidal bulge), camera shots, background colours and render(t). Characters, materials, 3D numbers,
whips and speed lines are Episode 1's code, untouched. Run once on a fresh copy.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "assets/challan-scene.js")
src = open(P, encoding="utf-8").read()
lines = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
DUR = 59.09


def talk(who):
    return [[round(l["words"][0]["start"], 2), round(l["words"][-1]["end"], 2)] for l in lines if l["speaker"] == who]


def swap(start, end, new):
    global src
    i = src.index(start)
    j = src.index(end, i)
    src = src[:i] + new + src[j:]


# ---------------------------------------------------------------- timing
swap("// ---------------------------------------------------------------- timing", "// ---------------------------------------------------------------- helpers", f"""// ---------------------------------------------------------------- timing (dialogue track: assets/audio/lines.json)
// Challan #3 "Chand ki FIR": night at home -> the Earth-Moon system (whip on "हर साल") -> snap home before "मतलब छुट्टी बढ़ेगी?"
const DUR = {DUR};
const SW = {{ space: 10.3, snap: 34.0 }};
const WHIPS = [
  {{ c: SW.space, b: 0.22, a: 0.2, dir: -1, k: 1.1 }},
  {{ c: SW.snap, b: 0.09, a: 0.12, dir: 1, k: 1.35 }}, // snap back: the fastest move
];
const NUMS = [
  {{ value: 3.8, dec: 1, plus: false, fly: 10.7, land: 11.06, lock: 11.94, out: 13.1, rim: "#4CC9F0" }}, // "तीन point आठ"
  {{ value: 2, plus: false, fly: 37.0, land: 37.35, lock: 37.55, out: 38.85, rim: "#FFD23F" }}, // "लगभग दो millisecond"
];
const T_LASER = 17.0; // "Laser मारो": the pulse leaves Earth
const T_TIDE = 24.6; // "tides!": the ocean bulge swells
const T_TROMBONE = 38.9;
const T_END = 39.75; // end card
const T_BEAM = 53.5; // the gun fires at the dawn Sun for the teaser ("सूरज का बिजली का bill")
const T_BEAM_OFF = 55.4;
// speaking windows for lip flap (first to last word of each line)
const TALK = {{
  cop: {json.dumps(talk("cop"))},
  guy: {json.dumps(talk("guy"))},
}};

""")

# ---------------------------------------------------------------- the guy's acting
swap("  // ---- acting (guy-local", "  return { group: g, fig, pose, kulhad2 };", """  // ---- acting (guy-local positions; he faces +z, the cop stands to his front right)
  const REST_R = [0.16, 1.78, 0.6], SIP_R = [0.05, 2.3, 0.55], RAISE_R = [0.32, 2.3, 0.8], TOAST_R = [0.42, 2.6, 1.0], SKY_R = [0.3, 2.95, 0.55];
  const REST_L = [-0.3, 1.3, 0.58], POCKET = [-0.12, 1.45, 0.42], OFFER = [0.42, 2.0, 1.0], POINT_UP = [-0.25, 3.05, 0.6];
  const HAND_R = [[0, SIP_R], [0.85, SIP_R], [1.1, REST_R, "back"], [5.0, REST_R], [5.25, SKY_R, "back"], [7.4, SKY_R], [7.7, REST_R],
    [36.9, REST_R], [37.1, RAISE_R, "back"], [38.4, RAISE_R], [38.7, REST_R], [39.85, REST_R], [40.05, SIP_R], [40.6, SIP_R], [40.9, REST_R],
    [43.0, REST_R], [43.2, SIP_R], [44.0, SIP_R], [44.3, REST_R], [49.7, REST_R], [49.95, TOAST_R, "back"], [52.0, TOAST_R], [52.3, REST_R],
    [58.6, REST_R], [59.0, SIP_R]];
  const HAND_L = [[0, REST_L], [38.9, REST_L], [39.05, POCKET], [39.12, POCKET], [39.32, OFFER, "back"], [39.55, OFFER], [39.8, REST_L],
    [55.55, REST_L], [55.85, POINT_UP, "back"], [58.5, POINT_UP], [58.9, REST_L]];
  const LID = [[0, 1.1], [0.85, 1.1], [0.95, -1.75, "snap"], [1.5, -1.35], [3.8, -1.35], [4.0, 0.2], [4.8, 0.2], [5.0, -0.85], [34.0, -0.85],
    [35.8, -0.6], [38.85, -0.6], [38.95, 1.0], [39.2, 1.0], [39.35, 0.05], [39.95, 0.05], [40.05, 1.1], [40.6, 1.1], [40.9, 0.05], [43.1, 0.05],
    [43.2, 1.1], [44.0, 1.1], [44.3, -0.85], [49.75, -0.85], [49.95, -1.45], [52.0, -1.45], [52.3, -0.85], [55.5, -0.85], [55.7, -1.35],
    [58.6, -1.35], [59.0, 1.1]];
  const YAW = [[0, 0], [0.95, 0], [1.15, 0.55, "back"], [49.75, 0.55], [50.0, -0.35, "back"], [52.2, -0.35], [52.5, 0.55], [55.5, 0.55],
    [55.8, 0.25], [58.7, 0.25], [59.05, 0]];
  function pose(t, ti = t) {
    const breathe = Math.sin(TAU * ti / 1.5);
    const startle = Math.sin(Math.PI * seg(t, 0.9, 1.7)) * (t < 1.7 ? 1 : 0);
    const confused = smooth(1.6, 1.8, t) * (1 - smooth(3.7, 3.95, t));
    const smug = smooth(35.8, 36.1, t) * (1 - smooth(38.8, 38.95, t)) + smooth(5.0, 5.3, t) * (1 - smooth(7.6, 7.8, t));
    const laugh = smooth(4.0, 4.1, t) * (1 - smooth(4.75, 4.9, t)) + smooth(38.9, 39.0, t) * (1 - smooth(39.3, 39.45, t));
    const sip = smooth(39.95, 40.05, t) * (1 - smooth(40.6, 40.8, t)) + smooth(43.1, 43.2, t) * (1 - smooth(44.0, 44.2, t))
      + (t < 0.85 ? 1 : 0) * (1 - smooth(0.83, 0.95, t)) + smooth(58.9, 59.0, t);
    const lookUp = smooth(5.1, 5.4, t) * (1 - smooth(7.5, 7.8, t)) + smooth(55.6, 55.9, t) * (1 - smooth(58.6, 58.95, t));
    const dt = t - SW.snap;
    const wind = dt >= 0 && dt < 1.2 ? Math.exp(-((dt / 0.32) ** 2)) : 0;
    fig.position.y = 0.018 * breathe + 0.12 * startle + 0.03 * Math.abs(Math.sin(t * 22)) * laugh;
    torso.scale.set(1.08 * (1 + 0.015 * breathe), 1 - 0.015 * breathe + 0.06 * startle, 0.88);
    head.rotation.y = track(t, YAW) + 0.06 * Math.sin(TAU * ti / 5);
    head.rotation.z = 0.06 * Math.sin(TAU * ti / 3) + 0.12 * confused - 0.08 * smug;
    head.rotation.x = -0.04 - 0.16 * sip - 0.12 * laugh + 0.04 * Math.sin(t * 22) * laugh - 0.42 * lookUp;
    head.position.y = 2.62 + 0.012 * breathe;
    const talking = within(t, TALK.guy) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.45 * startle,
      brows: [0.05 * confused + 0.07 * startle, 0.22 * confused, -0.02 * confused + 0.05 * smug + 0.07 * startle, -0.3 * smug],
      curve: lerp(1, 0.3, confused),
      smileW: 1 + 0.5 * laugh + 0.15 * smug,
      open: Math.max(startle * 0.9, talking * 0.55, laugh * (0.5 + 0.4 * Math.abs(Math.sin(t * 22)))),
    });
    quiff.rotation.x = -0.55 * wind;
    quiff.scale.set(1 + 0.1 * wind, 1 - 0.45 * wind, 1 + 0.6 * wind);
    quiff.position.z = 0.16 - 0.14 * wind;
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR);
    kulhad.position.copy(hR).add(new THREE.Vector3(-0.02, 0.08, 0.04));
    kulhad.rotation.x = -0.8 * clamp01(sip);
    const kp = kulhad.position;
    steam.forEach((s, i) => {
      const p = (((ti / 1.5 + i / 3) % 1) + 1) % 1;
      s.position.set(kp.x + 0.04 * Math.sin(TAU * (p + i * 0.3)) - 0.9 * wind * p, kp.y + 0.18 + 0.55 * p, kp.z + 0.1 * p - 0.6 * wind * p);
      s.scale.set((0.5 + 1.1 * p) * (1 + 1.2 * wind), 0.5 + 1.1 * p, 0.5 + 1.1 * p);
      s.material.opacity = host.hideSteam ? 0 : 0.5 * Math.sin(Math.PI * p) * (1 - 0.7 * clamp01(sip));
    });
    return { handL: hL };
  }
""")

# ---------------------------------------------------------------- the cop's acting
swap("  // ---- acting (cop-local", "  return { group: g, fig, pose, kulhadSlot, head };", """  // ---- acting (cop-local positions; he faces +z, the guy sits to his front left)
  const AIM = [0.3, 2.15, 0.72], UP = [0.34, 2.8, 0.42], LOW = [0.4, 1.55, 0.32];
  const HIP = [-0.5, 1.42, 0.12], STOP = [-0.42, 2.4, 0.62], TAKE = [-0.32, 1.98, 0.86], HOLD = [-0.22, 1.86, 0.62], SIP = [-0.06, 2.62, 0.55];
  const HAND_R = [[0, UP], [34.0, UP], [34.3, AIM, "back"], [38.85, AIM], [39.3, LOW], [41.6, LOW], [41.85, AIM, "back"], [53.2, AIM],
    [53.45, UP, "back"], [59.1, UP]];
  const HAND_L = [[0, HIP], [0.85, HIP], [1.0, STOP, "back"], [2.4, STOP], [2.7, HIP], [39.45, HIP], [39.6, TAKE, "back"], [39.7, TAKE],
    [39.85, HOLD], [40.0, SIP], [40.6, SIP], [40.9, HOLD], [45.1, HOLD], [45.3, STOP, "back"], [46.5, STOP], [46.8, HOLD], [58.3, HOLD], [58.9, HIP]];
  const LID = [[0, -0.75], [34.0, -0.75], [34.2, -0.3], [37.3, -0.3], [37.38, -1.8, "snap"], [38.85, -1.8], [39.15, 0.35], [39.45, 0.35],
    [39.6, -0.9], [39.95, -0.9], [40.05, 1.1], [40.6, 1.1], [40.9, 0.05], [41.6, -0.75], [59.1, -0.75]];
  function pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal, sunLocal) {
    const breathe = Math.sin(TAU * ti / 1.7);
    const shout = Math.sin(Math.PI * seg(t, 0.85, 1.6)) * (t < 1.6 ? 1 : 0);
    const hopeful = smooth(34.1, 34.4, t) * (1 - smooth(37.25, 37.4, t));
    const smug = smooth(52.1, 52.3, t) * (1 - smooth(55.2, 55.4, t));
    const shock = smooth(37.35, 37.45, t) * (1 - smooth(38.85, 39.0, t));
    const sad = smooth(38.85, 39.1, t) * (1 - smooth(39.4, 39.6, t));
    const sheepish = smooth(39.4, 39.6, t) * (1 - smooth(41.5, 41.7, t));
    const sip = smooth(40.0, 40.1, t) * (1 - smooth(40.6, 40.8, t));
    const toCam = smooth(41.6, 41.95, t) * (1 - smooth(49.6, 49.9, t));
    const lookSky = (1 - smooth(9.9, 10.3, t)) + smooth(55.6, 56.0, t);
    const stern = 1 - Math.max(smug, shock, sad, sheepish, hopeful);
    fig.position.y = 0.015 * breathe - 0.08 * sad + 0.08 * shout;
    fig.rotation.x = 0.1 * shout - 0.04 * sad;
    fig.rotation.y = 0.45 * toCam;
    torso.scale.set(1.12 * (1 + 0.02 * breathe), 1 - 0.02 * breathe - 0.05 * sad, 0.95);
    belly.scale.setScalar(1 + 0.03 * breathe);
    head.rotation.x = -0.03 + 0.28 * sad - 0.1 * shock - 0.15 * sip - 0.3 * lookSky * (1 - shout);
    head.rotation.z = 0.04 * Math.sin(TAU * ti / 3.4) + 0.1 * smug - 0.08 * hopeful;
    head.rotation.y = lerp(lerp(-0.25, 0, Math.max(shock, sad)), 0.1, toCam) + 0.05 * Math.sin(TAU * ti / 5);
    const talking = within(t, TALK.cop) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.5 * shock + 0.12 * hopeful,
      // stern: brows in a V; shock: high; sad: inner ends up; hopeful: both up, soft
      brows: [-0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * hopeful, -0.3 * stern + 0.25 * sad + 0.12 * hopeful,
        -0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * smug + 0.05 * hopeful, 0.3 * stern - 0.25 * sad - 0.2 * smug - 0.12 * hopeful],
      curve: lerp(lerp(-0.6, 1, Math.max(smug, sheepish, hopeful)), -1, sad),
      smileW: 1 + 0.2 * smug + 0.25 * hopeful,
      open: Math.max(talking * 0.6, shock * 0.35 * (1 - talking)),
    });
    halves.forEach((h, i) => (h.rotation.z = (i ? 1 : -1) * (0.15 * stern + 0.25 * Math.max(smug, hopeful) - 0.45 * sad)));
    if (host.copShout) {
      face.smile.scale.set(0.001, 0.001, 1);
      face.mouthO.position.y = -0.25;
      face.mouthO.scale.set(1.7, 1.9, 0.55);
    } else face.mouthO.position.y = -0.21;
    cap.rotation.z = 0.22 * sad + 0.08 * sheepish;
    cap.position.y = 0.36 - 0.03 * sad;
    // beacon: urgent while he chases the Moon, during the subscribe challan and on the loop back; dies with the trombone
    const onDuty = t < 10.3 || (t >= 41.6 && t < 49.7) || t >= 55.6;
    const fast = Math.sin(TAU * 3.2 * t) > 0 ? 1 : 0;
    const lazy = t > 39.45 ? 0.35 + 0.35 * Math.sin(TAU * 0.6 * t) : 0;
    const r = onDuty ? fast : lazy, b = onDuty ? 1 - fast : lazy * 0.8;
    bR.material.color.set("#FF2D3D").multiplyScalar(0.35 + 0.65 * r);
    bB.material.color.set("#2D7BFF").multiplyScalar(0.35 + 0.65 * b);
    lightR.intensity = 9 * r;
    lightB.intensity = 9 * b;
    const sw = seg(t, 37.6, 38.9);
    sweat.visible = t > 37.5 && t < 39.0;
    sweat.position.set(0.36, 0.18 - 0.3 * sw, 0.28);
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR, 0.24);
    gun.position.copy(hR).add(new THREE.Vector3(0, 0.08, 0.04));
    const down = hR.clone().add(new THREE.Vector3(0.1, -1.2, 1.2));
    const go = (a, b, t0, d = 0.25) => a.clone().lerp(b, outBack(seg(t, t0, t0 + d), 1.2));
    let target = moonLocal.clone();
    if (t >= 34.0 && t < 38.85) target = go(moonLocal, guyHeadLocal, 34.0, 0.3);
    else if (t >= 38.85 && t < 41.6) target = go(guyHeadLocal, down, 38.85, 0.5);
    else if (t >= 41.6 && t < 53.2) target = go(down, camLocal, 41.6, 0.3);
    else if (t >= 53.2 && t < 55.6) target = go(camLocal, sunLocal, 53.2, 0.3);
    else if (t >= 55.6) target = go(sunLocal, moonLocal, 55.6, 0.3);
    fig.updateMatrixWorld(true);
    gun.lookAt(fig.localToWorld(target.clone()));
    // the beam: at the Moon while he files the FIR, at the dawn Sun for the teaser
    const on1 = t < 9.9, on2 = t >= T_BEAM && t < T_BEAM_OFF;
    beam.visible = on1 || on2;
    beam.scale.set(1, 1, 0.01 + 30 * outExpo(on1 ? seg(t, 0.0, 0.3) : seg(t, T_BEAM, T_BEAM + 0.3)));
    beam.material.opacity = 0.9;
    // screen readout
    if (host.gunScreen) drawScreen(host.gunScreen, true);
    else if (t < 10.3 || t >= 55.6) drawScreen("FARAAR!", Math.floor(t * 3) % 2 === 0);
    else if (t < 37.35) drawScreen("CHHUTTI?", true);
    else if (t < 41.6) drawScreen("2 MS", true);
    else if (t < 53.2) drawScreen(t < 44.9 ? "COMMENT" : "SUBSCRIBE?", Math.floor(t * 3) % 2 === 0 || t < 44.9);
    else drawScreen("BILL!", true);
    return { handL: hL };
  }
""")
src = src.replace('      c.font = "bold 116px monospace";', '      c.font = `bold ${Math.min(116, Math.floor(470 / (0.6 * text.length)))}px monospace`;')

# ---------------------------------------------------------------- the duo: kulhad hand-off and the cop's aims
swap("  const tmp = new THREE.Vector3();\n  function pose(t, ti = t) {", "  return { group: duo, pose };", """  const tmp = new THREE.Vector3();
  const camWorld = new THREE.Vector3(0.6, 2.7, 9);
  function pose(t, ti = t) {
    duo.updateMatrixWorld(true);
    const guyHead = guy.group.localToWorld(new THREE.Vector3(0, 2.62, 0));
    const guyHeadLocal = cop.fig.worldToLocal(guyHead.clone());
    const selfHeadLocal = new THREE.Vector3(0, 2.82, 0);
    const camLocal = cop.fig.worldToLocal(duo.localToWorld(camWorld.clone()));
    const moonLocal = cop.fig.worldToLocal(duo.localToWorld(new THREE.Vector3(1.5, 6.2, -7)));
    const sunLocal = cop.fig.worldToLocal(duo.localToWorld(new THREE.Vector3(-3.0, 3.6, -7)));
    const g = guy.pose(t, ti);
    const c = cop.pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal, sunLocal);
    duo.updateMatrixWorld(true);
    k2.visible = t > 39.05 && t < 58.4;
    const from = guy.fig.localToWorld(g.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    const to = cop.fig.localToWorld(c.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    duo.worldToLocal(from);
    duo.worldToLocal(to);
    tmp.copy(t < 39.65 ? from : to);
    k2.position.copy(tmp);
    k2.scale.setScalar(outBack(seg(t, 39.05, 39.25), 2) * (1 - seg(t, 58.1, 58.4)));
    const copSip = smooth(40.0, 40.1, t) * (1 - smooth(40.6, 40.8, t));
    k2.rotation.set(-0.8 * (t >= 39.65 ? copSip : 0), t >= 39.65 ? -0.55 : 0.4, 0);
    if (cap) cap.rotation.x = -0.012 * t - 0.25 * inOutSine(seg(t, T_END, T_END + 1.6)) * (1 - inOutSine(seg(t, 41.5, 41.7)));
  }
""")

# ---------------------------------------------------------------- night sky props and the Earth-Moon world (after Episode 1's orbit world)
src = src.replace("scene.add(orbitWorld);\n", """scene.add(orbitWorld);

// ---- Challan #3: the Moon (shared look with Challan #2), a night sky over the home planet, a dawn Sun, and the Earth-Moon system
Object.assign(EARTH_COLORS, { moonHi: "#B4B8C6", moonMid: "#8E93A4", moonMare: "#5E6376", crater: "#727789" });
const rndC = mulberry32(5);
const CRATERS = Array.from({ length: 26 }, () => {
  const u = rndC() * 2 - 1, th = rndC() * TAU, s = Math.sqrt(1 - u * u);
  return { d: new THREE.Vector3(s * Math.cos(th), u, s * Math.sin(th)), r: 0.08 + 0.17 * rndC() };
});
function moonKind(m) {
  for (const c of CRATERS) {
    const a = m.angleTo(c.d);
    if (a < c.r * 0.55) return "crater";
    if (a < c.r) return "moonHi";
  }
  const n = landNoise(m.clone().multiplyScalar(1.6));
  return n > 0.9 ? "moonMare" : n > -0.2 ? "moonMid" : "moonHi";
}
const makeMoon = (radius, detail) => {
  const m = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(radius, detail), moonKind), earthMaterial());
  m.material.clearcoat = 0.1;
  return m;
};
// the suspect, high in the night sky behind the home planet
const skyMoon = makeMoon(1.15, 8);
skyMoon.position.set(1.5, 6.2, -7);
const skyMoonGlow = new THREE.Sprite(haloMat("rgba(220,230,255,0.55)", "rgba(220,230,255,0)"));
skyMoonGlow.scale.setScalar(5.5);
skyMoonGlow.position.copy(skyMoon.position).add(new THREE.Vector3(0, 0, -0.6));
// the teaser's dawn Sun on the horizon ("सूरज का बिजली का bill")
const skySun = new THREE.Mesh(sunGeo, new THREE.MeshBasicMaterial({ vertexColors: true, toneMapped: false }));
const skySunHalo = new THREE.Sprite(haloMat("rgba(255,183,3,0.85)", "rgba(255,183,3,0)"));
const skySunHalo2 = new THREE.Sprite(haloMat("rgba(251,86,7,0.45)", "rgba(251,86,7,0)"));
const skyProps = new THREE.Group();
skyProps.add(skyMoon, skyMoonGlow, skySun, skySunHalo, skySunHalo2);
chairWorld.add(skyProps);

// Earth-Moon world: Earth turning, the Moon on a magenta orbit line that slowly widens, the Apollo laser, the tidal bulge
const emWorld = new THREE.Group();
const EM_EARTH = new THREE.Vector3(0, 0, 0);
const emEarthSpin = new THREE.Group();
emEarthSpin.position.copy(EM_EARTH);
emEarthSpin.rotation.z = 0.41;
const emEarth = makeEarth(1.15);
emEarthSpin.add(emEarth);
emWorld.add(emEarthSpin);
const emDuo = makeDuo({ ground: false }); // the two, tiny, watching from the top of the Earth
emDuo.group.scale.setScalar(0.07);
emDuo.group.position.set(0, 1.15, 0);
emEarth.add(emDuo.group);
const emMoon = makeMoon(0.42, 6);
emWorld.add(emMoon);
const mirror = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.16, 0.03, 2, 0.01),
  new THREE.MeshPhysicalMaterial({ color: "#E8EEF8", metalness: 0.9, roughness: 0.08 }));
emMoon.add(mirror);
const emOrbit = new THREE.Mesh(new THREE.TorusGeometry(1, 0.012, 6, 220), new THREE.MeshBasicMaterial({ color: "#FF006E", toneMapped: false }));
emOrbit.rotation.x = Math.PI / 2;
emOrbit.position.copy(EM_EARTH);
emWorld.add(emOrbit);
const emOrbitOld = new THREE.Mesh(new THREE.TorusGeometry(1, 0.008, 6, 220),
  new THREE.MeshBasicMaterial({ color: "#FF8FC0", toneMapped: false, transparent: true, opacity: 0.45 }));
emOrbitOld.rotation.x = Math.PI / 2;
emOrbitOld.position.copy(EM_EARTH);
emWorld.add(emOrbitOld);
const laser = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 1, 8, 1, true),
  new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
emWorld.add(laser);
const pulse = new THREE.Sprite(haloMat("rgba(255,90,90,1)", "rgba(255,40,40,0)"));
emWorld.add(pulse);
const bulge = new THREE.Mesh(new THREE.SphereGeometry(1.15, 40, 24),
  new THREE.MeshPhysicalMaterial({ color: "#7FD8FF", transparent: true, opacity: 0.55, roughness: 0.2, clearcoat: 1, depthWrite: false }));
bulge.position.copy(EM_EARTH);
emWorld.add(bulge);
const tug = new THREE.ArrowHelper(new THREE.Vector3(0, 0, -1), new THREE.Vector3(), 1.2, 0xffd23f, 0.42, 0.3);
tug.line.material.linewidth = 3;
emWorld.add(tug);
scene.add(emWorld);
""")

# ---------------------------------------------------------------- camera
swap("// ---------------------------------------------------------------- camera", "// ---------------------------------------------------------------- 3D numbers (overlay scene)", """// ---------------------------------------------------------------- camera
const WORLDS = VERTICAL
  ? { space: { dir: [0, 0.5, 1], dist: 14.5, shift: [0, 0.1] } }
  : { space: { dir: [0, 0.42, 1], dist: 12.5, shift: [2.2, 0] } };
const up = new THREE.Vector3(0, 1, 0);

const SHOTS_V = [
  { t: 0, look: [0.9, 2.75, 0.5], dir: [-0.35, 0.02, 1], dist: 5.2, to: { dist: 4.6 } }, // hook: the cop aims his radar gun at the Moon
  { t: 3.85, look: [-0.45, 2.3, 0.2], dir: [0.3, 0.1, 1], dist: 5.0, to: { dist: 4.6 } }, // "फ़रार?": the guy, then he points up
  { t: 5.1, blend: 0.6, look: [0.3, 3.6, -0.5], dir: [0.06, -0.1, 1], dist: 12.0 }, // low and wide: the Moon above them
  { t: SW.snap, look: [0.2, 2.2, 0.3], dir: [0.04, 0.22, 1], dist: 9.6 }, // back home
  { t: 34.45, blend: 0.6, look: [1.0, 2.75, 0.5], dir: [-0.35, 0.08, 1], dist: 4.6 }, // "छुट्टी बढ़ेगी?": hopeful cop
  { t: 35.8, look: [0.1, 2.45, 0.25], dir: [0.06, 0.2, 1], dist: 9.8 }, // the answer: two-shot, room for the 2
  { t: 37.3, blend: 0.8, look: [1.0, 3.05, 0.5], dir: [-0.35, 0.08, 1], dist: 4.6 }, // push in: "only 2 ms?!"
  { t: 38.85, blend: 0.4, look: [1.0, 2.6, 0.5], dir: [-0.3, 0.05, 1], dist: 3.6 }, // trombone: his face
  { t: 39.4, look: [0.15, 2.1, 0.25], dir: [0.06, 0.22, 1], dist: 9.8 }, // chai together
  { t: T_END, blend: 1.5, look: [0.15, 3.6, 0.0], dir: [0.06, 0.4, 1], dist: 12.5 }, // end card: crane up toward the Moon
  { t: 41.6, look: [1.05, 2.75, 0.75], dir: [0.12, 0.1, 1], dist: 4.4, to: { dist: 4.0 } }, // to camera: the subscribe challan
  { t: 49.7, look: [-0.55, 2.35, 0.3], dir: [-0.1, 0.1, 1], dist: 4.7 }, // the guy raises his kulhad to camera
  { t: 52.1, look: [-0.6, 3.2, -0.3], dir: [0.1, 0.12, 1], dist: 12.0 }, // teaser: dawn on the horizon
  { t: 55.5, look: [0.3, 3.6, -0.5], dir: [0.06, -0.1, 1], dist: 12.0, to: { dist: 13.0 } }, // the Moon a little further away: the loop
];
const SHOTS_H = SHOTS_V.map((s) => ({ ...s, dist: s.dist * 0.62, to: s.to ? { dist: s.to.dist * 0.62 } : undefined }));
const SHOTS = VERTICAL ? SHOTS_V : SHOTS_H;

function shotAt(t) {
  let i = 0;
  while (i + 1 < SHOTS.length && t >= SHOTS[i + 1].t) i++;
  const s = SHOTS[i];
  const next = SHOTS[i + 1];
  const end = next ? next.t : DUR;
  let look = V(s.look), dir = V(s.dir).normalize(), dist = s.dist;
  if (s.to) dist = lerp(s.dist, s.to.dist, inOutSine(seg(t, s.t, end)));
  if (s.blend && i > 0) {
    const p = SHOTS[i - 1];
    const x = inOutSine(seg(t, s.t, s.t + s.blend));
    const pDist = p.to ? p.to.dist : p.dist;
    look = V(p.look).lerp(look, x);
    dir = V(p.dir).normalize().lerp(dir, x).normalize();
    dist = lerp(pDist, dist, x);
  }
  return { look, dir, dist };
}

function whipLevel(t) {
  let level = 0, dir = 0;
  for (const w of WHIPS) {
    let e = 0;
    if (t >= w.c - w.b && t < w.c) e = inCubic(seg(t, w.c - w.b, w.c));
    else if (t >= w.c && t < w.c + w.a) e = 1 - outExpo(seg(t, w.c, w.c + w.a));
    if (e * w.k > level) {
      level = e * w.k;
      dir = w.dir;
    }
  }
  return { level, dir };
}

function worldAt(t) {
  return t >= SW.space && t < SW.snap ? "space" : "chair";
}

// space: arrive close, pull back with a soft overshoot, drift slowly through the long explanation, rush in on the snap
function distMul(t) {
  const inn = lerp(0.32, 1, outBack(seg(t, SW.space, SW.space + 0.6), 1.3));
  const drift = 1 + 0.008 * (t - SW.space);
  const out = lerp(1, 0.25, inCubic(seg(t, SW.snap - 0.09, SW.snap)));
  return inn * drift * out;
}

function placeCamera(t, name, whip) {
  let look, dir, dist;
  if (name === "chair") {
    ({ look, dir, dist } = shotAt(t));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 6));
    if (t < SW.snap) dist *= 1 + 3.2 * inCubic(seg(t, SW.space - 0.22, SW.space));
    else dist *= lerp(4.2, 1, outBack(seg(t, SW.snap, SW.snap + 0.55), 1.2));
  } else {
    const w = WORLDS.space;
    const m = distMul(t);
    dir = V(w.dir).applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 9)).normalize();
    const right = new THREE.Vector3().crossVectors(up, dir).normalize();
    look = new THREE.Vector3().addScaledVector(right, w.shift[0] * Math.min(m, 1.6)).addScaledVector(up, w.shift[1] * Math.min(m, 1.6));
    dist = w.dist * m;
  }
  camera.position.copy(look).addScaledVector(dir, dist);
  camera.lookAt(look);
  camera.rotateZ(0.05 * whip.level * (whip.dir || 1));
  camera.fov = (VERTICAL ? 38 : 35) + 16 * whip.level;
  camera.updateProjectionMatrix();
}

""")

# ---------------------------------------------------------------- background
swap("// ---------------------------------------------------------------- background", "// ---------------------------------------------------------------- render(t)", """// ---------------------------------------------------------------- background
const BG = {
  night: ["#4B3A8C", "#140C33"],
  dawn: ["#FFB385", "#7A2E5C"],
  space: ["#2A3C6E", "#14213D"],
};
const bgEl = document.getElementById("w-bg");
const policeEl = document.getElementById("w-police");
function bgAt(t) {
  // home is night; the whip to space and the snap back cross over fast; dawn breaks for the teaser and fades back
  const mix = (p, q, x) => [col(p[0]).lerp(col(q[0]), x), col(p[1]).lerp(col(q[1]), x)];
  let a, b;
  if (t >= SW.space - 0.14 && t < SW.snap + 0.06) {
    const x = t < SW.space + 0.14 ? inOutSine(seg(t, SW.space - 0.14, SW.space + 0.14)) : 1 - inOutSine(seg(t, SW.snap - 0.06, SW.snap + 0.06));
    [a, b] = mix(BG.night, BG.space, x);
  } else {
    const x = inOutSine(seg(t, 52.4, 53.6)) * (1 - inOutSine(seg(t, 55.3, 56.0)));
    [a, b] = mix(BG.night, BG.dawn, x);
  }
  return [`#${a.getHexString()}`, `#${b.getHexString()}`];
}

""")

# ---------------------------------------------------------------- render(t)
swap("// ---------------------------------------------------------------- render(t)", "host.render = render;", """// ---------------------------------------------------------------- render(t)
const tmpV = new THREE.Vector3();
function render(t) {
  const whip = whipLevel(t);
  const name = worldAt(t);
  chairWorld.visible = name === "chair";
  earthWorld.visible = orbitWorld.visible = galaxyWorld.visible = false;
  emWorld.visible = name === "space";
  stars.visible = true; // night at home, space away
  stars.rotation.y = 0.02 * t;

  if (name === "chair") duo.pose(t);
  // night sky: the Moon (a touch further away by the last line), the dawn Sun rising for the teaser
  const away = inOutSine(seg(t, 57.5, 58.6));
  skyMoon.scale.setScalar(1 - 0.18 * away);
  skyMoon.position.set(1.5, 6.2 + 0.5 * away, -7 - 1.2 * away);
  skyMoon.rotation.y = 0.15 * t;
  skyMoonGlow.position.copy(skyMoon.position).add(new THREE.Vector3(0, 0, -0.6));
  const rise = outBack(seg(t, 52.4, 53.6), 1.1) * (1 - inOutSine(seg(t, 55.3, 56.0)));
  skySun.visible = skySunHalo.visible = skySunHalo2.visible = rise > 0.001;
  skySun.position.set(-3.0, lerp(-1.0, 3.6, rise), -7);
  skySun.scale.setScalar(0.9);
  skySun.rotation.y = 0.4 * t;
  skySunHalo.position.copy(skySun.position);
  skySunHalo2.position.copy(skySun.position);
  skySunHalo.scale.setScalar(4.2 * (1 + 0.04 * Math.sin(TAU * t)));
  skySunHalo2.scale.setScalar(7.5);
  // a cooler key light at night, warm again when the dawn Sun is up
  key.intensity = name === "chair" ? lerp(2.0, 2.4, rise) : 2.4;
  key.color.set(name === "chair" ? (rise > 0.5 ? "#fff1e0" : "#e8ecff") : "#fff1e0");

  // Earth-Moon system: the orbit widens on "3.8 cm" (shown hugely exaggerated) and again with the tides
  const R = 2.5 + 0.35 * inOutSine(seg(t, 11.06, 12.9)) + 0.35 * inOutSine(seg(t, 28.8, 31.0));
  const ang = 0.15 + 0.025 * (t - SW.space);
  const moonPos = new THREE.Vector3(Math.cos(ang) * R, 0, -Math.sin(ang) * R).add(EM_EARTH);
  emMoon.position.copy(moonPos);
  emMoon.rotation.y = Math.PI / 2 + ang; // the same face (and the mirror) always towards Earth
  mirror.position.set(0, 0.06, 0.41);
  emOrbit.scale.setScalar(R);
  emOrbitOld.scale.setScalar(2.5);
  emOrbitOld.visible = t > 11.2;
  emEarthSpin.rotation.y = (t < 31.0 ? 1.6 : 1.6 - 0.9 * seg(t, 31.0, 33.7)) * (t - SW.space); // the day lengthens
  if (name === "space") emDuo.pose(t);
  // the laser: Earth to the mirror and back, a pulse riding it ("Laser मारो, रोशनी लौटने का time नापो")
  const from = EM_EARTH.clone().add(moonPos.clone().sub(EM_EARTH).normalize().multiplyScalar(1.15));
  const to = moonPos.clone().add(EM_EARTH.clone().sub(moonPos).normalize().multiplyScalar(0.42));
  const lOn = t >= T_LASER && t < 21.3;
  laser.visible = pulse.visible = lOn;
  const grow = outExpo(seg(t, T_LASER, T_LASER + 0.4));
  const tip = from.clone().lerp(to, grow);
  laser.position.copy(from).lerp(tip, 0.5);
  laser.scale.set(1, Math.max(0.001, from.distanceTo(tip)), 1);
  laser.quaternion.setFromUnitVectors(up, tmpV.copy(to).sub(from).normalize());
  laser.material.opacity = 0.75;
  const cyc = ((t - T_LASER) / 1.3) % 2;
  pulse.position.copy(from).lerp(to, cyc < 1 ? cyc : 2 - cyc);
  pulse.scale.setScalar(0.55);
  // tides: the ocean bulge swells, leans ahead of the Moon, and an arrow tugs the Moon forward along its orbit
  const tide = outBack(seg(t, T_TIDE, T_TIDE + 0.6), 1.4) * (1 - seg(t, 33.4, 33.9));
  bulge.visible = tide > 0.001;
  bulge.scale.set(1 + 0.5 * tide, 1 + 0.05 * tide, 1 + 0.05 * tide);
  bulge.rotation.y = ang + 0.42; // leads the Moon
  const tugOn = seg(t, 27.4, 27.7) * (1 - seg(t, 30.9, 31.2));
  tug.visible = tugOn > 0.01;
  tug.position.copy(moonPos);
  tug.setDirection(new THREE.Vector3(-Math.sin(ang), 0, -Math.cos(ang)));
  tug.setLength(0.5 + 1.6 * tugOn, 0.55, 0.4);

  // background, the beacon's red/blue wash over the sky, camera, speed lines
  const [a, b] = bgAt(t);
  bgEl.style.background = VERTICAL
    ? `radial-gradient(130% 80% at 50% 42%, ${a} 0%, ${b} 80%)`
    : `radial-gradient(120% 120% at 32% 40%, ${a} 0%, ${b} 78%)`;
  const onDuty = name === "chair" && (t < 10.3 || (t >= 41.6 && t < 49.7) || t >= 55.6);
  const fast = Math.sin(TAU * 3.2 * t) > 0;
  policeEl.style.opacity = onDuty ? "0.55" : "0";
  policeEl.style.background = fast
    ? "radial-gradient(60% 40% at 15% 10%, rgba(255,45,61,0.75), rgba(255,45,61,0) 70%)"
    : "radial-gradient(60% 40% at 85% 10%, rgba(45,123,255,0.75), rgba(45,123,255,0) 70%)";
  placeCamera(t, name, whip);
  if (host.cameraOverride) host.cameraOverride(camera);
  drawLines(t, whip);

  renderer.clear();
  renderer.toneMappingExposure = name === "chair" ? 0.85 : 1.05;
  renderer.render(scene, camera);
  renderer.toneMappingExposure = 1.05;
  renderer.clearDepth();
  renderNumber(t);
  renderer.render(numScene, numCam);
}

""")

src = src.replace('for (const ch of "0123456789,+")', 'for (const ch of "0123456789,+.")')
src = src.replace("const fmt = (v) => Math.round(v).toLocaleString(\"en-US\");",
                  "const fmt = (v, dec = 0) => (dec ? v.toFixed(dec) : Math.round(v).toLocaleString(\"en-US\"));")
src = src.replace("const str = fmt(v) + (n.plus && p > 0.55 ? \"+\" : \"\");", "const str = fmt(v, n.dec) + (n.plus && p > 0.55 ? \"+\" : \"\");")
src = src.replace("const finalStr = fmt(n.value) + (n.plus ? \"+\" : \"\");", "const finalStr = fmt(n.value, n.dec) + (n.plus ? \"+\" : \"\");")
src = src.replace("// Challan: a cosmic traffic cop", "// Challan #3 \"Chand ki FIR\", built on Episode 1's scene. Episode 1's header follows.\n// Challan: a cosmic traffic cop")
open(P, "w", encoding="utf-8").write(src)
for name in ("SW.earth", "SW.orbit", "SW.galaxy", "T_SUN_WORD", "T_SELF_BEEP"):
    if name in src:
        print("still referenced:", name)
print("ok", len(src))
