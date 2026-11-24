/* Contrast inactive and programmatically activated selection; no pointer events. */
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");

async function main() {
  const [prefix, specPath, dataDir, output] = process.argv.slice(2);
  const packages = createRequire(path.join(prefix, "package.json"));
  const vega = packages("vega");
  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  const view = new vega.View(vega.parse(spec), {
    loader: vega.loader({ baseURL: dataDir }),
    logger: vega.logger(vega.Error),
    renderer: "none",
  });
  await view.runAsync();
  const fields = view.signal("drag_brush_tuple_fields");
  if (fields.length !== 1 || fields[0].channel !== "x") {
    throw new Error("expected single x projection from the sealed V8628 input");
  }
  const value = new Date(Date.UTC(2012, 0, 1));
  const tuple = { unit: "", fields, values: [[+value]] };
  view.change("drag_brush_store", vega.changeset().remove(() => true).insert(tuple));
  await view.runAsync();
  fs.writeFileSync(output, await view.toSVG(), "utf8");
  fs.writeFileSync("active-selection.json", JSON.stringify({
    signal: "drag_brush_tuple_fields", store: "drag_brush_store", tuple,
    values_in_store: view.data("drag_brush_store"),
    method: "dataflow injection, no DOM pointer events",
  }, null, 2) + "\n");
  view.finalize();
}

main().catch((error) => {
  process.stderr.write(String(error.stack || error) + "\n");
  process.exitCode = 1;
});
