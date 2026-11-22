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


## R03 · 실제 패치의 공개 경계 재검증에 따른 확정 분자 하향

- 증거 기준을 느슨하게 바꾼 것이 아니라 기존 공개시각/고정판 기준을 더 정확히 적용했다. 원판정은c9afe55a923a5cb432e5b0de2ada91dddd7e36aa에고정돼있다.
- 원판정: L-P2의후속52089개설17:37:25와survivingcommit f95152e를연결하여원PR종결17:38:10보다45초전에actualpatch공개라고세었다. 기본동일인2/4·타인포함4/4.
- 새자료:52089opened행은정상query200/0행으로미회수,4일관련사건조회도첫회수head연결은종결뒤. GitHubreview1349354160 submitted_at2023-03-20T20:36:41Z가f95152e를직접고정한다. currenthead/PRcreated/committerdate를동일공개판으로추정하지않는다.
- 새판정: 실제같은작성자·같은목적후속코드는존재하지만주창내정확SHA공개는미확인. L-P2의same_author/any_author주창값모두null로내린다. 기본동일인확인1/4·미관측1·미확인2,타인포함확인3/4·미확인1. 엄격0/4·노동0관측은변함없다. 30일감도same1/linked2·any2/linked2;60/90일same1/4·any3/4. 선행동일인L-P2제외1/3·any3/3,선행타인까지P1/P2제외1/2·any2/2.
- 관련보완:52043/51784/51166의openedhead복원은선행착수·사전작성근거를강화한다.52053openinghead는미회수이나종결전3/20 17:17:26review1349064316이final19e8640을고정한다.그변경의최초착수가firstlink뒤라는뜻은아니므로새양성분자로올리지않는다.
- 비용시점보완:25261 IssuesEvent openedbody에manyhours문구확인.비수치·다른사람·주창전구분유지.25605openedheadfeaabb7e는09:22:47이벤트에서확인되며REST생성09:22:46과분리한다.
- 영향행:cases L-P2/L-S1/N-S4, changes L-P2-6/S-C08, labor 해당행, events followup-pr-52089의SHA연결철회+보완3행,통계/필수표/수용원장. 원stream기록은역사로유지하고현재root판정이이를보완한다. 신규사례0·최소저작추가0.
- 판정을뒤집을최소자료:2023-03-20T17:38:10Z까지의52089head=f95152e인원opened/push/review/event또는동등공개불변판.확보되면원2/4조건을되살릴수있지만첫링크인과·노동근거는별도다.

## R04 · 기존 로직의 사후 통합을 실제 변화로 구분한 반증 보완

- R03 중간 결과와 원장/표는 원격 `416c6739ce24c7a2f77f4fd6911655363834652a`에 고정했다. R03의 f951 공개 오인 철회는 유지한다. 새 양성은 같은 PR을 새로 뽑은 것이 아니라 기존 L-P2의 다른 후속19e 근거다.
- 원판정: f951 주창 공개 미확인을 이유로 L-P2전체를미확인, 동일인1/4·타인포함3/4로 낮췄다. 52053의 설계가 링크 전에 시작됐다는 사실만으로 그 이후 실제 변경까지 없거나 미확인으로 취급할 위험이 남았다.
- 새근거: 52053의4commit을 각각 열고 first-parent명시비교를 했다. 같은작성자ID8078968의19e864062c0d253db1b10469876b553391dad0db는 첫부모3ce5d85 대비 any/all nullable→result_mask와 결과 마스크 생성·전파·해제를 실제2파일에 통합한다. 두번째부모1f7a7f2는 GitHub committer/52043 merged_at2023-03-17T19:48:49Z 일치·API서명valid보고로 첫링크18:45:21뒤 생성됨이 확인된다. 따라서통합의하한을부모생성에서추론하며, review1349064316은3/20 17:17:26에정확19e를고정하여원종결17:38:10전공개상한을준다. exactpush와개별서명의암호학적독립검증은미확인이다.
- 판정 기준: 원 SCOPE의 change는 동일행위자·동일요구의 실제diff이며 새로발명한로직에한정하지않았다. 선행착수는별도감도였다. 그러나통합이라는해석차이를숨기지않고유형을별도표시한다. 기본동일인2/4·타인포함4/4, 원작성자미확인L-S1만1. 기존로직통합을양성에서제외하면동일인1/슬롯4; 선행동일인착수L-P2의PR자체를제외하면1/슬롯3. 두분모는서로다르다.
- 같은목적·품질 근거: 작성자1474292973이52043/52053을기존공통경로작업으로직접연결한다. 정확19e의test_any_all.py L142–154에서[pd.NA,1] all(skipna=False)→NA,any→True를읽었다. 새시험추가나조사자실행은없다. 3ce5의69파일통합은타깃별의미가다르므로새양성으로합산하지않는다.
- 영향행: cases L-P2, changes L-P2-4의잘못된exactopening연결정정과L-P2-7추가, followup-pr-52053의SHA연결철회·public앵커2추가, labor L-P2, statistics/sensitivity/필수표/수용원장. 총events173/changes38/source영수증528. 새선정PR0·최소배당추가0(54유지), 엄격0/4·노동미확인유지.
- 원문: streams/pandas/final-risk-review.json, sources-supplement-final-risk.jsonl의8영수증. R03의f951 후기만으로창내양성을되살리지않으며fa750의최초head도미확인유지. 판정을뒤집을최소자료는19e첫부모대비변경·행위자·부모생성기록의반증또는별도공개기록이다. 링크인과와사람시간은독립자료가추가로필요하다.
