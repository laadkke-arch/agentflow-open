# AF-RES-069 · 자체 점검

**연구 수용 상태: PARTIAL.** 기록 검사가 통과해도 최초판·동일 실제 비용·대상 실행 미확인을 완료로 바꾸지 않는다. 현재 문서는 결과 묶음의 검사 상태를 적고, 마지막 HANDOFF에는 최종 GitHub 재열람과 정확한 검사 HEAD를 덧붙인다.

## 1. 동결, 경로, 계보

| 항목 | 확인된 기록 | 한계 |
| --- | --- | --- |
| 실제 시작판 | foundation76b8c1d15812fbf91b879f8444fd188ae7445802 | 계획판320424d8…과 분리 |
| 선행 | AF-RES-065 HANDOFF@18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d | 선행의 후보·과거 결과 미열람 |
| 첫 모집 봉인 | c5b0410ef23fa44fdc3c4129682f9a468330b783 | 동일 tree의 로컬 commit 뒤 본문 독해, 원격 발행 완료 전 |
| 입력·양갈래 질의 봉인 | 03d1e436cfa7dc209b57b19508ef4b2e75942824 | 최초판3건 모두 미검증 |
| 원실험 봉인 | de1727aada52835ebcde4ff1c92c3940db215476 | 이후 sources는 사후 기록만 append; 원질의·순위·판정 불변 |
| 편집 경로 | docs/workstreams/research/AF-RES-069/ | dot-control 및 다른 작업 브랜치 변경 금지 유지 |

## 2. 수량과 분모

모집75행, 관측 문제3, 엄격 문제0, 질의18, 원순위90, 최초 접근30, 본문을 읽은 대표 URL27, 반환 canonical URL76, 직접 읽은 반환 계보18/반환 계보52다. 독립 최소수25=선정3+선별6+반환 신규16이며, 사후 FAA2문서를1관련 계보로 추가해26이다. sources99행을 독해99건으로 해석하지 않는다.

확정 적합은 A만0/B만0/공통0/둘 다 미확정3이다. 엄격층0은 빈 분모이며, 관측층에서 적합0과 다르다. 미열람·접근실패는 부적합 증거가 아니다. 전체 웹 재현율·원 개발자 선택 변화·채택·시간 절감·금전/토큰 비용은 미측정이다. 연구 연산58=A25+B33으로 동일 비용 비교는 미달이다.

## 3. 세부 질문과 반례 연결

| 질문 | 결과 행 | 근거 절·원행 | 반례 선정과 판독 | 남은 원자료 |
| --- | --- | --- | --- | --- |
| Q1 | 표1, Q1 | RQ-F1-01 L47–59; RQ-F2-04 L3–69; RQ-F3-03 L8–32 | 고정 순번 탈락 기록; 사후 P2반품 | 최초판·T0 상태·bot 확인 |
| Q2 | 표2, Q2 | problems 삭제/보존 필드; IA-01..04 | 첫5의 records→행정 기록, leaf→결정 결과 | 새 표현은 새 봉인 필요 |
| Q3 | 표2상세30행, 원장90행 | runs 중복·source direct_read·classification | 제품 요약/403/판독 불가와 alias를 수량에서 분리 | 미열람 반환 원문 |
| Q4 | Q4, D03/D04 | B-P2-S01..05; B-P3-S04의 절 | 역할/변수/목적이 다른 실제 반환 원문을 기각 | target protocol/adapter |
| Q5 | Q5, SR-01..04 | TreeView/ColumnView/특허/Tarkan §2.2.5/8 | 다른 위젯, 셀/머리글, 원리/성공 차이 | 같은 revision과 실행 관측 |
| Q6 | Q6, 상세30행 | 각 minimal_rejection_counterexample | True lock/leaf echo/Children/두 줄 잘림 | resume-checks의 환경·입력 |
| Q7 | 표3, Q7 | counts/costs/ledger-audit | URL27과 별칭28 구별; 미확인 순위 정의 분리 | 동일 총비용 실험·미측정 지표 |
| Q8 | Q8, PS-* | 작성자 댓글·PR patch·P2반품·P3실패 | 봉인 후 대상 전체 반환 댓글을 읽어 신규성·진행 중 가정 반박 | P3 notes/편집 이력·날짜 있는 채택 기록 |

기계 판독 가능한 상세 연결은 [question-coverage.json](evidence/question-coverage.json)에 있다. 각 질문마다 결과 위치, 원행 ID, 직접 읽은 절, 반례 선정 경로·판독 결과, 미확인과 재개 원자료를 넣었다.

## 4. 판독 주체와 가림

A/B는 같은 모델의 별도 문맥이다. 후보를 상대에게 전달하지 않았지만 공유 파일시스템의 접근 차단은 아니었다. root는 양쪽을 아는 모집·통합 판독자다. 선정 감사에는 root 잠정 판단이 전달되었다. 사후 의미 판독자는 기존 점수를 보지 않은 별도 문맥이지만 같은 모델이며 사람은 아니다.

A-P1 자동 반환의 PR 포인터와 도구가5자리를 넘게 반환한 노출을 기록했다. 봉인 전 댓글/연결 PR 본문을 의도적으로 연 호출은0이다. 모델의 학습 노출을 배제할 수 없으므로 절대적 새로움을 주장하지 않는다.

## 5. 실제 검산과 수정 이력

독립 원장 감사는 봉인 de1727aa…의41항목을 검사하여 **실제 종료0**이었다. 표23열,90판정행, source/rank/cost 조인,58연산, URL27/76, 계보18/52, 최소25가 맞았다. 과거649638c… checkpoint에서는 A JSONL 끝 빈 줄4건 때문에 감사 종료1이었고, 이를 보존한 채 최종 봉인 전에 빈 줄을 고쳤다. [first-arms-audit](evidence/first-arms-audit.json), [ledger-audit](evidence/ledger-audit.json).

최초 delivery 검사도 종료1을 남겼다. sources의 기존85행은 값이 동일했으나 재직렬화 공백 때문에 바이트 비교가 실패했다. 봉인 git blob의 정확한 바이트를 복원한 뒤 사후14행만 붙였고 실패 영수증을 삭제하지 않았다.

후행 의미 대조 생성 중 JSON의 reason/gap 키 차이로 첫 명령이 종료1이었다. 원판을 바꾸지 않고 올바른 키를 읽어 종료0으로 다시 생성했으며 operations에 기록했다. RESULT 최종 주장 검토에서 ‘최초 본문’, ‘제목 셀 renderer’, ‘상호 참조’ 표현을 각각 관측 본문, 아이콘·수량 데이터 셀, JO→AIM 참조로 좁혔다. 이런 문장 수정은 원실험 판정 수정이 아니다.

최종 파일·표 검사 명령은 다음과 같다. 실행 cwd는 저장소 root이다. 실제 영수증이 생성되기 전에는 아래 항목의 통과를 가정하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-069/evidence/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-069/manifest.json --fetch
```

<!-- FINAL_VALIDATION_STATUS -->
결과 내용 커밋 **0c3ab1c1c8359d3c5f85c8b9e51dc7119f8b2dec**에서 `session check --fetch`를 실제 실행했고 **종료0**이었다. 실행 위치는 `/workspace/scratch/41ae7a55914b/agentflow-open`, 시작/완료는 `2026-11-23T09:26:19.220766+00:00` / `2026-11-23T09:26:29.129963+00:00`이다. fetch가 확인한 통합 HEAD는 **dfe4c46e3e27629d44ff12ec2f613ba4e031c42e**, manifest 시작판은 **76b8c1d15812fbf91b879f8444fd188ae7445802**, 선행은 **18e4449eb0ac04464aee8fa6cc07f1f6a54d0b5d** 그대로다. contract hash는 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`, outside_paths/unmerged_paths/errors는 모두 빈 배열이었다. [전체 영수증](evidence/session-check-result.json).

같은 결과 SHA로 GitHub의 RESULT, source/rank/judgment, 문제·질의·frame, 수용 파일 등 **13파일을 다시 열었다**. 반환한 전체 내용 길이와 Git blob SHA를 로컬 커밋 객체와 대조했고, 원격 JSON/CSV를 다시 파싱한 **8검사 모두 통과**했다. [원격 대조](evidence/result-remote-verification.json). 이 SHA의 수용 파일은 검사 전 pending 항목을 포함하므로, 현재 audit 묶음에서 실제 결과로 갱신한다. 그 다음 고정 audit SHA도 다시 열고 마지막 HANDOFF에 대조를 기록한다.

최종 delivery checker는 같은 결과 HEAD에서 audit 작업 파일을 포함해 **41검사, 실패0, 실제 종료0**이다. RESULT의5표 및 전달한 모든 Markdown 표 열 수, CSV18/23열, 조인, 원래85 source행의 정확한 바이트, 사후14행, 고정 질의·순위·판정 불변을 검사했다. [delivery-audit-committed](evidence/delivery-audit-committed.json). 독립 claim review17항목도 미해결0이며 같은 모델의 후행 검토라는 범위를 유지한다.
<!-- END_FINAL_VALIDATION_STATUS -->

## 6. 미실시와 부분 인계 이유

제품 통합·런타임 실행·장치 조작·초보자 사용자 시험은0회다. 같은판/최초판·P3댓글·기준일 전체 이슈 상태도 미확인이다. 최소20원문은 충족했으나 동일 총비용과 엄격층, 실제 진행 중 선택의 근거가 부족하므로 PARTIAL이다. 새로운 성공 자료를 후행으로 읽더라도 원실험을 소급 고치지 않는다.

환경·실행 명령·고정 코드 SHA·입력 행렬은 [resume-checks.md](evidence/resume-checks.md)에 있다. 가장 먼저 원이슈 최초판·기준일 맥락을 확인한 뒤, 실제로 남아 있는 설계 선택에 대해서만 새 비교를 봉인한다. 마지막 HANDOFF는 고정 결과/수용 파일 재열람 뒤 단독 커밋한다.
