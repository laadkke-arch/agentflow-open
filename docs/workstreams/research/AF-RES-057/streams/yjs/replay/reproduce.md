# Yjs 연구 재실행

이 입력은 `cases.json`에 봉인한 연구용 입력이다. 제품의 공개 시험 실행, 요청자의 역사적 실행, CI 실행과 구분한다. 관측 원본은 이 디렉터리의 `YN1.stdout.json`, `YN2.stdout.json`, `YT1.stdout.json`과 각 `receipt.json`이다. 최초 실행은 Node v24.22.3/npm 11.19.1에서 2026-11-23 UTC에 했으며 14개 변형 모두 예외 없이 끝났다. Node 반환 코드 0만 세지 않고 각 결과의 `status=completed`도 확인했다.

## 재현 명령과 입력

저장소 루트에서 다음 명령을 실행한다. 이 명령은 커밋한 lock의 전이 의존성과 integrity를 복원하며 AF-RES-057의 소유 경로 안에만 쓴다. npm lifecycle script는 실행하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.py --install
```

의존성을 이미 복원했다면 `--install`을 생략한다. Node/npm과 Python 3은 선행 입력이다. 이 스크립트는 `dependency-lock-13.0.0-94.json`, `dependency-lock-13.0.8.json`, `dependency-lock-13.6.28.json`에서 package.json과 package-lock.json을 만들고 각 디렉터리에서 다음과 동등한 명령을 실행한다.

```sh
npm ci --ignore-scripts --no-audit --no-fund
```

그 다음 `node research_replay.cjs <복원된 yjs 모듈의 절대 경로> YN1`, `YN2`, `YT1`을 실행한다. 경로는 스크립트가 계산하므로 기존 조사자의 임시 절대 경로가 없어도 실행할 수 있다. 재실행 출력과 영수증은 `docs/workstreams/research/AF-RES-057/.cache/yjs/reproduce/<version>/`에 생기며, 봉인한 원본 결과는 덮어쓰지 않는다.

| 자리 | 제품 고정판 / npm gitHead | 입력 변형 수 | 확인할 주요 출력 |
|---|---|---:|---|
| YN1 | 13.0.0-94 / dd2b8bc6c79d98e2fb8d773339d9de7532114eba | 8: normal, reverse, single_author, literal_only × A/B | normal A undo=`this text can not be undone`, B undo=`mine `; 둘의 redo=`this text can not be undonemine ` |
| YN2 | 13.0.8 / 772bb87d5cfcc4d9e87ba970731c6aa58f6809bf | 4: deletion, insertion_control × A/B | deletion A undo=`123 World`, B undo=`Hello123 World`; 둘의 redo=`123 World`; insertion 두 조작 undo=`123`, redo=`123Hello World` |
| YT1 | 13.6.28 / 0a09ff854b2ecd942b3c0f0e741253a214cee1bf | 2: boundary true/false | A undo=[1,2,3], B undo=[]; 둘의 redo=[1,2,3,4,5,6] |

문자열의 공백은 의미가 있다. YN1 `mine `에는 끝 공백이 있으며, YN2 `Hello123 World`에는 Hello와123 사이 공백이 없다. YN1 reverse는 첫 undo 후 A/B의 화면 텍스트가 같지만 남은 undo 깊이가 0/1이고, redo 뒤 두 번 undo하면 A는 보호 문장을 보존하고 B는 빈 문자열이 된다. single_author는 두 사건 모두 null origin이므로 두 조작 모두 보호하지 않는다. literal_only에서는 A에 undo 항목이 없고 B는 해당 삽입을 취소한다.

## 판과 실행 범위

`package-pin-verification.json`은 세 npm tarball의 gitHead가 봉인 SHA와 같고 설치된 UndoManager 소스 바이트가 고정 GitHub 원문과 같은 것을 기록한다. 재현 lock에는 당시 제품이 요구한 범위 안에서 2026년에 해석한 전이 의존성이 포함된다. 역사적 작성자나 CI의 Node 버전·전이 의존성을 복원한 것은 아니다. YN1 13.0.0-94는 이슈 작성 전에 공개된 호환 프리릴리스이며 작성자가 사용한 판은 미확인이다. 당시 마지막 정식판12.3.3의 동일 API 지원은 확인하지 못했다.

YT1 연구 실행은 공개 helper를 읽은 뒤 빈 단일 문서로 등가 입력을 구성했다. 공개 fixture는 사용자3개를 만들지만 선택 시험에서 실제 편집하는 것은 array0 하나다. 공식 test runner는 실행하지 않았다. 공개 assertion은 A undo만 선언하고 B와 redo는 연구용 확장이다. YN2의 private undoStack 복사는 원문 입력을 재현한 것이며 지원 API라고 보증하지 않는다.

## 사후 판 민감도: 주 분모에서 제외

2022년 수정 diff를 읽은 뒤에만 YT1과 같은 입력을13.0.8에서 실행했다. A와 B 모두 undo=[]가 관측되었고, boundary가 있음에도 undo 항목은1개였다. 이 결과는 버전 제한의 반례이며 봉인 전 예측의 추가 적중이 아니다. 재현하려면 다음을 사용한다.

```sh
python -B docs/workstreams/research/AF-RES-057/streams/yjs/replay/reproduce.py --install --include-posthoc-sensitivity
```

이 경우 출력은 주14개와 별도의 민감도2개다. 실행 당시 사용한 입력 선언은 `sensitivity-plan.json`, 실제 상태는 `YT1-sensitivity-1308.stdout.json`에 보존했다.
