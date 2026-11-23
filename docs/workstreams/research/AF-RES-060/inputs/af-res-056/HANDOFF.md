# AF-RES-056 인계 — 현재 고정 비교 완료, 역사 모집·구현 완결은 부분

**상태: `partial_handoff` / 완전 충족 아님.** 현재 공개 태그에서 고정한8요구×L/V16비교는 완료했다. L은8건 모두 빈 반환이고 V는 JS-4에 SC-032 하나를 추가했다. 같은 구현·판·허용 두 행동 안에서 두 조건을 함께 확인한 완결과 한 조건을 확인한 부분은 모두0이며, 실제 후보1개는 미확인이다. 확정 근접오답0을 오탐률0으로 바꾸지 않는다. 결과가 효과를 보이지 않았다는 이유로 표본·용어·게시 필드를 사후 확대하지 않았다.

역사적 tag/alias·삭제/태그 제거 모집단 복원과 원 환경의 공동 구현 증거가 남아 있다. 마지막 재개 지점과 결손 입력은 아래에 구체화했다. 질문이나 허가 요청 없이 관측 가능한 작업·교차 검토·원격 커밋·지정 검사를 수행하고 부분 인계로 종료한다.

## 1. 고정 결과와 두 필수 표 위치

- **결과/최종 수용 원장 고정 SHA:** `2f8ec01e6b52bef4fc3cd003b1690383b6496526`.
- **깨끗한 결과판의 실제 검증 영수증 SHA:** `46f1a7e533ac7c49c532a75faeb564ce4630e4b8`. 이 커밋은 원격 재열람/세션 검사 영수증2파일만 추가하며 결과·수용 원장을 바꾸지 않았다.
- [RESULT.md 고정판](https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/RESULT.md): **표1 L1–18, 데이터16행**, **표2 L20–29, 데이터8행**. 파일은 서론 없이 표1부터 시작한다. Q1–Q7은 L31 이후, 가장 중요한 세 약점은 마지막 L217–223이다.
- [수용 원장 고정판](https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/evidence/acceptance-evidence.json):36기준의 상태·분자·분모·단위·파일/행·결손·최소 재개 자료. `full_acceptance=false`.
- [8개 반환 카드](https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/cards.md), [Q1–Q7 자체 검토](https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/SELF_CHECK.md), [전체 원문 원장](https://github.com/laadkke-arch/agentflow-open/blob/2f8ec01e6b52bef4fc3cd003b1690383b6496526/docs/workstreams/research/AF-RES-056/sources.jsonl).

RESULT의 Git blob은 `9b20636d8f86835476e33b9046a0eef6b7961ae0`, SHA256는 `b7bbdb73b18a31f644c386c0d9b227d425f62a80f4afd98f0f3996711249d86d`다. 최초 결과 묶음78cad3d0… 이후 본문은 바뀌지 않았다. 최종 수용 JSON blob은 `5008ebed140ec6c6700bca4cafd7283fce933514`이며, 실제 수행한 발행 gate만 후속 갱신했다. 이 HANDOFF는 위 고정 결과와 검증을 가리키는 마지막 단독 파일 커밋 대상으로 작성했다. 자기 커밋 SHA를 본문 안에 소급 삽입하지 않는다.

## 2. 관측한 분모와 반환 결정

| 단위 | 실제 값 | 해석·남는 한계 |
| --- | --- | --- |
| 모집/선정 | 현재 공개 canonical tag40+40=80, 최초 revision1 직접 독해80, 선정4+4=8 | 당시 별칭·삭제·retagged 전체 유니버스는 미확인. 선정8개는 모두2021초 |
| 용어·개입 | literal20, V 허용7, 보류10; 중복 제거 추가 질의6, 영향 요구4/8 | validate→validation은 정의 근거로 허용; validation→Validator는 허용하지 않음 |
| 같은 목록 | Schema40 + LD전체22 =62게시행 | LD의18 부족은 목록 소진이며 접근실패가 아님. 당시판이 아닌 현재 재탐색판 |
| 비교·슬롯 | 16비교,48슬롯 = 무매치45 + 풀소진2 + 채움1 | L0/8→V1/8 비어 있지 않은 반환. SC-032 원순번32 |
| 같은 시행 | P1=1행동, P2=2행동, P3=2행동 | 논리행동합5를 한 시행5로 합치지 않음. 실제 이용자 클릭·채택 미측정 |
| 판정 | 본표 완결0·부분0·확정 근접오답0·미확인 고유후보1 | 정확도/오탐률은 null. L기존후보0이므로 밀림의 조건부 분모0, 해당 없음 |
| 창·문서 | 고유 도착응답3, 경계 확정2, 제목 없는JSON 경계 미확인1 | windows52행=빈47+행동5. 허용창의 조건 입증 기여문서0 |
| 판정 원장 | judgments19행=빈비교15+본표시행3+예산밖진단1 | 예산 밖 C2 진단을 본표 부분 성공으로 올리지 않음 |
| 반환 카드 | 전체 구현0, 조건부 보완4, 보류4 | 보완: JS-2/3/4·LD-3. 원문 전체를 해결했다고 추천하지 않음 |
| 원문 수 | sources269행, 고유 직접1차109저작, 필수 배당24 | 배당8+4+4+4+4. 같은 편집 시스템으로 묶는 민감도는107저작·22/24이며 별도 공개 |

269행의 분류는 직접1차190, 접근 실패 기록40, metadata/허가문18, 미러/재수록2, 내부 입력/자체 실행19다. 실패 기록40개를 모두 최종 미복구 결손40개로 해석하지 않는다. 같은 매뉴얼의 여러 절·suite 파일·같은 전거의 다른 표현·자체 실행을 새 외부 저작으로 부풀리지 않았다. [집계](evidence/source-counts.json)·[고유 저작](evidence/primary-works.csv)·[715검사 감사](evidence/review/source-audit-receipt.json)를 함께 본다.

## 3. 결론을 제한한 반례와 구현판

1. **목록의 검색 필드가 없으면 올바른 표준어도 반환을 만들지 못했다.** LD-3의 framing을 사전에 허용했고 jsonld.js/PyLD의 frame 소스도 나중에 확인했지만 LD 목록은 제목만 표시했다. 이 기능 누락 진단을 원 LD-3 완결 구현 발견으로 올리지 않았다. Schema의 Validator 표제는 사전 V의 validation과 다르며, 결과를 본 뒤 파생형을 추가하지 않았다.
2. **한 기능의 지원과 두 조건의 공동 충족은 달랐다.** SC-032@d5199551f758ba067612979ae32ec35693640ccf의 C++ C2-only 연구 schema는 datatype=string을 허용하고 array를 거절했으나 없는 pii 열 이름도 허용했다. 이는 그 schema의 동적 C1 누락이며 라이브러리 전체의 불가능이 아니다. 원문 Python 환경·값 존재 guard는 미확인이다. [실제3입력·build/run exit0](evidence/windows/sc032-execution.json).
3. **공식 기능 이름이 변이·옵션을 대신하지 못했다.** python-jsonschema4.26.0의 작은 공식 fixture14호출에서 해당 profile 기대12/12가 일치했고 format OFF 통제2는 모두 유효였다. default 누락{}는 그대로였고 입력 mutation은0/14였다. 문서판4.23.0·Ajv8.17.1을 실행했다고 하지 않는다. [실제 환경·출력](evidence/schema-diagnostics/runtime-receipt.json).
4. **LD 근접 음성이 연구자의 예상도 뒤집었다.** PyLD3.3.0@3ac1987d9be3648c09b7c7e34865ce82d637e742의 축소 연구 양성은 a=1 선택과 b/c/issuer 보존을 보였다. 입력·프레임 context의 values 매핑을 @nest로 바꾼 음성은 예상한 false/false 출력 대신 FrameError를 냈다. 최초 runner **exit1을 유지**했고, 후속 @requireAll 충돌/속성 병합 진단의 exit0은 원 시험의 성공으로 합치지 않았다. 원 credential·remote context·원 jsonld.js 실행은 미실시다. [최초 출력](evidence/ld-suppliers/execution-attempts/offline-frame.stdout.json)·[원인 진단](evidence/ld-suppliers/execution-attempts/nest-cause.stdout.json).
5. **같은 이름·관련 관계·여러 인터페이스가 독립 기능을 뜻하지 않았다.** LOC의 같은 Etching 철자는 URI/세목 범위가 달랐고 Getty의 painting 작품과 제작 행위도 다른 개념이었다. ajv-cli/jsonld-cli는 기존 엔진에 위임하며 PyLD는 JavaScript 구현을 이식한 별도 Python 코드다. 전거·계보를 독립 구현 성공 횟수로 세지 않았다. [Q7](evidence/authority/findings.md)·[Schema 계보](evidence/schema-diagnostics/FINDINGS.md)·[LD 계보](evidence/ld-suppliers/findings.md).

제목만으로 충분한 사례, 번역 때문에 들어온 확정 근접오답, 기존 L후보의 밀림을 적극 찾았으나 이번 고정 풀에서는 각각 관측0/미확인/조건부 분모0이었다. 이 부재를 일반 법칙으로 주장하지 않는다. framing 제거·slot3→4의 사전 감도도 변화0이지만 원래 최대 매치풀이1이어서 검증력이 제한된다.

## 4. 실제 검증, 정정과 출판 순서

### 고정판을 다시 연 뒤 실행한 명령

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-056/manifest.json --fetch
```

| 검증 | 실제 값·시각 UTC | 고정 영수증 |
| --- | --- | --- |
| 최초 결과 원격 재열람 | 78cad3d0595e0c40e06cfe1562ceda53c89029c1의 RESULT/수용 JSON2파일 전체 UTF-8 byte 및 blob 일치 | [remote-read-result.json](evidence/verification/remote-read-result.json) |
| 최초 결과 session check | 2026-11-23T02:30:15.021867~02:30:24.875953, exit0, passed, errors/outside_paths 빈 목록; 당시 final-review.md는 소유경로 미커밋 검토 | [session-check-result.json](evidence/verification/session-check-result.json) |
| 최종 수용판 원격 재열람 | 2f8ec01e6b52bef4fc3cd003b1690383b6496526의 두 파일 일치, 2026-11-23T02:32:22.571Z; 결과판의 작업 트리 clean 확인 | [46f1a7e5…/remote-read-final.json](https://github.com/laadkke-arch/agentflow-open/blob/46f1a7e533ac7c49c532a75faeb564ce4630e4b8/docs/workstreams/research/AF-RES-056/evidence/verification/remote-read-final.json) |
| 최종 깨끗한 결과판 session check | **2026-11-23T02:32:22.793604~02:32:33.437136, exit0**, passed, stderr 빈 문자열, errors/outside_paths 빈 목록 | [46f1a7e5…/session-check-final.json](https://github.com/laadkke-arch/agentflow-open/blob/46f1a7e533ac7c49c532a75faeb564ce4630e4b8/docs/workstreams/research/AF-RES-056/evidence/verification/session-check-final.json) |
| 본문·수용 원장 연결 | 실제191검사 통과, exit0 | [report-validation-ledger.json](evidence/verification/report-validation-ledger.json) |
| 교차 검산 | 순위35, 창31, 최종 source715 검사 통과 | [순위](evidence/review/ranking-audit-receipt.json), [창](evidence/review/window-audit-receipt.json), [원문](evidence/review/source-audit-receipt.json) |

최종 check가 확인한 통합판은 `a0b0c46acb42f70c4c248af1c93783e4f2838f03`이며 시작판보다 진행되었지만 계약 hash `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`는 같았다. 시작 manifest를 최신판으로 소급 바꾸지 않았다. Git의 계약/소유경로 검사는 연구의 역사 모집 완전성이나 구현 진실성을 인증하지 않는다. 위 clean check는 결과판2f8ec01e…를 대상으로 했고, 뒤의46f1a7e5…는 그 영수증만, 이 마지막 커밋은 HANDOFF만 추가한다.

검산 주체는 같은 ChatGPT 협업 세션이다. root가 통합·본표·SC-032 진단을, LD 담당이 모집/표준/공급자와 PyLD 진단을, catalog 담당이 목록/Schema 진단과 source/SELF 검토를, authority 담당이 Q7 및 별도 순위/창/최종 대조를 수행했다. **외부·인간·맹검 독립 검토는 없었다.** [최종 좁은 검토](evidence/final-review.md)의 당시 hash·미실시 gate 상태와 후속 실제 검증을 구분한다.

관측을 수정한 이력은 [SCOPE.md](SCOPE.md)에 있다. Markdown 기호까지 세던 v1창은 실제 표시487/479단어였고 같은 응답의 렌더500단어 v2로 정정했다. 첫 두 링크·순위·C1/C2·완결0은 같았다. 정정 때 이미 전체 진단이 노출됐으며 감사자의 최초 감도-only 권고도 보존했다. 표준 절 위치·CAT006 L291·Python 언어판/패키지판·최소 fixture의 범위·허용 validate→validation 서술도 바로잡았다. 원 시험의 실패/원 입력을 소급 수정하지 않았고, 원문/용어/순위 동결은 유지했다. 발행 직전 cards EOF 공백 검사 실패와 정정 후0도 [prepublication-check.json](evidence/prepublication-check.json)에 있다.

### 원격 묶음 SHA

| 묶음 | 원격 SHA | 봉인 내용 |
| --- | --- | --- |
| 사전 계약 | `628c330941babcb43b636d0a37ecb073b2c9d107` | manifest·입력판·사전 범위 |
| ① 모집·원문 조건·용어 | `1f63f0129207904a91ae9e01bb3e48c86415a644` | 80 frame·8계약·37용어행; 후보 순위 전 |
| ② 공식 목록·상위3 | `b765a189aa2a1f5982a4994fc0476273abbf7127` | 62게시행·16비교·48슬롯·경로 계획; 공급자 목적지 판정 전 |
| ③ 경로·판·반례·감도 | `d9fbc7c9a8a1ee7c4febb1b2f3f3d29c286b8bac` | 실제 창·진단·269원문행·전거·교차 감사 |
| ④ 결과·카드·자체 검토 | `78cad3d0595e0c40e06cfe1562ceda53c89029c1` | 필수16/8표·Q1–Q7·8카드·36기준·재생 입력 |
| 검증 수용판 | `2f8ec01e6b52bef4fc3cd003b1690383b6496526` | 최초 원격 재열람/실제 check·최종 검토 및 gate 갱신 |
| 깨끗한 결과판 검증 영수증 | `46f1a7e533ac7c49c532a75faeb564ce4630e4b8` | 최종 원격 재열람과 clean check 실제 출력2파일 |

배정 브랜치는 `work/research-af-res-056`, 소유 경로는 `docs/workstreams/research/AF-RES-056/`다. 계획 통합판 `d7e60daf1b5b2c918502c407982566369b7149e3`, 실제 시작판 `573a8f1a7cafa90b87bcbb4267e73fee12385bda`, 의존 HANDOFF `AF-RES-052@6e6818e345ff8ab9beffd0ea0e1cee9fd6f4ae01`, 읽은 결과판 `3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9`를 [manifest](manifest.json)에 보존했다. 의존052의 고정판으로 진행했고 같은 차수 다른 산출물을 기다리거나048/052의 예전 후보 묶음을 다시 분모에 넣지 않았다. `dot-control.json`과 공통 파일은 수정하지 않았다.

## 5. 막힌 이유와 다음 첫 행동

**첫 행동은 새 후보 검색이 아니라 역사 모집 입력의 판과 범위 확보다.** 2024cutoff를 포함하는 날짜가 명확한 공개 스냅샷의 발행자 URL·시각·SHA256, Posts/PostHistory/TagSynonyms의 포함 여부, 삭제/태그 제거 이력의 보존 범위를 먼저 확인한다. 필요한 자료가 실제로 있어야 `evidence/historical/` 아래 새 입력판으로 고정하고 기존 frame과 생성일/ID순·첫 적격4를 대조한다. 2024말 덤프 한 벌이 그 전에 삭제된 질문까지 모두 포함한다고 가정하지 않는다. [역사 필드 설명](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678)은 직접 읽었지만 실제 과거 덤프를 확보한 것은 아니다. archive/community dump 접근 실패는 sources의 META-HISTORY-F01/F02에 있다. 다른 질문이나 다른 질의로 빈자리를 바꾸지 않는다.

| 남은 결손 | 왜 현재 판정을 올릴 수 없는가 | 최소 재개 입력·다음 판별 |
| --- | --- | --- |
| 역사 모집·별칭 | 현재 tag API와 현재 empty synonyms는 과거 삭제/retagged/별칭 부재를 증명하지 못함 | 날짜·범위·hash가 있는 Posts/PostHistory/TagSynonyms 및 삭제 전 자료. 기존80 ID/최초GUID와 다른 앞선 적격 질문이 있는지 먼저 대조 |
| JS-4 원 환경·동적 C1·guard | C++ C2-only 진단은 Python 원 요구의 완결이 아니며 값 존재의 정확한 뜻도 미명시 | 원 Python/package lock·schema·동적 columns 투영 방식·guard 정의·양성/근접음성. 같은판·옵션에서 C1/C2와guard를 공동 확인 |
| LD-3 원 credential | PyLD 최소 @set/issuer fixture는 원 remote context/credential/jsonld.js 환경을 대신하지 않음 | 원 context의 고정 URI응답·원 package lock·명시 frame옵션과전체입력. 객체 경계·a=1선택·나머지필드보존의같은출력 |
| 게시 필드·창 모델 | 기능 열 부재, Validator 파생형, 제목 없는 JSON의 창 경계, 실제 UI 준비 비용이 분리돼 있음 | 새로운 기능 필드/별칭·관계와 JSON 창/목록 준비 규칙을 결과 전에 고정하는 별도 비교. 이번표 사후수정 금지 |
| 원문 body/화면의 독립 재현 | 공개 전문 캐시를 커밋하지 않았고 live 홈페이지는 바뀔 수 있음 | 같은 ID/GUID/bodyhash의 응답 및 원래 homepage snapshot. 없으면 동일 원문 재현 미실시/미확인 유지 |

## 6. 실행 명령과 필요한 입력

커밋된 결과로 가능한 검산은 아래다. stage1/stage2 Git 객체가 있는 이 브랜치 checkout이 입력이다. 첫 명령은 읽기 전용이며 stdout을 출력한다. session check는 계약/허용경로 검사이고 현재 통합판을 fetch한다.

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/validate_report.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-056/manifest.json --fetch
```

원래 receipt를 유지하려면 공급자/감사 재생은 별도 checkout에서 한다. 실제 수행한 진단과 아직 미실시인 재개를 혼동하지 않는다.

| 절차 | 명령·입력의 정확한 위치 | 이번 상태 |
| --- | --- | --- |
| SC-032 C2-only | [windows/FINDINGS.md](evidence/windows/FINDINGS.md)의 pinned 두 clone 명령 + `python -B docs/workstreams/research/AF-RES-056/evidence/windows/run_sc032_diagnostic.py`; 입력 schema_fixture.cpp, d5199551… 소스, nlohmann55f93686… | 실제 수행 완료. CMake 없이 g++14.2.0의 명시 소스/include 빌드. 원 Python 전체는 미실시 |
| Schema 공식 작은 fixture | `python -B docs/workstreams/research/AF-RES-056/evidence/schema-diagnostics/run_diagnostics.py`; selected-cases.json·고정 snapshots·설치 jsonschema4.26.0 환경 | 실제14호출 완료. v4.23.0/Ajv 원판·전체 suite는 미실시 |
| PyLD 최소 양성/음성·원인 | [REPLAY_PLAN.md](evidence/ld-suppliers/REPLAY_PLAN.md)의 고정 checkout·task-local dependency·replay_plan.py/trace_nest.py 명령; minimal-fixtures.json와dependency-lock.json | 실제 수행 완료, 최초exit1 보존. jsonld.js·원 credential·공식 suite는 미실시 |
| source 감사 재생 | [REPLAY.md](evidence/REPLAY.md)의 같은40 ID/GUID/bodyhash 복구 코드 뒤 `python -B docs/workstreams/research/AF-RES-056/evidence/review/source_audit.py` | 최초감사는실시. 새 캐시복구 명령은미실시; 전문캐시없이즉시재생된다고하지않음 |
| CLI 정확 의존판 | 보존된 당시 ajv-cli 설치 디렉터리에서 `npm ls --all --json ajv`와 `node -p "require('ajv/package.json').version"` | 그 설치환경/lock이 없어미실시. 지금 새로설치한버전을당시판으로채우지않음 |

원 요구 전체 공동시험의 완전한 재개 명령은 아직 입력·lock·모호한 guard가 확정되지 않아 만들 수 없다. 위 고정 진단 실행기를 원 프로그램 시험이라고 부르지 않는다. 각 카드의 최소 입력을 먼저 확보하고, 그 실제 프로그램의 실행 명령·옵션·입출력을 별도 연구판에 기록해야 한다. 현재 확인하지 못한 원 환경에 대한 성공 결과나 가상의 실행 로그는 없다.

## 7. 색인 제안 — 공통 색인에는 미반영

다음 항목을 후속 통합 담당자가 연구 색인에 연결할 수 있다. 소유 경로 밖 파일과 dot-control은 이번 작업에서 수정하지 않았다.

| 제안 색인 키 | 연결할 증거 | 정확한 설명 |
| --- | --- | --- |
| AF-RES-056 / 기능구→표준명 / same-budget L–V | RESULT 첫2표·matches/slots·vocabulary | 현재8요구에서신규후보1,허용창완결증가0,미확인1;역사모집부분 |
| 게시 기능 필드 결손 | catalog·LD-3 공급자 진단 | framing 기능은있지만제목전용목록에없음;완결구현누락률추정아님 |
| 주석/변이·format옵션·동적enum | Schema진단·SC0323입력 | 표준명/지원draft만으로요구결합판정불가;예산밖반례 |
| 객체 경계와 framing | LD공식시험·PyLD예측불일치 | @nest병합과특정frame키충돌;원credential미실시 |
| 전거 관계의 방향·동일철자다른URI | LOC2·Getty2·추가Etching세목 | 용어관계관리의설계유추;소프트웨어검색효과의외부검증아님 |

## 8. 가장 중요한 불일치·약점 3건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 현재 canonical-tag 모집과 당시 tag/alias·삭제 유니버스가 다름;8질문 모두2021초, LD3/4건은 응용층 생성/추출 | 역사 모집단의 첫4건·일반적인 문서 변환 요구에서의 효과라는 일반화 | [frame.csv](frame.csv) 80행, [LD tag 이력](evidence/ld-pre/requirements.json), [역사 스키마 설명](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678); sources META-HISTORY-01/02/F01/F02 | 2024cutoff의 Posts/PostHistory·당시 TagSynonyms 원본/덤프와 삭제·retagged 범위를 확보, 같은 ID 규칙으로 frame 대조 | 원순서/적격 첫4가 달라지면 역사 모집단 결론은 수정. 현재 고정 코호트16비교는 별도로 보존 |
| 용어와 게시 필드의 접점이 좁음; Validator≠validation, LD 기능 열 없음; L후보0·최대풀1 | 용어 연결의 일반 효과·오탐률·밀림·slot4 안정성 | [catalog.csv](catalog.csv) SC001–040/LD001–022, [matches.csv](matches.csv)16행, [순위 감사](evidence/review/ranking-audit.md); CAT002/010·LD-SUP-JS-DOC/PY-DOC | 기능 필드/출처 있는 별칭과 어형/역할 관계를 사전 정의한 별도 대조; 본표 사후 확대 금지 | 같은 의미의 게시명으로 후보와 양조건 증거가 늘거나, 새 근접오답/기존후보 밀림이 관측되면 효과·비용 판단이 바뀜 |
| 본표 구현 미확인·환경/판/guard 결손과 창 추출 정정; P3는 제목 없는 JSON; 최소 fixture가 원 요구 전체를 대신하지 못함 | 동일 구현·판·두 행동 안의 완결 및 정확도 | [windows.csv](windows.csv) P1/P2/P3, [judgments.csv](judgments.csv), [창 감사](evidence/review/window-audit.md), [C++ receipt](evidence/windows/sc032-execution.json), [PyLD exit1](evidence/ld-suppliers/execution-attempts/offline-frame-attempt.json) | 원 Python/jsonld 환경·고정 context/lock·모호한 guard 의미를 확보하고 동일 입력 양성/근접음성을 같은 판·옵션에서 실행; 두 조건 근거가 들어오는 사전 창 필요 | 실제 동일판 두 조건·guard 증거가 허용 창에서 함께 확인되면 완결로 승격. v1/v2 현재 결론은 둘 다0이며 사후 추가 창만으로 승격하지 않음 |

