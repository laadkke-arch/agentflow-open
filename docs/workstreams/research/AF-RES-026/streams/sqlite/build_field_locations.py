"""Location-only audit of sealed T0 fields. No later author facts enter T0."""
import json
from pathlib import Path
P=Path(__file__).parent
rows=[json.loads(x) for x in (P/'initial.jsonl').read_text().splitlines()]
sources={x['id']:x for x in json.loads((P/'sources.json').read_text())}

# Entries: field -> [(classification, locator, precise qualification)].
locs={
'S01':{
'goal':[('명시','body L3–4,L89–93','C ATTACH가 shell처럼 없는 파일을 생성하기를 요구')],
'inputs':[('명시','body L27–36,L40–58','메모리 연결·READWRITE·ATTACH 및 없는 파일이라는 코드/주장; 원 로그 경로와의 불일치는 R4로 유지')],
'outputs':[('명시','body L3,L10–13,L80–93','새 파일 생성/실행 완료를 원하는 목적과 이미 만든 빈 파일의 대조')],
'version':[('미상','body L1–93 전체','OP SQLite 판 미기재; T1 3.37 발언은 이 필드에 넣지 않음'),('연구자해석','S-D01 fixed 3.37.1','당시 공개 비교판의 선택이며 OP 판이 아님')],
'platform':[('명시','body C code L16–64; shell L10–13,L69–86','C·shell 코드와 경로는 명시'),('연구자해석','body L69–86','Unix형 환경으로 해석'),('미상','body L1–93 전체','정확 OS·판 미기재')],
'actors':[('명시','body L3–4,L36,L40–58','자기 C 코드와 별도 sqlite3 shell 비교'),('연구자해석','body L36,L40–58','동기 C API 호출 순서·같은 connection은 코드 정적 판독; 병행 실행을 관측하지 않음')]
},
'S02':{
'goal':[('명시','body L1–5','기존 DB를 C로 읽으려 하며 실행 오류의 수정 요청')],
'inputs':[('명시','body L20,L39','sqlite3_open의 ex1.db와 gcc -o mysql 명령')],
'outputs':[('연구자해석','body L1–5,L20–35,L39','당장 가능한 출력은 프로그램 실행과 연결 open/close; 전체 SELECT 조회 완료와 구별')],
'version':[('미상','body L1–39 전체','SQLite/GCC 판 미기재'),('연구자해석','S-D01 3.37.1; S-D03 GCC11.2','동시대 비교판을 고른 것; 설치판 추정 아님')],
'platform':[('명시','body L1,L39','bash 오류와 gcc 명령'),('연구자해석','body L39','Linux형 shell이라고 해석; Linux 배포판 확정 아님'),('미상','body L1–39 전체','OS 이름·판 미기재')],
'actors':[('연구자해석','body L20,L39','명령이 C 실행파일을 만들며 C가 DB파일을 연다는 코드/명령의 역할 구분')]
},
'S03':{
'goal':[('명시','body L16–18','열 타입과 view 계산식 두 변경 목적')],
'inputs':[('명시','body L7–13,L33–43','sqlite_version 결과 주석, OFF 설정, 원 schema, 전달/rename 코드')],
'outputs':[('명시','body L17–18,L50–51,L56–57','text 열·문자열 반복 view·commit')],
'version':[('명시','body L7','select sqlite_version()의 3.34.0 주석'),('연구자해석','S-D04/S-D05 version-3.34.0','같은 판 공식 테스트/구현 비교')],
'platform':[('명시','body L5–61','SQL script'),('연구자해석','body L5–61','봉인 필드의 CLI는 실행 도구 추정이며 OP가 명시한 실행 UI는 아님'),('미상','body L1–61 전체','OS·호출 앱은 미기재')],
'actors':[('명시','body L27–28,L40–43,L56–57','BEGIN→schema 변경→COMMIT script'),('연구자해석','body L43; S-D04 tests9.0–9.5','rename 때 schema가 검사되는 해석; 원문 실행 오류 및 당시 테스트 근거')]
},
'S04':{
'goal':[('명시','body L1–6','강제 재시작 뒤 삽입 행 복구 차이 질문'),('연구자해석','body L2,L5–6','보존 경계를 이해한다는 목적 요약; commit 성공을 전제하지 않음')],
'inputs':[('명시','body L5–6,L17–21','transaction INSERT·rowid 출력과 journal/locking/sync/page 설정')],
'outputs':[('명시','body L2,L6','재시작 전후 행/rowid 차이')],
'version':[('명시','body L16','3.37.0'),('연구자해석','S-D06/S-D07 version-3.37.0','같은 판 비교')],
'platform':[('명시','body L14–15','iPhone6S/iOS12.3')],
'actors':[('명시','body L2,L5–6','삽입 작업과 장치 재시작'),('연구자해석','body L2,L5–6','OS/장치와 transaction의 경계를 분리한 코딩'),('미상','body L1–21 전체','언어·wrapper·구체적 재시작 버튼·COMMIT 성공 여부는 T0에 없음')]
},
'S05':{
'goal':[('명시','body L1–8','재사용 성능을 위해 reset/clear를 다른 thread로 옮겨도 안전한지 질문')],
'inputs':[('명시','body L5–6','같은 connection에서 main의 다른 API와 별도 thread reset/clear')],
'outputs':[('명시','body L8','안전성 질문'),('연구자해석','body L1–3','성능은 원하는 이유로 표현; 측정값이나 안전성 필수조건과 동일시하지 않음')],
'version':[('미상','body L1–8 전체','SQLite 판·실효 threading mode 미기재'),('연구자해석','S-D01 fixed 3.37.1','공개 비교판 선택')],
'platform':[('명시','body L5–6','C API 이름과 여러 thread'),('미상','body L1–8 전체','OS·빌드 옵션 미기재')],
'actors':[('명시','body L5–6','main exec/prepare/step와 다른 thread reset/clear, same connection'),('미상','body L1–8 전체','같은 statement인지, 실제 호출 순서, FULLMUTEX 여부는 미기재')]
},
'S06':{
'goal':[('명시','body L1 문장1·3','config.h 설정 사용을 이어가고 주석 처리 변경이 우연인지 질문'),('연구자해석','body L1','기존 설정 경로 유지라는 목적 요약')],
'inputs':[('명시','body L1 문장1·2','같은 디렉터리 config.h 및 주석 처리됐다는 보고')],
'outputs':[('연구자해석','body L1','설정 헤더 반영은 목적을 요약한 값; 실제 출력/실행 로그는 없음')],
'version':[('미상','body L1 전체','정확 SQLite 판과 source 배포 형태 미기재'),('연구자해석','S-D08/S-D09 fixed 3.37.1','공개 비교판 선택')],
'platform':[('명시','body L1 문장1','여러 빌드 시스템'),('연구자해석','body L1; S-D08 L184–208','config.h/include로 C 전처리 경로를 해석'),('미상','body L1 전체','OS/compiler/build command 미기재')],
'actors':[('명시','body L1','여러 빌드 시스템'),('연구자해석','S-D08 L184–208; S-D09 L220–250','amalgamation/split source와 전처리기는 가능한 두 경로를 연구자가 나눈 것; 실제 source 형태는 미상')]
},
'S07':{
'goal':[('명시','body L3–9','PG/SQLite autovacuum의 파일 축소·공간 반환 비교'),('연구자해석','body L3','PG를 PostgreSQL로 해석; 원문은 약어만 사용')],
'inputs':[('명시','body L3,L5,L7','두 엔진의 공간 반환에 대한 작성자 가설; 사실 확정으로 코딩하지 않음')],
'outputs':[('명시','body L9','이해의 정확성 및 차이 확인')],
'version':[('미상','body L1–9 전체','SQLite/PG 판 미기재'),('연구자해석','S-D10 3.37.1; S-D11 PG14.1','당시 비교판을 선택; OP 설치 환경 없음')],
'platform':[('연구자해석','body L3–9','운영 인스턴스 로그 없는 개념 비교로 코딩'),('미상','body L1–9 전체','배포 OS·실제 mode 미기재')],
'actors':[('명시','body L3','PG의 주기적 daemon'),('연구자해석','body L5; S-D10 tests7.1–7.3','SQLite transaction/mode와의 차이는 공식 테스트에 따른 비교 틀; 원문이 FULL을 명시했다는 뜻 아님')]
},
'S08':{
'goal':[('명시','body L1,L30–44,L56–76','form 제출 값을 animalStream INSERT로 전달')],
'inputs':[('명시','body L3–11,L31–38','NOT NULL schema·req.body 필드·bare duration·bind array')],
'outputs':[('명시','body L1,L38–44','row 삽입 및 lastID 출력 기대')],
'version':[('미상','body L1–79 전체','Node/package/SQLite 판 미기재'),('연구자해석','S-D12 v5.0.2; S-D01 3.37.1','package와 SQLite는 별도 비교판이며 실제 bundle 조합이 아님')],
'platform':[('명시','body L13–30','Nodejs, sqlite3 require, Express, body-parser'),('미상','body L1–79 전체','정확 OS와 Node 판 미기재; 경로만으로 판 확정 안 함')],
'actors':[('명시','body L30–44,L56–76','form POST, request handler, db.run callback 구조'),('연구자해석','body L38–44; S-D12 README L1,L29–46','비동기 주체는 Node binding callback이라는 정적/API 해석. SQLite core 자체가 비동기라는 뜻이 아님; 실제 timing 실행 없음')]
}}

out=[]
for r in rows:
    case=r['case_id'];fields={}
    for field,entries in locs[case].items():
        vals=[]
        for kind,locator,note in entries:
            urls=([r['original_version']['url']] if locator.startswith('body') else [])+[sources[i]['url'] for i in sources if i in locator]
            vals.append(dict(classification=kind,locator=locator,note=note,
                url=';'.join(dict.fromkeys(urls))))
        fields[field]=dict(sealed_value=r[field],locations=vals)
    out.append(dict(case_id=case,original_artifact=r['original_version']['identifier'],source_url=r['original_version']['url'],
      audit_stage='T1 location audit of unchanged T0; original body only',contains_later_author_facts=False,
      input_sha256=r['input_sha256'],fields=fields,requirements=r['requirements'],
      note='원판·필드값을 변경하지 않고 명시/연구자해석/미상을 분리. 전체 본문 미기재 점검은 body-locations와 initial 원문 해시로 재현.'))
(P/'field-locations.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
print('wrote',len(out),'T0 field location audit rows')
