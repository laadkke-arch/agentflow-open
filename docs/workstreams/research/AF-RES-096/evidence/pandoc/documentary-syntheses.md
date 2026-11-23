# P3/P4 사전 문서 근거 합성

공개 답·댓글을 읽기 전, 봉인된 원 요구와 각 경로에서 이미 연 자료만으로 작성했다. **다음 코드는 연구자의 합성안이며 실행 성공 기록이 아니다.** 최초 판정은 `pre-review/`에 원바이트로 보존했다. 새로운 파일·검색·본문 시도를 추가하지 않았고 아래 근거 절을 각 경로에서 별도로 재열람했다.

## P3: 기존 R 값 생산 단계를 유지한 raw HTML 표지

R0는 R 코드 청크 안에서 `SIGNATURE`에 HTML 문자열을 대입하고, 문서 뒤의 YAML에 inline R 결과를 넣는다. 예시 값은 고정 문자열이다. 미래의 임의 동적 데이터 보존을 C2로 추가하지 않는다. 기존 생산 경계는 그대로 두고, **그 R 대입 직후** 다음 한 줄을 추가한다.

```r
SIGNATURE <- paste0("`", SIGNATURE, "`{=html}")
```

뒤의 원 YAML 구문과 template의 `$signature$`는 그대로 사용한다.

```yaml
---
title: '`r TITLE`'
signature: '`r SIGNATURE`'
---
```

연결 근거는 두 경로 모두에서 연 [PD-0001](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt) 하나다.

| 단계 | 문서가 지지하는 계약 | 이 입력에 적용하는 추론 |
|---|---|---|
|R 대입→inline R→YAML|이 단계는 새로 만든 연결이 아니라 원 R0가 제공한 값 생산 방식이다.|문자열 안 HTML은 바꾸지 않고 양끝에 Markdown raw 형식 표지만 추가한다. 주어진 문자열에는 backtick이나 YAML 작은따옴표가 없어 원의 single-quoted scalar를 깨지 않는다.|
|YAML 문자열→Pandoc metadata|4904–4906: 문자열 scalar를 Markdown으로 해석한다.|추가한 raw 표지를 인식하므로 HTML 태그를 일반 Markdown inline들로 재구성할 필요가 없다.|
|raw 표지→HTML 원문|5364–5377: 지정 형식의 raw inline; 5263–5274: HTML 출력에서 raw HTML 보존.|표시 대상 `<table>…</table>`를 raw HTML 값으로 전달한다. 의미 없는 새 br를 만들 변환 단계를 피한다.|
|metadata→사용자 template|4951–4953: metadata의 출력 형식 표현을 template variable로 설정한다.|기존 `$signature$`가 raw HTML 표현을 받으며 제목 뒤 의도적으로 둔 br는 수정하지 않는다.|

문서적 완결은 **Pandoc 3.6의 해당 Markdown/raw_attribute 계약과 주어진 입력**에 대한 판정이다. R Markdown이 실제로 쓴 `.md`, 원 2.11.2/3.1.11의 비교 출력, 원 작성자의 성공은 확인하지 않았다. 다른 입력에 literal backtick·작은따옴표·개행이 있으면 delimiter/YAML 인코딩을 다시 정해야 한다. `raw_attribute`를 끈 입력 variant에도 일반화하지 않는다. `-V` 우회안은 R 청크 결과를 옵션에 전달하는 시점이 비어 있어 별도 부분 후보로 유지한다.

## P4: 원 libraries와 전역 설정을 보존한 RawBlock 필터

원 질문은 HTML에 그림이 나오길 요구하며 `diagram.lua`는 실패한 시도다. 그 특정 필터만 써야 한다는 조건은 없다. 두 경로가 공통으로 연 [PD-0012](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md)의 777–874에는 raw TikZ→PDF→SVG→Image 예제가 있다. 원 예제의 최소 preamble에 R0가 제공한 `automata`, `positioning`, `arrows`와 전역 `tikzset`를 그대로 넣은 합성안이 [p4-raw-tikz.lua](p4-raw-tikz.lua)다.

아래는 **미실행 명령**이다. `example.tex`는 R0의 완전한 원 LaTeX 입력이고, 필터 파일은 이 디렉터리에서 복사해 사용한다.

```sh
pandoc --standalone -N --from=latex+raw_tex --to=html5 \
  --lua-filter=p4-raw-tikz.lua --embed-resources \
  example.tex --output=example.html
```

| 단계 | 직접 근거 | 구체적 연결 |
|---|---|---|
|LaTeX 입력→raw TeX|[PD-0001](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt) 3596–3605|명령에서 LaTeX reader의 raw_tex를 명시적으로 켠다.|
|raw tikzpicture→컴파일할 TeX|PD-0012 777–801,841–853|공식 RawBlock 예제의 그림 영역과 정확한 R0 preamble 의존을 합성한다. 다른 본문은 필터가 바꾸지 않는다.|
|TeX→PDF→SVG|PD-0012 803–824,3663–3688|pdflatex와 pdf2svg를 명시적으로 호출하고, 실패는 성공처럼 숨기지 않는다. preamble과 그림을 함께 해시하여 잘못된 이전 그림 재사용을 피한다.|
|SVG→HTML 표시|PD-0012 841–849; PD-0001 1015–1037|생성 SVG를 Image로 반환하고 `--embed-resources`로 HTML에 포함한다.|

필수 도구는 원 공식 예제가 요구하는 `pdflatex`, `pdf2svg`와 TeX의 `standalone`, `xcolor`, `tikz`/원 세 라이브러리다. **이 환경이나 질문자 환경에 설치됐다고 주장하지 않는다.** 코드의 명세상 연결과 실행 성공은 별개다. 실제 `-f latex+raw_tex -t native` AST, 생성 SVG, original labels/arrows 보존을 실행으로 확인하는 일이 다음 최소 점검이다. 별도의 외부 제품 원문을 경로 근거로 반입하지 않았다.

B에서 읽은 DG-0002는 기존 필터가 CodeBlock만 처리한다는 추가 진단을 준다. 이 사실은 A의 판정 근거가 아니다. 최종 완결 후보는 양쪽 모두 같은 두 주 도구 자료(PD-0012/PD-0001)로 지지한다. 따라서 B의 인접 자료 열람은 진단을 늘렸지만 이 최종 완결을 단독으로 만들지 않았다.

## 판정 해석의 교정

처음 P3는 새 -V 전달 방식의 빈 연결 때문에 부분, P4는 공식 예제의 누락 preamble 때문에 부분/원 필터 연결 반박으로 기록했다. 검토에서 두 빈 곳을 **원 입력에 있는 정보와 이미 열린 자료의 기능으로 구체적으로 닫을 수 있는지** 확인했다. 실제 실행이 없다는 이유만으로 문서적 완결을 막지 않도록 공통 기준을 적용했다. 새 명시조건이나 새 외부 근거를 만들지 않았고 사후 공개 답도 보지 않았다. 초기 판정과 별개로 최종 A/B 문서적 판정은 P3 양쪽 완결, P4 양쪽 완결이다. 원 사용자 실행 성공은 모두 미확인이다.
