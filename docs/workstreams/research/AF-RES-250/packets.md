# 독립 판단 카드 (A–F)

각 카드는 채택된 최종 스키마가 아니라 교체 가능한 판단 제안이다. 공통 source_id는 sources.jsonl; 선행 I IDs는 내부 원표를 뜻하며 독립 증거로 산입하지 않는다. 다른 카드의 필요 의존은 현재 0. 각 카드 안에서는 별도 원자산/판/행위자 필요관계가 존재한다. 카드 삭제는 자료의 물리적 삭제와 다르다.

## A / AF-RES-230 — 트랙 별 개별 export 첫 링크/재시험 확인

- **질문/목적:** 트랙 별 개별 export 첫 링크/재시험 확인
- **좁은 주장:** #5302 원작성자는 기존 혼합 출력 문제를 제기했고 이후 같은 계정으로 재시험했다고 보고했다. #5305는 selectedOnly 인자를 전달하도록 변경하여 병합되었다.
- **입력판/원근거:** A01 [issue body, comment 1746468973](https://github.com/audacity/audacity/issues/5302#issuecomment-1746468973) 2023-10-04 09:16:03Z(고정 followup); A02 [PR #5305 diff](https://github.com/audacity/audacity/pull/5305) ExportAudioDialog::DoExport @@1020; merge 425128b2a1846e7b039dac62e89438a9bbbf8a03 19:07:01Z. I230-3 #5302 rows.
- **더 강한 주장 보류:** 재시험에 사용한 build, PCM·출력 파일·파라미터, 독립 검증·모든 사용자 성공 미확인. 감사나 close로 대체 채택/성공 단정 금지.
- **대안:** Tracks 모드의 개별 경로 vs Labels 기반 시간 구간 경로; 원문 요구가 바뀌면 first link 재개. 변경 PR과 사용자 자기보고는 서로 다른 entity.
- **폐기/재개:** comment actor 불일치/수정된 원문에서 재시험 진술이 사라지면 A-report 철회; PR diff가 달라지면 A-code만 수정; 실제 PCM 검사가 실패하면 성공 추론 금지 유지.
- **필요 근거:** A01만으로 report, A02 추가로 patch; 외부 묶음 필요 없음.

## B / AF-RES-233 — 동명이인·저작/번역/편집 역할 연결

- **질문/목적:** 동명이인·저작/번역/편집 역할 연결
- **좁은 주장:** BnF는 Dumas père와 fils에 별도 ARK를 주며 W02와 W03에서 각각 fils, père의 역할을 구분한다. W01은 한 서지에 둘을 별도로 링크한다.
- **입력판/원근거:** B01 [père ARK](https://catalogue.bnf.fr/ark:/12148/cb119010630.public) 1802–1870; B02 [fils ARK](https://catalogue.bnf.fr/ark:/12148/cb11901062n) 1824–1895; B03 [W02](https://catalogue.bnf.fr/ark:/12148/cb38665336s) Auteur(s), other author; B04 [W03](https://catalogue.bnf.fr/ark:/12148/cb35752325z) same fields; B05 [W01](https://catalogue.bnf.fr/ark:/12148/cb45830647g) L57–68. I233-3 W01–W05.
- **더 강한 주장 보류:** 제목 문자열만으로 원저자 확정, 모든 판의 저작 귀속, 원고/표제면·raw MARC 확인, 동일 저자라고 병합 금지.
- **대안:** name index는 후보 탐색; ARK+role+edition은 판별, 권위 간 차이는 보류 상태; 같은 서지 두 역할을 두 사건으로 세지 않기.
- **폐기/재개:** BnF authority merge/role correction or title-page contradiction 시 해당 role edge 재개; 다른 저작·편집자 관계는 유지.
- **필요 근거:** B01–B04 필요 범위에 따라 선택, W01은 반례. 외부 묶음 필요 없음.

## C / AF-RES-234 — 그림 원자산 참조와 실제 렌더 구분

- **질문/목적:** 그림 원자산 참조와 실제 렌더 구분
- **좁은 주장:** 고정 OSM Bright style poi-level-3는 적격 school Point를 school_11에 연결한다. tile id40551996 type1 rank32 class school level 없음, atlas rect 85,123,17,17 DPR1은 334×157 안에 있다.
- **입력판/원근거:** C01–C05 commit 601ae60796ceceda2cbd2ed3d2ea92d17a84be4b: [style index92](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/style.json), [tile](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/tiles-omt/14/8711/5744.pbf), [index](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/sprite.json), [atlas](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/styles/osm-bright-gl-style/sprite.png), [TileJSON](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/tiles-omt/tiles.json). I234-3 R05–R08. C06 World style contrast.
- **더 강한 주장 보류:** 카메라 zoom≥16/overzoom, 실제 네트워크, DPR, 충돌·가시성·픽셀 재현, 최종 사용 미확인. strict sample의 3/3으로 O-I 승격 금지.
- **대안:** static reference lookup only vs runtime capture with viewport, loaded asset bytes, collision state. World style C06 is separate confirmed vacant W-I, not contradiction.
- **폐기/재개:** style/filter/feature ID/class/metadata/index/atlas digest 바뀌면 C의 해당 edge만 재검토; rendered result 다른 경우 static claim 유지 가능, runtime claim은 별개.
- **필요 근거:** C01,C02 for mapping; actual feature C04; atlas bounds C05; zoom context C03. 외부 묶음 필요 없음.

## D / AF-RES-235 — 역사 인용·현행 검증을 별도 판으로 저장

- **질문/목적:** 역사 인용·현행 검증을 별도 판으로 저장
- **좁은 주장:** WCAG 2.1의 2018 Parsing 원문과 2025 2.1 note, 2024 2.2 removed 상태를 구별한다. 이전 텍스트/앵커 보존과 적용 상태가 다르다.
- **입력판/원근거:** D01 [2.1 2018 #parsing](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) L1204–1214; D02 [2.1 2025 #parsing](https://www.w3.org/TR/2025/REC-WCAG21-20250506/#parsing) L1239–1255; D03 [2.2 2024 #parsing](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#parsing) L1434–1440. I235-3 T03/T14/T15.
- **더 강한 주장 보류:** 모든 파싱 버그가 무해함, 모든 규정에서 무조건 같은 판 적용, 테스트 도구 실제 결과를 규격 문장만으로 추론 금지.
- **대안:** historical citation과 current applicable version/state 병렬; latest-only는 역사 설명 손실, historical-only는 현행 오판.
- **폐기/재개:** 공식 판·errata 또는 사용자가 지정한 적용판 바뀌면 current judgment 재개; 역사 인용은 원판 자체 바뀌지 않는 한 유지.
- **필요 근거:** D01,D02,D03; 다른 묶음 필요 없음.

## E / AF-RES-236 — 추천 링크 읽음·이해·선택·실제 사용 분리

- **질문/목적:** 추천 링크 읽음·이해·선택·실제 사용 분리
- **좁은 주장:** #8793에서 기존 Reimport 버튼 사용 설명 후 공식 문서 링크가 추천되었고 같은 원작성자가 읽었다고 말했으나 설명이 불명확하고 잘못 생각했다며 명확성 요청을 유지했다.
- **입력판/원근거:** E01 [issue](https://github.com/godotengine/godot-proposals/issues/8793), [recommendation](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877072086) 13:10:13Z; [reply](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877111832) 13:40:07Z; [continued](https://github.com/godotengine/godot-proposals/issues/8793#issuecomment-1877143602) 14:02:53Z, 2024-01-04 times inherited I236-3 M2. E02 [fixed docs](https://github.com/godotengine/godot-docs/blob/ec71ddb6cc92414fc2f386e9790b747d30b88431/tutorials/assets_pipeline/import_process.rst#L29-L49).
- **더 강한 주장 보류:** 읽음 자기보고≠실제 click log, 정확히 읽은 historical stable bytes, 이해 완료, 대체 선택/실행/산출물/만족. no observed artifact != never used.
- **대안:** 발견/노출/읽음/이해 진술/선택/실행 증거를 별 상태; 링크만 전달 vs 대화형 설명·재질문.
- **폐기/재개:** 동일 actor or sequence or read claim 반증 시 E-report 재개; actual artifact 나오면 usage separately update; A의 다른 사람 retest로 보충 금지.
- **필요 근거:** E01 thread; 설명 내용에는 E02. 외부 묶음 필요 없음.

## F / AF-RES-237 — 작성자 노동과 총노동·검수·인수를 분리

- **질문/목적:** 작성자 노동과 총노동·검수·인수를 분리
- **좁은 주장:** METR early data 한 행의 두 시간은 README Data Spec상 동일 작성자의 initial/post-review 작업이다. dev655 issue1 232/10분, issue2 36/0분. reviewer/acceptance join 근거는 없다.
- **입력판/원근거:** F01 [data_complete.csv](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv) header and dev_id655 issue_id1/2; F02 [README Data Spec](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/README.md) (heading Data Spec, anchor not asserted). I237-3 stages.csv; I237-2 12 inherited rows.
- **더 강한 주장 보류:** 0 post-review 작성자 시간 ≠ reviewer 0; 전체 팀 노동, 인수 품질, AI 효과/절감, 12행의 모집 대표성 미확인.
- **대안:** 작성자 time pair만 제시; 별도 reviewer time+accepted artifact+actor join을 확보한 뒤 total labor 계산. 완료 사례만으로 비교 금지.
- **폐기/재개:** data dictionary 또는 author/row key 반증 시 actor/time 해석 재개; 추가 reviewer logs가 있으면 total-labor hold 재개, 기존 author times 그대로 유지.
- **필요 근거:** F01/F02 둘 필요; reviewer data 외부 미확인. 외부 묶음 필요 없음.
