"""Verify fixed line bounds and replace handwritten section labels with actual headings."""
import json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def read(n):return json.loads((P/n).read_text())
def write(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
cache={};log=[]
def get(sha,path):
 k=(sha,path)
 if k not in cache:cache[k]=subprocess.check_output(['git','show',sha+':'+path],text=True).splitlines()
 return cache[k]
def ranges(loc):
 result=[]
 for frag in re.findall(r'L\s*(\d+(?:\s*[–-]\s*\d+)?(?:\s*[·,]\s*\d+(?:\s*[–-]\s*\d+)?)*)',loc):
  for part in re.split(r'[·,]',frag):
   ns=[int(x) for x in re.findall(r'\d+',part)];result.append([ns[0],ns[-1]])
 return result

def fix(sha,path,loc,key):
 rr=ranges(loc)
 if not rr or not path.endswith('.md'):return loc
 text=get(sha,path);secs=[]
 for a,b in rr:
  assert 1<=a<=b<=len(text),(key,path,a,b,len(text))
  current='서두(제목 아래)';stack={}
  for i,line in enumerate(text[:b],1):
   m=re.match(r'^(#{2,6})\s+(.+)$',line)
   if m:
    level=len(m[1]);stack={k:v for k,v in stack.items() if k<level};stack[level]=m[2];current=' / '.join(stack.values())
   if i==a or (a<=i<=b and m):
    if current not in secs:secs.append(current)
 new='원 절: '+'; '.join(secs)+'; 행: '+', '.join('L'+str(a)+('–'+str(b) if b!=a else '') for a,b in rr)
 log.append({'id':key,'sha':sha,'path':path,'old_locator':loc,'locator':new,'line_ranges':rr,'actual_sections':secs,'line_count':len(text)})
 return new
claims=read('CLAIM_CHECK.json')
for c in claims:
 old=c['locator'];c['locator']=fix(c['sha'],c['path'],old,c['claim_id'])
 c['line_ranges']=ranges(old);c['locator_review']='고정 원 파일의 실제 절 제목과 행 범위를 확인; 수치·주장 판정은 변경하지 않음'
 f=P/'bundles'/f"{c['bundle_id']}.md";lines=f.read_text().splitlines();out=[]
 for line in lines:
  if c['claim_id'] in line:
   def repl(m):
    if m[2].split('#')[0]==c['source_url'].split('#')[0]:return '['+c['source_task']+' / '+c['locator']+']('+m[2]+')'
    return m[0]
   line=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',repl,line)
  out.append(line)
 f.write_text('\n'.join(out)+'\n')
write('CLAIM_CHECK.json',claims)
bs=read('bundles.json')
for b in bs['bundles']:
 for i,r in enumerate(b['source_refs']):r['locator']=fix(r['sha'],r['path'],r['locator'],b['id']+':ref'+str(i))
write('bundles.json',bs)
cs=read('evidence/conflicts-data.json');md=(P/'CONFLICTS.md').read_text()
for c in cs:
 for i,r in enumerate(c['source_refs']):
  old=r['locator'];new=fix(r['sha'],r['path'],old,c['id']+':ref'+str(i));r['locator']=new
  oldlabel=f"[{r['task']} · {r['path'].split('/')[-1]} · {old}]";newlabel=f"[{r['task']} · {r['path'].split('/')[-1]} · {new}]";md=md.replace(oldlabel,newlabel)
write('evidence/conflicts-data.json',cs);(P/'CONFLICTS.md').write_text(md)
write('evidence/locator-check.json',{'status':'fixed_line_bounds_and_section_labels_verified','source_objects':len(cache),'normalizations':log,'note':'원 고정 파일·행은 유지했다. 통합 초안의 손기입 Q/절 번호 일부를 실제 제목으로 바로잡았다. 이는 앞선 원 결과의 새 불일치 건수에 가산하지 않는다. 수정 전 분산 감사 파일은 원 작업 메모이며 canonical CLAIM_CHECK·bundles·CONFLICTS가 최종 위치다.'})
print('checked/normalized',len(log),'locators across',len(cache),'fixed files')
