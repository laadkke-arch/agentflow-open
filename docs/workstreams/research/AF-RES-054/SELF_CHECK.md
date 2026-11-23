# AF-RES-054 자체 검토

## 검토 주체·범위

종합 판정·편집자는 root assistant다. 기준/방법, 소프트웨어, 교육/공학을 조사한 별도 assistant 에이전트가 원문·집계·통합 원장을 교차검토했다. 이들은 같은 작업공간과 목적을 공유하며 외부 사람의 독립 심사 또는 독립 복제 연구가 아니다. 검토 파일의 SHA와 시각은 각 `*-review.md/json`에, 반영 상태는 `evidence/review-resolutions.json`에 있다. 문헌 자체의 직접복제 연구와 이번 에이전트 검토를 구별한다.

검토 기준은 사용자가 지정한 입력판, SCOPE의 사전 규칙, 실제 공개 파일, 고정 결과표다. 원래 기능 기준·마감·배정 분모가 없으면 수치를 만들지 않는다. 총 원문 수를 채웠다는 사실로 분야별 배당 또는 모집 요건의 결손을 상쇄하지 않는다. 전체 상태는 **부분 충족**이다.

## 질문별 주장·반대 증거·재개 조건

| 질문 | 주장 | 직접 근거 URL·위치 | 반대 증거 또는 반례 탐색 범위 | 결론이 틀릴 조건 | 미확인과 최소 재개 자료 |
| --- | --- | --- | --- | --- | --- |
| **Q1 배정과 개입** |8자리 모두 추적했으나 이름 있는 연구6개, 빈 자리2개다. Casdoc은 같은 복합 조건의 관찰이고, 같은 후보 설명만의 적격 배정 대비는 확보하지 못했다 | [Blueprint](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) printed518; [eXoa](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §§5.1–5.2; [Newton](https://users.ime.usp.br/~gerosa/papers/Newton.pdf) Table3; [Casdoc](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf) §3.1; BM-B01/B02, SW-N-P/C-P |전문에서 DesignPattern의 실제 구현Task22/32와 Casdoc의 별도 배정 조건 부재를 확인했다. 소프트웨어32metadata·다른 분야36metadata를 유지하고 Pillai/CAD/Kruse는 진단으로만 읽었다. SCOPE에 선정 전 노출·질의 변경을 기록했다 |원 실험판이 동일 후보·접근권에서 설명만 무작위화했거나, 보존한 모집틀의 미해결 metadata에서 규칙 안의 선행 적격 연구가 확인될 경우 |원 배포자료·배정표·실험판SHA와 빠진 보조 질의 이력. 결과를 본 뒤 교체하지 말고 새 모집 규칙을 먼저 동결 |
| **Q2 시간과 품질** |첫 paste/문서 전환/메시지/명목 소요시간/최종 제출을 구별했다. Blueprint·E01에는 원 이진 pass가 없으며 Newton의 완료 레이블은 기능 판정식이 미확인이다 | [eXoa](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §§5.1.2/5.3.1–2, Tables X/XII; [Newton 패키지](https://zenodo.org/records/10459420) TutorialStudy/Woz_Script/result.json; [DesignPattern](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml) Procedure/Data collection; [Bichler SAV](https://osf.io/mykxc/) 및 CD-P01 Methods |완료자 전용 시간,25분과33–68분 로그 불일치, 계획45분을 넘는4/10대조 행,45분 연습과 약35분 검사를 대조했다. 원래 pass가 있는지 코드북·과제지·튜토리얼·채점 설명을 읽었다 |원래 프로토콜의 제출·종료·기능 체크리스트가 발견되어 같은 관측 레이블과 정확히 대응하는 경우. 독립 채점자 부재만으로 배제한 것은 아님 |원 timer 시작/종료/제출 이벤트 의미, late/no-submit/withdrawn 규칙, 원 기능 판정식·버전. 새 통과선은 후속 제안으로만 가능 |
| **Q3 원행 결합** |Newton24단위 artifact, Casdoc122검색조각, Pillai112분석행 연결은 실제 수행했다. 목표 배정×시각×최종품질 결합은 수행하지 못했다 | [Newton](https://zenodo.org/records/10459420) Participant/exp 폴더; [Casdoc](https://zenodo.org/records/14868205) phase2.ID/phase3.ID; [Pillai](https://osf.io/85tye/) ID/Subj_ID/Condition; [Bichler](https://osf.io/mykxc/) Cond/TimeP/KPost; RC-04/05, SW-N-R/A, CD-D01/D02-* |Casdoc 중복 헤더7종·같은시각 초과72행, 복합 instruction 코드, Newton/질의 그래프 단위, Kruse50프롬프트=25×2, CAD55기계질의를 검사했다. DesignPattern 공유ID 부재와 원 제출물 분실을 확인했다 |공개한 사람키/폴더 규칙이 다른 코호트·기간을 가리키거나, 같은 원자료에 검증된 최종 grade/timer 열이 있는데 놓쳤을 경우 |같은 코호트의 비식별 배정·제외 원장과 공통키; event 집계 정의; 판정 열. 정렬순서나 익명 질의ID로 임시 연결하지 않음 |
| **Q4 공동 결과 범위** |같은N·정확한q/t이면 Fréchet 정수 경계를 쓴다. B02는 저자가 교집합3/1을 명시해 점식별된다. 정의가 없는 이진 종점에 [0,N]을 원 결과인 듯 붙이지 않았다 | [eXoa](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §5.3.2; [Imbens–Manski](https://cemmap.ac.uk/wp-content/uploads/2020/08/CWP0903.pdf) §3; [Balke–Pearl](https://ftp.cs.ucla.edu/pub/stat_ser/r199-jasa.pdf) §§2–3; calculate_bounds.py/evidence/calculation-check.json |N1–25의6200 q/t조합과 경계 정수표를 전수 확인했다. 정확한 주변수가 있어도 양부호가 가능한 가상 예, Blueprint q 미정, eXoa 미보고t의 두 허용표를 구분했다 |원문의3/1이 같은40분·같은12명·네과제 모두의 교집합이 아니거나, 알려진 구조적 제약을 빠뜨려 허용표가 실제 설계에서 불가능할 때 |B02 원 배정·제출·test 원장. 다른 연구는 원 사건 정의와 같은N의 정확한 주변수부터 필요 |
| **Q5 대비와 불확실성** |B02의 저자 표본 대비는1/6이고, 가상 주변수의 차이는[−1/10,1/5]다. 둘을 CI로 부르지 않으며 교차 설계에서 개인 인과효과를 만들지 않았다 | [eXoa](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §5.3.2; [Imbens–Manski](https://cemmap.ac.uk/wp-content/uploads/2020/08/CWP0903.pdf) §§2–3; [Newton](https://users.ime.usp.br/~gerosa/papers/Newton.pdf) Table3/§4.2 |각 군 하한과 상대군 상한을 교차시켜 대비를 검산했다. Newton 같은12명·다른 자료집/기간, Casdoc 형식 자유선택, E01 분석분모를 확인했다 |과제·문턱·분모가 실제로 다르거나, 공통의 짝 제약이 경계를 더 좁히는데 누락했을 때. 저자집계 오류가 확인되면 점 대비도 수정 |짝과 기간·순서·과제키, 원 grade/clock; 표본추론을 하려면 그 설계에 맞는 별도 불확실성 분석. 현재 CI 계산 미실시 |
| **Q6 반례** |부분 시간의 단축·성공자 선택·원행이 아닌 코드/점수표·전체/하위 종점 변경을 실제 사례와 구성 반례로 구별했다 | [AF050 고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/RESULT.md); [eXoa](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) Table XII/§5.3.2; [DesignPattern](https://zenodo.org/records/10849702) data.csv; [Pillai](https://osf.io/pd95v/) Experiment2 |원주변표와 양립하지만 전체3/1 문장에 모순인 표를 만들고 배제했다. Blueprint 성공자 평균 반전은 가상임을 표시했다. T22의 반대방향, Pillai143−16−11−3=113 대112, Urry 조건N 뒤바뀜, Bichler 원고/자료 차이를 읽었다 |구성표의 합이 틀리거나 관측 사실로 잘못 제시됐을 때; 원고의 다른 판/코호트가 불일치를 설명할 때; 이전 결과를 이번 직접열람 수에 더했을 때 |최종 출판본·정오표·파일 판 기록, 제외 사람의 조건별 원장, 원문에 없는 실제 실패/철회 사유를 채워 넣지 않을 것 |
| **Q7 허용 문장** |도구 묶음 비교, 저자 공동 집계, 원자료 연결 감사의 각 수준에 맞는 문장을 반환한다. 동일 후보 설명 효과·동등 품질 총시간·후속 재작업은 현 자료로 확정하지 않는다 | RESULT 표1/2와§7/§10의 직접 링크; [Blueprint](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), [Newton](https://users.ime.usp.br/~gerosa/papers/Newton.pdf), [Casdoc](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf); 각 source_id의 내용·한계 |설계자·참가자·채점자·자료관리자 관점에서 훈련/대기/실패 비용, 최종 기능/순위/지식 점수, 코드 분실·판 변경을 비교했다. 교육 전이/추적 점수를 설계 완성품 기능으로 대체하지 않았다 |같은 후보 설명만의 배정 또는 품질 동등성과 후속 수정 이력을 확인하는 자료가 발견될 때 더 강한 문장 허용. 현재 문장이 해당 조건을 넘어서는 경우 수정 |연구별 minimum_resume_input을 먼저 확보; 설명 조작·전원 시계·원 pass·추적 원장을 새로 설계하는 것은 후속 제안으로 표기 |


## 정량 점검

| 점검 | 예정/관측 분모 | 결과 |
| --- | --- | --- |
| 필수 여덟 자리 추적 |8자리 |8/8자리 기록; 이름 있는6, 빈2. 신규6자리 중 이름 있는4, 배정 비교 적격3 |
| 새 소프트웨어4·교육1·CAD1 |4/1/1 |metadata 선정3/1/0; 실제 배정 비교2/1/0. 부족분을 진단 논문으로 교체하지 않음 |
| 원문 최소·고유·전체 열람 |최소22고유; 행 수는 별개 |23고유1차 저작,229열람 행,229유일 source_id. 필수15필드 및 source 참조 검사 |
| 엄격 자료 배당 |개입/과제/루브릭4 |별도 독립 도구1/4; 정확한 실험 바이너리 동일성 확인0/4. 다른 범주의 초과분으로 보충하지 않음 |
| 예정 배정 단위·실측 분석 단위 |B0120, B0224묶음/96과제, S0112사람/24조건, S0221사람, S0313사람·8목표, E01 원배정 미확인 |S01 artifact24, S02분석21, S03검색조각122, E01분석231. 계획13×8을104실제 배정행으로 이름 붙이지 않음 |
| 목표 원행 직접 공동종점 |이름 있는6연구/계획8자리 |확보한 목표 직접계산0건. 개별 원행의 공동 성공0을 관측했다는 뜻 아님 |
| 저자 공동집계 |같은 분모·시간·pass 교집합 |B02 한 연구. Newton은 좁은 저자 완료 보조 종점으로 분리 |
| 정수·대비 산술 |N1–25의6200 q/t조합 |행열 합·비음수·경계 달성 가능성 확인. B02 point1/6, 가상 차이[−1/10,1/5] |
| 표/원장 대응 |8자리,19종점,10연결,34경계·대비·결측·구성 기록 |SOURCE ID 참조 해소; 별도 에이전트가 평탄화 단위/분모 누락을 지적하고 root가 수정 |
| 원격 고정판·session check |결과 커밋 후 수행 |실제 출력·종료코드·UTC를 evidence와 HANDOFF에 후속 기록. 실행 전 통과로 기재하지 않음 |

## 발견한 오류와 반영

- Casdoc의 단일 instruction 코드63/51과 복합코드 분리65/52를 병기하고 각 단위를 이름 붙였다.
- Blueprint의 CHI Fig4 참조와 실제 dissertation Fig5.4 위치를 분리했다. 이전 인계의 순위 위치 연결 주장을 재사용하지 않았다.
- eXoa의 나머지9/11명을 오답/미완료가 실제로 섞인 집단으로 단정하던 문구를 사유별 분해 미확인으로 고쳤다.
- B02-task3 대비의 CSV 단위를 rate difference로, Newton6/4는 observed_secondary_count로 분리했다. S01 event_rows의 실제588도 평탄화했다.
- E01-final의 결측0에 분석231행 분모를 붙이고 원배정 탈락은 미확인으로 명시했다. 약2100초는 강제 deadline 열에서 분리했다.
- Pillai143/112·CAD 같은6명의 교차/훈련·E01 압박층별 대비57/58·58/58·SLOT-E01 출판월/판 차이를 정규 CSV 열에도 표시했다.

위 수정은 원 종점·표본 규칙을 바꾼 것이 아니라 관측된 단위와 한계를 정확히 표시한 것이다. 원고판 사전점수4.75와 SAV4.573의 불일치는 미해결이며 최종 출판본 오류로 단정하지 않는다. 가장 중요한 세 약점과 최소 재개 행동은 RESULT와 최종 HANDOFF의 맨 끝 표에 동일하게 유지한다.

## 최종 반증 검토의 추가 정정

B02의 t3–12/1–12를 원문 전체가 허용하는 확정 범위로 읽힐 수 있는 표현을 고쳤다. 이는 x=q만 적용한 약한 외피다. Table XII의 부분 correct submissions를 같은40분 안 제출 사건에 연결하면 t≥11/10과 하단표(3,0,8,1)/(1,0,9,2)가 필요하다. 원문에 독립 제출flag/시각이 없어 이 연결은 조건부 민감도이며 관측 t가 아니다. 원문을 다시 읽은 RT-06을 추가해151열람 행이 되었고, 같은 저작이므로 고유23은 유지했다. 공동 성공3/1과 차이1/6은 두 해석에서 변하지 않는다. [원문](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §§5.1.2/5.3.2/Table XII; SCOPE R2b.

최종 문장 검토에서 E01의2×2를 독립군 요인설계로,4.75/4.573을 원인 미확인의 수치 불일치로 명확히 했다. CAD 사람 실험의 위치는 §5.3/Table2/Appendix F로 수정했다. Pillai의31명은 분석에 포함되지 않은 사람이며 사유 전체가 확인됐다고 부르지 않는다. Newton의 회기 약70분을 강제 cap으로 부르던 하위 원장의 표현도 수정했다.


## AF-RES-054#2 재개 검토 반영

재개 전 root151행에 없던 기존 crossdomain 접근15행과 재개 검토·입력 확인63행을 합쳐 최종229행/고유23저작으로 맞췄다. 같은 원문 재열람·실패는 고유수를 늘리지 않는다. `build_ledgers.py`가 모든 resume 출처 원장을 합치며, validator가 stream 전체 source ID 합집합과 root 원장의 일치를 검사한다.

별도 세 assistant의 검토 범위·입력 해시·원문 위치는 `streams/resume-baseline/review.md`, `streams/resume-software/review.md`, `streams/resume-acceptance/review.md`에 있다. root는 구성표를 Table XII/§5.3.2 제약에 한정했고, Casdoc 전원 연장선택권/3명 사용과 계획2400초를 원장에 반영했으며, Newton 로그를max−min 범위로 표현했다. A08b의8논문은 열람 총수, 적격 신규 비교는3/6이며 Bichler2026은2016/2022 분석의 복제이되 E01의115명과 중복이라는 계보를 명시했다. 최초 모집과1차 종점은 그대로다. 분담 검토자에게 root의 후속 모든 편집을 승인한 것으로 소급하지 않는다.
