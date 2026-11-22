import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const taskRequire = createRequire(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/__resolve__.js');
const { Workbook } = await import(taskRequire.resolve('@oai/artifact-tool'));
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const tables = JSON.parse(await fs.readFile(path.join(root, 'evidence/table-data.json'), 'utf8'));
const workbook = Workbook.create();
const checks = [];
const columnName = n => { let result = ''; while (n > 0) { n--; result = String.fromCharCode(65 + n % 26) + result; n = Math.floor(n / 26); } return result; };
const csvCell = value => '"' + String(value ?? '').replaceAll('"', '""') + '"';

for (const [name, rows] of Object.entries(tables)) {
  if (rows.length === 0) throw new Error('Empty table: ' + name);
  const headers = Object.keys(rows[0]);
  const matrix = [headers, ...rows.map(row => headers.map(header => String(row[header] ?? '미확인')))];
  const sheet = workbook.worksheets.add(name);
  const address = `A1:${columnName(headers.length)}${matrix.length}`;
  sheet.getRange(address).setNumberFormat('@');
  sheet.getRange(address).values = matrix;
  const observed = sheet.getRange(address).values;
  if (JSON.stringify(observed) !== JSON.stringify(matrix)) throw new Error('Grid round-trip mismatch: ' + name);
  // CSV export was not documented by either bounded help lookup. Serialize the
  // documented grid values directly, preserving literal text and UTF-8 content.
  const csv = observed.map(row => row.map(csvCell).join(',')).join('\n') + '\n';
  const imported = await Workbook.fromCSV(csv, { sheetName: name });
  const back = imported.worksheets.getItem(name).getRange(address).values;
  let importTimestampCoercions = 0;
  for (let r = 0; r < matrix.length; r++) for (let c = 0; c < headers.length; c++) {
    const actual = back[r][c];
    if (actual instanceof Date && actual.toISOString() === new Date(matrix[r][c]).toISOString()) {
      importTimestampCoercions++;
    } else if (String(actual ?? '') !== matrix[r][c]) {
      throw new Error('CSV import mismatch: ' + name + ':' + r + ':' + c);
    }
  }
  await fs.writeFile(path.join(root, name + '.csv'), csv);
  const inspection = await workbook.inspect({ kind:'region', sheetId:name, range:`A1:F${Math.min(matrix.length,3)}`, maxChars:1600, tableMaxCellChars:70 });
  checks.push({ file:name+'.csv', rows:rows.length, columns:headers.length, gridRoundTrip:true, csvImportCompatible:true, importTimestampCoercions, note:'Raw CSV keeps exact timestamp strings. Artifact Tool CSV import may coerce timestamps; exact raw-text round-trip is separately checked by Python csv.', inspection });
}
await fs.writeFile(path.join(root, 'evidence/artifact-table-check.json'), JSON.stringify({checked_utc:new Date().toISOString(), tool:'@oai/artifact-tool', scope:'UTF-8 CSV grid and delimiter preservation; no formula or historical-runtime test', checks},null,2)+'\n');
console.log(JSON.stringify(checks.map(({file,rows,columns,gridRoundTrip,csvImportCompatible,importTimestampCoercions})=>({file,rows,columns,gridRoundTrip,csvImportCompatible,importTimestampCoercions}))));
