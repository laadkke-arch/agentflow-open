"""Write the bounded search, acquisition and citation trail for strand B."""
from pathlib import Path
import json
from datetime import datetime, timezone

P=Path(__file__).resolve().parent
NOW=datetime.now(timezone.utc).isoformat()
sources=[json.loads(s) for s in (P/'sources.jsonl').read_text().splitlines()]
searches=[json.loads(s) for name in ('searches.jsonl','searches-single.jsonl') for s in (P/name).read_text().splitlines()]
attempts=list(searches)
attempts.extend([
 dict(attempt_id='Swb-EXPLORATORY-01',attempt_type='search_metadata_only',executed_date_utc='2026-11-22',index='system2 web search',queries=['"Sohan" "usage examples" "study" data github','"Acar" "2016" "information sources" "study materials"','"Jungloid Mining" pdf mandelin'],sort='service default relevance',actual_returned=None,screened_returned_positions=None,result='탐색 호출은 실행했으나 해당 호출의 순위별 반환 원장을 보존하지 못함. 후속 직접 열람은 source/open 행에 별도 기록.',limitation='반환 수·질의별 상한을 재현할 수 없으므로 완전 검색 주장에 쓰지 않음'),
 dict(attempt_id='Swb-EXPLORATORY-02',attempt_type='search_metadata_only',executed_date_utc='2026-11-22',index='system2 web search',queries=['"Prompter" "replication package" github','"NCQ" "code reuse" github study','"Seahawk" "replication" study','"eXoaDocs" user study data'],sort='service default relevance',actual_returned=None,screened_returned_positions=None,result='원산출물 탐색 호출은 실행했으나 해당 호출의 순위별 반환 원장을 보존하지 못함. NCQ 고정 저장소와 파일의 실제 열람 기록은 source/attempt에 있음.',limitation='반환 수·질의별 상한을 재현할 수 없으므로 완전 검색 주장에 쓰지 않음'),
])
for s in sources:
    attempts.append(dict(attempt_id='Swb-OPEN-'+s['source_id'],attempt_type='open_read',source_id=s['source_id'],
        source_url=s['original_url'],checked_utc=s['checked_utc'],result='required_sections_verified' if s['required_content_verified'] else 'partial_discovery_read_only',
        read_locator=s['read_locator'],observation_grade=s['observation_grade'],next_action=None if s['required_content_verified'] else s['limitations']))
failures=[
 ('Swb-FAIL-01','https://dl.acm.org/action/doSearch?AllField=API+documentation+examples+task+completion+time','native_ACM_search','not accessible via web tool','저자본/일반웹검색으로보완;native정렬순위와처음30건은미확인'),
 ('Swb-FAIL-02','https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=API%20documentation%20examples%20task%20time','native_IEEE_search','not accessible via web tool','IEEE/ACM venue명포함일반검색과저자본;native첫30건은미확인'),
 ('Swb-FAIL-03','https://www.cs.berkeley.edu/~mandelin/ProspectorPLDI05.pdf','paper_fetch','redirect to inaccessible Berkeley path','https://citeseerx.ist.psu.edu/document?doi=bee8a1da7c2eac2f517f58afe2da0f8ae3f7f5c7&repid=rep1&type=pdf'),
 ('Swb-FAIL-04','https://homes.cs.washington.edu/~bodik/ucb/research/ProspectorPLDI05.pdf','author_copy_fallback','not accessible via web tool','CiteSeer후보원문;미실행'),
 ('Swb-FAIL-05','http://prompter.inf.usi.ch/','original_replication_package','inaccessible via web tool','https://prompter.inf.usi.ch/'),
 ('Swb-FAIL-06','https://prompter.inf.usi.ch/','original_replication_package','inaccessible via web tool','저자Ponzanelli공개publication목록;논문내§4자료만검증,별도패키지수미산입'),
 ('Swb-FAIL-07','https://www.sciencedirect.com/science/article/pii/S0164121224000177','forward_candidate_fulltext','HTTP403','저자https://www.maymahmoud.org/publications/열었으나2024항목에PDF링크없음'),
 ('Swb-FAIL-08','https://pub.h-brs.de/frontdoor/deliver/index/docId/5631/file/Gorski2021_IJustLookedForTheSolution.pdf','repeat_fulltext_find','initialPDFopened;subsequentfindreturnedbotpage','기관저장소재접근또는저자공개postprint찾아Methods/표확인'),
 ('Swb-FAIL-09','tmp/codesnippets1.csv','local_decode','UnicodeDecodeError byte0x85 at39372 in strictUTF8','cp1252로재실행성공;142레코드,1emptyplaceholder'),
 ('Swb-FAIL-10','build_ledgers.py','arithmetic_builder_execution','추가 모델구간 행의 닫는 괄호 하나가 많아 SyntaxError, exit1','괄호 수정 후 python -B build_ledgers.py 재실행 성공; 효과16행'),
]
for aid,url,kind,result,next_action in failures:
    attempts.append(dict(attempt_id=aid,attempt_type=kind,url=url,executed_date_utc='2026-11-22',result=result,next_action=next_action))
attempts.extend([
 dict(attempt_id='Swb-EXEC-01',attempt_type='download_extract',executed_date_utc='2026-11-22',command='Python urllib.request.urlopen then pdftotext -layout (7 paper files)',inputs='URLs and SHA256 in sources.jsonl/download-receipts.json',exit_code=0,result='전문7개와localtext7개를tmp로격리;저작물전문을git에추가하지않음'),
 dict(attempt_id='Swb-EXEC-02',attempt_type='dataset_read',executed_date_utc='2026-11-22',command='csv.DictReader(io.StringIO(bytes.decode("cp1252")))',inputs='NCQ @ce14f193... data/user-study/codesnippets1.csv,codesnippets2.csv',exit_code=0,result={'study1_records':142,'study1_nonempty_snippets':141,'study1_used_1':41,'study1_empty_rows':1,'study2_records':156,'study2_used_1':38},limitation='코드원자료read/집계,원분석lint재실행아님'),
 dict(attempt_id='Swb-EXEC-03',attempt_type='arithmetic_ledger_build',executed_utc=NOW,command='python docs/workstreams/research/AF-RES-034/streams/software-b/build_ledgers.py',exit_code=0,inputs='hand-extracted original paper values in build_ledgers.py',result='16effectrows and sourcejoin assertion; see strand-counts.json',limitation='동일작성자자체검산;독립판독/새humanexperiment아님'),
 dict(attempt_id='Swb-EXEC-04',attempt_type='original_analysis_not_run',executed_utc=NOW,command='node data/scripts/user-study-snippets',inputs='NCQrepository@ce14f193f7014c120f04619826cb251818d99b0e; defaultcodesnippets1,secondfilecommented',exit_code=None,result='원저자코드정적판독만,패키지설치·코드실행안함',next_action='분리환경에서Node14.17.0와lockfile고정후각파일1회선택;출력오류수원Figure28조인;humancompletiontime재계산에는별timestamp자료필요'),
])

# Each selected primary family/source has an explicit final disposition. Search metadata
# includes all bounded returned positions; discovery-only returns are not falsely called
# completed full-text exclusions.
screening=[]
for s in sources:
    if s['count_category']=='software_primary': disp='include_primary_human'
    elif s['count_category']=='artifact': disp='include_independent_artifact'
    elif s['count_category']=='excluded_nonhuman': disp='exclude_no_human_task_execution'
    else: disp='discovery_only_not_counted'
    screening.append(dict(screening_id='Swb-S-'+s['source_id'],source_id=s['source_id'],study_family=s['study_family'],
        url=s['original_url'],title=s['title'],stage='required_fulltext_sections' if s['required_content_verified'] else 'partial_or_abstract',
        disposition=disp,count_minimum=s['count_minimum'],reason=s['limitations'],read_locator=s['read_locator']))
screening.append(dict(screening_id='Swb-S-PROSPECTOR',source_id='Swb-X08',study_family='SWB-PROSPECTOR',
        title='Jungloid Mining: Helping to Navigate the API Jungle',url=failures[2][1],stage='fulltext_access_attempt',
        disposition='access_failed_not_counted',count_minimum=False,reason='원논문링크·저자미러실패;검색요약의실험성능을효과행에넣지않음',next_source=failures[2][4]))

known={s['original_url']:s for s in sources}
discovery={}
for q in searches:
    for r in q['screened_returned_positions']:
        u=r['url']
        d=discovery.setdefault(u,dict(url=u,title=r['title'],discovered_via=[],query_level_screening=[]))
        d['discovered_via'].append({'attempt_id':q['attempt_id'],'returned_position':r['returned_position']})
        if 'screening_decision' in r:
            d['query_level_screening'].append({'attempt_id':q['attempt_id'],'returned_position':r['returned_position'],'decision':r['screening_decision'],'stage':r['screening_stage'],'reason':r['reason']})
for i,(u,d) in enumerate(discovery.items(),1):
    if u in known: continue
    # These are an auditable discovery tail, not an invented exhaustive eligibility review.
    screening.append(dict(screening_id=f'Swb-DISC-{i:03}',source_id=None,study_family=None,
        stage='title_and_returned_abstract' if d['query_level_screening'] else 'bounded_search_discovery',disposition='not_selected_for_fulltext_in_this_strand',
        count_minimum=False,reason='검색반환기록보존. 이미열람한원문/일반자료/후속후보가섞여있으므로이행은독립된적격·탈락수로합산하지않음.',**d))

citations=[
 dict(citation_id='Swb-CIT-01',study_family='SWB-EXO',direction='backward',from_source='Swb-P01',locator='§7;referencesp26',target_title='Using Structural Context to Recommend Source Code Examples',target_url='https://cs.uwaterloo.ca/~rtholmes/papers/icse_2005_holmes.pdf',target_source_id='Swb-P04',status='primary_read_included;dedupfamily'),
 dict(citation_id='Swb-CIT-02',study_family='SWB-EXO',direction='forward',from_source='Swb-X04',locator='APISonar reference16lines150–154',target_source_id='Swb-P01',target_url='https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.2906',status='citation_confirmed;candidateabstractonly;notadditionalhumanstudy'),
 dict(citation_id='Swb-CIT-03',study_family='SWB-REST',direction='backward',from_source='Swb-P02',locator='§VIreferences10',target_title='Adding Examples into Java Documents,2009',target_source_id='Swb-P01',target_url='https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf',status='sameEXOfamily;expanded2013primaryread;2009notseparatecohort'),
 dict(citation_id='Swb-CIT-04',study_family='SWB-REST',direction='forward',from_source='Swb-X05',locator='Cerit2019printedp19andreference43p113',target_source_id='Swb-P02',target_url='https://www.cs.cit.tum.de/fileadmin/w00cfj/sebis/thesis/190915_Cerit_Thesis.pdf',status='citation_confirmed;abstractandrelatedworkread;fullquantitativeextractionpendingnotcounted'),
 dict(citation_id='Swb-CIT-05',study_family='SWB-ACAR',direction='backward',from_source='Swb-P03',locator='§IV;reference21',target_title='Should I Protect You?2014',target_source_id='Swb-X06',target_url='https://winlab.rutgers.edu/~shubhamj/papers/USEC14apistudy.pdf',status='primaryabstractopened;changesAPIfunctionality;notcountedaslinkintervention'),
 dict(citation_id='Swb-CIT-06',study_family='SWB-ACAR',direction='forward',from_source='Swb-X02',locator='indexedreference17;initialPDFpp1–2',target_source_id='Swb-P03',target_url='https://pub.h-brs.de/frontdoor/deliver/index/docId/5631/file/Gorski2021_IJustLookedForTheSolution.pdf',status='candidatecitationfoundinprimaryindexedreferences;repeatPDFblocked;fullmethodspending'),
 dict(citation_id='Swb-CIT-07',study_family='SWB-STRATH',direction='backward',from_source='Swb-P04',locator='§8references2,5,12',target_title='Hipikat2003;Holmesthesis2004;RossonCarroll1996',target_url='https://cs.uwaterloo.ca/~rtholmes/papers/icse_2005_holmes.pdf',status='outof2005–2025scope;2004thesissamefamily;notnewexperimentalcount'),
 dict(citation_id='Swb-CIT-08',study_family='SWB-STRATH',direction='forward',from_source='Swb-P01',locator='§7andHolmesMurphy2005reference',target_source_id='Swb-P04',target_url='https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf',status='citation_confirmed;primaryincluded'),
 dict(citation_id='Swb-CIT-09',study_family='SWB-PROMPT',direction='backward',from_source='Swb-P06',locator='§7RelatedWork;Ponzanelli2013references',target_source_id='Swb-P05',target_url='https://lucaponzanelli.gitlab.io/assets/publications/Ponz2013a.pdf',status='primaryfulltextread;nonhumanalgorithmexcluded'),
 dict(citation_id='Swb-CIT-10',study_family='SWB-PROMPT',direction='forward',from_source='Swb-P07',locator='§12;reference6cites2014Promptertoolpaper',target_source_id='Swb-P06',target_url='https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf',status='samePrompterfamilyearlier2014versioncitationconfirmed;notexact2016paperedge'),
 dict(citation_id='Swb-CIT-11',study_family='SWB-NCQ',direction='backward',from_source='Swb-P07',locator='§12references6,8,9',target_title='Prompter2014;Blueprint2010;Seahawk2013',target_source_id='Swb-P06',target_url='https://lucaponzanelli.gitlab.io/assets/publications/Ponz2015c.pdf',status='Prompterexpandedprimaryread;Seahawkexcluded;BlueprinthandledbystrandA'),
 dict(citation_id='Swb-CIT-12',study_family='SWB-NCQ',direction='forward',from_source='Swb-X03',locator='§3.13printedp118',target_source_id='Swb-P07',target_url='https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume14/issue04/24172/DagRep.14.4.108/DagRep.14.4.108.pdf',status='citation_confirmed;seminarrecapnotnewexperiment'),
 dict(citation_id='Swb-CIT-CORRECTION',study_family='SWB-REST',direction='forward_search_false_positive',from_source='Swb-X01',locator='fullPDFreferencefindSohanreturned0',target_source_id='Swb-P02',target_url='https://tianyi-zhang.github.io/files/chi2018-examplore.pdf',status='notconfirmedcitation;priorprovisionalclaimretractedbeforecommit'),
]
for filename,rows in [('attempts.jsonl',attempts),('screening.jsonl',screening),('citation-walks.jsonl',citations)]:
    (P/filename).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
print(json.dumps({'attempts':len(attempts),'screening_rows':len(screening),'discovery_unique_urls':len(discovery),'citation_walks':len(citations),'checked_utc':NOW},ensure_ascii=False))
