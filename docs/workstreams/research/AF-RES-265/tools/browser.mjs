/* Execute isolated, loopback-only Three.js loads with browser and server receipts. */
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { setTimeout as delay } from 'node:timers/promises';
import assert from 'node:assert/strict';

const [rootArg, roundArg, only = ''] = process.argv.slice(2);
assert(rootArg && /^[12]$/.test(roundArg), 'usage: node browser.mjs <prepared dir> <1|2> [case,case]');
const root = resolve(rootArg);
const round = Number(roundArg);
const require = createRequire(join(root, 'npm', 'package.json'));
const { chromium } = require('playwright-core');
const executable = '/usr/bin/chromium';
const flags = [
  '--disable-crash-reporter', '--disable-background-networking', '--disable-component-update',
  '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
  '--disable-dev-shm-usage', '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1',
  '--proxy-server=http://127.0.0.1:1', '--proxy-bypass-list=127.0.0.1',
];
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const readJson = async file => JSON.parse(await readFile(join(root, file), 'utf8'));
const manifest = await readJson('input-manifest.json');
const allCases = await readJson('cases.json');
const selected = only ? only.split(',') : allCases.map(spec => spec.id);
assert(selected.every(id => allCases.some(spec => spec.id === id)), 'unknown case ID');
const specs = allCases.filter(spec => selected.includes(spec.id));
const fixtures = new Map(specs.map(spec => [spec.id, spec]));
const serverEvents = new Map();
const staticFiles = new Map([
  ['/', fileURLToPath(new URL('./harness.html', import.meta.url))],
  ['/harness.mjs', fileURLToPath(new URL('./harness.mjs', import.meta.url))],
]);
for (const src of manifest.files.filter(f => f.group === 'three')) {
  staticFiles.set('/three/' + src.path, join(root, src.group, src.path));
}
const contentTypes = new Map([
  ['html', 'text/html; charset=utf-8'], ['js', 'text/javascript'], ['mjs', 'text/javascript'],
  ['png', 'image/png'], ['wasm', 'application/wasm'], ['ktx2', 'image/ktx2'],
  ['gltf', 'model/gltf+json'], ['glb', 'model/gltf-binary'],
]);
const category = path => path.startsWith('/asset/') ? 'model' :
  path.includes('/libs/basis/') ? 'decoder-runtime' : 'harness-runtime';

const server = createServer(async (req, res) => {
  const name = req.headers['x-af-run'];
  const path = new URL(req.url, 'http://127.0.0.1').pathname;
  const spec = fixtures.get(name);
  let file = staticFiles.get(path);
  if (spec && path.startsWith('/asset/')) {
    const requested = decodeURIComponent(path.slice('/asset/'.length));
    if (Object.hasOwn(spec.paths, requested)) file = join(root, spec.paths[requested]);
  }
  if (spec?.omitWasm && path.endsWith('/basis_transcoder.wasm')) file = null;
  let status = 404;
  let headers = {'Cache-Control': 'no-store', 'Content-Type': 'text/plain; charset=utf-8'};
  let content = Buffer.alloc(0);
  if (file) {
    try {
      content = await readFile(file);
      status = 200;
      headers['Content-Type'] = contentTypes.get(file.split('.').at(-1)) ?? 'application/octet-stream';
    } catch (error) {
      status = 500;
      content = Buffer.from(error.code ?? 'read error');
    }
  }
  headers['Content-Length'] = content.length;
  if (!serverEvents.has(name)) serverEvents.set(name, []);
  serverEvents.get(name).push({ method: req.method, url: path, category: category(path), status,
    bodyBytes: content.length, bodySha256: sha256(content) });
  res.writeHead(status, headers).end(content);
});
await new Promise(resolve => server.listen({ host: '127.0.0.1', port: 0 }, resolve));
const origin = `http://127.0.0.1:${server.address().port}`;

const output = join(root, `round-${round}`);
await mkdir(join(output, 'frames'), { recursive: true });
let browser;
let unexpected = false;
try {
  browser = await chromium.launch({ headless: true, executablePath: executable, args: flags, timeout: 20000 });
  const environment = {
    chromium: browser.version(), executable, playwright: require('playwright-core/package.json').version,
    node: process.version, architecture: process.arch, platform: process.platform, flags,
    freshBrowserPerRound: true, freshContextPerCase: true, serviceWorkers: 'block',
    disableCache: ['route registration', 'CDP Network.setCacheDisabled', 'Cache-Control: no-store'],
    origin, round, started_utc: new Date().toISOString(),
  };
  for (const spec of [{ id: 'offline-probe' }, ...specs]) {
    const context = await browser.newContext({serviceWorkers: 'block',
      viewport: {width: 384, height: 384}, deviceScaleFactor: 1,
      extraHTTPHeaders: {'X-AF-Run': spec.id}});
    const record = { ...spec, round, started_utc: new Date().toISOString(),
      browserHttp: [], blocked: [], console: [], workers: [], pageErrors: [], non2xxWithoutFinish: [] };
    let lastEvent = performance.now();
    const pending = new Set();
    const rejectedResponses = new Map();
    await context.route('**/*', async route => {
      const url = route.request().url();
      if (new URL(url).origin === origin) await route.continue();
      else {
        record.blocked.push(url);
        await route.abort('blockedbyclient');
      }
    });
    const page = await context.newPage();
    page.setDefaultTimeout(30000);
    const cdp = await context.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    page.on('request', req => {
      pending.add(req);
      lastEvent = performance.now();
      record.browserHttp.push({ event: 'request', url: req.url(), method: req.method(), type: req.resourceType() });
    });
    page.on('response', res => {
      const status = res.status();
      record.browserHttp.push({ event: 'response', url: res.url(), status });
      // FileLoader can reject an HTTP error before consuming its response.
      // Preserve that distinction without waiting for a successful body read.
      if (status >= 400) {
        pending.delete(res.request());
        rejectedResponses.set(res.request(), { url: res.url(), status });
        lastEvent = performance.now();
      }
    });
    page.on('requestfinished', req => {
      record.browserHttp.push({ event: 'finish', url: req.url() });
      pending.delete(req);
      rejectedResponses.delete(req);
      lastEvent = performance.now();
    });
    page.on('requestfailed', req => {
      pending.delete(req);
      rejectedResponses.delete(req);
      lastEvent = performance.now();
      record.browserHttp.push({ event: 'failure', url: req.url(), error: req.failure()?.errorText });
    });
    page.on('console', msg => {
      if (['warning', 'error'].includes(msg.type())) record.console.push({ type: msg.type(), text: msg.text() });
    });
    page.on('pageerror', error => record.pageErrors.push(error.message));
    page.on('worker', worker => record.workers.push(worker.url()));
    try {
      await page.goto(origin, { waitUntil: 'load' });
      await page.waitForFunction(() => typeof window.afRun === 'function');
      const evaluation = spec.id === 'offline-probe' ? page.evaluate(() => window.afProbe()) :
        page.evaluate(config => window.afRun(config), spec);
      const time = setTimeout(() => { void context.close(); }, 65000).unref();
      try { record.outcome = await evaluation; }
      finally { clearTimeout(time); }
      for (let tries = 0; tries < 60 && (pending.size || performance.now() - lastEvent < 250); tries++) {
        await delay(100);
      }
      record.outstandingRequests = [...pending].map(req => req.url());
      record.non2xxWithoutFinish = [...rejectedResponses.values()];
      if (record.outcome.png) {
        const png = Buffer.from(record.outcome.png.split(',')[1], 'base64');
        const path = `frames/${spec.id}.png`;
        await writeFile(join(output, path), png);
        record.outcome.frame.png = { path, bytes: png.length, sha256: sha256(png) };
        delete record.outcome.png;
      }
      const tail = record.outcome.harnessError;
      if (tail || record.outstandingRequests.length || record.pageErrors.length) unexpected = true;
      if (spec.id === 'offline-probe') {
        assert.equal(record.outcome.absent.status, 404);
        assert.equal(record.blocked.length, 1);
      }
    } catch (error) {
      record.executionError = error.stack ?? String(error);
      unexpected = true;
    } finally {
      record.serverHttp = serverEvents.get(spec.id) ?? [];
      record.finished_utc = new Date().toISOString();
      await context.close().catch(() => {});
      await writeFile(join(output, spec.id + '.json'), JSON.stringify(record, null, 2) + '\n');
      const count = record.serverHttp.filter(event => event.category === 'model').length;
      console.log([spec.id, record.outcome?.load ?? (spec.id === 'offline-probe' ? 'probe' : 'unknown'),
        `modelHTTP=${count}`, `draw=${record.outcome?.draw?.calls ?? '-'}`,
        `px=${record.outcome?.frame?.foreground ?? '-'}`,
        record.executionError ?? record.outcome?.error ?? record.outcome?.harnessError ?? ''].join('\t'));
    }
  }
  await writeFile(join(output, 'environment.json'), JSON.stringify({
    ...environment, finished_utc: new Date().toISOString(), cases: specs.map(spec => spec.id),
  }, null, 2) + '\n');
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
}
if (unexpected) process.exitCode = 1;
