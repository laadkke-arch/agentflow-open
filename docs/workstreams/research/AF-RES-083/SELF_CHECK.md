# AF-RES-083 자가검산

## 판정 원칙과 최종 상태

**PARTIAL**을 유지한다. 여섯 예약 자리 중 실제 안내 2개, 공석 4개이며 실제 두 안내도 하나의 GeoPandas 저작에 속한다. 정확한 GDAL GEOARROW 호출 노출은 0/2, O02 핵심 모집은 0/3이다. 독립 자료 최소량과 외부 사건 최소량이 충족되었다고 핵심 모집·정오 비교까지 완료된 것으로 처리하지 않는다. 기계 검산의 종료 0은 기록 무결성 통과이며 연구 질문의 완전한 해결을 뜻하지 않는다.

## Q별 주장·원문·반대 근거·최소 확인

| 질문 | 주장과 근거 위치 또는 실행행 | 반대 근거를 찾은 경로와 결과 | 빈자리·최소 후속 확인 |
|---|---|---|---|
| Q1 | G04-1은 공간 왕복, G04-2는 schema 판 선택. `records.jsonl`, G083-S01의 old L272–285. O02 보조 guide는 각기 fit, kernel, model, BlackBody, AP/AUC 목적. | Arrow 일반 표 예제(G083-S09–10)와 GeoPandas CRS84 기대 시험(G083-S28)을 읽음. 파일 읽기·공간 복원·CRS 문자열 동일성은 같지 않음. | 원 guide에 exact fixture 없음. 원 입력을 명시하는 실제 재사용 안내와 소비자 시험을 구별해 확보. |
| Q2 | GeoPandas Parquet는 PyArrow 경로. G083-S02–06. 옛 NumPy AUC는 다른 namespace, O-S15. 실제 설치판 0. | 패키지의 Fiona/GDAL 의존과 호출 경로를 비교; dependency floor·CI 명세가 실제 build라는 가정 기각. 현재 링크 목적지는 별도 기록. | 역사 HTTP 흐름 미확인. build lock/해결 기록 및 실제 호출·판을 확보. |
| Q3 | 079 GN04–07과 O02 source/실행 수준은 `streams/root/dependency-observations.json`. 소비자 exact input join은 RESULT Q3 표와 각 POSTSEAL. | simps/cumtrapz 일부는 source-only; GAM 시험은 centered spline·alpha 차이, Astropy 시험은 100 K/100,000점 대 guide 10,000 K/1,000점. | 새 소비자 기능 실행 0. REPRODUCE.md의 정확 SHA·함수·fixture·기대 출력으로 재개. |
| Q4 | G04 두 원문 범위 모두 실제 편집. G083-P0/P1와 record-fingerprints. O02 실제 diff 7개를 4 사건 계보로 접음. | PR3348의 이유는 판 문구 노후화 방지. Astropy 제거 PR10972는 SciPy1.6 발행 이전. 404만으로 삭제 원인 추정하지 않음. | actual edit≠mandatory correction. 실제 reader의 잘못된 행동·당사자 수정 이유가 함께 있는 레코드 필요. |
| Q5 | 35d7e180에서 old/AB 봉인 후 후속 본문 취득. preseal 4 hash, GIS·OSS acquisition UTC 및 stream audit로 대조. A는 실제 두 행 모두 보류. | A가 하지 않은 일괄 치환을 가정한 오류 계산 거부. G04-2 old 문맥은 미래 지원의 명시적 약속이 아님. AUX-G04-A1에는 A/B가 없어 평가에 넣지 않음. | core 정오 분모 0. 보류 2/2·제안 종류와 오류율을 분리. |
| Q6 | `make_repairs.py`가 만든 RESEARCH-2건의 정·역 diff를 실제 patch로 적용. `rollback-receipt.json`의 각 steps argv/exit/hash에서 정방향2·역방향2 종료0. | publisher PUBLISHER-IDs와 구별. byte 복구로 기능 동등성을 주장하지 않음. 빈자리 patch 0. | 외부소비프로젝트에 실제 수정/되돌림은 수행하지 않음. 원문의 세 판 view 링크와 해시는 그대로 보존. |
| Q7 | 정적 유지 지지 1, 예방적 범위 명시 1. 새 지원판에 옛 WKB 제한을 그대로 적용하지 않음. O02 보조 설명의 서로 다른 목적을 분리. | 최신 native 지원(G083-S20–23), AP와 trapezoidal AUC의 의미 차이(O-S14–16), SciPy1.11 even 변경(UP-PR18209)을 읽음. | core에서 링크가 살아 있지만 반드시 정정해야 함을 확정한 행 0. G04-2의 실제 미래 encoding 재사용 레코드 필요. |
| Q8 | 외부 전거2·출판3 사건, 양끝5/5. 역사 bytes는 PLOS1/5. `streams/external/cases.jsonl`·CROSS_DOMAIN·pdf-comparison. | LC 분할은 복수 수신, 병합은 receiver ID 재사용, Nature HTML은 원래 올바름, PLOS 같은 DOI/date의 PDF 차이, JNCI 중복 공지 철회. | 실제 consumer 중복 적용0. 역사 export/PDF/Box2와 적용 로그 필요. 이 규칙은 소프트웨어 행동 증명이 아님. |

## 모집·자료량·판 확보를 따로 점검

| 항목 | 기준 | 확인 | 처리 |
|---|---|---|---|
| 원 모집 자리 | 6 | 6 ID 보존 | 충족 |
| 실제 지시 모집 | 6 | 2, 독립 core guide1 | **미달/PARTIAL** |
| 검색 후보 저장소 | 순서 고정 6 | G04 3 + O02 3 모두 검색 | 충족; 누락 경로·확장자를 원장에 남김 |
| 독립 원저작·사건 | 최소20 | raw lineage39, 코드·시험·CI 단독 제외35, 보수적25, 강한 통합23 | 최소량 충족; 124행을124저작으로 세지 않음 |
| 서로 다른 하류 저작 | 최소6 | guide11계보, O02 보조 guide6 | 자료량 충족; core 노출 분모와 합치지 않음 |
| 외부 실제 사건 | 두 제도·최소4 | 5사건/2제도 | 충족; 정책4계보는 사건 제외 |
| 옛·첫후속·최신 실제 문단 | 실제 안내2 | 2/2 | 전체 원 분모 기준2/6임을 병기 |
| 실제 문서 변경 | 관측과 필요 구별 | 2/2 literal edit, 필수 동작 정정 확정0 | 두 종류를 분리 |
| 연구 수선 가능 | 실제 안내2 | 정방향2/2·역방향2/2 | 소비자 기능 시험 아님 |
| 정오 기준 있는 평가 분모 | 비어 있으면 미확인 | core0 | A/B 우열·불필요/누락/유효 유지 비율 산출 불가 |
| 운영 오류율 | 실제 운영 레코드 필요 | 운영 레코드0 | 0/0, 산출 불가 |

## 원장 정정·시각·계수의 감사

사전 파일은 그대로 두었다. QGIS 검색 파일수 111은 검색행·manifest의 110으로 정정했고, G083-S10의 “third slot fills”는 실제 G04-3 공석과 충돌하는 설명 잔재로 정정했다. `streams/gis/postseal/corrections.jsonl`에 old/correct/evidence/effect를 함께 남겼다. normalized source에도 해당 postseal 정정을 붙여 원 제한 문구와 새 설명이 함께 보이도록 했다. 행 포함·순서·A/B는 바뀌지 않았다.

원자료 원장의 `opened_utc`는 원 stream의 최초 열기/취득일 수 있다. 별도 `read_utc`, `directly_opened_utc`, `visual_read_utc`가 있으면 `direct_read_utc`와 원 필드로 보존했다. 일부 웹 최초 열람 시각은 다음 clock 확인에 따른 UTC 상한이며 `opened_utc_precision`을 유지했다. 다운로드만 했거나 접근 실패한 자료를 직접 읽은 자료로 계수하지 않았다. 시도 33행은 전부 최소 자료량 제외다.

39 원 계보를 합치는 25/23 민감도는 계수용 group이다. 서로 다른 소프트웨어 사건이 실제로 같은 의미·함수·원인이라는 주장이 아니다. 원 lineage와 source→case 연결은 유지한다. 상세 mapping은 `streams/review/source-count-sensitivity.json`에 있다.

후속 감사가 찾은 Arrow 단수 `example` 경로 README3개는 root가 같은16.0.0 SHA에서 본문을 직접 읽었다. 등록 G04 검색식 일치와 공간 계약은 모두0이었다. `streams/root/supplemental-readme-check.json`에 URL·행·UTC·해시·제외 이유를 남겼고 원 고정frame/AB를 바꾸지 않았다. 직접 읽기 원장 행은121→124, 독립 자료 최소량 추가는0이다. 이 후속 확인을 사전 가림 표본으로 부르지 않는다.

## 실제 검사와 미실시

| 검사 | 명령 또는 근거 | 실제 결과·해석 |
|---|---|---|
| 계약 시작 | `python -B -m workbench.session start af-res-083 --allow docs/workstreams/research/AF-RES-083/ --output docs/workstreams/research/AF-RES-083/manifest.json --dependency work/research-af-res-079=cc527e2c4f827afaaaa63f75c897d863c3adcc80 --fetch` | 실제 수행, 시작 SHA f736bd557fa4c40aecb6833165823196cfa42af2. |
| 봉인 대조 | preseal 4 SHA256 및 remote35d7e180 blobs, stream별 원문 hash receipt | 원 sampling/AB 파일 byte 불변. 감사자가 GIS10+OSS17 옛 원문과 상류12 원문 hash도 확인. |
| 정역 diff | `python -B docs/workstreams/research/AF-RES-083/make_repairs.py` | source HEAD b433b1214e18d3ee8a23fc1253ecd216f0d98f8f에서 실제 수행. forward2, reverse2, vacancies0. |
| 구조·범위·연결 | `python -B docs/workstreams/research/AF-RES-083/audit.py` | `evidence/audit-receipt.json`에 시각·대상 SHA·검사별 결과를 기록. integrity와 completion gate를 별도 출력. |
| 계약 인계 검사 | `python -B -m workbench.session check docs/workstreams/research/AF-RES-083/manifest.json --fetch` | 결과 묶음의 정확 SHA에서 재실행한 종료값·fetch 대상은 HANDOFF에 기록. |
| 원격 게시·재열람 | 연결된 GitHub Git Data로 parent·expected_sha를 고정. 각 원격 tree와 로컬 commit tree 대조. | 단계별 SHA는 PROGRESS 및 HANDOFF. 최종 결과의 원격 재열람 영수증도 HANDOFF. |
| 소비자 기능·역사 환경 | GeoPandas·SciPy·Astropy native 실행 | **미실시**. 고정판 source·시험 선언을 읽었으며 기능 실행 성공으로 보고하지 않음. 실행 명령·입력은 REPRODUCE. |

문서·원장 작업이므로 저장소 전체 제품 테스트를 기능 증거처럼 덧붙이지 않았다. 079의 역사 실행도 반복하지 않았다. 파일 내 local/remote SHA가 다르더라도 Git Data 게시 전후 tree가 같음을 별도로 확인했으며, 자기 SHA를 파일에 소급 삽입하지 않는다.

## 반대 검토의 범위

병렬 조사 후 다른 stream 담당자가 원장을 **비맹검**으로 검토했다. 같은 모델 계열의 보조 검토이며 사람의 독립 재현이나 통계적 독립성은 아니다. `streams/review/audit.md`는 봉인·모집·계수·후속 가림·Q8·연구 diff를 검토하고, O02 조사자는 RESULT의 namespace·입력·날짜·source ID를 원장과 다시 대조해 불일치를 찾지 못했다. 감사 지적은 원장 오기/UTC 의미 정정 또는 결론의 한계로 반영했다. 검토 통과로 비어 있는 기능 관측을 채우지 않았다.

## 최소 재개와 인계 조건

첫 다음 행동은 `REPRODUCE.md`의 정확 소비자 SHA·fixture·환경 요구를 읽고, 현재 분모를 바꾸지 않은 채 실행 또는 새 모집의 단위를 고정하는 것이다. 이 기록에서 다음 세 종류의 빈칸을 보존한다: (1) 동일 상류 대상에 노출된 독립 원 안내, (2) 정확 소비 입력과 설치판의 실제 출력, (3) 필수 정정·이미 반영한 정정의 소비자 적용 상태. 최종 결과 문서의 마지막 세 약점에 각각 대상·입력·관측을 짝지었다.

HANDOFF는 이 점검과 결과 묶음 게시·원격 재열람·`workbench.session check --fetch` 후 마지막 **단독** 커밋으로 쓴다. 중앙 index/state 변경은 배정자 몫이며 이 작업은 지정 owned path 밖을 수정하지 않는다.
