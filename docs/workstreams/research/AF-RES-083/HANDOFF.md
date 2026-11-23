# AF-RES-083 #1 인계 — PARTIAL

## 1. 식별

- 작업 ID / 시도: **AF-RES-083 #1**.
- 배정 종류: web-pro 연구. 실제 실행 위치: 제공된 ChatGPT cloud executor. 별도 웹 Pro UI 모델 선택·계정 연결을 확인한 것으로 보고하지 않는다.
- 공개 작업자 참조: AF-RES-083 #1. 비공개 대화·계정 식별자·인증정보는 저장하지 않는다.
- 역할: 원 배포 안내 모집·사전 A/B 봉인·후속 문단/반례 대조·연구 복사본 역적용·인계.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-083`.
- 계획 기준: `e7a777f2c13b626532b5828591d6388743688b34`.
- 실제 시작 통합 SHA: **`f736bd557fa4c40aecb6833165823196cfa42af2`**. 배정 브랜치가 없어서 이 최신 통합판에서 만들었다.
- 유일한 선행 결과: **AF-RES-079@`cc527e2c4f827afaaaa63f75c897d863c3adcc80`**. HANDOFF, RESULT Q3–Q7, relations G04/O02, URL 정책 비교와 해당 실행행을 인수했다.
- 고정 **결과 SHA / 원격 재열람 SHA**: **`a73aa215b765357b6688652edabc73675149aea4`**.
- 마지막 실제 결과 검증: 2026-11-23 **14:07:14 UTC** 계약·44항목 검사, **14:07:27 UTC** 원격 파일 21/21 바이트 일치.
- 인계 커밋: 위 결과판 다음에 **이 HANDOFF.md만** 추가한다. 자신의 SHA를 문서에 소급 삽입하지 않으며 이 파일의 Git 이력과 최종 응답에서 확인한다.
- PR: 생성하지 않음. 통합/중앙 상태 변경은 수행하지 않음.
- 연구 상태: **PARTIAL**. 기록은 검토 가능하지만 필수 실제 안내 모집·행동 정오 비교는 미달이다.

### 게시한 묶음

|순서|완료한 묶음|원격 SHA|
|---|---|---|
|①|모집·판정 기준·실제 시작 manifest|`7b108414de50ff32f28d1fa3c03ef6f2492724e6`|
|②|옛 배포 지시·6자리/공석·A/B 봉인|`35d7e18024cced8cc81f9397b65e90e0e74bb907`|
|③|후속판·발행자 수정·반례·다른 분야 실제 사건|`b433b1214e18d3ee8a23fc1253ecd216f0d98f8f`|
|④|정역 수선·세 결과표·자가검산·비가림 검토|`a73aa215b765357b6688652edabc73675149aea4`|
|⑤|이 인계 파일 단독|이 파일의 마지막 Git commit; 부모는 위 ④|

인증 없는 `git push`는 불가했으므로 연결된 GitHub Git Data 기능으로 parent·expected_sha를 고정해 게시했다. 각 로컬/원격 tree 일치를 확인했고 force update는 하지 않았다. ④의 로컬 commit `bb72f900b35473134f277cae6de19032c8133b88`과 원격 결과 SHA의 tree는 **`1e5d00b46afa131430fd5b186a7a5a811806e98c`**로 같다. 이는 새 source 변경 없이 게시 방법만 달라진 것이다.

## 2. 사용자 요구 / 작업 범위

목표는 같은 상류 기능 변경 뒤 배포된 어떤 안내를 고쳐야 하는지 원 독자의 행동·입력/출력·판·근거 위치로 판별하는 것이다. G04는 GDAL3.9/GeoParquet/GeoArrow, O02는 SciPy1.6 명칭 이관에서 시작했다. SciPy1.14 제거와1.11 알고리즘 조건 변경은 후속 사건으로 구별했다.

배정 시 통합판의 AGENTS, STATE, RESEARCH_BRIEF, RESEARCH_WORKFLOW, DOT_AUTOMATION, dot-control 자기 행과 의존 행을 직접 읽었다. 기준 원본은 [f736bd5의 AGENTS](https://github.com/laadkke-arch/agentflow-open/blob/f736bd557fa4c40aecb6833165823196cfa42af2/AGENTS.md), [RESEARCH_BRIEF](https://github.com/laadkke-arch/agentflow-open/blob/f736bd557fa4c40aecb6833165823196cfa42af2/docs/product/RESEARCH_BRIEF.md), [dot-control](https://github.com/laadkke-arch/agentflow-open/blob/f736bd557fa4c40aecb6833165823196cfa42af2/docs/automation/dot-control.json)이다. 선행 인계는 [079 고정 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/cc527e2c4f827afaaaa63f75c897d863c3adcc80/docs/workstreams/research/AF-RES-079/HANDOFF.md)다.

쓰기 허용 경로는 **`docs/workstreams/research/AF-RES-083/`만**이다. 중앙 dot-control·STATE·운영 AgentFlow 추천 레코드·소비 프로젝트는 수정하지 않았다. 079의 역사판 실행·이관 사건 모집·URL 생존율 조사를 반복하지 않았다. 같은 회차의 다른 결과에 의존하거나 기다리지 않았다.

## 3. 실제 변경

아래 경로는 모두 고정 결과 SHA의 파일이다. [전체 결과 디렉터리](https://github.com/laadkke-arch/agentflow-open/tree/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083)에서 다시 읽을 수 있다.

|파일|변경 사항 / 이유|확인 방식|
|---|---|---|
|[RESULT.md](RESULT.md)|필수 세 표→분모→Q1–Q8→정확히3약점/다음 조사. PARTIAL과0/0 산출 불가 명시.|원문·후속 diff·반례·표별 분모 대조, 별도 비가림 검토.|
|[SCOPE.md](SCOPE.md), [manifest.json](manifest.json)|후보 순서·판 경계·사전 가림·평가 기준·허용 경로·의존 SHA 고정.|사전 커밋과 해시 불변; workbench 계약 검사.|
|[frame.csv](frame.csv), [records.jsonl](records.jsonl), [proposals.csv](proposals.csv)|6자리·2 실제 지시·4공석, 보조층, 원 지시와 사전 A/B.|② 원격 봉인과 byte 일치. 오기는 사후 정정 파일로만 추가.|
|[revisions.csv](revisions.csv)|핵심6행과 O02보조7행의 후속 관측·실제 publisher diff·평가 분모.|등록된 원 ID·사전 제안·원자료 참조 검산.|
|[sources.jsonl](sources.jsonl), [attempts.jsonl](attempts.jsonl)|직접 자료124행, 시도33행. URL·고정판/행·직접 열람 UTC·한계·지지/반증.|원문 직접 읽기, 계보 통합, 실패/스니펫 제외, UTC 의미 보존.|
|[patches/](patches/), [evidence/repairs/](evidence/repairs/)|연구 복사본2개의 정·역 diff와 실제 배포 원문 위치. 원 인용·옛 A/B 보존.|root와 별도 검토자 각각2/2 역적용 byte 복구, source span6/6.|
|[SELF_CHECK.md](SELF_CHECK.md), [audit.py](audit.py)|Q별 주장/반대 근거/빈자리/최소 확인, 구조·범위·참조44항목 검사.|결과 SHA에서 실제 종료0. 완료 gate와 integrity 분리.|
|[streams/](streams/)|GIS·O02·외부 실제 사건·상류 원문·비가림 감사.|source ID와 lineage로 연결. 같은 판/미러/수정 사건 중복은 접음.|
|[REPRODUCE.md](REPRODUCE.md)|미실시 소비자 실행의 정확 SHA·입력·기대 관측·명령.|원 fixture/test와 실제 설치 증거의 차이를 명시.|

## 4. 실제 검증 결과

### 수행한 명령과 결과

|검사|대상|실제 종료 / 결과|
|---|---|---|
|`python -B -m workbench.session start af-res-083 --allow docs/workstreams/research/AF-RES-083/ --output docs/workstreams/research/AF-RES-083/manifest.json --dependency work/research-af-res-079=cc527e2c4f827afaaaa63f75c897d863c3adcc80 --fetch`|시작 f736bd5|0, 계약 version2·허용 경로·의존 SHA 고정.|
|`python -B docs/workstreams/research/AF-RES-083/make_repairs.py`|b433b121의 원 기록 및 작업 복사본|0, 정방향2/2·역방향2/2·옛 원객체/판정 보존. 실제 명령·해시는 rollback-receipt.|
|별도 검토자의 복사본 patch 적용|동일 두 연구 diff|각 정/역0, before byte 복구2/2, 세 판 구간 해시6/6. make_repairs.py를 대신 실행한 검토가 아님.|
|`python -B docs/workstreams/research/AF-RES-083/audit.py`|**a73aa215b765357b6688652edabc73675149aea4**|**0**, integrity44/44, research completion=PARTIAL. 14:07:14 UTC.|
|`python -B -m workbench.session check docs/workstreams/research/AF-RES-083/manifest.json --fetch`|**a73aa215b765357b6688652edabc73675149aea4**|**0**, status=passed, freshness=remote_checked, outside/unmerged/errors 각 빈 배열. 14:07:14 UTC.|
|GitHub 고정 raw URL 재열람|결과 SHA의 주요21파일|**HTTP200·로컬/원격 byte 일치21/21**, 14:07:06–14:07:27 UTC. 아래 부록에 hash와 파일별 완료 시각.|

계약 검사에서 재확인한 integration은 **`fe18482050b7b911e17267fa7dcaaa5b5fb46eb2`**다. 실제 시작 f736bd5와 구별한다. contract hash는 **`19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`**로 유지됐고 검사기는 통과했다. 결과를 최신 integration 위로 rebase하거나 중앙 상태를 바꾸지는 않았다. 검사 전후 `git status --porcelain`은 비어 있었다.

### 오류·정정과 재현 조건

봉인 frame의 QGIS 파일수111은 실제110으로, G083-S10의 자리 초과 설명은 공간 계약 부재로 각각 사후 정정했다. 원 frame/records/proposals는 그대로다. UTC 상한값을 exact second로 표시하지 않도록 source 정규화에서 precision·read/visual/hash 시각을 보존했다. 후속 감사에서 찾은 Arrow 단수 example 경로 README3개도 실제 읽었지만 관련 지시0이므로 핵심 공석·독립 자료 최소량을 바꾸지 않았다. 감사자와 root의 중복 열람은 독립 발견으로 세지 않았다.

**미실시/미확인:** 실제 소비자 설치/build 기록, GeoPandas·Astropy 원 입력의 새 기능 실행, 실제 운영 추천 레코드 수선, 소비 프로젝트의 patch/revert, 옛 HTTP 흐름, 외부 사건4건의 역사적 전후 전체 bytes, 실제 소비자의 중복 정정 적용. 원 지시의 실제 설치판·exact 입력을 확보하지 못해 동일 조건의 기능 검증을 완료할 수 없었다. 공급자 시험 선언·다른 입력·최신 시연으로 대체하지 않았다. 문서·원장 변경의 결과를 제품 전체 테스트 통과로 부르지 않았다.

## 5. 판단·근거

### 연구 판정과 원래 분모

|항목|결과|
|---|---|
|핵심 원래 자리 / 실제 지시 / 공석|**6 / 2 / 4**|
|독립 핵심 안내 저작 / 정확한 GDAL GEOARROW 직접 노출|**1 / 0**|
|실제 지시의 old·first·latest 원문 / 실제 literal 편집|**2/2 / 2/2**, 같은 가이드|
|A 제안 / B 제안|A 보류2. B 유지1·예방적 범위 명시1.|
|핵심 독립 정오 비교 가능 행|**0**. 불필요·누락·유효 유지 비율0/0 산출 불가.|
|원자료 / 산입 계보 / 엄격 / 보수적 / 추가 통합|**124행 / 39 / 35 / 25 / 23**|
|하류 가이드 저작|**11**, O02 보조6. core 표본수와 다름.|
|다른 분야 실제 사건 / 제도 / 양쪽 읽기 / 역사 bytes|**5 / 2 / 5/5 / 1/5**|
|실제 운영 추천 레코드 / 오류율|**0 / 0/0 산출 불가**|

GeoPandas 두 안내는 관련 포맷 생태계에 있지만 079와 같은 GDAL 옵션을 호출하지 않는다. G04-1은 옛 WKB 범위 유지의 정적 지지를 얻었다. G04-2의 조건 주석은 역사적 재사용을 위한 예방적 제안이며 원 안내의 필수 정정은 미확정이다. 실제 발행자는 판 문구를 일반화하거나 교차참조를 명확히 했지만 그 편집이 GN05 동작 손실의 수선이라는 근거는 없었다.

O02에서 등록 문자열 검색은 핵심 안내0을 반환했지만, GAM 같은 간접 의존 안내는 실제 존재한다. 따라서 공석은 고정 검색의 결과이며 분야 전체에 안내가 없다는 결론이 아니다. 내부 backend 이관·구 모듈 제거·다른 namespace·다른 독자 목적을 보조층에서 비교하고 원 분모를 보존했다.

외부 다섯 사건은 전거1→2 분할·병합, PDF만의 정정, 정정의 재정정, 중복 공지 철회다. 동일성·조건·이력·중복 방지 규칙을 제공하지만 geometry/CRS나 적분값의 동등성을 증명하지 않는다. 실제 중복 공지 발행1과 실제 소비자 중복 적용0도 구별했다. 각 원문 URL·확인 UTC·한계·반증은 sources와 external 원장에 있다.

### 색인 반영 제안 — 중앙 파일은 수정하지 않음

배정자는 AF-RES-083을 **PARTIAL**로 반영하고 결과 SHA a73aa215, 최종 인계 commit, 핵심2/6·독립 core저작1·직접노출0·정오분모0·보수적 자료25·외부5사건을 함께 색인하는 것이 적절하다. 자료 최소량 충족이나 무결성 종료0만으로 DONE으로 올리지 않는다. 운영 레코드 변경 제안은0이다. 현재 유지·조건 주석은 소유 경로의 연구 복사본에만 적용했다.

기존 중앙 계약과의 충돌은 검사에서 발견하지 못했다. 후속 integration은 위 SHA로 변했으나 소유 경로 밖 변경은 없다. 공개 저장소에 저장한 것은 공개 원문 URL, 짧은 인용·요약, 공개 전거 JSON, source hash와 연구 diff다. 인증정보나 비공개 작업 원문은 포함하지 않는다.

## 6. 다음 대화의 첫 행동

1. 브랜치와 이 파일의 마지막 단독 commit을 재조회하고, 고정 결과 **a73aa215**와 비교한다. 이 인계 뒤 다른 결과가 붙었는지 확인한다.
2. 아래 두 명령을 정확 결과판에서 실행해 계약과 연구 기록을 복구한다. 이것은 새 기능 실행이 아니다.

```sh
git fetch origin refs/heads/work/research-af-res-083:refs/remotes/origin/work/research-af-res-083
git show a73aa215b765357b6688652edabc73675149aea4:docs/workstreams/research/AF-RES-083/REPRODUCE.md
python -B -m workbench.session check docs/workstreams/research/AF-RES-083/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-083/audit.py
```

3. **첫 구체 연구 행동:** 현재 공석을 사후 교체하지 말고, 재개 입력을 먼저 고정한다. 동일 대상에 노출된 독립 안내를 늘릴 경우 새 모집에서 직접 GDAL 옵션 지시와 GAM 같은 간접 호출 안내의 포함 조건을 사전에 구분한다. 기존 a73aa215와 079 cc527e2를 입력 SHA로 사용하며, 기대 결과는 실제 원 안내와 상류 심벌·독자 조건의 연결이다. 사용자에게서 새로운 사실이 필요하다고 가정해 현재 기록을 임의로 채우지 않는다.
4. **기능 관측을 이어갈 경우의 실행 입력:** GeoPandas old `60c9773e44fff8a35344c2a74431e00c5546a4ee`, first `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1`; old `test_write_spec_version`의 box(0,0,10,10)·EPSG:4326·지원 schema 값과 first의 native/WKB 짝 파일을 사용한다. Astropy old `01369fb9d230480220dd81813f3fff906f88d52d`의 `test_blackbody_scipy`는100 K·`logspace(0,8,100000)` Å·rtol0.01이다. 아래 Python 역할 변수는 실제로 준비한 격리 환경 경로를 넣어야 한다.

```sh
# 각 명령은 위 SHA의 해당 소비 저장소 checkout에서 실행한다.
"$AF083_OLD_PYTHON" -m pip freeze
"$AF083_NEW_PYTHON" -m pip freeze
"$AF083_OLD_PYTHON" -m pytest geopandas/io/tests/test_arrow.py -k test_write_spec_version -vv
"$AF083_NEW_PYTHON" -m pytest geopandas/io/tests/test_arrow.py -k 'test_read_parquet_geoarrow or test_geoarrow_roundtrip' -vv
"$AF083_OLD_PYTHON" -m pytest astropy/modeling/tests/test_blackbody.py -k test_blackbody_scipy -vv
```

재구성 환경이면 그 사실을 표시하고 당시 실제 설치판으로 부르지 않는다. file SHA256·Python/NumPy/PyArrow/GEOS/PROJ 또는 SciPy 판·종료/skip 이유·geometry/CRS/schema 또는 적분값·인자 허용을 함께 남긴다. 이 단계는 **미실시**이며 079의 다른 실행행으로 통과 처리하지 않는다. 더 자세한 fixture 경로와 입력 차이는 REPRODUCE 및 GIS/O02 POSTSEAL에 있다.

5. **판정을 바꿀 다음 관측:** (a) 동일 상류 심벌을 권하는 독립 원 안내 쌍, (b) 정확 소비판·입력의 실제 요구 출력, (c) 옛 any-version 문구를 미래 native 파일에 적용한 실제 재사용 레코드 및 이미 정정된 소비자의 적용 로그다. LC 역사 export·Nature 옛 PDF·JNCI Box2 전후를 확보하면 외부 증거 수준도 높일 수 있다.
6. 이 결과의 게시·검산·인계에 추가 승인은 필요하지 않았다. 새 모집·제품 선택·중앙 색인 반영은 현재 연구 기록의 자동 완료와 구별한다. 다른 회차 의존성은 AF-RES-079의 고정 SHA 하나뿐이다.

**새 채팅이 이 저장소 파일을 자동으로 기억하거나 읽는 것은 아니다. 고정 RESULT·SELF_CHECK·REPRODUCE와 이 인계를 직접 읽고 시작한다.**

## 부록. 고정 결과 SHA의 실제 검사·원격 재열람 영수증

이 부록은 인계 작성 전에 수행한 검사 출력을 요약한 것이다. 원격 raw URL은 `https://raw.githubusercontent.com/laadkke-arch/agentflow-open/a73aa215b765357b6688652edabc73675149aea4/docs/workstreams/research/AF-RES-083/` 뒤에 아래 파일 경로를 붙인 주소다. 모든 행에서 HTTP200, 원격 bytes와 해당 Git blob bytes의 완전 일치를 확인했다. 해시는 원격/로컬 공통 SHA256이다.

### workbench.session check --fetch

종료값 **0**, stderr 없음. 전체 stdout SHA256: `a7dcbd465c66e525b99f55aa1e645191a5929af8f78d0a7d9a75d7299c7b943f`. 변경 경로 전체 배열은 경로 수·소유 경로 판정·줄바꿈 연결 해시로 축약했다.

```json
{
  "status": "passed",
  "task_id": "af-res-083",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T14:07:14.101598+00:00",
  "checked_out_commit": "a73aa215b765357b6688652edabc73675149aea4",
  "task_base_commit": "f736bd557fa4c40aecb6833165823196cfa42af2",
  "integration_commit": "fe18482050b7b911e17267fa7dcaaa5b5fb46eb2",
  "scope_base_commit": "f736bd557fa4c40aecb6833165823196cfa42af2",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification",
  "changed_paths_count": 160,
  "changed_paths_all_under_owned_path": true,
  "changed_paths_newline_join_sha256": "93a4ebe03e634a5a3077872570012cc905b0f1d6acb3ac379e59da9ebb19296b"
}
```

### 정확 결과판의 audit.py

```json
{
  "target_sha": "a73aa215b765357b6688652edabc73675149aea4",
  "started_utc": "2026-11-23T14:07:14.111432+00:00",
  "finished_utc": "2026-11-23T14:07:14.213034+00:00",
  "exit_code": 0,
  "integrity_checks": 44,
  "integrity_pass": true,
  "research_completion_status": "PARTIAL",
  "functional_execution": false,
  "stdout_sha256": "34a79c0ce08a1d3c8c175c61fd88b5114f605670be13dd66b1f5afde23f69ec0"
}
```

### 원격 파일21/21 재열람

|파일|bytes|SHA256|수신 완료 UTC|
|---|---:|---|---|
|[RESULT.md](RESULT.md)|32923|`30d0c298ad6f21350b11c8e6d4ffbd703ecf1c7e502a36ee3f6f24ee9d263066`|2026-11-23T14:07:12.751670+00:00|
|[SCOPE.md](SCOPE.md)|9046|`ee36e284751707e72ddaad6306923198a92f5127ea537034124dcd6d077f1c3c`|2026-11-23T14:07:12.783599+00:00|
|[frame.csv](frame.csv)|8125|`9aeb54f73aad540d3c87e92cbb8b6f8d169d4bc2542d36747ccfdda79d7b60ca`|2026-11-23T14:07:12.771396+00:00|
|[records.jsonl](records.jsonl)|18402|`8e7faca41cb8a71ceea2429fdc7d57bc337d4b0da2fe6c94a903cff015e466d7`|2026-11-23T14:07:12.775930+00:00|
|[proposals.csv](proposals.csv)|7084|`ae7cd8021cc8560c86276e81bd1f926de019a2852343aed2d8a2c4c007468105`|2026-11-23T14:07:12.717089+00:00|
|[revisions.csv](revisions.csv)|15030|`edeea1c68d990bdc5d3635dbdc3b7b41486740cad7de4380bb5b511f661c82bd`|2026-11-23T14:07:12.783641+00:00|
|[sources.jsonl](sources.jsonl)|217694|`c3df26d08cfa50c95faa97e41042ddc1420088421a23295127f1b0bb2532c861`|2026-11-23T14:07:16.975978+00:00|
|[SELF_CHECK.md](SELF_CHECK.md)|10884|`2560ada627f80ce653dd437006cc98c9582d1e4b0f8b4f6f064743ddcb83396e`|2026-11-23T14:07:17.015452+00:00|
|[REPRODUCE.md](REPRODUCE.md)|5764|`ce4f07088fd9260c8a4a41499279fec1ac9082e9f8f217c16234395d849807c9`|2026-11-23T14:07:16.969910+00:00|
|[manifest.json](manifest.json)|1736|`e82c90ad7a2b1c930a1a366f19d5ded76403c9dc45e79c6e588562fb365d7f04`|2026-11-23T14:07:16.986046+00:00|
|[evidence/preseal.json](evidence/preseal.json)|645|`6b925f6eb4533e7ed11b3e46ef0664d61703c1278ad65f802ffa47e282728c22`|2026-11-23T14:07:16.954114+00:00|
|[evidence/denominators.json](evidence/denominators.json)|2438|`e92d4e0ae77bacc1509f3c63b968641676c1dd0d3a9c179467d0d18292709f1e`|2026-11-23T14:07:16.970450+00:00|
|[evidence/audit-receipt.json](evidence/audit-receipt.json)|7240|`6ebedea6afe7c8df45c6146edef0a5cad53ed127e4cea754450fac771ae853e1`|2026-11-23T14:07:21.523056+00:00|
|[evidence/rollback-receipt.json](evidence/rollback-receipt.json)|9278|`ae8d99681b352575a6dc908ccbcc51a7b61c07eb35b0f8c8e1d1fd3bab0db2be`|2026-11-23T14:07:21.555229+00:00|
|[patches/locations.json](patches/locations.json)|3167|`5e7fc2ca24a33c43c34c760fdc1034cd7d46e755b1f64213520c9f8d9a1b4020`|2026-11-23T14:07:21.470999+00:00|
|[patches/RESEARCH-G04-1.forward.diff](patches/RESEARCH-G04-1.forward.diff)|2841|`ff678b50c634c9a4774c44a943a1438a0904f0114c037470386c911e10c55c78`|2026-11-23T14:07:21.504023+00:00|
|[patches/RESEARCH-G04-1.reverse.diff](patches/RESEARCH-G04-1.reverse.diff)|2841|`4e7ead241de609e301da59e15cee9318e549902a1208d76a9ba571486c60cde3`|2026-11-23T14:07:21.472973+00:00|
|[patches/RESEARCH-G04-2.forward.diff](patches/RESEARCH-G04-2.forward.diff)|2955|`37850c929879e685fcce9c55b0d0a504d04060061524bfbc7fee0d5a829cb9f9`|2026-11-23T14:07:21.512309+00:00|
|[patches/RESEARCH-G04-2.reverse.diff](patches/RESEARCH-G04-2.reverse.diff)|2955|`9934f6b6fa01d933770d3d3d9a79e3e04e775da1128be681a0a543e07fe4454c`|2026-11-23T14:07:27.312218+00:00|
|[streams/review/audit.md](streams/review/audit.md)|15769|`d40c63e51fef5b940aab268c4db15fbd4808c8ee92a3d2148f06630ea51f01e1`|2026-11-23T14:07:27.515717+00:00|
|[streams/review/final-report-review.json](streams/review/final-report-review.json)|9972|`c97c04a1ded54eb222abbceea4f586dc03d7f192ac1763d6c7801eb15cd593d6`|2026-11-23T14:07:27.299645+00:00|

인계 작성 UTC: 2026-11-23T14:10:02.022666+00:00. 결과 SHA의 파일은 이 인계를 쓰는 동안 변경하지 않았다.
