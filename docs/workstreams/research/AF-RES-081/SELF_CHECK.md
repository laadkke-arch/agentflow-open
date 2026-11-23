# AF-RES-081 자가검산

| 질문 | 확인한 주장 및 근거 | 반대 근거를 찾은 경로와 결과 | 빈자리와 최소 확인 |
| --- | --- | --- | --- |
| Q1 | PR의 작성자·선택 음표 ghost 설명, 두 부모와 첫 부모의 한 줄 변경, 복사 멤버와 release/tree SHA를 확인했다. [MS-PR, MS-MERGE, MS-TAGS](sources.jsonl) | tracker 직접 열람·locale 경로·revisions·archive 시도가 원 본문을 반환하지 않았다. 077의 부분 cache를 보존하되 affected installer의 동등성을 주장하지 않았다. [시도](evidence/access-attempts.jsonl) | 최초 tracker 및 3.0/2.3.2 설치 지문 확보 후 같은 File→Parts 조작 |
| Q2 | dialog→createExcerpt→cloneStaves→Chord 가상 override→Note/자식의 호출을 확인했다. E01 화면과 모델 경계 통과, E05 unlinked clone을 실제 실행했다. [E01](evidence/runs/01-E01-U/r1/stdout.jsonl) · [E05](evidence/runs/13-E05-U/r1/stdout.jsonl) | `addClone`의 별도 clear, Explode의 분기·재선택, clipboard MIME/XML의 대조를 따라갔다. 같은 UI 명칭이나 API 이름으로 분기를 가정할 수 없었다. [MS-COPY-OUTSIDE](sources.jsonl) | E05 인자와 일치하는 사용자 입력 및 후속 선택 목적 확인 |
| Q3 | 즉시 raw 주소와 멤버십을 재결합하고 mark, color, visible·printing·drop-target을 읽었다. 새 master 주소와 XML의 stable position, link를 대조했다. [E06](evidence/runs/16-E06-U/r1/stdout.jsonl) | E06의 선택 없는 선택색과 UI Inspector의 U/G/L 동률을 찾았다. Raw 세 빌드의 저장 bytes 역시 E01의 차이를 숨겼다. [픽셀](evidence/desktop-pixels.json) · [저장 악보](evidence/runs/) | 다른 voice color, 실제 재생 중 mark, printing/drag의 경합은 별도 입력 |
| Q4 | 사전 저장된 E01–E06, fixed SHA, source 두 Part, 반증 시점, 12 모델 셀과 6 API 셀을 검산했다. [cases.csv](cases.csv) | E02가 원판의 비선택 대조다. E03은 root-only reset 가정을 약화하고, E05의 최소 변경으로 G/L을 구별했다. E06은 색만 쓰는 검사를 실패시킨다. | 가려진 tag를 품은 자식과 둘 이상의 실제 staff·voice mapping 입력 |
| Q5 | 01–18에 두 번씩, empty cwd·별도 Qt config·같은 fixture 지문과 exit를 읽었다. 누락 단계나 판독 불가 원장이 0이었다. [runs.jsonl](runs.jsonl) · [판독기](tools/compare.py) | U/G 4차이, U/L 3차이, G/L 1차이와 저장결과 6동일로 cross-check. fresh rebuild의 36회도 같은 normalized stages/MSCX SHA였다. [재실행](evidence/replay/) | E01 화면 6회는 별도. E02–E04 full GUI, E05 직접 UI 분모에는 실행 없음 |
| Q6 | U E01/E04는 신고 조건 위반. G/L은 그 조건을 만족한다. E05에서 G는 clone ghost 해소, L은 외부 복제 비트 보존, 원본 M1 selection은 셋 모두 유지. [E05-G](evidence/runs/14-E05-G/r1/stdout.jsonl) · [E05-L](evidence/runs/15-E05-L/r1/stdout.jsonl) | 원 suite G/L 14/14 통과, 후대 #22320의 explicit selection, #33610의 영속 표시값, #11212·#15590의 범위 입력을 확인했다. E05 비트를 유지해야 할 당시 소비자 계약을 찾지 못했다. [원시험 요약](evidence/original-summary.json) · [독립 사건 원장](sources.jsonl) | 멀티성부 Tools→Explode에서 초기에 복사한 음과 명령 종료 후 사용자가 실제 편집하는 음을 짝지어 확인 |
| Q7 | TEI active witnesses, 실제 Versioning Machine pane, Blender object/base와 explicit selection, Qt per-view/shared 선택 모델을 각 원문에서 읽었다. [TEI-48, VM-FAITH, BLENDER-DUP, QT-MODEL-VIEW](sources.jsonl) | lacuna/overlap, Qt opt-in 공유, Inkscape source 색 고정, ProseMirror selection serialization 및 Krita flatten을 비교했다. | 특정 편집기의 모든 레이어에 하나의 초기화 정책을 적용할 근거는 더 필요 |
| Q8 | 같은 첫 부모 재구성 및 G diff 검사, CTest 21/21, native 36/36, 화면 6/6, fresh native replay 36/36을 행동별로 대조했다. [빌드](evidence/build/) · [기존 suite](evidence/original/) · [재현](reproduce.md) | Ninja cycle, GCC DTL, Qt desktop enum·resource 복구의 실패와 재시도를 보존했다. 공식 릴리스 ZIP의 bytes와 역사 CI 실행 로그는 확보하지 못했다. | archive 빌드의 본래 toolchain과 reporter 설치물을 찾을 때 현재 재구성의 비교를 다시 평가 |

소스 표본은 43행, 고유 외부 계보 28, 다른 분야 13, 독립 실패·무변화 8이다. 실패한 원문 조회와 077 내부 결과는 이 계보에 산입하지 않았다. 원 사례·코드·시험·실제 악보가 모두 들어 있다.

## 재계산 항목

- 첫 커밋의 `cases.csv`와 `SCOPE.md`는 결과 판독 뒤 바뀌지 않았다. fixture SHA와 네 native 패치 SHA를 재계산했다. G는 실제 부모 diff와 비교했으며 L은 실험 구현이다. GUI compatibility patch는 추가 desktop 전용이다.
- 36회에 198개 시점 기록이 있고 108개 원 파일의 SHA·크기와 위치를 확인했다. 실제 포인터 목록에서 얻은 0/1과 probe가 쓴 membership을 대조했다. M1·P1, M2·P2와 fingering의 링크가 대칭이었다. 재열림 객체 주소가 새로 배정되고, 위치 키가 유지됐다.
- 18/18 셀에서 두 반복의 normalized 출력과 저장 SHA가 일치했다. 6/6 입력의 저장 SHA는 U·G·L 사이에도 일치했다. 발행한 표 2의 18행을 validator가 원장과 JSON에서 다시 만들었다.
- CTest exit와 21개 `result.xml`의 각 testcase 결과·failure/error element를 읽었다. `errors` attribute의 진단 수는 원본 XML에 저장했다. UI proof는 PNG hash, 입력 SHA, 스크립트 exit와 픽셀 범위를 확인했다.
- 화면 반복 6회는 New All 경로의 관측이다. native 전체 및 fresh 재실행의 분모를 각각 유지했다. E03 핑거링의 mark는 형식상 적용 불가에 해당한다. 36회에서 기대와 다른 판독 항목 0, 실행 실패 0, 판독 불가 0이었다.
- 독립적인 제3자 검토는 미실시다. 이 검사는 원시 기록에 의존한 자가검산이다.

```bash
AF081_PACKET=docs/workstreams/research/AF-RES-081
python -B "$AF081_PACKET/tools/compare.py" --format markdown
python -B "$AF081_PACKET/tools/verify.py" --pixels --replay "$AF081_PACKET/evidence/replay"
python -B -m workbench.session check "$AF081_PACKET/manifest.json" --fetch
```

[기계 검산 영수증](evidence/verify.json) · [재실행 시간](evidence/replay/start_utc.txt) · [재실행 원장](evidence/replay/runs.jsonl).
