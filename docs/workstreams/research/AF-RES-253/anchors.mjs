import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const headingPattern = /^h[1-6]$/;
const inlineHeadingPattern = /(?:^|\s)h[1-6](?:\s|$)/;
const htmlContentType = /^(text\/html|application\/xhtml\+xml)\b/i;
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const clean = text => text.replace(/\s+/g, ' ').trim();

function* elements(node) {
  if (node.tagName) yield node;
  for (const child of node.childNodes ?? []) yield* elements(child);
}

function text(node) {
  if (!node) return '';
  if (node.nodeName === '#text') return node.value;
  return (node.childNodes ?? []).map(text).join('');
}

function attr(node, key) {
  return node.attrs?.find(attribute => attribute.name === key)?.value ?? null;
}

function isHeading(node) {
  return headingPattern.test(node.tagName) || inlineHeadingPattern.test(attr(node, 'class') ?? '');
}

function parentChain(node) {
  const result = [];
  while (node?.tagName) {
    result.push(node);
    node = node.parentNode;
  }
  return result;
}

function summarizeHeading(node) {
  return node ? {
    tag: node.tagName, text: clean(text(node)).slice(0, 240),
    line: node.sourceCodeLocation?.startLine ?? null,
  } : null;
}

function parseFragment(parse5, bytes, contentType, fragment) {
  const charset = contentType.match(/charset\s*=\s*"?([\w-]+)/i)?.[1] ?? 'utf-8';
  const tree = parse5.parse(new TextDecoder(charset).decode(bytes), { sourceCodeLocationInfo: true });
  const all = [...elements(tree)];
  const matches = all.flatMap((node, index) => {
    const id = attr(node, 'id'), name = attr(node, 'name');
    if (id !== fragment && name !== fragment) return [];
    const ancestry = parentChain(node);
    const section = ancestry.find(item =>
      item.tagName === 'section' || (attr(item, 'class') ?? '').split(/\s+/).includes('sc'));
    const heading = ancestry.find(isHeading) ??
      (section ? [...elements(section)].find(isHeading) : null);
    const previousHeading = all.slice(0, index).findLast(isHeading);
    const nextHeading = all.slice(index + 1).find(isHeading);
    const sectionBody = clean(text(section));
    return [{
      tag: node.tagName, id, name, legacyName: node.tagName === 'a' && name === fragment,
      className: attr(node, 'class'), line: node.sourceCodeLocation?.startLine ?? null,
      parent: { tag: node.parentNode?.tagName ?? null, id: attr(node.parentNode, 'id') },
      section: section ? {
        tag: section.tagName, id: attr(section, 'id'), heading: summarizeHeading(heading),
        bodyTextSha256: sha(sectionBody), bodyTextLength: sectionBody.length,
      } : null,
      heading: summarizeHeading(heading),
      previousHeading: summarizeHeading(previousHeading), nextHeading: summarizeHeading(nextHeading),
    }];
  });
  const idMatches = matches.filter(node => node.id === fragment);
  const legacyMatches = matches.filter(node => node.legacyName);
  const chosen = idMatches[0] ?? legacyMatches[0] ?? null;
  return {
    charset, matches, distinctMatchCount: matches.length, idCount: idMatches.length,
    legacyNameCount: legacyMatches.length, otherNameCount: matches.filter(node => node.name === fragment && !node.legacyName).length,
    eligibleCount: matches.filter(node => node.id === fragment || node.legacyName).length,
    predictedTarget: chosen,
    targetKind: idMatches.length ? 'id' : legacyMatches.length ? 'legacy-name' : 'not-found',
  };
}

async function readResponse(receipts, cache, page) {
  const report = JSON.parse(await readFile(join(receipts, page.id + '.http.json'), 'utf8'));
  if (report.exitCode !== 0 || report.status !== 200 || !htmlContentType.test(report.contentType ?? '')) {
    return { report, blocked: 'HTTP 원바이트 수신 단계' };
  }
  const encodings = report.responseHeaders.at(-1)?.headers?.['content-encoding'] ?? [];
  if (encodings.some(encoding => encoding.toLowerCase() !== 'identity')) {
    return { report, blocked: 'identity 요청과 다른 Content-Encoding, 캐시 표현 확인 필요' };
  }
  const bytes = await readFile(join(cache, page.id + '.html'));
  assert.equal(sha(bytes), report.sha256, 'Raw HTML vs receipt fingerprint mismatch for ' + page.id);
  return { report, bytes };
}

async function browserLocation(page, fragment) {
  return page.evaluate(async id => {
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const headingQuery = 'h1,h2,h3,h4,h5,h6,.h1,.h2,.h3,.h4,.h5,.h6';
    const brief = value => value?.replace(/\s+/g, ' ').trim().slice(0, 240) ?? null;
    const summarize = element => element ? {
      tag: element.localName, id: element.getAttribute('id'), name: element.getAttribute('name'),
    } : null;
    const target = document.querySelector(':target');
    const section = target?.closest('section,.sc');
    const heading = target?.closest(headingQuery) ?? section?.querySelector(headingQuery);
    const rect = target?.getBoundingClientRect();
    return {
      href: location.href, hash: location.hash, title: document.title, contentType: document.contentType,
      match: summarize(target), matchingIds: Array.from(document.querySelectorAll('[id]'))
        .filter(element => element.id === id).map(summarize),
      matchingNames: Array.from(document.getElementsByName(id)).map(summarize),
      section: summarize(section), heading: brief(heading?.textContent), scrollX, scrollY,
      viewport: { width: innerWidth, height: innerHeight },
      targetRect: rect ? { x: rect.x, y: rect.y, width: rect.width, height: rect.height } : null,
      sectionText: section?.textContent?.replace(/\s+/g, ' ').trim() ?? null,
    };
  }, fragment);
}

async function openBrowser(browser, contextOptions, url, fragment, localBody) {
  const context = await browser.newContext(contextOptions);
  try {
    if (localBody) {
      const expectedUrl = new URL(url);
      await context.route('**/*', route => {
        const requested = new URL(route.request().url());
        requested.hash = '';
        if (requested.href === expectedUrl.href && route.request().isNavigationRequest()) {
          return route.fulfill({ status: 200, contentType: localBody.contentType, body: localBody.bytes });
        }
        return route.abort();
      });
    }
    const page = await context.newPage();
    const response = await page.goto(url + '#' + fragment, { waitUntil: 'load', timeout: 12000 });
    const contentType = response?.headers()['content-type'] ?? null;
    const http = {
      status: response?.status() ?? null, contentType, responseUrl: response?.url() ?? null,
      requestChain: [],
    };
    for (let request = response?.request(); request; request = request.redirectedFrom()) {
      http.requestChain.unshift(request.url());
    }
    if (http.status !== 200 || !htmlContentType.test(contentType ?? '')) {
      return { loadStatus: 'non-html-or-http-error', http, finalUrl: page.url() };
    }
    const bytes = await response.body();
    const { sectionText, ...location } = await browserLocation(page, fragment);
    return {
      loadStatus: 'observed-html', http, documentBytes: bytes.length, documentSha256: sha(bytes),
      ...location, sectionTextSha256: sectionText === null ? null : sha(sectionText),
    };
  } catch (error) {
    return { loadStatus: 'unobserved', error: String(error) };
  } finally {
    await context.close();
  }
}

async function save(out, key, receipt) {
  await writeFile(join(out, key + '.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify({
    key, parser: receipt.parser?.targetKind ?? null, live: receipt.live?.loadStatus ?? null,
    replay: receipt.sameBytesBrowser?.loadStatus ?? null, blocked: receipt.blocked ?? null,
  }));
}

export async function observeAnchors({ browser, parse5, inputs, out, cacheDir, httpDir, contextOptions }) {
  let success = true;
  for (const source of [...inputs.pages, ...inputs.rfc]) {
    const { report, bytes, blocked } = await readResponse(httpDir, cacheDir, source);
    for (const target of source.targets) {
      const { fragment } = target;
      const startedAt = new Date().toISOString();
      const live = await openBrowser(browser, contextOptions, source.url, fragment);
      const parser = bytes ? parseFragment(parse5, bytes, report.contentType, fragment) : null;
      const sameBytesBrowser = bytes ? await openBrowser(browser, contextOptions, report.finalUrl, fragment, {
        bytes, contentType: report.contentType,
      }) : null;
      const blockedSteps = [
        ...(blocked ? [blocked] : []),
        ...(live.loadStatus !== 'observed-html' ? ['Chromium 대상 URL 탐색'] : []),
        ...(sameBytesBrowser?.loadStatus === 'unobserved' ? ['동일 바이트 Chromium 대조'] : []),
      ];
      const observed = Boolean(bytes && live.loadStatus === 'observed-html' &&
        sameBytesBrowser?.loadStatus === 'observed-html');
      await save(out, source.id + '--' + fragment, {
        source, target, startedAt, finishedAt: new Date().toISOString(), observed,
        httpReceipt: source.id + '.http.json', originSha256: report.sha256,
        originBytesAgreeWithLive: live.documentSha256 && report.sha256 ? live.documentSha256 === report.sha256 : null,
        originBytesAgreeWithReplay: sameBytesBrowser?.documentSha256 && report.sha256
          ? sameBytesBrowser.documentSha256 === report.sha256 : null,
        parser, live, sameBytesBrowser, blocked: blockedSteps,
      });
      success = success && observed;
    }
  }
  return success;
}

export async function observeAnchorControls({ browser, parse5, root, out, cacheDir, contextOptions }) {
  const synthetic = {
    id: 'fixture', path: join(root, 'fixtures/anchor-controls.html'), provenance: 'local fixture',
    fragments: ['legacy', 'duplicate', 'priority', 'missing', 'other-name'],
  };
  const cases = [synthetic];
  if (cacheDir) {
    for (const fragment of ['parsing', 'non-text-content']) {
      cases.push({
        id: 'W22-authoring-' + fragment, path: join(cacheDir, fragment + '.html'),
        provenance: 'w3c/wcag tag WCAG22-20231005 commit 732353ba0ce6193afc262d432d5dfba50c0eff59',
        fragments: [fragment],
      });
    }
  }
  let success = true;
  for (const input of cases) {
    const bytes = await readFile(input.path);
    const contentType = 'text/html; charset=utf-8';
    for (const fragment of input.fragments) {
      const parser = parseFragment(parse5, bytes, contentType, fragment);
      const sameBytesBrowser = await openBrowser(browser, contextOptions,
        'https://af-res-253.test/' + input.id, fragment, { bytes, contentType });
      const observed = sameBytesBrowser.loadStatus === 'observed-html' && sha(bytes) === sameBytesBrowser.documentSha256;
      success = observed && success;
      await save(out, input.id + '--' + fragment, {
        provenance: input.provenance, artifactSha256: sha(bytes), fragment,
        parser, sameBytesBrowser, observed,
      });
    }
  }
  return success;
}
