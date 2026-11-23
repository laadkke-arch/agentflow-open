# 열람 창·같은 시행 판정 감사

**판정: 같은 시행의 경로와 예산 밖 진단을 섞어 성공을 만든 사례는 없다.** 동결된 SC-032 한 후보에 대해 1·2·2행동의 세 경로가 정확히 대응되고, 주표는 완결 0·한 조건 입증 0·미확인 후보 1이다. 감사 과정에서 발견한 실제 추출 결함은 **500 Markdown 단어를 500 렌더링 본문 단어로 표시한 것**이다. 같은 응답에서 렌더링 기준으로 다시 계산해 README와 홈페이지의 창을 정정했고, 첫 두 링크·조건 판정은 바뀌지 않았다. 최초 기록과 사후 정정 이력은 함께 보존한다.

감사자: `/root/authority_records`. 같은 모델의 팀내 검토이며 외부 독립·맹검 검토가 아니다. 원장·고정 공급자 Git 객체·원래 홈페이지 응답의 보존 텍스트·실행 영수증을 읽었다. 공급자 실행을 독립적으로 재실행하지 않았다. `window_audit.py`의 31개 구조·정정 검사는 실제 종료 0, 실패 0이다. 시각과 입력 파일 SHA256는 [window-audit-receipt.json](window-audit-receipt.json)에 있다.

## 1. 입력의 고정과 검사 범위

동결 순위는 `b765a189aa2a1f5982a4994fc0476273abbf7127`의 [slots.csv](https://github.com/laadkke-arch/agentflow-open/blob/b765a189aa2a1f5982a4994fc0476273abbf7127/docs/workstreams/research/AF-RES-056/slots.csv)다. 이 감사가 시작할 때와 끝날 때 모두 저장소 HEAD는 단계2였고, 이후 창·판정 파일은 단계3 게시를 준비하는 작업트리였다. 따라서 아직 게시되지 않은 결과 SHA를 만들어 적지 않았으며 실제 읽은 byte hash로 입력을 식별했다.

처음 읽은 v1 `windows.csv`의 SHA256는 `b9689c9dd113f697112402fdf36f634515437d33e92c95a0d7a8042e9f440abf`, `judgments.csv`는 `badeab5825b2f44cd4bebad677c9b3e2875dd8f12081e6158f19d57a75d542a7`이다. 감사 피드백 뒤 루트가 v2 창·source ID·설명을 고쳤고, 최종 기계 검사는 그 수정 파일의 hash를 receipt에 남겼다. 입력 조건·V 용어·목록·순위는 변경하지 않았다.

검사는 다음을 직접 대조했다.

- `windows.csv`와 고정 48슬롯의 comparison·slot·candidate·원순번·첫 URL 대응.
- 각 trial의 action index·action count·source ID·판정 URL 및 같은 시행 연결.
- README 고정 SHA와 첫 정보 링크의 실제 순서·줄 위치.
- v1 창의 byte hash와 렌더링 후 단어 수, v2 500단어의 경계·내용 차이.
- `judgments.csv`에서 본표와 `OUTSIDE-BUDGET`의 분리.
- C++ fixture hash와 기록된 stdout·구조화 cases·종료 코드의 일치. 이는 실행 기록 감사이며 새 실행 성적이 아니다.

## 2. 슬롯·창·시행·후보는 서로 다른 단위다

| 단위 | 실제 수 | 검산 |
| --- | --- | --- |
| 동결 자리 | 48 | 채움 1·빈 매치 45·풀 소진 2 |
| 빈자리 대응 window 행 | 47 | 각 빈자리당 정확히 1행, 가상 action/trial/source URL 없음 |
| 실제 논리적 action 행 | 5 | P1 1 + P2 2 + P3 2 |
| 전체 windows 행 | 52 | 47 + 5 |
| 서로 합치지 않는 대안 경로 | 3 | README 단독·README→첫 링크·README→둘째 링크 |
| 대표 후보 | 1 | SC-032·게시 원순번 32·JS-4 V만 해당 |
| 고유 응답 문서 | 3 | README·Schema 소개·meta-schema JSON |
| 본표 경로 판정 | 3 | 모두 미확인. 동일 README를 재사용하므로 세 명의 독립 독자나 독립 복제실험이 아님 |
| 빈 반환 비교 판정 | 15 | 47 빈자리를 47개 후보 실패로 세지 않음 |
| 예산 밖 진단 판정 | 1 | C2-only 연구 fixture, 본표 부분 점수와 분리 |
| 전체 judgments 행 | 19 | 빈 비교 15 + 경로 3 + 진단 1 |

52개의 window 행이 52번 원문을 연 것이 아니고, 경로를 합한 5행동이 한 사용자의 5행동 시행도 아니다. 현재 `within_budget`은 P1/P2에서 렌더링 창과 행동 수를 함께 명시하며 P3에서는 행동 수 2 준수와 JSON 창 경계 미확인을 분리한다. [원장](../../windows.csv)·[판정](../../judgments.csv)·[기계 검사](window-audit-receipt.json).

## 3. 첫 두 링크와 도착 문서

공급자 원문은 [README@d5199551f758ba067612979ae32ec35693640ccf](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md)다. 상태 배지는 첫 본문 제목 앞이므로 창에서 제외된다. 같은 Git 객체의 첫 본문 제목은 L3, 첫 정보 링크는 L8의 JSON Schema 홈페이지, 둘째는 L9의 `/schema`, 셋째는 L14–15의 nlohmann/json이다. 셋째를 더 유리한 구현 근거라는 이유로 앞당기지 않았다. 최초 `first-window-links.json`은 일부 위치를 한 줄씩 뒤로 적었으나 실제 URL 순서는 맞았으며, 감사 뒤 줄 위치가 8·9·14–15로 정정됐다.

| 경로 | action1 | action2 | 입증 가능한 범위 |
| --- | --- | --- | --- |
| JS-4-V-P1 | 고정 README | 없음 | 일반 C++·draft7·version2 설명. C1/C2 조건별 증거 미확인 |
| JS-4-V-P2 | 같은 README 응답 | `http://json-schema.org/` → `https://json-schema.org/` | 일반 소개와 커뮤니티 정보. SC-032 판별 구현 증거 미확인 |
| JS-4-V-P3 | 같은 README 응답 | `http://json-schema.org/schema` → `https://json-schema.org/draft/2020-12/schema` | 전송은 복구됐지만 제목 기준 창은 미정. 특정 구현 성적이 아님 |

README가 draft7이라고 설명하는 둘째 링크는 관측 당시 2020-12 meta-schema로 이동했다. 정확한 링크의 최종 판을 확인하지 않고 draft7 구현 증거로 취급하면 틀리는 실제 반례다. 이 문서는 168단어 JSON이며 `title` 속성이 있다는 사실과 HTML/README의 첫 본문 제목 아래 읽기 창이 정의됐다는 사실은 같지 않다. 제목 없는 문서의 전체 첫500단어를 허용하는 규칙은 사전에 없었다. 따라서 HTTP/MIME 실패 복구를 창 경계 복구로 올리지 않았다. [동일 URL 전송 복구 기록](../windows/schema-json-retry.json).

같은 문서의 전송 재시도·redirect는 별도 문서 action으로 세지 않는 사전 추상화다. 실제 네트워크 요청 수, 목록의 Load More·모달 클릭, 인간 독자의 UI 클릭 수를 측정한 것은 아니다. 최종 보고에서도 “두 번의 원문 열람 모델”이라는 범위를 유지해야 한다.

## 4. 발견한 500단어 추출 결함과 정정

사전 SCOPE는 GitHub URL의 README **렌더링 본문**을 첫 문서로 삼았다. 그러나 최초 창은 raw Markdown의 독립 `#` 표식과 code fence까지 공백 단어로 세었다. 이 때문에 v1은 상한을 넘긴 창이 아니라 지정한 본문 500단어보다 짧은 창이었다. 같은 응답에 대해 설치된 `pandoc 3.1.11.1`의 GFM→HTML 출력에서 첫 h1 이후 텍스트 노드를 추출하여 검산했다. 문단 경계는 공백으로, 코드 내용은 본문 단어로 세고, 태그·href 대상·Markdown 구문은 세지 않았다. 브라우저 레이아웃·줄바꿈을 실측했다는 뜻은 아니다.

| 문서 | v1 | v2 | 새로 들어온 내용 | 판정 변화 |
| --- | --- | --- | --- | --- |
| 고정 README | raw500·렌더487, L3–99 | 렌더500, L3–106 첫 단어까지 | 공유 라이브러리 기본값·CMake 옵션과 다음 문단 시작 | 첫 두 URL 동일. C1/C2·완결/부분 변화 없음 |
| 원래 홈페이지 응답 | raw500·렌더479, web L6–96 | 렌더500, web L6–105 | 2026-12-29와 2027-01-05의 예정 커뮤니티 행사 | 구현·판·두 조건의 증거가 새로 생기지 않음 |

README는 L105까지 499개 렌더링 단어이며 L106에서 500번째가 나오는 것을 prefix 렌더링으로 확인했다. 홈페이지는 루트가 보존한 **동일 최초 web 응답** `turn457540083view0`의 L6–185를 받았다. 그 raw 첫500단어 문자열이 기존 v1 창과 완전히 동일한지 먼저 검사했다. 이후 시점의 홈페이지로 대체하지 않았다. 원래 응답 전체에는 raw 678단어가 있다. [README v2 영수증](SC-032-rendered-window-v2.json)·[홈페이지 v2 영수증](SC-032-home-rendered-window-v2.json).

검토자의 최초 권고는 v1 관측을 그대로 두고 렌더링 재계산을 사후 경계 감도로만 남기는 보수적 처리였다. 루트는 사용자가 지정한 렌더링500 규칙을 끝까지 적용하기 위해 **규칙 변경이 아닌 기계 추출 결함 정정**으로 v2를 최종 원장에 채택하기로 했다. 두 판단의 차이를 숨기지 않는다. 같은 고정 원문·같은 첫 두 링크에서 결정적으로 경계만 재계산했고, v1도 보존하며 전후 결과가 같다는 근거는 확인했다. 다만 정정 때는 연구자가 이미 추가 공급자 본문과 시험 진단을 읽었으므로 v2를 비노출 상태의 최초 관측이라고 표시할 수 없다.

감사 종료 직전 실제 원장에는 `WIN-01-V2`, `WIN-02-V2`와 해당 L106/L105 경계가 반영됐고, v1 receipt는 남아 있었다. SCOPE와 FINDINGS에도 사후 노출·추출 결함·전후 무변화가 추가됐다. 단계3 게시 이후에는 결과판의 그 파일들이 실제로 봉인됐는지 다시 확인할 필요가 있다.

재생 명령:

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/review/render_window_check.py
python -B docs/workstreams/research/AF-RES-056/evidence/review/window_audit.py
```

첫 명령은 고정 공급자 checkout을 입력으로 사용한다. 홈페이지 재생은 최초 web 응답의 `evidence/transient/home-parsed-full.json`도 있을 때만 한다. 새 홈페이지 응답을 같은 입력이라고 간주하면 안 된다. 완전한 문서·500단어 발췌는 transient에만 두고 영구 감사에는 hash·위치·계수·자체 요약을 남겼다. README는 별도로 MIT 라이선스를 확인했지만 배포물의 원문 중복을 줄이기 위해 그 500단어 발췌도 transient로 옮겼다.

## 5. hash와 판을 섞지 않았는가

v1 창 receipt의 SHA256는 **말미 LF를 제외한 문자열**에 대한 값이고 transient 파일에는 LF가 하나 더 있었다. 두 창 모두 파일 끝 LF 하나를 제거하면 receipt hash와 정확히 일치했다. README 전체의 connector 텍스트 hash 차이도 canonical Git blob에 LF 하나를 더한 값으로 재현된다. 새 v2 receipt에는 문자열 hash와 말미 LF가 있는 파일 hash를 따로 적었다. 이는 내용이나 판 변경이 아니다.

세 경로의 구현 문서는 같은 고정 Git SHA다. 그 창은 version2와 과거 API 호환 설명을 보여 주지만 build판 2.4.1의 근거는 뒤에 별도로 읽은 CMake 선언이다. 이 정확판 정보를 최초 두 행동 안에서 보았다고 소급하지 않았다. 두 번째 도착 문서는 구현판을 가진 공급자 문서가 아니며, 구현 이름·일반 표준·동일 SHA를 섞어 한 구현의 두 조건 증거로 합치지 않았다.

## 6. 예산 밖 C2 시험을 성공으로 올렸는가

그런 합산은 없다. 본표 세 경로의 source ID는 README와 첫 두 문서로만 구성된다. enum 구현 코드 `WIN-06`과 실제 C++ 실행 `EXEC-SC032`는 `OUTSIDE-BUDGET` 진단 행에만 들어간다. [판정 원장](../../judgments.csv)의 본표 18행과 예산 밖 1행이 분리돼 있다.

실행 receipt에는 고정 공급자 SHA, nlohmann/json 의존 SHA, g++14.2.0, fixture hash, 컴파일 명령·stderr·종료 코드와 run stdout이 있다. 실행된 fixture의 현재 hash와 기록 값이 일치하고, stdout JSON은 `cases`와 일치한다. 관측은 string 허용·array 거절·존재하지 않는 pii 이름 수락이다. 이는 **의도적으로 C2만 넣은 연구 schema**의 양성·근접 음성 시험이다. 존재하지 않는 pii를 수락했다는 결과는 이 schema를 완전한 해답으로 취급하는 추론을 반증하지만, 라이브러리로 C1을 구현할 수 없음을 증명하지 않는다. [fixture](../windows/schema_fixture.cpp)·[실제 실행 receipt](../windows/sc032-execution.json).

추가로 field 이름 `desired_full_contract_accept`가 범위를 과하게 표현하는 문제를 지적했다. 해당 fixture는 원문 name/description 값 존재 guard를 입력에 재현하지 않았다. 따라서 그 bool은 **두 분석조건 C1/C2에 대한 연구자의 기대값**으로 해석해야 하며 원문 전체 계약의 양성 실행으로 읽을 수 없다. 원래 code·stdout을 소급 바꾸지 않고 루트가 해석 정정을 추가한 것을 확인했다. 원문 Python 프로그램, 제품판, guard의 정확한 의미와 실제 지원은 여전히 미확인이다.

## 7. 결론을 뒤집으려 시도한 경계와 남는 한계

| 반증 시도 | 실제 확인 | 결론이 달라질 조건 |
| --- | --- | --- |
| 첫500의 빠진 13·21개 표시단어에 조건 근거가 있었는가 | README 빌드 설정·홈페이지 행사만 추가됨 | 같은 고정 응답의 정정된 500번째 경계 안에서 C1/C2의 구현판 근거가 새로 발견되는 경우 |
| 두 번째/세 번째 정보 링크를 잘못 골랐는가 | 순서는 홈페이지→meta-schema→nlohmann이며 첫 둘만 사용 | 첫 두 링크 정의나 source 구조가 달라져야 함. 결과에 유리한 셋째 링크를 이번 본표에 넣을 수 없음 |
| 세 경로의 증거를 합쳐 한 번의 성공을 만들었는가 | 각 판정 source ID가 해당 trial의 action source와 정확히 같고 모두 미확인 | 실제 한 trial 안에서 같은 구현·판·환경의 두 조건이 확인될 때만 완결로 변경 |
| C2 실행을 본표 부분 성공이나 원문 전체 성공으로 올렸는가 | 예산 밖 행으로 분리, oracle 범위 과장은 해석 정정 | 해당 시험이 허용 창에 직접 들어오고 원문 환경·guard까지 맞춰질 경우. 현재는 해당 없음 |
| JSON 전송 성공을 유효한 판독창으로 오인했는가 | 168단어 문서는 읽었지만 제목 경계 미확인 유지 | 제목 없는 자료의 경계를 사전에 정한 별도 실험에서 다르게 평가 가능. 이번에 전체를 사후 읽어도 특정 구현 증거는 없음 |

실제 독자의 클릭·선택·채택은 관측하지 않았다. 홈페이지의 원래 전체 응답은 저작물 중복 보존을 줄이기 위해 transient에 있으며, 훗날 같은 live URL이 바뀌면 hash만으로 그 본문을 복원할 수 없다. 이것은 저장된 receipt와 고정 README의 재현성 차이로 남는다. 기능 증거가 없다는 현재 판정이 소프트웨어 자체의 기능 부재나 단어 연결의 일반적 무효를 뜻하지도 않는다.

## 가장 중요한 감사 약점 세 건

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| 최초 raw500은 렌더500과 달랐고 수정 시 추가 본문 노출이 있었음 | 처음부터 정확한 동일500단어 예산을 적용했다는 주장 | README L3–99→L106; 홈페이지 webL6–96→L105; review v2JSON·SCOPE 정정 | 단계3 원격 판에서 v1/v2·수정시점·최종 창 범위가 함께 보존됐는지 확인 | 실제 렌더500 안에 두 조건 근거가 있거나 v2 기록이 다른 시점 응답을 사용한 것으로 드러날 때 |
| P3는 두 action이지만 제목 없는 JSON의 창 경계가 미정이고 draft7 링크가 2020-12로 이동 | 세 경로 모두 같은 판의 유효한 두 문서 창을 확보했다는 주장 | 고정 README L9; schema-json-retry.json final_url·window_rule_status | 제목 없는 응답 경계는 별도 사전 규칙으로 정하고 동일판 목적지의 유무를 조사 | 유효한 허용 창·같은 구현판의 C1/C2 근거를 확보한 경우. HTTP200만으로 바뀌지 않음 |
| C2-only 시험의 full_contract 이름이 원문 guard보다 넓은 성공을 암시 | 원문 전체 요구를 양성·음성으로 실행 검증했다는 주장 | schema_fixture.cpp의 세 사례; sc032-execution.json cases; fixture-scope-correction.json | 원문 Python 판·입력의 name/description guard 의미부터 고정 | 모든 원문 guard와 두 조건을 동일 구현·판·환경에서 함께 확인할 때. 현재 본표에는 더하지 않음 |
