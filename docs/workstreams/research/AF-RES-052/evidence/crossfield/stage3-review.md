# Stage3 독립 방법·증거 감사

- 검토자: crossfield (동일 모델 계열의 별도 판독이며 인간 독립 검증이 아니다).
- 최종 파일 고정 통지를 받은 뒤 검토한 시각: 2026-11-23T00:38:41.259781+00:00.
- 읽을 때의 저장소 HEAD: `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e`. 후보·키·경로를 목적지 관측 전에 봉인한 기준은 `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e`이다.
- 범위: 두 도메인의 관측 원장·도착·경로·감도와 root sources의 최소 배당. 기존 원장 및 로컬 보존 원문을 읽어 대조했다. 새 사용자 실험, 브라우저 클릭 실행, 패키지 설치·행동 시험을 수행하지 않았다. 다른 파일을 고치지 않았다.

## 판단

**현재 원장의 결론을 뒤집는 중대한 증거·경로 오류를 발견하지 못했다.** 이는 표본 전체가 의미적 수용 조건을 충족했다는 판정이 아니다. 주표본은 자연층 네 요구의 목록 매치가 관측 0이고 보강층에서 목적에 연결된 풀을 확보하지 못했다. 따라서 주표본의 요구별 독립 구현 승격·손실 효과는 미확인으로 남아야 한다. D-M1의 C1 옵션 노출 차이는 별도 진단이며 전체 요구의 완결이나 자연층 성공으로 승격할 수 없다.

| 검토 항목 | 직접 대조한 원장·위치 | 판정과 허용되는 표현 |
| --- | --- | --- |
| 주표본의 목적 미연결 | Python `PY-E01`–`PY-E05`, P-S1 경로49행, observation-summary의 requirement_complete_ids/gain_loss | 사전 목적 없음으로 완결 ID·count·증감이 null/CSV 빈 필드다. 관측0이 아니다. 메타데이터상의 B rank5 URL 승격은 별개로 말할 수 있다. |
| 주표본과 진단 분리 | Python slot_id P-S1/D-P1, Markdown case_id D-M1 및 primary_sample_member=false | D-P1/D-M1은 조직·계보 범주에서 만든 진단이다. root의 자연4+보강4 및24방식 행에 새 유효 표본처럼 더하지 않는다. |
| 미구체화 경로 | Python paths 106행: P-S1 49, D-P1 57 | P-S1 49행은 시작 URL이 구체화됐다. D-P1 중49행만 instantiated=True이며6행의 미해결 시작URL과2행의 다음hop 자리표시는 False다. instantiated는 성공한 도착이나 실제 인간 클릭을 뜻하지 않는다. |
| 한 시행 두 동작 | Python actions/arrival_ids, Markdown D-M1-B-P08과 50개 경로 | 대표 열기1, 다른 대표 추가1, 그룹 열기1+멤버1, 대표1+실제 첫두href 중 하나1의 비용 구분이 유지된다. 서로 다른 시행의 부분조건을 합쳐 완결을 만들지 않았다. |
| 현재와 역사판 | Markdown ME-GOLD-C1/C2, ME-HISTORY, Python PY-E08/PY-E09 및 PY-A04/PY-A17 | 현행 문서/명시 조합과 원요청 환경이 분리되어 있다. react-stringify10.0.2 표기를 임의 수정하지 않았고 unified10.1.1 성공을 주장하지 않는다. 6.6.0 사용자 보고를8.2.0 실패로 일반화하지 않는다. |
| D2와 D3 | Markdown code-handler.js L20–72, code-indent.js L11–20, code-fence.js L10–21, stringify-compiler.js L31–38, to-markdown-tests.js L810–819/L929–930 | 소스·assertion은 fences=true/backtick 및 언어·값 보존의 조건부 조합 가능성을 지지한다. 실제 설치 의존판을 관측하거나 시험을 실행한 D3가 아니다. utility는 wrapper의 같은 계보이며 별도 독립 대안으로 세지 않았다. |
| 부분 조건과 완결 | Markdown D-M1-B-P08, ME-R4-C1/ME-R4-C2, diagnostic-metrics | B 그룹→rank4는 C1만 지지하며 C2는 미확인. 완결 ID는 공집합, 한 시행 최대0이다. A/C에4번째 슬롯을 더해도 C1 직접 노출만 달라지고 완결 ID 증감은0이다. 역사판 수치는 여전히 미확인이다. |
| 접힌 내용과 화면 표현 | Markdown MA-R4, visibility-check | 유일한 C1 양성의 fence/fences L160–167에는 details 조상이0이다. 다른 접힌 예제를1동작 양성 근거로 쓰지 않았다. 이것은 HTML 구조와 원문 순서의 판독 투영이며 viewport·실제 사용자의 이해/채택 측정은 아니다. |
| PyPI 스냅샷 혼합 방지 | PY-A04/PY-O04와 PY-A17/PY-O17 | 초기7.0.0은347단어의 부분 창, 후기8.2.0은 별도 창이다. 두 응답을 이어800단어로 만들거나 방식별로 유리한 판을 배정하지 않았다. 초기창의 잔여 내용은 미확인이다. |
| 실패를 소스 대체로 바꾸지 않기 | PY-A07 옵션 fragment, PY-A10 Compose tree, PY-A14 build base | 정확 fragment 미확인, tree 실패, unresolved build:index를 별도 보존한다. 후속 고정 README나 build base를 읽은 사실을 성공한 원 URL 도착·2동작 근거로 바꾸지 않았다. |
| 첫두 정보href | SCOPE 도착 규칙, Python 첫 매뉴얼 반환 L0–45, Markdown MA-R3/MA-R4 | Python에서 제외한 사이트 탐색은 첫 본문 제목 앞이며 첫 본문href는 PEP381이다. Markdown 본문 Contents는 정보 절 링크로 센다. 이번 첫두href의 현재 원장에서 명백한 규칙 충돌은 발견하지 못했다. 다른 TOC 정의의 감도는 미실시로 남긴다. |
| 최소24저작 배당 | root sources.jsonl의 counts_in_minimum=True 24행 | 요구4/목록·작성규칙4/공급자문서8/릴리스·시험4/타분야4. 모두 direct_open=True, failure 없음, duplicate_of 없음, 서로 다른 work_id24개다. 동일 remark README 재열람, PyPI README 재게시, AWS 하위 문서 확대, Inter release를 소프트웨어 시험으로 전용하는 중복은 배당에 없다. |

## 숫자를 옮길 때 보존해야 할 단위

- P-S1의 정확 URL5개, upstream2개, B의 rank5 승격1개, 원4번의 존재는 관측 사실이다. 원4번 PyPI는 이미 앞에 있는 bandersnatch 계보이며 원5번 AWS S3는 저장 인프라다. 이 숫자를 독립 미러/빌드 백엔드 대안 수로 쓰지 않는다.
- D-M1은 정확URL6개와 upstream2개이나 mdast는 데이터 명세다. 별도 이름·상류가 보인다는 사실만으로 실행 가능한 대안이 늘었다고 할 수 없다.
- Markdown의 조건부 D2 gold ID1개는 현재 조합의 가능성이다. 원풀의 제한 창 완결, 대표1동작 완결, 각2동작 경로의 완결 합집합, 한 시행 최대는 모두 관측0이다. 원요청 역사판 완결은 미확인이다.
- P-S1 완결 분모를 요구와 연결된 풀로 정하면0이므로 그 비율은 해당 없음이다. 메타데이터 기회가 있는 보강 슬롯1개와 계획된4자리를 분모·단위 없이 섞지 않는다.
- 전체 source행 수나 직접 unique work 수는 quota24와 별개의 모집단이다. 직접 열람의 수가 많아도 자연 표본의 빈 매치나 목적 미연결을 보충하지 않는다.

## 남는 정확한 한계와 바뀌는 조건

1. **의미적 비교 입력 부족:** 자연4개에서 미리 정한 명사-절 매치가 없고 P-S1에는 목적이 없다. 같은 규칙으로 목적 연결된 기능 절과4번째 이후 독립 실행 구현이 확보되어야 주표본의 증감 판정이 가능해진다. 현재 자료만으로 조건을 새로 만들면 사후 요구 합성이다.
2. **역사판과 실제 실행 결손:** 원요청 lockfile/보존 첨부로 패키지 식별과 설치판을 확정하고 그 판에서 원래 두 code 노드를 같은 시행으로 실행해야 역사판 완결로 바뀐다. 현재 소스만으로 해당 결손을 없앨 수 없다.
3. **도착 창의 제한:** Python PyPI 초기 창의 잔여 응답, fragment 정확 도착, Compose 원 tree 성공과 실제 렌더/사용자행동은 관측하지 못했다. 이들에 관한 정답·성공 주장은 보류한다. 현재 C1 양성은 details 밖에 있지만 실제 독자의 이해까지 입증하지는 않는다.

## 검토한 파일의 내용 해시

아래 해시는 검토 시점 내용이다. 이후 내용이 달라지면 해당 변경 부분을 다시 판독해야 한다.

| 파일 | SHA-256 |
| --- | --- |
| `evidence/python/evidence.csv` | `e2ff6d5b47db15af682c4ee4f5bee7d332fe5d59212b625dbc85d581be0b3499` |
| `evidence/python/paths.csv` | `2db572126995b5ae2ad6fe0aa5a51f601d7266c31c76a25a35349e0ea7472f36` |
| `evidence/python/arrivals.jsonl` | `4218938dda395b005c58c088e24862e65061aa0a38d1b15ba6ca8d924a1621da` |
| `evidence/python/observations.md` | `06085c4cacc6ee28bb52f37d5a194c250881ae0b439be668cd2ef0ab0162b7fc` |
| `evidence/python/observation-summary.json` | `6a44a16fed89f202a763450bfc570919e05e232936f7545b6dfbe8010fccec0f` |
| `evidence/markdown/evidence.csv` | `4c694ad01ed0b5052ab7a8de7fef042c5868143823f1e6ea694a9944b9ef8ed1` |
| `evidence/markdown/paths.csv` | `95a73dc5fff84c03f1a9d8ab84ca47a0422043b4e9f9e022a6a3c7e12a950b96` |
| `evidence/markdown/arrivals.jsonl` | `53b2959e92e7a69c3775a1837d8c193c96975e550875a6f782796a6131749739` |
| `evidence/markdown/diagnostic-metrics.json` | `b4e90419f1c878306ca500e6b7ccd299aa96c5fce6961e2b1529e37015b76c41` |
| `evidence/markdown/visibility-check.json` | `99402ccca86d8761abbacde7426af656ac9dc1e4518334f698b3486925261b54` |
| `evidence/markdown/sensitivity-observations.csv` | `6432e7b3b2748c5be3787f4c90fefcb50f5365b39a5387f623f8bb55a96500a2` |
| `evidence/markdown/observations.md` | `e8173e95e1d9a3de285809213287bdb139aaaff5964be3aa6bdbbe9fea9df6a4` |
| `sources.jsonl` | `646e577baa7cb4375a92f3ed6d25a22af7f2740585d6ccd477bab62d5084cde7` |
