// ---------------------------------------------------------------- background
const BG = {
  chair: ["#FFD6A5", "#FF6B6B"],
  earth: ["#00B4D8", "#0B3D91"],
  orbit: ["#2A3C6E", "#14213D"],
  galaxy: ["#5A189A", "#240046"],
};
const bgEl = document.getElementById("w-bg");
const policeEl = document.getElementById("w-police");
function bgAt(t) {
  // colours cross over inside each whip window
  const order = [[0, "chair"], [SW.earth, "earth"], [SW.orbit, "orbit"], [SW.galaxy, "galaxy"], [SW.snap, "chair"]];
  let from = BG.chair, to = BG.chair, x = 0;
  for (let i = 1; i < order.length; i++) {
    const [c, name] = order[i];
    const half = i === 4 ? 0.06 : 0.14;
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

// ---------------------------------------------------------------- render(t)
function render(t) {
  const whip = whipLevel(t);
  const name = worldAt(t);
  chairWorld.visible = name === "chair";
  earthWorld.visible = name === "earth";
  orbitWorld.visible = name === "orbit";
  galaxyWorld.visible = name === "galaxy";
  stars.visible = name === "orbit" || name === "galaxy";

  if (name === "chair") duo.pose(t);
  // Earth spins: Africa and Europe face the camera while "सत्रह सौ" lands; the tiny duo rides along
  earthSpin.rotation.y = 0.8 * (t - 10.94);
  if (name === "earth") tinyDuo.pose(t);
  clouds.forEach((c, i) => {
    const a = 0.5 * t * (1 + 0.15 * (i % 3)) + i * 0.8;
    const tilt = -0.6 + 0.17 * i;
    c.position.set(Math.cos(a) * 1.9, Math.sin(tilt) * 1.9 * Math.sin(a + i), Math.sin(a) * 1.9 * Math.cos(tilt));
    c.rotation.y = a;
  });

  // Orbit: Sun pulses (punches on "Sun"), Earth races along the magenta line
  const pulse = 1 + 0.04 * Math.sin(TAU * t * 1.25) + 0.22 * Math.exp(-10 * Math.max(0, t - T_SUN_WORD)) * (t >= T_SUN_WORD ? 1 : 0);
  sun.rotation.y = 0.4 * t;
  sun.scale.setScalar(pulse);
  halo1.scale.setScalar(4.6 * pulse);
  halo2.scale.setScalar(8.5 * (0.98 + 0.04 * Math.sin(TAU * t * 0.8)) * pulse);
  const theta = 0.4 + 0.55 * (t - SW.orbit);
  miniEarth.position.set(Math.cos(theta) * ORBIT_R, 0, Math.sin(theta) * ORBIT_R);
  miniEarth.rotation.y = 3 * t;
  const dummy = new THREE.Object3D();
  for (let i = 0; i < TRAIL; i++) {
    const a = theta - 0.035 * (i + 1);
    dummy.position.set(Math.cos(a) * ORBIT_R, 0, Math.sin(a) * ORBIT_R);
    dummy.scale.setScalar(1 - i / TRAIL);
    dummy.updateMatrix();
    trail.setMatrixAt(i, dummy.matrix);
  }
  trail.instanceMatrix.needsUpdate = true;

  // Galaxy: differential rotation in the shader; the Sun's dot rides its ring
  stars.rotation.y = 0.03 * t;
  galMat.uniforms.uTime.value = t - SW.galaxy + 2;
  const sa = SUN_A + omega(SUN_R) * (t - SW.galaxy + 2);
  sunDot.position.set(Math.cos(sa) * SUN_R, 0.05, Math.sin(sa) * SUN_R);
  sunCore.position.copy(sunDot.position);
  const swell = outBack(seg(t, SW.galaxy + 0.3, SW.galaxy + 0.7), 2);
  sunDot.scale.setScalar(1.15 * swell * (1 + 0.12 * Math.sin(TAU * t * 2)));
  sunCore.scale.setScalar(0.36 * swell);
  sunRing.material.opacity = 0.6 * seg(t, SW.galaxy + 0.2, SW.galaxy + 0.6);

  // background, the beacon's red/blue wash over the sky, camera, speed lines
  const [a, b] = bgAt(t);
  bgEl.style.background = VERTICAL
    ? `radial-gradient(130% 80% at 50% 42%, ${a} 0%, ${b} 80%)`
    : `radial-gradient(120% 120% at 32% 40%, ${a} 0%, ${b} 78%)`;
  const onDuty = name === "chair" && (t < 9.3 || (t >= 20.3 && t < 24.6));
  const fast = Math.sin(TAU * 3.2 * t) > 0;
  policeEl.style.opacity = onDuty ? "0.55" : "0";
  policeEl.style.background = fast
    ? "radial-gradient(60% 40% at 15% 10%, rgba(255,45,61,0.75), rgba(255,45,61,0) 70%)"
    : "radial-gradient(60% 40% at 85% 10%, rgba(45,123,255,0.75), rgba(45,123,255,0) 70%)";
  placeCamera(t, name, whip);
  drawLines(t, whip);

  renderer.clear();
  renderer.toneMappingExposure = name === "chair" ? 0.85 : 1.05;
  renderer.render(scene, camera);
  renderer.toneMappingExposure = 1.05;
  renderer.clearDepth();
  renderNumber(t);
  renderer.render(numScene, numCam);
}

host.render = render;
new FontLoader().load("assets/fonts/fredoka-700.typeface.json", (font) => {
  buildGlyphs(font);
  render(host.clock.t);
  host.ready();
});
render(host.clock.t);
