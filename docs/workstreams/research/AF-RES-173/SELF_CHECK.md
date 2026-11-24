# AF-RES-173 자기점검 (독립 검토 아님)

상태 PARTIAL. 확인일 UTC 2026-11-24 (세션의 제공 시간, 정확 시각 별도 미측정). 사전 모집과 엄격쌍 조건 미달. source 자체/출력 관측/권고 층을 구분했다.

| 질문 | 연결 근거·행 | 판단·미충족 | 다음 최소 관측 |
|---|---|---|---|
| Q1 | S06,S08,S09,S22,S23,S27,S33; B01–B06,B13 | 문서 읽기/파일/metric/QA 구분. 문서별 원 임베딩·locale 미확인 | original example + first issue text + stored font/style/lang/embedding |
| Q2 | S07,S10–S13,S32,S47–S49,S59–S61; B01,B02,B12–B16 | LO 정확 tag recipe 3개 및 fixed commit recipe, 실제 binary 0; TL 정확 TLPDB 본문 실패 | archive package manifest/file list + font hashes; year db record and tar |
| Q3 | S15,S17–S19,S50–S52,S55–S58; B01,B02,B10,B14–B16 | 후보 저자 고지·이력, 실제 복제 font판/원 font 고지 미확인; 라이선스 때문에 바꿨다고 추정 안 함 | exact font file notices, authors and selected version |
| Q4 | S16,S24,S25,S27,S31; O01–O05 | 보고 1, 다중변경 2, 기대/실측 2; 엄격 0 | before/after same input hashes + exact renderer, fonts + line/page/glyph |
| Q5 | S15,S21,S27–S29,S51,S56; O01,O06,O07,O12,O13 | 반례 조사: Liberation 오류 은폐, 수직지표 이의, 잘못된 이름, hinting 차이, glyph 정책. 실제 same-layout 누락 glyph 및 same-width complex shaping의 엄격 반례 없음 | exact same string/locale/script & glyph trace, independently observed output |
| Q6 | S36–S39; O08–O11,P01–P04 | 네 제작기록 읽음. 원판 직접 페이지 대조/면수/가독성 측정 없음 | exact two editions, original scans, matching page/anchor IDs |
| Q7 | A01–A04; S22,S27,S28,S33,S55–S61 | 4개 용도 링크 및 최소 재현 입력. 복제/같은 쪽/문자는 조건부 또는 보류 | file notice & hash / fixed renderer outputs / glyph trace |

## 분모 및 검산

- frame.csv 66행=LO 검색 보조 38+사전 자리 8+보충 B 16+판제작 P 4. LO query counts 13/9/12/4 (중복 제거 38); 13 본문 판독, 25 미열람. C 접두 원순번은 검색 정렬의 row key이고 sources의 C01–C04는 보조 사례 label이므로 같은 번호의 관계를 가정하지 않는다. 연결은 실제 URL 및 source ID로 한다. TL 연도순 원 frame 미복원. 사전 8자리 판정 0 포함/0 제외확정/8 미확인; 보충 모집으로 대체하지 않았다.
- sources.jsonl 61행, 접근 open 45/failed 16, 산입 35 unique work_id, 관측 계보 label 28. 산입 제외 26(접근 실패16, 읽은 진입점/기간밖/부적합 등10). 이는 계보 분류 수이지 28개 독립 실험 성공이 아니다. 동일 계보 LO-bundle, Carlito/Caladea 고지+README 등은 독립 반복으로 세지 않았다. 원장 형식 정정 S53/S54 count boolean 오류를 후속 commit으로 수정.
- 항목별 중복 가능한 자료: 사건/결정/제안 11(S06,S07,S08,S16,S22,S23,S27,S28,S32,S33,S34; 보충), 제작자 글꼴 기록·고지 9(S17,S18,S50,S51,S52,S55,S56,S57,S58), 고정판 소스 패키지 결정 5(S07,S32,S59,S60,S61; 서로 다른 release archive 0; LO 중심 동일 계보), QA 보고/변경 5(S16,S24,S25,S27,S31; 엄격쌍 0), 서지 전자판 제작 4(S36–S39; 두 판 실제 페이지 대조 0). 이 범주 수를 합산하여 원자료 수로 쓰지 않는다. 전체 35건은 직접 읽은 넓은 산입 원자료지만 범주별 엄격 요건 4 QA쌍 및 실제 배포 포함과 두 판 실물 비교는 미달. 출처마다 읽은 절 및 한계를 기입.
- substitutions 16행, outputs 13행, advice 4행. 표1은 일부 ID 묶음(16 ID 모두), 표2는 O01–O13, 표3 A01–A04. strict pairs 0, report-only O01 1, 비교 제외 O02/O03 2, expected-vs-observed O04/O05 2, metadata O06/O12/O13 3, name O07 1, production O08–11 4.
- connector에서 fixed commit 0ff19a6b7e6ad1279827c972c48f1d627e279ec3의 7개 파일을 재열람: sources 61 JSONL parse 성공, source ID 중복 0, 다른 파일의 Sxx reference 누락 0, count boolean 및 필수 url/access/reason 타입 검사 통과. CSV 물리 줄수 67/17/14/5(헤더 포함). 완전한 CSV 파서/링크 재접속 전체 검사 및 독립 검토/로컬 실행은 안 했다. 원장과 substitutions의 S16/S23 날짜 불일치를 보정 commit으로 수정.
- 표본 오염 방지: 범위 먼저 커밋. 목적 검색 결과를 이미 보았으므로 코어 검색 제목/일부 본문만으로 실제 first four라고 주장하지 않음. 공식 Bugzilla/release/TUG 차단/실패가 남아 있어 8자리 미확인. 해당 검색은 보조 재개 위치.
- H1 metric compatibility → 모든 속성 보존이라는 강한 해석을 반박하려고 S15/S27/S28/S51/S56을 열었다. H2 실제 fallback/engine/input/QA에 따라 결과가 달라짐과 비교. Carlito의 테스트 수치 보존(S27)이라는 반대 증거도 포함. S24/S16의 입력 변경을 엄격쌍에서 제외. 법적 권한을 bundle 포함으로 유추하지 않았고 외부 분야의 anchor/줄 유지 보고는 물리 면수나 font 동일성으로 옮기지 않았다.

## 남은 수

사전 8자리 8개 미확인, 실제 archive 4개 목표 중 0, 엄격 QA 4개 목표 중 0, 직접 판면 비교 4개 목표 중 0(제작기록 4개). Q5의 두 지정 엄격 반례 미확인. 모든 Q에 근거 또는 결론을 바꿀 최소 자료가 있다. Codex에 넘길 입력은 HANDOFF에서 정확히 명시한다. 중앙 상태 변경 없음.
