# R 세 자리의 사후 배포 대조

## 관측 결과와 분모

| 항목 | 관측 분자 / 원분모 | 해석 |
|---|---:|---|
| 선정된 태그→생성 HTML 커밋 연결 | 3/3 | 입력 SHA를 생성 커밋 메시지가 지칭하고 HTML이 태그의 판을 표시한다. |
| 실제 Pages deployment 객체 | 1/3 | archive 객체만 취득. 성공 상태는 못 읽었다. |
| 역사적 Pages 성공 상태·런 ID | 0/3 | tag Actions 조회는 모두 0건; 현재 API의 부재를 당시 미실행으로 해석하지 않는다. |
| 현재 공개 URL에서 선정 판 표시 | 2/3 | asciicast 2.3.1, bench 1.1.4. archive는 1.1.14. |
| 역사 생성물과 현재 응답의 대표 HTML 바이트 동일 | 2/3자리, 4/6파일 | 각 자리의 index와 대표 leaf 1개씩. 전체 사이트, 부속 asset, JS 실행, 연속 가용성의 분모가 아니다. |
| 독립된 두 소비자 보존 요구 확인 | 0/3 | 사전 C2 미확인 그대로. 두 조건의 동일 역사 배포 충족률은 0/0 산출 불가. |
| 공개 root / dev의 판 차이 | 3/3 | 자동 모드 설정과 현재 다른 판 표시의 실제 짝. |

직접 연 R 자료 원장은 83행이지만 최소 자료량에 산입하는 보수적 계보는 **5개**다. 소비 프로젝트 3계보, pkgdown 공식 계약 1계보, JamesIves 공식 계약 1계보다. bench #151은 동일 릴리스에 연결되는 운영 기록으로서 bench 계보에 합쳤다. 이 조사에서 추가로 확인한 무변경 관측은 asciicast·bench 두 계보이며 아래 한계를 붙인다. 공급자 설명서 여러 파일/판과 동일 원자료 재열람은 계보를 늘리지 않는다.

## 태그에서 생성물, 공개 URL까지

| 사례 | 입력 tag / SHA | 생성물 commit / UTC | HTML 판·generator | 현재 공개 관측 | 한계 |
|---|---|---|---|---|---|
| R1 archive | v1.1.12 / a4c6ec37fc8737a189ca7ec7095ec0161888f9e8 | 45e0d9ebc168cf3632bc2d737c9db2318668a826 / 2025-03-24T12:34:38Z | 1.1.12 · pkgdown 2.1.1 | root·reference/archive_read.html은 1.1.14, dev는 1.1.14.9000 | 생성물과 현재 HTML 모두 읽었으나 동일한 판이 아니다. deployment 2328795124의 생성만 관측, success 미확인. |
| R2 asciicast | v2.3.1 / f992b26f3cb30c799fbb95f6148852d8ae8a7f18 | 92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1 / 2024-01-21T20:53:46Z | 2.3.1 · pkgdown 2.0.7 | root·articles/asciicast-demo.html은 2.3.1, dev는 2.3.1.9000 | 대표 HTML 두 개가 역사 생성물과 정확히 같다. 당시 실제 serving 및 중간의 연속성은 증명하지 않는다. |
| R3 bench | v1.1.4 / 45c72b2dcbba2b181d24c175ebb90ff8ed5eccad | b352fa4902c7fc0d1edc17f957c646072bfd8b9c / 2025-01-16T22:46:16Z | 1.1.4 · pkgdown 2.1.1 | root·reference/mark.html은 1.1.4, dev는 1.1.4.9000 | 대표 HTML 두 개가 역사 생성물과 정확히 같다. 당시 실제 serving 및 중간의 연속성은 증명하지 않는다. |

R1 자료는 R-P003–R-P010, R2는 R-P013–R-P019, R3은 R-P022–R-P028에 있다. 원태그의 사이트 진입 URL, 생성 커밋 메시지, raw Git blob, 현재 사이트 응답을 각각 독립 필드로 저장했다. HTML 내부 링크는 index→대표 reference/article, leaf→`../index.html`, 판 표시는 navbar, generator 표시는 footer에서 읽었다. 각 문서의 출처 링크가 `main`을 가리키는 경우도 있어, HTML 내용의 판이 맞다는 이유로 모든 소스 링크까지 고정판이라고 말할 수 없다.

archive의 원태그 DESCRIPTION이 제시한 root 주소는 지금 최신 정식판을 돌려준다. 이 주소만으로 1.1.12를 달라고 하는 요구에는 충분하지 않다. 그러나 유지관리자가 옛판 URL을 영구 보존하겠다고 말한 근거는 없으므로 약속 위반 또는 실제 운영 실패로 채점하지 않는다. Git에 남은 HTML은 과거 생성물 복구 근거이며, 독자가 원 사이트에서 같은 판을 계속 열 수 있었다는 근거와 다르다.

### 두 무변경 관측의 지문

| 사례·파일 | 역사 생성물 SHA-256 = 현재 응답 SHA-256 |
|---|---|
| asciicast index.html | cd5bab13fd944d99cae00a71e1877d1c140c527cfbea5a9a2d258d0525c2d6f0 |
| asciicast articles/asciicast-demo.html | c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c |
| bench index.html | f5a7eb67c19efc9d0762025f77777a50e03e15699b69da59f1ea5af6df4393af |
| bench reference/mark.html | 2616955d9ab37227e598bd460f6835a8cd746875a444640c9e56012006610e54 |

같은 URL이 살아 있다는 관측에 그치지 않고 내용·판 표시까지 대조했다. 다만 서로 다른 시간대에 모든 파일이 그대로였다는 보장은 아니다. `deployments.jsonl`은 비교한 6개 HTML의 크기·전체 지문·URL·읽은 UTC를 보존한다.

## 책임과 교환 조건

| 사례 | 생성 책임 | 업로드 책임과 중간물 | 호스팅 책임 | 관측된 권한·실행 한계 |
|---|---|---|---|---|
| archive | GitHub Actions에서 설치한 pkgdown; 한 `deploy_to_branch(new_process=FALSE)` 호출 안에서 생성 | 같은 함수가 임시 gh-pages worktree를 만들고 생성물을 git commit/push | 별도 GitHub Pages 설정과 serving | GITHUB_TOKEN을 GITHUB_PAT로 전달. workflow에 contents 권한 block 없음. 실제 유효 scope 미확인. |
| asciicast | pkgdown `build_site_github_pages(new_process=FALSE,install=FALSE)` | `docs` HTML 트리 → JamesIves v4.4.1 → gh-pages; clean:false | 별도 GitHub Pages 설정과 serving | contents:write 명시. 해당 artifact를 branch에 올린 커밋 존재. Pages success 상태 미확인. |
| bench | pkgdown `build_site_github_pages(new_process=FALSE,install=FALSE)` | `docs` HTML 트리 → JamesIves v4.5.0 → gh-pages; clean:false | 별도 GitHub Pages 설정과 serving | job contents:write 명시, 전역 read-all. Pages success 상태 미확인. |

세 workflow 모두 저장소 루트의 패키지·README·man·선택적 vignette를 입력으로 삼고 push, release published, workflow_dispatch를 트리거로 둔다. PR은 빌드만 하고 업로드하지 않는 분기가 있다. 원 설정 및 공식 고정판 구현 근거는 R-P001–2, R-P011–12, R-P020–21, R-P029–37이다.

역사 HTML footer는 generator 표기판을 확인하게 하지만 전체 환경을 고정하지 않는다. `any::pkgdown`과 `r-lib/actions@v2`는 실행 때 해석되는 값이고 실제 설치 로그는 못 읽었다. 따라서 footer의 pkgdown 2.0.7 / 2.1.1과 그 공식 구현은 대조할 수 있으나 R·Pandoc·템플릿·모든 의존 패키지의 당시 판을 추정하지 않는다.

### 한 함수 안에 두 단계가 들어 있는 경우

pkgdown v2.1.1의 `deploy_to_branch()`는 build 호출 뒤 branch push를 수행한다. 같은 코드에서 `subdir`를 지정하면 특정 판의 문서를 별도 경로에 놓을 수 있다. 이 한 함수는 GitHub Pages 서비스를 활성화하거나 최종 URL을 다시 열어 검증하지 않는다. 이름의 deploy를 종단 공개 확인으로 읽으면 경계가 사라진다.

반대로 `build_site_github_pages()`는 이름에 GitHub Pages가 있어도 HTML 및 `.nojekyll`·`CNAME`을 생성하는 함수다. git push는 없다. `CNAME` 생성은 URL path가 루트일 때만 수행되므로 서브경로를 그대로 custom-domain 설정과 합치면 안 된다. R-P033–34의 v2.0.7/v2.1.1 구현을 직접 대조했다.

JamesIves의 해당 고정판 README 역시 성공을 branch 게시 성공으로 정의한다. `folder`, `branch`, `clean`을 쓰는 이 경로에 `upload-pages-artifact`/`deploy-pages` 방식의 artifact ID·environment 설정을 그대로 더해 한 배포라고 부르면 다른 전달 경로를 혼합한 것이다. 두 방식 모두 별도 선택지로는 가능하지만 이 세 프로젝트가 당시 그 artifact 경로를 사용했다는 근거는 없다.

## 안내를 바꾸는 실제 경계

1. **정식판과 개발판.** 세 소비자의 `_pkgdown.yml`은 `development.mode:auto`를 선택했다. 실제 root/dev 응답도 다른 판을 보여 준다. 현재 정식판을 원하는 독자는 root로, 개발 변경을 원하는 독자는 dev로 안내한다. 임의의 옛판 고정 URL을 이 둘 중 하나로 대신할 수 없다.
2. **개발 변경과 정식 사이트 재게시.** bench 유지관리자의 [2025 upkeep #151](https://github.com/r-lib/bench/issues/151)은 필요시 released-site 재게시를 별도 항목으로 표시했다. 같은 tag의 workflow_dispatch와 pkgdown v2.1.1의 원래 재게시 지침을 함께 읽으면 버전 숫자·작업 branch·수동 실행이 다른 결과를 내는 이유를 설명할 수 있다. 체크리스트 완료는 실행 런 증거가 아니다. 이 기록은 A/B 동결 후 발견했으므로 사전 점수를 바꾸지 않는다.
3. **root와 보존할 하위 경로.** R2/R3의 clean:false는 현재 입력에 없는 gh-pages 파일을 남긴다. release/dev 두 출력을 한 branch에 둘 수 있다는 계약이나, 이 옵션만으로 모든 옛판 내용을 보존한다는 보장은 아니다. archive의 임시 worktree 방식과 단순 docs 폴더 복사를 같은 경로라고 부르지 않는다.

## 비용과 짧은 답에 남길 것

비교 보기의 링크 수 A=1/B=2는 설정 수가 아니다. 실제 선택 세 자리의 빌드·게시 운영 공급자는 GitHub(앞 역할은 Actions, 뒤 역할은 Pages) 한 곳이다. pkgdown, r-lib/actions, JamesIves는 사용하는 OSS 구현이며 외부 호스팅 사업자로 추가 계산하지 않는다. 패키지 다운로드 저장소와 CDN까지 포함하는 공급망 전체의 공급자 수는 조사 범위 밖이다.

새 프로젝트에 설정을 옮길 때 대조할 **설정 블록 6개**를 열거할 수 있다: 트리거/입력 ref, R·Pandoc·의존성, generator와 출력 위치, branch 전달, token/write 권한, URL와 release/dev 정책. 이는 실측 작업시간이나 자동으로 남은 작업 6개라는 뜻이 아니다. 실제 원 프로젝트에는 여섯 블록에 해당하는 설정이 이미 존재한다. 별도 Pages 게시 원본·DNS·UI 권한 설정은 직접 관측하지 못했으므로 **추가 미확인 1블록**으로 둔다. archive의 유효 write scope도 미확인이다.

릴리스 담당자의 공개 작업 기록은 workflow와 bench 체크리스트까지다. 수동 승인이 필수였는지, 수행 시간, 실제 청구액은 미확인이다. 독자의 추가 확인 비용은 먼저 대표 HTML 두 개와 판 라벨을 읽는 것으로 측정 범위를 정했고, 세 자리 총 6파일을 역사 생성물과 대조했다. 이미 취득한 로컬 HTML을 다시 읽을 때 새 HTTP 요청을 만들지 않았다.

세 카드의 첫 선택은 **B(원본에서 HTML을 만들고 gh-pages에 올리는 교환 조건 포함)**가 설명 범위를 충족한다. 기존 R 빌드와 branch가 이미 완성되어 있다면 A의 Pages 설정 링크만으로 다음 게시 행동을 안내할 수도 있다. 이는 준비 상태에 따른 조건부 대안이지 새로운 배포 성공 판정이 아니다. 보존 목적이 불명확할 때 물을 한 필드는 “현재 정식판을 가리키는 주소면 충분한가, 특정 옛판에 고정해야 하는가”다. root/dev 실제 짝과 archive의 현재 root 변화가 이 필드의 실질성을 보여 준다. 특정 옛판이면 generator의 별도 subdir와 보존 정책 및 최종 URL 확인을 붙여야 한다.

## 미확인과 재개 입력

- archive deployment 객체 `2328795124`의 statuses URL이 첫 재개 지점이다. HTTP 403 응답은 공개 unauthenticated GitHub API rate limit remaining=0, reset=2026-11-23T14:22:27Z라고 밝혔다. 반복 요청으로 우회하지 않았다. GitHub connector는 deployments endpoint를 지원하지 않아 400을 반환했다. 공개 `/deployments` 페이지 시도는 404였다. 다음 정상 접근에서 성공 state·log URL·게시 URL을 확인해야 한다.
- R2/R3 deployment lookup도 403으로 미확인이다. 입력과 gh-pages 출력 SHA가 `deployments.jsonl`에 있어 그대로 조회를 재개할 수 있다. GitHub connector의 combined status 조회는 세 출력 모두 빈 배열이었다.
- 모든 태그에서 C2 원요구를 찾지 못했으므로 사용자 목적을 보존 판정으로 추측하지 않는다. 사후 bench 운영 기록도 C2의 대체 근거가 아니다.
