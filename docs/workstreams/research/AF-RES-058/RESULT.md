# AF-RES-058 · 같은 권고의 설명과 정오별 최종 선택 — PARTIAL

## 표 1. 여덟 고정 연구 자리

| 연구·층·배정 단위 | 원과제·조건 N | 같은 후보·순위·권고의 증거 | 설명의 차이·원 자극 주소 | 정답 원천 | 최종 응답 원천·연결 수 | 가능한 해석·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| A01 · A · Ramos 등, SIGIR2020 · 사람 간, 무작위 절차 미보고 | 항공 문서 검색·선택 후 quiz; T/TA/TAB 각 완료자50, 최초 배정 N 미확인 | 같은 BM25 방법진술. Fig1(TAB)/Fig5(TA)의 query·첫2제목은 같음; Fig4(T)는 query·둘째 결과 다름. 실제 impression ID·순위 미확인(EU/예시 한정 관측) | T 제목 / TA 초록 / TAB 초록+단어 기여 막대·hover 숫자. [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) Fig1/4/5; [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) SearchBar.js | Cranfield query002 qrel25행 회수; −1·이진 relevance 기준 미확인. quiz키는 문서 권고 참값과 다름. [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz) | 고정 패키지 bookmark559/quiz459/exit67행. 같은 batch 익명 exit ID67 연결; 조건·150완료자 대응·최종 문서 노출 D 미확인. [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) | J3/JU: 신뢰·quiz 성과를 정오별 수락으로 전환 불가. HEAD의 지시/재시도/길이 차이가 당시 개입인지는 미확인 |
| A02 · A · Search Result Presentation for Non-Native Language Documents, IUI Companion2024 · 사람 안 과제/화면(정확 배정 미확인) | 비모국어 문서10개 중 관련 문서 선택; A–F 여섯 화면, N 미확인 | 같은 예시 제목·저자·URL의 A–F를 실제 확인. 전체 후보10·순위·과제별 권고 대응표 미확인(EU) | A 기본; B 번역 snippet; C/D 오른쪽 원어/번역 keyphrase; E/F 아래 원어/번역 keyphrase. [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf) 여섯 화면 | 관련 문서 하나를 찾도록 요청; 유일한 정답인지·전문가/사전 key·복수정답 규칙 미확인 | 저자 poster의 평균/요약만, 정식 본문403; 최종 선택 원행·결측 미확보 | J3/JU: 번역·정보량·배치가 함께 바뀜. poster를 정식 원논문 직접 읽음으로 계산하지 않음 |
| A03 · A · 미충원 | 미실시 — 선정 연구 없음 | 해당 없음 — 연구 없음 | 해당 없음 — 연구 없음 | 해당 없음 — 연구 없음 | 미실시 — 연구 없음 | 앞선 방법 접근 미확인 때문에 최초4개 복원 미완료; 음성 결과0이 아님 |
| A04 · A · 미충원 | 미실시 — 선정 연구 없음 | 해당 없음 — 연구 없음 | 해당 없음 — 연구 없음 | 해당 없음 — 연구 없음 | 미실시 — 연구 없음 | 다른 층/진단 연구로 빈자리를 메우지 않음 |
| B01 · B · Panigutti 등, CHI2022 · 사람 안 2과제, 순서 배정 | 미래 MI 확률 초기/최종 추정; Dr.AI/Dr.XAI; 모집31−주의1−초기100 두 명=분석28 | 권고 A=100은 모두 동일·맞음이라는 방법(E2). 서로 다른 유사 환자2명, item 동일성 EU; 연속 응답이라 후보 순위 해당 없음 | 진단 dot·반사실 조건 강조·요약 규칙·hover. [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf) §3.3–3.5/Fig1–2; 캡션·본문만 판독, 픽셀 미확인 | 두 환자 미래 MI 양성은 저자 진술; 독립 환자key 미확인. 위험확률 답의 이산 정답 규약 부재 | WOA 중앙값 .31 vs0만; 최종 F=100 정수 횟수 미확인. 오권고는 설계상0 | J3/J4: 절댓값 WOA/판단 변경 크기와 최종 수락은 다름. 오권고 거절 효과는 해당 없음; 다른 환자·hover 동시 변화 |
| B02 · B · Schemmer 등, IUI2023 · 사람 간 무작위 | 호텔 리뷰 fake/genuine: 초기 답→AI→최종 답. 모집200−1=199; Control100/Feature99, 16시행/인 | 32 pool에서 16개, TP/FP/TN/FN 각4라는 방법(E2); 조건별 itemID·완전 자극 쌍 미확인 | LIME 단어 강조와 같은 AI권고. [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) Fig5(PDF11): 초기/지원후 화면 쌍, control/feature 렌더쌍 아님 | Ott2011/2013: 고용된 허위 리뷰와 사이트에서 채집한 실제로 간주한 리뷰; 숙박 진위 독립검증 아님. [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf) | Table3 RAIR/RSR·정확도 평균; 원응답 공동표 미확보. §6.3 no missing은 SEM 맥락 | J3: 초기 불일치 부분분모를 전체 정오수락 분모로 쓸 수 없음. v3 확인; 정정 VoR 전문 미확인 |
| B03 · B · Schoeffer 등, CHI2024 · 사람 간3군 무작위 | bio 직업 professor/teacher; N600 동수배정→계획200/군. baseline/task-relevant/gendered, 14판단/인 | 같은14 bio·같은 binary 예측은 방법(E2); Fig1 두 설명의 같은 bio/권고만 관측. 실제로 서로 다른543/214특징 모델, F1 .87/.77 | 단어 강조·색 있는 권고; baseline은 강조/색 없음. [AD-M26](https://arxiv.org/pdf/2209.11812v5) Fig1(PDF5), AppendixA/B; 모델확률은 화면 미표시 | BIOS 첫문장 직업명 추출·정규화, 이후 첫문장 제거. 선택14개 원ID 미확인; 실제 자격 검증 아님. [AD-BIOS-P](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/bios_bias.pdf) | Fig3/5 비율만. Table1 정8/오6과 그림 정권고 몫50%가 불일치; 포함/가중 규칙·원행 미확보 | J3: 분모를12로 추정하지 않음. EAAMO2023/arXiv 개정은 같은 계보이며 독립 연구로 추가 안 함 |
| B04 · B · Kayser 등, EMNLP2024 · 사람 안4블록, 순서 배정 | Xray finding: Not/Maybe/Definitely present; 포함85, 조건별20, None/SM/NLE/Combined | 같은80이미지·모델 권고, 조건별 균등 빈도/70% 정답은 방법(E2). 할당ID 미확인; 같은 모델을4개 모델처럼 표기 | GradCAM / 자연어 이유 / 둘 다 / 없음. [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) Fig2·Fig15 화면 확인; 같은 None/Combined 쌍은 미확인 | 3방사선 전문의가160사례 사전 채점, 그중80선정; Maybe+Definitely 양성. Not/Definitely 충돌 제외; 설명7점은 별도 변수 | Fig6 GLMM 예측률; 응답·배정·전문가 key 원행 미확보. 연결 GitHub는 README1개뿐 | J3-model: 계획1190/510을 관측 D로 쓰지 않음. NLE−None 오수락+6.3pp는 모형 기술차; 실제 읽기/원문 링크 효과 아님 |

## 표 2. 조건별 정오층·대비·결측 원장

| 연구·조건·대비 | 맞는/틀린 권고 | 배정·판정 가능·결측 분모 | 권고 수락 수/분모 | 최종 정답 수/분모 | 조건 간 차이·가능 범위 | 원행/저자 집계/미확인 | 근거 주소·표·열 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A01 · T (O001) | 맞는 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 1 |
| A01 · T (O002) | 틀린 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 2 |
| A01 · TA (O003) | 맞는 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 3 |
| A01 · TA (O004) | 틀린 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 4 |
| A01 · TAB (O005) | 맞는 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 5 |
| A01 · TAB (O006) | 틀린 권고 | 완료50/군; 배정N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 6 |
| A01 · TAB−TA (C001) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 1 |
| A01 · TAB−TA (C002) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 2 |
| A01 · TAB−T (C003) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 3 |
| A01 · TAB−T (C004) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 4 |
| A01 · TA−T (C005) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 5 |
| A01 · TA−T (C006) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S24](https://health-nlp.com/files/pubs/sigir20.pdf) [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S33](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/contrasts.json / 6 |
| A01 · T 결측 (O165) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함;150−67을 결측으로 계산 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 1 |
| A01 · TA 결측 (O166) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함;150−67을 결측으로 계산 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 3 |
| A01 · TAB 결측 (O167) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함;150−67을 결측으로 계산 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S31](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429) [SW-S32](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429/client/data) [SW-S34](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz); streams/software/outcomes.json / 5 |
| A02 · A (O007) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 7 |
| A02 · A (O008) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 8 |
| A02 · B (O009) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 9 |
| A02 · B (O010) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 10 |
| A02 · C (O011) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 11 |
| A02 · C (O012) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 12 |
| A02 · D (O013) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 13 |
| A02 · D (O014) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 14 |
| A02 · E (O015) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 15 |
| A02 · E (O016) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 16 |
| A02 · F (O017) | 맞는 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 17 |
| A02 · F (O018) | 틀린 권고 | 사람N 미확인; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 미확인 — 자료가 주는 범위 없음 | JU/J3; 원분자/분모 미확인 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 18 |
| A02 · B−A (C007) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 7 |
| A02 · B−A (C008) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 8 |
| A02 · C−A (C009) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 9 |
| A02 · C−A (C010) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 10 |
| A02 · D−A (C011) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 11 |
| A02 · D−A (C012) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 12 |
| A02 · E−A (C013) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 13 |
| A02 · E−A (C014) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 14 |
| A02 · F−A (C015) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 15 |
| A02 · F−A (C016) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | unidentified | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/contrasts.json / 16 |
| A02 · A 결측 (O168) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 7 |
| A02 · B 결측 (O169) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 9 |
| A02 · C 결측 (O170) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 11 |
| A02 · D 결측 (O171) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 13 |
| A02 · E 결측 (O172) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 15 |
| A02 · F 결측 (O173) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [SW-S28](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf); streams/software/outcomes.json / 17 |
| A03 · 미실시 (O019) | 맞는 권고 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv); SCOPE §2 |
| A03 · 미실시 (O020) | 틀린 권고 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv); SCOPE §2 |
| A03 · 결측 (O174) | 미실시 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv) |
| A04 · 미실시 (O021) | 맞는 권고 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv); SCOPE §2 |
| A04 · 미실시 (O022) | 틀린 권고 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv); SCOPE §2 |
| A04 · 결측 (O175) | 미실시 | 해당 없음 — 연구 없음 | 해당 없음 | 해당 없음 | 해당 없음 | 미실시 | [frame.csv](frame.csv) |
| B01 · Dr.AI (O023) | 맞는 권고 | 모집31/분석28, 사람 안; 계획D=28; 판정D·결측m 미확인 | 미확인/미확인 | 원 이산 정답 종점 부재 | WOA 중앙값은 수락 비율 아님 | J3 (WOA 주변통계); AF 최종정확도 기준은 J4; 원분자/분모 미확인 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 1 |
| B01 · Dr.AI (O024) | 틀린 권고 | 설계상 오권고0; 관측응답 분모라는 뜻 아님 | 해당 없음 — 설계상0 | 해당 없음 — 설계상0 | 해당 없음 — 비교할 오권고 없음 | J3 (WOA 주변통계); AF 최종정확도 기준은 J4; 원분자/분모 미확인 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 2 |
| B01 · Dr.XAI (O025) | 맞는 권고 | 모집31/분석28, 사람 안; 계획D=28; 판정D·결측m 미확인 | 미확인/미확인 | 원 이산 정답 종점 부재 | WOA 중앙값은 수락 비율 아님 | J3 (WOA 주변통계); AF 최종정확도 기준은 J4; 원분자/분모 미확인 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 3 |
| B01 · Dr.XAI (O026) | 틀린 권고 | 설계상 오권고0; 관측응답 분모라는 뜻 아님 | 해당 없음 — 설계상0 | 해당 없음 — 설계상0 | 해당 없음 — 비교할 오권고 없음 | J3 (WOA 주변통계); AF 최종정확도 기준은 J4; 원분자/분모 미확인 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 4 |
| B01 · Dr.XAI−Dr.AI (C021) | 맞는 권고만·별도 WOA | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | WOA 중앙값 .31−0=.31; 수락률 차이 아님 | J3; alternateendpoint | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/contrasts.json / 5 |
| B01 · Dr.XAI−Dr.AI (C029) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3/J4 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); 통합 정의 / C029 |
| B01 · Dr.XAI−Dr.AI (C031) | 틀린 권고 | 해당 없음 — 설계상 오권고0 | 해당 없음 — 설계상0 | 해당 없음 — 설계상0 | 해당 없음 | J3/J4 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); 통합 정의 / C031 |
| B01 · Dr.AI 결측 (O176) | 정오 미배분 | 저자 사람 제외3(주의1/초기일치2); 원시행 결측·정오별 배분 미확인 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 1 |
| B01 · Dr.XAI 결측 (O177) | 정오 미배분 | 저자 사람 제외3(주의1/초기일치2); 원시행 결측·정오별 배분 미확인 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M12](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf); streams/adjacent/outcomes.json / 3 |
| B02 · Control (O041) | 맞는 권고 | 분석100명; 계획D=800; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | RAIR/RSR 부분분모와 구별; 조건차 미확인 | J3; 원분자/분모 미확인 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B02 · Control (O042) | 틀린 권고 | 분석100명; 계획D=800; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | RAIR/RSR 부분분모와 구별; 조건차 미확인 | J3; 원분자/분모 미확인 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B02 · Feature (O043) | 맞는 권고 | 분석99명; 계획D=792; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | RAIR/RSR 부분분모와 구별; 조건차 미확인 | J3; 원분자/분모 미확인 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B02 · Feature (O044) | 틀린 권고 | 분석99명; 계획D=792; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | RAIR/RSR 부분분모와 구별; 조건차 미확인 | J3; 원분자/분모 미확인 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B02 · Feature−Control (C030) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452); 통합 정의 / C030 |
| B02 · Feature−Control (C032) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452); 통합 정의 / C032 |
| B02 · Control 결측 (O185) | 정오 미배분 | Feature 사람 제외1; SEM자료 결측0 저자진술과 원배정 응답 결측 미확인을 구별 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B02 · Feature 결측 (O186) | 정오 미배분 | Feature 사람 제외1; SEM자료 결측0 저자진술과 원배정 응답 결측 미확인을 구별 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [RT-SCH-P](https://publikationen.bibliothek.kit.edu/1000158077/150613452) [RT-OTT11-P](https://aclanthology.org/P11-1032.pdf) [RT-OTT13-P](https://aclanthology.org/N13-1053.pdf); streams/root/schemmer-ott-notes.md / Table3 audit |
| B03 · baseline (O027) | 맞는 권고 | 계획200/군; 실제군N 미확인; 계획D=1600; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 5 |
| B03 · baseline (O028) | 틀린 권고 | 계획200/군; 실제군N 미확인; 계획D=1200; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 6 |
| B03 · task-relevant (O029) | 맞는 권고 | 계획200/군; 실제군N 미확인; 계획D=1600; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 7 |
| B03 · task-relevant (O030) | 틀린 권고 | 계획200/군; 실제군N 미확인; 계획D=1200; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 8 |
| B03 · gendered (O031) | 맞는 권고 | 계획200/군; 실제군N 미확인; 계획D=1600; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 9 |
| B03 · gendered (O032) | 틀린 권고 | 계획200/군; 실제군N 미확인; 계획D=1200; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 그림 분모 충돌; 원개수·범위 미확인 | J3; 원분자/분모 미확인 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 10 |
| B03 · task-relevant−baseline (C017) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/contrasts.json / 1 |
| B03 · task-relevant−baseline (C018) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/contrasts.json / 2 |
| B03 · gendered−baseline (C019) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/contrasts.json / 3 |
| B03 · gendered−baseline (C020) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 미확인 — 원개수 차이·자료 기반 범위 없음 | J3 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/contrasts.json / 4 |
| B03 · baseline 결측 (O178) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 5 |
| B03 · task-relevant 결측 (O179) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 7 |
| B03 · gendered 결측 (O180) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M26](https://arxiv.org/pdf/2209.11812v5); streams/adjacent/outcomes.json / 9 |
| B04 · None (O033) | 맞는 권고 | 포함85, 사람 안; 계획D=1190; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락73.8%, 정확도73.8%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 11 |
| B04 · None (O034) | 틀린 권고 | 포함85, 사람 안; 계획D=510; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락47.3%, 정확도52.7%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 12 |
| B04 · SM (O035) | 맞는 권고 | 포함85, 사람 안; 계획D=1190; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락71.4%, 정확도71.4%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 13 |
| B04 · SM (O036) | 틀린 권고 | 포함85, 사람 안; 계획D=510; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락46.9%, 정확도53.1%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 14 |
| B04 · NLE (O037) | 맞는 권고 | 포함85, 사람 안; 계획D=1190; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락74.5%, 정확도74.5%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 15 |
| B04 · NLE (O038) | 틀린 권고 | 포함85, 사람 안; 계획D=510; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락53.6%, 정확도46.4%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 16 |
| B04 · Combined (O039) | 맞는 권고 | 포함85, 사람 안; 계획D=1190; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락72.3%, 정확도72.3%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 17 |
| B04 · Combined (O040) | 틀린 권고 | 포함85, 사람 안; 계획D=510; 판정D·결측m 미확인 | 미확인/미확인 | 미확인/미확인 | 참고 모형 수락46.3%, 정확도53.7%; 원개수 아님 | J3-model; 원분자/분모 미확인 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 18 |
| B04 · SM−None (C022) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 -2.4pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 6 |
| B04 · SM−None (C023) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 -0.4pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 7 |
| B04 · NLE−None (C024) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 +0.7pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 8 |
| B04 · NLE−None (C025) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 +6.3pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 9 |
| B04 · Combined−None (C026) | 맞는 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 -1.5pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 10 |
| B04 · Combined−None (C027) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 -1pp; 원개수 차이 아님; 새 유의성 주장 없음 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 11 |
| B04 · NLE−None / 높은 설명품질 하위군 (C028) | 틀린 권고 | 미확인 — 공통 판정 분모 미확인 | 미확인 (양 조건 A/D) | 미확인 (양 조건 C/D) | 모형 기술차 +10.1pp; 원개수 차이 아님; 분할 기준 다름·동일 항목 구성 미확인/BH 유의표시 소실 | J3-model | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf); streams/adjacent/contrasts.json / 12 |
| B04 · None 결측 (O181) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함; 시간분석만 제외5.1%를 여기 전용 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 11 |
| B04 · SM 결측 (O182) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함; 시간분석만 제외5.1%를 여기 전용 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 13 |
| B04 · NLE 결측 (O183) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함; 시간분석만 제외5.1%를 여기 전용 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 15 |
| B04 · Combined 결측 (O184) | 정오 미배분 | 원배정 대비 건너뜀·철회·미연결 m 미확인; 정오층에 배분 안 함; 시간분석만 제외5.1%를 여기 전용 안 함 | 미확인 | 미확인 | m 미확인으로 보완 범위 미계산 | 결측 원행 미확보 | [AD-M30](https://aclanthology.org/2024.emnlp-main.1051.pdf) [AD-FOOL-PKG](https://github.com/maximek3/fool-me-once/tree/2a945776782d48403da0d36f56b25d44a43f1af3); streams/adjacent/outcomes.json / 17 |

<!-- END_REQUIRED_TABLES -->

## 판정과 읽는 법

**연구 상태: PARTIAL.** 고정된 여덟 자리의 표는 모두 만들었으나 실제 선정은 A층2개·B층4개이고 A03/A04는 미충원이다. 선정 연구의 정오별 수락 원개수를 연결해 낸 셀은 **0개**다. 이는 참여자0명·설명 효과0·오권고 수락0이라는 뜻이 아니다. 독립된 진단층에서는 D01/D04의 공개 응답 기록으로 정오별 수락과 최종 정답을 복원했다. 이들을 빈 선정 자리에 넣지 않았다. 수치가 없는 칸은 이유와 다음 최소 입력을 [reproduce.md](reproduce.md), [outcomes.csv](outcomes.csv)에 남겼다.

현재 제품에 돌려줄 수 있는 결론은 **설명 제공 조건에서 맞는 권고 수락과 틀린 권고 수락이 함께 높게 관측된 사례가 있고, 전체 정확도 상승만으로 오류 선별 개선을 판정할 수 없다는 것**이다. 동시에, 오류를 검증하는 부담을 줄이는 설명이 특정 과제의 과잉 수락을 낮춘 독립 실험도 있다. 따라서 효과 방향을 설명의 존재 하나로 일반화하지 않는다. 아래 Q5의 D04 원개수, Q6의 D06 반례, Q7의 조건부 설계 대안이 이 판단의 직접 근거다.

표의 N은 사람 수, D는 정오를 판정할 수 있는 권고 시행 수, A는 최종 답=권고, C는 최종 답=정답이다. 사람 수×설계 시행수는 **계획 D**로만 표기했다. `미확인`은 자료가 부족한 것, `관측0`은 실제 관측 파일에서 센0, `해당 없음`은 그 종점의 분모가 정의되지 않는 것, `미실시`는 선정 연구 자체가 없는 것을 뜻한다. `미확인/미확인`은 정수 분자·분모를 회수하지 못했다는 뜻이다. 모든 차이는 개입−대조이며 pp는 퍼센트포인트다.

동일성 E1은 항목별 자극·키로 확인, E2는 방법에만 명시, EU는 미확인이다. **한 예시의 E1은 전체 배정의 E1이 아니다.** 결과 등급 J1은 같은 공개 원행에서 연결한 값, J2는 저자가 명시한 교차 원개수, J3는 주변수·그림·모형 평균, J4는 원래 종점 부재, JU는 확인 자료 부족이다. 이번 주 질문에 J2로 쓸 선정 연구의 교차 원개수는 확보하지 못했다. B04의 J3-model은 원개수와 엄격히 분리했다.

### 모집·자료 배당·결과 노출

시작판은 `3f4d43b19cd76d56983e6f500eebe7010eb3fa51`이다. 계획 당시 SHA와 다르며 실제 시작판을 [manifest.json](manifest.json)에 기록했다. [SCOPE.md](SCOPE.md)의 R0/R1을 결과표 열람 전에 원격 커밋하고, 이어 발견 메타데이터와 방법 선정을 각각 고정했다. 정확한 질의·필터·UTC·정렬·페이지 한도·재시도·스니펫 노출은 각 stream의 search-log와 [evidence/commits.csv](evidence/commits.csv)에 있다. Crossref는 발견 수단이며 논문 실측 근거가 아니다.

발견 합집합에서 A547/B406 고유 DOI를 얻었고 venue·연도·주제 메타데이터 기준을 적용한 A32/B39 중 발행일·DOI 순으로 각30개 방법을 검토했다. A01은 원순번24, A02는28, B01/B02/B03/B04는12/20/26/30이다. ACM403·ACL 검색 shell 때문에 사전 지정 웹 검색 보완을 사용했으며 native 전수 목록과 동등하다고 보지 않는다. 현재 조사 범위의 최초 적격 후보를 보존한 것이며 세계 전체의 최초 네 연구라는 주장은 아니다. [frame.csv](frame.csv)의 순번·결격·접근 범위가 판단 근거다.

A의 방법 미확인7개 중 후속에 원문2개를 열어 부적격임을 확인했다. 미확인5개(원순번7/8/9/22/26)와 원순번15의 main-paper 방법을 demo로 대신 읽은 한계가 남았다. 고정된 선정표를 소급 바꾸지 않고 `streams/software/methods-sensitivity.json`에 정정했다. B의 앞선 제외4건은 공식 초록/방법 요약까지만 확인해 전문 기준의 제외 확실성이 낮다. 결과·정답키·공개 데이터 성공을 기준으로 연구를 바꾸지 않았지만 **선정 완전성 자체는 미확인**이다. 진단층의 인용 추적을 주 모집 성공으로 계산하지 않는다.

| 자료군 | 목표 | 적격 심층 실측 | 판정과 경계 |
| --- | ---: | ---: | --- |
| 선정 사람 실험 원논문 | 8 | 정식 원논문5; A02 저자 poster1 별도 | 미달. A03/A04 미충원, A02 정식 본문 미독 |
| 별도 발행 자극·실험 도구·프로토콜 | 4 | 엄격한 독립 프로토콜 계보2 | 미달. Poursabzi 등록과 Vasconcelos 등록 계보. 후자의3등록을1로 보수 집계 |
| 저자 데이터/분석 패키지 | 4 | 4 | 충족: A01, D01, D03, D04. README/CSV/노트북을 따로 세지 않음 |
| 반대·복제·다른 분야 독립 사람 실험 | 4 | 7 논문 계보(D01–D07) | 수량 충족. 동일 논문의 실험·재사용 참가자·개정판은 독립 추가 수가 아님 |
| 정답 원천·보조 데이터 | 별도 보고 | 6 | Ott 두 원논문+데이터, BIOS 논문, MIMIC-NLE 논문, Cranfield. 주 실험8개를 대신하지 않음 |
| 모델·원천 도구 지원 | 별도 보고 | 3 | DrXAI, BIOS, MIMIC-NLE 저장소. 인간 응답/배정 패키지가 아니므로 프로토콜 목표를 채우는 데 쓰지 않음 |
| 고유 외부 심층 1차 저작 | 최소20 | **28** | 총수 충족. 선별 방법만 읽은 저작을 포함한49와 구별; 검색·실패·내부파일·자가생성 진단 제외 |

출처 기록109개를 계보로 묶었다. 28개 합계는 `5+1+2+4+7+6+3`이며 저작을 여러 자료군에 중복 배정하지 않았다. 같은 DOI의 저자 보고서·PDF/HTML·수정판, 같은 저장소의 코드·데이터, 같은 코호트의 재분석은 해당 계보 안에서만 기록했다. 각 자료의 URL·고정판/해시·UTC·읽은 절·확인 내용·한계·반대 출처는 [sources.jsonl](sources.jsonl), 계보별 목록은 [evidence/works.csv](evidence/works.csv)에 있다. 자료 수 충족으로 여덟 자리·식별성 부족을 덮지 않는다.

## Q1. 실제로 같게 유지한 것은 무엇인가?

**선정 연구 어느 것도 모든 배정 시행에서 후보·순위·권고·설명만의 차이를 한꺼번에 검증하지 못했다.** A01은 검색 엔진이 같다는 방법 문장과 두 예시 결과가 일치하는 것까지 확인했다. 그러나 참가자가 자유롭게 query를 바꾸며, T의 예시는 query와 둘째 결과부터 달랐다. 현재 저자 저장소는 TA/TAB의 bars on/off를 구현하지만 T의 당시 배포 경로는 회수하지 못했다. 저장소 HEAD의 재시도 경로·보상 설명·초록40단어 구현과 논문의50단어 서술 차이는 배포판 연결이 필요한 단서다. 이것을 당시 실험 오류가 확정된 것으로 쓰지 않았다. [SW-S24 Fig1/4/5](https://health-nlp.com/files/pubs/sigir20.pdf), [SW-S31 고정 코드](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429), [감사](streams/software/package-audit.json).

B01에서는 같은 AI 권고값100을 보여도 환자 두 명은 서로 다르다. B03에서는 같은 14개 bio에 같은 이진 예측을 고르도록 두 모델을 선별했지만 모델 자체는543특징/214특징으로 다르고, 권고의 색도 baseline과 달랐다. B04는 같은 모델과 각 이미지의 조건별 같은 빈도를 명시하지만 할당표가 없고, 참가자에게는 조건마다 다른 모델 일련번호를 제시했다. 이 차이는 설명·평판·기간 효과를 분리하는 데 필요하다. [AD-M12 §3.3](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf), [AD-M26 §3.2/AppendixB](https://arxiv.org/pdf/2209.11812v5), [AD-M30 AppendixD](https://aclanthology.org/2024.emnlp-main.1051.pdf).

진단층 D04에서는 공개 행에 들어 있는 동일한 리뷰 본문의 해시별 정답·AI 예측이 조건 간 일치함을 확인했다. 이것은 같은 모델이라는 말보다 강한 근거다. 다만 논문320개와 달리 고유 본문319개가 나오며 하나는 같은 본문으로 중복된다. 각 주요 조건에서318개 본문은5회, 나머지1개는10회로 나타나므로 원래 itemID가 없는 한 중복 문항인지 동일 텍스트의 별도 항목인지 모른다. 조건과 사람 키는 구별해 집계했고 이 행들을 임의로 합치거나 삭제하지 않았다. [DI-LAI-DATA](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285), [lai-audit.json](streams/diagnostics/lai-audit.json).

반대로 D03의 Fig1은 동일 아파트·동일 $1.6M 예측의 Clear2/BB2 화면을 확인할 수 있었으나 원 종점은 연속 가격 추정이다. 좋은 동일성 근거가 있어도 질문에 맞는 정오 수락 분모가 자동으로 생기지 않는다. 2특징/8특징 대조는 예측값까지 달라지는 비교다. [DI-POU-P Fig1](https://doi.org/10.1145/3411764.3445315), [저자 패키지](https://github.com/Foroughp/Manipulating-and-Measuring-Model-Interpretability).

## Q2. 근거에는 무엇이 들어 있었고 실제로 읽었는가?

설명 종류를 한 단어로 합치지 않았다. A01은 원문 초록·BM25 단어 기여 막대·hover 숫자이고 확률은 아니다. A02는 번역된 snippet와 keyphrase 및 위치 변경이다. B01은 요약 규칙·반사실 조건·hover 강조, B02/B03은 판정할 본문의 단어 강조, B04는 생성 이유 문장과 GradCAM이다. D01은 강조·서술·대안 설명과 신뢰도 표시, D04는 단어 강조나 예제, D06은 미로 경로, D07은 완전/부분적인 이유 표현이다. 원천의 문장·발췌·링크·숫자·예제·강조·선택 열람 여부는 [stimuli.csv](stimuli.csv)의 원 자극 주소와 details에 각각 보존했다.

실제 본 화면 쌍의 범위는 다음과 같다. 전체 실험 자극을 열었다고 확대하지 않는다.

| 사례·원 자극 | 직접 확인한 한 쌍 | 그 쌍만으로 확인하지 못한 것 |
| --- | --- | --- |
| A01 [Fig1/5](https://health-nlp.com/files/pubs/sigir20.pdf) | 같은 항공 query·첫 두 제목, TA와 TAB의 초록/막대 차이 | 모든 노출 후보·순위, T 포함 세 조건 배정, 당시 버전 |
| A02 [저자 poster](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf) | 같은 기계번역 논문 제목·URL의 A/B 및 C–F | 열 개 후보 전부·항목 배정·최종 선택 |
| B03 [Fig1](https://arxiv.org/pdf/2209.11812v5) | 같은 여성 bio·Professor 권고에 task-relevant/gendered 강조 | baseline 화면 쌍·14개 전체 mapping |
| D03 [논문 Fig1](https://www.jennwv.com/papers/manipulating.pdf)·[패키지](https://github.com/Foroughp/Manipulating-and-Measuring-Model-Interpretability) | 같은 아파트·$1.6M 예측의 Clear2/BB2 | 연속 오차를 정오 수락으로 바꿀 사전 기준 |
| D06 [Fig6 p12](https://cicl.stanford.edu/papers/vasconcelos2023explanations.pdf) | 같은25×25 미로·시작점·네 출구·권고D/정답A, 분홍 경로의 유무 | 이 그림은 medium 예시다. hard에서 나온 긍정 효과를 이 화면의 실측 효과라고 부르지 않음 |

B01 Fig1/2는 본문·캡션을 읽었으나 PDF 픽셀 취득이 실패했다. B02 Fig5는 한 사람의 지원 전/후 화면으로, 설명 없는 AI 조건과 설명 있는 AI 조건의 같은 항목 렌더 쌍은 아니다. B04 Fig2의 정오 권고×설명 품질 네 유형과 Fig15 Combined UI는 시각 확인했으나 같은 case의 None/Combined 화면 쌍은 회수하지 못했다. 이는 [각 출처의 read_status](sources.jsonl)에 반영했다.

**실제 외부 원문 링크 열람을 배정한 비교는 이번 확보 자료에서 확인하지 못했다.** A01의 제목은 내부 corpus 원문 뷰를 열고 A02의 문서 클릭은 참가자의 선택이다. B04의 instruction video 링크도 의료 근거 원문 링크가 아니다. D02의 OnDemand는 AI 도움 요청 버튼이어서 외부 문헌 열람의 배정으로 해석할 수 없다. 클릭한 사람만 비교하면 관심·능력·불신에 따른 자기선택이 섞인다. 화면 제공·hover 가능·강제 대기·초기 답 요구는 실제 읽음과 각각 구별했다. [DI-BUC-P §3–4](https://doi.org/10.1145/3449287), [A01 코드](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429).

현재 해석의 단위는 대체로 **설명을 제공하는 조건의 결과**다. 제공된 모든 설명을 읽었다거나, 읽은 것 자체가 수락을 바꿨다는 효과는 미확인이다. 같은 후보의 독립 원문 링크 열기만 배정하고 노출·최종 선택을 잇는 공개 자료가 나오면 이 제한이 바뀐다.

## Q3. ‘틀린 권고’의 참값은 누가 어떻게 만들었는가?

Q5의 수락은 각 연구가 사전에 정한 정답과 AI 답의 일치 여부에 따른다. 그것이 현실 세계의 완전한 참값이라는 주장은 별도다. 설명 문장의 오류, 사용자의 취향, 권고의 오류, 자신감 표현을 서로 다른 변수로 유지했다.

**검색 적합성.** A01의 query002와 Cranfield qrel을 직접 읽었다. 25개 관련도 행은 등급1:2, 2:5, 3:13, 4:4, −1:1이다. README는1을 가장 높은 관련성,4를 최소 관심으로 설명하지만 −1은 정의하지 않는다. 미등재 문서 전부를 오답으로 처리할 수 없고, 실험이 어떤 등급을 관련/비관련으로 이진화했는지도 미확인이다. 참가자 quiz의1/4/2/2 정답키는 문서 권고의 참값과 다르다. A02는 관련 문서 하나를 찾도록 요청하지만 유일한 정답이 있는지는 미확인이고 사전 전문가 key도 회수하지 못했다. [SW-S34 README/cran.qry/cranqrel](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz), [cranfield-audit.json](streams/software/cranfield-audit.json).

**리뷰 진위.** B02/D04의 계보는 Ott2011/2013으로 추적했다. 허위 리뷰는 작성자에게 만들도록 의뢰했고 실제로 간주한 리뷰는 TripAdvisor 등 사이트에서 조건에 맞게 채집했다. 2013 논문은 채집된 리뷰가 완벽한 gold standard는 아님을 인정한다. 실제 숙박 여부를 개별 검증한 자료로 부르지 않는다. 공식 2011 배포 패키지는800 positive 리뷰의 ID·텍스트 표현이고, later positive/negative 합본과 같은 자료라고 가정하지 않았다. 해당 레이블은 응답 전에 정해졌으며 참가자 사후 다수결로 만든 정답은 아니다. [RT-OTT11-P §3](https://aclanthology.org/P11-1032.pdf), [RT-OTT13-P §2](https://aclanthology.org/N13-1053.pdf), [RT-OTT-D](https://aclanthology.org/attachments/P11-1032.Datasets.zip).

**직업 분류.** B03의 BIOS 라벨은 bio 첫 문장의 직업명을 추출·정규화한 것이고 그 문장은 문제에서 제거한다. 실제 자격이나 현재 고용을 전문가가 검증한 참값이 아니다. 현실에서 professor와 teacher가 겹칠 수 있지만 실험은 두 레이블 중 하나를 요구한다. 선택된14개의 원ID와 라벨 행은 미확인이고 모델의 고확률과 정답도 별개다. [AD-BIOS-P §3–4](https://doi.org/10.1145/3287560.3287572), [AD-BIOS-PKG](https://github.com/microsoft/biosbias).

**의료 finding.** B04는 참가자 이전에 방사선 전문의3명이160개 case를 채점한 뒤80개를 고른다. Not present/Definitely present의 강한 충돌은 제외하되 Maybe 경계는 남기고, Maybe+Definitely를 양성으로 묶는다. 전문가 pairwise κ .451/.458/.502와 강한 충돌 제외 규칙을 함께 읽어야 한다. MIMIC-NLE 학습 데이터나 모델 출력으로 이 전문가 정답키를 대신하지 않았다. 설명의 임상 정확도7점과 권고 finding의 정오를 분리했기 때문에 **맞는 권고에 잘못된 근거** 또는 **틀린 권고에 그럴듯한 근거**가 동시에 가능하다. [AD-M30 §3.4/AppendixD.2–D.3](https://aclanthology.org/2024.emnlp-main.1051.pdf), [MIMIC-NLE 원논문](https://arxiv.org/abs/2207.04343).

진단층에서도 선을 유지했다. D06은 미로의 벽·경로·출구라는 생성 규칙으로 참값을 검증할 수 있지만 D03의 합성 outlier `actual_price=-1`은 실제 가격이 아니다. D02 음식 대체안은 탄수화물·flavor의 사전 점수 최적화에 따른 적합성이지 개인의 맛 선호 정답이 아니다. D07 문법 과제는 오류 **개수** 응답이며 교정문 전체의 품질과 다르다. [D06 원문 §4](https://cicl.stanford.edu/papers/vasconcelos2023explanations.pdf)·[등록](https://api.osf.io/v2/registrations/vp749/), [DI-POU-DATA](https://github.com/Foroughp/Manipulating-and-Measuring-Model-Interpretability), [DI-BUC-P](https://doi.org/10.1145/3449287), [DI-DEJ-P §4](https://nielsvanberkel.com/files/publications/cscw2025a.pdf).

## Q4. 권고 수락의 실제 시행을 어디까지 연결했는가?

A01은 공개 export가 없다는 결론에서 멈추지 않고 코드와5개 batch를 읽었다. bookmark snapshot559행/익명ID185종, quiz459행/ID165종, exit67행/ID67종이 있으며 exit의67ID 모두 같은 batch의 두 표와 연결된다. 일부 저장된 quiz 점수166행은 HEAD answerkey와166/166 일치했다. 그러나 조건 열·최초 노출 후보·순위·최종 삭제/철회 이벤트·논문의150완료자 대응이 없어 정오별 권고 수락으로 연결하지 않았다. 이67을 연구 참가자67명 또는 미응답83명으로 바꾸지 않는다. [SW-S32 고정 package](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429), [package-audit.json](streams/software/package-audit.json).

B02는 초기 자기 답을 실제로 수집한다는 점에서 목적에 가깝다. 하지만 RAIR은 ‘초기 인간 오답·AI 정답’에서 AI를 따라간 비율, RSR은 ‘초기 인간 정답·AI 오답’에서 자기 답을 지킨 비율이다. 초기부터 AI와 같은 답인 시행은 해당 부분분모에 들어가지 않는다. Table3의 Control/Feature RAIR29.59/38.87%, RSR71.87/69.45%를 전체 정권고/오권고 수락률로 대입하지 않았다. 평균 비율을 사람 수와 곱해 정수로 역산하지도 않았다. [RT-SCH-P §3.2 식1–3/Table3](https://publikationen.bibliothek.kit.edu/1000158077/150613452), [별도 표 재검토](streams/adjacent/self-review.md).

B01에서도 초기 답I=100인 두 명을 제외한 것은 `WOA=abs(F−I)/abs(A−I)`에서 분모가0이기 때문이다. 이 사람들을 단순 부주의나 설명 실패로 분류할 수 없다. 절댓값 WOA는 판단 변경의 크기이므로 증가만으로 권고 방향으로 이동했다는 보장도 없다. B04는 본 시험에서 독립 초기 답을 받지 않으므로 최종 동의가 원래 판단과 같았는지 권고로 바뀐 것인지 나누지 못한다. [AD-M12 §4.1](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf), [AD-M30 AppendixD](https://aclanthology.org/2024.emnlp-main.1051.pdf).

진단층 D01/D04는 같은 응답 행에 정답·권고·최종 답이 있어 공동표를 직접 만들 수 있다. D01의 `assignmentId/questionId/task/condition`에는 모호한 중복200키·400행이 있어 원기록 분석과 모호키 전부 제외 감도를 분리했다. D04의 조건·사람·시행 키는 중복되지 않았다. 개인 행을 저장소에 재게시하지 않고 입력 SHA·스키마·집계·재현 코드를 남겼다. 자료 내부의 핵심 답 결측0은 실제 관측이지만 **전체 원배정 대비 중단/탈락0**으로 일반화하지 않았다. [입력 영수증](streams/diagnostics/input-receipt.json), [집계 코드](streams/diagnostics/reproduce_diagnostics.py), [outcomes.csv](outcomes.csv).

## Q5. 맞는 권고와 틀린 권고의 수락은 각각 어떻게 달라졌는가?

선정 연구의 원개수 대비는 모두 미확인이다. B01은 애초 오권고를 넣지 않았고, B03은 분모가 충돌하며, B04는 모형 평균만 확인했다. 이 결과를 설명 무효로 해석하지 않는다. 아래는 주 모집과 별도인 **진단층의 공개 원행 관측**이다. 숫자는 해당 공개 분석 파일의 기록 수이며 전체 모집단·원배정의 무결측 효과가 아니다.

| 연구·과제·조건 | 권고 정오 | 판정 가능 D | 권고 수락 A/D | 최종 정답 C/D | 제3 오답 | 개입−대조 수락 차이 | 근거 |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| D04 리뷰 · machine | 맞음 | 1,395 | 908/1,395 | 908/1,395 | 해당 없음 | 대조 | DI-LAI-DATA, `actual_label/predicted_label/user_label` |
| D04 리뷰 · machine_and_heatmap | 맞음 | 1,395 | 1,107/1,395 | 1,107/1,395 | 해당 없음 | +14.2652pp | 같은 원행·분모 |
| D04 리뷰 · machine | 틀림 | 205 | 123/205 | 82/205 | 관측0 | 대조 | 같은 파일 |
| D04 리뷰 · machine_and_heatmap | 틀림 | 205 | 152/205 | 53/205 | 관측0 | +14.1463pp | 같은 원행·분모 |
| D01 Amazon · Conf. | 맞음 | 3,864 | 3,690/3,864 | 3,690/3,864 | 해당 없음 | 대조 | DI-BAN-DATA, `task/condition/pred/y/choice` |
| D01 Amazon · Conf.+Single | 맞음 | 3,822 | 3,669/3,822 | 3,669/3,822 | 해당 없음 | +0.5000pp | 저자 필터 분석파일 |
| D01 Amazon · Conf. | 틀림 | 736 | 256/736 | 480/736 | 관측0 | 대조 | 같은 파일 |
| D01 Amazon · Conf.+Single | 틀림 | 728 | 220/728 | 508/728 | 관측0 | −4.5628pp | 같은 파일 |
| D01 LSAT · Conf. | 맞음 | 1,326 | 1,086/1,326 | 1,086/1,326 | 해당 없음 | 대조 | 같은 파일 |
| D01 LSAT · Conf.+Single | 맞음 | 1,313 | 1,094/1,313 | 1,094/1,313 | 해당 없음 | +1.4202pp | 같은 파일 |
| D01 LSAT · Conf. | 틀림 | 714 | 331/714 | 338/714 | 45 | 대조 | 같은 파일 |
| D01 LSAT · Conf.+Single | 틀림 | 707 | 358/707 | 300/707 | 49 | +4.2779pp | 같은 파일 |

출처는 [D04 고정패키지](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285)와 [D01 고정패키지](https://github.com/uw-hai/Complementary-Performance/tree/6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f)다. 다른 조건 대비와 모호키 제외 감도는 [contrasts.csv](contrasts.csv)에, 필터 전후6대비는 [sensitivities-prefilter.json](streams/diagnostics/sensitivities-prefilter.json)에 따로 있다. Conf.+Single은 신뢰도에 단일 설명을 더한 실제 조건명이며, D04 machine_and_heatmap은 별도의 무권고 heatmap 조건과 다르다. 해당 CSV의52개 관측 수락 대비는 같은 과제의 여러 조건 및 분석 집합을 포함하며52개 독립 연구가 아니다. 새로운 군집 무시 검정은 하지 않았다. D04 본문은 사람 간 조건 배정을 명시하지만 무작위화 절차와 원배정 명부는 확인하지 못했으므로 이 표는 기술 비교이며 설명의 인과 효과를 확정하지 않는다.

분모부터 손검산한 D04는 각 조건80사람키×20=1,600행, 정권고1,395+오권고205=1,600이다. 전체 최종 정답은 대조908+82=990, 강조1,107+53=1,160이므로 **정확도61.875%→72.5%, 오권고 수락60%→74.1463%**다. 저자 Fig3/4의 반올림된61.9/72.5와60/74.1도 맞는다. root가 별도 코드로 네 셀을 다시 세었고 [실행 결과](streams/root/independent-calculation.json)를 남겼다. [원논문 v4 Fig3/4](https://arxiv.org/pdf/1811.07901v4).

여기서 ‘오류 선별이 나빠졌다’는 표현은 **오권고 거절률이40%→25.8537%로 내려갔다**는 뜻에 한정한다. 정권고 수락도65.0896%→79.3548%로 오르므로 모든 차별·교정 지표가 악화됐다는 결론은 아니다. 같은 정오 혼합비에서 전체 정확도와 오권고 거절 방향이 갈릴 수 있다는 반례다. D01 Amazon의 음의 오수락 차이는 설명이 언제나 과잉 수락을 만든다는 반대 주장도 막는다.

B04 Fig6의 모형 평균은 그와 다른 수준의 증거다. 정권고 수락 예측률은 None73.8/SM71.4/NLE74.5/Combined72.3%, 오권고 수락 예측률은47.3/46.9/53.6/46.3%다. 후자는 이진 합침 규칙에서100−오권고 정확도로 변환했다. NLE−None의 정/오 수락 기술차는+0.7/+6.3pp이지만 정수 A/D, 동일 항목별 조건표, 이 차이의 새 유의성은 확인하지 않았다. 계획 D를 곱해 정수화하지 않는다. [AD-M30 Fig6 p18906](https://aclanthology.org/2024.emnlp-main.1051.pdf), [산술 검사](streams/adjacent/arithmetic-check.json).

## Q6. 좋은 평균과 함께 오류 선별이 나빠지는 조건과 반대 결과

### 1) 긍정 지표가 질문을 대신한 경우

A01 저자 보고서의 perceived-truth 긍정 응답은 TAB36/50, TA24/50, T33/50이다. 원래5범주의 합을 직접 더해 각50을 확인했지만 이것은 지각된 참값 설문이다. 같은 보고서는 query 없이 quiz에 성공할 수 있는 경우와, 초기 bookmark 중심 설계에서 상위 문서를 한꺼번에 선택해 점수를 얻는 문제를 설명한다. 틀린 점수·비관련 문서를 의도적으로 넣어 조사하는 일은 미래 과제로 남겼다. “신뢰가 올랐다”를 “오답을 걸렀다”로 바꾸지 않는 직접 반대 자료다. [SW-S33 PDFpp7–8/§6](https://cs.brown.edu/media/filer_public/36/96/36968fbe-c532-4630-a5b9-18c512efb1c7/ramosjerome.pdf), [손검산](streams/software/diagnostic-margins.json).

B01의 WOA 증가는 모두 맞는 조언이라는 조건에 한정된다. B02 Table3의 자신감 변화0.19/0.06과 §6.1의 설명 조건 증가 서술 방향도 맞지 않는다. 정정 VoR 전문이 확보되지 않았으므로 이 자신감 효과는 제품 주장에 사용하지 않는다. 긍정적 요약이 있어도 본 질문에 맞는 원개수·원판을 먼저 확인했다. [B01 §4.1](https://ricerca.sns.it/retrieve/e3aacdfe-98f4-4c98-e053-3705fe0acb7e/CHI2022.pdf), [B02 Table3/§6.1](https://publikationen.bibliothek.kit.edu/1000158077/150613452).

### 2) 분모·보정·조건별 하위집단의 문제

B03 Table1은14개 중 정권고8·오권고6이다. 그런데 Fig3의 정권고 수락몫+Fig5의 잘못된 거절몫은 baseline34.5+15.5=50%, task34+16=50%, gender32.2+17.8=50%다. 본문/각주가 말하는14시행 분모라면8/14=57.1429%여야 한다. 두 반올림 값의 합 오차≤0.1pp로 이 차이를 설명할 수 없다. 처음 나오는 anti-stereotype2개가 별도 분석되는 것은 확인했지만 ‘따라서12개’라는 규칙은 찾지 못했다. 서로 다른 AI 검토자가 원문을 다시 읽었고 이 불일치를 보존했다. [AD-M26 Table1/§3.3/각주7/Fig3·5/AppendixC](https://arxiv.org/pdf/2209.11812v5), [별도 검토](streams/diagnostics/review-b03.md).

B04의 고품질 설명·오권고에서 NLE40.9%와 None51.0% 정확도 모형 평균은 오수락+10.1pp로 변환할 수 있다. 그러나 NLE는 그 조건 자체의 설명 품질, None은 다른 조건 품질의 평균으로 하위집단을 나누므로 같은 이미지 집합이라는 보장이 없다. Fig5의 비보정 유의표시는 Fig7 BH보정의 해당 비교에서는 유지되지 않는다. Fig5 캡션의 NLE76.5%와 실제 Combined 막대도 불일치한다. 반대로 Fig7의 Insightful 혼합집단(오권고·낮은 설명품질과 정권고·높은 설명품질을 묶음)에는 Combined 관련 유의표시가 남는다. 이를 정권고만의 Convincing 패널 효과라고 옮기지 않는다. 따라서 ‘좋은 설명은 항상 위험’ 또는 ‘모든 효과가 보정 후 사라짐’ 둘 다 주장하지 않는다. [AD-M30 Fig5–7/§4.3](https://aclanthology.org/2024.emnlp-main.1051.pdf), [locator-errata.json](streams/adjacent/locator-errata.json).

D01 필터 전후에는 정권고 수락의 작은 차이 부호가 Amazon과 Beer에서 바뀌었다. 과제·정오층·분석 집합이 다른 수치를 한 평균으로 합치지 않았고, Beer의 중복400행도 무조건 제거한 결과만 선택하지 않았다. D04 저자 페이지의 구버전 코드 오류·재실험 공지는 열어 읽되 원 코호트와 새 코호트를 확정할 연결표가 없으므로 독립 복제로 가산하지 않았다. [D01 감도 원개수](streams/diagnostics/sensitivities-prefilter.json), [D04 저자 정정 공지](https://chenhaot.com/papers/human-predictions/).

### 3) 현재 결론을 제한하는 긍정·경계 실험

D06 Vasconcelos의 미로 실험은 경로 강조가 어려운 문제에서 과잉 수락을 낮출 수 있음을 보고한다. 생성 미로의 잘못된 권고는 벽을 통과하는 등 확인 가능한 오류이고, 강조는 그 확인 작업을 줄여 준다. 그러나 쉬운/중간 문제에서는 같은 뚜렷한 이득이 없고 글 설명도 같은 개선을 주지 않았다. Study1 N340, Study2의 일부 조건과 Study3의 여러 조건은 앞선 참가자를 재사용한다. 논문의 총731명과 연구별 N을 중복 더하지 않았다. Table1의1.74는 logit 계수이지1.74pp가 아니다. hard 각85×정12/오3의 계획1,020/255에서 실제 원개수를 역산하지 않았다. [RT-VAS-P §§4–7/Table1](https://cicl.stanford.edu/papers/vasconcelos2023explanations.pdf), [hard 프로토콜 q17의 logistic link](https://api.osf.io/v2/registrations/g6tjh/?format=json).

이 저자의 Appendix§12.3에는 먼저 시도한 Wikipedia QA 두 연구를 작은 효과 때문에 조기 중단했다는 기록도 있다. 등록의 문단 수·보상 차이까지 읽었지만 공개 정오별 정수 결과는 없었다. 후속 성공한 미로만 보고 일반화하지 않았다. Fig6의 예시 쌍은 medium이라는 점도 고정했다. [RT-VAS-P pp37–38](https://cicl.stanford.edu/papers/vasconcelos2023explanations.pdf), [earlier QA 등록](https://api.osf.io/v2/registrations/h9256/).

D07 de Jong의 그래프/문법 과제에서는 부분적 설명이 틀린 조언 수락뿐 아니라 맞는 조언 수락도 낮출 수 있다. 그래프 StudyI280−16=264, 문법 StudyII213−3=210이지만 코호트 간 중복 미확인이므로474명의 독립 사람이라고 합치지 않았다. 12개 중9정/3오라는 방법만으로 실제 셀 수를 만들지 않았다. 문법에서 모든 정오층 결과가 같은 명확성을 보인 것도 아니다. 이 연구는 위 미로 결과의 과제 의존성을 직접 논의하며 무조건 신뢰를 낮추는 디자인의 비용을 보여 준다. [DI-DEJ-P §§3–5/Fig2·8](https://nielsvanberkel.com/files/publications/cscw2025a.pdf), [세부 판독](streams/diagnostics/dejong-findings.md).

D02의 OnDemand/Update/Wait는 버튼·초기 판단·30초 대기 등 처리 자체를 바꾸므로 순수 설명 효과로 쓰지 않았다. D05는 신뢰도 bin별 서로 다른 항목과 새9명/이전 코호트 비교가 섞이고, D03은 예측을 이해하는 능력과 자기 가격 추정의 구분이 중요했다. 이 세 연구의 조정 평균·연속 오차·전환율을 주 표의 원 수락횟수로 치환하지 않았다. [DI-BUC-P](https://doi.org/10.1145/3449287), [DI-ZHA-P](https://doi.org/10.1145/3351095.3372852), [DI-POU-P](https://www.jennwv.com/papers/manipulating.pdf)·[별도 등록](https://aspredicted.org/xy5s6.pdf).

## Q7. 소프트웨어 설계자에게 돌려줄 문장과 설계 대안

**바로 사용할 문장:** “후보에 설명을 제공한 효과는 맞는 권고 수락과 틀린 권고 수락을 따로 확인해야 한다. 전체 정확도나 신뢰도 상승만으로 오류 선별이 개선됐다고 결론 내릴 수 없다.” 이는 D04의 직접 원행 반례와 A01/B01의 종점 차이로 지지된다. 적용 대상을 ‘소프트웨어 부품 선택에서 이미 검증된 성과’라고 넓히지 않는다.

**보류할 문장:** “원문 링크를 붙이면 사용자가 실제로 읽고 틀린 패키지를 더 잘 거른다.” 이번에 실제 링크 열람을 배정한 동일 후보 비교는 확인하지 못했고, A층은 두 자리 미충원·완전한 item mapping 미확인이다. “설명은 항상 도움이 된다/항상 과잉 수락을 만든다”도 D01 Amazon·D06·D07의 다른 방향과 양립하지 않는다.

부품 추천으로 옮기려면 후보 버전·라이선스/기능/호환성 조건·검색 시점·순위를 고정하고, 사용자 응답 전에 참값을 판정할 검증 규칙이 있어야 한다. 두 후보가 모두 요구를 만족하면 하나를 거절했다고 정답으로 채점할 수 없다. 추천과 근거가 각각 참인지 따로 남겨야 하며, 링크의 실제 접근·추가 클릭·읽기 시간·문서 판이 다른 경우 그것도 개입의 일부다. 이는 기존 실험에서 확인한 결손을 제품 판단에 적용한 **설계 추론**이며 새로운 효과 관측이 아니다.

| 관점 | 대안1: 이유 요약·강조를 기본 제공 | 대안2: 검증할 원문·조건·판을 대조하고 독립 판단을 지원 | 사용·중단 조건 |
| --- | --- | --- | --- |
| 권고를 받는 사람 | 빠르게 의미를 파악할 수 있으나 그럴듯한 오답도 수락할 수 있음(D04/B04) | 요구와 원문을 직접 대조할 수 있으나 클릭·읽기 비용 및 미열람이 생김 | 동일 후보의 정/오 수락을 각각 확인. 정권고 수락 이득과 오권고 수락 비용의 허용 기준을 명시; 단지 전체 정확도가 올랐다는 이유로 계속하지 않음 |
| 근거 작성자 | 읽기 좋은 문장·선택적 강조를 작성 | 근거의 정확한 위치·적용 버전·반대 조건·검증 가능한 이유를 작성 | 설명 품질과 권고 정오를 별도 채점. 권고가 맞아도 근거가 틀린 경우를 숨기지 않음(B04) |
| 정답 채점자 | 분류 데이터 라벨을 재사용하기 쉬움 | 버전별 기능 제약·허용 대안·불확실 라벨을 사전에 정함 | 리뷰의 실제/가짜나 직업 추출 라벨을 소프트웨어 적합성 참값으로 전용하지 않음. 복수 적합 후보·판 수정은 별도 층 |
| 검색 화면 설계자 | 초록·언어·배치·강조 등을 한꺼번에 바꾸면 효과 원인을 분리하기 어려움(A01/A02) | 후보·순위·권고를 고정하고 제공 조건·선택 열람·실제 노출을 각각 기록 | 같은 모델 선언만으로 동일성을 승인하지 않음. itemID×조건×기간 mapping과 최종 답·건너뜀·철회가 연결되지 않으면 오류 선별 효과 주장을 중단 |

대안2가 실증적으로 항상 우월하다고 주장하지 않는다. D06은 검증을 쉽게 만드는 설명의 가능성을 주지만 외부 문서 클릭이나 패키지 설치 실험은 아니다. D02는 독립 판단·대기가 실제로 추가 개입이라는 경고이고 D07은 회의적 태도가 정권고 수락도 줄일 수 있음을 보여 준다. 두 대안의 제품 선택을 뒤집을 최소 증거는 **같은 후보·같은 권고·같은 판에서 설명 또는 실제 원문 열람만 사전 배정하고, 정답키와 최종 선택·초기 일치·결측을 공동 집계한 기존 공개 자료**다. 실제 열람의 효과라면 제공 조건만이 아니라 배정된 열람 방식과 노출 기록까지 필요하다.

이번 조사로 설계자 총 노동시간, 실제 설치, 후속 재작업을 추산하지 않았다. AF054의 완료시계·개인 코드·가상 조합과 AF038의 사람 참가자0명은 출발 사실로 인수했으며 재분석하지 않았다. 사용한 것은 공개된 기존 실험·집계와 그 식별성 한계다.

## 추가 분석: 주변수만 같아도 부호는 달라질 수 있다

다음은 **자가 생성 논리 반례**로 실제 참가자·관측·외부 저작이 아니다. 각 조건에 판단기회100, 정/오 권고50/50, 총수락60, 최종정답60을 고정했다. 오권고 거절 뒤 제3 오답을 허용하면 같은 주변수에서 두 개입 세계가 모두 가능하다.

| 가능한 표 | 정권고 수락=정답 | 정권고 거절=오답 | 오권고 수락 | 오권고 거절 후 정답 | 오권고 거절 후 제3 오답 | 총수락/전체 | 최종정답/전체 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 공통 대조 | 40 | 10 | 20 | 20 | 10 | 60/100 | 60/100 |
| 개입 세계Ⅰ | 45 | 5 | 15 | 15 | 20 | 60/100 | 60/100 |
| 개입 세계Ⅱ | 35 | 15 | 25 | 25 | 0 | 60/100 | 60/100 |

각 정오층의 행합은50이다. 세계Ⅰ의 오권고 수락 차는15/50−20/50=−10pp, 세계Ⅱ는25/50−20/50=+10pp이고 정권고 수락 차도 반대로 바뀐다. 오답 선택지별 개별 분포까지 같다고 주장하지 않는다. 손합·실행 검산은 [three-choice-diagnostic.json](streams/software/three-choice-diagnostic.json)에 있다. 이진 강제 선택에서 총수락 T와 정답 C, 오권고 D가 모두 알려지면 오수락 `(T+Dwrong−C)/2`가 식별되므로 그 상황까지 비식별이라고 부르지 않았다. 기존054의 가상 조합을 재계산한 것은 아니다.

결측 m이 정오층별로 알려질 때의 최악–최선 범위와 현재 계산할 수 없는 칸은 [reproduce.md §7](reproduce.md)에 있다. 미확인 m에 임의 수를 넣거나 탈락자의 정오층을 추정하지 않았다. B04 모형 확률과 B03 인쇄 비율을 정수로 역산하지 않은 이유도 같은 식별성 원칙이다.

## 자체 검토·검사 범위·최소 재개 입력

[SELF_CHECK.md](SELF_CHECK.md)는 Q1–Q7별 주장·직접 근거·반대 자료·판정이 뒤집힐 조건을 연결한다. 별도 AI 조사자가 통합 원장의 출처 연결·계보·계획/관측 구분과52개 관측 대비를 검산했고, B03은 다른 AI가 원문을 다시 열었다. A/B/진단의 최초 원장 작성자가 자신의 표를 재검토한 부분은 자체 검토로, root가 D04 원행을 별도 코드로 다시 센 부분은 별도 재계산으로 표시했다. 인간 심사·독립 참가자 복제가 아니다. [원장 검토 범위](streams/diagnostics/review-ledgers.md), [B층 검토](streams/adjacent/self-review.md), [A층 검토](streams/software/self-review.json).

원격 고정판의 결과·수용 원장을 다시 읽고 실행한 계약 검사 주체·명령·SHA·출력은 최종 `evidence/final-verification.json` 및 `HANDOFF.md`에서 확인한다. 이 결과 파일이 먼저 고정되어야 하므로 그 후의 성공을 여기서 미리 단정하지 않는다. 상태 PARTIAL은 파일 저장과 별개의 연구 수용 판정이다. 우선 재개 행동은 **B03의 공개 분석 코드·포함 마스크·정수 교차표/정오표가 새로 제공됐는지 확인해14대12/가중 문제부터 해결하는 것**이다. 이는 기존 자료의 식별성 확인이며 저자에게 연락하거나 새 참가자를 모집하라는 지시가 아니다.

| 불일치·약점 | 영향받는 주장 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| A 두 자리 미충원·선행 방법5개 및 main-paper proxy 한계·A02 정식 본문 미독 | 소프트웨어/IR 최초4개와 같은 후보 설명 효과 | [frame.csv](frame.csv), [방법 감도](streams/software/methods-sensitivity.json), [A02 poster](https://www.dl.soc.i.kyoto-u.ac.jp/~tajima/papers/iui24poster.pdf) | 고정 원순번7/8/9/22/26와15 원문 방법, A02 본문을 확보해 기존 순서에 대조 | 방법 적격성과 첫4개를 확정하고 동일 item/조건·원응답을 회수하면 충원·등급 재판정 |
| B03 14중8 대비 그림 정권고 몫50%; B02 정정 VoR 미확인; B04 모형·하위군·보정 한계 | 선정 연구의 정오별 수락 차이 및 강한 효과 방향 | [B03 Table1/Fig3·5](https://arxiv.org/pdf/2209.11812v5), [B02 Table3](https://publikationen.bibliothek.kit.edu/1000158077/150613452), [B04 Fig5–7](https://aclanthology.org/2024.emnlp-main.1051.pdf) | 먼저 B03 공개 포함 마스크·가중 규칙·정수표/정오표 확인; 이어 원판별 응답·배정키 | 같은 정의의 관측 분자·분모가 일치하면 J1/J2 및 정오별 차이로 갱신 |
| 제공과 실제 읽음 미분리; 데이터 라벨·검증 비용이 부품 선택과 다름 | 원문 링크 읽기의 효과, 설치·재작업·노동시간으로의 외삽 | [stimuli.csv](stimuli.csv), [D04 package](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285), [D06 Fig6/§12.3](https://cicl.stanford.edu/papers/vasconcelos2023explanations.pdf) | 같은 후보·판·정답키에 제공/배정열람/실제노출·최종선택을 잇는 기존 공개 자료 탐색 | 별도 배정된 검증 가능한 근거와 공동 응답표가 재현되면 제품 문장 범위 재판정; 현재 자료만으로 노동·설치 효과는 추산하지 않음 |
