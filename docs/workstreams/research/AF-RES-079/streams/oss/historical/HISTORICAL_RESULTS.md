# OSS 역사판 native 실행 추가 결과

**2026-11-23 UTC에 네 역사판을 실제 설치·실행했고, 동일 입력에 대한 4/4 자연 사건의 양판 실행 근거를 확보했다.** 기존 `streams/oss/`의 안정화 파일은 수정하지 않았다. 따라서 기존 파일의 “역사판 native 0/4, 미실행”은 작성 당시 상태이고, 이 문서와 새 원기록이 아래 입력에 한해 그 상태를 갱신한다.

## 실행 환경과 실제 명령

`environment-discovery.json`에서 Python 3.8/3.9, Docker/Podman, Conda/Mamba가 없고 uv가 있음을 실제 확인했다. uv 0.13.9를 통해 이 `historical/` 디렉터리 아래 CPython 3.8.20을 설치했다. 전역 Python 설치와 기존 환경은 변경하지 않았다.

네 환경의 공통 조건은 **CPython 3.8.20, NumPy 1.19.5, 같은 Linux x86_64 호스트**다. SciPy 1.4.1, 1.5.0, 1.5.4, 1.6.0은 각각 `envs/scipy-<판>`에 설치했다. 공개 `https://pypi.org/simple`에서 wheel만 허용했고 소스 빌드는 하지 않았다. 환경·캐시·Python 배포물은 이 하위 디렉터리의 `.gitignore`에서 제외했다.

재현 진입점은 다음과 같다. 내부의 정확한 argv·시점·cwd·종료값은 각 `*.receipt.json`에 보존했다.

```bash
python -B docs/workstreams/research/AF-RES-079/streams/oss/historical/run_recorded.py --label install-python38 --timeout 150 -- uv python install 3.8 --no-bin --system-certs --no-config
python -B docs/workstreams/research/AF-RES-079/streams/oss/historical/install_and_probe.py
python -B docs/workstreams/research/AF-RES-079/streams/oss/historical/compare_pairs.py
```

첫 wheel 명령은 `--only-binary=:all:`와 `--no-build`를 함께 주어 CLI 옵션 충돌로 종료 **2**였다. 이를 설치나 제품 동작 실패로 세지 않았다. 첫 실패 로그·명령은 `*-wheels-attempt1.*`에 보존했고, 같은 wheel-only 제한을 주는 `--only-binary=:all:`만 남긴 재시도는 네 환경 모두 종료 **0**이었다.

실제 설치·probe 완료 시각은 **2026-11-23T11:49:48.886249Z**, 결합 검사 완료 시각은 **2026-11-23T11:51:13.679566Z**다. 설치·freeze·probe 프로세스는 모두 종료 **0**이다. 이는 모든 호출이 값을 반환했다는 뜻이 아니다. probe는 예상된 오류도 관측 결과로 저장한다.

## 분모와 결합 방법

| 단위 | 분자 / 분모 또는 건수 | 의미 |
|---|---:|---|
| 역사판 설치·실행 | 4 / 4 판 | 1.4.1, 1.5.0, 1.5.4, 1.6.0 |
| 자연 사건 양판 native 근거 | 4 / 4 사건 | 사건 수를 추가하지 않음 |
| 원 호출 기록 | 200행 | 판마다 같은 probe의 50호출 |
| 명시한 구/신 API 대응 비교 | 49행 | P1/P2가 같은 원 호출을 재사용하므로 독립 사건 49개가 아님 |
| 기록 입력의 SHA-256이 정확히 같은 대응 | 46 / 49 비교 | 숫자 입력·shape·dtype·인자 기록을 정렬 JSON으로 해시 |
| 명시적 인자 대응이 있는 비교 | 3 / 49 비교 | MAD scale 어댑터 1행, KDTree radius 대응 2행 |
| 독립 외부 원저작 추가 산입 | 0 | 실행 자료와 연구자 구별 입력은 원저작 모집 수를 늘리지 않음 |

O01은 1.4.1→1.5.0, O02/O03/O04는 1.5.4→1.6.0을 비교했다. `paired-observations.jsonl`에는 이전/이후 row ID·파일·원 입력·양쪽 입력 해시·명시적 인자 대응·출력·오류·경고가 있다. `paired-summary.csv`는 같은 비교를 요약한다.

원 probe의 `historical_pair_claim=false`는 그대로 유지했다. 단일 실행 기록만으로 양판 비교가 완성됐다고 선언하지 않기 위한 표시다. 별도 결합 검사가 네 결과 파일의 판·NumPy·Python·50행·파일 해시·동일 probe 해시를 확인한 후 `paired-observations.jsonl`에서만 `native_pair_observed=true`를 기록했다.

값 비교와 형/형상 비교는 분리했다. 예를 들어 NumPy 정수 scalar를 JSON 숫자로만 평탄화하면 놓치는 형 변화는 원 직렬화의 `dtype` 표지로 별도 검출한다. 오류는 클래스와 메시지를 따로 비교했다. 경고 뒤에 예외가 난 경우 원 probe가 경고를 저장하지 못하므로 이 경우의 경고 일치 여부는 `null`이며 “경고 없음”으로 해석하지 않는다.

## O01: 정상 어댑터는 작동하지만 빈 배열 계약은 달라진다

근거 행: `O01-P1-normal`, `O01-P2-normal`, `O01-P2-normal-adapter`, `O01-P1-empty_2d`, `O01-P2-empty_2d`.

| 동일 데이터 / 요구 | 1.4.1 구 호출의 실제 결과 | 1.5.0 대응 호출의 실제 결과 | 확인한 차이 |
|---|---|---|---|
| `[1,3,2]`, P1 옛 이름 유지 | float64 1.4826 | float64 1.4826 + DeprecationWarning | 정상값·형은 유지, 경고는 추가 |
| `[1,3,2]`, P2 새 이름의 기본값 | float64 1.4826 | float64 1.0 | 이름만 교체하면 기본 동작 불일치 |
| 같은 데이터, P2 `scale=1/1.4826` | float64 1.4826 | float64 1.4826 | 명시적 scale 어댑터가 이 입력에서 복구 |
| 빈 `(3,0)`, `axis=1`, P1/P2 | scalar NaN | float64 shape `[3]`의 NaN 배열 | 구 이름 wrapper를 유지해도 반환 형상 변화 |

float32 입력과 공급자 axis 예에서도 P1은 값·직렬화 형을 유지하지만 기본값 P2는 달라졌다. 잘못된 axis는 양판 모두 AxisError, `nan_policy=raise`는 양판 모두 ValueError이며 메시지도 같았다. 정상 P1 수용과 무수정 P2 거절은 실제 실행으로 뒷받침된다. 그러나 빈 배열까지 포함한 전체 P1 동등성은 기각해야 한다. 관계 제안 ④는 유지된다.

## O02: 범위를 고정한 별칭은 실행에서도 일치했다

근거 행: `O02-P1/P2-normal`, `reverse`, `empty`, `singleton`, `float32`, `complex`, `axis`, `invalid_axis`, `mismatched_x`, `distribution_alias`.

`integrate.trapz`의 P1과 `integrate.trapezoid`의 P2는 고정 NumPy 1.19.5에서 정상·역순·빈 입력·단일 점·float32·complex·2D axis의 **값/형상/dtype 직렬화가 모두 같았다**. 잘못된 axis는 IndexError, 길이가 맞지 않는 x는 ValueError로 클래스와 메시지도 같았다. stats 분포의 옛/새 이름에 대한 공급자 입력도 같은 PDF 값을 반환했다. 총 20개 대응 중 16개는 같은 반환 표현이고 4개는 같은 오류다.

이 사건의 범위 있는 별칭 ②를 실행된 입력 범위에서 지지한다. 같은 명명 결정의 `simps→simpson`, `cumtrapz→cumulative_trapezoid`는 이 probe에 별도 실행이 없으므로 이 두 기능의 전체 동작까지 검증했다고 표현하면 안 된다. 현재 자료는 자연 사건의 대표 기능 trapz와 stats 분포 별칭을 실행한 것이다.

## O03: 보류했던 정확 반경 차이를 확인했고, 정상 입력의 형 변화도 찾았다

근거 행: `O03-P1-normal`, `O03-P1-exact_boundary`, `O03-P2-normal`, `O03-P2-exact_boundary`, `O03-P1/P2-complex_query`.

트리 점은 `[[0],[1],[2]]`, 질의점은 `[0]`이다.

| 요구 / 반경 | 1.5.4 `query(k=None)` | 1.6.0 대응 호출 | 결론 |
|---|---|---|---|
| P1, bound 1.1 | 거리 `[0,1]`, 인덱스 `[0,1]`; 인덱스 원소 `numpy.int64` | 같은 거리·인덱스 값; 인덱스 원소는 Python `int` | 값만 보면 같지만 형 계약까지 동일하지 않음 |
| P1, bound 1.0 | 거리 `[0]`, 인덱스 `[0]` | 거리 `[0,1]`, 인덱스 `[0,1]` | 구 strict 경계와 신 포함 경계의 실제 차이 |
| P2, radius 1.1 | 거리와 인덱스 두 목록 | `query_ball_point`는 인덱스 `[0,1]`만 반환 | 거리 정보 유실 확인 |
| P2, radius 1.0 | 거리 `[0]`, 인덱스 `[0]` | 인덱스 `[0,1]`만 반환 | 반환 계약과 경계가 함께 다름 |

complex 질의는 구/신 대응 모두 같은 TypeError와 메시지로 거절했다. 따라서 이 경계에 대한 오류 계약은 유지된다. 정상 P1을 “값만 유지”라는 좁은 범위로 말할 수는 있지만, 봉인 P1이 포함한 형과 경계까지 승인할 수는 없다. 기존 `O03-BOUNDARY-RADIUS`의 보류는 이 실행 입력에 한해 **차이 확인/동등성 기각**으로 갱신할 수 있다. 관계 ④와 거리·정렬 어댑터 필요성은 유지되며, 어댑터에는 구 strict 경계와 정수 형을 보존할지의 결정도 필요하다.

## O04: 공급자 정상·경계 입력과 오류 조건이 일치했다

근거 행: `O04-P1/P2-provider`, `float32`, `complex`, `wrong_shape`, `empty`.

공급자 입력 `input=[[1,2],[3,4]], labels=[[1,2],[2,4]], index=[4,8,2]`는 양판 및 신 이름에서 float64 shape `[3]`, 값 `[4,0,5]`였다. float32 입력과 빈 입력도 같은 값·표현이었다. complex 입력은 같은 TypeError, label shape 불일치는 같은 ValueError였고 메시지도 같았다. 총 10개 대응 중 6개 반환 표현이 같고 4개 오류가 같았다. 실행한 범위에서 P1/P2 결론은 불변이며 별칭 ②를 지지한다.

## 남는 한계와 다음 최소 확인

이 실행은 원문 예측을 실제 표본 동작으로 바꿨지만 모든 입력의 동등성을 증명하지는 않는다. 자연 모집 분모도 계속 OSS 4사건이다. 연구자가 구성한 구별 입력이나 두 질문의 반복 비교를 독립 자연 사건으로 추가하지 않는다.

가장 중요한 남은 항목은 O03의 거리·정렬·strict 경계·정수 형을 모두 명시한 어댑터를 만들고 그 어댑터가 구 계약을 복원하는지 확인하는 일이다. 현재 실행은 어댑터의 필요성을 보였고 어댑터 자체를 구현·검증한 것은 아니다. O01도 scale 정상값 복구를 보였지만 빈 배열 형상까지 보존하는 호환 wrapper는 별도 검사 대상이다. O02의 simps/cumtrapz는 구현 근거가 있으나 개별 실행 범위 밖이라는 제한을 유지한다.

두 판의 직접 실행, 비교 행, 명령·실패·종료값은 모두 이 디렉터리에 보존했다. 기존 안정화 원장을 자동으로 덮어쓰지 않았으므로 부모의 결과 통합에서 어느 보류가 어떤 행으로 바뀌는지 명시해야 한다.
