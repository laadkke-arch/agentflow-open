# Matplotlib 사전 모집 규칙

이 단계는 3.6.3 발행판만 연다. 발행 SHA `f3ac5407f8ffc861cae1ea87eddd06c63b222e4b`, 판 루트 `3.6.3/`, 완전 판 tree `3252e5b162258de399b9fa614b6854bd9da661f9`의 `gallery/**/*.html` 목록을 전수 열거한다. 새판 tree/본문/변경 설명은 열지 않는다.

## 적격과 제외

한 페이지의 첫 설명용 자원(외부 이미지 또는 내장 data/JS), 설명, 실행 가능한 예제 코드, Download Python source 연결이 함께 있는 첫 논리 예제 한 개가 단위다. `index.html`, `sg_execution_times.html`, 첫 설명용 그림/내장 표현이 있으면 대표 자원으로 삼고, 없으면 첫 예제에 대응하는 실제 Download Python source를 대표 download-python 자원으로 삼는다. `sgskip`처럼 그림 없이 code+download가 있는 사례도 적격이고, GUI/실표시는 미실시로 구별한다. 코드만 있고 연결 자원이 없는 경우와 자료 접근 실패는 분리한다. 첫40 및 같은 source blob 또는 같은 첫 코드+자원 연결의 별칭은 제외한다. animation_demo/pause_resume는 098 계승 예제이며 HBox는 첫40에 포함된다.

코드의 실행 가능성은 저자 Python source와 코드가 존재한다는 정적 판독이다. 이 조사에서 예제 Python을 실행하지 않으며 GUI/JS 실제 표시 여부를 주장하지 않는다. 자동 inventory 목적은 제목·첫 설명·first-example 코드의 호출을 추출한 것이다. 본문 직접 열람과 의미 판독은 선택 행에 별도 기록하며 자동 읽은 HTML 수를 고유 1차 자료 수에 넣지 않는다.

## 첫 예제 경계

Sphinx Gallery의 `section.sphx-glr-example-title`과 그 실제 DOM id를 찾고 첫 설명용 img/data resource를 고른다. 첫 그림에 앞선 setup/code 및 해당 그림 직후 첫 Python block을 연결한다. 다중 output/code 페이지에서 이후 그림은 별도 표본이 아니다. 경계를 선택 행 원 HTML과 소스에서 직접 검토한다. `base`, `src`, `srcset`, `picture/source`, data URI를 보존한다. 대소문자·확장자·fragment·1x/2x는 정규화하지 않는다.

## 경로와 선택

버전 루트 `3.6.3/`만 제거한다. 절 경로는 `gallery/...html#실제-id`다. `SHA256(UTF-8("AF106|Matplotlib|" + old_section_path))`의 소문자 hex 오름차순, 동률은 경로순으로 정한다. 주 층은 후속 단계에 A(옛 외부 자원 경로 부재), M(외부 자원 잔류·옛 본문 또는 공개 Download Python source 경로 소멸/이동), G(앞 두 층에 들지 않음)의 우선순위로 배타적으로 분류한다. 각 2자리다. 소스 blob의 단순 변경은 M이 아니다.

공개 `_downloads/<hash>/name.py` 경로와 저자 `examples/...py` 경로는 별도다. 해시 주소 소멸이 M 신호를 만들 수 있지만 저자 예제의 삭제·이동을 뜻하지 않는다. 저자 source tag(3.6.3 `c23ccdde...`)와 발행 HTML 문서 revision(`655f616...`)도 별도다. 새판은 102에서 인수한 docs revision을 사용하며 새 코드 내용은 원격 예측 봉인 뒤에만 읽는다.

## 자료 수와 보조 대조

같은 논리 예제의 양판, 같은 payload의 다른 주소/1x2x 동일 바이트, 같은 번들 멤버를 중복 산입하지 않는다. 기존102의 트리/릴리스/발행 자료는 계승이다. 주 결원이 생길 때 사용할 별도 대조는 이전 적격 잔여 목록의 해시순 첫4를 사전 지정하고, 주 표본 중복이면 그 다음 해시순으로 건너뛴다. 이 대조는 본문 자료 하한 확보용이며 주 혼동표에는 들어가지 않는다.

주층에서 못 찾는 방향의 보조는 지정 old/new documented-source revision 사이 실제 Git 이력에서 예제 source 이동/삭제를 가진 commit을 committer UTC, SHA 오름순 최대10개로 정한다. 신규 본문/변경 설명 개봉 전 목록을 봉인한다. 부모 원격 봉인 확인 후만 다음 단계로 진행한다.
