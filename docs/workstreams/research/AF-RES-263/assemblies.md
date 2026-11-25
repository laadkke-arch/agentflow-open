# 독립 결정 묶음과 9자리 제거 분석

이 문서는 선택지를 주는 설계 합성이다. 자료 제거는 논리적 ablation (실제 검색/실행/모델 성능 실험 아님). 제거는 아래 세 원자료 범주에서 해당 판단을 뒷받침하는 핵심 근거 하나를 보이지 않게 하는 것. 다른 원자료가 같은 결론을 독립 지지하면 낮은 강도로 유지하며, 제거 자료의 실측을 대신 만들지 않는다.

## 결정 묶음 세 개

- **P (보존)**: src/current type2, linkname note.txt, data 없음. 독립 추출 후 경로 읽기까지 목표라면 src/note.txt type0+B를 같은 archive에 추가한다. 보존자는 이름/링크 의미 보존, 앱은 B 읽기. F=S01/S02/T00, U=C01, T=T03/T01. 포기: current 자체에 B가 있는 단일 멤버 계약. 철회 조건: 소비자가 symlink를 만들 수 없거나 독립 regular가 필수. first https://github.com/libarchive/libarchive/issues/1034
- **D (내용 단독)**: src/current type0+B 하나만; 생성 시 target 읽기, archive 내부 의존 없음. 둘 다 넣는다면 GNU -h만으로 독립 payload 보장 금지; --hard-dereference나 독립 멤버 확인. F=S01/S02, U=C10, T=T09/T10. 포기: symlink 객체와 inode 관계. 철회 조건: 링크 의미 자체가 수신 목적/정책상 필수. first https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html
- **P+D (두 배포물)**: preserve.tar는 P의 target 동봉; standalone.tar는 D. 공통 snapshot B 해시/판과 두 acceptance, 각각 다른 추출 루트. 같은 archive에서 보조 이름 current.copy로 분리하는 변형은 이름 계약을 바꿈. F=S02/S04, U=C01+C10, T=T03+T09/T10. 추가 비용은 배포·판 일치 확인과 선택 UI, bytes/시간의 실측 수치 없음. 철회 조건: 단일 파일/단일 산출물 제약이 실제 고정이거나 두 수신군이 없음. first https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5

## 제거 행렬

| 조합·버린 근거 | 유지할 주장 | 다시 열 결정 | 바꾼 계약·대가 | 회복할 첫 URL |
|---|---|---|---|---|
| P - S02(형식) | C01 요청, T03 추출 기대 | typeflag/linkname/size 규범 문장을 보류 | 일단 링크 객체+대상이라는 목표만; 형식 검증 추가 | https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5 |
| P - C01(요구) | S02 타입 구분, T03 기대 | 실제 보존자가 이 선택을 원한다는 근거 회복 | 선택지로만 남기고 기본값 결정 보류 | https://github.com/libarchive/libarchive/issues/1034 |
| P - T03(시험) | S01/S02 규칙, C01 요구 | 동일 판에서 링크+대상 추출·내용 읽기 기대 약화; 실험 필요 | 새 루트에서 readlink/open 비교 | https://github.com/libarchive/libarchive/blob/d114ceee6de08a7a60ff1209492ba38bf9436f79/tar/test/test_basic.c |
| D - S01(형식/옵션) | C10 실제 목표, T09 역참조+hardlink 기대 | --hard-dereference 정확 옵션·규격 문장 보류 | data-only acceptance 유지, CLI 채택 보류 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/doc/tar.texi |
| D - C10(요구) | S01, T09/T10 가능성과 함정 | 실제 배포자가 링크를 전혀 원치 않는다는 판단; C02는 별도 수신 사례로 유지 | regular-only 선택지 유지, 목적 우선순위 미결 | https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html |
| D - T09(시험) | C10 당사자 보고, S01 옵션, T10 다른 도구 기대 | 같은 GNU 소스의 -h dedup 회귀 기대; 동판 재검사 | 독립 payload 검사 필요, 다른 도구 테스트를 대신 쓰지 않음 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at |
| P+D - S02(형식) | C01+C10 다른 목적, T03+T09 기대 | 동일 멤버 강한 충돌의 규격 근거; S04 정책만으로 대체 금지 | 두 산출물의 개념적 대안, 형식 채택 보류 | https://man.freebsd.org/cgi/man.cgi?query=tar&sektion=5 |
| P+D - C10(요구) | 보존 요구 C01와 타입 차이, C02/C13 별도 배포 사례 | 두 번째 배포물 실제 원소비자 요구/수신 비용 | P 유지, D는 옵션; 불필요한 이중 생성 피함 | https://www.mail-archive.com/bug-automake@gnu.org/msg04198.html |
| P+D - T09(시험) | 서로 다른 요구, 형식 경계, T03 | standalone의 GNU -h 단독 사용 가능성 및 두 산출물 동일 B 검증 | P/D 검수 분리; D를 type0 검사 전 발행 금지 | https://github.com/gnu-mirror-unofficial/tar/blob/de72aa0cd63a6bb5d206227a609ff113e5b26171/tests/link04.at |

9/9 예정 행 작성, 실험 관측 0, 정상 공석 0, 재실행 결과 미확인 9. 다른 근거의 개별 판과 위치는 sources.jsonl. 구분: F 형식 근거가 빠져도 목적 차이는 사라지지 않으며, U가 빠져도 기술 가능성은 유지, T가 빠져도 규칙은 유지하되 실제 도구 동작 예측의 신뢰를 낮춘다. 이중 배포가 최적이라는 추천은 아님.
