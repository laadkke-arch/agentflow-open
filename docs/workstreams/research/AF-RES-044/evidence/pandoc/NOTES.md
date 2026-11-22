# Pandoc route P — sealed requirements; raw HTML blocked

원질의 최초40에 N2/K2 정원을 적용했다. 선택 P1 #6037, P2 #6095, P3 #6126, P4 #6166. 최초15 본문이 한 도구 출력에 노출되었지만 선택은 생성순서 최초 적격이며 16–40은 제목만 보았다. #6087은 저자의 fork 개발/upstreaming 작업 추적이므로 제외했다. 댓글은 요구 봉인 뒤에만 노출되었다.

## 이름층 경계

P3의 일반 HTML/CSS→PDF 방향, P4의 DITA 출력 형식 이름은 기능 이름이다. 특정 입력 표본·구문·보존조건·정확 호출·버전이 없으므로 N이다. 실제 지원 근거 없이는 완전 대안이 아니다. P1은 사용자 지정 checkbox 문자, P2는 두 구체 LaTeX 명령의 대체 텍스트 보존이 필수라 K다. P2의 원요구는 **reader 방향**이다. 나중의 writer 변경을 원요구 해결로 오인하면 안 된다.

## 원풀을 관측하지 못한 이유

`https://pandoc.org/MANUAL.html` raw HTTP403, error code1010. robots/anti-bot 우회하지 않았다. 사전 fallback인 `jgm/pandoc` gh-pages는 없었다. 새로 확인한 공식 `jgm/pandoc-website` 저장소는 source/build files이며 배포 HTML을 제공하지 않는다. 검색도구의 가공 텍스트·URL 목록으로 raw href나 DOM순번, HTML 해시를 만들지 않았다.

`pool-P.csv`의24칸은 **관측 결측**이다. `원풀 완전 대안 수=미확인`, 조건부 회수도 미확인이다. 관측 결측을 실제 후보0·적격0으로 바꾸면 안 된다. 관측된 풀에서 적격이0일 때의 해당없음과 다르다. 이 route가 비교실험 본체에 참여한 것으로 승인하지 않는다.

## 노출·정정

요구 봉인 후 공식 게시HTML의 경로를 찾던 웹 검색이 MANUAL.txt 일부(일반 옵션, PDF engines, 문서 속성 등)를 자동 출력했다. 해당 검색은 `https://github.com/jgm/pandoc-website`를 찾기 위한 것이며 후보로 산입하지 않았다. 요구선정 전 본문 노출은 parent의 pilot-exposure에 이미 있다. 이후 #6095 웹 open에서 댓글·닫힘 commit writer 수정이 노출되었으나 요구는 이미 봉인되었다.

## 다음 첫 행동

원 URL의 발행 HTML을 정상적으로 읽을 수 있는 환경에서 원요구4와 봉인 discovery-plan에 따라 DOM/raw href를 수집한다. source hash·실제 metadata·원순서를 먼저 별도 새 봉인으로 남기고24슬롯을 새 반복 관측으로 수행한다. 과거 미관측을 사후 성공으로 덮어쓰지 않는다.

## 별도 의미진단(주풀/효과 계산에 미산입)

- **P1**: task_lists 기능은 공식 매뉴얼에 있다. 협력자는 필터 사용을 제안했지만 실제 다른 사용자의 필터는 bullet이 다시 보이는 부작용을 보고한다. 지원 이름과 정확 출력 제어는 다르다. 최초 요청자가 출력형식을 안 적었으므로 그 방향은 연구자 해석임도 남겼다.
- **P2**: original reader 요청을 닫은 commit `28e01fac74c88a777dc69c693f1296e46e1d738c`는 writer 및 writer fixtures만 바꾼다. 현재 reader는 includegraphics의 `alt` 옵션은 읽는다. 원요구의 tagmcbegin/alt 두 매크로를 읽는지와는 별개다. completed라는 상태만으로 같은 해법으로 묶으면 방향을 잃는 실제 반례다.
- **P3**: 현재 공식 PDF engine 목록과 `PDF.hs` dispatch는 `pagedjs-cli` HTML→PDF 연동을 확인시킨다. 이것은 일반 추가 엔진 지원의 별도 긍정 근거다. 처음 언급된 Vivliostyle/PDFReactor/Antenna House 각각의 native adapter까지 증명하지는 않는다. 원풀은 결측이므로 이 긍정을 수집·그룹 성공으로 세지 않는다.
- **P4**: 공식 output formats 전 범위를 읽었다. DocBook4/5/JATS/native XML은 DITA writer의 근거가 아니다. custom Lua writer 경로가 있다는 사실로 DITA 구현을 발명하지 않았다. 실제 DITA writer의 존재는 미확인이다.

## source count 및 경계

직접 확인한 고유 원문12개: 원요구4, 공급자/부품/설정6(매뉴얼1·Lua filter문서1·reader/writer/PDF 코드각1·JSON filter문서1), 유지보수자 변경/배포2. 원매뉴얼의 여러 절과 web/source 재배포는 중복제외한다. 실패4, followup3, manual재열람1은 산입하지 않는다. `sources-P.jsonl`20행, counted=true12. 모든 내용은 공개 원문이며 전체 HTML·소스·issue bodies의 임시 사본은 지웠다.

## 최소 재개 자료

정상 raw HTML 접근이 우선이다. 별도 공식 배포자료는 `https://github.com/jgm/pandoc/releases/tag/3.14`(2026-11-12)와 assets의 Windows zip/Linux archive다. **그 내부에 MANUAL.html이 있는지는 아직 확인하지 않았다.** 이것을 게시 HTML로 간주하지 않는다. 최소 재개는 원 manual HTML 정상접근 또는 공식 archive의 member 목록을 확인한 뒤 출처·링크 해석이 맞는지 별도 절차를 사전 고정하는 것이다.
