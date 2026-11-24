# AF-RES-164 HANDOFF — PARTIAL

- 결과판 SHA: e7908cc08278e815fc4bf7b57d41c58f4cf571cc (RESULT.md 및 SELF_CHECK.md 포함, 해당 SHA에서 재열람). 이 HANDOFF는 결과판 뒤 마지막 별도 커밋으로 기록한다. 자기 자신을 포함하는 커밋 해시는 파일 안에 자기참조로 기록할 수 없으므로 브랜치 마지막 커밋/외부 완료 기록에서 확인한다.
- 작업 브랜치 work/research-af-res-164; owned_path docs/workstreams/research/AF-RES-164/. 시작 실제 통합판 d32c697b4345442a4c91f62b8fb0bbed19e58034. 계획 ded3420249a3d60ebbb578a8432cf262d3ffa7d7와 비교 4 ahead/0 behind, 변경은 dot-control뿐. 선행 AF-RES-160 고정 result_commit 3e93d6cdaaaa6213682da9d2588677c35b3f2517의 HANDOFF, RESULT, comparisons.csv, SCOPE_CORRECTION 읽음. RUNNING 배정 확인, dot-control 편집 안 함.
- 인계 상태: PARTIAL. 원문 구간 직접 판독 21 고유 저작(교정 포함), 비교 하한에서 교정 제외 20. 원전 범주 보수적 후보 12/22(5/8 소프트웨어 비교,1/5 별도 저자 자료,2/5 후속/비용 원규약,2/2 전사 비교 보고서,2/2 디지털화 비교 보고서). 범주 잔여 10(3+4+3), 총 비(非)교정 원문 수로도 2 부족; 전사·디지털화는 각 2개 동등 품질과 노동까지 충족하지 못함. 완전 전문·부록 판독을 주장하지 않는다. DBLP 자연층 순위/전수 분모 불명: 16 예정 자리 미판독, 조건부 최대 32. API 접근 실패는 0 결과가 아님. 보충층 검색 원순위 미확보. 엄격 G1–G4 물리 단위 대조 0, 같은 연구의 조건부 원척도 대조 2.
- 보존 관측: Lattanzi 1995 실험2 원표 G.1 24인(8/8/8). A 직접 98.125, B 제공 스택 65, C 수정 상속 115.625. A−B=33.125, A−C=−17.5 원척도, A 공유; A/C 유의 차이 미검출. 24/24 각 단계합 검산 일치. 표5.3 Hours와 기록 양식·G.1 척도 관계 미확인: 분·인시로 바꾸지 않음. 공통 인수는 저자 보고뿐, 개별 검수표·실제 코드 미확보. 생산자/사전 숙련/유지 비용과 전체 절감은 미확인. S07 59h 견적 vs40h 실측은 직접팔 부재로 계산 금지.
- 파일: SCOPE.md, frame.csv, sources.jsonl, studies.csv, arms.csv, contrasts.csv, lattanzi-raw.csv, COUNTEREXAMPLES.md, RESULT.md, SELF_CHECK.md, HANDOFF.md. 결과 원장 38/41/18/23/20/24행(sources/frame/studies/arms/contrasts/raw). 
- 검증: GitHub에서 각 묶음 커밋 및 대표 파일 재열람; RESULT/SELF_CHECK 결과판 재열람. 원격 CSV 원시 숫자 합계 JS 재검산만 실제 실행. 제품 실행·빌드·대량 재생·원자료 재통계·독립 검토 없음.

## 묶음별 대표 커밋
| 묶음 | SHA | 대표 재열람 |
|---|---|---|
| ① 범위 | 6ffcf9e45cb44ac2de27b81ab527fdc67760bee2 | SCOPE.md |
| ② 모집 | d43575f8b10d3e230e6b86b7fac300aee489cf0c | frame.csv |
| ③ 관측 | 2de105458e771057edebef35456dfa0f657003d0 / 20c410754bb9f3ac36b4d4efa2d387676fe8e823 | lattanzi-raw.csv / contrasts.csv |
| ④ 반례/보강 | 72490a318f8a9937964fa80e398b85d4dd169d59 / 8456b9cf4608fb2a8d9043b3c9a7091fbab0a9c4 / af5067234cae16a2e75cc652129b961e43b0dba9 | COUNTEREXAMPLES.md / sources.jsonl / contrasts.csv |
| ⑤ 결과·자기검산 | 90e2e43bfd3a81de5f82521dff66a44842c9fc83 / e7908cc08278e815fc4bf7b57d41c58f4cf571cc | RESULT.md / SELF_CHECK.md |

## 다음 첫 행동: 자연 모집 복원 (공개 재개 입력)
Codex에서 아래 공개 자료 다운로드와 정렬을 먼저 재현한다. 아직 실행하지 않은 명령이다. XML이 당일 스냅샷과 달라질 수 있으므로 실제 UTC 다운로드 시각·해시와 검색 결과를 새 원장에 기록하고 원판 보존. 제목에 키워드가 없는 연구를 임의 보강해 자연층을 채우지 않는다. 다운로드 실패 시 DBLP ESE/TSE/ESEM 연도별 발행 목록과 Springer/IEEE/ACM 원 발행 목록에서 같은 기준으로 전수 확인. 원출처 링크에서 첫 8편씩 전문·부록을 연다. 실제 양쪽 구현이 2편 미만이면 다음 8편. 각 기간의 부족·제외·미열람 수를 원분모로 기록.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-164
git switch --track origin/work/research-af-res-164 # 로컬 브랜치가 없을 때
git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 HEAD
git status --porcelain
mkdir -p /tmp/af-res164-dblp
cd /tmp/af-res164-dblp
curl -fL https://dblp.org/xml/dblp.xml.gz -o dblp.xml.gz
curl -fL https://dblp.org/xml/dblp.dtd -o dblp.dtd
gzip -dc dblp.xml.gz > dblp.xml
sha256sum dblp.xml.gz dblp.dtd
date -u
# Python 환경에 lxml이 있는지 확인하고 없다면 별도 승인/가용 환경에서 실행.
python - <<'PY'
from lxml import etree as E
import re,json
from pathlib import Path
groups=[r'\b(?:reuse|component|library|framework)\w*\b',r'\b(?:effort|time|productivity)\w*\b',r'\b(?:experiment|empirical|comparison)\w*\b|\bsame task\b']
prefix=('journals/ese/','journals/tse/','conf/esem/')
rows=[]
for _,e in E.iterparse('dblp.xml',events=('end',),tag=('article','inproceedings'),load_dtd=True,resolve_entities=True,no_network=True):
    key=e.get('key','')
    if key.startswith(prefix):
        y=e.findtext('year','')
        t=e.find('title')
        title=''.join(t.itertext()) if t is not None else ''
        if y.isdigit() and 1990<=int(y)<=2025 and all(re.search(g,title,re.I) for g in groups):
            doi=next((u.split('doi.org/',1)[1] for u in e.xpath('ee/text()') if 'doi.org/' in u),'')
            rows.append(dict(year=int(y),title=title,key=key,doi=doi,ee=e.xpath('ee/text()')))
    e.clear()
    while e.getprevious() is not None: del e.getparent()[0]
seen=set()
for i,j in [(1990,2007),(2008,2025)]:
    matched=sorted((r for r in rows if i<=r['year']<=j),key=lambda r:(r['year'],r['title'].casefold(),r['doi'] or r['key'],r['key']))
    kept=[]
    for r in matched:
        identity=r['doi'].casefold() if r['doi'] else (r['title'].casefold(),r['year'])
        if identity in seen: continue
        seen.add(identity);kept.append(r)
    print(json.dumps(dict(period=[i,j],returned=len(matched),unique=len(kept),ordered=kept),ensure_ascii=False))
PY
```

주의: 위 코드는 공개 XML 제목 기반 재현 초안(표제 형태 변화·DTD/메모리·별칭/저작 중복 수작업 확인 필요), 실행 결과 아님. SCOPE의 제목/서지 검색식 및 공개 저자 보관소 보완과 대조하여 후보 원순위·DOI·중복판 사유를 기록한다. XML 수집 자체는 전문 판독으로 산입하지 않는다.

## 두 번째 재개 입력: 원표 단위·검수
S06 공개 PDF: https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content ; Table 5.3/5.5, App D/E/G, 인쇄 pp.78–89,165–173. 1998 후속판 후보 https://www.sciencedirect.com/science/article/pii/S0164121297100139 (원문 미확인; 같은 계보 여부 및 단위 확인용으로만). PDF 단위가 명확해져도 제출별 검수표와 관측창이 없으면 동등성 조건부 유지. 
```sh
curl -fL 'https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content' -o /tmp/af-res164-lattanzi.pdf
pdftoppm -f 87 -l 88 -png /tmp/af-res164-lattanzi.pdf /tmp/af-res164-table
pdftoppm -f 174 -l 178 -png /tmp/af-res164-lattanzi.pdf /tmp/af-res164-task
pdftoppm -f 182 -l 182 -png /tmp/af-res164-lattanzi.pdf /tmp/af-res164-raw
# PDF 판/쪽번호 달라지면 pdfinfo 및 인쇄 페이지로 다시 찾는다.
cd "$(git rev-parse --show-toplevel)"
python - <<'PY'
import csv,collections
rows=list(csv.DictReader(open('docs/workstreams/research/AF-RES-164/lattanzi-raw.csv')))
g=collections.defaultdict(list)
for r in rows:
    total=sum(int(r[x]) for x in ['design','library','code','debug'])
    assert total==int(r['printed_total'])==int(r['computed_total'])
    g[r['group']].append(total)
assert len(rows)==24
assert {k:(len(v),sum(v)) for k,v in g.items()}=={'A':(8,785),'B':(8,520),'C':(8,925)}
m={k:sum(v)/len(v) for k,v in g.items()}
print(m,m['A']-m['B'],m['A']-m['C'])
PY
```
기대 관측: 24행 합 일치, 98.125/65/115.625, 33.125/−17.5; 단위 확정 이전에는 원척도만. 원본 개별 채점/실제 코드 입수 시 합격 기준과 제출 목록을 R1–24에 연결. 논문 독립 반복 연구를 확보해도 동일 관측계보 중복 제외. Q7: S17 File3 표40/본문42의 정정과 최종 오류점수, S18 평가 14/19 원분모, S14/S20 동일 원물의 작업자 인시·공통 합격선을 추가 조사. 
색인 제안: AF-RES-164 — 동일 납품·직접/재사용 노동: Lattanzi 원척도 양방향 대조(물리 단위 미확인), 모집/품질/원장 하한 PARTIAL, RESULT.md 및 SELF_CHECK.md 참조.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| DBLP 전체 결과와 원순위 미복원, 보충층 편향 | 일반 빈도·기간별 대표성·22저작 범주 하한 | DBLP 공개 XML과 발행 목록 정렬·중복 제거, 최초 8+8 및 조건부 추가 | 자연층 독립 연구 중 완전한 G1–G4 짝 및 반대 부호 |
| Lattanzi 표의 시간 단위 의문, 개별 제출·인수표 부재, A/C 비유의 | 33.125 및 −17.5의 물리 인시·일반화 | S06 G.1/App E 원기록 단위, 1998 후속판·저자 정정, 제출/채점표 | 분/시간 확정과 동등 검수, 누락 순증가가 해당 원척도 차이를 넘는 실측 |
| 전사·디지털화 품질/오류·역할·탈락 불일치, 기계시간 혼입 | 타 분야의 절감 수치 전용 및 완결성 | S17 표/본문 정정, S18 미평가 5개, S14/S20 작업자별 시트·같은 합격선 | 원물 동일·검수/정정 포함·실패 원분모 복구 후 양팔 활동 인시의 반대 방향 |
