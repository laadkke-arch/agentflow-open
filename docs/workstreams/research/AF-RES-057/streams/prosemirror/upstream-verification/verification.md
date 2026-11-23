# PT1 원시험 한 그룹의 별도 로컬 실행

**결과: 고정 `history1.5.0@554d6eedb76704d1db62d85768611ce4b611abd2`의 `history enables undo` 한 시험을 원본 fixture/helper와 upstream 실행기로 실행해 1개 선택·1개 통과했다.** 이 기록은 기존 최소 재생의 fixture 차이를 확인하는 별도 후속 증거다. 공개 CI, 원작성자의 실행, 새로운 사전 적중으로 세지 않는다.

- 기록 UTC: 2026-11-23T03:54:40.499599+00:00
- 실행 주체: `/root/prosemirror`, 같은 모델 연구 분담자; ChatGPT 클라우드 checkout.
- 실제 시험 UTC: 2026-11-23T03:53:26.926211+00:00부터 2026-11-23T03:53:27.285150+00:00까지.
- 실제 명령: `npm test -- --grep '^history enables undo$'`.
- 실제 종료 코드: 0. stdout: `history / enables undo / 1 passing (8ms)`.
- 실행 종류: `local_original_source_test`; `public_CI=false`.

## 무엇을 그대로 실행했는가

[고정 원파일](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/test/test-history.ts#L1-L38)의 원래 import, `mkState`, `type`, `command`, `history()` 설정, `prosemirror-test-builder` schema, 선택 시험 L31–38을 수정 없이 사용했다. 원 assertion 두 개는 a,b 입력 뒤 `doc(p("ab"))`, undo 뒤 `doc(p())`의 구조 동등성 검사다. 별도 출력 관측을 추가하지 않았으므로 raw 문서 문자열을 이 실행의 stdout이 출력했다고 주장하지 않는다. 시험 통과가 원래 equality assertion의 통과 근거다.

기존에 직접 취득한 고정 원본 `src/history.ts`와 `test/test-history.ts`를 별도 owned cache로 바이트 그대로 복사하고, upstream `pm-buildhelper src/history.ts`로 제품과 시험을 컴파일했다. source/test 해시는 빌드 후에도 같았다. upstream `pm-runtests`는 `@marijn/testtool`의 Mocha `grep(new RegExp(grep))`를 사용한다. 완전한 원시험 파일은 등록하지만 `^history enables undo$`의 고정 필터 때문에 **그 한 시험만 실행**한다. 웹시험은 없었고 브라우저는 사용하지 않았다.

opB closeHistory, redo, remote-b 확장을 이 원군에 넣지 않았다. 이 결과는 **기존 PM 봉인12변형·사후6변형과 별도인 추가 로컬 원시험1건**이며 기존 분모나 예측을 수정하지 않는다. PT1의 의미적 답은 E에서 봉인 전에 이미 노출됐으므로 새 적중 제한은 유지된다.

## 실제 단계·입력·산출

실행 cwd는 `/workspace/scratch/9ecab2fc200b/agentflow-open/docs/workstreams/research/AF-RES-057/.cache/prosemirror/upstream-verification`이다. 다음 세 단계의 실제 receipt·stdout·stderr를 보관했다.

```bash
npm install --ignore-scripts --no-audit --no-fund
npm run prepare
npm test -- --grep '^history enables undo$'
```

`install-receipt.json`에 최초 설치 시각/exit0, `execution-receipts.json`에 빌드/시험 시각과 각각 exit0이 있다. `source-fixture.json`은 SHA·고정 URL·바이트 해시, `execution-file-hashes.json`은 원본/컴파일 결과/실행기 해시, `environment.json`은 관측 환경과 패키지 버전이다. `test.stdout.txt`의1 passing이 선택·통과 개수 근거다. stderr의 npm 환경설정 경고는 보관했으며 실패로 바꾸지 않았다.

## 버전 경계

원본 `package.json`의 scripts/name/exports는 유지했다. 다만 원본 semver 범위를 연구용 정확 버전으로 고정했고 공통 core overrides를 넣었다. 따라서 고정 source의 실제 원시험 실행은 확인했지만, 2025 당시 작성자/CI의 전체 의존 묶음을 복원했다고 하지 않는다. 원본 manifest와 실행 manifest를 `original-package.json`/`package.json`으로 나눴다. 모든 설치 내용은 `package-lock.json`에 integrity와 함께 남겼다.

Node `v24.22.3`, npm `11.19.1`, `Linux-6.18.57-x86_64-with-glibc2.41`에서 실행했다.

| 의존 패키지 | 실제 설치 버전 |
| --- | --- |
| `@prosemirror/buildhelper` | `0.1.5` |
| `@marijn/testtool` | `0.1.3` |
| `@marijn/buildtool` | `0.1.6` |
| `prosemirror-test-builder` | `1.1.1` |
| `prosemirror-model` | `1.22.3` |
| `prosemirror-state` | `1.4.3` |
| `prosemirror-transform` | `1.8.0` |
| `prosemirror-view` | `1.33.11` |
| `prosemirror-schema-basic` | `1.2.5` |
| `prosemirror-schema-list` | `1.6.1` |
| `rope-sequence` | `1.3.4` |
| `mocha` | `10.8.2` |
| `typescript` | `5.9.3` |
| `ist` | `1.1.7` |

buildhelper/test-builder의 npm metadata 원문과 취득 영수증도 동봉했다. buildhelper0.1.5의 gitHead는822baee1b5f7bb100dbb8c3efe04ba37e18d36eb, test-builder1.1.1의 gitHead는09c41ad66b3c848c405af285ed470afc4e61cae0이다. 나머지 transitive 패키지는 현재 해결된 판을 lock으로 고정했다. 패키지 metadata 취득이나 설치는 외부 연구 저작 수를 늘리는 데 사용하지 않는다.

## 재개·재현 명령

checkout 루트에서 다음을 실행한다. 고정 두 원본 URL을 내려받아 저장된 SHA-256을 확인하고, 보관한 manifest/lock을 owned cache에 복사한 뒤 `npm ci`, upstream build, 정확 한 시험을 실행한다. cache가 없는 환경에서도 입력을 복원한다.

```bash
python docs/workstreams/research/AF-RES-057/streams/prosemirror/upstream-verification/reproduce.py
```

`npm ci` 재현 명령은 후속 담당자를 위한 절차다. 이 세션의 실제 최초 설치 명령은 위에 기록한 `npm install`이며 재현 스크립트를 추가로 실행하지 않았다. 기존 `sources.jsonl`, cases/predictions/observations/review 파일은 변경하지 않았다. 이 companion을 통합한 최종 보고서에서는 이전 시점의 upstream 미실시와 이후의 로컬 원시험1건을 시각으로 구분해야 한다.
