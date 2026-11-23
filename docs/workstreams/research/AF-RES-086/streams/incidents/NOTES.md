# Q6 — 생성·게시 성공과 독자 경로의 불일치

## 판정과 분모

**강한 완결 반례는 첫12건에서0/12, 별도 후속4건에서0/4다.** 이는 반례 부재의 증명이 아니다. 실제 발행자가 남긴 생성 산출물·게시 success·잘못된 공개 JSON을 함께 연결한 사건1건을 찾았지만, 회복 직후 JSON의 내용 지문과 해당 원 run 재열람을 확보하지 못했다. 이 부분 연결은082보다 진전이며, 엄격한5요소 완료 조건은 그대로 둔다.

검색 프로토콜을 실행 전에 `PROTOCOL.md`에 기록했다. 네 저장소에서2024–2025년에 생성된 이슈를 같은 검색식·created ascending으로 찾아 각각 첫3건을 고정한 **층별 첫12건**이다. 전체 사건에서 무작위로 뽑은 표본이나 네 서비스의 전체 오류율이 아니다. 서버 조회는 병렬로 했고, 아래 검토 순서는 생성 UTC·번호로 정렬했다. 이후 발견한 관련4건을 추가하되 처음의 탈락 자리를 교체하지 않았다. RTD 검색의30행 상한도 보존했다.

| 집계 | 결과 | 의미 |
|---|---:|---|
| 먼저 읽은 사건 |12/12|네 계열에서3건씩; 부적합한 원자료도 자리 유지|
| 먼저 읽은 것 중 관련 자료 |8/12|로깅·폼·forge 기능요청·테마 안내4건은 최소 원자료량에서도 제외|
| 별도 후속 사건 |4/4|RTD11531, mike229, deploy-pages383, mike248|
| 직접 읽은 고유 이슈 |16|같은 사건 댓글·다른 프로젝트 재현은 중복 계보로 계산|
| 보수적 관련 독립 계보 |12|처음8+후속4; typst 재현은383 계보|
| 원장 행/최소량에 넣는 고유 원자료 행 |42/19|댓글·검색·오탐·404·빈응답 제외; 같은 사건은 여러 행이어도 계보 하나|
| 생성물+게시success+틀린reader내용 연결 |1|typst catalog 사건; 회복 지문 부족|
| 완결 강한 반례 |0/12 및0/4|두 분모 합산·고정 소비자4자리와 합산하지 않음|
| 이 연구자의 새 생성/배포 |0|역사 공개 기록 읽기만 수행|

## 첫12개 고유 사건과 탈락 이유

|순서|생성UTC|사건|판독과 한계|
|---:|---|---|---|
|1|2024-01-03T19:51:48Z|[RTD10990](https://github.com/readthedocs/readthedocs.org/issues/10990)|SysLogRenderer 오류. 독자 경로와 무관해 관련 계보 제외.|
|2|2024-01-05T16:50:55Z|[RTD11001](https://github.com/readthedocs/readthedocs.org/issues/11001)|CherryPy 문서 소실의 원인은 관리자의 프로젝트 삭제. 실제 주소 손실이지만 route-only 오류가 아니다.|
|3|2024-01-17T18:26:58Z|[RTD11042](https://github.com/readthedocs/readthedocs.org/issues/11042)|폼·템플릿 설계 논의. 관련 계보 제외.|
|4|2024-01-24T14:49:57Z|[mike199](https://github.com/jimporter/mike/issues/199)|YAML tag 파싱으로 생성 자체가 실패. 회복 보고까지 있으나 양단 성공의 반례가 아니다.|
|5|2024-02-05T22:40:09Z|[mike202](https://github.com/jimporter/mike/issues/202)|다른forge 지원·설정 안내. 고정 독자URL 사건이 없어 관련 계보 제외.|
|6|2024-02-25T07:10:51Z|[MkDocs3579](https://github.com/mkdocs/mkdocs/issues/3579)|RTD 테마 안내문 범위 논쟁. 관련 계보 제외.|
|7|2024-02-27T18:38:20Z|[MkDocs3583](https://github.com/mkdocs/mkdocs/issues/3583)|gessha.dev build-success 후404라는 발행자 보고. 게시 성공·ref·복구 기록이 없다.|
|8|2024-03-07T12:33:00Z|[MkDocs3593](https://github.com/mkdocs/mkdocs/issues/3593)|404.html의절대CSS경로 오류 제보에 maintainer가 중첩 경로 필요성을 설명. site_url 확인을 받아들인 답변까지; 양단run은 없다.|
|9|2024-07-22T10:30:10Z|[mike223](https://github.com/jimporter/mike/issues/223)|FireFly의 구주소 namespaces는404, `/latest/reference/namespaces/`는존속한다는 발행자 보고. 자동 구주소 이동을 지원하지 않는다는 maintainer 답변.|
|10|2024-08-02T21:35:01Z|[Pages365](https://github.com/actions/deploy-pages/issues/365)|성공한build 뒤assets누락 보고. 해당run10222259682 재조회404, 게시 성공 자료 없음.|
|11|2024-09-19T11:35:57Z|[Pages373](https://github.com/actions/deploy-pages/issues/373)|동일source에publish success로그와404보고. private 원repo의run10939969440은 현재404. 생성·요청전체URL·복구가 빈다.|
|12|2024-10-09T21:24:46Z|[Pages377](https://github.com/actions/deploy-pages/issues/377)|업로드/게시 도구버전 오류, 새게시실패후404. 업그레이드후에도validation error로 끝나므로publish-success 조건 반박.|

`incidents.csv`에는 각각의 원문URL·생성시각·원장ID·한계·다음 최소 확인을 넣었다. 사건의 닫힘 여부를 성공 판정으로 사용하지 않았다. 댓글에 다른 사람의 비슷한 현상이 등장해도 첫12의 독립 사건 수를 늘리지 않았다.

## 가장 가까운 불일치: typst catalog (Pages383 계보)

원자료는 [deploy-pages383의2025-11-15댓글](https://github.com/actions/deploy-pages/issues/383#issuecomment-3536181171)과 그 댓글이 가리킨 [발행자의 dev-builds issue1](https://github.com/typst-community/dev-builds/issues/1)이다. 후자는2025-11-15T06:28:11Z에 생성되고07:18:11Z에 갱신된 원기록이다. 현재 source text를 읽었으므로2025 당시 별도의 아카이브 캡처로 오인하지 않는다.

|단계|직접 읽은 값|증거 주체·한계|
|---|---|---|
|소스|`7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f`; committer2025-10-28T02:45:41Z|Git commit API. 이 시간은게시시각이 아니다.|
|입력·생성설정|같은SHA의gh-pages.yaml은`build_catalog.py`, `RELEASE_EVENT`, 업로드와`deploy needs: build`를연결|고정파일은동적release입력이같은소스에서달라질수있음을설명; 실행성공으로는세지않음.|
|발행된release|record262635061; `typst-main.2025-11-14.0da0165`; published2025-11-15T06:00:00Z|실제release API의두asset목록·size·digest를읽음. 이것은Pagesartifact가아님.|
|게시대상artifact|`4575825543`; created2025-11-15T06:00:13Z;3160bytes; publisher digest `sha256:d53e4f18bc9a7e8b0c1d5dd6ba9f81ac546136d6f89531100a0f80a826c46b87`|발행자가보존한run19385417200의원로그. 연구자가ZIP를다운로드해서얻은hash가아님.|
|게시승인|sourceSHA로생긴deploymentID, `page_url=https://typst-community.github.io/dev-builds/`, success및exit0|발행자의retainedlog. 원runAPI는현재404이고기간조회0건.|
|실제독자경로|`https://typst-community.github.io/dev-builds/catalog.json`; artifact에는2025-11-14와2025-09-19이름이있고응답에는2025-09-19만있다는`jq`출력쌍|발행자가다운로드·curl명령과출력을기록했다. 당시수신자의입증이며연구자당시관측아님.|
|회복|같은commit의dispatch가새artifact를올바르게쓴다고발행자가명시; 재실행은해결못함|정확한회복artifactID·회복후catalog출력/지문이보존된형태로없다. 완결강한반례조건은미달.|

이 사건은 **source SHA를 유일한 게시물 ID로 쓰거나 success 상태를 독자 내용으로 대체하면 안 된다**는 구체적인 경계를 준다. 저장소 소스가 같아도 release 입력과 artifact가 달랐다. 다만 SHA 재사용 하나가 유일한 원인이라는 초기 설명도 후속 2025년 대조에서 약해졌다. 같은 SHA의 dispatch는 내용을 갱신했고 release는 갱신하지 않았다는 원기록이 있으므로, 원인을 SHA 중복 하나로 확정하지 않는다. 생성기 일반의 실패율 또는 모든 Pages 배포의 문제로 확대하지 않는다.

현재 2026-11-23 catalog를 직접 읽었을 때 HTTP 200 / 11,378 bytes였고 선정한 2025 release 이름도 있었다. 이것은 회복의 정확한 2025년 시점을 채우지 않는다. `4ae9e290e75aeae378c18a374046f7c5748dd278b5bc612751ed9f7450b249a3`은 이번 수신 본문의 연구자 SHA256이다. 앞의 publisher artifact digest와 서로 다른 객체다.

## 반대 방향과 다른 경계

**이름이 다르지만 같은 소스판:** [RTD 11531](https://github.com/readthedocs/readthedocs.org/issues/11531)은 2024-08-08에 MESA의 release-r24.03.1 / stable의 footer git hash가 같았는데 경고 배너는 달랐다고 기록했다. RTD 담당자는 수동 stable이 진짜 alias로 동작하지 않는다고 설명했다. 이는 경고문구·별칭만으로 다른 내용판을 선언하는 추론을 반박한다. 전체 페이지 byte 동일성의 직접 증거는 아니다. 현재 stable은 MESA 26.4.1이고 옛 release 주소는 `/en/24.03.1/`로 최종 이동하여 r24.03.1 / Revision 7ecf3dfa를 반환했다. 현재 두 페이지가 다르다는 것이 2024년 보고를 반증하지 않는다.

**같은 실제판의 표시 별칭:** [mike 229](https://github.com/jimporter/mike/issues/229)은 1.0.0의 1.0 / stable 표시가 바뀌는 예다. maintainer는 별칭들이 동등하며 real version에 대한 포인터라고 답했다. 이름 표시가 무작위라는 진술을 실제 독자가 임의의 문서판을 받았다는 진술로 바꾸지 않는다.

**루트 404와 versioned 404:** [mike 248](https://github.com/jimporter/mike/issues/248)에서 `/blog/`에 25.4가 반복 추가되는 현상은 Cloudflare Pages의 루트 404 부재와 SPA 처리로 설명됐다. 발행자는 versioned 404를 루트에 복사한 뒤 정상 404가 나온다고 보고했다. 회복은 구페이지 내용의 복원이 아니라 오류 응답 처리의 정상화다. 현재 GET도 404지만 2025년 회복 시각과 동일 내용을 증명하지 않는다.

**원주소 소실 / 내용 존속:** FireFly의 2024년 원보고는 옛 deep path 404와 새 versioned path 내용 존속을 함께 설명했다. 현재 두 경로는 모두 404여서 현재 본문으로 역사적 동시 제공을 재구성할 수 없다. 지금 링크가 404라는 사실을 2024년 당시 새 경로도 실패했다는 근거로 소급하지 않는다.

## 비용과 재현 범위

실측은 `COSTS.json`과 `attempts.jsonl`이다. GitHub connector 46호출(검색 4, 본문·댓글 32, 후속 10), web 검색 도구 1회 / 검색식 2개, 직접 공개 GET 논리 호출 6회가 있다. connector 내부의 HTTP 요청수·wire bytes는 도구가 노출하지 않으므로 미확인이다. 직접 GET의 수신 본문은 277,631 bytes이며 200 세 건 / 404 세 건이다. MESA 옛 주소 한 건은 redirect를 따랐으므로 논리 GET 6을 실제 HTTP 교환 6이라고 부르지 않는다. TLS·헤더·리다이렉트 응답 바이트는 측정하지 않았다.

독자는 목표 URL의 내용·판표시만 확인할 수 있지만, 역사적 약속을 판정하려면 사건 시각·보관 응답이 추가로 필요하다. 릴리스 담당자는 source / 입력·run·artifact·게시 상태와 반환 경로를 연결해야 한다. 서비스 제공자는 동일 SHA의 다른 artifact·별칭 해석·현재 active 상태와 실제 반환 byte를 대조해야 한다. 이 역할별 필요 필드는 원사건에서 관측했지만 각 역할의 사람 시간·청구 금액은 관측하지 않았다. 본 조사 호출수를 사용자의 보편적 업무시간으로 바꾸지 않는다.

## 다음 최소 확인

1. typst의 2025-11-15 dispatch run #11의 artifact ID와 그 직후 catalog.json 출력을 공개 보관 기록에서 찾는다. 입력은 source `7d14b2f…`, run `19385417200`과 연관 #9 / #10 / #11, 원 URL catalog.json이다. 올바른 2025-11-14 이름의 회복 출력이 식별되면 강한 완결 반례 판정을 바꾼다.
2. MESA 2024-08-08 두 URL의 HTML과 RTD version 메타데이터를 구한다. 소스 footer 동일성에서 실제 본문·절 동일성으로 증거 수준을 높일 수 있다.
3. FireFly 2024-07-22 원 deep path와 새 path의 동시 capture 및 게시 run을 찾는다. 자동 별칭이 구 deep path를 보존하지 못한 범위를 정확히 한정한다.
