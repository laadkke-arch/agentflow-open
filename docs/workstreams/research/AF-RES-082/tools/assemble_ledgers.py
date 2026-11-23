"""Normalize research ledgers; no network or product execution."""
import csv,json,pathlib,datetime
D=pathlib.Path(__file__).resolve().parents[1]
def jl(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
def dumpjl(p,rows):p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))

def main():
 sources=[]
 files=[('evidence/root-sources.jsonl','root'),('streams/python/sources.jsonl','python'),('streams/r/sources.jsonl','r'),('streams/publication/sources.jsonl','publication'),('streams/incidents/sources.jsonl','incidents'),('streams/costs/sources.jsonl','costs')]
 for f,reader in files:
  for old in jl(D/f):
   x=dict(old)
   x.update(source_id=old.get('source_id',old.get('id')),lineage_id=old.get('lineage_id',old.get('lineage')),kind=old.get('kind',old.get('source_type',old.get('type'))),url=old.get('url',old.get('original_url')),version=old.get('version',old.get('fixed_version',old.get('fixed_version_section_lines',''))),section=old.get('section',old.get('locator',old.get('fixed_version_section_lines',''))),opened_at_utc=old.get('opened_at_utc',old.get('opened_utc')),questions=old.get('questions',[]),case_ids=old.get('case_ids',old.get('cases',[])),observed=old.get('observed',old.get('confirmed_content',old.get('content',''))),limitations=old.get('limitations',old.get('limits_unverified',old.get('limit',''))),claim_support=old.get('claim_support',old.get('claim','')),reader=old.get('reader',reader),origin_ledger=f)
   x['directly_opened']=old.get('directly_opened',True)
   x['count_toward_minimum']=old.get('count_toward_minimum',old.get('count_as_independent',True))
   if x.get('kind') in ['recruitment_metadata','release_inventory'] and not x['case_ids']:x['count_toward_minimum']=False
   # Provider manuals/code in different versions or URLs remain one original work.
   url=x['url'] or ''
   if reader=='incidents':
    x['canonical_lineage']=x['lineage_id']
    # Background Q&A/feature context is retained, but excluded from the conservative minimum.
    if old.get('actual_incident') is False:x['count_toward_minimum']=False
   elif '/r-lib/pkgdown/' in url and '/issues/' not in url and '/pull/' not in url: x['canonical_lineage']='OFF-PKGDOWN'
   elif 'pkgdown.r-lib.org/' in url:x['canonical_lineage']='OFF-PKGDOWN'
   elif ('/sphinx-doc/sphinx/' in url or 'www.sphinx-doc.org/' in url) and '/issues/' not in url and '/pull/' not in url:x['canonical_lineage']='OFF-SPHINX'
   elif 'docs.readthedocs.' in url:x['canonical_lineage']='OFF-RTD'
   elif 'docs.github.com/en/pages/' in url:x['canonical_lineage']='OFF-PAGES'
   else:x['canonical_lineage']=x['lineage_id']
   sources.append(x)
 ids=[x['source_id'] for x in sources]; assert len(ids)==len(set(ids)), 'Duplicate source IDs'
 dumpjl(D/'sources.jsonl',sources)
 deployments=[]
 for f,kind in [('streams/python/deployments.jsonl','consumer_deployment'),('streams/r/deployments.jsonl','consumer_deployment'),('streams/publication/events.jsonl','cross_domain_event'),('streams/incidents/events.jsonl','independent_documentation_event')]:
  for old in jl(D/f):deployments.append(dict(old,record_type=kind,origin_ledger=f))
 dumpjl(D/'deployments.jsonl',deployments)
 frames=list(csv.DictReader((D/'FRAME.csv').open()))
 lookup={x['case_id']:x for x in frames if x.get('case_id')}
 prelinks=list(csv.DictReader((D/'prelinks.csv').open()))
 reader_urls={x['case_id']:x['reader_url'] for x in prelinks}
 req=[]
 for f in ['streams/python/requirements.jsonl','streams/r/requirements.jsonl']:
  for x in jl(D/f):
   case=x['case_id']; base=lookup[case]; status=x.get('status',x.get('condition_status',''))
   confirmed=status in ['observed_owner_statement','supported_public_site_intent','confirmed']
   req.append({'case_id':case,'original_rank':base['original_rank'],'repo':base['full_name'],'language':base['language'],'tag':x['tag'],'tag_sha':x['tag_sha'],'requirement_id':x.get('requirement_id',x.get('condition_id')),'status':'confirmed' if confirmed else 'unconfirmed','role':x['role'],'requirement':x['requirement'],'original_quote':x.get('short_quote',x.get('original_utterance','')),'source_id':x['source_id'],'source_url':x.get('url',x.get('source_url')),'section':x.get('section',x.get('locator')),'reader_url':x.get('reader_url') or reader_urls[case],'limitations':x.get('limit',x.get('limitations')),'phase':'initial_requirements_seal'})
 for r in req:
  r['postbudget_locator_audit']='ROOT-P3-README-LOCATOR: stable badge L5; options/#enable L44,L140; legacy link L53. Original condition unchanged.' if r['case_id']=='P3' else ''
 with (D/'requirements.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(req[0]),lineterminator='\n');w.writeheader();w.writerows(req)
 independent=sorted(set(x['canonical_lineage'] for x in sources if x['count_toward_minimum'] and x['directly_opened']))
 index=[{'canonical_lineage':l,'source_ids':[x['source_id'] for x in sources if x['canonical_lineage']==l],'counted_source_ids':[x['source_id'] for x in sources if x['canonical_lineage']==l and x['count_toward_minimum']],'reader_groups':sorted(set(x['reader'] for x in sources if x['canonical_lineage']==l))} for l in independent]
 (D/'evidence'/'lineage-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'source_rows':len(sources),'counted_independent_lineages':len(independent),'deployments_events':len(deployments),'requirements':len(req),'confirmed_requirements':sum(x['status']=='confirmed' for x in req),'lineages':independent},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
