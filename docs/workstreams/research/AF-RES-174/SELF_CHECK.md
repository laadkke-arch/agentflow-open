# AF-RES-174 자기점검 — PARTIAL
독립 심사 아님. 작성자 본인의 행/출처 대조.
| Q | 근거 행 ID | 확인 및 미충족 |
|---|---|---|
| Q1 | I-V3376,I-V3558,I-V3746,I-G95,I-G101,I-G125; inputs V1–G3, RV/RG/C1/C2 | 6 임시 자연, 4 예비, 2 대조 슬롯(1 결측). 자연 순위 확정 불가. |
| Q2 | D-VLABEL,D-VLAYOUT,D-G070,D-G096,D-GEX,D-GNEWS2 | 4 버전 소스 + 보충; historical issue exact versions 일부 없음. |
| Q3 | M-IMHOF,M-CMS,M-ESWEIGHT,M-ESSTD,M-WAPO,M-PUD,M-KERN,M-NOVASCOTIA,M-DARWIN1/2 | 원전 4, 지도 결정 4(1 약한 의미 결정), 독립 map observation 4 계보. 교재 별도. |
| Q4 | predictions.csv, SHA d250d3667857506f1c4d2be470e51759a530259c | 48행, 12×4. 최초 결과 노출; 후속 읽기 전에 동결했으나 valid blind 0. |
| Q5 | IMG-V2a/b,IMG-V3,IMG-RG2,O-V3558b,O-V3746b,O-G125a/b,O-G139a/c, outcomes.csv | 실제 이미지 4(3 사건), 이미지 실패6. 후속 보고는 같은 work; 별도 출판 0/4. 기대 fixture 0. |
| Q6 | O-G153,O-V3336,O-G125b,O-G139c,M-MAPBOXOPT,M-KERN,M-NOVASCOTIA | N만 설명하는 환경/geometry/레이어 오류, 동률 오귀속, 조건 부적합, same-anchor 중복. 독립 독자 평가 없음. |
| Q7 | 표3, M-PUD,M-WAPO,D-VDOC,D-GEX,O-V3746b | 조건 질문과 2개 링크 분기, 외부 추가 없는 행 유지. |
분모 점검: frame 181 data rows=180 raw search+1 missing C2; raw search 79+62+39=180, 중복20, 고유160. inputs 12 data rows, predictions 48 data rows, outcomes 12 data rows. 임시 자연6+예비4+대조2. 노출11/결측1; valid false 12/12; score denominator 0, same/opposite valid 0/0. 출력별 후속 동일 조건 판독 0. 사례별 ID가 부족한 행은 추정하지 않았다.
원장 73 rows, 42 counted unique works, 36 assigned lineage IDs, 접근 실패9. 산입 범주 input6/tool4/cartography4/map_decision4/supplement24, 별도 고정 결과0. M-NOVASCOTIA는 실제 제작자 의미-가독성 결정이나 placement IDs 없으므로 엄격한 네 사례 하한을 만족했다고 주장하지 않는다(3 강한 사례+1 의미 결정). 최소 총량 충족, 유형 18/22 최대, 17/22 엄격. 동일 issue 그림/댓글 산입 제외. 별도 계보 독립성 판정 불충분. 제목만 본 결과와 모든 재열람 시도는 완전 원장화 못함(검색 원순번은 frame).
반증 시도: near-only reactive geometry와 버전/환경 차이를 실제 후속 댓글에서 확인; G125 accepted full rows; G139 ties 정렬은 identity 보장 못함; G153 cross-layer 제약; Mapbox 자체 anchor/sort 기능 중복. Imhof의 지리 면 원리 tSNE 겹침에서 무효; Kern 수동 편집 metric tradeoff; Nova Scotia 조건부 관례 예외. 지도 원전이 반대 ID를 독립적으로 맞혔다는 증거 없음.
검사: 코드 실행/렌더링/독립 평가 미실시. JSONL/CSV 행수와 대표 파일 SHA 재열람 및 경로 한정 확인만. HANDOFF 별도 커밋 예정. 다음 행동: 날짜/초기 편집 이력/결과 분리 원본 확보, 6+2 모집 재고정; 이미 노출 사례는 회귀용으로만; 별도 결과 4개와 역사적 환경을 Codex에 전달.
