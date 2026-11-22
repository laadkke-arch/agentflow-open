# S 경로 방법·반례·읽기 경계

## 선정과 순서

SCOPE v1 원격 커밋 2ccbf7ab660d6e16dab637eea40867cbc4f83499 뒤에 GitHub 검색을 처음 실행했다. 정확한 질의는 `repo:sphinx-doc/sphinx is:issue builder in:title,body created:2020-01-01..2025-12-31`, sort=created, order=asc, topn=30이다. 최초 네 요청 7019→7032→7054→7093은 모두 특정 입력과 출력/행동을 명시해 순서대로 채택했다. 정원 이후 26건은 교체 후보로 쓰지 않았다. #7096은 #7095와 본문 내용이 중복되는 노출이었다. 두 건 모두 정원 뒤이며 선정 요구 중복은 아니다. 대체 원장 WeasyPrint를 사용하지 않았다.

GitHub search 응답의 생성시각은 null이었으므로 fetch_issue로 30개 이슈의 실제 created_at을 각각 읽었다. frame-S.csv는 30개 노출순·날짜·판독범위와 선정 이유를 보존한다. 선택한 네 본문은 전부 읽었고, 정원 이후 긴 traceback은 전체 코드 분석을 하지 않았다. 노출한 30개 전부를 독립 직접 원문 수로 세지 않았다.

공급자 열람 전 2026-11-22 18:35:06 UTC에 requirements-S.json을 봉인했다. SHA256은 `2327ef6a3916ba0e1909ceb80be0a56c7f1c9b759cc4ad070f880fcf5766cd69`다. 요구 모두 contract_required이며 이름만 물은 요구는 0/4다. 특정 버그 보고의 성공 주장·작성자의 기대·우리 문서 판독을 구별했다.

## 실제 후보 취득

처음 열린 공급자 색인은 공식 builders 페이지다. /en/2.3 경로는 도구 접근에 실패해 발행자 v2.3.1 태그 문서로 대체했다. /stable은 /master로 이동했다. PyPI는 9.2.0을 2026-10-21 업로드로 표시하고 공식 changelog는 2026-10-20 릴리스, 9.3.0 개발중으로 표시했다. 판 미지정 S2/S3만 규칙에 따라 v9.2.0 문서를 사용했다. S2 원문은 semver가 없어도 cad1f86… 소스 핀을 가진다. 2020 소스핀을 2026 stable과 같은 판이라고 보지 않는다.

S1은 먼저 읽은 v2.3.1 builders 색인에서 gettext 명명 항목을, 다음 configuration 문서에서 gettext가 명칭에 나타나는 첫 다섯 설정을 파일 순으로 취했다. configuration 파일 안 순서는 compact→uuid→location→auto_build→additional_targets다. S2/S3/S4에서는 원 요구에 있는 HTML 명칭이 첫 여섯 명명 class 항목에 나타나므로 html→dirhtml→singlehtml→htmlhelp→qthelp→applehelp로 고정했다. 최신판의 앞부분 공통 builder 요약은 링크 없는 텍스트이고, 실제 클래스 링크/앵커를 가진 명명 항목 순서를 따랐다. 약한 연관 후보를 정확한 이미지 API나 캐시 API로 사후 교체하지 않았다.

원 URL은 발행자 GitHub 태그 파일 URL에 실제 명명 항목의 line anchor를 붙인 직링크다. 서로 다른 외부 링크를 임의로 섞거나 미러를 추가한 풀이 아니다. 파일 위치를 전달하기 위해 생성한 publisher line anchor라는 사실을 pool의 url_construction에 명시했다. 이 방식의 자연성은 공식 목차/항목 순서의 링크 표본에 한정되며 일반 웹 검색 순위를 대표하지 않는다.

**사전 고정의 실제 부족:** SCOPE 단계1은 공식 버전 매뉴얼 목차·builder/extension 색인을 허용했지만, builders를 먼저 읽은 뒤 configuration로 이동한다는 세부 seed 순서와 명명 항목에서 GitHub line anchor를 생성하는 절차는 사전에 명시하지 않았다. S1에서는 configuration를 ‘매뉴얼 목차’ 범위로 해석했고, 실제 최초 GitHub 읽기 인수 순서 builders→configuration를 후보 발견순으로 삼았다. 그러나 나중에 읽은 공식 doc/contents.rst L16–18의 원 목차 순서는 **configuration→builders→extensions**다. 따라서 전체 목차를 한 번 펼쳐 순서대로 취한 표본이라고 주장할 수 없으며, 세부 탐색순서의 완전 사전 고정 조건은 미충족이다. 또한 태그 .rst는 자동 class/confval 참조를 정의하지만 우리가 저장한 #L 직링크 자체가 본문에 적힌 원 href는 아니다. 정확한 표현은 ‘자연 명명 항목을 발견한 뒤 재현 가능한 발행자 직링크로 변환’이다. 원 href 6개를 그대로 뽑은 표본이라고 부르지 않는다. 이 한계는 Stage2 고정 뒤 공개하며 pool 순서나 URL을 고쳐 결과를 바꾸지 않는다. 다음 최소 재조사는 seed URL 전체와 traversal 순서·앵커 생성 허용 여부를 외부 원문 열람 전에 명시한 새 표본이다.

4×6 슬롯은 모두 채워졌다. pool의 frozen_utc 2026-11-22 18:37:44 UTC는 원문 관측 cutoff이며 실제 파일 생성은 18:38:47.406899 UTC다. 두 시각을 구별한 보조 영수증은 receipts-S.json에 있다. pool-S.csv SHA256은 `d9f3b3161cc1e7fc04ff0aff74c218c403223416775a59c7a16d9b3baca1b92e`다. 주 단계1에서 여섯 슬롯이 찼으므로 이후 레지스트리·튜토리얼·구현 코드는 귀속/반례 보조 근거로만 읽었다. 뒤에서 더 좋은 답의 문서를 발견해도 주풀에 삽입하지 않았다.

## 대표 링크가 실제로 여는 범위

같은 파일의 서로 다른 line anchor는 같은 원문 전체를 연다. 추가 클릭0은 대표가 가리키는 파일 전체를 읽을 수 있다는 뜻이다. 앵커 밖 절을 안 보이는 것으로 처리하면 손실을 부풀린다. 따라서 coding의 document_group과 pinned_document_url로 직접 문서 접근을 닫아 계산해야 한다. 예를 들어 S1-2 gettext_compact를 열어도 같은 configuration.rst에 gettext_location 절이 있다. S1-A1의 보완 근거는 builder S1-1과 config 후보 중 아무 하나를 함께 열면 접근 가능하다. S1-1만 열어서는 별도 configuration 원문이 없어 위치 표시 설정 근거가 부족하다.

세 빌더 앵커가 카드에 서로 다른 출력 부품을 보여 주는 것과 그 직링크들이 같은 원문을 반복 여는 것은 별개다. 기능 중복 슬롯과 원문 중복 슬롯을 분리해야 한다. B가 구분을 숨긴다고 해도 같은 열린 문서 안 다른 부품 절이 없어지는 것으로 세지 않는다. 이 관찰은 한 URL이 여러 부품을 설명하는 Q7의 실제 반례다.

## 상류·부품·판·방향

HTMLHelp/QtHelp/AppleHelp는 Sphinx의 같은 도메인·매뉴얼에서 소개된다. 그러나 발행자 PyPI Code 링크는 sphinx-doc/sphinxcontrib-htmlhelp, sphinxcontrib-qthelp, sphinxcontrib-applehelp의 별도 저장소를 가리키고, Sphinx pyproject도 별도 패키지 의존성으로 선언한다. 동일 문서 호스트를 구현 상류로 사용하지 않는다. 실제 당시에 설치한 외부 확장판은 미확인이므로 문서태그와 배포판을 구분한다.

standard HTML, directory HTML, single HTML은 한 저장소 안 다른 부품이고 URI/파일 배치/색인 계약이 다르다. HTMLHelp/QtHelp/AppleHelp도 HTML 출력을 만들지만 추가 형식·도구 조건이 다르다. 이 차이를 고정 원 요구 전체의 완전 양방향 대체 가능으로 확대하지 않았다. relations-S.csv의 양방향 판정은 모두 실제 고정 원 요구를 기준으로 unknown이다. 일부 좁은 HTML 출력 목적에서의 조건부 대체 가능성은 이 자료로 추정할 수 있으나 주 원요구를 그렇게 줄이지 않았다.

## 네 요구에 대해 풀에서 입증된 범위

| 요구 | 풀의 지지 | 풀에서 부족한 핵심 | 완전 적격 경로 |
| --- | --- | --- | --- |
| S1 | gettext POT 생성과 configuration의 위치 정보 출력 flag를 함께 읽으면 기능 수준의 S1-A1 지지 | Windows 상대경로 회귀 해결, 2.3.0/2.3.1 실제 결과 | 0, 조건부 회수 해당 없음 |
| S2 | 여러 HTML 출력 빌더의 존재·출력 차이 | 개별 이미지 자동 링크 해제와 전역 동작 유지; 전역 off는 소비자가 거부 | 0, 조건부 회수 해당 없음 |
| S3 | 같은 열린 builders 원문에 HTML/LaTeX 출력 소개 | doctree-resolved 이후 이미지 등록·복사·URI를 두 빌더에서 맞추는 호출 계약 | 0, 조건부 회수 해당 없음 |
| S4 | HTML 출력 빌더들 및 서로 다른 출력 배치 | sphinx-material 함수값 html_context에서 두 번째 빌드 캐시가 유지된다는 결과 | 0, 조건부 회수 해당 없음 |

한계가 있는 네 요구를 다른 적격 질문으로 교체하지 않았다. 이는 A/B/C 어느 방식의 일반적 무가치를 입증하지 않는다. 이번 고정 발견 절차가 원 요청에 충분한 후보를 공급하지 못했다는 음성 관측이다. 모두 0인 완전 적격 분모를 0%로 표시하지 않는다. 판 완화만으로 빠진 기능/수정 근거가 생성되지는 않으므로 완화판의 완전 적격 경로도 0이다.

## 반대 결과를 찾은 보조 경로

- S2의 실제 per-image 답은 현재 configuration L2208–2232의 no-scaled-link에 있다. 3.0 도입 표시와 v9.2.0 HTML 구현 L961–987의 노드 클래스 검사도 확인했다. 이는 초기 여섯 출력형식 링크가 제대로 된 호출 근거를 놓친 반례다. 주풀을 고치지 않았다.
- S3의 현재 HTML copy_image_files는 _images_dir, LaTeX는 outdir로 복사한다. 동일한 source node/image 목적을 같은 경로로 합치면 안 된다는 반증이다. 다만 늦게 추가한 이미지의 등록·정확한 이벤트 순서까지 완전 입증하지 않았다.
- S4의 v2.3.1 get_stable_hash는 최종 str(obj) 해시를 쓰고 BuildInfo 불일치 시 모든 문서를 outdated로 내보낸다. 문서의 ‘HTML 출력 가능’이 함수값을 가진 테마의 캐시 안정성을 보장하지 않는다.
- S1 국제화 가이드는 상대경로 주석 예시를 보여 주지만 예시를 구버전 Windows 회귀가 해결됐다는 실제 관측으로 쓰지 않았다.

## 출처 수와 검토 경계

sources-S.jsonl 57행 가운데 최소수 산입 19개: 소비자 원 요청4, 공식 공급자 문서6, 구현소스3, 배포/귀속6. 버전만 다른 같은 매뉴얼·HTML 구현은 보수적으로 중복 그룹 하나로 세었다. 실패2, stable 별칭2, 정원후 노출26, 기타 중복/발견색인은 제외했다. 후보 URL은24개 슬롯/18개 고유 URL, 고정 문서3개(둘은 같은 builders 매뉴얼의 다른 판)다. 공식 문서 수를 후보 URL 수로 부풀리지 않았다.

분류는 내부 조사자 한 명의 문서 판독이며 독립 사용자 실험이 아니다. 코드 실행, 사용자 클릭/채택, 실제 빌드 성공, 과거 태그의 운영 설치판은 미확인이다. root는 별도 원문 대조와 구조 검산을 수행할 수 있으나 사람 효용 관측으로 바뀌지는 않는다.
