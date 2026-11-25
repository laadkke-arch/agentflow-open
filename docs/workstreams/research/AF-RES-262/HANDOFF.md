# AF-RES-262 HANDOFF — PARTIAL
고정 결과판: [ad6f9ba75387b1152770d0c24c85a0b6c7afdb11](https://github.com/laadkke-arch/agentflow-open/commit/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11) (SELF_CHECK까지 포함; HANDOFF는 다음 단독 커밋으로 작성). [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/RESULT.md) · [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/SELF_CHECK.md) · [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/SCOPE.md) · [judgments.csv](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/judgments.csv) · [conditions.csv](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/conditions.csv) · [denominators.md](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/denominators.md) · [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/sources.jsonl) · [revisions.md](https://github.com/laadkke-arch/agentflow-open/blob/ad6f9ba75387b1152770d0c24c85a0b6c7afdb11/docs/workstreams/research/AF-RES-262/revisions.md).

## 자체 상태 및 결과
**PARTIAL**. 원자료 수 하한은 28개(4 CSN, 12 원코드 파일, 8 규격/시험, 4 NIST)로 충족했지만, 정확한 주표 12개 중 3개 정렬 소스가 접근 실패하여 9개만 원판 판독, 정렬의 별도 미판정 슬롯도 미확인. 별도 3개 정렬 보강 파일을 주표 성공으로 세지 않았다. 실제 신규 실행/독립 평가자 검토/실제 사용자 배정·도입 관측 없음. 판정은 정적 판독과 언어 계약에 제한. 열람 시각은 원장 기록 시각 및 확인 구간으로 보존했으며 개별 초 단위 확인 시각은 미확보.

- 네 Python 질의: 84 원평정 행/40 고유 URL, 중복 44행, 실제 0점 14행, 빈점수·조인 실패·질의 미출현 0. 첫 3개씩 12 URL 봉인, 23 원행/0점 4 원행. 논문 Table 2 4026/2089 vs 고정 CSV 4006/2079(전체/Python) 차이는 원인 미확인.
- 원평정 ≥2가 모두인 확정 양성 4, 모두 <2 음성 4, 상충 4. 부가조건 Y3/N4/U3/NA2. 확정 양성 중 Y1/N2/NA1, 원질의 양성·새 조건의 공동 성공 하한/상한 1–4/12(상충을 잠재적으로 양성 처리하는 경우 포함). 이는 표집틀 안의 정적 판독 범위이고 모집단 추정이 아니다. J1/J2의 높은 관련성과 기본 JSON escaping에 따른 literal unicode 실패 공존; 원평정 오류라는 뜻 아님.
- 보강 슬롯은 4 예정/실제 미판정 3/미확인 1. 정확한 0점과 미판정 다름. TREC qrels의 실제 0점과 미등재 대조 확인. 원 자료로 검색 순위나 실제 채택·검수·절감 시간 추론 금지.
- 독립 평정자 ID 없음. 자체 재집계 확인만 수행. 37 원장 행: 30 성공/7 실패/28 산입, 최소 접근 횟수 48.
- 착수 integration SHA dc6b22120b23a6af8558bd6031ea8ff8af041dcf, control blob 2196164b74a17be5eb4bfe93db8ac0d4ed4571fd, 249 의존 결과 a61cee2b8882e79226f383217440ab71f2637f8c. 지정 branch 및 owned_path만 사용. RESULT까지 GitHub compare 7개 신규 파일 전부 owned_path, SELF_CHECK 별도 1개 신규 파일 원격 확인. dot-control 미수정. 실제 추론 설정/모델 effort의 독립 확인은 못 함.

## 후속 첫 행동 (Codex 또는 공개 원자료 복구 담당)
S1–S3 원 URL은 judgments.csv 및 sources.jsonl F-S1/F-S2/F-S3. 아래 exact commit/path의 공개 archive/API/원 git object를 다시 확인하되 이동판/다른 SHA로 바꾸지 않는다.
```sh
git clone --no-checkout https://github.com/github/CodeSearchNet.git csn
git -C csn checkout --detach 106e827405c968597da938f6b373d30183918869
git -C csn hash-object resources/annotationStore.csv
git -C csn rev-parse HEAD
python - <<'PY'
import csv, collections
p='csn/resources/annotationStore.csv'
qs=['sort string list','write csv','pretty print json','read text file line by line']
norm=lambda s:' '.join(s.split()).casefold()
with open(p,encoding='utf-8-sig',newline='') as f:
    rr=list(csv.DictReader(f))
print('total',len(rr))
for q in qs:
    a=[r for r in rr if norm(r['Language'])=='python' and norm(r['Query'])==q]
    keys=list(dict.fromkeys(r['GitHubUrl'].strip() for r in a))
    print(q,len(a),len(keys),sum(r['Relevance'].strip()=='0' for r in a),keys[:3])
PY
# 3개는 각각 별도 빈 임시 디렉터리에서 공개 원격의 exact object 요청:
# git init S1 && git -C S1 fetch --depth=1 https://github.com/stevepeak/inquiry.git f6ea435c302560ba19985b5d4ce2c97e2f321508
# git -C S1 show f6ea435c302560ba19985b5d4ce2c97e2f321508:inquiry/query.py
# git init S2 && git -C S2 fetch --depth=1 https://github.com/mirukan/lunafind.git 77bdfe02df98a7f74d0ae795fee3b1729218995d
# git -C S2 show 77bdfe02df98a7f74d0ae795fee3b1729218995d:lunafind/order.py
# git init S3 && git -C S3 fetch --depth=1 https://github.com/OnroerendErfgoed/oe_utils.git 7b2014bda8ac6bb71b7138eaa06ac17ef3ff4a6d
# git -C S3 show 7b2014bda8ac6bb71b7138eaa06ac17ef3ff4a6d:oe_utils/search/__init__.py
```
위는 미실행 명령. CSV 기대 blob 98beff4e3dca397ca4f7084e584874de4e6c7bcf; 4006 전체, 각 질의 (21,10,8),(22,10,1),(19,10,0),(22,10,5), 첫 3 URL이 judgments.csv selected_slot과 일치. 다르면 CSV encoding/정규화/판을 검토하고 재집계 차이 보존. S1–3 확보 시 exact SHA 및 blob hash, 원줄, 함수명, 입력 불변 판정, 호출 경계, 다음/이전 공개 함수 최대 5개 원파일 순서 및 원평정 key/anchor 교차를 기록. 계속 실패하면 U 유지. 비공개/권한 우회 금지.

## 후속 동적 검증 인계 (미실행)
새 제품이나 CSN 모델 실행이 아니라 격리된 최소 fixture 검산만 제안한다. CPython v3.7.0 고정 원시험(P07/P08) 및 문서(P09/P10)와 candidates exact SHA/원줄은 conditions.csv 및 sources.jsonl. 환경 버전, 입력 및 함수 경계 기록; 외부 저장소 전체 import, 서비스 API, 사용자 자료 전송 금지. 필요 최소 함수만 원문/해시와 함께 검토 후 샌드박스에서 실행; 원함수와 fixture를 구분한다.
- sort: 확보한 정확판 함수 계약에 맞춰 ['b','a','a'] 입력, 호출 전후 원 리스트 및 반환/정렬 결과 비교. 원순서 변경이면 불변 N; 계약상 문자열 정렬 대상이 아니면 NA. 입력 불변과 정렬 정확성은 분리.
- C1/C2: 원 writer 호출 경계로 csv.writer를 동일 dialect에서 사용해 ['a,b','c'] 또는 C2의 comma-containing property key를 작성한 후 csv.reader 동일 dialect로 읽어 필드 완전 일치 검사. C1 기본 delimiter ';' 및 명시 comma 별도. 기대: 같은 dialect/문자열 계약에서 왕복. 필드 분할·손실이면 N 또는 호출 전제 수정. C3는 CSV 출력 경로가 없으면 NA 유지.
- J1/J2: 원 코드의 dumps/dump 옵션 그대로 {'x':'αΩ'} 입력. 기대: 출력 literal αΩ 없음, json.loads의 값은 동일. 실제 Unicode 문자가 있으면 literal 판정 반전; roundtrip 성공만으로 반전하지 않음. J3 JSON 분기 별도. 실행 환경 stdout 인코딩·ensure_ascii 옵션 보존. 원 서비스 client import/인증/네트워크 없이 분리.
- R1/R2/R3: 두 줄 및 긴 N줄의 가짜 file-like object에 read/readlines 호출 감지, readline 호출 기록, 입력/결과 누적 및 caller 경계 정리. R1 whole text splitlines/누적; R2 helper는 readline 한 줄(전체 caller tree 누적 별도); R3 handler NA. 전체 파일 read/누적 확인 시 streaming Y 철회. helper와 전체 pipeline 메모리 사용 분리. 필요한 경우 tracemalloc 크기 증가 검산은 interpreter/version별 별도 측정.
- 원시험 검산 예: 정확 v3.7.0이 준비된 격리 CPython 빌드에서 ./python -m test test_csv test_json (미실행); 전체 빌드/반복 검산은 실행 담당 결정. Python 버전이 다르면 다른 판으로 표시. 
- 원영수증 형식: case_id, repo/SHA/blob/path/line, source/fixture 차이, Python 버전·환경, 실행 command, literal input, expected, actual stdout/stderr 및 exit, 전후 값·메모리(해당 시), 반전 판정, UTC. 재검산 없이 완료 표기 금지. qrels는 원 URL에서 다운로드해 topic 19335의 전체 block 및 (19335,1200258) 미등재 재검산; 없는 pair를 0으로 기록하지 않는다.

## 색인 제안
AF-RES-262 → code-search human relevance, added requirement, partial design, unjudged, denominator/pooled evaluation; dependency AF-RES-249. 결과 상태 PARTIAL로 색인, 독립검토/실행 미실시 및 3개 정확판 미확보 명시. 중앙 dot-control 또는 다른 경로 직접 수정하지 않는다.
