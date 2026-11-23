# 하위 조사 재현

## 실행한 범위

`audit_crossdomain.py`는 공개 파일4개를 고정 SHA256으로 확인하고 분석행 수·스키마·군별 합계·실제 키 연결을 계산한다. 개인별 행이나 ID 값은 결과 파일에 내보내지 않는다. 원 배정 대장이 없는 상태에서 배정표를 새로 만들거나 개념 점수에 통과선을 붙이지 않는다. 실제 실행 시각·종료코드0·라이브러리 버전은 `audit-crossdomain-receipt.json`, 최초 다운로드의 URL·상태·해시는 `postfreeze-fetch-receipts*.json`에 있다.

저장소 루트에서 실행했다.

```bash
python -B docs/workstreams/research/AF-RES-054/streams/crossdomain/audit_crossdomain.py
```

원문/비식별 원데이터 cache는 커밋하지 않는다. 다른 환경에서 재개할 때에는 아래 명령이 필요하다. `pandas`와 `pyreadstat`가 이미 설치되어 있다면 설치 명령은 생략할 수 있다. 모든 생성 경로는 이 하위 디렉터리 안이다.

```bash
python -B -c "from pathlib import Path; Path('docs/workstreams/research/AF-RES-054/streams/crossdomain/cache/tmp').mkdir(parents=True, exist_ok=True)"
TMPDIR="$PWD/docs/workstreams/research/AF-RES-054/streams/crossdomain/cache/tmp" python -m pip install --no-cache-dir --target docs/workstreams/research/AF-RES-054/streams/crossdomain/cache/deps pyreadstat narwhals pandas
python -B docs/workstreams/research/AF-RES-054/streams/crossdomain/audit_crossdomain.py --download
```

재개 입력은 `https://osf.io/download/mykxc/`의 SAV, `x9uge`, `fseb4`, `t895q`의 CSV다. 해시가 바뀌면 스크립트는 중단한다. 그때 새 판을 구판인 것처럼 사용하지 말고 file-version API와 원판을 먼저 확인한다.

## 연구 한 개의 손 검산: E01

SAV의 `Cond`는0=문제풀이/1=풀이 예제, `TimeP`는0=압박 없음/1=압박 있음이다. 네 셀 수는58,58,57,58이므로 `58+58+57+58=231`이다. 각 셀의 KPost 비결측 수가 같은58,58,57,58임을 `bichler-analysis-aggregate.json`에서 확인한다.

압박 없음의 예제군 KPost 평균은8.411754385964912, 문제풀이군은8.16051724137931이다. 이 둘을 해당57명·58명으로 가중하면 다음과 같다.

```text
(57 × 8.411754385964912 + 58 × 8.16051724137931) / 115
= 8.28504347826087
```

두 자리 반올림8.29는 읽은 54쪽 저자 원고의 AppendixB TableB1의 사후 점수를 재현한다. 이 계산은 **지식 점수의 평균**이며 성공률이 아니다. 같은 저자 원고의 TableB2의 문제풀이 사전4.75와 증가3.59는 `8.16-4.75=3.41`이어서 맞지 않는다. 공개 원행 평균으로는 `8.16051724137931-4.573275862068965=3.587241379310345`이며 증가 열과 일치한다. 각 원행에서도 세 열의 산술이 일치하는지 코드가 검사했다. 최종 출판본의 표는 별도로 열지 못했으므로 이를 최종 출판본의 확정 오류라고 부르지 않는다.

`q`는 원래 binary pass 기준이 없고 `t`는 제출시각/완료 상태가 없으므로 계산하지 않았다. `CL6.notna().sum()==83`은 인지부하 문항 응답 수이며 `t==83`의 검증이 아니다. 따라서 Frechet 극단 정수표의 입력을 이 연구에서 만들지 않았다.

## 반례 한 개의 손 검산: 분석행 완전성과 배정 완전성

Pillai E2의 본문은143명을 모집했다고 쓰고, 제외 사유를16명 미복귀·11명 컴퓨터 오류·3명 최소 참여시간 미달로 보고한다. `143-16-11-3=113`이나 분석 N과 실제 정확도 CSV는112명이다. 설명되지 않은1명의 처리를 임의 입력하지 않는다.

정확도 파일112행을 왼쪽에 두고 평정 파일112행을 `ID+Condition`으로 결합하면112행이며, 전략 파일114행 중 **모든 열이 빈2행**을 제거한112행과 결합해도112행이다. 이 두 파일의 ID 중복0·미연결0은 공개 분석 표본을 확인한다. `143-112=31`의 부재 참가자를0명으로 만들지 않으며, 그31명의 군별 분모·실패/결측 사유를 만들어 내지도 않는다. 사전계획은 시간 부족 참가자를 제외하므로112명의 정확도 평균으로143명의 기한 내 성공률을 주장하면 추정 대상이 달라진다.

추가로 전략 CSV의 빈2행을 탈락2명으로 세면 `114`를 사람 N으로 오인한다. 이 반례는 물리적 파일 행, 분석 사람, 원래 배정 사람을 구분해야 함을 보여준다.

## 실시하지 않은 것

- E01 원 배정 대장 왼쪽 결합, 원 이진 품질 통과·시각 교집합, 그 효과 구간: 필요한 원 자료/정의가 없어 **미실시**.
- Pillai143명 전체 배정 분모 복구와 기한 내 공동 결과: 대장·시각·원 통과 정의가 없어 **미실시**.
- CAD6명×질의×기간 자료 결합: 공개 원행 미확보와 코드 URL 로그인벽으로 **미실시**.
- 새 참여자 모집, 저자 연락, 가정으로 성공/실패 값을 보간하는 절차: **미실시**.
