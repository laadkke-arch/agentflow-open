# 반례와 원값

## 문자 이름

반례 입력 23행은 [controls.csv](controls.csv)에 먼저 고정했다. CPython 22키와 ICU 69키를 두 프로세스씩 실행했다. 예정 182 / 관측 182 / 결측 0, 반복 간 원값 차이 0이다. CPython은 ICU 버퍼를 받는 두 입력의 적용 범위 밖이다. 두 프로세스의 레코드 위치와 각 결과는 [errors.csv의 controls 행](errors.csv)에 있다.

| 바꾼 한 조건 | 양성·음성 결과 | 영향을 받는 가정 |
| --- | --- | --- |
| 정확 표기 → ASCII 소문자 | CPython은 `latin capital letter oi`·`latin capital letter gha`·`line feed`·`lf`를 수용한다. `CJK UNIFIED IDEOGRAPH-4E00`와 `HANGUL SYLLABLE GA`는 성공하지만 전체 소문자와 CJK hex의 `4e00` 변경만으로 `KeyError`. ICU UNICODE/EXTENDED의 CJK·한글 예는 양쪽 표기 모두 성공한다. [CPython 1회 원값](receipts/controls/python-1.stdout#L6), [ICU CJK 원값](receipts/controls/icu-1.stdout#L41) | CPython에서 ASCII 소문자를 일괄 허용한다는 가정이 깨진다. ICU는 이번 사례를 접어 비교하지만 choice의 alias 범위는 그대로다. |
| 선두·중간·후미 공백 1개 추가 | 원문에 맞는 choice라 해도 세 변형 모두 CPython은 `KeyError`, ICU는 65535 / 12. [CPython 원값](receipts/controls/python-1.stdout#L10), [ICU 원값](receipts/controls/icu-1.stdout#L32) | UAX44-LM2의 비교 규칙을 두 공개 API가 그대로 적용한다는 가정이 깨진다. |
| 공식 `LF`를 `L`로 축약, 공식 `LINE FEED`를 legacy `LINE FEED (LF)`로 변경 | `LF`와 `LINE FEED`는 CPython에서 U+000A. `L`, legacy와 `<control>`은 양쪽 모두 miss. 전체 NameAliases 보존본은 두 판 각각 abbreviation 354행, 한 글자 0행이다. [분모](receipts/controls/single-letter.stdout), [CPython 음성](receipts/controls/python-1.stdout#L3) | property value 약칭이나 임의 축약을 문자 이름 별칭으로 처리하면 결과가 달라진다. |
| ICU 합성 label의 문자 유형 또는 choice 변경 | `<control-000A>`와 `<CONTROL-000a>`는 EXTENDED에서 10 / status 0. `<noncharacter-FFFF>`는 EXTENDED 65535 / status 0. `<control-FFFF>`, 존재하지 않는 이름 및 나머지 두 choice는 65535 / status 12. 역방향 ICU EXTENDED는 U+FFFF에서 19 / status 0 / `<noncharacter-FFFF>`. UNICODE·ALIAS는 0 / status 0, CPython은 ValueError/default None. [검색·역방향 원값](receipts/controls/icu-1.stdout#L56), [반복 2](receipts/controls/icu-2.stdout#L56) | `cp == 0xFFFF` 단독으로 실패를 판단하면 유효한 noncharacter 조회를 버린다. |
| ICU 출력 버퍼 용량 256 → 1 또는 23 | U+01A2 용량 1에서 세 반환 길이는 23/24/23, status 15, 각 한 바이트 `4c`, 범위 내 NUL 없음. 용량 23의 UNICODE·EXTENDED는 23 / −124 `U_STRING_NOT_TERMINATED_WARNING`, `U_SUCCESS=1`, NUL 없음. 같은 용량의 ALIAS는 24 / 15, 텍스트 23바이트로 잘림. [실행 1](receipts/controls/icu-1.stdout#L71), [실행 2](receipts/controls/icu-2.stdout#L71) | I02의 NUL 표현을 버퍼 경계까지 일반화하면 안 된다. I09의 길이 검사와 상태를 같이 봐야 한다. |

CPython의 표 기반 경로는 ASCII 대문자로 비교하고 CJK·한글 분기는 별도 접두사 검사와 hex/음절 파서를 탄다. ICU는 upper/lower를 만든 뒤 보통 이름·합성 label에 쓰는 입력과 choice를 분리한다. [P03 L1055–1071](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Modules/unicodedata.c#L1055-L1071), [P03 L1394–1443](https://github.com/python/cpython/blob/60403a5409ff2c3f3b07dd2ca91a7a3e096839c7/Modules/unicodedata.c#L1394-L1443), [I03 L1545–1631](https://github.com/unicode-org/icu/blob/8eca245c7484ac6cc179e3e5f7c1ea7680810f39/icu4c/source/common/unames.cpp#L1545-L1631), [I09 L1437–1458](https://github.com/unicode-org/icu/blob/8eca245c7484ac6cc179e3e5f7c1ea7680810f39/icu4c/source/common/ustring.cpp#L1437-L1458)

## 시간대의 입력·반환 ID

IANA 2024b의 `backward` 원행은 `US/Eastern → America/New_York`와 `Asia/Calcutta → Asia/Kolkata` 방향이다. `zic` 2.41로 두 결과 트리를 만들었다. `backward`를 포함한 트리에서 두 쌍 각각 inode와 SHA-256이 같고, 제외했을 때 두 Link 파일이 없었다. 같은 CPython을 써서 파일이 있는 경우 `ZoneInfo.key`와 `str`이 입력을 보존하고, 파일을 빼면 옛 두 이름만 `ZoneInfoNotFoundError`로 바뀌는 것을 확인했다. `tzdata` 모듈 fallback은 탐지 결과 `None`. [T01 raw L127/L311](https://github.com/eggert/tz/blob/6903dde39ed637adaafc352c4b6993739253f058/backward#L127), [컴파일·해시](receipts/tz/zic.stdout), [포함](receipts/tz/python-tz.stdout), [제외](receipts/tz/no-backward.stdout)

ICU 데이터가 `tzdata=2024b`, `cldr=46.0`인 상태에서 `US/Eastern`은 달력 객체 ID로 보존됐고, canonical 및 IANA API에서는 `America/New_York`였다. `Asia/Kolkata`와 `Asia/Calcutta`는 CLDR canonical이 `Asia/Calcutta`, IANA preferred가 `Asia/Kolkata`. 객체 ID는 입력 그대로였다. `Invalid/AF_RES_240`는 두 ID 검사 API에서 `U_ILLEGAL_ARGUMENT_ERROR`, `ucal_open`에서는 정상 상태로 `Etc/Unknown`을 반환했다. [T03 timezone.xml](https://github.com/unicode-org/cldr/blob/e1d37acce5dae468c414172be53b666d58d45be8/common/bcp47/timezone.xml#L217), [T07 공개 헤더](https://github.com/unicode-org/icu/blob/8eca245c7484ac6cc179e3e5f7c1ea7680810f39/icu4c/source/i18n/unicode/ucal.h#L1368-L1417), [ICU 원값](receipts/tz/icu-tz.stdout)

시간대에서 두 독립 Link 쌍과 오류 대조 키 1개를 시험했다. 조건은 CPython 포함, CPython 제외, ICU 내장 자료 세 가지로 각각 입력 5건, 관측 15/15. 반례의 전제는 해당 Link가 제공되는지와 어느 반환 ID API를 택했는지다. 운용 시간 계산과 번역된 지역 표시명은 조사 범위 밖이다.

## 정정

- 고정 ICU 헤더의 일반 miss 예상 10을 구현과 실측의 12로 정정한다. 본 실험 40키 × 2회, 반례 44키 × 2회가 관측됐다. 원문 상수 둘 모두는 오류표에서 유지한다.
- 원래 Name→코드가 ICU 전체에서 된다고 읽을 수 있던 AF-RES-222의 choice 미기재 5자리는 UNICODE/EXTENDED 성공, ALIAS 실패로 구체화했다.
- 시간대의 canonical ID와 사용자가 입력한 ID 둘 다 실제로 반환되는 API를 확인했다. IANA preferred와 CLDR canonical은 Kolkata 쌍에서 서로 다른 값을 낸다.
