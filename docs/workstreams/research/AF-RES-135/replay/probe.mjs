import {createRequire} from "node:module";
import {readFileSync} from "node:fs";
import {createHash} from "node:crypto";
import {relative, resolve} from "node:path";
import {fileURLToPath} from "node:url";

const environment = JSON.parse(readFileSync("case.json", "utf8"));
const fixture = environment.inputs;
const started = new Date().toISOString();

function digest(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function encode(value) {
  if (value === null) return {kind: "null"};
  if (value === undefined) return {kind: "undefined"};
  if (Number.isNaN(value)) return {kind: "nan"};
  if (Object.is(value, -0)) return {kind: "negative_zero"};
  if (value === Infinity) return {kind: "positive_infinity"};
  if (value === -Infinity) return {kind: "negative_infinity"};
  return {kind: typeof value, value};
}

function exception(error) {
  return {kind: "exception", name: error.name, code: error.code ?? null, message: error.message};
}

function measure(operation) {
  try { return encode(operation()); }
  catch (error) { return exception(error); }
}

const rootPackage = resolve("node_modules/d3-scale/package.json");
const manifest = JSON.parse(readFileSync(rootPackage, "utf8"));
const mode = manifest.type === "module" ? "import" : "require";
const require = createRequire(import.meta.url);
const packageRequire = createRequire(rootPackage);
const outputs = {};
const result = {utc: started, node: process.version, platform: process.platform, arch: process.arch,
  mode, package_version: manifest.version, outputs};
const missing = {null: null, undefined: undefined, NaN: NaN};

try {
  const mod = mode === "import" ? fileURLToPath(import.meta.resolve("d3-scale")) : require.resolve("d3-scale");
  const {scaleLinear} = mode === "import" ? await import("d3-scale") : require("d3-scale");
  result.entry = relative(process.cwd(), mod);
  result.entry_sha256 = digest(mod);
  result.direct = Object.fromEntries(Object.keys(manifest.dependencies).sort().map(name => {
    const dependencyManifest = JSON.parse(readFileSync(resolve("node_modules", name, "package.json"), "utf8"));
    const mod = packageRequire.resolve(name);
    if (!mod.startsWith(resolve("node_modules", name) + "/")) {
      throw new Error(`Unexpected resolution for ${name}: ${mod}`);
    }
    return [name, {version: dependencyManifest.version, entry: relative(process.cwd(), mod), sha256: digest(mod)}];
  }));
  const newScale = () => scaleLinear().domain(fixture.domain).range(fixture.range);
  const defaultScale = newScale();
  const clampedScale = newScale().clamp(true);
  for (const x of fixture.numbers) {
    outputs[`default.n${x}`] = measure(() => defaultScale(x));
    outputs[`clamp.n${x}`] = measure(() => clampedScale(x));
  }
  for (const key of fixture.missing) outputs[`default.${key}`] = measure(() => defaultScale(missing[key]));
  const unknown = newScale();
  result.unknown_setter = null;
  if (typeof unknown.unknown === "function") {
    outputs["unknown.support"] = {kind: "method_present"};
    try {
      const setterResult = unknown.unknown(fixture.unknown_value);
      result.unknown_setter = {returns_same_scale: setterResult === unknown, getter: measure(() => unknown.unknown())};
      for (const key of fixture.missing) outputs[`unknown.${key}`] = measure(() => unknown(missing[key]));
    } catch (error) {
      for (const key of fixture.missing) outputs[`unknown.${key}`] = exception(error);
    }
  } else {
    outputs["unknown.support"] = {kind: "method_absent"};
    for (const key of fixture.missing) outputs[`unknown.${key}`] = {kind: "method_absent"};
  }
  outputs["invert.n50"] = typeof defaultScale.invert === "function"
    ? measure(() => defaultScale.invert(fixture.invert)) : {kind: "method_absent"};
  if (fixture.checks.some(key => !(key in outputs))) throw new Error("Incomplete output vector");
  result.status = "observed";
} catch (error) {
  result.status = "load_or_setup_failed";
  result.failure = exception(error);
}
result.completed_utc = new Date().toISOString();
process.stdout.write(JSON.stringify(result) + "\n");
