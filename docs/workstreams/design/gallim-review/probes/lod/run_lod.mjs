import { LOD, Object3D, PerspectiveCamera } from 'three';
function mk(h, initF) {
  const lod = new LOD(); const N = new Object3D(); const F = new Object3D();
  lod.addLevel(N, 0); lod.addLevel(F, 100, h);
  if (initF !== 'default') { N.visible = true; F.visible = initF; }
  return { lod, N, F };
}
function step(o, d, zoom = 1) {
  const cam = new PerspectiveCamera(); cam.zoom = zoom; cam.position.set(0, 0, d); cam.updateMatrixWorld(true);
  o.lod.updateMatrixWorld(true); o.lod.update(cam);
  return o.F.visible && !o.N.visible ? 'F' : (o.N.visible && !o.F.visible ? 'N' : `?N${o.N.visible}F${o.F.visible}`);
}
const paths = { P1: [80, 95], P2: [120, 95], P3: [80, 100, 95], P4: [120, 90, 95] };
const out = [];
for (const h of [0.1, 0]) for (const [p, seq] of Object.entries(paths)) {
  const o = mk(h, false); out.push({ path: p, h, init: 'F=false', stages: seq.map(d => step(o, d)).join('|') });
}
// default construction: F.visible starts true (Object3D default), no explicit init
for (const [p, seq] of Object.entries(paths)) { const o = mk(0.1, 'default'); out.push({ path: p, h: 0.1, init: 'default(F.visible=true)', stages: seq.map(d => step(o, d)).join('|') }); }
// controls
const ctl = [['X1a',0.1,false,[95]],['X1b',0.1,true,[95]],['X2a',0.1,false,[100]],['X2b',0.1,true,[90]],['X2c',0.1,true,[89.999]]];
for (const [id,h,f,seq] of ctl) { const o = mk(h,f); out.push({ path:id, h, init:`F=${f}`, stages: seq.map(d=>step(o,d)).join('|') }); }
{ const o = mk(0.1,false); out.push({path:'X4 zoom 1,.9,1,1.1,1 @95', h:0.1, init:'F=false', stages:[1,.9,1,1.1,1].map(z=>step(o,95,z)).join('|')}); }
console.log(JSON.stringify({ three: '0.170.0', node: process.version, results: out }, null, 1));
