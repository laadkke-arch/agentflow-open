# AF-RES-238 인계 · PARTIAL

## 1. 식별과 상태

- AF-RES-238, 시도 1. Codex Cloud 실행 및 자체 검산. 독립 판독 미실시.
- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-238`. 소유 경로 `docs/workstreams/research/AF-RES-238/`.
- 시작 `610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6`. 계획판 `914dbfa789ebec97063ed97130ea2a71c2e9f503`. 의존 AF-RES-224 `c9897ac1ac8a9445e261fd350385a727f9a5d4b2`, 중앙 DONE 및 인계 자체 PARTIAL. [AF-RES-224 인계](https://github.com/laadkke-arch/agentflow-open/blob/c9897ac1ac8a9445e261fd350385a727f9a5d4b2/docs/workstreams/research/AF-RES-224/HANDOFF.md)
- **고정 결과판 `1f1221c9b9dd9ad65938b0a3ea007ebc24e03841`**. 이 인계의 부모이며 GitHub에서 새로 복제해 확인한 SHA다. [결과판 경로](https://github.com/laadkke-arch/agentflow-open/tree/1f1221c9b9dd9ad65938b0a3ea007ebc24e03841/docs/workstreams/research/AF-RES-238)
- 목표 카운티 원행 0/4, 주 원행 0/2, 원셀 0/48, 결합률·MOE 각각 0/2, 실제 명제 0/10, 실제 가림 카드·키 0/30. 목표 S2301·DP03 0/8, 공식 MLB 개인 박스 0/2. **AF-RES-242로 넘길 실제 판독 패킷은 보류**한다.

## 2. 결과와 막힌 위치

2023 ACS5 카운티 VRE 디렉터리에서 **B23025 지원을 확인**했다. ZIP 본문과 80개 재현값은 받지 못했다. Census worked example의 부호 설명과 구간 순서 불일치를 원 정수로 검산했다. 표준 분모와 산술, 주·카운티 포함관계, 0분모와 주석 상태 처리는 독립적으로 재생할 수 있도록 구현했다. 102개 원장 항목 중 산입한 직접 저작 29개, 서로 다른 비교 사건 6개, 목표 카운티 독립 수치 확인 0개다. [RESULT](RESULT.md) · [출처 원장](sources.jsonl) · [반례와 정정](COUNTEREXAMPLES.md)

원인과 범위는 다음과 같다.

- `www2.census.gov`, `api.census.gov`, `www.bls.gov`, `statsapi.mlb.com` 등의 실제 GET에서 환경 프록시가 연결을 거절했다. 37건 모두 CONNECT 403과 curl exit 56이다. 현재 실효 정책은 제한 모드이며 대상 호스트가 허용 목록에 없다. 승인된 범위에서 해당 정책을 유지했다. [원 요청·UTC·응답 영수증](receipts/http-attempts.jsonl) · [환경 정책 관측](receipts/network-policy.json)
- 직접 웹 리더는 2023 DAT에서 크기 제한, B23025 VRE ZIP에서 Forbidden, data.census.gov 대상 표에서 본문 미반환, BLS XLSX에서 MIME 미지원이었다. Census의 데이터 API는 기관 정책상 키도 필요하며, 이번 요청은 키 확인에 이르기 전에 차단됐다. [Census API 안내](https://www.census.gov/library/video/2026/adrm/requesting-a-census-data-api-key.html)
- 717838 공식 플레이와 718034 공식 요약 및 2차 박스는 열었다. 두 경기의 공식 H/AB 합계 재수신이 필요하다. 색인 원행 후보의 계산은 `.222/.225/.214`이며 ACS 수치 검증과 별개다. [경기 계산 경계](COUNTEREXAMPLES.md#경기-합계와-복제)

## 3. 대표 파일과 커밋

| 단계 | 커밋 | 남긴 것 |
| --- | --- | --- |
| ① | `ac703af532af1e7d9296b2e57932b72d163561b8` | 사전 [SCOPE](SCOPE.md), [session.json](session.json), 시작 기록 |
| ② | `73d1218446f2089da115788a63cdb97ca2fe487f` | [inputs.json](inputs.json), 출처·HTTP 원장 |
| ③ | `4997ac1b59bcb620e31106503388e13dbfd23174` | 두 표, [rows](rows.csv), [ratios](ratios.csv), [run.py](run.py), 패킷 보류 상태 |
| ④ | `eef8c1bb03d582a57fb8830a3cb0be62459b01a6` | 반례, VRE 수신 시도, 재생 결함 정정, [verify.py](verify.py) |
| ⑤ | `1f1221c9b9dd9ad65938b0a3ea007ebc24e03841` | [RESULT](RESULT.md), [SELF_CHECK](SELF_CHECK.md) 및 각 Q의 근거·미달·마지막 약점 3건 |
| ⑥ | 이 인계 | 이 파일을 단독으로 추가 |

## 4. 고정 결과판의 실행 증거

2026-11-24 23:27 UTC, GitHub에서 처음 복제한 결과 SHA에서 확인했다. Linux 6.18.57 x86_64, glibc 2.41, Python 3.12.14, Git 2.52.0이다. `git diff --check` 및 범위·인용 ID·파일 읽기 검사를 통과했다. 변경 26개 전부 소유 경로, Q1–Q7과 마지막 약점 3행, 102 출처 ID, 37개 헤더 지문, 48개 행 상태, 10개 예정 명제, 세 헤더 전용 카드 지문과 빈 키를 다시 확인했다.

| 명령 | 결과 | 실제 범위 |
| --- | --- | --- |
| `python -I docs/workstreams/research/AF-RES-238/verify.py` | exit 0, stderr 0바이트 | 실제 실패 영수증의 8개 산출물 바이트 일치. 합성 48셀·6 원행·2 비율·30 카드 두 번 재생. 같은 seed의 카드 지문과 판독 키 일치. 변조 파일은 거부. |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-238/session.json --fetch` | exit 0, `passed`, `remote_checked` | 최신 검증 기준 `7369707441e2eb70e84004ca6cb3bfeefc8b4061`. 시작판과의 변경은 진행표뿐이다. 의존 SHA와 공통 계약 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc` 일치. `outside_paths=[]`, `errors=[]`. |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit 0, `passed` | doctor, acceptance(공통 55, repo-intake 7, reference-audit 9 및 export·Git bundle), research-case, original-smoke 통과. 자동 `check-all`은 `no_active_sessions`로 개별 manifest 미발견. 개별 계약은 바로 위 명령으로 검사했다. 시작·종료 checkout 모두 동일 SHA·clean. |

정상 진입점의 실제 명령·입력 지문·출력은 [수신 실행](receipts/run-fetch-vre.json)과 [실패 영수증 재생](receipts/run-archived-attempts.json)에 있다. 둘 다 실행기 exit 2다. 고정판의 `inputs.json` SHA256 `476fc9c5dc4a6075a8bcca47840501107d6c751efbbe335bb4c9aa13689b6049`, `run.py` `11933cb8e7cafe96695aaba746ee6c7011760c1e49c3239b9f04cdc99df53669`, `http-attempts.jsonl` `b4d05d0ffdbb514008357d397dc97e3faa106f29e4238456f82f51408eaef73b`다. [동일 입력에서 실행한 자체 검산 기록](receipts/verify-local.json)

고정판 자체 검산의 핵심 stdout은 다음과 같다. 공통 검사와 이 검산은 기관 수신 성공이나 별도 판독자의 판단을 측정하지 않는다.

```text
county_cells=0/48 county_dat_rows=0/4 state_dat_rows=0/2 packet_rows=0/30
archived failure replay: 8 byte-identical deliverables
county_cells=48/48 county_dat_rows=4/4 state_dat_rows=2/2 packet_rows=30/30
synthetic: all 48 slots, 6 rows, 2 ratios, SDR and fallback, 30 opaque cards, repeatable seed
tampered DAT: refused, packet withheld
```

## 5. 재개 첫 행동

기관 다운로드가 승인된 실행환경에서 다음 입력을 먼저 수신한다. DAT와 VRE는 `www2.census.gov`가 필요하다. 동판 데이터 API의 허용 호스트는 `api.census.gov`이며 기존 승인된 키를 `CENSUS_API_KEY` 환경변수로만 제공한다. 이 단계의 성공 여부는 아직 미확인이다.

```sh
git fetch origin work/research-af-res-238
git show 1f1221c9b9dd9ad65938b0a3ea007ebc24e03841:docs/workstreams/research/AF-RES-238/inputs.json
af238=docs/workstreams/research/AF-RES-238
af238_tmp=$(mktemp -d)
python -I "$af238/run.py" fetch --download-dir "$af238_tmp/http" --only dat23 api-ca api-tx api-states
python -I "$af238/run.py" replay --download-dir "$af238_tmp/http" --out "$af238_tmp/first"
```

첫 재생에서 여섯 DAT 행과 두 추출 경로, 48셀의 개별 상태, 실제 두 합계비를 읽는다. 이후 아래 입력을 같은 임시 위치에 추가한다. `laus23`은 2023 연평균 XLSX로 수동 열람할 경우만 포함한다. `mlb-717838`과 `mlb-718034`는 `statsapi.mlb.com`이다.

```sh
python -I "$af238/run.py" fetch --download-dir "$af238_tmp/http" --only vre23 s2301-ca s2301-tx dp03-ca dp03-tx dat22 mlb-717838 mlb-718034
python -I "$af238/run.py" replay --download-dir "$af238_tmp/http" --out "$af238_tmp/second"
```

정상 수신의 SHA256을 검토하고 `inputs.json`에 고정한 후, 같은 자료로 재생한다. 성공 패킷이 이미 있으면 `--key "$af238_tmp/second/key.json"`을 주어 seed를 재사용한다. `publisher-http.json`의 기관 헤더·상태와 `replay.json`의 원문 헤더·원행·지문·계산을 함께 검토한다. 두 주 및 네 카운티의 E/M 추출이 일치하고, 네 카운티 EA/MA가 실제 토큰 또는 공식 개별 부재로 확인되어야 한다. API를 열 수 없으면 동일 판의 `ACSDT5Y2023.B23025`와 네 GEO_ID의 공식 각주를 확보해 주석 상태별 증거를 남긴다. `S2301`, `DP03`의 수치는 카운티율과 반올림·단위를 맞춘다. VRE는 003·005의 동판 E가 일치하는지 확인하고 재현값을 적용한다. 감춰진 입력 전체를 볼 수 있는 공개 브랜치 링크 대신, 값과 키가 완성된 뒤 manifest와 해당 층 카드만 별도 판독자에게 전달한다.

완료 판정 전에 새 결과 커밋에서 위 `verify.py`, 개별 `session check --fetch`, 공통 `cloud_check.py`를 다시 실행한다. 현재 `verify.py`의 archived 체크는 이번 실패 스냅샷 8개 파일용이다. 실측 산출물을 덮어쓰는 다음 갱신에서는 실패 스냅샷 대조와 새 고정 입력 재생을 각각 보존하도록 그 검사를 조정한다.

## 6. 색인 반영 제안

AF-RES-238 / PARTIAL / 고정 결과 `1f1221c9b9dd9ad65938b0a3ea007ebc24e03841` / B23025 카운티 VRE 지원 확인·기관 바이트 미수신 / 다음 첫 행동 동판 DAT 및 API 원행 수신 / AF-RES-242 보류. 진행표와 자료 색인 갱신은 통합 담당이 한다.
