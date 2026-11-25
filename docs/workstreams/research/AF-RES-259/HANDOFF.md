# AF-RES-259 HANDOFF

**자체 상태: PARTIAL**. 고정 결과 SHA **0b8a45bc2f7f5869565f2951489c662da8a1de7a**. [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/RESULT.md) · [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/SELF_CHECK.md) · [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/sources.jsonl) · [orgs.csv](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/orgs.csv) · [attributions.csv](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/attributions.csv) · [changes.md](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/changes.md) · [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/SCOPE.md) · [RC 원행](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/ror-release-records.json) · [rename 원행](https://github.com/laadkke-arch/agentflow-open/blob/0b8a45bc2f7f5869565f2951489c662da8a1de7a/docs/workstreams/research/AF-RES-259/rename-records.json).
작업 브랜치 work/research-af-res-259, 착수 9eeb7105c7edec2c5c4c0a1f722916b9d664b236, AF-RES-246 의존 고정 28896307db15beb91d8550d6e95ec3317c8f6c36. 결과 고정 뒤 compare 재조회: ahead 12 / behind 0, 변경 9파일 전부 owned_path 내부, 외부 경로 0. SELF_CHECK 파일 blob e1a49cefe53b2ca5ab2ef6f72cbd7368988df8d9. dot-control 수정 안 함. 이 HANDOFF는 그 뒤 단독 커밋. 별도 독립 검토·신규 제품 실행 없음.

## 완료·미달
- 43개 고유 work_id / 14 공급계보, 73행 원장(성공 47, 실패 26, 중복 성공 4 미산입). 그룹 하한 지명 원행 3/6, 운영자 10/4, 역사 5/4, 당대 원문 후보 4/4, 통제 11/4. 보조 10. 총수 초과로 지명 원행 및 표집 미달을 덮지 않음. UTC 날짜만, 개별 시각 영수증 미수신.
- 소르본 2018-01-01, 알토 2010-01-01 공식 전환 확인. 알토 제3 전신 모집 제외. v2.5 RC에서 025xed883·01yvrd251 inactive → 02en5vm52 active 및 역 predecessor 둘, 4/8 명시·4/8 미수신·정상 공석 0/8. v2.13 후계 역방향 유지. 현행 API/생산 ZIP 0/6. Aalto 020hwjq30 외부 등록부 후보, 두 전신 및 관계 미수신.
- UPMC에 EQAR 011htkb76과 RC 01yvrd251 불일치, 2015 협의체와 2018 대학에 동일 02en5vm52의 범위 충돌. 현재 매핑은 보류. 생산 ZIP before/after 판별 미완료.
- 출판물 후보 4/4 실제 소속 위치 확인, 사전 지정 시간순+DOI 최초 적격 표집 0/4. P03 출판자 2009와 Pure 2010 불일치; HAL 현재 컬렉션과 과거 소속 다름. 원문 유지와 현재 링크 분리 필요.
- Sumy 동일 ID rename은 완료 통지와 실제 RC 불일치 및 다음 판 정정, Neuro-SU parent/child는 동일 판 양쪽 관계 확인. IANA AN Preferred-Value 공석·YD→YE 구분. 원문 역사·현재 연락·검색 alias 세 목적의 링크 대안과 철회 조건 도출. 등록기관 status를 저자/연구실/논문 전체에 소급하지 않음.

## 다음 첫 행동 — Codex 네트워크 접근 가능한 환경에서 생산판 확보
웹 도구에서 ROR API 직접 요청 및 Zenodo ZIP 미수신. URL 표면과 발행 목록만 성공했고 실제 생산 행이 아님. 아래 **실행하지 않은** 명령을 권장한다. 입력판은 Z01 v2.4(18985120), Z02 v2.5(19356124), Z03 v2.16(24378467). 최신 릴리스가 달라져도 먼저 이 셋 고정. API 메타데이터에 게시된 파일 링크/체크섬을 이용하고 RC와 비교. 쓰기는 임시 경로 또는 owned_path만. 실패 시 HTTP 코드와 응답을 남기고 성공으로 세지 않음.
```bash
cd "$(git rev-parse --show-toplevel)"
git rev-parse HEAD
git diff --name-only 9eeb7105c7edec2c5c4c0a1f722916b9d664b236 HEAD
export TMP259="$(mktemp -d)"
python - <<'PY'
import os, json, hashlib, zipfile, urllib.request, pathlib, datetime
d=pathlib.Path(os.environ["TMP259"])
ids={"025xed883","01yvrd251","02en5vm52","011htkb76","020hwjq30","020kwj692"}
names=["paris-sorbonne","paris sorbonne","pierre et marie curie","pierre-et-marie-curie","pierre and marie curie","sorbonne university","sorbonne université","aalto university","aalto-yliopisto","helsinki university of technology","teknillinen korkeakoulu","helsinki school of economics","helsingin kauppakorkeakoulu","university of art and design helsinki"]
for ver,rid in [("2.4",18985120),("2.5",19356124),("2.16",24378467)]:
    api=f"https://zenodo.org/api/records/{rid}"
    try:
        with urllib.request.urlopen(api,timeout=90) as response:
            meta=json.load(response)
            print("META",ver,datetime.datetime.now(datetime.timezone.utc).isoformat(),response.status,response.geturl())
        (d/f"{ver}-meta.json").write_text(json.dumps(meta,ensure_ascii=False))
        files=[f for f in meta["files"] if f["key"].endswith(".zip")]
        if len(files)!=1: raise ValueError(f"select actual ROR release ZIP from metadata: {files}")
        f=files[0]; url=f["links"].get("content") or f["links"]["self"]
        z=d/f"{ver}.zip"; algo,expected=f["checksum"].split(":",1)
        h=hashlib.new(algo)
        with urllib.request.urlopen(url,timeout=180) as response,z.open("wb") as out:
            print("ZIP",ver,response.status,response.geturl(),datetime.datetime.now(datetime.timezone.utc).isoformat())
            while chunk:=response.read(1024*1024):
                h.update(chunk);out.write(chunk)
        assert h.hexdigest()==expected,(ver,h.hexdigest(),expected)
        print("CHECKSUM",ver,algo,h.hexdigest())
        with zipfile.ZipFile(z) as zp:
            print("MEMBERS",ver,zp.namelist())
            js=[n for n in zp.namelist() if n.endswith(".json") and ("schema_v2" in n or "schema-v2" in n)]
            if len(js)!=1: raise ValueError("inspect members and choose actual schema v2 JSON")
            data=json.loads(zp.read(js[0]))
            if not isinstance(data,list): raise ValueError("inspect JSON schema and do not assume records")
            found=[]
            for r in data:
                ri=r["id"].rsplit("/",1)[-1]
                nv=[n["value"].casefold() for n in r["names"]]
                if ri in ids or any(k in v for k in names for v in nv):
                    found.append(r)
            (d/f"{ver}-matches.json").write_text(json.dumps(found,ensure_ascii=False,indent=2))
            print("ROWS",ver,len(data),"MATCH",len(found))
            for r in found:
                print(json.dumps({k:r.get(k) for k in ("id","status","names","relationships","admin","established")},ensure_ascii=False))
    except Exception as e: print("FAIL",ver,repr(e))
PY
for id in 025xed883 01yvrd251 02en5vm52 011htkb76 020hwjq30; do
  curl -sSL --max-time 40 -D "$TMP259/api-${id}.headers" -o "$TMP259/api-${id}.json" -w '%{http_code} %{url_effective}\n' "https://api.ror.org/v2/organizations/$id"
done
for name in 'Helsinki University of Technology' 'Helsinki School of Economics' 'Teknillinen korkeakoulu' 'Helsingin kauppakorkeakoulu' 'Aalto University' 'Paris-Sorbonne University' 'Université Pierre-et-Marie-Curie'; do
  for extra in default all_status; do
    # all_status is documented by R03; confirm syntax in fixed docs before run
    if [ "$extra" = all_status ]; then arg='&all_status'; else arg=''; fi
    # urlencode name in the API query, preserve HTTP headers and body by query key
    key="$(printf '%s_%s' "$name" "$extra" | sha256sum | cut -c1-12)"
    curl -sSL --max-time 40 -G --data-urlencode "query=$name" -D "$TMP259/query-$key.headers" -o "$TMP259/query-$key.json" -w '%{http_code} %{url_effective}\n' "https://api.ror.org/v2/organizations?${arg#&}"
  done
done
```
정상 기대: checksum 일치한 전체 행으로 존재/명시/공석/미등재 구별; 2.5의 두 inactive와 후계 관계가 RC와 일치할지 확인하고 2.4/2.16의 변화(새 ID, alias 제거, 관계 누락 또는 철회)를 그대로 기록. 011htkb76이 다른 scope/withdrawn/정상 행이면 UPMC 후보 판정 재검토. Aalto 과거 이름이 단지 후계 alias인지 별도 inactive인지 또는 미등재인지 구분. 실패 응답/0-hit 검색을 전체 판 미등재로 처리하지 말 것. 실제 raw API와 생산 ZIP, 관측 UTC, HTTP, release version, hash, JSON path, 원행 및 검색 전체 페이지를 영수증에 보존. 검색 예시는 첫 페이지 호출만이므로 all_status 결과의 pagination까지 별도 수집·검증해야 한다.

## 그 다음 행동 — 표집 재현
입력 창은 Sorbonne [2017-01-01,2018-01-01), [2018-01-01,2019-01-01), Aalto [2009-01-01,2010-01-01), [2010-01-01,2011-01-01). 출판일은 실제 출판자 first published, DOI 소문자 사전순 tie-break. HAL [API 문서](https://api.archives-ouvertes.fr/docs/)에서 실제 스키마/collection 확인 후 예시 GET:
```bash
curl -sSL --max-time 60 -G 'https://api.archives-ouvertes.fr/search/' \
  --data-urlencode 'q=collCode_s:SORBONNE-UNIVERSITE AND producedDateY_i:[2017 TO 2018]' \
  --data-urlencode 'fl=halId_s,doiId_s,producedDate_s,uri_s,fileMain_s,structName_s,collCode_s' \
  --data-urlencode 'rows=100' --data-urlencode 'start=0' -o "$TMP259/hal-page0.json"
```
위 필드명·컬렉션은 실행 전 문서와 실제 응답 검증(예비 입력, 정확 동작 미확인). numFound와 start/page 전체, 다른 Sorbonne/전신 컬렉션 포함 여부 및 중복 DOI 체크. Aalto [공식 Pure 연구결과](https://research.aalto.fi/en/)에서 Research output과 기간 필터를 생성하고 실제 URL·페이지 총수·export/HTML 원본 보존. 2009/2010만 포털 연도 필터에 의존하면 P03처럼 탈락할 수 있으므로 인접 2008–2011까지 조회해 실제 DOI 발행일로 다시 제한, 출판자 날짜 누락 시 정렬 미확정. HAL 역시 생산연도와 실제 첫 발행일의 경계 건 보강. 양쪽 모두 날짜 순 후보 전수 정렬 후 최초 공개 출판원문 DOI 1건씩 선정, 접근 실패를 제외할 때 사유/위치 기록, 같은 DOI의 사후 포털 필드와 최초 원문 소속·ID를 별도 보존. PDF는 페이지 이미지 확인. 실제 최초 적격이 후보 P01–P04와 다르면 표 2 재작성, 같으면 후보를 선정으로 승격. 전체 모집단·정렬 누락 검증이 안 되면 계속 PARTIAL.

## 색인 제안
기관 정체성/시간 경계: 역사 원문→후대 기관 전거→typed directed successor/predecessor→현재 연락(별도 역할), same-ID rename와 parent/child 대조, registry RC와 production 분리, EQAR crosswalk 충돌/보류, 저장소 연도 반례, IANA preferred 비교. 현재 확정 추천 규칙이 아니라 판정 대안. AF-RES-246의 인물 전거 미확인을 기관 ROR로 메우지 않음. 색인 등록 및 중앙 상태 변경은 조정자가 담당. 다음 첫 행동은 생산판 고정 ZIP의 실제 행 확보.
