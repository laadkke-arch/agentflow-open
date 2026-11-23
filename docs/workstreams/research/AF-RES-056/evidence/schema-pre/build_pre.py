"""Build compact audit ledgers from public API receipts. No candidate data read."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, html, json, re

P = Path(__file__).resolve().parent
meta = json.loads((P / 'metadata.json').read_text())
revisions = json.loads((P / 'revisions-p1.json').read_text())
now = datetime.now(timezone.utc).isoformat()

def dump(name, obj):
    (P / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def writecsv(name, rows):
    with (P / name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def textbody(s):
    return html.unescape(re.sub('<[^>]+>', '\n', s))

def norm(s):
    return re.sub(r'\s+', ' ', s.casefold().replace('-', ' ')).strip()

# These decisions are written before candidate ranks or provider pages are read.
decisions = {
1:('exclude','폴더에서 복수 schema를 참조하는 방식 질문. optional의 대상/허용·거절 출력이 불명확하여 별도 필수조건 둘을 고정할 수 없다.'),
2:('exclude_domain','국가별 dropdown 표시와 flat 제출 형태가 목적. JSON Schema 검증/주석 처리 자체의 두 조건으로 바꾸지 않는다.'),
3:('exclude_joint_requirement','서로 다른 validator의 가설적 동작을 묻는 호환성 해석. 동일 환경에서 함께 원하는 두 조건이 아니라 상반된 두 환경 예상이다.'),
4:('exclude_domain','Schema→Pydantic 클래스 생성; 지정한 유효성 검사·주석 처리 범위 밖.'),
5:('selected','가변 길이 숫자 배열과 마지막에만 가능한 선택적 문자열을 별도 판정할 수 있다.'),
6:('exclude_purpose','같은 개념의 schema와 형식 수를 묻는 용어 질문; 작동 요구가 아니다.'),
7:('selected','schema 자체 검증에서 root object와 property schema primitive 제한이 명시됨.'),
8:('selected','외부 schema 참조 해결과 Person의 enum/필수 속성 검증이 코드에 명시됨; 두 조건은 code-derived.'),
9:('selected','동적 columns와 pii의 관계, metadata의 값 존재/타입 제한을 명시함. 추가 enum 조건을 누락하지 않고 C2 내 검사로 보존.'),
10:('eligible_after_quota','추가 속성 오류와 a/b 타입 오류를 함께 반환해야 한다는 명시 요구; 첫4 이후.'),
11:('after_quota','생성 schema에서 추가 키 거부; class 생성 맥락과 조건 독립성 경계.'),
12:('eligible_after_quota','draft06 schema의 내부/외부 reference와 합성 person/member 검증; 첫4 이후.'),
13:('eligible_after_quota','YAML→JSON 검증 파이프라인 유지 및 오류 위치 line/column; 첫4 이후.'),
14:('eligible_after_quota','root 필수 속성을 유지하며 배열 각 항목 title을 요구; 첫4 이후.'),
15:('eligible_after_quota','action에 따라 from의 주소/그룹 판정 달라짐; format ip-address와 draft07 표준명 구별 필요.'),
16:('exclude_domain','Angular dropdown titleMap의 동적 필터 UI; 검증/주석 목적 아님.'),
17:('eligible_after_quota','draft04 제약 재사용과 field별 description 유지의 주석 목적; 첫4 이후.'),
18:('exclude_domain','Java class→array schema 생성; validation 목적의 독립 조건 둘 아님.'),
19:('after_quota','단일 if 관계의 C# 작성 syntax; 최초판 본문은 이미지 외 두 조건을 독립화하기 어려움.'),
20:('after_quota','재사용 enum 참조 syntax. desired 값 제한은 코드에 있으나 이후 질문이라 선정하지 않음.'),
21:('eligible_after_quota','bar의 값으로 다른 object key를 찾아 존재/제약 확인; 첫4 이후.'),
22:('eligible_after_quota','bark/meow에 따른 tail enum 분기 및 두 입력 허용; 첫4 이후.'),
23:('exclude_domain','JSON.parse syntax error와 큰 파일 파싱 문의; schema validation 조건 둘 아님.'),
24:('eligible_after_quota','두 nested 값 conjunction일 때 Sector required; 첫4 이후.'),
25:('eligible_after_quota','head string과 가변 tail boolean/integer; 첫4 이후. number/integer 원문 불일치 존재.'),
26:('exclude_domain','patternProperties→TypeScript 인터페이스 대응; code generation.'),
27:('exclude_purpose','여러 프로젝트 schema 관리/배포 전략; 구체 두 작동 조건의 입력·출력 부족.'),
28:('exclude_domain','form 크기와 버튼 잘림 CSS/시각 문제. 이후 rev3 본문이 API 진단 출력에 먼저 노출되었음을 기록.'),
29:('exclude_domain','JSON→POJO 및 클래스 생성 개념; schema validation 아님.'),
30:('exclude_domain','Kafka message schema envelope 제거 설정; JSON Schema 표준의 검증/주석 아님.'),
31:('eligible_after_quota','빈 HTTP body와 빈 object를 구별해 거부; transport 입력과 schema instance 구분 필요.'),
32:('after_quota','두 boolean의 적어도 하나 true라는 한 predicate. 문장 두 개를 독립 조건 둘로 세지 않음.'),
33:('eligible_after_quota','임의 key object에서 특정 value 존재; 키 목록을 미리 고정하지 않는 요구.'),
34:('after_quota','Confluent serializer/schema-registry 통합 문제; 최초 tags에는 jsonschema 없음.'),
35:('eligible_after_quota','두 sibling의 임의 property names가 겹치면 거부/분리면 허용; 첫4 이후.'),
36:('eligible_after_quota','radius/diameter 선택과 둘 다 없을 때 default 삽입; annotation와 mutation 구별용 사후 반례 후보, 주표 대체 금지.'),
37:('exclude_domain','fluent schema response serialization 빌드 설정; validation·annotation 범위와 다름.'),
38:('eligible_after_quota','중복 schema 재사용과 context별 nullable 차이; 첫4 이후.'),
39:('exclude_domain','React UI groups 내 경로 전달 syntax; 작동 조건 두 개 부족.'),
40:('exclude_domain','JSchema ToString 출력 공백 축약; instance validation/annotation 아님.')}

reqs=[
 {'case_id':'JS-1','screen_rank':5,'question_id':65660787,'input':'길이를 고정하지 않은 JSON array','c1':'모든 마지막 이전 요소는 number이며 중간 string은 거부한다.','c2':'마지막 string은 허용하지만 필수는 아니다: 전부 number인 배열도 허용한다.','source_location':'revision1 본문 array schema·허용 [3,4,5,"hello"]·거부 [3,"hello",4,5] 및 마지막 설명','language':'명시 없음','product_version':'명시 없음','draft':'명시 없음; draft07은 정의 비교용이며 요청판으로 가정하지 않음','product_exposure':'없음','replaceability':'특정 구현 고정 없음','extra_constraints':'가변 n; 빈 배열의 기대는 명시되지 않음','l_terms':['list of numbers','last element','optional'],'quotes':{'c1':'text is only allowed on the last element','c2':'the string can be optional'},'interpretation':'순서에 의존하는 한 predicate를 position restriction과 optionality 두 독립 검사로 분리. fixed tuple·string anywhere는 근접 오답.'},
 {'case_id':'JS-2','screen_rank':7,'question_id':65699699,'input':'검증 대상인 draft07 JSON Schema 문서','c1':'검증 대상 schema의 root type은 object이다.','c2':'그 properties 내 각 property schema의 type 값은 string/number/integer/boolean만 허용한다.','source_location':'revision1 첫 요구 문단과 sample JSON; simpleTypes enum 수정의 실패 설명','language':'명시 없음','product_version':'명시 없음','draft':'원문 $schema draft-07','product_exposure':'jsonschema.net 및 ajv의 draft07 meta-schema URL; 본문에만 노출, 목적지 미열람','replaceability':'특정 엔진 필수라고 명시되지 않음','extra_constraints':'null/array/object를 property type에 허용하지 않음; arbitrary latest draft를 추가하지 않음','l_terms':['validate JSON Schema','primitive type'],'quotes':{'c1':'root of JSON schema should have type as object','c2':'property can only be of primitive type'},'interpretation':'메타 검증의 두 위치별 enum 제약. 일반 인스턴스 검증만 보여주는 문서는 완결 아님.'},
 {'case_id':'JS-3','screen_rank':8,'question_id':65726164,'input':'types.json과 definitions.json, Node/TypeScript Person instance','c1':'person.sex가 참조하는 외부 types.json#/properties/gender를 같은 검증 체인에서 해결하고 enum 제약을 적용한다.','c2':'Person의 name/surname/sex/email 필수 속성을 유지하여 example Person 검증을 수행한다.','source_location':'revision1 types.json properties.gender $ref 및 definitions.person.sex/$ref·required, isPerson(riccardo) 호출','language':'Node.js / TypeScript','product_version':'Ajv 판 명시 없음','draft':'두 문서가 draft-04를 선언하지만 $id/JSONSchemaType 사용; 불일치 자체 보존','product_exposure':'Ajv, ajv validation docs URL; 코드 기반 사례','replaceability':'Ajv 사용을 직접 묻는다. 다른 엔진은 대안 진단이며 원요구 완결과 분리','extra_constraints':'email format도 source schema에 있음. 형식 assertion 통과는 별도 미확인 guard; literal draft04/$id 혼용을 자동교정하지 않음','l_terms':['dependent json-schemas','$ref'],'quotes':{'c1':'one dependent on the other','c2':'required'},'interpretation':'C1/C2 둘 다 source code-derived, 오류 메시지 해결을 두 개로 중복계수하지 않음. email 및 dialect guard를 확인하지 못하면 전체 요구 완결 승격 금지.'},
 {'case_id':'JS-4','screen_rank':9,'question_id':65731152,'input':'각 문서마다 이름·수가 달라지는 columns object와 pii array','c1':'pii의 값은 해당 instance columns에 실제 존재하는 column 이름으로만 제한한다.','c2':'column_datatype 값을 integer/string/object 중 하나로 제한한다.','source_location':'revision1 첫 3개 요구 문단 및 columns/pii example','language':'Python 3.x','product_version':'python-jsonschema 판 명시 없음','draft':'명시 없음','product_exposure':'jsonschema import/validate; 현재 설치판 미확인','replaceability':'Python jsonschema 사용 예제이지만 대안 금지는 명시하지 않음','extra_constraints':'이름·description·datatype에 값이 있어야 한다는 추가 문의를 보존한다. 빈 문자열/null/공백 기준은 미명시이므로 minLength1로 자동번역하지 않는다. 전체 요구를 반환하려면 이 guard도 별도 확인해야 한다.','l_terms':['schema check','validate','restrict column data type'],'quotes':{'c1':'The columns names and number of columns are dynamic','c2':'restrict column data type'},'interpretation':'정해진 enum과 동적 다른 instance 값 참조를 혼동하지 않음. 핵심 두 조건 이외의 값 존재 의미가 모호하므로 두조건 완결과 전체질문 해결을 별도 표시한다.'}
]
by_rank={r['screen_rank']:r for r in reqs}
rows=[]; sources=[]; revision_audit=[]
for rank,q in enumerate(meta['items'],1):
    rs=[x for x in revisions['items'] if x['post_id']==q['question_id'] and x.get('body')]
    rv=min(rs,key=lambda x:(x.get('revision_number',99999),x['creation_date']))
    assert rv.get('revision_number')==1
    rq=by_rank.get(rank,{})
    bodyhash=hashlib.sha256(rv['body'].encode()).hexdigest()
    rq.update({'original_revision_guid':rv['revision_guid'],'original_body_sha256':bodyhash,'url':q['link'],'created_utc':datetime.fromtimestamp(q['creation_date'],timezone.utc).isoformat()}) if rq else None
    state,reason=decisions[rank]
    sid=f'SCH-Q{rank:02d}'
    rows.append({'frame_id':f'JS-F{rank:02d}','domain':'JSON Schema','screen_rank':rank,'question_id':q['question_id'],'creation_utc':datetime.fromtimestamp(q['creation_date'],timezone.utc).isoformat(),'question_url':q['link'],'original_title':html.unescape(rv.get('title',q['title'])),'current_title':html.unescape(q['title']),'original_revision':1,'revision_guid':rv['revision_guid'],'original_body_sha256':bodyhash,'original_tags_json':json.dumps(rv.get('tags',[])),'current_tags_json':json.dumps(q['tags']),'original_domain_tag_present':'jsonschema' in rv.get('tags',[]),'status':state,'case_id':rq.get('case_id',''),'reason':reason,'product_exposure':rq.get('product_exposure','미선정; title/body의 tool 노출은 선정 점수로 쓰지 않음'),'answer_comment_vote_used':False,'source_id':sid})
    sources.append({'source_id':sid,'work_id':f'so-question-{q["question_id"]}','자료종류':'사용자 질문' if rq else '모집 질문','원본_URL':q['link'],'최종_URL':revisions['final_url'],'발행자':'Stack Overflow question author via Stack Exchange official API','확인_UTC':revisions['checked_at_utc'],'판_또는_SHA':f'revision1 {rv["revision_guid"]}; body-sha256:{bodyhash}','쪽_절_행_셀':rq.get('source_location','최초 본문 전체; metadata rank '+str(rank)),'관련_Q와_사례_ID':'Q1;'+rq.get('case_id',f'JS-F{rank:02d}'),'확인한_내용':reason if not rq else rq['c1']+' '+rq['c2'],'확인범위와_한계':'최초 개정 본문을 API로 직접 열람. 답/댓글/추천은 읽지 않음. 현재 public tagged cohort이며 삭제/retagging 이전 모집 전체 미복원.'+(' r28의 후속rev3은 진단 출력에서 먼저 노출됨; 원판 선정에는 사용하지 않음.' if rank==28 else ''),'지지_또는_반증':'모집·요구 확인','직접열람_상태':'직접 열람','중복_계보':'질문 현재판/개정판은 같은 work_id. API 배치응답 자체를 추가 저작으로 세지 않음.','quota_bucket':'questions' if rq else 'additional_screening','reader':'root'})
    revision_audit.append({'question_id':q['question_id'],'body_revision_number':1,'revision_guid':rv['revision_guid'],'original_body_sha256':bodyhash,'original_title':html.unescape(rv.get('title',q['title'])),'original_tags':rv.get('tags',[]),'revision_metadata':[{'revision_number':x.get('revision_number'),'creation_date':x['creation_date'],'revision_guid':x['revision_guid'],'tags':x.get('tags')} for x in revisions['items'] if x['post_id']==q['question_id']]})

C07='https://json-schema.org/draft-07/draft-handrews-json-schema-01'
V07='https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01'
C04='https://json-schema.org/draft-04/json-schema-core'
V20='https://json-schema.org/draft/2020-12/json-schema-validation'
v=[]
def vocab(case,raw,target,relation,allowed,uri,section,reason,condition):
    v.append({'mapping_id':f'JS-V{len(v)+1:02d}','case_id':case,'raw_function_phrase':raw,'normalized':norm(raw),'target_term':target,'target_normalized':norm(target),'relation':relation,'direction':'user_phrase -> standard_name','allowed_V':allowed,'definition_uri':uri,'section':section,'condition_preserved':condition,'reason':reason,'phase':'before_catalog_ranking','reader':'root'})
vocab('JS-1','list of numbers','items','broader_related',False,V07+'#rfc.section.6.4.1','6.4.1','items의 schema/고정 tuple 정의만으로 가변 마지막 위치 제약을 보존할 수 없다.','C1+C2')
vocab('JS-1','last element','contains','broader',False,V07+'#rfc.section.6.4.6','6.4.6','contains는 어느 위치 하나라도 만족; 마지막만 허용과 다르다.','C1')
vocab('JS-1','optional','default','different_behavior',False,V07+'#rfc.section.10.2','10.2','선택적 문자열은 값 삽입 요청이 아니다. default는 부재 허용/마지막 배치와 동의가 아니다.','C2')
vocab('JS-2','validate JSON Schema','meta-schema','definition',True,C07+'#rfc.section.4.3.2','4.3.2','schema를 기술하고 검증하는 schema의 명시적 정의. root/property 제약은 판정에 그대로 남김.','C1+C2; draft07')
vocab('JS-2','primitive type','type','related',False,V07+'#rfc.section.6.1.1','6.1.1','표준 type에는 array/null/object도 포함; 원문의 허용4개를 넓힌다.','C2')
vocab('JS-3','dependent json-schemas','schema references','definition_context',True,C04+'#rfc.section.7.1','7.1','원본문 $ref 코드가 schema 간 URI reference임을 확정; property dependencies와 구분한다.','C1; draft04 literal; Node/Ajv')
vocab('JS-3','$ref','dereferencing','definition_context',True,C04+'#rfc.section.7.2.3','7.2.3','문서가 URI를 해석해 참조 schema를 사용하는 처리로 정의; 수집/다운로드 일반 기능으로 확대하지 않음.','C1; canonical/inline 차이 보존')
vocab('JS-3','dependent json-schemas','dependencies','different_relation',False,V07+'#rfc.section.6.5.7','6.5.7','properties의 조건 의존과 외부 schema $ref 관계는 다르다.','C1')
vocab('JS-4','schema check','validation','definition',True,C07+'#rfc.section.3.1','3.1','표준은 validation을 instance가 주어진 제약을 충족하는지 checking으로 정의. 후보 생성용 일반 행위에만 대응하며 C1/C2 지원을 주장하지 않음.','C1+C2; Python constraints retained')
vocab('JS-4','validate','validation','definition',True,C07+'#rfc.section.3.1','3.1','같은 표준 절의 행위/기능명 대응. L은 어형변화를 하지 않으며 V에서만 추가.','C1+C2')
vocab('JS-4','restrict column data type','enum','definition_partial_atom',True,V07+'#rfc.section.6.1.2','6.1.2','명시한 세 문자열 중 하나와 같아야 하는 C2에만 enum 정의가 대응. 동적 C1로 확대하지 않음.','C2 only; C1 and value-presence guard remain')
vocab('JS-4','schema check','dependentRequired','different_relation',False,V20+'#section-6.5.4','6.5.4','정해진 property-name 의존은 다른 instance의 동적 키 목록 참조와 같지 않음.','C1')

writecsv('frame.csv',rows); writecsv('vocabulary.csv',v);dump('requirements.json',reqs);dump('revision-audit.json',revision_audit)
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
dump('pre-freeze-receipt.json',{'created_at_utc':now,'metadata_sha256':hashlib.sha256((P/'metadata.json').read_bytes()).hexdigest(),'revisions_response_sha256':revisions['response_sha256'],'first40_count':len(rows),'first_original_body_count':sum(x['original_revision']==1 for x in rows),'selected_ranks':[5,7,8,9],'selected_ids':[x['question_id'] for x in reqs],'candidate_data_read':False,'standard_names_fixed':True,'no_provider_destinations_read':True,'warning':'This is an analyst audit and definition mapping, not external ground truth. Preserve ambiguity in JS-3/C2 and JS-4/C2.'})
print(json.dumps({'selected':[x['case_id']+':'+str(x['question_id']) for x in reqs],'frame':len(rows),'vocabulary':len(v),'allowed':sum(x['allowed_V'] for x in v)},ensure_ascii=False))
