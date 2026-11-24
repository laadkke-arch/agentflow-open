# AF-RES-217 HANDOFF

## 실제 상태

**DONE · AF-RES-217 1차 · Codex Cloud 실행 검증.** 고정 모델 6/6의 Git blob·크기·SHA-256을 확인하고 구성과 네트워크를 직접 판독했다. 12개 모드 자리 × 두 독립 프로세스 24/24에서 지정 모델을 열고 읽었다. 예상 지원 7자리(14회)와 예상 미지원 5자리(10회)가 모두 202 예상과 일치했다. 양성은 Init 0/exit 0, 명시 음성은 legacy 구성 오류·Init −1/exit 1이었다. 원자료 33개, 공개 보고 4사건, 별도 대조 10회와 C ABI 검증 4회다.

- 저장소 laadkke-arch/agentflow-open. 작업 브랜치 work/research-af-res-217. 시작 87ffc1539bcf33da0fccf45eb15982a02d93e409, 지시 기준 bb146773bbffba5e724e8c842951e2c25198c2da보다 5커밋 앞섰으며 차이는 작업표 한 파일이었다.
- 마지막 결과 SHA **89af301cc161dd22a13b7c8aa47e8c2ed4c75f44**를 원격에서 다시 가져와 확인했다. 이 인계는 해당 결과 직후 마지막 별도 커밋이다.
- 의존 AF-RES-202는 중앙 DONE, 고정 인계 cc543b8d1b8f8748fa363999b76a55f05de2266c다. 202의 자체 판정 PARTIAL과 당시 구성 0/6·실행 0/12를 그대로 전제로 사용했다. [202 인계](https://github.com/laadkke-arch/agentflow-open/blob/cc543b8d1b8f8748fa363999b76a55f05de2266c/docs/workstreams/research/AF-RES-202/HANDOFF.md)
- 실제 실행 위치는 Codex Cloud Linux x86_64, Debian 13이다. 별도 초기화한 Bookworm amd64 패키지의 Tesseract 5.3.0-2와 Leptonica 1.82.0-3+b3를 사용했다. 확인 시각 2026-11-24T21:56:58Z.
- 묶음 커밋 순서 9bba14b(범위·계약) → cf088e3(원장·입력) → 118fe66(구성·본 실행) → c8cb240(반례·오프셋 정정) → 89af301(결과·자체 검토).

## 대표 결과와 실제 판단

- 고정판의 모드 표와 추천은 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/89af301cc161dd22a13b7c8aa47e8c2ed4c75f44/docs/workstreams/research/AF-RES-217/RESULT.md). OEM1은 eng·ara 여섯 모델에서 시작했다. OEM0은 legacy 가능한 빌드에서 tessdata eng만 시작했다. 이 세 모음의 고정 ara에는 OEM0 링크를 제안할 근거가 없다.
- [inputs.json](inputs.json)과 [components.csv](components.csv)에 각 파일의 고정 원출처·지문·구성·실제 파일 위치가 있다. −d 표시 offset과 raw file offset의 4 B 차, A04 config의 낡은 Cube 주석과 현재 OEM1을 대조했다. [CONTRASTS.md](CONTRASTS.md)
- [runs.csv](runs.csv), [본 실행 원출력](receipts/main.jsonl), [대조 원출력](receipts/controls.jsonl)에 실제 파일 경로·Init·프로세스 상태·stdout·stderr와 trace가 있다. 경로 누락, 바이트 파싱, legacy 구성, 일부 언어 성공 및 정상 0 B를 구별한다.
- [sources.jsonl](sources.jsonl), [frame.csv](frame.csv), [SELF_CHECK.md](SELF_CHECK.md)에 자료·사건·실행의 각 분모와 남은 조건을 기록했다. 작성자 자체 대조 및 독립 프로세스 재집계 수행. 별도 독립 검토자, 다른 엔진 빌드 직접 비교, 과거 사용자 환경 및 OCR 정확도 검증은 미실시다.

## 검사와 저장

- GitHub에서 89af301cc161dd22a13b7c8aa47e8c2ed4c75f44를 새 clone으로 열었다. 표 1–3의 열 순서와 6/12/6행, 마지막 약점 3행, 12행의 202 예상·실행 증거, 원장 33/51 산입, CT01–10과 4 B 정정을 확인했다. 새 프로세스에서 components.csv와 runs.csv를 재집계해 cmp 각각 exit 0, recheck.py exit 0을 확인했다. 6개 모델을 새 경로에 다시 받아 지문과 raw header를 재대조했다. [재현 명령과 원로그](receipts/COMMANDS.md)
- 인계 전 실행한 python -B -m workbench.session check docs/workstreams/research/AF-RES-217/session.json --fetch는 2026-11-24T21:56:17.236326Z에 exit 0, passed, remote_checked, stderr 0 B였다. 검사한 작업 SHA는 89af301cc161dd22a13b7c8aa47e8c2ed4c75f44, 당시 통합판은 fc095c323d0177401d34f1daa7b4d1c529e2351f다. scope base는 실제 시작 SHA, 계약 SHA-256은 19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc이며 outside_paths, unmerged_paths, errors는 모두 빈 배열이었다. 통합판의 후속 차이는 작업표 파일이었다. 작업 diff는 소유 경로 안에 있다. [시작 manifest](session.json)
- 해당 새 clone의 깨끗한 89af301에서 python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean도 21:56:16–22Z 동안 exit 0. doctor, acceptance, reference-audit discovery, original-smoke가 통과했다. 전역 check-all은 공유 docs/tasks에 활성 세션 없음으로 보고했다. AF-RES-217 개별 원격 계약은 위 명령으로 확인했다.
- 전체 기록의 획득·검사 명령과 입력은 [COMMANDS.md](receipts/COMMANDS.md)에 있다. 주요 고정 산출물 SHA-256은 RESULT 2802b6d8b304fd36d7b966076d26dc716851c2936a523ca1b9079536c5a48eff, sources f8b51f9ea11dac1dfa709a9bfc17595456e2f29f1ca0ed99c788c03f53c9f781, CONTRASTS 4f28442ec5a4089543c380289da11cfb9cb90100fe20715ce8e6d575d640099f다.

## 색인 반영 제안과 첫 재개 행동

색인에는 **AF-RES-217 · 파일 식별과 Tesseract OEM 실제 초기화 · DONE · 구성 6/6, 실행 12자리×2 · AF-RES-202 cc543b8**로 한 행을 추가할 수 있다. 결과 링크는 고정 SHA의 RESULT.md를, 반례 링크는 같은 판의 CONTRASTS.md를 사용한다. 실제 파일, 효과 모드, 일부 언어 성공, OCR 품질을 독립 관측으로 읽는다.

다음 첫 행동은 GitHub에서 work/research-af-res-217 최신 SHA의 인계와 결과 링크를 다시 확인하고 결과 묶음을 검토하는 것이다. 판정을 재집계할 때 repo 루트에서 python -B docs/workstreams/research/AF-RES-217/receipts/recheck.py를 실행한다. 추가 제품 환경을 적용하려면 그 빌드의 legacy 유무와 실제 선택 파일 지문부터 검증한다.
