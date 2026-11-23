// Researcher auxiliary diagnostic. This is not an upstream test or historical output.
// Run from repository root after the pinned install in reproduce.md.
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { forceManyBody, forceSimulation } from './cache/d3-run/node_modules/d3-force/src/index.js';
import lcg from './cache/d3-run/node_modules/d3-force/src/lcg.js';

const root = fileURLToPath(new URL('.', import.meta.url));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sourceMatches = ['manyBody.js', 'simulation.js', 'jiggle.js', 'lcg.js'].map(name => {
  const installed = fs.readFileSync(root + 'cache/d3-run/node_modules/d3-force/src/' + name);
  const tagged = fs.readFileSync(root + 'cache/d3-src__' + name);
  return { file: name, installed_sha256: sha(installed), tagged_sha256: sha(tagged), equal: installed.equals(tagged) };
});
if (!sourceMatches.every(x => x.equal)) throw new Error('Installed source is not identical to the fetched fixed tag');

function pairwise(nodes, { strength = -30, distanceMin = 1, distanceMax = Infinity, alpha = 1 } = {}) {
  // Explicit O(n²) researcher reference for the documented/code-derived 1/r kernel.
  // No random perturbation is emulated. Coincident inputs are excluded from this comparison.
  return nodes.map((a, i) => nodes.reduce((v, b, j) => {
    if (i === j) return v;
    const dx = b.x - a.x, dy = b.y - a.y;
    let d2 = dx * dx + dy * dy;
    if (d2 === 0) return { vx: NaN, vy: NaN };
    if (d2 >= distanceMax * distanceMax) return v;
    if (d2 < distanceMin * distanceMin) d2 = Math.sqrt(distanceMin * distanceMin * d2);
    const s = typeof strength === 'function' ? strength(b) : strength;
    return { vx: v.vx + dx * s * alpha / d2, vy: v.vy + dy * s * alpha / d2 };
  }, { vx: 0, vy: 0 }));
}

function run(id, xy, options = {}, reference = true) {
  const input = xy.map(([x,y,s],index) => ({ index, x, y, vx: 0, vy: 0, ...(s === undefined ? {} : {s}) }));
  const nodes = structuredClone(input);
  const f = forceManyBody().strength(options.strength ?? -30);
  if ('distanceMax' in options) f.distanceMax(options.distanceMax);
  if ('distanceMin' in options) f.distanceMin(options.distanceMin);
  if ('theta' in options) f.theta(options.theta);
  f.initialize(nodes, lcg());
  f(1);
  const ref = reference ? pairwise(input, options) : null;
  return { case_id: id, evidence_type: 'researcher_auxiliary', input, options: {
    strength: typeof options.strength === 'function' ? 'node.s' : (options.strength ?? -30),
    distanceMin: options.distanceMin ?? 1, distanceMax: options.distanceMax ?? 'Infinity', theta: options.theta ?? 0.9,
    alpha: 1, random: 'd3-force@3.0.0 src/lcg.js seed1', operation: 'force.initialize(nodes,lcg()); force(1)',
  }, output: nodes, all_finite: nodes.every(n=>[n.x,n.y,n.vx,n.vy].every(Number.isFinite)),
  velocity_sum: nodes.reduce((v,n)=>[v[0]+n.vx,v[1]+n.vy],[0,0]), reference: ref,
  reference_max_absolute_component_error: ref ? Math.max(...nodes.flatMap((n,i)=>[Math.abs(n.vx-ref[i].vx),Math.abs(n.vy-ref[i].vy)])) : null };
}

const pair = [[0,0],[3,4]];
const cluster = [[-100,-80],[0,0],[0.1,0.2],[0.2,0.1],[0.15,0.35],[0.35,0.25],[10,9]];
const cutoff = [[0,0],[9.9,0.1],[10.1,0.2]];
const cases = [
  run('D3-N',pair),
  run('D3-B',pair,{distanceMax:4}),
  run('D3-AUX-EQUALITY',pair,{distanceMax:5}),
  run('D3-AUX-MIN',[[0,0],[0.03,0.04]],{distanceMin:1}),
  run('D3-AUX-NOMIN',[[0,0],[0.03,0.04]],{distanceMin:0}),
  run('D3-AUX-COINCIDENT',[[0,0],[0,0]],{},false),
  run('D3-AUX-THETA0',cluster,{theta:0}),
  run('D3-AUX-THETA09',cluster,{theta:0.9}),
  run('D3-AUX-THETA2',cluster,{theta:2}),
  run('D3-AUX-CUTOFF-EXACT',cutoff,{theta:0,distanceMax:10}),
  run('D3-AUX-CUTOFF-APPROX',cutoff,{theta:0.9,distanceMax:10}),
  run('D3-AUX-MIXED-SIGN',[[0,0,0],[-3,4,30],[3,5,-30]],{theta:0,strength:n=>n.s}),
];
const installedVersions = Object.fromEntries(['d3-force','d3-quadtree','d3-dispatch','d3-timer'].map(name=>[name,JSON.parse(fs.readFileSync(root+'cache/d3-run/node_modules/'+name+'/package.json')).version]));
const result = { task: 'AF-RES-061', evidence_type: 'researcher_auxiliary', performed_utc: new Date().toISOString(),
  component_commit: '156712c8c3285d77cb487e1685c5adafcd0394a4', runtime: process.version,
  platform: process.platform, architecture: process.arch, os_release: os.release(), installedVersions, sourceMatches,
  script_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
  reference_limits: 'Pairwise reference is researcher-written from the inspected implementation kernel; not independent physical truth. Coincident jitter is excluded. theta0 is tested, not assumed exact for signed aggregate pruning.', cases };
console.log(JSON.stringify(result,null,2));
