# RESULT 원문·판정 표현 검토

검토 UTC: 2026-11-22T17:14:01.870690+00:00. 검토한 RESULT SHA256: `5cb1ecdd367c520bdf11cb954ea9095a8c90cac26ea21ef518c3eb779d107a21`. 범위는 첫 필수표·핵심결과·Q1–Q5이며, 새 외부 조회를 하지 않았다. 기존 원장과 사후 추가 감사 원문만 대조했다. 보고서 파일을 직접 수정하지 않았다.

## 수정이 필요한 두 곳

| 위치 | 발견 | 정확한 근거와 권장 수정 | 결론 영향 |
| --- | --- | --- | --- |
| 표1 G06 현재 증거 | `2026-01-28 공식 stable 발표`는 발표일과 archive listing 시각을 혼동한다. | `adjudicators/gnu/sources.jsonl` GNU-GT-ANNOUNCE의 exact Date는 `Thu, 29 Jan 2026 03:42:11 +0100`(line67), publication_date도2026-01-29T03:42:11+01:00이다. `adjudication.csv` G06 dated_publisher_evidence도29다. **2026-01-29 공식 stable 발표**로 수정. URL: https://lists.gnu.org/archive/html/info-gnu/2026-01/msg00007.html . `criterion-dependence.json`의28일 표현도 사후 요약 오류로 ERRATA에 남길 것. | KEEP과H효과0은 변하지 않음. 날짜의 종류·재현성 정정. |
| 표1 R05 과거 근거 | `class.Rd`는 실제 원 archive member 이름과 다르다. | `components.jsonl` R05 H.metadata의 실제 member는 **`SingleCellExperiment/man/SingleCellExperiment.Rd`**. URL: https://bioconductor.org/packages/3.11/bioc/src/contrib/Archive/SingleCellExperiment/SingleCellExperiment_1.10.0.tar.gz . | 판정·수치 변화 없음. exact locator 정정. |

선택적 문구 개선: 표1 G02의 `Bash/Gawk 공통 프로젝트·배경 단서`는 두 별개 프로젝트를 같은 프로젝트로 읽힐 여지가 있다. `G01과 같은 Bash 배포·GNU 발행자 배경 단서`로 좁히는 것이 정확하다. 실제 same-project 관계는 G01↔G02, G03↔G04이며 G01↔G03은 같은 POSIX target이다.

## 요청한 세 항목 확인

- **원배포9개: 맞음.** `references.jsonl`의 `archive_url` 또는 `original_distribution_url`을 정규화해 고유 URL9개를 재계산했다. G01/G02는 Bash archive, G03/G04는 gawk-doc deb, R04/R06은SCE archive를 공유한다. 나머지6개는 각각 단독이므로9archive/12출판문서다. 프로젝트9개와 archive9개는 이번 결과에서 숫자가 같지만 다른 단위다.
- **현재 판정12개: 표현 지지.** KEEP11·R01REPLACE의 기준 확정12개이며, 원 href가 모두200이라는 뜻이 아니다. Q4는 GNU6개200·Bioc5개200/R01의404를 정확히 구별한다. current-source 최소수10과 기준판정12는 다른 분모다. RESULT는 외부 독립gold0, 기준 미확정0, 추가 판독 행동0/12를 적절히 나눈다.
- **G03의 선행 gawk5.0.1: 맞음.** G-H06 원장은 `Edition5.0 for gawk5.0.1; GNU info member`이며 `gawk-5.0.1/doc/gawk.info`의 Preface text offsets53100–53202/약line912가2008 POSIX를 말한다. B는 Debian gawk-doc5.1.0-1 HTML의2018각주다. H를B와 같은5.1.0 또는 당시POSIX 전체snapshot이라고 하지 않았으며 이 구분을 유지하면 된다.

## 지지되는 해석과 남길 제한

핵심결과와Q1–Q5는 충분히 제한되어 있다. N이1page/1GET이 아니라 필요한PDF/source까지 포함한다는 점, current7이최신판요구7이 아니라는 점, G03은B에판이이미있어H필수사례가아니라는점, H가선택한중복/약한근거일수있다는점, B/BH보류규칙이N의효과와결합되어있다는점, 내부기준일치와외부독립gold를분리한점이 모두 보존돼 있다.

POSIX 새판의anchor실패와bash-completion 하위directory의내용차이는 원12표본의잘못유지분자에넣지 않았다. R01의BNH tarball후보도기준판정의검증HTML주소와구별했다. 이범위에서 추가로 뒤집어야할행동판정이나 분모는 발견하지 못했다.

이검토는보고서작성뒤동일작성팀이원장과대조한것이며미노출판독이나독립정답이아니다. 두정정뒤파일hash가달라지므로위hash의리뷰범위를후기보고서전체검사로소급하지않는다.
