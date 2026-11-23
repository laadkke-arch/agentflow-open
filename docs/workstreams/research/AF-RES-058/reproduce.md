# AF-RES-058 재현·분모 검산

## 1. 무엇을 재현했는가

실행 주체는 이 세션의 root, software_ir, adjacent, diagnostics AI 조사자다. 공개 저자 파일의 읽기·해시 확인·집계와 문서 간 산술 검사를 실제로 실행했다. 사람 실험, 저자 웹 앱 배포, 임상 모델 실행, 저자 R 회귀모형의 재적합은 하지 않았다. 파일 생성 성공과 여덟 연구의 정오별 수락 식별은 별개다. 원행은 ignored `_cache/`에서 읽었고 공개 산출물에는 개인별 응답 대신 URL·고정판·스키마·합계·재현 코드를 남겼다.

원 모집은 `SCOPE.md`, `frame.csv`, 압축된 `evidence/recruitment-A-snapshot.json.gz`, `evidence/recruitment-B-snapshot.json.gz`에 고정했다. ① 규칙·발견 목록·방법 선정 커밋은 `evidence/commits.csv`를 따른다. 압축 전 메타데이터 파일은 탐색 원장으로도 보존하며 외부 읽은 저작 수에 더하지 않는다.

## 2. 고정 입력과 실제 실행

| 자료 | 고정판·입력 | 실제 확인 범위 |
| --- | --- | --- |
| A01 검색 실험 패키지 | [4a308f7](https://github.com/bcbi-edu/p_eickhoff_transparent-ir/tree/4a308f735066b2741d2931cd0e5dc0d372f06429), ZIP SHA256 `c4a91787e7858d8f65fafd2b3dcd7a68978cd1c74d657d159ac119bf6b749db0` | 코드·배치 JSONL·저장 점수·조건 열 부재; 배포 당시 판은 미확인 |
| A01 Cranfield | [원 tar.gz](https://ir.dcs.gla.ac.uk/resources/test_collections/cran/cran.tar.gz), SHA256 `8c48a8412e4a7e6e0dd5af99c959f8d75fdf88135602adc1a56aa22770652d64` | README, query002, qrel, 제목 정확 대응; binary relevance 기준 미확인 |
| D01 Bansal 분석파일 | [6cebab4](https://github.com/uw-hai/Complementary-Performance/tree/6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f), `decision-result-filter.csv`, SHA256 `0cc48875d451e095db8307e7b2cf616d5ad2277e200c8d2579e07db174c1f9f0` | 66,040 공개 기록, 키 중복, 같은 행의 정답·권고·최종 답 |
| D01 필터 전 파일 | 같은 판의 `decision-result-prefilter.csv`, SHA256 `1074a05e0a4f113a1f8b8bfe8a887f455ad57dec5a4838fbe5357c85e3e84af6` | 68,810 기록; 필터 전후 감도. 전체 원배정 명단이라는 뜻은 아님 |
| D04 Lai 분석파일 | [7c5ae6b](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285), `label.jsonlist.gz`, SHA256 `d3616e73d4db03d6e21f574246d318e7f0300facdfe6ff88aa2630cef8364c5f` | 14,400 기록, 권고 없는 6,400 기록 구별, 두 조사자의 별도 집계 |

개별 PDF·OSF 등록·저자 도구의 해시와 읽은 절은 `sources.jsonl`의 `version_date_or_hash`, `read_utc`, `locations`, `scope_and_limits`를 따른다. 원본 URL에 immutable SHA가 없는 경우 취득 시각과 바이트 해시를 고정판의 대용으로 기록했으며 최신판 전체를 검증했다는 뜻은 아니다.

저장소 최상위에서 실행한다. 아래 명령들의 입력은 모두 위 고정판 또는 소유 경로의 원장이다.

```bash
python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/reproduce_diagnostics.py --download
python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/sensitivity_prefilter.py
python -B docs/workstreams/research/AF-RES-058/streams/root/verify_lai_and_bounds.py
python -B docs/workstreams/research/AF-RES-058/streams/adjacent/audit_checks.py
python -B docs/workstreams/research/AF-RES-058/assemble_ledgers.py
python -B docs/workstreams/research/AF-RES-058/assemble_outcomes.py
```

이번 diagnostics 집계는 이미 취득한 동일 해시의 파일로 `--download` 없이 실행했다. 캐시 없는 재현자에게만 `--download`가 필요하다. 세 명령의 실제 실행 receipt는 각각 `streams/diagnostics/execution.json`, `sensitivities-prefilter.json`, `streams/root/independent-calculation.json`이다. adjacent 검사의 실제 산출물은 `streams/adjacent/arithmetic-check.json`이다. A01 두 감사 명령의 전체 인자와 실행 UTC는 `streams/software/reproduce.md`, `package-audit.json`, `cranfield-audit.json`에 있다. 재실행하면 실행 UTC가 바뀌므로 기존 고정 커밋과 비교할 때 수치와 입력 해시를 대조한다.

## 3. 연결 키와 계산식

권고 수락은 `final = recommendation`, 최종 정답은 `final = truth`다. 개인의 신뢰도 설문, 정확도 평균, 권고 쪽으로 움직인 연속 정도, 설명 클릭은 이 정의를 대신하지 않는다. `D(c,g)`는 조건 c에서 권고 정오 g를 판정할 수 있고 최종 답을 관측한 기록 수, `A(c,g)`는 그중 최종 답이 권고와 같은 수, `C(c,g)`는 최종 답이 정답인 수다. 실제 원배정 분모와 공개 분석 파일의 D는 별도다.

```text
D(c,g) = Σ 1[condition=c AND (recommendation=truth)=g AND final observed]
A(c,g) = Σ 1[위 조건 AND final=recommendation]
C(c,g) = Σ 1[위 조건 AND final=truth]
O(c,wrong) = Σ 1[위 조건 AND final≠recommendation AND final≠truth]
ΔA(g) = 100 × [A(intervention,g)/D(intervention,g) − A(control,g)/D(control,g)]
```

정권고에는 A=C, 오권고에는 A+C+O=D가 성립한다. 이진 강제 선택에서만 O=0이어서 오권고 거절이 최종 정답과 같다. 건너뜀·철회는 O에 넣지 않는다. D01의 Human은 AI 예측 열이 있어도 권고가 화면에 제공되지 않았으므로 수락 A는 해당 없음이다. 해당 파일의 reference-model 정오층별 인간 정확도만 남긴다.

D01은 같은 행의 `task, condition, assignmentId, questionId, pred, y, choice`로 센다. questionId가 원 자극 ID라는 보장이 없으므로 자극 목록과 순서대로 결합하지 않는다. D04는 같은 행의 `experiment, anonymized_worker_id, review_num, predicted_label, actual_label, user_label`을 쓴다. 리뷰 본문 해시는 조건 간 동일성 감사에만 사용한다. 원래 최초 자기 답과 열람 로그는 두 패키지에서 복원하지 못했다.

배정은 사람 단위이고 한 사람의 여러 시행은 독립 사람이 아니다. 이 문서의 비율 차이는 공개 기록의 기술 통계다. 사람 군집과 항목 효과를 무시한 새 유의성 검정·신뢰구간은 만들지 않았다. 연구 간 분모·정답 비율·모집단도 합치지 않았다.

## 4. 공개 원행 및 저자 그림 손검산: D04

[저자 고정 데이터](https://github.com/vivlai/deception-machine-in-the-loop/tree/7c5ae6bb4b7dcd5613e620e4731b9c3c67ed8285)와 [논문 v4 Fig3/4](https://arxiv.org/pdf/1811.07901v4)를 대조했다. 정수는 원행에서 셌고 반올림된 그림에서 역산하지 않았다.

| 조건 | 정권고 수락 | 정권고 거절 | 정권고 D | 오권고 수락 | 오권고 거절=최종 정답 | 오권고 D | 전체 최종 정답 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| machine | 908 | 487 | 1,395 | 123 | 82 | 205 | 990/1,600 |
| machine_and_heatmap | 1,107 | 288 | 1,395 | 152 | 53 | 205 | 1,160/1,600 |

분모부터 더하면 각각 80개 익명 사람 키×20행=1,600, 1,395+205=1,600이다. 정답 수는 908+(205−123)=990, 1,107+(205−152)=1,160이다. 따라서 전체 정확도는 61.875%→72.5%(+10.625pp), 맞는 권고 수락은 65.0896%→79.3548%(+14.2652pp), 틀린 권고 수락은 60.0000%→74.1463%(+14.1463pp)다. Fig3의 61.9/72.5, Fig4의 60/74.1과 반올림 범위 안에서 일치한다.

이 자료는 **전체 정확도 상승과 오권고 거절률 하락이 동시에 가능함**을 보인다. 맞는 권고 수락도 상승하므로 모든 식별 지표가 악화됐다고 주장하지 않는다. 예컨대 정권고 수락률−오권고 수락률의 차는 약 5.09→5.21pp로 조금 늘어난다. 원래부터 AI와 같은 답이었는지, 설명 때문에 답을 바꿨는지는 초기 답 부재로 구별할 수 없다.

저자 페이지의 2019-01-10 이전 코드 오류·재실험 공지를 별도 읽었다. 현재 패키지와 논문 v4의 대응은 위 수치로 확인한 범위이며, 과거 모든 배치의 교체 내역까지 확인한 것은 아니다. 공지·재게시·같은 참가자 재분석을 독립 실험으로 세지 않았다.

## 5. 제3 오답과 필터 감도: D01

LSAT `Single` 오권고층은 358 수락+300 최종 정답+49 제3 오답=707이다. 거절 349건 모두를 정답으로 세면 49건을 잘못 더한다. `Conf.`는 331+338+45=714다. Single−Conf.의 오권고 수락 차는 358/707−331/714=+4.2779pp, 최종 정답 차는 300/707−338/714=−4.9061pp다. 두 차가 반대 부호라는 사실만으로 절댓값까지 같다고 놓을 수 없다.

Beer에는 200개 중복 키 그룹에 400행이 있고 일부 최종 답·시간이 다르다. 주 집계는 저자 필터 파일의 모든 기록(66,040), 감도는 모호한 키의 400행을 모두 제외한 집합(65,640)이다. 임의 first/last 선택은 하지 않았다. Amazon/LSAT에는 이 모호성이 발견되지 않았다. 감도를 독립 코호트로 더하지 않는다.

필터 전후 `Single−Conf.`를 같은 정의로 따로 계산한 결과, 정권고 수락 차의 부호가 Amazon −0.09785→+0.49997pp, Beer +0.30400→−0.07302pp로 바뀐다. 이것은 작은 기술 차의 필터 민감도이지 유의한 방향 전환의 증거가 아니다. 오권고 수락 차는 Amazon −5.19737→−4.56283pp, LSAT +2.92503→+4.27795pp, Beer +4.70426→+5.48937pp였다. 정확한 원개수·해시는 `streams/diagnostics/sensitivities-prefilter.json`에 있다. 이미 관측된 제외 전 응답을 결측이라고 가정하지 않았다.

## 6. 선정 연구의 계획 분모와 불가능한 칸

| 연구 | 손으로 확인한 수·산식 | 왜 정오별 A/D가 되지 않는가 | 다음 최소 입력 |
| --- | --- | --- | --- |
| A01 | 저자 perceived-truth 긍정 TAB36/50, TA24/50, T33/50; 559 bookmark·459 quiz·67 exit 기록; 67 exit ID는 같은 batch의 두 표와 연결 | 신뢰 설문은 수락 종점이 아님. 배정 조건·전체 노출 후보·순위·당시 판 없음. 150−67을 결측으로 볼 코호트 대응도 없음 | 배포 SHA와 조건 배정·impression·docID·분석 포함표 |
| A02 | 접근 가능한 저자 poster의 A–F 여섯 화면, 후보10 중 관련 문서 하나 찾기 요청(유일한 정답인지 미확인) | N·정답키·배정 순서·최종 선택표 미확인. 한 화면의 동일 제목은 전체 항목 동일성을 입증하지 않음 | 정식 본문 및 사람×과제×조건·정답·최종 선택 |
| B01 | 31−1−2=28명; 분석 후 설계 각28시행; 오권고는 설계상0 | WOA 중앙값 .31/.00은 최종 답=권고 횟수가 아님. 모든 권고가 맞아 오권고층 비율은 해당 없음 | 환자 키·I/A/F·환자 정답·이산 채점 규약 |
| B02 | Control100, Feature99; 각16시행 중 정/오8 설계 →800/792씩 | 계획 곱셈이고 원행 수 아님. RAIR/RSR은 초기 불일치의 서로 다른 분모에 한정한 평균 | 초기 답·권고·정답·최종 답의 공동표, 정정 VoR |
| B03 | Table1 정8+오6=14; 동수 배정 계획200/군 →정1,600/오1,200 | 본문 전체14분모 주장과 Fig3+5의 정권고몫50%가 충돌. 8/14=57.1429%와 반올림으로 양립 불가 | Fig3/5 포함 마스크·가중 규칙·군별 정수 교차표 |
| B04 | 포함85×조건별20, 정70% 설계 →정1,190/오510 | 실제 배정/완료/결측을 센 수가 아님. Fig6은 모형 예측률이며 곱셈으로 정수화 불가 | 사람×영상×finding×기간×조건×응답 및 전문가 키 |

A01 원문 relevance도 일부 복원했다. query002의 qrel25행은 등급1:2, 2:5, 3:13, 4:4, −1:1이다. README에서 −1의 뜻을 확인하지 못했고 미등재 문서를 모두 오답이라고 놓지 않았다. bookmark 제목143종 중142종은 정규화 후 단일 corpus 제목과 맞고1종은 다중 대응이다. 이 연결만으로 화면에 노출된 D나 relevance의 이산 기준은 생기지 않는다.

## 7. 주변수 비식별성과 결측 범위

`streams/root/independent-calculation.json`의 두 가상 세계는 각 조건 N=100, AI정답80/오답20, 최종정답80을 고정하고도 오권고 수락 차가 +80pp/−80pp일 수 있음을 보인다. **실제 관측이 아니며 AF054의 계산을 다시 수행한 것도 아니다.** 이 반례는 총수락 수를 고정하지 않는다. 이진 강제 선택에서 총수락 T까지 알려지면 오권고 수락은 `(T+Nwrong−C)/2`로 식별되므로 그 경우까지 불가능하다고 일반화하지 않는다.

세 선택지 이상에서는 오권고 거절 후 제3 오답이 있어 총수락까지 같아도 식별되지 않을 수 있다. `streams/software/three-choice-diagnostic.json`은 N100·정권고50/오권고50·총수락60·최종정답60을 고정한 대조와 두 가능한 개입표를 보인다. 대조의 정권고 수락40/오권고 수락20, 세계Ⅰ45/15, 세계Ⅱ35/25이므로 정권고 수락 차는 +10/−10pp, 오권고 수락 차는 −10/+10pp다. 이는 논리 진단이며 읽은 외부 저작·관측 셀·연구 수에 넣지 않는다.

정오층별 미응답 m과 관측 A,D가 알려지고 빠진 응답의 권고 정오가 이미 정해져 있을 때만 해당 층 수락률의 최악–최선 범위는 `A/(D+m)`–`(A+m)/(D+m)`이다. 두 조건 차의 범위는 개입 하한−대조 상한에서 개입 상한−대조 하한이다. 현재 선정 연구는 D/A 또는 m이 없으므로 수치 구간을 제시하지 않는다. 자료가 주는 제한이 없는 확률의 논리 범위 [0,1], 차 [−1,1]은 유익한 관측 추정구간이 아니다. 원래 배정표가 없는 공개 파일 내 결측0을 전체 연구의 결측0으로 바꾸지 않는다.

## 8. 원장·필수 표 재생성과 검사 범위

`assemble_ledgers.py`는 선별 원순번, 계보별 고유 저작, 출처, 자극을 통합한다. `assemble_outcomes.py`는 실제 원개수, 계획 분모, 저자 모형 예측률을 별도 필드에 보관하고 결측 행을 추가한다. `outcomes.csv`의 `source_file/source_row`와 `contrasts.csv`의 같은 열은 사람이 읽을 수 있는 1부터 시작하는 원장 행 위치다. CSV의 `미확인`과 JSON의 null은 숫자0으로 바꾸지 않는다.

`RESULT.md`의 첫 표는 여덟 고정 자리를, 둘째 표는 각 조건의 정/오층·조건차·결측을 보인다. 빈 A03/A04는 미실시이지 음성 연구가 아니다. 수치가 없는 이유와 요구되는 입력은 각 행의 source와 이 문서의 표를 따른다. 최종 고정판 재열람·workbench 계약 검사는 `evidence/final-verification.json`과 마지막 `HANDOFF.md`에 실제 실행 후 기록한다. 이 문서 작성 시점에 실행하지 않은 검사를 미리 통과했다고 표시하지 않는다.
