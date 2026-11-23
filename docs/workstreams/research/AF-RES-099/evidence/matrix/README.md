# 여섯 실행과 원 산출물

[실행 원장](../../runs.jsonl)에서 `kind=primary` 6행과 보조 실행을 구별한다. 작업 디렉터리는 행의 `path`, 실제 인자는 `processes`, B의 외부 프로그램은 `child_processes`에 있다. 임시 디렉터리에서 사라진 실제 PDF와 TeX 로그는 B 두 행의 `events/0-diagram.pdf`, `events/0-diagram.log`에 계측기가 사전에 복사했다. 소스의 Lua 바이트는 AF-RES-096에 고정돼 있다. [입력 지문](../../inputs.json)

| 경로 | 저장한 출력 |
| --- | --- |
| A | [A1](A1/) · [A2](A2/) HTML·reader AST·Chromium 화면, TeX/PDF/SVG 호출 없음 |
| B | [B1](B1/) · [B2](B2/) RawBlock AST, 실제 컴파일 PDF, 원 SVG, HTML, HTML에서 디코딩한 SVG, Chromium 화면 |
| C | [C1](C1/) · [C2](C2/) 원 TeX를 컴파일한 PDF의 페이지 SVG, 동일 1100×1450 브라우저 viewport의 PDF 래스터 참조·SVG 화면. PDF 확인용 HTML은 연구자가 만든 viewer |
| C+ | 외부 파일 [1](CPLUS-EXTERNAL-1/)·[2](CPLUS-EXTERNAL-2/), data URL [1](CPLUS-EMBED-1/)·[2](CPLUS-EMBED-2/), HTML만 옮긴 [외부 누락](CPLUS-MISSING-1/) |
| 보조 | [A 콜백](A-OBSERVED/) · [원문에서 그림 제거](B-NOPIC/) · [B의 HTML만 이동](B-ONLY-HTML/) · [문서 전역 색 정의 누락](B-CUSTOM-PREAMBLE/) |

`browser.json`은 별도 오프라인 컨텍스트의 본문·표시된 이미지·공급한 리소스·오류다. 화면은 같은 viewport에서 저장했다. C SVG는 이 버전의 mutool이 `-oout.svg`를 페이지명 `out1.svg`로 출력했다. B의 RawBlock 내용은 질문 최초 TeX에서 파생된 reader 출력이다. [원 TeX 저자 infcs.ltd의 최초판](https://stackoverflow.com/revisions/79393445/1)
