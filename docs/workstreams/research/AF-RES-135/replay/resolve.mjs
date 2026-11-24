import {createRequire} from "node:module";
import {readFileSync, realpathSync} from "node:fs";
import {dirname, resolve} from "node:path";

// Use the SemVer implementation bundled with the recorded npm version.
const npm = realpathSync(process.argv[2]);
const require = createRequire(npm);
const semver = require("semver");
const {catalog, releases} = JSON.parse(readFileSync(0, "utf8"));

function choose(name, ranges, cutoff) {
  const candidates = Object.entries(catalog[name] ?? {})
    .filter(([version, pkg]) => pkg.utc && pkg.utc <= cutoff && semver.valid(version)
      && !semver.prerelease(version) && ranges.every(range => semver.satisfies(version, range)))
    .map(([version]) => version);
  return semver.rsort(candidates)[0] ?? null;
}

function lock(version, cutoff, pins = {}) {
  const root = catalog["d3-scale"][version];
  const direct = Object.fromEntries(Object.entries(root.dependencies).map(([name, range]) => {
    const candidate = pins[name] ?? choose(name, [range], cutoff);
    if (!candidate || !semver.satisfies(candidate, range)) {
      throw new Error(`${name} ${range} unavailable at ${cutoff}`);
    }
    return [name, candidate];
  }));
  const packages = {};
  const top = { "d3-scale": version, ...direct };

  function visit(name, current, path, visible) {
    if (packages[path]) {
      if (packages[path].version !== current) throw new Error(`Conflicting packages at ${path}`);
      return;
    }
    const pkg = catalog[name][current];
    packages[path] = {name, version: current, ...pkg};
    const nextVisible = {...visible};
    const nested = [];
    for (const [dep, range] of Object.entries(pkg.dependencies)) {
      if (nextVisible[dep] && semver.satisfies(nextVisible[dep], range)) continue;
      const found = choose(dep, [range], cutoff);
      if (!found) throw new Error(`${name}@${current}: ${dep} ${range} unavailable at ${cutoff}`);
      nextVisible[dep] = found;
      nested.push([dep, found]);
    }
    for (const [dep, found] of nested) visit(dep, found, `${path}/node_modules/${dep}`, nextVisible);
  }

  for (const [name, current] of Object.entries(top)) {
    visit(name, current, `node_modules/${name}`, top);
  }
  return {version, cutoff, direct, packages};
}

function tryLock(version, cutoff, pins) {
  try {
    return lock(version, cutoff, pins);
  } catch (error) {
    return {version, cutoff, error: error.message};
  }
}

const base = Object.fromEntries(releases.map(({version, utc}) => [version, tryLock(version, utc)]));
const orders = {publish: releases.map(x => x.version), semver: semver.sort(releases.map(x => x.version))};
const matched = {};
for (const order of Object.values(orders)) {
  for (let i = 1; i < order.length; i++) {
    const a = order[i - 1], b = order[i], key = `${a}..${b}`;
    if (matched[key]) continue;
    const left = catalog["d3-scale"][a], right = catalog["d3-scale"][b];
    const cutoff = left.utc > right.utc ? left.utc : right.utc;
    const shared = Object.keys(left.dependencies).filter(name => name in right.dependencies);
    const pins = Object.fromEntries(shared.map(name =>
      [name, choose(name, [left.dependencies[name], right.dependencies[name]], cutoff)]));
    const failures = Object.keys(pins).filter(name => !pins[name]).map(name => ({
      name, left: left.dependencies[name], right: right.dependencies[name],
    }));
    const pair = {left: a, right: b, cutoff, pins, failures};
    if (!failures.length) pair.locks = [tryLock(a, cutoff, pins), tryLock(b, cutoff, pins)];
    matched[key] = pair;
  }
}
process.stdout.write(JSON.stringify({base, matched}));
