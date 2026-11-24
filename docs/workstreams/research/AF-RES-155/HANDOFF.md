# AF-RES-155 HANDOFF — PARTIAL

## 1. 식별과 고정판

- AF-RES-155 시도 1, Codex Cloud Linux 실행과 GitHub 왕복. 단일 작업자의 사전 예측·실행·자기점검이다. 독립 검토나 독자 판독은 미실시.
- 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-155`, 허용 경로 `docs/workstreams/research/AF-RES-155/`.
- 계획 기준 `f140af3179b7d9271710778104ccee5b4812e2ef`, 실제 시작 `898409b64886fba63e0d2c4ffe43b12ab656375e`. 차이는 중앙 진행표 두 커밋, 92줄 추가다. 선행 AF-RES-148은 진행표 DONE, 인계 PARTIAL, 고정 결과 `7afb5730cf9b17effa4413380da69e000e74e15d`.
- 검사한 결과판 **`1c1e68c33507139561abe5160f6f29600ecb81ca`**. 아래 검사는 이 결과판의 새 checkout에서 2026-11-24 16:26:56–16:27:17 UTC에 수행했다. HANDOFF.md는 그 결과판 다음의 단독 커밋이다. 인계 커밋 자체의 SHA는 GitHub에서 이 파일을 가리키는 커밋으로 조회한다.
- 시작은 [session.json](session.json)의 `workbench.session start --fetch`로 고정. 결과판에서 원격 통합판은 `c9399e68ad29da03b751efa7e2d90a16562d3bf0`, 선행 브랜치는 같은 고정 결과 SHA였다. 통합판의 추가 차이는 중앙 진행표 한 파일이다. 계약 2 해시 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`. 결과판에서 소유 경로 50개, 외부 경로 0.

## 2. 결론과 근거

- #9305·#9308의 작성자 명령을 Pandoc 3.1.11에서 재현했다. #9305는 AST에 pre 문자열이 남아도 plain에서 둘째 셀이 빠진다. pre 제거가 지정된 두 줄을 되살리고, HTML reader는 같은 입력을 네이티브 격자 표로 읽는다. #9308에서 CommonMark reader와 중괄호 대조의 plain 결과는 같고 hl_lines AST만 갈린다.
- #15872는 시간상 근접판 Prettier 3.1.1과 Mustache.js 4.2.0 및 CommonMark.js 0.30.0을 사용했다. 기본 escape가 백틱을 바꿔 예상한 경계 파손이 생기지 않았다. 기대 코드 문자는 사라졌다. 같은 템플릿과 대입을 비이스케이프한 구성에서는 포맷을 먼저 하면 코드가 둘로 갈라지고, 확장 먼저이면 렌더링과 문자값이 보존됐다. 작성자 원래 도구·설정·파서가 확인되지 않아 그 프로젝트의 실행과는 구별한다.
- #15853은 `addCartItem` POST 입력과 `updateCartItem` PATCH 출력/기대를 확인했다. 실제 동일 함수와 resolved 설정 및 lint 판이 없어서 해당 실행을 보류했다. 공개 댓글 하나와 403 첨부 시도는 원장에 있다.
- 자연 짝 적격 0/4. 동일 A의 구성에서 출력/권고가 갈린 3행, 음성 2행. 실제 B의 nested 종류가 갈라준 것은 raw가 고정된 조건의 한 짝이다. E2/E3의 B 중복, E4의 동일 길이 C는 유효 판독 결과가 공석이다. 실제 사용자 이해·질문 수·시간을 추정하지 않는다.
- [RESULT.md](RESULT.md)의 표 3개, Q1–Q8, 실제 선택 기반 계약 예 2개와 [SELF_CHECK.md](SELF_CHECK.md)가 결과다. [sources.jsonl](sources.jsonl) 47행에서 고유 외부 자산 28개, 음악 묶음을 합친 계보 26개. 원요청 6, 기술 9, 별개 배포 시험 7, 디지털 문헌 판본 3, 음악 악보 3개를 직접 읽었다. 역사 인쇄 원면은 0/2. K.498은 공식 공개 소스의 총보·파트를 LilyPond 2.24.4에서 재각보해 I m.9의 기보/실음을 보았으며 원 배포 2.16.1 PDF와 동일 지문 확인은 공석이다. [교차 분야 증거](evidence/cross-domain.md)

## 3. GitHub 저장과 원격 재열람

[evidence/remote-receipts.md](evidence/remote-receipts.md)에 앞 묶음의 원격 대표 파일 지문과 UTC를 보존했다.

| 묶음 | 원격 SHA | 실제 다시 읽은 파일 |
|---|---|---|
| ① 범위와 세션 | `932cf329952886bec4fe20a33b248709915a9ca2` | SCOPE.md |
| ② 원본과 사전 봉인 | `dee0da5de6ba1f93d60177d5a9b11f72b8b81557` | predictions.csv |
| ② 재생 코드 | `9f1c49d76cf75589839cf372d6f32bfe4470ab37` | replay/run.py |
| ③ 두 주 실행 | `d275b794cfeec98d9fff56c90cee641d7bea3b39` | runs.jsonl |
| ④ 별도 보정 봉인 | `2cf433e1185fedc499188e786fbf2995a24f86b9` | evidence/escape-amendment.md |
| ④ 반례·비용·원전 | `e17a0edb25a689dd3273045a654a4ac9b76d08a1` | distinctions.csv, sources.jsonl |
| ⑤ 결과·자기점검 | `1aa6db264f1b3400b0546ba9024af1068460a8e9` | RESULT.md, SELF_CHECK.md |
| ⑤ 출처 역참조 보정과 검사 결과판 | `1c1e68c33507139561abe5160f6f29600ecb81ca` | sources.jsonl SHA-256 `1e77a1a5baa58a89534e1f12e0354549507a2ee4435eac0e34cb0504a14ad23f`, 16:26:32 UTC |

[inputs.jsonl](inputs.jsonl), [packets.jsonl](packets.jsonl), [predictions.csv](predictions.csv), [runs.jsonl](runs.jsonl), [distinctions.csv](distinctions.csv), [costs.csv](costs.csv)를 읽을 수 있다. 이번 결과 색인 제안은 `AF-RES-155 / PARTIAL / 이 문서의 결과판과 AF-RES-148 고정 의존`이다.

## 4. 실제 검사

| 실행 명령 | 종료 | 결과와 실제 로그 SHA-256 |
|---|---|---|
| `bash replay/bootstrap.sh TOOL_DIR` | 0 | Pandoc 배포 archive 검사, lockfile 고정 설치, Node v24.22.1. `e88ff78e87c687271ddbec681612cc0676a4eaf2737ab0e64b7a32cb63d98e49` |
| `python -m workbench.session check docs/workstreams/research/AF-RES-155/session.json --fetch` | 0 | 16:27:01 UTC passed, remote_checked, outside/unmerged/errors 0. 위 계약 및 통합·의존 SHA를 확인. `597f0c0997a1695bb1340bc969a44f7a6d7e94a912666e77b3f4c2d78cea21a4` |
| `python replay/run.py --tools TOOL_DIR --repeat final --phase all` | 0 | 20행 중 19 실행, E4 1 미실행. 66단계 종료 0. stdout/stderr/AST를 고정 원장 두 반복에 대조. `7aef35d42d3954691ef16b9971a42ab0fec13da07cb41b679262fe194dae7416` |
| `python replay/check_evidence.py --compare-replay LOG` | 0 | 4 원문 지문, 12 예정/9 실제 packet, 14 fixture, 주·보정 40행/132단계, 결과 재생 20행, 출처 재집계 확인. `705ed9903dce8517a92f169d7c570b3b9f76fa39f746bc45fb713b9aef370a24` |
| `python scripts/check.py --require-git` | 0 | 공통 단위 55, lab 7·9, demo 및 Git bundle 복원 통과. bundle SHA-256 `8ba1477acc16c8789641ef1cc4b23a2b0ea378b9167941955fdb6001cda408e1`. 로그 `a76039c02c62a5c4e68ec771c9f002a32e4feb2feeb99a4ddbd5339b5c87000a` |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 0 | 16:27:10–16 UTC, doctor/acceptance/research-case/original-smoke/sessions 모두 종료 0. 시작·끝 clean. 자동 check-all 내부는 docs/tasks 기준 no_active_sessions다. 자기 폴더 manifest의 명시 검사 결과를 위 별도 행에서 확인했다. 로그 `874c2d5a4b7a5d5e2d9fb9991a189b0c77dfcb3cfdd29804cf5181fb3a6f5dfc`, receipt `43822155030e4dfb9ff3165f9a70a404e7a1629cfd9ef284320cd99ec3c9d899` |
| `git -c core.whitespace=cr-at-eol diff --check BASE HEAD`, `sha256sum -c evidence/music/sha256.txt`(music 폴더 안) | 각 0 | CRLF는 입력 지문 보존 목적. PNG 3개 동일. 작업 checkout 상태 clean. |

실행 입력 SHA-256은 `inputs.jsonl` `bd09583a4431a8e7179aefa414175d88ecfae8a3797cf11305eb7e0a973995a0`, `packets.jsonl` `544ec7f5c4aaf0eabeeef31fa47c13cef94c37419769f380f116774c6ea341f1`, `session.json` `8b256f2910ce057e2d12e4a08987ea8b6f88dab1aa5c5258c4374c92e0ea4195`, lockfile `7838b499e72cd1850b2dba819124233ab2880301214696279eb1766f0ebe027e`, Pandoc 바이너리 `9c91e481cfaac807e20fcb72dadad1e531a9e3f8233d10ade7405bf90d76fd5e`. 두 반복의 실제 입력/출력 지문은 커밋된 [runs.jsonl](runs.jsonl) 전체 SHA-256 `b359fc050c5c620ed4bcb528692ae47df8f76f7eae7b1cb730c8cdde44ba0734` 아래 남겼다. 원장에 공급자 시험 6/6을 별도로 보존했다.

## 5. 첫 재개 행동

GitHub의 인계와 검사판을 분리해 확인하고 새 checkout에서 도구와 결과를 재생한다. 다음 스크립트는 Node v24.22.1과 Python 3.12.14의 Linux x86_64에서 사용한다. 작업 브랜치 최신판이 달라졌으면 아래 고정 SHA로 기존 판정을 재생한 뒤 변경점을 확인한다.

```sh
af155_checkout=$(mktemp -d /tmp/af155-resume.XXXXXX)
git clone --no-tags --single-branch --branch work/research-af-res-155 \
  https://github.com/laadkke-arch/agentflow-open.git "$af155_checkout"
cd "$af155_checkout"
af155_base=docs/workstreams/research/AF-RES-155
git rev-parse HEAD
git show HEAD:"$af155_base/HANDOFF.md"
git checkout --detach 1c1e68c33507139561abe5160f6f29600ecb81ca
af155_tools=$(mktemp -d /tmp/af155-replay-tools.XXXXXX)
af155_output=$(mktemp /tmp/af155-replay-output.XXXXXX.jsonl)
bash "$af155_base/replay/bootstrap.sh" "$af155_tools"
python -m workbench.session check "$af155_base/session.json" --fetch
python "$af155_base/replay/run.py" --tools "$af155_tools" --repeat resume --phase all > "$af155_output"
python "$af155_base/replay/check_evidence.py" --compare-replay "$af155_output"
python scripts/check.py --require-git
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

미완료 비교의 다음 입력과 명령이다.

1. **X05 작성자 경로**는 R03과 R03-X에서 공개되지 않은 실제 formatter/플러그인·Mustache 구현/escape·Markdown parser 버전 및 대응 바인딩을 확보한 후 이어간다. 입력은 `replay/fixtures/template.md`의 UTF-8 CRLF/NBSP 원바이트 및 두 바인딩이다. 기록된 구성 경로의 `run.py --phase main`과 `--phase escape-contrast`를 그대로 둔다. 원래 구현이 확보된 새 작업공간에서 실제 formatter와 확장·파서 argv를 `runs.jsonl`의 대응 세 단계와 비교한다. 작성자 원시 확장 입력과 구성 바인딩을 구별한다.
2. **E4 동등성**은 실제 같은 파일의 입력과 원하는 출력을 고정한 뒤 시작한다. 프로젝트 lockfile의 도구 경로에서 `prettier --find-config-path SAME.tsx`, `eslint --print-config SAME.tsx`, `prettier SAME.tsx > FORMATTED.tsx`, `eslint --format json SAME.tsx`를 순서대로 기록한다. 원 파일을 바꾸지 않고 같은 파일 경로의 적용 설정과 비교해야 한다. 사용자 실행판과 동일 파일이 없으면 E4는 공석을 유지한다.
3. **문헌 원면**은 Folger Q2 [소장 URL](https://digitalcollections.folger.edu/bib163901-157451)의 1.2 첫 독백과 [Bodleian F1 이미지 PDF](https://firstfolio.bodleian.ox.ac.uk/download/pdfs/F-ham.pdf)의 F TLN 297을 열린 기관 경로에서 대조한다. PDF를 정상 다운로드할 수 있으면 `pdfinfo F-ham.pdf`, `pdftoppm -f 2 -l 4 -r 220 -png F-ham.pdf folio`로 원면의 목표 어구를 찾고 면 번호를 남긴다. Q2는 ISE TLN 313과 소장본·서명을 맞춘다. 사람 확인 페이지로 막힌 Folger 소장본은 별도 승인된 접근이나 공개 대체 팩시밀리를 사용한다. 음악은 [Mutopia A4 배포 ZIP](https://www.mutopiaproject.org/ftp/MozartWA/KV498/k498/k498-a4-pdfs.zip)을 열 수 있는 곳에서 `unzip -l k498-a4-pdfs.zip`으로 총보와 파트 파일을 식별하고 `pdftoppm -f 1 -l 2 -r 160 -png INPUT.pdf output`으로 I m.9를 대조한다. 현재 재각보 지문·버전과 결과는 [evidence/cross-domain.md](evidence/cross-domain.md)에 있다.

| 불일치·약점 | 판단에 미치는 영향 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| 자연 짝 0/4 및 X05 실제 구현 불명. 기본 escape는 사전 예측을 뒤집음 | 구성 결과로 실제 제작·소비 도구의 필수값을 단정하기 어려움 | 원 파일과 실제 formatter·Mustache 설정·parser·대입 두 상태 확보 | 정확히 같은 A에서 서로 다른 실제 확장값 때문에 결과가 갈리고 한 근거 필드로 판별 |
| E4 같은 함수 및 effective lint 미확보. 유효 C의 성과 분모 0 | 규칙 추가의 실제 가치 및 무관 문맥 오분기 추정 불가 | 같은 함수에서 원입력, 원하는 결과와 merged config 증거 확보 | 증명 가능한 동일 함수의 진단과 출력이 rule 적용 여부를 드러냄 |
| 역사 문헌 원면 0/2 및 음악 출판 PDF 미열람 | 표면과 편집 표시 해석에 사본·렌더러 차이가 남음 | Folger Q2/F1 허용 원면과 2014 Mutopia 총보/파트 I m.9 | 실제 원면의 철자·편집부호 또는 출판 PDF 같은 마디가 디지털·재각보 판독을 확인하거나 바꿈 |
