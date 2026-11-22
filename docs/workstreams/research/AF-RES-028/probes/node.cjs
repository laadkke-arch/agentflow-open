'use strict';

const { once } = require('events');
const { exec, spawnSync } = require('child_process');
const fs = require('fs');
const pathModule = require('path');

async function errorOr(fn, value = 'resolved') {
  try {
    await fn();
    return value;
  } catch (error) {
    return error.code || error.name;
  }
}

async function cluster() {
  const api = require('cluster');
  if (!api.isPrimary) {
    process.once('disconnect', () => process.exit(0));
    return;
  }
  const worker = api.fork();
  const closed = once(worker, 'exit');
  await once(worker, 'online');
  const positive = worker.isConnected();
  const ended = once(worker, 'disconnect');
  worker.disconnect();
  await ended;
  const boundary = worker.isConnected();
  await closed;
  return { positive, boundary };
}

async function webcrypto() {
  const { subtle } = require('crypto').webcrypto;
  const ed = Buffer.from('302a300506032b6570032100d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a', 'hex');
  const ec = Buffer.from(
    '3059301306072a8648ce3d020106082a8648ce3d03010703420004' +
    '6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296' +
    '4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5', 'hex');
  async function imp(key, algorithm) {
    try {
      const imported = await subtle.importKey('spki', key, algorithm, true, ['verify']);
      return { result: imported.type === 'public' && imported.usages.includes('verify') ? 'imported' : 'wrong-key',
               algorithm: imported.algorithm };
    } catch (error) {
      return { result: error.name, message: error.message };
    }
  }
  const literal = await imp(ed, { name: 'ECDSA', namedCurve: 'NODE-ED25519' });
  const boundary = await imp(ec, { name: 'ECDSA', namedCurve: 'P-256' });
  const proprietary = await imp(ed, { name: 'NODE-ED25519', namedCurve: 'NODE-ED25519' });
  const standard = await imp(ed, { name: 'Ed25519' });
  return { positive: literal.result, boundary: boundary.result, diagnostic: { literal, boundary, proprietary, standard } };
}

async function response(http2) {
  const api = require(http2 ? 'http2' : 'http');
  const before = [];
  let finished;
  const server = api.createServer((req, res) => {
    before.push(res.finished);
    res.write('o');
    before.push(res.finished);
    res.end('k');
    finished = res.finished;
  });
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const origin = 'http://127.0.0.1:' + server.address().port;
  let body = '';
  let session;
  try {
    const stream = http2
      ? (session = api.connect(origin)).request({ ':path': '/' })
      : (await once(api.get(origin), 'response'))[0];
    await new Promise((resolve, reject) => {
      stream.setEncoding('utf8');
      stream.on('data', (chunk) => { body += chunk; });
      stream.on('end', resolve);
      stream.on('error', reject);
    });
  } finally {
    if (session) session.close();
    await new Promise((resolve) => server.close(resolve));
  }
  return { positive: { finished, body }, boundary: before };
}

function tty() {
  const stream = process.stdin;
  if (!stream.isTTY || typeof stream.setRawMode !== 'function') {
    return { blocked: 'stdin is not a POSIX TTY' };
  }
  const base = stream.isRaw;
  stream.setRawMode(true);
  const active = stream.isRaw;
  stream.setRawMode(false);
  return { positive: active, boundary: [base, stream.isRaw] };
}

async function child() {
  const positive = await new Promise((resolve, reject) => {
    exec('pwd -P', { cwd: new URL('file:///tmp/') }, (error, out) => {
      if (error) reject(error);
      else resolve(out.trim());
    });
  });
  const boundary = await errorOr(() => new Promise((resolve, reject) => {
    exec('pwd -P', { cwd: new URL('https://fixture.invalid/') },
         (error) => error ? reject(error) : resolve());
  }));
  return { positive, boundary };
}

function wasi() {
  const { WASI } = require('wasi');
  function run(version, hasStart) {
    try {
      const options = { args: ['/af028'], env: { AF028: 'yes' } };
      if (version !== undefined) options.version = version;
      const host = new WASI(options);
      const name = hasStart ? '5f7374617274' : '5f6f74686572';
      const hex = '0061736d010000000104016000000302010005030100010606017f0141000b' +
                  '071a03066d656d6f7279020006' + name + '000004666c616703000a08010600410124000b';
      const module = new WebAssembly.Module(Buffer.from(hex, 'hex'));
      const instance = new WebAssembly.Instance(module, { wasi_snapshot_preview1: host.wasiImport });
      const before = instance.exports.flag.value;
      host.start(instance);
      return { before, after: instance.exports.flag.value };
    } catch (error) {
      return { code: error.code || error.name, message: error.message };
    }
  }
  const positive = run(undefined, true);
  const negative = run(undefined, false);
  return { positive, boundary: negative.code ? 'throws' : negative,
           diagnostic: { negative, explicit_preview1: run('preview1', true) } };
}

function domain() {
  const owner = require('domain').create();
  let received;
  const args = [];
  owner.on('error', (err) => { received = err; });
  const wrapped = owner.intercept((...values) => args.push(values));
  const error = new Error('af028 fixture');
  wrapped(error);
  const positive = { same_error: received === error, callback_count: args.length };
  wrapped(null, 'ok');
  return { positive, boundary: args[0] };
}

function path() {
  const positive = pathModule.format({ root: '/', name: 'file', ext: '.txt' });
  const boundary = pathModule.format({ root: '/', name: 'file', ext: '.txt', base: 'literal' });
  return { positive, boundary, diagnostic: { bare_extension: pathModule.format({ root: '/', name: 'file', ext: 'txt' }) } };
}

async function https() {
  const api = require('https');
  const tls = require('tls');
  const key = fs.readFileSync(pathModule.join(process.env.AF028_FIXTURES, 'agent1-key.pem'));
  const cert = fs.readFileSync(pathModule.join(process.env.AF028_FIXTURES, 'agent1-cert.pem'));
  async function idle(delay) {
    const server = api.createServer({ key, cert });
    let fired = false;
    server.on('timeout', () => { fired = true; });
    if (delay !== null) server.setTimeout(delay);
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    const client = tls.connect({ host: '127.0.0.1', port: server.address().port, rejectUnauthorized: false });
    try {
      await once(client, 'secureConnect');
      await new Promise((resolve) => setTimeout(resolve, 140));
      return { timeout: server.timeout, fired };
    } finally {
      client.destroy();
      await new Promise((resolve) => server.close(resolve));
    }
  }
  return { positive: await idle(null), boundary: await idle(30) };
}

function diagnostics() {
  const channel = require('diagnostics_channel').channel('af028-fixture');
  const messages = [];
  const handler = (value) => { messages.push(value); };
  channel.subscribe(handler);
  channel.publish('first');
  const returned = channel.unsubscribe(handler);
  channel.publish('second');
  return { positive: { returned, messages }, boundary: channel.unsubscribe(handler) };
}

function histogram() {
  const h = require('perf_hooks').createHistogram();
  for (const value of [1, 2, 2]) h.record(value);
  const map = h.percentiles;
  const positive = { map: map instanceof Map, min: map.get(0), max: map.get(100) };
  const mapBrand = require("util").types.isMap(map);
  const viaMapGet = Map.prototype.get.call(map, 100);
  h.reset();
  h.record(5);
  return { positive, boundary: [h.percentiles.get(0), h.percentiles.get(100)],
           diagnostic: { mapBrand, viaMapGet } };
}

async function crypto() {
  const { createCipheriv } = require('crypto');
  const algorithm = 'aes-128-cbc';
  const iv = Buffer.alloc(16);
  const positive = await errorOr(() => createCipheriv(algorithm, Buffer.alloc(15), iv));
  const cipher = createCipheriv(algorithm, Buffer.alloc(16), iv);
  const out = Buffer.concat([cipher.update('fixture'), cipher.final()]);
  return { positive, boundary: out.length === 16 };
}

async function assert() {
  const api = require('assert');
  return { positive: await errorOr(() => api.doesNotReject(Promise.resolve('yes'))),
           boundary: await errorOr(() => api.doesNotReject(Promise.reject(new Error('fixture')))) };
}

function decoder() {
  const { StringDecoder } = require('string_decoder');
  const first = new StringDecoder('utf8');
  const positive = [first.write(Buffer.from([0xe2])), first.end(), first.write(Buffer.from('A'))];
  const second = new StringDecoder('utf8');
  return { positive, boundary: [second.write(Buffer.from([0xe2])), second.end(Buffer.from([0x82, 0xac]))] };
}

function consoleTest() {
  function streams(code) {
    const cp = spawnSync(process.execPath, ['-e', code], { encoding: 'utf8', timeout: 4000 });
    if (cp.status !== 0) throw Error(cp.stderr || cp.error);
    return { stdout: cp.stdout.trim().split('\n').filter(Boolean), stderr: cp.stderr.trim().split('\n').filter(Boolean) };
  }
  return { positive: streams('console.debug("marker"); console.log("marker")'),
           boundary: streams('console.error("marker")') };
}

function mainmodule() {
  const value = spawnSync(process.execPath, ['-e', 'process.stdout.write(typeof process.mainModule)'],
                          { encoding: 'utf8', timeout: 4000 });
  return { positive: { same: process.mainModule === require.main,
                       entry: process.mainModule?.filename === __filename },
           boundary: value.stdout };
}

const probes = {
  assert, child, cluster, console: consoleTest, crypto, decoder, diagnostics, domain,
  h2: () => response(true), histogram, http: () => response(false), https,
  mainmodule, path, tty, wasi, webcrypto,
};
Promise.resolve().then(() => probes[process.argv[2]]()).then((result) => {
  if (result !== undefined) process.stdout.write('AF028_JSON ' + JSON.stringify(result) + '\n');
}).catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
