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

async function buildInputs(planPath) {
  const tracked = ['plan.json', 'fixture/index.html', 'fixture/map.js', 'fixture/package.json',
    'fixture/package-lock.json', 'fixture/fingerprints.json', 'replay/drive.mjs'];
  const fileHashes = Object.fromEntries(await Promise.all(tracked.map(async (name) => [
    name, await shaFile(name === 'plan.json' ? planPath : join(root, name)),
  ])));
  const pins = await json(join(fixture, 'fingerprints.json'));
  const releaseFiles = Object.fromEntries(await Promise.all(Object.keys(pins.package_files).map(async (name) => [
    name, await shaFile(join(fixture, 'node_modules', 'ol', name)),
  ])));
  for (const [name, hash] of Object.entries(releaseFiles)) {
    assert.equal(hash, pins.package_files[name].sha256, name);
  }
  const {outputFiles, metafile} = await build({
    absWorkingDir: fixture,
    entryPoints: ['map.js'],
    bundle: true,
    format: 'iife',
    target: 'chrome120',
    charset: 'utf8',
    outfile: 'fixture-bundle.js',
    write: false,
    metafile: true,
  });
  const browserSources = Object.entries(metafile.outputs['fixture-bundle.js'].inputs);
  const loadedSources = Object.fromEntries(await Promise.all(browserSources.map(async ([name, info]) => [
    name, {sha256: await shaFile(join(fixture, name)), bytesInBundle: info.bytesInOutput},
  ])));
  for (const [name, hash] of Object.entries(releaseFiles)) {
    assert.equal(loadedSources['node_modules/ol/' + name]?.sha256, hash, 'browser bundle includes ' + name);
  }
  const bundle = outputFiles[0].text;
  const versions = Object.fromEntries(await Promise.all(['ol', 'esbuild', 'playwright-core'].map(async (name) => [
    name, (await json(join(fixture, 'node_modules', name, 'package.json'))).version,
  ])));
  const lock = await json(join(fixture, 'package-lock.json'));
  assert.equal(versions.ol, pins.version);
  assert.equal(lock.packages['node_modules/ol'].integrity, pins.tarball.integrity);
  return {
    html: await readFile(join(fixture, 'index.html'), 'utf8'),
    bundle,
    metadata: {
      browserBundleSha256: digest(bundle), browserBundleBytes: Buffer.byteLength(bundle),
      versions, fileHashes, loadedSources, releaseFiles, npmIntegrity: lock.packages['node_modules/ol'].integrity,
      sourceCommit: pins.source_commit,
    },
  };
}

async function surface(page, out) {
  const bytes = await page.locator('#map').screenshot({animations: 'allow', scale: 'css'});
  const name = digest(bytes) + '.png';
  try {
    await writeFile(join(out, 'surfaces', name), bytes, {flag: 'wx'});
  } catch (error) {
    if (error.code !== 'EEXIST') throw error;
  }
  return {sha256: digest(bytes), path: 'surfaces/' + name};
}

async function runCase(browser, plan, scenario, input, out) {
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
    assert.equal(loadedBundleSha256, input.metadata.browserBundleSha256, 'actual inline browser code');
    const initial = await page.evaluate(({settings, row}) => {
      window.af127.session = window.af127.prepare(settings, row);
      return window.af127.session.initial;
    }, {settings: plan, row: scenario});
    assert.deepEqual(initial.rect, plan.mapRectCssPx);
    assert.equal(initial.dpr, plan.dpr);
    assert.equal(initial.loadedOlVersion, input.metadata.versions.ol);
    assert.equal(initial.projection, plan.view.projection);
    assert.deepEqual(initial.afterSeed.selectedIds, plan.seed[scenario.selection]);
    const [mapX, mapY] = plan.positions[scenario.position];
    const [left, top] = plan.mapRectCssPx;
    const start = [left + mapX, top + mapY];
    const moves = plan.moves[scenario.gesture].map(([dx, dy]) => [start[0] + dx, start[1] + dy]);
    const steps = [];
    async function step(phase, client, action) {
      await page.evaluate((label) => window.af127.session.setPhase(label), phase);
      if (action) await action();
      steps.push(await page.evaluate((point) => window.af127.session.afterRender(point), client));
    }

    const surfaces = {initial: await surface(page, out)};
    await step('hover', start, () => page.mouse.move(...start));
    await step('down', start, () => page.mouse.down({button: 'left'}));
    for (const [index, point] of moves.entries()) {
      await step('move-' + (index + 1), point, () => page.mouse.move(...point));
    }
    const end = moves.at(-1) ?? start;
    await step('up', end, () => page.mouse.up({button: 'left'}));
    await new Promise((resolve) => setTimeout(resolve, plan.settleMs));
    await step('settled', end);
    surfaces.settled = await surface(page, out);
    const records = await page.evaluate(() => window.af127.session.records());
    return {
      scenario, initial, loadedBundleSha256, commanded: {start, moves, end}, steps, records, surfaces, notices,
    };
  } finally {
    await context.close();
  }
}

const allowedModes = ['pilot', 'main', 'controls', 'supplement', 'all'];
const {values} = parseArgs({options: {
  mode: {type: 'string'},
  out: {type: 'string'},
  chromium: {type: 'string', default: '/usr/bin/chromium'},
  plan: {type: 'string', default: join(root, 'plan.json')},
}});
assert.ok(values.out && allowedModes.includes(values.mode), 'supply --mode and --out');
const plan = await json(values.plan);
assert.ok(values.mode === 'pilot' || plan.sealed, 'non-pilot replay needs a sealed plan');
assert.equal(plan.renderWaitFramesAfterEachCommand, 2);
const input = await buildInputs(resolve(values.plan));
const out = resolve(values.out);
await mkdir(join(out, 'surfaces'), {recursive: true});
const modes = values.mode === 'all' ? ['main', 'controls', 'supplement'] : [values.mode];
const startedUtc = new Date().toISOString();
const browser = await chromium.launch({executablePath: values.chromium, headless: true,
  args: ['--disable-background-networking', '--disable-dev-shm-usage', '--no-sandbox']});
try {
  for (const mode of modes) {
    const folder = join(out, mode);
    await mkdir(folder, {recursive: true});
    const rows = new Map(plan.cases[mode].map((row) => [row.id, row]));
    for (const id of plan.executionOrder[mode]) {
      const result = await runCase(browser, plan, rows.get(id), input, out);
      await writeJson(join(folder, id + '.json'), result);
      console.log(id, result.records.length, 'events', result.notices.length, 'notices');
    }
    await writeJson(join(folder, 'environment.json'), {
      mode, startedUtc, finishedUtc: new Date().toISOString(),
      codeCommit: execFileSync('git', ['rev-parse', 'HEAD'], {cwd: root, encoding: 'utf8'}).trim(),
      browser: browser.version(), executable: values.chromium, executableSha256: await shaFile(values.chromium),
      node: process.version, arch: arch(), kernel: release(), userAgent: await (async () => {
        const page = await browser.newPage();
        try {
          return await page.evaluate(() => navigator.userAgent);
        } finally {
          await page.close();
        }
      })(),
      ...input.metadata,
    });
  }
} finally {
  await browser.close();
}
