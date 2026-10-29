"""Shared scene patcher for Cycle 2 episodes (Challan #4 onward): turns Episode 1's scene into an episode from data.

Each episode keeps a small `patch-scene.py` that calls `build(ep_dir, cfg)`. Characters, materials, 3D numbers, whips
and speed lines stay Episode 1's code; what changes per episode is data plus one block of world JS:

  cfg = {
    "title": str, "dur": float,
    "space": [[in, out], ...],          # time ranges in the episode's space world (whip out at `in`, snap home at `out`)
    "nums": [{value, dec?, plus?, fly, land, lock, out, rim}],
    "act": {                             # all acting is keyed data (see the JS below for the named hand positions)
      "guy": {handR, handL, lid, yaw, mood: {startle: [t...], smug|confused|laugh|sip|lookUp: [[in, out], ...]}},
      "cop": {handR, handL, lid, aim: [[t, target]], beam: [[in, out]], screen: [[t, text, blink]], duty: [[in, out]],
              lazyFrom, sweat: [in, out], mood: {shout: [t...], confused|suspicious|hopeful|smug|shock|sad|sheepish|sip|
              toCam|lookSky: [[in, out], ...]}},
      "k2": {pop, give, sipA, sipB, end},  # the second kulhad: out of the guy's pocket, into the cop's hand
      "alt": [[in, out]],                # windows where the home sky fades to BG.alt (e.g. the teaser)
    },
    "bg": {"home": [inner, outer], "space": [...], "alt": [...]},
    "shots": [...], "space_shots": [...],  # camera keys; `look` may name a FOCUS point (string) in space shots
    "world_js": str,                     # defines epWorld (Group), FOCUS {}, skyAt(t) -> {name: [x, y, z]}, episodeRender(t, name)
    "exposure": [home, space],
  }
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup(ep):
    """Copies Episode 1's scene, vendor libs, fonts and own sound effects into the episode (fresh copy every run)."""
    a = os.path.join(ep, "assets")
    os.makedirs(os.path.join(a, "audio"), exist_ok=True)
    for d in ("vendor", "fonts"):
        shutil.rmtree(os.path.join(a, d), ignore_errors=True)
        shutil.copytree(os.path.join(ROOT, "assets", d), os.path.join(a, d))
    shutil.copy(os.path.join(ROOT, "assets/challan-scene.js"), os.path.join(a, "challan-scene.js"))
    for f in ("radar.mp3", "trombone.mp3", "whistle.mp3"):
        shutil.copy(os.path.join(ROOT, "assets/audio", f), os.path.join(a, "audio", f))


GUY_JS = """  // ---- acting (guy-local positions; he faces +z, the cop stands to his front right). Keys and moods: ACT.guy
  const GP = {
    REST_R: [0.16, 1.78, 0.6], SIP_R: [0.05, 2.3, 0.55], RAISE_R: [0.32, 2.3, 0.8], TOAST_R: [0.42, 2.6, 1.0], SKY_R: [0.3, 2.95, 0.55],
    REST_L: [-0.3, 1.3, 0.58], POCKET: [-0.12, 1.45, 0.42], OFFER: [0.42, 2.0, 1.0], POINT_UP: [-0.25, 3.05, 0.6], OPEN_L: [-0.55, 2.1, 0.95],
  };
  const named = (keys) => keys.map(([t, v, e]) => [t, typeof v === "string" ? GP[v] : v, e]);
  const HAND_R = named(ACT.guy.handR), HAND_L = named(ACT.guy.handL);
  function pose(t, ti = t) {
    const M = ACT.guy.mood;
    const breathe = Math.sin(TAU * ti / 1.5);
    const startle = pulseAt(t, M.startle);
    const confused = mood(t, M.confused);
    const smug = mood(t, M.smug, 0.25);
    const laugh = mood(t, M.laugh, 0.1);
    const sip = mood(t, M.sip, 0.1);
    const lookUp = mood(t, M.lookUp, 0.3);
    const wind = gust(t);
    fig.position.y = 0.018 * breathe + 0.12 * startle + 0.03 * Math.abs(Math.sin(t * 22)) * laugh;
    torso.scale.set(1.08 * (1 + 0.015 * breathe), 1 - 0.015 * breathe + 0.06 * startle, 0.88);
    head.rotation.y = track(t, ACT.guy.yaw) + 0.06 * Math.sin(TAU * ti / 5);
    head.rotation.z = 0.06 * Math.sin(TAU * ti / 3) + 0.12 * confused - 0.08 * smug;
    head.rotation.x = -0.04 - 0.16 * sip - 0.12 * laugh + 0.04 * Math.sin(t * 22) * laugh - 0.42 * lookUp;
    head.position.y = 2.62 + 0.012 * breathe;
    const talking = within(t, TALK.guy) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, ACT.guy.lid),
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
"""

COP_JS = """  // ---- acting (cop-local positions; he faces +z, the guy sits to his front left). Keys and moods: ACT.cop
  const CP = {
    AIM: [0.3, 2.15, 0.72], UP: [0.34, 2.8, 0.42], LOW: [0.4, 1.55, 0.32],
    HIP: [-0.5, 1.42, 0.12], STOP: [-0.42, 2.4, 0.62], TAKE: [-0.32, 1.98, 0.86], HOLD: [-0.22, 1.86, 0.62], SIP: [-0.06, 2.62, 0.55],
  };
  const named = (keys) => keys.map(([t, v, e]) => [t, typeof v === "string" ? CP[v] : v, e]);
  const HAND_R = named(ACT.cop.handR), HAND_L = named(ACT.cop.handL);
  function pose(t, ti, aims) {
    const M = ACT.cop.mood;
    const breathe = Math.sin(TAU * ti / 1.7);
    const shout = pulseAt(t, M.shout);
    const hopeful = mood(t, M.hopeful);
    const confused = mood(t, M.confused);
    const suspicious = mood(t, M.suspicious);
    const smug = mood(t, M.smug);
    const shock = mood(t, M.shock, 0.08);
    const sad = mood(t, M.sad, 0.15);
    const sheepish = mood(t, M.sheepish);
    const sip = mood(t, M.sip, 0.1);
    const toCam = mood(t, M.toCam, 0.3);
    const lookSky = mood(t, M.lookSky, 0.35);
    const stern = 1 - Math.max(smug, shock, sad, sheepish, hopeful, confused);
    fig.position.y = 0.015 * breathe - 0.08 * sad + 0.08 * shout;
    fig.rotation.x = 0.1 * shout - 0.04 * sad;
    fig.rotation.y = 0.45 * toCam;
    torso.scale.set(1.12 * (1 + 0.02 * breathe), 1 - 0.02 * breathe - 0.05 * sad, 0.95);
    belly.scale.setScalar(1 + 0.03 * breathe);
    head.rotation.x = -0.03 + 0.28 * sad - 0.1 * shock - 0.15 * sip - 0.3 * lookSky * (1 - shout);
    head.rotation.z = 0.04 * Math.sin(TAU * ti / 3.4) + 0.1 * smug - 0.08 * hopeful + 0.14 * confused - 0.06 * suspicious;
    head.rotation.y = lerp(lerp(-0.25, 0, Math.max(shock, sad)), 0.1, toCam) + 0.05 * Math.sin(TAU * ti / 5);
    const talking = within(t, TALK.cop) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, ACT.cop.lid) + 0.55 * suspicious,
      eyeS: 1 + 0.5 * shock + 0.12 * hopeful + 0.15 * confused,
      // stern: brows in a V; shock: high; sad: inner ends up; hopeful/confused: up and soft; suspicious: one brow up
      brows: [-0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * hopeful + 0.06 * confused, -0.3 * stern + 0.25 * sad + 0.12 * hopeful + 0.2 * confused,
        -0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * smug + 0.05 * hopeful + 0.1 * suspicious, 0.3 * stern - 0.25 * sad - 0.2 * smug - 0.12 * hopeful - 0.1 * confused],
      curve: lerp(lerp(lerp(-0.6, 1, Math.max(smug, sheepish, hopeful)), 0.1, confused), -1, sad),
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
    // beacon: urgent while on duty; lazy once he has his chai
    const onDuty = within(t, ACT.cop.duty);
    const fast = Math.sin(TAU * 3.2 * t) > 0 ? 1 : 0;
    const lazy = t > ACT.cop.lazyFrom ? 0.35 + 0.35 * Math.sin(TAU * 0.6 * t) : 0;
    const r = onDuty ? fast : lazy, b = onDuty ? 1 - fast : lazy * 0.8;
    bR.material.color.set("#FF2D3D").multiplyScalar(0.35 + 0.65 * r);
    bB.material.color.set("#2D7BFF").multiplyScalar(0.35 + 0.65 * b);
    lightR.intensity = 9 * r;
    lightB.intensity = 9 * b;
    const [s0, s1] = ACT.cop.sweat;
    const sw = seg(t, s0 + 0.1, s1);
    sweat.visible = t > s0 && t < s1;
    sweat.position.set(0.36, 0.18 - 0.3 * sw, 0.28);
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR, 0.24);
    gun.position.copy(hR).add(new THREE.Vector3(0, 0.08, 0.04));
    // the gun swings from target to target with a soft overshoot
    const A = ACT.cop.aim;
    let target = aims[A[0][1]].clone();
    for (let i = 1; i < A.length && t >= A[i][0]; i++) {
      target = aims[A[i - 1][1]].clone().lerp(aims[A[i][1]], outBack(seg(t, A[i][0], A[i][0] + 0.3), 1.2));
    }
    fig.updateMatrixWorld(true);
    gun.lookAt(fig.localToWorld(target.clone()));
    const bw = ACT.cop.beam.find(([a, b]) => t >= a && t < b);
    beam.visible = !!bw;
    beam.scale.set(1, 1, 0.01 + 30 * outExpo(bw ? seg(t, bw[0], bw[0] + 0.3) : 0));
    beam.material.opacity = 0.9;
    if (host.gunScreen) drawScreen(host.gunScreen, true);
    else {
      let s = ACT.cop.screen[0];
      for (const x of ACT.cop.screen) if (t >= x[0]) s = x;
      drawScreen(s[1], !s[2] || Math.floor(t * 3) % 2 === 0);
    }
    return { handL: hL };
  }
"""

DUO_JS = """  const tmp = new THREE.Vector3();
  const camWorld = new THREE.Vector3(0.6, 2.7, 9);
  function pose(t, ti = t) {
    duo.updateMatrixWorld(true);
    const local = (p) => cop.fig.worldToLocal(duo.localToWorld(V(p)));
    const aims = { guy: cop.fig.worldToLocal(guy.group.localToWorld(new THREE.Vector3(0, 2.62, 0))), cam: local(camWorld.toArray()) };
    const sky = skyAt(t);
    for (const k in sky) aims[k] = local(sky[k]);
    const g = guy.pose(t, ti);
    aims.down = cop.fig.worldToLocal(cop.fig.localToWorld(new THREE.Vector3(0.4, 0.35, 1.6)));
    const c = cop.pose(t, ti, aims);
    duo.updateMatrixWorld(true);
    const K2 = ACT.k2;
    k2.visible = t > K2.pop && t < K2.end + 0.3;
    const from = guy.fig.localToWorld(g.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    const to = cop.fig.localToWorld(c.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    duo.worldToLocal(from);
    duo.worldToLocal(to);
    tmp.copy(t < K2.give ? from : to);
    k2.position.copy(tmp);
    k2.scale.setScalar(outBack(seg(t, K2.pop, K2.pop + 0.2), 2) * (1 - seg(t, K2.end, K2.end + 0.3)));
    const copSip = smooth(K2.sipA, K2.sipA + 0.1, t) * (1 - smooth(K2.sipB - 0.15, K2.sipB, t));
    k2.rotation.set(-0.8 * (t >= K2.give ? copSip : 0), t >= K2.give ? -0.55 : 0.4, 0);
    if (cap) cap.rotation.x = -0.012 * t;
  }
"""

CAMERA_JS = """// ---------------------------------------------------------------- camera
const up = new THREE.Vector3(0, 1, 0);
const SHOTS_V = __SHOTS__;
const SPACE_SHOTS_V = __SPACE_SHOTS__;
const scaleShots = (list) => list.map((s) => ({ ...s, dist: s.dist * 0.62, to: s.to ? { dist: s.to.dist * 0.62 } : undefined }));
const SHOTS = VERTICAL ? SHOTS_V : scaleShots(SHOTS_V);
const SPACE_SHOTS = VERTICAL ? SPACE_SHOTS_V : scaleShots(SPACE_SHOTS_V);

const lookOf = (s, t) => (typeof s.look === "string" ? FOCUS[s.look](t).clone() : V(s.look));
function shotAt(t, list) {
  let i = 0;
  while (i + 1 < list.length && t >= list[i + 1].t) i++;
  const s = list[i];
  const next = list[i + 1];
  const end = next ? next.t : DUR;
  let look = lookOf(s, t), dir = V(s.dir).normalize(), dist = s.dist;
  if (s.to) dist = lerp(s.dist, s.to.dist, inOutSine(seg(t, s.t, end)));
  if (s.blend && i > 0) {
    const p = list[i - 1];
    const x = inOutSine(seg(t, s.t, s.t + s.blend));
    const pDist = p.to ? p.to.dist : p.dist;
    look = lookOf(p, t).lerp(look, x);
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
  return within(t, SPACE) ? "space" : "chair";
}

// space: arrive close, pull back with a soft overshoot, drift slowly, rush in on the snap home
function distMul(t) {
  const [a, b] = SPACE.find(([a, b]) => t >= a && t < b);
  const inn = a <= 0.01 ? 1 : lerp(0.32, 1, outBack(seg(t, a, a + 0.6), 1.3));
  const drift = 1 + 0.008 * (t - a);
  const out = lerp(1, 0.25, inCubic(seg(t, b - 0.09, b)));
  return inn * drift * out;
}

function placeCamera(t, name, whip) {
  let look, dir, dist;
  if (name === "chair") {
    ({ look, dir, dist } = shotAt(t, SHOTS));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 6));
    for (const [a, b] of SPACE) {
      if (a > 0.01) dist *= 1 + 3.2 * inCubic(seg(t, a - 0.22, a)) * (t < a ? 1 : 0);
      if (t >= b && t < b + 0.55) dist *= lerp(4.2, 1, outBack(seg(t, b, b + 0.55), 1.2));
    }
  } else {
    ({ look, dir, dist } = shotAt(t, SPACE_SHOTS));
    dir.applyAxisAngle(up, 0.05 * Math.sin(TAU * t / 9)).normalize();
    dist *= distMul(t);
  }
  camera.position.copy(look).addScaledVector(dir, dist);
  camera.lookAt(look);
  camera.rotateZ(0.05 * whip.level * (whip.dir || 1));
  camera.fov = (VERTICAL ? 38 : 35) + 16 * whip.level;
  camera.updateProjectionMatrix();
}

"""

BG_JS = """// ---------------------------------------------------------------- background
const BG = __BG__;
const bgEl = document.getElementById("w-bg");
const policeEl = document.getElementById("w-police");
function bgAt(t) {
  // the whip to space and the snap home cross over fast; the home sky can fade to BG.alt (ACT.alt windows)
  const mix = (p, q, x) => [col(p[0]).lerp(col(q[0]), x), col(p[1]).lerp(col(q[1]), x)];
  let x = 0;
  for (const [a, b] of SPACE) {
    if (t >= a - 0.14 && t < b + 0.06) x = a <= 0.01 ? (t < b - 0.06 ? 1 : 1 - inOutSine(seg(t, b - 0.06, b + 0.06)))
      : t < a + 0.14 ? inOutSine(seg(t, a - 0.14, a + 0.14)) : 1 - inOutSine(seg(t, b - 0.06, b + 0.06));
  }
  const [h0, h1] = mix(BG.home, BG.alt, mood(t, ACT.alt, 0.6));
  const s = BG.space;
  return [`#${h0.lerp(col(s[0]), x).getHexString()}`, `#${h1.lerp(col(s[1]), x).getHexString()}`];
}

"""

RENDER_JS = """// ---------------------------------------------------------------- render(t)
const tmpV = new THREE.Vector3();
function render(t) {
  const whip = whipLevel(t);
  const name = worldAt(t);
  chairWorld.visible = name === "chair";
  earthWorld.visible = orbitWorld.visible = galaxyWorld.visible = false;
  epWorld.visible = name === "space";
  stars.visible = true;
  stars.rotation.y = 0.02 * t;
  if (name === "chair") duo.pose(t);
  episodeRender(t, name);

  // background, the beacon's red/blue wash over the sky, camera, speed lines
  const [a, b] = bgAt(t);
  bgEl.style.background = VERTICAL
    ? `radial-gradient(130% 80% at 50% 42%, ${a} 0%, ${b} 80%)`
    : `radial-gradient(120% 120% at 32% 40%, ${a} 0%, ${b} 78%)`;
  const onDuty = within(t, ACT.cop.duty);
  const fast = Math.sin(TAU * 3.2 * t) > 0;
  policeEl.style.opacity = onDuty ? "0.55" : "0";
  policeEl.style.background = fast
    ? "radial-gradient(60% 40% at 15% 10%, rgba(255,45,61,0.75), rgba(255,45,61,0) 70%)"
    : "radial-gradient(60% 40% at 85% 10%, rgba(45,123,255,0.75), rgba(45,123,255,0) 70%)";
  placeCamera(t, name, whip);
  if (host.cameraOverride) host.cameraOverride(camera);
  drawLines(t, whip);

  renderer.clear();
  renderer.toneMappingExposure = name === "chair" ? __EXP_HOME__ : __EXP_SPACE__;
  renderer.render(scene, camera);
  renderer.toneMappingExposure = 1.05;
  renderer.clearDepth();
  renderNumber(t);
  renderer.render(numScene, numCam);
}

"""


def build(ep, cfg):
    setup(ep)
    P = os.path.join(ep, "assets/challan-scene.js")
    src = open(P, encoding="utf-8").read()
    lines = json.load(open(os.path.join(ep, "assets/audio/lines.json"), encoding="utf-8"))
    talk = lambda who: [[round(l["words"][0]["start"], 2), round(l["words"][-1]["end"], 2)] for l in lines if l["speaker"] == who]
    whips = []
    for a, b in cfg["space"]:
        if a > 0.01:
            whips.append({"c": a, "b": 0.22, "a": 0.2, "dir": -1, "k": 1.1})
        whips.append({"c": b, "b": 0.09, "a": 0.12, "dir": 1, "k": 1.35})
    J = lambda x: json.dumps(x, ensure_ascii=False)

    def swap(start, end, new):
        nonlocal src
        i = src.index(start)
        j = src.index(end, i)
        src = src[:i] + new + src[j:]

    swap("// ---------------------------------------------------------------- timing", "// ---------------------------------------------------------------- helpers",
         f"""// ---------------------------------------------------------------- timing (dialogue track: assets/audio/lines.json)
// {cfg['title']}: built by tools/cycle2_patch.py from episodes/<ep>/patch-scene.py (all timing and acting is data)
const DUR = {cfg['dur']};
const SPACE = {J(cfg['space'])};
const WHIPS = {J(whips)};
const NUMS = {J(cfg['nums'])};
const ACT = {J(cfg['act'])};
// speaking windows for lip flap (first to last word of each line)
const TALK = {{
  cop: {J(talk('cop'))},
  guy: {J(talk('guy'))},
}};

""")
    src = src.replace("const V = (a) => new THREE.Vector3(a[0], a[1], a[2]);", """const V = (a) => new THREE.Vector3(a[0], a[1], a[2]);
// mood windows [[in, out], ...] eased over `e` s; one-shot jumps that rise and fall over 0.8 s; the hair gust after a snap home
const mood = (t, wins = [], e = 0.2) => wins.reduce((m, [a, b]) => Math.max(m, smooth(a, a + e, t) * (1 - smooth(b - e, b, t))), 0);
const pulseAt = (t, starts = []) => starts.reduce((m, a) => Math.max(m, t >= a && t < a + 0.8 ? Math.sin(Math.PI * seg(t, a, a + 0.8)) : 0), 0);
const gust = (t) => WHIPS.reduce((m, w) => (w.dir > 0 && t >= w.c && t < w.c + 1.2 ? Math.max(m, Math.exp(-(((t - w.c) / 0.32) ** 2))) : m), 0);""")
    swap("  // ---- acting (guy-local", "  return { group: g, fig, pose, kulhad2 };", GUY_JS)
    swap("  // ---- acting (cop-local", "  return { group: g, fig, pose, kulhadSlot, head };", COP_JS)
    swap("  const tmp = new THREE.Vector3();\n  function pose(t, ti = t) {", "  return { group: duo, pose };", DUO_JS)
    src = src.replace("scene.add(orbitWorld);\n", "scene.add(orbitWorld);\n\n" + cfg["world_js"].strip("\n") + "\nscene.add(epWorld);\n", 1)
    cam = CAMERA_JS.replace("__SHOTS__", J(cfg["shots"])).replace("__SPACE_SHOTS__", J(cfg["space_shots"]))
    swap("// ---------------------------------------------------------------- camera", "// ---------------------------------------------------------------- 3D numbers (overlay scene)", cam)
    swap("// ---------------------------------------------------------------- background", "// ---------------------------------------------------------------- render(t)", BG_JS.replace("__BG__", J(cfg["bg"])))
    exp = cfg.get("exposure", [0.85, 1.05])
    swap("// ---------------------------------------------------------------- render(t)", "host.render = render;",
         RENDER_JS.replace("__EXP_HOME__", str(exp[0])).replace("__EXP_SPACE__", str(exp[1])))
    # Episode 1 fix-ups carried by every episode since #2
    src = src.replace('      c.font = "bold 116px monospace";', '      c.font = `bold ${Math.min(116, Math.floor(470 / (0.6 * text.length)))}px monospace`;')
    src = src.replace("  lctx.clearRect(0, 0, LW, LH);\n  if (whip.level < 0.02) return;",
                      "  lctx.clearRect(0, 0, LW, LH);\n  lines.style.visibility = whip.level < 0.02 ? \"hidden\" : \"visible\";\n  if (whip.level < 0.02) return;")
    src = src.replace('for (const ch of "0123456789,+")', 'for (const ch of "0123456789,+.")')
    src = src.replace("const fmt = (v) => Math.round(v).toLocaleString(\"en-US\");",
                      "const fmt = (v, dec = 0) => (dec ? v.toFixed(dec) : Math.round(v).toLocaleString(\"en-US\"));")
    src = src.replace("const str = fmt(v) + (n.plus && p > 0.55 ? \"+\" : \"\");", "const str = fmt(v, n.dec) + (n.plus && p > 0.55 ? \"+\" : \"\");")
    src = src.replace("const finalStr = fmt(n.value) + (n.plus ? \"+\" : \"\");", "const finalStr = fmt(n.value, n.dec) + (n.plus ? \"+\" : \"\");")
    src = src.replace("// Challan: a cosmic traffic cop", f"// {cfg['title']}, built on Episode 1's scene. Episode 1's header follows.\n// Challan: a cosmic traffic cop")
    for name in ("SW.", "T_SUN_WORD", "T_SELF_BEEP", "T_BEAM", "T_END"):
        if name in src:
            print("still referenced:", name)
    open(P, "w", encoding="utf-8").write(src)
    print("ok", P, len(src))
