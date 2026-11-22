"""Materialize fixed three cases and nine A/B/C configurations."""
import csv,json,datetime
from pathlib import Path
P=Path(__file__).resolve().parent
J='https://journal.r-project.org/articles/'
RSTYLE='https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/'
INS='https://www.recensamantromania.ro/rezultate-recensamant-1992/'
R420='https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz'
R421='https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz'
UCI='https://archive.ics.uci.edu/dataset/53/iris'
CRAN='https://cran.r-project.org/src/contrib/'

c1=dict(case_id='RJ01',layer='consumer_first_RJournal',
analysis_title='Measuring the Extent and Patterns of Urban Shrinkage for Small Towns Using R',
consumer_url=J+'RJ-2022-004/',consumer_locator='§2 Data and methods; §3 Fig2 left panel1992; Table2 alternative',
purpose='Oltenia34개 소도시의 축소 양상·지표 관계를 PCA로 분석',
target_time='primary1992; 비교2018;1992/2002/2011 census와2018 statistics',
input_name='Romanian official census/statistics를 조합한13지표 연구입력',
field='Fig2 left panel: PC1 variance,1992',
reported_value='그래프 막대가5를 넘음; 정확한 소수값은 미표기·미확인',
unit='표준화된13지표의 주성분 분산',
publisher_url=INS,publisher_locator='Volumul1-1992 table03 도시별인구; Volumul2 socioeconomic tables',
publisher_edition='1992 census publication exists; author13-indicator workbook remains unlinked',
publisher_value='해당 PC1 분산값 미확인; 발행자 원표와 연구행렬 매핑 미확인',
usage_edition='미확인: reference years만 제시, 판·표·파일ID는 미특정',
usage_evidence='본문§2는1992/2002/2011 census와2018통계 사용 선언; supplement는 research_data.xlsx를 지목하나 파일 미포함',
run_id='미확인',
run_input_evidence='ZIP shrinking_cities.r lines12,17–21,37는 의도한 입력·변환만 기재; 실행ID/입력해시/저장run object 없음',
publisher_exists=True,candidate_publisher_exists=True,specific_usage=False,run_link=False,value_checked=False,candidate_value_checked=False,actual_used_edition_value_verified=False,strict_positive=False,
current_correction='미확인:1992 원자료의 실제 사용판·후속정정판 및 같은13지표 입력을 연결하지 못함',
missing_reason='연구 workbook 부재; 발행자 table/file mapping 부재; 정확 Fig2 값 부재; 소비 실행 부재',
source_ids=['RJ-C-004','RJ-SUP-004','RJ-P-INS1992','RJ-P-INS-XLS-FAIL'],
publisher_coverage='1992 census-edition catalogue 확인;13-indicator source coverage unknown',
usage_granularity='reference period only',
strongest_claim='공식1992 census판은 공개돼 있고 소비자는 이를 이용했다고 쓰지만, 해당13지표 행렬·정확PC1값·실제소비판은 연결되지 않았다.',
alternative_fields=[{'field':'Table2 Std.dev(PC1,1992)','value':'2.40','not_substituted':True},{'field':'Table2 variance proportion PC1','value':'1992=0.44;2018=0.44, but cumulative44.2% vs44.0%','not_substituted':True,'limit':'다른 기간의 같은 반올림값이며 판 대조가 아님'}],
minimum_next_evidence='research_data.xlsx 원본과 해당 파일을 사용한 당대기록 및13열↔발행자표·판 매핑; Fig2 생성시 row slice의 이유')

c2=dict(case_id='RJ02',layer='consumer_first_RJournal',
analysis_title='A Computational Analysis of the Dynamics of R Style Based on108Million Lines of Code from All CRAN Packages in the Past21Years',
consumer_url=J+'RJ-2022-006/',consumer_locator='§2.1 Data Source; §3 Fig1 top-left fx_assign, firstyear1998; §5 Reproducibility',
purpose='CRAN exported function에서 R 스타일의 역사적 변화 측정',
target_time='mirror acquisition declaration2020-07-01; analysis1998–2019; selectedfield1998',
input_name='CRAN package source tarballs; selected1998 one-submission-per-package sample',
field='Fig1 fx_assign:1998 exported functions using = assignment',
reported_value='A:그래프상0%; C:당대 저자 feature record0/386=0%',
unit='exported functions 비율(%)',publisher_url=CRAN+'Archive/',
publisher_locator='고정 저자명세의 Archive/Old16개 tar파일; DESCRIPTION 및 R/ member; cran_1998_publisher_receipts.json',
publisher_edition='1998 selected16 filename-versioned tarballs,16/16 current publisher object retrievals',
publisher_value='독립 전체 lintr/export 선택 재실행은 미수행; 저자 파생값0/386과 구별',
usage_edition='Zenodo4026589/v1.0 commit07a60457c88dbb20858441047f248d61ce2955c7의 target_meta 및 syntax_feature_yr1998가16개 tarball을 명시',
usage_evidence='논문§5가 archived DOI 지목; fixed README lines25–41+target_meta.RDS year1998 rows16; yearly feature record16path 모두 일치',
run_id='미확인',run_input_evidence='당대 selected-input manifest와 파생 feature record는 있음; original runID·입력 tar SHA·실제 read receipt는 없음',
publisher_exists=True,candidate_publisher_exists=True,specific_usage=True,run_link=False,value_checked=False,candidate_value_checked=False,actual_used_edition_value_verified=False,strict_positive=False,
current_correction='공식정정사유 미확인. filename/internalVersion 불일치3건(acepack,class,nnet) 관측; 당시 style를 최신package로 바꾸면 대상기간이 바뀜',
missing_reason='소비자의 원 tar bytes/hash 및 원 실행ID 없음; 원 CRAN전체 mirror snapshot 불명;0%는 author artifact 재독이며 independent publisher feature calculation 아님',
source_ids=['RJ-C-006','RJ-SUP-006','RJ-A-RSTYLE','RJ-A-RSTYLE-FIXEDTREE','RJ-A-FILE-06','RJ-A-FILE-07','RJ-A-FILE-08','RJ-P-CRAN-ACEPACK','RJ-P-OLD061-INDEX'],
publisher_coverage='declared1998tarball URL16/16 retrieved in full; same bytes as2020consumer unknown',
usage_granularity='1998 selected16 versioned tarballs; entire mirror snapshot/bytes unknown',
strongest_claim='당대 archive가1998 입력16개를 filename/version 수준으로 지목하고 같은 이름의 발행자객체16/16에 도달했다. 실제 실행·소비바이트·독립0% 검증은 별개다.',
author_record_reread=True,author_record_value={'true':0,'denominator':386,'value_percent':0,'record_packages':16,'not_independent_publisher_validation':True},
prior_hypothesis_refuted='A의 날짜만으로는U미확인이라는 초기판정에서 C의 고정 input manifest를 읽고 U=true로 변경; 표본·필드 변경 없음',
alternative_fields=[{'field':'Table2 basecommunity numberofpackages','value':'5157','not_substituted':True}],
minimum_next_evidence='당대 runID와16tarball hashes/read events 또는 원 code.db+locked extractor/lintr environment; 동일 export 선정·파싱으로 발행자객체를 독립 대조')

c3=dict(case_id='RJ03',layer='consumer_first_RJournal',analysis_title='rmonad: pipelines you can compute on',
consumer_url=J+'RJ-2022-007/',consumer_locator='§5 Statistical analysis of Iris data; printed get_value(m)[id] ANOVA Species row Df column',
purpose='Iris Petal.Length~Species의 ANOVA/Kruskal-Wallis/t-test를 파이프라인에 넣어 결과·오류 추적 시연',
target_time='historical Iris observations; original analysis executiondate/Rrelease unknown; article2022-06-21',
input_name='R datasets::iris via data(iris)',field='ANOVA Species row Df',reported_value='2',unit='degrees of freedom',
publisher_url=R420,publisher_locator='src/library/datasets/data/iris.R, Species=gl(3,50); same member inR4.2.1',
publisher_edition='publisher candidatesR4.2.0(2022-04-22) andR4.2.1(2022-06-23), not consumer-identified',
publisher_value='candidate SpeciesDf=3−1=2; both releases identical iris.R SHA256',
usage_edition='미확인: data(iris)는 입력이름만, 실제 R/datasets release를 특정하지 않음',
usage_evidence='본문§5 및 supplement rmonad.R lines62–68; unrelated toy-sessionInfo는 이 실행에 결합하지 않음',
run_id='미확인; Fig3 node1–4 are in-graph node IDs, not a globally dated runID',
run_input_evidence='그림은 수행결과와 nodes를 보이지만 저장Rmonad객체·inputhash·세션/실행ID가 없어 publisher edition으로 연결하지 못함',
publisher_exists=True,candidate_publisher_exists=True,specific_usage=False,run_link=False,value_checked=False,candidate_value_checked=True,actual_used_edition_value_verified=False,strict_positive=False,
current_correction='UCI는 samples35/38 수정 안내; iris.data와bezdekIris.data 차이 실제 확인. Df2는 불변이지만 대안SumSq는436.6↔437.1. R후보두판 iris.R는 동일',
missing_reason='원 실행의 R/datasets판 미상. 여러 판·수정 전후파일에서 같은Df2라 값일치만으로 실제사용판을 구별할 수 없음',
source_ids=['RJ-C-007','RJ-SUP-007','RJ-P-IRIS','RJ-P-R-420','RJ-P-R-421','RJ-P-UCI','RJ-P-UCI-IRIS'],
publisher_coverage='two full R tarballs and bothUCIvariants read; not original consumer object',
usage_granularity='dataset name only',value_check_scope='candidate compatibility only; actual-used-edition verification=false',
strongest_claim='공개 R후보의 독립 원자료는 보고Df2와 양립한다. 동일바이트·동일Df를 가진 여러 판과 정정변형이 있어 원래 사용판·실행은 특정하지 못한다.',
alternative_fields=[{'field':'same ANOVA table Species SumSq','consumer_value':'437.1','R420_R421_bezdek':'437.1028→437.1','uci_iris':'436.6437333333333→436.6','not_substituted':True,'limit':'후보배제에 도움되나 하나의 실제 R판 사용을 증명하지 않음'},{'field':'Fig3 elapsed seconds/prose milliseconds','value':'captionseconds vs prosems','not_substituted':True,'limit':'실행메타데이터이며 주입된 Iris field가 아님'}],
minimum_next_evidence='당대 저장Rmonad객체/세션 및 입력객체 digest가 executionID와 연결되고 publisher Rrelease/iris bytes와 맞는 기록')
cases=[c1,c2,c3]

def cfg(urls,values,evidence,new,j,*,p=False,u=False,r=False,v=False,candidate=False,reread=False):
    return dict(visible_urls=urls,visible_values=values,evidence=evidence,new_fact=new,judgment=j,publisher_exists=p,specific_usage=u,run_link=r,value_checked=v,candidate_value_checked=candidate,record_reread=reread)
c1['A']=cfg([c1['consumer_url']],['Fig2 exactPC1variance unknown; alternativeTable2std.dev2.40'],'§2 censusreferenceyears+methods; §3 figure/table','baseline','사용 선언은 일반연도 수준. 정확판·값·실행 모두미확인')
c1['B']=cfg([c1['consumer_url'],INS],['publisher1992 censuscatalogue; PC1value unavailable'],'INS Vol1table03/Vol2 목록','B−A: publisher구분1992 census판 공개 존재','P후보존재만확인;13지표 입력매핑없음',p=True)
c1['C']=cfg([c1['consumer_url'],INS,J+'RJ-2022-004/RJ-2022-004.zip'],['PC1exactvalue stillunknown; workbookmissing'],'shrinking_cities.r12,17–21,37–38,47–66; ZIPinventory','C−B: inputfilename, sheet, scaleTRUE, row slicing 확인; workbook실물없음 발견','코드는실행영수증아님;U/R/V미확인',p=True)
c2['A']=cfg([c2['consumer_url'],'https://doi.org/10.5281/zenodo.4026589'],['graph~0%; targetyear1998; acquisition2020-07-01'],'§2.1, §3Fig1, §5 citedarchiveDOI; archivecontentsnotyetvisible','baseline','취득일·개념적corpus범위만으로specificinput불명')
c2['B']=cfg([c2['consumer_url'],CRAN+'Archive/'],['publisherfilenameeditions exist; primary0% not independently calculated'],'Publisher archive catalogue; exact16filechecks only become selectable throughCmanifest','B−A: publisher가tarfilename판을구분함; mirror날짜와별개','P발행판후보존재; 실제chosen16은B자료만으로선택불가',p=True)
c2['C']=cfg([c2['consumer_url'],'https://zenodo.org/records/4026589',RSTYLE+'target_meta.RDS',RSTYLE+'data/syntax_feature_yr1998.RDS',RSTYLE+'rjournal_submission/figures.R',CRAN+'Archive/acepack/acepack_1.1.tar.gz'],['authorrecord0/386=0%;16selectedtarballs;16/16publisherretrieval'],'DOI→fixedtag/commit→target_meta16path→feature16path; independentpublisherfiles samefilename; receiptsjson','C−B: specific selectedversions nowdeclared; generic-date-only U미확인 가설반증. 정확0/386은authorrecord재독','U=true(filename/version), R=false,V=false; 원 소비바이트와 실행은미확인',p=True,u=True,reread=True)
c3['A']=cfg([c3['consumer_url']],['ANOVA SpeciesDf2; alternativeSumSq437.1'],'§5 data(iris), aov, printedoutput; Fig3nodes','baseline','dataset이름+계산식+값은있으나version/run identity없음')
c3['B']=cfg([c3['consumer_url'],R420,R421,UCI],['candidateDf2 inbothRreleases/UCIvariants; iris.Rhashsame; altSumSq437.1vs436.6'],'publisher literaldata and corrections; iris_value_comparison.json','B−A: 같은Df여도 edition/rowvalue달라짐; Rreleasepair는같은irisbytes','candidatevalue양립만;실제사용판미상으로strictV=false',p=True,candidate=True)
c3['C']=cfg([c3['consumer_url'],R420,R421,UCI,J+'RJ-2022-007/RJ-2022-007.zip'],['reportedDf2; candidateDf2; nooriginalinputhash'],'rmonad.R62–95; nocachedIrisRmonadobjectinZIP','C−B: intendedinput and transform readable, noadditionalactualversion/run record','recipe와nodeplot을runid로승격불가;strictU/R/V미확인',p=True,candidate=True)
for r in json.loads((P/'cran_1998_publisher_receipts.json').read_text()):
    if r['source_url'] not in c2['C']['visible_urls']:
        c2['C']['visible_urls'].append(r['source_url'])
for c in cases:
    for previous,next_level in [('A','B'),('B','C')]:
        for field in ['visible_urls','visible_values']:
            c[next_level][field]=list(dict.fromkeys(c[previous][field]+c[next_level][field]))
metadata=json.loads((P/'frame_all_metadata.json').read_text())['rows']
sources={r['source_id']:r for r in map(json.loads,(P/'sources.jsonl').read_text().splitlines())}
for c,suffix in zip(cases,['004','006','007']):
    entry=next(r for r in metadata if r['doi'].endswith('-'+suffix))
    c['analysis_title']=entry['title']
    c['consumer_first_recorded_open_utc']=sources['RJ-C-'+suffix]['opened_utc']
    c['first_open_precision']='Earliest semantic web UTC uninstrumented; recorded metadata GET time shown. Consumer-field freeze completed2026-11-22T22:09:48.058572+00:00 before publisher reading.'
    c['publisher_first_recorded_open_utc']={'RJ01':'2026-11-22T22:12:48Z (INS2011); exact1992 initialwebUTC uninstrumented; verifiedreread22:15:29Z','RJ02':'2026-11-22T22:11:02Z','RJ03':'2026-11-22T22:11:02Z'}[c['case_id']]
    c['configuration_limit']='Constructed A/B/C evidence packets and self-reading, not blinded independent evaluators. Later C-guided publisher16-file check is explicitly separated from B catalogue.'
(P/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')

def csvwrite(name,rows):
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for row in rows:w.writerow({k:(json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v) for k,v in row.items()})
csvwrite('consumers.csv',[{k:v for k,v in c.items() if k not in ['A','B','C']} for c in cases])
readingrows=[]
for c in cases:
    for level in ['A','B','C']:
        readingrows.append(dict(case_id=c['case_id'],configuration=level,field=c['field'],target_time=c['target_time'],**c[level]))
csvwrite('readings.csv',readingrows)
csvwrite('runs.csv',[dict(case_id=c['case_id'],run_id=c['run_id'],input_name=c['input_name'],input_declaration=c['usage_evidence'],run_input_evidence=c['run_input_evidence'],consumer_input_hash='미확인',original_run_link=False,author_saved_record=c['case_id']=='RJ02',later_audit_not_original='iris_value_comparison.json' if c['case_id']=='RJ03' else ('rstyle_author_value_reading.json' if c['case_id']=='RJ02' else 'ZIPinventoryonly'),source_urls=c['C']['visible_urls'],missing_reason=c['missing_reason'],minimum_next_evidence=c['minimum_next_evidence']) for c in cases])

editions=[dict(case_id='RJ01',edition_id='INS-RPL1992',publisher_url=INS,published_or_changed='referenceperiod1992; currentcataloguepublicationdateunknown',period='1992 census reference',file_id='VOL1_1992_Tabel03 andVol2catalogue; actual13indicators unmapped',hash='미확인',hash_origin='none',selected_field_value='미확인',previous_next='1992→2002census is reference-period change, not verified correction sequence',used_vs_candidate='publishercandidate; consumeractualeditionunconfirmed',limit='research_data.xlsx absent')]
for r in json.loads((P/'cran_1998_publisher_receipts.json').read_text()):
    editions.append(dict(case_id='RJ02',edition_id=r['declared_local_path'].rsplit('/',1)[-1],publisher_url=r['source_url'],published_or_changed='authorrecordmtime inrstyle_1998_input_manifest.csv; publisherarchivefilename independently confirmed',period='selectedyear1998',file_id=r['declared_local_path'],hash=r.get('sha256'),hash_origin='calculatedfullcurrentpublisherbytes2026-11-22',selected_field_value='component; aggregatepublisherfx_assign not independently computed',previous_next='full16-object nextsnapshotunidentified',used_vs_candidate='author-declaredfilenameversion; actualconsumerbyteequivalenceunconfirmed',limit='DESCRIPTION '+', '.join(r.get('description_package_version',[]))+'; nooriginalrunhash'))
for version,url,date in [('R4.2.0',R420,'2022-04-22'),('R4.2.1',R421,'2022-06-23')]:
    editions.append(dict(case_id='RJ03',edition_id=version,publisher_url=url,published_or_changed=date,period='historicalIris150observations',file_id='src/library/datasets/data/iris.R',hash='77af4424d5361afe1c46e7fb95bc4f95681f5515a586cb41c062b111c691dc5c',hash_origin='calculatedmemberbytesfromfullpublisherarchive',selected_field_value='candidateSpeciesDf2; alternativeSumSq437.1028',previous_next='R4.2.0→R4.2.1 officialadjacentreleasepair',used_vs_candidate='researchercandidate; notactualconsumerdeclaration',limit='R4.2.1 publicreleasedate followsconsumerpublication; identicalbytes do not establishuse'))
for file,sha,val in [('iris.data','6f608b71a7317216319b4d27b4d9bc84e6abd734eda7872b71a458569e2656c0','Df2; altSumSq436.6437333333333'),('bezdekIris.data','0fed2a99db77ec533a62dc66894d3ec6df3b58b6a8f3cf4a6b47e4086b7f97dc','Df2; altSumSq437.1028')]:
    editions.append(dict(case_id='RJ03',edition_id='UCI53/'+file,publisher_url='https://archive.ics.uci.edu/static/public/53/iris.zip',published_or_changed='recorddonated1988-06-30; variant/correctiondateunknown',period='historicalIris150observations',file_id=file,hash=sha,hash_origin='calculatedZIPmemberbytes',selected_field_value=val,previous_next='co-publishedvariants; notadatednexteditionpair',used_vs_candidate='auxiliarycounterexample notconsumerinputroute',limit='Rconsumer saysdata(iris); UCIcopiesnotactualconsumedobject'))
csvwrite('editions.csv',editions)
summary=dict(audit_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),case_count=3,configuration_rows=len(readingrows),publisher_exists=sum(c['publisher_exists'] for c in cases),specific_usage=sum(c['specific_usage'] for c in cases),run_link=sum(c['run_link'] for c in cases),value_checked=sum(c['value_checked'] for c in cases),candidate_value_checked=sum(c['candidate_value_checked'] for c in cases),strict_positive=sum(c['strict_positive'] for c in cases),conditioned_strict_value_rate='해당 없음: 원래 사용판+실행 객체에 대한 독립 기준 분모0',notes=['Pcounts publisherdistinguishedcandidateedition existence, notmatched13inputfields','U-RJ02 limitedto1998selected16filenames; entiremirrorsnapshotunknown','candidatevalueagreementisnotstrictV','allcases same-modelselfreading; parentreviewnotexternalindependentread'])
(P/'case_counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
