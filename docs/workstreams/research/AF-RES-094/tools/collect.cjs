const { createHash } = require('node:crypto');
const { execFile } = require('node:child_process');
const fs = require('node:fs/promises');
const path = require('node:path');
const { promisify } = require('node:util');

const run = promisify(execFile);
const chromium = require('./chromium.cjs');
const [mode, output, cache] = process.argv.slice(2);
if (!['preflight', 'main'].includes(mode) || !output || !cache) {
  throw new Error('usage: collect.cjs preflight|main NEW_EVIDENCE_DIR NEW_TEMP_BODY_DIR');
}

const root = path.dirname(__dirname);
const now = () => new Date().toISOString();
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const visibleHeaders = new Set([
  'date', 'content-type', 'content-encoding', 'content-length', 'location',
  'last-modified', 'etag', 'cache-control', 'age', 'server', 'via',
]);

function publicHeaders(headers) {
  return Object.fromEntries(Object.entries(headers).filter(([key]) => visibleHeaders.has(key)));
}

function parts(input) {
  return input.trim().split(/\r?\n\r?\n/).flatMap((block) => {
    const [statusLine, ...rest] = block.split(/\r?\n/);
    if (!statusLine?.startsWith('HTTP/')) return [];
    const headers = Object.fromEntries(rest.filter(line => line.includes(':')).map(line => {
      const index = line.indexOf(':');
      return [line.slice(0, index).toLowerCase(), line.slice(index + 1).trim()];
    }));
    return [{ status_line: statusLine, headers: publicHeaders(headers) }];
  });
}

async function put(file, data) {
  await fs.writeFile(path.join(output, file), JSON.stringify(data, null, 2) + '\n');
}

async function inspect(file, url, purpose, mime) {
  const { stdout } = await run('python3', ['-B', path.join(__dirname, 'inspect_response.py'),
    'html', file, url, purpose, mime || ''], { maxBuffer: 2 ** 20 });
  return JSON.parse(stdout);
}

async function boundedRun(command, args) {
  try {
    const value = await run(command, args, { maxBuffer: 2 ** 20 });
    return { ...value, code: 0 };
  } catch (error) {
    return { stdout: error.stdout || '', stderr: error.stderr || '', code: error.code ?? null };
  }
}

async function curlView(id, url, purpose, action) {
  const body = path.join(cache, id + '.body');
  const headers = path.join(cache, id + '.headers');
  const startedAt = now();
  const outcome = await boundedRun('curl', ['--disable', '--silent', '--show-error', '--location',
    '--max-redirs', '8', '--max-time', '20', '--compressed', '--header', 'Cache-Control: no-cache',
    '--dump-header', headers, '--output', body, '--write-out', '%{json}', '--url', url]);
  const endedAt = now();
  const metrics = outcome.stdout ? JSON.parse(outcome.stdout) : {};
  const bytes = await fs.readFile(body).catch(() => null);
  const blocks = parts(await fs.readFile(headers, 'utf8').catch(() => ''));
  const response = {
    id, method: 'http', action, started_utc: startedAt, response_utc: endedAt,
    asked_url: url, final_url: metrics.url_effective || null,
    status: metrics.http_code || null, proxy_connect_status: metrics.http_connect || null,
    redirect_count: metrics.num_redirects || 0,
    mime: metrics.content_type || null, header_chain: blocks,
    decoded_body_bytes: bytes?.length ?? null, decoded_body_sha256: bytes ? sha(bytes) : null,
    curl_exit: outcome.code, error: outcome.stderr.trim().slice(0, 300) || null,
    analysis: bytes ? await inspect(body, metrics.url_effective || url, purpose, metrics.content_type) : null,
  };
  await put(id + '.json', response);
  return response;
}

function escapeHtml(text) {
  return text.replaceAll('&', '&amp;').replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

async function prepareCard(page, card) {
  const first = '<a id="first" href="' + escapeHtml(card.first_url) + '">' + escapeHtml(card.first_text) + '</a>';
  const additional = card.additional_url ? '<br><a id="extra" href="' + escapeHtml(card.additional_url) +
    '">' + escapeHtml(card.additional_label) + '</a>' : '';
  const html = '<!doctype html><meta charset="utf-8"><main>' + first + additional + '</main>';
  await page.setCard(html);
}

async function browserDom(page, purpose) {
  return page.evaluate((target) => {
    const shorten = (value, limit = 400) => (value || '').replace(/\s+/g, ' ').trim().slice(0, limit);
    const t = document.body?.innerText || '';
    const headings = Array.from(document.querySelectorAll('h1,h2,h3')).map(el => shorten(el.innerText, 100)).filter(Boolean).slice(0, 24);
    const markers = ['Hello World!', 'pip install', 'Page not found', 'Example Domains',
      'https://pypi.org', 'https://rdrr.io/r/base/system.file.html', 'Find Names of R System Files',
      'cpython-freethreading', 'What does it do?', 'Using SVG files', 'Sign in'];
    const selectors = {
      'P3-body': '#enable', 'P3-next': '#what-does-it-do, #enable',
      'P1-next': '#minmal, #user-content-minmal',
      'R1-next': '#ref-examples', 'R2-body': '#using-svg-files', 'R2-next': '#using-svg-files',
    };
    const textNeedles = { 'P1-next': 'master = https://pypi.org', 'R1-next': 'https://rdrr.io/r/base/system.file.html' };
    const decodedGithub = document.querySelector('article.markdown-body, [data-testid=read-only-cursor-text-area]');
    const inCode = textNeedles[target] && Array.from(document.querySelectorAll('pre, [data-line-number], .react-code-text'))
      .find(el => (el.innerText || '').includes(textNeedles[target]));
    const section = inCode || (selectors[target] && document.querySelector(selectors[target]));
    if (section) section.scrollIntoView({ block: 'start', behavior: 'instant' });
    const firstVisible = Array.from(document.querySelectorAll('main,article,h1')).find(el => el.innerText);
    return {
      title: document.title,
      headings, markers: markers.filter(marker => t.includes(marker)),
      selected_section: section ? section.id || section.tagName : null,
      section_sample: shorten(section?.innerText, 180),
      github_reading_surface: Boolean(decodedGithub),
      visible_excerpt: shorten(firstVisible?.innerText || t, 320),
      visible_candidates: Array.from(document.querySelectorAll('a[href]')).filter(anchor => {
        return anchor.getClientRects().length &&
          /\.(svg|cast)(?:[?#]|$)|\/en\/1\.x\/|^https:\/\/rdrr\.io\/r\/base\/system\.file\.html$|^https:\/\/pypi\.org\/?$/.test(anchor.href);
      }).slice(0, 20).map(anchor => ({ href: anchor.href, label: shorten(anchor.innerText, 80) })),
      code_uri_visible: Boolean(inCode),
    };
  }, purpose);
}

async function browserView(page, id, url, purpose, action, trigger) {
  const observation = await page.capture(trigger);
  const final = observation.chain.at(-1);
  const bytes = observation.bytes;
  const mime = final?.mimeType || null;
  const body = path.join(cache, id + '.body');
  if (bytes) await fs.writeFile(body, bytes);
  const dom = await browserDom(page, purpose).catch(error => ({ error: String(error).split('\n')[0] }));
  const shot = id + '.png';
  const screenshot = await page.screenshot(path.join(output, shot)).then(() => shot, () => null);
  const chain = observation.chain.map(response => ({
    url: response.url, status: response.status,
    headers: publicHeaders(Object.fromEntries(response.headers.map(header =>
      [header.name.toLowerCase(), header.value.value]))),
  }));
  const result = {
    id, method: 'browser', action, started_utc: observation.started, response_utc: observation.finished,
    asked_url: url, final_url: await page.url().catch(() => null), status: final?.status ?? null, mime,
    header_chain: chain, redirect_count: chain.filter(hop => hop.status >= 300 && hop.status < 400).length,
    decoded_body_bytes: bytes?.length ?? null, decoded_body_sha256: bytes ? sha(bytes) : null,
    browser_event_count: { top_document_requests: observation.topRequests,
      other_requests_observed_by_capture: observation.otherRequests },
    failed_top_requests: observation.navFailures, error: observation.error, body_capture_error: observation.bodyError,
    dom, screenshot,
    analysis: bytes ? await inspect(body, final?.url || url, purpose, mime) : null,
  };
  await put(id + '.json', result);
  return result;
}

function reachable(receipt) {
  return receipt.status >= 200 && receipt.status < 300 && receipt.analysis?.kind !== 'error_document';
}

function candidateSort(candidates, preferred) {
  return candidates.toSorted((a, b) => Number(b.href === preferred) - Number(a.href === preferred));
}

async function nextBrowser(page, target, receipt) {
  const lookup = { menu_opens: 0, candidates: [], stop_reason: '' };
  if (!reachable(receipt)) return { ...lookup, stop_reason: '첫 입구의 본문 또는 노출 근거 없음' };
  let candidate = receipt.analysis?.candidates?.[0];
  if (!candidate && receipt.dom?.code_uri_visible && ['R1-next', 'P1-next'].includes(target.purpose_id)) {
    candidate = { href: target.add_url, type: 'literal', label: '지정 예제에 표시된 전체 문자 URI' };
  }
  if (target.purpose_id === 'P1-next' || target.purpose_id === 'R1-next') {
    const live = receipt.dom?.visible_candidates?.find(entry => entry.href.replace(/\/$/, '') === candidate?.href);
    if (live) return { ...lookup, candidates: [{ ...live, type: 'href' }] };
    if (candidate && receipt.dom?.code_uri_visible) return { ...lookup, candidates: [{ ...candidate, type: 'literal' }] };
    return { ...lookup, stop_reason: '지정 URI가 실제 화면 코드나 href에 노출됐는지 미확인' };
  }

  if (target.purpose_id === 'P3-next') {
    let candidates = receipt.dom?.visible_candidates || [];
    if (candidates.length === 0) {
      const opened = await page.click('menu', '').catch(() => false);
      lookup.menu_opens += Number(opened);
      if (opened) {
        candidates = await page.evaluate(() => Array.from(document.querySelectorAll('readthedocs-flyout'))
          .flatMap(el => el.shadowRoot ? Array.from(el.shadowRoot.querySelectorAll('a[href]')) : [])
          .filter(anchor => anchor.getClientRects().length && /\/en\/1\.x\//.test(anchor.href))
          .map(anchor => ({ href: anchor.href, label: (anchor.textContent || '').trim() })));
      }
    }
    return { ...lookup, candidates: candidateSort(candidates.map(c => ({ ...c, type: 'href' })), target.add_url),
      stop_reason: candidates.length ? '' : '실제 화면에 노출된 목표 계열 링크 없음' };
  }

  if (target.purpose_id === 'R2-next') {
    const candidates = receipt.analysis?.candidates?.filter(candidate => receipt.dom?.visible_candidates?.some(item => item.href === candidate.href)) || [];
    return { ...lookup, candidates,
      stop_reason: candidates.length ? '' : '지정 절의 SVG/cast 공개 클릭 주소 없음' };
  }
  return { ...lookup, stop_reason: '본문 대조에서 추가 목표 없음' };
}

async function runBrowser(browser, target, card, id, oneView = false) {
  const context = await browser.newContext();
  try {
    const page = await context.newPage();
    await prepareCard(page, card);
    const first = await browserView(page, id + '-1', target.first_url, target.purpose_id,
      'card_first_click', () => page.click('card', '#first'));
    const docs = [first];
    if (oneView) return { docs, menu_opens: 0 };
    const lookup = card.additional_url ?
      { candidates: [{ href: card.additional_url, type: 'card_link', label: card.additional_label }], menu_opens: 0 } :
      await nextBrowser(page, target, first);
    const chosen = lookup.candidates[0];
    if (chosen?.type === 'card_link') {
      const secondPage = await context.newPage();
      await prepareCard(secondPage, card);
      docs.push(await browserView(secondPage, id + '-2', chosen.href, target.purpose_id,
        'card_additional_click', () => secondPage.click('card', '#extra')));
    } else if (chosen?.type === 'href') {
      docs.push(await browserView(page, id + '-2', chosen.href, target.purpose_id,
        'document_link_click', () => page.click('href', chosen.href)));
    } else if (chosen?.type === 'literal') {
      docs.push(await browserView(page, id + '-2', chosen.href, target.purpose_id,
        'verbatim_visible_uri_navigation', () => page.navigate(chosen.href, 'none')));
    }
    return { docs, ...lookup };
  } finally {
    await context.close();
  }
}

async function runHttp(target, card, id, oneView = false) {
  const first = await curlView(id + '-1', target.first_url, target.purpose_id, 'card_first_get');
  const docs = [first];
  if (oneView) return { docs, menu_opens: 0 };
  const candidates = card.additional_url ?
    [{ href: card.additional_url, type: 'card_link', label: card.additional_label }] :
    reachable(first) ? candidateSort(first.analysis?.candidates || [], target.add_url) : [];
  const chosen = candidates[0];
  if (chosen) docs.push(await curlView(id + '-2', chosen.href, target.purpose_id,
    { card_link: 'card_additional_get', href: 'document_href_get', literal: 'verbatim_literal_uri_get' }[chosen.type]));
  return { docs, candidates, menu_opens: 0, stop_reason: chosen ? '' :
    reachable(first) ? 'GET 응답의 지정 후보 없음 또는 본문 대조 종료' : '첫 입구의 본문 또는 노출 근거 없음' };
}

async function observe(browser, target, card, method, id, oneView) {
  const handler = method === 'browser' ?
    () => runBrowser(browser, target, card, id, oneView) : () => runHttp(target, card, id, oneView);
  const initial = { route_id: id, purpose_id: target.purpose_id, card: card.card,
    planned_method: method, first_url: target.first_url, card_added_url: card.additional_url || null,
    entry_registered_utc: now() };
  try {
    const observed = await handler();
    return { ...initial, ...observed };
  } catch (error) {
    // Preserve response receipts already written. An instrumentation failure is not a site result.
    const docs = [];
    for (const index of [1, 2]) {
      const receipt = await fs.readFile(path.join(output, id + '-' + index + '.json'), 'utf8').catch(() => null);
      if (receipt) docs.push(JSON.parse(receipt));
    }
    return { ...initial, docs, instrumentation_error: String(error).split('\n')[0] };
  }
}

const methods = ['browser', 'http'];
const label = (target, extra = null) => ({ first_url: target.first_url,
  first_text: target.purpose_id, additional_url: extra, additional_label: '후속 자료' });
const controls = [
  ['control-public-positive', 'https://pypi.org/project/pip/'],
  ['control-github-blob', 'https://github.com/octocat/Hello-World/blob/master/README'],
  ['control-github-missing', 'https://github.com/octocat/Hello-World/blob/master/af-res-094-missing-public-control.txt'],
  ['control-public-policy', 'https://www.iana.org/domains/reserved'],
];

async function main() {
  await fs.mkdir(output, { recursive: false });
  await fs.mkdir(cache, { recursive: false });
  const configuredProxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch();
  const meta = {
    mode, started_utc: now(), browser: 'Chromium ' + browser.version, automation: browser.automation,
    browser_response_body_collector: Boolean(browser.collector), browser_response_body_collector_error: browser.collectorError,
    curl: (await run('curl', ['--version'])).stdout.split('\n')[0],
    html_parser: (await run('python3', ['-c', 'import lxml; print(lxml.__version__)'])).stdout.trim(),
    environment_proxy_configured: Boolean(configuredProxy),
    browser_context_per_card: true, headers_allowlist: Array.from(visibleHeaders),
  };
  const all = [];
  try {
    if (mode === 'preflight') {
      for (const [id, url] of controls) {
        const target = { purpose_id: id, first_url: url };
        all.push(...await Promise.all(methods.map(method =>
          observe(browser, target, label(target), method, id + '-' + method, true))));
      }
    } else {
      const freeze = JSON.parse(await fs.readFile(path.join(root, 'freeze.json'), 'utf8'));
      const cardTexts = JSON.parse(await fs.readFile(path.join(__dirname, 'card_texts.json'), 'utf8'));
      const runGroup = async (target) => {
        const entries = [];
        for (const cardName of target.card_order) {
          const card = { ...label(target, cardName === 'B' ? target.add_url : null),
            card: cardName, ...cardTexts[target.purpose_id] };
          entries.push(...await Promise.all(methods.map(method => observe(browser, target, card,
            method, target.purpose_id + '-' + cardName + '-' + method, false))));
        }
        return entries;
      };
      const aux = async (purpose, url, phase) => {
        const target = { purpose_id: purpose, first_url: url };
        return Promise.all(methods.map(method => observe(browser, target, label(target), method,
          purpose + '-' + phase + '-' + method, true)));
      };
      const r2 = await aux('R2-blob', freeze.git_blob_auxiliary[1], 'primary');
      for (const target of freeze.targets) all.push(...await runGroup(target));
      const r1 = all.filter(row => row.purpose_id === 'R1-next' && row.card === 'B');
      const different = (rows) => rows.length === 2 && [0, 1].every(i => rows[i].docs[0]) &&
        JSON.stringify(rows[0].docs.slice(0, 1).map(d => [d.status, d.analysis?.kind])) !==
        JSON.stringify(rows[1].docs.slice(0, 1).map(d => [d.status, d.analysis?.kind]));
      const auxiliary = { r1_reused_receipts: r1.map(row => row.docs[0]?.id), r2_primary: r2, retries: [] };
      if (different(r1)) auxiliary.retries.push(...await aux('R1-blob', freeze.git_blob_auxiliary[0], 'retry'));
      if (different(r2)) auxiliary.retries.push(...await aux('R2-blob', freeze.git_blob_auxiliary[1], 'retry'));
      await put('blob-comparison.json', auxiliary);
    }
  } finally {
    await browser.close();
  }
  meta.finished_utc = now();
  await put('run.json', meta);
  await put('routes-observed.json', all);
  for (const row of all) console.log(row.route_id, row.docs.map(doc => doc.status || 'no-origin-status').join('→'),
    row.instrumentation_error || row.docs[0]?.analysis?.kind || row.docs[0]?.error || '');
}

main().catch(error => { console.error(error); process.exitCode = 1; });
