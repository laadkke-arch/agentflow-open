// Public package probe. Encoding follows the AF-RES-139 replay.
const {readFileSync, writeFileSync, realpathSync} = require("node:fs");
const {createHash} = require("node:crypto");
const {pathToFileURL, fileURLToPath} = require("node:url");
const {relative, resolve} = require("node:path");
const {Script, createContext} = require("node:vm");

const CASE_TIMEOUT_MS = 250;
const callContext = createContext({invoke: null});
const callScript = new Script("invoke()");

const [pkg, mode, inputPath, outputPath] = process.argv.slice(2);
const packageRoot = resolve("node_modules", pkg);
const readJson = path => JSON.parse(readFileSync(path, "utf8"));
const hash = data => createHash("sha256").update(data).digest("hex");
const fileHash = path => hash(readFileSync(path));

function encode(value) {
    if (typeof value === "number") {
        if (Object.is(value, -0)) return {type: "number", value: "-0"};
        if (!Number.isFinite(value)) return {type: "number", value: String(value)};
        return {type: "number", value};
    }
    if (value === undefined) return {type: "undefined"};
    if (value === null) return {type: "null"};
    if (Array.isArray(value)) return {type: "array", value: serializeArray(value)};
    if (value instanceof Set) return {type: "set", value: serializeArray([...value])};
    if (value instanceof Float64Array) return {type: "float64", value: serializeArray([...value])};
    if (typeof value === "object") return {type: "object", value: Object.fromEntries(
        Object.keys(value).sort().map(key => [key, encode(value[key])]))};
    return {type: typeof value, value: String(value)};
}

function serializeArray(values) {
    const encoded = Array.from({length: values.length}, (_, index) =>
        Object.hasOwn(values, index) ? encode(values[index]) : {type: "hole"});
    if (encoded.length < 129) return encoded;
    return {length: encoded.length, sha256: hash(JSON.stringify(encoded)),
        head: encoded.slice(0, 3), tail: encoded.slice(-3)};
}

function decode(value) {
    const specials = new Map([["NaN", NaN], ["-0", -0], ["undefined", undefined], ["max", Number.MAX_VALUE]]);
    if (Array.isArray(value)) return value.map(decode);
    return specials.has(value) ? specials.get(value) : value;
}

function order(a, b) {
    const aMissing = a == null || Number.isNaN(a);
    const bMissing = b == null || Number.isNaN(b);
    if (aMissing || bMissing) return Number(aMissing) - Number(bMissing);
    return a - b;
}

function errorInfo(error) {
    return {name: error?.name ?? null, code: error?.code ?? null, message: error?.message ?? String(error),
        stack: error?.stack ?? null};
}

async function load() {
    if (mode === "require") {
        const resolved = require.resolve(pkg);
        const api = require(pkg);
        return {api, resolved: require.cache[resolved]?.filename ?? resolved};
    }
    if (mode !== "import") throw Error("unknown public loader " + mode);
    const helper = await import(pathToFileURL(resolve("resolve.mjs")).href);
    const resolved = fileURLToPath(helper.entry(pkg));
    return {api: await import(pkg), resolved};
}

function runCase(api, item) {
    const {mode, function: name, input, representation} = item;
    const values = input.range_desc ?
        Array.from({length: input.range_desc[0] - input.range_desc[1] + 1}, (_, i) => input.range_desc[0] - i) :
        decode(input.values);
    const sorted = mode === "sorted_copy" ? values.slice().sort(order) : values;
    const wrap = a => representation === "set" ? new Set(a) : representation === "float64" ? new Float64Array(a) :
        item.accessor ? a.map(value => ({value})) : a;
    const original = wrap(values);
    const argument = mode === "direct" ? original : wrap(sorted);
    const p = decode(item.p);
    const argument_before = encode(argument);
    const original_before = encode(original);
    const p_before = encode(p);
    const accessor_trace = [];
    let result;
    if (typeof api[name] !== "function") {
        result = {type: "api_absent", property_type: typeof api[name]};
    } else {
        const args = name === "median" ? [argument] : [argument, p];
        if (item.accessor) args.push((box, index, container) => {
            accessor_trace.push([encode(index), container === argument]);
            return box.value;
        });
        try {
            callContext.invoke = () => api[name](...args);
            result = encode(callScript.runInContext(callContext, {timeout: CASE_TIMEOUT_MS}));
        } catch (error) {
            result = {type: error.code === "ERR_SCRIPT_EXECUTION_TIMEOUT" ? "timeout" : "exception", ...errorInfo(error)};
        } finally {
            callContext.invoke = null;
        }
    }
    const argument_after = encode(argument);
    const original_after = encode(original);
    const p_after = encode(p);
    const equals = (left, right) => JSON.stringify(left) === JSON.stringify(right);
    return {id: item.id, input_sha256: item.input_sha256, result, argument_before, argument_after,
        original_before, original_after, p_before, p_after, accessor_trace,
        argument_mutated: !equals(argument_before, argument_after), original_mutated: !equals(original_before, original_after),
        p_mutated: !equals(p_before, p_after)};
}

async function main() {
    const manifestPath = resolve(packageRoot, "package.json");
    const manifest = readJson(manifestPath);
    const direct = {};
    const lock = readJson(resolve("package-lock.json"));
    for (const field of ["dependencies", "optionalDependencies", "peerDependencies"]) {
        for (const [name, range] of Object.entries(manifest[field] ?? {})) {
            const candidates = ["node_modules/" + pkg + "/node_modules/" + name, "node_modules/" + name];
            const location = candidates.find(item => lock.packages[item]);
            const observed = location ? readJson(resolve(location, "package.json")) : null;
            direct[name] = {field, range, version: observed?.version ?? null,
                integrity: location ? lock.packages[location].integrity ?? null : null};
        }
    }
    const fingerprint = {case_timeout_ms: CASE_TIMEOUT_MS, package: manifest.name, version: manifest.version, runtime: process.version,
        arch: process.arch, platform: process.platform, loader: mode, direct, manifest_sha256: fileHash(manifestPath),
        lock_sha256: fileHash(resolve("package-lock.json")), inputs_sha256: fileHash(inputPath)};
    try {
        const target = await load();
        const loaded = realpathSync(target.resolved);
        const cases = readJson(inputPath).map(item => runCase(target.api, item));
        return {...fingerprint, status: "ok", entry: relative(packageRoot, loaded), entry_sha256: fileHash(loaded), cases};
    } catch (error) {
        return {...fingerprint, status: "load_error", error: errorInfo(error), cases: []};
    }
}

main().then(data => {
    writeFileSync(outputPath, JSON.stringify(data) + "\n");
    process.stdout.write(JSON.stringify({package: data.package, version: data.version, status: data.status,
        cells: data.cases.length}) + "\n");
    if (data.status !== "ok") process.exitCode = 1;
}).catch(error => {
    process.stderr.write(JSON.stringify(errorInfo(error)) + "\n");
    process.exitCode = 1;
});
