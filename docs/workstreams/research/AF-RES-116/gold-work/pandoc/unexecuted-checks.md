# 필요한 최소 실행 확인 — 전부 미실행

이 문서는 후속 재현 계획이다. 다음 Pandoc/TeX 명령을 이 작업에서 실행하지 않았고 새 바이너리·패키지를 설치하지 않았다. 정확한 historical 바이너리 경로와 원 engine 환경을 확인한 후 실행해야 한다. 지금 알려진 자료만으로 원 P3 command를 복원할 수는 없다. 기계 판독형 명령·입력 hash·성공 기준은 `unexecuted-checks.json`에 있다.

아래 working directory는 이 폴더의 `reproduction-inputs/`다. `<...>`를 그대로 실행하는 명령으로 제시하지 않기 위해 shell 변수에 **이미 확보한 정확한 바이너리 경로**를 지정하는 형태로 썼다. 경로 지정은 설치 명령이 아니다.

## P1 / Pandoc 2.19.2

```sh
PANDOC_2192_BIN=/absolute/path/to/pandoc-2.19.2
"$PANDOC_2192_BIN" --version
"$PANDOC_2192_BIN" P1-original.md --self-contained --toc --output=P1-original.html
"$PANDOC_2192_BIN" P1-hierarchy-counter.md --self-contained --toc --output=P1-hierarchy-counter.html
"$PANDOC_2192_BIN" P1-raw-wrapper-candidate.md --self-contained --toc --output=P1-raw-wrapper-candidate.html
```

버전 확인은 2.19.2여야 한다. 원 입력 결과는 TOC와 본문을 구분하여 확인한다. source 분석상 원 TOC에는 A1/A2가 있고 B1/B2가 없을 것으로 예상하지만, 이것은 아직 이 작업의 실행 관측이 아니다. 본문 B1/B2와 한 `Fenced3` wrapper도 함께 확인한다.

`P1-hierarchy-counter.md`는 연구자가 B2만 `###`로 바꾼 입력이다. 첫 제목보다 깊은 하위 제목이 같은 Div 안에 있어도 처리될 수 있다는 반례를 검사한다. 이 변경은 원 제목 계층을 바꾸므로 해결책이나 자연 입력으로 취급하지 않는다.

`P1-raw-wrapper-candidate.md`는 원 `Fenced3`의 여닫는 native fence를 명시적 raw HTML block으로 바꾼 후보다. 같은 계보의 2024 maintainer 제안을 2.19.2 입력에 적용한 것이며 성공 검증은 아니다. 두 peer heading의 TOC 포함, 하나의 emitted group, HTML nesting/ID/속성 보존을 모두 검사해야 한다. native Div AST는 원래 그대로가 아니다. 실제 conditional Lua filter를 포함한 경우에는 같은 filter 순서에서 별도 확인해야 한다.

## P2 / 고정 Pandoc 3.8.3

```sh
PANDOC_383_BIN=/absolute/path/to/pandoc-3.8.3
"$PANDOC_383_BIN" --version
"$PANDOC_383_BIN" --from=markdown+smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
"$PANDOC_383_BIN" --from=markdown+smart --to=native --abbreviations=P2-space-enriched.yaml P2-example.md
"$PANDOC_383_BIN" --from=markdown+smart --to=native --abbreviations=P2-tab-enriched.txt P2-example.md
"$PANDOC_383_BIN" --from=markdown-smart --to=native --abbreviations=P2-bare-keys.txt P2-example.md
```

모든 P2 입력은 원 schematic에서 연구자가 만든 최소 입력이다. 실제 완전한 원 파일이나 약어 목록이 아니다. bare 파일은 `Foo.`와 `HTML`만 한 행씩 갖는다. enriched 파일은 같은 key 뒤 space 또는 tab과 설명을 갖는다. source 분석상 bare 파일+smart만 token 다음의 NBSP 효과를 갖고, enriched 행의 bare key는 인식되지 않을 것으로 예상한다. native 출력의 정확한 `Str`와 `Space`/NBSP를 비교해야 하며 exit code가 0인 것만으로 동등한 인식이라고 세지 않는다.

period 없는 `HTML`도 검사에 넣었으므로 오래된 “마침표 필수” 제한을 현재 고정판에 잘못 옮기지 않는다. smart를 끈 대조에서는 약어 NBSP 효과를 기대하지 않는다. 입력 파일의 before/after hash가 그대로인지 확인하면 설명·주석 보존과 parsing 동작을 분리할 수 있다.

이 작은 집합의 검사로 전체 YAML key의 동등성을 증명하지 않는다. 실제 파일을 받으면 생성기의 unique key 정책, quoting, multiline, 중복 key, token 내 허용 문자에 맞춰 별도로 비교해야 한다.

## P3 / 실제 TeX 환경이 확인된 뒤

```sh
ACTUAL_TEX_ENGINE_BIN=/absolute/path/to/the-confirmed-latex-engine
"$ACTUAL_TEX_ENGINE_BIN" --version
"$ACTUAL_TEX_ENGINE_BIN" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
"$ACTUAL_TEX_ENGINE_BIN" -interaction=nonstopmode -halt-on-error -recorder P3-followup-with-listfiles.tex
```

이는 원 후속 TeX 입력의 component 재현이다. `P3-followup-with-listfiles.tex`에는 package 판을 log에 남기는 `\listfiles`만 덧붙였다. 일반 LaTeX 엔진군에서 쓰는 위 옵션을 전제로 하며, 원 사용자의 정확한 engine이 확인되지 않은 상태에서 임의 현재 pdflatex 실행을 역사 재현이라고 부르지 않는다. table width 경고가 남으면 필요한 횟수까지 반복하여 안정 여부를 확인한다.

원 Markdown의 정확한 Quarto/Pandoc 렌더 명령은 unknown이다. 첨부의 `format` YAML만으로 어떤 command, engine, template이 실제 선택되었는지 확정하지 않는다. 순수 Pandoc으로 `.tex`를 생성하는 진단을 하려면 다음처럼 별도 기록할 수 있다.

```sh
PANDOC_21403_BIN=/absolute/path/to/pandoc-2.14.0.3
"$PANDOC_21403_BIN" --version
"$PANDOC_21403_BIN" --from=markdown --to=latex --standalone P3-original-layoutissue.md --output=P3-pandoc-diagnostic.tex
```

이 명령이 Quarto 전용 `format` 처리를 재현한다고 주장하지 않는다. 원 pipeline을 확인한 뒤 같은 환경에서 다음 네 경우를 비교해야 한다.

1. 앞 문단 때문에 figure가 다음 페이지로 실제 이동하고 원 표가 남은 입력.
2. 앞 문단을 제거하여 figure가 같은 페이지에 들어가는 대조.
3. 표 제거 대조.
4. 표를 다른 figure로 바꾸는 대조.

figure 위치, 표 존재, 각 페이지 body text area와 최하단 text/table 좌표, engine/longtable 판, log diagnostics를 기록한다. 2–4의 정상 흐름은 원 preservation 요구를 충족한 성공으로 바꾸지 않는다.

독립 upstream 최소 입력도 `P3-upstream-158.tex`에 남겼다. 동일하게 기록한 환경에서 원 입력과 첫 figure에 `[htbp]`를 넣은 대조를 비교할 수 있다. 두 번째가 성공하면 실제 `h` 배치로 float를 피했는지 확인해야 한다. 이 upstream test가 통과한 것만으로 exact P3 해결을 확정하지 않는다.
