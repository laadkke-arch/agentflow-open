# AF-RES-100 · jq 사후 행동과 반환 링크

사전 봉인은 `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`이다. 그 판의 J1–J4 요구를 먼저 읽은 뒤 **2026-11-23T20:25:18.093231Z**에 첫 후속 API 요청을 시작했다. 이 문서는 봉인한 정책·패킷·완결 판정을 바꾸지 않는다. 외부 원문은 임시 `_cache`에만 보존하며, 재열람 주소·payload 식별자·SHA-256·짧은 해석은 `sources.jsonl`에 남겼다.

## 후속과 실행 귀속

| 사례 | 최초 답과 수정판 | 현재 채택 | 30일 내 질문자 행동 | 동일판·원입력·정확 출력의 실행 확인 |
| --- | --- | --- | --- | --- |
| J1 · 79694539 | API에 공개 답 0개. 최초 답 revision은 공석이다. | 없음 | `inputs[]`로 오류는 없어졌지만 JOIN은 안 된다고 반박했다. [댓글 140577987](https://stackoverflow.com/questions/79694539#comment140577987_79694539) | 미확인. 부분 file2만 있고 전체 두 입력·jq판·최종 출력이 없다. 오류 없는 종료는 요구 성공이 아니다. |
| J2 · 79699191 | 첫 답 79699725는 질문자 자기답. [최초판](https://stackoverflow.com/revisions/CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A/view-source)의 배열 길이 가설을 [수정판](https://stackoverflow.com/revisions/5931D56D-480F-4826-9124-71C9BDE946CB/view-source)에서 EventData/UserData 구조 차이로 교정했다. 후발 답 79700162도 첫판과 확장판을 읽었다. | 79700162 · yq로 pipeline을 재작성하는 답 | 두 제안의 null/string 오류를 보고하고, 일부 null 필드 횟수를 제시했다. 자기답을 고치며 원 R0에 없던 UserData 이벤트를 밝혔다. | 미확인. 자기보고·진단 출력은 있으나 전체 Security.json·판·최종 변환 결과가 없다. 채택 답의 단일 Event XML은 답변자 예제다. |
| J3 · 79711268 | 첫 답 79711304의 [최초·현재 동일판](https://stackoverflow.com/revisions/D0B335C6-803E-4397-9B63-6FB8F341D246/view-source)은 `inputs`와 인용한 `$@`를 사용한다. | 없음 | 처음에는 `$@` 대신 JSON 내용 변수를 넣어 파일명 오류를 냈다. 설명 뒤 추가 JSON 파일 1개에서 작동했다고 [질문자 댓글 140613190](https://stackoverflow.com/questions/79711268#comment140613190_79711304)에 보고했다. | 부분적인 성공 자기보고. 원문에는 jq 1.7·Ubuntu 24.04.2·WSL2가 있지만 후속의 실제 argv·최종 JSON·실행판 로그가 없어 엄격 확인은 미확인이다. |
| J4 · 79727040 | 첫 답 79727098의 [최초판](https://stackoverflow.com/revisions/53C19479-AE75-4E7C-B257-C76836AE1792/view-source)은 괄호와 from_entries, VolName·null Iops 출력을 제시한다. [수정판](https://stackoverflow.com/revisions/36D141D1-35DA-4E57-A1DC-E6DBFE382ED4/view-source)은 우선순위 설명을 보충한다. | 79727098 | 질문자가 최초 답 이전 [revision 5](https://stackoverflow.com/revisions/9D6F0AC7-7630-4A2F-9890-F26C78B073F1/view-source)에서 Tags.Name을 Tags.Key로 고치고 추가 태그가 있음을 명시했다. 질문자 댓글은 0개다. | 미확인. 채택과 답변자의 출력 예시만 관측했으며 질문자 실행 보고는 없다. |

원장에서 재계산되는 값은 **공개 답 4개/답이 있는 질문 3개, 현재 채택 2/4, 30일 내 질문자 댓글 또는 자기답 3/4, 질문자 질문 수정까지 포함한 후속 4/4, 엄격 동일판·전체 원입력·정확 출력 확인 0/4**다. 21개 revision 항목 중 본문이 있는 것은 16개다. 공개 댓글은 15개이며 30일 밖 댓글은 J1의 제3자 추측 1개다. 이 값들은 API에 현재 공개된 기록의 개수다. 삭제 답·삭제 댓글·댓글의 과거 수정·채택 변경 시각을 완전히 복원한 값은 아니다.

현재 채택은 질문/답 API metadata로 읽었다. 이를 특정 시점의 채택 사건이나 실행 성공으로 바꾸지 않았다. 공개 사용자를 질문자·답변자·제3자 편집자/댓글 작성자로 구별했고 **도구 유지관리자라고 검증된 사람은 없다.** 점수·추천은 실행 근거로 수집하지 않았다.

## 가장 중요한 사후 차이

### J1: 오류를 없앤 동작과 JOIN 목적이 다르다

질문자의 후속은 `inputs[]` 사용이 오류 없는 종료를 만들었지만 원하는 JOIN을 만들지 못했다고 말한다. 최초 원문이 요청한 것은 디버깅을 더 진행할 방법이며, 두 전체 파일이 없어 실제 오류의 유일 원인이나 최종 JOIN 결과는 확인되지 않았다. 사전 주 조건인 중간입력 관측과 강화 민감도인 실제 JOIN 성공을 합치지 않아야 한다. [질문자 후속](https://stackoverflow.com/questions/79694539#comment140577987_79694539)

2025-10-13의 제3자 댓글은 비인쇄 문자·stream 제어를 원인 후보로 추측한다. 질문으로부터 약 97일 뒤이며 실제 재현이 아니다. 30일 질문자 후속이나 확인된 원인으로 세지 않았다. [해당 댓글](https://stackoverflow.com/questions/79694539#comment140793862_79694539)

### J2: 자기답의 성공보고도 원뜻과 입력 범위를 대조해야 한다

첫 자기답은 `Event[0-(Event|length)]`를 배열 길이를 지정한 반복이라고 설명했다. 고정 jq 매뉴얼의 정수 인덱스·음수 인덱스·colon slice 정의에 비추면 이는 여러 Event를 순회하는 표현이 아니라 **단일 Event를 지정하는 표현**이다. 이는 문서에 따른 정적 해석이며 이 조사에서 명령을 실행한 결과가 아니다. 따라서 당시 무오류 실행 자기보고를 모든 Event의 완결된 변환으로 세지 않는다. [자기답 최초판](https://stackoverflow.com/revisions/CE0C3B2C-23EA-43DE-8F89-4B01A7CC654A/view-source), [jq 고정판 Array Index/Slice](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L468-L501)

수정 자기답은 일부 Event에 EventData 대신 UserData가 있었다고 밝혔다. 이는 R0에서 추정했던 content 결손과 다른 구조 결손이다. 수정판에 진단 출력과 `?` 사용이 있지만 원 전체 데이터·판·최종 변환 결과는 없다. 후반부에는 다른 필터의 미해결 동작도 남아 있다. [자기답 수정판](https://stackoverflow.com/revisions/5931D56D-480F-4826-9124-71C9BDE946CB/view-source)

현재 채택 답은 sed와 jq를 줄이고 yq의 XML 옵션으로 바꾸는 대안을 제공한다. 수정판의 예제는 단일 Event의 Data를 사전으로 바꾸며 CommandLine은 null이다. 이는 FALSE/TRUE 의미를 확인한 원 EVTX 실행이 아니다. 답에 붙은 yq 문서·데모 링크 자체는 여기서 추가 열지 않았고, 명령·출력은 답변자에게만 귀속했다. [채택 답 수정판](https://stackoverflow.com/revisions/7AFEF78E-3B19-4DE1-8B20-FEB85A0491A7/view-source)

### J3: 먼저 명명된 출력 소비자와 실패한 실행 경계가 다르다

사전 규칙은 본문의 명명 순서 때문에 Windows Terminal을 선택했다. 실제 공개 후속은 JSON 설정을 소비하는 앱보다 **Bash가 jq에 어떤 argv를 넘겼는가**를 설명한다. `$@`를 JSON 내용으로 바꾼 실패 보고와 파일 인수 그대로 사용할 때의 성공 보고를 모두 보존했다. 앞선 설명에 대한 짧은 감사 댓글을 정확한 명령 실행의 증명으로 쓰지 않았다. [실패 보고](https://stackoverflow.com/questions/79711268#comment140613110_79711304), [답변자 설명](https://stackoverflow.com/questions/79711268#comment140613115_79711304), [질문자 성공 자기보고](https://stackoverflow.com/questions/79711268#comment140613190_79711304)

추가로 GNU Bash **5.2**의 공식 배포 archive에서 `doc/bashref.texi`를 읽었다. 공식 배포 index의 해당 artifact 시각은 2022-09-26으로 J3 이전이다. 실제 사용자 Bash판을 확인한 것은 아니다. 5.3 archive의 현재 index 시각이 질문 이후인 2025-07-30이라 그 metadata만으로 질문 이전을 단정하지 않고 5.2를 사용했다. Single/Double Quotes, Special Parameters의 `$@`, Word Splitting 절은 인수 생성 경계를 설명한다. 이 자료는 **32패킷 모두의 밖에서 사후에 연 보조자료**다. B를 Bash로 재순위하거나 초기 승패를 고치지 않았다. [고정 archive](https://ftp.gnu.org/gnu/bash/bash-5.2.tar.gz), [공식 배포 index](https://ftp.gnu.org/gnu/bash/)

### J4: 후속 원뜻 정정은 실행 확인과 별개다

질문자는 2025-08-06 09:14:23Z에 Tags.Key=VolName으로 직접 정정했다. 이는 최초 답보다 앞서며, 다른 태그도 있으므로 version만 제외해서는 안 된다고 덧붙였다. 봉인한 주 해석을 사후에 지지하지만 사전 근거로 역수입하지 않는다. 답변자가 제시한 Iops=null도 원 질문자의 실제 AWS·jq 실행 결과로 바꾸지 않는다. [질문자 revision 5](https://stackoverflow.com/revisions/9D6F0AC7-7630-4A2F-9890-F26C78B073F1/view-source)

## 반환 카드: 질문별 최대 두 링크

아래는 **사후 반환 제안**이다. 초기 발견률·패킷 충분성의 새 성공으로 세지 않는다.

| 사례 | 반환 링크·볼 절 | 실패 조건 한 줄 |
| --- | --- | --- |
| J1 | [jq 1.7.1 고정 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L3238-L3304): input/inputs, debug, input_filename, input_line_number | 중간값·입력 소비 순서를 보지 않고 오류만 제거하면 JOIN 목적을 놓칠 수 있다. |
| J2 | [jq 고정 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L441-L559): 선택적 접근, 정수 인덱스/슬라이스, `.[]?`; 추가 절 from_entries L1157–1169·update-assignment L3410–3431. [yq 대안의 고정 답 revision](https://stackoverflow.com/revisions/7AFEF78E-3B19-4DE1-8B20-FEB85A0491A7/view-source): XML 옵션·Data 사전 예제. | EventData 부재와 content 결손을 구분하며, 단일 Event 예제를 전체 EVTX 처리 성공으로 세지 않는다. |
| J3 | [jq 고정 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L240-L263): JSON/파일 인수 옵션·inputs L3249–3259. [Bash 5.2 archive](https://ftp.gnu.org/gnu/bash/bash-5.2.tar.gz): `doc/bashref.texi` Single/Double Quotes L439–472, `$@` L1850–1870, Word Splitting L2725–2767. | 파일명 인수 목록 `$@`와 JSON 내용 문자열을 교환하면 입력 계약이 달라진다. |
| J4 | [jq 고정 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L561-L621): comma/pipe/parenthesis; from_entries L1157–1169 | 괄호 없이 sibling 값을 태그 필터로 보내거나 VolName 대신 다른 태그 조건을 선택하면 원 요구를 놓친다. |

| 사례 | 독자 관점 | 도구 유지관리자 관점 | 검색 결과 편집자 관점 |
| --- | --- | --- | --- |
| J1 | 입력 소비와 진단 절부터 읽는다. | 불완전 입력이 막는 확인 범위를 드러낸다. | clean exit를 JOIN 성공으로 요약하지 않는다. |
| J2 | envelope 종류와 결손 위치를 먼저 확인한다. | null content와 EventData 부재를 나눈다. | 자기답의 수정 전후와 yq의 다른 pipeline을 표시한다. |
| J3 | 파일명·JSON 내용·Bash 인수 목록을 구분한다. | argv 생성 단계와 출력 앱 소비 단계를 나눈다. | 실제 후속에 맞는 Bash 절을 반환하되 사후 개선임을 표시한다. |
| J4 | 괄호 범위와 Key=VolName을 확인한다. | 외부 API 실행 없이도 확인된 형식과 없는 값을 구별한다. | 채택·답변자 예시·질문자 원뜻 수정·실행을 분리한다. |

## 자료·재현과 미실시

`outcomes.jsonl`은 질문별 1행의 상세 귀속 원장이다. `sources.jsonl`의 **47행 모두 `count_minimum=false`**이며, 현재 질문4·현재 답4·revision21·댓글15·사후 보조자료3행으로 구성된다. 같은 current/revision 본문은 중복 여부를 표시했다. 보조자료3은 기존 고정 jq 매뉴얼 재열람, GNU 배포 index, Bash5.2 매뉴얼이다. 새로운 독립 47자료나 사전 하한 충족 47개라고 세면 안 된다.

원자료 재수집 절차는 `python -B docs/workstreams/research/AF-RES-100/evidence/outcomes/jq/fetch_outcomes.py`, 기록 재구성은 같은 경로의 `assemble_outcomes.py`다. 재수집은 현재 공개 상태가 바뀔 수 있으므로 기존 `_cache`를 별도 보존한 새 사본에서 해야 한다. 최초 수집은 `fetch-receipts.json`의 URL·UTC·응답 SHA-256에 고정된다. Bash·jq 매뉴얼의 archive/member·문자/바이트·행 범위는 별도 receipt와 sources에 있다.

원 사용자 명령, AWS 호출, 데모 링크, 과거 68질문, P4 렌더링은 실행·재조사하지 않았다. 이 사후 자료는 사람의 실행에 대한 귀속과 문서의 의미를 대조한 것이며, 새 런타임 실험 결과가 아니다.
