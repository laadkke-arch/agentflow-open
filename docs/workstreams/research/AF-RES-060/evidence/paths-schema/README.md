# JSON Schema 이용자 경로 준비 코드

이 묶음은 단계2 `412192e28356bee13e4c11f20511ab5ec590662c` 이후에 준비했다. 아직 실제 계획을 넣어 실행하지 않았고, 새 외부 목적지·신규 요구 본문·C1/C2 판정을 읽지 않았다. 기능표를 수정하지 않는다.

## 입력과 실행 시점

실제 단계3 SHA와 그 판에서 고정한 요구×공급자 쌍을 받은 뒤에만 실행한다. JSON 입력은 다음 형식의 배열이다. 예시 ID는 설명용이며 실제 계획이 아니다.

```json
[
  {"requirement_id": "ACTUAL_REQUIREMENT_ID", "catalog_id": "SC-001"}
]
```

```sh
python -B docs/workstreams/research/AF-RES-060/evidence/paths-schema/prepare_paths.py \
  --stage3-sha ACTUAL_STAGE3_COMMIT_SHA \
  --plan docs/workstreams/research/AF-RES-060/evidence/ACTUAL_CASE_PROVIDER_PLAN.json
```

실제 SHA인지의 원격 검증은 통합 연구자의 단계3 영수증에서 수행한다. 이 스크립트는 네트워크 접근을 하지 않으므로 SHA 형식만 검사하며, 원격 검증을 했다고 표시하지 않는다. 출력은 이 경로 아래 새 디렉터리에만 쓰며 기존 결과를 덮어쓰지 않는다.

## 첫 창 규칙

- SC001–031은 단계2의 `_raw/` 캐시만 읽는다. 저장된 응답 SHA256과 Git blob을 먼저 맞춘다. SC032는 캐시도 읽지 않고 `inherit_AF_RES_056_only`로 표시한다. 다른 공급자는 캐시 범위 밖으로 남기고 새 원문을 취득하지 않는다.
- F1의 첫 기능 절과 달리, 본문의 **첫 제목부터 500 표시단어**를 쓴다. 제목이 없으면 문서 시작이다. 원대표 URL에 fragment가 있으면 그 앵커의 절을 사용한다. 앵커가 해소되지 않으면 다른 절로 대체하지 않고 막힘을 기록한다.
- 고정 편집 renderer의 Markdown/코드/RST/AsciiDoc 표시 텍스트 규칙을 재사용한다. HTML은 첫 main/article, 없으면 body이며 semantic nav/footer/script/style·명시된 site chrome을 제외한다. 배지·image-only 링크는 정보 링크가 아니다.
- 렌더러가 제목 ID를 내지 않을 때 GitHub 방식의 slug를 생성하되, `derived_heading_id_match`와 원문에 실제 있는 ID를 구분한다. 이 파생 앵커에 의존하게 되면 실제 경로 검토에서 원래 호스트의 앵커와 맞는지 확인해야 한다.
- 응답 해시 → Git blob/고정판 → 선택 컨테이너 해시 → 표시창 해시를 연결한다. 새 창 파일은 생성했을 뿐 아직 직접 읽지 않은 상태로 표시한다.

## 첫째·둘째 정보 링크

표시창 안에 실제 등장한 순서를 유지한다. 규격·설치·사용·API·예시·내부 fragment는 허용하고, chrome/nav/login/badge/emptyimage와 라이선스·기여 같은 유지보수 문서는 제외한다. 저자가 README에 쓴 내부 목차 fragment는 정보 링크로 취급하며 사이트의 HTML nav chrome과 구분한다.

상대 링크는 **같은 고정 README의 문서 URL**을 기준으로 해소한다. 원대표 URL은 별도 칸에 보존하고 변경하지 않는다. 다른 공급자나 외부 링크를 임의 고정판으로 바꾸지 않는다. 정확히 같은 해소 URL만 중복 제거하며 query/fragment를 지우지 않는다.

각 링크의 label·원 href·해소 URL·문서순서·창의 줄·주변 저자 문맥·포함/제외 사유를 모두 저장한다. 기계적으로 목적을 판별할 수 없는 링크가 첫 두 정보 링크 선택에 영향을 주면 `needs_link_classification`으로 멈춘다. 뒤의 좋은 링크를 자동으로 끌어오지 않는다.

이때 연구자는 **같은 캐시의 첫 창만** 읽고 다음과 같은 분류 파일을 만들 수 있다. 요구 결과나 외부 목적지의 유용성을 이유로 사용할 수 없다. 분류 파일의 해시도 출력에 남긴다.

```json
{
  "SC-001": {
    "EXACT_RESOLVED_URL": {
      "decision": "include",
      "reason": "같은 표시창의 앞 문장에서 API 문서라고 직접 설명함"
    }
  }
}
```

그다음 `--link-overrides 분류파일 --output 새로운출력디렉터리`로 재현한다. 정확 URL 중복 제외는 분류 파일로 해제할 수 없다. 이 단계는 링크의 문서 목적 분류이며 C1/C2 지원 판정이 아니다.

## 출력과 한계

`prepared-paths.json`은 공급자별 첫 창과 P2/P3의 최초 두 링크를 담는다. 동일 공급자의 창은 요구·질의·목록 조합 사이에 재사용하며, 그 이유로 문서를 새로 읽은 횟수를 불리지 않는다. 이 코드는 두 번째 목적지를 열지 않고 단독으로 이용자 경로 완결 여부를 말하지 않는다.

HTML은 고정 응답의 정적 텍스트를 처리한다. 명시된 hidden/aria-hidden 및 semantic chrome은 제외하지만 외부 CSS·JavaScript를 실행하여 화면을 재구성하지 않는다. 해당 표시 차이가 창 경계에 영향을 주는지는 실제 경로 검토에서 별도로 표시해야 한다.

준비 시에는 코드의 AST 문법만 검사했다. 실제 캐시를 넣은 실행·표시창 검토·링크 분류는 단계3 고정 뒤 별도 요청을 기다린다.
