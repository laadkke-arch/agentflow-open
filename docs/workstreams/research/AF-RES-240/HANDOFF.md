# AF-RES-240 인계

## 식별과 상태

**완료 / REVIEW_READY.** 두 고정 바이너리와 ICU 이름 오류 상태를 실행해 확인했다. 자체 검토를 수행했다. 독립 검토는 미실시다. 실행 위치는 제공된 Codex Cloud Linux 셸이다.

- 저장소 `laadkke-arch/agentflow-open`, 시도 1, 브랜치 `work/research-af-res-240`, 소유 경로 `docs/workstreams/research/AF-RES-240/`.
- 계획 SHA `914dbfa789ebec97063ed97130ea2a71c2e9f503`에는 240 항목이 없었다. 시작 SHA `64e139f16309e41e30f9ec634eabe17fef908bbd`는 계획보다 5커밋 앞이며 차이는 진행표였다. 시작판과 최종 계약 검사판에서 240 항목 및 222 의존 핀이 같았다. [범위와 착수 차이](SCOPE.md)
- 의존 `fe41449d156eb5e723c254a0530863468c084480`. AF-RES-222의 중앙 DONE과 자체 PARTIAL를 유지한다. 222의 36방향은 정적 예상이다. [선행 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/fe41449d156eb5e723c254a0530863468c084480/docs/workstreams/research/AF-RES-222/HANDOFF.md)
- **고정 결과 SHA `cfabee892503403b3900f9100d3a141d08475a71`.** 이 SHA의 [결과](https://github.com/laadkke-arch/agentflow-open/blob/cfabee892503403b3900f9100d3a141d08475a71/docs/workstreams/research/AF-RES-240/RESULT.md), [자기 점검](https://github.com/laadkke-arch/agentflow-open/blob/cfabee892503403b3900f9100d3a141d08475a71/docs/workstreams/research/AF-RES-240/SELF_CHECK.md)
- ① `6f5e021638b2a84373239d26a84decd23fa82f5c` 범위·예측·입력을 GitHub에 먼저 봉인. ② `43a7d9a62047b79062d70be7da45a120578a5161` 원장·고정 빌드·원영수증. ③ `f53a99ab85ed4d1fdc900b551655110b72a727f3` 필수 표와 주관측. ④ `11d5e186580c935640e214cac2a921e3176b67c3` 반례·정정. ⑤ `cfabee892503403b3900f9100d3a141d08475a71` RESULT·SELF_CHECK. ⑥ 이 파일 단독 커밋.

## 결과와 주요 근거

- CPython 3.13.0/UCD 15.1.0은 13/13 별칭을 찾고 역방향에서 다섯 공식 Name을 돌려준다. 000A는 `name`에서 `ValueError`, `name(cp, None)`에서 `None`이다. ICU4C 76.1/UCD 16.0의 ALIAS는 네 correction을 수용한다. UNICODE/EXTENDED는 공식 Name을 검색하고 다섯 Name을 표시한다. 000A의 EXTENDED는 `<control-000A>`다.
- ICU header의 `U_INVALID_CHAR_FOUND`(10)와 일반 miss의 실제 `U_ILLEGAL_CHAR_FOUND`(12)가 달랐다. 본 실험 80회와 반례 88회의 miss 모두 숫자 65535와 status 12를 함께 반환했다. 유효 `<noncharacter-FFFF>`는 EXTENDED에서 같은 숫자와 status 0이었다. CPython CJK·한글 알고리즘 이름의 소문자 실패와 ICU exact-capacity NUL 경고도 두 번 재생했다. [상수별 원값](errors.csv), [반례](COUNTEREXAMPLES.md)
- 시간대 두 Link에서는 입력 ID echo, CLDR canonical, IANA preferred가 실제로 서로 달라질 수 있었다. `Asia/Kolkata`의 ICU CLDR canonical은 `Asia/Calcutta`였다. 원래 입력과 반환 목적을 각각 남길 근거다. [시간대 로그](receipts/tz/icu-tz.stdout)
- 자료 62행, 직접 확인/재열람 성공 39, 실패 23, 산입 29 고유 저작 / 7 lineage. 분석 사례는 문자 6점과 시간대 Link 2쌍. UCD 원행 38/38 바이트 일치. 36 방향 중 적용 34, N/A 2, 본 실험 204/204(별칭 104 포함), 반례 182/182, 시간대 입력×조건 15/15, 본 실험·반례의 원값 회차 차이 0. [자료 원장](sources.jsonl), [바이트와 입력](inputs.csv), [방향과 키](directions.csv), [하위 호출](calls.csv), [환경 지문](environment.json)

## 고정 결과판 검증

새 GitHub checkout에서 ⑤를 detach해 검사했다. 흩어진 영수증을 파싱해 두 회차의 102키·36방향·136 오류/통제 행을 재생성하여 커밋된 표와 비교했다. Q1–Q7의 직접 근거·미확인, 반례, 첫 두 표, 마지막 세 약점, 로컬 파일/행 링크, probe/입력 해시를 확인했다. GitHub 비교는 시작판 대비 앞 5 / 뒤 0, 추가 183파일 모두 소유 경로 안이다. RESULT blob `9deef89cc96202ad2aa0ab9c4f99d7e820d70a23`, SELF_CHECK blob `2d87f695191079778ecba02cf8891e1d47c4929f`를 원격에서 다시 읽었다. [고정 결과 비교](https://github.com/laadkke-arch/agentflow-open/compare/64e139f16309e41e30f9ec634eabe17fef908bbd...cfabee892503403b3900f9100d3a141d08475a71)

| 명령·대상 | 실제 종료 및 범위 |
| --- | --- |
| `python -m workbench.session start af-res-240 --allow docs/workstreams/research/AF-RES-240/ --dependency work/research-af-res-222=fe41449d156eb5e723c254a0530863468c084480 --output docs/workstreams/research/AF-RES-240/session.json --fetch` | exit 0, 시작 통합·계약·의존 고정. [manifest](session.json), [start stdout](receipts/session-start.stdout) |
| `python -m workbench.session check docs/workstreams/research/AF-RES-240/session.json --fetch` | exit 0, 2026-11-24T23:24:57Z, `passed` / `remote_checked`, 검사 SHA ⑤, 통합 `7369707441e2eb70e84004ca6cb3bfeefc8b4061`, 계약 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`. manifest를 제외한 변경 경로 182, outside/unmerged/errors 각 0. |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit 0, 23:24:57–23:25:04 UTC, 검사 SHA ⑤, 시작·끝 clean. doctor, acceptance(공통 55 + lab 7/9, demo, export, Git bundle 복원), reference-audit discovery, 원본 smoke 통과. 기본 `check-all` 내부 단계는 exit 0 / `no_active_sessions`으로 실제 활성 세션 검사는 미실행이다. 소유 경로의 AF-RES-240은 위 개별 명령에서 검사했다. |
| `run.sh main/controls/tz` 및 no-backward 대조 | ④ 새 clone에서 11쌍 stdout/stderr 동일. ⑤에서도 23:26:49–23:26:51 UTC에 별도 깨끗한 checkout, `env -i`, 동일 지문의 빌드를 사용해 11쌍을 재생했고 각각 바이트 일치, exit 0. [④ 재생 원로그](receipts/replay/replay.stdout) |
| CPython `test_ucn` 및 ICU `/tsutil/cucdtst/TestCharNames` | 양쪽 exit 0. CPython 14 run/2 skip, ICU 한 하위 시험. 대상 시험만 실행했다. [상류 시험 영수증](receipts/build/) |

⑤ 검사 출력의 요약 영수증. stdout SHA-256은 개별 check `8789fd642289882c937d71857fe61eb08c5b18bb8c785b6cd645a33ce65ea180`, 공통 검사 `1acdb2676d5a2949f5a337178723545d0afa517b5628dae4b1c37a24d8bfc24c`, ⑤ 재생 `4c90f9f402f91ff9861cdb98861eed3e8f943e1cf4e862463a0142872953d091`. 개별·공통·⑤ 재생 stderr는 0바이트다.

```text
session: passed, remote_checked, outside_paths=[], unmerged_paths=[], errors=[]
cloud: passed, exit=0, source_start.clean=true, source_end.clean=true
cloud.sessions: status=not-executed, reason=no_active_sessions, count=0, freshness=not_checked
result replay: main python×2 ICU×2, controls python×2 ICU×2, timezone 3; all stdout/stderr exact
```

## 약점과 다음 첫 행동

1. 검토자는 이 인계의 부모 `cfabee892503403b3900f9100d3a141d08475a71`에서 [표 1](RESULT.md#표-1)과 `errors.csv`의 `Q6-synthetic-ffff` 및 `Q6-unknown`을 먼저 대조한다. miss와 성공의 값 65535를 각각 상태 12·0과 같이 읽는다. 정확 용량의 NUL 경고도 `Q6-exact-buffer`에서 확인한다.
2. 결과를 다른 배포판에 적용하기 전에 [environment.json](environment.json)의 빌드·data 지문을 새 결과와 비교하고 같은 main/controls를 다시 실행한다. 현재 범위는 단일 Linux 빌드/데이터 쌍이다. 원래 UCD 배포 파일 전체와 보존본의 byte identity, 여러 운영체제의 재빌드, 전체 제품 시험, 현지화된 시간대 표시의 실측은 미확인이다.
3. 색인 제안은 `AF-RES-240 / 동일 코드의 입력 alias·표시 Name·실패 상태 / 완료·독립 검토 대기 / RESULT.md / AF-RES-222 고정 의존` 한 행이다. 소비자의 버전·choice·방향·변경하지 않은 원문 문자열·상태를 lookup 관측에 함께 보존한다. IANA/CLDR의 사례도 입력·정규 ID·표시가 각각 어느 API를 탔는지 기록하는 비교로 연결할 수 있다.

재현에 필요한 정상 진입점과 입력. 체크아웃은 위 결과 SHA이며 Bash, C/C++ 컴파일러, Make, pkg-config, curl, Git 및 Linux의 zic(시간대만)를 사용했다.

```sh
af_owned="$PWD/docs/workstreams/research/AF-RES-240"
af_build=$(mktemp -d)
(
  cd "$af_build"
  bash "$af_owned/receipts/build/build-cpython.command.sh"
  bash "$af_owned/receipts/build/build-icu.command.sh" icu
)
af_python="$af_build/cpython-60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/python"
"$af_owned/run.sh" main "$af_python" "$af_build/icu-prefix" "$af_build/main"
"$af_owned/run.sh" controls "$af_python" "$af_build/icu-prefix" "$af_build/controls"
python -m workbench.session check "$af_owned/session.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

`run.sh`는 `inputs.csv` 또는 `controls.csv`를 읽는다. 시간대 빌드의 고정 소스·명령·입력 순서는 [zic 명령](receipts/tz/zic.command.sh)에 있다. 재현에서는 스크립트의 작업 디렉터리를 새 빌드 경로로 바꾸고 `environment.json`의 tzdb SHA 아카이브를 `sources/T05-archive`에 둔다. 두 TZif 트리에서 `run.sh tz "$af_python" "$af_build/icu-prefix" "$af_build/tz" "$af_build/tzbuild/with-backward"`와 `"$af_python" -I "$af_owned/probe.py" tz --tzdir "$af_build/tzbuild/no-backward"`를 실행한다.
