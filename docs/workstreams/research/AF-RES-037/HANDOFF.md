# AF-RES-037 · HANDOFF

**상태: `recorded_with_unmet_conditions`.** 고정한 A8·B4를 추적하고 원장·결과·재집계·검사 기록을 커밋했다. 고유 외부 1차 저작 최소수와 필수 형식은 충족했다. 수용 조건 24개 중 5개는 미충족으로 남겨 종료한다. 엄격 사슬 0건은 관측 결과이며 그 자체가 미충족 사유는 아니다. 역사적 프로그램 실행은 미확인이다.

## 고정 결과와 찾아갈 위치

- 저장소: `laadkke-arch/agentflow-open`; 작업 브랜치: `work/research-af-res-037`.
- **결과 SHA: `c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b`**. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/RESULT.md), [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/evidence/acceptance-evidence.json), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/SELF_CHECK.md), [반환 카드](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/cards.md).
- 필수 표 1: 고정 `RESULT.md` L3–16, 제목 바로 뒤 A/B 전체 12사건.
- 필수 표 2: 같은 파일 L18–24, 엄격·회고/유추·별도 코드 기준 감도.
- 같은 우선순위 약점 3건: 같은 파일 L146–150. 이 HANDOFF 끝에도 동일 내용을 보존했다.
- 작성·수정 범위: `docs/workstreams/research/AF-RES-037/`만. `dot-control.json` 수정 없음.
- 계획 기준: `chore/workspace-foundation@922bf3171cab62f30469720ac80327ad3f24fbf9`.
- 실제 배정·scope 기준: `de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62`. 배정 환경·모델 표시는 [manifest.json](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/manifest.json)에 기록했다. 세션에서 확인 가능한 모델 표시는 GPT-6 Astra Pro이며 별도 `web-pro` 모델 선택 상태는 미확인이다.
- 의존 고정본: AF-RES-017 `34c14d6d2ad8802cf68ff9d9db4a3f810b4e057a`, 022 `df80ec2406042a73c2114e316894173f66309cda`, 033 `03ff2eb1264b85016266de1f36ddebe45f5fface`. 지시된 운영 문서와 의존 HANDOFF·033 결과를 읽고 중복 제외에 반영했다.

이 HANDOFF는 결과·수용 원장을 원격 고정 SHA에서 재독하고 아래 세션 검사가 종료된 **후에 작성한 마지막 별도 커밋의 유일한 파일**이다. 자기 자신의 커밋 SHA를 본문에 소급 기입하지 않는다. 최종 SHA는 이 파일을 추가한 커밋 또는 `git log -1 --format=%H -- docs/workstreams/research/AF-RES-037/HANDOFF.md`로 확인한다.

## 결과 해석

| 조건 | A | B | 해석 범위 |
| --- | --- | --- | --- |
| 최초 수신 제안 기준·명시 인과·모든 접점 확인 | 0/8 | 0/4 | 정확한 선행 원전, 작성자 연결, 같은 기준선의 선택 변경, 같은 목적 반영을 모두 만족한 사슬 없음 |
| 회고·유추를 허용하되 같은 최초안 기준 유지 | 0/8 | 0/4 | 유용한 작동 유사성 후보 A1/B3와 완결 인과를 구별 |
| 표준을 포함하고 기존 실행 코드로 기준선을 이동하는 별도 감도 | 해당 감도 대상 없음 | 1/4 — B02 | GMLJP2 파일 경계의 좁은 축 순서 준수 사슬. 저자의 첫 학습·새 원리 발견을 뜻하지 않음 |
| 엄격 역사적 양성 대조 적격 | 0 | 0 | 조건부 회수율은 양쪽 모두 **해당 없음** |
| 같은 목적의 후속 반영 기록 | 7/8 | 3/4 | 고정 명세·코드·시험·완료 공지를 정적으로 읽은 수. 역사 실행 성공 수가 아님 |

A-G03의 CRS 식별과 데이터 축 매핑은 최초 실질안에 이미 있었다. API WKT1 기본 유지·CLI WKT2 전환이라는 후속 선택 변경은 별도 하위 결정이다. B02도 최초 RFC 정책과 기존 코드→패치를 섞으면 다른 질문에 답하게 된다. 반대로 B01은 hz 영감과 알고리즘 독립 구현을 함께 말하며, B03는 1998 초기 소스에서 기존 글꼴에 대한 불만·새 Feta·이름 있는 악보 본보기를 확인했다. 정확한 제공 원전과 이전 선택의 공백 때문에 둘 다 엄격 양성으로 올리지 않았다. B04의 역사 독서는 먼저 정한 수학적 표현을 설명할 가능성이 남고 원 발행본 접근도 실패했다. 근거 URL·절과 반대 근거는 위 필수 표, `chains.csv`, `judgments.csv`에 연결했다.

검색기에 반환할 12카드는 시점·용도 한정 선례 2개(A-G03/B02), 잘못 닮은 링크 8개, 판정 보류 2개(B01/B03)다. 전체 설계와 독립 부분을 분리했다. 저자가 원리를 처음 알게 된 시점과 역사적 검색 색인 존재는 12건 모두 미확인이다. 이번 조사에 새로 등장했다는 사실을 작성자의 무지나 검색 성능으로 바꾸지 않았다.

**색인용 한 줄:** AF-RES-037 — 결정 우선 A8·출처 명시 B4, 고유 1차 저작49; 최초안 기준 완결 인과 A0/8·B0/4, 표준 포함·기존 코드 기준 B02만 조건부1/4; 기존 결정 설명·새 학습·정적 반영을 분리하고 원전 공백과 반례 미확정을 보존.

## 확인한 범위와 재계산

| 항목 | 고정 수치 | 확인 범위 |
| --- | --- | --- |
| 선정 사건 | A8 + B4 = 12 | CSSWG4·GDAL4, B의 인쇄/지도/음악 경로; A/B 같은 사건 중복0 |
| 표집 원장 | 219행 | CSS40, GDAL76, B103. B는 분야별 최초10결과30행과 예산 밖73행을 구별. GDAL76에는 기간 전 경계71행·title-only1행이 포함됨 |
| 출처 원장 | 168행 | 기존 stream159 + 반례④ 보조9. 실패·판 복원·후속 조회도 포함하므로 168개 원전 열람이라고 표현하지 않음 |
| 고유 직접 열람 1차 저작 | 49개 | A 최초8 / 제공 규칙10 / 수신 후속15 / 독립 반대 기록10 / 추가 초기·기준선·선행 구현6 |
| 더 보수적인 출처 감도 | 46개 | NUMDAM2와 mutable NEWS1을 제외해도 범주별 최소수 충족 |
| 판단 행 | 25행 | 엄격12 + 회고/유추12 + B02 감도1; 감도 행은 새 사건이 아님 |
| 구조·참조·재집계 검사 | 130/130 통과 | source 필수 키·고유 작품·사건 결합·실제 CSV 행·두 필수 표·원장 참조 등 |
| CSV 독립 가져오기 | 3파일 성공 | Artifact Tool: frame219×24, chains12×31, judgments25×29; 원본 해시 대조 |
| 수용 조건 | 19/24 met | 아래 5개 미충족; 구조 검사 통과와 구별 |
| 역사 런타임 | 0건 실행 | 정적 문헌·패치·시험 확인과 구별 |

원작품 한 개는 한 범주로만 계산했다. B02의 인접 코드13570·시험13569는 같은 변경 작품으로 묶어 stream 단순합50→49로 정정했다. 제공 규칙10은 실제 인과 donor10이라는 뜻이 아니다. 명시 연결 선행작2, 당시 관련 규범 계통5, 후기·다른 실무 비교3으로 나눴다. 원래 기록과 정정 이유·분모는 `evidence/protocol-amendments.jsonl`에 보존했다.

재계산 근거는 [recount.json](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/evidence/recount.json), [validation.json](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/evidence/validation.json), [CSV 확인](https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/evidence/csv-verification.json)이다. Q1~Q7별 직접 근거·반대 근거·남은 미확인은 `SELF_CHECK.md`와 수용 JSON의 `questions` 배열에 있다. 물리적 CSV 행은 `evidence/csv-row-locations.json`, 출처 행은 `evidence/source-locations.json`으로 다시 찾는다.

## 미충족·막힌 이유·다음 첫 행동

| 조건 | 관측 분자/분모 | 막힌 이유 | 첫 재개 자료·행동 |
| --- | --- | --- | --- |
| AC03 A 최초판 동결 전 완전한 후속 결말 비노출 | 7/8 | A-C03 선정 후 최초판 복원 중 후속 결의 검색 스니펫이 노출됨 | `streams/csswg/method.md` L20·AM01을 읽고 고정 표집을 유지. A-C03 제외 감도0/7을 사용; 사후에 비노출로 복구하지 않음 |
| AC05 B 원 발행자/기관 초기 수신 본문 | 3/4 | B04 AMS403·Stanford503; Typekit 미러는 최소수에서 제외 | [Stanford STAN-CS-78-648](https://i.stanford.edu/pub/cstr/reports/cs/tr/78/648/CS-TR-78-648.pdf) 기관 원본 접근과 동일 발행본 여부부터 확인 |
| AC06 B 핵심 제공 원전 접점 | 1/4 | B01 hz/URW1993, B03 정확 악보 판·이전 글꼴, B04 Goudy/Zapf 원전·원 수신본 공백 | 우선 [LilyPond1.0.1](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)의 `Documentation/tex/fonts.doc` L11–23 및 `mf/feta-toevallig.mf` L10–28에서 명명된 악보의 정확 판을 식별하고 그 판을 직접 읽음 |
| AC18 다른 분야 원리 자체의 독립 발명 | 0/1 | pdfTeX의 알고리즘 독립 구현은 원리의 독립 발명을 입증하지 않음 | [Thành2000 §4 p38·참고문헌40–43](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf)에서 영감과 독립 구현의 대상을 분리한 채 최초 설계 기록 탐색; 인용 부재만으로 확정하지 않음 |
| AC19 확정된 타 분야 채택을 공급자 제약으로 반영 전 새로 포기 | 0/1 | RFC72 v1부터 조건부이며 최초 보존 CI 코드가 이미 sugar-off. 채택→공급자 실패→철회 사슬 미확인 | `streams/review-counts/countertype4.json`을 먼저 읽고 [최초 CI 도입 커밋75c0dc3](https://github.com/OSGeo/gdal/commit/75c0dc375faabbe7d27d9d9a0eb4a98bd41cf44f) 이전의 실행·실패 기록 존재 여부 확인. 없으면 미확인 유지 |

결말 비노출 위반은 복구 가능한 원문 접근 공백과 다르다. 뒤늦게 원전을 확보해도 AC03의 역사적 관측은 바뀌지 않는다. 사전 범위가 소진된 뒤 양성 수를 맞추려고 사건이나 표집 기간을 늘리지 않았다. B04 접근 실패와 B01/B03 원전 미확보는 실패 URL·대체 경로를 원장에 남겼다.

## 묶음별 원격 커밋

| 묶음 | 원격 SHA | 내용 |
| --- | --- | --- |
| ① 사전 고정 | `b6ba3ccb7631ef1d219300ce28844e444f99baaa` | manifest·표집/판정 규칙·이전 사건 중복 제외 |
| ② 최초판 동결 | `7a33c17be2d25b2c1936038205187e8108bf4482` | A/B 초기 원장·후보·최초판; 별도 후속 조사 전 동결 |
| ③a 추적 | `1ba493dc0481a8105d0cdb3e7281d79831c09061` | CSS 후속과 제공 원문·반례 |
| ③b 통합 관측 | `d3643808010c5d465aea05e0efea46f625e8b9c9` | 전체 사슬·구현·반례·통합 원장 |
| ④ 결과·수용 | `c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b` | 두 필수 표·카드·자체 점검·130개 검사·CSV 확인·정정 기록 |
| 마지막 별도 HANDOFF | 본 파일을 추가한 커밋, 부모 `c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b` | 아래 고정 SHA 재독·세션 검사 후 작성; 다른 파일 변경 없음 |

## 결과·수용 파일을 원격 고정 SHA에서 다시 연 영수증

GitHub에서 두 파일을 `c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b`로 다시 읽고 로컬의 커밋 대상 본문과 정확히 일치함을 확인했다. 이 단계는 결과 커밋 이후, 세션 검사 이전에 실행했다.

| 파일 | Git blob SHA | 재독 결과 |
| --- | --- | --- |
| `RESULT.md` | `20df16b263afa7a78d49a82c4c545b5759de9071` | 본문 일치. SHA-256 `095dfb750a7867ea0f0aa3dc596af27ea9ce560836ad6f57ac6fb9b864afe0e3` |
| `evidence/acceptance-evidence.json` | `977bd38ee19acb4d6703642d7f4f124f7912797a` | 본문 일치. 미충족 AC03/AC05/AC06/AC18/AC19, 원장168·고유49 재확인 |

고정 수용 JSON의 `postcommit_checks`는 작성 순서상 실행 전 상태를 유지한다. 실제 실행 후 영수증은 이 마지막 HANDOFF에만 기록한다. 검사 후 과거 결과 커밋을 재작성하지 않았다.

## 지정 세션 검사 — 실제 실행됨

실행 위치: 저장소 루트. 실행 명령은 요청과 동일하다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-037/manifest.json --fetch
```

종료 코드 **0**, `status=passed`, `freshness=remote_checked`. 검사 시점은 **2026-11-22T19:33:43.533771+00:00** (한국 시간 2026-11-23 04:33:43)이다. 검사 직전 HEAD는 결과 SHA와 일치했고 `git status --porcelain=v1 --untracked-files=all`의 출력은 비어 있었다. 검사 출력의 변경 경로 68개는 모두 소유 경로 아래였다. 다음은 stdout에서 경로 목록만 개수로 축약한 기록이다.

```json
{
  "status": "passed",
  "task_id": "af-res-037",
  "freshness": "remote_checked",
  "checked_at": "2026-11-22T19:33:43.533771+00:00",
  "checked_out_commit": "c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b",
  "task_base_commit": "de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62",
  "integration_commit": "96ca12b9599a0459ecac42d1923b13b0c2b19924",
  "scope_base_commit": "de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_path_count": 68,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

이 검사는 Git 계약·소유 경로·의존 신선도 검사다. 원문 인과 해석이나 역사적 소프트웨어 실행 성공을 대신하지 않는다. 결과 파일의 130개 구조 검사와 문헌 수용 조건19/24도 별도로 보고했다.

## 실행하지 못한 역사 시험: 고정 입력·명령·막힌 전제

현재 관측 환경은 GDAL3.10.3·pdfTeX1.40.26이며 Python2와 LilyPond는 PATH에서 찾지 못했고 JP2KAK 드라이버는 인식되지 않았다. 아래 과거 버전들을 이 환경에서 실행했다고 주장하지 않는다. `<...>`는 확보해야 할 정확 버전의 경로 자리표시자다. 재개 시 checkout·cache·출력도 소유 경로의 `reproduction/` 아래에 둔다.

### A-G02 · RFC72 pytest

입력은 [59d0840b1980d1a1a84701b6dae5fc5c78e999f5](https://github.com/OSGeo/gdal/commit/59d0840b1980d1a1a84701b6dae5fc5c78e999f5)의 `autotest/osr/osr_ct.py` 전체 모듈이다. 앞 시험이 상태를 설정하므로 필요한 초기화를 건너뛰어 단일 함수만 실행하지 않는다. 당시 Python bindings·PROJ4·pytest 조합과 정확한 의존 버전은 미확인이다.

```sh
cd "<GDAL_59d0840b1980d1a1a84701b6dae5fc5c78e999f5_CHECKOUT>/autotest"
python -m pytest -vv -p no:sugar --color=no -o console_output_style=classic osr/osr_ct.py
```

기존 좌표 입력 `(-117.5,32,0)`을 사용한 고정 시험과 대조한다. ASAN 별도 검증의 첫 자료는 같은 SHA의 `gdal/ci/travis/gcc52_stdcpp14_sanitize/script.sh`이며 GCC5.2·ASAN2/UBSAN0·suppression·파일별 프로세스가 전제다. 과거 CI 전체 스크립트의 설치·삭제 단계를 실행하지 않았다. RFC72의 sugar-off는 당시 명시된 조건이지 이번 환경에서 관측한 새 포기 사건이 아니다.

### A-G03 · RFC73 축 매핑과 WKT 출력 기본값

입력 SHA는 [ab9e80368ef662712c963191fd86fde2c5b75600](https://github.com/OSGeo/gdal/commit/ab9e80368ef662712c963191fd86fde2c5b75600)이다. 대응 PROJ6 개발판·database·bindings가 필요하며 정확한 PROJ 당시 SHA는 미확인이다. 첫 자료는 연결 PR1185의 당시 CI 설정이다.

```sh
cd "<GDAL_ab9e80368ef662712c963191fd86fde2c5b75600_CHECKOUT>/autotest"
python -m pytest osr/osr_ct.py::test_osr_ct_2 osr/osr_ct.py::test_osr_ct_4 osr/osr_ct.py::test_osr_ct_6 -q
gdalsrsinfo EPSG:4326
gdalsrsinfo -o wkt1 EPSG:4326
python -c 'from osgeo import osr; s=osr.SpatialReference(); s.ImportFromEPSG(4326); print(s.ExportToWkt())'
```

정확한 역사 환경의 실행 파일이 PATH에 있어야 한다. 고정 시험의 기본 축 `(32,-117.5)`와 명시적 GIS 축 `(-117.5,32)`가 같은 UTM 위치로 연결되는지 확인한다. CLI WKT2:2018 기본과 API WKT1 기본은 별도 확인한다. 실행 성공만으로 최초안 이전의 저자 노출·선택 변경이 증명되지는 않는다.

### A-G04 · RFC74 문서 빌드

입력은 [3a9f10aaca02876a01e090ef8437e513a4877fdf의 conf.py](https://github.com/OSGeo/gdal/blob/3a9f10aaca02876a01e090ef8437e513a4877fdf/gdal/doc/source/conf.py)와 같은 버전의 문서다. 당시 Sphinx·Breathe·LaTeX·theme/extensions·Doxygen XML(`gdal/doc/build/xml`)이 필요하다.

```sh
AF037_OUTPUT="<REPO>/docs/workstreams/research/AF-RES-037/reproduction"
cd "<GDAL_3a9f10aaca02876a01e090ef8437e513a4877fdf_CHECKOUT>/gdal/doc"
sphinx-build -b html source "$AF037_OUTPUT/rfc74-html"
```

HTML 빌드만으로 당시 DNS·게시 권한·redirect 전체를 검증하지 않는다. 이번에는 고정 conf와 완료 공지만 직접 확인했다.

### B02 · GDAL1.6 GMLJP2 회귀 시험

입력 버전은 GDAL1.6.0 고정 SHA `5e41f124fd07442bd0bbba87134a3c1901922fc3`이다. 먼저 [JP2KAK 문서 L23–30](https://github.com/OSGeo/gdal/blob/5e41f124fd07442bd0bbba87134a3c1901922fc3/gdal/frmts/jp2kak/frmt_jp2kak.html)의 Kakadu SDK·빌드 전제를 확인한다. Python2·해당 GDAL bindings·JP2KAK가 필요하며 현재 확보되지 않았다. 입력 fixture는 `autotest/gdrivers/data/ll.jp2`와 `autotest/gdrivers/data/gmljp2_dtedsm_epsg_4326_axes.jp2`; 대상은 `jp2kak_7`이다.

```sh
cd "<GDAL_1_6_0_CHECKOUT>/autotest/gdrivers"
python2 jp2kak.py
GDAL_IGNORE_AXIS_ORIENTATION=NO "<GDAL_1_6_0_BIN>/gdalinfo" "<GDAL_1_6_0_CHECKOUT>/autotest/gdrivers/data/gmljp2_dtedsm_epsg_4326_axes.jp2"
```

`jp2kak_7`의 기대 geotransform은 `(42.999583333333369,0.008271349862259,0,34.000416666666631,0,-0.008271349862259)`이다. 드라이버 부재로 skip되면 통과로 기록하지 않는다. 현재의 실행 전제는 2008년 공급자 제약으로 채택을 포기했다는 증거가 아니다.

### B01 · pdfTeX 폭 확장 모드

첫 입력 원문은 [2001 운용 예제](https://tug.org/TUGboat/tb22-3/tb72thanh.pdf) pp147–148이다. 해당 판의 plain-TeX 예제와 `cmr10+20,+15,+10,+5,-5,-10` expansion TFM 변형, pdfTeX0.14h를 먼저 확보한다. 원전의 네 번째 expansion-factor 인자는 현대판 문법과 달라 현재1.40.26로 역사 실행을 대신할 수 없다.

```sh
cd "<AF037_REPRODUCTION_WITH_VERBATIM_2001_INPUT>"
"<PDFTEX_0_14H_BIN>/pdftex" expansion-demo.tex
```

`expansion-demo.tex`는 pp147–148의 해당 버전 입력을 그대로 전사한 파일이어야 한다. `pdfadjustspacing` 0/1/2와 `pdfprotrudechars` 0/1/2를 원문 조건대로 비교한다. 정확한 역사 배포본·font 변형·완전한 시험 입력은 아직 준비하지 않았으므로 명령은 실행하지 않았다. 이 비교는 기능 작동을 확인하며 hz 원전·저자 최초 노출 공백을 해결하지 않는다.

### B03 · 현재 관련 spacing 시험과 1998 글꼴 사건의 분리

현대 관련 시험 입력은 `3596756be0fac1f81066a99d2054329212172b2d`의 `input/regression/spacing-stem-direction.ly`, `spacing-uniform-stretching.ly`다. LilyPond2.26 실행 파일이 필요하다.

```sh
AF037_OUTPUT="<REPO>/docs/workstreams/research/AF-RES-037/reproduction"
"<LILYPOND_2_26_BIN>/lilypond" -o "$AF037_OUTPUT/optical" "<LILYPOND_3596756be0fac1f81066a99d2054329212172b2d_CHECKOUT>/input/regression/spacing-stem-direction.ly"
"<LILYPOND_2_26_BIN>/lilypond" -o "$AF037_OUTPUT/uniform" "<LILYPOND_3596756be0fac1f81066a99d2054329212172b2d_CHECKOUT>/input/regression/spacing-uniform-stretching.ly"
```

이 명령은 현대 spacing 관련 기능만 확인한다. 1998 Feta 글꼴 교체의 전후 증명에는 별도의0.1 글꼴·정확 악보 판·같은 음표 입력이 필요하다. 첫 재개 자료는 [1.0.1 tar](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz)의 `ANNOUNCEMENT`, `Documentation/tex/fonts.doc`, `mf/feta-toevallig.mf`다. tar SHA-256은 `fd833684a7147d821c17fa262ec04422f0aa65d1468e59814daa43fdcb2244aa`이다.

### CSS와 B04의 남은 실행 범위

CSS는 고정 명세 변경·WPT·Servo parser 시험을 정적으로 확인했다. 역사 브라우저·runner 조합의 실행은 미확인이다. C02의 첫 실행 입력은 [WPT8808af59f7ef5e6ca27e7fd0b0a50613c8156a72의 compat/webkit-pseudo-element.html](https://github.com/web-platform-tests/wpt/blob/8808af59f7ef5e6ca27e7fd0b0a50613c8156a72/compat/webkit-pseudo-element.html)이며 그 SHA의 runner 문서·대응 브라우저를 먼저 복원해야 한다. 검증되지 않은 현대 runner 명령을 역사 명령으로 적지 않는다. C03은 브라우저 구현 자체가 미확인이다. B04는 구체적으로 변경된 선택·대응 구현을 먼저 식별해야 하므로 전체 METAFONT 실행을 인과 검증 명령으로 제시하지 않는다.

## 같은 우선순위의 약점 3건과 다음 조사

아래 세 항목은 모두 같은 우선순위다. RESULT의 마지막 세 행과 동일하며, 첫 자료를 읽은 뒤 해당 접점만 갱신한다.

| 중요한 불일치·약점 | 영향받는 결론 | 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 제공 원전·초기 기준선의 공백: B01 hz/URW, B03 실제 악보 판·0.1 글꼴, B04 원 발행본 | B의 C2/R을 완결 인과 사슬로 올릴 수 없고 B04 원문 열람 조건은 미충족 | [Thành §4·참고문헌40–43](https://www.tug.org/tugboat/tb21-4/tb69thanh.pdf); [LilyPond1.0.1 fonts.doc11–23](https://lilypond.org/download/sources/v1.0/lilypond-1.0.1.tar.gz); [AMS 원문 접근 실패](https://www.ams.org/journals/bull/1979-01-02/S0273-0979-1979-14598-1/S0273-0979-1979-14598-1.pdf) | 먼저 B03의 1.0.1 fonts.doc와 mf/feta-toevallig.mf에서 명명된 Bärenreiter Schubert Auf dem Strom·Hofmeister Müller Etüden für Horn의 정확한 판을 식별하고 해당 판을 직접 읽는다. B01은 Zapf1993·URW1993, B04는 Stanford STAN-CS-78-648 원본 정상 접근을 별도 재개. | 정확한 선행 원전과 같은 저자의 변경 전 선택·읽은 뒤 변경 발언·동일 목적 구현이 연결될 때만 strict C3 증가 |
| B02의 기준선과 분야 경계: 최초 RFC안과 기존 실행 코드는 서로 다른 전후 비교 | 고정 기준 B0/4와 표준 포함·기존 코드 기준 감도1/4의 해석 | [RFC20 v1](https://trac.osgeo.org/gdal/wiki/rfc20_srs_axes?version=1); [#2131 c1–2](https://trac.osgeo.org/gdal/ticket/2131#comment:1); [GML §12.4.3.1](https://docs.ogc.org/bp/03-105r1/03-105r1.zip) | 첫 자료는 RFC20 v1과 #2131의 2008-01-04~22 기록. 같은 작성자가 출처 노출 전에 다른 선택을 유지한 설계 기록을 찾고, EPSG 지리 실무와 소프트웨어 인터페이스 규범의 권한 관계를 분리한다. | 동일 원안 기준의 새 인과 접점이 생기거나, 새 연구에서 코드 기준·표준 포함을 사전 선언했을 때만 다른 분모로 결과를 제시. 실행 성공만으로 기준선 문제는 해소되지 않음 |
| 초기 접두부 표집·우발 노출·정적 검증의 한계 | 일반 채택률·검색 성능·역사적 실행 성공으로의 확대 | [CSS #2157 최초 알림](https://lists.w3.org/Archives/Public/public-css-archive/2018Jan/0020.html); [RFC74 공식화 공지](https://lists.osgeo.org/pipermail/gdal-dev/2019-May/050244.html); [GDAL1.6 JP2KAK 전제 L23–30](https://github.com/OSGeo/gdal/blob/5e41f124fd07442bd0bbba87134a3c1901922fc3/gdal/frmts/jp2kak/frmt_jp2kak.html) | 표집은 교체하지 않고 A-C03 제외 감도0/7을 유지. 실행을 재개하려면 첫 자료인 GDAL1.6 JP2KAK 문서와 고정 jp2kak_7 fixture를 읽어 Python2·Kakadu 환경부터 확보한다. 다른 사건은 HANDOFF의 버전별 명령 사용. | 독립적으로 고정한 새 표집·노출 기록이 생기면 외적 타당성 재평가; 해당 역사 버전 시험이 실행돼야 실행 여부만 갱신. 당시 검색색인·저자 첫 독서가 확인되기 전 검색 성공률은 계산하지 않음 |

