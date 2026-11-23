# D-M1 반환 카드 — 주표본 밖의 진단 예시

원래 주표본의 M-N1/M-N2/M-S1/M-S2에는 적격 풀을 만들지 못했다. 아래 카드는 `D-M1`의 부분조건 차이를 설명하는 제안이며 자연/보강 적중 또는 실제 사용자의 채택으로 세지 않는다.

| 카드 ID | 반환 형태 | 설계자에게 보낼 한 줄 | 깨지는 조건·예산 |
| --- | --- | --- | --- |
| D-M1-K1 | 원문 한 개 | [remark-stringify Options](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167): 현재11.0.0 계열에서 언어 없는 code도 backtick fence로 내보내는 C1 옵션을 확인할 수 있다. | C2 언어·내용 유지와 요청의 역사판은 이 창만으로 미확인; 원순위4라 A/C3자리에서는 잘리고 B형제 경로는2동작. |
| D-M1-K2 | 보완 절 묶음 | [직렬화 옵션](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167) + [code handler](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/handle/code.js#L20-L72) + [행동 시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L810-L819): 명시한11.0.0/2.0.0 조합의 backtick·lang·value 보존을 D2로 연결한다. | utility 범위가 실제 설치판은 아니며 실행하지 않음; 코드/시험은 동결된 첫 두 href 경로 밖이므로2동작 완결 카드로 주장하지 않음. |
| D-M1-K3 | 구현 둘 | **보류** — [rank4 serializer](https://github.com/remarkjs/remark/tree/main/packages/remark-stringify)와 [rank6 mdast](https://github.com/syntax-tree/mdast)를 두 완결 구현으로 반환할 근거가 없다. | mdast는 자료 구조 명세다. 첫6 안의 독립 공급자 runtime과 두 조건을 함께 지지하는 동일판 근거가 추가돼야 반환 가능. |

## 목적별 반례

| 독자 목적 | 도와주는 정보 | 잘못된 대표 또는 과장 |
| --- | --- | --- |
| 어떤 도구라도 code AST를 Markdown으로 출력 | rank4 serializer의 역할과 현재 옵션, 필요하면 코드·시험 묶음 | parser·CLI·명세의 URL 수를 독립 완결 구현 수로 계산 |
| 이 버전에서 이 방향으로 출력 | 원요청의 정확 패키지 식별·lockfile과 그 판의 옵션/시험 |2023년 이후 default 변경을2022년 환경에 소급 |
| AST 처리기와 serializer를 함께 쓰는 법 | root의 역할 설명과 wrapper가 utility로 전달하는 연결 | parser 입력 예시 또는 데이터 명세만으로 출력의 lang/value 보존을 확인했다고 주장 |

필수조건을 만족하는 부분이 C1뿐이면 카드에 **C1 확인·C2 미확인**을 함께 표시한다. 독립 대안 수0, 직접 도착 증거0, 역사판 미확인은 서로 다른 상태다. 상세 경로와 판정은 `paths.csv`, `evidence.csv`, `diagnostic-metrics.json`을 따른다.
