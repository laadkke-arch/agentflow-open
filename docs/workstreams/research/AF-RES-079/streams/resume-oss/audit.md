# AF-RES-079#2 · OSS·대조 재개 감사

**핵심 행동 결과는 재확인됐다.** 원장상 OSS 자연쌍은 4/4이고, 네 역사판의 200호출에서 만든 49대응이다. 이번 별도 도구 에이전트는 기존 격리 환경을 읽기 전용으로 사용하여 핵심 18호출을 다시 실행했다. 네 프로세스 모두 종료 0이며 새 설치는 하지 않았다. 18호출을 새 자연 사건이나 49대응 전수 독립 재실행으로 세지 않는다.

검토자는 `oss_controls_audit`, 검토 방식은 **비가림 감사**다. RESULT와 첫 관계를 이미 읽었으므로 기존 자연4·대조2 가림 재판독에 합치지 않으며 독립 일치율도 계산하지 않는다. 실행 시각·정확한 `-c` 입력·실행기·stdout·종료값은 [audit.json](audit.json)에 보존했다. 원문의 재열람과 실패한 재시도는 [reopens.jsonl](reopens.jsonl)에 따로 남겼고 독립 원저작 수 증가는 0이다.

## 실행·관계 판정 대조

| 사건 | 검증한 내용 | 수용 범위와 한계 |
| --- | --- | --- |
| O01 MAD | 1.4.1→1.5.0 옛 이름의 정상 결과 1.4826은 유지하고 경고가 추가된다. 새 이름 기본 결과는 1.0이며 역수 scale을 지정하면 1.4826이다. 빈 `(3,0)`, `axis=1`은 scalar NaN에서 shape `[3]` 배열로 변한다. | ④ 후속 관계와 정상 입력 adapter는 지지한다. 전체 기능을 ② 무조건 별칭으로 취급할 근거가 없다. 빈 입력·경고 정책은 별도다. |
| O02 적분/분포 이름 | 1.5.4와 1.6.0에서 고정 NumPy1.19.5의 정상 trapz 결과 4.5가 같고 1.6.0 trapezoid도 같다. 기존 20대응은 반환 표현 일치16·예외형 일치4다. | 같은 namespace의 명시적 별칭을 지지한다. `stats.trapezoid`는 수치 적분과 다른 분포 역할이다. 같은 모집 사건의 simps/cumtrapz는 별도 native 실행이 없음을 유지한다. |
| O03 KDTree 모드 | 기존 `query(k=None)`의 exact bound1.0은 구판 인덱스 `[0]`, 신판 `[0,1]`이다. bound1.1의 숫자는 같지만 index 원소는 np.int64에서 Python int로 달라진다. `query_ball_point`는 거리 없이 인덱스만 반환한다. | ④ mode→대체 메서드 관계이며 단순 교체 수용은 기각된다. 거리·경계·정렬·형 어댑터는 아직 미검증이다. |
| O04 label sum | 공급자 표본의 두 판 결과 `[4,0,5]`가 float64·shape `[3]`으로 같고 신판 sum_labels도 같다. 기존 10대응은 반환 표현 일치6·예외형 일치4다. | 실행한 요구 범위의 ② 별칭을 지지한다. 반환의 직렬화 표현 일치이며 모든 Python 객체 성질의 동등성은 아니다. |
| C01 scikit-learn 이름 | 같은 발행자의 0.9 namespace 변경/forwarding 근거와 이후 제거판의 구분은 일관된다. | 계보·별칭 선언 수용. 0.8/0.9 load_iris·estimator의 양판 실행은 0쌍이므로 행동 수용을 확대하지 않는다. |
| C02 PIL/Pillow | 보존된 PIL1.1.7 archive를 다시 해시하고 descriptor 및 기존 영수증과 일치함을 확인했다. 원 selftest에 이미 `from PIL import Image`가 있다. | 같은 import 문자열을 배포물 동일성으로 취급하지 않는 ④ fork 관계는 타당하다. 원 PIL은 실행하지 않았고 PGP 신뢰도 검증하지 않았다. 현재 Pillow fixture만으로 역사 호환성을 승인할 수 없다. |
| C03 imp | 현재 live 문서가 제거 stub이며 원 find_module 절은 3.11 문서에 남아 있음을 공식 문서에서 재확인했다. 원 계약의 tuple/ImportError와 대체 경로의 ModuleSpec/None은 다른 계약이다. | 옛 API·인용은 ① 보존하고 개별 대체 API를 ④ 연결한다. 역사 3.11/3.12 동일 입력 실행은 여전히 0쌍이다. |

O01 [구판 문서](https://docs.scipy.org/doc/scipy-1.4.1/reference/generated/scipy.stats.median_absolute_deviation.html)와 [신판 문서](https://docs.scipy.org/doc/scipy-1.5.0/reference/generated/scipy.stats.median_abs_deviation.html)의 scale 계약, [KDTree PR12382](https://github.com/scipy/scipy/pull/12382)의 compatibility layer 선언, [Python3.12 이관표](https://docs.python.org/3.12/whatsnew/3.12.html#imp), [3.11 find_module](https://docs.python.org/3.11/library/imp.html#imp.find_module), [현재 imp stub](https://docs.python.org/3/library/imp.html)을 직접 재열람했다. 재열람 본문과 HTTP 상태 측정은 구별한다. 이번 web reader의 성공을 새로운 HTTP200 영수증으로 사용하지 않았다.

## 바로잡을 문서 연결 2건

1. `streams/oss/OSS_NOTES.md`는 이전 체크포인트다. 아직 native0/4, exact-radius 미확인, 설치·실행 명령 미실행이라고 적혀 있다. 원문을 보존하면서 맨 앞에 후속 [49대응 영수증](../oss/historical/paired-check.receipt.json)이 갱신한 범위를 안내해야 한다. 현재 RESULT와 relations의 수치는 후속 근거를 정확히 사용한다.
2. `relations.csv`의 C01–C03 공통 `behavior_acceptance` 문구에 “later historical paired execution”이 들어 있다. 대조의 양판 native는 실제0/3이다. “역사 양판 미실행; 원 선언/정적 근거와 별도 표시한 현재 보조 실행만 사용”으로 바꾸면 오독이 줄어든다. 이 수정은 대조의 계보 관계를 기각하는 것이 아니다.

## 반례를 찾아 확인한 경계

PR12382는 KDTree와 cKDTree 간 default leafsize 차이를 기술한다. 이번에 실행한 public KDTree는 1.5.4와 1.6.0 **모두10**이었다. 이 PR의 차이를 전후 출시판의 기본값 변화로 확대하면 안 된다. 기존 RESULT는 그렇게 확대하지 않는다.

기존 serializer는 tuple/list 바깥 컨테이너를 모두 JSON 배열로 바꾸고, np.scalar는 dtype 태그를 남긴다. 따라서 원장 명칭처럼 “기록한 값·shape·dtype·직렬화 표현”의 일치만 주장할 수 있다. O03의 인덱스 scalar형 차이는 원장에도 보존되어 있으며 재실행에서도 확인됐다. 예외 전에 발생한 경고가 원 probe에서 누락되는 제한도 기존 paired receipt가 정확히 밝히고 있다.

원 저자 답변의 Image-SIG URL은 이번 web reader에서 접근 실패했다. 이를 내용 부재로 판정하지 않았으며 기존 원문 열람 기록을 그대로 보존한다. PIL archive 재확인은 과거 런타임 재현이나 원저자의 포크 병합 동의 증거로 확대하지 않는다.

## 최종 분모와 인계

- OSS 자연 전후 원문 4/4, 역사 native 사건쌍 4/4. 상세 비교 O01 13·O02 20·O03 6·O04 10 = 49. 정확히 기록된 입력 payload 일치46, 명시적 파라미터 매핑3이다.
- 이번 재개 검증은 기존 네 환경에서18호출과 leafsize 속성2개를 추가 관측했다. 실행한 subset은 원장의 핵심 차이·불변 결과와 일치한다. 전체49대응 재실행을 주장하지 않는다.
- 대조의 전후 선언·원문3/3, 역사 native0/3. 현재 Pillow/Python 관측은 그 분자를 늘리지 않는다.
- 해시 검사: 네 원 로그 모두 각각50행·기록된 결과 해시·동일 probe 해시·명시 환경과 일치했다. archive 해시도 재확인했다.

부모 편집자는 위 문서 연결2건을 반영한 뒤 이 검토를 최종 수용 기록에 인용할 수 있다. 실제 소비자 계약에 필요한 추가 입력, O02의 미실행 개별 alias, C01/C02 역사 실행을 필요한 경우에만 후속 조사한다. 이번 감사는 전체 제품·모든 판의 호환성 보증이 아니다.
