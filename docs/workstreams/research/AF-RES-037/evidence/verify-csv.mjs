import fs from "node:fs/promises";
import assert from "node:assert/strict";
import crypto from "node:crypto";

// The launcher supplies the documented primary-runtime library. This verifier
// writes only one receipt in owned_path; the requested deliverables remain CSV.
const { Workbook } = globalThis.af037Artifact;
const root = new URL("../", import.meta.url);
const recount = JSON.parse(await fs.readFile(new URL("evidence/recount.json", root), "utf8"));
const specs = [
  { name: "frame.csv", rows: recount.frame_rows, id: "case_id" },
  { name: "chains.csv", rows: 12, id: "case_id" },
  { name: "judgments.csv", rows: 25, id: "case_id" },
];
const results = [];
for (const spec of specs) {
  const csv = await fs.readFile(new URL(spec.name, root), "utf8");
  const workbook = await Workbook.fromCSV(csv, { sheetName: "Ledger" });
  const sheet = workbook.worksheets.getItem("Ledger");
  workbook.recalculate();
  const matrix = sheet.getUsedRange().values;
  assert.equal(matrix.length, spec.rows + 1, `${spec.name} row count`);
  const header = matrix[0];
  assert.equal(new Set(header).size, header.length, "duplicate columns");
  const idCol = header.indexOf(spec.id);
  assert.ok(idCol >= 0);
  const values = matrix.slice(1).map(r => r[idCol]);
  assert.ok(values.every(v => !v || v === "해당 없음" || v === "미확인" || /^(A-[CG][0-9]{2}|B[0-9]{2})$/.test(v)), "unrecognized case ID");
  const ids = new Set(values.filter(v => /^(A-[CG][0-9]{2}|B[0-9]{2})$/.test(v)));
  assert.deepEqual([...ids].sort(), [...recount.selected_ids].sort(), "case joins");
  if (spec.name === "frame.csv") {
    const selectedCol = header.indexOf("selected");
    assert.equal(matrix.slice(1).filter(r => String(r[selectedCol]) === "true").length, 12);
  }
  if (spec.name === "judgments.csv") {
    const interpretation = header.indexOf("interpretation");
    const complete = header.indexOf("complete_chain");
    const strict = matrix.slice(1).filter(r => r[interpretation] === "strict_initial_proposal");
    assert.equal(strict.length, 12);
    assert.equal(strict.filter(r => String(r[complete]) === "true").length, 0);
  }
  const inspect = await workbook.inspect({ kind: "table", range: "Ledger!A1:D3", include: "values,formulas", tableMaxRows: 3, tableMaxCols: 4, maxChars: 1000 });
  results.push({ file: spec.name, sha256: crypto.createHash("sha256").update(csv).digest("hex"), data_rows: matrix.length - 1, columns: header.length, case_ids: [...ids].sort(), parsed_by: "@oai/artifact-tool Workbook.fromCSV", checks_passed: true, inspected: inspect.ndjson });
}
const receipt = { checked_utc: new Date().toISOString(), runtime: process.version, results, output_format: "CSV analytical data, as explicitly requested", rendering: "해당 없음: formatted workbook creation was not requested; CSV import and data joins checked", historical_runtime_execution: false };
await fs.writeFile(new URL("evidence/csv-verification.json", root), JSON.stringify(receipt, null, 2) + "\n");
console.log(JSON.stringify({ checked: results.map(r => ({ file: r.file, rows: r.data_rows, columns: r.columns, passed: r.checks_passed })) }));
