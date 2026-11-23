# AF-RES-055#1 인계

**부분 완료.** IANA 정식 데이터 두 연속 판 쌍을 독립 판독했고, 교통 두 쌍은 적격 원 ZIP·공통 효력일 결손으로 보류했다. 두 필수 표에는 16판독 자리와 24보기를 모두 보존했다.

## 고정 결과와 검증

- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-055`, 작업자 codex-cloud. 계획 통합판 `d7e60daf1b5b2c918502c407982566369b7149e3`, 실제 시작판 `573a8f1a7cafa90b87bcbb4267e73fee12385bda`. 의존 인계는 `537712e2f716a0ff9b517b23ac7c4ec2fb37435d`, 읽은 선행 데이터 결과판은 `4e1a76cd0ca25bfe616797b623f9ecb435261fcb`다. [작업 계약](manifest.json) · [범위와 규칙](SCOPE.md)
- **결과 SHA `f3faf7002c287d103f380c23d04a344e6d40ebc1`.** 필수 표 1의 머리는 1행, 자리 16개는 3–18행이다. 표 2의 머리는 20행, 보기 24개는 22–45행이다. [표 1](https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/RESULT.md#L1) · [표 2](https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/RESULT.md#L20) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/f3faf7002c287d103f380c23d04a344e6d40ebc1/docs/workstreams/research/AF-RES-055/evidence/acceptance-evidence.json)
- 고정 결과 두 파일을 GitHub 연결에서 열었다. 같은 SHA의 raw GET 두 개도 HTTP 200이었고 checkout과 바이트가 일치했다. `workbench.session check ... --fetch`는 2026-11-23 01:56:56 UTC에 시작해 exit 0, `remote_checked`, 범위 밖 변경 0이다. 같은 SHA의 별도 checkout에서 `scripts/check.py --require-git`도 exit 0이다. 적용 범위는 Git 계약과 기존 Workbench 검사다. 운영 교통과 외부 소비자의 실행은 미확인이다. [고정 결과 검사 출력](evidence/final-check.json)

| 묶음 | 원격 SHA | 보존 근거 |
| --- | --- | --- |
| ① 선별·키·비용 사전 규칙 | `ce506de0c4797e356ce3391c2c96df1a8d9eb10d` | 시작 계약, 공식 목록의 후보 투영과 우선순위 |
| ② 원본·예측 고정 | `fbde561bb0b33aa4616020e14d732c3d1c4ab248` | 네 데이터 tar 귀속, 시각·멤버·실패 원장, 8개 기대 |
| ③ 계산과 별도 재실행 | `61e1f4981b5597db5affc45153bde826ccfe939c` | 8판독 양쪽 일치, 역순 재실행, 실제·통제 반례, 실행 영수증 |
| ④ 필수 표·비용·자체 검토 | `f3faf7002c287d103f380c23d04a344e6d40ebc1` | RESULT, SELF_CHECK, 24보기·48프로필, 수용 원장 |
| 고정 결과 검증 영수증 | `fca3b8e4841785ae6867f32dbc0bba62651803b1` | 원격 두 파일의 바이트 확인과 검사 UTC·종료 코드·출력 |

## 확인한 내용

- 시간대 8/8판독에서 zdump와 명시 TZif를 연 Python이 일치했고 별도 빈 폴더에서 역순으로 재실행해 8/8을 확인했다. 뉴욕은 두 순간 모두 유지했다. 베이루트 2023a→2023b의 2023-04-20 21:00Z는 +10,800→+7,200초, 04-21 00:00 EEST→04-20 23:00 EET다. 23:00Z는 유지다. 2023c 되돌림, CET Zone→Link의 무변화 값, Choibalsan의 역사 시간대를 따로 검산했다. [판독](runs.jsonl#L9) · [반례](evidence/contrasts.json)
- 교통은 본판독 0/8이다. MBTA 날짜층 목록의 30쌍에서 권장 사용 겹침 0/30을 관측했다. 이 범위는 목록의 라벨 UTC로 정렬했다. MBTA 보관 정책은 날짜를 조정하고 오류판을 교체할 수 있다. 12/26·12/29와 03/10·03/12 ZIP의 요청은 CONNECT 403이며 BART·HSL의 고정 연속 원 ZIP을 찾지 못했다. 같은 수/다른 집합, 일정 동일 재발급 및 달력 누락은 작성 통제에서 관측했다. [후보·효력 원장](editions.csv) · [GET 실패 응답](evidence/acquisition.json)
- 직접 열람 행 60개, 실패 18개, 계보를 묶은 배당 산입 원문 37/22다. 보기 24개를 각각 냉/온에서 실행했다. 시간대의 냉 과거는 V0 0/4, V1 2/4, V2 4/4 일치했고 냉 다음은 전부 보류했다. 기확보 조건에서는 모든 시간대 보기가 두 목적에서 일치했다. 교통 12보기의 기준값은 미확인이다. URL만 보고 다음 유지를 단정한 대조는 시간대 2/4 오판했다. [출처](sources.jsonl) · [보기와 비용](views.csv) · [질문별 자체 검토](SELF_CHECK.md)

## 다음 첫 행동과 실행 입력

첫 행동은 MBTA의 원 목록을 파일로 받고, 기존 투영과 동일 창의 게시 메타데이터를 대조하는 것이다. 실패 원인은 현 네트워크 정책의 CONNECT 403과 보관 권장 구간 비겹침이다. 게시자의 원래 게시시각·효력과 공지 대응을 확인할 수 있는 원 ZIP이 필요하다. 아래 네 ZIP 주소는 실패한 요청의 재현 입력이다. 공통일이 확인되기까지 후보로만 둔다.

```sh
af055_gtfs=$(mktemp -d /tmp/af055-transit.XXXXXX)
date -u +%FT%TZ
curl -fLsS --max-time 60 https://cdn.mbta.com/archive/archived_feeds.txt \
  -D "$af055_gtfs/index.headers" -o "$af055_gtfs/archived_feeds.txt"

for af055_day in 20231226 20231229 20230310 20230312; do
  date -u +%FT%TZ
  if curl -fLsS --max-time 60 "https://cdn.mbtace.com/archive/$af055_day.zip" \
    -D "$af055_gtfs/$af055_day.headers" -o "$af055_gtfs/$af055_day.zip"; then
    sha256sum "$af055_gtfs/$af055_day.zip"
    unzip -p "$af055_gtfs/$af055_day.zip" feed_info.txt
  fi
done
```

- 목록과 원래 발행자 배포 기록에서 첫 30쌍의 인접성·게시일과 공통 유효기간을 확정한다. 공지층에는 2023-03-12 후보 이전의 원 발행자 공지 순서 및 해당 노선·날짜의 ZIP 연결이 필요하다. MBTA 결손이 남으면 BART, HSL 순서의 공식 날짜별 두 원본과 발행 메타데이터를 사용한다. 파일의 봉인 전에 표본 규칙을 바꾸게 되면 관측 범위와 전후 판정을 SCOPE에 기록한다. [MBTA 보관 기준](https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs-archive.md) · [BART 정적 배포](https://www.bart.gov/schedules/developers/gtfs) · [HSL 정적 배포](https://www.hsl.fi/en/hsl/open-data)
- 두 파일과 공통 서비스일이 입증되면 `YYYY-MM-DD`, `ROUTE_ID`, `DIRECTION`을 봉인하고 아래 위치의 두 ZIP을 독립 판독한다. 같은 수와 기여 집합, 키 미확인, 개명 대응을 따로 처리한다. 이어서 교통 8판독·12보기 및 두 표의 조건부 분모를 갱신한다. IANA는 고정 원본과 별도 빌드 그대로 재실행할 수 있다. [재실행](reproduce.md)

```sh
python -B docs/workstreams/research/AF-RES-055/replay.py gtfs /tmp/af055-transit/old.zip YYYY-MM-DD ROUTE_ID DIRECTION
python -B docs/workstreams/research/AF-RES-055/replay.py gtfs /tmp/af055-transit/next.zip YYYY-MM-DD ROUTE_ID DIRECTION
python -B -m workbench.session check docs/workstreams/research/AF-RES-055/manifest.json --fetch
```

**색인 제안** `AF-RES-055 | 과거 답 복원과 다음판 추천 이유의 분리, IANA 실측 2쌍·GTFS 보류 2쌍, V0–V2 냉온 비용 | docs/workstreams/research/AF-RES-055/RESULT.md | AF-RES-051@537712e2`.

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| MBTA 30개 권장 구간 쌍은 겹침이 없고 교통 원 ZIP 두 판의 확보 실패 | 동일 서비스일의 실제 예정 수·집합 변화, 게시일순 표본의 교통 대표성 | [후보 원장](editions.csv) · [MBTA 권장일 정의](https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs-archive.md) · [원 GET](evidence/acquisition.json) | 발행자가 보존한 게시시각·유효기간·공통일이 있는 연속 ZIP 둘과 공지-발행 대응 확보 | 동일 서비스일·키의 적격 두 판을 원본과 해시로 묶어 Python/SQLite가 같은 집합을 주면 해당 슬롯의 보류를 바꾼다 |
| 냉 목록 CONNECT 403과 기확보 바이트 비용의 분리 | 현재 진입 URL의 냉 복원율과 V2의 상대적 접근 비용 | [보기 원장](views.csv) · [획득·도구 준비](evidence/preparation.json) | 공개 IANA 목록·tar를 정상 수신하는 환경에서 같은 세 레코드와 동일 캐시 규칙으로 다시 측정 | V0가 목록과 두 판을 냉 조회해 독립 재계산까지 도달하면 현재의 냉 보류·비용 비교가 달라진다 |
| 두 시각 판독기가 zic와 TZif를 공유하며 외부 소비자의 설치 기록이 없다 | 값 일치의 독립 범위와 예전 설치판·기관의 실제 적용 | [실행 영수증](evidence/receipts.json) · [캐시·변환 대조](evidence/contrasts.json) | Beirut 2023-04-20T21:00Z를 별도 컴파일러와 해당 소비자의 데이터판·파일 해시 영수증에서 대조 | 공통 컴파일에서 발생한 오류나 실제 다른 설치판이 확인되면 해당 소비자의 적용 판정을 변경한다 |
