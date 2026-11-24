# AF-RES-156 HANDOFF — PARTIAL
- 작업: 기존 시간대 부품을 쓰는 소비자의 실제 이관 노동, Django/pandas. 본 작업은 자체 시간대 알고리즘 신규 구현을 하지 않았다. 원격 연구 문서·원장만 추가. dot-control.json 변경 없음. 계획 SHA f140af3179b7d9271710778104ccee5b4812e2ef, 실제 base 35ca756d1b18af5d89c3eb53659365c09f1f88e3, dependency AF-RES-147 result 30afd115c302f468d5007e380f72228c45130c37 (RESULT 3a6794815caedd96f06752e042f11143f664861d). 147 결과 재실행하지 않음.
- **결과판(인계 직전 고정 SHA)** ef71cee3114731142a50b06eb63efb9d250b5934. [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/ef71cee3114731142a50b06eb63efb9d250b5934/docs/workstreams/research/AF-RES-156/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/ef71cee3114731142a50b06eb63efb9d250b5934/docs/workstreams/research/AF-RES-156/SELF_CHECK.md), [원장](https://github.com/laadkke-arch/agentflow-open/blob/ef71cee3114731142a50b06eb63efb9d250b5934/docs/workstreams/research/AF-RES-156/sources.jsonl). 인계 자신 SHA는 순환 참조하지 않고 작업 브랜치 HEAD로 확인.
- 판정: 출처 개수와 2개 프로젝트 실제 변경/도메인 게시 원자료 확보. Q1 earliest generic support·same-day tag ordering, Q4 엄격 첫 여섯 배포 사건/전체 후속 변경 기록, pandas +2 후속 기능판, Q7 offset 없는 역사적 시분초·실운행 조인, 실행/CI/공통 체크 결측 때문에 PARTIAL. 사람 시간과 일치 대안 미관측으로 총 순절감은 계산 불가(0건 측정, 노동이 0이라는 뜻 아님). 별개 시간대 부품 전환이지 이전에 자체 tzdb engine을 구현하려 했다는 증거 없음.

## 판단을 다음 설계로 전달
Django D1–D8: 3.2 선택 지원→4.0 기본 및 4.x 호환 유지→4.1 UTC alias 경고→5.0 제거. D6 core +6/-66은 실제 adapter 제거이며 배포는 주요 4.0→4.2 창 외. D3 serializer 일부 간소화, D4는 이미 동일 UTC 객체 이름 변경. 다운스트림 X1 django-rq 경고→5.0 관련 patch +3/-1. X2/X3 django-upgrade 1.8.0 자동 fixer가 import 오류를 생성, #174 보정. P1/P2: 1.5 명시적 지원→3.0 default ZoneInfo/ValueError, 명시적 pytz 계속. P3/P4: 실제 reporter benchmark 119ms vs 11.3ms, fastpath 추가. P5: future cutoff 회귀, 제안 미병합. P8: pandas 3.0.3의 key 기반 cache가 from_file 원자료를 바꾸는 13h 오류, 3.1 fallback; PEP615. 저자 보고 P7 28,704 fuzz는 실행 증빙 아님. 기존 엔진 재사용으로 무엇을 없애는지와 소비자가 맡는 입력 정책/호환/시험/설치/직렬화/운영을 나란히 건네고, 사람 시간 없이 절감량 단정 금지.
T1/T2 실제 JR East/Osaka Metro 시간표에서 24시 이후 표기. 계획과 실제 운행 구별. A1/A2 AAPB 실제 catalog date(1961-00-00, 1962-02-28 created vs 1962-04-21 broadcast), NARA digitized vs source creation 규약. 원시 서비스일/정밀도/종류 보존 조건, 해당 기관 소프트웨어 사용 미추론.

## 실제 커밋 및 원격 검사
| 묶음 | 고정 SHA | 재열람 |
|---|---|---|
| ① 범위 | 6b27d5a329cfe78cf5de4ccd2972b9f6bf7476de | SCOPE 원문 match |
| ② 모집·기준 입력 | 3387248581df67fecc3e4d5db4ff0d02fa2bd2e9 | timeline match |
| ③ 관측 | 06220b96ac3a4d6623dfdd8ca846d173ddd82b8a | changes match |
| ④ 반례·비용·분야 | 56ecc979948e009e6ae3205520ee329ac11ecd90 | sources/effort/downstream match |
| 보정(원판 보존) | e68281ad1a38fc300748f540f36e4ad9bd9c4f1d | SCOPE_CORRECTION/release_refs/merge_parents/sources match |
| ⑤ 결과 및 자기검토 | ef71cee3114731142a50b06eb63efb9d250b5934 | RESULT 18988자, SELF_CHECK 4678자 exact match; 11개 파일 전부 다시 fetch |

결과판 원격 재집계(JavaScript에서 connector response content parse): JSONL 77개 행/77 고유 ID, 필수 키 누락 0, HTTPS 아님 0, counted 29/29 고유 work_id(Django 결정 6, pandas 4, 소비자 변경 10, 규약 5, 교통 2, 아카이브 2). 미산입 48(9 실패/불충분 포함). RESULT/SELF_CHECK/effort/downstream의 명시적 S-ID 참조 60종, 원장 결손 0. 범위 표기는 범위로 읽어 자기검토에서 대조했고 모든 외부 링크 재접속이나 의미 검증 자동화는 하지 않음. CSV 행 수/열 수 timeline 27/8, changes 16/15, effort 12/11, downstream 3/9, release_refs 15/5, merge_parents 8/9; 필드수 불일치 0. release_refs 키는 project+tag(프로젝트만으로 고유 ID가 아님). 결과표 data rows(마지막 분모 행 포함) 7/16/7/3, 마지막 약점 3 정확. Compare base→result ahead 6, behind 0, 11 files all within owned prefix, outside 0. 전부 원격 읽기/정형검사, checkout 검증 아님. 실제 환경/모델 tier 검증 불가; 독립 평가자 없음, 자체 검토. 
실행검사/manifest 생성은 미실시: 이 세션은 GitHub connector를 통해 파일 작성과 원격 읽기를 수행했고 로컬 git checkout이나 프로젝트 CI를 실행하지 않았다. 시간 절감 추정이나 외부 CI 성공 주장 없음.

## 실행 가능한 다음 첫 행동
1. 다음 worker는 본 HANDOFF, RESULT, SELF_CHECK, sources, SCOPE_CORRECTION을 결과판 SHA로 읽고 아래 명령으로 disposable checkout에서 계약/소유 경로 검사를 보강한다(원본 원격 경로를 수정하거나 결과 SHA를 다시 쓰지 말 것). 새 manifest 작성은 원래 시작점에서 준비한 기록이 없으므로 **사후 재검증**이며 처음 실행 전에 봉인한 manifest라는 주장 금지. AGENTS.md / docs/CLOUD_WORKFLOW.md의 실제 CLI 및 dependency branch 확인 후 실행. 실패 시 stdout/exit code와 실제 SHA 기록.
```sh
git clone https://github.com/laadkke-arch/agentflow-open.git af-res-156-check
cd af-res-156-check
git checkout --detach 35ca756d1b18af5d89c3eb53659365c09f1f88e3
task=docs/workstreams/research/AF-RES-156
mkdir -p "$task"
python -B -m workbench.session start af-res-156 --allow "$task/" --dependency work/research-af-res-147=30afd115c302f468d5007e380f72228c45130c37 --output "$task/manifest.json" --fetch
git checkout --detach ef71cee3114731142a50b06eb63efb9d250b5934
python -B -m workbench.session check "$task/manifest.json" --fetch
python -B scripts/check.py --require-git
# Codex Cloud 환경에서 실제 필요한 경우:
# python scripts/cloud_check.py --environment codex-cloud --fetch-contract
git diff --name-only 35ca756d1b18af5d89c3eb53659365c09f1f88e3 ef71cee3114731142a50b06eb63efb9d250b5934
```
2. 외부 재현은 별도 허용 환경에서 의존 설치/격리 후(설치 미실행) 실제 버전 확인: Django 3.1.7,3.2,4.0,4.1,4.2,5.0 각 tag의 timezone/form/migration writer tests; 3.1.8/3.2.10의 공개 순서. pandas v1.4.4/v1.5.0/v2.0.0/v2.1.0/v2.3.3/v3.0.0/v3.0.3/v3.1.0의 해당 test 소스/실행 로그. Django 공식 checkout의 tests/runtests.py utils_tests.test_timezone migrations.test_writer (실제 실행 환경 및 모듈 확인), pandas checkout에서 python -m pytest pandas/tests/tslibs/test_timezones.py pandas/tests/indexes/datetimes/test_constructors.py pandas/tests/io/json/test_pandas.py (빌드 및 버전에 따른 파일·모듈 확인). 정확한 고정 입력: D1 2011-09-01 12:20 Europe/Paris; 2015-10-25 02:30 fold 0/1; P2 2024-01-01 US/Pacific 및 ambiguous/nonexistent exception; P3 Europe/Paris minute range 2024; P5 Brussels 2038/2100/2200 July UTC; P7 1800-01-01 Asia/Tokyo sub-minute offset; P8 실제 TZif Asia/Tokyo bytes, key US/Eastern/None, compare 3.0.3 vs 3.1.0. 같은 tzdb 버전/offset/원시 key/data hash/exception/result/elapsed를 기록. 기존 147 replay를 반복하지 않는다. 사람시간/비교 대안 확보 전에는 계산 금지.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| Q1/Q4 엄격 모집 미완, pandas +2 미발표 | 처음 여섯 사건·동일 기간 배포 부담 완결 아님 | 태그 peel, 2.0/2.1/4.2 전체 변경·3.1 링크, 새 기능판, 최초 지원 이전 API 테스트 | 다른 최초 지원판 또는 실제 추가 배포/반려 사건 |
| Q5 matched 사람시간/운영/CI 미확인 | 코드 삭제→총노동 절약 수치 불가 | 담당자 공개 작업기록·지원 티켓·CI artifact 및 동일 입력/기간 비교 | 양쪽 실제 노동의 동일 범위 합계 또는 회귀 반증 |
| Q7 공식 시간표 2, 실제 catalog 2지만 원행 운행 조인/역사적 시분초 없음 | 분야 정책 필요만 확인, 해당 조직 실제 이관 미확인 | MBTA archived trip 25906883 stop1721 및 actual record; 원 offset 없는 역사 메타데이터/디지털 생성시각 | 원자료와 UTC 변환 오류·회복의 재현/조인 |
