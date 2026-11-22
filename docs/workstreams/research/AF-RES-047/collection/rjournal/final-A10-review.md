# A10 최종 변경 범위 정적 검토

**A10 이후 판정과 원장 전파는 정합하다.** 발견했던 낡은 상태표시 두 개는 root가 수정했고, 재생성된 행에서 직접 재확인했다. 현재 미해결 실질 보고 오류는 발견하지 않았다. 이 판단은 연구 전체 수용 완료를 뜻하지 않는다.

검토 UTC: 2026-11-22T23:26:12.292887+00:00. 검토 RESULT SHA256: 07ce5a039ae9a257ac57aa38900af6c1b26527ca4fcff932b077f1d94da6e7fb.

같은 모델의 별도 문맥에서 RESULT, SELF_CHECK, amendments A10, cases/readings/analysis-summary/sensitivity, 수용 원장과 검산 출력의 변경 범위를 읽었다. 외부 독립 평가가 아니며 원문 추가 열람, 대형 파일 재전송, 원 과학 실행 재현은 하지 않았다. Root 파일도 수정하지 않았다.

## 판정과 수치

| 항목 | 확인 결과 |
|---|---|
| RUN02 외부 R | 1. 선택 R1의 같은 archive 실행 기록과 독립 발행자 fingerprint의 연결로 한정한다. |
| RUN02 V·엄격 양성 | 둘 다0. CHROM=1은 출력 기록 재독으로 남는다. |
| 자연층 | R0/6·V0/6; 조건부 V는 분모0이므로 해당 없음. |
| 실행 보강층 | R1/2·V0/2; R 확인 사례 중 조건부 V0/1. |
| 구성별 R | RUN02 A0·B0·C1. 전체 구성 집계도 A0·B0·C1. |
| 수용 원장 | case_summary와 source_summary가 각각 통합 요약과 정확히 같다. full_acceptance=false·partial을 유지한다. |
| 자료 수 | 접근/열람311행, 고유31저작, 필수 역할27저작. |
| 검산 | 저장된 구조검사61/61 통과. 이 변경 범위 검토의26조건도 통과. |
| 필수 표 | 첫8행·둘째24행·종결 정확3행을 유지한다. |
| 감도 | 40행·표시 변화17행·원래 결측의 새 손실0인6행. RUN02 자료 식별자/실제 사용 근거 제거 시 외부 R1→0, V0 유지. |

## A/B 경계

RUN01·RUN02의 A/B 네 packet에서 audit_only_*를 제외한 모든 열을 확인했다. 새 archive SHA256, 487,611,787 bytes, run/Collection UUID, 정확 실행 timestamp, CHROM1·POS1·END63267·DP0와 RUN01의 좌표값이 노출되지 않는다. audit_only_*에는 전체 감사 문맥이 남지만 packet에서 제외한다고 명시한다.

RUN02 B에 발행자의 MD5 목록과 현재 제공 파일 checksum 차이가 들어간 것은 B의 발행자 범위다. 이 상태만으로 어떤 소비 파일과 일치하는지 모른다고 정확히 제한했다. C에 archive member와 원 실행 기록이 추가되면서 발행자 목록↔소비 archive의 연결이 확인된다. 현재 publisher의 전체 hash를 읽었다는 것과 소비 archive와의 일치 결론을 구별한다.

## 발견 후 수정된 두 행

| ID | 최초 발견 | 수정 후 재확인 |
|---|---|---|
| A10-RJ-01 | RUN02 C의 run_link=True와 달리 C_slot_status가 publisher-to-local representation unresolved로 남았다. | same-archive 실행 graph/log/output 존재, selected R1 publisher linkage confirmed by full bytes and exact-path publisher MD5, selected CHROM V unresolved로 명시한다. |
| A10-RJ-02 | 실제 사용 근거 제거 행의 original_evidence_state가 present_local이었다. | present_external_run으로 갱신됐다. baseline R1→제거 후 R0은 기존부터 맞았고 현재도 같다. |

A10은 이전 external R0, 원 snapshot·bundle3 SHA, 새 전체 계산 시간과 근거, 영향을 받은 C·집계·감도 행을 보존한다. 기존 SCOPE를 완화한 승격이나 독립 syscall 관측이라고 쓰지 않는다. 실행 당시 스크립트는 verify_full_fastq-executed-snapshot.py로 보존되어 실행 영수증의 SHA와도 일치한다.

자료·표본·정확 주 값·실제 미사용 음성례·metadata-only 전후 비교의 남은 한계는 계속 부분 수용으로 남는다. 앞선 final-report-review의 R0은 당시 snapshot의 기록이고, review-adjudication은 그 이후 근거에 의한 변경 판정이다. 이번 검토는 그 변경이 최종 보고서와 원장에 전파됐는지를 확인했다. 최종 결과 commit 재열람과 HANDOFF 완료는 이 파일에서 주장하지 않는다.
