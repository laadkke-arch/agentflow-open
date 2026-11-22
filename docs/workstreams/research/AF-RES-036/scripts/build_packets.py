"""Build fixed four-view packets, then balance them over four fresh contexts."""
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1]
def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def readl(path): return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def writel(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows))

refs=readl(P/'references.jsonl')
components={c['ref_id']:c for c in readl(P/'components.jsonl')}

packets=[]
for ref in refs:
    rid=ref['ref_id']; c=components[rid]
    b='Original citation\nDocument: '+ref['consumer_title']+'\nEdition: '+ref['consumer_version']+'\nDistribution: '+ref['original_distribution_url']+'\nMember: '+ref['member']+'\nOriginal href: '+ref['original_href']+'\nLink text: '+ref['link_text']+'\nPresealed minimum purpose (collector paraphrase): '+ref['minimal_purpose']+'\n\nOriginal context:\n'+ref['context']
    n=c['N']['text'];h=c['H']['text']
    for label,part in [('N',n),('H',h)]:
        assert sha(part)==c[label]['sha256'],(rid,label,'component hash')
    for view,labels in [('B',['B']),('BN',['B','N']),('BH',['B','H']),('BNH',['B','N','H'])]:
        allparts={'B':b,'N':n,'H':h}
        parts={k:allparts[k] for k in labels}
        text='\n\n'.join('['+k+']\n'+parts[k] for k in labels)
        packets.append({'ref_id':rid,'view':view,'parts':parts,'part_sha256':{k:sha(v) for k,v in parts.items()},'part_utf8_bytes':{k:len(v.encode()) for k,v in parts.items()},'input_text':text,'input_text_sha256':sha(text),'input_utf8_bytes':len(text.encode()),'empty_evidence':{k:c[k].get('empty_evidence',not c[k].get('raw_excerpt','')) for k in ('N','H')}})
assert len(packets)==48
writel(P/'packets.jsonl',packets)
bykey={(r['ref_id'],r['view']):r for r in packets}
plan=json.loads((P/'reading-plan.json').read_text())
for reader in ('fresh-1','fresh-2','fresh-3','fresh-4'):
    directory=P/'readers'/reader;directory.mkdir(parents=True,exist_ok=True)
    assignments=[]
    for a in sorted((r for r in plan['rows'] if r['reader_id']==reader),key=lambda r:r['case_order']):
        p=bykey[a['case_id'],a['view']]
        inp={'ref_id':p['ref_id'],'view':p['view'],'input_text':p['input_text']}
        fn=f"{a['case_order']:02d}-{a['case_id']}.json"
        content=json.dumps(inp,ensure_ascii=False,indent=2)+'\n'
        (directory/fn).write_text(content)
        assignments.append({**a,'file':fn,'file_sha256':sha(content),'input_text_sha256':p['input_text_sha256']})
    (directory/'assignment.json').write_text(json.dumps({'reader_id':reader,'model_family':'same internal model family; not human study','parent_history':'none','read_sequentially_one_case_then_decide':True,'assignments':assignments},ensure_ascii=False,indent=2)+'\n')

checks=[]
for ref in refs:
    rid=ref['ref_id']
    n1=bykey[rid,'BN']['parts']['N'];n2=bykey[rid,'BNH']['parts']['N']
    h1=bykey[rid,'BH']['parts']['H'];h2=bykey[rid,'BNH']['parts']['H']
    checks.append({'ref_id':rid,'N_identical':n1.encode()==n2.encode(),'H_identical':h1.encode()==h2.encode(),'B_identical':len({bykey[rid,v]['parts']['B'] for v in ('B','BN','BH','BNH')})==1,'N_sha256':sha(n1),'H_sha256':sha(h1)})
receipt={'packets':len(packets),'cases':len(refs),'checks':checks,'all_identical':all(r['N_identical'] and r['H_identical'] and r['B_identical'] for r in checks),'packet_file_sha256':hashlib.sha256((P/'packets.jsonl').read_bytes()).hexdigest(),'adjudication_available_to_readers':False}
(P/'evidence/packet-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(refs),'packets':len(packets),'all_identical':receipt['all_identical']}))
