# AF-RES-123 최종 인계

**PARTIAL.** 대체판의 본 48/48과 대조 36/36, 고유 1차 저작 41개, 두 깨끗한 경로 재생 및 고정 결과 검사를 완료했다. 저자 GIF 원 주소의 shell CONNECT 403과 두 GitHub 별칭의 S3 redirect 목적지에서 shell CONNECT 403 및 web 500으로 GIF 프레임 판독이 막혔다. 공개 본문과 댓글 목록에는 저자의 런타임·뷰어·시작 brush·정확한 포인터 위치가 없다. 실제 원 CSV의 절대 URL·바이트와 제품 채택도 미확인이다. [결과](RESULT.md) · [저자 자료 접근](evidence/issue-8628.json) · [출처 55개 주소](sources.jsonl)

빈 선택에서 6월 막대 위의 1px 오른쪽 move는 두 렌더러에서 1월을 처음 선택했다. 같은 x의 빈 plot은 6월을 선택했다. 비교 가능한 48행 중 16행에서 첫 extent가 계획한 판정과 101 CSS px 차이 났으며 그중 12행은 빈 선택의 막대, 4행은 shared가 기존 overlay를 down에서 접은 뒤 막대가 드러난 조건이다. 초기 선택을 이동한 원형·local은 폭을 보존했다. local fallback은 16/16 짝에서 이동과 최종 범주가 같았고, 두 조건의 정지 표면도 같았다. x가 고정된 수직 이동과 1px band 경계 대조로 좌표 원점 변화와 범주 경계 포함을 구분했다. [본 시도](runs.jsonl) · [SVG와 Canvas 원기록](evidence/main) · [대조](evidence/controls/RECEIPT.md)

기존 범위 전체를 옮길 목적이면 translate, 비선택 외관을 바꿀 목적이면 조건 색, 데이터의 시간 범주를 해석할 목적이면 projection을 돌려줄 수 있다. 사용자의 첫 down 직전 기존 brush와 실제 hit, 첫 move가 보이는 기록 하나를 받으면 우선 절의 적용 조건을 더 정확하게 고를 수 있다. 좌표계 불일치를 고칠 spec 변경은 보류했다. [세 기능 절·조건](RESULT.md) · [48개 전후 반환](decisions.csv)

## 기반과 변경 구조

작업은 Codex Cloud에서 통합판 `3215fdb429e307175b2f277a9a167d2d07361883`로 시작했다. AF-RES-119 `be7d6e3365e090ca674b4f0baaf570a27f8e51cf`를 manifest 의존으로 고정하고 검사판 `038ac865c8d2cada84e32989bdd5eb174f4bb7d8`의 V8628 원형·두 수정·CSV·npm lock을 재사용했다. 기본 관리 checkout의 `work` ref 이름 충돌은 원 상태로 복구한 뒤 별도 GitHub clone에서 작업했다. [범위](SCOPE.md) · [manifest](manifest.json) · [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/be7d6e3365e090ca674b4f0baaf570a27f8e51cf/docs/workstreams/research/AF-RES-119/HANDOFF.md)

`fixture`에 원 CRLF 사양과 의미 diff, 데이터·패키지·font SHA를 고정했다. `plan.json`은 pilot에서 얻은 같은 mark/plot 좌표, 초기 드래그, 두 반복 및 대조 좌표를 담는다. `replay`는 Node의 브라우저 입력, 페이지의 읽기 관측, Python의 판정·별도 검산으로 구성했다. 상태 초기화는 브라우저 드래그이며 관측 단계는 store나 신호를 읽는다. 두 렌더러에 같은 코드와 패키지를 사용했다. 공통 계약을 재사용했고 고정 결과판의 177개 변경은 소유 경로 안이다. [재생](reproduce.md) · [검사한 경로](evidence/acceptance/changed-paths.txt)

## GitHub 검사판

검사한 결과 SHA는 `0a4acb5368e2f064e9b3eb21b52d219de262440f`다. 이전 판과 고정 결과판을 GitHub에서 각각 별도 clone해 npm ci 후 본·대조를 모두 재생했다. 1차 원장과의 비교는 시각 필드를 제외하고 각 84/84 일치했다. 고정 결과판의 `workbench.session check … --fetch`, `cloud_check.py --environment codex-cloud --fetch-contract --require-clean`, `scripts/check.py --require-git`가 종료 0이다. 필수 표 2·24·4행, 본 로그 ID 48개, callback 9,330행, 원 실행 SHA 84개를 다시 셌다. 계약·원장 검산과 브라우저 관측은 같은 작업자의 별도 실행이며 독립 판독은 미실시다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123) · [명령·환경·지문·종료](evidence/acceptance/RECEIPT.md) · [자가 검토](SELF_CHECK.md)

| 묶음 | GitHub에서 다시 읽은 커밋과 대표 파일 |
| --- | --- |
| ① 원문·판·측정 계약 | [da7e4b31b3ec652fbfe0f27dd5f586af51450457](https://github.com/laadkke-arch/agentflow-open/commit/da7e4b31b3ec652fbfe0f27dd5f586af51450457) · SCOPE |
| ② 실행기·pilot·좌표 봉인 | [89c07f5379a364ab443dccf8947db4bce180af46](https://github.com/laadkke-arch/agentflow-open/commit/89c07f5379a364ab443dccf8947db4bce180af46) · plan |
| ③ 본행·원 이벤트 | [1001383dd80873e80ceeeb32f0c085050ea53e91](https://github.com/laadkke-arch/agentflow-open/commit/1001383dd80873e80ceeeb32f0c085050ea53e91) · main receipt와 첫 runs 엔트리 |
| ④ 반대 입력·다른 분야 | [c8d5eed811b03c796efa25cc65924f94aa5dbe56](https://github.com/laadkke-arch/agentflow-open/commit/c8d5eed811b03c796efa25cc65924f94aa5dbe56) · controls receipt |
| ⑤ 재대조·필수 표·자가 검토 | [0a4acb5368e2f064e9b3eb21b52d219de262440f](https://github.com/laadkke-arch/agentflow-open/commit/0a4acb5368e2f064e9b3eb21b52d219de262440f) · RESULT, SELF_CHECK, verification |
| ⑤ 고정 결과 수용 증거 | [37e7429e6060e2771c5cbd9c768f125db99f9bd5](https://github.com/laadkke-arch/agentflow-open/commit/37e7429e6060e2771c5cbd9c768f125db99f9bd5) · acceptance receipt |
| ⑥ 인계 | 이 파일만 추가하는 후속 커밋 |

## 첫 재개 행동

공개 GitHub 첨부를 받을 수 있는 환경에서 다음 입력으로 GIF bytes와 SHA를 먼저 확보한다. 본문, 캡처의 첫 down 전 brush, 첫 이동과 최종 위치를 순서대로 대조한다. 보이는 포인터와 actual input event를 구분하고 GIF에 안 보이는 엔진·브라우저·렌더러는 저자의 호스트 자료가 있어야 채운다.

```sh
af123_media=$(mktemp -d /tmp/af123-media.XXXXXX)
curl -fLsS --max-time 30 \
  'https://github.com/user-attachments/assets/f9e3cffb-5998-4607-b71e-7e090fa71521' \
  -o "$af123_media/8628.gif"
file "$af123_media/8628.gif"
sha256sum "$af123_media/8628.gif"
```

색인 제안 — AF-RES-123 · 동일 차트의 실제 down hit와 구간 이동·신규 선택·투영 링크의 경계 · PARTIAL · [결과](RESULT.md) · AF-RES-119 고정 인계 의존.

| 가장 중요한 불일치·약점 | 다음에 열 자료·할 조사 | 무엇을 보면 판정이 바뀌나 |
| --- | --- | --- |
| GIF와 원 런타임·CSV SHA가 공석이어서 저자 동작을 대체판과 직접 연결할 수 없다. | [공개 첨부](https://github.com/user-attachments/assets/f9e3cffb-5998-4607-b71e-7e090fa71521)와 [원글 정보를 저장한 파일](evidence/issue-8628.json). | 영상과 환경 정보에서 원 down 대상, 첫 움직임과 상태가 확인된다. |
| 5.6.0 배포본의 내부 문자열은 5.5.0이다. 단일 Chromium·DPR의 stack 원점 관측이다. | [번들 지문](fixture/fingerprints.json)과 [수직 반례](evidence/controls/C08-vertical-exit-svg-1.json)를 다른 명시 판과 동일 입력으로 대조한다. | 범주와 실제 hit가 같은데 offset 오차를 재현하지 못하거나 같은 원점에서도 오차가 남는다. |
| 사용자 의도·채택, 독립 판독과 키보드·터치 경로가 미관측이다. | [반환 원장](decisions.csv)과 [분야별 최소 단서](evidence/cross-domain.md)로 가림 판독과 입력별 대조를 진행한다. | 어떤 범위·색을 보존하려는지와 다른 입력에서도 같은 기능 절이 통하는지가 확인된다. |
