REVIEW_READY

# AF-RES-152#1 인계

공개 원전 66개와 공급원 3곳에서 새 항목 26건, 기존 상태 전이 13건, 안정 대조 8건을 판독했다. 창 안에서 지정 채널에 들어온 새 항목은 25건이다. 유보에서 S/F는 새 항목 14/15, P는 13/15, O는 10~14/15를 찾았다. 높은 예산 주류에서 P의 발견 중앙값은 27시간, S는 57시간이었다. 같은 비용으로 전체 보관 목록을 읽을 수 있다는 구성에서 높은 예산 희소 수요의 O는 350/364 질의 판정을 맞혔다. 제공자와 요청에 따라 유지·확인 방법의 순서가 달라졌다. [결과](RESULT.md) · [자체 점검](SELF_CHECK.md)

## 1. 식별과 고정 근거

- 작업 브랜치 `work/research-af-res-152`, 저장소 `laadkke-arch/agentflow-open`. 허용 경로는 `docs/workstreams/research/AF-RES-152/`다. Codex Cloud Linux x86_64, Python 3.12.14, Git 2.56.1, curl 8.14.1, SQLite 3.53.1에서 실행했다. 세부 모델·추론 강도는 미확인이다. [작업 계약](manifest.json)
- 계획판 `ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19`, GitHub 시작판 `35ca756d1b18af5d89c3eb53659365c09f1f88e3`. 마지막 재생·검산의 결과판은 `1334ae6cb6bf615664efcc17e54f9c95b69ea5d4`다. 검사한 시각은 2026-11-24 16:43 UTC다. 이 인계만 담은 후속 커밋은 원격 브랜치 HEAD에서 확인한다. [범위 등록](SCOPE.md) · [검사한 결과판](https://github.com/laadkke-arch/agentflow-open/blob/1334ae6cb6bf615664efcc17e54f9c95b69ea5d4/docs/workstreams/research/AF-RES-152/RESULT.md)
- 선행 두 인계는 도달한 범위와 남은 운영 질문을 고정하는 데 사용했다. 이번 실험의 데이터를 공급하지 않는다. [AF-RES-024 4af13008](https://github.com/laadkke-arch/agentflow-open/blob/4af1300841c1c39f9ef6e76d78579034d1ae0c51/docs/workstreams/research/AF-RES-024/HANDOFF.md) · [AF-RES-147 30afd115](https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/HANDOFF.md)

| 묶음 | 다시 읽은 원격 커밋의 대표 파일 | 실제 변경과 검증 |
| --- | --- | --- |
| ① 탐색·비교 등록 | [2d72a0b · SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/2d72a0b7c158d27f591f901b58d9a6ba7ed2405d/docs/workstreams/research/AF-RES-152/SCOPE.md) | 기준 SHA와 선행, 모집 시기, 두 예산 및 판정을 고정 |
| ② 모집·원전 | [221aa2f · policies](https://github.com/laadkke-arch/agentflow-open/blob/221aa2f3ef9362481bae1f6249d26e628e4ef5cc/docs/workstreams/research/AF-RES-152/policies.md) | 정책 입력과 출처 원장을 고정 |
| ③ 주 관측 | [4cfaeeb · events](https://github.com/laadkke-arch/agentflow-open/blob/4cfaeeb10131a1826480714bb4cff37e19d86536/docs/workstreams/research/AF-RES-152/events.jsonl) | Workers의 제품 분류에 맞추어 10월 표본을 교정. 물리적으로 가린 학습 입력과 유보 재생을 실행 |
| ④ 반례·검산 | [cb91429 · REPLAY](https://github.com/laadkke-arch/agentflow-open/blob/cb914291475bc6334a8fb8d4388cd4b3c15da3d3/docs/workstreams/research/AF-RES-152/REPLAY.md) · [4aa15fd · measure](https://github.com/laadkke-arch/agentflow-open/blob/4aa15fd81fc3c2f3e50e440a9b6faf320a86c7be/docs/workstreams/research/AF-RES-152/measure.py) | 중단 재개·가림·복구·민감도·비용을 비교하고 HTTP 측정 프로그램을 보존 |
| ⑤ 결과와 자체 점검 | [1334ae6 · RESULT](https://github.com/laadkke-arch/agentflow-open/blob/1334ae6cb6bf615664efcc17e54f9c95b69ea5d4/docs/workstreams/research/AF-RES-152/RESULT.md) · [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/1334ae6cb6bf615664efcc17e54f9c95b69ea5d4/docs/workstreams/research/AF-RES-152/SELF_CHECK.md) | 필수 표 세 개와 Q1–Q7, 불일치 3건을 저장. 아래 검사는 이 결과판을 GitHub에서 새 체크아웃해 수행 |

## 2. 검사한 범위

- [REPLAY.md의 원장 재생과 민감도 명령](REPLAY.md#원장-재생과-두-중단-검사)을 새 체크아웃에서 모두 종료 0으로 실행했다. 학습 영수증, 결과·요약, 독립 계수, 복구 판독, 비용 및 민감도 출력이 커밋된 파일과 바이트 일치했다. 2026-02-05 직전의 물리 가림 실행과 같은 시간까지의 전체 입력, 2025-11-07 18 UTC 중단 후 별도 실행의 복원과 연속 실행의 CSV 네 개도 바이트가 같다. 처음 재개 검사에서 요청·열람 CSV의 정렬 키가 달라져 체크포인트에서 열 순서를 보존한 뒤 다시 대조했다. [명령](REPLAY.md) · [입력과 출력 해시](verification.json)
- 원장 재계수는 97행, 고유 원전 66, 11개 발행 주체 그룹이다. 세부 하한은 발행 29/8, 당사자 변화 12/6, 운영 12/6, 다른 분야 정정 5/4다. 목표 신규의 유보 미발견 29행과 56,784 대상시간/실행 중 미확인 192, 704 정책×주 예산 및 정책에 동일한 질의열을 확인했다. [검산](verification.json) · [원자료](sources.jsonl)
- 실제 운영의 유보 복구 직접 관측은 0/2이고 S/F는 사후 기록을 2/2 읽었다. 별도 구성에서 회복 시간을 8→12시로 바꿔 결번 보완은 9→13시, 마지막 유효 반영은 12→16시였다. 재개의 유효한 쓰기는 각 6건, 재수신된 문서의 추가 쓰기는 0건이다. 희소층 제거로 낡은 추천의 P/S 순서가 반전했다. [사건별 결과](outcomes.csv) · [복구 구성](recovery.json) · [민감도](sensitivity.csv)

```sh
p=docs/workstreams/research/AF-RES-152
python -B -m workbench.session check "$p/manifest.json" --fetch
python -B scripts/check.py --require-git
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

세 명령이 모두 종료 0이었다. 지정 계약 검사는 갱신된 통합판 `ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8`까지 fetch하고 경로·선행·계약을 통과했다. 공통 검사는 두 lab의 test·demo, export, Git bundle 복원 등을 실행했다. Cloud 종합의 중앙 활성세션 탐색은 `no_active_sessions`였고 이 과제의 manifest는 별도 명령에서 검증했다. 독립 작업자의 판독이나 새 AI 세션, Windows 재생, 외부 부하 시험은 미실시다.

## 3. 다음 첫 행동과 미확인

수용 검토의 첫 행동은 결과 SHA의 `CF-2025-11` 미발견 16행과 `CF-2026-01`의 표시일·편입일이 뒤바뀌는 대조를 확인하는 것이다. [사건 원장](events.jsonl) · [결과 행](outcomes.csv) · [production 편입](https://github.com/cloudflare/cloudflare-docs/pull/26259)

작은 실제 HTTP 표본 9회 중 6회는 공개 GitHub/Raw에서 몸체와 파싱·SQLite 저장을 계측했다. M07–M09의 원래 호스트는 실행 환경의 CONNECT 403으로 공급자 응답이 미확인이다. 이 경로가 열리는 실행 위치에서 `python -B "$p/measure.py" --out "$scratch/new-http-sample.csv"`로 동일 입력을 다시 받고, [규모 식과 비용 재생](REPLAY.md#실측과-규모-조건)을 사용해 10만 건의 REST/전송 제약을 교차 확인한다. PLOS 원판·정정판 PDF는 열람 도구 500이었다. 정확한 두 입력 주소와 대조 명령을 같은 문서에 남겼다. 실제 `304` 비율, 최초 웹 편입·사람 검토 시간은 여전히 미확인이다.

색인에 넘길 표기는 **AF-RES-152 · 새 자료와 기존 근거의 같은 예산 배분·복구 · REVIEW_READY**다. 기준 충족과 미확인 범위는 위 결과판·원장·재현 명령으로 판단한다. [결과](RESULT.md) · [원격 브랜치](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-152/docs/workstreams/research/AF-RES-152)
