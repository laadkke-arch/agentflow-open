# 고정 결과판 검사 영수증

대상 `ae8b00dad97ba242d7f274a539964cc66c1f1070`. GitHub에서 새 clone을 만들고 이 commit으로 detach했다. 로컬 checkout과 [원격 RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ae8b00dad97ba242d7f274a539964cc66c1f1070/docs/workstreams/research/AF-RES-137/RESULT.md)의 바이트를 대조했다. 독립 checkout의 검사 전후 porcelain이 비어 있었다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-137/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-137/replay/verify_report.py docs/workstreams/research/AF-RES-137
```

| 명령 | 종료값 | stdout·stderr · 범위 |
|---|---:|---|
| workbench.session check --fetch | 0 | [stdout 원문](workbench-check.json), stderr 0 bytes. checked_out_commit은 위 고정 SHA. 34 changed_paths 전부 owned, outside_paths 0, unmerged_paths 0, errors 0. |
| verify_report.py | 0 | [stdout 원문](reaggregation.json), stderr 비어 있음. 64 coverage행, 서로 다른 두 page size 증거의 80 sequences, 61 events, 25 compatibility행, 8 release행, 7 correction행, 37 고유 집계 원전. |
| 18개 archive 확정판 재회수 | 0 | 첫 clean 시도에서 네 기록 뒤 HTTP 503 종료 1. 같은 명령을 깨끗한 입력 경로에서 다시 실행해 18개 파일 해시, wheel 메타, 최초 업로드 시각 모두 일치. 코드는 최종판과 동일. |
| sparse-before, sparse, image, image 이전 공급판 | 각각 0 | [깨끗한 재실행 대조](rerun-comparison.json). 고정 수치 입력과 gallery source SHA 동일. sparse 출력 두 개와 이전 공급판을 쓰는 3×3 축은 JSON 바이트 일치, 새 공급판의 8개 3×3 고정 변형도 동일. 원본 gallery 512×512 모양·최대 1.0·동일 post-noise 입력의 반복을 확인. |
| SciPy 1.10.1, Python 3.12.14 | 1 | `python -m pip install --dry-run --no-cache-dir --disable-pip-version-check --only-binary=:all: --no-deps 'scipy==1.10.1'`. stderr `No matching distribution found for scipy==1.10.1`. 소비자 옛 MinCI가 이 버전에서 통과한다는 근거로 쓰지 않았다. |

원본 gallery에는 `default_rng()` 호출에 seed가 없다. 처음 전체 JSON의 바이트 동일성을 검사하자 원본 합계 행만 달랐다. 이 관측으로 실행 설명과 집계의 원본/고정 입력 경계를 수정했다. 각 원본 run에서는 한 번 생성된 배열을 두 차례 RL에 주어 같은 출력을 확인했다. 최신 독립 예제의 source SHA 및 전후 stdout은 [비교 JSON](rerun-comparison.json)에 있다. 고정 입력의 결과와 RNG가 바꾸는 원본 실사례 합계는 각각 다른 비교다.

Git 계약 확인은 업무 내용 전체의 진실성이나 다른 세션의 독립 검토를 확인하지 않는다. 위 명령은 검사판에 해당하며 후속 영수증·인계 문서와 구분한다.
