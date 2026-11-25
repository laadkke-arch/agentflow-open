# HANDOFF — AF-RES-267

**자체 상태 DONE · 인계 REVIEW_READY.** CPython 3.12.0 final에서 합성 스냅샷 12개와 원 벡터 전부를 실행했다. 회차마다 86/90 통과했고 F t24의 B2/B3/B6/B7만 값이 달랐다. 별도 판독은 반환 시점 판정 전부에 동의했다. 입력을 바꾼 뒤 복원한 통제는 원 채점기가 8/8 통과시켰고, 별도 판독에서는 8/8 호출 도중의 쓰기를 확인했다.

- **고정 결과 `7155d95fb2194fb03e65826689f09871a1785261`** · [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/7155d95fb2194fb03e65826689f09871a1785261/docs/workstreams/research/AF-RES-267/RESULT.md) · [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/7155d95fb2194fb03e65826689f09871a1785261/docs/workstreams/research/AF-RES-267/SELF_CHECK.md).
- **검사 영수증 `9a32518ec26f59fd73d31d20d631ed84337d0fcd`** · [고정 결과 재생 및 저장소 검사](https://github.com/laadkke-arch/agentflow-open/tree/9a32518ec26f59fd73d31d20d631ed84337d0fcd/docs/workstreams/research/AF-RES-267/receipts/fixed).
- AF-RES-267 시도 1 · Codex Cloud/Linux x86_64 실행 담당 · `laadkke-arch/agentflow-open`, `work/research-af-res-267`. 소유 경로 `docs/workstreams/research/AF-RES-267/`. 시작 `9eeb7105c7edec2c5c4c0a1f722916b9d664b236`, 선행 고정 인계 `a61cee2b8882e79226f383217440ab71f2637f8c`. [범위·노출·세션 핀](SCOPE.md) · [AF-RES-249 인계](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/HANDOFF.md).

## 산출물과 관측

| 파일 | 확인한 내용 |
| --- | --- |
| [snapshots.csv](snapshots.csv) | 12좌석의 actor·task·phase·parent/hash와 사례표·원장 조인. 고유 코드 5. N t0와 F t0/t12−는 같은 bytes |
| [vectors.csv](vectors.csv) | 90개 벡터별 기대·실제·타입·반환 상태·exit 및 r1/r2 실행기와 참조판의 원행 |
| [replay.md](replay.md)와 [receipts](receipts/) | 원 runner/fixture, 정확판 fingerprint, 세 개의 빈 폴더 실행과 통제. 각 호출의 argv·stdout/stderr·exit·SHA256 |
| [revisions.md](revisions.md) | 동률, 비연속 전역 그룹, bool, 복원, 함수 예외. A1/A6 공개 예시 표기 및 가상 reviewer/acceptor 별칭 불일치 |
| [sources.jsonl](sources.jsonl) | 직접 산입 28파일/3계보. 249 8, 정확판 CPython 8, 언어·복사·로딩 5, nbgrader 7. 원장 54행, 성공 50, 실패 4 |

분석 실행은 원 채점기 29회와 별도 참조판 29회였다. 각 24회는 스냅샷 두 회차, 각 5회는 네 통제와 함수 예외 대조다. 고정 결과를 새 Git archive에서 읽어 각각 12회를 더 실행했다. **총 원 채점기 41회·309 벡터, 별도 참조판 41회·309 벡터.** 분석 r2와 고정 결과 재생에서 각각 stdout/stderr·exit·지문 24쌍이 최초 회차와 일치했다. 개별 실패 수와 프로세스 수를 분리했다. [r1](receipts/r1/summary.json) · [r2](receipts/r2/replay-comparison.json) · [통제·예외](receipts/controls/summary.json) · [고정 결과 재생](receipts/fixed/replay/summary.json).

원 검증기의 파일 SHA256은 `e0f1afe777b4e224f704946f223f52c83f96bcf466e0724d8d7f6f92f47f9f2f`다. 소스의 `sys.version_info[:2]` 조건은 패치판을 고정하지 않는다. 실제 바이너리는 GitHub v3.12.0 태그 소스 `0fb18b02c8ad56299d6a2910be0bab8ad601ef24`에서 빌드한 `823adc445e057c565f905df18a7fa19dad1a21ec084f9be6a43ab4c79fdf6c23`다. python.org 아카이브 HTTP 403 및 빌드 경고 원문도 보존했다. [환경](receipts/r1/environment.json) · [빌드](receipts/build/commands.txt).

## 인계 전 검사

2026-11-25 01:21:33–01:21:43 UTC에 고정 결과 SHA `7155d95fb2194fb03e65826689f09871a1785261`를 깨끗한 checkout에서 확인했다. 별도 적합성 검사와 공통 저장소 검사는 소스 저장소의 Python 3.12.14로 실행했다. 이 판의 과제 채점 호출은 0회다.

| 명령·대상 | 종료 및 범위 | 원영수증 |
| --- | --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-267/session.json --fetch` | 0, `passed/remote_checked`. 통합 ref `6cb99cc0af8ff62035d4ddce1df5cf9bc6906b7c`, 계약 v2, 의존 SHA 유지, 검사한 변경 238경로, 외부 0 | [session stdout](receipts/fixed/repository/session.stdout) |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0. doctor, acceptance, reference-audit discovery, 원본 smoke, check-all 명령 종료 0. check-all은 `no_active_sessions`; 소유 경로 안의 핀은 위 개별 검사에서 판정 | [cloud-check JSON](receipts/fixed/repository/cloud-check.json) |
| `python scripts/check.py --require-git` | cloud_check 내부에서 실제 종료 0. core 55, lab 7·9, demo·독립 export·Git bundle 복원 | [acceptance stdout 원문](receipts/fixed/repository/child-logs/acceptance.stdout.log.gz) |
| 고정 결과의 Git archive 재생과 readback | 둘 다 종료 0. 같은 실행판의 12회·90 벡터, 두 필수 표·마지막 세 행·Q1–Q7·원 스트림·지문 대조 | [명령](receipts/fixed/commands.txt) · [readback 원문](receipts/fixed/readback.stdout) · [결과 지문](receipts/fixed/result-files.sha256) |

시작 SHA부터 영수증 커밋까지 356개 파일이 소유 경로 안에 추가됐다. 중앙 진행표의 시작/결과 Git blob이 같다. 이 인계 커밋은 HANDOFF 한 파일만 추가한다. 저장소 검사 범위는 위 고정 결과 SHA다. [변경 경로](receipts/fixed/changed-paths.txt) · [진행표 지문](receipts/fixed/dot-control-blobs.txt).

배치별 커밋은 사전 범위 `9298b59`, 원자료 묶음 `99a2904/14eff18/dd85e8b`, 최초 실행 `66c0136`, 재생·본표 `875e14d`, 반례·정정 `6e9529e`, RESULT `e52293e`, SELF_CHECK `7155d95`, 고정 결과 재검산 `9a32518) 순서다.

## 미확인과 다음 첫 행동

실제 사람, 열람, 실험, 독립 검토자, 품질 검수, 인수 및 사람 노동의 관측 단위는 0이다. 실행 담당의 자체 검토와 별도 참조 코드 호출까지 시행했다. 일반 입력 전수·다른 실행판·네이티브 호출 안의 모든 중간 상태는 미확인이다. 예외 대조에서 실행기는 함수 호출 예외를 기록했고, 모듈 최상단 오류와 timeout은 소스에서 분기 경계를 확인했다.

통합 담당의 첫 행동은 [원 자극](receipts/original/stimuli.md#L39-L40)과 [복원 통제 B2](receipts/controls/runs/restore_input/reference/stdout.jsonl#L3)를 함께 읽어 입력 변경 금지가 어느 시점의 불변을 요구하는지 확인하는 것이다. 반환 때 상태를 요구한다면 기존 채점기의 이 판정은 유지된다. 호출 내내 불변을 요구한다면 해당 주장에 중간 상태의 원영수증을 연결한다. 원 249 기준과 합성 사례 판정의 개정은 별도 버전에서 검토한다.

색인 제안은 **AF-RES-267 · 고정 합성 검증기 실행 · DONE**. 결과 경로는 위 RESULT, 핵심 의존은 AF-RES-249 `a61cee2b` 및 CPython v3.12.0으로 등록할 수 있다. 검색어는 연속 그룹, 동률 삽입, bool 타입, 입력 복원, 귀속 SHA, 자동 채점/독립 인수다.
