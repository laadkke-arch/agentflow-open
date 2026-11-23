# AF-RES-073 자체 점검 — PARTIAL

## 판정 범위

실제 검색 입력 3건·9보기·18질의·90순위, 원문 작업52회와 총70연산의 기록은 완결했다. 직접 읽은 독립 원저작은 보수적 계보 병합 후43개다. 자료 수가 충분하다는 사실과 최초판 적격3건이라는 완료 조건은 다르다. 첫 main 추가판을 첫 공개 PR/창설판처럼 취급한 부분은 사후 정정되었고, P3의 C2는 실제로 후대에 추가되었다. 따라서 중앙 DONE이나 연구 완전 완료를 주장하지 않는다.

수치 기준은 [정규화 원장 수치](evidence/normalized-counts.json), 판단 근거는 [RESULT.md](RESULT.md), 실행 검산은 [수용 기록](evidence/acceptance-evidence.json) 및 [검사 영수증](evidence/validation-receipt.json)이다. 영수증의 checked_head와 입력 SHA256을 구분한다. 이후 문서 커밋을 이전 검사에 포함된 것으로 말하지 않는다. 마지막 결과 SHA에 대한 실제 check와 GitHub 재열람은 HANDOFF에 별도 적는다.

## 실행 영수증

결과 본문 고정 커밋 `d2ed9b26bd993cad0e7e5c58788bc59dbafc0be3`의 깨끗한 실제 checkout에서 증거 검사247항목·종료0을 얻었다. 지정 `session check --fetch`는 첫 fetch 실패(종료2)를 보존한 뒤 정확한 refspec 진단 조회와 재시행으로 종료0을 얻었다. 통합 HEAD는 `4d5185e75e52f405bfa7d149c32a0cd135395bbd`로 전진했지만 계약 hash와 고정 의존은 유지되었다. 허용 경로 밖·unmerged·계약 오류는0이다.

같은 커밋의 소유 경로 내부 임시 detached worktree에서 `python -B scripts/cloud_check.py --environment chatgpt-executor --fetch-contract --require-clean`을 실제 실행했다. doctor·acceptance·research-case·original-smoke·sessions 다섯 검사 묶음이 모두 종료0이고 시작/끝이 clean이다. [영수증](evidence/common-check.json)과 로그를 복사한 뒤 임시 worktree를 제거했다. 이는 저장소 공통 회귀 검사이며 JEP/SPEC 목표 시스템의 적용 시험이 아니다. 환경 이름은 호출자 표지이고 특정 클라우드 계정 연결의 증거가 아니다.

## Q별 답·원절·반증 탐색·재개 입력

| Q / 주장 ID | 답과 RESULT 행 | 직접 읽은 원절 주소·자료 ID | 자기 결론을 뒤집으려고 찾은 경로 | 판독 결과 | 남은 미확인 | 재개 최소 입력 |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 / C01 | 표1 P1/P2/P3. main-first 3입력은 확인했지만 창설판3건은 미충족. P1 첫 PR는 같고 P2/P3는 앞선 초안 존재. | [JEP122 L43–45·Appendix](https://github.com/jupyter/enhancement-proposals/blob/2b194a3c090fd375321871c47a3de503a0758206/122-jupyter-book-incorporation/jupyter-book-incorporation.md) REC-JEP-01; [SPEC9 첫 PR L135–138·171–173](https://github.com/scientific-python/specs/blob/6ddd0d85a8acf184e2e7e35899c0d80af639dc94/spec-0009/index.md) P2-POST-S09; [JEP97 첫 PR](https://github.com/jupyter/enhancement-proposals/blob/0f4510266ead738e62f1d9e412d6bb9e7eb7a97d/97-add-schema/add-schema-to-notebook-format.md) PS-P3-S03 | main added 이력·rename·삭제 후 재추가→생존 SPEC7 브랜치→사후 PR commits·added blob·March14판. | SPEC7 초기 전역 시드와 후대 권고가 다름; SPEC2는 파일명 재사용. SPEC9 알려진 대안 목록 변화. JEP97 불변/일대일은3월14일 추가. 최초판 가정이 무너짐. | 전체 PR-first 순위와 Git 이전 작성판. | JEP/SPEC 각 첫8 후보의 최초 PR added commit/path/blob, 원 Google/summit/3월1일 초안의 시점 고정판. 이전 frame을 덮어쓰지 말고 새 층 봉인. |
| Q2 / C02 | P1-B-Q1-R1/R2/R3와 P1-C-Q1-R2/R3; P2-B-Q1-R1/R2/R3와 P2-C-Q1-R2/R3; P3-B-Q1-R2와 P3-C-Q1-R3. C는 대상·역할을 특정하지만 새로운 유효 선택까지 보장하지 않음. | [Netfabb 그룹 기능](https://help.autodesk.com/cloudhelp/2025/ENU/NETF/files/GUID-1D986637-BDFE-46AA-94C1-F1E63E151FB2.htm) P1-B-S01/S03의 실제 주소·절은 sources에 보존; [Feast governance](https://github.com/feast-dev/community/blob/master/governance.md) P2-C-S03; [JSON Schema2020-12 core §8.2.1](https://json-schema.org/draft/2020-12/json-schema-core) P3-C-O3 | 의미가 비슷한 B 결과에서 대상·권한·독자 종류가 실제로 같은지 확인. C 후보도 범위 밖 자율성과 내부 위임을 대조. | 기하 객체 그룹과 사람의 관리권은 다름. 읽기권은 승인권이 아니고 canonical 표기는 불변 내용을 보장하지 않음. | 명사 복원만의 인과 효과, 질의 길이·역할 추론 영향. | 길이를 맞춘 대안 질의와 source-supported actor/observer 표기, 사전 봉인 및 결과 미노출 판독자. |
| Q3 / C03 | 표2의90행 전부. 82 URL,52문서 작업,46원저작 연결 순위(3중복 재사용). unread22는 실패가 아님. | 각 행의 실제 도착 URL·read_sections·source_id. [nbformat raw schema](https://github.com/jupyter/nbformat/blob/main/nbformat/v4/nbformat.v4.5.schema.json) P3-A-O2; 원시 영수증27파일의 SHA는 original-seal에 있음. | URL별로 같은 제품·번역·미러·도구 재작성 여부를 대조. 원 제목과 실제 도착 주소가 다른 사례 추적. | Netfabb판·OMI언어별·nbformat문서/코드·ONES글을 계보로 합침. Kobo로그인 실패, COPIM재작성, eduKate가상 사례를 원증거에서 제외. | 미열람22자리의 본문과 실패 원문의 내용. | 원순위 ID/원주소를 유지한 새 비용층에서 실제 발행자 원문; 원검색 분자에 소급하지 않음. |
| Q4 / C04 | P1-A-Q2-R5/P1-B-Q2-R1, P2-C-Q1-R2/R3, P3-B-Q1-R2/P3-C-Q2-R1/R2. 이동/책임수락, 개정/공개범위, 라벨유지/실제변환을 구별. | [Jupyter newsubprojects@2021](https://github.com/jupyter/governance/blob/9eb214d2f9a8ea51cb11e2f7e103ddd9213f4106/newsubprojects.md) P1-POST-S03; [VTML 원논문](https://www.w3.org/Conferences/WWW4/Papers/190/) P3-B-O3; OMI §versioning·migration P3-C-O1/O2 | 후보를 채택하면 원 조건을 깨뜨리는 최소 입력과, 두 선택이 같게 보이는 대조 입력을 원문 규칙에 적용. A의 가까운 기존 기능도 다시 비교. | P1 임시 적격1건 철회. 내부 위임은 범위 밖 독립성과 다름. private 인선은 all-public과 충돌. 태그 무시만으로 선택 버전이 보존되지 않을 수 있음. | 수신 프로젝트에서 입력을 실행한 결과, 변환 손실/실제 권한 감사. | judgments의 minimal_falsifier/control_input 쌍, 같은 버전·구성의 실행 로그 또는 운영 기록. |
| Q5 / C05 | 모든 행 target application not_run. 두 조건의 같은 구성 적격0, 적용 성공률은 분모0으로 산출 불가. | [nbformat v5.7.3 reads](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/nbformat/__init__.py) PS-P3-S12; [validator](https://github.com/jupyter/nbformat/blob/bbd0f83b67a126cd04c48a03ad053c52e6597d96/nbformat/validator.py) PS-P3-S13; 같은 SHA의 tests/test_api.py·test_validator.py PS-P3-S14/S15 | 원 시험·기존 release와 실제 코드를 읽어 ‘strict schema reject=reader fail’ 주장을 반증. 해당 SHA check-runs도 조회. | reads는 ValidationError를 기록한 뒤 반환 가능; future minor에서는 추가속성 완화. 시험 소스만 읽었고 실행 안 함. CI 반환0은 과거 실행 부재 증거가 아님. | 정확한 과거 dependency lock·실제 구형 앱 설정·C2 URI 바이트 고정 운영. | postseal/P3/NEXT.md의 버전·명령, fixtures.json 4입력, resolver/URI/해시와 실행환경 기록. |
| Q6 / C06 | semantic-overlap의41행. 부분 원리 교집합과 원저작/구현 동일성은 다름. 두 조건 적격 교집합0. | [NARA accession](https://www.archives.gov/records-mgmt/accessioning) POST-X-01; [AnnualMove §custody](https://www.archives.gov/records-mgmt/accessioning/annual-move) POST-X-02; [UAF §8.5–8.6](https://www.uaf.edu/theatrefilm/stage-managers-handbook.php) POST-X-03; [Kent pp39–40](https://www-s3-live.kent.edu/s3fs-root/s3fs-public/file/SM%20Handbook.pdf?VersionId=CZOkpiRCPICm8bJQIvjcJCT8lsTaplsO) POST-X-04 | 경로 봉인 뒤 두 독립 분야에서 같은 말의 다른 대상과 다른 말의 같은 역할 분리를 읽음. 동일 분야 Kent와 UAF도 대조. | 물리이전/법적수락, 준비응답/완료보고 분리. Kent에는 동일 완료규약 확인 못함. 법적custody와 OSS권한, 보고와 독립검증을 동치로 삼지 않음. | 실제 수신 설계에서 원리가 작동하는지. 사용자 예시 사전노출로 무힌트 발견 아님. | 같은 최소 입력에 대해 행위자·대상·관찰자·조건을 명시한 새 검증. 원검색 적중은 계속0 추가. |
| Q7 / C07 | 표3·decisions23행. 존재/저자인지/승인/실제 적용 결과를 분리. | [JEP122 승인](https://github.com/jupyter/enhancement-proposals/pull/123#issuecomment-2195794991); [SPEC9 PR323](https://github.com/scientific-python/specs/pull/323); [JEP97 March16](https://github.com/jupyter/enhancement-proposals/pull/97#issuecomment-1471548986); [nbformat PR343](https://github.com/jupyter/nbformat/pull/343); [WWW4 프로그램](https://www.w3.org/Conferences/WWW4/Program_Full.html) | 검색 봉인 후 유지보수자 발언·수정 patch·release를 직접 읽고 초기 선택과 대조. 새로웠다는 주장을 깨는 선행 인지 탐색. | P1조직편입 승인 확인. P2 Matplotlib 선행인지·single-vendor 삭제·draft 승인 확인. P3 strict/permissive 차이 선행인지·proposal수락 확인. VTML1995 존재 확인. | 실제 JEP97 구현출시, SPEC9 채택성과, P1개별권한/기술결과, VTML저자인지. | commit/tag/원시험 결과·당사자의 날짜 있는 선택 설명. gist 최초판·history. 현재순위로 당시순위 추정 금지. |
| Q8 / C08 | 표3 및 비용표. A22/B24/C24;공통비용P1=7/P2=7/P3=8;적격전부0;first-qualified null. 사후62는 별도. | runs166행, original-seal27파일, postseal-costs62행연결. 각 open은 source 및 rank로 연결. | 실제지출과 상한을 다시 세고, 더 긴 보기의 마지막 원문을 제거해 비교. 중복 재사용과 실패 비용 유지. | P1/P2의 비용8 문서는 동일비용7에서 제외. 부분 원리의 종류는 다르지만 효율 우위는 입증 안 됨. | 전체 연구 노동시간·도구 내부 HTTP/토큰비용·모집지원연산의 통일된 비용·사용자 시간 절감. | 동일 비용의 추가 실험·실제 판독/구현/승인 행동의 시간 및 결과 관측. |

## 오류 발견과 수정의 계보

- 원 검색·열기·출처의27개 봉인 파일은 변경하지 않았다. 뒤늦게 발견한 사실은 postseal과 파생 판정에서만 반영했다.
- P1 A의 임시 적격1건은 C1의 구체적 표준·프로토콜 기준을 일반 연동성으로 대신한 문제로0으로 수정했다. 임시 판정 커밋과 self-review를 유지한다.
- P1 B receipt의 ‘July2024’ 자동노출 설명은 실제 최초 Git May22의 오기이며 date-audit에 정정했다. 모집 날짜·질의는 원래 정확했다.
- P3 C checkpoint의 unread0은 status명 집계 누락이었다. 원순위 기준 미열람2로 파생 원장을 맞췄다. 검색반환 시점/보기총비용을 판독 비용으로 쓰던 표기 역시 실제 open 연결로 고쳤다.
- 통합 판독 여부와 최소량 산입 여부를 분리했다. 같은 저작의 후속판도 직접 읽었으면 읽은 사실을 보존하지만 독립 수를 늘리지 않는다. PR343/릴리스는 nbformat 구현 계보에 보수적으로 합쳤다.
- queries.jsonl의 removed는 A행에도 제안별 삭제 후보 목록이 반복되는 메타데이터다. A의 실제 질의는 명칭을 보존하며 실제 삭제/복원 대응은 query-mapping.csv의 A공란·B/C열을 따른다. IA-07에 명시하고 원질의를 고치지 않았다.
- P2 표1의 연구자가 구체화한 두 선택과 원문의 실제 모델 목록을 구분했다. P3의 contradict는 공여 규칙을 그대로 적용했을 때의 조건 충돌이며 목표 실행 반증이 아니다.

## 실제 판독자와 검토의 독립성

root와 같은 모델의 분담 에이전트3개가 실제 자료를 읽었다. P1/P2/P3의 원문·질의·비용 기록을 분담했으며, root가 통합과 비소프트웨어 사후 대조를 했다. P1 담당은 통합 원장과 계보·원문 플래그를, P3 담당은 RESULT의 주장·조건·수치를 다시 대조했다. [원장 검토](review/ledger-review.md), [결과 검토](review/result-review.md)에 범위가 있다. 같은 모델 협업 검토와 자체 재판독으로 표기한다. 독립 인간 판독자0, 눈가림된 피험자0, 무힌트 인간 실험0이다. 원문의 가용성 문장과 후속 결과의 미리보기 노출도 exposure에 보존한다.

## 수치의 의미와 남은 행동

관측된0: 두 조건을 같은 구성에서 지지한 적격, 원 검색 분자에 추가된 사후 자료. 분모0 산출불가: 목표 적용 성공률. 미측정: 실제 사용자 시간 절감·역할별 작업 비용·목표 시스템 실행. 접근 실패: Kobo 로그인 원문1회 및 사후 Discourse2/gist2; 원저작 부족과 혼동하지 않는다. 미열람22자리는 내용의 부정 판단이 아니다.

재개에 필요한 첫 입력은 첫 PR/창설판의 모집틀이다. 현재 기록을 보존하고 새로운 질의 봉인을 만들어야 한다. 이어서 판정자가 고정 조건·관찰자·최소 입력을 받아 목표 시험을 실행한다. 정확한 실행 안내는 [reproduce.md](reproduce.md), [P3 NEXT.md](postseal/P3/NEXT.md)에 있으며 실제 실행하지 않은 명령은 실행 결과로 세지 않았다. 마지막 불일치·다음 조사·판단이 바뀔 관측은 RESULT 맨 마지막 W1~W3 세 행으로 고정했다.
