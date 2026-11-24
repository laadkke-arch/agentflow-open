| 표 1. 저장소·모집층 | 예정/실제 PR(개) | 본문+통합 대화 반환 / 전 스레드 완독 확인(PR) | 링크·이름만·무제안(잠정 PR) | 깊은 판독·공석 | 판독 불가/미확인 |
|---|---:|---:|---|---|---|
| pydata/xarray 본창 | 24/24 | 24/24 / 0/24 독립 완독 확인 | link 1(유추 포함), name 7, none 8, 후보1, 기타7 | 링크 자리1 후보+2 보류, 이름1 및 거절 후보1; 최초 diff 미완 | 통합 응답 댓글 211개, 일부 excerpt; edit/pagination 미확인 24/24 |
| scikit-image/scikit-image 본창 | 24/24 | 24/24 / 0/24 독립 완독 확인 | link 2, name 4(서식1 포함), none 2, 후보1, 기타15 | 링크 자리3 후보, 이름1, 거절1 후보; 최초 diff 미완 | 댓글 243개, 일부 excerpt; edit/pagination 미확인 24/24 |
| pydata/xarray 보충층 | 24/24 | 24/24 / 0/24 독립 완독 확인 | link 0, name 6, none 8, 후보2, partial1, 기타7 | 내부 링크 후보2 추가 관찰; 엄격한 공개기능 자리는 보류 | 댓글 589개; #9618 371개 중 첫 18 nonempty 관찰, #9636 첫16 등; 완독 미확인 24/24 |
| scikit-image 보충층 | 조건부/0 | 해당 없음 | 본창 2 link PR 잠정 충족 | 보충 미개시 | 엄격 재분류 결과 <2이면 다음 24 조사 |
| 합계(보충 포함, 추론 합산 금지) | 72/72 | 72/72 / 0/72 독립 완독 확인 | link 3, name 17, none 18, 후보4, partial1, 기타29 | 사건 원장 15행; 정규 10자리 모두 완결하지 못함 | 응답 1,043 댓글 수(완독 수 아님); 접근 자체 실패 PR 0, 개별 범위 결측 72 |

| 표 2. 사건·요구 조작 | 제안 전 SHA·구간 | 제안 URL·당사자·UTC | 응답과 첫 수정 SHA·구간 | 최종 상태·당시 사용 가능 범위 | 인지·귀속·경쟁 설명·미확인 |
|---|---|---|---|---|---|
| X-L1 #9580 날짜 해상도 문맥 | base 5c641821, 글로벌 설정안; 직전 tree 미확인 | [ChrisBarker-NOAA→kmuehlbauer](https://github.com/pydata/xarray/pull/9580#issuecomment-2395751675), 2024-10-07 02:07:47; decimal.localcontext | 동일 작성자 명시 답/첫 diff 미확인; head cecd5613 overflow hunk +244 | closed unmerged, #9618 후속; Python 3.10 context 존재, 날짜 연산 아님 | 유추이며 대체 계약 미입증; 이미 해상도 옵션 논의 |
| X-L2-C #9588 상속 좌표 시험 | original L1605–1612; exact SHA 미확인 | [TomNicholas→shoyer](https://github.com/pydata/xarray/pull/9588#discussion_r1790429869), 10-07 15:18:56; #9473 | [10-08 02:56:58](https://github.com/pydata/xarray/pull/9588#discussion_r1791110146) 이미 dedup 구현 설명, 최초 수정 미확인 | c057d13 merged; #9473 open 후 closed unmerged | 링크 후보(공개판 아님); 거절/보존 보고, 새 인지 아님 |
| X-N1 #9570 pyright 설정 | base e227c0bd; 기존 disable 의도 | [headtr1ck/benbovy→max-sixty](https://github.com/pydata/xarray/pull/9570#issuecomment-2390765468), 10-03 07:58:23; 이름만 | [10-04 02:54:46](https://github.com/pydata/xarray/pull/9570#issuecomment-2392698533); 최초 diff 미확인 | merged 98596ddd, 당시 구체 CLI 계약 미확인 | 선행 계획·CI 문제; 귀속 미확인 |
| X-N2 #9584 mypy stubs | pyproject original L128 | [max-sixty→hollymandel](https://github.com/pydata/xarray/pull/9584#discussion_r1788676646), 10-05 18:54:30; 이름만 | [18:57:35](https://github.com/pydata/xarray/pull/9584#discussion_r1788677201) fixed 보고; diff 미확인 | open draft, head fde2b3df; current docs 지원, 당시 버전 미확인 | 환경 수정 보고; 릴리스/노동시간 미확인 |
| X-N3 #9589 내부 parser | utils.py original L833; custom dim_arg_to_dims_set | [headtr1ck→shoyer](https://github.com/pydata/xarray/pull/9589#discussion_r1793907941), 10-09 17:33:07; 이름만 | [10-10 08:55:52](https://github.com/pydata/xarray/pull/9589#discussion_r1795004788) switch, 09:30:56 set 필요; 최초 SHA 미확인 | [707231e](https://github.com/pydata/xarray/commit/707231e3ae17d2dcb68975e5189c42421a88d0df) utils +832/+892, 시험; internal | 명시 수정+병합 hunk, 단 공개 링크 아님; 순서/메서드 요구 차이 |
| X-S1 #9627 보충 내부 효율 | base 0c1d02e0 | [TomNicholas→shoyer](https://github.com/pydata/xarray/pull/9627#discussion_r1802265485), 시각 미확인; 이전 #9470 | [응답](https://github.com/pydata/xarray/pull/9627#discussion_r1803419252) latest commit 효율; 첫 diff 미확인 | merged de3fce8; 공개판 계약 미확인 | 타 리뷰/선행 수정 경쟁 설명 |
| X-S2 #9636 보충 NodePath | base 8f6e45ba | [TomNicholas→shoyer](https://github.com/pydata/xarray/pull/9636#discussion_r1807438109), 시각 미확인; private NodePath pinned | [리뷰어](https://github.com/pydata/xarray/pull/9636#discussion_r1807439100) 이미 수정; 1f07b63 참조 diff 미실시 | merged e58edcc; 내부 경로 처리 | 수정 선행 가능, 동일 작성자 인지 미확인 |
| S-N1 #7566 footprint | original L102 custom wrapper, 분리안 선행 | [stefanv→lagru](https://github.com/scikit-image/scikit-image/pull/7566#discussion_r1786849807), 10-03 21:12:12; namedtuple 이름 | [10-04 13:19:15](https://github.com/scikit-image/scikit-image/pull/7566#discussion_r1787708163) own validator 제시, wrapper 뺄 예정; 첫 diff 미확인 | merged 4fb2464d; Python 3.10 namedtuple 가능하나 validation 다름 | 보존/거절 보고, prior plan |
| S-P1 #7589 원리 | base efe339b0 이미 Poisson 사용 | [jmtayloruk→Schefflera-Arboricola](https://github.com/scikit-image/scikit-image/pull/7589#issuecomment-2432000664), 10-23 12:31:25; 원리 link | [10-26 14:20:47](https://github.com/scikit-image/scikit-image/pull/7589#discussion_r1817859908) Wiki 이미 참조; 첫 diff 미확인 | 4678f1b L40–48; 원리/문서와 연산 별개 | 기존 인지 보고; 원리 후보 |
| S-L1 #7589 batch suggestion | PR iterative review, UI 이력 없음 | [mkcor→Schefflera-Arboricola](https://github.com/scikit-image/scikit-image/pull/7589#issuecomment-2444693290), 10-29 15:56:15; GitHub docs | 답과 실제 batch 사용 미확인 | merged 4678f1b; 권한 필요, 현재 docs | 같은 patch를 손으로 편집 가능; runtime 아닌 workflow |
| S-C1 #7576 sparse 반환형 | original L66; 10-15 min1.10 실패 보고 | [lagru→jarrodmillman](https://github.com/scikit-image/scikit-image/pull/7576#discussion_r1834941659), 11-08 19:26:55; SciPy sparse section | stefanv 19:34:41 및 19:47:58 flag 제안; 다른 actor, 최초 diff 미확인 | [14540c8](https://github.com/scikit-image/scikit-image/commit/14540c8d193c45b737454e4efa36fd35a930e6cf) graph +31/+69; matrix default, array opt-in, tests; SciPy>=1.11.2 | 시간적+타 actor 보호 변경; 직접 귀속 아님, 공개 버전 미확인 |
| S-L2-C #7589 Poisson 설명 | original L38, 기존 호출 | [mkcor→Schefflera-Arboricola](https://github.com/scikit-image/scikit-image/pull/7589#discussion_r1881529157), 12-12 07:41:40; NumPy doc | [12-13 16:40:58](https://github.com/scikit-image/scikit-image/pull/7589#discussion_r1884199771) done, first diff 미확인 | 4678f1b L40 Shot_noise 링크, L42 기존 함수; 2.0 doc, 1.24 floor 확인 필요 | 문서 수정 보고; 제안 URL 최종 미채택; runtime 귀속 금지 |
| S-L3 #7575 free-threaded wheel | base ef21164f; 2025-02-07 author 이미 조사 | [rgommers→jarrodmillman](https://github.com/scikit-image/scikit-image/pull/7575#issuecomment-2645983273), 2025-02-08 23:37:07; NumPy workflow | [23:59:01 다른 유지보수자](https://github.com/scikit-image/scikit-image/pull/7575#issuecomment-2645988481), #7699가 이미 02:04:21 생성 | 원 draft closed; #7699 merged 72eaa676, no-build-isolation/nightly 조건 | 다른 사람+선행; 소실된 CI log, 실제 후속 수정 귀속 미확인 |
| S-L4 #7589 clip | 03-07 normalization 질문; review tree 미확인 | [mkcor→Schefflera-Arboricola](https://github.com/scikit-image/scikit-image/pull/7589#discussion_r1996944730), 2025-03-15 15:00:46; fixed implementation | reviewer 시험 어두움 보고, 작성자 답 미확인, first SHA 미확인 | [4678f1b L45–48](https://github.com/scikit-image/scikit-image/blob/4678f1bdd55e24e5545b86107eae10cb89aa8095/doc/examples/filters/plot_deconvolution.py#L45-L48) normalization+default clip 유지; 0.24.x | 기능 존재≠동등한 출력; 보존 관측 |
| S-N2 #7579 dependency extra | [dff9fbd](https://github.com/scikit-image/scikit-image/blob/dff9fbd17dd4f3efcce6eeffab03b8b420602e44/pyproject.toml#L88) joblib 직접 | [stefanv→lagru](https://github.com/scikit-image/scikit-image/pull/7579#discussion_r1797237861), 10-11 17:20:02; 이름만 | [10-19 10:01:32](https://github.com/scikit-image/scikit-image/pull/7579#discussion_r1807278917) 명시 채택; [09b24f5](https://github.com/scikit-image/scikit-image/commit/09b24f5ccefc0e88d392c685d8e33a8f9776fa29) 3 files | 7649039 merged; sphinx-gallery v0.17.0 extra=joblib | 직접 귀속+정확한 hunk(이름만); prior parallel, 실제 배포/실행 미확인 |

| 표 3. 대상·시점 | 반환할 기능 절·보존 조건 | 채택·거절·유보 근거 | 관측 비용·단위 | 뒤집힐 관측 |
|---|---|---|---|---|
| 초기 설계자·문맥 스코프 결정 전 | decimal.localcontext 3.10 절 + Decimal 전용/복원; CF time에는 확인 질문 | X-L1 유추, 실제 대안과 다름 | 읽은 supplier 절 1; 답 간격 미확인 | 실제 CF API의 context override 계약 및 당시 판 발견 |
| 작성자·dependency 수정 전 | sphinx-gallery v0.17.0 parallel extra 한 절 + Python/floor/직접 joblib 의존 여부 | S-N2 이름만으로 이미 변경; 링크 효용 자체 미측정 | exact diff 3파일·dependency 선언 1조작; supplier metadata 1절; 7d16h41m30s 달력 답, 노동 미확인 | extra 이전판 미지원 또는 consumer 직접 joblib import |
| 기존 코드 유지보수자·sparse 전환 전 | SciPy sparse classes + dia_array/diags_array 버전 2절; default matrix 유지 및 array opt-in | S-C1 다른 actor 보호 hunk, 1.10 실패 보고 | floor+return type+operator+tests 별도; 21m03s 타인 응답, 노동 미확인 | 구판 계약상 배열 반환 허용 또는 별도 ABI 정책 |
| 예제 작성자·noise/clip 선택 전 | RL signature/clip 및 poisson lam; 값 범위와 scaling 확인 | S-L4 최종 normalization 유지, S-L2-C 문서만 | 최종 1파일; supplier 2절; 32h59m18s 문서 응답; clip 제안→merge 3d00h45m38s | 동일 PSF/입력/iterations에서 clip=False 동등 품질/범위 |
| 리뷰어·수정 적용 전 | GitHub batch suggestions 절 + 권한/conflict 확인 | S-L1 UI 사용 미확인 | 추가 절1; 달력/노동/클릭 모두 미확인 | batch commit metadata와 author acknowledgment |
| 구버전 사용자·wheel 지원 전 | pinned NumPy workflow + script 2절; Py_GIL_DISABLED, Cython nightly, build isolation 명시 | S-L3 대체 PR가 링크 이전 생성, 다른 actor | 타인 답 21m54s; 실제 노동/CI 비용 미확인 | 원작성자가 링크를 보고 처음 해결했다는 날짜 일치 hunk |
| 자료 편집자·정정 전 | 동일 표 ID/버전/항목 원표+정정판, 제보자 확인 분리 | C1·C2 변경은 보이지만 제보자 없음; C3·C4는 HMRC 표시 | C1 2판, C2 2판, C3 notice+bulletin 2저작; 노동 미확인 | 공지의 named reporter와 같은 셀의 즉시 수정판 연결 |

## 상태 및 요약

**PARTIAL.** 검색으로 사전 모집한 본창 48개와 xarray 보충 24개, 총 72개 PR의 번호/UTC/상태를 기록했다. 통합 대화 반환과 전 종류의 페이지 끝까지 완독을 혼동하지 않는다. 공개 링크를 받은 동일 작성자가 동일 실행 조작을 바꾸었다고 **현재 확인한 15개 사건에서 확증한 수 0건**, 그러나 적격 사건 전체와 비교 가능 분모는 미확인이므로 채택률 산출 불가. 링크가 무익하다는 결론도 아니다. 이름만 제안한 #7579의 명시 응답+정확한 commit, #9589의 명시 응답+merge hunk, #9584 환경 수정 보고가 대조된다. #7576은 링크를 근거로 반환형을 보존해야 한다는 타인 발언과 최종 보호 코드가 연결되며, 작성자 개인의 공로/인지와는 분리된다.

## Q1 모집

SCOPE.md의 첫 고정 커밋은 대화 판독 전 번호만 선정했다. repo/is:pr/created:2024-10-01..2024-10-31, created asc, 24 per repo. 검색 결과에서 생성시각 null이어서 PR metadata 재조회. 25번째 xarray 9615/scikit-image 7594. 시각은 각 층에서 오름차순이고 중복 번호 없음. 본창 X의 link 1, 후보 1로 엄격한 최소2 불충족 가능성이 커 다음 24번호를 별도 고정 후 조사; 본창 S의 두 linked PR이 관측되므로 보충 미개시. 단 전 스레드 완독 전 결정한 잠정 보충이므로 후속 완독으로 조건 재검산해야 한다. 본창·보충 효과 합산 금지. M=merged, C=closed unmerged, O=open: X 본 19/4/1, S 본 20/4/0, X 보충 23/1/0. 이는 연구 시점 원격 상태이지 생성 시점 상태 아님.

## Q2 판독 단위와 오탐

frame.csv의 screen_class는 PR별 1차 상호배타적 잠정 분류. name에는 내부/문서/서식 후보가 남고 none은 반환 excerpt에서 무제안이지 전체 스레드의 부재 증명 아님. X 본 기타7=self_issue2+self_name1+xref2+bot2. S 기타15=template6+release4+self_issue2+self_link1+self_name2. X 보충 기타7=xref1+bot2+self_issue2+self_name1+link_excluded1. #7580 noqa/formatting은 본문상 name으로 남기되 엄격 기능 이름에서 제외; X #9586 np.result_type은 기존 사용 및 upstream 변경 요청, #9598 문서 wording 등 별도 검토. #9588 미병합 #9473 링크 및 #9627/#9636 내부 링크 후보; 문서 링크인 #7589 NumPy Poisson은 이미 호출한 함수, 링크 대상 명칭과 실행 조작이 다름. #7566의 validator 링크는 작성자 자신이 붙였다. #9580의 decimal은 실제 기존 기능이지만 scope 유추. 각 사건의 발언 주소·역할·UTC(확인 가능한 시각)·공급 URL·대상 줄을 events.jsonl에 유지했다. 7 PR의 추가 thread query (#9589 3, #9588 6, #7579 3, #9584 7, #7589 13, #7566 10, #7576 14 threads)에서 줄·DB id를 얻었지만 원래 review commit은 반환되지 않았다. edited body/history, resolved/outdated 및 독립 페이지 끝 확인이 없어 분모 전체를 엄격 적격/비적격으로 확정 못했다.

## Q3 심층 자리(사전 순위와 실제 판독 구별)

| 저장소 | 예정 자리 | 잠정 배치 | 근거/공석 |
|---|---|---|---|
| X | link 1 | X-L1 #9580 | 유추, direct replacement 요건 보류; parent/first SHA 미확인 |
| X | link 2 | X-L2-C #9588 후보 | #9473 당시 unmerged, 엄격 공개판 자리 공석(잠정) |
| X | link 3 | 공석/미확인 | 보충 X-S1/X-S2 내부 링크; #9618 장문 미완독 때문에 확정 공석 아님 |
| X | name 1 | X-N1 #9570 | prior plan, exact first hunk 미확인 |
| X | rejection/no revision 1 | X-L2-C | 명시 보존 설명, 공개 링크 eligibility 미확인 |
| S | link 1 | S-L1 #7589 (10-29) | workflow tool, batch 실제 사용 미확인 |
| S | link 2 | S-L3 #7575 (02-08) | pinned recipe, 다른 actor 먼저 시작; S-C1 11-08 보호 경고 및 S-L2-C 12-12 문서링크는 별도 후보 |
| S | link 3 | S-L4 #7589 (03-15) | clip flag, 최종 default 유지; reviewer experiment 보고 |
| S | name 1 | S-N1 #7566 | namedtuple 거절/보존 보고, prior plan |
| S | rejection/no revision 1 | S-L3 또는 S-L4 | S-L3 타인 prior repair; S-L4 최종 보존; earliest explicit rejection 선정은 미완독 때문에 보류 |

위 순위는 관측한 UTC 중 구체 동작 링크의 잠정 순서이지 전체 모집창의 확정 순위가 아니다. 원리 링크 S-P1 10-23을 포함하면 S의 순서부터 바뀐다. strict 공개기능 정의 아래에서는 S-P1 일반 원리, S-C1 호환성 경고, S-L2-C 문서만을 분리했다. 한 PR 복수 사건과 동일 사례의 거절 자리 중복 가능 표시. #7579, #9584, #9589는 이름만 대조 추가 관측. 정확히 부모·수정·병합 파일 및 작성자 응답을 연결한 1/15 사건은 S-N2(이름만). 나머지 14건은 이 강한 관측 기준을 충족하지 못한다. GitHub compare에서 base/head/merge는 얻었지만 original_commit_id 및 first subsequent commit 목록은 미확인이다. 후보 #9473의 closed 여부를 조사했으나 모든 historical tree가 소실되었다고 단정할 수 없다.

## Q4 귀속

events.jsonl의 arrival / ack / first_learned / intent / changed / merge_release 여섯 칸을 독립 판독했다. 15행 중 확증한 최초 인지 0/15, 확인 불가 15/15. 직접 귀속+정확한 hunk nonlink 1(S-N2), 직접 보고+merge hunk nonlink 1(X-N3), 환경 보고만 1(X-N2), 문서 보고만 1(S-L2-C); rejection/preservation report 3(X-L2-C,S-N1,S-P1), retained final without direct 1(S-L4), other actor temporal hunk 1(S-C1), prior other actor 1(S-L3), not_verified 3(X-L1,X-S2,S-L1), unverified 2(X-N1,X-S1). 단위 사건, 중복 없는 15개. 명시 귀속 코드 변경 링크 0/15 관찰 원장; 실제 적격 링크의 확인 가능한 비교 분모 미확정. 별도 시간순 연관 S-C1 1/15(다른 actor)이며 S-L2-C 문서 보고·최종 문구 변경은 코드 연관 수에 더하지 않는다. 기타 첫 수정 미확인. 후속 커밋이 제안보다 앞서는 후보 S-L3(대체 PR가 링크보다 약21h33m 먼저), X-S2(리뷰어 보고) 적극 검사. S-N2조차 parallel 기능 자체는 제안 전에 택한 것으로, dependency 표현의 변경만 귀속. 이름 제안과 링크 제안의 비교 효과 실험 아님. 129의 후발 리뷰어 인지와 원작성자 인지 구별 원칙을 유지했다.

## Q5 당시 계약 및 경계 사례

contracts.csv 15행(14 사건 및 한 사건 DIA 별도 계약; S-P1은 Q7 아닌 원리 설명 사례로 Poisson 계약 S-L2-C와 공유, 독립 실행 동작 없음). 확인한 공급 version section과 consumer floor는 별도다. 예컨대 S-N2 당시 0.17 extra 실제 존재; 직접 joblib가 필요한 다른 코드가 없다는 조건. sparse SciPy 1.10 dia_array와 1.11 diags_array 도입 차이, 비주대각 padding, array *의 의미 변경은 단순 이름 치환을 깨는 반례. pixel_graph에서 default matrix를 유지하고 array 명시를 지원, invalid type ValueError 시험 hunk를 판독했다. S-L4 clipping은 output range, normalization은 input scale이므로 같은 조작이 아니다. Poisson nonnegative lam, int64 boundary, RL num_iter/clip 조건을 기록; 당시 numpy 1.24 공급 절까지 확인 못했다. namedtuple 자체와 validator의 역할, decimal scope와 날짜 dtype 차이, wheel isolation와 nightly Cython 설치 조건을 별도 기록. **실행: 미실시.** 실제 테스트 코드 판독≠시험 통과; #9584 fixed, #7589 dark output, #7579 사전 build 9→6분은 당사자 보고. 배포 포함 확인 미실시. 불충분한 계약은 미확인으로 기록, 정상/경계 입력은 실행 예측/반례이지 실측치가 아니다.

## Q6 언제 어떤 링크를 반환하는가

표 3은 **조사 결과를 적용한 설계 제안**이며 당시 당사자에게 실제로 전송한 실험이 아니다. 첫 설계 단계에선 후보 절 하나 + 전제 조건을 제공하되 질문의 조작이 모호하면 입력/반환형/보존 의무부터 묻는다. 이미 선택된 의존성과 구버전을 가진 유지보수자에게는 exact version floor·대표 입력/경계 입력·fallback/opt-in을 함께 반환해야 한다. #7579는 한 절의 작은 링크가 충분할 가능성이 있지만 이름만으로 실제 채택하였으므로 링크 추가효과를 주장하지 않는다. #7576은 동일 이름만으로 안전하지 않아 조건 링크/시험이 필요했다. #7589는 잘못된 대안을 적용하지 않는 보존 선택도 가치가 있다. #7575는 대안이 늦게 도착하면 기존 수정 여부를 먼저 확인; 리뷰어의 제안을 새 공로로 표시하지 않는다. 원장 cost는 달력 시간(답·병합 간격), 정확한 diff 파일 수 또는 aggregate 파일, 제안 당시 공개 절 수를 구별. 보고된 실제 노동 시간 0건 확인/15(값=미확인이지 노동시간 0). 3파일 exact hunk는 S-N2뿐; 9→6분은 사전 local build runtime 보고이지 링크로 절약된 사람 노동 아님. 읽기 절 수는 표 3에 이번에 확인한 절 수로만 기록, 당사자 읽은 절 수는 미확인. 구버전 사용자에게는 버전/보존 조건 없이 링크만 주는 자동 적용 금지.

## Q7 다른 분야: ONS 정정

evidence/hunks-and-corrections.md의 C1~C4는 PR 분모 밖. C1 동일 series G7G6 2022Q2 FTE SA 480→479 thousand를 원표와 현재판으로 확인, 공지 2022-09-13, 즉시 수정판/GB·UK 표제 차이 검증 미완. C2 같은 표 R68.8→R68, 건수 11,835/13,528/14,933, 비율 23.1/26.6/30.4%는 그대로, 2026-10-23 정정. 두 사건 모두 명시 제보자 없음(연락 담당은 귀속 증거 아님). C3 HMRC가 통보했다고 2025-10-08 공지가 명시; 10월 bulletin에 일부 수정 반영. 전체 £4.2bn revision 전부를 HMRC에게 돌릴 수 없음(다른 update 혼입). C4 별도 HMRC named notice에서 실제 같은 셀 전후판 미확인. 따라서 제보자 확인과 수정 확인은 두 축이다. 이 과제의 직접 인과와 같은 규칙으로, 수정판이 존재한다고 제보자의 전부 공로를 추정하지 않는다.

## 원전·한계

sources.jsonl 108행, 성공 표시 104, 실패 4. 보수적으로 minimum_count=true 35개 독립 work_id(중복 없음): 본창 PR 14개(X 6, S 8)+외부 비교 PR 2; version docs 7, tool docs 2, tagged metadata 1, deployment recipe 1; 소비자 지원 환경 2; 정정/공지/표/방법론 6(사건별 전후판 합산하지 않음). 직접 읽은 범위를 이 최소량으로 산입하되 완독과 당시 모든 버전 충족은 별도. 현재 docs 2개 및 방법론 1을 제외해도 32개 후보이고 PR 최소 12 및 각6, 독립 공급 자료 6, 환경 2, 정정 관련 4개를 넘는다. 전체 채택 수/PR 비율 분모는 확정 못함. 자료가 공개되어도 review tree·최초 hunk·원본 수정 이력을 복원하지 못한 것은 미확인이다. 72 PR 응답 총 댓글 1,043은 통합 반환량이며 pagination dedup/종류별 완독 집계 아님. 명시적으로 장문 일부만 읽은 사례가 남으므로 “직접 귀속 0건”을 모집창 결론으로 승격하지 않는다. 별도 reviewer session 및 정식 workbench check 미실시.

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
|---|---|---|
| 모집은 고정됐지만 전수 스레드·편집 이력 및 보충 조건은 미확정 | 72 PR 각각 REST issue/comments, reviews, pulls/comments 전 페이지와 thread replies 확인; #9618 등 장문 우선 | 더 이른 적격 링크 또는 동일 작성자의 직접 최초 인지/채택 발언 |
| 명시 답이 있어도 exact original_commit_id/first diff/당시 지원판 및 배포가 다수 결측 | review original_commit_id → commit 목록 → 부모/첫 hunk → release tag; 계약 경계 시험 | 링크 후 동일 actor·동일 조작의 최초 변경과 지원판 계약 동시 확인 |
| 다른 actor의 선행 수정·정정 공지와 원표 변경의 분리, 비용은 노동시간 미확인 | #7699 timestamp/actor, C1 즉시 수정판·C3/C4 같은 셀; 작성자 보고와 실측 별도 | 선행으로 보인 수정의 실제 후행 또는 named reporter+수정 동일 row, 실제 비용 기록 |
