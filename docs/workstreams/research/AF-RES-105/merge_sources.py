"""Canonical source ledger. Reader records remain unchanged in evidence/ subdirectories."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
old=[json.loads(x) for x in (P/'sources.jsonl').read_text().splitlines()];by={x.get('source_id',x.get('id')):x for x in old}
for path in sorted((P/'evidence').glob('*/sources-part.jsonl')):
 for line in path.read_text().splitlines():
  if not line.strip():continue
  s=json.loads(line);sid=s.get('source_id',s.get('id'));assert sid,path;s['reader_record']=str(path.relative_to(P));by[sid]=s
for sid,s in by.items():
 s['source_id']=sid
 aliases={'opened_utc':'direct_opened_utc','lineage':'same_work_lineage','version':'version_section','location':'preserved_evidence','observed':'confirmed','case':'case_id'}
 for k,a in aliases.items():
  if k not in s and a in s:s[k]=s[a]
 if 'supports' not in s:s['supports']=[s.get('supports_or_counters','see reader evidence')]
 s.setdefault('refutes',[])
 if not s.get('questions'):
  where=s.get('reader_record','')
  s['questions']=['Q7'] if 'crossdomain' in where else ['Q6','Q7'] if 'official' in where else ['Q5'] if 'followup' in where else ['Q3'] if 'proposals' in where else ['Q1','Q2'] if 'initial' in where else ['Q4'] if 'auxiliary' in where else ['Q1']
 if 'case' not in s:s['case']=s.get('case_ids',s.get('case_refs',s.get('case_id','method_or_source_support')))
 c=s.setdefault('counting',{})
 if 'counted_unique_primary_source' not in c:c['counted_unique_primary_source']=bool(s.get('count_unique_primary',c.get('counts_toward_24_primary_sources',False)))
 if c.get('counts_toward_qgis_official_minimum'):c['category']='official'
 if c.get('counts_toward_qgis_upstream_example_minimum'):c['category']='upstream_test'
 if sid in ['QG-T-O-POLY2NB','QG-T-O-NB2LINES']:c['category']='additional_official'
 if 'category' not in c:
  if c.get('selected_request_event') or sid.startswith('BL-T') and sid.endswith('-INITIAL'):c['category']='chronological_request'
  else:c['category']=s.get('count_category',s.get('source_kind','supplementary_evidence'))
 c.setdefault('reason',s.get('count_reason','see original counting fields'))
 if c['category']=='chronological_request':c['mandatory_minimum_category']=True
 if sid=='BL-O1':
  s['terminology_note']='manual4.0 says Group Index; supplied node UI says Group ID. This is a terminology correspondence, not a direct quote.'
  s['location']='Inputs: Value and Group Index (node UI Group ID); Properties: data type/domain; Outputs: Leading, Trailing, Total; Examples/Table'
 if sid=='BL-O4':s['terminology_note']='manual4.0 says Scale; supplied node UI says Offset Scale. These terms are mapped, not quoted as identical labels.'
 s['canonical_reader_record_preserved']=True
(P/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in by.values()))
print('canonical sources',len(by),'counted',sum(s['counting']['counted_unique_primary_source'] for s in by.values()))
