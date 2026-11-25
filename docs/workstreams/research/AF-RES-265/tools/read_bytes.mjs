/* A separate DataView parser for the pinned fixtures. */
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import assert from 'node:assert/strict';

const root = process.argv[2];
assert(root, 'usage: node read_bytes.mjs <input directory>');
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const viewOf = bytes => new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);

function container(data) {
  const view = viewOf(data);
  const magic = data.toString('ascii', 0, 4);
  const version = view.getUint32(4, true);
  const length = view.getUint32(8, true);
  assert.deepEqual([magic, version, length], ['glTF', 2, data.length]);
  const header = { magic, version, length, headerHex: data.subarray(0, 12).toString('hex'), chunks: [] };
  let doc, bin;
  for (let at = 12; at < length;) {
    const size = view.getUint32(at, true);
    const kind = data.toString('ascii', at + 4, at + 8);
    const start = at + 8;
    const end = start + size;
    assert(end <= length && size % 4 === 0);
    assert.equal(kind, at === 12 ? 'JSON' : 'BIN\0');
    const payload = data.subarray(start, end);
    let padding;
    if (kind === 'JSON') {
      const json = new TextDecoder('utf-8', { fatal: true }).decode(payload);
      const trimmed = json.replace(/ +$/, '');
      assert(trimmed.endsWith('}'));
      doc = JSON.parse(trimmed);
      padding = payload.subarray(Buffer.byteLength(trimmed));
    } else {
      assert(!bin);
      const logicalLength = doc.buffers[0].byteLength;
      bin = payload.subarray(0, logicalLength);
      padding = payload.subarray(logicalLength);
      assert(logicalLength <= size && padding.length <= 3 && padding.every(byte => byte === 0));
    }
    header.chunks.push({ kind, header: at, start, end, length: size,
      padHex: padding.toString('hex'), sha256: sha256(payload) });
    at = end;
  }
  assert(doc);
  return { doc, bin, header };
}

const types = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };
const methods = {
  5120: [1, 'getInt8'], 5121: [1, 'getUint8'], 5122: [2, 'getInt16'],
  5123: [2, 'getUint16'], 5125: [4, 'getUint32'], 5126: [4, 'getFloat32'],
};

function sampled(doc, buffers, accessorIndex) {
  const acc = doc.accessors[accessorIndex];
  const bv = doc.bufferViews[acc.bufferView];
  const data = buffers[bv.buffer];
  const offsets = viewOf(data);
  const [size, method] = methods[acc.componentType];
  const count = acc.count;
  const width = types[acc.type];
  const viewOffset = bv.byteOffset ?? 0;
  const accessorOffset = acc.byteOffset ?? 0;
  const stride = bv.byteStride ?? size * width;
  const start = viewOffset + accessorOffset;
  const end = start + (count - 1) * stride + width * size;
  assert(end <= viewOffset + bv.byteLength && viewOffset + bv.byteLength <= data.length);
  const elements = Buffer.alloc(count * width * size);
  const values = Array.from({ length: width }, () => []);
  for (let i = 0; i < count; i++) {
    const origin = start + i * stride;
    data.copy(elements, i * size * width, origin, origin + size * width);
    for (let c = 0; c < width; c++) {
      values[c].push(offsets[method](origin + size * c, true));
    }
  }
  return { accessor: accessorIndex, view: acc.bufferView, buffer: bv.buffer,
    componentType: acc.componentType, type: acc.type, count, viewOffset, viewLength: bv.byteLength,
    accessorOffset, stride, start, end, first: values.map(column => column[0]),
    last: values.map(column => column.at(-1)), min: values.map(column => Math.min(...column)),
    max: values.map(column => Math.max(...column)), declaredMin: acc.min ?? null,
    declaredMax: acc.max ?? null, logicalBytes: elements.length, sha256: sha256(elements) };
}

const manifest = JSON.parse(await readFile(join(root, 'input-manifest.json'), 'utf-8'));
const entries = [];
for (const item of manifest.files.filter(row => row.group === 'assets' && /\.gl(?:b|tf)$/.test(row.path))) {
  const input = join(root, item.group, item.path);
  const data = await readFile(input);
  const { doc, bin, header } = input.endsWith('.glb') ?
    container(data) : { doc: JSON.parse(data.toString('utf8')), header: null };
  const buffers = await Promise.all(doc.buffers.map(async b => {
    const bytes = b.uri ? await readFile(join(dirname(input), b.uri)) : bin;
    assert(bytes.length >= b.byteLength);
    return bytes.subarray(0, b.byteLength);
  }));
  const geometry = doc.meshes.flatMap((mesh, mi) => mesh.primitives.map((primitive, pi) => ({
    mesh: mi, primitive: pi, material: primitive.material ?? null, mode: primitive.mode ?? 4,
    POSITION: sampled(doc, buffers, primitive.attributes.POSITION),
    indices: sampled(doc, buffers, primitive.indices),
  })));
  entries.push({ path: item.path, bytes: data.length, sha256: sha256(data), glb: header, geometry });
}
await writeFile(join(root, 'node-static.json'), JSON.stringify({
  parser: 'Node DataView and JSON.parse', finished_utc: new Date().toISOString(), entries,
}, null, 2) + '\n');
console.log(`read ${entries.length} serializations, ${entries.reduce((n, e) => n + e.geometry.length, 0)} mesh primitives`);
