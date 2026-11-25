# 반례, 충돌, 정정 — ④

## 발견한 원자료 반례 (가상 실패 시나리오와 분리)

1. **동일 레코드에 복수 역할/부분 철회:** B05 [Correspondance](https://catalogue.bnf.fr/ark:/12148/cb45830647g) L57–68은 한 서지(2019, FRBNF45830647)에 Sand와 두 Dumas의 서로 다른 authority 링크, 별도 편집자 링크를 보인다. 한 레코드가 복수 edge를 지지한다. 예컨대 fils 역할 정정이 관측되더라도 père/편집자 링크를 자동 철회하지 않는다(정정은 가정, 실제 정정 미관측). B03/B04에서 별 저작 역할 직접 대조. 동일 이름만으로 합치거나 한 서지를 세 독립 사건으로 세지 않는다.
2. **판/텍스트/상태 불일치:** D01 [WCAG 2.1 2018](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#parsing) 4.1.1 → D02 [2.1 2025](https://www.w3.org/TR/2025/REC-WCAG21-20250506/#parsing) 같은 기준 텍스트와 note → D03 [2.2 2024](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#parsing) removed. 인용 가능=현행 적용의 반례. 같은 문서의 다른 edition, 기준 ID와 applicability를 별도 키. 옛 인용을 버리지 않는다. D02/D03의 정확한 도구 실행은 미관측.
3. **서로 다른 actor/성과를 이어 붙이는 반례:** A01 원작성자의 테스트 발언(2023-10-04)과 E01 원작성자의 링크 읽음 발언(2024-01-04)은 다른 서비스, 다른 actor, 다른 action, 다른 대상이다. E01의 발화에 여전히 명확성 문제가 있으므로 '추천→읽음→선택→실행→성공' 연결의 실제 반례. A02 code change와 병합도 성공 산출물에 대한 증명은 아니다. A의 report와 E의 read를 보완하되 join하지 않는다.
4. **정적 자산 vs 화면:** C01–C05 원자료로 적격 feature→school_11 및 atlas rect 경계를 확인. 그러나 미확인 렌더 변수들이 남아 있다. C06은 같은 프로젝트의 다른 World style에 8 layers, icon-image 0 및 sprite 없음. O-I를 World의 W-I로 전이할 수 없다는 실제 반례. 고정 타일 maxzoom14와 layer minzoom16은 overzoom 조건이 필요함을 나타내나 실제 충돌/로드/가시성 증거는 아니다.
5. **0과 결측:** F01 [CSV](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs/blob/7ff2d7670235f531dff77eff58355bd77392f396/data_complete.csv) issue2의 post-review 0은 관측 수치다. F02 정의상 저자 작업시간이지 reviewer time이 아니다. 따라서 0을 독립 검수/인수 시간에 옮기는 것은 실제 원행+정의에 반한다. issue1 232/10은 합산해도 author pair의 범위만(242분); 총노동 및 효과/품질 미확인.
6. **종합에서 결론이 유지되거나 바뀌는 실제 사례:** H03 [updated review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6464774/) L492–501, 911–914, 1546: 두 후속 보고를 Newnham1993에 붙이고 결론 유지, subgroup은 결합하지 않음. H04 [review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8941847/) L429–444: 형식 변경과 결론이 변경된 substantive amendment는 별도. 자료 수 증가=결론 변화, 새 문서=새 사건이 아님. H04에서 구체 이전/이후 결론 비교 원문은 미확인.

## W-I 행 열 수 정정

I234-4 [고정 layers.csv](https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/layers.csv): header 20개, W-I 원행 19개. 마지막 M13/not strict가 feature_evidence/source_ids로 이동하고 unknown이 누락되는 형태. 빈 feature_evidence를 복원하고 원자료를 다시 연결한다. 이 작업에서 원본 수정하지 않는다. C06 [World style](https://github.com/maplibre/demotiles/blob/601ae60796ceceda2cbd2ed3d2ea92d17a84be4b/style.json) blob a5f8b44babce223fafcbe0b3c45132d3f1c46e43 전 layers 8, layout.icon-image 0, root sprite 없음. W-I는 additional contrast, vacant_confirmed; index/layer ID/source/source_layer/min/max/filter/property/font/feature 모두 정상 공석. W-I를 O-I 학교 그림의 원표와 혼동하지 않는다.

정정된 20열 제안 (다른 필드는 원표 유지):
```csv
"slot","publisher","role","cohort","style_sha","style_identity","selection_status","layer_count","index","layer_id","source","source_layer","minzoom","maxzoom","filter_original","property_original","font_original","feature_evidence","source_ids","unknown"
"W-I","MapLibre","icon","additional contrast","601ae60796ceceda2cbd2ed3d2ea92d17a84be4b","style.json","vacant_confirmed","8","","","","","","","","","","","M13","not strict"
```
M13은 AF-RES-234의 원자료 ID, 이 작업 대응 C06; 해당 원문에서 0 확인. 열 수 오류를 근거 부재로 전환하지 않는다.

## 사전 범위 정정/검사

- 계획 SHA 7369707441e2eb70e84004ca6cb3bfeefc8b4061 → 시작 SHA 78b64ce8b84ef1d37c2a7100dc376c65dd97e74a compare: ahead15, behind0, only dot-control.json +317/-12. 계획 blob f6587b49dccac907b5e2dd1e67bf3e36c1590ccd, 시작 blob 952d292095e8034b5fddbc98ebe56fbe9a5347c3. 둘 다 직접 blob parse; 계획판에는 AF-RES-250 entry 없음(계획 기준), 시작판 RUNNING, 명시 여섯 의존 SHA 모두 일치. 238–242의 입력/출력/정답은 사용하지 않음.
- C04 direct PBF wire parse 성공: poi layer 1867 features, target feature ID40551996 type1, class school, rank32, level absent. 단 JS byte→string에서 비ASCII 문자 깨짐이 발생하여 해당 명칭 주장은 제외(ASCII filter inputs에는 영향 없음). C05 PNG signature/IHDR만 읽음. CRC/픽셀 decode/render 미실시. 원작업의 이미지 보기와 이 작업의 binary-header 읽기를 구별.
- ③ 최초 L 예시/removed lost_claim에 A02 patch나 C04/C05 상세와 같은 확장 정보가 섞여 복구 비용과 불일치. ④ assemblies/removals에서 L narrow를 축소하고 F01/F02의 heading locator를 정확한 고정 파일+Data Spec으로 정정. 비용 L=5 additional, X=12 additional(각 최초 6 별도); 두 안의 주장 범위가 같은 것으로 세지 않는다. 이 수치는 설계 산정, 모델 실험 결과 아님.
- 사례간 실제 hard dependency를 발견하지 못했다(15쌍 모두 검토, 5 independent/10 complement). '발견하지 못함'은 세계의 모든 근거 계보가 독립이라는 증명이 아니다. 동일 보고서에 공동 역할, 동일 사건에 다른 발언, 동일 study에 여러 보고, 동일 work 여러 판은 내부 연결로 보존. 공동 근거 상실 시 그 근거에 직접 연결된 주장만 다시 연다.
- PEP622→634/635는 실제 분할 사례. P05 PEP703 acceptance에서는 rollback 조건을 명시하지만 MADR0008/0009/0016에는 명시 조건이 없다. 재개 조건을 후대 작성자의 제안으로 표시하고 과거 author 주장으로 가장하지 않는다.
