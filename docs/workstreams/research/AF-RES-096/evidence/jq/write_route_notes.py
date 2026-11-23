import collections, datetime, json, pathlib
P=pathlib.Path(__file__).resolve().parents[2]
plan={r['label']:r for r in json.loads((P/'corpus-plan.json').read_text())['repositories']}
notes={
'JQ-0001':('공식 매뉴얼', 'raw input/output, 배열순회와 lexical binding, 객체/문자열 더하기, range, select, 누락키 null, match offset/global, 문자열 slice, foreach/limit 상태형 filter의 명세와 예제를 직접 확인했다. J1/J3의 구체 filter 및 J4 괄호깊이 filter의 구성 근거; J2 offset값은 자료에서 생성할 수 없다.', '같은 거대 단일매뉴얼이 여러 요구의 모든 연산을 포함한다. 정확한 J4 filter 원 시험이나 사용자판 실행결과는 아니다.', ['Q3','Q4','Q5'], 'main_manual_implementation', True),
'JQ-0016':('배포판에 포함된 IBM decNumber 구현', '파일 시작의 decimal arithmetic 라이브러리 설명과 저작·라이선스를 확인했다. J1의 one/two/array 등 어휘가 유사해 상위 노출됐으나 부모-자식 JSON 묶기와 연결되지 않았다.', 'jq 프로젝트 고유 구현이 아닌 포함된 외부 저작물이다. 수치연산 correctness를 조사하지 않았다. 자료 하한에서는 보수적으로 제외한다.', ['Q3','Q4'], 'vendored_implementation_excluded', False),
'JQ-0080':('상류 원 시험과 기대출력', 'object constructor/array 및 lexical binding fixture의 입력·기대출력을 확인했다. range/인덱싱, 객체 merge와 문자열 concat fixture는 J3의 조합에 지지를 준다.', 'J1/J2/J3의 실제 질문 입력 전체를 그대로 시험한 기록은 아니다. 서로 다른 절을 별개 독립 자료로 세지 않는다.', ['Q4','Q5'], 'upstream_original_test', True),
'JQ-0072':('공식 생성 parser 구현', '문자열 interpolation, EACH iterator, object key-value pair grammar reduction을 확인했다. 문법 구현은 manual 조합을 뒤집는 반례를 주지 않았다.', '생성 parser를 읽은 것으로 end-to-end 해법·runtime 실행성공을 주장하지 않는다. 반환 링크 2개에는 사용하지 않았다.', ['Q3','Q4','Q5'], 'main_manual_implementation', True),
'JQ-0117':('상류 shell 원 시험과 기대출력', 'raw input의 줄/stream 처리와 rawfile/slurpfile 문자열/JSON 로딩 기대출력 및 비교명령을 확인했다.', '정확한 질문별 bracket/title extraction filter의 원 시험이 아니다. 조건 판정에 반환되지 않은 경로에서는 보조 관찰로만 남겼다.', ['Q4','Q5'], 'upstream_original_test', True),
'JQ-0004':('공식 jq builtin 구현', 'range/3가 시작·끝·증분과 재귀적 상태 갱신으로 값을 내는 구현을 확인했다. J3의 2개씩 증가하는 위치순회에 부합한다.', '입력 객체의 위치 교대 전제를 확인하지 못한다. J3 최종 반환은 manual+test라 이 파일을 별도 판정근거로 끌어오지 않았다.', ['Q4','Q5'], 'main_manual_implementation', True),
'JQ-0002':('공식 C builtin 구현', '+의 타입별 문자열/배열/객체 동작과 match가 문자열을 받으며 g flag를 해석하는 구현을 확인했다. UTF8 Oniguruma PerlNG를 사용하며 Oniguruma 없는 빌드에서 match 계열은 지원하지 않는 반대조건도 확인했다.', '사용자 설치판·빌드가 밝혀지지 않아 그 환경에서 실행됨을 주장할 수 없다. 코드 열람과 실제 실행은 별개이다.', ['Q4','Q5'], 'main_manual_implementation', True),
'JQ-0055':('공식 JSON parser 구현', 'JSON literal/number 처리에서 유효하지 않은 literal을 거절하는 분기를 확인했다. 비JSON 로그는 기본 JSON 파싱 대신 raw-input 경계가 필요하다는 설명에 부합한다.', '원 로그 처리 전체를 이 파일이 해결하지 않는다. J4-A 반환 두 링크에는 포함되지 않았고 manual의 raw-input을 직접 근거로 사용했다.', ['Q3','Q4','Q5'], 'main_manual_implementation', True),
'CU-0001':('공식 coreutils 매뉴얼', 'cat이 입력 파일을 표준출력으로 복사하는 계약과 binary/text mode 유의사항을 확인했다. J2의 cat sample.json → jq 경계에는 정상 전달 근거이나 없는 offset을 생성하지 않는다.', '사용자의 cat 구현/OS/옵션이 미확인이다. GNU 9.5 비교판 근거이며 질문자가 GNU판을 사용했다는 증거는 아니다.', ['Q4','Q5'], 'adjacent_manual_implementation', True),
'CU-0002':('공식 cat 구현', 'simple_cat에서 read와 write를 반복하는 단순복사 및 특별 옵션이 없을 때의 분기를 확인했다.', 'file bytes가 완전한 JSON인지·원 offset이 있는지는 확인하지 않는다. J2-B 최종 두 링크에서는 제외했다.', ['Q3','Q4','Q5'], 'adjacent_manual_implementation', True),
'OP-1322':('공식 Overpass 구현', 'make_area의 from/into/pivot 속성, 좌표·영역 생성, 객체/태그와 결과 저장 경계를 읽었다. 검색토큰 pair/range/indices와 관련된 어휘는 JSON 배열의 연속객체 merge와 다른 작업이었다.', '선정된 파일은 요청의 두 JSON 객체를 합치는 근거를 제공하지 않았다. Overpass에 그런 기능이 전혀 없다는 일반적 부정 결론은 내리지 않는다.', ['Q3','Q4','Q5'], 'adjacent_manual_implementation', True),
'OP-1142':('공식 Overpass 구현', '좌표·공간 인덱스 계산과 bounding box/range 변환을 확인했다. 위치순 JSON 배열 merge에 대한 문서나 기대출력은 아니다.', '이 파일의 비관련성은 전체 Overpass 프로젝트의 기능 부재를 뜻하지 않는다. J3는 jq-only 조건이므로 생산자 재작성도 완결 대안이 아니다.', ['Q3','Q4','Q5'], 'adjacent_manual_implementation', True),
'GR-0005':('공식 grep 구현', 'prline의 출력 분기에서 matching 전체 줄을 쓰는 기본 흐름을 확인했다. grep은 파이프라인의 문자열 줄 경계를 보존한다.', '선택·색상·출력옵션 전 조합을 검증한 것은 아니다. J4-B 반환두링크에서는 별도 사용하지 않는다.', ['Q4','Q5'], 'adjacent_manual_implementation', True),
'GR-0001':('공식 grep 매뉴얼 원문', '기본 matching line 출력과 stdin, -o의 matched nonempty part 출력, PCRE 선택 관련 설명을 확인했다. -o 자체가 균형괄호 처리 의미를 제공한다고 읽지 않았다.', '이 문서의 PCRE 언급만으로 외부 PCRE recursion syntax/지원여부를 확인했다고 주장할 수 없다. GNU 3.11은 사용자판이 아닌 비교판이다.', ['Q4','Q5'], 'adjacent_manual_implementation', True),
}
all_events=[]
exposures={}
for case,rs in [('J1','AB'),('J2','BA'),('J3','AB'),('J4','BA')]:
 for r in rs:
  q=P/f'evidence/routes/{case}-{r}'
  all_events.extend(json.loads(s) for s in (q/'access.jsonl').read_text().splitlines())
  for x in json.loads((q/'exposure.json').read_text())['slots']:
   if not x.get('empty'): exposures[x['file_id']]=x
body=[e for e in all_events if e['event']=='body_attempt' and e['status']=='success']
records=[]
for fid in sorted({e['file_id'] for e in body}):
 own=[e for e in body if e['file_id']==fid]
 own.sort(key=lambda e:e['started_utc']); first=own[0]
 nav=[e for e in all_events if e['event']=='section_navigation' and e['file_id']==fid]
 x=exposures[fid]; repo=plan[fid.split('-')[0]]
 typ,content,limits,qs,cat,eligible=notes[fid]
 records.append({
  'source_id':fid, 'source_type':typ, 'original_url':x['url'], 'reread_url':x['url'],
  'published_utc':repo['published_utc'], 'publication_precision':'release/commit time; individual file authorship dates not separately established',
  'checked_utc':first['started_utc'], 'version':repo['version'], 'commit':repo['commit'], 'repo':x['repo'],'path':x['path'],
  'body_sha256':first['body_sha256'], 'body_bytes':first['bytes'],
  'read_sections':sorted({f"{e['start_line']}-{e['end_line']}" for e in nav},key=lambda s:int(s.split('-')[0])),
  'read_routes':list(dict.fromkeys(f"{e['case_id']}-{e['route']}" for e in own)),
  'directly_verified':content, 'supports_or_refutes_questions':qs, 'limitations_unknown':limits,
  'authorship_lineage':('IBM decNumber vendored in jq' if fid=='JQ-0016' else repo['repo']),
  'event_lineage':f"{repo['repo']}@{repo['commit'] or repo['version']}",
  'minimum_count_eligible':eligible, 'minimum_category':cat,
  'access_method':'해당 경로가 frozen official-source corpus에서 과금 open한 본문만 탐색했다. 네트워크 archive 수집비용은 별도 corpus-build 기록이며 여기 UTC는 연구자가 경로본문을 처음 연 시각이다.',
  'repeat_access_rule':'같은 원문 여러 경로 열람은 source 1건; 섹션/재열람/미러를 별개자료로 세지 않는다.',
  'attribution':'위 direct_verified는 읽은 원문의 사실 요약; 질문 해결을 위한 filter 조합/비관련성 판정은 각 judgment.json에 연구자 추론으로 별도 표시.'
 })
(P/'evidence/jq/sources-note.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
audit=json.loads((P/'evidence/jq/route-audit.json').read_text())
rows=[]
for x in audit['routes']:
 q=P/f"evidence/routes/{x['case_id']}-{x['route']}"
 j=json.loads((q/'judgment.json').read_text())
 rows.append(f"| {x['case_id']}/{x['route']} | {' → '.join(x['opened_file_ids'])} | {x['attempts']}/4; 실패 {x['failed']} | {' + '.join(x['used_file_ids'])} | {x['judgment']} | {x['body_bytes']:,} |")
main=sum(r['minimum_count_eligible'] and r['minimum_category']=='main_manual_implementation' for r in records)
adj=sum(r['minimum_count_eligible'] and r['minimum_category']=='adjacent_manual_implementation' for r in records)
tests=sum(r['minimum_count_eligible'] and r['minimum_category']=='upstream_original_test' for r in records)
summary='''# jq J1–J4 경로 열람·사전판정 요약

- 단계① 원격 봉인: `abf2bc2ac9303cb96e6109eba107684e5f858a42`.
- 순서: J1 A→B, J2 B→A, J3 A→B, J4 B→A. 같은 연구자 `jq_recruit`가 읽었으며 경로별 기억노출을 기록했다.
- 공개 답·채택·댓글: 이 요약 작성까지 **미열람**. 이 파일과 `judgment.json`은 사후 결과로 보정하지 않는다.
- 사전 노출 4자리 전부를 노출순서대로 열었고 반대조건을 찾아본 뒤 종료했다. 조기중단은 없었다.

## 경로 원장

| 요청/경로 | 실제 본문 열람 순서 | 시도/한도 | 반환 파일 | 사전판정 | 본문 bytes |
|---|---|---|---|---|---:|
'''+ '\n'.join(rows)+'''

본문 과금은 32회, 실패·재시도 0회, 초과 0회이다. 각 경로 검색2회는 루트의 사전 랭킹 실행기록을 따른다. 반환자료는 모두 해당 경로에서 열린 파일이고 반환 절은 실제 section navigation 범위의 합집합에 들어간다. `route_audit.py`와 `route-audit.json`이 이 규칙을 다시 계산한다. 파일 수/시도 수가 같다고 bytes·읽기시간까지 같았다는 뜻은 아니다.

## 사전 비교 분모

| 층 | 요청 수 | A만 | B만 | 양쪽 완결 | 어느 쪽도 완결 아님 | 기술적 비교불가 |
|---|---:|---:|---:|---:|---:|---:|
| jq 경계 요청 | 3 | 0 | 0 | 2 | 1 | 0 |
| jq 동일범위 대조 | 1 | 0 | 0 | 1 | 0 | 0 |

경계 B의 인접 원문 노출 3/3, 본문 열람 3/3, 최종 반환 2/3(J2 cat, J4 grep), 완결 여부 변경 0/3이다. J3 Overpass 원문 두 개는 위치순 JSON 병합과 관계없는 영역/공간 인덱스 구현이라 반환하지 않았다. 불일치쌍 0/3이며 불일치쌍 내 B 승률은 **산출 불가**이다. 같은 연구자의 기억노출이 있어 독립·맹검 연구자 비교를 주장하지 않는다.

## 조건별 판정과 반례

**J1 — 양쪽 완결(문서기반).** 바깥 item의 startTime을 변수에 묶고 그 item의 자식만 순회하는 구체 filter를 제시했다. 원 질문과 같은 input을 유지하는 binding/pipe의 명세와 원 시험이 근거이다. 질문의 JSON 닫힘 누락·동일 command에 다른 출력 기록은 남겨두었다. 소수점 3자리 강제는 원문에 명시되지 않아 요구를 추가하지 않았다.

**J2 — 양쪽 부분.** title과 tracks를 같은 객체로 구성하는 연산은 지지된다. 원 입력에 offset 값이 없어 요구한 숫자 3645/3820은 유도할 수 없다. cat 원문도 입력 복사만 설명하며 그 결손을 메우지 않는다. 제목에서 단어가 빠진 기대값과 뒤바뀐 title 매핑도 실제 입력의 정정 없이는 단정할 수 없다. 추가로 물을 것은 offset과 표제 규칙을 포함한 완전한 원 입력이다.

**J3 — 양쪽 완결(문서기반).** range(0;length;2), 인덱싱, +를 결합한 jq-only filter로 연속 두 항목을 합친다. 문자열 연결과 객체 병합은 같은 +의 타입별 의미로 확인했다. 인접 Overpass 코드가 제공하는 생산자 변경은 명시된 jq-only 조건의 답이 아니다. 홀수 길이/중복 key의 원 요구가 없다는 한계와 오른쪽 key 우선 의미를 기록했다.

**J4 — 양쪽 완결(문서기반 합성); 가장 큰 민감도.** 단순히 “jq로 코드를 만들 수 있다”는 주장에 그치지 않고 `proposed_filter.jq`를 작성했다. raw-input으로 받은 로그에서 marker의 global match offset을 찾고, 각 suffix를 문자별로 누적하며 대괄호 깊이가 처음 0이 되는 지점에서 멈춘다. 이 구성은 중첩·빈 []·반복 marker·이웃 status 제외를 명시적으로 다룬다. 14개 manual 절을 읽어 사용 연산을 연결했다. 그러나 동일 filter의 컴파일/실행과 질문 원 입력을 사용하는 상류 회귀시험은 아직 없다. 문서의 연산계약을 조합한 연구자 해법을 “발견된 완성 snippet”과 구별해야 한다. literal balanced brackets를 벗어나는 quote/escape/multiline 규칙은 미확인이다. A에서는 Oniguruma 없는 빌드의 match 불가를 구현에서 직접 확인했다.

## 한계와 최소 후속

1. 거대한 jq 매뉴얼 한 파일이 첫 노출로 4개 요청의 대부분 기능을 모두 제공한다. 현 비교는 파일 슬롯 정책이며 절 단위 검색·답 작성 난도·동일 bytes 예산의 효과가 아니다. 다음 최소 확인은 J4의 구체 filter를 고정 jq 1.7.1에서 원 입력과 중첩/빈/반복 반례로 실행하는 것이다. 이 실행은 사후 보조 검증으로 기록하고 사전 승패를 소급 변경하지 않는다.
2. J2 원 입력 결손은 검색 정책 효과와 구별한다. 원 작성자의 이후 공개 정정에서 offset/제목 규칙이 실제로 제공되는지 단계② 원격 봉인 뒤 읽어야 한다.
3. 인접 파일 노출이 실제라도 범용 토큰 때문에 Overpass 공간계산이 상위에 왔다. 다음 최소 확인은 사후에 정확한 JSON 출력 원문이 있는지 조사하되 그 링크를 사전 경로 근거로 소급 추가하지 않는 것이다.

## 자료 하한용 기록

직접 연 고유 파일 '''+str(len(records))+'''개를 `sources-note.jsonl`에 기록했다. 기존 R0 4개는 `sources.jsonl`의 선정행에 별도 있다. 보수적 분류는 main 매뉴얼/구현 '''+str(main)+'''개, adjacent 매뉴얼/구현 '''+str(adj)+'''개, 상류 원 시험 '''+str(tests)+'''개이며 포함된 IBM decNumber 1개는 외부 하한에서 제외했다. 같은 파일 재열람과 같은 파일의 다른 절을 별개 자료로 세지 않는다. 원문 저작/배포 계보는 jq, GNU coreutils, GNU grep, Overpass의 4개 프로젝트 사건군이며 고유 파일 수를 독립 사건 수로 부풀리지 않는다. 이 4개 프로젝트 사건군과 R0 4개 질문 사건은 다른 종류의 분모이다.
'''
(P/'evidence/jq/summary.md').write_text(summary)
print(json.dumps({'files':len(records),'main':main,'adjacent':adj,'upstream_tests':tests,'path':'evidence/jq/sources-note.jsonl','summary':'evidence/jq/summary.md'},ensure_ascii=False))
