# AF-RES-229 반례와 변경 기록

| 처음 검사한 설명 | 실제로 반박을 시도한 위치 | 관측과 남은 조건 |
| --- | --- | --- |
| 같은 호환 범위에서 높은 판이 항상 선택된다 | `>=8.0.2,<8.1.1`의 두 인덱스와 같은 wheel 파일 route·지문. [기준](receipts/main/range-exclusive-baseline-r1/) · [제거](receipts/main/range-exclusive-unmarked-r1/) | 철회 속성 하나를 삭제하자 8.0.2 → 8.1.0. 두 쪽의 선택 경고는 0. 8.1.1이 들어오는 범위에서는 제거 전후 8.1.1을 선택했다. |
| 정확판은 철회·누락 두 경우 모두 실패한다 | 같은 정확 요청. [사유 포함](receipts/main/pin-target-baseline-r1/) · [링크 누락](receipts/controls/pin-target-missing-r1/) | 기준은 파일 GET과 report, stderr 경고 1 및 종료 0. 링크만 뺀 페이지는 GET 200이지만 wheel GET/report 0, 두 resolver 오류, 종료 1. 링크 부재 조건에서는 저장된 wheel과 서버 파일 route를 유지했다. 미러의 노출 방식을 비교한 결과다. |
| 철회 사유를 지우면 항상 경고가 사라진다 | `data-yanked=""` 및 속성 미포함을 정확 요청으로 대조. [빈 값](receipts/controls/pin-target-empty-r1/) · [부재](receipts/main/pin-target-unmarked-r1/) | 같은 8.1.0 wheel과 SHA를 읽었다. 빈 **HTML** 값의 report flag는 true이며 stderr의 치환 사유는 `<none given>`이다. 속성을 빼면 flag false와 stderr 0 B다. JSON은 사양에서 bool true를 무사유 표시에 사용하고 문자열은 비어 있지 않아야 한다. [R03](https://packaging.python.org/en/latest/specifications/simple-repository-api/) · [P03](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/models/link.py#L262-L363) |
| PyPI 배너에 경고가 있으면 새 범위 선택에서도 같은 경고가 나온다 | 기본 16회의 raw stderr, 범위 r1/r2 및 정확 핀 r1/r2와 2024년 cache 기록. [실행 원장](matrix.csv) · [H01](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847) | 이 resolver는 철회 후보를 건너뛴 성공에 선택 경고 0, 실제로 선택할 때 1을 냈다. 당시 로그는 cache wheel 설치 성공이라는 별개 증거다. 다른 미러는 후보를 숨길 수 있고 규격은 설치기가 철회 파일을 거절하는 것도 허용한다. [R02](https://packaging.python.org/en/latest/specifications/file-yanking/) |
| 비철회 후판이면 영향을 받은 도구가 모두 회복된다 | 시험 범위 밖의 plugin 원기록과 수정판 발행자 기록. [D09](https://docs.pytest.org/en/8.1.x/changelog.html#pytest-8-1-1-2024-03-08) · [H04](https://github.com/pytest-dev/pytest/issues/12061) · [H05](https://github.com/pytest-dev/pytest/issues/12069) | 8.1.1의 보완은 두 path 관련 제거의 복원이다. #12069의 별도 사용자는 8.1.1에서 사설 `call_runtest_hook` 제거가 남았다고 보고했다. 하류 fork 한 곳은 8.0.2로 돌아갔다. [H02](https://github.com/hrushikesh-s/atomate2/commit/4e90106a626a0697a04baf5f9b1c9907bde4006b) |
| 원 DOI가 열리고 별도 후속 DOI가 보이면 계속 같은 방식으로 인용할 수 있다 | 전체 철회 공고·원문·색인 3개를 정정 공고·원문에 대조. [X01–X08](sources.jsonl) | 전체 철회 사례는 원문을 읽을 수 있고 색인도 별도 공고 DOI를 연결하지만 상태는 Retraction이다. 정정 사례는 수정 범위를 따로 제시한다. PLOS는 예외로 내용이 내려가도 식별 메타데이터를 남긴다. 상태 종류와 목적을 원 DOI 접근 여부와 함께 보아야 한다. |

## 정정 및 재생 범위

- 기본 묶음의 16개 파일 선택·경고 판정 변경 0. 보조 2행은 기본 분모 밖에 추가했다. `missing`에는 보고 파일이 생성되지 않았으므로 report의 `is_yanked` 항목은 해당 없음이다.
- 원장 위치·확인 UTC를 고정 원문 재열람으로 보완했다. 계산에 쓰인 원응답·wheel SHA·기대값은 첫 두 커밋의 입력과 같다. 200의 자체 PARTIAL과 중앙 DONE은 간접 선행의 표시 불일치다. 이번 착수 판단은 중앙과 실제 브랜치가 일치한 216과 216의 네 원응답을 사용했다.
- 같은 코드·wheel·fixture를 새 임시 venv로 재생한다. 로컬 포트·시각·임시 경로를 정규화하고 파일·SHA·상태·경고 채널과 사유·종료·GET 수를 비교한다. 처음 출력과 다시 얻은 원출력을 따로 보존한다. [재생 검산](receipts/replay-audit.json)
