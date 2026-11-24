# AF-RES-153 HANDOFF — PARTIAL

- 작업자 수용 상태: **PARTIAL**. 원문 20저작 조건부 산입(특허 발행 원면 제3자 호스팅 포함; 공식 호스트만 인정 시 14), 핵심 직접쌍 0/8, 적격 독립 연구 0/2. 모집창 A4/B7로 15→30씩 완결 못함. 비교군 실제 개봉/개인 원면/탈락 조인 미확인. 11 사례행을 참가자 전후쌍으로 속이지 않았다.
- 실제 작업 문맥: 단일 GPT-6.2 응답, 공개 웹 + GitHub connector, 독립 검토자 0, 신규 인간 참여자 0. AF-RES-145 사전안/판정/인계 노출 있음. 145 중앙 DONE이나 고정 인계 PARTIAL. 8이슈 재검색/자기 판정 사람 전환 없음.
- 실제 시작판 9e378ca91c399454466196617cf362d0cdb514f9. 계획판 f140af3179b7d9271710778104ccee5b4812e2ef보다 ahead3/behind0, 변경 dot-control 한 경로 +92. sole predecessor 145 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/116eae3d2e252cfc1ee4da7017228db24fad42f0/docs/workstreams/research/AF-RES-145/HANDOFF.md) 및 원장, [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/2f41c8650ff45e531ce501118cc8b28296c74db9/docs/workstreams/research/AF-RES-145/RESULT.md) 읽음. 다른 배정 대기 없음. dot-control 변경 없음.
- 브랜치 `work/research-af-res-153`; 허용 경로 `docs/workstreams/research/AF-RES-153/`. **result_commit: f92048ad779897a10fafaf2ca2ca84c975cd42c9**. 이 HANDOFF만 마지막 별도 커밋(자기 SHA 본문 기록 불가; 응답에서 실제 SHA 보고). 결과판의 11 파일 전부 재열람 검산 완료.
- 판단: 사람의 실제 시각/구조 차용 및 실패의 부분 증거, 할당 자극에서 읽을 수 있는 새로운 작동 선택과 조건, 현장 팀 수정 사례를 찾았다. 그러나 같은 참여자의 사전 설계/실제 예시 열람/사후 설계를 연결하지 못했다. 개인의 신규 선택률, 자발적 검색 성공률, 시험 개선률, 근/원거리 인과 효과, 링크 형식별 시간·품질 개선 산출 불가. 0 유효쌍은 0 효과가 아니다.

## 커밋 및 원격 재열람
| 묶음 | 실제 원격 SHA | 대표 재열람 파일 / blob |
|---|---|---|
| ① 범위·판정 | e8a00888ed5029b758a4a833335b817b23463299 | SCOPE.md 28ca7b1e7ac3cd1114dc86ddbc0e4da5e872edb3 |
| ② 모집·기준 | d74d80b7e87319140372a2a0a8193d981877ef48 | frame.csv 189484eae432dcbf07d4e5de2f28163b23fd0c11 |
| ③ 본 관측 | 01a78c206c33d71ed166a5cff05b604054c50d18 | pairs.csv fb28415cbd9fbdeef7c07f6fbc61aff0171b77c8; exposures.csv 869d59c27c9f7d95b8bac9ba562d55afbfeb0f57 |
| ④ 대조·비용 | ee78f61491bbea4c644f8844b4e32f81c2302019 | sources.jsonl 1d636c3cf9afa615ab4cd2dcf6c9e25a6874c6f1; contrasts.csv 98cbdd47ff897d1347e0df63c0e037fa52d023a0 |
| ⑤ 필수 표·SELF_CHECK | f92048ad779897a10fafaf2ca2ca84c975cd42c9 | RESULT.md c15419562f218bd54d4cb4b041f32d0e8a7c7695; SELF_CHECK.md bbfa28605646de7558f1f87cb141f8cdad866185 |

⑤ 실제 시작판과 compare: ahead5/behind0, 추가 파일 11, 전부 owned_path, 외부 변경 0. ⑤에서 위 7개 대표 파일 포함 SCOPE/frame/frame-extension/SEARCH_LOG/exposures/pairs/contrasts/sources/COST_AND_ACCESS/RESULT/SELF_CHECK 총11개 재열람. RESULT/SELF_CHECK는 작성 내용과 정확 일치. JSONL 파싱, CSV 참조 재대조: source 34행, counted 20/고유20, strict 0, 존재하지 않는 source_id 참조 0. 고정 결과판 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/SELF_CHECK.md), [sources](https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/sources.jsonl).

## 분모 및 제한
| 항목 | 실제 | 목표/제한 |
|---|---|---|
| 모집 | 38 표시 반환행(11/8/8/11), 고유 층내 후보 A4/B7, 보충8행 | native 순위 아님, 층별 최초15·다음15 미완료 |
| 직접 읽은 저작 | 성공26자료행, 부분3, 실패5; 최소 산입20 고유=실험10(A4/B6)+특허6+현장2+2 | 20 조건부; 특허 원면 공식 호스트로만 좁히면 14. 제목/요약/중복/미접근 불산입 |
| 자극·배정 | 노출원장12행, S14 특허 8개 중 원면6 열람 | 개인 실제 자극/개봉/시각 불명; S25/26 미접근 |
| 전후 | 11 사례/반쪽/실패행, 엄격0; 유효 연구0 | 8쌍/2개 연구; 최초 4 익명 ID 선택 불가능 |
| 대조 | 19행, 무예시 특징·자기 고착·먼 예 실용성 감소·복사·실패 원문 보존 | 개인 대조/탈락 재계수 불가능, 검색 성공 유효분모0 |
| 시간 | 과제 분·시스템 지연·조사 경과를 분리 | 정확한 개인 열람/조사 인시, 토큰·비용, 링크 형식 차이 미측정 |

## 재개할 첫 행동과 명령
첫 행동: 결과판에서 [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/SCOPE.md)의 네 검색식·원래 반환순을 읽고, ACM DL / Design Society·ASME 네이티브 검색 UI에서 2010–2025 관련도순 목록의 원시 캡처/UTC를 먼저 보존한다. 15고유저작→적격 2 미만이면 다음15로 확장; 기존 프록시 순위/결측과 분리한 새 보정 파일로 남긴다. 각 저작의 author supplemental/OSF/Zenodo/대학 저장소를 끝까지 추적. 기존 고정판 덮어쓰지 않는다. 동시에 다음 정확한 자료부터 실제 다운로드 가능한 웹/실행 환경에서 확인:
- A03 S04 GitHub brownhci/sketchy-1.0 `data/pilot_data/sketchy_dec6_dec13_peeks_updated.csv` (15,062,721 bytes, blob e2a18ceca7542a754ba2c039ad4c9ed33c921ac5), README c89d7ed513afbf54c89720b220471802929f76c5; S05 Drive DB 백업 공개 링크. 읽기 전 파일 SHA256/열 이름/행수, ID·task·pre timestamp·peek timestamp·post version 연결 존재 여부 먼저 확인. 개인 식별 추적 금지.
- B07 S12 DOI 10.17863/CAM.69091, delftdata.zip 39.2MB; 직접 저장소 timeout. ZIP 목차, 스케치/CSV 식별자, 사전 단계 여부 먼저 확인; 없으면 탈락 사유.
- B04 S10 p533 Table2 패킷(본문 4,7,12,13 vs 표 4,7,11,12) 원 과제지와 배정표, B06 S14 실제 봉투별 개봉·초기/사후 그림 및 무예군, B09 S15 Fig2의 anonymous midpoint ID→자극→최종안 및 손상6 원자료. A05 S16의 실제 145 사건 원문·prior ID. X11 S18 OSF sbp2k 공개 파일(403; API도 실패)은 IEEE 별도 사례층, 정규 두 층 대체 금지. 각 저작별 최초 적격 4개 익명 ID만, no-change/탈락/한쪽 포함.
- S19–26 USPTO 공식 호스트의 8개 발행 원문 직접 확인(원면 2개 미접근, 6개 호스트 불일치); 동일 특허 중복 제거. 실험 원전과 발명자 원전 별개.
- 확보된 최소 자료가 있으면 Q별 새 관측/보정 커밋→동일 과제 대조군의 기저 선택·유지·악화 재집계→독립 검토자가 원전과 판정 검토. 새 인간 실험/외부 참여자 모집을 임의로 만들지 않는다.

실행 실패: container git ls-remote exit128 github.com DNS; python -m workbench.session --help exit1 ModuleNotFoundError; 원자료 raw fetch DNS, 대형 파일 본문 비어 있음/403/timeout. 체크아웃/manifest/공통 검사 미실시. 다음 네트워크 및 저장소 checkout 가능한 환경에서 실행(입력 정확):
```sh
git clone --no-checkout https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
git fetch origin chore/workspace-foundation work/research-af-res-153 work/research-af-res-145
git checkout --detach f92048ad779897a10fafaf2ca2ca84c975cd42c9
git rev-parse HEAD
git diff --name-only 9e378ca91c399454466196617cf362d0cdb514f9 HEAD
python -m workbench.session --help
python -m workbench.session start --help
python -m workbench.session check --help
python scripts/check.py --require-git
```
첫 두 명령은 로컬 미설치/미연결 환경에 한함. HEAD는 위 결과판 정확 SHA, diff는 11개 파일만 예상. 마지막 명령/manifest 규약은 현재 저장소 도움말과 AGENTS에 맞춰 실행, 결과 stdout/stderr+exitcode+SHA 보존. 원래 작업 시작 manifest를 사후 생성해 당시 실행으로 속이지 않는다. 재개 세션은 결과판을 읽은 뒤 최신 작업 브랜치 HEAD(인계 포함)를 확인하고, 허용 경로 및 145의 116eae3d2e252cfc1ee4da7017228db24fad42f0 의존을 고정한 새 세션 manifest를 허용 경로 안에 만들고 check --fetch한다. 명령 지원 여부와 입력 불일치가 있으면 그 자체를 기록. 기존 커밋 원본 보존. 

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| native 모집 15→30 미완료, A4/B7, 원파일 차단 및 특허 호스트 | 대표성/원전 하한 엄격14·조건20; 접근 실패≠공개 부재 | 원래 모집 재현/확장, S04/05/12/18 원파일 및 공식 특허 원면 | 두 독립 연구 최초 ID 8쌍 조인과 원전 하한 충족 |
| 엄격 분모0, 선택/부분행11; B04 과제표 불일치, 비교군·탈락 조인 미확인 | 실제 선택 변화·비교·검색 인과 결론 없음 | B04/B06/B09 패킷·최종안·무예 대조·개봉·결측, 독립 판독 | 동일 개인/과제/시각에서 변화/무변경/악화와 대조군 차이를 재계수 |
| 발명자 청구·팀 보고·연구자 구현을 실제 개인 채택·시험으로 치환 불가 | 작동·경계 링크는 제안, 효과/시간 개선은 미검증 | 원 과제 보존조건, 실제 실패·회귀 시험 원면 및 같은 링크 두 형식의 사람 작업자료 | 실제 새 선택/시험 변경과 보존/위반, 링크 형식 시간·품질 차이 관측 |
