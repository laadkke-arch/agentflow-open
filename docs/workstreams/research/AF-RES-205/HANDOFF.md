# AF-RES-205 HANDOFF — DONE

## 식별과 범위

- AF-RES-205 시도 1. Codex Cloud Linux x86_64에서 CPython 3.11.15와 pip 24.0으로 실행했다. 저장소 `laadkke-arch/agentflow-open`, 배정 브랜치 `work/research-af-res-205`, 허용 경로 `docs/workstreams/research/AF-RES-205/`.
- 시작 SHA `c860f8240ab7b7077e2d5b63e438ddd83ff69a27`, 계획 기준 `050278651b11a2a3a49d45baebf41c707c06b700`. 의존 AF-RES-187 [고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/HANDOFF.md)의 커밋은 `4dd004ba7bebb19ebc03f2539bf5716a14bd1787`이다. [범위·핀](SCOPE.md) · [작업 계약](session.json)
- 결과 고정 SHA는 이 인계 직전 ⑤ `2786b85b692ce28ef20f6904aa56c1bff1f4365d`이다. GitHub에서 이 SHA를 별도 checkout으로 다시 읽었다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/2786b85b692ce28ef20f6904aa56c1bff1f4365d/docs/workstreams/research/AF-RES-205/RESULT.md) · [고정 자체점검](https://github.com/laadkke-arch/agentflow-open/blob/2786b85b692ce28ef20f6904aa56c1bff1f4365d/docs/workstreams/research/AF-RES-205/SELF_CHECK.md)

## 실제 판정

| 완료 항목 | 결과 | 대표 증거 |
| --- | --- | --- |
| 정확 배포물 대조 | 4/4 PyPI SHA256 일치, 관련 6개 파일의 whole/구간/RECORD 태그 지문 일치, 가능한 venv의 로드 경로와 파일 해시 확인 | [artifacts.csv](artifacts.csv) · [verify-wheels](receipts/verify-wheels.json) |
| 8환경×4입력 | 32/32 기록. 28셀의 112개 독립 실행에서 반환 94, 호출 ValueError 18. A02의 4셀은 명시 의존성 충돌로 설치 종료코드 1 | [matrix.csv](matrix.csv) · [A02 resolver](receipts/A02/setup.jsonl#L3) |
| 값, 메모리와 쓰기 | Datasets 2.21.0은 지정 열의 값과 결측 위치를 반환했고 H1은 독립 writable 결과였다. Quantity False는 같은 단위 가변 float64에서 원본 쓰기 전파, 읽기전용에서는 공유와 쓰기 불가를 보였다. Astropy 6.1.0/2.0.0 명시 dtype은 거부됐고 암묵 dtype 및 cm/s는 사본이었다. | [RESULT 표 2–3](RESULT.md#표-2) · [advice.csv](advice.csv) |
| 통제·타 분야·재생 | 독립 copy, 가변 view, 읽기전용 view가 각 NumPy 판에서 통과. 보강 56개, 별도 잠금 재실행 112/112 일치. Linux private/shared 차이를 관찰하고 Microsoft/NARA/LOC는 원문 대조했다. | [COUNTEREXAMPLES](COUNTEREXAMPLES.md) · [보강 원출력](receipts/controls.jsonl) · [잠금 재생](receipts/replay-check.json) |
| 직접 원자료 | 28/22. Wheel 4/4, tag/fixture 8/6, NumPy/PyArrow 7/4, 고정 관측 5/4, 분야 4/4. 종류별 부족 0 | [sources.jsonl](sources.jsonl) · [frame.csv](frame.csv) |

완료 조건에 부족한 항목은 0이다. 제보자의 실제 판·입력·해결 여부는 미확인이다. 다른 ABI, sdist, 성능 및 nested/temporal 대규모 입력은 미확인이다. 독립 세션 검토는 미실시다.

## 고정 결과 재확인

- ⑤를 GitHub에서 fetch하고 새 checkout에서 [결과](RESULT.md), [출처 원장](sources.jsonl), [배포물 원장](artifacts.csv), [32셀](matrix.csv), [권고](advice.csv), [자체점검](SELF_CHECK.md), 원영수증을 다시 읽었다. 112 주영수증, 56 보강 영수증, 전체 자료 41행, 모집 113행, 8 권고 행, 표 순서·마지막 약점 3행 및 내부 링크를 다시 확인했다.
- 같은 ⑤에 `python -m workbench.session check docs/workstreams/research/AF-RES-205/session.json --fetch`가 exit 0과 `remote_checked`를 반환했다. 확인 시 기준 브랜치는 `bb146773bbffba5e724e8c842951e2c25198c2da`였다. 시작 SHA와의 파일 차이는 진행표 하나였고 계약 해시는 같았다. 허용 경로 밖 변경 0이다. 원 stdout SHA256 `d2dd0117d68b2be0b32a2ac32f74ca65d1ab1f8aba10e609a09e9861ce062b33`.
- 같은 ⑤의 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`는 exit 0이었다. 공통 55개와 두 lab 7·9개를 확인했다. 전체 세션 목록은 `no_active_sessions`였고 위 개별 계약 검사가 대상 작업을 확인했다. 원 stdout SHA256 `94ae4f799e019bec71abe7e972a8cb4b527ed99c2ad73dcccef1f77e1c5e21c7`. [④의 독립 checkout 기계적 기록](receipts/workbench-stage4.json)
- 최초 재실행 명령과 입력, exit 10 행동 예외 및 설치 종료코드, 각 보조 의존성의 wheel 해시는 [재현과 영수증](receipts/README.md), [입력과 지문](inputs.json)에 있다.

## 다음 첫 행동과 색인 제안

1. 통합 담당은 GitHub 작업 브랜치에서 이 문서와 고정 ⑤ RESULT를 열고, 표 2의 [A04 dtype/단위](receipts/A04/runs.jsonl#L9-L16)와 [A02 resolver](receipts/A02/setup.jsonl#L3)를 확인한 후 색인 반영을 판단한다.
2. 새 사용자 조건이 들어오면 원입력의 dtype·단위·chunk·결측과 정확 설치판을 먼저 고정한다. 같은 플랫폼에서 재확인이 필요하면 [README의 해시 잠금 재생](receipts/README.md)을 시작점으로 쓴다. 과거 사용자 해결 증거가 필요하면 RESULT 마지막 표의 [J02](https://discuss.huggingface.co/t/valueerror-unable-to-avoid-copy-while-creating-an-array-as-requested/93584) 최초 traceback과 당시 실행을 잇는 공개 자료가 첫 입구다.

색인 제안 — **AF-RES-205 DONE** · NumPy 복사 정책의 Datasets 2.20/2.21·Astropy 6.0.1/6.1 정확 wheel 대조, 32셀, 값·원버퍼·쓰기 경계 · [RESULT](RESULT.md) · 의존 AF-RES-187 `4dd004ba7bebb19ebc03f2539bf5716a14bd1787`.

## 커밋

1. `53880d79f633c3a6f74edcfcd4b7162947994fed` 범위·분모·작업 계약
2. `bf5aff8b5c1f18339835b1dbe03893e084c06e60` 원문·모집·wheel 지문
3. `e262deee47cf50b0978f0bd849c696aae092ff3a` 실행·표·영수증
4. `de65e7186c8e24a7ae502223a3ae5b50d3afe1c6` 반례·분야·잠금 재생
5. `2786b85b692ce28ef20f6904aa56c1bff1f4365d` RESULT·SELF_CHECK
6. 이 인계 파일
