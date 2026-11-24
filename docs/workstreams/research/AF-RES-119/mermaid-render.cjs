/* Render the exact npm Mermaid distribution in an isolated Chromium document. */
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");

async function main() {
  const [prefix, input, output, options, browserOptions] = process.argv.slice(2);
  const packages = createRequire(path.join(prefix, "package.json"));
  const puppeteer = packages("puppeteer");
  const source = fs.readFileSync(packages.resolve("mermaid/dist/mermaid.min.js"), "utf8");
  const diagram = fs.readFileSync(input, "utf8");
  const config = JSON.parse(fs.readFileSync(options, "utf8"));
  const launchOptions = JSON.parse(fs.readFileSync(browserOptions, "utf8"));
  const browser = await puppeteer.launch({ ...launchOptions, headless: "new" });
  try {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on("request", (request) => request.abort("blockedbyclient"));
    await page.setViewport({ width: 800, height: 600 });
    await page.setContent('<!doctype html><body><div id="scratch"></div><div id="result"></div></body>');
    await page.addScriptTag({ content: source });
    const result = await page.evaluate(async ({ diagram, config }) => {
      const mermaid = window.mermaid;
      mermaid.initialize({ ...config, startOnLoad: false });
      await document.fonts.ready;
      const scratch = document.getElementById("scratch");
      const markup = await new Promise((resolve, reject) => {
        try {
          mermaid.mermaidAPI.render("af119-svg", diagram, resolve, scratch);
        } catch (err) {
          reject(err);
        }
      });
      scratch.remove();
      document.getElementById("result").innerHTML = markup;
      const svg = document.querySelector("#result svg");
      if (!svg) {
        throw new Error("Mermaid produced no SVG element");
      }
      const shapes = Array.from(svg.querySelectorAll(
        ".labelText,.loopText,.slice,.legend text,.cluster,.node,.node rect,.node ellipse,.node polygon,.flowchart-link,.messageText,.actor",
      )).map((node) => {
        const css = window.getComputedStyle(node);
        const bounds = node.getBBox();
        return {
          tag: node.tagName,
          id: node.id,
          class: node.getAttribute("class"),
          text: node.textContent.trim(),
          transform: node.getAttribute("transform"),
          path: node.getAttribute("d"),
          visibility: css.visibility,
          font: css.fontFamily,
          fill: css.fill,
          box: [bounds.x, bounds.y, bounds.width, bounds.height],
        };
      });
      return { markup, shapes, xml: new XMLSerializer().serializeToString(svg) };
    }, { diagram, config });
    fs.writeFileSync(output, result.markup);
    fs.writeFileSync("output.browser.xml", result.xml);
    fs.writeFileSync("browser-observations.json", JSON.stringify(result.shapes, null, 2) + "\n");
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  process.stderr.write(String(error.stack || error) + "\n");
  process.exitCode = 1;
});
