'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');

const [install, fixturePath, groupName] = process.argv.slice(2);
const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
const {input} = fixture.groups.find(group => group.group === groupName);
const requirePackage = createRequire(path.resolve(install, 'package.json'));

function snapshot(value) {
  if (typeof value === 'function') {
    return {
      type: typeof value,
      source: value.toString(),
      name: value.name,
      constructor: value.constructor.name,
      keys: Object.keys(value),
      properties: Object.fromEntries(Object.entries(value))
    };
  }
  return structuredClone(value);
}

function inputValue(input) {
  if (input.input_kind === 'arrow') return () => {};
  if (input.input_kind === 'asyncTagged') {
    const fn = async () => {};
    fn.marker = input.input_value;
    return fn;
  }
  return input.input_value;
}

function validate() {
  const Ajv = requirePackage(input.module);
  const instance = new Ajv(input.options);
  if (input.register_draft07) {
    instance.addMetaSchema(requirePackage('ajv/dist/refs/json-schema-draft-07.json'));
  }
  const data = fixture.kind === 'ajv2019' ? input.data : inputValue(input);
  const before = snapshot(data);
  let result;
  try {
    const check = instance.compile(input.schema);
    result = {phase: 'validate', valid: check(data), errors: check.errors};
  } catch (error) {
    result = {phase: 'caught_compile_or_validate', error_name: error.name, error: error.message};
  }
  const after = snapshot(data);
  return {...result, before, after, unchanged: JSON.stringify(before) === JSON.stringify(after)};
}

async function convert() {
  const jsonld = requirePackage('jsonld');
  const before = structuredClone(input.document);
  const contextBefore = structuredClone(input.context);
  const loaderCalls = [];
  const options = {
    ...input.options,
    documentLoader: async url => {
      loaderCalls.push(url);
      throw new Error('Local fixture reached an external context');
    }
  };
  const observation = {};
  if (fixture.kind === 'rdf') {
    observation.nquads = await jsonld.toRDF(input.document, options);
    const {format, ...datasetOptions} = options;
    observation.dataset = await jsonld.toRDF(input.document, datasetOptions);
  } else {
    observation.output = await jsonld.compact(input.document, input.context, options);
  }
  return {phase: 'convert', ...observation, loader_calls: loaderCalls,
          unchanged: JSON.stringify(before) === JSON.stringify(input.document),
          context_unchanged: JSON.stringify(contextBefore) === JSON.stringify(input.context)};
}

async function main() {
  const observed = fixture.kind.startsWith('ajv') ? validate() : await convert();
  const outputBytes = Buffer.from(JSON.stringify(observed), 'utf8');
  console.log(JSON.stringify({
    case: fixture.case,
    group: groupName,
    node: process.version,
    version: requirePackage(fixture.package + '/package.json').version,
    output_sha256: crypto.createHash('sha256').update(outputBytes).digest('hex'),
    observed
  }));
}

main().catch(error => {
  console.error(error.stack);
  process.exitCode = 1;
});
