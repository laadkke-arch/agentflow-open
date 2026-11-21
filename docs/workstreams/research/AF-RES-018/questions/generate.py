#!/usr/bin/env python3
"""Build/reproduce non-identifying question metadata; never persist source bodies.
Original input prints only after exact normalized question-text SHA-256 validation.
"""
from pathlib import Path
import subprocess,json,random,hashlib,urllib.request,urllib.error,datetime,re,html,argparse
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
SHA011='478c301b693896e2c6d777f46ac441f071bfdfe8'
SHA014='42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9'
def git_json(sha,path):return json.loads(subprocess.check_output(['git','show',sha+':docs/workstreams/research/'+path],text=True))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
class Plain(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_data(self,d):self.parts.append(d)
 def handle_starttag(self,t,a):
  if t in ['p','li','br','pre','blockquote','h1','h2','h3']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['p','li','pre','blockquote']:self.parts.append('\n')
def text_of(body,title=''):
 p=Plain();p.feed(body);return '\n'.join(' '.join(x.split()) for x in (html.unescape(title)+'\n'+''.join(p.parts)).splitlines() if x.strip())
def request_json(url):
 req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-018-public-research/1.0'})
 with urllib.request.urlopen(req,timeout=25) as r:return json.load(r),r.status

def select_old():
 cases=git_json(SHA011,'AF-RES-011/CASES.json')['cases'];ns=git_json(SHA011,'AF-RES-011/evidence/near-misses.json')['pairs'];req={x['case_id'] for x in ns if x.get('count_as_near_miss') and x['sample']=='main'};rng=random.Random(18018);ids=[]
 for scope in ['whole','part']:
  fixed=sorted(x['id'] for x in cases if x['id'] in req and x['whole_or_part']==scope);pool=sorted(x['id'] for x in cases if x['id'] not in req and x['whole_or_part']==scope);ids+=fixed+rng.sample(pool,15-len(fixed))
 meta={x['id']:x for x in git_json(SHA014,'AF-RES-014/queries/metadata.json')}
 rows=[]
 for c in cases:
  if c['id'] not in ids:continue
  m=meta[c['id']];rows.append({'id':c['id'],'cohort':'011','source_subset':'main','source_sha':SHA011,'url':c['url'],'date':c['date'],'platform':c['platform'],'whole_or_part':c['whole_or_part'],'I5':m['I5'],'must':m['must'],'constraints':c.get('constraints',[]),'question_summary':c['question_summary'],'question_summary_source':'011 CASES.json question_summary','input_mode':'pending','initial_retrieval':None})
 supplements=[('SX01','35392','2016-08-16','whole','present','Evernote에서 독립해 자기 데이터를 개방형 파일로 보유하고 다른 도구로 처리할 수 있는 노트 대안을 찾는다.','데이터의 공개 형식과 앱 독립성'),('SX08','84072','2022-09-22','whole','present','기존 텍스트의 단어 길이·순서·문장부호와 외형을 보존하면서 알아볼 수 없는 텍스트로 바꾸는 도구를 찾는다.','기존 텍스트 길이·순서·문장부호 보존'),('SXR05','26907','2015-12-02','part','present','Java의 String 또는 String[] 명령행에서 미리 옵션 목록을 선언하지 않고 임의 옵션과 값을 추출할 파서를 찾는다. Map 반환은 선호다.','임의 옵션 이름 수용')]
 for sid,qnum,date,scope,i5,summ,must in supplements:
  n=next(x for x in ns if x['case_id']==sid);rows.append({'id':sid,'cohort':'011','source_subset':'supplementary','source_sha':SHA011,'url':n['url'],'date':date,'platform':'softwarerecs','whole_or_part':scope,'I5':i5,'must':[{'target':must,'polarity':'positive'}],'constraints':[{'target':must,'polarity':'positive','force':'must'}],'question_summary':summ,'question_summary_source':'worker paraphrase of fixed011 supplement; no original body stored','input_mode':'pending','initial_retrieval':None})
 return rows

def fetch_old():
 rows=select_old();logs=[];se=[r for r in rows if r['platform']=='softwarerecs'];nums=[re.search(r'/questions/(\d+)',r['url']).group(1) for r in se];u='https://api.stackexchange.com/2.3/posts/'+';'.join(nums)+'/revisions?site=softwarerecs&filter=withbody&pagesize=100';at=now();d,status=request_json(u);logs.append({'url':u,'at_utc':at,'status':status,'item_count':len(d.get('items',[])),'has_more':d.get('has_more'),'body_saved':False})
 items=d.get('items',[])
 if d.get('has_more'):
  for page in range(2,6):
   uu=u+'&page='+str(page);dd,ss=request_json(uu);logs.append({'url':uu,'at_utc':now(),'status':ss,'item_count':len(dd.get('items',[])),'has_more':dd.get('has_more'),'body_saved':False});items+=dd.get('items',[])
   if not dd.get('has_more'):break
 for r in rows:
  if r['platform']=='softwarerecs':
   num=int(re.search(r'/questions/(\d+)',r['url']).group(1));found=[x for x in items if x.get('post_id')==num and x.get('revision_number')==1 and x.get('body')]
   if found:
    x=found[0];body=x['body'];text=text_of(body,x.get('title',''));guid=x['revision_guid'];r['input_mode']='original';r['initial_retrieval']={'url':'https://api.stackexchange.com/2.3/revisions/'+guid+'?site=softwarerecs&filter=withbody','revision_guid':guid,'revision_number':1,'at_utc':at,'status':status,'body_html_sha256':hashlib.sha256(body.encode()).hexdigest(),'question_sha256':hashlib.sha256(text.encode()).hexdigest(),'word_count':len(text.split()),'normalization':'questions.generate.text_of v1; title + rendered body; paragraph lines; collapse spaces','creation_date_utc':datetime.datetime.fromtimestamp(x['creation_date'],datetime.timezone.utc).isoformat()};r['date']=r['initial_retrieval']['creation_date_utc'][:10];r['sha256']=r['initial_retrieval']['question_sha256'];r['word_count']=len(text.split());print('\nORIGINAL',r['id'],r['date'],r['sha256'],'\n'+text)
   else:r['input_mode']='summary';r['initial_retrieval']={'url':u,'at_utc':at,'status':status,'reason':'revision1 body not returned'}
  else:
   r['input_mode']='summary';r['initial_retrieval']={'url':r['url'],'status':'pending_original_attempt','reason':'history/first version not yet verified'}
  if r['input_mode']=='summary':r['sha256']=hashlib.sha256(r['question_summary'].encode()).hexdigest();r['word_count']=len(r['question_summary'].split())
  inp={'case_id':r['id'],'question_date':r['date'],'question_url_excluded_from_search':r['url'],'input_mode':r['input_mode'],'question_sha256':r['sha256'],'question_source':r.get('initial_retrieval'),'question_summary':r['question_summary'] if r['input_mode']=='summary' else None,'read_original_command':('python '+str(Path(__file__).relative_to(Path.cwd()))+' --emit '+r['id']) if r['input_mode']=='original' else None,'common_run_instructions':'Read this question only and assigned condition rules. Original command retrieves only fixed question revision, never answers; no source body is saved. Do not read metadata/gold/other runs. User cap is <=10 candidates, <=12 search queries, <=20 open attempts including check stage. A uses unchanged RULES_A A section. Freeze discovery raw answer and rank before asking parent for three blind check candidates. Checks use remaining same budget; do not edit discovery after injection. Record literal queries, actual URLs, UTC times, post-question/unknown dates, exposures. Write only assigned run JSON.'}
  (ROOT/'questions/inputs'/f"{r['id']}.json").write_text(json.dumps(inp,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'questions/old-metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(ROOT/'questions/original-retrieval.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n');(ROOT/'questions/selection.json').write_text(json.dumps({'seed':18018,'main_ids':sorted(r['id'] for r in rows if r['source_subset']=='main'),'supplement_ids':['SX01','SX08','SXR05'],'rationale':'all 8 main strict-N threads mandatory; seeded fill to whole15/part15; all3 strict-N supplements added'},ensure_ascii=False,indent=2)+'\n')

def emit(qid):
 inp=json.loads((ROOT/'questions/inputs'/f'{qid}.json').read_text())
 if inp['input_mode']=='summary':print(inp['question_summary']);return
 d,status=request_json(inp['question_source']['url']);x=next(x for x in d['items'] if x.get('revision_guid')==inp['question_source']['revision_guid'] and x.get('body'));t=text_of(x['body'],x.get('title',''));sha=hashlib.sha256(t.encode()).hexdigest()
 if sha!=inp['question_sha256']:raise SystemExit('INPUT HASH MISMATCH: do not silently substitute a current question')
 print('Verified question-only input. SHA256:',sha,'HTTP:',status,'UTC:',now());print(t)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fetch-old',action='store_true');p.add_argument('--emit');a=p.parse_args()
 if a.fetch_old:fetch_old()
 elif a.emit:emit(a.emit)
