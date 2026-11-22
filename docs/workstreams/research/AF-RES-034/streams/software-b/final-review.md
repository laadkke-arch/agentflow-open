# 통합 결과 B 연구군 검토

검토일: 2026-11-22 UTC. 검토 시 저장소 HEAD는 `f31b498c56dc9f06f76a163d0601280df0704f7a`였다. 통합 `RESULT.md`, `measures.md`, `future-study.md`, `studies.csv`, `effects.csv`의 작업트리를 읽고 B의 고정 원장 및 임시 보관한 원문 Methods/결과와 대조했다. **통합 파일은 수정하지 않았고 이 파일에 문제와 수정안만 남긴다.** 같은 B 추출자의 자체 재검이므로 독립 판독으로 세지 않는다.

## 결론

**핵심 서술의 숫자·분모·효과 방향에서 결론을 뒤집는 오류는 발견하지 않았다.** NCQ 두 코호트와 고정 순서, 단계별 중앙값과 총시간, Acar의 분석 인원/반복시행/조건부 보안, eXoaDocs의 완료자 조건부 시간, Prompter의 고정 예산 품질을 적절하게 구별했다.

우선 수정할 것은 **통합 CSV의 대표 필드 누락 두 종류**다. 값은 `detail_json`과 분지 원장에 보존돼 있으므로 새로운 추정 없이 매핑을 고치면 된다. 그 밖에 원 단위 구분·ID 연결·짧은 표현을 고칠 수 있다.

## 수정 제안

| ID·우선도 | 위치·현상 | 근거·영향 | 수정안 |
| --- | --- | --- | --- |
| BREV-01 · 높음 | `effects.csv` SWB-E13~E16의 `original_values`에 원보고 값이 없다. E13/E14는 `{}`, E15/E16은 단위만 있다. E15/E16의 `recalculation_inputs`는 `{}`, `recalculated_result`에는 근사 구간이 없다. | 원장 `effects.jsonl` 13~16행의 `original_report`/`recalculated_interval`은 통합 `detail_json`에만 남았다. 대표 열만 읽으면 실제 재계산 입력과 산출 구간을 재현할 수 없다. | `original_report`를 `original_values`에 병합하고 E15/E16의 계수·SE를 `recalculation_inputs`에, `recalculated_interval`을 `recalculated_result`에 포함. 아래 정확값 참고. `original_counts`도 E04 원값에 보존하면 1/12·3/12의 분자와 분모가 명시된다. |
| BREV-02 · 높음 | `studies.csv` B 15군행 모두 `arm_trials`가 빈칸이며 NCQ 4군행의 `time_result`가 `{}`다. 원 `median_total_seconds`/`median_final_package_seconds`가 `quality_result`에만 담겼다. | Acar `trial_n`, Prompter/NCQ `n_trials`가 원 arm에 있다. 통합 대표 시간·시행 열이 실제 미보고처럼 보인다. | `trial_n`/`n_trials`를 `arm_trials`에 매핑. Acar SO/공식/책/자유=52/52/56/56; Prompter=12/12; NCQ 각 실험=10/10. NCQ 원 시간 필드를 `time_result`로 옮기거나 복사. eXoaDocs 48/48, REST80/50은 **배정 과제기회 유도값**이므로 실제 시도수처럼 무표시 입력하지 않는다. |
| BREV-03 · 보통 | `effects.csv` SWB-E08/E09의 `original_values.unit`가 `percentage points`다. 이는 B 원장의 단위 표현을 그대로 옮긴 것이다. | 원 Prompter 평균70/46 및 중앙68/40은 **완성도 percent(%) 수준값**이고 차이24/28만 percentage points다. `RESULT.md`의70/46%와+24%p는 맞다. [원문 §4.4, 저자 PDF p23](https://lucaponzanelli.gitlab.io/assets/publications/Ponz2015c.pdf). | 원값 단위 `percent`와 차이 단위 `percentage_points`를 분리한다. 비율1.5217/1.7과 상대 변화52.17%/70%는 차이24/28%p와 구별해 유지. 원장 수정 시 phase3 이전판을 보존하고 BREV-03을 수정 사유로 기록. E08 분모 `24pairedtasks`도 `24 task executions, 12 paired participants`로 명확히 하면24쌍으로 오독하지 않는다. |
| BREV-04 · 보통 | B 효과16행의 `study_id`가 전부 빈칸이고 `claim_ids`가 `[]`다. source ID와 family는 정확하다. | 특히 NCQ는 같은 family의 독립 실험2개이므로 family만 조인하면 효과가 어느 코호트인지 자동 구별되지 않는다. 빈 claim 배열에 대한 조인 검사는 연결 완전성을 확인하지 않는다. | E01~04→SWB-EXO-1; E05~07/E15~16→SWB-ACAR-1; E08~09→SWB-PROMPT-2; E10→SWB-NCQ-1; E11~12→SWB-NCQ-2; E13→SWB-REST-1; E14→SWB-STRATH-1. `claim_ids`는 출처의 C-SWB-EXO/ACAR/PROMPT/NCQ/REST/STRATH를 해당 행에 연결하거나 통합 주장 ID와 명시적으로 매핑. |
| BREV-05 · 낮음 | `RESULT.md` Acar 행의 `56수행−2제외`, `measures.md` §2의 `56명 수행 중2명 제외`. | 원문 §V-A는56명이 lab study에 참여했고 한 명은 **과제 수행을 거부**하여 제외됐다고 말한다. 56명이 모두 과제를 수행했다고 읽히는 표현은 과하다. [Acar §V-A, p295](https://userlab.utk.edu/files/papers/kim/2016/acar2016you.pdf). | `56명 참여/등록 중2명 제외→54명 분석,216시행`으로 표현. 전체 배정224시행은 관측값으로 새로 채우지 않는다. 현재 `people_enrolled=56`, `people_analyzed=54`는 맞다. |
| BREV-06 · 낮음 | `RESULT.md` 필수 표2 NCQ 행의 `Swb-A02~04는snippetraw`. | A02/A03은 CSV 원자료이고 A04는 **lint 분석 절차 코드**다. 본문 원산출물 절과 `measures.md`는 이 구분을 이미 맞게 썼다. | `Swb-A02~03은 snippet CSV, A04는 lint 분석 코드; 사람 시간 raw 없음`으로 좁혀 쓴다. |
| BREV-07 · 보통·미시행 설계 보완 | `future-study.md` §2는 성공시간을 성공 사건과 행정적 검열로 분석한다고 한다. 자발적 포기·확정 실패가 행정적 종료와 어떻게 달라지는지 분석 규칙은 미지정이다. | 이미 문서가 실패·철회·상한을 별도 기록하고 전체 배정자의 품질을 공동 지표로 두므로 방향은 좋다. 다만 빠른 실패/포기를 모두 비정보성 우측 검열로 분석하면 성공시간이 낙관적으로 보일 수 있다. | `예산 상한의 행정적 종료와 자발적 포기/확정 실패를 구분하고, 후자는 단순 독립 검열로 가정하지 않는다. 제한시간 내 성공확률·실제 소비노동·실패 상태를 공동 보고하며 분석법/민감도는 사전 고정한다` 한 문장을 추가. 이는 외부에서 관측된 효과가 아니라 제안 설계의 미지정 규칙이다. |

### BREV-01·02의 정확한 입력

| 행 | 원보고/재계산 값 또는 군별 시간 |
| --- | --- |
| SWB-E13 | `time_Wilcoxon_p=0.051`, `API_trials_Wilcoxon_p=0.017`, `success_Fisher_p=0.0003`. 군별 정확 평균을 새로 추정하지 않는다. |
| SWB-E14 | `success=7`, `partial=1`, `trials=8`, `people=2`. 대조군 시간효과 없음. |
| SWB-E15 | 공식 대SO 기능: beta=−1.535, SE=.634, 원 OR=.215, p=.015. `exp(beta±1.96*SE)`=[.0621850912,.7464997477]. 원보고 CI가 아닌 반올림 입력 기반 비보정 근사95%Wald 구간. |
| SWB-E16 | 공식 대SO 기능성공자 조건부 보안: beta=2.218, SE=.796, 원 OR=9.184, p=.005. 동일식=[1.9306176932,43.7354943451]. 위험차 CI가 아니며 기능성공122시행의 반복측정 모형. |
| SWB-NCQ-1-A1/A2 | NCQRetrieval `median_total_seconds=748`; NCQBasic+Web=936. 각10시행/10사람, 전원 완료. |
| SWB-NCQ-2-A1/A2 | NCQ `median_total_seconds=847`, `median_final_package_seconds=57`; VSCode+Web=849/380. 각10시행/10사람, 전원 완료. |

## 확인된 주요 항목

| 대상 | 검토 결과 |
| --- | --- |
| eXoaDocs | 24사람/12+12, 96과제기회, 40분, T1 880→533초와−347초·−39.43% 일치. 시간표의 완료자 n 미공개, 테스트통과 전체3/12 대1/12, T3의3/12 대4/12도 일치. 전체 배정자의 동등품질 노동효과로 확대하지 않음. |
| REST | 26사람·16/10, 본과제5개/연습별도, p시간=.051을 유지. API호출·부분성공·미시도와 사람 시간을 구별. 군별 시간 원평균은 미확인 그대로. |
| Acar | 분석54명·216시행, SO/공식13사람·52시행씩,35/52 대21/52 기능,18/35 대18/21 조건부보안,18/52씩 joint 결과 모두 일치. Q 판정·동률의 비등가성·2명 제외 한계 유지. |
| Strathcona | 2사람·8시행 단일군,7성공·1부분성공,3시간 예산,서버4–12초를 사람 시간에서 제외한 해석 일치. |
| Prompter | 12사람·24산출물, 조건/과제/순서 균형,90분 고정,70/46% 평균·68/40% 중앙,유지보수 p=.23 일치. 실제 절감 분으로 변환하지 않음. |
| NCQ | 별도10명 코호트2개,총20사람·40시행,baseline 항상 먼저. 연구1−188초,연구2 총−2초/선택−323초가 모두 군중앙 차이이며 paired 개인차의 중앙/평균이 아님을 유지. 단계 중앙을 차감해 나머지 노동을 만들지 않음. |
| NCQ A01 | 저자 고정 commit 조작 지시문이며 실제 실험 제공판 동일성 미확인. 실험 전용 protocol로 과장하지 않음. 이를 엄격 제외할 때 전체 산출물7개라는 민감도 적절. |
| NCQ A02/A03 | 저자가 원래 분리한2코호트 snippet CSV. 사람시간 raw로 세지 않음. P ID 재사용을 동일 사람으로 합치지 않음. |
| NCQ A04 | 원 lint 분석 코드로 두 파일의 first/second study 대응 확인. 독립내용의 분석 절차로 산입하되 원 분석 실행/시간 재현을 주장하지 않음. |
| 미시행 비교 | 자유검색 대 목적·근거 링크, 병렬 무작위, 사전지식·동일요구·공동품질/시간·채택후 추적·자료제공 비용 구분이 B 연구의 주요 결함을 반영한다. 제안90/60분·60명·약63/군을 관측수치와 혼동하지 않는다. |

## 검토한 통합 파일의 SHA256

아래는 검토 당시 작업트리 bytes의 해시다. root가 수정하면 새로운 해시가 되는 것이 정상이며 이 리뷰는 아래 판에 대한 기록으로 남긴다.

| 파일 | SHA256 |
| --- | --- |
| RESULT.md | afaa1a8e88c3d04ad207190333b2819d7e41e31297f1953b7d8c8432ff9490da |
| measures.md | 3506e55834b7c4a22ef5c94176ef33e2743540112b1d4482c4f0f49ea1b3e7f2 |
| future-study.md | cde6e5e9b8419fce71a45e257fee8a6203b0308f46f2ba84bf65f272b1064141 |
| studies.csv | 36d95b3afe8cc80219197e17cf0ca8dcf113c8bb1a27e7e7ffc71527f7946988 |
| effects.csv | 7489d20fa259af089cd82a92eee59d709206c653bcd9e303ed39a5d6c93a6734 |
