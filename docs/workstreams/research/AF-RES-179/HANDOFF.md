# AF-RES-179 HANDOFF — PARTIAL

## 판정 및 결과 위치

- 자체 판정: **PARTIAL**. 자료 유형별 최저 수 및 실제 CLI/실효 Python 비교는 충족. 고정 하류 환경 2개 이상에서 동일 연결의 판·정확 SQL·입력·출력/오류를 결합하는 핵심 조건은 미충족. 고정 환경에서는 E1 한 사슬(실패, JSON_OBJECT 계열)만 충분; E2는 JSON_VALID 오류이나 정확 SQL/입력/실효 판 누락, E3/E5는 정상화 보고만. 외부 X10 B-type 사슬은 고정 표본 빈칸으로 대체하지 않는다. 원제보자의 첫 사용일·집단 사용률을 판정하지 않는다.
- branch: `work/research-af-res-179`; owned path: `docs/workstreams/research/AF-RES-179/`. 계획 기준 128f673685ec804c526a38e3f89d4d8a43fcd299; 시작 통합판 6fa67328360b02bc7e7270d4ad3300bfe0f286bd. 의존: AF-RES-170 @ 8e4ab12e3deac49a04817e17163987365171d2bb (자체 PARTIAL, 중앙 DONE; 명령 제공된 고정 SHA). dot-control 전체 직접 fetch가 크기 문제로 빈 결과, raw 경로도 접근 불가였으므로 최신 비교 diff에서 해당 항목/의존을 확인했다. SCOPE에 경계와 색인 확인 기록. 중앙 진행표·공용 색인 변경 없음.
- result_commit (대표 파일 및 자체점검 고정 SHA): `7599d87d39302958b580c2dbc29f1690b0f8f0e7`. 이 HANDOFF를 추가하는 마지막 커밋은 자기 자신의 SHA를 본문에 넣을 수 없으므로 브랜치의 최종 HEAD/부모 위 result_commit으로 식별한다.
- [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [sources.jsonl](sources.jsonl), [packages.csv](packages.csv), [observations.csv](observations.csv), [advice.csv](advice.csv), [frame.csv](frame.csv), [SCOPE.md](SCOPE.md), [CONTRASTS.md](CONTRASTS.md).
- 직접 산입한 고유 원자료 46개: 상류 6, 패키지 18, 하류 10, 소비 코드 6, 분야 비교 6. 61 원장 행 중 51 직접 읽음(46 산입, 5 제외), 9 접근 실패, 1 검색 전용. 별도 17 패키지 행, 20 사건 맥락(고정 6, 대비 14), 60 술어 자리. 미확인 54/60(고정 17/18), 실패 3/60, 성공 보고 3/60(고정 0; Swift J 두 환경, 외부 Python B 하나). 독립 관측을 문서 수로 부풀리지 않음: 고정 제보자 라벨 3, 대비 라벨 9; 신원 독립성 미입증. 이 작업자가 직접 재실행한 실효 연결 및 독립 검토 없음.
- 적용 가능한 결론: 기본 포함(3.38 이상, OMIT_JSON 제외)과 실제 연결 증거는 별개. 전통 J(JSON_VALID), A(->>), B(jsonb())를 분리하고 입력/타입/값을 맞춘다. Python.org Windows 3.9.0a5와 a6의 레시피 차이, macOS와 Windows 3.8 차이, SQLAlchemy #4437 CLI/Python 컴파일 차이는 배포 이름만으로 추론 불가한 반례. 3.45 이상이라는 정보로 현재 jsonb() 성공을 확정하지 않고 실제 연결 BLOB 및 roundtrip을 확인한다. NULL/빈 결과도 기능 없음과 구분한다. 도서관·교통은 안내와 이용 관측을 분리하되 지점/노선별 원시 영수증 부족을 명시. 제품 DB, 수집기, 최종 반환 형식 결정 안 함.

## 수행 및 검산 이력

| 묶음 | 고정 커밋 |
|---|---|
| ① 범위·판정 | 1e56b9f2b6029d8abd8e690c0f7b769013030dc4 |
| ② 열람 원장 | 26c735fa3ca074bab19d2cd088ed0649c32942f8 |
| ②b 대비 추가 | 4f6150224d5c7c0bdab2e38911a24e054804c2cf |
| ②c 태그/배포 보정 | 54b35c87efd8412c6eda9fd469c37b762cc71 |
| ③ 패키지·관측 | c83842ddd18859174cbc9d4353c2af2ca7dc9a74 |
| ④ 경쟁 설명·안내 | 34d264af72cef460e1c25552cda5ae98ecbed9d8 |
| ④b 외부 B 사슬 | 9ad623fa7f6571ad3dba4898dda649657c23f9d7 |
| ⑤ 필수 표·자체점검 | 7599d87d39302958b580c2dbc29f1690b0f8f0e7 |
| ⑥ 이 인계 | final branch HEAD |

⑤의 RESULT와 SELF_CHECK를 해당 SHA에서 다시 읽었다. RESULT 첫 표 1, 이후 표 2·3의 열 이름 일치, 마지막 표의 요청 열 이름 및 약점 정확히 3행 확인. 대표 blob RESULT 22c92811c6a1ed196899c44dac3660dd054fc05f; SELF_CHECK 07c62ffea55daaaf0732292a356921609a66f604. 시작판과 ⑤ compare: ahead 8, behind 0, 변경 9개 파일 모두 owned path 아래 추가. 이전 ④b 검산에서 61 고유 source ID, 산입 46, frame 61, package 17, observation 60(20×3), advice 10; CSV quote-aware width, 참조 ID 해소 0 누락, 대표 blob 고정 확인. 자기점검에 세부 기록. 독립 검토·실행 검사·CI 성공은 주장하지 않는다.

## 첫 재개 행동 — Codex Cloud

우선 고정 ⑤ 또는 HANDOFF를 포함하는 후속 HEAD를 확보하여 E1/E2 및 17개의 고정 미확인 셀을 읽고, 실제 원제보와 독립 재현을 구분한 별도 관측 ID를 배정한다. 공식 설치 산출물/패키지 해시와 라이브러리 연결이 확보될 수 있는지 먼저 판별한다. Windows/macOS/RHEL 원래 환경이 클라우드에서 불가능하면 접근·환경 미충족과 정확히 어느 값이 없는지 기록하고, 최신 Linux 재현으로 역사 원환경 관측을 대체하지 않는다. 다음 조사 순서는 (1) E1의 공식 Windows a5/a6, (2) E2 Label Studio 고정 조작과 연결, (3) E4/E5 교체 전후 실제 DLL 확인, (4) CLI/Python 동일 호스트 대비, (5) 원제보 원문에 있는 실제 재시험 출력 및 지점/노선 원시 영수증 찾기. 새 실험은 원제보의 날짜/환경과 합치지 않는다.

작업본에서 저장소 계약 및 검사 명령 (권한/환경 확인 후; 결과 저장은 owned_path 아래만):

```sh
git fetch origin
git switch work/research-af-res-179
git rev-parse HEAD
git diff --name-only 6fa67328360b02bc7e7270d4ad3300bfe0f286bd HEAD
git show 7599d87d39302958b580c2dbc29f1690b0f8f0e7:docs/workstreams/research/AF-RES-179/RESULT.md
python -m workbench.session start --help
python -m workbench.session check --help
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python scripts/check.py --require-git
```

새 세션 계약 생성이 필요하면 CLOUD_WORKFLOW의 start 사용법에 따라 `python -m workbench.session start af-res-179 --allow docs/workstreams/research/AF-RES-179/ --output docs/workstreams/research/AF-RES-179/session.json --fetch`를 사용하고 고정 의존 SHA 지정 옵션은 도움말에서 확인해 설정한다(공용 docs/tasks에 쓰지 않음). 이후 `python -m workbench.session check docs/workstreams/research/AF-RES-179/session.json --fetch`. 계약이 새 최신 통합판을 요구하거나 owned_path만으로 생성 불가하면 통합 담당에게 넘기고 이 브랜치의 기존 결과를 덮어쓰지 않는다. 시작/검사 미실행 사유: 이 세션은 GitHub 파일·커밋 인터페이스로만 조사/커밋하였고 checkout/원환경 실행/CI를 하지 않음. 위 명령의 성공/실패는 새 실행자가 exit code, SHA, stdout/stderr를 남긴 후에만 판정.

### 같은 연결 고정 입력 (비운영 격리환경)

아래를 다음 작업자의 owned_path 내 `probe.py`로 저장하고 대상 Python 실행 파일 절대 경로로 실행한다. CLI와 같은 호스트에서도 서로 다른 프로세스임을 표기한다. 배포/설치 artifact URL·판·OS·아키텍처·SHA256·실제 라이브러리 경로 및 UTC를 함께 보존. 과거 설치판과 DLL 교체는 격리 VM/실험 환경에서만, 운영 파일 교체 금지. 외부 설치 및 OS가 제공되지 않으면 보류. 이 코드는 현재 실행한 결과가 아니라 다음 작업용 고정 입력.

```python
import sqlite3, sys, platform, datetime
print("utc", datetime.datetime.now(datetime.timezone.utc).isoformat())
print("env", sys.executable, sys.version, platform.platform(),
      "sqlite3.sqlite_version", sqlite3.sqlite_version)
valid = '{"a":2}'
nullval = '{"a":null}'
con = sqlite3.connect(":memory:")
tests = [
    ("identity", "SELECT sqlite_version(), sqlite_source_id()", ()),
    ("flags", "PRAGMA compile_options", ()),
    ("J-valid", "SELECT json_valid(?), typeof(json_valid(?))", (valid,valid)),
    ("J-invalid", "SELECT json_valid(?), typeof(json_valid(?))", ("broken","broken")),
    ("J-null", "SELECT json_valid(NULL), typeof(json_valid(NULL))", ()),
    ("J-family-E1", "SELECT json_object('a',2,'c',4)", ()),
    ("A", "SELECT ? ->> '$.a', typeof(? ->> '$.a')", (valid,valid)),
    ("A-missing", "SELECT ? ->> '$.missing', json_type(?,'$.missing')", (valid,valid)),
    ("A-null", "SELECT ? ->> '$.a', json_type(?,'$.a')", (nullval,nullval)),
    ("B", "SELECT typeof(jsonb(?)), hex(jsonb(?)), json(jsonb(?))", (valid,valid,valid)),
    ("B-python-type", "SELECT jsonb(?)", (valid,)),
    ("B-valid", "SELECT json_valid(jsonb(?),8)", (valid,)),
]
for label, sql, params in tests:
    print("input", label, repr(sql), repr(params))
    try:
        rows = con.execute(sql, params).fetchall()
        print("rows", repr(rows), "python-types",
              [[type(v).__name__ for v in row] for row in rows])
    except sqlite3.Error as e:
        print("error", type(e).__name__, str(e))
con.close()
```

```sh
# 각각 고정 대상 실행 파일로 대체하고 출력 원문 저장
python docs/workstreams/research/AF-RES-179/probe.py
sqlite3 --version
sqlite3 :memory: "SELECT sqlite_version(), sqlite_source_id(); PRAGMA compile_options; SELECT json_valid('[]');"
```

Windows에서 `where.exe python` 및 `where.exe sqlite3`, Unix에서 `command -v python; command -v sqlite3` 추가. 필요하면 OS별 실제 모듈 로더 경로 조사(예: ELF _sqlite3 공유 라이브러리의 ldd 또는 macOS otool -L, Windows 로드된 DLL 경로). 런타임 정보 없이 설치 이름/CLI로 결과를 추정하지 않음.

기대 관측(가설, 미실행): Windows 3.9.0a5 E1과 같은 공식 빌드면 JSON_OBJECT 오류, a6는 JSON1 opt-in 레시피에 따라 J 정상일 가능성; Windows 3.8.10 stock은 J 실패 가능성, macOS 3.7/3.8 stock은 J 가능성. 3.38 기본 빌드 J=1/0, A integer 2, B 미도입; 3.45 기본 빌드 B blob 및 JSON roundtrip; OMIT_JSON 빌드는 달라질 수 있다. JSON null과 없는 키가 A에서 모두 SQL NULL일 수 있어 json_type으로 차이를 확인. J-null은 판별 대상 판의 실제 결과 그대로 기록. 오래된 선택 빌드가 J 성공해도 A/B 성공으로 확대하지 않음.

Label Studio E2: D2의 RHEL 7.9/Python 3.6.8/LS 1.0.0/Django 3.1.4 및 보고된 3.8.3은 재현 후보, 연결 판 미확인. 원문 실패 진입은 `label-studio start NEW_PROJECT --init`; 반드시 격리 DB/새 프로젝트에서만 실행하고 설치 wheel 해시, migrations plan, stderr 저장. C4/C5와 실제 wheel의 migration 일치부터 점검. Django 연결에서 `SELECT sqlite_version(), sqlite_source_id()`, `PRAGMA compile_options`, J/A/B 고정 입력을 같은 `django.db.connections['default'].cursor()`로 실행; 앱 startup에서 여는 연결을 이용하고 별도 :memory: 결과로 대체하지 않음. 실제 migration의 SQL·파라미터와 예외/출력을 Django 3.1.4의 connection.execute_wrapper 등으로 수집(설치판 API 확인 후), JSONField 행의 유효/무효 입력 및 NULL 허용 조건을 검증한다. E3 보고 3.35.2로 바뀐 것은 별개 환경으로 같은 절차를 반복. E4/E5 LS1.4의 교체 DLL 버전 미상은 새 버전 추정 금지. 완결을 위한 최소 증거는 두 고정 환경의 같은 연결 판·SQL·입력·typed 출력/오류와 실제 migration 대응; 새 실험이면 원제보의 당시 성공이 아니라 재현 결과로만 기록한다.

## 독립 검토 요청 및 색인 제안

독립 검토자는 고정 하류 사슬 수와 E1의 JSON_OBJECT 대 J 구분, E2 정확 DDL 결여, X10 외부 증거 승격 금지, D10 CLI와 Python 별개 연결, Q6 지점/노선 원시 기록 결여를 우선 대조한다. 유형별 최소 수 충족만으로 DONE으로 바꾸지 않는다.

색인 제안 한 줄: AF-RES-179 (PARTIAL) — SQLite/Python JSON 기능별 패키지·실효 연결·typed SQL 판정, 46 원자료/60 자리, 고정 사슬 부족; 실제 연결·정확 조작 단위 검증 필요.
