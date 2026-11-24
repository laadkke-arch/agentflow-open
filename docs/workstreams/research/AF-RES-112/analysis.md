## 판정과 사용 범위

**AF-RES-112는 PARTIAL이다.** 고정 모집틀에서 자연 요청은 Godot 3건을 확보했고 LilyPond 3자리는 비었다. 주 수신은 독립 새 AI 문맥 6개에서 18단계를 실제 수행했다. 예정 12꾸러미·36단계 중 나머지 6꾸러미·18단계는 미모집으로 미실행이며, 조기 종료는 없다. 원문을 직접 읽은 고유 1차 저작 총계는 73개지만, 필수층 배당은 요청3/6·문서/원례8/8·회귀/실패6/6·타분야4/4로 **21/24**이다. 다른 층의 초과분을 요청층 부족에 더하지 않는다. [자료 대사](audit-sources/AUDIT.md), [모집 원장](frame.csv), [관측 수](evidence/observation-counts.json).

관측한 세 쌍에서 A와 B는 같은 순서로 같은 본문을 읽었고 최종 라벨도 같았다. 엄격한 ‘원 목적의 필수조건을 같은 판·설정의 실제 노출 근거로 모두 지지’ 기준에서는 A만0·B만0·양쪽0·어느 쪽도3이다. 이는 **조건 판정 가능한 세 사건의 기술 통계**다. G1/G3의 조건부 라벨은 원 예제가 추가 검증용 골격이 될 수 있다는 제한된 판단이며, load/preload 결과 또는 재시작 복원을 확인했다는 뜻이 아니다. G2는 명시적으로 보류했다. 최종 라벨의 gold 일치 4/6과 충분한 근거 성공 0/6을 분리한다. 역사판 수치 정확도는 판정 가능 분모가 0이므로 **null**이다. [독립 평가](adjudication/REVIEW.md), [조건별 근거 연결](adjudication/assessments.json).

따라서 이번 결과로 140자 안내가 일반적으로 유효하거나 무효라고 결론내리지 않는다. 좁은 표본, 충분히 자세한 공통 요청, ZIP/저장소 뷰어, 단계별 1500자 제한과 반복 없는 단일 수신의 결합에서 **추가 안내에 따른 주요 경로·근거·판정 변화가 관측되지 않았다**고만 말할 수 있다. 양성 발견 수는 완료 조건이 아니지만 모집과 핵심 분야 비교의 결손은 완료 판정을 막는다.

## Q1. 전문을 읽어야 구별되는 일과 모집의 한계

단순히 “이 링크에 해당 기능이 있는가”보다, **무엇을 같게 두고 무엇만 바꾸어야 같은 목적의 대조가 되는가**가 핵심이었다. G1에서는 새 Path2D 노드와 새 Curve2D 자원이 같지 않다. G2에서는 같은 Number 타입을 쓴다는 사실과 같은 UID/경로로 식별된다는 사실이 다르다. G3에서는 씬을 다시 연다는 호출과 자원을 새로 만드는 동작이 같다고 보장되지 않는다. 이러한 구별은 원 코드·공식 문서·판별 입력을 함께 읽어 조건부 기준으로 만들 수 있었다. 다만 “전문을 읽은 사람은 역사판 실행값까지 풀 수 있다”는 강한 전제는 충족하지 못했다. 원 작성자의 보고와 현재 설치판 관측을 독립된 역사판 확인으로 치환하지 않았다. [gold.csv](gold.csv), [Godot3.4 Resources의 내장 자원·씬·해제 절](https://docs.godotengine.org/en/3.4/tutorials/scripting/resources.html).

모집 저장소·질의·기간·정렬·중복 제거·적격 기준은 원격 `c8fcd064130259914c782a1f277bddd105711fdd`에서 먼저 고정했다. Godot는 두 저장소의 네 검색 합집합에서 생성시각/숫자 ID순 첫40 고유 원사건을 검토했다. 직접 읽은 이슈 글은41개이며, 동일 작성자의 앞선 댓글을 재게시한 문서 이슈1개를 제외했다. 첫 적격 사건은 순번4·8·9의 #56680·#57026·#57268이다. 세 사건의 원 링크는 문서 절 대신 공개 재현 저장소/ZIP이었다. 적격 정의에 원 예제를 포함했으므로 결과를 본 뒤 문서 링크로 교체하지 않았다. 원 fragment는 모두 없었고 A/B에 같은 주소를 보존했다. [Godot 모집틀·배제 이유](recruitment/godot/frame.csv), [전체 판독 기록](recruitment/godot/full-records.json), [검색 영수증](recruitment/godot/search-receipts.json).

LilyPond의 고정 GitHub 질의는 0건이었다. 공식 사용자 목록의 2022-01 date/thread index와 mbox를 가용 경로로 확보하지 못해, 시간순 첫40의 분모가 unknown이다. 이것은 적격 문의가 없다는 증거가 아니다. 공식 도메인 검색의 개별 히트, 기간 밖 2018년 문의, 후속 답장은 진단·보조층에만 두었다. 원 정규식의 단어 경계 이스케이프 오류는 별도 정정했으며 원 봉인 파일을 소급 수정하지 않았다. [LilyPond 결손](recruitment/lilypond/README.md), [프로토콜 정정](protocol-amendment.json).

공통 요청에는 원 목적과 보존 조건을 정리하고 구별용 정상/경계 입력을 덧붙였다. 특히 G2의 모든 값이 같은 정상 대조는 연구자 구성 입력이다. **자연 공개 요청3개와 합성 입력을 결합한 관측**이며, 합성 입력 개수를 자연 사건 수로 늘리지 않는다. 정상·경계 입력의 출처와 연구 구성 여부는 `frame.csv`의 `input_origin`, 입력 봉인은 `inputs-seal.json`에 있다.

## Q2. 제작자가 준 것, 알고 있던 것, 봉인의 실제 순서

제작자는 원 요청·목적·버전·보존 조건과 원 저자가 건넨 첫 링크만 받았다. B는 찾을 대상, 다음 확인, 유지할 조건을 86·74·73 Unicode 문자로 적었으며 답·검증 완료 상태·새 URL·후속 위치를 넣지 않았다. 같은 쌍의 공통 요청과 URL은 바이트 단위로 같다. B 추가 비용은 합233자·503 UTF-8 바이트이다. 각 원 URL에는 fragment가 없었으므로 유지할 fragment도 없었다. 무엇을 찾아야 할지 부족했던 LilyPond 자리는 한 줄을 만들어내지 않았다. [꾸러미](packets.jsonl), [제작 입력 봉인](inputs-seal.json).

별도 gold 문맥은 B와 수신 답을 보지 않고 전체 원문·공식 문서·원 예제를 읽었다. root는 gold 파일의 해시·행 수를 프로그램으로 다뤘으며 주 수신을 원격 봉인하기 전 내용은 열지 않았다. 패킷 원격 봉인 `d6966cff…`와 gold 원격 봉인 `a3179524…`는 첫 수신보다 앞선다. 주 수신 봉인은 `dd3c615d…`; 그 뒤 전체 기준을 열고 평가했다. 본문 좌표·판정 내용은 후속 메타데이터 정리에도 변하지 않았다. [문맥/도구 해시](evidence/reader-contexts.json), [원 수신 봉인](evidence/reader-seal.json), [노출 불변 대사](evidence/exposure-invariance.json).

**그러나 절차가 완벽히 분리되지는 않았다.** 모집의 전체 규칙은 먼저 봉인했지만, 개별 사건 입력이 로컬에서 결정된 후 gold 독해를 시작했고 그 개별 입력의 원격 봉인은 더 늦었다. 또한 gold의 `read_start_utc=01:52:00Z`는 당시 계측값이 아니라 사후 분 단위 근사치다. 공통 종료 표기도 일부 후속 읽기의 상한이 아니다. 정규화 원장에서는 이 24행의 개별 열람 시각을 null로 하고 원 표기와 정정을 보존했다. 이 기록으로 정밀한 최초 판독 순서를 증명하지 않는다. 제작자의 능동 작업 시작/종료도 계측하지 않아 `created_at`을 제작 시간으로 환산하지 않는다. [gold 방법](gold-work/gold-method.md), [시각 정정](gold-work/clarifications.md), [자료 감사의 시각 정책](audit-sources/AUDIT.md).

## Q3. 독자가 실제로 선택한 경로

각 A/B는 과거 대화를 물려받지 않는 `fork_turns=none` 새 AI 문맥으로 배정했다. G1 A/B, G2 B/A, G3 A/B 순서를 적용했고, 한국어 요청과 같은 제한 도구를 사용했다. 설정 모델은 상속된 GPT-6 Astra Pro이며 provider의 정확한 실행판·seed는 노출되지 않았다. 사람이 읽은 시험이나 일반 웹 Pro UI 세션 전환 시험으로 부르지 않는다. 공유 디스크에 접근 권한 차단을 걸지는 않았으므로 가림은 허용 파일·도구와 실제 기록에 의한 절차적 가림이다. 평가자는 방법명 배정표를 보지 않았지만 시작 이벤트의 hint 유무로 방식을 추측할 수 있었다. [문맥 근거](evidence/reader-contexts.json), [평가 가림 한계](adjudication/REVIEW.md).

독자는 `reader_runtime.js`를 통해 실제로 다음 개봉을 선택했다. GitHub 저장소는 contents API로 만든 목록과 파일 본문을, ZIP은 실제 다운로드의 목록과 선택한 UTF-8 member를 보여 주었다. 전체 응답은 전송 프로그램 안에 두고 최대1500자씩만 문맥에 출력했다. 원문이 작다고 다음 파일을 자동으로 채우지 않았다. 외부 검색, 보이지 않은 링크 추측, 다른 꾸러미·gold 접근은 허용하지 않았다. 내부 이동·다음 구간·이미 읽은 구간의 재노출·실패도 개봉1회로 정했고, 자동 리다이렉트는 같은 개봉 안에 hop을 남겼다. 이전 단계에서 실제 본 링크는 다시 목록을 노출하지 않고 선택할 수 있게 했다. [프로토콜](SCOPE.md), [도구](reader_runtime.js), [ZIP 전송](read_archive.py).

세 쌍의 실제 경로는 다음과 같다. 모든 시작 주소에 fragment가 없었으며, 다른 판으로의 이동이나 실패 개봉은 관측되지 않았다. GitHub의 source/API 뷰를 실제 브라우저의 스크롤·링크 DOM과 동등한 인터페이스라고 주장하지 않는다. G1의 원문주소·API 요청·파일 blob은 확인됐으나 HTTP 최종 도착 주소가 별도로 노출되지는 않았다. 원 helper의 `arrival_confirmed=true`는 connector 표시 주소의 확인이므로, HTTP 리다이렉트 확인으로 읽지 않도록 파생 궤적과 표2에 한정했다. ZIP의 최종 HTTP 주소는 urllib 응답에서 실제 관측했다. [파생 원장 설명](evidence/ledger-derivation.json).

| 사건 | A/B 공통 경로 | 각 방식의 총 본문 | 도달하지 못한 핵심 |
| --- | --- | ---: | --- |
| G1 | 저장소 목록 → Scene.gd → Path2D.tscn | 2569자 / 2629B | Path2D.gd·LocalPath2D.tscn·자원 수명 문서·동일판 실행 |
| G2 | ZIP 목록 첫 구간 → 다음 구간 → filesystem_cache7 | 3512자 / 3684B | 원 Number/Sum 스크립트와 .tres 배열·저장값 |
| G3 | ZIP 목록 → main.gd → main.tscn | 1168자 / 1192B | A_Thing.gd·project.godot·원판 재시작 관측 |

주 수신 전체는18개봉·14498자·15010B이다. 같은 수신 안의 동일 위치 재노출은0자이나, A와 B 사이에는7249자가 동일하다. 이는 두 독자가 같은 자료를 선택한 관측이며 한 문맥이 상대 답을 읽었다는 증거가 아니다. 도구 호출과 생각 시간까지 합친 wall time은 `pairs.csv`에 남겼지만 모델 계산량·능동 노동 시간·사람의 절약 시간으로 사용하지 않는다.

## Q4. 한 번 더 읽으면 무엇이 달라졌는가

첫 개봉은 여섯 문맥 모두 목록뿐이라 보류였다. 두 번째 개봉에서 G1과 G3의 네 문맥은 실행 흐름의 일부를 읽고 제한적 조건부로 바뀌었다. G2 두 문맥은 목록 다음 부분을 읽고도 보류를 유지했다. 세 번째에는 G1/G3가 저장된 초기 상태를, G2가 캐시의 분류와 반복 숫자를 추가로 읽었다. 두 번째에서 세 번째로 바뀐 최종 등급은 없지만, **정보가 늘지 않았다는 뜻은 아니다**. 정확한 부분 복원은 전체18단계 중10단계, 전체 필수조건을 지지한 단계는0이다. [단계별 답](answers.csv), [18단계 독립 판정](adjudication/assessments.json).

G1에서는 양쪽 생성 분기가 모두 `preload`라는 점을 읽었다. 실제 `load` 대조가 없음을 표시했고, 저장된 빈 곡선으로 재생성 뒤 점 수를 확정하지 않았다. 캐시와 잔존 참조의 설명은 문서로 확인한 사실이 아니라 사전 지식/가설로 남았다. G2에서는 캐시의 같은 숫자 필드를 읽었지만 그 필드가 UID라는 의미, 현재 파일의 실제 값, 합계는 확정하지 않았다. 7 또는 동일값일 때4v라는 산술 기대는 실행 관측으로 세지 않았다. G3에서는 변경 후 출력이 g1/g2/g2여서 g3 관측이 빠진다는 사실을 읽었고, 실제 setter와 재시작 결과는 남겨 두었다. gold의 축약 `dict[0]`, `strr=1`과 달리 노출 원문은 문자열 키/값 `{"0":1.0}`, `"1"`이다. 독자의 정확한 표기를 오류로 세지 않았다. [검토 상세](adjudication/REVIEW.md).

최종6개 중 위험한 확정은0, 명시적 정당 보류는2, 중요한 미확인을 남긴 제한적 조건부는4였다. 모델의 기존 지식만으로 역사값을 자신 있게 채택한 사례는 관측되지 않았다. 다만 기존 지식의 영향을 완전히 제거한 실험도 아니다. 잘못된 판으로 이동한 실제 수신은0이며, 후속 Godot4 예제를 원3의 답으로 대체할 위험은 별도 gold 반례층에서 확인했다. 가정상 위험과 수신자가 실제로 범한 오류를 합치지 않는다.

## Q5. 최초 해석을 바꾸는 반례와 다른 분야

**G1의 “load면 초기화, preload면 공유”라는 단순 규칙은 유지할 수 없다.** 현재 설치된 Godot4.7.2의 구성 대조에서 `load_released / preload_shared / preload_local / load_held`의 새 인스턴스 점 수는0/1/0/1이었다. 참조 보유와 local 설정이 결과를 뒤집는다. 이는 연구자가 만든 현재판 대조4개이며 원3.4.2 프로젝트의 독립 재현4회가 아니다. 원 사용 목적이 공유 수정이라면 무조건 독립 복제하는 처방도 목적을 바꾼다. [실행 입력·명령](gold-work/run_gold_checks.py), [현재판 영수증](gold-work/run-controlled-current-engine.json), [원 요청](https://github.com/godotengine/godot/issues/56680).

**G2에서는 정상 입력이 결함을 숨길 수 있었다.** 같은 Number/Sum 구조로 모든 저장값을1로 만들면 현재판 합은4였다. 원 ZIP의 경계 입력은 현재판에서8을 출력하고 assertion이 실패했다. UID 속성을 제거하고 경로로 구별한 대조는7이었다. 원 이슈의 보고값4와 현재 실행값8은 다르며 어느 쪽도 다른 판의 정답으로 대체하지 않는다. 원 실행의 OS 종료값이0이어도 stderr의 assertion 실패가 있으므로 ‘통과’가 아니다. 같은 타입이라는 이유로 값을 합친다고 일반화하거나 모든 참조를 Make Unique로 바꾸는 해법은 의도한 원1의 두 번 참조까지 훼손할 수 있다. [원 실행 영수증](gold-work/run-current-engine.json), [대조 영수증](gold-work/run-controlled-current-engine.json), [정정/재확인](gold-work/clarifications.md), [별도 UID 실패보고 #54774](https://github.com/godotengine/godot/issues/54774).

**G3에서는 나중에 연결된 예제의 판·설정이 다르다.** 원 링크는 Godot3 ZIP이며 local flag가 명시되지 않았다. 나중 Godot4 포트에는 이미 `resource_local_to_scene=true`가 들어 있었다. 설치4.7.2로 그 포트를 실행한 관측은 최초1→변경0→재시작1; 그 flag만false로 바꾼 보조 관측은 최초1→변경0→재시작0이었다. 배열·사전·문자열을 모두 관측했다. Godot3.4.2의 고정 engine 소스에서는 새 씬 인스턴스 생성과 이전 씬의 지연 해제 순서를 확인했으나, 역사판 원 ZIP은 실행하지 못했다. 배열·사전 속 자원 복제가 별도로 실패한 #71243도 읽어 local flag 하나로 모든 중첩 구조가 해결된다고 단정하지 않았다. [scene_tree.cpp L1254–1298](https://github.com/godotengine/godot/blob/45eaa2daf1e3d2571a9f31a3421911262ec82f51/scene/main/scene_tree.cpp#L1254-L1298), [실패보고 #71243](https://github.com/godotengine/godot/issues/71243), [원·포트 해시](gold-work/original-artifact-receipts.json).

별도 Godot 실패층에서는 공유 CSGMesh라도 생성 비용이 작다고 보장되지 않는 보고, 공유 OccluderShape의 인스턴스 동작 문제, 공유/고유 StyleBox를 섞어 편집할 때의 충돌을 비교했다. 보고자의 원 증상·절차를 읽은 것이며 이번에 그 세 실패를 실행 재현한 것은 아니다. 특히 StyleBox의 긴 backtrace 중간은 전부 읽지 않았다고 원장에 남겼다. [#57714](https://github.com/godotengine/godot/issues/57714), [#58003](https://github.com/godotengine/godot/issues/58003), [#61053](https://github.com/godotengine/godot/issues/61053), `sources.jsonl`의 GREC 해당 행.

LilyPond 보조 자료는 공통 변수를 수정하는 일과 한 파트의 표현만 바꾸는 일을 구분한다. Learning Manual의 `hornNotes`/include 예는 공통 원본을 총보와 파트에 쓰되 파트에 별도 transpose를 적용한다. Notation Reference의 tags는 공통 악보 안에서 파트용/총보용 짧은 구간을 선택하는 장치이며 untagged 음악은 남긴다. 태그는 음악식에 적용되므로 book/score 블록을 임의로 거르는 일반 필터가 아니다. Extending 문서는 음악 변수를 backslash로 참조할 때 복사하는 것과 Scheme 직접 참조의 제자리 변경 위험을 구별한다. Godot의 공유 Resource 직관을 LilyPond의 음악 변수에 그대로 옮기면 이 차이를 놓친다. [Learning §4.4.5](https://lilypond.org/doc/v2.24/Documentation/learning/scores-and-parts), [Notation §3.4.2](https://lilypond.org/doc/v2.24/Documentation/notation/different-editions-from-one-source), [Extending §1.2.2](https://lilypond.org/doc/v2.24/Documentation/extending/lilypond-variables).

원 회귀 입력 `tag-filter.ly`는 하나의 common에서 전체/파트/총보를 나누고, `tag-group.ly`는 악기 선택과 다른 태그 그룹의 관계를 비교한다. `part-combine-relative.ly`는 상대음 해석 위치를 구별하며, `part-combine-global.ly`는 뒤의 tie 유무가 앞 음의 성부 합침 판단까지 바꿀 수 있음을 다룬다. 공식 기대 설명과 입력을 읽었지만 이번 세션에서 조판하지 않았으므로 통과한 새 시험으로 세지 않는다. [tag-filter 원문](https://lilypond.org/doc/v2.24/input/regression/f5/lily-a8bde065.ly), [tag-group 원문](https://lilypond.org/doc/v2.24/input/regression/42/lily-3680e428.ly), [relative 원문](https://lilypond.org/doc/v2.24/input/regression/eb/lily-991936d1.ly), [global 원문](https://lilypond.org/doc/v2.24/input/regression/30/lily-7e7e73c9.ly), [수신·해시 영수증](recruitment/lilypond/regression-receipts.json).

타 분야 두 곳도 주 성과에 더하지 않고 같은 URL이 다른 질문을 받는 실제 자료로 읽었다.

| 분야 | 원 규격과 실제 예 | 질문에 따라 달라지는 단위·예외 | 확인의 한계 |
| --- | --- | --- | --- |
| 박물관 | IIIF Presentation2.1.1 §2.1; Harvard object299843 원 Manifest | 작품 전체와 개별 Canvas는 다른 단위. 실제 JSON에는7 Canvas가 있으며 특정 뷰 선택과 작품 찾기가 다른 질문 | 숫자 label로 앞/뒷면을 추측하지 않음. 2.x sequences/canvases와3.x items를 혼용하지 않음 |
| 기술 표준 | RFC9110 §8.6/§9.3.2; Werkzeug 고정판 test_response_304_no_content_length | HEAD/304의 Content-Length는 대응 GET/200의 길이 의미일 수 있고 생략 가능. 본문이 없으니 항상0이라는 해석은 틀림 | 원 구현 테스트의 assertion을 읽었지만 실행하지 않음. 204의 금지와304의 허용·조건을 구별 |

[IIIF2.1.1](https://iiif.io/api/presentation/2.1/#basic-types), [Harvard 원 Manifest](https://iiif.harvardartmuseums.org/manifests/object/299843), [Harvard 실제 JSON 관측](evidence/harvard-manifest-observation.json), [RFC9110 §8.6](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.6), [Werkzeug 고정 테스트](https://github.com/pallets/werkzeug/blob/6389612fd1ee1bd93579eed5026e8fd471d04abd/tests/test_wrappers.py#L1064-L1073). Harvard는 웹 텍스트 서비스가 content-type을 처리하지 못했으나 같은 원 URL의 HTTP JSON을 직접 받아 읽었다. 도구의 실패를 자료 부재로 해석하지 않았다.

## Q6. 안내 효과, 기존 지식, 반복 노출을 얼마나 구별했는가

본 결과를 원격 봉인한 뒤 사전 지정 G2/L2의 B에서 보존 조건 구절을 삭제했다. G2 C는 74자에서 `타입·배열 구조는 그대로 두어도 ` 18자를 빼56자가 되었다. 길이 동일 대조가 아니다. 새 문맥 r13은 A/B와 같은 세 개봉·3512자·3684B를 읽고 세 단계와 최종 모두 보류했다. L2 C는 공석이라 실행하지 않았다. 보조 실제3단계·미실행3단계를 주18관측에 더하지 않았다. [음성 대조 꾸러미](negative-packets.jsonl), [보조 궤적](control-trails.jsonl), [보조 평가](adjudication/control-review.md).

**삭제한 것은 hint의 반복 강조다.** 공통 요청에는 타입·배열 구조를 유지하라는 조건이 계속 들어 있다. 그러므로 결과가 같다는 사실로 그 조건이 불필요하다고 말할 수 없다. r13 첫 판단의 ‘배열 참조가 중복되어 있다면’은 의도하지 않은 중복이라는 한정이 없어 의도된 원1의 반복까지 문제로 오해할 여지가 있다. 그러나 원인 확정이나 무조건 Make Unique 처방으로 이어지지 않았고 최종은 유보였다. 이를 위험한 확정으로 늘리지 않았다.

주 수신에서도 A/B 공통 요청이 이미 충분히 구체적이어서 B가 새로운 정보보다 주의를 반복했을 가능성이 크다. 세 쌍 모두 경로가 같고 동일 모델 계열의 단일 반복뿐이라 우연한 선택 안정성, 사전 지식, 안내 효과를 추정해 분해할 수 없다. 또한 원 URL에서3개봉 안에 모든 gold 조건에 도달하는 최적 경로가 실제 존재하는지는 별도로 입증하지 못했다. 낮은 성공 수에는 안내보다 예산·인터페이스의 상한이 영향을 줄 수 있다. 같은 원 요청과 그 코드 예제는 별도 저작이어도 같은 작성자·사건에 종속된다. A/B가 같은 본문을 읽은7249자를 독립된 자료7249자로 세지 않는다. 기존 지식과 잠정 주장은 답의 `prior_knowledge`와 평가의 source coverage에서 구별했다.

좁은 안내 때문에 A는 찾은 반례를 B만 놓친 차등 사례는0건이었다. 그러나 양쪽 모두 필요한 반례의 전체 근거에 도달하지 못했으므로 ‘안내가 반례 탐색을 해치지 않는다’는 보장도 없다. G2의 두 번 목록 개봉은 장황한 캐시 파일이 원 코드까지의 경로를 막을 수 있음을 보여 주지만, 그 장벽을 B가 유발했다는 증거는 아니다. 이 결과를 보고 좋은 사례를 추가해 주 표본을 바꾸지 않았다.

## Q7. 업스트림에 남길 기록과 후속 독자의 몫

이번 요청들에 대해 입증된 분류는 **세 번 열어도 원 목적의 전체 조건은 미확인: G1·G2·G3**이다. URL만으로 충분, 한 줄이 있어야 충분, 다음 절까지 읽으면 충분이라는 성공 분류를 부여할 사례는 확보하지 못했다. G1/G3는 다음 구현 검사를 설계할 일부 코드를 복원했고 G2는 먼저 열어야 할 원 파일이 남았다. 이를 단순히 ‘실패’ 하나로 버리면 무엇을 확인했고 다음에 어디를 읽어야 하는지가 사라진다. [쌍 원장](pairs.csv), [실제 노출](trails.jsonl), [상세 답](answers.csv).

업스트림에 유용한 최소 연구 기록은 원 요청·원 URL/fragment, 실제 도착/판/파일 해시, 한 줄의 근거가 된 요청 구간, 실제 읽은 위치·누적 비용, 확인한 조건과 아직 남은 구별 입력이다. 특히 `조건부`라는 라벨과 `source_segment_sufficient_for_original_goal=false`를 함께 보존해야 한다. 원 링크를 더 좋은 후계 URL로 조용히 교체하거나, 보조 현재판 실행값을 수신자의 본문 근거로 소급하지 않는다. 이것은 후속 제품 설계를 위한 제안이며 중앙 DB·계약·원장을 변경한 구현이 아니다.

| 관측 가능한 비용 | A | B | 보조 C |
| --- | ---: | ---: | ---: |
| 실제 수신 꾸러미 | 3 | 3 | 1 |
| 본문 개봉 | 9 | 9 | 3 |
| 본문 문자 | 7249 | 7249 | 3512 |
| 본문 UTF-8 바이트 | 7505 | 7505 | 3684 |
| 한 줄 추가 문자/바이트 | 0/0 | 233/503 | 56/122 |
| 능동 제작·판독 작업시간 | 미계측 | 미계측 | 미계측 |

공통 요청·URL의 문자/바이트는 `metrics.json.costs`에 별도로 두었다. 이것은 4500자 본문 예산과 다른 전달 비용이고 JSON 문법/레이블/시스템 지시의 전체 토큰 비용은 아니다. 작성·판독 중 기록된 시작/종료 차이는 도구 지연과 추론을 포함하는 wall time이며, 능동 시간이나 장기 사용자 시간 절약으로 환산하지 않는다. URL만, 짧은 확인선, 후속 전문 독해의 세 선택은 유지할 수 있지만 이 실험에서 한 줄의 인과적 성과를 입증한 선택은 없다.

## 자료·실행·반복 횟수의 대사

| 자료층 | 목표 | 확보한 고유 1차 저작 | 필수 배당 | 결손 |
| --- | ---: | ---: | ---: | ---: |
| 실제 링크 인계 요청 | 6 | 3 | 3 | 3 |
| 공식 문서·원 사례 | 8 | 13 | 8 | 0 |
| 별도 회귀·실패·상충 | 6 | 16 | 6 | 0 |
| 두 타분야의 규격·실제 예 | 4 | 4 | 4 | 0 |
| 합계 | 24 | 36 | 21 | 3 |

`sources.jsonl`은97행으로 원문 직접열람85행과 접근실패12행을 구분한다. 직접열람85=고유1차73+동일저작 중복11+제외 재게시1이다. 고유1차73=필수층 배당 가능36+심사·관련성 제외34+미배당 보조3이다. 같은 Godot 매뉴얼의 절/판, 같은 엔진의 파일/PR, 원 예제의 후속 포트는 각각 한 계보로 묶었다. LilyPond 공식 제목이 다른 매뉴얼5개와 원파일/기대 입력이 다른 회귀4개는 저작 단위를 구별했다. 이것은 독립 저자·실험 수가 아니다. [배당과 모든 계보](audit-sources/allocation.json).

| 관측/실행 단위 | 실제 | 산입 제한 |
| --- | ---: | --- |
| 자연 주 사건 | 3 | LilyPond 공석3과 합성 입력은 별도 |
| 주 새 수신 문맥 / 단계 | 6 / 18 | 6꾸러미·18단계 미모집, 조기종료0 |
| 보조 삭제 수신 문맥 / 단계 | 1 / 3 | L2 보조 미모집1꾸러미·3단계 |
| 현재 Godot4.7.2 import/run 명령 | 14 | import5·관측 run9; 아래 변형 분리 |
| 원 G2 현재판 / 작성자 후속 G3 포트 현재판 | 각1 run | 원 역사판 재현이 아님 |
| 연구 구성/변형 현재판 | 7 run | G1구성4, G2변형2, G3flag변형1 |
| 원 요청 당시 Godot 역사판 실행 | 0 | 정확한 바이너리/빌드 미확보 |
| LilyPond 조판 / Werkzeug 테스트 실행 | 0 / 0 | 원 입력·기대·코드 독해만 |
| 도구 합성 검사 | 2 synthetic sessions | 수신 예산·순서 제어 검사; 주 문맥/자료 수에 미산입 |

주 수신 뒤에 원 자료와 반례·비용을 추가로 정리했으며 사후 보조를 주 사건 성과에 합산하지 않았다. 원 영수증의 관측 주체·환경·명령·종료값을 유지했다. 논문식 인간 실험·전문가 독립 실사용 확인·전체 사이트 확률·장기 시간 절약은 수행하거나 추정하지 않았다.

## 저장·재현·검사 범위

계획 기준은 `c40ef7723d851b628233bfb60dff8dfd292385cf`, 실제 시작은 `0bcaf7c90f3324447fd1b8bf12c514187ca4776b`이다. 관련 필독 파일의 계획 이후 변경은 dot-control의112 배정 행이며108의 입력은 같았다. 운영 선행108의 HANDOFF `8b00aaa2…`와 RESULT/pairs/metrics `806cdff8…`를 직접 읽었다. 108의 값 일치8/16·8/16과 충분한 근거4·2를 재채점하지 않았고, 다른 PLAN#27 작업자의 파일·검토·중간 결과를 사용하지 않았다. [시작/차이 영수증](evidence/repository-input.json), [계약 manifest](manifest.json), [묶음별 원격 SHA](evidence/commits.jsonl).

변경 범위는 이 작업의 owned_path뿐이다. 원격 반영은 GitHub Git-data API의 기대 HEAD 조건으로 수행했다. 셸 push의 인증 실패는 우회 계정 변경 없이 연결된 지정 계정 도구로 처리했다. 중앙 진행표·main·통합 브랜치를 수정하지 않았다. 만료된 공개 ZIP 다운로드 서명 쿼리는 후속 메타데이터 정리로 제거했으며, 원 노출 문자열·선택·판단 불변을 검증하고 원 seal SHA와 파생 파일 해시를 구분했다.

`reproduce.md`에는 원장 재계산과 미실시 역사판/조판 검사의 명령·입력·최소 재개 행동이 있다. 결과판을 먼저 원격 커밋한 뒤 고정 SHA의 RESULT·원장·대표 근거·재현 절차를 다시 읽고, 그 판에서 명시 session check와 저장소 공통 검사·작업 검산을 수행한다. **검사 결과는 후속 영수증 커밋의 `evidence/final-verification.json`과 HANDOFF에 기록한다.** 이 결과 본문에 아직 실행하지 않은 최종 검사를 통과했다고 미리 쓰지 않는다. 자동 발견 세션 수와 이 manifest의 명시 검사를 따로 보고하며, 뒤의 영수증/HANDOFF를 앞선 결과판 검사에 포함시키지 않는다.
