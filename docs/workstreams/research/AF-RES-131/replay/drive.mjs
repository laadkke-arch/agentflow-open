import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import {arch, release} from 'node:os';
import {join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs} from 'node:util';

const root = fileURLToPath(new URL('..', import.meta.url));
const fixture = join(root, 'fixture');
const require = createRequire(join(fixture, 'package.json'));
const {build} = require('esbuild');
const {chromium} = require('playwright-core');
const json = async (path) => JSON.parse(await readFile(path, 'utf8'));
const digest = (data) => createHash('sha256').update(data).digest('hex');
const shaFile = async (file) => digest(await readFile(file));
const writeJson = async (file, value) => writeFile(file, JSON.stringify(value) + '\n', {flag: 'wx'});

async function buildInputs(version, pin, lock, html) {
  const packageRoot = join(fixture, 'node_modules', pin.npm_alias);
  const packageInfo = await json(join(packageRoot, 'package.json'));
  assert.equal(packageInfo.version, version);
  const lockEntry = lock.packages['node_modules/' + pin.npm_alias];
  assert.equal(lockEntry.version, version);
  assert.equal(lockEntry.integrity, pin.npm_integrity);
  assert.equal(lockEntry.resolved, pin.npm_tarball);
  const releaseFiles = {};
  for (const [name, expected] of Object.entries(pin.package_files)) {
    const hash = await shaFile(join(packageRoot, name));
    assert.equal(hash, expected, version + ' ' + name);
    releaseFiles[name] = hash;
  }
  const {outputFiles, metafile} = await build({
    absWorkingDir: fixture,
    entryPoints: ['map.js'],
    alias: {ol: pin.npm_alias},
    bundle: true,
    format: 'iife',
    target: 'chrome120',
    charset: 'utf8',
    outfile: 'fixture-bundle.js',
    write: false,
    metafile: true,
  });
  const sources = metafile.outputs['fixture-bundle.js'].inputs;
  const loadedSources = {};
  for (const [name, hash] of Object.entries(releaseFiles)) {
    const source = 'node_modules/' + pin.npm_alias + '/' + name;
    assert.ok(sources[source]?.bytesInOutput > 0, 'browser bundle includes ' + source);
    loadedSources[name] = {sha256: hash, bytesInBundle: sources[source].bytesInOutput};
  }
  const bundle = outputFiles[0].text;
  return {
    html, bundle, pin,
    metadata: {
      browserBundleSha256: digest(bundle), browserBundleBytes: Buffer.byteLength(bundle),
      ol: packageInfo.version, sourceCommit: pin.git_commit, loadedSources,
      npmIntegrity: lockEntry.integrity, tarballSha256: pin.tarball_sha256,
    },
  };
}

async function runCase(browser, plan, scenario, input) {
  const context = await browser.newContext({
    viewport: plan.viewport, deviceScaleFactor: plan.dpr, locale: 'ko-KR',
    timezoneId: 'UTC', reducedMotion: 'reduce', colorScheme: 'light', serviceWorkers: 'block',
  });
  const notices = [];
  try {
    await context.route('**/*', async (route) => {
      notices.push({type: 'network', text: route.request().url()});
      await route.abort();
    });
    const page = await context.newPage();
    page.on('pageerror', (error) => notices.push({type: 'pageerror', text: error.message}));
    page.on('console', (message) => {
      if (['warning', 'error'].includes(message.type())) notices.push({type: message.type(), text: message.text()});
    });
    await page.setContent(input.html);
    const script = await page.addScriptTag({content: input.bundle});
    const loadedBundleSha256 = digest(await script.textContent());
    assert.equal(loadedBundleSha256, input.metadata.browserBundleSha256);
    const initial = await page.evaluate(({settings, row, pin}) => {
      window.af131.session = window.af131.prepare(settings, row, pin);
      return window.af131.session.initial;
    }, {settings: plan, row: scenario, pin: input.pin});
    assert.deepEqual(initial.rect, plan.mapRectCssPx);
    assert.equal(initial.dpr, plan.dpr);
    assert.equal(initial.loadedOlVersion, scenario.version);
    assert.equal(initial.projection, plan.view.projection);
    assert.deepEqual(initial.afterSeed.selectedIds, plan.seed[scenario.collection === 'included' ? 'in' : 'out']);
    assert.deepEqual(initial.afterSeed.geometry, plan.feature.coordinate);
    assert.deepEqual(initial.afterSeed.center, plan.view.center);
    assert.equal(initial.afterSeed.resolution, plan.view.resolution);
    assert.equal(initial.afterSeed.rotation, plan.view.rotation);
    assert.equal(initial.radiusCssPx, plan.feature.radiusCssPx);
    assert.equal(initial.selectedStyleMatchesPoint, true);
    assert.equal(initial.activeInteractions.includes('translate'), scenario.translateActive);

    const [mapX, mapY] = plan.positions[scenario.position];
    const [left, top] = plan.mapRectCssPx;
    const start = [left + mapX, top + mapY];
    const moves = plan.moves[scenario.gesture].map(([dx, dy]) => [start[0] + dx, start[1] + dy]);
    const steps = [];
    async function step(phase, client, action) {
      if (scenario.observers || phase === 'settled') {
        await page.evaluate((label) => window.af131.session.setPhase(label), phase);
      }
      if (action) await action();
      const observed = scenario.observers || phase === 'settled';
      const snapshot = await page.evaluate((point) => window.af131.session.afterRender(point),
        observed ? client : null);
      if (observed) steps.push(snapshot);
    }

    const surfaceSha256 = digest(await page.locator('#map').screenshot({animations: 'allow', scale: 'css'}));
    await step('hover', start, () => page.mouse.move(...start));
    await step('down', start, () => page.mouse.down({button: 'left'}));
    for (const [index, point] of moves.entries()) {
      await step('move-' + (index + 1), point, () => page.mouse.move(...point));
    }
    const end = moves.at(-1) ?? start;
    await step('up', end, () => page.mouse.up({button: 'left'}));
    await new Promise((resolve) => setTimeout(resolve, plan.settleMs));
    await step('settled', end);
    const records = await page.evaluate(() => window.af131.session.records());
    const status = notices.some(({type}) => type === 'pageerror' || type === 'network' || type === 'error')
      ? 'error' : 'observed';
    return {scenario, status, initial, loadedBundleSha256, surfaceSha256,
      commanded: {start, moves, end}, steps, records, notices};
  } catch (error) {
    return {scenario, status: 'error', error: String(error), stack: error.stack, notices};
  } finally {
    await context.close();
  }
}

const allowedModes = ['main', 'controls', 'supplement', 'bare', 'all'];
const {values} = parseArgs({options: {
  mode: {type: 'string'},
  out: {type: 'string'},
  chromium: {type: 'string', default: '/usr/bin/chromium'},
}});
assert.ok(values.out && allowedModes.includes(values.mode), 'supply --mode and --out');
const plan = await json(join(fixture, 'input.json'));
const cases = await json(join(fixture, 'cases.json'));
const pins = await json(join(fixture, 'versions.json'));
const lock = await json(join(fixture, 'package-lock.json'));
const html = await readFile(join(fixture, 'index.html'), 'utf8');
assert.equal(plan.renderWaitFramesAfterEachCommand, 2);
const tracked = ['fixture/input.json', 'fixture/cases.json', 'fixture/versions.json', 'fixture/index.html',
  'fixture/map.js', 'fixture/package.json', 'fixture/package-lock.json', 'replay/drive.mjs', 'predictions.csv'];
const fileHashes = Object.fromEntries(await Promise.all(tracked.map(async (name) => [name, await shaFile(join(root, name))])));
const inputs = new Map();
for (const [version, pin] of Object.entries(pins)) {
  inputs.set(version, await buildInputs(version, pin, lock, html));
}

const out = resolve(values.out);
await mkdir(out, {recursive: true});
const startedUtc = new Date().toISOString();
const browser = await chromium.launch({
  executablePath: values.chromium, headless: true,
  args: ['--disable-background-networking', '--disable-dev-shm-usage', '--no-sandbox'],
});
try {
  const cdp = await browser.newBrowserCDPSession();
  const sys = await cdp.send('SystemInfo.getInfo');
  await cdp.detach();
  const browserVersions = Object.fromEntries(Array.from(inputs, ([key, value]) => [key, value.metadata]));
  const environment = {
    mode: values.mode, startedUtc,
    codeCommit: execFileSync('git', ['rev-parse', 'HEAD'], {cwd: root, encoding: 'utf8'}).trim(),
    browser: browser.version(), executable: values.chromium, executableSha256: await shaFile(values.chromium),
    browserEngineSha256: values.chromium === '/usr/bin/chromium'
      ? await shaFile('/usr/lib/chromium/chromium').catch(() => null) : await shaFile(values.chromium),
    node: process.version, arch: arch(), kernel: release(),
    playwright: (await json(join(fixture, 'node_modules/playwright-core/package.json'))).version,
    esbuild: (await json(join(fixture, 'node_modules/esbuild/package.json'))).version,
    gpu: {devices: sys.gpu.devices, featureStatus: sys.gpu.featureStatus},
    fileHashes, browserVersions,
  };
  const modes = values.mode === 'all' ? allowedModes.slice(0, -1) : [values.mode];
  let unsuccessful = 0;
  for (const mode of modes) {
    const folder = join(out, mode);
    await mkdir(folder, {recursive: true});
    for (const scenario of cases.filter((row) => row.mode === mode)) {
      const result = await runCase(browser, plan, scenario, inputs.get(scenario.version));
      await writeJson(join(folder, scenario.id + '.json'), result);
      console.log(scenario.id, result.status, result.records?.length ?? 0, 'events', result.notices.length, 'notices');
      if (result.status !== 'observed') {
        unsuccessful++;
        console.error(scenario.id, result.error ?? result.notices);
      }
    }
  }
  await writeJson(join(out, 'environment-' + values.mode + '.json'), {
    ...environment, finishedUtc: new Date().toISOString(), unsuccessful,
  });
  if (unsuccessful) process.exitCode = 1;
} finally {
  await browser.close();
}
