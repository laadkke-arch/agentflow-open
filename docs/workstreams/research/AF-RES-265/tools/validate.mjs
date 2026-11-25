/* Khronos glTF Validator diagnostic. No browser or decoder is implied. */
import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

assert(process.argv[2], 'usage: node validate.mjs <prepared dir>');
const root = resolve(process.argv[2]);
const require = createRequire(join(root, 'npm', 'package.json'));
const validator = require('gltf-validator');
const cases = JSON.parse(await readFile(join(root, 'cases.json'), 'utf8'));
const ids = ['Box-G', 'BoxTextured-G', 'Lamp-G', 'Lamp-R', 'ktx-on',
  'unused-present', 'external-present', 'external-absent', 'fallback-on'];
const results = [];
for (const id of ids) {
  const cfg = cases.find(c => c.id === id);
  const calls = [];
  const input = await readFile(join(root, cfg.paths[cfg.entry]));
  const entryPath = cfg.paths[cfg.entry];
  const report = await validator.validateBytes(new Uint8Array(input), {
    uri: cfg.entry,
    maxIssues: 100,
    externalResourceFunction: async relative => {
      const path = decodeURIComponent(relative);
      if (!Object.hasOwn(cfg.paths, path)) {
        calls.push({ relative, result: 'unserved' });
        throw new Error('File excluded from this test: ' + relative);
      }
      const bytes = await readFile(join(root, cfg.paths[path]));
      calls.push({ relative, bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex') });
      return new Uint8Array(bytes);
    },
  });
  results.push({ id, entryPath, entrySha256: cfg.sha256, calls, report });
  const { numErrors, numWarnings, numInfos, numHints } = report.issues;
  console.log(`${id}\tE=${numErrors} W=${numWarnings} I=${numInfos} H=${numHints}\treads=${calls.length}`);
}
await writeFile(join(root, 'validator.json'), JSON.stringify({
  version: validator.version(), finished_utc: new Date().toISOString(), results,
}, null, 2) + '\n');
