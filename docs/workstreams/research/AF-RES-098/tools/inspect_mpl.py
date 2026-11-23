"""Inspect already-retrieved HTML/PNG bytes; does not execute gallery examples."""
import base64
import csv
import hashlib
import json
import pathlib
import re
import struct
import urllib.parse
import zlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = pathlib.Path('/tmp/af098-root')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class Section(HTMLParser):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.level = 0
        self.start = None
        self.end = None
        self.elements = []
        self.base = None
        self.target_tag = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'base':
            self.base = a.get('href')
        if self.level == 0 and a.get('id') == self.target and self.start is None:
            self.level = 1
            self.start = self.getpos()[0]
            self.target_tag = tag
        elif self.level and tag not in VOID:
            self.level += 1
        if self.level and (any(k in a for k in ['src', 'srcset', 'href', 'data']) or tag in ['svg', 'script', 'picture', 'source']):
            self.elements.append({'tag': tag, 'line': self.getpos()[0], 'attrs': a})
    def handle_endtag(self, tag):
        if self.level and tag not in VOID:
            self.level -= 1
            if self.level == 0:
                self.end = self.getpos()[0]

def png_info(b):
    assert b[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8
    chunks = []
    idat = bytearray()
    while pos < len(b):
        length = struct.unpack('>I', b[pos:pos+4])[0]
        kind = b[pos+4:pos+8]
        data = b[pos+8:pos+8+length]
        crc = struct.unpack('>I', b[pos+8+length:pos+12+length])[0]
        assert zlib.crc32(kind + data) & 0xffffffff == crc
        row = {'type': kind.decode(), 'bytes': length, 'sha256': hashlib.sha256(data).hexdigest()}
        if kind in [b'tEXt', b'iTXt']:
            row['text'] = data.decode('latin1')
        if kind == b'IDAT':
            idat.extend(data)
        chunks.append(row)
        pos += length + 12
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'signature_mime': 'image/png', 'dimensions': struct.unpack('>II', b[16:24]),
            'chunks': chunks, 'IDAT_sha256': hashlib.sha256(idat).hexdigest(),
            'decoded_scanline_sha256': hashlib.sha256(zlib.decompress(idat)).hexdigest(),
            'crc_all_valid': True}

def receipt(sid, group='matplotlib'):
    return json.loads((ROOT / 'evidence' / group / 'receipts' / (sid+'.json')).read_text())

def main():
    out = ROOT / 'evidence' / 'matplotlib'
    rows = []
    audits = []
    source_pins = {'3.7.0': 'd6dd1b79142e4e2483244c25ff1e3ddb664722d3',
                   '3.7.1': 'b3bd929cf07ea35479fded8f739126ccc39edd6d'}
    for ver, pin in [('3.7.0', '410d8388303fab638bbedbd1d2eace0e5efb0de9'),
                     ('3.7.1', 'dbd81bd88621dbfee4c0da45e62a5aeb5722378c')]:
        for cid, name, anchor in [('MP1', 'animation_demo', 'pyplot-animation'),
                                  ('MP2', 'pause_resume', 'pausing-and-resuming-an-animation')]:
            hid = 'MPL-OLD-FINAL-'+cid if ver == '3.7.0' else cid+'-NEW-HTML'
            raw = (CACHE/hid).read_bytes()
            body = raw.decode()
            parsed = Section(anchor)
            parsed.feed(body)
            assert parsed.start and parsed.end
            imgs = [x for x in parsed.elements if x['tag'] == 'img']
            assert len(imgs) == 1
            img = imgs[0]
            hreceipt = receipt(hid)
            base = urllib.parse.urljoin(hreceipt['final_url'], parsed.base or '')
            resolved = urllib.parse.urljoin(base, img['attrs']['src'])
            variants = []
            for suffix in ['1x', '2x']:
                aid = cid+'-'+ver+'-'+suffix
                ar = receipt(aid)
                info = png_info((CACHE/aid).read_bytes())
                variants.append({'id': aid, 'http': ar, 'png': info})
            assert resolved == variants[0]['http']['requested_url']
            assert 'Matplotlib '+ver+' documentation' in body
            downloads = [x for x in parsed.elements if x['tag'] == 'a' and '_downloads/' in x['attrs'].get('href', '')]
            audit = {'case_id': cid, 'version': ver, 'publication_commit': pin,
                     'body': hreceipt, 'section': anchor, 'section_lines': [parsed.start, parsed.end],
                     'base_element': parsed.base, 'resolution_base': base,
                     'reference_element': img, 'payload_variants': variants,
                     'section_all_uri_elements': parsed.elements,
                     'download_targets': [urllib.parse.urljoin(base, x['attrs']['href']) for x in downloads],
                     'P': 'YES', 'U': 'YES', 'G': 'UNKNOWN',
                     'scope': 'Fixed publisher HTML, all target-section URI attributes, PNG signature/chunks/CRC. No browser request or example execution.',
                     'generation_limit': 'Versioned producer metadata and publication commit do not identify an actual generation job with input/output hashes.'}
            section_text='\n'.join(body.splitlines()[parsed.start-1:parsed.end])
            audit.update(figcaption_count=len(re.findall(r'<figcaption\b',section_text)),
                         picture_count=len(re.findall(r'<picture\b',section_text)),
                         source_count=len(re.findall(r'<source\b',section_text)),
                         source_sha256=receipt(cid+'-'+ver+'-SOURCE')['sha256'])
            audits.append(audit)
            p = variants[0]
            rows.append({'case_id': cid, 'project': 'Matplotlib', 'version': ver,
                         'source_url': 'https://raw.githubusercontent.com/matplotlib/matplotlib/'+source_pins[ver]+'/examples/animation/'+name+'.py',
                         'source_sha256': audit['source_sha256'], 'body_url': hreceipt['requested_url'],
                         'body_sha256': hreceipt['sha256'], 'section': anchor,
                         'section_locator': 'L'+str(parsed.start)+'-L'+str(parsed.end),
                         'literal_reference': img['attrs']['src'], 'base_uri': base,
                         'payload_url': resolved, 'payload_mime': p['http']['content_type'],
                         'payload_bytes': p['png']['bytes'], 'payload_sha256': p['png']['sha256'],
                         'included_P': 'YES', 'used_U': 'YES', 'generated_G': 'UNKNOWN',
                         'publication_url': 'https://github.com/matplotlib/matplotlib.github.com/commit/'+pin,
                         'generation_record_url': '',
                         'build_rule_urls': 'https://github.com/matplotlib/matplotlib/blob/'+source_pins[ver]+'/doc/devel/release_guide.rst',
                         'generation_record_status': 'Procedure only; no hash-bound execution record',
                         'counterexample': 'Same path/length, changed PNG Software tEXt; identical IDAT/scanlines across two releases.',
                         'limitation': 'Static PNG is not interactive animation; exact ver-doc commit/build environment unbound.',
                         'evidence': 'evidence/matplotlib/audit.json'})
    comparisons = []
    for cid in ['MP1', 'MP2']:
        old = next(x for x in audits if x['case_id']==cid and x['version']=='3.7.0')
        new = next(x for x in audits if x['case_id']==cid and x['version']=='3.7.1')
        for a,b in zip(old['payload_variants'], new['payload_variants']):
            comparisons.append({'case_id':cid, 'variant':a['id'].split('-')[-1],
                                'same_length':a['png']['bytes']==b['png']['bytes'],
                                'same_file_bytes':a['png']['sha256']==b['png']['sha256'],
                                'same_IDAT':a['png']['IDAT_sha256']==b['png']['IDAT_sha256'],
                                'same_scanlines':a['png']['decoded_scanline_sha256']==b['png']['decoded_scanline_sha256'],
                                'changed_chunk_types':[x['type'] for x,y in zip(a['png']['chunks'],b['png']['chunks']) if x['sha256']!=y['sha256']]})
    # Inline animation excluded at recruitment: inspect static assembly, not runtime behavior.
    inline = (CACHE/'MPL-OLD-FINAL-animate_decay').read_text()
    match = re.search(r'frames\[0\]\s*=\s*"(data:image/png;base64,[\s\S]*?)"', inline)
    assert match
    encoded = match.group(1).replace('\\\n', '').split(',', 1)[1]
    frame = base64.b64decode(encoded)
    (CACHE/'MPL-inline-frame0.png').write_bytes(frame)
    ids = re.findall(r'img id="([^"]+)"', inline)
    inline_audit = {'source_id':'MPL-OLD-FINAL-animate_decay',
                    'html_url':receipt('MPL-OLD-FINAL-animate_decay')['requested_url'],
                    'img_ids':ids, 'frame_assignments':len(re.findall(r'frames\[\d+\]\s*=',inline)),
                    'frame0':png_info(frame), 'new_Animation_present':'new Animation(frames' in inline,
                    'scope':'Data URI decoded; script wiring read statically; browser request/playback not executed.',
                    'external_frame_URL_required':False, 'main_sample_included':False}
    result = {'rows':audits,'comparisons':comparisons,'inline_supplement':inline_audit,
              'sealed_prediction_commit':'0df9ea9edbcee995d631eef54b65fd43f73c245f'}
    (out/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    with (out/'lineage.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(json.dumps({'rows':len(rows),'comparisons':comparisons,'inline_frames':inline_audit['frame_assignments'],'inline_frame0_sha256':inline_audit['frame0']['sha256']},indent=2))

if __name__ == '__main__':
    main()
