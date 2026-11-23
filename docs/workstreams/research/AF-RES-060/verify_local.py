"""Read-only rank/scope/link verification; writes only its own observed receipt."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import csv,json,hashlib,re,subprocess
from replay import rank,terms_for
P=Path(__file__).resolve().parent
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
OWNED='docs/workstreams/research/AF-RES-060/'
BASE='3f4d43b19cd76d56983e6f500eebe7010eb3fa51'
def rc(f):return list(csv.DictReader((P/f).open(encoding='utf-8')))
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
reqs=json.loads((P/'requirements.json').read_text()); req={r['case_id']:r for r in reqs}
vocab=rc('vocabulary.csv'); cat=rc('inputs/af-res-056/catalog.csv'); features={x['catalog_id']:json.loads(x['added_features_json']) for x in rc('features.csv')}
mm=rc('matches.csv');ss=rc('slots.csv');pp=rc('paths.csv')
checks=[]
for m in mm:
    terms=terms_for(m['case_id'],m['query'],vocab)
    actual=rank(req[m['case_id']],terms,cat,None if m['fields']=='F0' else features)
    checks.append({'comparison_id':m['comparison_id'],'terms_equal':terms==json.loads(m['terms_json']),'all_matches_equal':actual==json.loads(m['all_matches_json'])})
assert len(mm)==48 and all(x['terms_equal'] and x['all_matches_equal'] for x in checks)
assert len(ss)==144 and sum(x['display_status']=='filled' for x in ss)==18
assert len(pp)==84 and len({(x['case_id'],x['catalog_id']) for x in pp})==28
assert all(x['judgment'] in ('complete','partial','confirmed_wrong','unconfirmed') for x in pp)
freeze=json.loads((P/'evidence/feature-freeze.json').read_text());assert sha('features.csv')==freeze['sha256']['features.csv']
changed=set(subprocess.check_output(['git','diff','--name-only',BASE],cwd=ROOT,text=True).splitlines())
untracked=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines())
assert all(x.startswith(OWNED) for x in changed|untracked)
control='docs/automation/dot-control.json'
control_unchanged=subprocess.check_output(['git','diff',BASE,'--',control],cwd=ROOT)==b''
assert control_unchanged
report=(P/'RESULT.md').read_text();lines=report.splitlines();tables=[];current=[]
for line in lines+['']:
    if line.startswith('| '): current.append(line)
    elif current: tables.append(current);current=[]
assert len(tables[0])-2==48 and len(tables[1])-2==12 and len(tables[-1])-2==3
assert tables[-1][-1]==lines[-1] or lines[-1]==''
missing=[]
for file in ['RESULT.md','cards.md','SELF_CHECK.md','reproduce.md']:
    for url in re.findall(r'\]\(([^\n)]+)\)',(P/file).read_text()):
        if re.match(r'^[a-z]+:',url) or url.startswith('#'):continue
        local=url.split('#')[0]
        if local and not (P/local).exists():missing.append({'file':file,'target':url})
assert not missing,missing
out={'observed_utc':datetime.now(timezone.utc).isoformat(),'actor':'root cloud executor','head_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'base_sha':BASE,'owned_path':OWNED,'changed_owned_files':len(changed),'untracked_owned_files':len(untracked),'outside_owned_files':[],'dot_control_unchanged':control_unchanged,'rank_replay_48_equal':True,'rank_checks':checks,'feature_hash_unchanged':True,'counts':{'catalog':62,'requirements':12,'vocabulary':len(vocab),'comparisons':48,'slots':144,'filled_slots':18,'paths':84,'unique_pairs':28},'table_rows':[len(tables[0])-2,len(tables[1])-2,len(tables[-1])-2],'missing_internal_links':missing,'checked_files_sha256':{f:sha(f) for f in ['RESULT.md','cards.md','SELF_CHECK.md','features.csv','requirements.json','vocabulary.csv','matches.csv','slots.csv','paths.csv','changes.csv']},'interpretation':'Read-only logical/byte/scope validation, not supplier behavior or research-sufficiency certification.'}
(P/'evidence/verification').mkdir(exist_ok=True)
(P/'evidence/verification/local-integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['head_sha','changed_owned_files','untracked_owned_files','dot_control_unchanged','rank_replay_48_equal','table_rows','missing_internal_links']}))
