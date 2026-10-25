// ---------------------------------------------------------------- keyed acting
// track(t, [[time, value, ease?], ...]): values are numbers or [x, y, z]; ease "back" overshoots into the key.
function track(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [t0, v0] = keys[i];
    const [t1, v1, ease] = keys[i + 1];
    if (t < t1) {
      const x = ease === "back" ? outBack(seg(t, t0, t1), 1.4) : ease === "snap" ? outExpo(seg(t, t0, t1)) : inOutSine(seg(t, t0, t1));
      return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], x)) : lerp(v0, v1, x);
    }
  }
  return keys[keys.length - 1][1];
}
const V = (a) => new THREE.Vector3(a[0], a[1], a[2]);
const within = (t, wins) => wins.some(([a, b]) => t >= a && t < b);
// lip flap: two incommensurate sines so the mouth never repeats a pattern
const flap = (t) => clamp01(0.35 + 0.4 * Math.sin(t * 31) + 0.35 * Math.sin(t * 19.3 + 1.1));

// a kulhad: unglazed terracotta cup of chai
function makeKulhad() {
  const k = new THREE.Group();
  const terracotta = clay("#B5562F", { roughness: 0.92 });
  const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.1, 0.24, 28), terracotta);
  const lip = new THREE.Mesh(new THREE.TorusGeometry(0.145, 0.018, 8, 28), terracotta);
  lip.rotation.x = Math.PI / 2;
  lip.position.y = 0.12;
  const chai = new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.135, 0.01, 28), clay("#C68E5E", { roughness: 0.35 }));
  chai.position.y = 0.105;
  k.add(cup, lip, chai);
  return k;
}

// shared head pieces: skin sphere, ears, nose, eyes with lids and glints, brows, smile, open mouth
function makeFace(skin, { browMat, browR = 0.02, browLen = 0.1, noseR = 0.035 }) {
  const eyeMat = new THREE.MeshPhysicalMaterial({ color: "#1A1410", roughness: 0.25, clearcoat: 1 });
  const sparkle = new THREE.MeshBasicMaterial({ color: "#FFFFFF" });
  const mouthMat = clay("#5A2A1E");
  const head = new THREE.Group();
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.5, 48, 32), skin);
  skull.scale.set(1, 0.95, 0.95);
  head.add(skull);
  for (const sx of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), skin);
    ear.position.set(0.48 * sx, -0.02, 0);
    ear.scale.set(0.45, 0.75, 0.55);
    head.add(ear);
  }
  const nose = new THREE.Mesh(new THREE.SphereGeometry(noseR, 12, 10), skin);
  nose.position.set(0, -0.08, 0.47);
  head.add(nose);
  const eyes = [], lids = [], brows = [];
  for (const sx of [-1, 1]) {
    const eye = new THREE.Group();
    eye.position.set(0.18 * sx, -0.01, 0.425);
    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.075, 20, 16), eyeMat);
    ball.scale.set(0.85, 1.2, 0.5);
    const glint = new THREE.Mesh(new THREE.SphereGeometry(0.017, 10, 8), sparkle);
    glint.position.set(0.02, -0.012, 0.04);
    // eyelid: a skin hemisphere rotating over the eye (-PI/2 open, 0 half-closed, ~1.1 closed)
    const lid = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 10, 0, TAU, 0, Math.PI / 2), skin);
    lid.scale.set(0.075 * 0.85 * 1.15, 0.075 * 1.2 * 1.12, 0.075 * 0.5 * 1.3);
    eye.add(ball, glint, lid);
    head.add(eye);
    eyes.push(eye);
    lids.push(lid);
    const brow = new THREE.Group();
    brow.position.set(0.18 * sx, 0.15, 0.425);
    const bm = new THREE.Mesh(new THREE.CapsuleGeometry(browR, browLen, 6, 10), browMat);
    bm.rotation.z = Math.PI / 2;
    brow.add(bm);
    head.add(brow);
    brows.push(brow);
  }
  const smileGeo = new THREE.TorusGeometry(0.06, 0.012, 8, 20, Math.PI * 0.8);
  smileGeo.rotateZ(Math.PI * 0.1);
  const smile = new THREE.Mesh(smileGeo, mouthMat);
  smile.position.set(0, -0.2, 0.43);
  const mouthO = new THREE.Mesh(new THREE.SphereGeometry(0.045, 14, 10), mouthMat);
  mouthO.position.set(0, -0.21, 0.425);
  head.add(smile, mouthO);
  return { head, eyes, lids, brows, smile, mouthO };
}

// face state: lid angle, eye scale, brows [leftY, leftRot, rightY, rightRot], smile curve (1 smile, -1 frown), mouth open
function applyFace(f, { lid, eyeS = 1, brows = [0, 0, 0, 0], curve = 1, smileW = 1, open = 0 }) {
  f.lids.forEach((l) => (l.rotation.x = lid));
  f.eyes.forEach((e) => e.scale.setScalar(eyeS));
  f.brows[0].position.y = 0.15 + brows[0];
  f.brows[0].rotation.z = brows[1];
  f.brows[1].position.y = 0.15 + brows[2];
  f.brows[1].rotation.z = brows[3];
  f.smile.rotation.z = curve >= 0 ? Math.PI : 0;
  f.smile.position.y = curve >= 0 ? -0.2 : -0.25;
  const s = Math.max(0.001, 1 - clamp01(open));
  f.smile.scale.set(smileW * s, Math.max(0.001, Math.abs(curve)) * s, 1);
  f.mouthO.scale.set(0.001 + clamp01(open), 0.001 + 1.35 * clamp01(open), 0.4);
}

function makeArms(parent, sleeve, cuffMat, skin, shoulder) {
  const arms = [];
  for (let i = 0; i < 2; i++) {
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.095, 18, 14), skin);
    const upper = new THREE.Mesh(new THREE.CapsuleGeometry(0.115, 1, 8, 16), sleeve);
    const fore = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 1, 8, 16), sleeve);
    const cf = new THREE.Mesh(new THREE.CylinderGeometry(0.115, 0.115, 0.08, 18), cuffMat);
    parent.add(hand, upper, fore, cf);
    arms.push({ hand, upper, fore, cf });
  }
  // i = 0 left, 1 right; hand positions in the parent's space
  return function setArms(handL, handR, elbowOut = 0.2) {
    [handL, handR].forEach((hp, i) => {
      const sx = i ? 1 : -1;
      const a = shoulder(sx);
      const elbow = a.clone().lerp(hp, 0.5).add(new THREE.Vector3(elbowOut * sx, -0.2, -0.08));
      const wrist = elbow.clone().lerp(hp, 0.82);
      arms[i].hand.position.copy(hp);
      setSegment(arms[i].upper, a, elbow, 0.115);
      setSegment(arms[i].fore, elbow, wrist, 0.11);
      arms[i].cf.position.copy(wrist);
      arms[i].cf.quaternion.copy(arms[i].fore.quaternion);
    });
  };
}

// ---------------------------------------------------------------- the guy: designer-vinyl toy in his armchair
function makeGuy() {
  const skin = clay("#E8A87C");
  const hairMat = clay("#3B2416", { roughness: 0.7 });
  const hoodie = clay("#FF8A3D");
  const hoodieDeep = clay("#EE7428");
  const joggers = clay("#1E3A8A");
  const joggersDeep = clay("#172E6E");
  const sneaker = clay("#F6F5F0");
  const sole = clay("#34C759");
  const phones = clay("#2A2D34", { roughness: 0.55 });
  const sand = clay("#E8C07D", { roughness: 0.9 });
  const wood = clay("#8A5A35", { roughness: 0.5, envMapIntensity: 0.6 });
  const g = new THREE.Group();

  // mid-century armchair: sand upholstery, walnut frame, splayed tapered legs
  const chair = new THREE.Group();
  const base = new THREE.Mesh(new RoundedBoxGeometry(1.75, 0.08, 1.45, 4, 0.03), wood);
  base.position.set(0, 0.62, 0);
  const seat = new THREE.Mesh(new RoundedBoxGeometry(1.6, 0.3, 1.35, 5, 0.12), sand);
  seat.position.set(0, 0.81, 0.02);
  const back = new THREE.Mesh(new RoundedBoxGeometry(1.55, 1.1, 0.28, 5, 0.12), sand);
  back.position.set(0, 1.5, -0.66);
  back.rotation.x = -0.2;
  chair.add(base, seat, back);
  for (const sx of [-1, 1]) {
    const arm = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.06, 1.25, 4, 0.025), wood);
    arm.position.set(0.9 * sx, 1.3, -0.05);
    chair.add(arm);
    chair.add(cylinderBetween(new THREE.Vector3(0.9 * sx, 1.28, 0.45), new THREE.Vector3(0.9 * sx, 0.62, 0.45), 0.032, 0.032, wood));
    chair.add(cylinderBetween(new THREE.Vector3(0.9 * sx, 1.28, -0.55), new THREE.Vector3(0.9 * sx, 0.62, -0.5), 0.032, 0.032, wood));
    chair.add(cylinderBetween(new THREE.Vector3(0.6 * sx, 0.62, -0.62), new THREE.Vector3(0.62 * sx, 1.95, -0.9), 0.035, 0.035, wood));
    for (const sz of [-1, 1]) {
      const bx = 0.85 * sx, bz = 0.72 * sz;
      chair.add(cylinderBetween(new THREE.Vector3(0.75 * sx, 0.6, 0.6 * sz), new THREE.Vector3(bx, -0.16, bz), 0.045, 0.028, wood));
    }
  }
  g.add(chair);

  const fig = new THREE.Group();
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.36, 0.42, 10, 28), hoodie);
  torso.position.set(0, 1.56, -0.04);
  torso.scale.set(1.08, 1, 0.88);
  const pocket = new THREE.Mesh(new RoundedBoxGeometry(0.46, 0.2, 0.07, 4, 0.035), hoodieDeep);
  pocket.position.set(0, 1.38, 0.29);
  pocket.rotation.x = -0.15;
  const hood = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.1, 12, 28), hoodie);
  hood.position.set(0, 2.05, -0.1);
  hood.rotation.x = Math.PI / 2 - 0.35;
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.13, 0.2, 16), skin);
  neck.position.set(0, 2.16, 0);
  fig.add(torso, pocket, hood, neck);
  for (const sx of [-1, 1]) {
    fig.add(cylinderBetween(new THREE.Vector3(0.07 * sx, 2.02, 0.25), new THREE.Vector3(0.075 * sx, 1.8, 0.3), 0.014, 0.014, sneaker));
  }
  const bandGeo = new THREE.TorusGeometry(0.27, 0.035, 10, 40, Math.PI * 1.3);
  bandGeo.rotateZ(Math.PI * 0.85);
  bandGeo.rotateX(Math.PI / 2);
  const band = new THREE.Mesh(bandGeo, phones);
  band.position.set(0, 2.1, -0.02);
  band.rotation.x = 0.25;
  fig.add(band);
  for (const sx of [-1, 1]) {
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.105, 0.08, 24), phones);
    cup.rotation.z = Math.PI / 2;
    cup.position.set(0.25 * sx, 2.04, 0.12);
    fig.add(cup);
  }
  fig.add(capsuleBetween(new THREE.Vector3(-0.2, 1.16, 0), new THREE.Vector3(0.2, 1.16, 0), 0.25, joggers));
  for (const sx of [-1, 1]) {
    fig.add(capsuleBetween(new THREE.Vector3(0.2 * sx, 1.15, 0.05), new THREE.Vector3(0.22 * sx, 1.1, 0.64), 0.155, joggers));
    fig.add(capsuleBetween(new THREE.Vector3(0.22 * sx, 1.08, 0.68), new THREE.Vector3(0.23 * sx, 0.24, 0.78), 0.135, joggers));
    const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.08, 20), joggersDeep);
    cuff.position.set(0.23 * sx, 0.2, 0.78);
    const shoe = new THREE.Mesh(new RoundedBoxGeometry(0.25, 0.17, 0.44, 4, 0.07), sneaker);
    shoe.position.set(0.23 * sx, 0.05, 0.84);
    shoe.rotation.y = 0.12 * sx;
    const soleM = new THREE.Mesh(new RoundedBoxGeometry(0.27, 0.07, 0.46, 4, 0.03), sole);
    soleM.position.set(0.23 * sx, -0.07, 0.84);
    soleM.rotation.y = 0.12 * sx;
    fig.add(cuff, shoe, soleM);
  }

  const face = makeFace(skin, { browMat: clay("#3B2416") });
  const head = face.head;
  head.position.set(0, 2.62, 0);
  const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.53, 48, 24, 0, TAU, 0, 1.45), hairMat);
  hairCap.position.set(0, 0.02, -0.01);
  hairCap.rotation.x = -0.38;
  hairCap.scale.set(1, 0.96, 0.97);
  head.add(hairCap);
  const quiff = new THREE.Group();
  quiff.position.set(0.0, 0.36, 0.16);
  const wave = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 18), hairMat);
  wave.scale.set(0.27, 0.12, 0.25);
  wave.position.set(0.02, 0.07, 0.07);
  wave.rotation.x = -0.75;
  const crown = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 18), hairMat);
  crown.scale.set(0.3, 0.11, 0.26);
  crown.position.set(0, 0.04, -0.1);
  crown.rotation.x = -0.15;
  quiff.add(wave, crown);
  head.add(quiff);
  fig.add(head);

  const kulhad = makeKulhad();
  const kulhad2 = makeKulhad(); // the one he offers the cop; handed over by the caller
  fig.add(kulhad);
  const setArms = makeArms(fig, hoodie, hoodieDeep, skin, (sx) => new THREE.Vector3(0.38 * sx, 1.98, -0.02));
  const steam = [];
  const steamMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.6, transparent: true, opacity: 0.6 });
  for (let i = 0; i < 3; i++) {
    const s = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 10), steamMat.clone());
    steam.push(s);
    fig.add(s);
  }
  g.add(fig);

  const shGeo = new THREE.PlaneGeometry(3.2, 2.8, 16, 16);
  shGeo.rotateX(-Math.PI / 2);
  const sh = new THREE.Mesh(shGeo, new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false, toneMapped: false }));
  sh.position.set(0, 0.01, 0.1);
  g.add(sh);

  // ---- acting (guy-local positions; he faces +z, the cop stands to his front right)
  const REST_R = [0.16, 1.78, 0.6], SIP_R = [0.05, 2.3, 0.55], RAISE_R = [0.32, 2.3, 0.8];
  const REST_L = [-0.3, 1.3, 0.58], CHEST = [-0.06, 1.85, 0.36], POCKET = [-0.12, 1.45, 0.42], OFFER = [0.42, 2.0, 1.0];
  const HAND_R = [[0, SIP_R], [1.35, SIP_R], [1.6, REST_R, "back"], [6.85, REST_R], [7.05, RAISE_R, "back"], [7.85, RAISE_R], [8.15, REST_R],
    [28.3, REST_R], [28.55, SIP_R], [29.3, SIP_R], [29.6, REST_R], [30.2, REST_R], [30.45, SIP_R]];
  const HAND_L = [[0, REST_L], [5.25, REST_L], [5.45, CHEST, "back"], [6.05, CHEST], [6.35, REST_L], [26.5, REST_L], [26.7, POCKET], [26.85, POCKET],
    [27.15, OFFER, "back"], [27.9, OFFER], [28.2, REST_L]];
  const LID = [[0, 1.1], [1.33, 1.1], [1.45, -1.75, "snap"], [1.9, -1.35], [4.3, -1.35], [4.5, -0.85], [8.0, -0.85], [8.2, -1.25], [20.3, -1.25], [20.9, 0.2],
    [25.9, 0.2], [26.05, 1.0], [26.6, 1.0], [26.9, 0.05], [28.3, 0.05], [28.55, 1.1], [29.3, 1.1], [29.6, 0.05], [30.2, 0.05], [30.45, 1.1]];
  const YAW = [[0, 0], [1.4, 0], [1.6, 0.55, "back"], [8.2, 0.55], [20.3, 0.55], [29.0, 0.55], [29.6, 0.15]];
  function pose(t, ti = t) {
    const breathe = Math.sin(TAU * ti / 1.5);
    const startle = Math.sin(Math.PI * seg(t, 1.38, 2.2)) * (t < 2.2 ? 1 : 0);
    const confused = smooth(4.3, 4.5, t) * (1 - smooth(7.9, 8.1, t));
    const smug = smooth(20.6, 20.9, t) * (1 - smooth(25.8, 26.0, t));
    const laugh = smooth(25.95, 26.05, t) * (1 - smooth(26.5, 26.7, t));
    const sip = smooth(28.45, 28.55, t) * (1 - smooth(29.3, 29.5, t)) + smooth(30.35, 30.45, t) + (t < 1.35 ? 1 : 0) * (1 - smooth(1.33, 1.45, t));
    const dt = t - SW.snap;
    const wind = dt >= 0 && dt < 1.2 ? Math.exp(-((dt / 0.32) ** 2)) : 0;
    fig.position.y = 0.018 * breathe + 0.12 * startle + 0.03 * Math.abs(Math.sin(t * 22)) * laugh;
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
      s.material.opacity = 0.5 * Math.sin(Math.PI * p) * (1 - 0.7 * clamp01(sip));
    });
    return { handL: hL };
  }
  return { group: g, fig, pose, kulhad2 };
}

// ---------------------------------------------------------------- the cop: khaki, pot belly, moustache, beacon cap, radar gun
function makeCop() {
  const skin = clay("#C98B5E");
  const shirt = clay("#C9A66B");
  const shirtDeep = clay("#B08D57");
  const trousers = clay("#9C7A45");
  const leather = clay("#5A3A22", { roughness: 0.5 });
  const gold = new THREE.MeshPhysicalMaterial({ color: "#E0B040", roughness: 0.3, metalness: 0.8 });
  const black = clay("#1D1D22", { roughness: 0.4 });
  const hairDark = clay("#2B1A10");
  const g = new THREE.Group();
  const fig = new THREE.Group();
  for (const sx of [-1, 1]) {
    fig.add(capsuleBetween(new THREE.Vector3(0.2 * sx, 1.2, 0), new THREE.Vector3(0.2 * sx, 0.24, 0.02), 0.155, trousers));
    const shoe = new THREE.Mesh(new RoundedBoxGeometry(0.25, 0.15, 0.42, 4, 0.06), black);
    shoe.position.set(0.2 * sx, 0.07, 0.09);
    fig.add(shoe);
  }
  const belt = new THREE.Mesh(new THREE.CylinderGeometry(0.43, 0.43, 0.12, 32), leather);
  belt.position.y = 1.3;
  belt.scale.z = 0.88;
  const buckle = new THREE.Mesh(new RoundedBoxGeometry(0.14, 0.1, 0.04, 3, 0.015), gold);
  buckle.position.set(0, 1.3, 0.39);
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.4, 0.5, 10, 28), shirt);
  torso.position.set(0, 1.78, 0);
  torso.scale.set(1.12, 1, 0.95);
  const belly = new THREE.Mesh(new THREE.SphereGeometry(0.37, 28, 20), shirt);
  belly.position.set(0, 1.52, 0.17);
  const strap = new THREE.Mesh(new RoundedBoxGeometry(0.07, 0.95, 0.03, 2, 0.01), leather);
  strap.position.set(0.05, 1.8, 0.4);
  strap.rotation.set(-0.12, 0, -0.62);
  const badge = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.02, 16), gold);
  badge.rotation.x = Math.PI / 2;
  badge.position.set(-0.2, 2.0, 0.37);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.14, 0.2, 16), skin);
  neck.position.set(0, 2.3, 0);
  fig.add(belt, buckle, torso, belly, strap, badge, neck);
  for (const sx of [-1, 1]) {
    const ep = new THREE.Mesh(new RoundedBoxGeometry(0.22, 0.05, 0.15, 2, 0.02), shirtDeep);
    ep.position.set(0.38 * sx, 2.22, 0);
    const pk = new THREE.Mesh(new RoundedBoxGeometry(0.15, 0.13, 0.04, 2, 0.015), shirtDeep);
    pk.position.set(0.18 * sx, 1.93, 0.36);
    fig.add(ep, pk);
  }

  const face = makeFace(skin, { browMat: hairDark, browR: 0.028, browLen: 0.13, noseR: 0.055 });
  const head = face.head;
  head.position.set(0, 2.82, 0);
  // a proud moustache: two curling halves
  const stache = new THREE.Group();
  stache.position.set(0, -0.14, 0.45);
  const halves = [];
  for (const sx of [-1, 1]) {
    const half = new THREE.Group();
    half.add(capsuleBetween(new THREE.Vector3(0.01 * sx, 0, 0), new THREE.Vector3(0.15 * sx, -0.02, -0.03), 0.04, hairDark));
    const curl = new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 10), hairDark);
    curl.position.set(0.17 * sx, 0.03, -0.04);
    half.add(curl);
    stache.add(half);
    halves.push(half);
  }
  head.add(stache);
  // cap with a red band, black visor, gold badge and a beacon on top
  const cap = new THREE.Group();
  cap.position.set(0, 0.36, -0.02);
  const crownM = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.5, 0.26, 36), clay("#B8955A"));
  crownM.position.y = 0.1;
  const bandM = new THREE.Mesh(new THREE.CylinderGeometry(0.505, 0.505, 0.09, 36), clay("#C62828"));
  bandM.position.y = 0.0;
  const visor = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.03, 24, 1, false, -Math.PI / 2, Math.PI), black);
  visor.position.set(0, -0.04, 0.36);
  visor.scale.set(1.35, 1, 1.0);
  visor.rotation.x = 0.18;
  const capBadge = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 16), gold);
  capBadge.rotation.x = Math.PI / 2 - 0.1;
  capBadge.position.set(0, 0.1, 0.48);
  cap.add(crownM, bandM, visor, capBadge);
  const red = new THREE.MeshBasicMaterial({ color: "#FF2D3D", toneMapped: false });
  const blue = new THREE.MeshBasicMaterial({ color: "#2D7BFF", toneMapped: false });
  const bR = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12, 0, TAU, 0, Math.PI / 2), red);
  bR.position.set(-0.07, 0.23, 0);
  const bB = new THREE.Mesh(new THREE.SphereGeometry(0.075, 16, 12, 0, TAU, 0, Math.PI / 2), blue);
  bB.position.set(0.07, 0.23, 0);
  const lightR = new THREE.PointLight("#FF2D3D", 0, 6, 2);
  lightR.position.set(-0.3, 0.5, 0.4);
  const lightB = new THREE.PointLight("#2D7BFF", 0, 6, 2);
  lightB.position.set(0.3, 0.5, 0.4);
  cap.add(bR, bB, lightR, lightB);
  head.add(cap);
  const sweat = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 12), new THREE.MeshPhysicalMaterial({ color: "#8FD3FF", roughness: 0.1, clearcoat: 1, transparent: true, opacity: 0.9 }));
  sweat.scale.set(0.8, 1.3, 0.8);
  head.add(sweat);
  fig.add(head);

  // radar speed gun: body, nose, red lens, grip, rear screen with a live readout
  const gun = new THREE.Group();
  const gunMat = clay("#30343B", { roughness: 0.45 });
  const gBody = new THREE.Mesh(new RoundedBoxGeometry(0.17, 0.15, 0.4, 4, 0.04), gunMat);
  const gNose = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.09, 0.14, 24), clay("#4A505A"));
  gNose.rotation.x = Math.PI / 2;
  gNose.position.z = 0.26;
  const lens = new THREE.Mesh(new THREE.CircleGeometry(0.07, 24), new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false }));
  lens.position.z = 0.335;
  const grip = new THREE.Mesh(new RoundedBoxGeometry(0.09, 0.22, 0.11, 3, 0.03), gunMat);
  grip.position.set(0, -0.15, -0.08);
  grip.rotation.x = 0.3;
  const stripe = new THREE.Mesh(new RoundedBoxGeometry(0.175, 0.03, 0.2, 2, 0.01), clay("#FFC21A"));
  stripe.position.set(0, 0.06, 0.05);
  const scrCanvas = document.createElement("canvas");
  scrCanvas.width = 256;
  scrCanvas.height = 96;
  const scrTex = new THREE.CanvasTexture(scrCanvas);
  scrTex.colorSpace = THREE.SRGBColorSpace;
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.15, 0.056), new THREE.MeshBasicMaterial({ map: scrTex, toneMapped: false }));
  screen.position.set(0, 0.02, -0.202);
  screen.rotation.y = Math.PI;
  gun.add(gBody, gNose, lens, grip, stripe, screen);
  fig.add(gun);
  const beam = new THREE.Mesh(
    new THREE.CylinderGeometry(0.035, 0.06, 1, 12, 1, true),
    new THREE.MeshBasicMaterial({ color: "#FF3B3B", toneMapped: false, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }),
  );
  beam.geometry.translate(0, 0.5, 0);
  beam.geometry.rotateX(Math.PI / 2); // grows along +z from the lens
  beam.position.z = 0.34;
  gun.add(beam);
  const kulhadSlot = new THREE.Group(); // the kulhad lands here once he takes it
  fig.add(kulhadSlot);
  const setArms = makeArms(fig, shirt, shirtDeep, skin, (sx) => new THREE.Vector3(0.44 * sx, 2.1, 0));
  g.add(fig);
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.4), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false, toneMapped: false }));
  sh.rotation.x = -Math.PI / 2;
  sh.position.y = 0.01;
  g.add(sh);

  let lastScreen = "";
  function drawScreen(text, on) {
    const key = text + on;
    if (key === lastScreen) return;
    lastScreen = key;
    const c = scrCanvas.getContext("2d");
    c.fillStyle = "#0E1A12";
    c.fillRect(0, 0, 256, 96);
    if (on) {
      c.fillStyle = "#62FF8E";
      c.font = "bold 58px monospace";
      c.textAlign = "center";
      c.textBaseline = "middle";
      c.fillText(text, 128, 50);
    }
    scrTex.needsUpdate = true;
  }

  // ---- acting (cop-local positions; he faces +z, the guy sits to his front left)
  const AIM = [0.3, 2.15, 0.72], UP = [0.34, 2.8, 0.42], BLOW = [0.14, 2.62, 0.5], SELF = [0.18, 2.5, 0.85], LOW = [0.4, 1.55, 0.32];
  const HIP = [-0.5, 1.42, 0.12], STOP = [-0.42, 2.4, 0.62], TAKE = [-0.32, 1.98, 0.86], HOLD = [-0.22, 1.86, 0.62], SIP = [-0.06, 2.62, 0.55];
  const HAND_R = [[0, AIM], [8.55, AIM], [8.8, UP, "back"], [9.2, UP], [20.3, BLOW], [20.8, BLOW], [21.05, SELF, "back"], [24.4, SELF], [25.0, LOW], [31.5, LOW]];
  const HAND_L = [[0, HIP], [1.2, HIP], [1.38, STOP, "back"], [2.9, STOP], [3.2, HIP], [27.55, HIP], [27.85, TAKE, "back"], [28.0, TAKE], [28.25, HOLD],
    [28.5, SIP], [29.3, SIP], [29.6, HOLD], [30.3, HOLD], [30.55, SIP]];
  const LID = [[0, -0.75], [8.1, -0.75], [8.3, -0.15], [9.2, -0.15], [20.3, -0.3], [20.95, -0.3], [21.25, -1.8, "snap"], [24.4, -1.8], [24.7, 0.35], [26.9, 0.35],
    [27.25, -0.9], [28.35, -0.9], [28.55, 1.1], [29.3, 1.1], [29.6, 0.05], [30.3, 0.05], [30.55, 1.1]];
  function pose(t, ti, guyHeadLocal, selfHeadLocal) {
    const breathe = Math.sin(TAU * ti / 1.7);
    const shout = Math.sin(Math.PI * seg(t, 1.2, 1.9)) * (t < 1.9 ? 1 : 0);
    const smug = smooth(8.1, 8.3, t) * (1 - smooth(9.1, 9.3, t)) + smooth(20.3, 20.5, t) * (1 - smooth(20.95, 21.1, t));
    const shock = smooth(21.2, 21.3, t) * (1 - smooth(24.35, 24.6, t));
    const sad = smooth(24.4, 24.8, t) * (1 - smooth(26.9, 27.3, t));
    const sheepish = smooth(27.0, 27.3, t);
    const sip = smooth(28.45, 28.55, t) * (1 - smooth(29.3, 29.5, t)) + smooth(30.45, 30.55, t);
    const stern = 1 - Math.max(smug, shock, sad, sheepish);
    fig.position.y = 0.015 * breathe - 0.08 * sad + 0.08 * shout;
    fig.rotation.x = 0.1 * shout - 0.04 * sad;
    torso.scale.set(1.12 * (1 + 0.02 * breathe), 1 - 0.02 * breathe - 0.05 * sad, 0.95);
    belly.scale.setScalar(1 + 0.03 * breathe);
    head.rotation.x = -0.03 + 0.28 * sad - 0.1 * shock - 0.15 * sip;
    head.rotation.z = 0.04 * Math.sin(TAU * ti / 3.4) + 0.1 * smug;
    head.rotation.y = lerp(-0.25, 0, Math.max(shock, sad)) + 0.05 * Math.sin(TAU * ti / 5);
    const talking = within(t, TALK.cop) ? flap(t) : 0;
    applyFace(face, {
      lid: track(t, LID),
      eyeS: 1 + 0.5 * shock,
      // stern: brows in a V; shock: high; sad: inner ends up
      brows: [-0.02 * stern + 0.09 * shock + 0.02 * sad, -0.3 * stern + 0.25 * sad, -0.02 * stern + 0.09 * shock + 0.02 * sad + 0.05 * smug, 0.3 * stern - 0.25 * sad - 0.2 * smug],
      curve: lerp(lerp(-0.6, 1, Math.max(smug, sheepish)), -1, sad),
      smileW: 1 + 0.2 * smug,
      open: Math.max(talking * 0.6, shock * 0.35 * (1 - talking)),
    });
    halves.forEach((h, i) => (h.rotation.z = (i ? 1 : -1) * (0.15 * stern + 0.25 * smug - 0.45 * sad)));
    cap.rotation.z = 0.22 * sad + 0.08 * sheepish;
    cap.position.y = 0.36 - 0.03 * sad;
    // beacon: urgent while he is on duty, dies with the trombone, then a lazy blink
    const onDuty = t < 9.3 || (t >= 20.3 && t < 24.6);
    const fast = Math.sin(TAU * 3.2 * t) > 0 ? 1 : 0;
    const lazy = t > 27.3 ? 0.35 + 0.35 * Math.sin(TAU * 0.6 * t) : 0;
    const r = onDuty ? fast : lazy, b = onDuty ? 1 - fast : lazy * 0.8;
    bR.material.color.set("#FF2D3D").multiplyScalar(0.35 + 0.65 * r);
    bB.material.color.set("#2D7BFF").multiplyScalar(0.35 + 0.65 * b);
    lightR.intensity = 9 * r;
    lightB.intensity = 9 * b;
    // a sweat drop slides down his temple from the self-reading to the trombone
    const sw = seg(t, 21.7, 24.6);
    sweat.visible = t > 21.6 && t < 24.7;
    sweat.position.set(0.36, 0.18 - 0.3 * sw, 0.28);
    // hands, gun and its target
    const hR = V(track(t, HAND_R));
    const hL = V(track(t, HAND_L));
    setArms(hL, hR, 0.24);
    gun.position.copy(hR).add(new THREE.Vector3(0, 0.08, 0.04));
    const sky = new THREE.Vector3(1.2, 14, 7);
    const barrelUp = hR.clone().add(new THREE.Vector3(0, 2, 0.4));
    const down = hR.clone().add(new THREE.Vector3(0.1, -1.2, 1.2));
    let target;
    if (t < 8.55) target = guyHeadLocal.clone();
    else if (t < 20.3) target = guyHeadLocal.clone().lerp(sky, outBack(seg(t, 8.55, 8.8), 1.2));
    else if (t < 20.85) target = barrelUp;
    else if (t < 24.4) target = barrelUp.clone().lerp(selfHeadLocal, outBack(seg(t, 20.85, 21.05), 1.4));
    else target = selfHeadLocal.clone().lerp(down, inOutSine(seg(t, 24.4, 25.0)));
    fig.updateMatrixWorld(true);
    gun.lookAt(fig.localToWorld(target.clone()));
    // the beam: fires into the sky on "बैठे हो?"
    const bl = seg(t, T_BEAM, T_BEAM + 0.3);
    beam.visible = t >= T_BEAM && t < SW.earth + 0.05;
    beam.scale.set(1, 1, 0.01 + 30 * outExpo(bl));
    beam.material.opacity = 0.9;
    // screen readout
    if (t < 20.9) drawScreen("SPEED?", Math.floor(t * 3) % 2 === 0);
    else {
      const p = seg(t, 20.95, 21.25);
      drawScreen(p < 1 ? String(Math.round(720000 * p)) : "720000+", true);
    }
    return { handL: hL };
  }
  return { group: g, fig, pose, kulhadSlot, head };
}

// ---------------------------------------------------------------- the duo on their tiny planet
function makeDuo({ ground = true } = {}) {
  const duo = new THREE.Group();
  let cap = null;
  if (ground) {
    const capGeo = paintLowPoly(new THREE.IcosahedronGeometry(GROUND_R, 14), (m) => {
      const ang = Math.acos(Math.min(1, m.y));
      const wobble = 0.08 * Math.sin(m.x * 9 + 1.1) + 0.06 * Math.cos(m.z * 11 - 0.7);
      if (ang < 0.62 + wobble) return Math.sin(m.x * 14) * Math.cos(m.z * 12) > 0.55 && ang > 0.38 ? "sand" : "land";
      if (Math.hypot(m.x + 0.55, m.z + 0.62) < 0.2 + wobble) return "land";
      if (Math.hypot(m.x - 0.7, m.z + 0.35) < 0.14 + wobble) return "sand";
      if (Math.hypot(m.x - 0.2, m.z - 0.75) < 0.16 + wobble) return "land";
      return "ocean";
    });
    cap = new THREE.Mesh(capGeo, earthMaterial());
    cap.material.specularIntensity = 0.3;
    cap.material.clearcoat = 0.1;
    cap.material.color.setScalar(0.78);
    const pivot = new THREE.Group();
    pivot.position.y = -GROUND_R;
    pivot.add(cap);
    duo.add(pivot);
  }
  const guy = makeGuy();
  guy.group.position.set(-0.75, 0, 0);
  guy.group.rotation.y = 0.4;
  const cop = makeCop();
  cop.group.position.set(1.05, -groundDrop(1.05, 0.5) + 0.01, 0.5);
  cop.group.rotation.y = -0.55;
  duo.add(guy.group, cop.group);
  const k2 = guy.kulhad2;
  duo.add(k2);
  const tmp = new THREE.Vector3();
  function pose(t, ti = t) {
    // where the guy's head is, in the cop's own space, so the gun can aim at it
    duo.updateMatrixWorld(true);
    const guyHead = guy.group.localToWorld(new THREE.Vector3(0, 2.62, 0));
    const guyHeadLocal = cop.fig.worldToLocal(guyHead.clone());
    const selfHeadLocal = new THREE.Vector3(0, 2.82, 0);
    const g = guy.pose(t, ti);
    const c = cop.pose(t, ti, guyHeadLocal, selfHeadLocal);
    duo.updateMatrixWorld(true);
    // kulhad #2: pops out of his hoodie pocket, travels in his hand, and the cop takes it
    k2.visible = t > 26.75;
    const from = guy.fig.localToWorld(g.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    const to = cop.fig.localToWorld(c.handL.clone().add(new THREE.Vector3(0.02, 0.08, 0.05)));
    duo.worldToLocal(from);
    duo.worldToLocal(to);
    tmp.copy(t < 27.9 ? from : to);
    k2.position.copy(tmp);
    k2.scale.setScalar(outBack(seg(t, 26.75, 26.95), 2));
    const copSip = smooth(28.45, 28.55, t) * (1 - smooth(29.3, 29.5, t)) + smooth(30.45, 30.55, t);
    k2.rotation.set(-0.8 * (t >= 27.9 ? copSip : 0), t >= 27.9 ? -0.55 : 0.4, 0);
    if (cap) cap.rotation.x = -0.012 * t - 0.25 * inOutSine(seg(t, T_END, T_END + 2.3)); // the planet keeps turning under them
  }
  return { group: duo, pose };
}
