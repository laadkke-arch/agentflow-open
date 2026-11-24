# AF-RES-175 — 공개 시험의 객체별 보존 및 조건부 조합 판정

| 연구·모델·객체 | 송신판·방향·옵션 | 입력 값·원문 주소 | 수신판·제출물 주소 | 첫 결측 |
|---|---|---|---|---|
| G1 Myran / 식별 | Revit 2018 ENU, 2017-10-25, IFC2x3 CV2.0 → 각 수신 도구 | 모델명/클래스만, [초기 연구 §4.2.1](https://isprs-archives.copernicus.org/articles/XLII-2-W13/1339/2019/isprs-archives-XLII-2-W13-1339-2019.pdf) | [제출 ZIP 목록](https://zenodo.org/records/3964368/preview/benchmarkTask1_exportedIFC.zip?include_deleted=0), [보고 v2](https://zenodo.org/records/6470370) | 원 GlobalId |
| G2 Myran / 단위 | 동일 | [Table 7](https://repository.tudelft.nl/file/File_44c29669-921a-4261-ba53-df452e91ca8c) 단위 entity 집계; 개별 단위값 미확인 | GD01–07 후보, 정확 열-참가자 조인 없음 | 원 단위값·entity ID |
| G3 Myran / 공간관계 | 동일 | [초기 연구 Fig3](https://isprs-archives.copernicus.org/articles/XLII-2-W13/1339/2019/isprs-archives-XLII-2-W13-1339-2019.pdf) 원래 층 배치 불일치도 존재 | [제출 ZIP](https://zenodo.org/records/3964368) | 원 관계 ID·양 끝 객체 |
| G4 Myran / 하중 또는 대응 속성 | 동일 | [Task1 §4.4/Table 7](https://doi.org/10.1111/tgis.12709) 하중별 시험행 없음; 대체 속성값 미확인 | [보고 v2](https://zenodo.org/records/6470370) | 하중은 표 미측정; 대응 원 속성 키/값 |
| S1 §5.2 프레임 / 식별 | RFEM 5.14.02→SAP 19.2.1(A), RFEM 5.23→SAP 22(B); 반대도 별도 제작; 표 SAV/문장 CV2.0 충돌 | [Table 2/7](https://www.mdpi.com/2076-3417/11/23/11430) 형상 E, 객체 ID 없음 | 동일 논문 표 7; 제출 파일 링크 미확인 | 원 native ID/GlobalId |
| S2 같은 프레임 / 단위 | 동일 | [Fig6 §5.2](https://www.mdpi.com/2076-3417/11/23/11430) 50 kN/m, 25 kN (명목량) | 동일 논문 표 7; 단위별 grade 없음 | 원 IFC 단위 정의/환산 |
| S3 프레임 / 경계조건 | 동일 | [Fig6/Table7](https://www.mdpi.com/2076-3417/11/23/11430) 구속 조건 설명·그림; DOF keyed 값 없음 | 양방향 E/E, 동일 논문 | 원 노드 ID 및 DOF별 값 |
| S4 프레임 / 하중 | 동일 | [Fig6 §5.2](https://www.mdpi.com/2076-3417/11/23/11430) 50 kN/m, 25 kN; signed target 미확인 | 순 E/E, 역 P/P; [표7](https://www.mdpi.com/2076-3417/11/23/11430) | 하중 대상·부호, 실제 제출과 수신량 |

단위: 고정 속성 자리, 예정 8, 원 연구 보고를 판독한 자리 8, 같은 객체/판/실제 값 완결 0, 결측 8. 제외 0(미측정 G4도 유지); G4 대응 속성 미확인. GD01–15는 목록 후보 별층이며 8자리 분모에 포함하지 않는다.

| 속성·요청 목적 | 원값 | 수신·재출력 값 | 보존·손실·미측정 | 같은 객체·판의 근거 주소 |
|---|---|---|---|---|
| G1 식별 | 원 GlobalId 미확인 | 미확인 | 미확인 | [R01](https://doi.org/10.1111/tgis.12709), [D13](https://zenodo.org/records/3964368/preview/benchmarkTask1_exportedIFC.zip?include_deleted=0), 객체 조인 없음 |
| G2 단위 | 개별 값 미확인 | aggregate만 | 값 미확인 | [R01 Table7](https://doi.org/10.1111/tgis.12709) |
| G3 공간관계 | 원 층 그룹 이상 보고 | 관계 수/외관 | 값·관계 미확인 | [R11 Fig3](https://isprs-archives.copernicus.org/articles/XLII-2-W13/1339/2019/isprs-archives-XLII-2-W13-1339-2019.pdf) |
| G4 하중/대응 속성 | 미확인 | 하중별 표 없음 | 하중 미측정(공개 표 범위), 대응 속성 미확인 | [R01](https://doi.org/10.1111/tgis.12709) |
| S1 식별 | 원 ID 없음 | 형상 E | 식별 미확인 | [R07 Table7](https://www.mdpi.com/2076-3417/11/23/11430) |
| S2 단위 | kN/m, kN 명목 | 단위 비교 없음 | 별도 단위값 미측정 | [R07 Fig6](https://www.mdpi.com/2076-3417/11/23/11430) |
| S3 구속 | Fig6 설명, keyed DOF 없음 | E/E 양방향 | 연구자 등급 양호, 값 미확인 | [R08 Table7](https://www.mdpi.com/2076-3417/11/23/11430) |
| S4 하중 | 50 kN/m, 25 kN 명목 | RFEM→SAP E/E; SAP→RFEM P/P | 방향별 저자 판정 차이; 정량 손실량 미확인 | [R07–08](https://www.mdpi.com/2076-3417/11/23/11430) |
| GC1 단위 entity 누락 | 원표 class count | 두 행에서 7열 -100% (잠정 원면 판독); 본문 7/16 사례 | entity 집계 손실; 물리량 손실 단정 금지 | [R03/R12 p826](https://repository.tudelft.nl/file/File_44c29669-921a-4261-ba53-df452e91ca8c), [D13](https://zenodo.org/records/3964368/preview/benchmarkTask1_exportedIFC.zip?include_deleted=0) |
| GC2 동수·외관 | 원 feature counts | ACCA 두 도구 동일 수, usBIM.viewer site wireframe 이상 | 수 일치와 외관 불일치; 속성 수치 비교 없음 | [R04](https://doi.org/10.1111/tgis.12709) |
| GC3 무오류 재출력 | 원 건물 | Revit 빈 모델, Tekla 한 beam, ArchiCAD 간판만 | 외관/내용 손실 보고, 구문 검사 합격 아님 | [R04](https://doi.org/10.1111/tgis.12709) |
| GC4 wall type | 원벽 수 | -718 IfcWall/+718 IfcWallStandardCase | 표현 변화, 동 객체 의미 보존 미확인 | [R12 Table8](https://doi.org/10.1111/tgis.12709) |
| SC2 편집 | 건물 객체 | Tekla 단일 reference block | 시각 참조 가능, 편집 객체 아님 | [R09 §5.3](https://www.mdpi.com/2076-3417/11/23/11430) |
| AV3 메뉴 기능 | DVD 메뉴 동작 | ISO 동작 유지; MPEG2 화면만 | 기관 보고의 목적별 손실 | [A04 pp38–39](https://www.digitizationguidelines.gov/guidelines/FADGI_BDV_p2_20140908.pdf), 개별 파일 미공개 |
| MARC1 필드 범위 | 명세의 MARC 요소 | nac / ignore 및 880/$6 linkage 한계 | 의도된 미변환/구현 한계, 실제 인수값 미확인 | [M04](https://loc.gov/bibframe/mtbf/), [M09](https://github.com/lcnetdev/marc2bibframe2) |

단위: 주층 8 + 지정 교정 5 + 분야 보충 예시 2. 실제 원표 판독·보고 등급은 있지만 동일 객체의 원값·수신값을 조사자가 판독한 건 0. GC1 16은 본문의 사례 분모, 원면 절대/비율 블록 각각 14열(잠정). 7/16은 개별 unit entity 개수나 물리량 손실률이 아니다. 14열과 16의 대응 미확인. S의 E/F/P는 Excellent/Fair/Poor 등급, 값의 차이나 백분율 아님. 실제 왕복 0.

| 보내려는 조합·방향 | 사양으로 답할 범위 | 공개 시험으로 답할 범위 | 반환 원전·문장 | 추가 입력 |
|---|---|---|---|---|
| A-VIEW Revit→뷰어/협업 도구, 단방향 시각 | CV/RV 참조 범위 | G: 정상 개방/재출력과 내용 손실이 별개; SC2 단일 블록 | [G](https://doi.org/10.1111/tgis.12709), [bSI](https://www.buildingsmart.org/compliance/redevelopment/) “시각 참조 후보, 지정 객체/방향 확인 필요” | 동일 IFC 해시, 제품판/옵션, 기대 화면/객체 |
| A-ATTR1 RFEM→SAP, 하중 재사용 | SAV 도메인의 표현 가능성 | S의 두 버전쌍 하중 E, 재료 P | [S](https://www.mdpi.com/2076-3417/11/23/11430), [RFEM5](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001472) “조건부 후보, 수치 보존 미확인” | signed target ID/단위/좌표계/하중 case, 수신값·정확 옵션 |
| A-ATTR2 SAP→RFEM | 동일 사양이어도 방향별 구현 다름 | S 하중 P, 재료 F; 역방향 별도 입력 | [S](https://www.mdpi.com/2076-3417/11/23/11430), [CSI import](https://docs.csiamerica.com/help-files/sap/Menus/File/Import/Import_IFC_File.htm) “해당 판의 하중 재사용은 보류” | 동일 입력·양 판/옵션·받은 실제 값 |
| A-EDIT A→B→A 편집 복귀 | CV/RV의 완전 왕복 목적 아님 | G 재출력과 S self reimport는 cross-tool 복귀 아님 | [bSI](https://www.buildingsmart.org/compliance/redevelopment/), [S](https://www.mdpi.com/2076-3417/11/23/11430) “검증된 조합 없음, native 원본 유지 후보” | 객체 매핑, B에서 수정, B 출력→A 실제 재수입 결과 |
| A-UNIT Revit→교환 도구, 단위 관계 | IFC 단위 정의 가능 | G 집계 손실 관측 | [Table7](https://doi.org/10.1111/tgis.12709), [NIST IFA](https://www.nist.gov/services-resources/software/ifc-file-analyzer) “단위값과 환산 확인 전 보류” | 원 객체·단위값, 제출파일/참가자, 수신값 |

단위: 5개의 IFC 목적/방향 조합; advice.csv에 분야 간 적용 1 추가. 같은 객체/판의 실증 확정 0, 조건부 시각/속성 후보 2, 재검증/보류 3. 사양 링크 1개·양 구현 옵션·동일 객체 결과를 각각 범위, 실행 전제, 수용 증거로 구분하며 어느 한 층도 다른 층을 대체하지 않는다.

## Q1. 공개 시험 단위 및 입력/제출 연결

G의 원보고(2021; 2019 benchmark) §3.1–3.2 Table2는 Myran IFC2x3 27.14MB, UpTown IFC2x3 241.04MB, Savigliano IFC4 21.55MB. 43 reports/33 packages는 보고 집계, Myran 40, Savigliano 25, UpTown 20의 열기 기록은 모델별 중복 가능한 관측이다. Table7/8은 재출력 entity counts/차이; 개별 참가자 ID가 아니다. [2019 설계 원보고](https://isprs-archives.copernicus.org/articles/XLII-2-W13/1339/2019/isprs-archives-XLII-2-W13-1339-2019.pdf) pp1341–42 원면에서 Myran Revit2018 ENU CV2.0, UpTown Revit2015 2017-03-20 CV2.0, Savigliano Revit2019 ITA 2019-03-14 DTV1.0을 확인. UpTown 크기 표기는 초기 252.7MB/후기 241.04MB, MiB 환산 가능하지만 동일 파일 해시 확인 전 단정하지 않는다. 데이터 페이지 접근 실패 및 사용 동의 표시(검색 캐시만), 원본 입수 미완료.

[제출 레코드 3964368](https://zenodo.org/records/3964368)와 [보고 3964445](https://zenodo.org/records/3964445), [v2 6470370](https://zenodo.org/records/6470370)을 확인. [ZIP preview](https://zenodo.org/records/3964368/preview/benchmarkTask1_exportedIFC.zip?include_deleted=0)에서 모델/도구를 포함한 15개 파일·중첩 ZIP 후보를 직접 판독해 GD01–15로 기록. 데이터셋 당 하나의 work_id를 사용. v2 추가 1Task_DelResults_Rlinks.pdf (15.2MB, MD5 0ab606fd83e743064570ad50dd5ea6ad); 웹 추출 제한으로 설문 행은 미판독. 모델 파일명 fixed 및 버전 표기 차이 때문에 모델명만으로 같은 원판/참가자/실행을 확정하지 않는다.

S [2021 논문](https://www.mdpi.com/2076-3417/11/23/11430) Table2, Tables3–4, §5.2 Fig6–7/Table7. 행/열은 방향과 2 release 쌍 A/B × 형상·재료·구속·하중의 정성 등급. 입력 설명은 있으나 공개 native/IFC 제출물·실험 ID는 확인하지 못했다. 정확 공개 시점은 논문/레코드의 발행판 범위, 개별 업로드 시점 미확인.

## Q2. 원값과 집계의 차이

G 원 GlobalId, STEP entity ID, unit assignment value 및 대상 ID를 직접 판독하지 못했다. [NIST IFA](https://www.nist.gov/services-resources/software/ifc-file-analyzer)는 entity별 worksheet와 instance row를 제공하는 방법이지만 2024 문서이며 이 연구의 원판 또는 직접 실행이 아니다. original spatial grouping의 불일치도 수신 손실과 별개. S §5.2 원문의 명목 하중 50 kN/m, 25 kN을 읽었으나 signed target과 수신 수치를 조인 못 했다. [IFC2x3 TC1 규격](https://standards.buildingsmart.org/IFC/RELEASE/IFC2x3/TC1/HTML/ifcstructuralanalysisdomain/lexical/ifcstructuralanalysismodel.htm)에서 GlobalId, LoadedBy, IsGroupedBy, HasResults를 별개의 의미로 읽었다. 규격의 객체 표현은 연구 모델의 실제 값이 아니다.

## Q3. 제품판/옵션과 단계

S의 버전쌍은 Table2에 명시되나 §5.2 첫 문장의 CV2.0과 Table7의 SAV 문맥이 충돌. 정확 exporter MVD/setting log를 요구. [RFEM5 FAQ](https://www.dlubal.com/en/support-and-learning/support/faq/002307), [RFEM5 KB](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001472)는 SAV 지원, 하중 및 단면/재료명 범위, CV solid 전환 등을 설명. [CSI 도움말](https://docs.csiamerica.com/help-files/sap/Menus/File/Import/Import_IFC_File.htm)의 entity 선택, 양 view 중복, section mapping, .ifcimp.log는 정확 19.2.1/22 스냅샷 아님. 최신 KB/24.2.0 릴리스 정보는 역사판으로 소급하지 않는다. G의 열기, 시각 관찰, NIST 비교, 재출력은 단계별 분리; 무오류는 구문 검증 증거 아님. S의 형상 E 또는 참조 block은 편집성 증거 아님. 수치 보존 실측/실제 A→B→A 없음.

## Q4. G 지정 반례와 분모

Table7 p826 [원 PDF](https://repository.tudelft.nl/file/File_44c29669-921a-4261-ba53-df452e91ca8c) 스크린샷 원면에서 절대수 및 비율 블록 각각 14개 열로 판독. 본문 7/16 사례에서 IfcDerivedUnit/IfcDerivedUnitElement 누락. 원면 잠정 7열은 FreeCAD, ArchiCAD 2열, Allplan, AutoCAD Architecture, AutoCAD Civil, FME. D13 파일명은 각각 GD01–07 후보(Archicad.zip GD15도 있음), 원면 열과 참가자 매칭/원래 16 분모 미확인. ACCA PriMus, usBIM.viewer 수 동일 및 latter wireframe anomaly (GD08/09 둘 다 28.5MB; 크기 같아도 바이트 일치 아님). Revit 빈 결과, Tekla 한 beam, ArchiCAD 간판만은 본문 보고; GD02/10/11 등의 작은 파일이 그 사례라고 확정하지 않음. Savigliano -718/+718 wall class는 집계 기준을 바꿀 때 동수가 될 수 있으나 동일 객체 수치 보존 증거 아님. **동수이면서 실제 수치가 다른 요청 사례는 확보 실패**; 대응 속성 원값과 실제 수신값 필요. 결론을 깨는 가능성: 단위 entity 생략이 같은 물리량의 정상 단위 환산일 수 있음; 현재 보고로는 구별 불가. UpTown NIST 분석 제외 보고; 전체 도구 대표 통계 아님.

## Q5. S 지정 방향 비교

Table7 행/열을 그대로 판독한 방향 ledger SC1-A–E: RFEM→SAP A/B 모두 geometry E, material P, restraints E, loads E; SAP→RFEM A/B 모두 geometry E, material F, restraints E, loads P. self reimport E는 그 자체의 결과만. 본문의 RFEM→SAP 문제 없음 진술은 material P와, 역방향 하중만 손실 진술은 material F와 긴장. 원 모델은 양측 별도 제작. 50 kN/m 및 25 kN이 명목 동일하여도 객체·단위계·좌표·부호·대상 ID·옵션이 같다고 확정 못 하므로, 방향별 저자 등급의 차이로 한정. 하나의 파일 왕복 또는 실제 물리량 보존·구조 안전 판단 금지.

## Q6. 분야 간 비교

AV: [BFI Open Reel](https://www.bfi.org.uk/features/open-reel-open-source-digital-preservation-uks-videotape-heritage) V210→FFV1 frameMD5 비교 절차; [Kromer](https://retokromer.ch/publications/IASA_49.html) 5.7PB migration 보고; [FADGI pp38–39,42–43](https://www.digitizationguidelines.gov/guidelines/FADGI_BDV_p2_20140908.pdf) Smithsonian ISO DVD 메뉴 기능 보존/접근 MPEG2 화면만 및 NARA 여러 소스 WinFF, DVD ISO와 원본 확인 후 인수. 3 work, 4 프로젝트 계보; 개별 파일 ID·기대/실제값 공개 대응 0. 바이트 동일/복호화 프레임 동일/상호작용 기능 동일은 다른 수용 조건.

MARC: [LC pilot p3,p5](https://www.loc.gov/bibframe/docs/pdf/bibframe-pilot-phase1-analysis.pdf) 18m 대상 중 13.5m 변환, 13.4m Works, Work/Instance 분리 및 명칭 병합 미해결. [MARC→BF](https://loc.gov/bibframe/mtbf/) nac/ignore와 [BF→MARC](https://www.loc.gov/bibframe/bftm/)는 방향별 매핑, [PCC](https://www.loc.gov/aba/pcc/taskgroup/MARC-Simplification-for-BF-Conversion-final-report.pdf) 목적별 파생 MARC, [LC 도구](https://www.loc.gov/bibframe/news/bibframe-to-marc-conversion.html) 이중입력 부담, [XSL 구현](https://github.com/lcnetdev/marc2bibframe2) localfields false, 001 idfield, 880/$6 연결 미시도, split 및 중복 위험, 테스트 기대 assertion. 실제 동일 레코드 필드별 수용 결과를 읽은 시험 0. 필드 수·리소스 수·관계 보존이 다르다는 경쟁 설명은 가능하나 동일 필드 실험을 대신하지 않는다. 원저자 참고문헌 보충 R14–16은 목록 순 3건 탐색, 적격 첫 2 시험 아직 0/2(공개 입력/출력 미확인), 원목록은 G 참고문헌 첫 부분 Azhar/Baik/Barbini까지 확인; 다음 순서 유지.

## Q7. 반환 문장과 최소 질문

“보기만 하면 됩니까, 지정 속성을 재사용해야 합니까, 아니면 편집 후 원래 도구로 되돌아가야 합니까?” 속성/복귀라면 어느 객체·값(단위/관계 포함)과 두 제품 버전·옵션인지 묻는다. 사양 링크는 표현 범위, 양 구현 링크는 경로 설정, 동일 입력-결과 시험 링크는 특정 조합의 실증을 반환. 마지막이 없으면 조건부 또는 보류. 사용자에게 동일 도구쌍이라도 방향과 목적별 문장을 달리 반환할 수 있다. advice.csv의 필요한 입력 그대로 사용.

## 조건부 대안 및 추가 분석

- 원 작성자: 원본 식별과 저작 의도가 성공. 수신 사용자: 시각 확인/편집/수치 중 필요한 것 성공. 시험 주최자: 고정 판과 동일 실험 키·측정 정의. 보존 담당: 원자료 보관, 실제 인수 검증과 허용된 파생물 손실. 네 정의를 합치지 않는다.
- 설명 A: 구현과 프로필에 따라 일부 의미가 손실된다. 경쟁 B: 같은 의미를 다른 entity/class, 단위 환산, 참조 범위로 나타낸 결과일 뿐이다. G 누락·빈 모델은 A의 위험을 뒷받침하지만 단위 누락/벽 치환이 실제 의미 손실인지는 B와 구분하지 못한다. S 양방향 차이는 A를 지지하나 두 native 모델 및 MVD 불일치는 B(입력 차이) 가능성. S 참조 블록과 AV MPEG2는 의도된 범위가 다른 결과를 설명하는 실제 반례. MARC nac/ignore도 의도된 손실 가능성. 같은 객체·판·입력 해시·실제 수신값을 요청하는 것이 두 설명을 가르는 최소 관측.
- 단방향 참조+native 원본 유지, 필요한 속성만 명시한 별도 정규화 매핑, 완전 왕복 전 검증의 세 정책은 사용자 목적에 따라 후보. 제품 DB/검색/Studio 연동 선택은 하지 않는다.
- 하한 점검: 57 source rows, 23 unique substantive work IDs(재열람/목록 제외); 원 연구 3(+공개 시험 자격 미확인 보충 연구 3), 파일 내용 0/6, 역사판 계열 문서 3/6(정확 두 제품 subversion 옵션 0), AV 3개 work의 보고 4 프로젝트이나 엄격 동일 파일 수용 0/3, MARC 6개 work이지만 동일 필드 수용 0/3. 문서 수 하한만 넘겼고 요구 층별 하한·핵심 8자리 판독은 미충족. 주 관측 계보 2, 폭넓은 기관·보충 실측 보고 계보 후보 10(같은 G 설계/결과는 하나; FADGI 내 두 프로젝트는 둘; 규격/도구문서는 계보 실측 아님). 직접 실험/변환 없음. 자기 판정 PARTIAL.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사·원자료 | 결론이 바뀌는 관측 |
|---|---|---|---|
| G 본문 7/16 vs 원면 14열, 파일 후보만 연결 | 어떤 제품/판에서 단위·객체 손실인지 | [v2 reports](https://zenodo.org/records/6470370), [ZIP](https://zenodo.org/records/3964368), 원 Myran 승인된 접근 | 설문 ID–파일–정확 원본 hash를 조인하고 단위 객체/환산량 비교 |
| S SAV/CV2.0 충돌, separate native, E/P 정성 등급 | RFEM↔SAP의 하중 재사용 및 왕복 | [원보고 §5.2/Table7](https://www.mdpi.com/2076-3417/11/23/11430), 원 입력·출력 및 양 버전 옵션/로그 | 동일 대상·부호·단위의 수신 실제값 및 A 재수입 확인 |
| AV/MARC 개별 수용값 및 적격 보충 시험 부족 | 일반화, 22층 하한 및 동수·다른 값 반례 | [FADGI](https://www.digitizationguidelines.gov/guidelines/FADGI_BDV_p2_20140908.pdf), [LC pilot](https://www.loc.gov/bibframe/docs/pdf/bibframe-pilot-phase1-analysis.pdf), G 원 참고문헌 순서 | 공개 동일 원본/출력 키와 필드·관계·기대·실제 수용값, 독립 두 시험 확보 |
