# AF-RES-204 HANDOFF

- 실제 판정: **PARTIAL**. 공개/자가 Nominatim·Photon 4형태 × submit/per-keystroke/offline 12자리 및 목적별 링크/질문/반례 비교는 작성 완료. 원사건의 2022–2025 전체 날짜·번호순 최초 두 건씩이 확정되지 않았으므로 DONE 아님.
- 결과 고정 SHA(이 HANDOFF 직전): `020e8e468f15369abddc54f9613685e09a4277fa`. 시작 c860f8240ab7b7077e2d5b63e438ddd83ff69a27; 계획 050278651b11a2a3a49d45baebf41c707c06b700에서 4커밋 앞섬, 시작 전 차이는 dot-control만. 선행 193 지정 2beb6cb6a1857942c41670458ae32f4895777366 HANDOFF/RESULT 확인.
- [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/RESULT.md), [SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/SELF_CHECK.md), [sources](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/sources.jsonl), [frame](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/frame.csv), [surfaces](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/surfaces.csv), [cases](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/cases.csv), [routes](https://github.com/laadkke-arch/agentflow-open/blob/020e8e468f15369abddc54f9613685e09a4277fa/docs/workstreams/research/AF-RES-204/routes.csv), SCOPE/REFINEMENTS.
- 산입 고유 work 34, 9개 계보: 운영 4/4, 엔진 10/6, 소비자 9/5, 데이터 3/3, Open Library 7/4, 별도 보강 코드 1. 49행 중 15개 미산입, 그중 열람 실패 9. 자료 유형별 최소 직접 열람 자체는 충족. 그러나 엄격 선발 근거만 따로 보수적으로 세면 소비자 0/5, 사건 0/4 확정(4자리 부족). 9개 서로 다른 원사건 중 임시 표본 4와 보강 5. N1 #2677, N2 #2813, P1 #759, P2 #805; #836/#867 보강, #715/#722 host 결측, #726 원본문 적격 조건 결손. #805는 이전 앱 공개 Nominatim + Photon 오프라인 이행 문의이며 성공이 아니다. #759 편입 전 구값과 이유는 REFINEMENTS.md.
- 핵심: 공개 Nominatim의 1 req/s는 앱 전체이며 명시 제출 조건, 자동완성 금지와 LLM/일반 자동결선 플랫폼 제한이 있다. 자체 Nominatim에는 공개 호스트 금지를 복사하지 않되 suggestions 계약도 아니다. Photon은 검색 중 후보 지원, 공개 demo는 공정 사용/제한/가용성 비보장. 직접 운영은 사전 구축 인덱스 또는 import·런타임·버전/갱신 전제. 완전 단말과 LAN 구별, 로컬 후보+명시 제출 가능. Open Library 단건 API 대 월별 배포·적재의 대조. 실제 수치·가격·SLA·오프라인 성공은 미확인.
- ⑤의 고정 SHA에서 9개 대표 파일 전부 fetch_file 재열람 완료. RESULT blob 64ab54fef52de72b87c06c66fba70d2233d16147, SELF_CHECK blob 3eab80b8cddce01e31d77ff56df2d9410663da1f, sources blob 821c5a09afc1b0d09f59bf30e8d753d77e03d0d3. JSONL 49행/산입 34/고유 34, frame 34행, surfaces 12, cases 4, routes 3; 세 표 헤더 일치, 마지막 약점 표 정확히 3행, 결과 끝에 위치 확인. 시작 SHA→⑤ ahead 5, 변경 9파일 모두 owned path. 독립 검토 아님.
- 실제 수행은 GitHub 연결 도구를 이용한 읽기/커밋 및 원문 조회. 새 지오코딩 API 호출, 배포, 공유 서버 부하 측정, 실환경 검사, 새 코드 실행 없음. 로컬 checkout/workbench session/CI 검사도 실행하지 않음. 실행 가능한 checkout/manifest가 없는 웹 조사 환경에서 공유 경로를 수정하지 않았다.

## 순서와 기록

1. 689f45665766a10602210313d3f056f54c768133 — 범위/판정
2. a48b71b2f52971583b5aef259674e7f45f365aa2 — 원문/모집
3. d326bc67e53cae4ad3215ea1b5b4e56841fd39c4 — 12자리/사례/표 초안
4. 0d8a3825713d3ae0130b14a35f65ebe59dbd0b92 — 반례/타 분야/앞선 사례 보정
5. 020e8e468f15369abddc54f9613685e09a4277fa — RESULT/SELF_CHECK
6. 이 HANDOFF — 최종 인계

## 재개 첫 행동 — 엄격 표본 모집 복구

막힌 이유: 웹 Discussion 날짜순 검색 X11–X15는 DisabledError, General 목록은 최신 활동순/일부 카테고리·상태이고 완전한 시계열 아님. REST issue 검색의 키워드/상위 결과만으로 discussion 포함 전수임을 입증할 수 없다. 발견 후보를 임시로 보존했고 누락을 0으로 간주하지 않았다. Codex/권한 있는 실행 환경에서 고정 입력(두 repo, 2022-01-01T00:00:00Z~2025-12-31T23:59:59Z, 제목 아닌 본문 조건, 날짜/번호 오름차순, 결과 독립 선발, 호스트 모호하면 결측)을 적용하여 **전체 page 읽기부터** 실행. 다음 명령은 미실행 제안이며 공개 GitHub metadata 읽기만 수행(새 지오코딩 요청 금지). 인증 권한/gh 버전과 pageInfo 확인 후 사용하고, 실패는 원장에 남긴다. 임시 파일은 /tmp만, 결과 변경은 owned path만.

```sh
git fetch origin
git switch work/research-af-res-204
git rev-parse HEAD
git diff --name-only c860f8240ab7b7077e2d5b63e438ddd83ff69a27 HEAD
gh --version
for repo in osm-search/Nominatim komoot/photon; do
  owner=${repo%/*}; name=${repo#*/}
  gh api --paginate --slurp "repos/$repo/issues?state=all&sort=created&direction=asc&per_page=100" > "/tmp/$name-af204-issues.json"
  gh api graphql --paginate --slurp -f owner="$owner" -f name="$name" -f query='query($owner:String!,$name:String!,$endCursor:String){repository(owner:$owner,name:$name){discussions(first:100,after:$endCursor,orderBy:{field:CREATED_AT,direction:ASC}){nodes{number,title,body,createdAt,url} pageInfo{hasNextPage endCursor}}}}' > "/tmp/$name-af204-discussions.json"
  jq -r '.[]|.[]|select(has("pull_request")|not)|select(.created_at >= "2022-01-01" and .created_at < "2026-01-01")|[.created_at,.number,.html_url,.body]|@json' "/tmp/$name-af204-issues.json" > "/tmp/$name-af204-issues.jsonl"
  jq -r '.[]|.data.repository.discussions.nodes[]|select(.createdAt >= "2022-01-01" and .createdAt < "2026-01-01")|[.createdAt,.number,.url,.body]|@json' "/tmp/$name-af204-discussions.json" > "/tmp/$name-af204-discussions.jsonl"
  cat "/tmp/$name-af204-issues.jsonl" "/tmp/$name-af204-discussions.jsonl" | jq -s 'sort_by(.[0],.[1])' > "/tmp/$name-af204-ordered.json"
done
```

기대 관측: issue PR 제외, discussion 마지막 hasNextPage=false와 에러 없음, 날짜·번호 정렬 후 원본문 확인. 검색 동의어(autocomplete/typeahead/suggestions, offline/local/no internet, public/official/demo endpoint/hostname)로 후보를 넓히되 원문 전체에서 명시 조건과 호스트를 독립 판정. 날짜순 최초 두 적격 사건의 본문 및 운영자 원답변을 직접 열고 주표본을 갱신. X01 #2590 public comparison의 범위 해석 및 #759 실제 비교 적격성을 재검토. 원자료 5번째는 동일 사건의 독립 작성 댓글/구성 문서를 직접 열되 사건 수에 합산하지 않음. 새로운 앞선 후보 발견 시 구값과 근거·수정 이유를 별도 커밋. 정확한 문서 당시 판이 없으면 현재 정책 소급 금지. 지역/단말/데이터 갱신에 관한 성공 사례 추가 탐색; 배포·실행·부하 측정은 이번 범위 밖.

## 색인 반영 제안

AF-RES-204 — PARTIAL; 운영자/host scope × 요청 패턴 × engine contract × dataset/index/runtime를 분리하는 추천 경로, 12자리/34개 고유 직접 근거, 4개 임시 사례(엄격 모집 미확정). 193과의 연결은 목적-제공자 계약 차이 원리만. 최종 제품 스키마·랭킹 결정을 후속 설계자에게 열어 둠. 통합 담당자에게 상태/결과 SHA와 결손 전달; 이 작업에서 dot-control.json 또는 공용 INDEX 수정하지 않음.
