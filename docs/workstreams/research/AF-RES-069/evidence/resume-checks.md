# AF-RES-069 · 미실시 확인의 환경·명령·입력

아래 제품 검사와 원자료 복원은 **미실시**다. 실제로 실행한 것은 소스 읽기, 원장 검산, Git/session 계약 검사이며 각각 영수증을 구분한다. 이 파일은 실행 결과가 아니다. 다른 저장소를 현재 작업 범위 안에서 변경하지 않았다.

## 첫 행동: 원이슈 최초판과 당시 진행 상태 확보

필수 입력은 P1 `jupyterlab/jupyterlab#19647`, P2 `home-assistant/core#180207`, P3 `inkscape/inbox#13819`의 생성 시 본문과 변경 이력, 기준일 `2026-11-23T08:24:37Z`의 상태 증거다. 관측 body SHA-256과 날짜는 `../problems.jsonl`에 있다. GitHub REST의 `updated_at`이나 현재 body만으로 최초판을 확인했다고 하지 않는다.

현재 공개 API 응답을 다시 얻는 읽기 명령은 다음과 같다. 실행 환경은 공용 인터넷 접근과 curl을 가진 조사 환경이다. 출력은 해당 후속 작업의 허용 경로에 보존하고 HTTP 코드·UTC·본문 해시를 함께 기록한다.

```sh
curl --fail-with-body --location 'https://api.github.com/repos/jupyterlab/jupyterlab/issues/19647'
curl --fail-with-body --location 'https://api.github.com/repos/home-assistant/core/issues/180207'
curl --fail-with-body --location 'https://gitlab.com/api/v4/projects/inkscape%2Finbox/issues/13819'
curl --fail-with-body --location 'https://gitlab.com/api/v4/projects/inkscape%2Finbox/issues/13819/notes?per_page=100&sort=asc&order_by=created_at'
```

마지막 notes 요청은 이번 실행에서401이었고 공개 웹도 본문을 반환하지 않았다. 허용된 공개 수정 이력 또는 정당한 접근권한이 있는 담당자의 export가 필요하다. 같은 제한에 계속 재시도하거나 권한을 바꾸어 우회하지 않는다. 최초판을 제공하지 않는 endpoint 성공은 최초판 검증 성공이 아니다. P2는 신고자의 장치 반품 댓글5750354113을 함께 읽고, 현재 실제 시험 가능한 다른 당사자가 있는지도 별도 증거로 확인해야 한다. 상대에게 연락하는 작업은 이번 범위에 포함하지 않는다.

## P1: 고정 PR 코드의 회귀와 빠진 경계

환경: JupyterLab의 해당 revision 개발·test 의존성이 이미 설치된 별도 checkout, Python3.12, pytest. 보고자의 Windows11 / Python3.12.10 조건과 sys_prefix/system 경로 동일성을 별도 표시한다. 이 연구는 의존성 설치나 제품 실행을 하지 않았다.

입력: `JUPYTERLAB_CHECKOUT`에 외부 검증용 checkout 절대경로를 설정한다. 확인할 PR head는 `f12cea5b7d7296fabfabcb362005763a879ae06f`; 보고된 원문 code는 `9312e29b7bbc95ef905b96afe00c93361943f2f6`이다. 아래 Git 명령은 읽기만 하고 checkout을 전환하지 않는다.

```sh
git -C "$JUPYTERLAB_CHECKOUT" rev-parse HEAD
git -C "$JUPYTERLAB_CHECKOUT" show f12cea5b7d7296fabfabcb362005763a879ae06f:jupyterlab/commands.py
git -C "$JUPYTERLAB_CHECKOUT" show f12cea5b7d7296fabfabcb362005763a879ae06f:jupyterlab/tests/test_jupyterlab.py
```

검증용 checkout HEAD가 위 PR head와 같은 상태에서 그 checkout root를 실행 위치로 하여:

```sh
python -m pytest jupyterlab/tests/test_jupyterlab.py -k test_disable_extension_does_not_lock_it -q
```

이 한 테스트는 PR에 실제 존재하는 test 이름으로 확인했다. 하지만 이것 하나로 전체 조건을 통과했다고 하지 않는다. 추가로 검증할 입력 행렬은 다음과 같다. 명령/설정 조작은 임시 Jupyter 설정 경로를 사용하는 제품 테스트 환경에서 구현하고 원본 사용자 설정을 대상으로 삼지 않는다.

| 입력 ID | 초기값·순서 | 통과 관측 | 아직 없는 실행물 |
| --- | --- | --- | --- |
| P1-T1 | page_config 없음, disable, 새 handler 및 새 프로세스 enable | disable은 새 lock을 만들지 않고 다음 실행에서도 동일 | PR test는 handler 경계; 실제 프로세스·경로 조합 추가 필요 |
| P1-T2 | 기존 해당 항목 locked=True, disable | 기존 True 보존; 무조건 unlock은 탈락 | 고정판에서 실행한 trace 없음 |
| P1-T3 | 진짜 구판 disabled 항목 존재, locked 키 없음 | 구판 전환 의도 유지 | 작성자 수동 확인 보고만 있음 |
| P1-T4 | 초기 disabled 비어 있음, 빈 하위 dict 정리, 이후 새 disable | 새 항목을 구판으로 복사하지 않음 | 저장 후 재읽기·새 프로세스 trace 없음 |
| P1-T5 | sys_prefix=system / 서로 다른 경로 | 경로 중복과 계층 차이가 lock 불변을 깨지 않음 | 두 환경 실행·설정 전후 기록 없음 |

최소 재개 산출물은 고정 HEAD, 실제 cwd, 입력 fixture, stdout/stderr, 종료코드, 설정 전후 해시다. 작성자의 PR 테스트 보고를 이 명령의 실제 결과로 복사하지 않는다.

## P2: 실제 leaf 명령 계약의 확인

환경: Home Assistant Core2026.8.3 코드와 정확한 장치 조합. Mini firmware `v3.3.0.441_26022721`, Doorbell `v3.0.0.6543_26052720`, 현재 pairing 유지. Chime 모델/식별자와 동작 가능한 공개·인가된 API 경로는 아직 없다. 신고자는 Mini를 반품했으므로 원 신고자 환경에서 바로 재현 가능하다고 가정하지 않는다.

`HA_CORE_CHECKOUT`은 별도 읽기용 저장소 경로다. 우선 지원 파일과 Chime 경로를 확인한다. tag 존재와 resolved SHA를 기록하고 잘못된 tag를 다른 버전으로 조용히 대체하지 않는다.

```sh
git -C "$HA_CORE_CHECKOUT" rev-parse 2026.8.3
git -C "$HA_CORE_CHECKOUT" ls-tree -r --name-only 2026.8.3 -- homeassistant/components/reolink
git -C "$HA_CORE_CHECKOUT" grep -n -i -E 'chime|volume' 2026.8.3 -- homeassistant/components/reolink
```

실제 setter endpoint를 확인하지 않았으므로 허구의 curl 쓰기 명령을 제공하지 않는다. 다음 단계는 위 코드에서 사용하는 dependency의 정확한 판·leaf ID/명령·응답 계약을 원문으로 특정하는 것이다. 그 뒤 작성할 실행 명령은 대상 식별자, 현재값, 요청값, 응답의 의미, 신뢰할 실제 결과의 출처를 입력으로 받아야 한다.

| 입력 ID | 고정 대상·경계 | 성공을 구분할 관측 |
| --- | --- | --- |
| P2-T1 | Mini→Doorbell→Chime C 유지; 루트 Chimes={} | 중간 채널에서 C를 특정할 수 있는지; 목록 비어 있음만으로 부재 단정 금지 |
| P2-T2 | 부모 볼륨 값과 Chime C 값을 서로 다르게 설정 | C 대상 명령이 부모가 아닌 C의 값을 바꾸는지 |
| P2-T3 | 현재 C=2, 요청 C=0, 허용된 장치 시험 | ACK/echo와 C의 실제 최신 설정·필요한 음향 관찰 구별 |
| P2-T4 | 응답 캐시 또는 다른 leaf 값이 섞인 경우 | 대상·출처·최신성을 검증하지 못하면 성공 미확인 |

외부 프로토콜에 setter가 없으면 관계 원리는 구현 부품으로 승격되지 않는다. 신뢰할 setter 결과 보증이 있으면 별도 GET을 필수조건으로 추가하지 않는다. 장치의 재페어링은 C1을 바꾸므로 별도 조건 변경 실험이다.

## P3: 정확한 revision과 실제 UI 검증

환경: Inkscape `e1e8684`로 보고된1.5-dev, GTK4.22.4/gtkmm4.20, Linux Mint22. 이 짧은 commit의 전체 SHA 및 현재 위젯을 먼저 확인해야 한다. `INKSCAPE_CHECKOUT`과 `INKSCAPE_BINARY`는 별도 검증 환경의 절대경로 입력이다.

```sh
git -C "$INKSCAPE_CHECKOUT" rev-parse 'e1e8684^{commit}'
git -C "$INKSCAPE_CHECKOUT" show e1e8684:src/ui/dialog/undo-history.cpp
git -C "$INKSCAPE_CHECKOUT" show e1e8684:src/ui/dialog/undo-history.h
"$INKSCAPE_BINARY" --version
"$INKSCAPE_BINARY"
```

앞의 show가 경로/commit 부재로 실패하면 실제 revision의 tree부터 확인하며, Doxygen 또는1.4-6으로 대체해 동일판이라고 쓰지 않는다. 실제 GUI에서 Undo History를 열고 같은 종류의 행동을 연속 수행한 묶음과 서로 다른 행동을 만든다. 창의 원래 폭·높이·배율·글꼴·언어를 먼저 기록한 뒤 긴 수량 제목, 명확한 짧은 제목, 두 줄 제목을 같은 크기에서 비교한다. 본문에는 픽셀 폭이 없으므로 임의 숫자를 원저자 제약이라고 쓰지 않는다.

통과 관측은 세 의미를 초보자가 설명할 수 있고 제목이 보이며 잘리지 않고 원래 작은 공간을 유지하는 것이다. 코드의 headers_visible만 켠 screenshot은 이해도 성공을 입증하지 않는다. 사용자 검증이 필요하면 별도로 승인된 실제 참가자·절차가 필요하며, 이 연구는 사람에게 연락하거나 모집하지 않았다. 독립 사용성 시험은 미실시다.

## 저장소 검사 재실행

실행 위치: `/workspace/scratch/41ae7a55914b/agentflow-open` 또는 같은 Git 내용을 가진 checkout root. 정확한 현재 HEAD를 먼저 기록한다.

```sh
git rev-parse HEAD
python -B docs/workstreams/research/AF-RES-069/evidence/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-069/manifest.json --fetch
git status --porcelain
```

이 검사들은 기록 구조·소유 경로·계약을 확인한다. 제품 동작·원문 최초판·같은 비용·원 개발자의 채택을 검증하는 명령이 아니다.
