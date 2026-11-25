# 반례·정정 기록 (SCOPE → RESULT)
- 이전 SCOPE 예상: C는 보통 기본 검정. 정정: N07 CSS Color 4 §3.2 color initial CanvasText, §6.4 currentColor; C는 독립 문서의 color, black은 제어된 light 환경 기대에 한정. N04 initial fill black과 color 초기값 구별. 실제 픽셀 미실행.
- 이전 경쟁 가설: 파일·형상 동일하면 같은 표시. A01/A02/A03 exact ordered path match 3/3, root fill=currentColor vs selected symbol fill absent (A04 removeAttrs). B wrapper에서 fill 복원. 파일 동일성 아닌 문맥·선택 조건 필수. T03, T10 반대 사례; 특정 icon 실행 필요.
- 단일 file의 모든 symbol이 표시 의존이라는 생각 철회: 2050 symbol 중 두 ID만 선택. X1 실제 ID 없음 확인, file 존재만으로 target 유효성 불충분; T07 display:none 존재 반례, T04/T05 active nested ref는 한 파일만으로 부족한 반대 사례.
- X2 같은 basename/다른 absolute URI와 bytes; X3 unused defs href: 표시 필요성 vs 브라우저 요청 여부 분리, 미실행이므로 fetch 없음 단언 철회. O4 원본 외부 참조 정상 공석. 
- I02 당사자 보고 GET 실패와 maintainer ZIP 포함 주장 공존: HTTP 상태·실제 누락은 미확인. I01 subset 제안과 T02 교차 출처는 현재 표본의 동일 출처에 조건부.
- G05 공식 OGC sample binary 미수신 → G02 GDAL publisher SQL actual rows를 명시적 별도 표본으로 대체 비교; 원래 artifact 행을 채웠다고 주장하지 않음.
- 정정 근거는 sources.jsonl, 정확한 4 통제/조건은 bundles.md. SCOPE 원판을 보존하여 변경 순서를 추적. 독립 검토 미실시.
- 후속 정정: G06 GDAL byte.gpkg 실제 bytes 12800 B와 G07 SQLite 파일 규격을 정적으로 판독. G02 SQL x는 G06 binary byte와 이름/last_change가 다르다. matrix 값은 일치하지만 동일 serialized data가 아니다. byte evidence JSON에 page offset/serial types/overflow를 저장. 본체 증거가 있는 GDAL sample로 비교하고, OGC 74984 미수신 유지. T08c red-bg.css를 열어 외부 red rule 자체도 확인했지만 픽셀/네트워크는 여전히 미실행.
