"""Recreate all24 displaced/added boundary positions from sealed candidates."""
from pathlib import Path
import argparse,csv,io,json

ROOT=Path(__file__).resolve().parent
def jl(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def build():
    packets=jl(ROOT/'packets.jsonl');notes=json.loads((ROOT/'evidence/displacement-notes.json').read_text())
    rows=[]
    for case,ds in notes.items():
        for policy,action in [('A','displaced'),('B','added')]:
            f=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(case,policy,'F'))
            s=next(p for p in packets if (p['case_id'],p['policy'],p['mode'])==(case,policy,'S'))
            for no in [3,4]:
                fs=f['slots'][no-1];ss=s['slots'][no-1];fid=fs['file_id'] or f'EMPTY-{no}';n=ds[fid]
                sections=[]
                if not fs['empty']:
                    raw=(ROOT/fs['cached_body']).read_bytes();text=raw.decode()
                    for a,b in n['review_char_ranges']:
                        assert 0<=a<b<=len(text)
                        sections.append({'url':fs['url'],'char_start':a,'char_end':b,
                                         'byte_start':len(text[:a].encode()),'byte_end':len(text[:b].encode()),
                                         'line_start':text.count('\n',0,a)+1,'line_end':text.count('\n',0,b-1)+1,
                                         'inside_S':ss['char_start']<=a and b<=ss['char_end']})
                rows.append({'case_id':case,'question_id':f['question_id'],'action':action,'policy':policy,'slot':no,
                             'file_id':fid,'url':fs.get('url'),'sha256':fs.get('sha256'),
                             'F_packet':f['packet_id'],'F_chars':json.dumps([fs.get('char_start'),fs.get('char_end')]),
                             'S_packet':s['packet_id'],'S_chars':json.dumps([ss.get('char_start'),ss.get('char_end')]),
                             'empty_charged':fs['empty'],'classification':n['classification'],
                             'required_evidence_impact':n['required_evidence_impact'],
                             'independent_original_test':n['independent_original_test'],
                             'build_or_resource_limit':n['build_or_resource_limit'],
                             'original_sections':json.dumps(sections,ensure_ascii=False),
                             'review_phase':'post-seal2 displacement audit; sealed judgments unchanged'})
    assert len(rows)==24
    stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary={'positions':len(rows),'displaced':sum(r['action']=='displaced' for r in rows),
             'added':sum(r['action']=='added' for r in rows),'empty_added':sum(r['empty_charged'] for r in rows),
             'unique_nonempty_files':len({r['file_id'] for r in rows if not r['empty_charged']}),
             'note':'Each position has pairedF/S exposure; twoemptyaddedpositions become fouremptyfilepositions across32packets.'}
    return stream.getvalue(),summary

def main():
    a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');o=a.parse_args()
    csvbody,summary=build()
    outputs={'displacement.csv':csvbody,'evidence/displacement-summary.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
    for rel,body in outputs.items():
        if o.check:assert (ROOT/rel).read_bytes()==body.encode(),'reconstruction mismatch '+rel
        else:(ROOT/rel).write_bytes(body.encode())
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
