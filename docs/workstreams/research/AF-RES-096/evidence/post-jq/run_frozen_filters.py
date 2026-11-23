"""Post-seal validation of frozen researcher filters; no route judgment is changed."""
import datetime,hashlib,html,json,pathlib,subprocess
from html.parser import HTMLParser
P=pathlib.Path(__file__).resolve().parents[2]
OUT=P/'evidence/post-jq';C=OUT/'_cache';V=OUT/'validation';V.mkdir(exist_ok=True)
BIN=(C/'jq-linux-amd64').resolve();SEAL='d03ca37daf0c43688c68bc39417d84a9b84803e9'
class CodeBlocks(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.inpre=False;self.buf=[];self.blocks=[]
 def handle_starttag(self,tag,attrs):
  if tag=='pre': self.inpre=True;self.buf=[]
 def handle_data(self,data):
  if self.inpre:self.buf.append(data)
 def handle_endtag(self,tag):
  if tag=='pre':self.blocks.append(''.join(self.buf));self.inpre=False
records=json.loads((P/'evidence/outcomes/public-records.json').read_text())
def firstblocks(case):
 x=next(x for x in records if x['case_id']==case);r=min(x['question_body_revisions'],key=lambda r:r['creation_epoch']);par=CodeBlocks();par.feed((P/r['body_cache']).read_text());return r,par.blocks
r4,b4=firstblocks('J4');r1,b1=firstblocks('J1');r3,b3=firstblocks('J3')
fixtures=[]
def fixture(name,case,text,expect,provenance,source_url):
 path=V/(name+'.txt');path.write_text(text);fixtures.append({'id':name,'case_id':case,'input_file':str(path.relative_to(P)),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'input_bytes':len(path.read_bytes()),'expected_stdout':expect,'provenance':provenance,'source_url':source_url});return fixtures[-1]
fixture('J4-original-line','J4',b4[0], 'specificword=[this is some(of the possible[text])]\n','Verbatim first R0 code block; HTML entity decoding only.',r4['url'])
fixture('J4-original-empty','J4',b4[1], 'specificword=[]\n','Verbatim R0 empty-value code block; HTML entity decoding only.',r4['url'])
fixture('J4-synthetic-repeated-nested-neighbor','J4','prefix=[], specificword=[left[inner]right], neighbor=[tail], specificword=[], suffix=done\n','specificword=[left[inner]right]\nspecificword=[]\n','Researcher-created adversarial case combines explicit nesting, empty value, repetition, and neighbor exclusion; not a public regression.',None)
fixture('J4-synthetic-no-marker','J4','prefix=[ignore], status=[keep-out]\n','','Researcher-created negative control: matching app line without target marker.',None)
fixture('J1-original-truncated','J1',b1[0],None,'Verbatim first R0 JSON fragment. Known incomplete syntax; this run measures that limitation, not filter correctness.',r1['url'])
fixed=b1[0].rstrip();assert fixed.endswith(',');fixed=fixed[:-1]+'\n  ]\n}\n'
fixture('J1-minimum-syntax-repair','J1',fixed,'2024-12-31T00:00:00Z, a, 1125.000\n2024-12-31T00:00:00Z, b, 2119.000\n2024-12-31T00:00:00Z, c, 0.000\n','Researcher removes terminal comma and adds only missing outer-array/object closures; no data fields or values changed. Number textual spelling is observed separately from pairing requirement.',r1['url'])
fixture('J3-original-simple-array','J3','["a","b","c","d"]\n','["ab","cd"]\n','Original explicit simple example, exact array values; compact-output flag only affects whitespace.',r3['url'])
fixture('J3-array-envelope','J3','{"elements":["a","b","c","d"]}\n','["ab","cd"]\n','Researcher combines original simple array with original .elements envelope mentioned in jq command; full original Overpass file unavailable.',r3['url'])
filter_records=[]
for route in ['A','B']:
 f=P/f'evidence/routes/J4-{route}/proposed_filter.jq';data=f.read_bytes();gitpath=f.relative_to(P.parents[3]) if False else str(f.relative_to(pathlib.Path.cwd()))
 frozen=subprocess.run(['git','show',SEAL+':'+gitpath],capture_output=True,check=True).stdout
 assert data==frozen, 'frozen filter bytes changed'
 filter_records.append({'case_id':'J4','route':route,'path':str(f.relative_to(P)),'sha256':hashlib.sha256(data).hexdigest(),'sealed_bytes_match':True,'flags':['-R','-r']})
for case in ['J1','J3']:
 j=json.loads((P/f'evidence/routes/{case}-A/judgment.json').read_text());data=j['proposed_solution'].encode();f=V/(case+'-sealed-filter.jq');f.write_bytes(data)
 filter_records.append({'case_id':case,'route':'A/B equivalent proposal','path':str(f.relative_to(P)),'sha256':hashlib.sha256(data).hexdigest(),'proposal_source':f'evidence/routes/{case}-A/judgment.json#proposed_solution','flags':['-r'] if case=='J1' else ['-c']})
# J3 simple-array variant is an explicitly declared post-seal adaptation of only envelope removal.
j3=next(x for x in filter_records if x['case_id']=='J3');original=(P/j3['path']).read_text();assert original.startswith('.elements | ');simple=original[len('.elements | '):];f=V/'J3-simple-array-adaptation.jq';f.write_text(simple)
filter_records.append({'case_id':'J3','route':'post-seal envelope adaptation','path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'flags':['-c'],'adaptation':'Remove .elements | for the R0 simple array; no other expression change.'})
results=[]
for f in filter_records:
 fs=[x for x in fixtures if x['case_id']==f['case_id']]
 if f['case_id']=='J3':fs=[x for x in fs if ('simple' in x['id'])==('adaptation' in f['route'])]
 for x in fs:
  cmd=[str(BIN),*f['flags'],'-f',str((P/f['path']).resolve())];started=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,input=(P/x['input_file']).read_bytes(),capture_output=True,timeout=20)
  stem=x['id']+'-'+f['route'].split('/')[0].replace(' ','_');(V/(stem+'.stdout')).write_bytes(r.stdout);(V/(stem+'.stderr')).write_bytes(r.stderr)
  result={'case_id':x['case_id'],'fixture_id':x['id'],'filter_route':f['route'],'filter_file':f['path'],'filter_sha256':f['sha256'],'input_file':x['input_file'],'input_sha256':x['input_sha256'],'executable_sha256':hashlib.sha256(BIN.read_bytes()).hexdigest(),'command_argv':cmd,'stdin_file':x['input_file'],'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_file':str((V/(stem+'.stdout')).relative_to(P)),'stderr_file':str((V/(stem+'.stderr')).relative_to(P)),'exact_expected_match':r.stdout.decode()==x['expected_stdout'] if x['expected_stdout'] is not None else None,'expected_exit':'nonzero expected for deliberately unclosed original fragment' if 'truncated' in x['id'] else 0,'out_of_route_budget':True,'attribution':'researcher execution after remote seal2; not asker execution and cannot change frozen verdict'}
  results.append(result)
(OUT/'validation-inputs.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n');(OUT/'validation-filters.json').write_text(json.dumps(filter_records,ensure_ascii=False,indent=2)+'\n');(OUT/'runtime-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for r in results:print(json.dumps({k:r[k] for k in ['case_id','fixture_id','filter_route','exit_code','stdout','stderr','exact_expected_match']},ensure_ascii=False))
