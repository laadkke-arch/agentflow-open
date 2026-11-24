# 원시 스냅샷 판독과 조인 검산

- 과제에 대응할 CSV의 목록과 바이너리 지문은 [ACQUISITION](ACQUISITION.md)에 있다. [선정판 e2131c14](https://github.com/laadkke-arch/agentflow-open/blob/e2131c1447d9fe541aad5cd9bc61492b9ed5ec15/docs/workstreams/research/AF-RES-157/selection.csv)를 원격에서 다시 읽고 blob `b1987f703854c97c7b8f5838633ddb0db825ee2f`를 대조한 뒤 실제 스냅샷 구조를 해석했다. 파일럿 CSV 논리 행은 헤더 다음을 1로 센다.
- [전수 구조](pilot-metadata.json)에서 196개 사건 후보 ID가 모두 다르다. 참가자×완료 참조 57개 중 26개에 여러 행. 참가자×상대 레이블 145조합 중 42개 반복, 최다 5행. 상대 여러 명으로 연결된 참가자 키 26개와 참가자가 여러 명인 상대 레이블 38개. 상대·완료 참조 교집합 0. 참가자 숫자 키 교집합 48과 양쪽에만 있는 9/18은 문자열 집합 검사다. 과제나 제작자 관계를 인증하지 않는다. 타임스탬프 숫자 동률 0, 원 CSV 행 순서 감소 86개는 동종 열의 위치 감소다. 세 사건의 동률·역순·고아 값은 해당 사건 열 부재로 미확인이다.
- [전수 내용 검사](pilot-snapshots.json)에서 두 스케치 역할 각 196개의 배열 판독, 상대 예시 빈 배열 0, 완료 빈 배열 2. 완료 참조 57개마다 단일 직렬화, 추가 참조 행 139개이고 내용이 동일하다. 같은 그림 배열이 열 사이에서 일치한 62행에 두 참조 ID·레이블은 다르다. 별개 작품의 동일 그림, 공용 예시 복제, 파이프라인 재사용, 태그 의미가 달랐을 가능성을 남긴다. 완료 저장을 여러 번 한 사건으로 세면 같은 자료를 과대계수한다. 예시 참조 100개 중 39개가 여러 상대 레이블과 결합해 해당 열을 원작자 외래키로 단정하기 어렵다.
- [pairs.csv](../pairs.csv)의 24개 계획 자리와 진단 4개는 봉인 자료다. Fig.7 등 저자 선정 6행을 별도 덧붙였다. 공개 배열에 들어 있던 상대와 완료 스케치 획의 다름, 사람이 같은 작업에서 실제 변경한 결정, 동일 그림 재저장의 확인은 세 판정이다. 사람의 엄격 사건 조인 결과 0, 관측 무변경은 미확인. 수집 코드에는 편집 동작과 일반 사건이 모두 snapshot을 저장하는 경로가 있어, 저장 증명은 event kind를 좁힌 뒤 판단한다.
- [strict_join.py](../replay/strict_join.py)는 사용자가 검증한 동일 시계의 정상화 사건만 입력으로 받는다. 연구 원자료의 필드를 추정하여 변환하지 않는다. [인공 입력](../replay/synthetic.csv) 27행의 이중 저장, 무변경, 동시각, 다른 과제, 다중 자극, 사후 저장 없음, 렌더뿐, 문서 키 충돌 및 고아를 [예상 결과](../replay/synthetic-expected.json)와 대조했다. 인공 적격 2쌍 중 1 변화·1 무변경, 봉인 첫 네 자리에서 동률·결측을 유지. [간격 2tick과 다중 자극 허용의 동시 변화](synthetic-sensitivity.json)는 연산 검산이며 사람 결과와 무관하다.

## 실행 영수증

- 입력 코드 상태는 ② `e2131c1447d9fe541aad5cd9bc61492b9ed5ec15`의 선정판 뒤 ③ 로컬 작성 상태다. UTC 2026-11-24T17:08:32Z, Python 3.12.14, Linux. 아래 명령 각각 종료 0. 인공 입력의 기대 JSON은 손계산으로 작성했다. 출력 증거는 Git에 저장되어 경로별 지문을 재검사할 수 있다.
- 데이터 입력 SHA-256 `aec34f174ac350448b62a2223a859303ae496f99ba526775e027e914a4a1afbc`. [synthetic.csv](../replay/synthetic.csv)는 별도 입력이고 임의 문자·시간을 사용한다.
- 실제 실험의 DB와 Cambridge/OSF에는 실행하지 않았다. 정렬 전후 대표 자리는 같은 연구 공개판 안에서만 번호를 공유한다.

```sh
P=docs/workstreams/research/AF-RES-157
python -B "$P/replay/observed.py" /tmp/af-res-157/a03/pilot.csv
python -B "$P/replay/observed.py" /tmp/af-res-157/a03/pilot.csv --events
python -B "$P/replay/strict_join.py" "$P/replay/synthetic.csv" --expected "$P/replay/synthetic-expected.json"
python -B "$P/replay/strict_join.py" "$P/replay/synthetic.csv" --gap 2 --include-multi-stimulus
```
