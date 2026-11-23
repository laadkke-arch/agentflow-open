'use strict';
// Six frozen researcher runs only. No external data, issue code evaluation, or
// outcome-guided parameter changes. Original JSON objects are data inputs.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const BASE = __dirname;
const MOD = path.join(BASE, 'scratch/runtime/node_modules');
const vl = require(path.join(MOD, 'vega-lite'));
const vega = require(path.join(MOD, 'vega'));
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const read = rel => JSON.parse(fs.readFileSync(path.join(BASE, rel), 'utf8'));
const save = (rel, value) => {
  const p = path.join(BASE, rel);
  fs.mkdirSync(path.dirname(p), {recursive: true});
  const text = typeof value === 'string' ? value : JSON.stringify(value, null, 2) + '\n';
  fs.writeFileSync(p, text);
  return {path: rel, bytes: Buffer.byteLength(text), sha256: sha(text)};
};
const clone = o => JSON.parse(JSON.stringify(o));
// Exact escape-removal operation frozen in operation-refinements.json.
const unescapeAccess = s => s.replace(/\\([.\[\]\\])/g, '$1');
const fieldTitle = fd => typeof fd.field === 'string' ? fd.field.replace(/\\([.\[\]\\])/g, '$1') : '';
const ordinaryName = s => s.replace(/[.\[\]]/g, '');

function changed(a, b, at = '') {
  if (JSON.stringify(a) === JSON.stringify(b)) return [];
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
    return [...keys].flatMap(k => changed(a[k], b[k], at + '/' + k.replace(/~/g, '~0').replace(/\//g, '~1')));
  }
  return [{pointer: at || '/', before: a === undefined ? {absent: true} : a,
           after: b === undefined ? {absent: true} : b}];
}

function packages() {
  const rows = [];
  function scan(dir) {
    if (!fs.existsSync(dir)) return;
    for (const name of fs.readdirSync(dir)) {
      if (name.startsWith('.')) continue;
      const location = path.join(dir, name);
      if (name.startsWith('@')) { scan(location); continue; }
      const manifest = path.join(location, 'package.json');
      if (!fs.existsSync(manifest)) continue;
      const p = JSON.parse(fs.readFileSync(manifest, 'utf8'));
      rows.push({name: p.name, version: p.version, path: path.relative(MOD, location),
                 package_json_sha256: sha(fs.readFileSync(manifest))});
      scan(path.join(location, 'node_modules'));
    }
  }
  scan(MOD);
  return rows.sort((a, b) => a.path.localeCompare(b.path));
}

function importedPackages() {
  const found = new Map();
  for (const file of Object.keys(require.cache)) {
    if (!file.startsWith(MOD + path.sep)) continue;
    let dir = path.dirname(file);
    while (dir.startsWith(MOD)) {
      const manifest = path.join(dir, 'package.json');
      if (fs.existsSync(manifest)) {
        const p = JSON.parse(fs.readFileSync(manifest, 'utf8'));
        found.set(dir, {name: p.name, version: p.version, path: path.relative(MOD, dir)});
        break;
      }
      dir = path.dirname(dir);
    }
  }
  return [...found.values()].sort((a, b) => a.path.localeCompare(b.path));
}

function versionReport() {
  const data = {
    UTC: new Date().toISOString(), node: process.version, platform: process.platform,
    architecture: process.arch, vega_lite_export: vl.version, vega_export: vega.version,
    vega_lite_main: path.relative(BASE, require.resolve(path.join(MOD, 'vega-lite'))),
    vega_main: path.relative(BASE, require.resolve(path.join(MOD, 'vega'))),
    vega_lite_main_sha256: sha(fs.readFileSync(require.resolve(path.join(MOD, 'vega-lite')))),
    vega_main_sha256: sha(fs.readFileSync(require.resolve(path.join(MOD, 'vega')))),
    canvas_present: fs.existsSync(path.join(MOD, 'canvas/package.json')),
    installed_packages: packages(), imported_packages: importedPackages()
  };
  if (data.vega_lite_export !== '5.1.0' || data.vega_export !== '5.20.2') {
    throw new Error('Refuse compiler/runtime version substitution.');
  }
  save('versions.json', data);
  return data;
}

function observationTree(root) {
  const rows = [];
  function visit(mark, address, chain) {
    const markInfo = {name: mark.name || null, role: mark.role || null, marktype: mark.marktype || null};
    for (const [index, item] of (mark.items || []).entries()) {
      const itemPath = address + '/items/' + index;
      const row = {path: itemPath, ...markInfo, ancestors: chain};
      for (const key of ['text', 'fill', 'stroke', 'opacity', 'strokeOpacity', 'fillOpacity', 'x', 'y',
                          'x2', 'y2', 'width', 'height', 'size', 'shape', 'font', 'fontSize', 'limit',
                          'align', 'baseline', 'angle', 'description', 'aria']) {
        if (item[key] !== undefined) row[key] = typeof item[key] === 'number' && !Number.isFinite(item[key])
          ? {nonfinite: String(item[key])} : item[key];
      }
      if (item.datum !== undefined) row.datum = JSON.parse(JSON.stringify(item.datum));
      if (item.bounds) row.bounds = {x1: item.bounds.x1, y1: item.bounds.y1, x2: item.bounds.x2, y2: item.bounds.y2};
      rows.push(row);
      for (const [childIndex, child] of (item.items || []).entries()) {
        visit(child, itemPath + '/items/' + childIndex, [...chain, {...markInfo, item_index: index}]);
      }
    }
  }
  visit(root, '/root', []);
  return rows;
}

async function main() {
  const versions = versionReport();
  if (process.argv.includes('--versions')) {
    console.log(JSON.stringify({vega_lite: vl.version, vega: vega.version,
      node: process.version, installed_packages: versions.installed_packages.length,
      imported_packages: versions.imported_packages, canvas_present: versions.canvas_present}));
    return;
  }
  const boundary = read('inputs/V02-original-boundary.json');
  const v03 = read('inputs/V03-original.json');
  if (!Array.isArray(boundary.data.values) || boundary.data.values.length !== 3 ||
      !Array.isArray(v03.data.values) || v03.data.values.length !== 10) throw new Error('Wrong input rows.');
  if (Object.keys(boundary.data).some(k => k !== 'values') || Object.keys(v03.data).some(k => k !== 'values'))
    throw new Error('Only original inline data is allowed.');
  const normal = clone(boundary);
  normal.data.values = normal.data.values.map(row => Object.fromEntries(Object.entries(row).map(([k, v]) => [ordinaryName(k), v])));
  normal.repeat.row = normal.repeat.row.map(s => ordinaryName(unescapeAccess(s)));
  normal.repeat.column = normal.repeat.column.map(s => ordinaryName(unescapeAccess(s)));
  normal.spec.encoding.color.field = ordinaryName(unescapeAccess(normal.spec.encoding.color.field));
  save('inputs/V02-researcher-normal.json', normal);
  const runs = [];
  for (const [condition, input] of [['normal', normal], ['boundary', boundary]]) {
    for (const operation of ['A', 'B']) {
      const spec = clone(input);
      if (operation === 'B') {
        spec.repeat.row = spec.repeat.row.map(unescapeAccess);
        spec.repeat.column = spec.repeat.column.map(unescapeAccess);
        spec.spec.encoding.color.field = unescapeAccess(spec.spec.encoding.color.field);
      }
      runs.push({run_id: `V02-${condition}-${operation}`, requirement_id: 'V02', condition, operation,
        original: input, spec, compile_options: operation === 'A' ? {fieldTitle} : {},
        operation_code: operation === 'A' ? fieldTitle.toString() : unescapeAccess.toString(),
        normal_input_origin: condition === 'normal' ? 'researcher rename control; not author external normal example' : 'original body JSON'});
    }
  }
  for (const operation of ['A', 'B']) {
    const spec = clone(v03);
    if (operation === 'A') spec.layer[0].encoding.y.axis.labelColor.condition.test = "datum.value === '4. Hygiene & Cleaning'";
    runs.push({run_id: `V03-fixed-${operation}`, requirement_id: 'V03', condition: 'fixed-original-10-records',
      operation, original: v03, spec, compile_options: {}, operation_code: spec.layer[0].encoding.y.axis.labelColor.condition.test});
  }
  save('input-diffs.json', {
    researcher_normal_from_original: changed(boundary, normal),
    runs: runs.map(r => ({run_id: r.run_id, operation_code: r.operation_code,
      spec_changes: changed(r.original, r.spec), compile_option_keys: Object.keys(r.compile_options),
      original_schema: r.original.$schema || null, actual_schema: r.spec.$schema || null}))
  });
  const receipts = [];
  for (const r of runs) {
    const started = new Date().toISOString();
    const warnings = [];
    const logger = vega.logger(vega.Warn);
    for (const level of ['warn', 'error', 'info', 'debug']) logger[level] = (...args) => {
      warnings.push({level, args: args.map(a => a instanceof Error ? a.stack : String(a))}); return logger;
    };
    const result = {
      run_id: r.run_id, requirement_id: r.requirement_id, condition: r.condition, operation: r.operation,
      started_UTC: started, input: save(`inputs/${r.run_id}.json`, r.spec),
      compile_option_keys: Object.keys(r.compile_options), operation_code: r.operation_code,
      normal_input_origin: r.normal_input_origin || null, compiler: vl.version, runtime: vega.version,
      original_schema: r.spec.$schema || null, warnings
    };
    let view;
    try {
      const compiled = vl.compile(r.spec, {...r.compile_options, logger}).spec;
      result.compiled = save(`outputs/${r.run_id}.vega.json`, compiled);
      const blockedLoader = {load: async url => {throw new Error('External loads prohibited in replay: ' + url);},
        sanitize: async url => {throw new Error('External image loads prohibited in replay: ' + url);}};
      view = new vega.View(vega.parse(compiled), {renderer: 'none', logger, loader: blockedLoader});
      await view.runAsync();
      const svg = await view.toSVG();
      result.svg = save(`outputs/${r.run_id}.svg`, svg);
      const observations = observationTree(view.scenegraph().root);
      result.scenegraph = save(`outputs/${r.run_id}.scenegraph.json`, observations);
      if (typeof vega.sceneToJSON === 'function') {
        const serialized = vega.sceneToJSON(view.scenegraph().root);
        result.scenegraph_export = save(`outputs/${r.run_id}.scenegraph-export.json`, serialized);
      }
      result.status = 'rendered';
      result.observation_count = observations.length;
    } catch (error) {
      result.status = 'failed';
      result.error = {name: error.name, message: error.message, stack: error.stack};
    } finally {
      if (view) view.finalize();
      result.finished_UTC = new Date().toISOString();
      receipts.push(result);
      save('render-receipts.json', receipts);
      console.log(JSON.stringify({run_id: result.run_id, status: result.status,
        warnings: result.warnings, error: result.error || null, input: result.input, svg: result.svg || null}));
    }
  }
  versionReport();
  if (receipts.some(r => r.status !== 'rendered')) process.exitCode = 1;
}
main().catch(error => {console.error(error.stack); process.exitCode = 1;});
