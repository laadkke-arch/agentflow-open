# 결과 SHA 검증 영수증

검사 대상은 **b40b4dfeb8b7079f6568e511105117b02f477d14**다. 이후의 영수증·HANDOFF 문서 커밋을 이 검사에 포함했다고 주장하지 않는다. 모든 공통 코드는 이 결과판 그대로이며 검사기나 시간 제한을 수정하지 않았다.

| 검증 | 실제 결과 | 근거 |
|---|---|---|
| 연구 데이터 감사 | exit0 | data-audit.stdout.log, run-summary.json; 6질문·12경로·봉인 불변·분모·원자료 최소량 검사 |
| 개별 manifest 계약 검사 | exit0, remote_checked | session.stdout.log; 실제 최신 통합0537c02a3f84a8807a38cbb5c8d3dccdc3743243, outside_paths=[] |
| 공통 검사 최종 시도 | exit0, clean start/end | cloud-final.receipt.json 및 final-summary.json; 같은 결과 SHA의 별도 worktree |
| 공통 내부 checks | doctor0/acceptance0/research-case0/original-smoke0/sessions0 | final-*.stdout.log 및 .stderr.log |
| 공통 내장 check-all 제한 | no_active_sessions, count0, not-executed | final-sessions.stdout.log; exit0을 활성 AI/세션 검증 성공으로 바꾸지 않음. AF092 개별 manifest는 별도 검사했음 |
| 원격 결과 재열람 | 10파일 blob 일치; 98변경파일 모두 owned path; dot-control 동일 | remote-readback.json |
| 외부 원 출력 재열람 | 최초 답7/7·댓글7/7 본문 해시 동일; 고정 Pandoc fixture 동일 | primary-readback.json |

`cloud-final.stdout.log`에는 unittest55개, repo-intake7개, reference-audit9개 통과와 예제/재사용/복원 검증이 있다. 이것은 workbench의 환경·코드·기록 검사이며 신규 질문의 jq/Pandoc/Quarto 변환 실행이나 문헌 주장 자체를 인증하는 검사가 아니다. 연구 상태 PARTIAL은 P2의 공평 비교·원 Quarto 연결 결손 때문에 유지한다.

## 실패 기록을 포함한 세 번의 공통 검사

1. **첫 시도 exit1, 약180초:** 제가 TMPDIR를 조사 경로의 docs 아래에 설정했다. 공통 단위 테스트가 ROOT/docs를 새 tempfile 작업공간으로 복사하므로 자기 복사본이 입력에 포함되었다. 캐시가15G로 늘고 child unittest가 내부180초 제한을 넘었다. `cloud.stdout.log`, `cloud.stderr.log`, `cloud-first.receipt.json`, `timeout-diagnosis.json`에 실패와 환경을 보존했다. 생성한 ignored tmp만 정리했다.
2. **별도 clean worktree, OS 기본 temp, exit1, 약8.7초:** 단위55개 및 프로젝트별7/9개 테스트는 통과했지만 Git bundle 복원이 실패했다. 초기 shallow repository에 부모 f10c81baa98d9bad0407c9af8b4fa91cf9b70f6e가 없었다. `cloud-retry.stdout.log`, `cloud-second.receipt.json`, `retry-summary.json`에 원 오류를 남겼다.
3. **같은 SHA, 전체 이력 확보, exit0, 약9.6초:** `git fetch --unshallow origin` 종료0 뒤 shallow=false·누락 부모 commit 존재를 확인했다. 소스·검사기 수정 없이 같은 별도 worktree에서 공통 명령을 다시 실행했다. `cloud-final.receipt.json`, `cloud-final.stdout.log`, `cloud-final.stderr.log`, `final-summary.json`에 최종 결과를 보존했다.

이 재시도는 확인된 환경/이력 결손을 해결한 필수 gate 재실행이다. 앞 실패를 지우거나 첫 실행이 통과한 것으로 쓰지 않는다. manifest 개별검사와 데이터 감사는 첫 결과판에서 이미 exit0이었다.

## 실행 명령

```bash
python -B docs/workstreams/research/AF-RES-092/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-092/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

최종 공통 실행은 동일 SHA의 독립 worktree, OS 기본 임시 경로, 완전한 Git 이력에서 이루어졌다. `codex-cloud`는 호출자가 붙인 환경 라벨이며 계정·새 AI 대화·외부 모델 연결의 증거가 아니다. 각 원 receipt의 로컬 로그 경로는 당시 값을 보존했고, 이 폴더에 복사한 파일과 해시는 `log-index.json`에서 대응시킨다.

## 원격·원 출력 일치 범위

RESULT·sources·candidates·outcomes·metrics·cards·SELF_CHECK와 최초답/댓글/상류 영수증을 GitHub의 불변 결과 SHA로 다시 열었다. 파일 blob 지문이 로컬 결과판과 같았다. 원 답 최초판과 댓글을 공식 StackExchange API로 다시 열어 본문 SHA256을 대조했다. J3의1998/초기*=10, P2의[2]{} 재정의, P3의 질문자 해결 보고를 다시 확인했다. Pandoc6836 fixture의 숫자 참조는 `Str "1."`로 마침표를 포함한다. 초기 정확문자열 `Str "1"` probe=false는 이 구두점 차이로 설명되며 전체 고정 파일 해시는 같았다.

P1 실제 fontfile/코드포인트, P2 원 Quarto tex/PDF, P3 원 전체 입력·정확판·출력 및 J1 jqplay는 여전히 미확인이다. 이 검증으로 해당 결손을 채웠다고 보고하지 않는다.
