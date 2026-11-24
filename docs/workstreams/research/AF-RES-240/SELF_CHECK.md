# AF-RES-240 자기 점검

자체 검토를 수행했다. 별도 검토자나 독립 세션의 검토는 미실시다. 상류 회귀시험·깨끗한 checkout 재생·Git 계약 검사는 각각 별도 절차다.

| 질문 | 점검한 직접 근거 | 반증 시도 | 예정 / 관측 / 결측 및 범위 |
| --- | --- | --- | --- |
| Q1 라이브러리·data 판 | [environment](environment.json), I01/I07/I08, P01/P02/P06, [ldd](receipts/main/ldd.stdout), [data 확인](receipts/build/data-check.stdout) | 시스템 Python 3.13.5가 같은 UCD였으므로 patch 숫자까지 비교. 시스템 ICU가 섞이지 않도록 prefix·hash·data 버전을 대조 | 대상 2 / 2 / 0. 원 python.org archive 접근 실패를 고정 Git 소스판으로 대체. OS/서명/재빌드 byte identity는 미확인 |
| Q2 표본 바이트 | R01, U01–U05, [inputs.csv](inputs.csv), [38행](receipts/build/ucd-compare.stdout) | FE18의 `BRAKCET`와 `BRACKET`를 각각 보존. 000A placeholder·legacy·formal alias 분리 | 표본×판 38 / 38 / 0. 13 alias 전개. 원배포 파일 전체 바이트 미대조 |
| Q3 CPython 방향 | P02–P05, [원로그 1](receipts/main/python-1.stdout), [원로그 2](receipts/main/python-2.stdout), [test_ucn](receipts/build/python-test_ucn.stdout) | 검색이 되는 000A에 Name 부재. 2118/FE18의 이름과 별칭이 서로 다름 | 호출 60 / 60 / 0. 18방향 중 old 없는 1 N/A. 전 UCD/legacy 객체는 범위 밖 |
| Q4 ICU choice·오류 | I02/I03/I06/I08, [원로그 1](receipts/main/icu-1.stdout), [원로그 2](receipts/main/icu-2.stdout) | 동일 old/alias 입력에 세 choice 분리, status 0의 빈 Name과 합성 label 확인 | 호출 144 / 144 / 0. 18방향 중 old 없는 1 N/A. 데이터 로딩 실패·기존 오류 상태는 미측정 |
| Q5 예상과 실측 | R02, I02–I06/I09, [errors.csv](errors.csv), [상류 시험](receipts/build/icu-TestCharNames.receipt) | 헤더 문구와 구현을 따로 예측 처리, 숫자·상수 비교. 버퍼 1/23의 NUL 경계 재생 | 본 실험 miss 80/80에서 65535/12, 구현 예상 102키/102키, 반복 원값 불일치 0. 헤더 10과의 차이 40키. ICU 다른 판은 미확인 |
| Q6 음성·경계 | U01/U03/U05, P03, I02–I04/I09, [controls.csv](controls.csv), [반례](COUNTEREXAMPLES.md) | case/space/one-letter/legacy/unknown/valid 0xFFFF와 크기 경계를 각각 변경 | 호출 182 / 182 / 0, 91키 차이 0, 유효 FFFF 성공 2 및 FFFF 반환 실패도 관측. 전체 abbreviation 단문 0은 두 고정 파일 조건 |
| Q7 시간대 | T01–T09, [IANA 빌드](receipts/tz/zic.stdout), [ICU API](receipts/tz/icu-tz.stdout), [ZoneInfo 원값](receipts/tz/python-tz.stdout) | Kolkata 대조로 IANA/CLDR 출력 분리. Link 제거 대조 및 미등록 키, `Etc/Unknown` fallback | 입력×조건 15 / 15 / 0, Link 독립쌍 2. 시각 계산·다국어 표시 미측정 |

- [sources.jsonl](sources.jsonl) 62행은 서로 다른 source_id를 갖는다. 직접 확인 37행 및 판 불일치/재열람 2행, 접근 실패 23행이다. 성공행 work_id 35개 중 고유 산입 29개(UCD/정책 6, CPython 5, ICU 8, 222 2, 시간대 8), lineage 7개다. 같은 UCD 파일의 다른 버전과 빌드된 데이터는 중복으로 세지 않았다. 최초 열람 시각을 되살릴 수 없는 문헌의 UTC는 시간창이다.
- [directions.csv](directions.csv) 36자리 = 관측 34 + 범위 밖 N/A 2. 102키 각각에 예정된 호출 2회 모두 연결됐다. 전체 204 / 204 / 0, 별칭 104 / 104 / 0. [errors.csv](errors.csv) 136행 = 본 실험 오류·부재 45 + 반례 91. 상태 0의 빈 문자열을 누락으로 집계하지 않았다.
- [깨끗한 재생](receipts/replay/replay.stdout)에서 GitHub ④ 커밋의 별도 clone, 비어 있는 실행 환경, 동일 지문의 두 빌드를 사용했다. 본 실험 네 프로세스·반례 네 프로세스·시간대 세 프로세스의 stdout와 stderr가 각각 바이트 일치. ⑤ 결과 SHA 확인과 계약 검사 결과는 마지막 인계에서 식별한다.
- 상류 CPython `test_ucn`은 14개 run/2 skip, ICU는 `/tsutil/cucdtst/TestCharNames`만 통과했다. ICU 필터 앞 `/`를 빠뜨렸던 최초 실행은 CLI exit 1이고 다시 실행한 대상 시험 exit 0이다. 시간대 `zic` 준비에서도 clean 환경의 Git DNS 및 PATH 적용 오류를 고친 뒤 실제 출력(exit 0)을 보존했다. 두 제품의 전체 suite는 미실시다.
- [RESULT.md](RESULT.md)의 첫 두 표·Q1–Q7·비용/대안·마지막 세 약점 표, [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md), 원로그와 예측의 연결을 대조했다. 핵심 runtime/오류 조건에 미달 없음. 미확인은 위 표와 각 Q에 표시했다.
