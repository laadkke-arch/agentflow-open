# AF-RES-064 인계

**부분 인계.** 고정 12요구·36슬롯·11쌍에서 첫 주소를 바꾼 6쌍을 포함해 A/B의 **두 조건 공동 확인은 각각 0/11쌍, 0/12요구**였다. 개명 허용과 원문 그대로의 판정에서 신규 지지와 손실은 관측 0이다. 예정 A/B 22경로는 모두 재생했고 최종 창은 22/22가 한도 내다. jschon 두 경로의 정정 전후 반복 노출을 제외한 실제 엄격 경로는 **20/22**다. 스캔 원 픽셀과 원 요청 환경의 미확인도 남아 있다.

## 고정판에서 먼저 열 파일

1. [표 1. 12요구와 원순번](https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/RESULT.md#표-1-고정-12요구와-상위-슬롯) 및 [표 2. 11쌍의 창·판정·실행](https://github.com/laadkke-arch/agentflow-open/blob/6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f/docs/workstreams/research/AF-RES-064/RESULT.md#표-2-채운-11쌍의-도착표시실행).
2. [수용 원장 34항목](https://github.com/laadkke-arch/agentflow-open/blob/8f97be50a4071e05e138c5237569e94c512c5abd/docs/workstreams/research/AF-RES-064/evidence/acceptance-evidence.json) 및 [실제 노출 편차](evidence/actual-exposure.json). 첫 재개 행동은 이 둘에서 JS-3/SC-027 W03/W04의 원위치와 이전 노출 제외 사유를 확인하는 것이다.

저장소는 `laadkke-arch/agentflow-open`, 작업 브랜치는 `work/research-af-res-064`다. 최초 시작 SHA는 `598d0238e008479aa65400b5ad8a61f194f08c00`이며 계획판은 `aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75`였다. 선행 AF-RES-060 인계는 `87bd0362f7adce5a5e002036dc71a6fc93eeead1`, 입력 본문은 `ccde193ec33f68fea5eaef1cc6f6cea803e1823f`다. [계약](manifest.json) · [입력 해시](evidence/input-check.json)

## 확인 범위

- 빈 슬롯 25개는 관측 무매치 18, 후보 풀 소진 7이다. A 14행동·6,948단어·31,794 bytes, B 12행동·5,747단어·24,218 bytes였다. B는 2행동을 줄였고 논리 raw bytes는 3,377 늘었다. P 11경로의 실제 엄격 범위는 10/11이다. 과거 060의 611단어와 경계 불명은 이전 81/84 값으로 보존했다. [비용](evidence/costs.json)
- 세 고정판 12/12 입력군을 시도했다. Ajv 8.17.1 합성 draft-07은 두 문자열 ID, 숫자 ID 거부, 빈 객체, 비변경 4/4였다. tsc 소스 빌드가 실패한 뒤 같은 gitHead의 배포판을 사용했다. jschon 0.11.1의 리터럴 입력은 평가 전 실패, 명시적 2020-12 재구성은 4/4였다. Ruby JSON-LD 3.3.2의 리터럴 URL은 BBS context 로드 실패, 이전 singular 및 plural alias는 b/c 값 혼합, 재구성 노드는 C1 4/4와 구조 정확 C2 0/4였다. Ruby가 사용한 코드는 gem과 소스 21파일을 검산했다. [실행 원장](runs.jsonl) · [배포·옵션](evidence/runtime/package-identity.json)
- 단일 Codex Cloud 연구자가 표시기, 창 독해, 실행과 자체 검토를 맡았다. 40개 출처 기록 중 32개를 최소 수에 넣었고 계보는 31개다. 《프랑켄슈타인》의 두 출판판에 대해 인쇄 33과 vii의 고정 스캔 대응 전사를 대조했다. 원 픽셀은 이미지 호스트 프록시 및 뷰어 오류로 미확인이다. [출처 원장](sources.jsonl) · [판·쪽 대조와 오류](evidence/library.md)

## 고정 결과·실제 검사

| 단계 | 원격 SHA | UTC 2026-11-23 | 고정한 내용 |
| --- | --- | --- | --- |
| ① | `6c7e40576337d4f2a71727df901d52a7eeb5d3e1` | 05:06:24 | 36슬롯 및 경계 시험, 목적지 규칙, 세 입력 판정표 |
| ② | `34be54e4423c6683b59c1e79e8646cca395cb0b2` | 05:14:09 | 순위와 같은 소스판의 A/B/P 및 첫 표시 |
| ② 정정 | `cb6935dd693afdfe3ef963059340c0b51716a33c` · `9f5b3fc729ea3eda120fb8d0dd142bda94d21cd0` | 05:15:11 · 05:16:31 | jschon RST 코드·doctest 및 원문 행 검산 |
| ③ 문서 봉인 | `d76d4da64024ab3ca11aff0f84d53b7bbe07ea4c` | 05:18:27 | 조건·환경 판정, 실행 전 문서 digest |
| ③ 실행 | `4ceb21251a5eea9000ae2cdd49fe1d4b94dc6c40` | 05:34:50 | 세 엔진 및 보관판 실행, 비용·노출 |
| ④ 고정 결과 | `6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f` | 05:59:09 | 필수 표, 직접 자료, 자체 검토와 수용 원장 |
| ④ 검사 영수증 | `8f97be50a4071e05e138c5237569e94c512c5abd` | 06:01:27 | 계약과 저장소 검사, 결과판 GitHub 재열람 |

Codex Cloud 셸에서 결과 SHA `6341dce67a4dd4e38f68c2f16c9ae9f499b18f6f`를 검사했다. 05:59:43–05:59:45 UTC의 `python -B -m workbench.session check docs/workstreams/research/AF-RES-064/manifest.json --fetch`는 종료 0, passed, remote_checked였고 outside/unmerged/errors가 모두 빈 배열이었다. 확인 시 통합 SHA는 `88f0fabfecdfbcc4377d75baebd40039128ed637`였다. 같은 SHA의 `python -B scripts/check.py --require-git`도 통과했다. [계약 검사](evidence/verification/session-check.json) · [저장소 검사](evidence/verification/repository-check.json)

GitHub에서 결과 SHA의 RESULT와 수용 원장을 내려받아 로컬 바이트·Git blob·첫 두 표의 실제 DOM ID를 확인했다. 검사 영수증 SHA에서도 두 파일과 계약 영수증을 06:02:05 UTC까지 재열람했다. RESULT blob은 `9cc0b77306cf15a6114d03fc323761a1232620c4`, 갱신 수용 원장 blob은 `75357bc413b545f950cdc26913ce0b86618c2512`다. 빈 캐시·재사용으로 같은 26개 표시와 33경로를 재현했다. 41개 실행 출력의 판정과 값은 재현했고 Ruby 보관판 G1의 loader 호출 순서는 한 번 달라졌다. [원격 재열람](evidence/verification/remote-reread.json) · [재생 및 실행 재확인](evidence/verification/local-replay.json)

## 재개 입력과 색인

[재현 절차](reproduce.md)는 한 쌍과 전체 재생, 검산, 세 임시 환경의 명령을 담았다. 깨끗한 판정자에게 건넬 JS-3/SC-027 자료는 `python -B replay.py --cache <빈 디렉터리> --pair JS-3/SC-027 --output <임시 폴더>`의 output과 060의 requirements.json에서 추린 해당 조건·환경이다. 판정자가 보는 입력은 재생 파일의 해당 경로 텍스트, 행, 액션 수다. 원 실행이 끝나는 최소 추가 입력은 원 runtime·옵션과 BBS 응답 bytes다. 원 스캔 대조의 시작점은 [1818 p33/1831 p33 주소와 실패 원장](evidence/library.md)이다.

색인 편집 시 AF-RES-064를 ‘기능명으로 바꾼 첫 주소의 두 창 이득 관측 0, 실제 엄격 20/22, 세 고정판 실행’으로 등록할 수 있다. RESULT의 두 표와 이 인계, AF-RES-060 결과판을 연결한다.

- jschon을 세 번 읽은 노출 약점 → 이전 창을 모르는 판정자가 최종 W03/W04를 한 번씩 읽는다.
- 넓은 표제와 이웃 절의 관련성 약점 → 좁은 공개 API나 시험 위치를 새 표본에 먼저 봉인하고 같은 창 예산에서 비교한다.
- 원 Ajv/Drupal·JS-3·jsonld.js 환경 및 2021 context 배포 결손 → 원 판·옵션·payload·HTTP 바이트를 확보한 뒤 네 입력군을 해당 환경에서 다시 실행한다.
