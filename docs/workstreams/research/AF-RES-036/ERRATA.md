# AF-RES-036 · 재개 정정 원장

기준은 원격 `f403243dbf5f097536a1fd9fda55dfce4382329a`다. 이전 커밋·raw수집·봉인B/packets/decisions/판정은 보존했다. 이 정정은 처음 표집이나 판독을 다시 한 것이 아니다.

| ID | 정정한 행·파일 | 이전 범위·문제 | 정정 내용 | 결론에 미치는 영향·남긴 기록 |
| --- | --- | --- | --- | --- |
| E01 | sources.jsonl/attempts.jsonl/costs.csv 및 source/cost 요약·alias | 공통집계기가 collector만 읽어 결정봉인뒤GNU/Bioc기준판정64source·64attempt를 누락. 기준12행의primary_source_ids는raw원장에있지만canonical과조인불가. | 명시적원고대응으로64source를variants/비산입보충행으로연결. 추가59GET·67exchange·실패2·56,698,339B·493.333131s를단계구분하여포함. | 기준판정행동·48결정불변. 수집157GET→기준확인포함216GET. 적격원문하한50은불변. review/resume-quant/integration-applied.json의전후hash·대응표. |
| E02 | collectors/bioc/nh-ready.md의모든component1600자표현 및 최종설명 | rawexcerpt와metadatawrapper포함카드를구별하지않은표현. | raw N/H는전부1600자이내; wrapper전체N은G04 2113·R04 1692자임을RESULT/수용파일에명시. 옛메모·카드바이트는수정하지않음. | 정보길이를같게고정한BN/BNH비교불변. 전체카드길이1600준수라고보고하지않음. components.jsonl·resume-quant audit. |
| E03 | CX-G02의read_location | 원문핵심문장은맞으나‘Main points/About this release’라는절제목은부정확. | 실제위치는§1 ‘Overview of main changes’,재개웹표시87–90행으로canonical location에정정하고이전위치는rawvariant에보존. | ONS가2021–2023을2023경계로제공한다는반례내용불변. review/resume-cross-costs/sources.jsonl 및REVIEW.md. |
| E04 | PROGRESS.md | f403243에산출물·판독·기준판정이있으나진행표는초기범위커밋과배정까지만기록. | 실제git이력의후속봉인·관측·판독·기준판정커밋을추가하고재개상태를기록. | 완료묶음을다시수행하지않음. Git SHA/시각이기준이며서술을과거실행증거로만들지않음. |
| E05 | 재개후원문재독의출처·비용범위 | 전작업216GET와현재감사의추가10GET/웹도구조회는다른실행이다. | 재개감사는별도phase로원문alias·시도·미계측을연결하고추가최소수0으로보존. 전작업수치와후기감사합을분리. | C1/C2두번째조회실험으로가산하지않음. evidence/resume-cost-summary.json과각review원장. |
| E06 | criterion-dependence.json의G06설명및초기RESULT문구 | gettext1.0의FTP목록수정일2026-01-28을공식발표일로쓴오류. | GNU-GT-ANNOUNCE의원시Date는Thu,29Jan202603:42:11+0100이므로공식발표일은2026-01-29. 봉인metadata는보존하고최종표1에서구분·정정. | 원adjudication.csv의dated_publisher_evidence는이미29로맞으며KEEP판정불변. raw발표Date와filemtime을합치지않음. |
| E07 | 초기RESULT의R05H멤버표기 | class.Rd로줄여쓴경로가실제멤버와다름. | SingleCellExperiment/man/SingleCellExperiment.Rd로정정. | 봉인components.jsonl의정확멤버·hash·판독바이트불변. 최종보고의위치만수정. |

현재7층이‘최신판을명시한7문장’이라는뜻이아니고, G06 stable이원문추가한정이라는것은기존base-audit에서이미알린해석제약이다. 새발견한정정처럼처리하거나봉인층을사후수정하지않았다. 과거판목적은G03 한건이며 R경로는0을유지한다.
