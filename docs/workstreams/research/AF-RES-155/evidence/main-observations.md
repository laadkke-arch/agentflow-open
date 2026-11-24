# ③ 주 실행 개봉

두 GitHub fresh clone을 `9f1c49d76cf75589839cf372d6f32bfe4470ab37`에 각각 detached checkout으로 고정했다. `bash replay/bootstrap.sh TOOL_DIR`(소유 경로 내 replay 기준)과 `python replay/run.py --tools TOOL_DIR --repeat W1|W2` 모두 종료 0. 각각 별도 설치 경로에 Pandoc 3.1.11 Linux x86_64와 lockfile의 npm 의존성을 설치했다. [설치 W1](af155-W1-setup.txt) · [설치 W2](af155-W2-setup.txt). 두 checkout과 두 설치는 같은 호스트에 있다.

[runs.jsonl](../runs.jsonl) 첫 구간은 W1/W2 각각 16행이다. 15개 경로를 실행했고 #15853은 자료 불일치로 각 1행을 미실행으로 남겼다. 실제 하위 프로세스는 반복당 47개(9×2 + 5×5 + 1×4)이며 종료 코드와 stdout/stderr를 보존했다. 두 반복의 47개 단계 출력과 파싱 요약이 일치했다. 각 경로의 실제 인수와 시간, stdin 또는 원파일 SHA-256은 원장에 있다.

- Pandoc #9305 원 명령은 성공 종료했지만 plain에서 둘째 값이 사라졌다. JSON AST에 해당 문자열이 들어 있는 `RawBlock`이 남아 있다. pre 제거 및 span 대체는 두 값과 순서를 같은 27바이트로 쓴다. HTML reader에서는 원 입력 바이트를 그대로 읽어 네이티브 Table/CodeBlock으로 바꾸고 두 값을 격자 표에 쓴다. CRLF→LF만 바꾸면 AST와 plain 양쪽 출력이 원 명령과 같다.
- #9308 원 명령의 `Para`에는 info string과 코드가 한 문단으로 들어간다. CommonMark reader와 중괄호 속성 구성의 plain 32바이트는 같은 반면, `hl_lines` AST 속성은 중괄호 구성에만 남는다.
- #15872 정적 예는 Prettier 3.1.1에서 바깥 fence를 4→3으로 줄인 뒤 CommonMark.js HTML이 같다. 꺾쇠나 이스케이프 모드에 대한 추측 없이 원문 이중 중괄호를 Mustache.js 4.2.0 기본값으로 실행하자 백틱이 `&#x60;`으로 바뀌었다. 양 순서 모두 code block과 다음 문단을 유지했지만 보이는 코드에는 백틱 문자가 들어 있지 않았다. 보고의 원시 fence 확장과 이 구성 실행은 입력/엔진 정보가 같다는 근거가 없다. 선행 예측은 기본 이스케이프에서 뒤집혔으므로 보존했다. 실제 보고에 나타난 비이스케이프 결과를 별도 보정 실험으로 대조할 근거가 생겼다.
- #15853은 두 반복 모두 실행 명령을 구성할 근거가 부족하다. `inputs.jsonl`의 `E4-input`은 Input과 Output/Expected의 다른 기호, 호출, 원문 범위 SHA를 남긴다. 이 예는 기술 실행 실패와 구별되는 입력 비교의 결측이다.

W1 원장 SHA-256 `eeee55f8f6ec4de9df2de421062ae6318ac6f5d03592b3c79f26ecb562655b32`. W2 `44512a6f41fb3df6e2e7759dabb89f7b10a9f04999cd0ef289373c4378f61ba6`. 타임스탬프와 작업공간 식별자는 반복마다 다르다.
