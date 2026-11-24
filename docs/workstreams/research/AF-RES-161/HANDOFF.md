# AF-RES-161#1 HANDOFF — PARTIAL

**PARTIAL, 원격 결과 커밋 완료.** 최초 요청의 하위 자료 하한과 핵심 교정 거래 판독 미달. 자료 22개 총량은 넘었으나 거래/판 이력 2/8(6개 부족, 사건 계보 단위로 엄격히 세면 1/8, 7개 부족). 자연층과 보강층을 혼합하지 않았다. 150의 재생 실험을 반복하지 않았다.

| 항목 | 고정 값 |
|---|---|
| 저장소 / 브랜치 | laadkke-arch/agentflow-open / work/research-af-res-161 |
| 소유 경로 | docs/workstreams/research/AF-RES-161/ |
| 계획판 → 시작판 | ded3420249a3d60ebbb578a8432cf262d3ffa7d7 → d32c697b4345442a4c91f62b8fb0bbed19e58034, 4 commits ahead, dot-control.json 변경만 |
| 의존 | AF-RES-150 DONE, ff2c1fc8786ba70a1432f1089f8f81288e43a61d |
| 실제 결과판 | **fb1c5e91209a77554e2e6f6c3e16a6aa59a23917** · [RESULT 고정판](https://github.com/laadkke-arch/agentflow-open/blob/fb1c5e91209a77554e2e6f6c3e16a6aa59a23917/docs/workstreams/research/AF-RES-161/RESULT.md) · [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/fb1c5e91209a77554e2e6f6c3e16a6aa59a23917/docs/workstreams/research/AF-RES-161/SELF_CHECK.md) |
| 마지막 인계 SHA | 이 파일을 단독 추가한 현재 마지막 커밋; 자기 자신의 SHA를 파일에 넣을 수 없어 아래 git log로 확인 |
| 검사 | GitHub API compare: 6 ahead, 11 파일, 모두 소유 경로=true; 원장 84행, 고유 source_id 84, 산입 집계 {"report 1":15,"guidance 1":5,"history 1":2,"library 1":2,"geographic 1":2}; CSV 행수 frame/transactions/fields/citations=58/21/22/8. git diff --check 및 workbench 실행 검사는 미실시 |

| 묶음 | 원격 커밋 | 같은 SHA 재열람 대표 |
|---|---|---|
| ① | 9b1ada99e537a8f98f51e75bbee505f654986b28 | SCOPE.md |
| ② | b74c8b5e3b5f590387cfa4fd8159eb8fde388d4c | frame.csv |
| ③ | 726d19069e15995306c32ddaf3853d2c7e8fc7ce | fields.csv |
| ④ | 5cc93a832365077663004575dd06f430ae3d8ba0 | COUNTEREXAMPLES.md |
| ④ 보정 | 9f365696fa3fb0d62b3e8b26a52b841d94ce75f0 | COUNTEREXAMPLES.md |
| ⑤ | fb1c5e91209a77554e2e6f6c3e16a6aa59a23917 | RESULT.md, SELF_CHECK.md |

## 넘길 판단

- #6371의 42049802와 OL14863262W 24~26은 동일 거래인지 미확인. 같은 게시글은 조인 키가 아니다. 네 무관 필드 손실은 보고 수준, 실제 필드 원값과 독립 작성자 역할 미확인. 2022 설명은 revision-1 복원, 2023 역 diff는 제안.
- 2019 Wikidata 보강에서 두 실제 객체의 고정 revision을 읽었다. Q59165607 986442520→1038289881→1048159568(병합판의 바로 다음 편집이 undo); Q314104 936463156→1039041773→1048159950(별도 bot rewrite→undo). 두 복구가 1분 차이; 후자의 P910은 전자의 undo만으로 복구되지 않았다. 3 대상 행 수정, 4 무관/안정 행 유지, 0 직접 손실은 선택한 7행에서만. 후속 유효 독립 편집의 보존 직접 비교 없음.
- Q7: 과거 고정판의 특정 필드 확인에는 한 URL, 현재 정정 과정을 물으면 oldid+diff/복구 revision, 조인·판 결측이면 둘 다 근거 보류. 전체 snapshot vs 부분 역수정 vs immutable citation+정정 관계는 조건부 대안, 실행 구현 아님.
- OL 자연 최초 보고 34개 중 16자리 본문, 연속 원판 0/16(결측/비적격 포함). WD 원순위 16자리 미복원(8+조건부 8), 자연 양성 0이라고 단정 금지. 추가 W05–W08은 보강층. 자료 산입 26, 필수 history만 미달; 실제 외부 인용 전후 고정판과 지리 분할 및 ID 연속성도 미확인.

## 첫 재개 행동 (공개 자료만, read-only)

1. B01의 transaction 구성원 원문부터 열고 모든 페이지의 object key 및 revision/time/edit summary를 확보한다. B02의 24/26 비교와 24·25·26 개별 원판을 대조한다. 25를 자동으로 merge라고 가정하지 않는다. 필요한 최소 필드: key, revision, last_modified, created, authors, title, description, covers, subjects, transaction/member ID. 출처가 한 판만 돌려주면 실제 revision 값을 먼저 검증. 이 단계에서 C1/C2 조인을 지지·반박·미확인 중 갱신한다.
2. 자연 WD 원 모집: 공개 Phabricator advanced search, project Wikidata, created after 2020-01-01 before 2026-01-01, merge undo / merge revert 두 검색, created asc + T ID 동률, 전체 union 첫 8, 원판 2 미만일 경우 다음 8. UI가 정렬/범위를 내주지 않으면 그 실패와 시도 URL을 기록하고 공개 archive 원순위 복원 시도. 이미 발견된 보강 사례로 자리를 대체하지 않는다.
3. 원판 6개 더 직접 판독(계보 단위 7), 특히 OL natural first16의 B09–18, WD W05 Q65788404, W06 Q5380480/Q18674739(2023-08-03, 2023-11-13 후보), W07 Q97445914(2023-04-06 00:14–00:22)에서 정확한 revision ID와 독립 수정 값을 찾는다. 외부 Commons W04 P6243 및 OL I5206C의 원 edition dump를 추가 확인. 확인된 실제 revision ID만 좁게 비교하고 dump 전량 재생 금지.
4. 대량 덤프가 불가피하면 Codex에게 C1 정확히 24/25/26 세 판, 24↔25 및 25↔26 비교와 위 필드, 42049802 member join만 입력. 기대 관측: 각 쌍의 changed field와 값 및 timing, 첫 결측, merge/undo linkage. 별도 실제 변경 검사는 금지.

```sh
# 저장소 루트, 읽기 전용 검증
git fetch origin refs/heads/work/research-af-res-161:refs/remotes/origin/work/research-af-res-161
git log -1 --format=%H refs/remotes/origin/work/research-af-res-161 -- docs/workstreams/research/AF-RES-161/HANDOFF.md
git diff --check d32c697b4345442a4c91f62b8fb0bbed19e58034 refs/remotes/origin/work/research-af-res-161
git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 refs/remotes/origin/work/research-af-res-161
# 공개 원장 읽기. 성공한 응답의 revision 번호와 object ID를 검증.
D=$(mktemp -d /tmp/af161-ol-XXXXXX)
curl -fL --max-time 30 'https://openlibrary.org/recentchanges/2010/11/26/merge-authors/42049802?page=1' -o "$D/42049802-p1.html"
curl -fL --max-time 30 'https://openlibrary.org/recentchanges/2010/11/26/merge-authors.json' -o "$D/2010-11-26-merge.json"
curl -fL --max-time 30 'https://openlibrary.org/works/OL14863262W/Tales_of_Soldiers_and_Civilians_18_stories?_compare=Compare&b=26&a=24&m=diff' -o "$D/work-diff.html"
for v in 24 25 26; do
  curl -fL --max-time 30 "https://openlibrary.org/works/OL14863262W.json?v=$v" -o "$D/work-$v.json"
done
python - "$D" <<'PY'
import json, pathlib, sys
d=pathlib.Path(sys.argv[1])
fields=['key','revision','last_modified','created','authors','title','description','covers','subjects']
for v in (24,25,26):
    p=d/f'work-{v}.json'
    try:
        x=json.loads(p.read_text())
        assert x.get('key')=='/works/OL14863262W' and int(x.get('revision',-1))==v
        print(v,json.dumps({k:x.get(k) for k in fields},ensure_ascii=False))
    except Exception as e:
        print(v,'MISSING_OR_WRONG_REVISION',str(e))
PY
# Wikidata read-only revision discovery; no edit, undo or merge POST.
curl -fLG --max-time 30 'https://www.wikidata.org/w/api.php' \
  --data 'action=query' --data 'prop=revisions' --data 'titles=Q65788404' \
  --data 'rvprop=ids|timestamp|comment' --data 'rvlimit=50' --data 'format=json'
# continue via returned continuation token; exact oldid only after discovering it.
```

명령은 **미실행**. raw JSON endpoint가 실제 historical revision을 보장하지 않으므로 조건 실패 시 HTML 고정판 또는 발행처의 공개 history/dump로 대체. 모든 응답은 읽기 전용, m=revert/undo 링크 클릭이나 POST 금지. workbench 계약 검사는 manifest가 없고 이 웹 작업자에서 실행하지 못함; Codex가 최신 AGENTS/RESEARCH_WORKFLOW와 workbench.session --help를 읽은 뒤 올바른 세션 계약 입력으로 검사할 것. 본 작업의 GitHub 비교/원장 파싱과 별개다.

색인 제안 한 줄: **AF-RES-161 · 오병합 이후 독립 편집 및 하류 인용 계보의 복구 (PARTIAL, Q1 교정 미조인/자연층 결측/2019 실제 편집 2원전).**

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| C1/C2 조인 키와 OL 실제 값 부재 | #6371에서 한 거래의 저자 복구와 무관 필드 손실을 함께 입증했다는 주장 보류 | 42049802 모든 구성원, OL14863262W 24/25/26 고정 JSON·history (B01–08) | 같은 transaction의 work ID/revision과 복구 요약 일치 또는 다른 transaction이 명시됨 |
| 자연 WD 원순위 미복원, 역사 원전 2/8, 보강에 유효 독립 후속 편집의 보존 비교 없음 | 선택 복구가 독립 편집을 지킨다는 운영 일반화·빈도·실제 전체 무손실 판정 보류 | Phabricator 원 검색 순서, OL 첫 16, W05 Q65788404의 merge/후속/undo 판 | 동일 원장에 다른 편집자의 유효 필드 값이 남거나 사라진 네 시점 및 실제 restore 모드 |
| 하류 KG-B는 확인했지만 외부 고정 서지와 지리 ID 전후 미확인 | URL만으로 같은 대상/판/절을 안내하는 정책과 다른 분야 전이 범위 제한 | W04 Commons 원판 P6243, I5206C 실제 edition dump, LCCN 및 GNIS Feature ID 전후 | 외부 인용의 전후 동일 대상 또는 대상 변경, 정정판과 함께 확인 가능 |
