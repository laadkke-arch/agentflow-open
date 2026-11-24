const fs = require("node:fs");

const [moduleDirectory, operation, bindingPath] = process.argv.slice(2);
const input = fs.readFileSync(0, "utf8");

if (operation === "expand") {
  const mustache = require(moduleDirectory + "/mustache");
  const variables = bindingPath ? JSON.parse(fs.readFileSync(bindingPath, "utf8")) : {};
  process.stdout.write(mustache.render(input, variables));
} else if (operation === "parse") {
  const {Parser, HtmlRenderer} = require(moduleDirectory + "/commonmark");
  const document = new Parser().parse(input);
  const blocks = [];
  for (let block = document.firstChild; block; block = block.next) {
    const inline = [];
    for (let node = block.firstChild; node; node = node.next) {
      inline.push({type: node.type, literal: node.literal});
    }
    blocks.push({
      type: block.type,
      info: block.info,
      literal: block.literal,
      sourcepos: block.sourcepos,
      inline,
    });
  }
  process.stdout.write(JSON.stringify({blocks, html: new HtmlRenderer().render(document)}) + "\n");
} else {
  throw new Error("Expected expand or parse.");
}
