# AF-RES-049 인계

## 1. 식별

- 작업 AF-RES-049#1, codex-cloud. 지정 브랜치 `work/research-af-res-049`에서 Linux 클라우드 셸과 GitHub 연결을 사용했다.
- 저장소 `laadkke-arch/agentflow-open`, 허용 경로 `docs/workstreams/research/AF-RES-049/`.
- 계획 통합판 `d8c8d029bfb6107520ae74d2a172b2b18840e764`. 실제 시작·마지막 갱신 확인 통합판 `522ea9092d4d56ef6db0bd4f707bfc90032e179e`. 의존 인계 `7649739855299e7c054286d5d5126a76c701fd01`, 045 결과·코드 `29c5da579b7a29118f31541092e6a51f3d77219d`. [manifest](manifest.json) · [시작 영수증](evidence/session-start.json)
- 고정 결과 SHA **`ab50b40bd12109fb13c29f2f0256e6654ae81c47`**. 원격 재열람 2026-11-23T00:30:07.707Z, 계약 검사 2026-11-23T00:30:07.634019+00:00.
- **부분 인계**. 정량 재생과 저장 증거는 완료했다. #13600 원본 첨부 2개와 Adobe CS6 지정 2쪽의 직접 판독이 미충족이다. 세 layout 실패의 PNG 픽셀은 미확인이다.

## 2. 요구 범위와 결론

3.0.2/Agg에서 M03 A의 text anchor는 두 factor에서 축 비율 (.5,.5)였다. B는 .01에서 (.505051,.505051)로 그려졌고 .001에서는 (5.050505,5.050505) 및 layout 예외가 반복됐다. 2.2.2에서는 A와 B가 두 factor에서 같은 중앙 및 같은 PNG였다. 실제 y=.5를 주석하는 목적과 축 프레임 가운데를 함께 요구하면 혼합 좌표를 쓴다. M02는 10개 모두 판독됐고 30개 B는 데이터 축을 C와 같게 유지하면서 12개 이름을 표시했다. 두 원리가 M02에서 조건부 B를 내므로 동률 대조다. [결과 표 1](RESULT.md#L1) · [결과 표 2](RESULT.md#L28) · [반환 카드](cards.md)

## 3. 원격 커밋

| 묶음 | 고정 SHA | 근거 |
| --- | --- | --- |
| ① 표본·판정·노출 | [ef159f3b81ab210003668be9ffd0faa82c450b09](https://github.com/laadkke-arch/agentflow-open/commit/ef159f3b81ab210003668be9ffd0faa82c450b09) | SCOPE, 28 예정 행, 시작 영수증 |
| ② 원문·입력·기준선 | [a920b7835593bf19b7a03ddfe7ccc4bc28456e6d](https://github.com/laadkke-arch/agentflow-open/commit/a920b7835593bf19b7a03ddfe7ccc4bc28456e6d) | 직접 원문·fixture, 배포 해시와 첫 출력 전 x 보충 |
| ③ 새 관측·짝 비교·반례 | [4946188ca809d59277c2766ad7e4d660131c29de](https://github.com/laadkke-arch/agentflow-open/commit/4946188ca809d59277c2766ad7e4d660131c29de) | 28 관측 JSON, 25 PNG, PNG 판독·명령 로그 |
| ④ 결과·자체 검토·수용 원장 | [6ba96529bd5828acc025027ee6f720156a361b2f](https://github.com/laadkke-arch/agentflow-open/commit/6ba96529bd5828acc025027ee6f720156a361b2f) | 두 필수 표, 카드를 포함한 결과 및 검산 |
| ④ 고정 결과 및 검사 영수증 | [ab50b40bd12109fb13c29f2f0256e6654ae81c47](https://github.com/laadkke-arch/agentflow-open/commit/ab50b40bd12109fb13c29f2f0256e6654ae81c47) | ④ 결과의 원격 재열람과 작업 계약 통과, A24 갱신 |

이 파일은 고정 결과 확인 뒤 `HANDOFF.md`만 포함하는 마지막 커밋이다. 커밋 ID는 `git log -1 --format=%H -- docs/workstreams/research/AF-RES-049/HANDOFF.md`로 찾는다.

## 4. 실행과 검증

| 구획 | 실행/예정 | 정상 PNG | Layout 예외 | 미실행 |
| --- | ---: | ---: | ---: | ---: |
| 3.0.2 주패널 | 20/20 | 18 | 2 | 관측 0 |
| 2.2.2 판 감도 | 4/4 | 4 | 관측 0 | 관측 0 |
| 3.0.2 목적 감도 | 4/4 | 3 | 1 | 관측 0 |

주패널 9 PNG 쌍은 파일과 디코딩 RGB가 동일했고 한 쌍은 같은 layout 실패다. M03 저장 성공 13행의 수치 anchor와 RGB 차분이 허용오차 안에서 일치했다. M02 판독은 서로 다른 원 PNG와 R1/R2 동일 바이트로 교차 확인했다. 저장 단계 실패는 관측 0이다. 고유 원전 34개는 요구·후속 4, 구현·회귀 8, 공식 환경 14, 인쇄·도판 4, 지도·라벨 4다. 직접 열람 불가 3행은 산입에서 뺐다. [runs.csv](runs.csv) · [sources.jsonl](sources.jsonl) · [명령 영수증](evidence/command-receipts.json) · [수용 원장](evidence/acceptance-evidence.json)

아래 명령을 고정 결과 체크아웃에서 실행했다. 시작 2026-11-23T00:30:06.834940+00:00, 종료 2026-11-23T00:30:07.640020+00:00, exit **0**, stderr 빈 문자열. stdout에서 114개 `changed_paths`는 모두 허용 경로였다. 아래에는 경로 목록만 생략했다. 직전 결과판의 전체 stdout·stderr는 [session-check.json](evidence/session-check.json)에 있다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-049/manifest.json --fetch
```

```json
{
  "status": "passed",
  "task_id": "af-res-049",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T00:30:07.634019+00:00",
  "checked_out_commit": "ab50b40bd12109fb13c29f2f0256e6654ae81c47",
  "task_base_commit": "522ea9092d4d56ef6db0bd4f707bfc90032e179e",
  "integration_commit": "522ea9092d4d56ef6db0bd4f707bfc90032e179e",
  "scope_base_commit": "522ea9092d4d56ef6db0bd4f707bfc90032e179e",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

| 고정 결과 원격 재열람 | Git blob | 확인 |
| --- | --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/RESULT.md) | `148d577aecebe0be0f23b174a1af6f373b7bdf9c` | 로컬 내용과 동일, 표 1 주패널 20·판 감도 4행, 표 2 두 행, 마지막 약점 세 행 |
| [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/evidence/acceptance-evidence.json) | `74c8674f59178517f06f3a5284a4abb6b7bf0270` | 로컬 내용과 동일, A24 충족, 부분 인계 유지 |

[deliverable-validation.json](evidence/deliverable-validation.json)의 구조·원장·PNG 검산은 exit 0이다. 초기 호스트의 3.0.2 wheel 불가와 micromamba 등록 실패는 별도 기록했다. SHA를 확인한 Anaconda Python 3.6.8과 PyPI wheel의 분리 설치로 복구했다. 당시 Windows/TkAgg, 별도 호스트와 별도 판독자 및 도너 채택 인과는 미확인이다. [환경과 실패 원장](evidence/environment.json) · [짝 비교](evidence/replay-pairs.json)

## 5. 부분 충족과 다음 첫 행동

첫 행동은 브랜치 head에서 이 인계의 단독 변경과 고정 결과 SHA를 대조한 뒤, 원문에 직접 접근 가능한 환경에서 #13600의 .01/.1 PNG 및 CS6 PDF 300–301쪽을 여는 것이다. 접근 가능한 경우 아래 정확한 입력을 쓴다. 실패한 현행 환경의 egress 403과 브라우저/문서 크기 제한은 원장 I01-A/B와 P01-F에 있다.

```sh
AF049_READ="$(mktemp -d /tmp/af049-originals-XXXXXX)"
curl -fL 'https://user-images.githubusercontent.com/48286302/53886840-3c395700-4021-11e9-9da3-09ce1f8f810d.png' -o "$AF049_READ/issue-13600-factor-0.01-normal.png"
curl -fL 'https://user-images.githubusercontent.com/48286302/53887412-81aa5400-4022-11e9-842a-9a0d8f3f496a.png' -o "$AF049_READ/issue-13600-factor-0.1-extra.png"
curl -fL 'https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf' -o "$AF049_READ/indesign_reference.pdf"
pdftotext -f 300 -l 301 -layout "$AF049_READ/indesign_reference.pdf" "$AF049_READ/cs6-300-301.txt"
```

현재 수신 출력 재생은 [고정 명령](reproduce/README.md)을 따른다. 경계 B의 guard만 바꾼 별도 실행에서는 Matplotlib 3.0.2, factor .001, 기본 data transform, rect [0,0,1,.95]와 원래 PNG 크기를 유지한 뒤 [#13603의 guard](https://github.com/matplotlib/matplotlib/pull/13603/files) 변경을 별도 판으로 기록한다.

색인 제안 — AF-RES-049 · Matplotlib 색 막대 좌표와 범례 동률 대조 · 부분 인계 · `docs/workstreams/research/AF-RES-049/RESULT.md` · AF-RES-045 의존, 주패널 20·판 감도 4·원전 34.

## 6. 마지막 약점

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 3.0.2 M03 경계 B에 PNG가 없음 | 경계의 실제 B 글자 픽셀 비교 | [runs L5/L15](runs.csv#L5) · [#13603](https://github.com/matplotlib/matplotlib/pull/13603/files) | 같은 입력에 guard만 바꾼 별도 출력 | 원판 저장이 관측되거나 변경판의 별도 범위에서 픽셀 확인 |
| 도너만의 효과 및 독자 해독은 미확인 | 원리 제공의 추가 효용과 M02 30개 전체 식별 | [판독](evidence/png-readback.csv) · [기존 API](https://matplotlib.org/3.0.2/tutorials/advanced/transforms_tutorial.html#axes-coordinates) | API만 준 군과 도너 제공군을 같은 목적에서 비교 | 경쟁 예측 분리와 추가 효과를 관측 |
| 원문 생성판·첨부·Adobe CS6 지정 페이지 미확인 | 당시 작성자 출력 및 출판판의 비교 | [I01-A/B](sources.jsonl#L5) · [P01-F](sources.jsonl#L33) | 두 PNG와 Adobe PDF 300–301쪽의 직접 열람 | 원본과 대상판의 대응 및 역사 환경 위치를 확인 |
