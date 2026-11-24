# AF-RES-139 최종 인계

**PARTIAL.** simple-statistics 30판의 두 공개 함수에서 126셀씩 실행했다. 두 깨끗한 경로와 결과판의 새 경로에서 각각 3,780셀을 확인했다. 발표순 29쌍은 스칼라 변화 0, 불변 29, 미확인 0이다. 따라서 검출률은 산출 불가다. E는 2쌍을 강제로 확인했고 D는 23쌍을 다시 확인했다. 사후 배열형 p는 6.1.0→6.1.1에서 변했고 C는 이 경계를 생략한다. 34개 고유 원전을 읽었다. SWR의 같은 서비스일 기본·임시표 셀과 ONS의 잠정·개정 공표 표시를 확인했다. ONS Table 1 원표 ZIP 둘의 시트·셀은 미확인이다. [결과](RESULT.md) · [검산](SELF_CHECK.md) · [도메인 셀](domain-cells.csv)

## 기준·검사

- 계획판 `1d65b0b7aaef85350df8842dfc05a6be69148b38`, 작업 시작 GitHub 통합판 `588e642b99e695e710573b9418b60364d7f3880b`. 기존 원격 작업판이 없어서 그 통합판에서 시작했다. 유일한 등록 선행 AF-RES-135의 고정 인계 `880833d80f8547e91e42f1d2269c7d4d4a31c0a7`, 원장·결과 `a6a52f73843d8340024cdefb9c6cba7b0b73621c`를 읽었다. 135의 중앙 DONE과 인계 PARTIAL을 분리했다. [manifest](manifest.json) · [135 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/HANDOFF.md)
- 결과 겸 검사 SHA `1aabc75823d6f919ac74ca9e06cfc8d1b614f2ec`. 새 checkout의 공개 require 30회, 독립 집계, `workbench.session check … --fetch`, `scripts/check.py --require-git`, Cloud 공통 검사 종료값은 모두 0이다. 직접 세션 검사는 검사 시 최신 통합 `c2abce983c8f1126bb34b499e0999fcf0c5f1199`를 가져왔다. 결과판 변경 40경로가 모두 소유 범위다. manifest를 제외하는 세션 검사에는 39경로다. Cloud 공통 명령의 일괄 세션 카탈로그는 활성 세션 0을 반환했고 이번 manifest는 직접 명령으로 별도 검사했다. [명령·종료·stdout/stderr·대상 경로](evidence/acceptance.json)
- 제3차 설치의 경로는 `/tmp/af139-fixed-run-C`, 캐시는 `/tmp/af139-fixed-npm-C`였다. 고정 입력 SHA-256과 판별 lock/진입점 지문, 다시 읽은 행의 SHA-256을 검사 기록에 보존했다. 두 원래 경로의 raw만이 고정 정답 비교의 입력이다. [재생](evidence/replay.json) · [원자료](runs.jsonl)

## 묶음과 원격 재열람

| 묶음 | 원격 고정판과 대표 파일 | 관측 |
| --- | --- | --- |
| ① 모집·입력·신호 정의 | [dc1f97f96a3fbf5b781a6e3b538bad34ad737507 · SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/dc1f97f96a3fbf5b781a6e3b538bad34ad737507/docs/workstreams/research/AF-RES-139/SCOPE.md) | 공식 tar 실행과 변경 문구 판독 전에 모집 및 비교 규칙 고정 |
| ② 배포·시점·신호 예측 | [38ac75a5a8196575216e6c0d6644e3c5c0769902 · signals](https://github.com/laadkke-arch/agentflow-open/blob/38ac75a5a8196575216e6c0d6644e3c5c0769902/docs/workstreams/research/AF-RES-139/signals.csv) | 양 순서, A/C/D/E 및 단독 F/N, 30판 잠금. 첫 Node 공개 호출 전에 원격 바이트 확인 |
| ③ 실행·출력 전용 비교 | [0e0185ecb9500fc84f9eb995999b5ad7e0036412 · output-pairs](https://github.com/laadkke-arch/agentflow-open/blob/0e0185ecb9500fc84f9eb995999b5ad7e0036412/docs/workstreams/research/AF-RES-139/evidence/output-pairs.csv) | 두 경로·전체 값·예외·배열, 양 순서의 raw 전용 비교. 신호와 결합 전 봉인 |
| ④ 경보·질의 비용 | [fe64f3d42a44258297eeff57e6211c1ea91ef795 · cost-summary](https://github.com/laadkke-arch/agentflow-open/blob/fe64f3d42a44258297eeff57e6211c1ea91ef795/docs/workstreams/research/AF-RES-139/evidence/cost-summary.csv) | 518 질의, 42 합계, 사후 배열형 p 별도 |
| ⑤ 타 분야 셀 | [58fea3078ac18c20658c60e6e55941faa1c78211 · domain-cells](https://github.com/laadkke-arch/agentflow-open/blob/58fea3078ac18c20658c60e6e55941faa1c78211/docs/workstreams/research/AF-RES-139/domain-cells.csv) | SWR 계획표 2셀, ONS 표시 2셀, 고유 원전 34 |
| ⑥ 결과와 확인 | [1aabc75823d6f919ac74ca9e06cfc8d1b614f2ec · RESULT](https://github.com/laadkke-arch/agentflow-open/blob/1aabc75823d6f919ac74ca9e06cfc8d1b614f2ec/docs/workstreams/research/AF-RES-139/RESULT.md) | 세 표와 Q1–Q7, 검토표, 독립 계산 |
| ⑥ 검사 영수증 | [d91805f6d046977035380be6bae22c00f0a3a4f7 · acceptance](https://github.com/laadkke-arch/agentflow-open/blob/d91805f6d046977035380be6bae22c00f0a3a4f7/docs/workstreams/research/AF-RES-139/evidence/acceptance.json) | 12:55:12.987 UTC 원격 HTTP 200, SHA-256 `169f28282587db01740db8de75cdb25d1d1cfdb94fd34e30968d4c5c68d493b1` 일치 |
| ⑦ 인계 | 마지막 별도 커밋의 이 파일 | 분기 head에서 최종 재열람 |

[원격 파일 재열람 원장](evidence/remote-reads.jsonl)에 ①~⑥ 각 고정판의 HTTP·시각·로컬/원격 일치 지문이 있다. 출력 전 예측과 출력 전용 판독의 SHA는 그대로 보존했다.

## 실제 구조와 범위

AF-RES-135의 tar 무결성 검사·파일 취득·원장 기록을 `replay/common.py`에 맞춰 재사용했다. 모집, 예측, Node 공개 진입, 출력 판독, 경보·비용 재생을 각각 작은 스크립트로 두었다. 공통 로더와 사례 직렬화는 두 함수와 두 설치 경로에서 함께 쓴다. 출력 전용 판독은 고정 입력과 실행 로그만으로 먼저 실행했다. 사후 벡터 입력은 별도 진입과 원 로그다. 런타임 직접 의존이 있는 판은 없어서 공유판 맞춤 설치 추가 0회다. NaN 인수의 정렬 사본은 사전에 NaN-last로 정했고 6.1.1의 공개 번들 대응 미해소는 강제 판정으로 남겼다. [범위](SCOPE.md) · [재생 코드](replay/) · [반례](evidence/counterexamples.json)

미실시는 ONS ZIP 워크북 원표, SWR 실제 운행과 당일 추가 지시, 과거 사용자 npm 설치·다른 런타임·ESM, 삭제된 과거 공지의 존재 여부다. 소프트웨어 관측은 135의 OpenLayers·d3 또는 브라우저를 다시 실행하지 않고 새 패키지에 적용했다. 통합 진행표는 이 작업 diff에 없다. [범위 검사](evidence/acceptance.json) · [출처 및 접근](sources.jsonl)

색인 제안 — AF-RES-139 · simple-statistics 30판의 quantile·median 재확인 신호, 질의 이월 비용 및 ONS/SWR 대조 · PARTIAL (ONS 원표 ZIP) · 선행 AF-RES-135. [결과](RESULT.md)

## 첫 재개 행동

ONS가 배포한 2023 잠정·개정 ASHE Table 1 ZIP을 두 본문 모두 받을 수 있는 환경에서 아래 명령으로 읽는다. 이 Cloud 셸에서는 연결 터널 403, 웹 파서에서는 ZIP 다운로드 형식으로 인해 본문을 받지 못했다. 업로드나 권한 변경을 진행한 상태는 아니다. [원표 목록](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/allemployeesashetable1) · [취득 영수증](evidence/external-access.json)

```sh
ons_scratch=$(mktemp -d /tmp/af139-ons.XXXXXX)
ons_tables='/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/allemployeesashetable1'
for edition in 2023provisional 2023revised; do
  curl -fSsLG 'https://www.ons.gov.uk/file' \
    --data-urlencode "uri=$ons_tables/$edition/ashetable1$edition.zip" \
    -o "$ons_scratch/$edition.zip" || exit
  sha256sum "$ons_scratch/$edition.zip"
  unzip -l "$ons_scratch/$edition.zip"
done
```

두 ZIP에서 Gross annual pay의 UK full-time, both sexes, median 열, 2023-04-19가 들어 있는 기간의 단위 GBP/year와 1년 이상 근무 조건을 찾아 고정한다. XLS는 xlrd, XLSX는 openpyxl의 data-only 읽기를 사용한다. 파일명·워크시트·표시 주소·실제 셀 값·단위와 게시판의 £34,963/£35,004를 비교한다. £17.40/£17.52 시간당 추정은 초과근무 제외라는 단위가 맞을 때만 보조 대조에 사용한다. [ONS 2024 개정 설명](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2024#data-sources-and-quality)

소프트웨어 재생은 Node v24.22.1, npm 11.9.0 환경의 결과 checkout에서 아래 명령을 사용한다. 새 디렉터리와 캐시를 만들고 증거 재계산 출력은 임시 경로에 둔다.

```sh
root=docs/workstreams/research/AF-RES-139
scratch=$(mktemp -d /tmp/af139-replay.XXXXXX)
python -B "$root/replay/run.py" --cohort A --folder "$scratch/run-A" --cache "$scratch/npm-A" --output "$scratch/A.jsonl"
python -B "$root/replay/run.py" --cohort B --folder "$scratch/run-B" --cache "$scratch/npm-B" --output "$scratch/B.jsonl"
python -B "$root/replay/compare.py" --first "$scratch/A.jsonl" --second "$scratch/B.jsonl" --out "$scratch/rebuilt"
python -B "$root/replay/audit.py" --fresh-run "$scratch/A.jsonl"
python -B -m workbench.session check "$root/manifest.json" --fetch
```

| 중요한 불일치·약점 | 다음 조사·자료 또는 실험 | 결론을 바꿀 관측 |
| --- | --- | --- |
| 29개 스칼라 쌍은 모두 불변이고 6.1.1의 배열형 p는 달라졌다. | [사후 원로그](evidence/posthoc-array-p.json)의 두 p 벡터와 깊은 위임 입력을 미리 고정한 별도 실험에 넣는다. | E가 실제 벡터 변화를 강제 확인·공지·본문 신호 없이 놓치면 권장 반환 범위를 줄인다. |
| 매 발행에서는 E가 D보다 적게 실행한다. 두 끝판 질의의 실행 수는 A와 같고 취득은 더 크다. | [비용 원장](costs.csv)을 바탕으로 보존 캐시에서 실제 타르 취득과 사용자 대기를 같이 잰다. | 캐시 지속성 또는 실행 단가가 달라져 중간판 검사 순비용을 역전시키면 정책 선택을 바꾼다. |
| ONS 공표 표시와 SWR 계획표 반례는 확인했다. ONS의 구판·개정 원표 좌표, SWR 실운행은 미확인이다. | 위 ONS ZIP 두 개에서 같은 연간 중위 셀을 읽고 필요한 운행 기록은 별도로 확인한다. [셀 원장](domain-cells.csv) | 원표의 판간 관계가 표시와 다르거나 SWR 당일 지시가 임시표를 바꾸면 적용 범위를 수정한다. |
