# AF-RES-249 자체 점검 (⑤)

자체 문서·원장 재판독이다. 별도 독립 연구자 검토·실제 사람 실험·CPython 실행은 시행하지 않았다. 검토 입력은 RESULT 커밋 14144273298126fbd6ff7e2724a8436a3771bdf9의 GitHub 원문 14파일. 이 문서 커밋 후 고정 결과 SHA에서 15파일을 다시 열고 HANDOFF에 최종 재확인 영수증을 남긴다.

## Q별 근거, 반증 탐색, 남은 판정
| Q | 직접 열어 확인한 근거 ID·위치(원장 URL) | 실제 찾은 경쟁 증거/반전 및 판정 | 미확인 |
|---|---|---|---|
| Q1 | D01 pp.517–518; D03 evaluation; D05 198–211,233–235; D06 VI–VII; D10 V; M01 §2; 236 chain/rivals M1–3/S1 | 미리보기 클릭 없이 노출, 이미 알던 이름/실패 사례, 제3자 zip·링크 전 close; exposure/understanding/attempt/replacement/acceptance를 분리 | 실제 joined causal event 없음 |
| Q2 | D01 directed task; D02 Table1; D10 §III; P01 L29–40; F01 methods | 명시 API 과제 자체가 priming. 사전 자유회상 부재 U, 이름/원리/조건/실행 가능성 분리. N의 upper-bound 원리는 이미 알려짐 | 과거 기억·사후 보고 진실, probe reactivity 미확인 |
| Q3 | D05 order; D06 §VI; D10 §V; M01 §2; M02 L137–172; M04 items9–11 | 자력 inline 발견, 순서효과, 양쪽 후기 제공. E/L 초기창과 후기를 분리, 1기 주분석; 2기 탐색; 전체 배정 유지. 2025 원문 CAPTCHA → 2010 원문, 최신 기준 주장 없음 | carryover/확산·검정력·실제 배정 실행 미확인 |
| Q4 | T01–T05 docs and fixed tests; T06 implementation supplement | 정렬 groupby/Counter 비연속 키 반례; bisect_left 동률 없는 공개 예시만 통과, tie/empty/unchanged/type 검사. 허용 수동 구현 별도. A2/A5 및 B2/B3/B6/B7 기대 확인 손계산 | 3.12.16 docs와 v3.12.0 테스트 실행 대조, 실제 코드 pass 미확인 |
| Q5 | D01–D06,D08,D10; P02 header+1–27; P03 dataset layout; P06 raw JSON 100 entries, P07/P08 corroboration; 236/237 고정 원표 | URL/clone 타임스탬프/예제 origin은 사람 교체 증명 아님. P06 자극 데이터지 행동 로그 아님. 같은 hash 다른 actor 반전, parent/actor/session/diff/role/receipt 누락 시 보류 | P06 당시 study exact version, P03 대형 원자료, 공개 기록의 완전 join 미확인 |
| Q6 | P01/P02; D03/D10; M03 selection; M04; 237 cohort/evaluation | 후기 작성자 0분은 reviewer 0분 아님. 미열람·중단·known·실패 전부 분모. synthetic 71/3 vs 성공자 52/3, 검수 증가 역전 | 사람시간·인수·효과 및 selection assumptions 미확인 |
| Q7 | F01 methods; F02 원자극/실험; F03 Table1; F04 Exp2 Fig3/Table2; D10 §V.B | 고착은 부적합 예시 복제도 유발, 자체 생성/경고/자력 발견 경쟁 설명. K 유지, N 새 이름과 부합 및 교체, R 열람거절, F 교체+실패. revisions.md C1–C8 및 N'/N''/N'''/R'/F'/F''/K'/missing | 별도 코더 일치·실험 효과 일반화 없음 |

## 자료 분모와 실제 상태
- 원장 41 source_id 유일, 산입 24 distinct work/file (17 lineage), 개발 검색·예제 7 / 프로토콜·데이터 4 / 고착 4 / 방법 4 / Python 5. 보수적으로 D04(예제 평가)·P01(자료사전)을 빼도 22 = 6/3/4/4/5. P02 실제 anonymized data, P03 독립 공개 구축 프로토콜, P06 별도 공개 실제 stimulus data, 서로 다른 계보. 논문과 별도 자료는 별도 artifact이지 독립 실험으로 중복 산정하지 않는다. P06 당시 study version 동일성 미확인. D05/F01 일부 화면 실패, 직접 열린 원문 텍스트를 산입; X01/X05/X06 실패 3행, 그 외 비산입 14행. 전체 링크의 미래 접근성, 전체 저작 전수 열람을 주장하지 않는다. 원장 열람 시각 UTC 창으로 표시, 구체 구간·제약 남김.
- 236: 중앙 DONE 자체 PARTIAL; 3 official URL/40 본층, 작성자 교체 0 관측(실제 사용 0 단정 금지), 별도 S1 실패. 237 중앙 DONE 자체 PARTIAL; 고정 cohort 12행 한 개발자, 7 observed post-author zero, reviewer/acceptance key UNKNOWN 12. 225는 brief/236 근거만 참조; 238–242 결과 미사용. 서로 다른 선행 사건을 하나로 합치지 않음.
- 실험 예정 24명/48 배정, 주분석 1기 24, 2기 탐색24, task×E/L 각12(1기 각6). 실제 모집·배정·사람 사건·추적·테스트·독립 채점/인수 모두 0건(미실행); 예정 자리 비어 있음, 관측 결측률 N=0 정의 불가. 실제 성공률/인수율/평균 비용 산출 금지. 가상 4개는 실제 독립 사건 0과 구별. 0=관측된 값일 때만, U=미확인, NA=적용 밖, VACANT=배정 전 공석.
- 합성 원장 worked-traces.csv 4행 ×26열, dictionary 65행 ×6열; 12 snapshot(3/case)·4 mock source fixture·78 unique event_id(K18/N21/R18/F21), 모두 synthetic, 실제 관측 아님. 4 case 모두 participant/assignment/session/artifact 및 3 checkpoint 해시 참조 대조 일치(12/12). SHA256은 합성 원문에서 산출, 외부 URL 실제 캡처 아님. 이벤트 시간·인수·labor는 가정. author/reviewer/acceptor 분을 각각 합하면 K15,N20,R17,F19 총71; 인수3은 가정. 가상 임상·개발자 모집/검수 아님.
- RESULT 첫 표 4행 6열, 둘째 표 4행 5열, Q1–Q7 7절, 마지막 약점 표 3행 4열 재판독. 첫 두 표 원행·계획 분모 일치, 링크/원장 source_id 연결 및 실패 경로 보존. scope 선행 봉인과 revisions correction 별도 커밋. 
- 완료 판단: 설계 범위만 DONE 후보. 하한을 엄격히 22로 보아도 충족. 실험의 실제 효능/인과/비용/독립 인수는 측정되지 않음. 후속 runner와 독립 코더는 아직 시행 전. 결과 SHA에서 재판독 및 경로 비교가 실패하면 PARTIAL로 변경한다.
