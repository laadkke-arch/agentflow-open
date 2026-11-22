# AF-RES-046 · 규칙·판독 수정 이력

## R01 · 추가층 기능 적격 문구를 사용자 원문으로 복원

- 변경 UTC: 2026-11-22T22:08:06.274183+00:00
- 원 규칙: SCOPE Q1.4의 추가층도 자연층과 같은 사용자보이는 기능 변경이어야 한다는 문구.
- 수정: 사용자 Q1은 해당 기능 조건을 자연층에만 두었다. 추가층은 첫 공개 구체 코드+사람 리뷰의 같은 목적 예제/부품/원리 링크이면 내부 구현/성능 변경도 적격이다.
- 이유: 작업자의 최초 SCOPE가 사용자 지시보다 불필요하게 좁았다. 후속 결과·작성자 응답 판독 전에 지시 원문과 비교해 바로잡았다. 양성 결과 수를 본 뒤의 확대가 아니다.
- 영향: scikit-learn 추가층 순번 25535,25554,25555 등 내부 변경 제외 후보 및 pandas 추가층 앞선 내부변경 제외 후보. repo별 frame의 원 제외와 새 판정, 선정 후보 및 노출 이력을 보존한다. 원 규칙에 따른 최종 집계는 아직 없고 두 추가층 선정이 봉인되지 않은 상태였다.
- 원 봉인: a0c819405dfe4ab5b81a72459a067f3905977afe. 새 규칙은 이 변경 커밋 이후 적용. 자연층8의 규칙은 불변.


## R02 · 봉인 뒤 최초 공개판 복원과 사후 본문 교정

- 시점: 2026-11-22 22:35~22:45 UTC, 묶음3 원격57d749eeae66a1e62b5e75cce644c6ba82b5d47b 뒤. 표본 선정이나 성공 기준을 바꾸지 않은 증거 보완이다.
- 원판정: 살아 있는 commit/review head는 확보했지만 정확한 최초 opened head는0/12, N-S2는선정시provisional. 자연rank7 sklearn25272의 surviving판은개설다음날committer시각이라최초diff미확인.
- 새근거: 공식 공개 ClickHouse의 GH Archive 정규화 opened행12슬롯+제외25272, 당시 head/base/body, 불변GitHub diff. 최초공개판12/12를공개미러기준으로복원했고25272의최초test-onlydiff도확인했다. rawgzipendpoint403과원eventID미보존은미확인으로유지한다.
- 바뀐SHA: L-P2 pandas51116의기존첫commit777c35c83e7ad35fa8f665497515be633c109b45→실제openedhead87ade9fa4e0b523582a3e1e1476c94ed9f948219. L-S1의링크전a897a34d7d989bf317de17f80948639c0fd5ecf1과최초openedhead39a39ad309414b4d8a1a93bc3105980d2222a589를분리한다. 나머지10슬롯후보head는일치한다.
- 본문정정: N-P1의50514참조는후첨이므로개설때이미제시했다는해석철회. L-S2의25484와경고제거완료문구, L-S1의oldPR숫자24497도후첨. 외부프로젝트명과다른원개설참조는각복원원장에서개별판정한다. N-P1/N-P3의body는template지만제목과실제첫diff/회귀시험이구체사용자동작을제시하므로슬롯유지.
- base와parent/merge-base구별: N-S1,L-S2,N-P2,L-P1등은실제openedbase와featurecommitparent또는3-dotmerge-base가다르다. N-S1의초기PRdiff는det_curve검증도포함한다. L-S1은ogrisel이연공유branch의betatim mergehead·79commits/14files이며모든초기코드를ogrisel단독작업으로귀속하지않는다.
- 영향행: baselines12, frame선정12+탈락25272, cases12, opening사건12추가. 원stream파일·당시선정판정은수정하지않았다. root에기존값과복원값을함께저장한다.
- 원집계/새집계: 자연8/링크0, 추가4/링크4, 같은작성자후속변경2,엄격0,주창노동측정0은모두동일. 슬롯교체0·최소수추가0. 첫공개판복원만0/12→12/12(미러근거), rawevent독립확인0/12는유지.
- 재개/반증: initial-public-heads.csv와두stream initial-public-head-recovery.json의정확SQL/URL로같은opened행확인. raw event를독립확보할수있을때eventID·head/base·bodyhash를대조한다. 결과가충돌하면복원상태를내리고원판정을남긴다.
