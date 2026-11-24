# 미실행 제품 시험과 정확한 재개 입력

## 실행 상태

실제 실행한 연구는 12개 검색 arm과 원장 생성·검산이다. 후보의 원 프로젝트 적용, Node-RED/React Flow 실행, physical Windows touchpad 시험, 원 개발자의 추천 수신·재실행, 자동 탐색기 제품 실행은 하지 않았다. `choices.csv`의 `experiment_executed=False`를 유지한다. 공통 저장소 검사 통과도 이 상태를 바꾸지 않는다.

현재 Linux 작업공간에는 Python·Node·npm·Git이 있지만 요청 당시의 OS·브라우저·touchpad·프로젝트 설정이 고정되어 있지 않다. 원문 최초판과 일부 버전·그림 구조도 미확인이다. 따라서 합성 fixture를 실행해서 원 요청의 성공이라고 기록하지 않는다. 아래는 재개 명령과 구체 입력이며, 명령을 적었다는 사실이 실행 증거는 아니다.

## 1. 결과판과 연구 원장 검사

HANDOFF의 `검사한 결과 SHA`를 `AF109_RESULT_SHA`에 넣고 공개 원격의 해당 판을 읽는다. 이미 이 저장소를 가진 작업자는 새 clone 대신 같은 SHA의 깨끗한 사본을 사용할 수 있다. 출력·캐시·추가 실험은 계속 이 작업의 허용 경로 안에 둔다.

```sh
git fetch origin work/research-af-res-109
git show "$AF109_RESULT_SHA:docs/workstreams/research/AF-RES-109/RESULT.md"
git show "$AF109_RESULT_SHA:docs/workstreams/research/AF-RES-109/reproduce.md"
python -B -m workbench.session check docs/workstreams/research/AF-RES-109/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-109/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

세 Python 명령의 작업 디렉터리는 **그 결과 SHA로 checkout된 저장소 루트**다. 단순히 `git show`만 하고 다른 HEAD에서 검사하지 않는다. 기존 결과 원장을 재생성할 필요가 있을 때만 `assemble_evidence.py`와 `recalculate.py --write`를 쓰며, 원 검색 수집기 `collect_search.py`를 실행해 판독된 표를 덮어쓰지 않는다. 결과 수정이 생기면 새 SHA로 필요한 검사를 다시 한다.

## 2. 27개 시험 입력을 중복 제거하여 꺼내는 명령

아래 명령은 이미 커밋된 `choices.csv`에서 시험 큐를 출력한다. 제품을 실행하지 않는다. 같은 시험키를 여러 후보가 제안한 경우 한 번만 출력하되 출처행을 함께 보존한다. 이 큐의 `minimum_input`과 `expected_output`이 실행할 입력·판별 기준이다. 연구자가 제안한 값과 자연 요청의 값을 구분한다.

```sh
python -B - <<'PY'
import csv, json
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-109/choices.csv')
rows = list(csv.DictReader(p.open()))
tests = {}
for row in rows:
    if row['new_test_flag'] != '1':
        continue
    key = row['test_key']
    if key not in tests:
        tests[key] = {
            'test_key': key, 'request_id': row['request_id'],
            'minimum_input': row['minimum_input'],
            'expected_output': row['expected_output'],
            'broken_source_assumption': row['broken_source_assumption'],
            'eligibility': row['current_eligibility'],
            'executed': False, 'candidate_ids': []}
    tests[key]['candidate_ids'].append(row['candidate_id'])
assert len(tests) == 27
for test in tests.values():
    print(json.dumps(test, ensure_ascii=False))
PY
```

원 요청 문자열은 requests.jsonl에 저장한 URL의 title/body에서 얻는다. CRLF/CR→LF만 정규화한 입력 지문을 `experiment_input_sha256`와 비교한다. hash가 다르면 현재 웹 원문을 기존 입력인 것처럼 사용하지 말고 별도 판으로 보존한다. 자연 입력에 없는 값을 넣은 시험은 `researcher_proposed_synthetic_or_diagnostic`으로 유지한다.

## 3. 요청별 실행 준비·입력·실패 판별

| 요청 | 먼저 필요한 실제 환경·입력 | 실행할 행동과 관측 | 통과로 오인하면 안 되는 결과 |
| --- | --- | --- | --- |
| R1 | 원 요청의 Node-RED3.1.0·현재 원문판, 수정 전/후 고정 소스, locale catalog. 실제 메뉴 key와 handler를 원 소스에서 확인 | 같은 flow ID·이름에서 menu와double-click으로 열어 환경변수만 바꾸고 재개봉. locale key누락 fixture와 키는있으나옛의미 fixture를 분리. UI label·dialog목적·저장상태·locale별결과 기록 | Edit로 바꿨다는 것은 원 요청자가 이미 제안한 구현. nonempty번역이나msgcmp통과만으로의미성공 아님. 사람의첫클릭시험은이연구에서모집하지 않음 |
| R2 | 원문 Node-RED버전`3.13`의 실제 설치판을 먼저 식별. Node18.16.1·npm8.3.0·Windows/Chrome 원구성, 후속18.6/20.10불일치 유지 | 메뉴와double-click·tab선택·panel표시·이름저장재개봉을각각관찰. console/DOM/computed CSS/ancestor/hit target기록. API대조는새로만든폐기가능빈flow에만label변경 | API성공은Properties pane복구가아님. opacity0의visible판정이나DOM존재만으로사용가능하다고판정하지않음. 실사용flow에빈node배열을보내지않음 |
| R3 | Node-RED3.1.3·Node16.20.2·npm8.19.4·Docker/Firefox121라는원문구성; 실제비밀대신명시적인synthetic A/B값; 기존flow/global변수식별자 | 초기Inject값을확인하고①plaintext global만추가②Inject flow만수정③두행동결합④secret명시교체⑤새키에retain표식으로나눔. outgoing delta·저장된키집합·runtime관측을단계별기록. 같은작업을고정수정판과비교 | 실제데이터값이표식과같은경우,얕은merge·삭제의도·ID변경을별도로대조. 원문실패를재현하지못한synthetic단위함수통과는수리성공아님 |
| R4 | 당시React Flow판·원code sandbox·겹친두node의bounding box·dragHandle영역; 미확인판을현행으로대체할때별도층표시 | 같은좌표의body/handle클릭·drag·선택ID·delete후node/edge를기록. wrapper none+child auto,안쪽만none,nodrag,명시ID삭제를별도fixture로비교 | ID삭제는selection조건을복구하지않음. pointer bubbling과hit target은다름. click-through로drag경로가사라지면두조건동시성공아님 |
| R5 | 원첨부이미지와실제topology를먼저읽음:동일끝점pair인지fan-out인지확정. 실제edge/handle ID·추가순서·화면크기·당시버전 | edge수를1→2→3으로늘려data cardinality와geometry를분리관찰. handle좌표갱신,ELKgap/overhang,master경로와peer재라우팅책임을분리. 삭제·추가뒤기존edge경로도대조 | 같은끝점평행edge demo가fan-out요청을해결했다고쓰지않음.그림없이연구자가만든topology는사후합성층 |
| R6 | 실제Windows11 touchpad 장치명·driver·Chrome120/Edge버전·원Figma-like예제·panOnScroll=true/zoomOnPinch=true. Mac 대조도별도실장치로그 | 원wheel event의ctrlKey/deltaX/deltaY/deltaMode/cancelable/defaultPrevented/isTrusted,viewport 전후변환,listener/first-ACK를기록. physical pinch와일반scroll·Control+wheel을분리. 합성cancelable pair는별도진단층. macOS guard 제거판과원판을같은장치에서비교 | 합성isTrusted=false입력이나Parallels한환경의성공을모든Windows장치성공으로세지않음. scale변화가있어도늦은zoom·이중pan·anchor이동실패를유지 |

이 저장소에는 이27개 제품 시험을 실행하는 완성된 harness가 없다. 존재하지 않는 `npm test:af109` 같은 명령을 인계하지 않는다. 위 큐를 꺼낸 뒤 해당 원 프로젝트의 **고정 SHA의 package scripts·기존 회귀시험을 직접 읽고**, fixture와 관측 hook을 이 작업 경로의 별도 사후 실행층에 구현하는 것이 제품 실행의 첫 행동이다. 당시판을 알 수 없는 R2/R4/R5는 우선 그 입력을 확정해야 한다. R6은 이 Linux 환경에서 실제 Windows touchpad를 관측할 수 없어 장치가 있는 실행 환경이 추가로 필요하다.

## 4. 후속 증거를 다시 읽을 정확한 대상

| 목적 | 공개 입력 | 최소 다음 확인 |
| --- | --- | --- |
| R1 기여자 시험실행 | PR4506 head `7f24de442f997e376b512b79258f083c6010a12e` | 해당head의공개CI/job로그;원요청자camueller의고정버전재시험진술 |
| R3 회귀실행 | PR4526 head `58e2fcbeee66f3f9096e9e434d4b69d975ddaac3` |env-var.js/credentials.js변경과원sequence를같은실행에서대조;kanunnikau후속미확인 |
| R5 최초 입력 | [편집event11365940209](https://api.github.com/repos/xyflow/xyflow/issues/events/11365940209)와issue3758원첨부 |title수정전후뿐아니라최초body·topology확정 |
| R6 gate 수정 | PR4230 head `0dbbe5456a01c6b1cbcac382d3ddd2f744aaac40`, release11.11.3;PR4229 head `d1b50707ff7a5428963a1c303d79eb0b0ba3a627` |같은실장치eventtrace와느린zoom반례. `12.0.0-next.17`의공식package/tag를직접읽기 |
| R2 복구원인 | [원요청자comment1874067118](https://github.com/node-red/node-red/issues/4507#issuecomment-1874067118),링크된forum84186/2 |정확한Node버전·console자료를확인;복구진술만으로업그레이드효과확정금지 |

## 5. 추천 인과효과와 시간

2024년 공개 사건은2026년 생성된 추천의 효과일 수 없다. 이번 작업은 원 개발자에게 연락하지 않았다. 기존 공개자료에서 추천 노출→동일 주체의 선택→같은 제안 실행→대안과 결과·시간이 연결되지 않으면 판정분모0을 유지한다. 단순히 나중에 비슷한 patch가 있거나 연구자의 시험이 통과하는 것으로 바꾸지 않는다. 새 외부 연락·계정 변경·유료 API는 이 재개 절차의 전제가 아니다.
