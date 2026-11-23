#!/usr/bin/env python3
"""Materialize the independent, pre-ranking manual screen. No network or ranking."""
import csv
import datetime as dt
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat()

def save(name, data):
    (ROOT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def normalize(s):
    return re.sub(r'\s+', ' ', s.casefold().replace('-', ' ')).strip()

# Every available revision-one body was displayed and read, in frame order.
# Tuple: eligible, C1, C2, environment, origin/locus, reason/boundary.
SC = {
1: (True,'root usertype=employee이면 user 각 항목에 batchId 필요','각 user 항목의 firstName·lastName 문자열 필수 유지','draft-07; 런타임 명시 없음','p1+pre2 기대실패 / pre1 items.required와 properties','두 조건은 독립. 두 번째 조건은 prose가 아닌 코드 명시. 선택 1.'),
2: (True,'JSON:API 데이터의 type이라는 속성명을 schema에 표현','기존 id property의 string 제약을 유지','Ajv 웹앱 / Drupal 10 JSON:API','마지막 p / pre2 properties.id.type:string','C2는 별도 prose 요청이 아니라 기존 schema 코드에서 읽은 보존 조건. JS-1·056 JS-3와 같은 원칙으로 적격. id:1 근접음성은 C1만 만족. 선택 2; 봉인 전 일관성 정정.'),
3: (True,'unit가 있으면 문자열이어야 함','그 문자열을 Astropy FITS 규칙으로 검사하여 실패를 거부','Python / jsonschema / astropy.units; 판 미명시','pre1 type:string / p1,p2,pre2','문자열 타입과 FITS 적합은 독립. type은 코드 조건. 2번 일관성 정정 뒤 후순위 적격; 후보를 보고 교체하지 않음.'),
4: (True,'value가 런타임 minValue 이상','value가 런타임 maxValue 이하','TypeScript / TypeBox; 판 미명시','prose 및 Type.Number 예시','독립 하한·상한; 후순위 적격이나 이미 앞의 두 자리를 채움.'),
5: (True,'다른 schema 내부 entity의 id 경로 참조 해결','참조한 id의 string 제약 유지','Node.js / Ajv 8.11.0; strictSchema:false','prose 및 main/entity/request 코드','서로 다른 ref 경로 성공·실패는 저자 보고. 실행 미실시. 후순위 적격.'),
6: (False,'사전에 이름을 모르는 동적 객체에서 schema 생성','어떤 validator 제약인지 특정되지 않음','Vert.x 언급; Spring Boot는 제목','p1 전체','동적 생성 요청은 있으나 두 독립 양성 조건이 조작 가능하게 제시되지 않음.'),
7: (False,'같은 DTO에서 만든 JSON/schema 불일치 설명','무엇이 invalid인지 알고 싶음','C# / Json.NET API 코드; 판 미명시','pre1·pre2 및 마지막 p','DTO·instance·문제 dictionary가 본문에 없어 두 양성 입출력 조건을 고정할 수 없음.'),
8: (True,'profile.email이 있으면 bearer도 필요','profile.password가 있으면 bearer도 필요','JSON Schema 2019-09','마지막 두 p 및 schema','두 별도 필드 의존. dependentRequired 철자/값 형태 및 원문 오류를 교정한 실행으로 보고하지 않음. 후순위 적격.'),
9: (True,'instance를 미리 나열한 객체 중 하나로 제한','나열된 객체 자체도 fruit 정의에 맞는지 검사','JSON Schema 2020-12','p1,p2,pre1','instance 검사와 enum에 적힌 값의 검사 층을 구분. properties 배열은 원문 오류. 후순위 적격.'),
10: (False,'producer를 바꾸지 않고 plain JSON 소비','Oracle JDBC sink로 복제','Strimzi Kafka / Confluent JDBC sink / Schema Registry','앞 prose·connector YAML·끝 세 질문','직렬화 wire format/connector 연결 문제. 사전 Schema validation/annotation 범위 밖; 답의 난이도로 제외한 것 아님.'),
11: (True,'secondAmount < firstAmount 동적 비교','사용자 정의 제약 오류 메시지 제공','JSON Schema 2020-12; validator 제품 미명시','목록 첫째·둘째 항목','추가 label/다층 지침도 guard. custom vocabulary와 실행 validator 확장은 같지 않음. 후순위 적격.'),
12: (False,'allOf 안 조건부 USA 우편번호 schema가 왜 통과하는지 설명','별도의 두 번째 구현 요구 미확보','JSON Schema 2019-09','마지막 p 및 예시','순수 연산 설명 질문. 국가별 코드 여러 줄을 두 독립 사용자 기능 요구로 분할하지 않음.'),
13: (True,'누락된 required key를 구조적으로 식별','그 key를 해당 validation message와 연결한 dictionary 반환','Python jsonschema Draft202012Validator','p1,p2 및 expected-output pre','type 오류도 기존 출력에 보존; 메시지 문자열 분해 회피는 사용자 선호. 후순위 적격.'),
14: (True,'공통 color 정의를 중복하지 않고 두 subtype 허용','그 이외 추가 속성 거부','JSON Schema 2020-12','p1 및 마지막 p','두 양성 객체와 추가속성 음성 구별. kind:number 오기는 실행 성공으로 바꾸지 않음. 후순위 적격.'),
15: (False,'data.source-id가 sources.id 중 하나','참조한 source.type에 따라 서로 배타적인 attribute 요구','런타임/규격판 명시 없음','두 질문과 후속 prose','두 조건은 있으나 필요한 환경/명시적 환경 미정이 본문에 없음. custom code 여부 질문을 환경 미정 선언으로 간주하지 않음.'),
16: (False,'입력의 새 property 이름은 동적 properties 배열에 있어야 함','배열에 적힌 이름은 모두 입력에 있어야 함','본문 런타임·draft 미명시; 최초 태그에는 Ruby/Rails','강조 p 및 valid/invalid pre','독립 두 조건은 있음. 태그만으로 본문 환경을 발명하지 않음. valid 예시의 names/name 불일치도 보존.'),
17: (True,'REST 응답을 draft-07 또는 2020-12로 검증','동시 thread 사이 변수 혼합을 피함','JMeter 5.4.3; 현재 plugin은 0.4라고 저자 보고','p1,p2','C2는 보고된 잘못된 동작을 피하려는 조건이며 별도 prose 요청보다 약한 근거. 후순위 적격.'),
18: (False,'JSON Schema에서 PostgreSQL tables 자동 생성','독립 두 번째 출력 제약 미확보','Python / PostgreSQL; draft2019-09','prose·DDL 변환 호출','DB 생성은 사전 Schema validation/annotation 밖. 불완전 코드에서 임의 mapping 조건을 보충하지 않음.'),
19: (True,'ArgumentList의 일반 string 요소 허용','선택적으로 중첩된 string 배열도 허용','웹 JSON Schema Validator paste 사용; 판 미명시','p2,p4 및 desired input','중첩 string 배열의 내부 type도 보존. 제품 링크는 환경 진술이며 링크 밖 자료는 선정에 읽지 않음. 후순위 적격.'),
20: (False,'schema 문자열을 type-safe object로 변환','완전한 schema 타입 수작업 작성을 피하고 싶음','TypeScript는 최초 태그; 본문은 schema2020-12 링크','세 p','현재 요청은 한 parsing/typing 기능과 구현 선호. form 생성은 장래 목적이지 독립 출력 요구가 아님.'),
}
LD = {
1: (True,'Windows local JSON-LD 파일을 Turtle로 변환','Turtle에서 context를 사용한 JSON-LD 역방향도 유지','RDFLib 6.3.2 / Python 3.11 / Windows','p1,p2,pre1 및 마지막 p','두 방향 명시. 역방향 성공은 저자 진술뿐. 선택 1.'),
2: (False,'Google event snippet의 구매 링크 표시','snippet이 자기 페이지에 연결됐는지 확인','Google Search Console / movie-ticket web page','p3 및 마지막 두 p','검색 UI 노출·연결 진단으로 사전 제외 범주. 직접 JSON-LD 변환의 두 조건 아님.'),
3: (True,'R에서 application/ld+json script 내용 추출','추출 결과를 JSON으로 읽고 가격·설명 등 실제 필드를 보존','R / rvest+xml2+jsonlite+dplyr; 판 미명시','p1,pre1 html_nodes/html_text/fromJSON,pre2,pre3','텍스트 추출과 구조 파싱/필드 보존을 별개로 검사. 복수 script의 trailing-garbage 보고 보존. 선택 2.'),
4: (False,'startDate의 ISO8601 오류 원인 해결','별도의 두 번째 변환 조건 미확보','Google Webmaster Tools / JSON-LD Playground','전체 prose·단일 Event snippet','날짜 표현 한 문제. endDate가 예시에 있는 것을 두 번째 별도 요구로 승격하지 않음.'),
5: (True,'blank-node 내용을 sh:or의 list 안에 중첩','ex:User·ex:Person list 순서와 class 관계 보존','Fuseki DESCRIBE / 웹 RDF converter','pre1 input / pre2 desired output','구체 입출력과 환경 있음. 결과표의 bare sh:class string이 IRI인지 별도 미확인; 후순위 적격.'),
6: (True,'인스턴스 @type가 가리키는 class의 view 속성을 가져오기','두 class와 view/preferredView 관계를 원하는 출력에 유지','JSON-LD Playground frame; 판 미명시','문서 pre1·desired pre2·끝 p','desired JSON 자체가 문법 오류이며 사용자가 비표준 @type임을 인정. 불가능할 수도 있는 적격 요구를 후보수로 교체하지 않음.'),
7: (True,'compact IRI 값을 full IRI 값으로 풀기','원 출력의 animal property와 context 유지','JSON-LD Playground','input pre1 / desired pre2','C2는 desired-output 코드에서 읽은 조건. expansion의 표준 출력과 충돌할 수 있음. 후순위 적격.'),
8: (True,'Safari가 JSON-LD script를 읽을 때 예외를 피하기','trailing comma를 넣지 않아 valid JSON 유지','Safari; 판 미명시','pre1 및 오류 뒤 마지막 p','browser parse 동작과 JSON 유효성은 독립; 저자 관측이며 재현 실행 없음. 후순위 적격.'),
9: (True,'하위 페이지의 이름·URL·순번 계층을 표현','SiteNavigationElement 속성 경고를 제거','HTML script / schema.org validator; 제품판 미명시','nested pre / 마지막 no-subpage 대조','다층 데이터 표현과 semantic-property 경고 별개. 사용자 validator 성공 주장만 있고 실행 없음. 후순위 적격.'),
10: (True,'알려진 경로의 모든 leaf 속성을 회수','결합 결과에서 distinct triples만 얻기','SPARQL CONSTRUCT / triplestore; 제품판 미명시','p1·pre1·p2·끝 목록','LD에서 온 문서 재구성의 두 조건. 다중값·optional·unknown leaf 보존. 후순위 적격.'),
11: (True,'모든 component가 로드된 뒤 합치기','각 component 내용을 원하는 중첩 구조의 한 script로 보존','JavaScript 또는 ASP.NET 명시','p1 및 desired-output pre4·끝 p','동기화와 문서 생성은 별개; desired JSON ellipsis를 실행 가능한 자료로 간주하지 않음. 후순위 적격.'),
12: (False,'JSON-LD 링크를 sitemap 대용으로 쓰는 SEO 전략 질문','독립 두 번째 구현 조건 없음','React Helmet / MongoDB / Express','p1 전체','순수 SEO 전략/대안 문의. 구체적인 두 입출력 조건 없음.'),
13: (False,'valid한 VisualArtwork JSON-LD의 Google rich result 검출','독립 두 번째 문서변환 조건 없음','schema.org validator / Google rich-results tester','p1·pre1','Google 검색 UI 지원/노출 문제로 사전 제외; 현재 json-ld이나 최초 태그는 jsonschema였음.'),
14: (False,'@graph가 허용되며 더 좋은지 일반 설명','구체적인 두 양성 조건 없음','Google/Yoast 언급; 실행환경 미명시','두 p','순수 메타/선택 조언. 구체 입출력이 없으므로 제외.'),
15: (True,'fetch Response를 JSON 데이터로 읽기','itemListElement 아래 result blocks를 얻기','Vue3 / JavaScript / Google Knowledge Graph API','search/globalSearch code·마지막 p','응답 파싱과 결과 경로 접근을 구분. score는 질문 원 데이터 resultScore이며 SO 평점이 아님. 후순위 적격.'),
}

index=json.loads((ROOT/'revision-index.json').read_text())
frame=json.loads((ROOT/'frame.json').read_text())
gate=json.loads((ROOT/'stage2-gate.json').read_text())
assert gate['root_confirmed'] and len(index)==35
selected={('jsonschema',1):'JS-5',('jsonschema',2):'JS-6',('json-ld',1):'LD-5',('json-ld',3):'LD-6'}
fields=['tag','rank','question_id','created_utc','original_url','revision_url','revision_guid','current_tags_json','initial_tags_json','body_sha256','read_status','domain_eligible','C1','C2','environment','environment_basis','explicit_or_code_basis','independent_conditions','eligible','selection','exclusion_or_gap','source_id','body_work_id','body_cache_reused','read_reuse_of','read_recorded_utc','initial_title','current_title','scope_status']
out=[]; sources=[]; locators=[]
for tag,notes,prefix in [('jsonschema',SC,'S'),('json-ld',LD,'L')]:
    byrank={r['rank']:r for r in index if r['tag']==tag}
    for rank in range(1,21):
        if rank not in byrank:
            out.append(dict(tag=tag,rank=rank,read_status='not_run',eligible='not_run',selection='frame_position_unfilled',exclusion_or_gap='current_tag_frame_pool_exhausted: API has_more=false; 15 available/20 planned; no replacement',source_id='',scope_status='frame_missing'))
            continue
        r=byrank[rank]; n=notes[rank]; sid=f'H-SO-{prefix}{rank:02d}'
        data=json.loads((ROOT/'.cache'/f"{r['question_id']}.json").read_text())
        body=data['body']; assert hashlib.sha256(body.encode()).hexdigest()==r['body_sha256']
        row=dict(tag=tag,rank=rank,question_id=r['question_id'],created_utc=r['created_utc'],original_url=r['url'],revision_url=r['initial_revision_url'],revision_guid=r['revision_guid'],current_tags_json=json.dumps(r['current_tags'],ensure_ascii=False),initial_tags_json=json.dumps(r['initial_tags'],ensure_ascii=False),body_sha256=r['body_sha256'],read_status='read_complete_initial_body',domain_eligible='yes' if n[0] else 'see_exclusion',C1=n[1],C2=n[2],environment=n[3],environment_basis='first-body prose/code/edition; title/tag-only limitations are explicit',explicit_or_code_basis=n[4],independent_conditions='yes' if n[0] else 'not_sufficient_for_all_screening_gates',eligible='yes' if n[0] else 'no',selection=selected.get((tag,rank),'eligible_after_first_two' if n[0] else 'excluded'),exclusion_or_gap=n[5],source_id=sid,body_work_id=r['body_work_id'],body_cache_reused=str(r.get('body_cache_reused',False)).lower(),read_reuse_of=json.dumps(r.get('reused_from_row',{})),read_recorded_utc=NOW,initial_title=r['initial_title'],current_title=r['current_title'],scope_status='screened')
        out.append(row)
        counts={'p':0,'pre':0}
        for m in re.finditer(r'<(p|pre)(?:\s[^>]*)?>[\s\S]*?</\1>',body):
            typ=m.group(1); counts[typ]+=1
            locators.append(dict(source_id=sid,question_id=r['question_id'],block_id=f'{typ}{counts[typ]}',html_char_start=m.start(),html_char_end_exclusive=m.end(),html_start_line=body.count('\n',0,m.start())+1,html_end_line=body.count('\n',0,m.end())+1,block_sha256=hashlib.sha256(m.group().encode()).hexdigest()))
        sources.append(dict(source_id=sid,work_id=r['body_work_id'],kind='request_original_first_revision',lineage={'site':'Stack Overflow','question_id':r['question_id'],'revision_number':1,'revision_guid':r['revision_guid'],'representation':'Stack Exchange API body HTML','new_vs_056':'new 2023 request; not original 2021 training request','same_work_mirrors_counted':False},questions=['Q1','Q3','Q4','Q6'],case_ids=[selected[(tag,rank)]] if (tag,rank) in selected else [],original_url=r['url'],fixed_url=r['initial_revision_url'],api_url=f"https://api.stackexchange.com/2.3/posts/{r['question_id']}/revisions?site=stackoverflow&filter=withbody&pagesize=100&page=1",version={'revision_guid':r['revision_guid'],'body_sha256':r['body_sha256'],'original_created_utc':r['created_utc']},opened_utc=r['acquisition_utc'],read_utc=NOW,read_timestamp_basis='독해 완료를 이 원장 작성 때 기록; 각 최초 표출의 초 단위 시각은 별도 계측하지 않음',locus={'screening_frame':f'{tag} rank {rank}','body_scope':'complete original body incl code, excluding linked external pages','condition_loci':n[4],'block_index':'body-locations.json'},checked=n[5],scope_and_limit='원작성자 문제·원입력·코드·기대값만 직접 독해; 답/댓글/평점/공급자 F1/새 순위 미열람. 현재태그 모집이므로 역사적 모집단 복원 아님.',evidence_type=['observation: first-revision body read','author_claim: reported behavior','researcher_inference: eligibility and condition split'],opposing_source_ids=['H-STD-VAL07'] if tag=='jsonschema' else ['H-STD-LDAPI11'],access_status='opened_and_read',external_work_count_eligible=True))
        r['read_status']='read_complete_initial_body'; r['read_recorded_utc']=NOW; r['source_id']=sid

with (ROOT/'holdout.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
save('revision-index.json',index)
save('body-locations.json',{'coordinate_system':'decoded API body HTML Unicode character offsets, zero-based end-exclusive; p/pre numbered separately in source order','records':locators})

def req(case,tag,rank,C1,C2,language,version,dialect,guard,L,origins,fixtures,remaining,prohibitions):
    r=next(x for x in index if x['tag']==tag and x['rank']==rank)
    return dict(case_id=case,domain='JSON Schema' if tag=='jsonschema' else 'JSON-LD',stratum='new_holdout',status='selected',rank=rank,question_id=r['question_id'],url=r['url'],revision_url=r['initial_revision_url'],revision_guid=r['revision_guid'],body_sha256=r['body_sha256'],source_id=r['source_id'],C1=C1,C2=C2,language=language,version=version,dialect=dialect,guard=guard,L_terms=L,definition_file='evidence/holdout/requirements-new.json',condition_origins=origins,fixtures=fixtures,dynamic_values=remaining['dynamic'],preserved_fields=remaining['fields'],unspecified=remaining['unspecified'],prohibited_behavior=prohibitions,selection_basis='first eligible 2 in current canonical-tag creation order; chosen before candidate ranking, without F1/answers/comments/scores',claim_status='requirements and proposed tests; no provider execution or user success verified',frozen_utc=NOW)

requirements=[
req('JS-5','jsonschema',1,
'root usertypeがemployeeなら user arrayの各項目にbatchIdを要求する。',
'各項目のfirstName・lastNameを必須文字列として保つ。',
'명시 없음; draft-07 schema 환경만 고정','validator 제품판 미명시','원문 $schema=http://json-schema.org/draft-07/schema',
'원문 userType/usertype 대소문자 불일치, array 위치의 required 및 sample trailing comma를 보존한다. 이 오류를 자동 교정한 실행 성공으로 보고하지 않는다. visitor에게 batchId 의무가 없다는 해석은 조건문의 범위에서 얻은 연구자 해석이다. 빈 배열/root 속성 부재의 기대는 미명시.',
['batchId to be required','if then else'],
{'C1':{'origin':'explicit_prose_plus_expected_output','locus':'p1; p2; pre2 employee sample'},'C2':{'origin':'explicit_schema_code_not_separate_prose','locus':'pre1 $.properties.user.items.required; $.properties.user.items.properties.firstName/lastName'},'environment':{'origin':'code','locus':'pre1 $schema'}},
[{'id':'JS-5-P1','origin':'researcher_constructed_unrun','input':{'usertype':'employee','user':[{'firstName':'A','lastName':'B','batchId':'b1'}]},'expected':'C1=true,C2=true; accept'},
 {'id':'JS-5-P2','origin':'researcher_constructed_unrun','input':{'usertype':'employee','user':[{'firstName':'A','lastName':'B','batchId':'b1'},{'firstName':'C','lastName':'D','batchId':'b2'}]},'expected':'C1=true,C2=true; accept'},
 {'id':'JS-5-N1','origin':'researcher_near_negative_unrun','input':{'usertype':'employee','user':[{'firstName':'A','lastName':'B'}]},'expected':'C1=false,C2=true; reject'},
 {'id':'JS-5-N2','origin':'researcher_near_negative_unrun','input':{'usertype':'employee','user':[{'firstName':'A','batchId':'b1'}]},'expected':'C1=true,C2=false; reject'},
 {'id':'JS-5-G1','origin':'researcher_guard_probe_unrun','input':{'usertype':'visitor','user':[{'firstName':'A','lastName':'B'}]},'expected':'conditional batchId assertion inactive; source code name constraints remain'}],
{'dynamic':['root usertype controls item-level condition; batchId string contents not fixed'],'fields':['usertype','user array','firstName','lastName','batchId when employee'],'unspecified':['runtime','validator version','empty user array','root usertype/user absence']},
['입력에 batchId를 임의 삽입하여 검증을 대신하지 않는다(연구자 보존 규칙).','원문의 잘못된 schema가 실제 성공한다고 보고하지 않는다.']),
req('JS-6','jsonschema',2,
'JSON:API 데이터의 type 속성을 schema 키워드와 혼동하지 않고 기술하여 예시 type=article 데이터를 허용한다.',
'기존 schema 조각의 id 속성에 string 타입 제약을 유지한다.',
'웹앱 Ajv 명시; JavaScript는 도구명에서의 추론이며 본문 언어 선언은 없음','Ajv 판 미명시 / 서버 Drupal 10 JSON:API','JSON Schema draft 및 JSON:API 버전 미명시; draft-07은 정의 비교용',
'C2는 기존 schema 코드에서 읽은 유지 조건이지 별도 prose 요청은 아니다. type 및 id의 required는 본문에 없다. article을 유일한 enum 값으로 제한하라는 요청도 없다. 원 예시 trailing comma와 불완전 schema 조각을 자동 교정한 실행 성공으로 보고하지 않는다.',
['property named type','validate the JSON'],
{'C1':{'origin':'explicit_prose_plus_example','locus':'last p property named type; pre1 type:article'},'C2':{'origin':'code_implied_preservation_not_separate_prose','locus':'pre2 properties.id.type:string'},'environment':{'origin':'explicit_prose','locus':'p1 Ajv webapp / Drupal10 JSON:API'}},
[{'id':'JS-6-P1','origin':'researcher_constructed_from_source_unrun','input':{'type':'article','id':'1'},'expected':'C1=true,C2=true; accept; source trailing comma removed only in this named researcher fixture'},
 {'id':'JS-6-P2','origin':'researcher_constructed_unrun','input':{'type':'article','id':'2'},'expected':'C1=true,C2=true; accept; id value is not const1'},
 {'id':'JS-6-N1','origin':'researcher_near_negative_unrun','input':{'type':'article','id':1},'expected':'C1=true,C2=false; reject numeric id'},
 {'id':'JS-6-N2','origin':'researcher_near_negative_capability_probe_unrun','input':{'type':'article','id':'1'},'implementation_behavior':'rejects or renames the data property type as if it were a forbidden schema keyword','expected':'C1=false,C2=true; cannot claim complete'},
 {'id':'JS-6-G1','origin':'researcher_guard_probe_unrun','input':{},'expected':'do not invent required fields; original body does not specify absent-key result'}],
{'dynamic':['id string value','type value is data; allowed type-value set not specified'],'fields':['type property name and shown article value','id as string; description uuid is annotation text'],'unspecified':['Ajv version','JSON Schema dialect','JSON:API version','required keys','allowed resource types','UUID format assertion','exact app language beyond Ajv environment']},
['type 필드를 다른 이름으로 바꾸거나 제거해 문제를 우회하지 않는다(보존 추론).','id number를 string으로 강제변환하여 원문 type 검사를 대체하지 않는다.','uuid description을 실제 UUID format 제약이라고 발명하지 않는다.']),
req('LD-5','json-ld',1,
'Windows 로컬 파일의 JSON-LD를 읽어 Turtle로 내보낸다.',
'Turtle에서 context를 사용해 JSON-LD로 돌아오는 반대 방향도 같은 도구 흐름에서 지원한다.',
'Python 3.11 / Windows','RDFLib 6.3.2라고 요청자 명시','JSON-LD processingMode 및 Turtle 판 미명시; 1.1 표준은 용어 정의용',
'Windows 경로가 URL scheme c로 처리되어 실패한 trace를 보존한다. @id/@type, 언어 태그가 붙은 label/definitions를 보존할 필요가 있다. 원문 nested @context·@로 시작하는 prefix·angle-bracket IRI의 정확한 유효성은 별도 미확인; 일반 변환 기능만으로 그 원문 파일을 성공 처리했다고 하지 않는다.',
['converts JSON-LD to Turtle','from Turtle to JSON-LD','conversion circle'],
{'C1':{'origin':'explicit_prose_plus_code','locus':'p1,p3; pre1 Graph.parse/serialize'},'C2':{'origin':'explicit_prose','locus':'p1,p2; pre3 JSON-LD is previous conversion output'},'environment':{'origin':'explicit_prose','locus':'last p RDFLib6.3.2/Python3.11/Windows'}},
[{'id':'LD-5-P1','origin':'researcher_constructed_unrun','input_jsonld':{'@id':'https://example.org/item','https://example.org/name':{'@value':'A','@language':'en'}},'local_path':'C:\\af_res_060\\input.json','expected':'JSON-LD→Turtle triple and Turtle→JSON-LD language-tagged value preserved; graph-equivalent, no byte/ordering promise'},
 {'id':'LD-5-P2','origin':'researcher_constructed_unrun','input_turtle':'<https://example.org/item> <https://example.org/name> "A"@en, "B"@fr .','context':{'name':'https://example.org/name'},'expected':'Turtle→JSON-LD and reverse retain both language-tagged literals'},
 {'id':'LD-5-N1','origin':'researcher_near_negative_capability_probe_unrun','input':'valid local JSON-LD plus reverse-direction Turtle fixture','implementation_behavior':'JSON-LD→Turtle succeeds but Turtle→JSON-LD unsupported','expected':'C1=true,C2=false; partial'},
 {'id':'LD-5-N2','origin':'researcher_near_negative_environment_probe_unrun','input':'same valid JSON-LD at C:\\af_res_060\\input.json','implementation_behavior':'reverse conversion succeeds, local input parsed as URL scheme c and fails','expected':'C1=false,C2=true; reject complete claim'}],
{'dynamic':['file locations','context supplied by caller','RDF literals and language tags'],'fields':['@id','@type','skos:prefLabel@en','isDefinedAs values with en/fr/it/de tags'],'unspecified':['JSON-LD processingMode','desired whitespace/key order','numeric lexical round-trip','invalid-context repair','whether switching RDFLib version is acceptable']},
['서로 다른 엔진/판의 한 방향씩 성공을 합쳐 완결로 보지 않는다.','개념 IRI를 반드시 dereference해야 한다고 요구하지 않는다; 실제 remote @context loading과도 구별한다.','데이터의 literal/언어 태그 손실을 단순 성공으로 감추지 않는다.']),
req('LD-6','json-ld',3,
'R에서 HTML의 application/ld+json script 내용들을 추출한다.',
'복수 추출 결과를 trailing-garbage 오류 없이 JSON으로 읽어 가격·설명 등 원문에 있는 요청 필드의 값과 구조를 보존한다.',
'R; rvest/xml2/jsonlite/dplyr 코드 명시','각 package/R 판 미명시','JSON-LD processingMode 미명시; JSON-LD1.1 HTML 추출 정의는 번역용',
'원문은 price, lot area, description, location 등을 요청하지만 제시한 Product 부분에는 price와 description만 확인 가능하다. 없는 면적/위치를 생성하지 않는다. [1]/[2]/[3] excerpt와 JSON parser 오류는 저자 보고이며 실제 웹사이트를 재수집한 실행이 아니다.',
['extract some data','get data from <script type="application/ld+json">'],
{'C1':{'origin':'explicit_prose_plus_code','locus':'p1; pre1 html_nodes(...)/html_text()/fromJSON; pre2 error'},'C2':{'origin':'explicit_prose_plus_sample_fields','locus':'p1 price/lot area/description/location; pre3 Product/offers.price/description'},'environment':{'origin':'explicit_library_calls','locus':'pre1 library calls; later stringr attempt'}},
[{'id':'LD-6-P1','origin':'researcher_constructed_unrun','input_html':'<script type="application/ld+json">{"@context":"https://schema.org","@type":"Product","description":"Ångström plot","offers":{"price":950000,"priceCurrency":"SEK"}}</script>','expected':'one parsed object; offers.price remains number950000 and description Unicode preserved'},
 {'id':'LD-6-P2','origin':'researcher_constructed_unrun','input_html':'<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Site"}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"Product","description":"Ångström plot","offers":{"price":950000}}</script>','expected':'both JSON script contents handled separately/structured array, Product price/description retained'},
 {'id':'LD-6-N1','origin':'researcher_near_negative_capability_probe_unrun','input':'LD-6-P2 (two valid independent script bodies)','intermediate_output':['{"@context":"https://schema.org","@type":"WebSite","name":"Site"}','{"@context":"https://schema.org","@type":"Product","description":"Ångström plot","offers":{"price":950000}}'],'implementation_behavior':'both script texts extracted, but passed as concatenated JSON texts to one parser and rejected','expected':'C1=true,C2=false; actual parser execution not claimed'},
 {'id':'LD-6-N2','origin':'researcher_near_negative_capability_probe_unrun','input':'LD-6-P1','implementation_behavior':'script text extracted and parsed but output drops offers.price','expected':'C1=true,C2=false; field-loss counterexample'}],
{'dynamic':['different site script counts','listing price/description values','HTML content'],'fields':['offers.price','description','priceCurrency in shown sample','lot area/location only if actual source provides them'],'unspecified':['R/packages versions','schema.org version','exact area/location keys','output dataframe/list shape','malformed script policy']},
['원문에 없는 부동산 필드를 추측해서 채우지 않는다.','첫 script만 처리하는 기능을 복수 script 처리로 간주하지 않는다.','R 요구를 JavaScript API로 대체한 것을 완결로 보지 않는다.'])
]
# Keep this artifact in the requested Korean technical language.
requirements[0]['C1']='root usertype=employee이면 user 배열의 각 항목에 batchId를 요구한다.'
requirements[0]['C2']='각 항목의 firstName·lastName을 필수 문자열로 유지한다.'
preservation_origins=[
 {'usertype,batchId':'p1 explicit prose; pre2 expected failure; relation within user array is code context','firstName,lastName':'pre1 schema required/type and pre2 sample; source code requirement, not separate prose','user array':'pre1 schema/pre2 example; code-derived shape'},
 {'type':'last p explicit property-name request; pre1 example value article','id:string':'pre2 existing schema code; preservation inferred from code, not a separate prose request','description:uuid':'pre2 annotation text; no format validation request'},
 {'two conversion directions':'p1 explicit prose','context':'p2 explicit prose for Turtle→JSON-LD','@id,@type,prefLabel,language-tagged definitions':'pre3 sample-derived preservation guard; no separate prose assertion of byte-for-byte round-trip'},
 {'price,lot area,description,location':'p1 explicitly named requested data','offers.price,description':'pre3 actual code/output locations','priceCurrency':'pre3 sample-derived preservation guard, not separately requested in prose','lot area/location keys':'not shown in the Product excerpt; remain unspecified, do not invent'}
]
for r,origin in zip(requirements,preservation_origins):
    r['preserved_field_origins']=origin
save('requirements-new.json',requirements)

vocabfields=['mapping_id','case_id','raw_function_phrase','normalized','target_term','relation','direction','method','definition_uri','section','reason','phase']
assert next(csv.reader((ROOT.parent.parent/'vocabulary.csv').open()))==vocabfields
v=[]
def mapping(case,ident,raw,target,rel,method,url,section,reason):
    v.append(dict(mapping_id=f'{case}-{ident}',case_id=case,raw_function_phrase=raw,normalized=normalize(raw),target_term=target,relation=rel,direction='user_phrase -> standard_name' if method!='L,V' else 'original -> same normalized phrase',method=method,definition_uri=url,section=section,reason=reason,phase='post_stage2_pre_new_ranking'))
for r in requirements:
    for i,t in enumerate(r['L_terms'],1):
        mapping(r['case_id'],f'L{i}',t,t,'literal','L,V',r['revision_url'],'revision1; requirements-new condition_origins','원문 기능구; case/space/ASCII hyphen만 정규화. 제목의 나중 수정 문구는 쓰지 않음.')
val='https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01'
core='https://json-schema.org/draft-07/draft-handrews-json-schema-01'
api='https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/'
mapping('JS-5','V01','batchId to be required','required','definition_partial_atom','V',val+'#rfc.section.6.5.3','6.5.3','object의 지정 property 존재라는 원문의 C1 후건에만 대응. root→items 조건 연결 및 C2 지원은 별도 판정.')
mapping('JS-5','W01','if then else','dependencies','different_relation','withhold',val+'#rfc.section.6.5.7','6.5.7 vs6.6','property 존재 의존과 root 값에 따른 nested-item 조건은 같은 개념이 아님.')
mapping('JS-6','V01','validate the JSON','validation','definition_context','V',core+'#rfc.section.3.1','3.1','instance 제약 충족 여부를 검사하는 기능명. 056 JS-4와 같은 validate→validation 규칙. type 데이터속성/id:string/Ajv 환경은 그대로 남김; 지원 주장 아님.')
mapping('JS-6','V02','property named type','properties','definition_partial_atom','V',val+'#rfc.section.6.5.4','6.5.4','instance property 이름과 같은 properties map의 key에 subschema를 적용하는 정의. 구체 이름 type의 처리·id:string을 별도 확인하며 모든 property 기능을 완결로 승격하지 않음.')
mapping('JS-6','W01','property named type','type','different_role','withhold',val+'#rfc.section.6.1.1','6.1.1 vs6.5.4','schema keyword type은 instance primitive type 제약; 데이터의 type이라는 property 이름과 역할이 다르다.')
mapping('JS-6','W02','validate the JSON','Validator','derived_form','withhold',core+'#rfc.section.3.1','3.1','validation→Validator 어형 파생은 본표 매치 규칙 밖; 기존056 구별 유지.')
mapping('LD-5','V01','converts JSON-LD to Turtle','Deserialize JSON-LD to RDF','related_partial_pipeline_io_mismatch','withhold',api+'#deserialize-json-ld-to-rdf-algorithm','2.4;8.1','원문의 최종 출력 Turtle와 표준 중간 출력 RDF dataset은 다르다. Graph.parse가 중간 연산을 암시해도 전체 원문 기능구의 동의어 입증은 아님. 주표 보류; pipeline-expansion 감도에서만 사용 가능.')
mapping('LD-5','V02','from Turtle to JSON-LD','Serialize RDF as JSON-LD','related_partial_pipeline_io_mismatch','withhold',api+'#serialize-rdf-as-json-ld-algorithm','2.4;8.4','원문의 입력 Turtle text와 표준 입력 RDF dataset은 다르다. Turtle parser가 추가로 필요하며 전체 함수구와 I/O 동일성 미확보. 주표 보류; pipeline-expansion 감도에서만 사용 가능.')
mapping('LD-5','W01','conversion circle','flattening','different_operation','withhold',api+'#flattening','2.3 vs2.4','flattening은 JSON-LD 내부 node 배치 변환; JSON-LD↔Turtle 양방향과 동의 아님.')
mapping('LD-6','V01','get data from <script type="application/ld+json">','HTML script extraction','definition_context','V',api+'#html-content-algorithms','9.5-9.5.2','동일 media-type script에서 JSON-LD 내용 추출. 이 기능은 선택적이며 extractAllScripts 기본/옵션·R 지원·값보존은 별도 판정.')
mapping('LD-6','V02','extract some data','Extract Script Content','definition_partial_atom','V',api+'#extract-script-content','9.5.2','HTML script textContent→map/array 내부표현이라는 파싱 부분. HTML 선택 및 여러 scripts·목표필드 접근 전체를 증명하지 않음.')
mapping('LD-6','W01','extract some data','expansion','different_io_scope','withhold',api+'#expansion-algorithm','5.1','JSON-LD expansion은 term/IRI/value 정규화이며 HTML 추출 자체 아님. context 없는 항목 무시는 임의 필드 보존과도 다름.')
mapping('LD-6','W02','extract some data','framing','different_operation','withhold','https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/','056에서 고정 인수한 framing 경계; 이번 신규 직접열람 아님','framing은 linked graph를 frame형상으로 만드는 처리. HTML document script 추출 및 R JSON파싱과 동의 아님; 056 정의 재사용이며 새 출처로 세지 않음.')
with (ROOT/'vocabulary-new.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=vocabfields);w.writeheader();w.writerows(v)

std_notes={
'H-STD-CORE07':('JSON-Schema-core-draft07','2018-03-19 draft-handrews-json-schema-01','3.1 Validation;4.2 Instance;4.3.1 keywords','제약 충족 검사라는 validation 정의로 JS-6의 행위만 연결. 함수 확장/언어/실행 지원 증거는 아님.','H-SO-S02'),
'H-STD-VAL07':('JSON-Schema-validation-draft07','2018-03-19 draft-handrews-json-schema-validation-01','3.1-3.2;6.1.1;6.5.3-6.5.4;6.6;7.1-7.3','required는 object property 존재; properties는 동일 이름 child 적용; conditional은 subschema 경계 제한. 비선정03 FITS 사례도 읽었으나 format과 자동 등치하지 않음.','H-SO-S01;H-SO-S02;H-SO-S03'),
'H-STD-LDAPI11':('W3C-JSON-LD11-API','2020-07-16 Recommendation','2.4;3;8.1;8.4;8.6;9.5-9.5.2','양방향 RDF 알고리즘과 HTML script 추출/파싱의 입출력 확인. 추출은 선택, 기본 first-script와 extractAllScripts 구별. round-trip은 numeric lexical 손실 가능; 표준 API가 Windows/R 지원을 증명하지 않음.','H-SO-L01;H-SO-L03')}
for a in json.loads((ROOT/'standards-acquisition.json').read_text()):
    wid,edition,locus,note,opp=std_notes[a['source_id']]
    sources.append(dict(source_id=a['source_id'],work_id=wid,kind='official_standard',lineage={'new_vs_056':'existing work reread directly for new requirements','same_manual_sections_one_work':True},questions=['Q1','Q3','Q5','Q6'],case_ids=['JS-5','JS-6'] if '07' in a['source_id'] else ['LD-5','LD-6'],original_url=a['url'],fixed_url=a['url'],version={'edition':edition,'sha256':a['sha256']},opened_utc=a['acquisition_utc'],read_utc=NOW,locus=locus,checked=note,scope_and_limit='명시 절만 직접독해. 구현지원·설치시험·성공보고로 승격하지 않음. AF056 재사용 저작을 신규 고유저작 증가로 세지 않음.',evidence_type=['author_normative_definition','researcher_mapping_inference'],opposing_source_ids=opp.split(';'),access_status='opened_and_read',external_work_count_eligible=True,new_external_work=False))

# API documentation was directly opened with web tool; no answer payload was opened.
sources.append(dict(source_id='H-API-MANUAL',work_id='StackExchange-API-v2.3-manual',kind='official_acquisition_manual',lineage={'sections_one_work':True,'new_vs_056':'existing acquisition manual reread'},questions=['Q1','Q7'],case_ids=[],original_url='https://api.stackexchange.com/docs',fixed_url='https://api.stackexchange.com/docs/revisions-by-ids',version={'edition':'dynamic API2.3 docs; web retrieval, raw bytes not cached'},opened_utc=None,timestamp_precision='web tool 최초 열람의 정밀시각을 별도 기록하지 못함; read_utc는 실제 독해완료 원장 작성 시각. requests.jsonl은 API 실취득의 정확한 UTC를 보유.',read_utc=NOW,locus=['/docs/questions creation sort / tagged AND','/docs/revisions-by-ids','/docs/types/revision body/tags/title/revision_number'],checked='current-tag questions endpoint와 creation asc, revisions endpoint의 revision_number1/body·태그 사용을 확인. body/태그가 없을 가능성과 grace-period 수정 결합 한계를 보존.',scope_and_limit='API의 최초 revision은 작성자의 모든 keystroke나 작성 직후 수정 전 내용을 복원하지 않는다. API metadata100 수신 후 최초20만 노출; scoring/answer fields는 allowlist 제거.',evidence_type=['official_documentation','observed_acquisition_contract'],opposing_source_ids=['H-SO-L13'],access_status='opened_and_read',external_work_count_eligible=True,new_external_work=False))
with (ROOT/'sources.jsonl').open('w') as f:
    for s in sources:f.write(json.dumps(s,ensure_ascii=False)+'\n')
summary={'stage2_gate':gate,'generated_utc':NOW,'screened_frame_positions':40,'available_first_bodies':35,'read_first_bodies':35,'pool_exhausted_positions':5,'acquisition_failed_bodies':0,'selected_requirements':4,'selected':{r['case_id']:r['question_id'] for r in requirements},'eligible_by_tag':{t:sum(x.get('eligible')=='yes' for x in out if x['tag']==t) for t in ['jsonschema','json-ld']},'new_request_unique_works':len({r['body_work_id'] for r in index}),'new_selected_request_unique_works':4,'vocabulary_rows':len(v),'L_rows':sum(x['method']=='L,V' for x in v),'V_rows':sum(x['method']=='V' for x in v),'withhold_rows':sum(x['method']=='withhold' for x in v),'reviewer':'/root/authority, same model family separate context; own screen and self-check only','not_seen':['F1 files','new candidate rankings','answers','comments','Stack Overflow scores','accepted-answer status'],'known_prior_exposure':['AF056 original8 requirements and vocab/baseline for prior replay','SCOPE extraction rules, including pre-holdout clarification examples','Q7 authority research'],'limitation':'40 planned requests cannot all be read because current json-ld pool has15. All available35 read; no historical-tag restoration.'}
save('screening-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
