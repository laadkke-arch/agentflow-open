# 반례·판정 정정 이력

이 파일의 전후는 판독 중 경쟁 해석을 기록한 것이지 새 관측이나 독립 평가 결과가 아니다. SCOPE의 원표 선택 규칙은 변경하지 않았다. source ledger, judgments.csv, conditions.csv, denominators.md의 고정 원행을 참조한다.

| 초기 가능한 해석 | 직접 반례 / 확인 | 최종 판정 및 철회 조건 |
|---|---|---|
| 높은 관련성은 추가 기능조건 보증 | J1 원 3,2 및 J2 원 3,3; stdlib json 기본 ensure_ascii=True; P03/P08. | 문자 자체 보존 N. 원질의에는 이 조건이 없으므로 원점수 오류 아님. 실제 실행 환경에서 ensure_ascii=False로 고정되거나 요구가 의미상 복원으로 바뀌면 재판정. |
| write_csvs라는 이름이면 CSV 생성 | C3 pandas read_csv → self.write → bcolz carray; 원 2,3. | CSV 출력 조건 NA, 결합 성공 아님. CSV 출력 경로가 같은 고정 함수에서 확인되면 재판정. |
| 낮은 점수는 어떤 필수조건도 지지하지 않음 | C2 1/3, R2 2/1; 각각 실제 writerow 및 readline. R3 0/1의 인접 run은 file iterator. | 낮은 개별 점수와 일부 조건 지지 공존. R3 selected default_line 자체는 NA; caller와 혼동 금지. |
| writerow만 있으면 모든 CSV 환경에서 보증 | C1 default ';'; C2 caller가 표준 writer를 구성하지만 주입 writer가 가능. | Y는 확인한 표준 writer·일치 dialect·문자열·원 caller 한정. newline/encoding/OS 차이와 실제 테스트 결과 미확인. 다른 dialect나 writer면 U/N. |
| readline 사용하면 전체 프로그램 메모리 일정 | R2 load_children은 파싱 객체 누적, f가 임의 객체일 수 있음. | 선택 helper의 파일줄 단위 처리만 Y, caller 전체 U. R1 splitlines와 join은 반례 N. |
| 평정 0과 평가되지 않음은 같음 | 원표 S1 0/1, S3 0/0; CU/JU/RU 동일 SHA/path 및 앵커 범위 미등재; TREC 19335+1017759=0 vs 19335+1200258 비등재. | 0은 원관측, unjudged는 원기록 부재; 정책적 zero-fill은 별도 분석, 원자료에 쓰지 않음. |
| 정렬 3개 접근 실패를 다음 URL로 대체 | SX4/SX5/SX6 원파일은 읽었으나 선행 3 URL이 봉인됨. | 별도 보강 원자료로만 산입, 12 주표와 보강 미판정 슬롯의 분모는 불변. 접근 실패를 부적합으로 간주하지 않음. |
| 논문 Table2 숫자를 CSV 원행 수로 사용 | 논문 4026 / Python 2089, 고정 CSV 4006 / Python 2079 (Java 역시 -10). | 판별 가능한 원표 분모 사용, 차이 원인 미확인. 더 정확한 원자료가 발견되면 버전별 원장 추가. |
| 복수 행을 다수결로 사람 합의라 부름 | S2,C2,R1,R2는 threshold 상충; ID 열 없음. | P/M/H 분리. 원평정 단위 84개를 사람 84명이라 하지 않음. 사람 ID가 있는 원평정 판본 확보 및 독립 검증 후만 agreement 추정. |

세 관점의 이견: (1) 검색 설계자는 graded relevance를 탐색 우선순위 신호로 쓸 수 있다. (2) 소비자는 명시 제약을 gate로 요구한다. (3) 코드 작성자는 자신의 환경/호출자에 국한한 기능을 제공한다. 충돌은 점수 하나로 덮지 않고 원평정과 조건 적용범위, 증거·U 및 채택 사건을 별도 보존한다.
