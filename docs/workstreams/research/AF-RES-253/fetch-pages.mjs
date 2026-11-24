import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const inputs = JSON.parse(await readFile(new URL('inputs.json', import.meta.url), 'utf8'));
if (process.argv.length !== 4) {
  throw new Error('Usage: node fetch-pages.mjs CACHE_DIR RECEIPTS_DIR');
}
const cache = resolve(process.argv[2]);
const receipts = resolve(process.argv[3]);
await Promise.all([mkdir(cache, { recursive: true }), mkdir(receipts, { recursive: true })]);

const headerNames = new Set([
  'content-type', 'content-encoding', 'location', 'last-modified',
  'etag', 'date', 'content-length', 'vary'
]);

function selectedHeaders(rawHeaders) {
  return rawHeaders.trim().split(/\r?\n\r?\n/).filter(Boolean).map(block => {
    const [statusLine, ...lines] = block.split(/\r?\n/);
    const headers = {};
    for (const line of lines) {
      const colon = line.indexOf(':');
      const key = line.slice(0, colon).toLowerCase();
      if (headerNames.has(key)) {
        (headers[key] ??= []).push(line.slice(colon + 1).trim());
      }
    }
    return { statusLine, headers };
  });
}

async function receive(source) {
  const bodyPath = join(cache, source.id + '.html');
  const headersPath = join(cache, source.id + '.headers.tmp');
  await Promise.all([rm(bodyPath, { force: true }), rm(headersPath, { force: true })]);
  const curlArgs = [
    '--silent', '--show-error', '--location', '--max-redirs', '5',
    '--connect-timeout', '12', '--max-time', '45',
    '--user-agent', 'AF-RES-253/1.0 (public documents)',
    '--header', 'Accept: text/html,application/xhtml+xml',
    '--header', 'Accept-Encoding: identity',
    '--dump-header', headersPath, '--output', bodyPath,
    '--write-out', '%{json}', source.url
  ];
  const startedAt = new Date().toISOString();
  let result;
  let exitCode = 0;
  try {
    result = await exec('curl', curlArgs);
  } catch (error) {
    result = error;
    exitCode = error.code;
  }
  const finishedAt = new Date().toISOString();
  const body = await readFile(bodyPath).catch(error => {
    if (error.code === 'ENOENT') return null;
    throw error;
  });
  const headers = await readFile(headersPath, 'utf8').catch(error => {
    if (error.code === 'ENOENT') return '';
    throw error;
  });
  const details = result.stdout ? JSON.parse(result.stdout) : {};
  const receipt = {
    id: source.id, request: source.url, startedAt, finishedAt, exitCode,
    command: ['curl', ...curlArgs.map(arg => arg.replace(cache, '<CACHE>'))],
    status: details.http_code ?? null, finalUrl: details.url_effective ?? null,
    redirects: details.num_redirects ?? null, contentType: details.content_type ?? null,
    wireDownloadBytes: details.size_download ?? null,
    bytes: body?.length ?? null,
    sha256: body ? createHash('sha256').update(body).digest('hex') : null,
    responseHeaders: selectedHeaders(headers)
  };
  await Promise.all([
    writeFile(join(receipts, source.id + '.http.json'), JSON.stringify(receipt, null, 2) + '\n'),
    writeFile(join(receipts, source.id + '.curl.stderr'), result.stderr ?? '')
  ]);
  console.log(JSON.stringify({ ...receipt, command: undefined, responseHeaders: undefined }));
  return exitCode === 0 && receipt.status === 200 &&
    /^(text\/html|application\/xhtml\+xml)\b/i.test(receipt.contentType ?? '') &&
    Boolean(receipt.bytes);
}

const received = await Promise.all([...inputs.pages, ...inputs.rfc].map(receive));
if (received.some(success => !success)) process.exitCode = 1;
