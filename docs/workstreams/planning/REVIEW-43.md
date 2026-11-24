# REVIEW-43 · 같은 링크로 어떤 사용자의 어떤 요구까지 답할 수 있는가

탐색기의 목적은 개발자가 만들 소프트웨어의 전체 또는 일부와 그 목적을 받아, 다시 만들 필요가 없는 부품이나 다른 분야에서 가져올 원리를 원문 링크와 적용 이유로 돌려주는 것이다. 이번에 링크를 고르는 데 실제로 도움이 된 단서는 **보존해야 할 조작**이었다. 같은 버전 문자열도 최소판 비교 결과가 달랐고, 악보에서는 같은 수의 마디를 나타내는 쉼표 모양이 달랐다. ‘수정이 확인됨’, ‘두 라이브러리 포함’과 같은 표시에서는 주체와 실행 조건이 빠지면 사용자가 원한 결과까지 말하기 어려웠다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

**새 DONE은 AF-RES-178~185 여덟 건이고, 작업자 자체 판정은 여덟 건 모두 PARTIAL이다.** AF-RES-186은 계획 요청 시점에 Codex Cloud에서 진행 중이었다. 이번 배정안에는 완료된 자료에서 출발하는 웹 조사·설계 8건, 바로 준비할 수 있는 Codex 검사 1건, 186의 확정 인계 뒤에만 시작할 Codex 검사 1건이 있다. [진행표][control] · [작업 지시문 전체](NEXT_TASKS-43.json)

## 무엇을 읽고 검산했는가

`work/planning@b4be70c`의 최신 누적 검토인 REVIEW-42를 먼저 읽었다. 그 검토의 기준판과 요청 시점 통합판을 JSON 작업 ID 및 전체 필드로 비교했다. 기존 175행의 변경·삭제는 0건이고 새 행은 9개다. 새 DONE 여덟 개에 대해서만 중앙 `result_commit`과 해당 작업 브랜치 끝의 일치를 확인하고 소유 경로의 HANDOFF, RESULT, 자기점검, 출처·사건·결과 원장을 읽었다. 이전 결과는 누적 검토에서 이어받았다. 186은 중앙 행과 이미 배정된 brief로 범위를 확인했다. [직전 누적 검토][r42] · [직전 통합판][before] · [이번 통합판][control] · [두 통합판의 차이][delta]

| 진행표 기준판 | 전체 | DONE | RUNNING | BLOCKED | 이번 검토에 새로 포함한 결과 |
| --- | ---: | ---: | ---: | ---: | --- |
| 42차 `128f673` | 175 | 171 | 0 | 4 | 비교 기준 |
| 43차 `0f6765d` · 2026-11-24 19:40:46 UTC | 184 | 179 | 1 | 4 | 178~185 |

DONE 179건은 연구 177건과 연결 시험 2건이다. 179건 모두 중앙 `acceptance_evidence`가 빈 배열이다. 018은 대화 한도 뒤 인계 미커밋, 035는 실행 종료 뒤 인계 미확인 상태다. 149는 조사한 7주 중 지정한 세 유입 경로를 각각 6건씩 복원한 주가 없었고, 151은 최초 N0 응답·독립 가림 검토·원사용자 비용을 확보하지 못했다. 이 네 차단 상태와 이번 파일의 196 착수 보류는 서로 다른 진행표에 속한다. [기준판의 작업·차단 사유][control]

| 새 작업 | 중앙에 저장된 작업 브랜치 인계판 | 작업자가 명시한 결과·자체점검판 | 출처 원장 행 / 작업자의 직접 산입 단위 |
| --- | --- | --- | --- |
| 178 · 버전 비교 | [bbdf4dd][h178] | [3e56429][r178] | [47 / 고유 35][s178] |
| 179 · 특정 연결의 SQLite | [51e726b][h179] | [7599d87][r179] | [61 / 고유 46][s179] |
| 180 · 제보자 확인 | [6b1afbb][h180] | [c6a9908][r180] | [126 / 고유 36][s180] |
| 181 · 번역 초안 노동 | [a5d9b2c][h181] | [668a3d8][r181] | [36 / 고유 26, 고정 원작업 파일 0][s181] |
| 182 · 악보 출판 그림 | [630905e][h182] | [43864bc][r182] | [79 / 고유 36, 그림 원파일 URL 7][s182] |
| 183 · 금액 배분 | [ed7c727][h183] | [b36b477][r183] | [44 / 고유 24][s183] |
| 184 · 배포와 재빌드 | [2b83f0f][h184] | [094e290][r184] | [70 / 보조를 포함한 실질 문서 29, 고정 대상 재빌드 원자료 0][s184] |
| 185 · 의존성 조합 | [6581ffc][h185] | [a6e7aff][r185] | [59 / 고유 41][s185] |

이번 검토에서는 출처 JSONL **522행**과 작업별 고유 source_id 수, CSV 열 수·행 수, 180의 확인 시점, 181의 시간·단어 합계, 182의 양판 파일 지문, 183의 적격 비교 여부 등을 저장소 원장에서 검산했다. 한 사건의 여러 면이나 접근 실패도 원장에 들어간다. 표의 고유 자료 수는 작업자별 산입 기준이고, 여러 작업의 자료 수를 더해 독립 실험 수로 삼을 수 없다. 외부 실험을 새로 재현하거나 작업자의 역사 자료 전부를 독립 재수집한 범위까지는 검증하지 않았다. [180 확인 원장][confirm180] · [181 시간 원행][eff181] · [182 입력 지문][fix182] · [183 비교 원장][comp183]

## 42차까지 쌓인 제품 판단

| 설계자가 답해야 할 질문 | 앞선 근거의 범위 | 여전히 선택을 가르는 조건 |
| --- | --- | --- |
| 부분 설계와 목적을 어떻게 받을까 | 020의 전달 주장은 72/73이었으나 모든 충돌을 해소한 묶음은 2/16이었다. 103은 외관 10/10을 유지하면서 텍스트 선택을 잃었고, 107은 개별 발생 위치로 편집 6/6, 공유 정의만으로 0/6이었다. 159의 48자리에서 위치는 기능 46개, 소비 역할은 48개를 갈랐다. | 선택한 객체·다음 조작·보존할 값을 받는다. 구별이 되는 설계와 실제 원사용자가 그 뜻을 확인한 사건은 별도로 센다. |
| 먼 분야의 원리가 무엇을 더해 주나 | 010은 분야 단서로 원리 7군을 찾았다. 033은 단서 없이 본 144쌍에서 당시판 지지 0, 022는 미인지→선택 변경→시행 0/24, 145는 독립 초안 0/16이었다. 166의 대기열과 174의 지도 레이블은 각각 48예측 셀을 남겼으나 적격 사전 비교가 없었다. | 원리 설명, 당시 설계자에게 도달한 경로, 가까운 대안보다 추가로 가른 선택, 실제 선택 변경은 각기 다른 주장이다. |
| 링크 몇 개를 어떤 조합으로 보여줄까 | 040의 완전 적격은 0/8이었고 044의 고정 풀에서는 두 묶음 방법이 같았다. 114에서 충돌로 묶었던 138건은 118 기준으로 명시 충돌 7·미확인 131이다. 146은 48후보 중 직접 충족 0·부분 15·충돌 14·미확인 19였고 추가 노출 세 건은 한 요구에 몰렸다. 177의 mdBook 요청은 단일 페이지나 검색 중 하나를 허용했다. | 한 후보에 대한 두 근거, 서로 대체 가능한 두 후보, 같은 판에서 함께 작동해야 하는 두 부품을 구별한다. 검색 폭이나 최종 링크 수에 일반 최적값은 없다. |
| 옛 근거와 현재 후계를 어떻게 기억할까 | 055는 과거 답 4/4·다음 판 0/4였다. 075는 전체 후보 이력이 없으면 단독/공동 1위 주장을 각각 16/16 보류했다. 147은 당시 증빙으로 과거 답 112/112를 복원했다. 150의 세 보관안은 동일성 값과 근거가 함께 맞은 쌍이 7·9·15/16이었다. 161의 병합 취소 뒤 하류 P910에는 별도 undo가 필요했다. 169의 분할 언어 코드 네 개는 등록부가 후보 둘씩, 라이브러리는 기본값 하나씩을 가리켰다. | 과거 원문을 인용할 때와 오늘 사용할 대상을 정할 때의 최소 기록이 다르다. 169의 실제 개별 레코드 옛값→새값 쌍은 0이었다. |
| 무엇을 언제 다시 열고 어느 사용자에게 권할까 | 024의 주기 점검은 무효화 11/11, 신호 점검은 8/11이었다. 신호는 열람 108개가 적고 전송량은 5,672,462바이트 많았다. 152의 신규 15건 중 신호/희소 공급원 보장은 14, 주기는 13이었고 예산과 수요에 따라 지연 우위가 달랐다. 162는 공식 철회와 사용자별 노출 차이, 170은 8개 사이트의 설정 후보와 태그가 남은 편집을 찾았다. | 설정·출시·권한·실제 조작의 주어와 날짜가 필요하다. 170에서 같은 계정과 조건의 마지막 저장 실패→첫 성공은 0쌍이었다. |
| 작성자가 결과를 받거나 수용했다고 말할 수 있나 | 158의 제출 28건은 수신 확인이 아니었다. 163의 발신 35건 중 특정 통지를 지목하고 원제출자가 재개한 보강 사례가 1건 있었다. 171의 WCAG 자연 표본은 한 제출자의 여섯 건·공개 댓글 33개에서 당사자 후속 0건이었다. 보충에는 만족과 반대가 모두 있었다. | 닫힘·반응을 계정·대상·원요구·후속 행동에 연결해야 한다. |
| 참고 링크가 총노동·재작업을 줄였나 | 034는 한 단계 380→57초, 전체 849→847초였다. 160의 이식에는 1,061.9인시가 있었지만 비교 쪽에는 추정치가 섞였다. 164의 24명 실험은 그대로 사용/수정 상속 비교가 같은 직접작성 집단을 공유했다. 172는 역할별 합산과 실패 배정까지 갖춘 서식을 설계했으나 전원·동일 기능·물리 시간·독립 검수가 다 갖춰진 비교는 0이었다. | 사람별 활성창, 배정된 전체 분모, 산출 품질, 별도 검수·제공자 노동을 구분해야 한다. 기술적 재사용을 자동으로 절약 시간으로 환산할 수 없다. |
| 호환·보존·독립 검증의 어떤 증거가 있나 | 154는 입고 성공 후 명시 원본 회수 10/10, 기본 다운로드의 동일 바이트 6/10이었다. 165의 심사판과 배포 목록이 지정 파일까지 맞은 사례는 1/8, 167의 양판·같은 파일·실제 수신값 연결은 0이었다. 173은 글꼴 설치 규칙, 175는 방향별 재료·하중의 정성 등급까지였다. 176은 EARL 원보고→표시 55/55가 맞았고 주표본 20쌍의 독립 실행 여부는 미확인이었다. | 출하, 열림, 동일 객체·값, 실제 공동 동작, 동일 근거의 재표시는 서로 다른 판정이다. |

원문 범위와 이전 정정은 REVIEW-42에서 이어진다. 이 결과들은 링크 중심 답변을 설계할 때 비교할 대안과 필요한 증거를 좁힌다. 입력 API·DB 구조·상시 수집기·사용자 효과는 여전히 연구 대상이다. [42차 누적 근거 색인][r42] · [제품의 미결정 사항][product]

## 여덟 작업에서 확인된 것과 빈 고리

**178 · 같은 심볼을 바꿔도 사용자의 비교 규칙은 달라질 수 있다.** 지명한 세 소비자 모두 같은 호출 위치의 변경안을 추적했다. scikit-learn-extra #167은 실제 병합, Yellowbrick 것은 제안, Elpy 것은 포크다. Elpy 본류에서 경고를 억제하거나 setuptools를 추가한 수정은 옛 비교 함수를 유지했다. 보강 MNE 사례의 `1.0.dev0`와 `1.0`은 두 정책의 판정이 갈렸다는 당사자 보고가 있다. Manjaro 사례는 당시 parse 결과와 훗날 엄격한 버전에서 거부하리라는 코드 추론을 구분해야 한다. 지명 세 곳 모두 변경을 포함한 첫 출시 태그와 같은 입력·환경의 구/신 판정쌍은 미확인이다. 따라서 표준 문자열이라는 사실 외에 표준 정렬도 사용자의 의도인지가 권고 조건이다. [호출 11행][calls178] · [값 28행][vals178] · [실제 병합된 PR](https://github.com/scikit-learn-contrib/scikit-learn-extra/pull/167) · [MNE 버전 판정 보고](https://github.com/pypa/packaging/issues/514)

**179 · ‘JSON 지원’은 하나의 질의가 아니다.** 고정 6맥락×3술어 18자리 중 17개는 미확인이고, 한 건은 Label Studio의 `JSON_VALID` 실패다. 이 실패는 원 DDL·입력·실효판이 다 나오지 않는다. 반대로 CPython E1은 같은 커서에서 판·질의·오류가 연결되지만 실행한 식은 `json_object`다. 따라서 E1의 오류를 `JSON_VALID` 직접 실패로 옮기면 두 원문 모두 왜곡한다. 전체 60자리의 성공 3개는 Swift 두 환경과 별도 Python의 BLOB 반환 한 건이다. 같은 호스트에서 CLI 3.24.0과 Python 3.21.0이 갈린 보강 사례도 있다. 배포 레시피를 안내하는 문장, 특정 연결에서 원하는 값과 타입을 얻었다는 문장의 근거가 달라진다. [패키지 17행][pkg179] · [관측 60행][obs179] · [원 커서 보고](https://github.com/python/cpython/issues/84451#issuecomment-1093868742) · [앱 원제보](https://github.com/HumanSignal/label-studio/issues/679)

**180 · ‘확인됨’의 주어를 복원할 수 있는 범위가 생겼다.** VS Code 두 마일스톤에서 현재 목록의 앞 30개씩을 심사해 자연 8건·제외 52건을 얻었고, 보강 4건은 별도로 읽었다. 자연 8건의 지정 창 안에서 원제보자 텍스트 후속은 0이었다. 보강 #197268의 원제보자는 같은 명령의 대상 선택을 재시험했다고 명시했지만 빌드·fixture·숨김 상태는 고정되지 않았다. #197319는 간헐성에 더해 생성기도 바뀌었다. 공개 확인 원장 59행 중 ‘별도 실행/재현 진술’ 24행에는 사전 실패와 같은 사람의 반복이 섞인다. 최초/최종 마감 후 30일 창에 각각 6/4행이며 독립 실험 24회라는 근거는 없다. 병합 8개의 stable 태그 포함과 실제 동일 조건의 원제보자 사후 성공(확인 0건)을 분리한다. [사건별 허용 문장][cl180] · [확인 원장][confirm180] · [원제보자의 재시험 문장](https://github.com/microsoft/vscode/issues/197268#issuecomment-1832685935)

**181 · 번역자 한 명의 기록시간은 계산할 수 있었다.** 터키어 후보 문서 1의 직접 번역 다섯 분절을 다시 합하면 2,061,853ms, 원문 111단어, 약 3.23단어/분이다. 같은 원문 세 조건에는 서로 다른 세 사람이 배정되는 설계다. 언어별 네 자리, 총 여덟 문서의 24개 예정 배정 중 처리행을 본 배정은 하나였고, 고정 원 XML·완전한 세 조건 짝·독립 품질 연결은 각각 0이었다. 연구자가 보고한 언어별 속도 중앙값은 전체 연구의 통계이고, 100단어 환산값은 설명용 계산이다. 이를 고정 문서의 전후 절감이나 검수 포함 인시로 쓰면 안 된다. 원아카이브 열람 실패와 연구 설계에 없는 독립 검수는 서로 다른 공백이다. [직접 합산한 다섯 행][eff181] · [시간창·예시 구분][bound181] · [저자 논문](https://aclanthology.org/2022.emnlp-main.532/)

**182 · 같은 마디의 그림에서 읽힌 차이는 실제로 있다.** 두 출판판×여섯 시험의 12자리 중 첫 선정 속성을 11자리에서 읽었다. 02c 구판의 `3,16,12`와 신판의 `3,15,단독 온쉼표,12,3`에서 쉼표 묶음이 다르고 첫 숫자 3의 모양도 다르다. 33b의 붙임줄 곡선은 두 그림 모두에서 읽히지만 소리를 이어 재생했는지는 미확인이다. 같은 이름의 태그 XML 전체 blob이 일치한 쌍은 0/6, 첫 마디 내부가 일치한 쌍은 5/6, 국소 속성과 시각 결과를 대조한 쌍은 4/6이었다. 출판 문서에 실제 들어간 XML 바이트와 태그를 연결한 자리는 0/12, 직접 읽은 그림 원파일 주소는 7개여서 엄격한 하한 8개에도 한 개 모자랐다. 그림 차이를 변환기 버전 하나의 인과로 돌릴 수 없다. [입력 원장][fix182] · [시각 관측][obs182] · [구판 그림](https://lilypond.org/doc/v2.24/input/regression/musicxml/51/lily-32ce4bc4.png) · [신판 그림 PDF 7쪽](https://lilypond.org/doc/v2.26/input/regression/musicxml/collated-files.pdf#page=7)

**183 · 경쟁 규칙의 예측은 남았고 실행 적중률의 분모는 비었다.** 입력 8개×규칙 3개로 예측 24행을 결과 개봉 전 커밋했다. ②·④·⑥에서 앞 순서 지급과 최대 나머지 원리가 수령자를 다르게 지목했다. 같은 세 입력에서는 별도의 근접 반올림 규칙도 최대 나머지와 일치했다. MoneyPHP는 나머지를 부동소수로 비교하고 동률이면 입력 순서에 따르므로 정수 분수·고정 ID의 원리와 일반적으로 같다고 할 수 없다. 두 구현×8입력의 정확한 공개 기대값은 관련 예에 노출된 한 셀, 같은 입력·SHA의 공개 실행 출력은 0/16이다. 지명된 의석 원리가 추가 설명이나 반례를 주는 경우와 그것을 사전에 찾아서 더 나은 결정을 했다는 주장 사이에 증거 차이가 남는다. [고정 예측][pred183] · [16셀 판정][comp183] · [MoneyPHP 해당판 구현](https://github.com/moneyphp/money/blob/b358727ea5a5cd2d7475e59c31dfc352440ae7ec/src/Money.php#L319-L358)

**184 · 서로 다른 숫자를 세면 재현성이 부풀려진다.** Debian 4패키지×2아키텍처의 카탈로그 SHA256은 8개지만 같은 스냅샷의 서명 색인·원 buildinfo·해당 재빌드 산출 해시를 연결한 자리는 0/8이다. 주표본 밖의 lam 바이너리 표시 세 개는 로그 151245 하나를 가리킨다. 비교 로그 4개 중 실제 빌드 단계까지 가서 종료코드 2를 낸 것은 2개, 하나는 의존성 준비 실패, 하나는 원 buildinfo 조회 404다. 독일어·영어 grep 페이지의 같은 파일명과 해시는 재게시 증빙이다. ‘성공 재빌드가 없었다’거나 ‘바이트가 달랐다’는 결론은 이 자료로 낼 수 없다. 원장 70행 중 접근 실패 36, 고정 대상에 대한 당시 배포 자료 0/6·재빌드 자료 0/6으로 핵심 유형 하한을 채우지 못했다. [배포 후보][pk184] · [실제 빌드 단계 원장][runs184] · [원 실패 로그](https://reproduce.debian.net/amd64/api/v1/builds/151245/log)

**185 · 같은 lock이 있는 조합과 사용자에게 보장할 조합은 다르다.** 고정한 판 네 개의 manifest에서 간선을 읽었다. 배포 원본과 관련 구절을 맞춘 것은 2/4였다. Chromium `d41c4d24`의 같은 root와 lock에서는 png 0.18.0-rc와 zip 2.6.1(하류 패치)이 flate2 1.1.1로 연결된다. 별도 스냅샷의 flate2 1.1.5를 여기에 합칠 수 없다. ZIP 단독 컴파일 실패/수정판 보고도 있다. 그러나 같은 target·명령에서 PNG와 ZIP의 두 입출력이 성공한 사건, 두 소비자가 함께여서 정확판의 실패가 발생한 사건, 두 형식이 모두 필수라는 자연 발화와 같은 실행을 이은 사건은 확인되지 않았다. ‘구현이 Rust’, ‘C 컴파일러 불필요’, ‘unsafe 코드 없음’은 사용자가 다르게 선택할 조건이다. [요구 15행][req185] · [그래프 18행][gr185] · [실제 하류 lock](https://chromium.googlesource.com/chromium/src/+/d41c4d24cd81aef76cda21e4ea84ab2ddb2c71e6/third_party/rust/chromium_crates_io/Cargo.lock)

## 서로 어긋나는 결론을 어떻게 판정했는가

| 함께 읽으면 충돌하는 주장 | 이번 근거에서 허용되는 해석 | 결론을 바꿀 자료 |
| --- | --- | --- |
| ‘공식 후계나 기본 기능이면 같은 사용이 된다’ · ‘같은 이름인데 결과가 바뀐다’ | 178의 유효한 개발판 문자열에서 비교 결과가 갈렸다. 179의 E1은 함수군 문제를 보였으나 요청한 정확 식이 다르다. 185의 같은 패키지 ID는 활성 target을 결정하지 않는다. | 같은 실제 객체·조작·배포 경계를 확인할 때만 한 링크로 충분하다고 좁힐 수 있다. 187·188·193이 각각 복사, 좌표 기준, 패키지 제공자의 다른 경계를 본다. |
| ‘표시나 같은 이름이면 당사자가 원하는 결과도 보존됐다’ · ‘같은 듯해도 대상이 다르다’ | 180에는 원제보자의 특정 조작 재시험, 182에는 눈으로 읽히는 같은 곡선, 184에는 동일 원로그의 재표시가 있다. 어느 것도 다른 빌드·재생음·독립 성공을 대신하지 않는다. | 189는 작성자가 확정하는 상태, 190은 실제 면과 일부 위치, 192는 논문과 배포물의 서로 다른 목적을 원자료로 가른다. |
| ‘효율이나 원리의 가치를 수치화했다’ · ‘비교할 원자료가 없다’ | 181의 시간합은 관측됐으나 비교집단 행이 비었다. 183의 예측은 공개됐으나 적격 관측은 0이고 가까운 설명이 같은 예측을 냈다. 둘 다 효과 0이라는 통계로 바꿀 수 없다. | 195는 기존 번역 원자료를 검사한다. 191은 선택을 바꿨다는 편집 결정, 194는 제안 전부터 대안을 알았는지와 실제 처분을 조사한다. |

[178 값][vals178] · [179 관측][obs179] · [180 회신][confirm180] · [181 노동창][bound181] · [182 그림][obs182] · [183 경쟁 규칙][comp183] · [184 계보][runs184] · [185 조건][gr185]

## 다음 배정과 의존 관계

앞선 작업에서 원본 파일을 못 열었는데 웹 검색을 더 시켜도 자료의 성격은 달라지지 않는다. DivEMT의 고정 ZIP은 검사자가 열게 했다. 웹 작업은 앞선 결과가 비워 둔 제품 결정에 대해 원자료 입구와 관측 단위가 서로 다른 여덟 질문을 맡는다. 아래 ‘착수 가능’은 데이터 의존에 관한 판정이다. 실제 배정 순서와 병렬 한도는 진행 담당자가 적용한다. 모든 지시문에 작업자 단독으로 사용할 고정 선행, 모집·제외 규칙, 방향이 있는 질문 7개, 유형별 직접 자료 22~24개 이상, 반증·필수 표의 열과 파일·중간 커밋·자체점검·부분 인계 기준이 있다. [배정 JSON](NEXT_TASKS-43.json)

| ID · 담당 | 의존과 착수 상태 | 조사 대상과 판별 단위 | 바꿀 수 있는 제품 결정 |
| --- | --- | --- | --- |
| 187 · 웹 | 178 완료 · 착수 가능 | NumPy 2 복사 정책, Datasets/Astropy의 하류 호출·객체·태그 | 값만 필요한 요청과 메모리 공유가 필수인 요청에 어느 후계 링크를 줄지 |
| 188 · 웹 | 179 완료 · 착수 가능 | OSTN15 수평·OSGM15 높이 자료, 적용 지역과 기관 대조점 | 오프라인 좌표 변환에서 라이브러리 외에 어떤 격자·기준면 링크가 필요한지 |
| 189 · 웹 | 180 완료 · 착수 가능 | MUI 자동완성 요청의 표시 문자열·선택 ID·확정 조작과 원작성자의 후속 | 한 질문을 더 하면 다른 상태나 콜백 링크가 필요한지 |
| 190 · 웹 | 182 완료 · 착수 가능 | Alice 두 디지털 소장본의 표제지·구절·삽화·무쪽수 면 | 부분 링크에 판·스캔면·구절/그림 단서 중 어디까지 남길지 |
| 191 · 웹 | 183 완료 · 착수 가능 | CSS Color 4의 두 고정 초안과 편집 결정, 색지각·인쇄의 적용 한계 | 외부 원전이 실제로 보강하는 설계 제약과 가까운 구현 설명으로 충분한 경우 |
| 192 · 웹 | 184 완료 · 착수 가능 | seaborn/MAPIE의 선호 인용, 설계 논문, 버전별 배포 레코드 | 같은 프로젝트의 서로 다른 저작 중 인용·학습·재사용 목적별 첫 링크 |
| 193 · 웹 | 185 완료 · 착수 가능 | Debian bsd-mailx/cron의 대체 제공자와 로컬·원격 전달 목적 | 패키징의 택일이 최종 사용자에게도 유효한지, 마지막 단계에서 물을 조건 |
| 194 · 웹 | 180·183 완료 · 착수 가능 | 네 Python 설계 제안의 첫 초안·당시 대안·작성자 회신·결정 | 기존 기능 링크로 충분한 경우와 그 존재를 알아도 새 설계가 필요한 경우 |
| 195 · Codex | 181 완료 · 착수 가능 | DivEMT 두 고정 ZIP의 여덟 문서·24배정·분절 원행 | 번역자 작업창에서 실제로 비교 가능한 범위와 결측을 계산 |
| 196 · Codex | **186 의존 · BLOCKED** | 186이 확정한 인계물의 인용 문장·원자료를 세 저장안과 두 가용 조건으로 복원 | 링크·해시·원문 사본의 보관 비용과 나중에 되찾을 수 있는 주장 범위 |

원자료 입구로는 두 NumPy 소비자의 실제 논의, OS의 공식 변환 자료, MUI의 사용자 제보, Wikisource 두 소장본의 Index, 날짜가 붙은 W3C 초안, 프로젝트 자체 CFF, trixie 패키지 선언과 Python 제안서가 있다. 입구의 존재가 하류 배포 결과나 사용자 수용을 미리 입증하지는 않는다. [소비자 변경 PR](https://github.com/huggingface/datasets/pull/6976) · [OS 자료](https://www.ordnancesurvey.co.uk/geodesy-positioning/coordinate-transformations/resources) · [자동완성 원요구](https://github.com/mui/material-ui/issues/36085) · [스캔 색인](https://en.wikisource.org/wiki/Index%3ALewis_Carroll_-_Alice%27s_Adventures_in_Wonderland.djvu) · [CSS 공식 초안](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/) · [MAPIE의 저자 인용 파일](https://github.com/scikit-learn-contrib/MAPIE/blob/master/CITATION.cff) · [bsd-mailx의 배포 선언](https://packages.debian.org/trixie/bsd-mailx) · [PEP 618](https://peps.python.org/pep-0618/)

**186의 경계.** 186은 W3C JSON-LD 고정 시험 열 개를 Gold v0.3.0과 JS v3.1.0에서 새 프로세스로 두 번씩 돌려 예정 40행의 값·오류·채점·반복 일치·과거 제출과의 차이를 확인하는 기존 Codex 작업이다. 기준판의 `result_commit`은 null이다. 187~194는 그 시험·엔진·영수증·채점에 참여하지 않으며 미완료 결과에 의존하지 않는다. 195는 사람 번역의 원 이벤트를 검산한다. 196만 `depends_on = ["AF-RES-186"]`이다. 중앙 DONE·고정 결과 SHA·HANDOFF·실제 인용 원자료가 있어야 열고, 확정 결과를 그대로 사용해 오프라인 출처 복원과 보관 바이트를 측정한다. 새로 엔진을 실행하거나 186을 다시 채점하는 배정은 없다. [186의 배정 원문][p42] · [진행 중인 기준판][control]

후속 원자료도 구체적으로 남는다. 178의 첫 배포판에는 원 커밋의 태그 포함 관계와 태그 내부 파일이, 179의 원환경 복원에는 설치 산출물과 실효 라이브러리·SQL 원문이 필요하다. 182의 렌더러 효과와 185의 공동 작동에는 각각 동일 원문·옵션, 실제 target·양쪽 출력이 선행한다. 183의 현행 배분값은 이미 고정된 입력으로 별도 실행이 가능하지만, 그 실행은 2025년 이전 공개 실행의 공백을 소급해 채우지 않는다. 184의 재현성 판정에는 당시 서명 색인·동일 패키지 원 buildinfo·식별 가능한 재빌드 해시가 필요하다. 각 인계에 재개 위치가 있으므로 이번 웹 조사와 섞이지 않는다. [178][h178] · [179][h179] · [182][h182] · [183][h183] · [184][h184] · [185][h185]

## 다음 판단에 가장 중요한 약점 세 건

| 약점 | 지금 허용되는 주장 | 판단을 바꿀 다음 자료 |
| --- | --- | --- |
| 공식 문서의 기능과 사용자가 보존하려는 마지막 조작 사이에 빈 고리가 있다. | 비교 규칙, SQLite 함수군 오류, 단독 ZIP의 보고, 원제보자의 제한된 재시험까지 각각 확인됐다. | 187·188·189·193에서 원사용자의 객체·지역·상태·목적과 소비자가 실제 사용한 단계가 일치하는 원행을 찾는다. |
| 같은 이름·공통 프로젝트·여러 표시만으로 서로 다른 근거를 합치기 쉽다. | 특정 출판 그림, 하나의 빌드 로그가 가리키는 표시 셋, 하나의 root lock까지는 식별했다. | 190·192의 원면/저작 연결을 확보한다. 196은 186의 인계가 확정된 뒤 그 출처를 다시 열려면 무엇이 남아야 하는지 측정한다. |
| 실제 행동의 효과와 연구자가 구성한 비교의 분모가 다르다. | 개별 번역자의 시간은 계산됐고 금액 배분의 경쟁 예측도 고정됐지만, 총노동 절감과 외부 원리의 추가 적중률은 미확인이다. | 195의 원배정·시간·출력, 191의 외부 원리와 편집 결정의 연결, 194의 대안 제시 전후 당사자 판단이 해당 주장을 바꿀 수 있다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6/docs/RESEARCH_WORKFLOW.md
[r42]: https://github.com/laadkke-arch/agentflow-open/blob/b4be70c502a86ce9deea596aab661100164c4a6a/docs/workstreams/planning/REVIEW-42.md
[p42]: https://github.com/laadkke-arch/agentflow-open/blob/b4be70c502a86ce9deea596aab661100164c4a6a/docs/workstreams/planning/NEXT_TASKS-42.json
[before]: https://github.com/laadkke-arch/agentflow-open/blob/128f673685ec804c526a38e3f89d4d8a43fcd299/docs/automation/dot-control.json
[control]: https://github.com/laadkke-arch/agentflow-open/blob/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/128f673685ec804c526a38e3f89d4d8a43fcd299...0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6
[h178]: https://github.com/laadkke-arch/agentflow-open/blob/bbdf4dd15393062e59c16a9d46b38d8255c672f3/docs/workstreams/research/AF-RES-178/HANDOFF.md
[r178]: https://github.com/laadkke-arch/agentflow-open/blob/3e56429384a418279b291621e48799b54a638b67/docs/workstreams/research/AF-RES-178/RESULT.md
[s178]: https://github.com/laadkke-arch/agentflow-open/blob/bbdf4dd15393062e59c16a9d46b38d8255c672f3/docs/workstreams/research/AF-RES-178/sources.jsonl
[calls178]: https://github.com/laadkke-arch/agentflow-open/blob/bbdf4dd15393062e59c16a9d46b38d8255c672f3/docs/workstreams/research/AF-RES-178/calls.csv
[vals178]: https://github.com/laadkke-arch/agentflow-open/blob/bbdf4dd15393062e59c16a9d46b38d8255c672f3/docs/workstreams/research/AF-RES-178/values.csv
[h179]: https://github.com/laadkke-arch/agentflow-open/blob/51e726b67b53e00f0134b16bd762b3a684b86d04/docs/workstreams/research/AF-RES-179/HANDOFF.md
[r179]: https://github.com/laadkke-arch/agentflow-open/blob/7599d87d39302958b580c2dbc29f1690b0f8f0e7/docs/workstreams/research/AF-RES-179/RESULT.md
[s179]: https://github.com/laadkke-arch/agentflow-open/blob/51e726b67b53e00f0134b16bd762b3a684b86d04/docs/workstreams/research/AF-RES-179/sources.jsonl
[pkg179]: https://github.com/laadkke-arch/agentflow-open/blob/51e726b67b53e00f0134b16bd762b3a684b86d04/docs/workstreams/research/AF-RES-179/packages.csv
[obs179]: https://github.com/laadkke-arch/agentflow-open/blob/51e726b67b53e00f0134b16bd762b3a684b86d04/docs/workstreams/research/AF-RES-179/observations.csv
[h180]: https://github.com/laadkke-arch/agentflow-open/blob/6b1afbba225dac3f051ea4a8c7bb8a6585071aea/docs/workstreams/research/AF-RES-180/HANDOFF.md
[r180]: https://github.com/laadkke-arch/agentflow-open/blob/c6a99088bdcf582cfee8a4abf3f95fcb43c519f7/docs/workstreams/research/AF-RES-180/RESULT.md
[s180]: https://github.com/laadkke-arch/agentflow-open/blob/6b1afbba225dac3f051ea4a8c7bb8a6585071aea/docs/workstreams/research/AF-RES-180/sources.jsonl
[confirm180]: https://github.com/laadkke-arch/agentflow-open/blob/6b1afbba225dac3f051ea4a8c7bb8a6585071aea/docs/workstreams/research/AF-RES-180/confirmations.csv
[cl180]: https://github.com/laadkke-arch/agentflow-open/blob/6b1afbba225dac3f051ea4a8c7bb8a6585071aea/docs/workstreams/research/AF-RES-180/claims.csv
[h181]: https://github.com/laadkke-arch/agentflow-open/blob/a5d9b2cc5f295fe5cb15764e3965c14326c872d9/docs/workstreams/research/AF-RES-181/HANDOFF.md
[r181]: https://github.com/laadkke-arch/agentflow-open/blob/668a3d89e4690752cfb5ee17fc83edffc1fa218c/docs/workstreams/research/AF-RES-181/RESULT.md
[s181]: https://github.com/laadkke-arch/agentflow-open/blob/a5d9b2cc5f295fe5cb15764e3965c14326c872d9/docs/workstreams/research/AF-RES-181/sources.jsonl
[eff181]: https://github.com/laadkke-arch/agentflow-open/blob/a5d9b2cc5f295fe5cb15764e3965c14326c872d9/docs/workstreams/research/AF-RES-181/effort-quality.csv
[bound181]: https://github.com/laadkke-arch/agentflow-open/blob/a5d9b2cc5f295fe5cb15764e3965c14326c872d9/docs/workstreams/research/AF-RES-181/bounds.csv
[h182]: https://github.com/laadkke-arch/agentflow-open/blob/630905e804ee9d733f8a4807f5dc68367842d63c/docs/workstreams/research/AF-RES-182/HANDOFF.md
[r182]: https://github.com/laadkke-arch/agentflow-open/blob/43864bce94e7a499c2ff13c7d7baf51d7b1b9c5f/docs/workstreams/research/AF-RES-182/RESULT.md
[s182]: https://github.com/laadkke-arch/agentflow-open/blob/630905e804ee9d733f8a4807f5dc68367842d63c/docs/workstreams/research/AF-RES-182/sources.jsonl
[fix182]: https://github.com/laadkke-arch/agentflow-open/blob/630905e804ee9d733f8a4807f5dc68367842d63c/docs/workstreams/research/AF-RES-182/fixtures.csv
[obs182]: https://github.com/laadkke-arch/agentflow-open/blob/630905e804ee9d733f8a4807f5dc68367842d63c/docs/workstreams/research/AF-RES-182/observations.csv
[h183]: https://github.com/laadkke-arch/agentflow-open/blob/ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb/docs/workstreams/research/AF-RES-183/HANDOFF.md
[r183]: https://github.com/laadkke-arch/agentflow-open/blob/b36b477fdded2d6cb8d84f72ae6eb9ef60f2be63/docs/workstreams/research/AF-RES-183/RESULT.md
[s183]: https://github.com/laadkke-arch/agentflow-open/blob/ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb/docs/workstreams/research/AF-RES-183/sources.jsonl
[pred183]: https://github.com/laadkke-arch/agentflow-open/blob/ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb/docs/workstreams/research/AF-RES-183/predictions.csv
[comp183]: https://github.com/laadkke-arch/agentflow-open/blob/ed7c7278be22a5ad6eb8e87255c7d7064d12c9fb/docs/workstreams/research/AF-RES-183/comparisons.csv
[h184]: https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/HANDOFF.md
[r184]: https://github.com/laadkke-arch/agentflow-open/blob/094e290cca25942e8dd29f3992b828b1112f748c/docs/workstreams/research/AF-RES-184/RESULT.md
[s184]: https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/sources.jsonl
[pk184]: https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/packages.csv
[runs184]: https://github.com/laadkke-arch/agentflow-open/blob/2b83f0fa4f86e97b9643eafaeecc6596cd245561/docs/workstreams/research/AF-RES-184/runs.csv
[h185]: https://github.com/laadkke-arch/agentflow-open/blob/6581ffcae5a6d902c469e8275e6e6b2a70de2cc5/docs/workstreams/research/AF-RES-185/HANDOFF.md
[r185]: https://github.com/laadkke-arch/agentflow-open/blob/a6e7aff412155cf87305b53bc4fab71483db7d41/docs/workstreams/research/AF-RES-185/RESULT.md
[s185]: https://github.com/laadkke-arch/agentflow-open/blob/6581ffcae5a6d902c469e8275e6e6b2a70de2cc5/docs/workstreams/research/AF-RES-185/sources.jsonl
[req185]: https://github.com/laadkke-arch/agentflow-open/blob/6581ffcae5a6d902c469e8275e6e6b2a70de2cc5/docs/workstreams/research/AF-RES-185/requirements.csv
[gr185]: https://github.com/laadkke-arch/agentflow-open/blob/6581ffcae5a6d902c469e8275e6e6b2a70de2cc5/docs/workstreams/research/AF-RES-185/graphs.csv
