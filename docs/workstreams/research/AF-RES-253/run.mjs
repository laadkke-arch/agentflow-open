import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createReadStream } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { arch, platform, release } from 'node:os';
import { fileURLToPath } from 'node:url';
import { observeAnchors, observeAnchorControls } from './anchors.mjs';

const root = dirname(fileURLToPath(import.meta.url));
const inputs = JSON.parse(await readFile(join(root, 'inputs.json')));
const [suite, outputDir, cacheDir, httpDir] = process.argv.slice(2);
const suites = ['main', 'default', 'aria-controls', 'anchors', 'anchor-controls'];
if (!suites.includes(suite) || !outputDir || (suite === 'anchors' && !(cacheDir && httpDir))) {
  throw new Error('Usage: node run.mjs main|default|aria-controls|anchors|anchor-controls OUT [CACHE HTTP_RECEIPTS]');
}

const deps = resolve(process.env.AF253_DEPS ?? join(root, 'deps'));
const requireDep = createRequire(join(deps, 'package.json'));
const { chromium } = requireDep('playwright-core');
const parse5 = requireDep('parse5');
const browserPath = process.env.AF253_CHROMIUM ?? '/usr/bin/chromium';
const out = resolve(outputDir);
const viewport = { width: 1280, height: 800 };
const contextOptions = {
  viewport, locale: 'en-US', timezoneId: 'UTC', serviceWorkers: 'block',
};
const buckets = ['violations', 'incomplete', 'passes', 'inapplicable'];
const proxy = process.env.HTTPS_PROXY ?? process.env.https_proxy;
const usesProxy = suite === 'anchors' && Boolean(proxy);
const launchOptions = { executablePath: browserPath, headless: true };
if (usesProxy) {
  const proxyUrl = new URL(proxy);
  launchOptions.proxy = { server: proxyUrl.origin };
  if (proxyUrl.username) launchOptions.proxy.username = decodeURIComponent(proxyUrl.username);
  if (proxyUrl.password) launchOptions.proxy.password = decodeURIComponent(proxyUrl.password);
}

const sha = bytes => createHash('sha256').update(bytes).digest('hex');
async function fileSha(path) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(path)) hash.update(chunk);
  return hash.digest('hex');
}

async function json(name, value, compact = false) {
  await writeFile(join(out, name), JSON.stringify(value, null, compact ? undefined : 2) + '\n');
}

function pathFingerprint(path) {
  return fileSha(path).then(sha256 => ({ path, sha256 }));
}

async function environment(browser) {
  const cdp = await browser.newBrowserCDPSession();
  const devTools = await cdp.send('Browser.getVersion');
  await cdp.detach();
  const driver = requireDep('playwright-core/package.json');
  const driverPath = requireDep.resolve('playwright-core');
  const driverChromiumPath = join(dirname(driverPath), 'lib/server/chromium/chromium.js');
  const chromeBinary = process.env.AF253_CHROMIUM_BINARY ??
    (browserPath === '/usr/bin/chromium' ? '/usr/lib/chromium/chromium' : browserPath);
  return {
    suite,
    node: process.version,
    os: { platform: platform(), release: release(), arch: arch() },
    chromium: {
      version: browser.version(), devTools,
      entryPoint: await pathFingerprint(browserPath),
      binary: await pathFingerprint(chromeBinary),
      headless: true,
      profile: 'Playwright-assigned temporary profile per launch',
    },
    driver: {
      name: driver.name,
      version: driver.version,
      entrySha256: await fileSha(driverPath),
      chromiumDriverSha256: await fileSha(driverChromiumPath),
    },
    parse5: JSON.parse(await readFile(join(deps, 'node_modules/parse5/package.json'))).version,
    contextOptions,
    browserUsesInheritedHttpsProxy: usesProxy,
    inputSha256: sha(await readFile(join(root, 'inputs.json'))),
  };
}

async function accessibility(context, page) {
  const dom = await page.evaluate(() => {
    const button = document.querySelector('button');
    const idref = button.getAttribute('aria-labelledby');
    const describe = node => node && ({ id: node.id, text: node.textContent });
    return {
      idref, writtenButtonText: button.textContent,
      matchingSpans: Array.from(document.querySelectorAll('span')).map(describe),
      firstDomMatch: describe(document.getElementById(idref)),
      reflectedElements: button.ariaLabelledByElements?.map(describe) ?? null,
    };
  });
  const cdp = await context.newCDPSession(page);
  try {
    const { root } = await cdp.send('DOM.getDocument');
    const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: 'button' });
    const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: root.nodeId, selector: 'span' });
    const spanBackendIds = [];
    for (const spanId of nodeIds) {
      const { node } = await cdp.send('DOM.describeNode', { nodeId: spanId });
      spanBackendIds.push(node.backendNodeId);
    }
    const { nodes } = await cdp.send('Accessibility.getPartialAXTree', { nodeId, fetchRelatives: false });
    const axButton = nodes.find(node => node.role?.value === 'button' && !node.ignored);
    assert.ok(axButton?.name, 'No computed AX name for the button');
    return {
      ...dom, spanBackendIds, axNodes: nodes,
      axName: axButton.name.value,
      relatedBackendIds: axButton.name.sources.flatMap(source =>
        (source.attributeValue?.relatedNodes ?? []).map(node => node.backendDOMNodeId)),
    };
  } finally {
    await cdp.detach();
  }
}

function requestedCases() {
  const variants = suite === 'aria-controls'
    ? [
      ['aria', 'aria.html'],
      ['aria-reversed', 'aria-reversed.html'],
      ['aria-unique', 'aria-unique.html'],
    ]
    : inputs.fixtures.map(name => [name, name + '.html']);
  const modes = suite === 'default' ? ['default'] : Object.keys(inputs.modes);
  return { variants, modes };
}

async function runAudit(browser, version, js, binary, fixture, fixtureFile, mode) {
  const key = [version, fixture, mode].join('--');
  const options = inputs.modes[mode];
  const html = await readFile(join(root, 'fixtures', fixtureFile), 'utf8');
  const receipt = {
    key, version, fixture, mode, options, context: 'document',
    fixturePath: 'fixtures/' + fixtureFile, inputSha256: sha(html), axeSha256: binary.axeSha256,
    startedAt: new Date().toISOString(), console: [],
  };
  const context = await browser.newContext(contextOptions);
  const page = await context.newPage();
  page.on('console', msg => receipt.console.push({ type: msg.type(), text: msg.text() }));
  page.on('pageerror', error => receipt.console.push({ type: 'pageerror', text: error.message }));
  try {
    await page.setContent(html, { waitUntil: 'load' });
    receipt.domBefore = await page.content();
    receipt.location = page.url();
    if (suite === 'aria-controls') {
      receipt.accessibility = await accessibility(context, page);
    }
    await page.addScriptTag({ content: js });
    receipt.runtimeAxeVersion = await page.evaluate(() => window.axe.version);
    assert.equal(receipt.runtimeAxeVersion, version);
    receipt.ruleInventory = await page.evaluate(ids =>
      window.axe.getRules().filter(rule => ids.includes(rule.ruleId)), inputs.ruleIds);
    const data = await page.evaluate(opts => window.axe.run(document, opts), options);
    await json(key + '.json', data, true);
    assert.equal(data.testEngine.version, version);
    receipt.counts = Object.fromEntries(buckets.map(kind => [kind, data[kind].length]));
    receipt.status = 'observed';
  } catch (error) {
    receipt.status = 'unobserved';
    receipt.error = String(error);
  } finally {
    await context.close();
  }
  receipt.finishedAt = new Date().toISOString();
  await json(key + '.case.json', receipt);
  console.log(JSON.stringify({
    key, status: receipt.status, runtimeAxeVersion: receipt.runtimeAxeVersion,
    counts: receipt.counts, error: receipt.error,
  }));
  return receipt.status === 'observed';
}

async function observeAxe(browser) {
  const { variants, modes } = requestedCases();
  const metadataPath = process.env.AF253_BUILD_RECEIPT ?? join(root, 'receipts/builds/builds.json');
  const binaries = JSON.parse(await readFile(metadataPath));
  let success = true;
  for (const build of inputs.builds) {
    const { version, gitHead } = build;
    const binary = binaries.find(record => record.version === version);
    assert.ok(binary && binary.installedBytesEqual);
    assert.equal(binary.gitHead, gitHead);
    const js = await readFile(join(deps, 'node_modules', binary.axeFile), 'utf8');
    assert.equal(sha(js), binary.axeSha256, 'axe JS file fingerprint mismatch');
    for (const [fixture, fixtureFile] of variants) {
      for (const mode of modes) {
        const observed = await runAudit(browser, version, js, binary, fixture, fixtureFile, mode);
        success = observed && success;
      }
    }
  }
  return success;
}

await mkdir(out, { recursive: true });
const browser = await chromium.launch(launchOptions);
try {
  await json('environment.json', await environment(browser));
  let success;
  if (suite === 'anchors') {
    success = await observeAnchors({ browser, parse5, inputs, root, out, cacheDir, httpDir, contextOptions });
  } else if (suite === 'anchor-controls') {
    success = await observeAnchorControls({ browser, parse5, root, out, cacheDir, contextOptions });
  } else {
    success = await observeAxe(browser);
  }
  if (!success) process.exitCode = 1;
} finally {
  await browser.close();
}
