"""Recheck the two fixed asciicast publications without counting them as new cases."""
import hashlib
import json
import pathlib
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = pathlib.Path('/tmp/af098-root')

class Refs(HTMLParser):
    def __init__(self, offset=0):
        super().__init__(); self._line_offset=offset; self.elements=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if any(k in attrs for k in ['src','srcset','href','data']) or tag in ['script','svg','picture','source']:
            self.elements.append({'tag':tag,'line':self.getpos()[0]+self._line_offset,'attrs':attrs})

def main():
    directory=ROOT/'evidence/calibration'
    rows=[]; sources=[]
    for label,edition in [('OLD','1.0.0.9000'),('NEW','2.3.1')]:
        sid='CAL-'+label+'-HTML'; text=(CACHE/sid).read_text()
        anchor=text.index('id="using-svg-files"')
        start=text.rfind('<div class="section level2">',0,anchor)
        end=text.index('<div class="section level2">',anchor)
        assert start>=0 and end>anchor
        first_line=text[:start].count('\n')+1
        last_line=text[:end].count('\n')
        parser=Refs(first_line-1);parser.feed(text[start:end])
        all_parser=Refs();all_parser.feed(text)
        expected=['asciicast-demo_files/figure-html/unnamed-chunk-'+n+'.svg' for n in ['6','7']]
        candidate_refs=[e for e in all_parser.elements if any(v in expected for v in e['attrs'].values())]
        imgs=[e for e in parser.elements if e['tag']=='img']
        assert len(imgs)==(2 if label=='OLD' else 0)
        assert len(candidate_refs)==(2 if label=='OLD' else 0)
        assets=[json.loads((directory/'receipts'/('CAL-'+label+'-SVG'+n+'.json')).read_text()) for n in ['6','7']]
        body=json.loads((directory/'receipts'/(sid+'.json')).read_text())
        rows.append({'edition':edition,'body_receipt':body,'section_id':'using-svg-files',
                     'section_lines':[first_line,last_line],
                     'section_boundary':'enclosing div.section.level2 through before next div.section.level2 (Showing the code)',
                     'section_all_uri_elements':parser.elements,'document_candidate_references':candidate_refs,
                     'section_img_count':len(imgs),'section_inline_svg_count':sum(e['tag']=='svg' for e in parser.elements),
                     'section_script_count':sum(e['tag']=='script' for e in parser.elements),
                     'data_uri_literal_present':'data:' in text[start:end],
                     'file_candidates':assets,'P':'YES','U':'YES' if label=='OLD' else 'NO','G':'UNKNOWN',
                     'limit':'No image/SVG/cast resource reference in the new fixed section; files still exist in its publication tree. No claim about runtime execution.'})
        for r in [body]+assets:
            sources.append({'id':r['id'],'q':['Q3','Q4','Q5','Q7'],'case_id':['CAL-094'],
                            'url':r['requested_url'],'fixed_url':r['requested_url'],'utc':r['utc'],
                            'publisher':'r-lib/asciicast maintainers','lineage':'asciicast calibration inherited from AF-RES-094',
                            'version':edition,'locator':'#using-svg-files L'+str(first_line)+'-L'+str(last_line) if r==body else 'SVG XML candidate',
                            'observed':str(len(imgs))+' image references in exact section; '+str(len(candidate_refs))+' document attributes match the two old SVGs.' if r==body else 'Actual SVG bytes match same candidate at both fixed publications.',
                            'claim':'Tree inclusion does not imply current-section usage or current-build generation.',
                            'limitations':'Known AF-RES-094 correction; excluded from new cases and source minimum; generation job unverified.',
                            'counted':False,'dedup_basis':'Explicitly excluded calibration; two assets are one known event.',
                            'category':'calibration','sha256':r['sha256'],'bytes':r['bytes']})
    for old,new in zip(rows[0]['file_candidates'],rows[1]['file_candidates']):
        assert old['sha256']==new['sha256']
    out={'source_input':'AF-RES-094@082ba3b787edd92d804bf617397743e89d75c5f0','rows':rows,
         'main_denominator_increment':0,'source_minimum_increment':0,
         'generation_event_not_inferred_from_git_date':True,
         'parser_correction':'The id is on h2, not on its enclosing section div; heading-only parsing was rejected before stage3. Stage4 also changed line offset to a private attribute because HTMLParser.offset is its mutable column counter; reference counts and U judgments were unchanged, absolute attribute lines corrected.'}
    (directory/'audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (directory/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    print(json.dumps([{'edition':x['edition'],'lines':x['section_lines'],'img':x['section_img_count'],'U':x['U']} for x in rows]))

if __name__=='__main__':main()
