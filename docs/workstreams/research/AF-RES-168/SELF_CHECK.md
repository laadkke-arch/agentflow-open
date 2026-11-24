# AF-RES-168 자기검산 — PARTIAL (동일 작업자)

검산 대상 329d7773585b780a45675848d54abbe806609740. 별개 검토자 없음. GitHub 원격에서 직접 파일 재열람하여 JSONL 파싱, quoted CSV 파싱 및 ID/열수/참조 대조 수행(브라우저 실행/빌드/CI 아님).

```json
{
  "all": 78,
  "unique": 78,
  "counted": 35,
  "countedWorks": 35,
  "invalidUrls": 0,
  "missingSourceReferences": [],
  "checks": {
    "frame.csv": {
      "rows": 16,
      "columns": 11,
      "malformed": 0,
      "duplicate": 0
    },
    "claims.csv": {
      "rows": 16,
      "columns": 23,
      "malformed": 0,
      "duplicate": 0
    },
    "provenance.csv": {
      "rows": 28,
      "columns": 10,
      "malformed": 0,
      "duplicate": 0
    },
    "observations.csv": {
      "rows": 14,
      "columns": 13,
      "malformed": 0,
      "duplicate": 0
    },
    "advice.csv": {
      "rows": 8,
      "columns": 15,
      "malformed": 0,
      "duplicate": 0
    }
  },
  "frameRankConfirmed": 0,
  "claims2024Exact": 0,
  "claims2025Exact": 4
}
```

- base d32c697b4345442a4c91f62b8fb0bbed19e58034 대비 위 검산판: 9 commits ahead, 0 behind, 변경 8 파일, owned_path 밖 0. dot-control.json 변경하지 않음.
- frame F00에 X01-X04 범위 참조(개별 ID 네 건 존재), 제외 F09는 사전 정규식이며 존재 판독 아님. 후보에 전체 모집 순서·반환 범위 미확인. 정상 0 반환과 다름.
- BCD 데이터는 8×2 파일을 읽어 16×2 claim-time에 parent/context 정보를 보존. 2024 값 0/16, 2025 4/16: 2025 상세화로 fallback major를 바꾸지 않음. claims.csv의 16행은 실제 자연층 모집 확정이 아니라 예정 자리. 2024/2025 자료판 두 번을 32개 독립 주장으로 계산하지 않는다. 
- 원장 78행 35 counted work_id(중복 counted=0); 표시·원자료 공급 및 독립 관측 개수는 별개. PR 11; 규약/고정자료 8(2 데이터+6 문서); 엔진이력/보고 11(단순 버전 날짜 3 포함); 통계 2; 기상 3. 엄격한 메타데이터 3 및 편집 release notes 1 제외 31. 실제 별개의 브라우저 실행 관측 6은 충족 못함. 역사적 동일 술어의 사이트 호스트 수는 미확인; 표시 사이트/자료 호스트 구분. 실제 CSS 동일 값·버전 관측 확정 0/16, 실제 개수 unknown. 
- 표1 16행, 표2 14행, 표3 8행; 표 아래 단위/분모 있음. RESULT 끝 네 열 세 행. 결과 생성시 CSV 구조/원장 링크로 연결(직접 인용은 데이터 식별자/값 위주). 
- T01/T02 7068/170683*100=4.141010→4.1%. T03/T04 9.4°C→48.92°F, -5.6°C→21.92°F, 13kt→14.96014mph, 22kt→25.31716mph. 11:51 EST=16:51 UTC. 2개 도메인 각각 1 underlying lineage. KJFK 원보고와 history 값 일치하나 ingestion pipeline 미확인. FRED 시리즈 별도 메타데이터 1저작, 숫자는 BLS 의존. 동적 URL은 시점 지문 기록(재조회 시 달라질 수 있음).

| 질문 | 주장/미확인 → 직접 위치 | 원장 행·분모 | 반증/최소 증거 |
|---|---|---|---|
| Q1 | [align-content](https://github.com/mdn/browser-compat-data/blob/a630801ac9352a2a84c926e841b22d2c7476f824/css/properties/align-content.json) parent vs flex/grid/block; [CIU flexbox](https://github.com/Fyrd/caniuse/blob/e3d9f5f611976ae05c15b0a2e1f450f5e4e53ba6/features-json/flexbox.json) stats, #3; [contrib](https://github.com/Fyrd/caniuse/blob/main/CONTRIBUTING.md) stats 정의. 역사적 화면과 exact-value 일치 미확인 | B1A/B, C1A/B, R03, N1C/F; 16 계획 중 정식 순위 0 확정, 2024 정확값 0 | 고정된 실제 당시 표+값 조건, 당시 default/flag·제품 확인 |
| Q2 | [BCD README](https://github.com/mdn/browser-compat-data/blob/a630801ac9352a2a84c926e841b22d2c7476f824/README.md) 소비자; [CIU README](https://github.com/Fyrd/caniuse) BCD data; [P1](https://github.com/mdn/browser-compat-data/pull/26792) body/diff; exact import 미확인 | L01/L02/L07/L11, R01/R02/R03, P1, B8B; 28 edge 전체 | 당시 importer artifact/구체 row history/원데이터 커밋이 다른 원천을 가리킴 |
| Q3 | [collector](https://github.com/openwebdocs/mdn-bcd-collector) README 생성 검출, [P2](https://github.com/mdn/browser-compat-data/pull/28265) gaps/crashes and inferred values; [P5](https://github.com/mdn/browser-compat-data/pull/22702) reported tests; [bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1684236) comments 35–39 | R05 P1/P2/P5 E08 X05/X06; O01–O08,O14; exact raw 0/16 | browser patch/OS/value/input/pass or computed actual, timestamp and raw report |
| Q4 | [Mozilla Hacks](https://hacks.mozilla.org/2010/11/firefox-4-font-feature-support/) old syntax; two explicit notes B7A and C2A. 일반 공급과 독립 관측 구별 | L09/L10, O09, A04; 주석 공통 출전 1, 전체 cell lineage unknown | 두 셀이 별개 자료에서 같은 지원버전을 측정한 독립 실행기록 |
| Q5 | [P1](https://github.com/mdn/browser-compat-data/pull/26792) 33/32 추가; [P2](https://github.com/mdn/browser-compat-data/pull/28265) 소급 추정; [B3A](https://github.com/mdn/browser-compat-data/blob/a630801ac9352a2a84c926e841b22d2c7476f824/css/properties/align-self.json) 36 vs note52; [E11](https://bugzilla.mozilla.org/show_bug.cgi?id=1536148) option 예외 | B6A/B B8A/B, O07/O08/O10/O11; 정확 하위셀 4/16 증가, 독립 뒤집힘/전파 지연 0 확정 | same exact target claim original runs + independent contrary run + timestamped change commits |
| Q6 | [BLS](https://www.bls.gov/news.release/empsit.t01.htm) A-1 October, [FRED](https://fred.stlouisfed.org/series/UNRATE) source/note; [METAR](https://tgftp.nws.noaa.gov/data/observations/metar/stations/KJFK.TXT) 241651Z, [history](https://forecast.weather.gov/data/obhistory/KJFK.html) 11:51 | T01–T06 L26/27 O12/13, 2 분야 각 1 계보; 동시 독립 측정 없음 | 별도 조사 표본/독립 장비 same instant/predicate, 또는 서로 다른 ingest provenance |
| Q7 | A/B/C는 서로 대체 불가: [P1](https://github.com/mdn/browser-compat-data/pull/26792) 데이터 추가에 강하고 render는 미상; [CIU current](https://caniuse.com/mdn-css_properties_font-kerning_normal) 표시만 보강 | advice A01–08; CSS 6 질문 중 실제 match raw 0, 통계/기상 2 일치 | 동등 조건의 2 독립 run 및 그 결과가 추천 문장을 바꾸는 사례 |

경쟁 설명 1: native CIU가 BCD와 독립 관측을 했을 수 있다. R03/R04는 자체 시험과 외부 정보 양쪽을 허용하므로 모든 CIU를 BCD 복사로 묶지 않음. 해당 행 원천 미확인으로 B를 낮춤. 경쟁 설명 2: B3/B7의 값 차이는 실제 결함이 아니라 구문·prefix·abspos scope 차이일 수 있다. 따라서 독립 반박으로 세지 않음. 경쟁 설명 3: 여러 자료가 같은 옛 판을 지지해도 자체 실측이 아니라 소급 추정일 수 있다. P2의 crash/부모판 추정이 직접 근거, 기술 결론의 강도를 낮춤. 기술 분야 엄격한 동등 다수 합의 및 독립 반례가 미확보; 타 분야 일치로 대체하지 않음. 전체 directory·CIU 마지막 커밋·당시 렌더·실제 원실행이 첫 결측. 최종 상태 PARTIAL.
