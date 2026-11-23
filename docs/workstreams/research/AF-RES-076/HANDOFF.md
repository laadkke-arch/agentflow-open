# AF-RES-076 인계

**REVIEW_READY · 시도 1 · Codex Cloud.** 자연 요구 6건과 교정 요구 6건을 고정 후보 20건과 비교했다. 자연 120쌍의 직접 적격 분모는 0이라 직접 회수율을 산출할 수 없다. 교정군에서는 L/S/E 모두 5/5 직접 후보를 회수했고, 본 표시창의 두 조건과 환경 공동 확인은 0/108이었다. 자연군에서 S는 부분 5/10·전이 1/2였고 L과 E는 각각 4/10·0/2였다. E의 교정 전이 회수는 2/6이었다. URL만 저장한 L은 관측한 두 모집층 모두 구축·빈 캐시 전송량이 가장 작았다. [고정 결과와 필수 세 표](https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/RESULT.md)

## 식별과 고정 이력

작업은 `laadkke-arch/agentflow-open`의 `work/research-af-res-076`에서 했다. 소유 경로는 `docs/workstreams/research/AF-RES-076/`다. 계획 기준은 `39cadb6ecdf62d0b21c0cce67834f2aef3bf6853`, 배정 당시의 통합 HEAD와 브랜치 시작은 `3ac1f42628930ead89dfcb1bd38f3a8e74c9c192`, 계약의 통합 재조회는 `817ee771ebfa63d4a177ee12f46b9818a6335308`였다. 유일한 결과 의존은 AF-RES-072 `f77d2d68b3361df5a0fd70d5ea10df79b08b0f09`다. [계약](manifest.json) · [모집과 평가 규칙](SCOPE.md) · [072 인계](https://github.com/laadkke-arch/agentflow-open/blob/f77d2d68b3361df5a0fd70d5ea10df79b08b0f09/docs/workstreams/research/AF-RES-072/HANDOFF.md)

| 고정 단계 | 커밋 | 2026-11-23 UTC |
| --- | --- | --- |
| ① 모집과 원목록 | `3142bbb37ce878d77f340c5fef050fb64227aa62` | 10:09:53 |
| ② 요청 열람 전에 카드 고정 | `f613b3506d68d920f863031f58c21c6dc528d43d` | 10:12:07 |
| ② 자연·교정 입력 고정 | `596e55d00d4283a9c7d11036997435ca32681442` | 10:16:30 |
| ② 기대표 및 채점 사전시험 | `d041e6d98524039c43e27171c7fd7a2c875240fa` | 10:23:21 |
| ③ 라이브 순위·창·비용·실행 | `a531d41be8d446707ee1231491b9a5f48a5f3e8e` | 10:27:29 |
| ④ 개별 창 판독·후행 대조 | `8a1039ad3e62272f2ea5edd5ac068ffea918d48c` | 10:30:56 |
| ⑤ 검산한 연구 결과 | `abe6a4ff0ded1f7076e0f11381ac3da5d3984983` | 10:44:51 |

## 완료와 확인

Q1–Q8은 결과·판독 범위·반례·재개 입력까지 연결했다. 독립 원저작 23편, 후보 판정 240쌍, 원문이 표시되고 개별 판독이 있는 108자리, 고정판 양성 4개·범위 반례 2개, 사전 채점 9분기와 두 번의 오프라인 원장 대조를 확보했다. 라이브에서 원문 HTTP 108회와 반복 캐시 읽기 108회가 모두 고정판에 맞았다. 사후의 한 원문 충분 사례는 본 순위와 별도의 영수증이다. [수용 기록](https://github.com/laadkke-arch/agentflow-open/blob/abe6a4ff0ded1f7076e0f11381ac3da5d3984983/docs/workstreams/research/AF-RES-076/evidence/acceptance-evidence.json) · [자체 점검](SELF_CHECK.md) · [재현](reproduce.md)

Codex Cloud의 Linux x86_64 프로세스 사용자 `agent`, Git 작성자 `kk lee`, CPython 3.12.14로 실행했다. 결과 SHA `abe6a4ff0ded1f7076e0f11381ac3da5d3984983`의 깨끗한 checkout에서 아래 검사 세 개가 종료 0이었다. 명시한 세션 계약은 10:45:07.812479 UTC에 `passed / remote_checked`였다. 계약에 보고된 산출 경로 49개와 별도 계약 파일 1개가 소유 경로에 있다. 공통 검사기의 자동 세션 조회 응답은 `no_active_sessions`였고 계약 자체는 명시한 경로로 실행했다. Git 범위 검사는 별도로 종료 0이었다. [검산 원장](evidence/audit.json)

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-076/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
git diff --check 3ac1f42628930ead89dfcb1bd38f3a8e74c9c192 abe6a4ff0ded1f7076e0f11381ac3da5d3984983
```

10:45:35.725600–10:45:38.388004 UTC에 GitHub의 결과 SHA에서 10개 원장을 다시 열었다. 열람 10건은 HTTP 200이었고 `git show SHA:path`와 바이트가 모두 일치했다. GitHub 렌더에서 첫 세 표는 12×6, 108×7, 12×7이며 마지막 표는 3×3이었다.

| 원격 파일 | 바이트 | SHA-256 앞 12자리 |
| --- | ---: | --- |
| RESULT.md | 68,026 | `fc885e64ac33` |
| qrels.csv | 131,521 | `ae83dd998be8` |
| ranks.csv | 90,102 | `472ab5255a2a` |
| fetches.jsonl | 536,686 | `b99f865452a5` |
| slots.csv | 79,269 | `46991d1a04a1` |
| costs.csv | 8,667 | `05fd624ae565` |
| sources.jsonl | 64,651 | `b56c978344f1` |
| SELF_CHECK.md | 6,904 | `00bbcec0dc67` |
| evidence/acceptance-evidence.json | 8,008 | `c5e89cda1d3e` |
| evidence/audit.json | 3,108 | `47bcd1bc784d` |

## 남은 판단과 첫 행동

자연군은 2023년 초 이슈에 몰렸고 보고 당시 Windows·JP2, R 관계 API, CLI/Wasm·httpfs 등 원 실행환경을 복원하지 않았다. 학습용 교정 효과의 자연군 이전, 실제 사용자 채택율과 사람 활동시간, 시간 경과를 반영한 캐시 적중률은 미확인이다. 전체 후보와 창을 같은 작업자가 읽었다. Pillow #6871의 첫 글 검사 중 후속 댓글 첫 줄이 진단에 표시됐으며 입력 카드와 모집 규칙은 그 전에 고정돼 있었다. [모집 노출 기록](evidence/search-recruitment.json) · [판독 작업 경계](evidence/display-seal.json)

후속 독립 검토의 첫 행동은 결과 SHA를 체크아웃하고 아래 패킷을 만드는 것이다. NP03/X03, CP01/P01, CD03/D07의 요구 두 조건·환경과 실제 창만 보여 주고 카드·방식·순위·기존 판정을 숨긴다. CP01의 공동 충족과 CD03의 범위 반박 판정이 달라지면 표 2부터 다시 계산한다. 원래 환경에서 같은 기능이 확인되면 표 1의 직접 적격 분모부터 갱신한다. [재검토 입력](reproduce.md) · [약점 세 건](RESULT.md#판단을-바꿀-세-가지-약점)

```bash
af076=docs/workstreams/research/AF-RES-076
af076_review="$(mktemp -d)"
python -B "$af076/experiment/display.py" "$af076" "$af076_review/packet.jsonl"
python -B - "$af076_review/packet.jsonl" > "$af076_review/reader.jsonl" <<'PY'
import json, sys
targets = {("NP03","X03"), ("CP01","P01"), ("CD03","D07")}
seen = set()
with open(sys.argv[1]) as stream:
    for line in stream:
        row = json.loads(line)
        key = (row["request_id"], row["candidate_id"])
        if key in targets and key not in seen:
            seen.add(key)
            print(json.dumps({name: row[name] for name in ("request","edition","view")}))
assert seen == targets
PY
```

색인에는 ‘Pillow 12.0.0·DuckDB 1.4.3, 20후보·240쌍·108표시, 자연 직접 분모 0, 교정 직접 5/5, 실제 창 공동 확인 0’으로 연결할 수 있다.
