// Analyze package text as data. The historical package is never loaded here.
const {readFileSync, existsSync} = require("node:fs");
const {resolve, dirname, relative} = require("node:path");
const {createHash} = require("node:crypto");
const {createRequire} = require("node:module");
const [directory, entry, parserRoot] = process.argv.slice(2);
const acorn = createRequire(resolve(parserRoot, "package-lock.json"))("acorn");
const options = {ecmaVersion: "latest", sourceType: "module", locations: true};
const targets = ["quantile", "median"];
const cache = new Map();
const hash = value => createHash("sha256").update(value).digest("hex");
const knownArrayMethods = new Set(["slice", "sort", "push", "pop", "map", "concat"]);
const knownStatic = new Set(["Array.isArray", "Math.ceil", "Math.floor", "Number.isInteger"]);
const knownGlobals = new Set(["Error", "TypeError", "RangeError"]);

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

function document(path) {
    if (cache.has(path)) return cache.get(path);
    const text = readFileSync(resolve(directory, path), "utf8");
    const ast = acorn.parse(text, options);
    const value = {path, text, ast, declarations: new Map(), imports: new Map(), published: new Map()};
    walk(ast, node => {
        if (node.type === "FunctionDeclaration" && node.id) {
            const name = node.id.name;
            const previous = value.declarations.get(name) ?? [];
            previous.push(node);
            value.declarations.set(name, previous);
        }
        if (node.type === "ImportDeclaration") {
            for (const specifier of node.specifiers) {
                value.imports.set(specifier.local.name, {
                    from: node.source.value,
                    name: specifier.imported?.name ?? "default"
                });
            }
        }
        if (node.type === "VariableDeclarator" && node.id.type === "Identifier") {
            if (["FunctionExpression", "ArrowFunctionExpression"].includes(node.init?.type)) {
                const previous = value.declarations.get(node.id.name) ?? [];
                previous.push(node.init);
                value.declarations.set(node.id.name, previous);
            }
            const call = node.init;
            if (call?.type === "CallExpression" && call.callee.name === "require" &&
                typeof call.arguments[0]?.value === "string") {
                value.imports.set(node.id.name, {from: call.arguments[0].value, name: "default"});
            }
        }
        if (node.type === "AssignmentExpression" && node.left.type === "MemberExpression" &&
            node.left.object.name === "exports" && !node.left.computed && node.right.type === "Identifier") {
            value.published.set(node.left.property.name, node.right.name);
        }
        if (node.type === "ExportNamedDeclaration") {
            for (const specifier of node.specifiers) value.published.set(specifier.exported.name, specifier.local.name);
            if (node.declaration?.id) value.published.set(node.declaration.id.name, node.declaration.id.name);
        }
        if (node.type === "ExportDefaultDeclaration") value.published.set("default", node.declaration.name ?? node.declaration.id?.name);
    });
    cache.set(path, value);
    return value;
}

function binding(doc, name) {
    const candidates = doc.declarations.get(name) ?? [];
    if (candidates.length === 1 && !doc.imports.has(name)) return {doc, node: candidates[0], name};
    if (candidates.length || !doc.imports.has(name)) throw Error(`unresolved binding ${doc.path}#${name}`);
    const specifier = doc.imports.get(name);
    if (!specifier.from.startsWith(".")) throw Error(`unresolved external call ${specifier.from}#${specifier.name}`);
    const base = resolve(directory, dirname(doc.path), specifier.from);
    const candidate = [base, base + ".js"].find(path => path.endsWith(".js") && existsSync(path));
    if (!candidate) throw Error(`missing delegate ${specifier.from}`);
    const imported = document(relative(directory, candidate));
    const exported = imported.published.get(specifier.name);
    if (!exported) throw Error(`unresolved export ${imported.path}#${specifier.name}`);
    return binding(imported, exported);
}

function summarize({doc, node, name}) {
    const body = doc.text.slice(node.body.start, node.body.end);
    const tokens = [...acorn.tokenizer(body, options)].map(token => [
        token.type.label, typeof token.value === "bigint" ? token.value.toString() : token.value ?? null
    ]);
    return {name, path: doc.path, lines: [node.loc.start.line, node.loc.end.line],
        raw_sha256: hash(body), token_sha256: hash(JSON.stringify(tokens)), token_count: tokens.length};
}

function direct(root) {
    const delegates = new Map();
    const arrays = new Set(root.node.params.filter(node => node.type === "Identifier" && /^x$/.test(node.name)).map(node => node.name));
    walk(root.node.body, node => {
        if (/^(?:Function|ArrowFunction)/.test(node.type)) return false;
        if (node.type === "VariableDeclarator" && node.id.type === "Identifier" &&
            (node.init?.type === "ArrayExpression" ||
             (node.init?.type === "CallExpression" && node.init.callee.property?.name === "slice" &&
              arrays.has(node.init.callee.object?.name)))) arrays.add(node.id.name);
        if (!["CallExpression", "NewExpression"].includes(node.type)) return;
        const callee = node.callee;
        if (callee.type === "Identifier" && !knownGlobals.has(callee.name)) {
            if (root.node.params.some(parameter => parameter.name === callee.name)) throw Error(`dynamic parameter ${callee.name}`);
            delegates.set(callee.name, summarize(binding(root.doc, callee.name)));
        } else if (callee.type === "MemberExpression" && !callee.computed) {
            const object = callee.object.name;
            const method = callee.property.name;
            if (!knownStatic.has(`${object}.${method}`) && !(arrays.has(object) && knownArrayMethods.has(method))) {
                throw Error(`unresolved member call ${object}.${method}`);
            }
        } else if (callee.type !== "Identifier") {
            throw Error(`unresolved dynamic call ${callee.type}`);
        }
    });
    return Object.fromEntries([...delegates.entries()].sort(([left], [right]) => left.localeCompare(right, "en")));
}

function sourceMap(entryDocument) {
    const filename = resolve(directory, entryDocument.path + ".map");
    if (!existsSync(filename)) return new Map();
    const map = JSON.parse(readFileSync(filename, "utf8"));
    return new Map(map.sources.map((path, index) => [
        relative(directory, resolve(directory, dirname(entryDocument.path), path)), map.sourcesContent?.[index]
    ]));
}

function fingerprint(name) {
    const publicDoc = document(entry);
    const published = publicDoc.published.get(name);
    if (!published) throw Error(`unresolved public export ${entry}#${name}`);
    const publicFunction = binding(publicDoc, published);
    const publicBody = summarize(publicFunction);
    const path = `src/${name}.js`;
    if (!existsSync(resolve(directory, path))) {
        if (name !== publicFunction.name) throw Error(`no named declaration for ${name}`);
        return {status: "resolved", relation: "public-bundle-only", root: publicBody, public: publicBody,
            delegates: direct(publicFunction)};
    }
    const implementation = document(path);
    const source = binding(implementation, name);
    if (implementation.published.get("default") !== name && implementation.published.get(name) !== name) {
        throw Error(`unresolved packaged source export ${path}`);
    }
    const root = summarize(source);
    const delegates = direct(source);
    const map = sourceMap(publicDoc);
    const mapped = [root, ...Object.values(delegates)].every(item =>
        map.get(item.path) === document(item.path).text
    );
    const bodyExact = !mapped && root.token_sha256 === publicBody.token_sha256 &&
        Object.entries(delegates).every(([key, item]) =>
            item.token_sha256 === summarize(binding(publicDoc, key)).token_sha256
        );
    const relation = mapped ? "public-binding-and-sourcesContent" : bodyExact ? "public-binding-and-exact-body-tokens" : "unresolved";
    return {status: relation === "unresolved" ? "unknown" : "resolved", relation, root, public: publicBody, delegates,
        map_path: mapped ? entry + ".map" : null, reason: relation === "unresolved" ? "unconfirmed source/entry relation" : null};
}

const result = {};
for (const name of targets) {
    try {
        result[name] = fingerprint(name);
    } catch (error) {
        result[name] = {status: "unknown", reason: error.message};
    }
}
process.stdout.write(JSON.stringify(result));
