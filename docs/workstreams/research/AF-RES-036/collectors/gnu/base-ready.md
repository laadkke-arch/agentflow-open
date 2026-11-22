# G 경로: 목적지 관측 전 원 인용 봉인 준비

G01–G06은 서로 다른 출판 문서 6개다. GNU Bash 5.1 원 tarball의 man page와 reference manual은 별도 문서이고, Debian gawk-doc 5.1.0-1의 GNU Awk User’s Guide와 TCP/IP Internetworking With gawk도 별도 책이다. 분할 HTML 장·절 1개를 별개의 책으로 세지 않았다. GNU Make는 make-doc 4.3-2의 한 매뉴얼, GNU gettext는 0.20.2의 FAQ다. 프로젝트 수는 4이며 Bash/Gawk 각각 최대2다. R경로와 합친 전체 프로젝트수는 루트가 검산한다.

| ID | 실제 배포물/문서 | 최초 적격 href의 최소 목적 | 사전 층 |
| --- | --- | --- | --- |
| G01 | bash-5.1.tar.gz / doc/bash.html | POSIX Part 2 Shell and Utilities를 읽음; 문장에 연도/최신 요구가 없음 | ambiguous |
| G02 | 같은 archive / doc/bashref.html | 일반 명령의 programmable completion 예제 모음 | current |
| G03 | gawk-doc_5.1.0-1_all.deb / GNU Awk User’s Guide Preface | **문장이 명시한 2018 POSIX standard** | historical |
| G04 | 같은 deb / TCP/IP Internetworking With gawk | coprocess와 print/printf/getline 양방향 I/O 절 | current |
| G05 | make-doc_4.3-2_all.deb / GNU Make Rules | GCC -M/-MM의 system-header prerequisite 차이 | current |
| G06 | gettext-0.20.2.tar.xz / FAQ.html | newest gettext source release 배포 위치 | current |

## 직접 읽은 범위와 선정

각 source row는 `sources.jsonl`에 있다. `references.jsonl`은 원 href, 링크 텍스트, 문맥, 목적, source line, 정규화 offset, archive/member/context SHA256을 가진다. `base/Gxx.txt`는 수정 없는 원문 발췌이며 최대1200문자다. purpose/stratum은 명시적 조사자 해석으로 원문과 분리돼 있다. B에는 현재 목적지의 상태·관측·교체 권고를 넣지 않았다.

분할 GNU 매뉴얼은 index.html에서 `rel=next` 출판 순서를 따라 본문을 확인했다. Gawk 책 순서는 member path `gawk-html`, `gawkinet-html`, `gawkworkflow-html`이며 앞2개에서 적격 링크를 찾아 프로젝트상한2에서 멈췄다. 동일 manual의 chapter별 외부링크는 다른 표본으로 다시 세지 않았다. Bash reference의 홈페이지·GNU 라이선스·메일 링크는 제외하고 처음의 기술 자료인 bash-completion을 택했다.

GNU 원배포에서 built HTML이 없었던 후보는 coreutils8.32/9.0/9.1, findutils4.8/4.9, gawk5.1.0/5.1.1/5.2.0, make4.3/4.4, tar1.33/1.34, grep3.4/3.5/3.6, sed4.8/4.9다. gawk5.1.1 첫 fetch timeout은 재시도200으로 남았다. Debian의 coreutils8.32-4+b1, findutils4.8.0-1, tar-doc1.34-1 실제 deb에도 HTML이 없었다. Gawk와 Make는 지정된 Debian 대체 유통에서 실제 HTML을 얻었다. make-doc의 첫 추정 source directory는404였고 공식 Debian package 검색에서 source명 make-doc-non-dfsg를 찾았다. 검색 요약은 원문 수에 산입하지 않는다.

grep/sed의 두 공식 Debian 목록에는 기간2020–2022의 amd64/all 후보가 없었다(현재 남아 있는 패키지 날짜 기준). GNU 버전경로 후보는404였다. 이것은 모든 역사 HTML의 전역 부재 증명이 아니다. 관측한 유통 경로와 후보 목록만 소진했다고 기록한다. coreutils의 deb.debian.org에는 두 번째 기간판9.1-1도 있으나 최초8.32 package에서 HTML부재를 확인한 뒤 다음 프로젝트로 진행했다. 이 범위는 HTML 부재를 전체판으로 확대하지 않는다.

Gettext의 C# API book와 Java Javadoc book에는 외부 http href가 없었다. autosprintf는 라이선스와 생성기 footer만 있었다. 앞순서 runtime man pages에도 외부 href가 없었다. FAQ 앞 링크는 mail/contact와 Translation Project 기관 홈페이지다. 이후 첫 도구 배포 경로는 newest source URL이다. 일반 bibliography DOI/법률문서/내비게이션을 적격으로 채우지 않았다.

## 사전 노출 예외 G06

**G06의 원 href `https://ftp.gnu.org/gnu/gettext/`는 G-GET035에서 원 배포를 찾는 directory index로 이미 열었다.** 그때는 FAQ 본문을 아직 선택하지 않았다. 결과를 보고 다른 href로 교체하지 않고 `pre_exposed_current_target=true`로 보존한다. 엄격한 현재 상태 열람 전 봉인 분석에서는 제외해야 한다. 나머지5 목적지는 이 단계에서 요청하지 않았다. 같은 본문에서 현재 동작과 과거 증거를 분리할 수 있는지는 후속 N/H 단계에서 판단한다. 여기에는 유지/교체 정답을 작성하지 않았다.

## 원문·보관·재구성

큰 원 tarball/deb와 전체 추출 HTML은 실제 다운로드 비용/디스크 보관량에 포함되며 현재 작업공간에 있다. 커밋에는 정확한 B 발췌, archive/member/context hash, 원문 위치, 요청 원장과 재구성 코드를 넣는다. `commit-files.json`이 이 작은 필수 묶음이다. 전체 archive를 커밋했다고 주장하지 않는다. 재구성 명령은 `python -B docs/workstreams/research/AF-RES-036/collectors/gnu/reconstruct_base.py --download-missing`이다. 각 archive는 한 번만 취득해 두 reference가 공유할 때 물리1/논리2를 구분한다. 네트워크 재취득은 공개 URI가 계속 접근 가능할 때만 재현된다.

원문 archive목록 날짜는 판 선택 근거로 사용했으며 최초 배포 UTC, 독자 실제 클릭, runtime 동작을 증명하지 않는다. G06의 FAQ 문장 외 해당 버전의 support system 전부를 검사한 것은 아니다. B가 봉인될 때까지 N/H/대체 URI 검토를 시작하지 않는다.
