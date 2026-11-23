#!/usr/bin/env node
// AF-RES-090: CSV only. The user's owned_path overrides skill temp/output defaults.
// Resolve the public artifact-tool package from the primary runtime without
// installing dependencies or creating a node_modules link inside the checkout.
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
if (!runtimeModules) throw new Error('CODEX_PRIMARY_RUNTIME_NODE_MODULES is required');
const runtimeRequire = createRequire(path.join(runtimeModules, '..', 'package.json'));
const { Workbook } = await import(pathToFileURL(runtimeRequire.resolve('@oai/artifact-tool')).href);
if (process.argv.includes('--help-csv')) {
  const workbook = Workbook.create();
  console.log(workbook.help('CSV export', { search: 'csv|CSV', include: 'index,examples,notes', maxChars: 5500 }).ndjson);
  process.exit(0);
}

const base = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const prefix = 'docs/workstreams/research/AF-RES-090/';
const freezeCommit = 'c2a3f387cc962abd1ef383e39f750cc23ee5e51a';
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const readJSON = async rel => JSON.parse(await fs.readFile(path.join(base, rel), 'utf8'));
const readJSONL = async rel => (await fs.readFile(path.join(base, rel), 'utf8')).trim().split('\n').filter(Boolean).map(JSON.parse);
const text = value => value == null ? '' : typeof value === 'string' ? value : typeof value === 'object' ? JSON.stringify(value) : String(value);
const equalMatrix = (actual, expected, label) => {
  assert.equal(actual.length, expected.length, `${label}: row count`);
  for (let row = 0; row < expected.length; row++) {
    assert.equal(actual[row].length, expected[row].length, `${label}: column count row ${row}`);
    for (let col = 0; col < expected[row].length; col++) {
      if (actual[row][col] !== expected[row][col]) throw new Error(`${label} row ${row} col ${col}: ${JSON.stringify(actual[row][col]).slice(0,250)} != ${JSON.stringify(expected[row][col]).slice(0,250)}`);
    }
  }
};
const relative = value => {
  if (!value) return '';
  let result = value;
  if (path.isAbsolute(result)) result = path.relative(base, result);
  if (result.startsWith(prefix)) result = result.slice(prefix.length);
  assert(!path.isAbsolute(result) && !result.startsWith('..'), `Out-of-scope path: ${value}`);
  return result;
};
const jsonText = value => JSON.stringify(value);
const inputPaths = ['streams/python/targets.json', 'streams/python/traversals.json', 'streams/python/sources.jsonl', 'streams/python/freeze.json', 'streams/r/targets.json', 'streams/r/traversals.json', 'streams/r/sources.jsonl', 'streams/r/freeze.json', 'streams/ui/freeze.json'];
const inputHashes = Object.fromEntries(await Promise.all(inputPaths.map(async rel => [rel, digest(await fs.readFile(path.join(base, rel)))])));
const [pyTargets, pyTraversals, pySources, pyFreeze, rTargets, rWrapper, rSources, rFreeze] = await Promise.all([
  readJSON(inputPaths[0]), readJSON(inputPaths[1]), readJSONL(inputPaths[2]), readJSON(inputPaths[3]),
  readJSON(inputPaths[4]), readJSON(inputPaths[5]), readJSONL(inputPaths[6]), readJSON(inputPaths[7]),
]);
const rTraversals = rWrapper.traversals;
assert.equal(rWrapper.freeze_commit, freezeCommit);
assert(pyTraversals.every(row => row.candidate_freeze_commit === freezeCommit));
for (const row of rTraversals.filter(row => row.target_id === 'R2-next')) {
  assert.equal(row.followup_resource, 'no_explicit_path', 'Wait for final R2 SVG-path correction before building CSV');
  assert.equal(row.static_output, 'confirmed');
  assert.equal(row.strict_followup_success, false);
}
const allSources = [...pySources, ...rSources];
const sources = new Map(allSources.map(row => [row.source_id, row]));
assert.equal(sources.size, allSources.length, 'Source IDs must be unique');
const projects = { P3: 'cibuildwheel', P1: 'bandersnatch', R1: 'archive', R2: 'asciicast' };
const targetColumns = ['purpose_id','project','reader','publisher_promise','research_condition','target_version','target_section','basis_source_ids','basis_urls','start_a','start_b','sealed_next_resource','anchor','selection_rule','selection_evidence','success_criterion','unconfirmed','freeze_commit'];
const pyRules = {
  'P3-body': '지정된 3.3.0 enable 절을 고정. A는 실관측 버전 메뉴 v3.3.0, B는 입구 본문.',
  'P3-next': '고정 README가 Python 2 등에게 명시한 1.x root 지원표를 고정. 메뉴의 /1.x/options/ 표로 대체하지 않음.',
  'P1-body': '7.0.1 사용 설명의 첫 설정 예제 Mirror Configuration > Examples > Minmal L13–39. index의 CLI synopsis는 설정 예제 아님.',
  'P1-next': 'Minmal 첫 코드 블록의 소스 순서상 첫 동작 URI L23 master=https://pypi.org. 뒤 filtering 링크로 대체하지 않음.',
};
const targets = [
  ...pyTargets.map(row => ({
    purpose_id: row.purpose_id, project: projects[row.case_id], reader: row.reader,
    publisher_promise: row.publisher_promise, research_condition: row.research_condition,
    target_version: row.target_version, target_section: row.target_section,
    basis_source_ids: row.source_ids,
    basis_urls: row.source_ids.map(id => { assert(sources.has(id)); return sources.get(id).original_url; }),
    start_a: row.starts.A, start_b: row.starts.B, sealed_next_resource: row.sealed_next_resource,
    anchor: row.anchor, selection_rule: pyRules[row.purpose_id],
    selection_evidence: {
      path: 'streams/python/freeze.json', pointer: `/targets/${pyTargets.indexOf(row)}`, frozen_utc: pyFreeze.frozen_utc,
      candidate_second_views: row.candidate_second_views, candidate_link: row.candidate_link ?? null,
      raw_uri: row.raw_uri ?? null, uri_source_line: row.uri_source_line ?? null,
      example_code_sha256: row.example_code_sha256 ?? null,
      excluded_candidates: row.excluded_candidates ?? [],
      browser_menu_receipt: row.case_id === 'P3' ? 'streams/ui/freeze.json' : null,
    },
    success_criterion: row.success_criterion, unconfirmed: row.unconfirmed, freeze_commit: freezeCommit,
  })),
  ...rTargets.map(row => ({
    purpose_id: row.target_id, project: projects[row.case_id],
    reader: row.case_id === 'R1' ? (row.purpose === 'body' ? 'archive 1.1.12 archive_read 사용법과 예제를 읽는 독자' : 'archive_read 예제의 첫 동작 참조 system.file을 확인할 독자') : (row.purpose === 'body' ? 'asciicast 2.3.1 init_knitr_engine와 Using SVG files를 읽는 독자' : 'Using SVG files의 첫 SVG·재생 자원 또는 내장 데이터를 확인할 독자'),
    publisher_promise: row.owner_promise, research_condition: row.research_condition,
    target_version: row.target_version, target_section: row.section,
    basis_source_ids: row.basis_source_ids,
    basis_urls: row.basis_source_ids.map(id => { assert(sources.has(id)); return sources.get(id).original_url; }),
    start_a: row.start_a, start_b: row.start_b, sealed_next_resource: row.frozen_next_uri,
    anchor: row.selection_detail.section,
    selection_rule: row.purpose === 'body' ? '고정 생성 HTML의 지정 본문 절을 읽음.' : (row.case_id === 'R1' ? row.selection_detail.selection : 'Using SVG files 안의 첫 SVG·재생 자원 또는 내장 payload. 명시 경로 부재와 정적 preformatted 출력은 별도 판정.'),
    selection_evidence: { path: 'streams/r/freeze.json', pointer: `/${row.case_id}`, frozen_utc: rFreeze.frozen_utc, ...row.selection_detail, ...(row.target_id === 'R2-next' ? { prior_success_criterion: row.success_criterion, interpretation_adjustment: 'streams/r/evidence/R-coding-adjustment.json' } : {}) },
    success_criterion: row.target_id === 'R2-next' ? '실제 SVG/재생 payload 확인이 엄격 성공; static_output은 별도 보조 확인' : row.success_criterion,
    unconfirmed: row.unconfirmed + (row.target_id === 'R2-next' ? '; SVG/replay no_explicit_path; inline static output does not prove SVG or execution' : ''),
    freeze_commit: freezeCommit,
  })),
];
const viewColumns = n => [`view_${n}_source_id`,`view_${n}_requested_url`,`view_${n}_final_url`,`view_${n}_status`,`view_${n}_mime`,`view_${n}_receipt`,`view_${n}_bytes`,`view_${n}_sha256`,`view_${n}_started_utc`,`view_${n}_retrieved_utc`,`view_${n}_redirects`,`view_${n}_kind`];
const traversalColumns = ['traversal_id','purpose_id','project','route',...viewColumns(1),...viewColumns(2),'view_count','response_body_bytes','final_url','final_title','click_action','manual_uri_copy','manual_path_reconstruction','manual_uri_copy_required','manual_path_reconstruction_required','first_target_body','target_body','followup_resource','same_version','version_subject','static_output','svg_or_replay_status','strict_success','last_version','sealed_next_resource','source_ids','source_record','freeze_commit','method','observations','limitations','next_minimum_observation'];
const pyActions = row => row.views.map((view, index) => ({
  view: index + 1,
  action: index === 0 ? 'open given entry' : row.purpose_id === 'P3-body' ? 'open ReadTheDocs shadow DOM version menu; follow v3.3.0 href' : row.case_id === 'P3' ? 'open ReadTheDocs shadow DOM version menu; follow 1.x href' : 'follow Mirror Configuration link; read #minmal in same document',
  menu_document_views: 0,
}));
const pyVersionSubject = row => row.purpose_id === 'P3-next' ? '목적지 1.x 계열 판 확인. 1.x는 본문 목표 3.3.0과 다른 판이며, same_version=confirmed는 1.x 목적판을 가리킴. 지정 root 지원표 도달은 unconfirmed.' : row.purpose_id === 'P1-next' ? '7.0.1 예제가 지목한 외부 PyPI endpoint. endpoint 자체는 unversioned이고 두 열람 안에 열지 못함.' : `지정 본문판 ${row.case_id === 'P3' ? '3.3.0' : '7.0.1'}`;
const normalized = [
  ...pyTraversals.map(row => ({
    input: row, steps: row.views,
    data: {
      traversal_id: row.traversal_id, purpose_id: row.purpose_id, project: projects[row.case_id], route: row.route,
      view_count: row.view_count, response_body_bytes: row.total_response_body_bytes,
      final_url: row.final_url, final_title: row.final_title, click_action: pyActions(row),
      manual_uri_copy: false, manual_path_reconstruction: row.manual_reconstruction,
      manual_uri_copy_required: row.purpose_id === 'P1-next' && row.route === 'A', manual_path_reconstruction_required: false,
      first_target_body: row.first_target_body_status, target_body: row.target_body,
      followup_resource: row.followup_resource, same_version: row.same_version,
      version_subject: pyVersionSubject(row), static_output: 'not_applicable', svg_or_replay_status: 'not_applicable',
      strict_success: row.strict_target_reached, last_version: row.last_version,
      sealed_next_resource: row.sealed_target_url, source_ids: row.source_ids,
      source_record: `streams/python/traversals.json#/${pyTraversals.indexOf(row)}`,
      freeze_commit: row.candidate_freeze_commit, method: row.method, observations: row.observations,
      limitations: row.limitations + (row.purpose_id === 'P3-next' ? '; ' + row.version_relation : '') + (row.purpose_id === 'P1-next' && row.route === 'A' ? '; master URI는 문자값. 다음 열람에는 URI 복사가 필요하지만 실제 주 판독에서는 수행하지 않았음. 경로 수동 조립은 필요 없음.' : ''),
      next_minimum_observation: row.purpose_id === 'P3-next' ? '추가 한 문서로 https://cibuildwheel.pypa.io/en/1.x/ root 지원표. 현재 두 열람 분모 밖.' : row.purpose_id === 'P1-next' ? '고정 7.0.1 설정 예제에서 literal https://pypi.org를 추가 열람; endpoint의 판 귀속은 별도 미확인.' : row.target_body === 'confirmed' ? '본문 확인 범위 완료. 예제 실행은 별도 조건·환경 필요.' : '지정 7.0.1 서비스 입구의 본문이 실제 200으로 열리는 새 UTC 관측; 현재 판독 대체 금지.',
    },
  })),
  ...rTraversals.map(row => ({
    input: row, steps: row.steps,
    data: {
      traversal_id: row.traversal_id, purpose_id: row.target_id, project: projects[row.case_id], route: row.route,
      view_count: row.views, response_body_bytes: row.direct_response_bytes,
      final_url: row.final_url, final_title: row.steps.at(-1).title,
      click_action: row.steps.map((step,index) => ({ view: index + 1, action: step.reader_action })),
      manual_uri_copy: row.manual_uri_copy, manual_path_reconstruction: row.manual_path_reconstruction,
      manual_uri_copy_required: false, manual_path_reconstruction_required: false,
      first_target_body: row.target_body, target_body: row.target_body,
      followup_resource: row.followup_resource, same_version: row.same_version,
      version_subject: row.same_version_subject ?? (row.purpose === 'body' ? `지정 본문판 ${row.target_version}` : 'archive 1.1.12 예제의 외부 R base system.file 참조판. 외부 URI는 R 판을 고정하지 않으며 본문판 확인과 별도.'),
      static_output: row.static_output, svg_or_replay_status: row.svg_or_replay_status,
      strict_success: row.purpose === 'body' ? row.target_body === 'confirmed' && row.same_version === 'confirmed' : row.strict_followup_success ?? (row.target_body === 'confirmed' && row.followup_resource === 'confirmed' && row.same_version === 'confirmed'),
      last_version: row.entry_version, sealed_next_resource: rTargets.find(target => target.target_id === row.target_id).frozen_next_uri,
      source_ids: row.steps.map(step => step.source_id),
      source_record: `streams/r/traversals.json#/traversals/${rTraversals.indexOf(row)}`,
      freeze_commit: rWrapper.freeze_commit, method: row.method, observations: row.observations,
      limitations: [...row.unconfirmed, ...(row.failure ? [row.failure] : []), ...(row.target_id === 'R2-next' ? ['static_output=confirmed는 HTML 안 정적 출력만 뜻함. followup_resource=no_explicit_path이며 SVG·재생 payload·실행 성공이 아님.'] : [])],
      next_minimum_observation: row.minimum_next_observation,
    },
  })),
];
let receiptChecks = 0;
let rawChecks = 0;
const receiptEvidence = [];
for (const item of normalized) {
  assert.equal(item.data.view_count, item.steps.length);
  assert(item.steps.length >= 1 && item.steps.length <= 2);
  assert.equal(item.data.response_body_bytes, item.steps.reduce((sum, step) => sum + step.body_bytes, 0));
  for (let index = 0; index < 2; index++) {
    const step = item.steps[index];
    if (!step) { for (const column of viewColumns(index + 1)) item.data[column] = ''; continue; }
    const source = sources.get(step.source_id); assert(source, `Missing source ${step.source_id}`);
    const receiptPath = relative(step.receipt_path ?? source.receipt_path);
    const receipt = await readJSON(receiptPath);
    for (const key of ['source_id','requested_url','final_url','status','content_type','body_bytes','sha256','started_utc','retrieved_utc']) assert.equal(step[key], receipt[key], `${step.source_id}.${key}`);
    assert.equal(source.original_url, step.requested_url);
    for (const key of ['body_bytes','sha256']) assert.equal(source.fingerprint[key], step[key]);
    const rawPath = path.join(path.dirname(path.join(base, receiptPath)), 'raw', `${step.source_id}.bin`);
    let rawRehashed = false;
    try { const raw = await fs.readFile(rawPath); assert.equal(raw.length, step.body_bytes); assert.equal(digest(raw), step.sha256); rawChecks++; rawRehashed = true; }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
    receiptChecks++;
    receiptEvidence.push({source_id:step.source_id,receipt:receiptPath,sha256:step.sha256,bytes:step.body_bytes,raw_rehashed:rawRehashed});
    const n = index + 1;
    Object.assign(item.data, {
      [`view_${n}_source_id`]: step.source_id, [`view_${n}_requested_url`]: step.requested_url,
      [`view_${n}_final_url`]: step.final_url, [`view_${n}_status`]: step.status,
      [`view_${n}_mime`]: step.content_type, [`view_${n}_receipt`]: receiptPath,
      [`view_${n}_bytes`]: step.body_bytes, [`view_${n}_sha256`]: step.sha256,
      [`view_${n}_started_utc`]: step.started_utc, [`view_${n}_retrieved_utc`]: step.retrieved_utc,
      [`view_${n}_redirects`]: step.redirects,
      [`view_${n}_kind`]: step.status >= 400 ? 'error_response' : step.view_kind ?? 'rendered_document_html',
    });
  }
}
const traversals = normalized.map(item => item.data);
assert.equal(targets.length, 8); assert.equal(traversals.length, 16);
assert.equal(new Set(targets.map(row => row.purpose_id)).size, 8);
assert.equal(new Set(traversals.map(row => row.traversal_id)).size, 16);
for (const target of targets) {
  const pair = traversals.filter(row => row.purpose_id === target.purpose_id);
  assert.deepEqual(pair.map(row => row.route).sort(), ['A','B']);
  assert.equal(pair.find(row => row.route === 'A').view_1_requested_url, target.start_a);
  assert.equal(pair.find(row => row.route === 'B').view_1_requested_url, target.start_b);
}
const statusValues = new Set(['confirmed','refuted','unconfirmed','inaccessible','no_explicit_path','not_applicable']);
for (const row of traversals) for (const column of ['first_target_body','target_body','followup_resource','same_version','static_output','svg_or_replay_status']) assert(statusValues.has(row[column]), `${row.traversal_id}.${column}`);
assert.equal(traversals.filter(row => row.strict_success).length, 3);
assert.equal(traversals.find(row => row.traversal_id === 'P3-body-A').first_target_body, 'refuted');
assert.equal(traversals.find(row => row.traversal_id === 'P3-body-A').target_body, 'confirmed');
for (const row of traversals.filter(row => row.purpose_id === 'P3-next')) { assert.equal(row.followup_resource, 'unconfirmed'); assert(row.version_subject.includes('1.x는 본문 목표 3.3.0과 다른 판')); }
for (const row of traversals.filter(row => row.purpose_id === 'R2-next')) { assert.equal(row.followup_resource, 'no_explicit_path'); assert.equal(row.static_output, 'confirmed'); assert.equal(row.strict_success, false); }

const workbook = Workbook.create();
const csvQuote = value => /[",\r\n]/.test(value) ? `"${value.replaceAll('"','""')}"` : value;
const parseCSV = csv => {
  const rows = []; let row = [], field = '', quoted = false;
  for (let index = 0; index < csv.length; index++) {
    const char = csv[index];
    if (quoted) {
      if (char === '"' && csv[index + 1] === '"') { field += '"'; index++; }
      else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"') { assert.equal(field, ''); quoted = true; }
    else if (char === ',') { row.push(field); field = ''; }
    else if (char === '\r' || char === '\n') {
      if (char === '\r' && csv[index + 1] === '\n') index++;
      row.push(field); rows.push(row); row = []; field = '';
    } else field += char;
  }
  assert.equal(quoted, false, 'Unclosed CSV quote');
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
};
const outputs = [];
for (const [name, columns, rows] of [['targets', targetColumns, targets], ['traversals', traversalColumns, traversals]]) {
  const matrix = [columns, ...rows.map(row => columns.map(column => text(row[column])))];
  const sheet = workbook.worksheets.add(name);
  const range = sheet.getRangeByIndexes(0, 0, matrix.length, columns.length);
  range.setNumberFormat('@');
  range.values = matrix;
  workbook.recalculate();
  const authored = range.values.map(row => row.map(text));
  equalMatrix(authored, matrix, `${name}: artifact-tool write/read equality`);
  // Public documentation and one targeted help query did not expose CSV export.
  // CSV is a serialization boundary: serialize the artifact-tool-authored cells,
  // Native RFC4180 readback preserves every original UTC digit. fromCSV is also
  // inspected, but auto-detects ISO dates and truncates microseconds to milliseconds.
  const csv = authored.map(row => row.map(csvQuote).join(',')).join('\n') + '\n';
  const imported = await Workbook.fromCSV(csv, { sheetName: name });
  const importedRaw = imported.worksheets.getItem(name).getRangeByIndexes(0,0,matrix.length,columns.length).values;
  const dateCoercions = [];
  const importedValues = importedRaw.map((row, rowIndex) => row.map((value, columnIndex) => {
    const expected = matrix[rowIndex][columnIndex];
    if (value instanceof Date) {
      assert(/^\d{4}-\d{2}-\d{2}T/.test(expected), 'Unexpected inferred date outside UTC source field');
      assert.equal(value.getTime(), Date.parse(expected), 'Artifact date conversion changed epoch milliseconds');
      dateCoercions.push({row:rowIndex,column:columns[columnIndex],original:expected,artifact_value:value.toISOString(),source_csv_preserved:true});
      return expected;
    }
    return text(value);
  }));
  equalMatrix(importedValues, matrix, `${name}: artifact reimport, explicitly accounting for date coercion`);
  const formulas = await imported.inspect({ kind: 'formula', sheetId: name, range: imported.worksheets.getItem(name).getRangeByIndexes(0,0,matrix.length,columns.length).address, maxChars: 1200, options: { maxResults: 5 } });
  await fs.writeFile(path.join(base, `${name}.csv`), csv, 'utf8');
  const saved = await fs.readFile(path.join(base, `${name}.csv`));
  assert.equal(saved.toString('utf8'), csv);
  equalMatrix(parseCSV(saved.toString('utf8')), matrix, `${name}: exact saved CSV all-cell roundtrip`);
  outputs.push({path:`${name}.csv`,rows:rows.length,columns:columns.length,bytes:saved.length,sha256:digest(saved),all_csv_cells_equal:true,artifact_import_date_coercions:dateCoercions,formula_inspection:formulas.ndjson ?? formulas});
}
const inspection = await workbook.inspect({ kind:'sheet', include:'id,name', maxChars:1500 });
for (const [rel, sha] of Object.entries(inputHashes)) assert.equal(digest(await fs.readFile(path.join(base, rel))), sha, `Input changed during build: ${rel}`);
const counts = key => Object.fromEntries([...statusValues].map(value => [value, traversals.filter(row => row[key] === value).length]));
const verification = {
  status:'PASS', completed_utc:new Date().toISOString(), builder:'tools/build_csv.mjs',
  command:'"$CODEX_PRIMARY_RUNTIME_NODE" docs/workstreams/research/AF-RES-090/tools/build_csv.mjs',
  runtime_node:process.execPath, authoring_library:'@oai/artifact-tool (primary runtime)',
  scope:'Only targets.csv, traversals.csv, tools/build_csv.mjs and evidence/csv-verification.json are written. No XLSX/workbook extra artifact.',
  serialization_boundary:'Artifact-tool block writes with text format @ and exact cell reads; RFC4180 field escaping with repository-required LF record separators and exact all-cell readback. Public CSV-export help query matched 0 entries. Documented Workbook.fromCSV separately checked all non-date cells and date epoch milliseconds; its automatic Date conversion loses original microsecond formatting, so the actual CSV/native readback is authoritative for exact UTC strings. No alternate spreadsheet authoring library.',
  formula_policy:'Source observations are literal cells. No formulas or calculated evidence values introduced; JSON arrays/objects are serialized inside CSV fields.',
  visual_review:'CSV is a flat machine-readable ledger with no visual formatting; no XLSX or PNG artifact requested or created.',
  missing_value_policy:'Blank view_2 fields mean no second document opened. Blank sealed_next_resource is not itself a success; no_explicit_path/not_applicable remain explicit outcome categories.',
  bytes_policy:'Decoded response entity bytes including repeated independent GETs and error bodies; excludes headers/TLS/browser asset requests. Human time unmeasured.',
  freeze_commit:freezeCommit, input_sha256:inputHashes, outputs,
  denominators:{targets:targets.length,traversals:traversals.length,pairs:targets.length,http_document_reads:receiptChecks,response_body_bytes:traversals.reduce((sum,row)=>sum+row.response_body_bytes,0),strict_success:traversals.filter(row=>row.strict_success).length},
  axes:{target_body:counts('target_body'),followup_resource:counts('followup_resource'),same_version:counts('same_version'),static_output:counts('static_output')},
  checks:{unique_purpose_ids:true,unique_traversal_ids:true,each_purpose_has_A_B:true,entry_urls_match_target_contract:true,max_two_views:true,all_response_totals_match:true,all_source_ids_resolve:true,receipts_match_fields:true,all_paths_AF090_relative:true,all_csv_cells_roundtrip:true,inputs_unchanged_during_build:true,p3_first_screen_refuted_then_recovered:true,p3_1x_separate_destination_version:true,r2_static_output_separate_from_no_svg_path:true,no_auxiliary_read_promoted:true},
  receipt_checks:receiptChecks,raw_response_rehash_checks:rawChecks,receipt_evidence:receiptEvidence,
  artifact_tool_inspection:inspection.ndjson ?? inspection,
};
await fs.writeFile(path.join(base,'evidence/csv-verification.json'), JSON.stringify(verification,null,2)+'\n','utf8');
console.log(JSON.stringify({status:verification.status,...verification.denominators,receipt_checks:receiptChecks,raw_response_rehash_checks:rawChecks,outputs:outputs.map(({path,rows,columns,sha256})=>({path,rows,columns,sha256}))}));
