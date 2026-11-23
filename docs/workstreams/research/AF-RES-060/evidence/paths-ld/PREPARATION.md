# 사용자 경로 준비

이 문서는 단계3 봉인 전 준비 시점의 기록이다. 이후 실제 실행·독해는 observations.json과 findings.md에 기록했다. 아래 대기·미실행 표현은 준비 시점 상태이며 현재 작업 완료 상태를 대신하지 않는다.

F1 고정판: `412192e28356bee13e4c11f20511ab5ec590662c`.

`prepare_paths.py`는 취득해 둔 공급자 원문 캐시만 읽는다. 아직 이 스크립트를 실제 공급자 입력에 실행하지 않았고 새 목적지도 열지 않았다. stage3 SHA와 요구×공급자 계획을 받은 뒤 부모가 지정한 공급자에 대해서 실행한다. 조건·질의·순위를 입력으로 읽는 코드는 없다.

## 동작

첫 창은 F1의 기능절이 아니라 README/소개 본문의 첫 실제 제목부터 500 표시단어다. 원게시 URL에 fragment가 있으면 그 정확한 절을 사용한다. 명시 HTML id/name 우선, ASCII Markdown 제목의 생성 anchor를 지원한다. 비ASCII 생성 anchor를 정확히 확인할 수 없으면 더 유리한 절로 바꾸지 않고 미확인을 기록한다.

표시단어 계산과 Markdown/RST 렌더는 고정한 F1 renderer를 읽기 전용으로 가져오되 제목 선택은 별도 구현했다. 정보링크는 그 창에 표시된 본문 링크의 원순서다. 규격·설치·사용·API·예시·내부 fragment를 포함하고, chrome/nav/login/badge/빈 이미지·문서 목적지가 아닌 scheme은 제외한다. GitHub 이슈 목록처럼 저장소 활동 UI로만 가는 링크는 chrome으로 분류하지만 특정 issue/PR 문서 링크를 내용 확인 없이 일괄 제외하지 않는다. 링크가 좋은 답을 담고 있을지 추측하여 순서를 바꾸지 않는다.

각 링크의 원래 href, 절대 URL, 창 안 위치, 포함·제외 이유를 남긴다. 절대 URL 문자열의 정확 중복만 제거하며 query와 fragment를 보존한다. 첫째와 둘째 적격 링크는 P2/P3에 각각 따로 붙이고, P2의 두 번째 문서에서 P3를 찾지 않는다. P1은 첫 창만, P2/P3는 각각 최대 두 문서다. 정보링크 역할이 모호한 행은 destination을 열기 전에 창과 제외 이유를 부모가 검토할 수 있다.

GitHub 상대 링크는 고정 README blob URL을 base로 해소한다. crate HTML은 취득한 final URL을 base로 사용하고 그 값을 노출한다. 이 선택은 원게시 URL을 사용자에게 직링크로 바꾸는 실험이 아니며, 실제 취득할 판·목적지를 재현하기 위한 해소다.

## 실행 예정 명령

아래 `<stage3 SHA>`와 `<고정 공급자 IDs>`는 부모가 고정한 실제 값으로 교체한다.

```sh
python -B docs/workstreams/research/AF-RES-060/evidence/paths-ld/prepare_paths.py \
  --stage3-sha '<stage3 SHA>' \
  --ids '<고정 공급자 IDs>' \
  --output docs/workstreams/research/AF-RES-060/evidence/paths-ld/prepared-plan.json
```

출력 경로는 `evidence/paths-ld/` 아래로 제한한다. 생성되는 창은 준비 캐시이며 실제 요구별 독해·판정을 했다고 표시하지 않는다. 두 번째 목적지는 `not_fetched_or_read`로 남긴다. 그 취득·독해는 다음 승인된 단계의 별도 행동이다. 준비 단계에서 수행한 검사는 Python AST 문법 확인뿐이며 성공했다.

## 유지할 원문

`evidence/features-ld/raw/`의 원문은 같은 응답을 재사용할 때 필요하다. 이 준비 스크립트는 해당 파일과 기능표를 수정하지 않는다. 원문을 원격에 출판할 필요는 없지만 사용자 경로 판정을 마칠 때까지 로컬 캐시는 보존해야 한다.
