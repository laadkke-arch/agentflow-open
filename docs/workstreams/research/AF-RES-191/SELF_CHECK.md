# AF-RES-191 self-check

작성자 자체 검토. 독립 검토자 없음. 새 브라우저 렌더, pixel scoring, 실행·관찰 실험 없음. 질문별 링크와 판정은 RESULT/claims/decisions/transfer 및 sources.jsonl과 대조했다. 결과 전부는 지정 owned_path에만 둔다. 단계 ⑤ 뒤 고정 커밋에서 다시 읽기와 범위 비교를 한 후 HANDOFF에 실제 확인 결과를 별도로 남긴다.

| Q | 답 및 원자료 위치 | 실제 찾아본 반증 위치·결과 | 판정/미충족 |
|---|---|---|---|
| Q1 | A01 [§13.2](https://www.w3.org/TR/2025/CRD-css-color-4-20250424/), A02 [§14.2/Changes](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/), A03 [diff](https://github.com/w3c/csswg-drafts/commit/f5642b931d905128daa075fdfeba6c9e74475b5a), A04 [Ray correction](https://github.com/w3c/csswg-drafts/commit/24a74f8c006709dfbf0538af80ea3086b213228e) | A02 nonnormative §14.1 clipping acceptable 예; 세 선택은 그대로. §14.2.4 placeholder 및 2025 geometric prose 제거를 확인 | 연결 충족. 실제 엔진·pseudocode 미완 부분 명시 |
| Q2 | B01 [#10579](https://github.com/w3c/csswg-drafts/issues/10579), B02 [결의](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200859856), X03 [편집자](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3787184061), B03 [#9449](https://github.com/w3c/csswg-drafts/issues/9449) | D07 [Lea 수정](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200476676), B03 2023 red/canvas counter, D04 [PR44](https://github.com/color-js/apps/pull/44) 새 방법이 더 빠를 수 있음 | 결의 이유·순서 충족, 특정 외부 지각연구 인과 미확인 |
| Q3 | A02 §14.1.1/3/4/6, B03 .9 magenta/99% tint, D08 [grid](https://svgees.us/Color/ok-clip-lch-explorer.html), C02 [p13 Fig10](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/6/1/art00003) | 근소 음수 blue 예, D07 L 가설 정정; C02 144° no advantage, 별도 CIELAB 비교 | 모델값과 실제 사람 판단 분리; cyan 별도 수치/화면/observer 및 새 GMA 사람 효용 미확인 |
| Q4 | C01 [Oklab](https://bottosson.github.io/posts/oklab/), C02 [IPT](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/6/1/art00003), C03 [ΔE00 원문 DOI](https://doi.org/10.1002/col.1049), C04 [CAM16 DOI](https://doi.org/10.1002/col.22131), C05 [implementation](https://hajim.rochester.edu/ece/sites/gsharma/papers/CIEDE2000CRNAFeb05.pdf), D09 [toe](https://bottosson.github.io/posts/colorpicker/) | Oklab 비교 H .49 vs IPT .48/JzAzBz .43; C05 수학 불연속; C04 조명/크기 strata. A02 ΔEOKr2 별도 code에서 toe 원저자 인용 | 조건/거리/경계/규약 분리. Hung 원문 접근 실패; ΔEOK .02 실험사슬 미확인 |
| Q5 | B02, A03, A04, B05 [Ray](https://facelessuser.github.io/coloraide/gamut/#ray-tracing-chroma-reduction), D08 및 D04 | D03 [PR36](https://github.com/color-js/apps/pull/36) 반환 색공간 공정성, D04 PR44 P3 clip 우위·blue fold·cache; B04 [docs](https://colorjs.io/docs/gamut-mapping.html) 구 metric 예와 현재 설명 혼재 | 가까운 공학 설명 충족. 런타임 절대 순위·실측 동등성 아님 |
| Q6 | D01 [사진](https://bottosson.github.io/posts/gamutclipping/), E01 [ICC WP40](https://archive.color.org/files/WP40-Black_Point_Compensation_2010-07-27.pdf), E02 [Blurb](https://support.blurb.com/hc/en-us/articles/360027277391-Preparing-color-images-for-Adobe-InDesign-or-Blurb-s-PDF-Uploader-workflows), E03 [Epson](https://epson.com/Support/wa00351), E04 [darktable](https://docs.darktable.org/usermanual/5.6/en/module-reference/processing-modules/filmic-rgb/) | E02 perceptual vs E03 relative default; D01 original author recommends considering compression for many OOG; D09 same author different color picker tradeoff | 매체별 실패·비용 식별. 실제 로고·프린트 측색·영상 실측 미확인, 지침만 확인 |
| Q7 | RESULT 표3, transfer T01–06. [A02](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/), [C01](https://bottosson.github.io/posts/oklab/), [E01](https://archive.color.org/files/WP40-Black_Point_Compensation_2010-07-27.pdf) | CSS 허용 확인은 근접 규격으로 완료 가능한 반례. 인쇄 workflow가 목표별 다른 조건을 추가 | 세 목적별 근거 조합, 남는 조건 기록. 제품 최종 설계 미결정 |

## 모집 분모·증거 단위

| 종류 | 예정 | 산입 | ID |
|---|---:|---:|---|
| A 초안·이력 | 4 | 4 | A01–04 |
| B 제안/결의/제작자 | 5 | 5 | B01–05 |
| C 색과학 원연구·저자 | 5 | 5 | C01–05 |
| D 별도 색 입력·도표·저자 평가 | 4 | 4 | D01,D04,D08,D09 |
| E 인쇄·사진 작업 | 4 | 4 | E01–04 |
| 계 | 22 | 22 | 21 work_id, 14 lineage_id (같은 저작 두 CRD 별도 판으로 산입) |

33 ledger 행 중 22 산입, 11 제외/대조. frame의 D04-missing은 ② 중간 부족의 보존 행이지 새 자료 아님. D03은 비교 수정 PR만이라 ④에서 산입 하향; D09 독립 계산/단면으로 대체. D02,D05,D06,D07/X03 등 동일 계보 보고는 보수 제외. E01X 404를 E01 대체. X01 original hue study, X02 CodePen, X04 EdgeSeeker path access 미확인. C04 저자 논문 미러를 원저작 1개로만 계산. B02는 동일 issue 내 별도 공식 회의 원기록(논의 B01과 별도 work_id); D01/D09는 동일 저자·모델 계보지만 서로 다른 작업·자극·목표. 2025/2026 공식 판 2개는 한 work_id. 모집은 전수 문헌 연구가 아니며 목록의 22는 조회 성공한 고정판 또는 독립 작업물 수이다. 확인일은 작업 시작 UTC 날짜 단위(개별 초 미기록), living 자료는 exact SHA 미확인. 도표는 원문 설명/표 및 일부 PDF 페이지 screenshot; 새 렌더/화소 검산 없음.

사건 분모는 decisions J01–09의 날짜 있는 9개 단위(두 판 발행 포함; 결의1/편집2/발행2/문제·제안·가설·PR4). 사람 실험 C02 1개 직접 읽음(9명/30세션/세션당90 judgments). C03/C04는 여러 기존 데이터 재분석이지 각 관찰자를 고유 실험으로 합산하지 않음. CSS 세 GMA 비교의 관찰자·조건·비교값이 모두 있는 지각 실측 0개 발견. E02/E03 서로 다른 실제 작업 시스템, 출력 검증 없음. 관찰 자료가 없는 효용을 실측으로 표기하지 않았는지 K01–K14 자체 검토.

## 판단

최소 22자료 분모와 종류 충족, 두 규격 같은 절과 실제 결의+반영의 연결 및 원리/비용 적용 조건 판별 충족. 다만 외부 논문에서 #10579 변경에 이르는 원인 사슬, CSS 실측 효용, 실제 장치/영상은 미확인. 이 미확인 자체가 Q의 답이며 허용된 조사 범위 안의 규범 및 편집 결의 연결을 부정하지 않는다. 독립 검토와 실행 검증을 수행한 것으로 보고하지 않는다. 다음 세션이 판단을 보정할 때 RESULT 마지막 표의 세 약점부터 재개.

부가 검사 제안(미실행): GitHub 고정 SHA에서 9개 파일을 읽고 source_id/row count, 표 1/2/3 열 이름, 마지막 약점 행 3개, base 대비 changed files owned_path만인지 검사. 실행 필요 시 Codex Cloud의 checkout에서 Python 표준 json/csv, git diff를 사용; 브라우저/지각 실험은 과제 제외. 저장소 manifest와 workbench 검사는 로컬 repo checkout이 없으므로 실행하지 않았다.
