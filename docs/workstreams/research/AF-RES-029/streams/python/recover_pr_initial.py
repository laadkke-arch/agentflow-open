"""Recover earliest added official PEP draft in its public PR history."""
import pathlib,subprocess,json,hashlib,datetime,re
BASE=pathlib.Path(__file__).parent
GIT=['git','--git-dir=/workspace/scratch/ad0c7c69f3ab/af-res-029-python-peps.git']
for n,pr in [(667,2053),(686,2443),(727,3310)]:
 cid=f'pep-{n:04d}';ref=f'refs/heads/recovery-pr-{pr}';log=subprocess.check_output(GIT+['log',ref,'--no-renames','--diff-filter=A','--format=COMMIT\t%H\t%aI\t%cI','--name-only','--',f'{cid}.rst',f'peps/{cid}.rst']);(BASE/f'raw/{cid}/pr-{pr}-first-additions.tsv').write_bytes(log)
 entries=[]
 for l in log.decode().splitlines():
  if l.startswith('COMMIT\t'):_,sha,ad,cd=l.split('\t')
  elif l.endswith('.rst'):entries.append({'sha':sha,'author_date':ad,'committer_date':cd,'path':l})
 r=min(entries,key=lambda e:e['committer_date']);body=subprocess.check_output(GIT+['show',r['sha']+':'+r['path']]);p='originals/'+cid+'-'+r['sha'][:12]+'.rst';(BASE/p).write_bytes(body)
 meta=json.loads((BASE/f'raw/{cid}/pr-{pr}-read-receipt.json').read_text())
 fields={k.strip():v.strip() for k,v in (l.split(':',1) for l in body.decode().split('\n\n',1)[0].splitlines() if ':' in l)}
 r.update({'canonical_id':cid,'pr':pr,'local_original':p,'sha256':hashlib.sha256(body).hexdigest(),'fixed_url':f"https://github.com/python/peps/blob/{r['sha']}/{r['path']}",'raw_url':f"https://raw.githubusercontent.com/python/peps/{r['sha']}/{r['path']}",'blob_sha':subprocess.check_output(GIT+['rev-parse',r['sha']+':'+r['path']]).decode().strip(),'first_public_date':meta['created_at'][:10],'first_public_utc':meta['created_at'],'first_public_evidence':meta['url'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_title':fields.get('Title'),'initial_status_exposure':fields.get('Status'),'created_header':fields.get('Created'),'method':'Earliest added PEP in official repository PR ref, including pre-main-merge history; no subsequent versions read.'})
 (BASE/f'raw/{cid}/initial-pr-recovery.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
