# AF-RES-022 인계 · 늦게 알게 된 해법이 실제 선택을 바꾼 조건

## 인계 상태

**REVIEW_READY_WITH_GAPS**. 배정된 조사·원장·필수 표·교차 검토를 완료하고 작업 브랜치에 저장했다. 양성 사례의 보강 목표와 일부 역사 기록은 미충족으로 남겼다. 원문·표본 하한은 충족했으며, 미확인을 성공이나 비용 0으로 바꾸지 않았다.

- 저장소: `laadkke-arch/agentflow-open`
- 작업 브랜치: `work/research-af-res-022`
- 소유 경로: `docs/workstreams/research/AF-RES-022/`
- 배정 시 foundation: `435a5099a0abb0bb4b3c08d40401d0e304e82153`
- 계획 기준판: `b507fbcab09724a77270e658355f4b661cc35f02`
- 결과·검사 본 묶음: `3e28772096c8abbcbe83dc16fc2bebb961ffafe5`
- 인계 직전 참조 점검 커밋: `bed02c1702f99d0c7f685b2731aec6e7593e875a`
- 최종 인계 커밋: 이 파일을 추가한 마지막 커밋. 자기 SHA를 본문에 재귀적으로 넣지 않으며 아래 `git log -1 -- HANDOFF.md`로 확인한다. 진행 담당이 `result_commit`을 반영할 때는 이 최종 인계 커밋의 전체 SHA를 사용한다.
- 모델/위치: GPT-6 Astra Pro 세션 표기, 동일 상속 모델의 역할 분담. ChatGPT Linux cloud workspace `/workspace/scratch/3742f7a04774/agentflow-open`. 사용자 PC나 사람 코더의 실행으로 표기하지 않았다.

이 파일은 SELF_CHECK·수용 근거를 먼저 커밋하고 GitHub 고정판의 본문·blob SHA를 읽어 확인한 **뒤에** 작성했다. 공통 `dot-control.json`, STATE, 계약, 색인, 제품 코드는 변경하지 않았다. 이 인계는 해당 공통 파일의 상태를 자동으로 완료 처리했다는 뜻이 아니다.

## 핵심 결과와 실제 분모

| 측정 | 결과 | 해석 범위 |
| --- | --- | --- |
| A 결과 비조건 표집 | 24개 선택, 세 계열×8 | Backstage/Kibana 보존 문서, Apache 제안/메일, Rust 조직 설계 PR. 상한 전29심사−5제외=24; 상한 뒤28보류 |
| B 발견 경로 목적표집 | 고유9개: GitHub8·당사자 회고1 | A/B 같은 선택 중복0. 발생률의 주 분모에 더하지 않음 |
| 문헌 | 원장285행 중 보수 산입153 | 결정43·별도 후속66·공식 과거판/조건34·두 타 분야4·기타6. 같은 판의 단순 보강 등12개 추가 비산입 |
| A 엄격 관측 하한 | **0/24** | 명시 미인지→당시 사용 가능→발견 때문에 변경→후속 시행의 직접 연결. 실제 발생률0이라는 주장이 아님 |
| A 기지 제약 교정+시행 | **2/24: A01, A19** | annotation 타입·CommonMark 문법 조건을 바로잡은 사례. 새 해법의 존재를 처음 안 사건과 구별 |
| A 초기 표적 해법 인지 | 기지21/24, 미확인3/24 | A06·A07·A09. 생애 최초 인지일은 별도24/24 미확인 |
| 인지 기록완성 시나리오 | **0/24~2/24, 0~8.3%** | 최종 기능이 후발인 A06을 분리한 A07/A09에 한정. 미확인이 전부 음성/양성인 시나리오이며 **엄격 인과 상한·신뢰구간·모집단 추정이 아님** |
| B 엄격 연결 | **B08 1건** | Path를 조기에 문자열로 바꾸던 선택을 JSONEncoder 호환 확장점을 쓰는 출력 경계로 일부 변경. 실제 import 환경·절감량은 불명 |
| 재평가까지 포함한 연결 | **4건: A01, A19, B05, B08** | 6건 보강 목표에 미달. B05는 이미 알던 Plotly의 라이선스 오해 정정·후속 전환이지 직접 미인지 인과가 아님 |
| 후기 자체 구현 유지 | 후보 B01·B02·B09; 엄격 생산 유지0 | 기능 후발·전송 방식 불일치·교육용 예제 때문에 ‘생산 자체구현 유지3건’으로 승격하지 않음 |
| 범위를 한정한 A 시행 | 20/24 | A04·A17·A22·A24는 미확인. 문서 수용과 실제 구현을 구별 |
| 비용 | 45행으로33선택 모두 보존 | 달력10·변경 규모7·당사자 투입2·귀속 불명 로그1·미확인 반사실25행. 단위/귀속이 달라 합계 없음 |
| 조기 소개의 수량적 인과 절감 | A24/B9 모두 미확인 | 13h50m·하루·약1시간·4일·LOC를 절감액으로 합산하지 않음 |

B08의 변화는 프로그램 전체 대체가 아니다. 디렉터리 탐색·중복 비교 목적은 남고 JSON 출력 시점의 변환을 위임한다. YAML은 후속판에 새로 추가한 별도 자체 변환이다. 코드가 `simplejson`을 우선 import할 수 있어 실제로 CPython `json`만 실행했다고 단정하지 않았다. 첫 글·후속 코드가 같은 작성자 계보이며 당대 외부 보관본과 실행 환경은 미확인이다.

반대 선택도 중요했다. A20은 Criterion을 이미 고려했다. A07은 전체 Router API 노출을 거절하면서 내부 Router는 사용했다. B02는 처음 소개받은 stream 클라이언트가 필요한 datagram을 대신하지 못했다. B06은 원 시점에 Azure 기능이 없어 조기 링크만으로 초기 작업을 없앴다고 할 수 없다. B09는 내장 옵션을 알고도 교육용 후크 예제를 남겼지만 운영 시행은 확인하지 못했다. B07은 병합 전 시험 분기에서 외부 polyfill을 넣었다가 되돌린 경우다.

## 산출물과 재현 경로

| 파일 | 쓰임 |
| --- | --- |
| [RESULT.md](RESULT.md) | 제목 다음 필수4표, A/B를 합치지 않은 Q1–Q8 답, 당시 개입 링크와 반대 사례, 끝의 약점3행 |
| [SCOPE.md](SCOPE.md) | 입력 SHA·관측 창·사전 적격/정렬/상한·모델/실행 위치·동결 뒤 측정 정의 보강 |
| [sampling.csv](sampling.csv) | 포함/탈락/보류/검색만/차단과 원장 순번·URL·중복 ID |
| [decisions.jsonl](decisions.jsonl), [timeline.csv](timeline.csv) | 필요·대안·인지 주체·결정·시행의 날짜/정밀도/원문과 각 사례 최소 다음 입력 |
| [sources.json](sources.json) |285개 자료 행의 주소·판·확인UTC·읽은 절·내용·한계·계보·산입 여부 |
| [costs.csv](costs.csv), [counterexamples.md](counterexamples.md) | 원 단위·귀속·재사용과 채택/유지/철회/전이 양쪽 근거·실제 반례 검색 범위 |
| [SELF_CHECK.md](SELF_CHECK.md), [acceptance-evidence.json](evidence/acceptance-evidence.json) | Q별 결론/근거/반증/미확인/검사.33조건 중25 true,8 false |
| [statistics.json](evidence/statistics.json), [awareness-audit.json](streams/apache/awareness-audit.json) | 집계 정본, A24의 초기 표적 인지와 미확인 범위 |
| [validation.json](evidence/validation.json), [link-check.json](evidence/link-check.json), [session-check.json](evidence/session-check.json) | 실제36/36 검사, Q1–Q8 대표 원문9/9 재개방, 공통 gate exit0 |
| [coding-changes.json](evidence/coding-changes.json), [source-count-overrides.json](evidence/source-count-overrides.json), [reference-audit.json](evidence/reference-audit.json) | 재검토로 바꾼 판정·보수적 중복 제외·마지막 출처 ID 정정 |
| [PROGRESS.md](PROGRESS.md), `streams/` | 단계별 커밋·미확인·다음 출발점과 원 계열별 원장/검색 이력. 최종 상태는 이 HANDOFF 기준 |

통합 정본을 우선한다. stream별 원래 unknown과 최소 산입 수는 당시 조사 단계의 정의·집계이며 `raw_stream_flags`, `raw_record_family`, `stream_count_in_minimum`으로 남긴다. 같은 이름의 서로 다른 unknown을 더하지 않는다. CSV는 저장소 LF 개행으로 정규화해 원격 blob과 해시 입력 바이트를 일치시켰다.

다음 검사는 실행했고 기록했다. 역사적 제품 런타임이나 실제 팀의 인과효과를 재현한 명령은 아니다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/validate.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-022/manifest.json --fetch
```

`validate.py`는36/36, `session check --fetch`는 exit0·outside_paths=[]·errors=[]였다. 특정 Q의 주소를 다시 확인할 때는 아래처럼 범위를 좁힌다. GitHub 일부 원문은 web open이 실패했으나 같은 공개 URL의 일반 HTTP와 기존 공식 연결 경로에서 읽을 수 있었다. 차단 자체는 원문으로 산입하지 않았다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/recheck_links.py --source RUST-F04
```

원장을 다시 조립할 필요가 있을 때만 `tools/assemble.py`, 이어서 `tools/write_result.py`를 실행한다. 이 두 명령은 소유 경로의 생성 파일을 다시 쓰므로 새 조사 결과를 반영하려면 우선 stream/감사 입력을 갱신해야 한다. 검증 없는 현재 검색 결과를 과거 조건에 덮어쓰지 않는다.

## 입력·결과 커밋 확인 위치

| 단계 | 고정 커밋 | 확인한 내용 |
| --- | --- | --- |
| 입력017 | `34c14d6d2ad8802cf68ff9d9db4a3f810b4e057a` | HANDOFF, RESULT Q2·Q4–Q8,40행/7기원 중복 대조, statistics |
| 입력020 | `856e6b40ae12d43197a6f02f7bf6ab7a7506fd35` | HANDOFF, bundles/B21.md |
| ① 동결 | `00c2a14633e7503880f4aceb7c4909845298b3d7` | SCOPE·두 모집 경로·표집 메타데이터·manifest |
| ② F3 | `65bbd7ed738f8f4b48cad933209c516d36afb9f6` | Rust A17–A24 원안/후속/당대판 |
| ② F1 | `6729bb855853669a0119b496f102532123fe82e7` | Backstage/Kibana A01–A08 |
| ② F2 | `2d5efefe381e8a874e072411f76c579fa2cc0dd7` | Apache A09–A16, Message-ID/표결/릴리스 |
| ③ B·타 분야 | `de0bd1a9aed537823d355915d6e8b2d925cad2be` | B9·반례·특허/공학 대조 |
| ④ 결과·검사 | `3e28772096c8abbcbe83dc16fc2bebb961ffafe5` | RESULT·통합 원장·SELF_CHECK·수용 근거·검사 출력;38개 원격 blob과 로컬 바이트 일치 |
| ④ 참조 점검 | `bed02c1702f99d0c7f685b2731aec6e7593e875a` | 수용 근거의 EPO 차단 ID를 실제 CF-BLOCK-1..3으로 정정; 표본/분모 불변 |
| ⑤ 인계 | `git log -1 --format=%H -- docs/workstreams/research/AF-RES-022/HANDOFF.md` | 이 파일을 마지막 별도 커밋으로 추가. 반환 전체 SHA를 최종 result_commit에 사용 |

모든 묶음은 GitHub에서 해당 SHA의 파일을 다시 읽어 확인했다. 결과 본문과 검사 파일의 재현은 아래 명령으로 시작할 수 있다.

```bash
git show 3e28772096c8abbcbe83dc16fc2bebb961ffafe5:docs/workstreams/research/AF-RES-022/RESULT.md
git show bed02c1702f99d0c7f685b2731aec6e7593e875a:docs/workstreams/research/AF-RES-022/evidence/acceptance-evidence.json
git log -1 --format=%H -- docs/workstreams/research/AF-RES-022/HANDOFF.md
git diff --name-only 435a5099a0abb0bb4b3c08d40401d0e304e82153 HEAD
git status --porcelain
```

최종 확인에서는 diff 경로가 소유 경로에만 있어야 하며 status가 비어 있어야 한다. 마지막 인계 커밋 자체의 SHA·GitHub 재독 결과는 작업 완료 응답과 branch HEAD로 확인한다.

## 열린 판단과 다음 첫 행동

**다음 첫 행동은 A07의 최초5월10일 제안과5월28일 개정을 나란히 열고, 그 사이 제안자에게 Router의 어떤 정보를 소개했는지 기록 한 개를 찾는 것이다.** 이것이 A의 인지 미확인 범위를 바꿀 가장 직접적인 입력이다. 범용 검색을 다시 하거나017의40건을 재표집하지 않는다.

| 우선순위·ID | 열어야 할 최소 입력 | 그 입력이 바꿀 판정 |
| --- | --- | --- |
| 1 · A07 | 최초안 `5ec0bcf18041d2e6bb6046642ee0ce654121ba09`, 개정 `0af7534a54fda41593ebc2e0521778c0a8bec0db`, 그 사이 제안자 메시지/리뷰 revision | 이미 알았음/새로 소개됨, 공개 API 거절의 직접 이유. 내부 Router 구현은 이미 확인됨 |
| 2 · A09 |2018-02-06 원 Google Doc revision과 RocksDB DBWithTTL을 처음 소개한 메시지에 대한 Bowen의 답 |2월7일 SQL/Table idle retention 소개와 표적 RocksDB 인지를 혼동하지 않고 U를 줄임 |
| 3 · B03 | b-의 실제 `.pre-commit-config.yaml` 변경 커밋 또는 설정/실행 기록 | 재작성 계획 철회에서 실제 pygrep 채택으로 연결되는지 |
| 4 · B09 | 실제 SQLAlchemy/driver/PostgreSQL/PgBouncer 판·pool 설정·격리 요구, 자리표시자가 아닌 재현 설정, 오타 없는 코드의 성공 로그 | 날짜가 고정된 교육용 예제에서 실제 운영 시행으로 넘어갈 수 있는지 |
| 5 · A15·B06 | 이름·시작/종료·범위가 있는 worklog와 같은 변경의 폐기/재사용 diff. B06 하루 진술의 원 revision |13h50m/하루의 실제 귀속과 조기 링크의 회피 가능 부분을 분리 |
| 6 · 특허 | 출원05709452.6/14169289.7의 원 심사 통지·답변·각 제출 청구 세트 | 심판 요약을 넘어 제시 자료 전후 청구항 변경/유지를 직접 비교 |
| 7 · 전이 | 최초 사용 이전의 원 분야 소개 메시지와 받은 팀의 규칙/코드 변경 한 쌍; E1 코딩 데이터/정오표 | 구조 대응의 실제 유입 시점과144/147유추 불일치 해소 |

A07 재개 명령의 입력은 해당 고정 커밋을 보유한 공개 Kibana checkout이다. 아래 변수에는 실제 checkout 경로를 넣는다. 이 명령은 당시 작성자의 최초 인지를 자동으로 증명하지 않으며 확인할 개정 범위를 정한다.

```bash
AF022_KIBANA_CHECKOUT=/path/to/kibana

git -C "$AF022_KIBANA_CHECKOUT" show 5ec0bcf18041d2e6bb6046642ee0ce654121ba09:rfcs/text/0003_application_service_mounting.md
git -C "$AF022_KIBANA_CHECKOUT" show 0af7534a54fda41593ebc2e0521778c0a8bec0db -- rfcs/text/0003_application_service_mounting.md
```

B09의 **이미 수행한 정적 Git 대조**는 [b09-git-audit.json](streams/b/b09-git-audit.json)에 명령·입력·결과가 있다. 새 checkout에서 재개할 경우 입력은 공개 gist 저장소 `https://gist.github.com/5847e7fb93f51a140ff358d45bb1e761.git`이다.

```bash
AF022_GIST_CHECKOUT=/path/to/gist-checkout

git -C "$AF022_GIST_CHECKOUT" show cfe44f4ed1978a210e4eb58a3d185e9b1a0e8073:session.py
git -C "$AF022_GIST_CHECKOUT" show 9f824c53a67483181ab78a4d25367a741e5d0b63 -- session.py
git -C "$AF022_GIST_CHECKOUT" show 6a24929ee7c98a90a4ebee4c438ae34c9266f302 -- session.py
```

B09의 실제 운영 재현은 위 표의 DB/driver/pool 입력과 당시 실행 경로가 없어 수행하지 않았다. `session.py`에는 `CONNECTION_URL` 자리표시자와 `AsyncSession(enginer)`의 미정의 이름이 있어 원문 자체를 성공 실행 근거로 쓸 수 없다. 문법 검사나 현재 라이브러리로 만든 예제만 통과해도 당시 운영 시행이 확인되는 것은 아니다. 다음 담당자는 먼저 실제 실행 가능한 소스와 환경을 확보한 뒤, 해당 팀이 사용한 테스트 명령과 입력을 함께 기록해야 한다.

B08에서 실행하지 못한 것은 **작성 당시 환경의 재현**이다. 아래는 그와 구별되는, 선택한 좁은 API 조건을 다시 검사할 수 있는 명령이다. 입력은 Python3.10 환경, 선택적으로 당시 공식판 `simplejson==3.17.0`, 그리고 모듈명 `json` 또는 `simplejson`이다. 실제 작성자가 어느 모듈을 썼는지나 작업 절감량은 이 검사로 알 수 없다.

```bash
AF022_JSON_MODULE=json python3.10 - <<'PYCODE'
import importlib
import os
from pathlib import Path

module = importlib.import_module(os.environ['AF022_JSON_MODULE'])
class PathEncoder(module.JSONEncoder):
    def default(self, value):
        if isinstance(value, Path):
            return str(value)
        return super().default(value)

paths = [[Path('fixture/a.txt'), Path('fixture/b.txt')]]
encoded = module.dumps(paths, cls=PathEncoder)
assert module.loads(encoded) == [['fixture/a.txt', 'fixture/b.txt']]
assert isinstance(paths[0][0], Path)
print(module.__name__, 'output-boundary condition passed')
PYCODE
```

EPO 원장 재접근은 아래 원 URL부터 시작한다. 이번 실행에서는403이었으며 이를 원문 확인으로 세지 않았다. 접근이 계속 막히면 이미 읽은 공식 심판 PDF를 유지하고 원 통지/청구 diff는 미확인으로 남긴다.

```bash
curl --fail --location 'https://register.epo.org/espacenet/application?number=EP05709452'
curl --fail --location 'https://register.epo.org/espacenet/application?number=EP14169289'
```

## 진행 담당에게 넘기는 색인 반영 제안

공통 파일은 수정하지 않았다. 진행 담당에게 아래 내용의 반영을 제안한다.

1. AF-RES-022 결과 상태는 `REVIEW_READY_WITH_GAPS`; `result_commit`은 이 HANDOFF를 추가한 최종 커밋의 전체 SHA. 결과 경로는 이 디렉터리의 RESULT/HANDOFF/SELF_CHECK/acceptance다.
2. A24와B9,153원문을 별도 필드로 표시한다. A엄격하한0/24와 B엄격1을 합친 발생률을 만들지 않는다. 인지 기록완성0~2/24도 효과 상한으로 표시하지 않는다.
3. 제품 연구 색인에는 ‘어떤 날짜의 어떤 조건이 있는 링크가 구체 선택을 바꾸는가’와 ‘이미 알거나 당시 조건이 안 맞아 유지한 이유’를 함께 요약한다. 비용 총액·시장 규모·자료 없는 팀의 발생률은 이 결과에서 끌어내지 않는다.
4. 우선 보강 항목은 A07/A09 인지 원기록, B03 실제 설정, B09 운영 입력, 비용 귀속 기록, EPO dossier다. 다른 PLAN5 작업을 기다려야 하는 의존성으로 만들지 않는다.

## 가장 중요한 약점 3건과 다음 조사 제안

| 중요한 약점 | 판단에 미치는 영향 | 다음 조사·최소 확인 |
| --- | --- | --- |
| 초기 인지·사적 필요·최초 공개 구현을 분리할 기록이 부족함 |A0/24는 관측 하한만 지지한다. A07/A09의0~2/24를 인과효과 상한으로 읽을 수 없고, 외부에서 개입할 수 있었던 날도 확정 못함 |A07 최초안/개정 사이의 제안자 메시지1건과 A09 원Doc revision/첫 RocksDB 소개 답글1건부터 확보 |
| 투입·폐기·재사용·운영 시행의 귀속이 끊김 |수량적 절감은 전부 미확인. 후기 유지3건과 연결6건 목표도 미달. 교육용 예제 날짜를 운영 성과로 바꾸면 결론이 달라짐 |이름·날짜·범위가 있는 worklog와 같은 작업diff, B03 실제설정commit, B09 실제환경·성공로그 한 묶음 |
| 타 분야의 판정 단위와 역사적 유입 계보가 다름 |청구항 수정·개념생성·구조 대응을 소프트웨어 채택/절감으로 동일시할 수 없음. EPO 원dossier 차단과 E1의144/147불일치가 남음 |원 심사 통지/청구 세트 전후diff, E1 코딩 자료/정오표, 원 분야 소개 이전·이후의 실제 규칙 변경1쌍 |
