"""Official PEP Git provenance; authored output only within Python stream."""
import pathlib,subprocess,json,hashlib,datetime,re,sys
BASE=pathlib.Path(__file__).parent
GIT='/workspace/scratch/ad0c7c69f3ab/af-res-029-python-peps.git'
def git(*args):return subprocess.check_output(['git','--git-dir='+GIT,*args])
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
head=git('rev-parse','HEAD').decode().strip()
log=git('log','HEAD','--no-renames','--diff-filter=A','--format=COMMIT\t%H\t%aI\t%cI','--name-only','--','pep-*.rst','pep-*.txt','peps/pep-*.rst','peps/pep-*.txt')
(BASE/'raw/git-added-paths.tsv').write_bytes(log)
frame=[json.loads(l) for l in (BASE/'metadata-frame.jsonl').read_text().splitlines()]
by={r['canonical_id']:r for r in frame}; candidates={}
for l in log.decode().splitlines():
 if l.startswith('COMMIT\t'):
  _,commit,author_date,committer_date=l.split('\t')
 elif re.fullmatch(r'(peps/)?pep-\d{4}\.(rst|txt)',l):
  cid=re.search(r'pep-\d{4}',l).group()
  if cid in by:
   record={'canonical_id':cid,'first_commit_sha':commit,'first_commit_author_date':author_date,'first_commit_committer_date':committer_date,'initial_git_path':l}
   if cid not in candidates or committer_date<candidates[cid]['first_commit_committer_date']:candidates[cid]=record
rows=[]
for r in frame:
 c=candidates.get(r['canonical_id'])
 if c:
  c['fixed_url']=f"https://github.com/python/peps/blob/{c['first_commit_sha']}/{c['initial_git_path']}"
  c['raw_url']=f"https://raw.githubusercontent.com/python/peps/{c['first_commit_sha']}/{c['initial_git_path']}"
  c['blob_sha']=git('rev-parse',c['first_commit_sha']+':'+c['initial_git_path']).decode().strip()
  rows.append(c)
(BASE/'initial-version-ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
(BASE/'raw/git-recovery-receipt.json').write_text(json.dumps({'repository':'https://github.com/python/peps.git','checkout_type':'bare partial clone, blob:none; first history metadata of main HEAD','head':head,'checked_utc':now,'command':'git log HEAD --no-renames --diff-filter=A --format=COMMIT\\t%H\\t%aI\\t%cI --name-only -- pep-*.rst pep-*.txt peps/pep-*.rst peps/pep-*.txt','raw_saved':'raw/git-added-paths.tsv','raw_sha256':hashlib.sha256(log).hexdigest(),'frame_rows':len(frame),'recovered_first_additions':len(rows),'not_found':[r['canonical_id'] for r in frame if r['canonical_id'] not in candidates],'exposure':'No commit messages, outcomes or later text printed/read. Git log metadata contains only paths, SHA and dates. Earliest reachable main addition is earliest official archived draft; earlier private/unmerged drafts remain unobserved.','counted':False},indent=2)+'\n')
print('metadata',len(rows),'of',len(frame),'HEAD',head)
for number in map(int,sys.argv[1:]):
 cid=f'pep-{number:04d}';c=candidates[cid];body=git('show',c['first_commit_sha']+':'+c['initial_git_path']);txt=body.decode();header=txt.split('\n\n',1)[0];fields={k.strip():v.strip() for k,v in (l.split(':',1) for l in header.splitlines() if ':' in l)}
 local=f'originals/{cid}-{c["first_commit_sha"][:12]}.rst';(BASE/local).write_bytes(body)
 c.update({'local_original':local,'sha256':hashlib.sha256(body).hexdigest(),'first_title':fields.get('Title'),'created_header':fields.get('Created'),'discussion_to_header':fields.get('Discussions-To'),'post_history_header':fields.get('Post-History'),'initial_status_exposure':fields.get('Status'),'method':'Earliest main-reachable added file from full official Git history; root/current directory and txt/rst extensions checked; Git blob stored unchanged.','recovered_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 (BASE/f'raw/{cid}').mkdir(parents=True,exist_ok=True);(BASE/f'raw/{cid}/recovery.json').write_text(json.dumps(c,indent=2)+'\n')
 print(json.dumps(c))
