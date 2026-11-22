"""Build literal N/H components; never writes action decisions or answer keys."""
from pathlib import Path
from urllib.parse import urlsplit
import sys,json,hashlib,csv,re
ROOT=Path(__file__).resolve().parent;TASK=ROOT.parents[1]
sys.path.insert(0,str(ROOT));from parse_html import parse
def sha(b):return hashlib.sha256(b).hexdigest()
attempts=[json.loads(x) for x in (ROOT/'attempts.jsonl').read_text().splitlines()]
byid={x['attempt_id']:x for x in attempts}
sources=[json.loads(x) for x in (ROOT/'sources.jsonl').read_text().splitlines() if json.loads(x)['source_id'].startswith('G-B')]
def rawtext(path,kind='html'):
    p=ROOT/path;b=p.read_bytes()
    if kind=='html':d=parse(p);return d['text'],b,d['normalization']
    return b.decode('utf8',errors='replace'),b,'UTF-8 decode, errors=replace; no whitespace or markup changes'
def excerpt(path,source_id,start,end=None,kind='html',max_chars=1600,after=0):
    t,b,normal=rawtext(path,kind);s=t.index(start,after);e=t.index(end,s+len(start)) if end else s+len(start)
    while e>s and t[e-1].isspace():e-=1
    assert e-s<=max_chars,(source_id,e-s)
    out=t[s:e]
    return {'source_id':source_id,'path':str((ROOT/path).relative_to(TASK)),'source_sha256':sha(b),'normalized_text_sha256':sha(t.encode()),'normalization':normal,'start_char':s,'end_char':e,'source_line_approx':b[:b.find(start.encode())].count(b'\n')+1 if start.encode() in b else None,'text':out,'text_sha256':sha(out.encode()),'text_bytes':len(out.encode()),'text_chars':len(out),'truncated':False}
def source(id,title,attempt_ids,category,edition,date,case_ids,observed,limit,locations=None,count=True,group=None):
    rows=[byid[x] for x in attempt_ids]
    s={'source_id':id,'kind':category,'publisher':'IEEE / The Open Group' if id in ['G-N01','G-H04','G-X01'] else 'GitHub project maintainers' if id in ['G-N02','G-H02','G-H05'] else 'GNU project / FSF','publication_title':title,'original_url':rows[0]['url'],'fixed_url':rows[0]['url'] if category.startswith('historical') or category=='dated_publisher_announcement' else None,'edition':edition,'publication_date':date,'checked_utc':rows[0]['finished_utc'],'observations':[{'attempt_id':r['attempt_id'],'url':r['url'],'final_url':r.get('final_url'),'sha256':r['sha256'],'checked_utc':r['finished_utc']} for r in rows],'read_location':locations or [],'verified_content':observed,'question_ids':['Q2','Q6'],'case_ids':case_ids,'limits':limit,'duplicate_group':group or id,'count_toward_minimum':count,'minimum_categories':['current'] if category=='current_destination_text' else ['historical'] if category in ['historical_version_document','historical_version_member','historical_distribution','dated_publisher_announcement'] else [],'read_status':'necessary_content_confirmed' if count else 'opened_read_but_not_minimum_eligible'}
    sources.append(s);return s

posix_title=excerpt('current/POSIX-mindex.html','G-N01','The Open Group Base Specifications Issue 7, 2018 edition','IEEE Std')
posix_newer=excerpt('current/POSIX-mindex.html','G-N01','A newer edition of this standard exists')
posix_shell=excerpt('current/POSIX-shell.html','G-N01','The shell is a command language interpreter.')
completion=excerpt('current/G02.html','G-N02','Introduction','Installation',after=3500)
gawk_current=excerpt('current/G04.html','G-N04','12.4 Two-Way','As is the case')
gcc_current=excerpt('current/G05.html','G-N05','-MM ¶','-MF file')
gettext_current=excerpt('current/G06.html','G-N06','gettext-1.0.tar.gz','gettext-runtime-0.13.1')

h_bash=excerpt('history/bash-5.1-announcement.html','G-H01','Bash is the GNU Project','Please use `bashbug')
h_completion=excerpt('history/bash-completion-2.11-README.md','G-H02','## Introduction','## Installation',kind='text')
h_completion_release=excerpt('history/bash-completion-release-2.11.html','G-H05','Main things to notice in this release:','Other than that')
h_gawk_preface=excerpt('history/gawk-5.0.1/doc/gawk.info','G-H06','(1) The 2008 POSIX standard','(2)',kind='text')
t=(ROOT/'history/gawk-5.0.1/doc/gawk.info').read_text();gawk_node=t.index('File: gawk.info,  Node: Two-way I/O')
h_gawk=excerpt('history/gawk-5.0.1/doc/gawk.info','G-H06',"However, with 'gawk'",'There are some cautionary',kind='text',after=gawk_node)
h_gcc=excerpt('history/gcc-10.1.0-preprocessor.html','G-H03','-MM','-MF')
h_gettext=excerpt('history/gettext-0.21-announcement.html','G-H07','Download:','Here are the GPG')

source('G-N01','The Open Group Base Specifications Issue 7, 2018 edition',['G-NGET001','G-NGET003','G-NGET007','G-NGET008','G-NGET009'],'current_destination_text','2018 edition / IEEE1003.1-2017',None,['G01','G03'],'HTTP original G01 actually301→HTTPS200; G03directHTTPS200. The frame points to mindex; its Utilities table leads to the actual Shell Command Language chapter. Edition, shell-language text, and notice of a newer edition read.','One manuscript across scheme/frame/contents/chapter, counted once. Current text itself discloses edition history; no claim that this is the latest standard.',[posix_title,posix_newer,posix_shell],group='POSIX-Issue7-2018')
source('G-N02','bash-completion README rendered on project repository',['G-NGET002'],'current_destination_text','default-branch observation',None,['G02'],'Introduction identifies command-line completion recipes, helper functions and automatic loading.','Default branch is mutable. Full page also discusses older Bash versions; the selected introduction does not. Actual shell execution is untested.',[completion],group='bash-completion-readme-current')
source('G-N04','GNU Awk User’s Guide, Two-way I/O',['G-NGET004'],'current_destination_text','current GNU manual observation',None,['G04'],'Original fragment exists; §12.4 explains |& coprocess communication and print/printf/getline.','The actual mechanism paragraph was read; no execution of a coprocess.',[gawk_current],group='gawk-manual-current')
source('G-N05','GCC Preprocessor Options',['G-NGET005'],'current_destination_text','current GCC manual observation',None,['G05'],'Original fragment and index-MM exist. The -MM paragraph excludes system headers and explains inclusion delimiters.','Current document has new long-option names; no compiler execution/compatibility test.',[gcc_current],group='gcc-preprocessor-current')
source('G-N06','GNU gettext official distribution directory',['G-NGET006'],'current_destination_text','directory observation',None,['G06'],'The actual listing contains stable gettext-1.0 source archives dated2026-01-28 and prior version entries.','Listing dates are not first release timestamps. G-GET035 saw this same directory during sampling; source was already exposed before B seal.',[gettext_current],group='gnu-gettext-directory-current')
source('G-H01','Bash-5.1 release available',['G-HGET001'],'dated_publisher_announcement','Bash5.1','2020-12-07T15:47:25Z',['G01','G02'],'Publisher describes POSIX shell implementation, reference/manual-page roles, and included formatted HTML documents.','Does not identify a POSIX standard edition or prove current target accessibility.',[h_bash],group='bash51-release-announcement')
source('G-H02','bash-completion2.11 README',['G-HGET002'],'historical_version_member','tag2.11; release page links commit b12639a','2020-07-25T11:58:23Z (release metadata in G-H05)',['G02'],'Tagged README describes its collection of Bash completions and helper/loading facilities.','Tag is a version pointer, not itself an immutable full commit pin; read bytes hashed. Current target not implied.',[h_completion],group='bash-completion-readme-2.11')
source('G-H03','GCC10.1.0 Preprocessor Options',['G-HGET003'],'historical_version_document','GCC10.1.0','2020-05-07T11:36:26Z HTTP Last-Modified, not proven first publication',['G05'],'Versioned archived manual states the older -MM/system-header rule.','Historical exact version path and body hash; server timestamp is not independent publication clock.',[h_gcc],group='gcc-preprocessor-10.1.0')
source('G-H04','IEEE/Open Group1003.1-2017 catalog record',['G-HGET004'],'publisher_historical_catalog','1003.1-2017','Published2018-01-31; BoardApproval2017-12-06',['G01','G03'],'Publisher catalog records 2017-labelled standard published2018 and its four volumes.','CURRENT catalog also includes supersession by2024. Not an archived2018 snapshot, omitted from H packets and strict historical minimum.',count=False,group='ieee2017-catalog-current')
source('G-H05','bash-completion2.11 release notes',['G-HGET005'],'dated_publisher_announcement','2.11','2020-07-25T11:58:23Z',['G02'],'Release notes state oldest supported Bash version4.2 and nounset compatibility; source datetime attribute read.','Release text can be edited; not an assertion about current default branch. Title/notes are distinct from tagged README.',[h_completion_release],group='bash-completion-release-2.11')
source('G-H06','GAWK Effective AWK Programming User’s Guide5.0.1',['G-HGET006'],'historical_distribution','Edition5.0 for gawk5.0.1; GNU info member','2019-06-18 14:02 GNU archive listing',['G03','G04'],'Historical Preface calls the standard2008 at older www.opengroup URL; Two-way I/O node describes the |& mechanism.','One full info manuscript reused for2references. This is distributed info, not claimed historical HTML. Whole member differs from B5.1 HTML; selected historical citation sentence changes2008→2018 in B.',[h_gawk_preface,h_gawk],group='gawk-userguide-5.0.1')
source('G-H07','GNU gettext0.21 released',['G-HGET011'],'dated_publisher_announcement','GNU gettext0.21','2020-07-27T01:13:37Z',['G06'],'Dated publisher announcement gives source tar.gz/tar.xz downloads at ftp.gnu.org/gnu/gettext.','An old release announcement identifies historical distribution; it cannot identify the newest release at a later request.',[h_gettext],group='gettext021-release-announcement')
source('G-X01','Open Group2018 retrospective',['G-HGET008'],'auxiliary_read','2019 retrospective','2019-01-15',['G01','G03'],'Body discusses2018 certifications but no POSIX edition identification was found in the read section.','Search lead not sufficient for H; excluded from cards and minimum.',count=False,group='opengroup-2018-retrospective')

Nparts={'G01':[posix_title,posix_newer,posix_shell],'G02':[completion],'G03':[posix_title,posix_newer,posix_shell],'G04':[gawk_current],'G05':[gcc_current],'G06':[gettext_current]}
Hparts={'G01':[h_bash],'G02':[h_completion,h_completion_release],'G03':[h_gawk_preface],'G04':[h_gawk],'G05':[h_gcc],'G06':[h_gettext]}
Hmeta={'G01':[('G-H01','Bash5.1 publisher announcement','2020-12-07T15:47:25Z')],'G02':[('G-H02','bash-completion2.11 README','release2020-07-25T11:58:23Z'),('G-H05','release2.11 notes','2020-07-25T11:58:23Z')],'G03':[('G-H06','gawk5.0.1 GNU info Preface','archive listing2019-06-18 14:02')],'G04':[('G-H06','gawk5.0.1 GNU info Two-way I/O','archive listing2019-06-18 14:02')],'G05':[('G-H03','GCC10.1.0 manual','HTTP Last-Modified2020-05-07T11:36:26Z')],'G06':[('G-H07','GNU gettext0.21 release','2020-07-27T01:13:37Z')]}
extra_attempts={'G01':['G-NGET007','G-NGET008','G-NGET009'],'G03':['G-NGET007','G-NGET008','G-NGET009']}
section={'G01':'https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18','G02':'https://github.com/scop/bash-completion/#introduction','G03':'https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html','G04':byid['G-NGET004']['url'],'G05':'https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#index-MM','G06':byid['G-NGET006']['url']}
src={s['source_id']:s for s in sources};rows=[];(ROOT/'components').mkdir(exist_ok=True)
for i in range(1,7):
    rid=f'G{i:02}';a=byid[f'G-NGET{i:03}'];ne=Nparts[rid];he=Hparts[rid]
    nt='\n\n'.join(x['text'] for x in ne);ht='\n\n'.join(x['text'] for x in he);assert len(nt)<=1600;assert len(ht)<=1600
    frag=urlsplit(a['url']).fragment
    raw=(TASK/a['stored_path']).read_text(errors='replace')
    fragment_present=(bool(re.search(r'(?:id|name)=[\"\x27]'+re.escape(frag)+r'[\"\x27]',raw)) if frag else None)
    n={'text':nt,'text_sha256':sha(nt.encode()),'text_chars':len(nt),'text_bytes':len(nt.encode()),'source_ids':list(dict.fromkeys(x['source_id'] for x in ne)),'excerpts':ne,'original_request':{k:a.get(k) for k in ['url','status','redirect_chain','final_url','started_utc','finished_utc','sha256','attempt_id']},'additional_request_ids':extra_attempts.get(rid,[]),'current_section_url':section[rid],'original_fragment':frag or None,'original_fragment_exists':fragment_present,'required_section_exists':True,'text_history_overlap':rid in ['G01','G03'],'source_contains_history':rid in ['G01','G02','G03','G06'],'history_overlap_location':'newer edition notice and previous-edition links in mindex' if rid in ['G01','G03'] else 'README later contains older-Bash version discussion outside selected introduction' if rid=='G02' else 'directory includes dated older release entries outside selected latest1.0 entries' if rid=='G06' else None,'empty_reason':None}
    h={'text':ht,'text_sha256':sha(ht.encode()),'text_chars':len(ht),'text_bytes':len(ht.encode()),'source_ids':list(dict.fromkeys(x['source_id'] for x in he)),'excerpts':he,'historical_documents':[{'source_id':sid,'edition_or_document':ed,'event_or_publication_time':dt,'url':src[sid]['original_url']} for sid,ed,dt in Hmeta[rid]],'empty_reason':None,'contains_current_observation':False,'contains_collector_recommendation':False,'contains_answer_key':False,'time_basis_limit':'Publication/listing/edition time separate from retrievalUTC; see source rows. No present access assertion in H text.'}
    row={'reference_id':rid,'N':n,'H':h,'decision_or_adjudication_written':False}
    rows.append(row)
    for name,data in [('N',nt),('H',ht)]: (ROOT/'components'/f'{rid}-{name}.txt').write_text(data,encoding='utf8')
    (ROOT/'components'/f'{rid}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(ROOT/'evidence-components.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf8')
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in sources),encoding='utf8')

fields=['attempt_id','operation','role','case_ids','url','started_utc','finished_utc','status','failed','redirect_hops','minimum_http_requests','received_body_bytes','stored_response_bytes','elapsed_seconds','measurement','wire_bytes','logical_uses','notes']
with (ROOT/'costs.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
    for a in attempts:
        cs=list(a.get('case_ids',[]))
        if a['attempt_id']=='G-HGET006':cs=['G03','G04']
        w.writerow({'attempt_id':a['attempt_id'],'operation':a.get('operation'),'role':a.get('role','discovery_search'),'case_ids':';'.join(cs),'url':a.get('url',''),'started_utc':a.get('started_utc',a.get('queried_utc','')),'finished_utc':a.get('finished_utc',''),'status':a.get('status',''),'failed':bool(a.get('error')) if a.get('operation')=='GET' else '', 'redirect_hops':len(a.get('redirect_chain',[])) if a.get('operation')=='GET' else '', 'minimum_http_requests':1+len(a.get('redirect_chain',[])) if a.get('operation')=='GET' else '', 'received_body_bytes':a.get('received_body_bytes',''),'stored_response_bytes':a.get('stored_bytes',''),'elapsed_seconds':a.get('elapsed_seconds',''),'measurement':'actual_response_body_and_tool_elapsed' if a.get('operation')=='GET' else 'unmetered_search','wire_bytes':'unmeasured','logical_uses':len(cs),'notes':'Parallel request elapsed cannot be summed as researcher wall time. Body bytes exclude intermediate redirect bodies and protocol overhead. Card reading/human/service cost unmeasured.'})
summary={'N_components':len(rows),'H_components':len(rows),'N_raw_chars':{r['reference_id']:r['N']['text_chars'] for r in rows},'H_raw_chars':{r['reference_id']:r['H']['text_chars'] for r in rows},'N_unique_manuscripts':len({s['duplicate_group'] for s in sources if s['count_toward_minimum'] and 'current' in s['minimum_categories']}),'H_unique_manuscripts':len({s['duplicate_group'] for s in sources if s['count_toward_minimum'] and 'historical' in s['minimum_categories']}),'source_minimum_total':sum(s['count_toward_minimum'] for s in sources),'N_window_start':byid['G-NGET001']['started_utc'],'N_window_end':byid['G-NGET009']['finished_utc'],'current_history_overlap_source':['G01','G02','G03','G06'],'current_history_overlap_excerpt':['G01','G03'],'same_N_duplicate_source':['G01','G03'],'same_H_manuscript_used_twice':['G03','G04'],'measurement_scope':'retrieval only; no action decisions, no key, no C0 discovery labor or service-cost measurement'}
(ROOT/'nh-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
