'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const util = require('node:util');

const checkout = path.resolve(process.argv[2]);
const jsonld = require(checkout);
const JsonLdError = require(path.join(checkout, 'lib', 'JsonLdError.js'));

function describeError(error) {
  console.error(util.inspect(error, {depth: null, maxArrayLength: null, maxStringLength: null}));
  const seen = new Set();
  let current = error;
  while (current && !seen.has(current)) {
    seen.add(current);
    if (typeof current.details?.code === 'string') {
      return {
        kind: 'jsonld_error',
        code: current.details.code,
        name: error.name,
        message: error.message
      };
    }
    current = current.details?.cause;
  }
  return {
    kind: 'infrastructure_error',
    name: error.name,
    message: error.message,
    engineErrorClass: error instanceof JsonLdError
  };
}

async function observe(operation) {
  try {
    return {kind: 'json', value: await operation()};
  } catch (error) {
    return describeError(error);
  }
}

async function main() {
  const req = JSON.parse(fs.readFileSync(0, 'utf8'));
  const loads = [];
  function read(ref, mechanism) {
    const item = {document_iri: ref.document_iri, path: ref.path, mechanism, status: 'failed'};
    loads.push(item);
    const raw = fs.readFileSync(path.join(req.suite_root, ref.path));
    item.sha256 = crypto.createHash('sha256').update(raw).digest('hex');
    if (item.sha256 !== ref.sha256) {
      throw new Error('Unexpected SHA-256 for ' + ref.path);
    }
    const document = JSON.parse(raw);
    item.status = 'read';
    return document;
  }
  async function documentLoader(iri) {
    if (iri !== req.input.document_iri) {
      loads.push({document_iri: iri, mechanism: 'processor_loader', status: 'unmapped'});
      throw new Error('Unmapped document IRI: ' + iri);
    }
    return {
      documentUrl: iri,
      contextUrl: null,
      contentType: 'application/ld+json',
      document: read(req.input, 'processor_loader')
    };
  }
  const options = {base: req.base, processingMode: req.processing_mode, documentLoader};
  let actual;
  if (req.algorithm === 'expand') {
    actual = await observe(() => jsonld.expand(req.input.document_iri, options));
  } else if (req.algorithm === 'compact') {
    actual = await observe(() => jsonld.compact(
      req.input.document_iri, read(req.context, 'local_context_argument'),
      {...options, compactArrays: true}
    ));
  } else {
    throw new Error('Unknown algorithm: ' + req.algorithm);
  }
  let postExpansion = null;
  if (actual.kind === 'json' && req.reexpand) {
    postExpansion = {
      actual: await observe(() => jsonld.expand(actual.value, options)),
      expected: await observe(() => jsonld.expand(req.expected, options))
    };
  }
  process.stdout.write(JSON.stringify({
    protocol: 1, nonce: req.nonce, pid: process.pid, runtime: process.version,
    actual, loads, post_expansion: postExpansion
  }) + '\n');
}

main().catch(error => {
  describeError(error);
  process.exitCode = 2;
});
