# YT1 원 fixture·runner 후속 확인

**고정13.6.28의 원래 `testInfiniteCaptureTimeout` 1개를 선택해 로컬에서 실행했고 1/1 통과했다.** 이 확인은 기존 단일 문서 연구 재생과 원 helper의 세 사용자 fixture 차이를 확인하기 위해 결과 봉인 뒤에 추가했다. 공개 CI, 원작성자 실행, 새로운 사전 적중으로 계산하지 않는다. 기존 cases/predictions/source/observations/final-review를 수정하지 않고 별도 시점의 동반 기록으로 남긴다.

## 실제 실행과 결과

- 소스: [yjs/yjs@0a09ff854b2ecd942b3c0f0e741253a214cee1bf](https://github.com/yjs/yjs/tree/0a09ff854b2ecd942b3c0f0e741253a214cee1bf), v13.6.28.
- 원시험: [tests/undo-redo.tests.js L49–57](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/undo-redo.tests.js#L49-L57). 원래 `init(tc,{users:3})`, 두 push, stopCapturing, undo, `[1,2,3]` assertion을 그대로 사용했다.
- 원 helper·runner: [testHelper.js](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/testHelper.js), [tests/index.js](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/index.js), 원 package.json의 npm test와 rollup 설정. 소스·시험·package/build 파일58개의 git blob hash가 GitHub 고정 tree와 모두 같았다.
- 설치 명령: `npm ci --ignore-scripts --no-audit --no-fund`. 원 package-lock의 lib0 **0.2.99**, y-protocols **1.0.6**을 사용했다. lock은 설치·빌드 후 바뀌지 않았다.
- 시험 명령: `npm test -- --filter 'undoredo: infinite capture timeout$' --seed 57`.
- 실행 UTC: **2026-11-23T03:52:58.444508+00:00 ~ 03:53:08.486309+00:00**, 종료 코드0.
- 원 runner는 `[159/206] undoredo: infinite capture timeout`과 해당 함수의 Success 한 줄을 출력했다. **206은 등록된 시험 수이고 실행한 시험 수는1이다. 205개는 filter로 건너뛰었다.** runner의 `All tests successful!`을206개 실행으로 집계하지 않는다.

완전 stdout/stderr, 명령·시간·hash 영수증은 같은 디렉터리에 있다. Rollup의 circular dependency 경고 및 별도 testHelper.mjs 빌드의 external 경고도 삭제하지 않았다. 실제 실행 대상 `dist/tests.cjs` 빌드는 성공했고 선택 시험은 통과했다.

## 확인한 범위와 남는 제한

이 실행은 원 helper의 세 사용자 fixture에서도 **opA의 선언된 마지막 배열 `[1,2,3]`**이 성립함을 로컬에서 확인한다. 앞선 최소 재생의 opA 마지막 상태와 일치하므로 그 지점의 fixture 차이는 확인되었다. 모든 내부 구조·미사용 동료의 상태·다른 입력까지 완전히 등가라고 주장하지 않는다. 원시험에 없는 opB·redo·반복 undo assertion을 추가하지 않았다.

앞선 최소 재생은 새로 해석한 lib0 0.2.120을 썼고 이번에는 원 lock0.2.99를 썼다. 현재 Node v24.22.3/npm11.19.1은2025년 작성자/CI runtime을 복원한 것은 아니다. 같은 SHA 공개 CI 로그나 원작성자 실행의 결손은 이 로컬 검사로 채워지지 않는다. 이전 보고 시점의 원 runner 실행0 기록은 그때의 사실이고, root가 이번 후속1회를 별도로 반영할 수 있다. 주 연구26변형·사후 감도8변형에 이 원시험 실행을 섞어 새 예측 정확률을 계산하지 않는다.

## 재현 명령

저장소 루트에서 다음 명령을 실행하면 새 owned cache에 소스를 내려받고58개 blob·원 lock을 확인한 뒤, 같은 필터의 원 runner를 실행한다. Python3.12 이상의 tar 안전 추출, Node와 npm이 필요하다. 원시험 외 함수를 실행하는 선택지는 제공하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-057/streams/yjs/upstream-verification/reproduce.py
```

위 스크립트는 원본 소스를 고치지 않는다. 생성물은 `docs/workstreams/research/AF-RES-057/.cache/yjs/upstream-reproduce/`에 둔다. 현재 디렉터리의 기록을 덮어쓰지 않는다. 기계 판정과 정확한 의존판·로그 경로는 `verification.json`에 있다.
