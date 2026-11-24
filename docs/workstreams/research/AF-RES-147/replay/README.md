# AF-RES-147 재생 절차

Python 3.12, Python의 SQLite, POSIX 환경의 make·cc·GNU date, 공개 GitHub HTTPS를 사용한다. 소스 아카이브·빌드 디렉터리·SQLite 파일은 scratch에 두었다. 실행에는 pip 설치가 필요 없다.

```sh
set -eu
task=docs/workstreams/research/AF-RES-147
scratch=$(mktemp -d /tmp/af147-replay.XXXXXX)
python -B "$task/replay/prepare.py" --scratch "$scratch/upstream" --fetch --receipt "$scratch/preparation.json"
python -B "$task/replay/oracle_build.py" --scratch "$scratch/upstream" --output "$scratch/oracle.csv" --extras "$scratch/extra.json"
cmp "$task/oracle.csv" "$scratch/oracle.csv"
cmp "$task/evidence/origin-comparisons.json" "$scratch/extra.json"
python -B "$task/replay/run.py" --prepared "$scratch/upstream/prepared" --scratch "$scratch/sqlite-A" --output "$scratch/raw-A.json"
python -B "$task/replay/run.py" --prepared "$scratch/upstream/prepared" --scratch "$scratch/sqlite-B" --output "$scratch/raw-B.json"
python -B "$task/replay/score.py" --first "$scratch/raw-A.json" --second "$scratch/raw-B.json" --output "$scratch/result"
cmp "$task/answers.csv" "$scratch/result/answers.csv"
cmp "$task/ablation.csv" "$scratch/result/ablation.csv"
cmp "$task/evidence/transitions.jsonl" "$scratch/result/evidence/transitions.jsonl"
```

준비 명령은 각 원본 SHA-256과 추출 파일 SHA-256을 [취득 영수증](../evidence/artifacts.json)에 대조한다. 새 다운로드 없이 재생하려면 동일 바이트의 파일을 `upstream/downloads/{family}-{edition}.tar.gz`에 넣고 `--fetch`를 생략한다. 준비 출력 디렉터리는 비어 있어야 한다. `--initialize-digests`는 최초 관측 때만 사용했다. 변동 HTTP 응답 헤더, 처리 시간과 zic 빌드 바이너리 지문은 환경별로 재확인할 항목이다.

`oracle_build.py`는 정답 판독 경로다. tzdb 공급자 zic과 GNU date를 사용하고, CLDR는 판별 XML에서 수동 확인한 상속 계단을 minidom으로 읽는다. `run.py`는 TZif를 Python `ZoneInfo.from_file`로 읽고 ElementTree로 판별 LDML 부모를 계산한다. `run.py`는 정답 CSV나 평가기 없이 실행한다. `score.py`는 실행이 끝난 후 입력 계약과 정답 CSV로 채점한다. 경로 계약에서 한정한 기호를 포맷하는 소형 실행기이며, 임의 LDML·불완전한 locale 파일 트리·전체 숫자 포맷을 평가한 실험이 아니다.

사건 원장의 publish는 정책이 새 판을 아는 시점을 제공하는 고정 피드다. at는 UTC 날짜가 아닌 가상 틱이다. 시각 경과가 있는 실측 지연과 혼동하지 않는다. first는 빈 DB, retained는 앞 실행의 DB에서 동일 요청·전달 ID로 재생한다. 보존 DB의 카탈로그 조회에서는 이미 관측된 링크가 표시된다. 똑같은 요청의 재시도와 순서가 바뀐 이벤트는 각자 사건 ID가 있다. 원문 경로에서 읽은 바이트는 애플리케이션이 읽은 분량이다. 파일 시스템 페이지 캐시까지 비우는 시험은 하지 않았다.

A는 정확판을 직접 재취득해 안전하게 답한다. `A-url`은 URL의 마지막 결과를 사용하는 별도 구성 대조다. B와 C는 범위가 맞는 관측을 재사용하고 C는 호환된 요청 결과도 돌려준다. 수신 시기·판·키·출처 위치·현재 적합성·과거 실제 전달 여부를 함께 보고한다. 과거 답 복원은 보유 필드에 따라 보류할 수 있다. `wrong_hold`는 평가 기준상 답할 수 있는 사실 또는 실제 발생한 전달을 이 모형이 충족하지 못했음을 뜻한다. `warranted_hold`는 평가 결과도 보류이며 `hold_reason_mismatch`가 있으면 말한 이유만 다르다. 복원 비교는 정답과의 일치와 실제 이전 출력 보존을 별도 열로 둔다. 출처 비교의 누락·불일치도 별도 계수한다.

마스크는 C의 한 컬럼을 저장하지 않고 해당 인덱스 조건을 사용하지 않는 단계적 가설이다. `input_key`를 가려도 입력 본문은 남는다. 재사용 시 입력 본문을 다시 확인하는 안을 같은 마스크의 결과로 간주하지 않는다. 출처를 기준으로 복원하는 대체 방법은 관측 정합성과 호출자가 원 입력·컷오프를 제공하는지에 달려 있다. 마스크가 가리는 값을 사건 ID나 아카이브 URL에서 역산하지 않는다.

`costs.csv`의 logical bytes는 테이블 내부 행을 한 줄의 정규 JSON 튜플로 직렬화한 합이다. SQLite 페이지 수·파일 바이트, 실제 provider의 파일 open 횟수·로컬 읽기 B, 취득 시도와 SQL SELECT, SQLite 변경 건수, 등록·조회 경과를 따로 둔다. 준비 단계의 HTTP 응답 본문 바이트는 순수 HTTP 바디만 계측했다. TLS 오버헤드, 런타임 인터넷 전송, 사람 대기·처리 비용은 미측정이다. 판을 알려주는 외부 피드의 비용은 바깥에 있다. 두 실행의 공통 관측·오류·바이트를 지문으로 대조한다. 경과값과 다른 환경의 SQLite 페이지 결과는 다시 측정한다.
