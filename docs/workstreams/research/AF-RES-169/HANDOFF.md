# HANDOFF — AF-RES-169
status: PARTIAL
self_assessment: PARTIAL (not central control status)
review: self-check only, no independent review
branch: work/research-af-res-169
owned_path: docs/workstreams/research/AF-RES-169/
plan_baseline: 53eaa286136019510f052179f5f51d901bdac858
input_head: 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc
dependency: AF-RES-161 central DONE; fixed result 810904a5bdcb586fd7e0920488fbbfdb4b7ab0f1; previous worker self PARTIAL
result_commit: f5d2b2f95f8c6cf9c69f0f9b901780e91703e4b4
handoff_commit: this file's enclosing commit (self-reference intentionally not fabricated)

## 판정과 재개
- 핵심 결론: 옛 언어 코드 → 역사 원문, 현대 후보 집합, 특정 하류 정규화, 개인 의미 선택은 별개. B01–04의 단일 후계는 IANA PV와 CLDR35/ICU 일치; B05–08의 분할은 IANA Comments에 둘, CLDR38/ICU68.1 alias 한 값. B05 sap→aqt는 spn을 없애고 B06 leg→enl은 enx를 없애며, 실제 WALS Enxet 레코드는 enx. 해당 레코드의 과거 leg는 미관측. likelySubtags의 동일 국가/문자 체계로 의도 선택 불가. 정규화 목적이 명시된 단일 후계에서는 단일 현대 검색 키 가능. 실제 도구 지원은 별도.
- 자료: 127 ledger rows, 98 opened/29 blocked; 산입 31 distinct work IDs, 엄격히 동일 연속 저작의 판을 묶으면 22. 계보 표기 7(파생 ICU 포함, CLDR로 병합 6). 정식 결정 0/8, IANA 12/3, CLDR/소비자 13/5, 실제 태그 2/2, 전거 2/2, 지명 2/2. 요구된 8개 결정 원문 미확인으로 PARTIAL. 공식 자연표본 0/12, 보강 B 12/12; frame 715 action rows, 499 bibliographic requests, 141 retirement rows. IANA 필드 12/12, CLDR/ICU 저장 규칙 8/8, 직접 수정 diff 2, ICU 기대값 4/8. 실제 library 실행 0/8; 동일 개별 레코드 전후 치환쌍 0. Numeric authority/geo ID 비교 0; gazette PDF screenshot 403, 공식 PDF text read. 독립 원결정 관측 0.
- 첫 재개 행동: RA 공식 원목록 https://iso639-3.sil.org/code_changes/change_request_index 와 발행자 연간 결정표를 접근 가능한 환경에서 직접 확보; B01–08 https://iso639-3.sil.org/request/2013-008 등 changes.csv decision_url 8개 요청/최종 결정 PDF를 저장·판독, 요청번호/결정일/시행일/정의/후계 집합 재대조. S001/2/5/6, S027–34 block 이유와 S018 별도 누락 위험을 해소하고 자연 모집 순서 재산출. B 보강층은 지우지 않는다. 8 결정과 12 공식 자리 남음. 이후 S110/111 Jira 및 같은 레코드 수정 전후(최소 단일 1, 분할 1), 실제 언어 문맥, product support를 확인. 불충족 조건은 RESULT 마지막 표에 기록. 
- 이번 작업은 웹 자료 해석이며 runtime/build·별도 대량 replay·설치 미실행. 후속 Codex는 다음 고정 입력으로 정규화 재생만(의도 복원 아님).

## 고정 입력과 후속 실행 명령 (미실행)
다음은 검증 담당자용. GitHub 공개 원판을 이미 읽었고 runtime은 실행하지 않음.
```sh
git fetch origin chore/workspace-foundation work/research-af-res-169
git diff --check 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..origin/work/research-af-res-169
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..origin/work/research-af-res-169
git show f5d2b2f95f8c6cf9c69f0f9b901780e91703e4b4:docs/workstreams/research/AF-RES-169/SELF_CHECK.md
git clone --filter=blob:none https://github.com/unicode-org/cldr.git cldr
git -C cldr diff release-34 release-35 -- common/supplemental/supplementalMetadata.xml
git -C cldr diff release-37 release-38 -- common/supplemental/supplementalMetadata.xml
git -C cldr show 731ecf1b0423681756eac52909e9e9238e985a18 -- common/supplemental/supplementalMetadata.xml
git -C cldr show d6fc7eac94df0673ecc6cab071b32efdec5cf18f -- common/supplemental/supplementalMetadata.xml
git clone --filter=blob:none https://github.com/unicode-org/icu.git icu
git -C icu diff release-67-1 release-68-1 -- icu4c/source/data/misc/metadata.txt
git -C icu show release-68-1:icu4c/source/test/testdata/localeCanonicalization.txt
```
CLDR 34 blob e361d2e3149d0dca004dbad99595f7ecb99d886c → 35 0e8bf14384c95acd1b66aa23461a78bace096a2c: puz/pub, lmm/rmx, yuu/yug, ymt/mtm added. 37 blob 0aa69fba73133707746221916b4fc2585defe069 →38 02d0bb226d645d84bb2a4b7ecb55c232f85b3dea: sap/aqt, leg/enl, duj/dwu, tid/itd added. ICU67.1 metadata 4f1c3d79b7529bf7851edae85a949f9e0e9858fc, ICU68.1 b14427a72a07dea7e86537fd14e79b9c454abf71; expected test blob e41eaac05a74669e8ae530387a215c4100633e57. Inputs eight above. For Codex runtime check only, use separately built pinned ICU4C 67.1 and 68.1; compile a minimal C++ harness calling icu::Locale::createCanonical(input).getName() for these eight, record version, input, output, status; compare to stored rules and four public expectations. Do not mark absent alias as known runtime result; split actual runtime differences are observations to be made. No installation or execution was done by this worker. Exact expected split runtime output is a conditional hypothesis from metadata, not public test verdict.

## Commits (checked representative files by SHA)
① 3b7b7b0bf9292ecf3b4b83ac46afc810059101b5 SCOPE
② ae906f324f634d557666183c6ab58e88335c1dfc FRAME_NOTE, frame and sources
③ 04af88d4622a7e7de3fb722293ac442a7e4a0ace changes, consumers
④ cfe2c4533bdbc177972cd8c75cfa5954d00b5583 COUNTEREXAMPLES and advice
④b cc2642e8750174d36c600f2c69b816c43fa0f26f correction and actual diff/ICU
⑤ f5d2b2f95f8c6cf9c69f0f9b901780e91703e4b4 RESULT, SELF_CHECK
Remote compare before this handoff showed 6 ahead, 0 behind, all 10 changed paths within owned_path, no dot-control modification. Handoff is separate 7th commit.
대표: RESULT.md three required tables; SELF_CHECK.md Q1–Q7; changes.csv (12), consumers.csv (33), advice.csv (11), frame.csv (715), sources.jsonl (127), SCOPE.md, FRAME_NOTE.md, COUNTEREXAMPLES.md.
색인 제안 한 줄: AF-RES-169 (PARTIAL) — 폐기 언어 코드의 역사 인용·후계 집합·CLDR/ICU 정규화·사용자 언어 의도를 분리, split alias 4+4 반례와 고정판/실제 수정 diff 및 전거/지명 비교, RA 원결정 0/8 재개 필요.
