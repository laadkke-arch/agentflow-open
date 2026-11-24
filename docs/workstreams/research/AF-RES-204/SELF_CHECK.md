# AF-RES-204 SELF_CHECK — 자체 검토, 독립 검토 아님

- 결과: PARTIAL. 12자리 기능/정책 분리, 원문 최소치의 자료 유형별 직접 열람 수 충족. 그러나 엄격 최초 두 건씩의 모집을 확정할 수 없어 소비자 표본 조건 미달. 임시 표본은 엄격 표본에 산입하지 않음.
- 원장 49행, 고유 산입 work 34, 계보 9; 미산입 15, 접근 실패 9. 댓글은 사건 work 내부 위치로 연결. 문서 절/미러/검색 미리보기 중복 산입 없음. 운영 4/4, 엔진 10/6, 소비자 9/5(임시 4+보강 5; 엄격 선발 원자료 0/5), 데이터 3/3, Open Library 7/4, 별도 보강 코드 1. 9개 소비자 고유 사건(C01–C09), 그중 호스트 또는 운영 전제 연결된 임시 사례 4, 전체 기간 최초 두 건임이 확인된 사건 0/4. 비산입 X01–X15의 이유는 원장과 frame에 표시. N #2590 등 비산입 직접 열람을 최소치에 더하지 않음.
- 정적 구조 검산(④ 고정 입력 0d8a3825713d3ae0130b14a35f65ebe59dbd0b92, GitHub 파일 원문을 읽어 JS로 줄수/JSON 파싱/키 검사; 지오코딩 실행 없음): {"surfaceRows":12,"caseRows":4,"routeRows":3,"frameRows":34,"sourceRows":49,"included":34,"uniqueWorks":34,"lineages":9,"categoryCounts":{"operator":4,"engine":10,"consumer":9,"data":3,"openlibrary":7,"counterexample":1},"missingRequiredFields":[],"unknownTableSourceIDs":[],"tableCount":3,"duplicateSourceIDs":0,"failedReads":9,"strictChronologyConfirmed":0}. 표 2 임시 행만 4; P1/P2 변경은 ④ REFINEMENTS.md와 frame에 기록. ⑤ 결과 고정 SHA에서 대표 파일 재열람은 HANDOFF 작성 직전 별도 수행.
- Q별 반증 탐색 및 제한:

| Q | 직접 근거 / 열람 위치 | 반례 확인 / 반증 여부 | 결손 |
| --- | --- | --- | --- |
| Q1 | A01 scope https://operations.osmfoundation.org/policies/nominatim/ L2–18; A02 https://photon.komoot.io/ L0–21,74–83; B07/B08 repository | B03/B04/B09 자체 설치 문서로 같은 이름=같은 host 정책 가설 반증 | 자체 운영자별 정책 미확인 |
| Q2 | A01 Requirements/Unacceptable Use/LLMs L2–47; A02 terms; B10 API | C08 https://github.com/komoot/photon/discussions/836 L122–141, C06 https://github.com/komoot/photon/issues/867; 기능=운영 허용 가설 기각, 수치 미기재와 금지를 혼동하지 않음 | Photon 구체 합산/캐시 조건 미확인, 역사판 미확인 |
| Q3 | B02 https://nominatim.org/release-docs/latest/admin/Import/ L154–199; B06 https://nominatim.org/release-docs/latest/customize/SQLite/ L85–125; B09 https://github.com/komoot/photon/blob/master/docs/usage.md; D01–D03 | reverse-only, 변환 전제, D03 https://download1.graphhopper.com/public/ 버전 대조: 원천 데이터=검색 엔진 가설 기각 | 기기/버전/저장 용량별 실제 사용 미확인 |
| Q4 | C01 https://github.com/osm-search/Nominatim/issues/2677; C02 https://github.com/osm-search/Nominatim/issues/2813; C07 https://github.com/komoot/photon/discussions/759; C05 https://github.com/komoot/photon/discussions/805 | C03/C04 호스트 결측, C09 공개 사용 제안에 불과, #759 발견으로 P1/P2 보정; frame 엄격 순서 반증 가능 | X11–X15 실패, 0/4 최초 순서 확인 |
| Q5 | A01/A02; F01 https://github.com/maplibre/maplibre-gl-geocoder/blob/main/lib/index.ts blob c98275f8b96ce250192d2ec2ddace987986a59a0 L805–945 | F01 local-only 분기로 키별 remote 필수 가설 반증; C08/C06 데모 보장 가설 반증; 소량 제출 가능 반례 | 실제 네트워크 trace/실제 요청량 미확인 |
| Q6 | E01 https://openlibrary.org/developers/api?show_page_status=1 L85–131; E02 https://openlibrary.org/developers/dumps L58–110; E03/E04; E05/E06; E07 https://github.com/LibrariesHacked/openlibrary-search L220–232,242–265 | 실제 적재 사례로 덤프=즉시 검색 가설 반증; 단건 조회에는 덤프 생략 가능 | 실제 스냅샷 지연/현재 적재 시간 미확인 |
| Q7 | 표 3/routes.csv: A01, B01, A02, B08/B09/B10, D03/D02, B06, F01 | A01 LLM/generic platform restriction; F01 local-only; B02 reverse-only; E04 단건. 단일 제품 링크 보편 충분성 반증 | 최종 탐색 제품 구조·순위는 결정하지 않음 |

- 날짜/번호 순서 전수 조회를 마치지 못한 상태를 DONE으로 표시하지 않음. 기간 외/역지오코딩/정확도/UI 콜백/공유 부하 실측은 제외. 이행/관찰/규칙/설계 제안은 별도. 실제 응답 API 호출, 배포, 실행 시험, 외부 가격·SLA 검증 없음. 코드를 새로 작성하거나 벤치마크하지 않음. 독립 재검토자 없음.
