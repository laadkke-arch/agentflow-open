/* Offline Chromium replay with immutable browser inputs. */
'use strict';

const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const {createHash} = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {parseArgs} = require('node:util');

const root = path.resolve(__dirname, '..');
const fixture = path.join(root, 'fixture');
const variants = ['original', 'local', 'shared'];
const renderers = ['svg', 'canvas'];
const states = ['empty', 'active'];
const positions = ['mark', 'plot'];
const fontFamily = 'AF123 Replay Sans';
const offPlot = [2, 2];
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><title>V8628</title>
<style>body{margin:0;background:white}#viz{position:absolute;left:16px;top:16px}
canvas,svg{display:block;margin:0;border:0;padding:0}</style><main id="viz"></main></html>`;

const sha = value => createHash('sha256').update(value).digest('hex');
const readJSON = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const writeJSON = (file, value, indent) =>
  fs.writeFileSync(file, JSON.stringify(value, null, indent) + '\n');

function inputFiles(engine, font) {
  const fingerprints = readJSON(path.join(fixture, 'fingerprints.json'));
  for (const [file, expected] of Object.entries(fingerprints.files)) {
    assert.equal(sha(fs.readFileSync(path.join(fixture, file))), expected, file);
  }
  for (const [file, expected] of Object.entries(fingerprints.browser_bundles)) {
    assert.equal(sha(fs.readFileSync(path.join(engine, 'node_modules', file))), expected, file);
  }
  const fontBytes = fs.readFileSync(font);
  assert.equal(sha(fontBytes), fingerprints.font.sha256, 'font SHA-256');
  assert.deepEqual(readJSON(path.join(engine, 'package-lock.json')),
    readJSON(path.join(fixture, 'npm', 'package-lock.json')), 'engine lockfile');

  return {
    fontFamily, fontBase64: fontBytes.toString('base64'),
    csv: fs.readFileSync(path.join(fixture, 'data/seattle-weather.csv'), 'utf8'),
    fingerprints,
    bundles: Object.keys(fingerprints.browser_bundles).map(file => path.join(engine, 'node_modules', file)),
    versions: Object.fromEntries(['vega', 'vega-lite', 'playwright-core'].map(name => [
      name, readJSON(path.join(engine, 'node_modules', name, 'package.json')).version
    ]))
  };
}

function point(chart, plot) {
  return plot.map((value, i) => chart.system.plotOrigin[i] + chart.system.scale[i] * value);
}

function drag(start, horizontalOffsets) {
  return {start, moves: horizontalOffsets.map(dx => [start[0] + dx, start[1]])};
}

function planFromScene(chart) {
  const {bars, scales, system} = chart;
  assert.equal(scales.bands.length, 12);
  const june = scales.bands[5];
  const april = scales.bands[3];
  const september = scales.bands[8];
  const november = scales.bands[10];
  const mid = band => Math.round((band.start + band.end) / 2);
  const segment = band => bars.filter(bar => bar.month === band.value)
    .sort((a, b) => (b.bounds[3] - b.bounds[1]) - (a.bounds[3] - a.bounds[1]))[0];
  const july = scales.bands[6];
  const august = scales.bands[7];
  const juneMark = segment(june);
  const novemberMark = segment(november);
  const y = bar => Math.round((bar.bounds[1] + bar.bounds[3]) / 2);
  const blankY = Math.max(5, Math.floor(Math.min(...bars.map(bar => bar.bounds[1])) / 2));
  const mark = [mid(june), y(juneMark)];
  const plot = [mid(june), blankY];
  const outsideMark = [mid(november), y(novemberMark)];
  const outsidePlot = [mid(november), blankY];
  const seedStart = mid(april);
  const seedEnd = mid(september);
  const edge = Math.ceil(june.start);
  const edgeStart = mid(scales.bands[4]);
  const seedMonths = scales.bands.slice(3, 9).map(band => band.value);

  assert.equal(system.dpr, 1);
  assert.deepEqual(system.scale, [1, 1]);
  assert.ok(bars.every(bar => blankY < bar.bounds[1] - 1), 'blank row avoids all bar bounds');
  assert.ok([mid(july), mid(august)].every(x => x < seedEnd));
  assert.ok(mark[0] > juneMark.bounds[0] + 1 && mark[0] < juneMark.bounds[2] - 1);
  assert.ok(mark[1] > juneMark.bounds[1] + 1 && mark[1] < juneMark.bounds[3] - 1);

  return {
    sealedBeforeMain: true, chartSystem: system, offPlot, toleranceCssPx: [0.5, 1, 2, 4],
    primaryThresholdCssPx: 2, cases: {matrix: caseList('matrix'), controls: caseList('controls')},
    coordinates: {mark, plot, juneMark, novemberMark, blankY, edge, juneBand: june},
    seed: {gesture: drag([seedStart, blankY], [1, mid(june) - seedStart, seedEnd - seedStart]),
      extent: [seedStart, seedEnd], months: seedMonths},
    gestures: {
      mark: drag(mark, [1, 20, 40]),
      plot: drag(plot, [1, 20, 40]),
      edgeOut: drag([edgeStart, blankY], [1, edge - 1 - edgeStart]),
      edgeIn: drag([edgeStart, blankY], [1, edge - edgeStart]),
      clickIn: drag(plot, []),
      clickOut: drag(outsidePlot, []),
      reverseIn: drag(mark, [-1, -20, -40]),
      reverseOut: drag(outsideMark, [-1, -20, -40]),
      reverseOutPlot: drag(outsidePlot, [-1, -20, -40]),
      verticalExit: {start: mark, moves: [[mark[0], blankY]]}
    }
  };
}

function caseList(mode) {
  const cases = [];
  for (const variant of variants) {
    for (const renderer of renderers) {
      for (const state of states) {
        for (const position of positions) {
          for (const repeat of (mode === 'pilot' ? [1] : [1, 2])) {
            const prefix = mode === 'pilot' ? 'P' : 'M';
            cases.push({
              id: [prefix, variant, renderer, state, position, repeat].join('-'),
              variant, renderer, state, position, repeat, observers: true, gesture: position
            });
          }
        }
      }
    }
  }
  if (mode !== 'controls') return cases;

  const controls = [
    ['C01-edge-out', 'empty', 'plot', 'edgeOut', true],
    ['C02-edge-in', 'empty', 'plot', 'edgeIn', true],
    ['C03-click-in', 'active', 'plot', 'clickIn', true],
    ['C04-click-out', 'active', 'plot', 'clickOut', true],
    ['C05-reverse-in', 'active', 'mark', 'reverseIn', true],
    ['C06-reverse-out-mark', 'active', 'mark', 'reverseOut', true],
    ['C07-reverse-out-plot', 'active', 'plot', 'reverseOutPlot', true],
    ['C08-vertical-exit', 'empty', 'mark', 'verticalExit', true],
    ['C09-observers-off', 'empty', 'mark', 'mark', false]
  ];
  return controls.flatMap(([key, state, position, gesture, observers]) =>
    renderers.flatMap(renderer => [1, 2].map(repeat => ({
      id: [key, renderer, repeat].join('-'), variant: 'original',
      renderer, state, position, gesture, observers, repeat
    }))));
}

async function makePage(context, input, scenario, notices) {
  const page = await context.newPage();
  page.on('console', message => {
    if (['warning', 'error'].includes(message.type())) notices.push([message.type(), message.text()]);
  });
  page.on('pageerror', error => notices.push(['pageerror', error.message]));
  page.on('request', request => notices.push(['external request', request.url()]));
  await page.setContent(html);
  for (const bundle of input.bundles) {
    await page.addScriptTag({path: bundle});
  }
  await page.addScriptTag({path: path.join(__dirname, 'page.js')});
  const {variant, renderer, observers} = scenario;
  const spec = readJSON(path.join(fixture, variant + '.vl.json'));
  const chart = await page.evaluate(options => window.af123.prepare(options), {
    renderer, observers, spec, csv: input.csv, fontFamily, fontBase64: input.fontBase64
  });
  assert.deepEqual(chart.loads, ['data/seattle-weather.csv']);
  assert.ok(chart.font, 'pinned browser font loaded');
  assert.ok(chart.axes.every(axis => axis.font === fontFamily), 'pinned axis font');
  assert.equal(chart.timeZone, 'UTC');
  assert.equal(chart.lang, 'en-US');
  assert.equal(chart.versions.vega, input.versions.vega);
  return {page, chart};
}

async function observeStep(page, trajectory, phase, step, client, action) {
  const commandedAt = await page.evaluate(message => window.af123.begin(message), {phase, step});
  await action();
  const snapshot = await page.evaluate(client => window.af123.observe(client), client);
  trajectory.push({phase, step, client, commandedAt});
  return snapshot.first;
}

async function perform(page, chart, trajectory, phase, gesture, hoverOnly = false) {
  await observeStep(page, trajectory, phase, 'reset', offPlot, () => page.mouse.move(...offPlot));
  const start = point(chart, gesture.start);
  const before = await observeStep(page, trajectory, phase, 'hover', start, () => page.mouse.move(...start));
  if (hoverOnly) return before;

  await observeStep(page, trajectory, phase, 'down', start, () => page.mouse.down({button: 'left'}));
  for (const [i, target] of gesture.moves.entries()) {
    const client = point(chart, target);
    await observeStep(page, trajectory, phase, i === 0 ? 'first' : `move-${i + 1}`, client,
      () => page.mouse.move(...client));
  }
  const end = point(chart, gesture.moves.at(-1) ?? gesture.start);
  return observeStep(page, trajectory, phase, 'up', end, () => page.mouse.up({button: 'left'}));
}

function compactSnapshots(snapshots) {
  const invariants = {};
  for (const snapshot of snapshots) {
    const {axes, scales, aggregate, geometry, ...state} = snapshot.first;
    const preserved = {axes, scales, aggregate, geometry};
    const digest = sha(JSON.stringify(preserved));
    invariants[digest] = preserved;
    snapshot.first = {...state, invariantsSha256: digest};
  }
  return invariants;
}

async function runCase(browser, input, mode, scenario, plan, out) {
  const context = await browser.newContext({
    viewport: {width: 900, height: 650}, deviceScaleFactor: 1,
    locale: 'en-US', timezoneId: 'UTC', offline: true, hasTouch: false, isMobile: false
  });
  const notices = [];
  const trajectory = [];
  const raw = {scenario, startedUtc: new Date().toISOString(), trajectory, notices};
  let page;
  let chart;
  try {
    ({page, chart} = await makePage(context, input, scenario, notices));
    const {raster, compiled, ...description} = chart;
    raw.chart = {...description, staticPaintSha256: sha(raster)};
    fs.mkdirSync(path.join(out, 'compiled'), {recursive: true});
    const compiledFile = path.join(out, 'compiled', scenario.variant + '.json');
    if (!fs.existsSync(compiledFile)) writeJSON(compiledFile, compiled, 2);
    raw.compiledSha256 = sha(fs.readFileSync(compiledFile));

    const gesture = plan?.gestures[scenario.gesture];
    if (!plan) {
      plan = planFromScene(chart);
      writeJSON(path.join(out, 'plan.json'), plan, 2);
    } else {
      assert.deepEqual(chart.system, plan.chartSystem, 'sealed chart coordinates');
      await observeStep(page, trajectory, 'baseline', 'initial', null, async () => {});
      if (scenario.state === 'active') {
        const initialized = await perform(page, chart, trajectory, 'initialize', plan.seed.gesture);
        raw.initialization = {
          expected: plan.seed, observed: {extent: initialized.visual, months: initialized.projected}
        };
        try {
          assert.deepEqual(initialized.visual, plan.seed.extent);
          assert.deepEqual(initialized.projected, plan.seed.months);
        } catch (error) {
          raw.status = 'initialization_failed';
          throw error;
        }
      }
      await perform(page, chart, trajectory, 'test', gesture, mode === 'pilot');
    }
    assert.equal(notices.filter(([kind]) => kind !== 'warning').length, 0, 'browser errors or network');
    raw.status = mode === 'pilot' ? 'pilot' : 'executed';
  } catch (error) {
    raw.status ??= 'execution_failed';
    raw.error = String(error.stack ?? error);
  } finally {
    if (page) {
      const observed = await page.evaluate(() => window.af123.collect()).catch(() => null);
      if (observed) {
        raw.invariants = compactSnapshots(observed.snapshots);
        raw.events = observed.events;
        raw.snapshots = observed.snapshots;
        raw.finalPaintSha256 = sha(observed.finalRaster);
      }
    }
    await context.close();
  }
  raw.finishedUtc = new Date().toISOString();
  writeJSON(path.join(out, scenario.id + '.json'), raw);
  process.stdout.write(`${scenario.id}\t${raw.status}\t${raw.events?.length ?? 0} callbacks\n`);
  if (raw.error) process.stderr.write(`${scenario.id}: ${raw.error}\n`);
  return {plan, status: raw.status};
}

async function main() {
  const {values} = parseArgs({options: {
    mode: {type: 'string'}, engine: {type: 'string'}, out: {type: 'string'},
    chromium: {type: 'string', default: '/usr/bin/chromium'},
    font: {type: 'string', default: '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'}
  }});
  const {mode, chromium, font} = values;
  if (!['pilot', 'matrix', 'controls'].includes(mode) || !values.engine || !values.out) {
    throw new Error('usage: node drive.cjs --mode pilot|matrix|controls --engine <npm prefix> --out <new directory>');
  }
  const out = path.resolve(values.out);
  const engine = path.resolve(values.engine);
  fs.mkdirSync(out);
  const input = inputFiles(engine, font);
  const playwright = require(path.join(engine, 'node_modules/playwright-core'));
  const args = ['--disable-dev-shm-usage', '--disable-gpu', '--disable-background-networking'];
  const browser = await playwright.chromium.launch({
    executablePath: chromium, headless: true, args,
    env: {...process.env, TZ: 'UTC', XDG_CACHE_HOME: path.join(out, 'cache'), XDG_CONFIG_HOME: path.join(out, 'config')}
  });
  try {
    writeJSON(path.join(out, 'environment.json'), {
      startedUtc: new Date().toISOString(), mode, versions: input.versions,
      node: process.version, npm: execFileSync('npm', ['--version'], {encoding: 'utf8'}).trim(),
      chromium: browser.version(), chromiumCLI: execFileSync(chromium, ['--version'], {encoding: 'utf8'}).trim(),
      chromiumExecutable: chromium, os: os.version(), platform: process.platform, arch: process.arch,
      args, viewport: [900, 650], dpr: 1, timezone: 'UTC', locale: 'en-US',
      headless: true, offlineContext: true, browserFont: fontFamily, fingerprints: input.fingerprints
    }, 2);
    let plan;
    if (mode === 'pilot') {
      const discovery = await runCase(browser, input, mode, {
        id: 'P-discovery', variant: 'original', renderer: 'svg', state: 'empty', observers: true
      }, null, out);
      if (!discovery.plan) throw new Error('pilot failed to propose coordinates');
      plan = discovery.plan;
    } else {
      plan = readJSON(path.join(root, 'plan.json'));
      assert.ok(plan.sealedBeforeMain, 'missing coordinate seal');
    }
    let failures = 0;
    const cases = mode === 'pilot' ? caseList(mode) : plan.cases[mode];
    for (const scenario of cases) {
      const {status} = await runCase(browser, input, mode, scenario, plan, out);
      if (!['executed', 'pilot'].includes(status)) failures += 1;
    }
    process.stdout.write(`${mode}: ${cases.length - failures}/${cases.length} completed\n`);
    if (failures) process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

if (require.main === module) {
  main().catch(error => {
    process.stderr.write(String(error.stack ?? error) + '\n');
    process.exitCode = 1;
  });
}
