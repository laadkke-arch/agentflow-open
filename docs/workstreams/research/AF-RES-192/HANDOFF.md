# AF-RES-192 HANDOFF

- 상태: **PARTIAL** (핵심 역할 분기 및 4판 배포 레코드 확인, exact archive DOI/개념 DOI 이동 미확인). 자기점검 완료, 독립 검토 없음. 실제 모델 UI 확인 안 됨.
- 작업 브랜치: work/research-af-res-192. 계획 기준 0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6, 시작 foundation 72cf39aea54e2de2ba78a245593aefdc40205a16. 의존 AF-RES-184 2b83f0fa4f86e97b9643eafaeecc6596cd245561 (중앙 DONE/자체 PARTIAL) 고정 입력 읽음. 다른 동시 과제/186 의존 없음.
- **결과 직전 고정 SHA: 54863994cbf6ddee1aacc385679bf3fad2326306**. 대표 파일 [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/SELF_CHECK.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/sources.jsonl), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/frame.csv), [objects.csv](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/objects.csv), [changes.csv](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/changes.csv), [routes.csv](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/routes.csv), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/SCOPE.md).
- 검증: 위 SHA에서 RESULT/SELF_CHECK/sources/routes readback; foundation compare ahead 12/behind 0, 추가 파일 8개 전부 owned_path. 중간판 28eaf059...에서 50 JSONL unique IDs, CSV widths 0 errors, 16 routes, Q1–Q7 및 마지막 약점 3행, SHA256 형식 8/8 확인. HANDOFF는 이후 마지막 커밋. dot-control.json 및 색인 직접 수정 안 함.
- 범위: 2025-12-31 UTC cutoff seaborn v0.13.2/v0.13.1, MAPIE v1.2.0/v1.1.0. 저자 CFF/README 4/4, PyPI exact-version file records 4/4, 8 파일명·발행자 SHA256 기록, P01 JOSS 및 P02 PMLR 선호 논문, P03 old arXiv 및 P04 별도 알고리즘. 36개 직접 고유 자료(규칙5/저자태그 등13/논문4/릴리스·보관8/타 분야6), 보수적 32 work_id, 50행 원장(14 제외), 7 coarse lineage IDs; 4 release events, 4 paper works; 배포 기록은 사건 수와 별개. 종류별 부족 0.
- 핵심 관측: seaborn 두 판 동일 CFF/README 및 JOSS DOI, 다른 파일; CFF 권호 반전. JOSS가 연결한 software archive DOI 10.5281/zenodo.4645478는 v0.11.1, 10.5281/zenodo.8393472는 v0.13.0(둘 다 선택판 아님). MAPIE preferred Cordier 2023 PMLR은 DOI 미기재, old DOI는 Taquet arXiv 2022 (CFF 2021 오류); 두 버전 다른 파일. MAPIE CrossConformalClassifier.predict_set의 agg_scores="crossval"만 Romano Algorithm2를 따른다고 두 태그 소스 명시(기본 mean과 구분). seaborn relplot 인자 논문 예제↔두 태그 API 연결. 인용/원리/설치/과거판의 첫 링크 분리; 단일 목적에서 하나로 충분한 대조 존재. 도서 번역자·부분/전체, 원곡/편곡/편곡의 출판판 분리.
- 미확인: 4/4 선택판 archive DOI, 2/2 계보 concept DOI 및 조회일 actual redirect, PMLR 별도 DOI 존재, 과거 archive metadata, 정확한 release timezone/seconds/일부 전체 commit SHA와 GitHub asset filenames, 실제 package bytes 및 provenance 독립 검증. 표본 내 공식 권고 자체 없는 판 없음(0 관측; 외삽 금지). 실제 version DOI/개념 DOI가 같은 도착점을 갖는 사례는 규칙 수준만. 실제 설치·빌드·코드 실행·수학적 동등성 확인·사용자 클릭 실험 하지 않음. source ID F02–F06 접근 실패/미발견. 조회일 UTC 2026-11-24, 정확 초 미확인.
- **첫 재개 행동:** Codex Cloud에서 공개 API 읽기만 사용해 Zenodo record 8393472의 conceptrecid/conceptdoi, related_identifiers, versions 및 선택 4판 title/version/tag를 대조한다. 접근 실패하면 HTTP status/error를 보존하고 보류 유지. DOI absence를 추정하지 말 것. 새 빌드/재현 실험은 이 과제에서 제외. 실제 파일 검증 필요시 후속 별도 작업으로 분리.
- 색인 제안(편집 담당자): AF-RES-192 / 같은 repo의 논문·방법·버전 링크 목적별 분리 / PARTIAL / docs/workstreams/research/AF-RES-192/RESULT.md / AF-RES-184 fixed 2b83f0fa... / exact archive·concept DOI 미확인, 선호 DOI와 배포 버전 혼동 금지.

## 후속 실행 입력·명령 (미실행)
환경: Codex Cloud, 기존 공개 네트워크/일반 curl+Python3, 로그인·유료 API·권한 우회 금지. 임시 원자료는 /tmp, Git 변경 시 AF-RES-192 owned_path만. 브랜치 최신 상태 재확인 후 재개하며 아래는 원자료 조회이지 신규 빌드가 아니다. HTTP error는 성공으로 기록하지 않는다.

```sh
git fetch origin
git checkout work/research-af-res-192
git rev-parse HEAD
git diff --name-only 72cf39aea54e2de2ba78a245593aefdc40205a16..HEAD
mkdir -p /tmp/af192
cd /tmp/af192
date -u +%FT%TZ > retrieved_at.txt
curl -fLsS -D z8393472.headers -o z8393472.json 'https://zenodo.org/api/records/8393472'
curl -fLsS -D z4645478.headers -o z4645478.json 'https://zenodo.org/api/records/4645478'
curl -fLsS -D dc8393472.headers -o dc8393472.json 'https://api.datacite.org/dois/10.5281/zenodo.8393472'
curl -fLsS -G --data-urlencode 'q=metadata.title:mwaskom/seaborn' --data-urlencode 'all_versions=true' -o seaborn-records.json 'https://zenodo.org/api/records'
curl -fLsS -G --data-urlencode 'q=metadata.title:MAPIE' --data-urlencode 'all_versions=true' -o mapie-records.json 'https://zenodo.org/api/records'
python3 - <<'PY'
import json
from pathlib import Path
for p in Path('.').glob('*.json'):
    try: j=json.loads(p.read_text())
    except Exception as e:
        print(p, 'UNREADABLE', type(e).__name__); continue
    rs=j.get('hits',{}).get('hits',[]) if 'hits' in j else [j]
    for r in rs:
        m=r.get('metadata',{}); a=r.get('data',{}).get('attributes',{})
        print(p, r.get('id'), r.get('doi'), r.get('conceptdoi'), r.get('conceptrecid'),
              m.get('title'), m.get('version'), m.get('related_identifiers'), a.get('relatedIdentifiers'))
PY
# Only if actual concept DOI is found:
# curl -fLsS -D concept.headers -w '%{url_effective}\n' -o concept.html "https://doi.org/$VERIFIED_CONCEPT_DOI"
# For release published_at and asset names, if public endpoint is accessible:
curl -fLsS 'https://api.github.com/repos/mwaskom/seaborn/releases/tags/v0.13.2' -o seaborn-0132-release.json
curl -fLsS 'https://api.github.com/repos/mwaskom/seaborn/releases/tags/v0.13.1' -o seaborn-0131-release.json
curl -fLsS 'https://api.github.com/repos/scikit-learn-contrib/MAPIE/releases/tags/v1.2.0' -o mapie-120-release.json
curl -fLsS 'https://api.github.com/repos/scikit-learn-contrib/MAPIE/releases/tags/v1.1.0' -o mapie-110-release.json
```

관측 기준: 정확판은 version/tag 일치 및 관계 방향 근거가 있을 때만 연결. 목록 pagination/검색 실패는 미발견이지 부재가 아니다. concept DOI는 실제 UTC와 최종 URL을 보존하고 선택판 DOI와 비교; 개념/판 관계 역전 금지. release JSON의 published_at UTC 및 assets[]를 읽고 G01/G02와 비교. 새 관측으로 판정 바뀌면 이전값·이유·source ID를 다음 커밋에 기록.
