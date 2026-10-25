"""Turns Episode 1's scene (assets/challan-scene.js, copied here) into Challan #2 "Wazan Ka Challan".

Only the episode-specific blocks are replaced: timing, both characters' keyed acting, the duo's kulhad hand-off,
the two space worlds (Moon, Jupiter), camera shots, background colours and render(t). Characters, materials,
3D numbers, whips and speed lines are Episode 1's code, untouched. Run once on a fresh copy.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "assets/challan-scene.js")
src = open(P, encoding="utf-8").read()
lines = json.load(open(os.path.join(HERE, "assets/audio/lines.json"), encoding="utf-8"))
DUR = 57.13


def talk(who):
    return [[round(l["words"][0]["start"], 2), round(l["words"][-1]["end"], 2)] for l in lines if l["speaker"] == who]


def swap(start, end, new, keep_end=True):
    global src
    i = src.index(start)
    j = src.index(end, i)
    src = src[:i] + new + (src[j:] if keep_end else src[j + len(end):])


# ---------------------------------------------------------------- timing
swap("// ---------------------------------------------------------------- timing", "// ---------------------------------------------------------------- helpers", f"""// ---------------------------------------------------------------- timing (dialogue track: assets/audio/lines.json)
// Challan #2 "Wazan Ka Challan": home -> the Moon (whip lands on "चाँद") -> Jupiter (on "Jupiter") -> snap home before "तो वहाँ सीधा jail!"
const DUR = {DUR};
const SW = {{ moon: 17.7, jupiter: 24.06, snap: 29.25 }};
const WHIPS = [
  {{ c: SW.moon, b: 0.2, a: 0.18, dir: -1, k: 1 }},
  {{ c: SW.jupiter, b: 0.2, a: 0.18, dir: -1, k: 1.1 }},
  {{ c: SW.snap, b: 0.09, a: 0.12, dir: 1, k: 1.35 }}, // snap back: the fastest move
];
const NUMS = [
  {{ value: 168, plus: false, fly: 2.42, land: 2.78, lock: 3.66, out: 5.95, rim: "#FF2D3D" }}, // "एक सौ अड़सठ" on the chair
  {{ value: 28, plus: false, fly: 21.66, land: 22.01, lock: 22.45, out: 23.4, rim: "#8E9BB8" }}, // "अट्ठाईस" on the Moon
  {{ value: 400, plus: true, fly: 26.66, land: 27.01, lock: 27.57, out: 29.05, rim: "#E8914A" }}, // "चार सौ" on Jupiter
  {{ value: 168, plus: false, fly: 32.68, land: 33.03, lock: 33.91, out: 36.6, rim: "#34C759" }}, // "एक सौ अड़सठ": mass, everywhere
];
const T_BEAM = 52.3; // the gun fires at the Moon rising for the teaser ("चाँद की FIR")
const T_BEAM_OFF = 54.5;
const T_TROMBONE = 37.35;
const T_END = 38.75; // end card
// speaking windows for lip flap (first to last word of each line)
const TALK = {{
  cop: {json.dumps(talk("cop"))},
  guy: {json.dumps(talk("guy"))},
}};

""")

# ---------------------------------------------------------------- the guy's acting
swap("  // ---- acting (guy-local", "  return { group: g, fig, pose, kulhad2 };", """  // ---- acting (guy-local positions; he faces +z, the cop stands to his front right)
  const REST_R = [0.16, 1.78, 0.6], SIP_R = [0.05, 2.3, 0.55], RAISE_R = [0.32, 2.3, 0.8], TOAST_R = [0.42, 2.6, 1.0];
  const REST_L = [-0.3, 1.3, 0.58], CHEST = [-0.06, 1.85, 0.36], POCKET = [-0.12, 1.45, 0.42], OFFER = [0.42, 2.0, 1.0];
  const DOWN = [-0.42, 1.12, 0.92], WAVE = [-0.36, 2.75, 0.7];
  const HAND_R = [[0, SIP_R], [0.95, SIP_R], [1.2, REST_R, "back"], [6.9, REST_R], [7.1, RAISE_R, "back"], [8.1, RAISE_R], [8.4, REST_R],
    [34.9, REST_R], [35.1, RAISE_R, "back"], [36.3, RAISE_R], [36.6, REST_R], [38.85, REST_R], [39.05, SIP_R], [39.7, SIP_R], [40.0, REST_R],
    [42.0, REST_R], [42.2, SIP_R], [43.0, SIP_R], [43.3, REST_R], [47.75, REST_R], [48.0, TOAST_R, "back"], [50.4, TOAST_R], [50.7, REST_R],
    [56.65, REST_R], [57.05, SIP_R]];
  const HAND_L = [[0, REST_L], [9.3, REST_L], [9.5, CHEST, "back"], [10.4, CHEST], [10.6, REST_L], [14.1, REST_L], [14.3, DOWN, "back"],
    [16.4, DOWN], [16.7, REST_L], [37.8, REST_L], [37.95, POCKET], [38.05, POCKET], [38.3, OFFER, "back"], [38.6, OFFER], [38.85, REST_L],
    [54.7, REST_L], [54.95, WAVE, "back"], [56.3, WAVE], [56.7, REST_L]];
  const LID = [[0, 1.1], [0.95, 1.1], [1.05, -1.75, "snap"], [1.6, -1.35], [5.9, -1.35], [6.2, -0.85], [29.2, -0.85], [31.3, -0.6], [37.3, -0.6],
    [37.4, 1.0], [37.8, 1.0], [38.0, 0.05], [38.95, 0.05], [39.05, 1.1], [39.7, 1.1], [40.0, 0.05], [42.1, 0.05], [42.2, 1.1], [43.0, 1.1],
    [43.3, -0.85], [47.8, -0.85], [48.0, -1.45], [50.4, -1.45], [50.7, -0.85], [56.6, -0.85], [57.0, 1.1]];
  const YAW = [[0, 0], [1.0, 0], [1.2, 0.55, "back"], [47.8, 0.55], [48.05, -0.35, "back"], [50.5, -0.35], [50.8, 0.55], [56.7, 0.55], [57.1, 0]];
  function pose(t, ti = t) {
    const breathe = Math.sin(TAU * ti / 1.5);
    const startle = Math.sin(Math.PI * seg(t, 1.0, 1.8)) * (t < 1.8 ? 1 : 0);
    const confused = smooth(1.7, 1.9, t) * (1 - smooth(5.8, 6.1, t));
    const smug = smooth(31.3, 31.6, t) * (1 - smooth(37.25, 37.4, t)) + smooth(16.85, 17.0, t) * (1 - smooth(17.5, 17.65, t));
    const laugh = smooth(37.35, 37.45, t) * (1 - smooth(37.85, 38.0, t));
    const sip = smooth(38.95, 39.05, t) * (1 - smooth(39.7, 39.9, t)) + smooth(42.1, 42.2, t) * (1 - smooth(43.0, 43.2, t))
      + (t < 0.95 ? 1 : 0) * (1 - smooth(0.93, 1.05, t)) + smooth(56.95, 57.05, t);
    const rise = smooth(55.5, 55.9, t) * (1 - smooth(56.6, 57.0, t)); // "मैं चला...": half out of the chair
    const dt = t - SW.snap;
    const wind = dt >= 0 && dt < 1.2 ? Math.exp(-((dt / 0.32) ** 2)) : 0;
    fig.position.y = 0.018 * breathe + 0.12 * startle + 0.03 * Math.abs(Math.sin(t * 22)) * laugh + 0.22 * rise;
    fig.position.z = 0.12 * rise;
    fig.rotation.x = 0.12 * rise;
    torso.scale.set(1.08 * (1 + 0.015 * breathe), 1 - 0.015 * breathe + 0.06 * startle, 0.88);
    head.rotation.y = track(t, YAW) + 0.06 * Math.sin(TAU * ti / 5);
    head.rotation.z = 0.06 * Math.sin(TAU * ti / 3) + 0.12 * confused - 0.08 * smug;
    head.rotation.x = -0.04 - 0.16 * sip - 0.12 * laugh + 0.04 * Math.sin(t * 22) * laugh;
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
  const AIM = [0.3, 2.15, 0.72], UP = [0.34, 2.8, 0.42], BLOW = [0.5, 2.75, 0.32], LOW = [0.4, 1.55, 0.32];
  const HIP = [-0.5, 1.42, 0.12], STOP = [-0.42, 2.4, 0.62], TAKE = [-0.32, 1.98, 0.86], HOLD = [-0.22, 1.86, 0.62], SIP = [-0.06, 2.62, 0.55];
  const HAND_R = [[0, AIM], [30.4, AIM], [30.6, BLOW, "back"], [31.2, BLOW], [31.5, AIM], [37.3, AIM], [37.8, LOW], [40.45, LOW],
    [40.7, AIM, "back"], [51.9, AIM], [52.15, UP, "back"], [56.0, UP], [56.5, AIM]];
  const HAND_L = [[0, HIP], [0.95, HIP], [1.1, STOP, "back"], [2.6, STOP], [2.9, HIP], [38.4, HIP], [38.65, TAKE, "back"], [38.75, TAKE],
    [38.9, HOLD], [39.05, SIP], [39.7, SIP], [40.0, HOLD], [44.0, HOLD], [44.2, STOP, "back"], [45.1, STOP], [45.4, HOLD], [55.9, HOLD], [56.6, HIP]];
  const LID = [[0, -0.75], [16.85, -0.75], [16.95, -0.15], [17.6, -0.15], [29.25, -0.3], [33.0, -0.3], [33.05, -1.8, "snap"], [37.3, -1.8],
    [37.6, 0.35], [38.3, 0.35], [38.5, -0.9], [39.0, -0.9], [39.1, 1.1], [39.7, 1.1], [40.0, 0.05], [40.5, -0.75], [57.2, -0.75]];
  function pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal) {
    const breathe = Math.sin(TAU * ti / 1.7);
    const shout = Math.sin(Math.PI * seg(t, 1.0, 1.7)) * (t < 1.7 ? 1 : 0);
    const puzzled = smooth(16.85, 17.0, t) * (1 - smooth(17.5, 17.7, t));
    const smug = smooth(29.3, 29.5, t) * (1 - smooth(31.2, 31.4, t)) + smooth(50.6, 50.8, t) * (1 - smooth(54.4, 54.6, t));
    const shock = smooth(33.0, 33.1, t) * (1 - smooth(37.3, 37.5, t));
    const sad = smooth(37.3, 37.6, t) * (1 - smooth(38.2, 38.45, t));
    const sheepish = smooth(38.3, 38.5, t) * (1 - smooth(40.35, 40.55, t));
    const sip = smooth(39.0, 39.1, t) * (1 - smooth(39.7, 39.9, t));
    const toCam = smooth(40.45, 40.8, t) * (1 - smooth(47.75, 48.05, t));
    const stern = 1 - Math.max(smug, shock, sad, sheepish, puzzled);
    fig.position.y = 0.015 * breathe - 0.08 * sad + 0.08 * shout;
    fig.rotation.x = 0.1 * shout - 0.04 * sad;
    fig.rotation.y = 0.45 * toCam; // turns from the guy to the viewer
    torso.scale.set(1.12 * (1 + 0.02 * breathe), 1 - 0.02 * breathe - 0.05 * sad, 0.95);
    belly.scale.setScalar(1 + 0.03 * breathe);
    head.rotation.x = -0.03 + 0.28 * sad - 0.1 * shock - 0.15 * sip;
    head.rotation.z = 0.04 * Math.sin(TAU * ti / 3.4) + 0.1 * smug + 0.16 * puzzled;
    head.rotation.y = lerp(lerp(-0.25, 0, Math.max(shock, sad)), 0.1, toCam) + 0.05 * Math.sin(TAU * ti / 5);
    const talking = within(t, TALK.cop) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.5 * shock + 0.15 * puzzled,
      // stern: brows in a V; shock: high; sad: inner ends up; puzzled: one up, one down
      brows: [-0.02 * stern + 0.09 * shock + 0.02 * sad + 0.07 * puzzled, -0.3 * stern + 0.25 * sad + 0.2 * puzzled,
        -0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * smug - 0.02 * puzzled, 0.3 * stern - 0.25 * sad - 0.2 * smug + 0.1 * puzzled],
      curve: lerp(lerp(-0.6, 1, Math.max(smug, sheepish)), -1, sad),
      smileW: 1 + 0.2 * smug,
      open: Math.max(talking * 0.6, shock * 0.35 * (1 - talking)),
    });
    halves.forEach((h, i) => (h.rotation.z = (i ? 1 : -1) * (0.15 * stern + 0.25 * smug - 0.45 * sad)));
    if (host.copShout) {
      face.smile.scale.set(0.001, 0.001, 1);
      face.mouthO.position.y = -0.25;
      face.mouthO.scale.set(1.7, 1.9, 0.55);
    } else face.mouthO.position.y = -0.21;
    cap.rotation.z = 0.22 * sad + 0.08 * sheepish;
    cap.position.y = 0.36 - 0.03 * sad;
    // beacon: urgent while he is on duty (the stop, "jail", the subscribe challan, the loop back), dies with the trombone
    const onDuty = t < 6.2 || (t >= 29.25 && t < 31.3) || (t >= 40.45 && t < 47.8) || t >= 56.3;
    const fast = Math.sin(TAU * 3.2 * t) > 0 ? 1 : 0;
    const lazy = t > 38.4 ? 0.35 + 0.35 * Math.sin(TAU * 0.6 * t) : 0;
    const r = onDuty ? fast : lazy, b = onDuty ? 1 - fast : lazy * 0.8;
    bR.material.color.set("#FF2D3D").multiplyScalar(0.35 + 0.65 * r);
    bB.material.color.set("#2D7BFF").multiplyScalar(0.35 + 0.65 * b);
    lightR.intensity = 9 * r;
    lightB.intensity = 9 * b;
    const sw = seg(t, 33.5, 37.3);
    sweat.visible = t > 33.4 && t < 37.4;
    sweat.position.set(0.36, 0.18 - 0.3 * sw, 0.28);
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR, 0.24);
    gun.position.copy(hR).add(new THREE.Vector3(0, 0.08, 0.04));
    const sky = moonLocal.clone();
    const barrelUp = hR.clone().add(new THREE.Vector3(0, 2, 0.4));
    const down = hR.clone().add(new THREE.Vector3(0.1, -1.2, 1.2));
    const go = (a, b, t0, d = 0.25) => a.clone().lerp(b, outBack(seg(t, t0, t0 + d), 1.2));
    let target = guyHeadLocal.clone();
    if (t >= 30.45 && t < 31.45) target = go(guyHeadLocal, barrelUp, 30.45, 0.2);
    else if (t >= 37.3 && t < 40.45) target = go(guyHeadLocal, down, 37.3, 0.5);
    else if (t >= 40.45 && t < 51.95) target = go(down, camLocal, 40.45, 0.3);
    else if (t >= 51.95 && t < 56.4) target = go(camLocal, sky, 51.95, 0.3);
    else if (t >= 56.4) target = go(sky, guyHeadLocal, 56.4, 0.3);
    fig.updateMatrixWorld(true);
    gun.lookAt(fig.localToWorld(target.clone()));
    // the beam: fires at the Moon rising on "चाँद की FIR"
    const bl = seg(t, T_BEAM, T_BEAM + 0.3);
    beam.visible = t >= T_BEAM && t < T_BEAM_OFF;
    beam.scale.set(1, 1, 0.01 + 30 * outExpo(bl));
    beam.material.opacity = 0.9;
    // screen readout: the radar gun is in weight mode this episode
    if (host.gunScreen) drawScreen(host.gunScreen, true);
    else if (t < 2.78 || t >= 56.4) drawScreen("KG?", Math.floor(t * 3) % 2 === 0);
    else if (t < 3.66) drawScreen(Math.round(168 * seg(t, 2.78, 3.66)) + " KG", true);
    else if (t >= 40.45 && t < 51.95) drawScreen(t < 43.9 ? "COMMENT" : "SUBSCRIBE?", Math.floor(t * 3) % 2 === 0 || t < 43.9);
    else if (t >= 51.95) drawScreen("FIR!", true);
    else drawScreen("168 KG", true);
    return { handL: hL };
  }
""")
# the gun's screen fits longer words this episode
src = src.replace('      c.font = "bold 116px monospace";', '      c.font = `bold ${Math.min(116, Math.floor(470 / (0.6 * text.length)))}px monospace`;')

# ---------------------------------------------------------------- the duo: kulhad hand-off and the cop's aim at the viewer
swap("  const tmp = new THREE.Vector3();\n  function pose(t, ti = t) {", "  return { group: duo, pose };", """  const tmp = new THREE.Vector3();
  const camWorld = new THREE.Vector3(0.6, 2.7, 9); // roughly where the camera sits for the to-camera shots
  function pose(t, ti = t) {
    duo.updateMatrixWorld(true);
    const guyHead = guy.group.localToWorld(new THREE.Vector3(0, 2.62, 0));
    const guyHeadLocal = cop.fig.worldToLocal(guyHead.clone());
    const selfHeadLocal = new THREE.Vector3(0, 2.82, 0);
    const camLocal = cop.fig.worldToLocal(duo.localToWorld(camWorld.clone()));
    const moonLocal = cop.fig.worldToLocal(duo.localToWorld(new THREE.Vector3(1.1, 4.7, -5)));
    const g = guy.pose(t, ti);
    const c = cop.pose(t, ti, guyHeadLocal, selfHeadLocal, camLocal, moonLocal);
    duo.updateMatrixWorld(true);
    // kulhad #2: out of the hoodie pocket after the trombone, into the cop's hand; he keeps it till the loop
    k2.visible = t > 37.95 && t < 56.6;
    const from = guy.fig.localToWorld(g.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    const to = cop.fig.localToWorld(c.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    duo.worldToLocal(from);
    duo.worldToLocal(to);
    tmp.copy(t < 38.7 ? from : to);
    k2.position.copy(tmp);
    k2.scale.setScalar(outBack(seg(t, 37.95, 38.15), 2) * (1 - seg(t, 56.3, 56.6)));
    const copSip = smooth(39.0, 39.1, t) * (1 - smooth(39.7, 39.9, t));
    k2.rotation.set(-0.8 * (t >= 38.7 ? copSip : 0), t >= 38.7 ? -0.55 : 0.4, 0);
    if (cap) cap.rotation.x = -0.012 * t - 0.25 * inOutSine(seg(t, T_END, T_END + 1.7)) * (1 - inOutSine(seg(t, 40.4, 40.6)));
  }
""")

# ---------------------------------------------------------------- the Moon and Jupiter worlds (added after Episode 1's worlds)
src = src.replace("scene.add(earthWorld);\n", """scene.add(earthWorld);

// ---- Challan #2 worlds: the Moon (grey, cratered, the tiny duo standing on it) and Jupiter (banded, Great Red Spot)
Object.assign(EARTH_COLORS, {
  moonHi: "#B4B8C6", moonMid: "#8E93A4", moonMare: "#5E6376", crater: "#727789",
  jA: "#EBCB9E", jB: "#C4834E", jC: "#A85F33", jD: "#7E3F22", jE: "#D89A62", spot: "#B02E1A",
});
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
function jupiterKind(m) {
  if (m.distanceTo(new THREE.Vector3(0.35, -0.3, 0.89).normalize()) < 0.24) return "spot";
  const lon = Math.atan2(m.z, m.x);
  const b = m.y * 5.2 + 0.18 * Math.sin(lon * 3 + m.y * 4);
  const k = ((Math.floor(b) % 5) + 5) % 5;
  return ["jA", "jC", "jE", "jD", "jB"][k];
}
function makeBody(radius, detail, kindOf) {
  const m = new THREE.Mesh(paintLowPoly(new THREE.IcosahedronGeometry(radius, detail), kindOf), earthMaterial());
  m.material.clearcoat = 0.1;
  return m;
}
const moonWorld = new THREE.Group();
const moonSpin = new THREE.Group();
moonSpin.add(makeBody(1.6, 10, moonKind));
const moonDuo = makeDuo({ ground: false });
moonDuo.group.scale.setScalar(0.11);
moonDuo.group.position.set(0, 1.6, 0);
moonSpin.add(moonDuo.group);
moonWorld.add(moonSpin);
scene.add(moonWorld);

const jupWorld = new THREE.Group();
const jupSpin = new THREE.Group();
jupSpin.rotation.z = 0.05;
jupSpin.add(makeBody(2.3, 16, jupiterKind));
const jupDuo = makeDuo({ ground: false });
jupDuo.group.scale.setScalar(0.1);
jupDuo.group.position.set(0, 2.3, 0);
jupSpin.add(jupDuo.group);
jupWorld.add(jupSpin);
scene.add(jupWorld);

// the Moon rising behind the home planet for the teaser ("अगला challan... चाँद की FIR")
const skyMoon = makeBody(0.9, 6, moonKind);
chairWorld.add(skyMoon);
""")

# ---------------------------------------------------------------- camera
swap("// ---------------------------------------------------------------- camera", "// ---------------------------------------------------------------- 3D numbers (overlay scene)", """// ---------------------------------------------------------------- camera
const WORLDS = VERTICAL
  ? {
      moon: { dir: [0, 0.32, 1], dist: 8.6, shift: [0, 0.75] },
      jupiter: { dir: [0, 0.28, 1], dist: 12.2, shift: [0, 1.0] },
    }
  : {
      moon: { dir: [0, 0.32, 1], dist: 8.0, shift: [2.0, 0.1] },
      jupiter: { dir: [0, 0.28, 1], dist: 11, shift: [2.8, 0] },
    };
const up = new THREE.Vector3(0, 1, 0);

// chair-world shot list: [start, look-at, direction, distance]; a shot either cuts in or blends from the last one
const SHOTS_V = [
  { t: 0, look: [-0.45, 2.15, 0.2], dir: [0.3, 0.12, 1], dist: 5.6, to: { dist: 5.0 } }, // hook: the guy sipping, the gun pokes in
  { t: 1.0, look: [0.95, 2.45, 0.5], dir: [-0.4, 0.1, 1], dist: 4.8, to: { dist: 4.5 } }, // "रुको!": the cop
  { t: 2.5, blend: 0.4, look: [0.3, 2.75, 0.35], dir: [-0.15, 0.14, 1], dist: 8.2 }, // the 168 lands above the chair
  { t: 6.15, look: [0.1, 2.2, 0.25], dir: [0.06, 0.24, 1], dist: 10.2, to: { dist: 9.2 } }, // the guy explains: two-shot
  { t: 16.85, look: [1.0, 2.75, 0.5], dir: [-0.35, 0.08, 1], dist: 4.0 }, // "मतलब?"
  { t: SW.snap, look: [0.2, 2.2, 0.3], dir: [0.04, 0.22, 1], dist: 9.6 }, // back home
  { t: 29.95, blend: 0.5, look: [0.95, 2.6, 0.5], dir: [-0.4, 0.1, 1], dist: 5.0 }, // "jail!": smug cop, gunslinger blow
  { t: 31.3, look: [0.1, 2.45, 0.25], dir: [0.06, 0.2, 1], dist: 9.8 }, // the reversal: two-shot, room for the 168
  { t: 33.0, blend: 1.0, look: [1.0, 3.05, 0.5], dir: [-0.35, 0.08, 1], dist: 4.6 }, // push in on the cop's shock
  { t: 37.25, blend: 0.6, look: [1.0, 2.6, 0.5], dir: [-0.3, 0.05, 1], dist: 3.6 }, // trombone: his face
  { t: 37.95, look: [0.15, 2.1, 0.25], dir: [0.06, 0.22, 1], dist: 9.8 }, // chai together: two-shot
  { t: T_END, blend: 1.6, look: [0.15, 3.4, 0.25], dir: [0.06, 0.5, 1], dist: 12.5 }, // end card: crane up and back
  { t: 40.45, look: [1.05, 2.75, 0.75], dir: [0.12, 0.1, 1], dist: 4.4, to: { dist: 4.0 } }, // to camera: the subscribe challan
  { t: 47.8, look: [-0.55, 2.35, 0.3], dir: [-0.1, 0.1, 1], dist: 4.7 }, // the guy raises his kulhad to camera
  { t: 50.55, look: [0.15, 3.4, 0.0], dir: [0.08, 0.3, 1], dist: 12.0 }, // teaser: the Moon rises
  { t: 54.6, look: [-0.45, 2.15, 0.2], dir: [0.3, 0.12, 1], dist: 5.2, to: { dist: 5.6 } }, // back to the hook frame: the loop
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
  if (t < SW.moon) return "chair";
  if (t < SW.jupiter) return "moon";
  if (t < SW.snap) return "jupiter";
  return "chair";
}

// distance multiplier for the space worlds: arrive close, pull back with a soft overshoot, drift, rocket out on the whip
function distMul(t, name) {
  const s0 = SW[name];
  const s1 = name === "moon" ? SW.jupiter : SW.snap;
  const inn = lerp(0.32, 1, outBack(seg(t, s0, s0 + 0.6), 1.3));
  const drift = 1 + 0.03 * (t - s0);
  const out = name === "jupiter" ? lerp(1, 0.25, inCubic(seg(t, s1 - 0.09, s1))) : 1 + 3.2 * inCubic(seg(t, s1 - 0.2, s1));
  return inn * drift * out;
}

function placeCamera(t, name, whip) {
  let look, dir, dist;
  if (name === "chair") {
    ({ look, dir, dist } = shotAt(t));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 6));
    if (t < SW.snap) dist *= 1 + 3.2 * inCubic(seg(t, SW.moon - 0.2, SW.moon));
    else dist *= lerp(4.2, 1, outBack(seg(t, SW.snap, SW.snap + 0.55), 1.2));
  } else {
    const w = WORLDS[name];
    const m = distMul(t, name);
    dir = V(w.dir).applyAxisAngle(up, 0.06 * Math.sin(TAU * t / 7.5)).normalize();
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
  chair: ["#FFD6A5", "#FF6B6B"],
  moon: ["#4A5275", "#141832"],
  jupiter: ["#F4B076", "#7A3418"],
};
const bgEl = document.getElementById("w-bg");
const policeEl = document.getElementById("w-police");
function bgAt(t) {
  // colours cross over inside each whip window
  const order = [[0, "chair"], [SW.moon, "moon"], [SW.jupiter, "jupiter"], [SW.snap, "chair"]];
  let from = BG.chair, to = BG.chair, x = 0;
  for (let i = 1; i < order.length; i++) {
    const [c, name] = order[i];
    const half = i === 3 ? 0.06 : 0.14;
    if (t >= c - half && t < c + half) {
      from = BG[order[i - 1][1]];
      to = BG[name];
      x = inOutSine(seg(t, c - half, c + half));
      break;
    }
    if (t >= c + half) from = to = BG[name];
  }
  const a = col(from[0]).lerp(col(to[0]), x), b = col(from[1]).lerp(col(to[1]), x);
  return [`#${a.getHexString()}`, `#${b.getHexString()}`];
}

""")

# ---------------------------------------------------------------- render(t)
swap("// ---------------------------------------------------------------- render(t)", "host.render = render;", """// ---------------------------------------------------------------- render(t)
function render(t) {
  const whip = whipLevel(t);
  const name = worldAt(t);
  chairWorld.visible = name === "chair";
  earthWorld.visible = orbitWorld.visible = galaxyWorld.visible = false;
  moonWorld.visible = name === "moon";
  jupWorld.visible = name === "jupiter";
  stars.visible = name === "moon";

  if (name === "chair") duo.pose(t);
  // the Moon turns slowly under the tiny duo; Jupiter spins fast (its day is under 10 hours)
  moonSpin.rotation.set(0.35, 0.18 * (t - SW.moon) - 0.25, 0);
  if (name === "moon") moonDuo.pose(t);
  jupSpin.rotation.y = 0.45 * (t - SW.jupiter);
  if (name === "jupiter") jupDuo.pose(t);
  // the teaser's Moon climbs over the home planet's horizon
  const rise = outBack(seg(t, 50.7, 52.3), 1.1);
  skyMoon.visible = t > 50.6 && t < 54.7;
  skyMoon.position.set(1.1, lerp(-2.0, 4.7, rise), -5);
  skyMoon.rotation.y = 0.3 * t;
  stars.rotation.y = 0.03 * t;

  // background, the beacon's red/blue wash over the sky, camera, speed lines
  const [a, b] = bgAt(t);
  bgEl.style.background = VERTICAL
    ? `radial-gradient(130% 80% at 50% 42%, ${a} 0%, ${b} 80%)`
    : `radial-gradient(120% 120% at 32% 40%, ${a} 0%, ${b} 78%)`;
  const onDuty = name === "chair" && (t < 6.2 || (t >= 29.25 && t < 31.3) || (t >= 40.45 && t < 47.8) || t >= 56.3);
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

# the 3D digits can carry a decimal point (Challan #3's 3.8)
src = src.replace('for (const ch of "0123456789,+")', 'for (const ch of "0123456789,+.")')
src = src.replace("const fmt = (v) => Math.round(v).toLocaleString(\"en-US\");",
                  "const fmt = (v, dec = 0) => (dec ? v.toFixed(dec) : Math.round(v).toLocaleString(\"en-US\"));")
src = src.replace("const str = fmt(v) + (n.plus && p > 0.55 ? \"+\" : \"\");", "const str = fmt(v, n.dec) + (n.plus && p > 0.55 ? \"+\" : \"\");")
src = src.replace("const finalStr = fmt(n.value) + (n.plus ? \"+\" : \"\");", "const finalStr = fmt(n.value, n.dec) + (n.plus ? \"+\" : \"\");")
src = src.replace("// Challan: a cosmic traffic cop", "// Challan #2 \"Wazan Ka Challan\", built on Episode 1's scene. Episode 1's header follows.\n// Challan: a cosmic traffic cop")
open(P, "w", encoding="utf-8").write(src)
for name in ("SW.earth", "SW.orbit", "SW.galaxy", "T_SUN_WORD", "T_SELF_BEEP", "31.3"):
    if name in src:
        print("still referenced:", name, [m.start() for m in re.finditer(re.escape(name), src)][:5])
print("ok", len(src))
