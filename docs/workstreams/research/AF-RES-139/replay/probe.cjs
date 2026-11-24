const {readFileSync, realpathSync} = require("node:fs");
const {createHash} = require("node:crypto");
const {pathToFileURL, fileURLToPath} = require("node:url");
const {relative, resolve} = require("node:path");
const {performance} = require("node:perf_hooks");

const inputPath = process.argv[2];
const inputs = JSON.parse(readFileSync(inputPath, "utf8"));
const pkg = inputs.package;
const packagePath = resolve("node_modules", pkg, "package.json");
const packageRoot = resolve("node_modules", pkg);
const readJson = path => JSON.parse(readFileSync(path, "utf8"));
const fileHash = path => createHash("sha256").update(readFileSync(path)).digest("hex");

function encode(value) {
    if (typeof value === "number") {
        if (Object.is(value, -0)) return {type: "number", value: "-0"};
        if (!Number.isFinite(value)) return {type: "number", value: String(value)};
        return {type: "number", value};
    }
    if (value === undefined) return {type: "undefined"};
    if (value === null) return {type: "null"};
    if (Array.isArray(value)) return {type: "array", value: serializeArray(value)};
    return {type: typeof value, value: String(value)};
}

function serializeArray(values) {
    return Array.from({length: values.length}, (_, index) =>
        Object.hasOwn(values, index) ? encode(values[index]) : {type: "hole"});
}

function sameArray(left, right) {
    return left.length === right.length && Array.from({length: left.length}, (_, index) =>
        Object.hasOwn(left, index) === Object.hasOwn(right, index) && Object.is(left[index], right[index])
    ).every(Boolean);
}

function order(a, b) {
    if (Number.isNaN(a)) return Number.isNaN(b) ? 0 : 1;
    if (Number.isNaN(b)) return -1;
    return a - b;
}

function errorInfo(error) {
    return {name: error?.name ?? null, code: error?.code ?? null, message: error?.message ?? String(error),
        stack: error?.stack ?? null};
}

async function load() {
    try {
        const resolved = require.resolve(pkg);
        const api = require(pkg);
        const loaded = require.cache[resolved]?.filename ?? resolved;
        return {api, resolved, loaded, mode: "require"};
    } catch (error) {
        if (!["ERR_REQUIRE_ESM", "ERR_REQUIRE_ASYNC_MODULE", "ERR_PACKAGE_PATH_NOT_EXPORTED"].includes(error.code)) throw error;
        // This import is deliberately by the bare public package name.
        const imported = await import(pkg);
        if (require("node:fs").existsSync(resolve("resolve.mjs"))) {
            const helper = await import(pathToFileURL(resolve("resolve.mjs")).href);
            const resolved = fileURLToPath(helper.entry(pkg));
            return {api: imported.default?.quantile ? imported.default : imported, resolved, loaded: resolved,
                mode: "import", require_error: errorInfo(error)};
        }
        throw Error("missing import-resolution recorder");
    }
}

function runCase(api, fn, input_id, input, p, mode) {
    const original = input.map(value => value === "NaN" ? NaN : value);
    const argument = mode === "direct" ? original : original.slice().sort(order);
    const beforeOriginal = original.slice();
    const beforeArgument = argument.slice();
    let result;
    if (typeof api[fn] !== "function") {
        result = {type: "api_absent", property_type: typeof api[fn]};
    } else {
        try {
            const output = fn === "quantile" ? api[fn](argument, p) : api[fn](argument);
            result = encode(output);
        } catch (error) {
            result = {type: "exception", ...errorInfo(error)};
        }
    }
    return {
        cell: [fn, input_id, p ?? "-", mode].join("/"), fn, input_id, p, mode, raw_input: input, result,
        argument_before: serializeArray(beforeArgument), argument_after: serializeArray(argument),
        original_before: serializeArray(beforeOriginal), original_after: serializeArray(original),
        argument_mutated: !sameArray(beforeArgument, argument), original_mutated: !sameArray(beforeOriginal, original),
    };
}

async function main() {
    const started_utc = new Date().toISOString();
    const start = performance.now();
    const cpu = process.cpuUsage();
    const manifest = readJson(packagePath);
    const direct = {};
    const lock = readJson(resolve("package-lock.json"));
    for (const field of ["dependencies", "optionalDependencies", "peerDependencies"]) {
        for (const [name, requirement] of Object.entries(manifest[field] ?? {})) {
            const candidates = [`node_modules/${pkg}/node_modules/${name}`, `node_modules/${name}`];
            const location = candidates.find(item => lock.packages[item]);
            const observed = location ? readJson(resolve(location, "package.json")) : null;
            direct[name] = {field, range: requirement, version: observed?.version ?? null,
                integrity: location ? lock.packages[location].integrity ?? null : null};
        }
    }
    const target = await load();
    const loaded = realpathSync(target.loaded);
    const cases = inputs.functions.flatMap(fn =>
        Object.entries(inputs.arrays).flatMap(([inputId, input]) =>
            (fn === "quantile" ? inputs.quantile_p : [null]).flatMap(p =>
                inputs.modes.map(mode => runCase(target.api, fn, inputId, input, p, mode))
            )
        )
    );
    const used = process.cpuUsage(cpu);
    return {
        status: "ok", package: manifest.name, version: manifest.version, runtime: process.version,
        platform: process.platform, arch: process.arch, unit: "one process for both functions and all inputs",
        started_utc, finished_utc: new Date().toISOString(), direct, mode: target.mode,
        resolved: target.resolved, loaded, entry_relative: relative(packageRoot, loaded), entry_sha256: fileHash(loaded),
        lock_sha256: fileHash(resolve("package-lock.json")), inputs_sha256: fileHash(inputPath),
        supported: inputs.functions.every(name => typeof target.api[name] === "function"),
        require_error: target.require_error ?? null, node_internal_wall_ms: performance.now() - start,
        node_internal_cpu_us: used, cases,
    };
}

main().then(data => process.stdout.write(JSON.stringify(data))).catch(error => {
    process.stdout.write(JSON.stringify({status: "load_error", finished_utc: new Date().toISOString(), error: errorInfo(error)}));
    process.exitCode = 1;
});
