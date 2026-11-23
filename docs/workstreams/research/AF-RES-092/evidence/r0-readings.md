# R0 독해 · 답 열람 전

## J1 · 78264525

[R0](https://stackoverflow.com/revisions/78264525/1) · `CCF5E1CA-E037-4B3F-BBDE-C157644C8E01` · 2024-04-02T23:45:10Z

lunch/snacks[]/dinner 안 food 객체; is_pizza=true → 모든 food 객체에 extra_cheese=true 추가, 다른 구조/값 유지. 단계: JSON 입력 → jq 변환 → JSON 출력; 별도 생산자/소비자 미지정.

C1: 임의 깊이에 있는 food 객체마다 같은 키/값 추가. C2: 제시된 기대 출력에서 기존 필드와 중첩 구조 유지. 원문에 jq만 호출; JSON 형식은 독립 도구 근거가 아님.

확인 질문: food가 null/배열인 자리도 있습니까? 객체만 / 다른 타입도 있음. 미확인: 실제 jq 사용판, food 비객체 처리.

## J2 · 78265746

[R0](https://stackoverflow.com/revisions/78265746/1) · `CA8CC78E-A0DE-42CD-AAA7-F33598FB7F3B` · 2024-04-03T06:50:50Z

settings.tasks[].notebook_task.base_parameters 일부; JSON이 path 문자열 중간에서 끝남 → project/path 읽기와 갱신; 구체 새 값과 대상 원소는 없음. 단계: 불완전 JSON 조각 → jq → 조회값/수정 JSON; 외부 소비자 미지정.

C1: tasks의 notebook_task.base_parameters.project/path 조회·갱신. C2: 공석(독립된 두 번째 제약 없음). jsonnet/jquery는 태그뿐; Databricks나 Jsonnet 입력으로 추정하지 않음.

확인 질문: 모든 tasks 원소를 바꿉니까, 특정 원소만 바꿉니까? 전체 / 선택. 미확인: 완전 JSON, 새 값, 선택 기준, 사용판.

## J3 · 78304807

[R0](https://stackoverflow.com/revisions/78304807/1) · `D28425CF-C1D0-4AE9-9971-03D5F4750B75` · 2024-04-10T13:31:42Z

{"a":1,"b":2,"c":3}; --arg key b; 잘못된 .($key)와 문자열 경로 → b만 42, a=1,c=3 유지. 단계: JSON+문자열 인수 → jq → JSON; 인수 전달 외 별도 도구 미지정.

C1: 인수 key가 지목한 속성을 갱신. C2: 예시에서 다른 키 값을 유지. 쉘 종류 미지정; jq --arg와 객체 인덱싱 범위.

확인 질문: 키는 최상위 속성 이름입니까, 점으로 구분한 경로입니까? 리터럴 키 / 중첩 경로. 미확인: 실제 jq 사용판, 일반화할 키의 형태.

## P1 · 78273711

[R0](https://stackoverflow.com/revisions/78273711/1) · `9C7FEEF1-C3FF-4A16-A0F1-3341EE8A2AFA` · 2024-04-04T12:03:08Z

R Markdown YAML; xelatex; eisvogel; NotoSans-Regular 경로; 실패 문자는 사각형 표시 → PDF에서 원하는 Noto/이모지·특수문자 렌더링. 단계: R Markdown → Pandoc+Eisvogel → XeLaTeX/fontspec → PDF; HTML 분기 유지.

C1: PDF의 폰트/누락 글리프 문제 해소. C2: PDF와 HTML 출력을 헤더에 함께 유지. 명명된 rmarkdown/xelatex/fontspec/eisvogel만; 실제 글리프/폰트 설치는 추정 금지.

확인 질문: 실패 문자의 실제 Unicode 값이 해당 NotoSans 파일에 있습니까? 있음 / 없음. 미확인: 실제 문자 코드, 글꼴 커버리지/설치판, 완전 Rmd, 각 프로그램 당시판.

## P2 · 78311072

[R0](https://stackoverflow.com/revisions/78311072/1) · `0A5A0ED2-F43B-4AE1-8C8D-3E4E47D61CDF` · 2024-04-11T14:27:37Z

Quarto article PDF; 헤더가 빈 Markdown 2열 표와 Alice/Bob/Charles 행 → 표 위·아래 가로선 제거. 단계: Quarto Markdown → Pandoc LaTeX writer → LaTeX PDF.

C1: PDF 표의 top/bottom 수평선 제거. C2: 공석(독립된 두 번째 제약 없음). LaTeX 코드/YAML 허용은 대안 경로, 독립 제약 아님; Quarto와 직접 LaTeX 소비 단계만.

확인 질문: 모든 표에서 선을 지울까요, 이 표에서만 지울까요? 전역 / 한 표. 미확인: 실제 Quarto/Pandoc/TeX 사용판; R0 이미지 시각내용.

## P3 · 78358965

[R0](https://stackoverflow.com/revisions/78358965/1) · `6222ECAD-AF89-4FAF-884D-379F276D826D` · 2024-04-20T16:33:16Z

Better BibTeX 서지; footnote의 @achelis1897 인용, locator 있는/없는 두 형태; 1 또는 공백 출력 → 페이지 없는 전체 저작 인용과 bibliography를 정상 보존. 단계: Better BibTeX 서지+Markdown+CSL → Pandoc citeproc → 문서/서지 출력.

C1: 페이지번호 없는 인용도 정상 표시. C2: 동일 저작의 다른 인용과 bibliography도 정상 보존. CSL은 citeproc가 읽는 스타일 입력; 독립 외부 실행기로 단정하지 않음.

확인 질문: 같은 bib/Markdown에서 기본 CSL로 바꾸면 문제가 없어집니까? 없어짐 / 지속. 미확인: 실제 bib 엔트리, CSL 파일, 전체 명령, writer, 당시판.

