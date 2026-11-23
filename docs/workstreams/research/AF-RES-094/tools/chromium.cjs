const { chromium } = require(process.env.AF_PLAYWRIGHT || 'playwright');

class ChromiumPage {
  constructor(page) {
    this.page = page;
  }

  evaluate(fn, arg) {
    return this.page.evaluate(fn, arg);
  }

  setCard(html) {
    return this.page.setContent(html, { waitUntil: 'domcontentloaded', timeout: 7000 });
  }

  navigate(url, wait = 'interactive') {
    return this.page.goto(url, { waitUntil: wait === 'none' ? 'commit' : 'domcontentloaded', timeout: 17000 });
  }

  async click(kind, value) {
    const handles = {
      card: () => this.page.locator(value),
      menu: () => this.page.locator('readthedocs-flyout').getByRole('button').first(),
    };
    if (kind === 'href') {
      const item = await this.page.evaluateHandle((href) => {
        const roots = [document, ...Array.from(document.querySelectorAll('readthedocs-flyout'))
          .map(el => el.shadowRoot).filter(Boolean)];
        return roots.flatMap(root => Array.from(root.querySelectorAll('a[href]')))
          .find(el => el.href === href && el.getClientRects().length);
      }, value);
      const element = item.asElement();
      if (!element) return false;
      await element.click({ timeout: 7000 });
    } else {
      await handles[kind]().click({ timeout: kind === 'menu' ? 3500 : 7000 });
    }
    return true;
  }

  screenshot(path) {
    return this.page.screenshot({ path, animations: 'disabled', timeout: 6500 });
  }

  async url() {
    return this.page.url();
  }

  async capture(trigger) {
    const requests = [];
    const responses = [];
    const failures = [];
    const onRequest = request => requests.push(request);
    const onResponse = response => responses.push(response);
    const onFailure = request => failures.push(request);
    const top = request => request.isNavigationRequest() && request.frame() === this.page.mainFrame();
    this.page.on('request', onRequest);
    this.page.on('response', onResponse);
    this.page.on('requestfailed', onFailure);
    const started = new Date().toISOString();
    try {
      const navigation = this.page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 17000 });
      const [done, action] = await Promise.allSettled([navigation, trigger()]);
      const finished = new Date().toISOString();
      const main = responses.filter(response => top(response.request()));
      const final = done.status === 'fulfilled' && done.value || main.at(-1);
      let bodyError = null;
      const bytes = final ? await final.body().catch(error => {
        bodyError = String(error).split('\n')[0];
        return null;
      }) : null;
      return {
        started, finished, bytes, bodyError,
        error: [done, action].filter(result => result.status === 'rejected')
          .map(result => String(result.reason).split('\n')[0]).join(' / ') || null,
        chain: main.map(response => ({ url: response.url(), status: response.status(),
          mimeType: response.headers()['content-type'], headers: Object.entries(response.headers())
            .map(([name, value]) => ({ name, value: { value } })) })),
        navFailures: failures.filter(top).map(request => ({ url: request.url(), code: request.failure()?.errorText })),
        topRequests: requests.filter(top).length,
        otherRequests: requests.filter(request => !top(request)).length,
      };
    } finally {
      this.page.off('request', onRequest);
      this.page.off('response', onResponse);
      this.page.off('requestfailed', onFailure);
    }
  }
}

async function launch() {
  const proxyUrl = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch({ executablePath: process.env.AF_CHROMIUM || '/usr/bin/chromium',
    headless: true, proxy: proxyUrl ? { server: proxyUrl } : undefined });
  return {
    version: browser.version(), collector: true,
    automation: 'Playwright ' + require(require.resolve(process.env.AF_PLAYWRIGHT || 'playwright')
      .replace(/[/\\]index\.js$/, '/package.json')).version,
    newContext: async () => {
      const context = await browser.newContext({ viewport: { width: 1180, height: 800 },
        locale: 'en-US', timezoneId: 'UTC', serviceWorkers: 'block' });
      return {
        newPage: async () => {
          const page = await context.newPage();
          const cdp = await context.newCDPSession(page);
          await cdp.send('Network.enable');
          await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
          return new ChromiumPage(page);
        },
        close: () => context.close(),
      };
    },
    close: () => browser.close(),
  };
}

module.exports = { launch };
