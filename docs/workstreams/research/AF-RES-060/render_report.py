"""Render the two required result tables and cards from the counted ledgers."""
from pathlib import Path
from collections import Counter
import csv,json,re,posixpath

P=Path(__file__).resolve().parent
def rc(f):return list(csv.DictReader((P/f).open(encoding='utf-8')))
def esc(v):return str(v).replace('|','\\|').replace('\n',' ')
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(esc(c) for c in r)+' |' for r in rows])+'\n'
reqs=json.loads((P/'requirements.json').read_text()); req={r['case_id']:r for r in reqs}
features={f['catalog_id']:f for f in rc('features.csv')}
matches=rc('matches.csv'); match={m['comparison_id']:m for m in matches}
changes=rc('changes.csv'); slots=rc('slots.csv'); paths=rc('paths.csv')
verdict={(v['case_id'],v['catalog_id']):v for v in json.loads((P/'evidence/candidate-verdicts.json').read_text())}
counts=json.loads((P/'evidence/comparison-summary.json').read_text())
sources=json.loads((P/'evidence/source-counts.json').read_text())
sens=json.loads((P/'evidence/sensitivity-summary.json').read_text())
labels={'complete':'완결','partial':'부분(조건부)','confirmed_wrong':'확정오답','unconfirmed':'미확인'}

short={
'JS-1':('가변 배열의 마지막 이전은 number','마지막 string은 선택 사항','언어·판 미명시'),
'JS-2':('schema 인스턴스의 root type=object','property schema type은 네 primitive만','draft-07; 언어 미명시'),
'JS-3':('외부 gender $ref 해소와 enum 적용','Person 필수 네 필드 보존','Node/TypeScript·Ajv; draft04/$id 혼용'),
'JS-4':('pii 이름은 현재 columns에 존재','column_datatype∈integer/string/object','Python3; 값 존재의 의미 미명시'),
'LD-1':('breadcrumb 순번·이름·계층 URL 보존','ld+json script를 head에 부착','JavaScript/JSP/JSTL'),
'LD-2':('AEM 입력이 있을 때만 FAQ script','여러 Question/Answer 값 보존','AEM/HTL; 제품판 미명시'),
'LD-3':('values에서 a=1 객체 선택','선택 객체 b/c와 나머지 credential 보존','jsonld.js; 판·processingMode 미명시'),
'LD-4':('ALGYO/ACSEL 항목 선택','종목과 26.14/22.9 가격 대응 보존','PHP; 판 미명시'),
'JS-5':('root employee이면 각 user에 batchId 요구','firstName/lastName 필수 문자열 유지','draft-07; 런타임 미명시'),
'JS-6':('데이터 속성 type=article 허용','기존 id:string 제약 유지','Ajv 판 미명시·Drupal10'),
'LD-5':('Windows 로컬 JSON-LD→Turtle','context를 쓰는 Turtle→JSON-LD','Python3.11/RDFLib6.3.2'),
'LD-6':('R에서 ld+json script 내용 추출','복수 본문 파싱·가격/설명 보존','rvest/xml2/jsonlite/dplyr 판 미명시')}

card_notes={
'JS-1':'optional은 객체 필드 추론으로 발견됐다. 가변 마지막 위치와 중간 string 거부를 같은 판에서 보이는 예가 필요하다.',
'JS-2':'meta-schema라는 정의 기반 질의에도 후보가 없다. schema-as-instance의 두 위치 제약을 보이는 구현·판이 필요하다.',
'JS-3':'SC-027의 $ref 및 SC-040의 인라인은 하위 기능 근거다. Ajv에서 외부 enum 적용과 Person required 보존이 연결된 예가 없다. draft04/$id와 email guard도 남는다.',
'JS-4':'동적 instance 이름 집합과 정적 enum을 나눠 확인해야 한다. 일반 validate/준수 주장 및 다른 런타임은 원 Python 요구의 공동 성공 근거가 아니다.',
'LD-1':'JSON-LD 표현 변환은 breadcrumb 유도와 DOM head 부착을 대신하지 않는다. 원 JSP/JS 입력과 생성·부착 코드가 필요하다.',
'LD-2':'framing을 AEM 존재 조건/HTL 반복 출력으로 확장하지 않는다. 빈 입력과 복수 Q/A의 실제 template 출력이 필요하다.',
'LD-3':'Ruby의 framing 이름은 발견했지만 원 jsonld.js에서 a=1 선택과 b/c·나머지 문서 보존은 미확인이다. 별도 경로의 성공 절을 합치지 않는다.',
'LD-4':'선택과 PHP 출력은 graph 재구조화의 동의어가 아니다. 두 종목/가격 경로의 원 환경 예가 필요하다.',
'JS-5':'required를 포함한 필드 추론명이 검색됐지만 root 값 조건과 nested item required의 공동 지원은 미확인이다. userType/usertype 혼용과 원 코드 오류를 먼저 구분한다.',
'JS-6':'Ajv README의 properties.bar.type=string 및 compile(schema)를 id로 이름만 바꾸는 조건부 보완이다. type라는 데이터 이름의 처리와 id 숫자 거부·데이터 불변성은 미실행이며, 원 Ajv판/Drupal 통합도 미확인이다.',
'LD-5':'표준 RDF dataset 입출력은 Turtle text parser/serializer 및 Windows 경로 처리를 포함하지 않는다. 원 RDFLib6.3.2의 로컬 파일과 양방향 fixture가 필요하다.',
'LD-6':'HTML script 추출과 복수 JSON 텍스트 파싱은 각각 확인해야 한다. 단일 JSON-LD expansion/framing 이름으로 R 처리 흐름을 대체하지 않는다.'}

def candidate_link(cid,original=False):
    f=features[cid];url=f['original_destination_url'] if original else f['editor_fixed_url']
    return '['+cid+' '+f['title']+']('+url+')'
def selected(c):return json.loads(match[c+'-V-F1']['top3_ids_json'])
def return_link(c):
    ids=selected(c)
    if c=='JS-6':return '조건부 보완: '+candidate_link('SC-005',True)+'; C2 이름 전이만'
    if ids:return '재질문·보류: '+', '.join(candidate_link(x,True) for x in ids)+'; 지원 확정 링크 아님'
    return '[원 요청]('+req[c]['url']+')으로 재질문·보류; 반환할 구현 없음'

first=[]
for r in reqs:
    c=r['case_id'];a,b,e=short[c]
    for f in ['F0','F1']:
        for q in ['L','V']:
            m=match[c+'-'+q+'-'+f];allm=json.loads(m['all_matches_json']);top=allm[:3]
            ss=[s for s in slots if s['comparison_id']==m['comparison_id'] and s['display_status']=='filled']
            cc=Counter(s['judgment'] for s in ss)
            ranking='전체 '+str(len(allm))+'개'+(' ['+', '.join(x['catalog_id'] for x in allm)+']' if allm else '')
            ranking+='; 상위 '+(', '.join(x['catalog_id']+'(원 '+str(x['posted_rank'])+')' for x in top) if top else '없음')
            evidence=[]
            for x in top:
                cid=x['catalog_id'];v=verdict[c,cid];ft=features[cid]
                p=next(z for z in paths if z['case_id']==c and z['catalog_id']==cid and z['path']==v['chosen_path_id'])
                url=p['first_document'] or ft['editor_fixed_url'];sha=ft['implementation_sha'][:10] or '판 미확인'
                text=cid+'@'+sha+' '+v['chosen_path_id']+' C1미확인/C2'+('조건부' if v['C2_status']=='supported_conditionally' else '미확인')
                evidence.append('['+text+']('+url+') · '+','.join(v['source_ids']))
            state='완결 '+str(cc['complete'])+' / 부분 '+str(cc['partial'])+' / 오답 '+str(cc['confirmed_wrong'])+' / 미확인 '+str(cc['unconfirmed'])
            state+='; 검토 후보 '+str(len(ss))+'개, 진위확정 0개 → 정확도 산출 불가'
            empty=(('관측 무매치: 3슬롯' if not allm else '풀 소진: '+str(3-len(top))+'슬롯') if len(top)<3 else '빈 슬롯 0')
            first.append([c+' · '+('기존(튜닝)' if r['layer']=='existing_tuning' else '새 층'), 'C1 '+a+'; C2 '+b+'; '+e,q+' × '+f,ranking,'<br>'.join(evidence) if evidence else '해당 없음: 후보 분모 0',state,empty])

second=[]
def delta_text(d):
    return '풀 +'+str(len(d['all_new']))+'/-'+str(len(d['all_removed']))+'; 상위 +'+(','.join(d['top3_new']) or '0')+'/-'+(','.join(d['top3_removed']) or '0')
for ch in changes:
    c=ch['case_id'];ds={k:json.loads(ch[k+'_json']) for k in ['field_L','field_V','query_F0','query_F1']}
    jd=json.loads(ch['judgment_deltas_json']);jtexts=[]
    for ax in ds:
        new=jd[ax]['new_top3'];old=jd[ax]['removed_top3']
        jtexts.append(ax+': +'+','.join(labels[k]+str(v) for k,v in new.items()) if new else ax+': +0')
        jtexts[-1]+=' / -'+(','.join(labels[k]+str(v) for k,v in old.items()) or '0')
    both=json.loads(ch['both_required_candidates_json'])
    second.append([c+' · '+('기존' if ch['layer']=='existing_tuning' else '새 층'), 'L고정 '+delta_text(ds['field_L'])+'<br>V고정 '+delta_text(ds['field_V']), 'F0고정 '+delta_text(ds['query_F0'])+'<br>F1고정 '+delta_text(ds['query_F1']), ', '.join(both) or '관측 0', '<br>'.join(jtexts)+'; 모든 축 완결·확정오답 신규/탈락 0', '공통 E62: 62행·본문72요청·논리30,943단어; 요구별 재청구 없음',return_link(c),card_notes[c]])

text='# AF-RES-060 결과\n\n## 1. 고정 48비교: 같은 경로의 두 조건\n\n'
text+=table(['요구·기존/새 층','C1·C2·환경','L/V × F0/F1','전체 매치·상위 3개 원순번','같은 경로에서 확인한 구현·판·근거 주소','완결·부분·오답·미확인','빈 슬롯 사유'],first)
text+='\n## 2. 12요구의 네 조건 차이와 반환 판단\n\n'
text+=table(['요구','필드만 바꾼 차이','질의만 바꾼 차이','두 변경이 함께 필요했던 후보','완결/부분/오답의 신규·탈락','편집 원문·읽기 비용','반환할 링크와 조건','미확인·다음 확인'],second)
discussion=(P/'evidence/result-discussion.md').read_text()
# The reusable discussion source lives under evidence; RESULT lives one level above.
def root_link(m):
    url=m.group(2)
    if re.match(r'^[a-z]+:',url) or url.startswith('#'):return m.group(0)
    return m.group(1)+posixpath.normpath('evidence/'+url)+m.group(3)
discussion=re.sub(r'(\]\()([^\n)]+)(\))',root_link,discussion)
text+='\n'+discussion
text=text.replace('{{SOURCE_EVENTS}}',str(sources['source_events'])).replace('{{SOURCE_WORKS}}',str(sources['distinct_qualifying_works'])).replace('{{NEW_WORKS}}',str(sources['distinct_new_works'])).replace('{{QUAL_SOURCE_EVENTS}}',str(sources['qualifying_direct_source_events']))
(P/'RESULT.md').write_text(text)

cards=['# AF-RES-060 반환 카드','', '반환 등급은 전체 구현 0 / 조건부 보완 1 / 재질문·보류 11이다. 조건부 보완도 원 요청의 성공 보증이 아니다. 아래 구현 링크는 F0 원게시 URL이며 편집용 고정판 URL을 새 클릭 지름길로 제공하지 않는다. 증거 판·경로는 paths.csv와 RESULT 첫 표에서 감사한다.','']
for r in reqs:
    c=r['case_id'];a,b,e=short[c]
    cards += ['## '+c+' — '+('조건부 보완' if c=='JS-6' else '재질문·보류'),'',return_link(c),'','보존할 요구: C1 '+a+'; C2 '+b+'; 환경 '+e+'.','',card_notes[c],'','원 요청: ['+str(r['question_id'])+']('+r['url']+'). 원문 위치·prose/code 구분·양성/근접음성은 requirements.json의 '+c+'.','']
cards += ['## 사용·중단 조건','', '한 경로·같은 구현판에서 C1/C2와 환경·guard가 직접 확인되면 전체 구현으로 올릴 수 있다. 지금은 그러한 후보가 없다. JS-6의 이름 매개변수 전이를 허용하지 않는 사용처에서는 조건부 카드도 보류한다. 기능명만 보고 설치·런타임 교체·데이터 변형을 승인하지 않는다. 후속 명령은 evidence/next-checks/README.md에 있으며 모두 미실행 계획으로 표시했다.','']
(P/'cards.md').write_text('\n'.join(cards))
print(json.dumps({'first_table_rows':len(first),'second_table_rows':len(second),'cards':len(reqs),'result_bytes':(P/'RESULT.md').stat().st_size}))
