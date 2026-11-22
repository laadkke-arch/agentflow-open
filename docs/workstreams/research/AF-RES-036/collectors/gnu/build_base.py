from pathlib import Path
import sys,json,hashlib,csv,tarfile,io,re
sys.path.insert(0,str(Path(__file__).resolve().parent))
from parse_html import parse
ROOT=Path(__file__).resolve().parent
TASK=ROOT.parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
attempts=[json.loads(l) for l in (ROOT/'attempts.jsonl').read_text().splitlines()]
def att(name): return [r for r in attempts if r.get('stored_path','').endswith('/'+name) and r.get('status')==200][-1]
items=[
 dict(reference_id='G01',project='bash',publication_id='bash-manual-page',publication_title='BASH(1) Manual Page',version='Bash 5.1',archive='bash-5.1.tar.gz',member='bash-5.1/doc/bash.html',href='http://pubs.opengroup.org/onlinepubs/9699919799/',start='Portable Operating System Interface (POSIX) Part 2:',end='http://tiswww.case.edu/~chet/bash/POSIX',purpose='Bash man page의 SEE ALSO가 지목한 POSIX Part 2 Shell and Utilities 규격을 읽는다.',stratum='ambiguous',stratum_basis='문장은 Part 2와 Shell and Utilities 대상을 명명하나 연도/판 또는 최신판 요구를 명시하지 않는다. URI의 숫자를 목적 문장의 역사판 의도로 대신하지 않는다.',publication_date='2020-12-06 15:44',date_basis='GNU archive index date, not first public delivery timestamp',prior_exposure=False),
 dict(reference_id='G02',project='bash',publication_id='bash-reference-manual',publication_title='GNU Bash Reference Manual',version='Edition 5.1, Bash 5.1, updated 29 October 2020',archive='bash-5.1.tar.gz',member='bash-5.1/doc/bashref.html',href='https://github.com/scop/bash-completion/',start='Many more examples',end='An older version of the bash_completion package',purpose='일반 GNU/Unix/Linux 명령에 대한 programmable completion 예제 모음을 찾아 읽는다.',stratum='current',stratum_basis='본문은 더 많은 예제가 available하고 프로젝트가 now lives하는 주소를 제공한다. 특정 completion 릴리스 재현은 요구하지 않는다.',publication_date='2020-12-06 15:44',date_basis='GNU archive index date; manual itself says updated 2020-10-29',prior_exposure=False),
 dict(reference_id='G03',project='gawk',publication_id='gawk-user-guide',publication_title='The GNU Awk User’s Guide',version='gawk 5.1.0 / Debian gawk-doc 5.1.0-1',archive='gawk-doc_5.1.0-1_all.deb',member='gawk-doc_5.1.0-1_all/usr/share/doc/gawk-doc/gawk-html/Preface.html',href='https://pubs.opengroup.org/onlinepubs/9699919799/',start='The 2018 POSIX standard is accessible online at',end='(2)',purpose='Preface 각주가 명시한 2018 POSIX standard를 읽는다.',stratum='historical',stratum_basis='The 2018 POSIX standard라는 연도가 인용 문장에 명시되어 있다.',publication_date='2021-02-10 14:55',date_basis='Debian archive index date for binary documentation package',prior_exposure=False),
 dict(reference_id='G04',project='gawk',publication_id='gawk-tcpip-manual',publication_title='TCP/IP Internetworking With gawk',version='gawk 5.1.0 / Debian gawk-doc 5.1.0-1',archive='gawk-doc_5.1.0-1_all.deb',member='gawk-doc_5.1.0-1_all/usr/share/doc/gawk-doc/gawkinet-html/Gawk-Special-Files.html',href='https://www.gnu.org/software/gawk/manual/html_node/Two_002dway-I_002fO.html#Two_002dway-I_002fO',start='The ‘|&’ operator',end='gawk transparently extends',purpose='gawk networking을 읽기 전에 coprocess에 print/printf로 보내고 getline으로 받는 양방향 I/O를 이해한다.',stratum='current',stratum_basis='If you haven’t read it already, you should detour there to do so라는 사용 안내이며 외부 매뉴얼의 특정 판을 지정하지 않는다.',publication_date='2021-02-10 14:55',date_basis='Debian archive index date for binary documentation package',prior_exposure=False),
 dict(reference_id='G05',project='make',publication_id='gnu-make-manual',publication_title='GNU Make manual',version='GNU Make 4.3 / Debian make-doc 4.3-2',archive='make-doc_4.3-2_all.deb',member='make-doc_4.3-2_all/usr/share/doc/make-doc/make.html/Rules.html',href='https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#Preprocessor-Options',start='With the GNU C compiler, you may wish to use',end='The purpose of the sed command',purpose='자동 prerequisites를 만들 때 GCC -M 대신 -MM을 쓰면 system header를 제외하는 이유와 옵션 상세를 읽는다.',stratum='current',stratum_basis='may wish to use the -MM flag instead of -M이라는 현재 작업 안내이고 GCC의 특정 판을 요구하지 않는다.',publication_date='2020-05-20 08:41',date_basis='Debian archive index date for binary documentation package',prior_exposure=False),
 dict(reference_id='G06',project='gettext',publication_id='gnu-gettext-faq',publication_title='GNU gettext FAQ',version='GNU gettext distribution 0.20.2',archive='gettext-0.20.2.tar.xz',member='gettext-0.20.2/gettext-tools/doc/FAQ.html',href='https://ftp.gnu.org/gnu/gettext/',start='Where is the newest gettext source?',end='Prereleases are announced',purpose='GNU gettext의 newest stable source release가 배포되는 위치를 찾는다.',stratum='current',stratum_basis='Where is the newest gettext source? The newest gettext release is available라는 명시 문장.',publication_date='2020-04-14 05:48',date_basis='GNU archive index date, not first public delivery timestamp',prior_exposure=True),
]
refs=[];sources=[]
(ROOT/'base').mkdir(exist_ok=True)
for item in items:
    d=parse(ROOT/'members'/item['member']);a=att(item['archive'])
    link=next(x for x in d['links'] if x['href']==item['href'])
    start=d['text'].rfind(item['start'],0,link['start']+1);end=d['text'].index(item['end'],link['end'])
    assert start>=0, item['reference_id']
    while end>start and d['text'][end-1].isspace():end-=1
    excerpt=d['text'][start:end];assert len(excerpt)<=1200
    source_id='G-B'+item['reference_id'][1:]
    member=item['member'] if not item['archive'].endswith('.deb') else './'+item['member'].split('/',1)[1]
    rec={k:v for k,v in item.items() if k not in ('start','end','archive','member','href','stratum','prior_exposure')}
    rec.update(source_id=source_id,route='GNU',archive_url=a['url'],archive_sha256=a['sha256'],archive_body_bytes=a['received_body_bytes'],archive_attempt_id=a['attempt_id'],archive_local_path=a['stored_path'],member=member,member_local_path=str((ROOT/'members'/item['member']).relative_to(TASK)),member_sha256=d['member_sha256'],member_bytes=(ROOT/'members'/item['member']).stat().st_size,original_href=item['href'],link_text=link['link_text'],source_line=link['source_line'],text_location={'start_char':start,'end_char':end,'normalization':d['normalization'],'normalized_text_sha256':sha(d['text'].encode())},context=excerpt,context_chars=len(excerpt),context_bytes=len(excerpt.encode()),context_sha256=sha(excerpt.encode()),purpose_stratum=item['stratum'],fetched_utc=a['finished_utc'],pre_exposed_current_target=item['prior_exposure'],exposure_note='G-GET035 fetched the identical current directory URL as a distribution index before selecting this FAQ href; preserve and exclude from strict pre-outcome seal sensitivity.' if item['prior_exposure'] else 'No selected destination was requested before B selection.',current_target_opened_for_decision=False,history_collected=False,selection_rule='first eligible external technical/tool link in publication order; metadata/navigation/license/contact/home links excluded',truncated=False)
    (ROOT/'base'/f"{item['reference_id']}.txt").write_text(excerpt,encoding='utf8')
    (ROOT/'base'/f"{item['reference_id']}.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    refs.append(rec)
    sources.append({'source_id':source_id,'kind':'consumer_distribution_html','publisher':'GNU; Debian official repackaging' if item['archive'].endswith('.deb') else 'GNU','original_url':a['url'],'fixed_url':a['url'],'fixed_locator':a['url']+'!'+member,'publication_title':item['publication_title'],'edition':item['version'],'publication_date':item['publication_date'],'date_basis':item['date_basis'],'checked_utc':a['finished_utc'],'read_location':{'member':member,'source_line':link['source_line'],'text_offsets':[start,end]},'verified_content':item['purpose']+' 원 href와 주변 문장을 직접 읽음.','question_ids':['Q1','Q2','Q6'],'case_ids':[item['reference_id']],'limits':'원 소비자 배포 원문 확인. 현재 목적지 적합성·과거 목적지 본문은 아직 판정하지 않음. 배포 목록 날짜는 첫 공개 시각 증명이 아님.','duplicate_group':item['publication_id']+'@'+item['version'],'count_toward_minimum':True,'minimum_categories':['consumer'],'read_status':'necessary_content_confirmed','member_sha256':d['member_sha256'],'excerpt_sha256':sha(excerpt.encode())})
(ROOT/'references.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in refs),encoding='utf8')
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in sources),encoding='utf8')

# All obtained archive HTML inventories. Listing/404/failure records remain in attempts.
inventory=[]
for f in sorted(ROOT.iterdir()):
    if f.suffix not in ('.gz','.xz','.deb'):continue
    raw=f.read_bytes()
    try:
        if f.suffix=='.deb':
            offset=8;tf=None
            while offset<len(raw):
                hdr=raw[offset:offset+60];name=hdr[:16].decode().strip().rstrip('/');size=int(hdr[48:58]);body=raw[offset+60:offset+60+size];offset+=60+size+(size%2)
                if name.startswith('data.tar'):tf=tarfile.open(fileobj=io.BytesIO(body));break
        else:tf=tarfile.open(fileobj=io.BytesIO(raw))
        members=[m.name for m in tf.getmembers() if m.isfile() and m.name.endswith(('.html','.htm'))]
        a=att(f.name);chosen=[r['reference_id'] for r in refs if r['archive_url']==a['url']]
        inventory.append({'candidate_id':'G-C'+str(len(inventory)+1).zfill(2),'project':f.name.split('-')[0].split('_')[0],'archive':f.name,'url':a['url'],'archive_sha256':sha(raw),'date_basis':'see linked distribution index, not member mtime','html_members':len(members),'selected_references':';'.join(chosen),'outcome':'selected' if chosen else 'no_built_html' if not members else 'not_selected','reason':'independent publication and first eligible external href' if chosen else 'no built HTML members in actual archive' if not members else 'excluded or later publication in fixed order','attempt_id':a['attempt_id']})
    except Exception as e:
        inventory.append({'candidate_id':'G-C'+str(len(inventory)+1).zfill(2),'project':f.name.split('-')[0],'archive':f.name,'url':'','archive_sha256':sha(raw),'date_basis':'','html_members':'unknown','selected_references':'','outcome':'parse_failed','reason':str(e),'attempt_id':''})
with (ROOT/'frame.csv').open('w',encoding='utf8',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=list(inventory[0]),lineterminator='\n');w.writeheader();w.writerows(inventory)
(ROOT/'base-seal-summary.json').write_text(json.dumps({'references':len(refs),'distinct_publications':len({r['publication_id'] for r in refs}),'projects':sorted({r['project'] for r in refs}),'historical_refs':[r['reference_id'] for r in refs if r['purpose_stratum']=='historical'],'prior_exposed_current_target_refs':[r['reference_id'] for r in refs if r['pre_exposed_current_target']],'selected_destination_gets_before_seal':1,'rule':'one source row per independent book/man/FAQ, not per split chapter','archive_inventories':len(inventory)},ensure_ascii=False,indent=2)+'\n')
print('B refs built',len(refs),'source manuscripts',len(sources),'frame archives',len(inventory))
