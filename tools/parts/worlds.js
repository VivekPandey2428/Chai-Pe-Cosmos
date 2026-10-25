// ---------------------------------------------------------------- worlds
const chairWorld = new THREE.Group();
const duo = makeDuo();
chairWorld.add(duo.group);
scene.add(chairWorld);

const earthWorld = new THREE.Group();
const earthTilt = new THREE.Group();
earthTilt.rotation.z = 0.41;
const earthSpin = new THREE.Group();
const earth = makeEarth(1.6);
earthSpin.add(earth);
// the same two, tiny, standing on the equator in Africa
const tinyDuo = makeDuo({ ground: false });
tinyDuo.group.scale.setScalar(0.09);
tinyDuo.group.position.set(0, 0, 1.6);
tinyDuo.group.rotation.x = Math.PI / 2;
earthSpin.add(tinyDuo.group);
earthTilt.add(earthSpin);
earthWorld.add(earthTilt);
const clouds = [];
const cloudMat = glossy("#FFFFFF", { roughness: 0.5, clearcoat: 0.4, flatShading: true });
for (let i = 0; i < 8; i++) {
  const cl = new THREE.Mesh(new THREE.IcosahedronGeometry(0.17 + 0.05 * (i % 3), 0), cloudMat);
  cl.scale.set(1.5, 0.6, 1);
  clouds.push(cl);
  earthWorld.add(cl);
}
scene.add(earthWorld);
