# AF-RES-246 HANDOFF
**PARTIAL** — 세 제목 중 Secretary/Raptors 실제 소장·책 존재 근거를 확보했고 음악 비교의 원레코드/규칙을 확인했다. 두 실제 기관 전거 0/2, 지정 세 저작→전거 및 역방향 각각 0/3(확보 수), 실물/원출판사 목표 판 0/3, 교육 가공 명시 0 확보. 따라서 실제 두 사람 동일/별개 여부와 현행 저자 URI 모두 보류. 자료별 책/기관 하한 미달. 검색 실패를 부재로 해석하지 않는다.

## 고정 입력과 결과
- 저장소 laadkke-arch/agentflow-open, 작업 브랜치 work/research-af-res-246, 허용경로 docs/workstreams/research/AF-RES-246/. 통합 착수 254af7b27432337b01ee8e636c5aa6d67df05fa8. 진행표 blob 101bea49f1e22cc6a1ded054293b261d4e037c92 (contents empty→blob), task RUNNING attempt 1, depends_on 233. 계획 7369707441e2eb70e84004ca6cb3bfeefc8b4061; 계획 전체 diff 미실시. 의존 AF-RES-233 중앙 DONE/자체 PARTIAL 고정 08685fe6a837db69ffc5a34b0c1dd0eccbfa4918, HANDOFF/RESULT/works.csv/unresolved.md/authority.csv 읽음. 238–242 결과/정답 사용 안 함.
- ① 사전 범위·예측 446af5cec7cc270e60620efba65d9dc7da7233c2 (외부 추가 답 열기 전).
- ② sources.jsonl ca8ce64463fdfbcf0f5ee7fc7a0021a545718c63.
- ③ TABLES 4e878402bb563c76293a4eba065cf811434e7856; editions a582baedbb8b605edd9b414535c53764a7a89ea9; links 02448970254742ff0bdba6b57faeb5eff29e3fd1.
- ④ 보강 원장 4bb612da1d59b8bc27c52bbbf945ed36ec0905a3; 판/링크 정정 71ad1af41ff34d6847744805897effd4953948c8 / df3e9907fc35420ed11b9b1087e2dce0b17388ad; 반례 b23ee5208f0cb6acca57c57d2560a461f585fcfb.
- ⑤ RESULT b9ec239a2d30c298689a31e77f6eb276d20245ae; **최종 고정 결과 SHA(HANDOFF 직전) 6dea82cf016b980cb88948884baf4982e9227dfb**. ⑥ 이 HANDOFF만 단독 마지막 commit. 자기 SHA는 본문에 쓰지 않음.

대표 파일: [RESULT.md](RESULT.md), [sources.jsonl](sources.jsonl), [editions.csv](editions.csv), [links.csv](links.csv), [negative-searches.md](negative-searches.md), [SELF_CHECK.md](SELF_CHECK.md), [SCOPE.md](SCOPE.md), [TABLES.md](TABLES.md) (03 당시 snapshot; 04 보강은 최종 RESULT).
고정 결과 SHA에서 실제 GitHub 재열람 8/8 및 자체 구조 대조: JSONL 70행 정상 parse, counted 21 unique work IDs, 9 표시 lineage, 중복 source_id 0, 필수 키 누락 0, 파일 내 참조한 source ID 미등록 0. editions 3행·15열, links 12행·13열, target 및 control 각각 forward/reverse 3행씩. 필수 두 표 첫 내용, 표 1 3행×6열, 표 2 4행×5열, Q1–7 존재, 마지막 약점 3행. 통합 착수→고정 결과 +11/-0, 변경 파일 8개 전부 owned_path. dot-control 수정 없음. 이는 파일 및 자체 근거 대조이지 외부 endpoint 재호출, 제품 검사, 독립 검토가 아님. 독립 검토/바이너리 실행/반복 계측 미실시.

## 결과와 미달
- Q1 교육 자료 두 자리와 세 표제는 233 판독과 이번 색인 대조. 교육 원본 일반 부분은 직접 열람, 지정 Exercise 페이지와 강사용 원본은 429; 가공 여부 미확인.
- W1 Rough road: ISBN 9781584760412 후보만, 원판/책임표시 없음(E0). C04 정관사 정규화 제목 충돌, F20 타 이름 역할 미확인.
- W2 Secretary: B01 익산 실제 소장 표시 by Kate Davis, Blackbirch Press 2001, 9781567116649, reckey 125966365, species_key 125966363. 교육 CIP 2003과 상충, community 2002. E1 후보 소장 링크까지.
- W3 Raptors: B02 Boise/B03 LGNC/B05 FVCC, B04 조직 신간 소개(2002 표시), C06 PW 2002-08-12 가을 출판 예정으로 존재 보강. 2002 Kate Davis Mountain Press, OCLC 49512043/LCCN 2002004917/ISBN 9780878424610는 원행 미확인 후보. E1 후보 책 링크. 현행 인물 1959 날짜 미확인.
- 음악 M01 지정 work, M02 Cohen(lead vocals), M03 Buckley(artist credit/live cover, 구체 vocal/instrument 관계 미확인): work 1/1 및 recording 2/2 양방향 표시. M05 performance type ID 278 및 M06 composer/lyricist type. 동일 DB 계보 1, 도서 공석 대체 금지.
- 직접 산입 21 (교육·규칙 10/4, 책·출판·소장 4/6, 기관 자체 서지/전거/변경 1/5, 음악 6/5), 보강 6, 미산입 43. 엄격 출판사/소장/표제면 정의에서 B04 제외하면 20/책 3; E01 지정 페이지 직접 재열람 조건 추가 시 19. 책/기관별 하한 미달. 3 지정 제목 중 부분 2·결측 1, 양방향 완결 0, 대조 3조합 미결. 실제 정상 빈 검색 결과 관측 0. 모든 검색엔진 후보 URL을 보존한 것은 아니며 주요 실제 방문/실패 경로 기록. 개별 UTC 미기록(조사창).
- 사전 E0→E1→E2→E3 tier 유지. E2/E3는 실제 원행 검증 전 발행 금지. 두 교육 slot만 별도, 실제 실체 merge/split 보류.

## 재개 첫 행동 및 실행 담당 입력 (미실행)
1. 먼저 Raptors 원기관 서지부터: 정상 브라우저 LC Catalog https://catalog.loc.gov/ 에서 exact title + author, ISBN 9780878424610/087842461X 및 LCCN 2002004917. OCLC https://boisestate.on.worldcat.org/oclc/49512043 또는 Boise 소장 담당의 원 MARC export와 비교. 실제 010/020/040/245c/260/264/100/700($a,$d,$e,$4,$0,$1)/035/005 기록; 번호가 서로 다른 대상/판이면 후보 철회. 정상 결과에 실제 agent/authority ID가 있으면 그 ID로만 역방향 원행 요청. $0/$1 없으면 문자열 일치와 원행 공석을 별도 기록, 무리한 추정 URI 생성 금지.
2. 익산 B01 소장 상세의 실제 책 표제면/verso와 기관 MARC 요청, ISBN 9781567116649 및 Blackbirch 2001/2003 CIP를 대조. Rough road 9781584760412의 iKids 원출판 목록·실물·기관 서지에서 Bob Filipowich와 Kate Davis 역할 확인. 제목/ISBN이 충돌하면 판 구분. 2×3 조합의 두 방향을 업데이트.
3. 정상 공개 원기관 레코드 다운로드 예시(실행하지 않음; 접근 제한을 우회하지 않으며 403/429시 해당 요청 중지):
```sh
git fetch origin
git show 6dea82cf016b980cb88948884baf4982e9227dfb:docs/workstreams/research/AF-RES-246/RESULT.md
git diff --name-only 254af7b27432337b01ee8e636c5aa6d67df05fa8...6dea82cf016b980cb88948884baf4982e9227dfb
# Candidate bib (format endpoint availability unverified; if invalid use normal catalogue export)
tmp=$(mktemp -d)
date -u
curl --location --fail --max-time 30 -D "$tmp/bib.headers" \
  'https://lccn.loc.gov/2002004917/marcxml' -o "$tmp/bib.xml"
# inspect HTTP and MIME; if actual MARCXML obtained:
python3 - "$tmp/bib.xml" <<'PY'
import sys, hashlib, xml.etree.ElementTree as E
b=open(sys.argv[1],'rb').read()
print("sha256",hashlib.sha256(b).hexdigest())
r=E.fromstring(b)
for x in r.iter():
    if x.attrib.get('tag') in {'001','003','005','010','020','035','040','100','245','250','260','264','700'}:
        print(x.attrib, x.text if not len(x) else [(s.attrib.get('code'),s.text) for s in x])
PY
# Replace ID only with actually observed authority ID (not bib LCCN).
# curl --location --fail --max-time 30 -D "$tmp/auth.headers" \
#   "https://id.loc.gov/authorities/names/ACTUAL_ID.marcxml.xml" -o "$tmp/auth.xml"
# parse same as above with tags 005,010,100,400,500,670; inspect $a/$z, $d and source notes.
```
위 endpoint 경로는 다음 시험 입력이며 성공/유효한 형식 미관측. 정상 MARCXML record와 실제 대상 확인 전 응답을 근거로 세지 않는다. 원영수증 단위: URL+query, UTC, HTTP status/headers, 본문 SHA256, 원 MARC field/value 또는 BIBFRAME RDF agent, 판/역할, 공급기관 040/035. 정상 빈 집합과 실패 구분. 실제 010/005/100/670 판·책 역할 일치시 해당 한쪽만 E3 승격; 다른 역할/판/날짜나 교체 확인시 별도 기록. 
4. 강사용/학습용 교육 PDF Module 4 Exercises-1 및 서문 편집 방침(동일 원출처, 영상/원문)에서 modified/fictitious 등 명시 확인. 없으면 교육 성격 미확인 유지. 실제 기관 변경 결정(유효/취소 번호) 확인. source quotas의 남은 출판/기관 원자료 확보 및 별도 독립 검토 요청.

## 색인 제안
AF-RES-246 PARTIAL: bibliographic reverse lookup, education citation vs live authority, 245c/020/010/005/670/100/700 $0/$1/$e/$4, edition/role provenance, work↔recording, source lineage, unresolved-candidate UI. AF-RES-233의 B 빈칸을 일부 책 소장 링크로만 보강, 실제 authority 0/2는 그대로. 중앙 진행표·INDEX는 통합 담당이 갱신.
