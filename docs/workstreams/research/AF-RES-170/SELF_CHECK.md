# AF-RES-170 SELF_CHECK

자기 판정 **PARTIAL**. 중앙 상태와 다르며 독립 검토가 아니다. 결과 고정판 e28c786487f726c0289434ff08aff5bba1bb0dc0. 원장/표를 GitHub connector에서 다시 읽어 JS로 JSON/CSV 행·key·URL·표 순서를 확인했다. 제품 코드 실행/검증·외부 조작 실행은 없음.

| Q | 근거 행·원문 | 판정 | 미충족 / 다음 원자료 |
|---|---|---|---|
| Q1 | S01–S17,S28–S30,S60; F01–06,F14; frame D1–4,V0–3 | PARTIAL 8 후보 | 60개월 SAL + 모든 merge 제목/diff; V0 누락 보정 |
| Q2 | S07,S10,S26,S27,S40,S54–57 | PARTIAL | 역사 effective role/skin/namespace 및 defaults 상속 계산 |
| Q3 | S07,S14–17,S28–29,S31,S46,S49,S60–61; deployments D1–4,V0–3,R2 | 8 site 후보 sync 연결 | VE merge/approval 시간 4, role runtime 미확인; SAL bot 중복 제거 |
| Q4 | S35–39,S41,S47,S54–59,F20; I1–I10 | PARTIAL | historical raw tag array + exact revision UTC, VE edit histories 네 사이트, no save false-success 반례 |
| Q5 | I1–2 retry display, I5 unordered, I6/I9 incompatible, I10 tagged save candidate | strict save pair 0 | 동일 사람·URL·역할·조건의 ordered 실패→저장 |
| Q6 | S11–13,S23–25,S27,S39,S42–43,S48–50,S62–64; R2,R3,C1,C2 | PARTIAL | 철회 1/2, control 2 후보/실효값 미검증, 지점 전자자료 strict 0/2; screenshot 실패 F18/19 |
| Q7 | advice 28; D3-C/I10-A 및 S54–58 | 문장 강도 분리 | 당일 특정 역할 실제 저장 가능은 보류; 8 예정 자리 각 3판정 |

## 분모/실제로 읽은 문서
- sources.jsonl 84 접근 행, 산입 43 / 고유 work ID 43; 비산입 41. 산입 분류 {"config":22,"definition":6,"decision":6,"operation":7,"rail":2}. 요구 6/4/6/2/2/2 대비 config 22, decision 6, operation 7, definition 6, library 0, rail 2. 총량 22 이상이나 library 하한 2 부족. 일부 직접 읽은 제외 자료를 보수적으로 불산입. URL/확인구간/한계/내용 필수 필드 존재 true.
- 관측 계보 ID 고유 43 (산입 work 수준 라벨 기준; 통계적 독립성 의미 아님). 엄격한 독립 관측으로 재분류하면 자연층의 config 변경 5, 독립 SAL sync 사건 묶음 5, 직접 UI/조작 QA/공동체 보고 계보는 S35(두 사이트 한 QA), S36, S37, S41, S39(전달 S38 중복), S47(개발자 기전; S37 인용 중복), S58(서버 revision 메타데이터; S59 history 중복) 7. 동일 개발 조직/테스터·공동체 계정의 상관성은 제거하지 못했음. S31 SAL bot는 S29와 중복으로 독립 증거 추가 아님. 철도 별 운영자 2. source_lineage IDs는 재열람/미러/전달을 세지 않는 최소 출전 그룹이며 서로 독립인 사람 수는 미확인.
- frame 0행; deployments 0행; intervals 0행; advice 0행; RESULT 필수 3표 순서+마지막 약점표 true. 자연층 D1–4,V0–3 8 후보; 완전한 첫 4 확정 0/8; R2 1 설정 철회, R3 빈자리; C1/C2 2 control 후보; 4 beta follow-up 별도, R1/X1 반례 별도. SCOPE 모집 규칙→frame 1b1ffa...→VE 제목 누락 발견 보정 3fa440e...; outcome에 맞춘 교체 아님. 17 구간행: both 2 display retry, one-success 2, one-failure 3, both-unordered 1, incompatible 2, open 7. 자연층 저장 대표 8: strict pair 0, upper-only 1(D3), failure-only 1(D4), fully open 6. D3의 동일 계정·조건 없는 별 실패 I8은 상한과 결합하지 않음.
- 외부 링크 실제 접근 제한: Gerrit JS, historical SAL index partial, ticket F07–13, F15–17 header, F18/19 PDF screenshot redirect/size, F20 API DisabledError. UTF-8 text read only, 원본 PDF body/table cache and source status 표시. 자료 읽기 반복 횟수 전부 기계 로그로 재구성하지 못함; 84 기록행은 접근행 원장 수, 클릭 수 총합 아님. 
- 원장 ID 중복 없음 true. URL은 공개 링크를 기록, 이후 지속성 검사 안 함. countable lineage 수를 합계 문서 하한에 다시 더하지 않음.
- 비교 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc...e28c786487f726c0289434ff08aff5bba1bb0dc0: ahead 14, changed paths 7, owned only true. 수정된 파일 RESULT.md, SCOPE.md, advice.csv, deployments.csv, frame.csv, intervals.csv, sources.jsonl. dot-control 수정 없음. 
## 결론 반박 시도
1. 'default' 문자열을 제거한 broad query와 SAL을 읽자 2019 V0가 발견됨(모집 누락 실증); V4 순서 보정.
2. 실제 사용자 조작을 찾아 보니 S35 refresh, S39 same URL, S47 false submit, S41 version repair가 나온다. 배포를 시간적 충분조건으로 보는 가설 반박. 반대로 S58은 tagged reply 저장 실재, "실제 조작 관측 전무" 가설 반박. 다만 raw tags 및 같은 표면 실패를 못 찾아 엄격 0쌍 유지.
3. S12 A/B removal은 feature removal이 아님; S27+S49는 genuine flag off, S23/S24 익명 편집기 선택 복구는 출시와 별개, S25/S13은 유지 후보. 철도 actual arrival이 timetable과 다른 시계임을 확인; 도서관 support/kiosk/systemwide circulation으로 branch first entitlement를 바꿔치기하지 않음.
## 재개 입력·검증
아래 명령은 이 웹 작업에서 실행하지 않았다. GitHub 재열람 및 JS 구조 검사만 수행. Codex Cloud가 필요하면 public repo clone 및 read-only 정적 검사.
```sh
git fetch origin work/research-af-res-170
git checkout e28c786487f726c0289434ff08aff5bba1bb0dc0
git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc e28c786487f726c0289434ff08aff5bba1bb0dc0
python - <<'PY'
import csv,json,collections,pathlib
p=pathlib.Path('docs/workstreams/research/AF-RES-170')
s=[json.loads(x) for x in (p/'sources.jsonl').read_text().splitlines() if x.strip()]
print('source',len(s),collections.Counter(x['category'] for x in s if x['counted']))
for name in ('frame','deployments','intervals','advice'):
 r=list(csv.DictReader((p/(name+'.csv')).open()))
 print(name,len(r))
 if name=='intervals': print(collections.Counter(x['pair_status'] for x in r))
PY
git clone --filter=blob:none https://github.com/wikimedia/operations-mediawiki-config.git
git -C operations-mediawiki-config show 1812a7fdc2029e01ed7abbfdeb7920c807017c73
git -C operations-mediawiki-config show 188268c31b0907d91ea21e3053812e5bba638057
git -C operations-mediawiki-config log --all --since=2019-01-01 --until=2023-12-31 --date=iso-strict --format='%H %cI %s' -- dblists/visualeditor-nondefault.dblist wmf-config/InitialiseSettings.php wmf-config/CommonSettings.php
curl -fsS 'https://hu.wikipedia.org/w/api.php?action=query&prop=revisions&revids=22880382&rvprop=ids%7Ctimestamp%7Ctags&format=json&formatversion=2'
```
Public API 요청이 허용되는 실행 환경에서만 1회 정상 접근. 우회·개인 계정 검사 금지. git log는 모집 틀 보완용, 출력 읽어 변경 ID·SAL join 별도 수행. 당시 실제 사용자 실패·성공의 빈칸은 추정이나 실행으로 소급 충전하지 않음.
