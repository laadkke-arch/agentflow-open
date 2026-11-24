// Analyze package text as data. Only the separately locked Acorn parser is loaded.
const {readFileSync, existsSync} = require("node:fs");
const {resolve, dirname, relative} = require("node:path");
const {createHash} = require("node:crypto");
const {createRequire} = require("node:module");
const [directory, entry, parserRoot, packageName, depthArg] = process.argv.slice(2);
const depth = Number(depthArg);
const acorn = createRequire(resolve(parserRoot, "package-lock.json"))("acorn");
const options = {ecmaVersion: "latest", sourceType: "module", locations: true};
const targets = packageName === "d3-array" ? ["quantile", "quantileSorted", "median"] : ["quantile", "median"];
const inputs = new Map();
const docs = new Map();
const hash = value => createHash("sha256").update(value).digest("hex");
const arrayMethods = new Set(["slice", "sort", "push", "pop", "map", "concat", "subarray"]);
const knownStatic = new Set(["Array.isArray", "Math.ceil", "Math.floor", "Math.log", "Math.exp",
    "Math.sqrt", "Math.abs", "Math.sign", "Math.min", "Math.max", "Number.isInteger", "Float64Array.from"]);
const knownGlobals = new Set(["Error", "TypeError", "RangeError", "Number", "Array", "Float64Array"]);

function walk(node, visit) {
    if (!node || typeof node.type !== "string" || visit(node) === false) return;
    for (const value of Object.values(node)) {
        if (Array.isArray(value)) {
            for (const child of value) walk(child, visit);
        } else {
            walk(value, visit);
        }
    }
}

function text(path) {
    if (!inputs.has(path)) inputs.set(path, readFileSync(resolve(directory, path), "utf8"));
    return inputs.get(path);
}

function document(path) {
    if (docs.has(path)) return docs.get(path);
    const source = text(path);
    const doc = {path, source, declarations: new Map(), imports: new Map(), published: new Map()};
    const ast = acorn.parse(source, options);
    function declare(name, node) {
        const found = doc.declarations.get(name) ?? [];
        found.push(node);
        doc.declarations.set(name, found);
    }
    walk(ast, node => {
        if (node.type === "FunctionDeclaration" && node.id) declare(node.id.name, node);
        if (node.type === "ImportDeclaration") {
            for (const specifier of node.specifiers) {
                doc.imports.set(specifier.local.name, {from: node.source.value, name: specifier.imported?.name ?? "default"});
            }
        }
        if (node.type === "VariableDeclarator" && node.id.type === "Identifier") {
            if (["FunctionExpression", "ArrowFunctionExpression"].includes(node.init?.type)) declare(node.id.name, node.init);
            const call = node.init;
            if (call?.type === "CallExpression" && call.callee.name === "require" && typeof call.arguments[0]?.value === "string") {
                doc.imports.set(node.id.name, {from: call.arguments[0].value, name: "default"});
            }
        }
        if (node.type === "AssignmentExpression" && node.left.type === "MemberExpression" &&
            node.left.object.name === "exports" && !node.left.computed && node.right.type === "Identifier") {
            doc.published.set(node.left.property.name, {local: node.right.name});
        }
        if (node.type === "ExportNamedDeclaration") {
            for (const specifier of node.specifiers) {
                doc.published.set(specifier.exported.name, node.source ?
                    {from: node.source.value, name: specifier.local.name} : {local: specifier.local.name});
            }
            if (node.declaration?.id) doc.published.set(node.declaration.id.name, {local: node.declaration.id.name});
        }
        if (node.type === "ExportDefaultDeclaration") {
            const value = node.declaration;
            const local = value.name ?? value.id?.name ?? "(default)";
            if (!value.name && !value.id) declare(local, value);
            doc.published.set("default", {local});
        }
    });
    docs.set(path, doc);
    return doc;
}

function from(doc, {from: specifier, name}) {
    if (!specifier.startsWith(".")) throw Error("unresolved external " + specifier + "#" + name);
    const base = resolve(directory, dirname(doc.path), specifier);
    const file = [base, base + ".js"].find(path => path.startsWith(resolve(directory) + "/") &&
        path.endsWith(".js") && existsSync(path));
    if (!file) throw Error("missing delegate " + specifier);
    return exported(document(relative(directory, file)), name);
}

function binding(doc, name) {
    const candidates = doc.declarations.get(name) ?? [];
    if (candidates.length === 1 && !doc.imports.has(name)) return {doc, node: candidates[0], name};
    if (candidates.length || !doc.imports.has(name)) throw Error("unresolved binding " + doc.path + "#" + name);
    return from(doc, doc.imports.get(name));
}

function exported(doc, name) {
    const entry = doc.published.get(name);
    if (!entry) throw Error("unresolved export " + doc.path + "#" + name);
    return entry.from ? from(doc, entry) : binding(doc, entry.local);
}

const tokenValue = token => typeof token.value === "bigint" ? token.value.toString() :
    token.type.label === "regexp" ? [token.value.pattern, token.value.flags] : token.value ?? null;
const tokenize = source => [...acorn.tokenizer(source, options)].map(token => [token.type.label, tokenValue(token)]);

function summarize({doc, node, name}) {
    const body = doc.source.slice(node.body.start, node.body.end);
    const parameters = node.params.map(parameter => tokenize(doc.source.slice(parameter.start, parameter.end)));
    const tokens = tokenize(body);
    return {name, path: doc.path, lines: [node.loc.start.line, node.loc.end.line],
        raw_sha256: hash(body), token_sha256: hash(JSON.stringify([node.generator, node.async, parameters, tokens])),
        token_count: tokens.length};
}

function omittedDefault(root, name, param, maxArgs) {
    if (maxArgs === null || root.node.params.indexOf(param) < maxArgs) return null;
    if (param.right?.type === "Identifier") return binding(root.doc, param.right.name);
    const statement = root.node.body.body?.[0]?.expression;
    const decision = statement?.right;
    const test = decision?.test;
    if (statement?.operator === "=" && statement.left?.name === name &&
        decision?.type === "ConditionalExpression" && test?.operator === "===" &&
        test.left?.name === name && test.right?.name === "undefined" &&
        decision.consequent?.type === "Identifier") return binding(root.doc, decision.consequent.name);
    return null;
}

function direct(root, maxArgs) {
    const calls = new Map();
    function add(key, target, argc = null) {
        const older = calls.get(key);
        const maxArgs = older && (older.maxArgs === null || argc === null) ? null :
            Math.max(older?.maxArgs ?? 0, argc ?? 0);
        calls.set(key, {target, maxArgs: argc === null ? null : maxArgs});
    }
    const params = new Map(root.node.params.map(p => [p.name ?? p.left?.name, p]));
    const arrays = new Set(["x", "arr", "array", "values", "stack", "indices", "copy", "results"]
        .filter(name => params.has(name)));
    walk(root.node.body, node => {
        if (/^(?:Function|ArrowFunction)/.test(node.type)) return false;
        if (node.type === "VariableDeclarator" && node.id.type === "Identifier" &&
            (node.init?.type === "ArrayExpression" ||
             (node.init?.type === "CallExpression" && node.init.callee.property?.name === "slice" &&
              arrays.has(node.init.callee.object?.name)))) arrays.add(node.id.name);
        if (!["CallExpression", "NewExpression"].includes(node.type)) return;
        const callee = node.callee;
        if (callee.type === "Identifier" && !knownGlobals.has(callee.name)) {
            const param = params.get(callee.name);
            if (packageName === "d3-array" && callee.name === "valueof" && param) {
                if (param.right?.type === "Identifier") add("default:valueof", binding(root.doc, param.right.name));
                return;
            }
            if (param) {
                const fallback = omittedDefault(root, callee.name, param, maxArgs);
                if (!fallback) throw Error("dynamic parameter " + callee.name);
                add("default:" + callee.name, fallback, node.arguments.length);
                return;
            }
            const args = node.arguments.some(arg => arg.type === "SpreadElement") ? null : node.arguments.length;
            add(callee.name, binding(root.doc, callee.name), args);
        } else if (callee.type === "MemberExpression" && !callee.computed) {
            const object = callee.object.name;
            const method = callee.property.name;
            const sliceOfSelection = method === "subarray" && callee.object.type === "CallExpression" &&
                callee.object.callee.name === "quickselect";
            if (!knownStatic.has(object + "." + method) && !sliceOfSelection &&
                !(arrays.has(object) && arrayMethods.has(method))) {
                throw Error("unresolved member call " + object + "." + method);
            }
            // Array.sort(compare) passes a statically declared callback to a standard method.
            const sorter = method === "sort" && node.arguments[0];
            if (sorter?.type === "Identifier") add("sort:" + sorter.name, binding(root.doc, sorter.name));
        } else if (callee.type !== "Identifier") {
            throw Error("unresolved dynamic call " + callee.type);
        }
    });
    return calls;
}

function sourceMap(entry) {
    const filename = entry + ".map";
    if (!existsSync(resolve(directory, filename))) return new Map();
    const map = JSON.parse(text(filename));
    return new Map(map.sources.map((path, index) => [
        relative(directory, resolve(directory, dirname(entry), path)), map.sourcesContent?.[index]
    ]));
}

function tree(root, limit, seen = new Set(), maxArgs = null) {
    const body = summarize(root);
    const key = body.path + "#" + body.name;
    if (!limit || seen.has(key)) return {body};
    const visited = new Set(seen).add(key);
    const calls = Object.fromEntries([...direct(root, maxArgs)].sort(([a], [b]) => a.localeCompare(b, "en"))
        .map(([name, call]) => [name, tree(call.target, limit - 1, visited, call.maxArgs)]));
    return {body, calls};
}

function closure(branch) {
    return [branch.body, ...Object.values(branch.calls ?? {}).flatMap(closure)];
}

function compact(branch, maxDepth) {
    if (!maxDepth) return [branch.body.token_sha256, []];
    const list = Object.entries(branch.calls ?? {}).map(([name, child]) =>
        [name, compact(child, maxDepth - 1)]);
    return [branch.body.token_sha256, list];
}

function fingerprint(name) {
    const publicDoc = document(entry);
    const exposed = exported(publicDoc, name);
    if (entry.startsWith("src/")) return {exposed, root: exposed, used: "public-module-export"};
    const sourcePath = "src/" + (name === "quantileSorted" ? "quantile" : name) + ".js";
    if (!existsSync(resolve(directory, sourcePath))) {
        if (name !== exposed.name) throw Error("no named source/public declaration for " + name);
        return {exposed, root: exposed, used: "named-public-bundle-only"};
    }
    const fromSource = exported(document(sourcePath), name === "quantileSorted" ? name : "default");
    return {exposed, root: fromSource, used: "compare"};
}

function structure(source) {
    return JSON.stringify(acorn.parse(source, options), function (key, value) {
        if (["start", "end", "loc"].includes(key) || key === "raw" && this.type === "Literal") return undefined;
        return typeof value === "bigint" ? value.toString() : value;
    });
}

function compare(root, exposed, relation, limit) {
    const candidate = tree(root, limit);
    if (relation !== "compare") return {relation, candidate};
    const map = sourceMap(entry);
    const paths = new Set(closure(candidate).map(item => item.path));
    if ([...paths].every(path => map.get(path) === text(path))) {
        return {relation: "public-binding-and-sourcesContent", candidate};
    }
    if ([...paths].every(path => typeof map.get(path) === "string" && structure(map.get(path)) === structure(text(path)))) {
        return {relation: "public-binding-and-structurally-mapped-sources", candidate};
    }
    const fromBundle = tree(exposed, limit);
    const identical = hash(JSON.stringify(compact(candidate, limit))) === hash(JSON.stringify(compact(fromBundle, limit)));
    if (!identical) throw Error("unconfirmed source/entry relation at depth " + limit);
    return {relation: "public-binding-and-exact-tokens", candidate};
}

const result = {};
for (const name of targets) {
    result[name] = {};
    for (let limit = 1; limit <= depth; ++limit) {
        try {
            const {root, exposed, used} = fingerprint(name);
            const value = compare(root, exposed, used, limit);
            result[name][limit] = {status: "resolved", ...value, public: summarize(exposed),
                signature: hash(JSON.stringify(compact(value.candidate, limit)))};
        } catch (error) {
            result[name][limit] = {status: "unknown", reason: error.message};
        }
    }
}
const reads = Object.fromEntries([...inputs].map(([path, source]) =>
    [path, {bytes: Buffer.byteLength(source), sha256: hash(source)}]));
process.stdout.write(JSON.stringify({functions: result, reads}));
