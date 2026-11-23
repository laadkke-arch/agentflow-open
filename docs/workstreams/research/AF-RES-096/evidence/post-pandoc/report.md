# Pandoc 공개 후속 및 고정판 보조 실행

**사전 판정은 변경하지 않았다.** 공개 후속을 열기 전에 두 경로의 원장과 판정은 원격 `d03ca37daf0c43688c68bc39417d84a9b84803e9`에 봉인되었다. 이 디렉터리의 답·댓글·이미지·추가 매뉴얼 절과 실행은 모두 네 번의 사전 본문 접근 예산 밖에서 얻은 사후 자료다.

## Q6: 공개 후속의 귀속

| 요청 | 최초 답 UTC / 수정 UTC | 현재 채택 | 질문자의 30일 내 후속 | 원 입력·명령·판·출력의 직접 확인 | 봉인 판정과의 관계 |
|---|---|---|---|---|---|
|P1 / 79332660|2025-01-06 13:52:47 / 수정 없음|없음|질문자 self-answer 1건|Strong를 custom-style=test Span으로 바꾸었다는 코드와 성공 주장은 있다. 원 문단 role, 완전 명령·판·생성 DOCX는 없다.|사전 양쪽 반박과 양립한다. 다른 AST 요소를 직접 스타일링하는 우회 성공을 원 paragraph role 보존 성공으로 바꾸지 않는다.|
|P2 / 79369213|답 없음|없음|질문자 댓글 1건|원본·결과를 unzip해 VE name/id 중복을 확인했다고 보고했다. 실제 XML은 공개 본문에 없다.|사전 양쪽 부분과 맞는다. 매뉴얼만으로 관측된 중복을 설명하거나 고칠 수 없다는 반례다.|
|P3 / 79375162|2025-01-23 18:22:50 / 수정 없음|79382172|공개 댓글·본문 수정 없음|답의 옵션과 결과 이미지를 읽었다. 이미지 판은 R4.4.2, rmarkdown2.29, Pandoc3.1.11.1이다.|사전 양쪽 완결은 raw 표지 합성안이었다. 사후 답은 같은 주 도구 매뉴얼의 다른 절에 있는 더 직접적인 옵션이다.|
|P4 / 79393445|2025-01-28 14:19:23 / 14:26:47|없음|공개 댓글·본문 수정 없음|답은 PDF→SVG mutool 명령과 브라우저 SVG 이미지를 제공한다. 실제 PDF 바이트·도구판·통합 HTML은 없다.|외부 그림 렌더링 방향을 지지하지만 봉인된 Pandoc 변환의 실행 성공을 입증하지 않는다.|

현재 채택 표지는 조회 시점의 상태다. **언제 채택되었는지, 질문 개설 후 30일 이내에 채택되었는지는 미확인**이다. 모든 공개 답 3건은 30일 안에 게시되었지만 이것과 채택 시각은 다른 변수다. 네 질문 모두 생성본 이후의 질문자 본문 수정은 조회된 revision에 없었다. 삭제된 답이나 댓글은 이 조회로 복원하지 못한다.

분모는 네 질문이다. 공개 답이 있는 질문 3/4, 현재 채택 1/4, 30일 내 질문자의 별도 행동 2/4, **원 입력·명령·판·출력을 모두 갖춘 질문자 실행 확인 0/4**다. P1의 self-answer는 성공 자술이므로 무시하지 않되 변환 대상이 바뀌었다는 사실을 같이 기록한다. 이 수치는 연구자가 따로 실행한 결과와 합산하지 않는다.

### 직접 읽은 공개 자료가 바꾸는 이해

P1의 [질문자 최초 답](https://stackoverflow.com/revisions/6F659201-6815-46E2-BB6F-5C2C61CC5090/view-source)은 Lua AST 조작으로 사용자가 다른 진입점을 찾았음을 보여 준다. 그러나 Strong 전체를 스타일링하는 코드에는 원 `role=custom`과 특정 paragraph style의 일대일 대응이 없다. 답이 있다는 이유로 원 요청 완결을 추정하면 서로 다른 요구를 비교하게 된다.

P2의 [질문자 댓글](https://stackoverflow.com/questions/79369213#comment139974623_79369213)은 원본과 결과의 XML을 실제로 열었다고 명시한다. 다른 참여자의 ‘아마 reference.docx 문제’라는 추정과 질문자의 중복 관측은 구분했다. 다음 확인은 두 VE 항목의 `w:type`, `w:name`, `w:styleId`를 직접 받는 것이다. 댓글의 설명만으로 특정 Pandoc 버그나 특정 Word 판 문제라고 단정하지 않는다.

P3의 [최초 답](https://stackoverflow.com/revisions/DF73AC92-8281-499B-963C-D995EEE0FB91/view-source)은 `markdown_in_html_blocks`를 끄는 `--from` 형식을 Rmarkdown의 `pandoc_args`로 전달한다. [고정 Pandoc3.6 매뉴얼의 해당 절](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L5282-L5318)을 사후에 별도로 읽어 해석 범위를 확인했다. [답 이미지](https://i.sstatic.net/6HYjjQOB.png)의 판·출력은 **답변자에게 귀속**한다. 원 질문의 Pandoc3.1.11과 이미지의3.1.11.1은 같은 문자열이 아니다. 현재 채택과 함께 보아도 질문자 환경의 재실행 로그가 되지는 않는다.

P4의 [최초 답](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source)과 [수정판](https://stackoverflow.com/revisions/073D223B-CBA7-45F6-AEB4-9A59CA3BC841/view-source)을 구분해서 읽었다. 수정판은 round-trip 비효율과 HTML에 넣을 수 있다는 설명을 추가한다. [이미지](https://i.sstatic.net/JpHiEJI2.png)는 네 상태와 간선뿐 아니라 원 문서의 앞뒤 문구도 포함한 SVG 화면이다. 답의 브라우저 지원 형식 일반화는 기술 근거로 사용하지 않았다. 이 경로는 이미 컴파일한 PDF가 있는 상황에 대한 추가 선택지이며 원 `diagram.lua` 호출의 복구 증거는 아니다.

## 보조 실행: P3의 표 변환

[공식 Pandoc3.6 릴리스](https://github.com/jgm/pandoc/releases/tag/3.6)에서 Linux amd64 asset `211860252`를 내려받았다. 릴리스 게시 시각은 `2024-12-08T05:45:08Z`, 태그의 source SHA는 고정 비교판과 같은 `8a72b8449ddccd84fcdffc1a09ae18c4baaca32a`다. archive 32,764,256bytes와 실제 프로그램에 대해 아래 해시를 기록했다. 릴리스 API의 공식 digest 필드는 비어 있으므로 이 값은 독립 서명 검증이나 재현 빌드 증거가 아닌 현지 측정값이다.

| 대상 | SHA256 |
|---|---|
|공식 tar.gz|`8e3702b195f75412e425df46f8f3f08241b66a2b33abbd9e04eda501bfde860c`|
|실행 바이너리|`7f1ac56064cdc02cdf8bd913f9ea45ba07fbb74419e755328c4571e4470769b2`|

원 R0에서 정확한 `SIGNATURE` 문자열과 `RMtemplate.html`을 추출하고, R/knitr가 끝났다고 가정한 **합성 중간 Markdown**을 만들었다. R은 이 환경에 없다. 따라서 원 Rmd 전체를 렌더링한 것이 아니며 실제 knitr 중간 파일을 포착한 것도 아니다. 버전 출력용 R 코드의 본문 결과는 생략했고 signature와 title metadata의 Pandoc 단계만 검사했다.

| 입력·방식 | 종료값 | 표 안 br | 문서 전체 br | 행 / 셀 | 원 table 바이트 보존 |
|---|---:|---:|---:|---:|---|
|원 문자열, 기본 markdown|0|38|40|4 / 12|아니오|
|봉인 raw HTML 표지 합성안|0|0|2|4 / 12|예|
|사후 답의 확장 비활성화 옵션|0|0|2|4 / 12|예|

세 결과 모두 원 approver/date 문자열을 포함했다. 남은 두 br는 원 template의 제목 뒤에 의도적으로 있던 것이다. raw 표지와 사후 옵션의 출력 HTML은 바이트 단위로 같았으며 SHA256은 `c9cbb331cf3fad29c934b4dcf3010812030f07033a2a7031b6b15e7db13cabca`다. 이것은 봉인된 합성안의 Pandoc 연결을 지지하는 실행 관측이다. 사용자의 과거판 결과, R 평가 시점, 임의의 미래 문자열, 문서 다른 곳의 의도적 Markdown까지 검증한 것은 아니다.

사후 카드에서는 문자열을 바꾸지 않는 공개 답의 옵션을 우선 안내할 수 있다. 다만 그 옵션은 다른 HTML 블록 내부의 의도적인 Markdown 해석에도 영향을 줄 수 있으므로 문서 전체가 같은 요구를 가지는지는 별도 조건이다. 이 카드 개선을 사전 B 단독 적중으로 다시 계산하지 않는다.

## 보조 실행: P4의 호출 경계와 실패

원 R0의 `example.tex`를 그대로 추출해 Pandoc3.6의 `latex+raw_tex` reader로 읽었다. JSON AST 변환은 종료값0이며 RawBlock 두 개 중 하나가 원 TikZ 환경이었다. 따라서 입력이 RawBlock 콜백에 도착한다는 부분은 실제 관측으로 좁혔다.

다음 변환은 봉인 `d03ca37…`의 Lua 파일과 현 파일이 바이트 단위로 같은지 먼저 확인한 뒤 실행했다. 필터 SHA256은 `a63d10a7ee391a518ddf6f646a5714ebb902b00a3d4f608333d1c1f25581176c`이며 **필터를 고치지 않았다**. HTML 변환은 종료값83으로 실패했고 내부 `pdflatex` 종료값은1이었다. 직접 오류는 `pdflatex.fmt`를 찾을 수 없다는 것이다. `pdf2svg`, `standalone.cls`, `xcolor.sty`, TikZ와 원 세 라이브러리 역시 사전 의존성 조회에서 없었다.

이 환경은 `pdflatex --version`을 출력할 수 있지만 실제 TeX 문서를 컴파일할 준비가 된 환경은 아니었다. SVG 생성·HTML 내장·그림의 라벨/화살표 보존은 **미확인**으로 남는다. 시스템 패키지를 설치하거나 Inkscape로 교체하여 봉인 필터의 의미를 바꾸지 않았다. 첫 다음 행동은 필요한 TeX 포맷·패키지와 `pdf2svg`를 이미 갖춘 실행 환경에서 아래 동일 재현 절차를 돌리는 것이다. 그때 원 네 상태·모든 라벨·간선이 포함된 SVG와 HTML 이미지가 관측되어야 이 실행 결손이 해소된다.

## 원격 결과에서 다시 실행하는 방법

실행 입력이 무시된 캐시에만 남지 않도록 `prepare-probes.py`에 공식 릴리스 URL·archive/binary 해시·두 R0 revision GUID·본문 해시를 고정했다. 이 프로그램은 공개 API에서 원문을 다시 받아 해시를 검증한 뒤 `run-probes.py`가 짧은 코드/문자열을 추출한다. 이 재구성도 실제 실행해 두 R0 해시 일치를 확인했다. 원문을 장문 통복제하여 커밋하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-096/evidence/post-pandoc/prepare-probes.py
python -B docs/workstreams/research/AF-RES-096/evidence/post-pandoc/run-probes.py
```

두번째 프로그램은 봉인 필터의 원바이트와 Git commit을 대조한다. 정규 실행 명령·작업 디렉터리·UTC·종료값·stderr·입출력 해시는 `execution.json`에 있다. 외부 의존성은 `dependencies.json`, 공식 바이너리 출처는 `release-3.6.json`/`binary-receipt.json`, 입력 재구성은 `prepare-receipt.json`이다. 프로그램은 자체 패키지 설치를 하지 않으며 임시 TeX 파일 위치도 소유 경로의 캐시로 제한한다.

## 자료와 추론의 구분

- **직접 사실:** API의 현재 표지·답 revision 시각·댓글 본문, 두 답 이미지에 보이는 판과 출력, 공식 asset 메타데이터, 해시, 실제 프로그램 종료값과 출력 계수.
- **연구자 추론:** P1의 후속이 원 요청과 다른 대상을 스타일링한다는 판단, P3 두 수정안이 이 입력에서 같은 기능을 한다는 판단, P4 단독 바이너리 존재만으로 실행 준비를 가정할 수 없다는 해석.
- **설계 제안:** P3의 사후 카드를 확장 옵션 절로 더 짧게 만들기, P2에 style XML을 한 번 묻기, P4의 재현 환경에서 동일 봉인 필터를 다시 실행하기.

`outcomes.json` 네 행에는 최대 두 사후 반환 링크·되물을 한 가지·유지/변경 이유를 따로 두었다. `sources-note.jsonl`의 사후 답·댓글·이미지·반복 매뉴얼·실행 출처는 모두 최초 24자료 하한에서 제외했다. 독립 사용자 사건은 여전히 네 질문이며 이미지와 답 revision을 새 사건으로 늘리지 않는다.
