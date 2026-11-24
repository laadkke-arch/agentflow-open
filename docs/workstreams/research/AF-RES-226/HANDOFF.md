# AF-RES-226 HANDOFF — PARTIAL

- 역할: web-pro 조사·설계; 독립 검토 미실시. 작업 범위 내 결과를 GitHub에 저장했다. 자료 수 기준은 충족했지만 주표본 핵심 시간·주석·인수 연결 결손으로 PARTIAL.
- repository `laadkke-arch/agentflow-open`, branch `work/research-af-res-226`, owned path `docs/workstreams/research/AF-RES-226/`. 계획판 fc095c323d0177401d34f1daa7b4d1c529e2351f, 실제 착수 f3895893e32e2c055cefde446d34f1467fa27b4c. 계획판에는 226 없음, 착수판 226 RUNNING/attempt1/depends_on 207. 양 판의 207 결과 ded4731e82fd2e9efd1e10cec6c60f2dd55f7259 일치 확인. 중앙표는 변경하지 않았다.
- **결과판 SHA: `8b9445c89969db89f1cc02e8e504b8b1bf02e18d`**. 이 HANDOFF는 ⑥ 마지막 단독 커밋이며 결과판 SHA는 직전 ⑤의 고정판이다. 최종 handoff commit은 GitHub branch HEAD에서 확인.

## 1. 묶음과 대표 파일
| 단계 | 고정 커밋 | 결과 |
|---|---|---|
| ① 범위/예측 | a51afdd54112c88b50dde037f4cfd6beb492fc45 | SCOPE.md |
| ② 자료 원장/초기 관측 | 82781923e03e556ea331e9bc7c5d8d086f9d49a4 | sources.jsonl, scope-recheck.md |
| ③ 주표본/필수 표 | 4a2fc3df6c5638b023ca6637bc45a5c827990f51 | cohort.csv, joins.csv, labour.csv, tables-draft.md |
| ④ 반례·정정 | 931526981500b6f2a32c3e97f974b6f472b438a0 | counterexamples.md, answers.md, review-pair-witness.csv, 원장 정정 |
| ⑤ 결과·자체점검 | 8b9445c89969db89f1cc02e8e504b8b1bf02e18d | RESULT.md, SELF_CHECK.md, SCOPE.md 및 원장 갱신 |

결과부터 읽기: [RESULT.md](RESULT.md), [SELF_CHECK.md](SELF_CHECK.md), [sources.jsonl](sources.jsonl), [cohort.csv](cohort.csv), [joins.csv](joins.csv), [labour.csv](labour.csv), [answers.md](answers.md), [review-pair-witness.csv](review-pair-witness.csv), [counterexamples.md](counterexamples.md).

## 2. 관측과 중요한 미확인
- 6/6 실제 .tgt 세션 열람; 12/12 분절 자리 출력과 위치 관측. P/PA/PM 모두 PE 조건으로 직접 작성 HT 대조 없음. 세션별 W id·cur 및 익명 생산자 키 기록. 동일 basename 후보 12/12, 실제 같은 판의 annotation 원행 연결 확인 0/12; 12/12 미확인. 생산 시간, reviewer 시간·독립성 행 키, 수용 판정/재작업/인수 키 각각 12/12 결측. 0은 연결 확인 성공 건수이지 실제 0 시간 아님.
- 산업 Terribile 역할 집계 4/4(WPH Q1–Q3); 평균 PE 작성/개정 속도가 높았지만 job별 원행·동일 판·독립 검수자 시간·수용품질 연결 미확인. 다른 연구의 사람/분모와 결합 금지. 전체 인수 노동 우열 미확인.
- Temizöz pilot: En1→Tr1 79.17min, Tr1→En1 69.71min 두 단계 합계의 실제 공개 짝 반례. 별도 평가자 시간 및 계약 인수 기록 미확인; HT 대 PE 비교 아님. DG21/Yawat optional annotator protocol은 확인할 가치가 있으나 현재 로그 미확인. SW 검사 원연구/규정의 단계별 인시와 결함 수 별도 기록은 구조 대조이며 개별 acceptance log 연결은 미확인.
- 원장 44기록/27직접 자료 산입(27 work_id, 15 lineage)/17미산입. 22 유형 하한 6/5/4/4/3 충족; 9 연구 사건 계보, 6 DG21 실제 세션/2 반복 참가자/3텍스트/12 분절 자리. 별도 계보 수와 자료 수를 혼동하지 않음. 실패 10경로 포함; 특히 F01–F06/F08/F10 XML/MIME/400·접근 오류. Temizöz PDF screenshot timeout으로 parsed 표 판독. 공개 자료 부재 단정 금지. 원본 파일 bytes hash 및 LS14 개별 원행, 산업 xlsx/부록, SW 개별 log→repair→acceptance는 미확인. 개별 확인 UTC가 아니라 원장 기록 시각을 사용한 제한도 명시.

## 3. 결과판 재열람과 자체 검토
2026-11-24 UTC, ⑤ SHA에서 GitHub fetch_file로 RESULT/SELF_CHECK/sources/cohort/joins/labour/answers/SCOPE/review-pair-witness/scope-recheck/counterexamples 11파일을 다시 열었다. 표1 12행, 표2 산업 데이터 4행, Q1–Q7 제목, 마지막 약점 3행, cohort 12행, joins 12행, labour 28행(24 DG21 단계+4 집계), 원장 44행/산입 27/15 lineage와 pilot 2행을 대조했다. ⑤와 착수판 GitHub compare: ahead 5/behind 0, changed 12파일 모두 owned path 내, dot-control.json 변경 없음. Q1 모드 오해, Q2 문자열 동일성 반례, Q3 시간장 혼용, Q4 표시≠인수, Q5 optional 로그 및 Temizöz 반례, Q6 평균 및 언어별 방향반전, Q7 결함 수≠인시를 다시 확인. 원자료 실행·설치·자동 검사 및 독립 검토는 하지 않았다(웹 조사 역할); 아래 명령은 **실행하지 않은 Codex 인계 입력**이다.

## 4. 다음 첫 행동 — Codex 원자료 획득, 고정판부터
첫 행동: r649의 공개 SVN tree를 실제 읽고 F01/F02/F03에서 막힌 XML/주석 schema를 원바이트로 수신 가능한지 확인. 원 경로/권한 조건 준수, 실패 시 HTTP/status/명령/UTC 기록. r649 접근 실패 시 새 판을 임의 대체하지 말고 대체 판과 변경 사유/재선정 규칙을 따로 기록.

```sh
# 실행 위치: 임시 작업공간. 신규 설치는 자동 수행하지 않음.
SVN=https://svn.code.sf.net/p/tprdb/svn
REV=649
mkdir -p af226-input
svn ls -R -r "$REV" "$SVN/PUBLIC/DG21" > af226-input/dg21-public-tree.txt
svn ls -R -r "$REV" "$SVN/PUBLIC/DG21error" > af226-input/dg21error-public-tree.txt
svn ls -R -r "$REV" "$SVN/TPRDB/DG21" > af226-input/dg21-tprdb-tree.txt
svn ls -R -r "$REV" "$SVN/TPRDB/LS14" > af226-input/ls14-tree.txt
svn export -r "$REV" "$SVN/PUBLIC/DG21" af226-input/DG21-public
svn export -r "$REV" "$SVN/PUBLIC/DG21error" af226-input/DG21error-public
svn export -r "$REV" "$SVN/TPRDB/DG21/Alignment" af226-input/DG21-alignment
svn export -r "$REV" "$SVN/TPRDB/DG21/Translog-II" af226-input/DG21-translog
find af226-input -type f -print0 | sort -z | xargs -0 sha256sum > af226-input/SHA256SUMS
find af226-input -type f \( -iname '*.log' -o -iname '*.aln*' -o -iname '*.crp' -o -iname '*schema*' \) -print
grep -inE 'keepProtocol|reviewer|annotator|revision|acceptance|segDur|startTime|endTime|pause' af226-input/dg21error-public-tree.txt
# 실제 artifact/input 고정 후 저장소 경로 차이 검사
git diff --name-only f3895893e32e2c055cefde446d34f1467fa27b4c 8b9445c89969db89f1cc02e8e504b8b1bf02e18d
git show 8b9445c89969db89f1cc02e8e504b8b1bf02e18d:docs/workstreams/research/AF-RES-226/cohort.csv
```

입력 6세션 = P01_P13, P02_P14, P01_PA8, P02_PA13, P01_PM14, P02_PM8; 각각 segId 1,2; 대조 R06–11의 W id/cur 범위. 우선 PUBLIC/DG21error/SessionProps 및 Translog-II의 동일 basename 원행을 열고 실제 schema에 따라 source/text/segment/revision/actor/condition/token span을 확인. TPRDB/DG21error 경로는 실제 tree에서 발견되는 경우만 사용. XML parsing은 기존 도구 또는 Python 표준 xml.etree.ElementTree로 실제 root/attributes/namespace를 판독 후 구성; 예상 field를 실제 관측으로 기록하지 말 것. 오류주석과 원출력의 normalized token sequence/좌표/판 SHA 대조, 추가 P19 세션의 실제 역할 확인. Yawat .aln/.crp/.log 또는 다른 주석 파일·설정/actor/time 원출전이 공개 tree에 없다면 탐색 범위와 결측 위치 기록(비공개 원자료를 가정하거나 우회하지 않음). optional log 발견 시 시간장/actor/독립성/가림/작업 완료와 인수판 키 검증. 동일 actor 중복 구간 제거; 타 actor 동시시간은 인시 합산. 시간 정의 300ms vs v2/v3 차이 유지. 해당 합계가 stage sum인지 final acceptance까지인지 명기. 근거가 없으면 보류 유지.

후속 대조: I01 Terribile DOI 및 저자판에서 합법 공개 데이터/부록이 실제 제공되는지 확인, job+stage+actor+source words+active hours+quality/verdict를 개별 join. 동일 분모로만 sum(words)/sum(hours) 또는 matched job hours 검증. S01/JPL 및 S02/Porter의 공개 원 inspection log와 rework/acceptance record를 찾되 집계만 있으면 그 상태 유지. 외부 접근/시간 원행 실패를 보완한 뒤 independent reviewer에게 원행 기준으로 블라인드 재검 의뢰. 새 소프트웨어 실행·설치·자동검사는 Codex에 넘기며 지금 세션은 실행하지 않음.

## 5. 색인 반영 제안(수정 안 함)
AF-RES-226 PARTIAL | 12/12 output positions, 0/12 exact error/time/acceptance joins confirmed; 4/4 industry aggregate roles, 27 direct sources, paired-review positive counterexample; DG21 all PE; same-quality total labour unknown | RESULT fixed 8b9445c89969db89f1cc02e8e504b8b1bf02e18d | next r649 export + reviewer protocol/accepted revision join | central owner only.
