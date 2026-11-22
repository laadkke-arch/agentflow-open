#!/usr/bin/env python3
"""Canonical source ledger and conservative AF-RES-030 minimum-count audit.

Only writes sources.jsonl and evidence/source-counts.json beside this script.
Reads committed stream ledgers, never ignored original downloads. The compiler
aggregates each named researcher's direct-reading receipt; aggregation is not a
new independent reading of an external source. No network, Git or source edits.
"""
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from collections import defaultdict, Counter
import csv
import datetime as dt
import hashlib
import json
import re

P=Path(__file__).resolve().parent
SEAL='9de54923257d613359348c8ccee2ff8225c8a0d8'
INPUTS={}
EVENTS=[]
INITIAL={}
CHAINS={}
SCREEN={}
FRAME=[]

def rel(path): return str(path.relative_to(P))
def digest(b): return hashlib.sha256(b).hexdigest()
def read_jsonl(path):
    data=path.read_bytes();INPUTS[rel(path)]=digest(data)
    return [(j,json.loads(s))for j,s in enumerate(data.decode().splitlines(),1)if s.strip()]
def read_csv(path):
    data=path.read_bytes();INPUTS[rel(path)]=digest(data)
    return [(j,r)for j,r in enumerate(csv.DictReader(data.decode().splitlines()),2)]
def as_list(x):
    if x is None:return []
    if isinstance(x,list):return x
    return [x]
def unique(xs):
    out=[];seen=set()
    for x in xs:
        k=json.dumps(x,ensure_ascii=False,sort_keys=True)
        if k not in seen:out.append(x);seen.add(k)
    return out
def truth(x):return x is True or str(x).lower()=='true'
def flatten_links(x):
    if isinstance(x,dict):return [y for v in x.values()for y in flatten_links(v)]
    return as_list(x)
def iso_key(x):
    if not x:return ''
    try:return dt.datetime.fromisoformat(x.replace('Z','+00:00')).isoformat()
    except (ValueError,AttributeError):return ''
def clean_url(url):
    u=urlsplit(url);host=u.netloc.lower();path=u.path.rstrip('/')
    query=urlencode([(k,v)for k,v in parse_qsl(u.query)if k.lower()not in['utm_source','utm_medium','utm_campaign','raw']])
    if host=='api.github.com':
        m=re.match(r'/repos/([^/]+/[^/]+)/(issues|pulls)/(\d+)',path)
        if m: return f"https://github.com/{m[1]}/{'pull'if m[2]=='pulls'else'issues'}/{m[3]}"
    if host=='github.com':
        m=re.match(r'/([^/]+/[^/]+)/(issues|pull)/(\d+)',path)
        if m:return f'https://github.com/{m[1]}/{m[2]}/{m[3]}'
    return urlunsplit(('https',host,path,query,''))
def canonical_key(url):
    u=urlsplit(clean_url(url));host=u.netloc;path=u.path
    if host=='raw.githubusercontent.com':
        a=path.strip('/').split('/',3)
        if len(a)==4:return 'github-file:'+a[0]+'/'+a[1]+':'+a[3]
    if host=='github.com':
        m=re.match(r'/([^/]+/[^/]+)/blob/[^/]+/(.+)',path)
        if m:return 'github-file:'+m[1]+':'+m[2]
    if host in['matplotlib.org','numpy.org','scitools.org.uk']:
        # Equivalent editions of one manual chapter share a resource key.
        path=re.sub(r'^/\d+(?:\.\d+)+(?:/)', '/',path)
        path=re.sub(r'^/doc/\d+(?:\.\d+)+/', '/doc/',path)
        path=re.sub(r'^/cartopy/docs/v\d+(?:\.\d+)+/', '/cartopy/docs/',path)
        return 'document:'+host+path+('?' +u.query if u.query else'')
    return clean_url(url)
def locator(path,line,sid):return dict(file=rel(path),line=line,source_id=sid)

for stream in sorted((P/'streams').iterdir()):
    if not stream.is_dir():continue
    for line,r in read_jsonl(stream/'initial.jsonl'):
        INITIAL[r['case_id']]=dict(row=r,origin=locator(stream/'initial.jsonl',line,r['case_id']),stream=stream.name)
    for line,r in read_jsonl(stream/'chains.jsonl'):
        CHAINS[r['case_id']]=dict(row=r,origin=locator(stream/'chains.jsonl',line,r['case_id']),stream=stream.name)
    for line,r in read_jsonl(stream/'screening-followups.jsonl'):
        SCREEN[r['case_id']]=dict(row=r,origin=locator(stream/'screening-followups.jsonl',line,r['case_id']),stream=stream.name)
    for line,r in read_csv(stream/'frame.csv'):
        FRAME.append(dict(row=r,origin=locator(stream/'frame.csv',line,r.get('frame_id')or r.get('issue_number')),stream=stream.name))

CASE_URL={clean_url(v['row']['root_url']):cid for cid,v in INITIAL.items()}
SELECTED_B={cid for cid,v in CHAINS.items()if v['row'].get('sample')=='B'}
ALL_A={cid for cid in INITIAL if re.fullmatch(r'[DMX]\d{2}',cid)}
ALL_B={cid for cid in INITIAL if re.fullmatch(r'[DMX]B\d{2}',cid)}

for stream in sorted((P/'streams').iterdir()):
    if not stream.is_dir():continue
    for name in ['source-ledger.jsonl','screening-sources.jsonl','reading-updates.jsonl','providers.jsonl']:
        f=stream/name
        if not f.exists():continue
        for line,r in read_jsonl(f):
            phase='T0'if name=='source-ledger.jsonl'else'provider_read'if name=='providers.jsonl'else'postseal_followup'
            EVENTS.append(dict(row=r,origin=locator(f,line,r.get('source_id')),phase=phase,stream=stream.name))
for line,r in read_jsonl(P/'cross/sources.jsonl'):
    EVENTS.append(dict(row=r,origin=locator(P/'cross/sources.jsonl',line,r['source_id']),phase='cross_domain_read',stream='cross'))
f=P/'design-sources.jsonl'
if f.exists():
    for line,r in read_jsonl(f):
        EVENTS.append(dict(row=r,origin=locator(f,line,r['source_id']),phase='provider_read',stream='design'))

# Frame-only excluded and accidental post-cap root readings are retained, never
# used to fill A/B or the36 minimum. No search-result-only row becomes a source.
existing_urls={clean_url(e['row']['url'])for e in EVENTS}
for fr in FRAME:
    r=fr['row'];stream=fr['stream'];url=clean_url(r['root_url'])
    if stream=='matplotlib':
        directly_read=truth(r.get('root_body_displayed'));excluded=r.get('disposition')=='excluded'
        overread=truth(r.get('post_cap_batch_overread'))
    elif stream=='duckdb':
        directly_read=truth(r.get('root_directly_read'));excluded=r.get('root_eligible')=='False'
        overread=directly_read and not truth(r.get('screened_for_selection'))
    else:
        excluded=r.get('eligibility')=='excluded';overread=False
        directly_read=excluded or r.get('eligibility')in['included_A','eligible_B_root']
    if not directly_read or not (excluded or overread):continue
    sid=f"FRAME-{stream}-{r['issue_number']}"
    extra=dict(source_id=sid,type='excluded_root_reading'if excluded else'post_cap_root_reading',publisher=r.get('ledger')or r.get('project')or stream,
       url=url,version='current root at T0 screening; created '+str(r.get('created_at')or r.get('created_utc')),
       checked_utc=r.get('screened_utc')or None,
       sections='current root body inspected for eligibility; exact paragraph anchors not separately recorded',
       observed=r.get('reason'),limitations='선정 제외 또는 상한후우연열람의 root 판독만 기록. 후속을 읽었다고 확장하지 않음. 같은 사건의 중복은 독립 사례로 세지 않음.',
       linked_Q_cases=['Q1','Q4'],duplicate_group=url,count_minimum=False,direct_read=True,
       category='excluded_root'if excluded else'post_cap_overread_root',
       checked_utc_limit=None if r.get('screened_utc')else'미확인: frame에는 독립적인 root 열람 UTC가 없음. 원문별 다른 읽기영수증이 있으면 그 UTC만 사용.',
       last_confirmed_location=fr['origin'],next_material='해당 root의 실제 열람 영수증; 이 누락은 필수36원문에 산입하지 않음')
    EVENTS.append(dict(row=extra,origin=fr['origin'],phase='T0_frame_only',stream=stream))

# Supplement selected threads with their post-seal chain record. No whole raw
# transcript is embedded; event summaries, URLs, dates and hashes are already
# committed in the named chain. Independent sources remain thread-level.
def local_comment_locations(obj,root):
    found=[]
    def visit(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in['url','question_url','first_response_url','last_confirmed_location','last_confirmed_url']and isinstance(v,str)and v.startswith(root+'#issuecomment-'):found.append(v)
                elif isinstance(v,(dict,list)):visit(v)
        elif isinstance(x,list):
            for y in x:
                if isinstance(y,str)and y.startswith(root+'#issuecomment-'):found.append(y)
                else:visit(y)
    visit(obj);return sorted(set(found),key=lambda u:int(u.rsplit('-',1)[-1]))
for cid,ch in CHAINS.items():
    r=ch['row'];url=clean_url(r['root_url']);summ=[]
    for key in ['messages','answers','recommendations','recommendation_changes','executions','other_events','late_history']:
        for x in as_list(r.get(key)):
            if isinstance(x,dict)and x.get('summary'):summ.append(x['summary'])
    qunknown=r.get('unknowns')or r.get('unknown')or []
    times=[r.get('checked_utc'),r.get('direct_read_utc'),r.get('windows',{}).get('checked_utc')]
    event=dict(source_id=f'CHAIN-READ-{cid}',type='same_thread_followup_chain',publisher=ch['stream']+' public participants',url=url,
      version='root30/root90 post-seal current public snapshot; per-comment edits retained in chain',checked_utc=next((z for z in times if z),None),
      sections=local_comment_locations(r,url),observed=summ or ['후속창과 실질 응답 부재를 chains에서 확인.'],
      limitations=qunknown or ['현재 공개 자료의 한계는 연결한 chains의 observation/windows/unknown 필드 참조.'],
      linked_Q_cases=['Q3','Q5','Q6','Q7','Q8',cid],duplicate_group=url,count_minimum=False,direct_read=True,
      current_reading_status='postseal_root30_and_root90_checked',chain_file=ch['origin'],
      late_window_separate=bool(r.get('late_history'))or bool(r.get('late_first_response')))
    EVENTS.append(dict(row=event,origin=ch['origin'],phase='postseal_chain_update',stream=ch['stream']))

# Root's targeted rereads are separate reading acts, never extra originals.
f=P/'evidence/root-provider-rechecks.jsonl'
if f.exists():
    for line,r in read_jsonl(f):
        rr=dict(r,publisher='original publisher; root targeted reread',type='targeted_provider_reread',version='same version as matched provider record',
                limitations='통합자의 선택적 재독이며 블라인드 독립 이중코딩이나 새 원문이 아님.',linked_Q_cases=['Q6','Q7','Q8'],count_minimum=False,direct_read=True)
        EVENTS.append(dict(row=rr,origin=locator(f,line,r.get('source_id')),phase='root_targeted_reread',stream='root'))
f=P/'evidence/source-root-rereads.jsonl'
if f.exists():
    for line,r in read_jsonl(f):
        EVENTS.append(dict(row=r,origin=locator(f,line,r['source_id']),phase='postseal_root_reread',stream='source_compiler'))

# These14 records satisfy the literal manual/test/decision requirement without
# relying on plain implementation code. Later fixes are explicitly prospective
# supplier work; they do not validate the initial recommendation retroactively.
QUALIFIED_PROVIDER={
 'M-P01':('contemporaneous_release_notes','requester NumPy1.24; release rule read'),
 'M-P03':('exact_version_manual','requester Matplotlib3.6.2; font-manager manual'),
 'M-P04':('exact_version_official_example','Matplotlib3.6.2 official embedding example'),
 'M-P08':('exact_minor_version_manual','requester3.9.1; docs footer has two later commits/dirty suffix retained'),
 'M-P09':('exact_version_manual','requester3.8.4; legend manual; setter success not inferred'),
 'DP01':('contemporaneous_manual_snapshot','immediately preceding July2024 documentation change'),
 'DP02':('same_event_contemporaneous_fix_test','July2024 supplier fix/test; not requester execution'),
 'DP03':('same_event_root90_regression_test','May2023 supplier test for April2023 report; later version, not original0.7.1 fit'),
 'DP06':('same_event_root90_fix_test','February2023 restricted fix/test for January2023 issue; unsupported feature remains unsupported'),
 'DP07':('same_event_root90_fix_test','February2023 binding fix/test for January2023 issue; remote input not fully covered'),
 'DP08':('same_event_contemporaneous_decision','January2023 linked PR body/metadata; detailed code not claimed'),
 'DP09':('same_event_contemporaneous_decision','July2024 linked PR body/metadata; detailed code not claimed'),
 'XD01':('exact_version_manual','reported xarray2022.03.0 I/O manual'),
 'XD11':('prior_applicable_standards_decision','array API2022 discussion and March2023 closure available before April2023 case')
}
MINIMUM_PROVIDER_WITNESS=['M-P01','M-P03','M-P04','DP01','DP02','DP06','XD01','XD11']
MINIMUM_CROSS_WITNESS=['C-L1','C-L2','C-S2','C-S4']
PROVIDER_WARNINGS={
 'M-P11':'Cartopy0.21.0 manual versus requester0.21.1 patch; retained as support, not strict minimum.',
 'XD05':'v2023.04.0 backend manual is later than January2023 X04; contemporaneous rioxarray registration separately supports mechanism. Excluded from strict minimum.',
 'M-P14':'upstream root only; comments/repair revision unavailable. Not a qualified manual/test/decision.',
 'DP10':'same window-functions documentation event as DP01; subsequent change may be wrong; no extra minimum credit.',
 'M-EVENT-24970':'same-event90 PR retained separately; author opted out of minimum credit.',
 'M-EVENT-24869':'same-event90 PR retained separately; author opted out of minimum credit.',
 'XD06':'same api.py document as XD03, exact earlier version corroboration; one resource across editions.',
 'DP12':'same plan_window.cpp document as DP04, alternative version; one resource across editions.'
}
GROUPS=defaultdict(list)
for e in EVENTS:
    url=e['row'].get('url')
    if not url:raise ValueError('source event without URL: '+str(e['origin']))
    GROUPS[canonical_key(url)].append(e)

def counting_group(key,aliases):
    if {'M-P03','M-P03-SOURCE'}&set(aliases):return 'provider-family:matplotlib-font-manager'
    if {'M-P09','M-P09-SOURCE'}&set(aliases):return 'provider-family:matplotlib-legend'
    if {'DP01','DP10'}&set(aliases):return 'provider-family:duckdb-window-functions-documentation'
    return key

RECORDS=[]
for key,events in sorted(GROUPS.items()):
    # Preserve the source ledger's stable identity and original URL where possible.
    events.sort(key=lambda e:(0 if e['phase']in['T0','provider_read','cross_domain_read']else 1,e['origin']['file'],e['origin']['line']))
    aliases=unique([e['row'].get('source_id')for e in events if e['row'].get('source_id')])
    primary=events[0]['row'];url=clean_url(primary['url']);cid=CASE_URL.get(url)
    is_provider=any(e['phase']=='provider_read'for e in events)
    is_cross=any(e['phase']=='cross_domain_read'for e in events)
    frame_categories={e['row'].get('category')for e in events if e['row'].get('category')}
    if cid in ALL_A:category='A_thread'
    elif cid in SELECTED_B:category='B_selected_thread'
    elif cid in ALL_B:category='B_nonselected_screening_thread'
    elif is_provider:category='official_provider'
    elif is_cross:category='cross_library_reference'if any(a.startswith('C-L')for a in aliases)else'cross_public_statistics'
    elif 'excluded_root'in frame_categories or any('excluded'in e['row'].get('type','')for e in events):category='excluded_root'
    elif 'post_cap_overread_root'in frame_categories:category='post_cap_overread_root'
    else:category='additional_original'
    qualified_ids=[a for a in aliases if a in QUALIFIED_PROVIDER]
    minimum=category=='A_thread'or is_cross or bool(qualified_ids)
    if minimum:
        reason='A selected thread, once only'if category=='A_thread'else'cross-domain observation/procedure original, once only'if is_cross else'qualified official manual/test/decision; once per counting group'
    else:
        reason='B and excluded/post-cap roots kept outside required36'if category in['B_selected_thread','B_nonselected_screening_thread','excluded_root','post_cap_overread_root']else'additional technical support/implementation/duplicate or version-limited material; not used for strict official minimum'
    versions=[];reading=[];known_times=[];all_urls=[];links=[];sections=[];observed=[];limitations=[]
    for e in events:
        r=e['row'];clock=r.get('checked_utc');phase=e['phase'];all_urls.append(r['url'])
        if r.get('direct_read_url'):all_urls.append(r['direct_read_url'])
        if iso_key(clock):known_times.append(clock)
        links+=flatten_links(r.get('linked_Q_cases'))
        sect=r.get('sections');sections+=as_list(sect)
        observed.append(dict(phase=phase,summary=r.get('observed'),origin=e['origin']))
        # Historical unread-at-T0 notes belong to their dated event, not current status.
        if phase not in['T0']:
            limitations+=as_list(r.get('limitations'))
        versions.append(dict(source_id=r.get('source_id'),url=r['url'],version=r.get('version','미확인'),
                             checked_utc=clock,sha256=r.get('sha256')or r.get('artifact_sha256')or r.get('body_sha256'),
                             source_minimum_flag=r.get('count_minimum'),phase=phase))
        reading.append(dict(source_id=r.get('source_id'),phase=phase,reader=r.get('reader')or r.get('adjudicator')or r.get('direct_read_method')or e['stream']+' stream reader',
                            checked_utc=clock,sections=sect,observed=r.get('observed'),limitations=r.get('limitations'),
                            direct_read_basis=r.get('direct_read_method')or r.get('read_mode')or ('explicit direct_read=true'if r.get('direct_read')is True else'named stream reading ledger; aggregate compiler did not re-open original'),
                            origin=e['origin'],retrieval_refs=r.get('retrieval_refs')or as_list(r.get('web_retrieval_reference'))))
    followup=any(e['phase']in['postseal_followup','postseal_chain_update']for e in events)
    if cid:
        limitations.append('원본문 creation-time 원판과 현재 수정본은 다름. 후속 열람은 T0 원판 미복원을 해소하지 않음. 공개 handle은 독립 사람 수가 아님.')
        status='root_first_response_and_postseal_windows_read'if followup else'root_and_first_response_read_followup_not_linked'
    elif category in['excluded_root','post_cap_overread_root']:
        status='excluded_root_and_followup_read'if followup else'root_eligibility_only_read'
    else:status='specified_sections_directly_read'
    if not limitations:limitations+=as_list(primary.get('limitations'))
    if not known_times:
        limitations.append('미확인: 이 frame-only 원문의 독립 열람 UTC가 공개 원장에 없다. 마지막 확인 위치는 provenance의 frame 행이며 다음 자료는 실제 원문 열람 영수증. 필수 최소수에서는 제외.')
    notes=[PROVIDER_WARNINGS[a]for a in aliases if a in PROVIDER_WARNINGS]
    if is_provider and not qualified_ids and not notes:notes.append('공식 구현 또는 보강 근거로 직접 읽었으나 필수 매뉴얼/시험/결정 자료수의 보수적 집계에서는 제외.')
    if any(a=='DP03'for a in aliases):notes.append('당시 보고판이 아닌 root90 후속 supplier test. 최초 기술 적합성을 소급 증명하지 않음.')
    cross_domain='library_reference'if category=='cross_library_reference'else'public_statistics_cognitive_interview'if is_cross else None
    cross_evidence=None
    if is_cross:
        cross_evidence=dict(domain=cross_domain,
           role='procedure'if any(a in['C-L2','C-S2']for a in aliases)else'observation_or_empirical_study',
           actual_dialogue_excerpts=any(a in['C-L1','C-S4']for a in aliases),
           illustrative_dialogue_not_counted_as_observation=any(a in['C-S3','C-S6']for a in aliases),
           source_limitations_preserved=True)
    explicit_comments=[]
    for e in events:explicit_comments+=local_comment_locations(e['row'],url)
    if cid in INITIAL:
        first=INITIAL[cid]['row'].get('first_response_url')
        if first and first.startswith(url+'#issuecomment-'):explicit_comments.append(first)
    if cid in SCREEN:explicit_comments+=local_comment_locations(SCREEN[cid]['row'],url)
    rec=dict(source_id=next((a for a in aliases if not a.startswith(('CHAIN-READ','FRAME-'))),aliases[0]),canonical_key=key,
      type=unique([e['row'].get('type','미확인')for e in events if e['phase']not in['postseal_chain_update','root_targeted_reread']]),
      publisher=unique([e['row'].get('publisher','미확인')for e in events if e['phase']not in['postseal_chain_update','root_targeted_reread']]),
      url=url,urls=unique(all_urls),version=unique([x['version']for x in versions]),editions=unique(versions),
      checked_utc=max(known_times,key=iso_key)if known_times else None,checked_utc_status='recorded'if known_times else'미확인: per-root reading UTC not recorded',
      sections=unique(sections),observed=observed,limitations=unique(limitations),linked_Q_cases=unique(links+([cid]if cid else[])),
      duplicate_group=counting_group(key,aliases),original_duplicate_groups=unique([e['row'].get('duplicate_group')for e in events if e['row'].get('duplicate_group')]),
      count_minimum=minimum,minimum_reason=reason,minimum_category='A_thread'if category=='A_thread'else'official_manual_test_decision'if qualified_ids else'cross_domain'if is_cross else None,
      category=category,case_id=cid,source_aliases=aliases,provenance=unique([e['origin']for e in events]),reading_status=status,
      reading_events=reading,compiler_reopened_external_original=any(e['phase']=='postseal_root_reread'for e in events),direct_read=True,
      direct_read_evidence_class='frame_only_body_displayed'if all(e['phase']=='T0_frame_only'for e in events)else'named_reader_source_or_chain_ledger',
      official_contemporaneous_qualified=bool(qualified_ids),official_qualification=[dict(source_id=a,basis=QUALIFIED_PROVIDER[a][0],scope=QUALIFIED_PROVIDER[a][1])for a in qualified_ids],
      qualification_notes=notes,cross_domain_evidence=cross_evidence,
      explicit_read_comment_urls=sorted(set(explicit_comments),key=lambda u:int(u.rsplit('-',1)[-1]))if explicit_comments else[],
      comments_are_not_independent_originals=True)
    RECORDS.append(rec)

# At most one minimum credit per declared source family, even when a manual and
# implementation are different resources. No duplicate same-thread credit.
credited=set()
for r in sorted(RECORDS,key=lambda r:(not r['count_minimum'],r['source_id'])):
    if r['count_minimum']:
        if r['duplicate_group']in credited:
            r['count_minimum']=False;r['minimum_reason']='same counting group already credited; retained as separate original/edition support'
        else:credited.add(r['duplicate_group'])

RECORDS.sort(key=lambda r:(r['category'],r.get('case_id')or'',r['source_id']))
SOURCE_BYTES=''.join(json.dumps(r,ensure_ascii=False)+'\n'for r in RECORDS).encode()
(P/'sources.jsonl').write_bytes(SOURCE_BYTES)
BY_CATEGORY=Counter(r['category']for r in RECORDS)
qualified=[r for r in RECORDS if r['official_contemporaneous_qualified']and r['count_minimum']]
cross=[r for r in RECORDS if r['cross_domain_evidence']]
A_records=[r for r in RECORDS if r['category']=='A_thread']
def find_alias(alias):return next(r['source_id']for r in RECORDS if alias in r['source_aliases'])
witness=([r['source_id']for r in sorted(A_records,key=lambda r:r['case_id'])]+
         [find_alias(a)for a in MINIMUM_PROVIDER_WITNESS]+[find_alias(a)for a in MINIMUM_CROSS_WITNESS])
source_by_id={r['source_id']:r for r in RECORDS}
cross_by_domain={domain:[r['source_id']for r in cross if r['cross_domain_evidence']['domain']==domain]for domain in['library_reference','public_statistics_cognitive_interview']}
minimum_flags=sum(r['count_minimum']for r in RECORDS)
expected_B={'XB03','DB04','XB06','DB07','XB08','MB09','XB13','XB14'}
conditions=[
 dict(condition='A24 directly read threads, 8 per project',met=len(A_records)==24 and Counter(INITIAL[r['case_id']]['stream']for r in A_records)==Counter({'matplotlib':8,'xarray':8,'duckdb':8}),evidence=[r['source_id']for r in A_records]),
 dict(condition='selected B8 distinct from A; remaining B72 separate',met=SELECTED_B==expected_B and BY_CATEGORY['B_selected_thread']==8 and BY_CATEGORY['B_nonselected_screening_thread']==72,evidence=dict(selected=sorted(SELECTED_B),nonselected_count=BY_CATEGORY['B_nonselected_screening_thread'])),
 dict(condition='at least8 contemporary official manuals/tests/decisions after duplicate control',met=len(qualified)>=8,evidence=[r['source_id']for r in qualified]),
 dict(condition='at least2 directly read originals from each of2 external domains, including observation and procedure',met=all(len(v)>=2 for v in cross_by_domain.values())and all(any(r['cross_domain_evidence']['role']=='procedure'for r in cross if r['source_id']in ids)and any(r['cross_domain_evidence']['role']=='observation_or_empirical_study'for r in cross if r['source_id']in ids)for ids in cross_by_domain.values()),evidence=cross_by_domain),
 dict(condition='explicit36-original witness uses24 A +8 official +4 cross, all unique counting groups',met=len(witness)==36 and len(set(witness))==36 and len({source_by_id[x]['duplicate_group']for x in witness})==36 and all(source_by_id[x]['count_minimum']for x in witness),evidence=witness),
 dict(condition='all A and selected B source records link post-seal followup reading',met=all(r['reading_status']=='root_first_response_and_postseal_windows_read'for r in RECORDS if r['category']in['A_thread','B_selected_thread']),evidence='chains.jsonl-derived reading event in each selected thread record'),
 dict(condition='all B80 source records link followup reading separately from minimum',met=all(r['reading_status']=='root_first_response_and_postseal_windows_read'for r in RECORDS if r['category']in['B_selected_thread','B_nonselected_screening_thread']),evidence='stream reading-updates/screening-sources/chains'),
 dict(condition='required-minimum records have UTC, direct reading sections, findings and limitations',met=all(r['checked_utc']and r['sections']and r['observed']and r['limitations']for r in RECORDS if r['count_minimum']),evidence='sources.jsonl count_minimum=true records')
]
conditions.append(dict(condition='all canonical originals have a recorded latest check UTC; historical missing times are not fabricated',met=all(r['checked_utc']for r in RECORDS),evidence='evidence/source-root-rereads.jsonl supplies20 current-root rereads; T0 null timestamps remain in dated reading_events'))
missing_time=[dict(source_id=r['source_id'],url=r['url'],category=r['category'],why=r['checked_utc_status'],last_location=r['provenance'],next_source='per-root original read receipt; never used for required minimum')for r in RECORDS if not r['checked_utc']]
stats=dict(schema_version='AF-RES-030-source-counts-v1',t0_seal_sha=SEAL,builder_sha256=digest(Path(__file__).read_bytes()),
 counting_rules=[
  'One canonical original per thread or file/document path. Comment fragments/API endpoints collapse to thread; Git tag/SHA editions of one file collapse to one original.',
  'A24 minimum; B8 and nonselectedB72 never fill the36 required originals. Excluded and post-cap roots are separate.',
  'Minimum provider subset deliberately uses explicit manuals/release notes/official examples/tests/decisions; plain implementation source stays additional.',
  'Same-event later supplier tests may qualify as contemporary evidence with a version-mismatch note; they never establish initial recommendation correctness or user execution.',
  'Manual and implementation source families receive at most one minimum credit even if represented by separate original resources.',
  'External empirical papers are distinguished from protocols and hypothetical training dialogue; PDF/HTML/DOCX mirrors are not extra sources.',
  'Named researcher direct-reading ledgers are aggregated. Compiler inspection of the ledger is not claimed as a new external reading.',
  'For20 originally undated frame-only roots, the compiler actually reopened and read the complete current root; the new UTC repairs latest-check metadata, not historical T0 timing, selection or minimum count.',
  'Search summaries, failed opens and metadata-only unviewed candidate rows are not source originals. Frame-confirmed root-only reads remain separate, with UTC gaps explicit.'
 ],input_sha256=INPUTS,sources_jsonl_sha256=digest(SOURCE_BYTES),
 counts=dict(canonical_original_records=len(RECORDS),required_minimum_qualified_unique=minimum_flags,
    originals_with_named_reading_ledger=sum(r['direct_read_evidence_class']=='named_reader_source_or_chain_ledger'for r in RECORDS),
    frame_only_displayed_roots=sum(r['direct_read_evidence_class']=='frame_only_body_displayed'for r in RECORDS),
    originals_with_recorded_check_utc=sum(bool(r['checked_utc'])for r in RECORDS),
    A_threads=BY_CATEGORY['A_thread'],B_selected_threads=BY_CATEGORY['B_selected_thread'],B_nonselected_screening_threads=BY_CATEGORY['B_nonselected_screening_thread'],
    all_B_eligible_screened_threads=BY_CATEGORY['B_selected_thread']+BY_CATEGORY['B_nonselected_screening_thread'],
    excluded_roots=BY_CATEGORY['excluded_root'],post_cap_overread_roots=BY_CATEGORY['post_cap_overread_root'],
    official_provider_originals_read=BY_CATEGORY['official_provider'],official_contemporaneous_manual_test_decision_qualified=len(qualified),
    official_additional_or_version_limited=BY_CATEGORY['official_provider']-len(qualified),
    cross_domain_originals=len(cross),cross_library_reference=len(cross_by_domain['library_reference']),cross_public_statistics=len(cross_by_domain['public_statistics_cognitive_interview']),
    selected_independent_case_roots=24+len(SELECTED_B),all_A_plus_eligible_B_roots=24+len(ALL_B),
    source_reading_events=len(EVENTS),explicit_logged_read_comment_permalinks=len({u for r in RECORDS for u in r['explicit_read_comment_urls']}),
    frame_candidate_metadata_rows=len(FRAME),missing_per_root_checked_utc_nonminimum=len(missing_time),
    historical_T0_utc_gaps_preserved_current_root_reread_utc_added=sum(r['compiler_reopened_external_original']for r in RECORDS)),
 categories=dict(BY_CATEGORY),selected_B_ids=sorted(SELECTED_B),A_case_ids=sorted(ALL_A),
 qualified_provider_sources=[dict(source_id=r['source_id'],url=r['url'],qualification=r['official_qualification'])for r in qualified],
 provider_exclusions=[dict(source_id=r['source_id'],url=r['url'],reason=r['qualification_notes']or[r['minimum_reason']])for r in RECORDS if r['category']=='official_provider'and not r['official_contemporaneous_qualified']],
 cross_domain_sources=cross_by_domain,
 minimum36_witness=dict(A24=[r['source_id']for r in sorted(A_records,key=lambda r:r['case_id'])],official8=[find_alias(a)for a in MINIMUM_PROVIDER_WITNESS],cross4=[find_alias(a)for a in MINIMUM_CROSS_WITNESS],total=36),
 linked_source_counts_by_case=[dict(case_id=cid,linked_source_originals=len([r for r in RECORDS if cid in r['linked_Q_cases']]),source_ids=[r['source_id']for r in RECORDS if cid in r['linked_Q_cases']])for cid in sorted(ALL_A|SELECTED_B)],
 same_event_source_counts=[dict(case_id=cid,original_thread_count=1,same_event_supplier_records=[r['source_id']for r in RECORDS if cid in r['linked_Q_cases']and set(r['source_aliases'])&{'DP02','DP03','DP06','DP07','DP08','DP09','DP10','M-EVENT-24970','M-EVENT-24869'}],note='General technical manuals and cross-domain analogies are linked evidence, not additional independent cases or same-event conversations.')for cid in sorted(ALL_A|SELECTED_B)],
 conditions=conditions,minimum_conditions_all_met=all(c['met']for c in conditions),
 known_gaps=missing_time,
 units_note='Source originals, unique case roots, reading acts, explicit read-comment locators and question/answer/execution rows are different units. This file does not call public handles independent people or use comments to inflate originals.',
 reproducibility=dict(command='python docs/workstreams/research/AF-RES-030/build_sources.py',network_required=False,ignored_raw_cache_required=False,writes=['sources.jsonl','evidence/source-counts.json']))
(P/'evidence/source-counts.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(counts=stats['counts'],conditions_all_met=stats['minimum_conditions_all_met'],failed=[c['condition']for c in conditions if not c['met']]),ensure_ascii=False,indent=2))
if not stats['minimum_conditions_all_met']:raise SystemExit(1)
