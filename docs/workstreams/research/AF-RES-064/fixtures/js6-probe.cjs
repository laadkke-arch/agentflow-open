// Prepared but not executed in AF-RES-060. Requires an independently verified pinned Ajv module.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
if (process.argv.length !== 3) throw new Error('Pass absolute path to the verified Ajv dist/ajv.js');
const modulePath = path.resolve(process.argv[2]);
const imported = require(modulePath);
const Ajv = imported.default || imported;
const input = JSON.parse(fs.readFileSync(path.join(__dirname, 'js6-fixtures.json'), 'utf8'));
const ajv = new Ajv({allErrors: true, coerceTypes: false, useDefaults: false, removeAdditional: false});
const validate = ajv.compile(input.schema);
const result = [];
for (const fixture of input.fixtures) {
  const data = JSON.parse(JSON.stringify(fixture.input));
  const before = JSON.stringify(data);
  const actual = validate(data);
  const unchanged = before === JSON.stringify(data);
  result.push({id: fixture.id, expected_valid: fixture.expected_valid, actual_valid: actual, unchanged, errors: validate.errors});
  assert.equal(actual, fixture.expected_valid, fixture.id);
  assert.ok(unchanged, fixture.id + ': input mutated');
}
process.stdout.write(JSON.stringify({case_id: input.case_id, module_path: modulePath, observed_utc: new Date().toISOString(), execution_scope: 'future extra-budget researcher fixture; not original-user success', result}, null, 2) + '\n');
