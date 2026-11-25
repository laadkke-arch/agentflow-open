# AF-RES-264 자체 검토

이 검토는 작성자가 원영수증과 코드·원자료를 다시 대조한 것이다. PDF의 MuPDF 1.25.1과 pypdf 6.21.4 판독은 독립 구현이다. 별도 작업자 검토는 미실행이다. 고정판 재생과 계약/저장소 검사 기록은 마지막 HANDOFF.md의 검증 표에서 찾을 수 있다.

| 질문 | 원근거 및 위치 | 자기 결론을 깨는 사례와 관측 | 남은 미확인과 최소 다음 확인 |
| --- | --- | --- | --- |
| Q1 | REL2232/REL23 asset 첫 행. 두 추출을 태그의 default.latex와 byte compare. `latex-file-list.txt`와 `.fls`, `pdffonts.txt` 비교. [도구 영수증](receipts/environment/tool-setup/packages.json) | 다른 템플릿이나 패키지가 로드되면 원인 판정 보류. 명시적인 빈 data-dir와 내장/태그 해시 일치 둘을 확인했다. class/package 목록 16/16 동일, on의 폰트 파일 선택 12개 추가를 별도 기록했다. | 당시 upstream 별도 서명과 역사 설치는 미확인. 출판 아카이브 서명이 나오면 공식 배포와 대조한다. |
| Q2 | W2232/W23 L148–159 및 L214–224, T2232 L361–372, T23 L362–379. [AST 원출력](receipts/matrix/v23-off-unique-r1/ast.json) · [TeX 원문](receipts/matrix/v23-on-unique-r1/tex-context.txt) | 두 판의 toc off와 2.2.3.2 toc on은 AST가 키를 받아도 제목 override 공석. writer가 메타데이터를 폐기한다는 대안과 충돌한다. 명시/생략 8+8, AST 본문 4개씩, override 2/16이다. | YAML이나 재정의된 template context는 미실행. 적용하려면 그 입력의 AST와 override 위치를 먼저 추출한다. |
| Q3 | [PDF p1 layout](receipts/matrix/v23-on-unique-r1/pages.txt)와 3패스 `.toc`/PDF. ARTICLE L3759–3788, 설치 article.cls L502–508. | 첫 패스의 인쇄 제목은 toc on 8/8, 항목 공석 8/8. 둘째/셋째에는 네 항목. 최종 p1 제목 및 본문·TOC 줄을 문구가 같은 경우에도 분리했다. off 8/8의 제목·항목 부재는 정상이다. | article 이외 및 다른 실제 문서의 페이지 나눔 미실행. 변경할 class의 `tableofcontents`를 확인해 동일 입력으로 교체 실행한다. |
| Q4 | [MuPDF outline/URI와 resolver](receipts/matrix/v23-on-unique-r1/mutool-resolved.json), [pypdf raw /Parent·/A/GoTo/D](receipts/matrix/v23-on-unique-r1/pypdf.json), MU-SHOW L232–261, PDF-PY L1181–1226. | 패스 1의 root 정상 부재 16/16, 패스 3 본문 트리 16/16. 키만 교체한 목적지는 일치하고 toc 토글은 이름/y를 바꾼다. bookmarks=false 사례의 정상 공석과 invalid의 독립 실패 exit 1/1을 대조했다. | 실제 GUI 패널 초기 상태 미실행. 필요 시 같은 원 PDF의 PageMode와 특정 리더의 초기 상태를 직접 대조한다. |
| Q5 | PATCH4853 diff L28–37, T23 L363–365, [양방향·삭제 비교](receipts/comparisons.json). | swap 둘과 조건부만 제거한 통제에서 셋 다 TeX+PDF 성공. 동일 템플릿에서는 두 writer의 TeX 바이트가 같다. 명시적 TOC bookmark 추가로 단일 제목 선택의 일반화를 깨뜨렸고 9.035 pt 이동을 기록했다. | 별도 클래스가 TOC 제목을 자동 등록하는지 미확인. 클래스 매크로 또는 명시적 삽입을 확인한 뒤 page·outline을 다시 읽는다. |
| Q6 | PDFTEX-MAN Ch.2, [원 PDF byte 마스킹](fixtures/compare.py), [24쌍](receipts/comparisons.json). | 반복 8쌍은 원바이트 불일치와 날짜/ID만 바꾼 전체 일치를 함께 확인. A/A는 원바이트 일치, A/B는 마스킹 일치. 같은 기본 제목 명시/키 생략은 TeX 차이와 같은 픽셀을 보였다. bbox 비교는 head 날짜 대신 page 기하를 사용했다. | 다른 엔진의 압축 Info나 ID 생성 규칙에 마스킹 재사용 미실행. 기존 두 literal date와 ID 일치 개수를 먼저 검사한다. |
| Q7 | ECOP L33,41–49, ECNAV L11–68, EPOP L44,68–78, EPNAV L8–32 및 EPUB33 §5.7.1–2, §7.4.2, §7.5. [실제 ElementTree 결과](receipts/epub/) | CC nav는 spine에, Page Blanche nav는 spine 밖. `Sommaire`는 nav 외부 헤더. 첫 판독 raw blob 4/4 불일치에 대해 CRLF만 LF로 바꾸는 검사를 추가했고 4/4 일치 확인. XML 결과는 공개 ZIP에서도 2/2 동일. | 리더 인터페이스·원출판사 제출 경로 미확인. 동일 ZIP의 지정 뷰어 목차 패널과 순차 페이지 이동부터 확인한다. |

## 분모와 경계

- 표 1은 16행×6열, 표 2는 11행×5열, 끝 표는 3행×4열이다. 표 1 링크는 주행렬 고정 증거 커밋을 가리킨다. CSV 16행은 바이너리·템플릿·입력·TeX·AST·PDF·목적지와 각 패스 종료를 연결한다. [RESULT](RESULT.md) · [원행 CSV](matrix.csv)
- 주행렬 16/16회, 48/48패스 종료 0과 두 판독 일치. 정상 공석은 최종 인쇄 TOC 8/16, 최종 outline 0/16, 첫 패스 outline 16/16이다. 제어 10/10 PDF 및 30/30패스 종료 0, 최종 outline 정상 공석 1/10. 잘못된 입력 1/1, 기대한 파서 실패 2/2. 본실험 실패·미실행 각 0이다. 원작성자의 사후 산출물은 미수신이다.
- 저장 영수증 검산은 26건·78패스, 커맨드의 stdout/stderr SHA 1,248개, 독립 PDF 재실행 8쌍, 쌍비교 총 24개, EPUB 2건이다. EPUB XML 및 깨진 입력 통제는 PDF 성공률 분모에서 뺐다. 개별 재생의 상태와 판독은 결과 디렉터리의 case별 파일로 추적된다.
- 35 원장 행 중 접근 성공 30, 실패 5, 성공 제외 5, 산입 work 25·lineage 19다. 요청·수정·릴리스 4/4, writer·템플릿·시험 원파일만 6/6과 매뉴얼 2추가, TeX/PDF/파서 7/5, EPUB 6/5다. 실패 경로도 출처와 완화 경로를 적었다. Adobe ISO 32000-1 전체 PDF는 크기 제한/CONNECT 403으로 미확인이고 원장 하한에서 제외했다. [원장](sources.jsonl)
- GitHub 착수판의 행·의존·허용 경로와 원작업 243 HANDOFF SHA를 일치시켰다. 작업 변경의 목표 경로는 `docs/workstreams/research/AF-RES-264/`다. nested manifest는 개별 검사가 사용하며 저장소 전체 `check-all`의 자동 대상에 추가하지 않았다. [착수 범위](SCOPE.md) · [manifest](session.json)

자체 판단은 **DONE**이다. 두 정확판의 핵심 실험, 템플릿 통제, 두 독립 PDF 엔진 판독, 두 EPUB 원입력 및 비교, 직접 자료 하한을 채웠다. 당시 사용자와 GUI의 미확인 사항은 위 표의 경계에 포함한다.
