# HANDOFF — AF-RES-213

## 상태와 인계
**PARTIAL**. 정확 결과 SHA: `b7389f021ce7826e12f9f7b9c755dfbc00f900f3` (HANDOFF 제외, 마지막 결과 커밋). 브랜치 `work/research-af-res-213`. 실제 시작 `87ffc1539bcf33da0fccf45eb15982a02d93e409`, 계획판 `bb146773bbffba5e724e8c842951e2c25198c2da` 대비 +5/−0 및 dot-control 변경만 확인. AF-RES-202 인계 `cc543b8d1b8f8748fa363999b76a55f05de2266c`의 전제(파일 존재≠실제 구성/로드)를 사용. 중앙 진행표는 고치지 않았다.

- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/RESULT.md): 핵심 3표, Q1–Q7, 대안과 3 약점.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/sources.jsonl), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/frame.csv), [objects.csv](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/objects.csv), [resolutions.csv](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/resolutions.csv), [requests.csv](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/requests.csv): 고정 증거/분모/24 소비자 판정.
- [CONTRASTS.md](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/CONTRASTS.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/SELF_CHECK.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/b7389f021ce7826e12f9f7b9c755dfbc00f900f3/docs/workstreams/research/AF-RES-213/SCOPE.md): 반례·정정·자체 검토·착수 범위. TABLE_DRAFT.md는 3차 당시 초안, 최종 판정으로 사용하지 말 것.
- 5 묶음 커밋: ① dcabd61f326c404d018b2b3b008bc67b36bf6bcb, ② 929f6e4f66f0dad332b5498d54efcf09cf501a42, ③ e7a0ce3b664d225d59ec94750d391219fa105dca, ④ 699b61b4bf879e0a16044c8e1e7a537dfa42f0c9, ⑤ b7389f021ce7826e12f9f7b9c755dfbc00f900f3. 이 문서는 별도 마지막 커밋.

## 핵심 관측·상태
- styles `f123868a546e6e7cec10e808ae04ef0e52bf2210`, locales `21a175a1d84cc1792dd73f5a627de004fba5b207`; 두 Nature 저널 별칭은 en-GB 및 동일 parent href, 본문 macro/layout 없음. 부모 nature.csl 8/2, APA 99/2, APA의 template는 runtime parent 아님. 세 locale XML 동일 term 및 date 비교 완료.
- Zotero 고정 소스 `5c3676746f92068667de0a01ffa9d92ebf70ed72`: bundle Nature/APA exact blob 및 3 locale exact blob 확인, alias 별도. 미설치 부모는 설치 시 GET/hidden, installed parent lookup 및 effective locale 강제; locale chrome resources/cache 코드. Pandoc 3.8.3 `568dab14533940ecee16824097400f1eabf13869`: basename local-first 후 URL; citeproc 비교판 0.12 `caec46cd273d3ac84a3de3eae936b2916e49e9fb` vendor locale embed, lang 우선; 실제 installed dependency solver/binary 미확인.
- 39/23 고유 원자료(7/7 XML, 5/4 spec/schema/fixtures, 15/5 consumer docs/code, 7/4 request/handling, 5/3 WordPress); ledger 64행, 57 열린 기록(포함 18 비산입), 7 열람 실패. 12/12 primary 목적 자리, 24/24 static consumer 판정. 6 사건과 7 request/handling 원자료 별도. 원제보→동일 저널 current alias→merged XML→당사자 회신 1건(Nature Communications, D04/D07/X05/X11); 정확 대상 두 저널 제보 0/2, publisher F01/F07 접근 실패, 저널 승인 0. 직접 renderer 실행 0, cache hit 실측 0, offline success 실측 0. 실행은 이번 사용자 경계상 하지 않았다. 현재 source/fixture 기대치와 실측 혼동 금지.
- 반례: Scientific Reports 2013 generic Nature 안내와 달리 current X09→nature-brackets (X10). X12–17 같은 parent 다른 locale; X18 abbreviation map 2776 keys / 63 다대일 출력 그룹. WordPress actual child file replacement 및 specificity contrast. 사용자 목적이 약어/metadata 결손이면 body edit보다 item path가 첫 링크. 
- 마지막 결과 SHA에서 10파일 모두 원격 재열람. RESULT blob 931a7ab6d1251e958289b919f658af6be134cd66 (28558자); SELF_CHECK e1edb727a9c081c741a183495dd451bdabb09246; ledger 671abfe02342c19b13b80469694cc7a4d4d0ec64; frame 6791946a46ea419bcbb6a60d8af53416a1692d75; objects 34332b61b0ada9a0793603dc24d553b1630d571f; resolutions b57d85dfad04e7fa11ba9dda34ef53a1c246b873; requests 34250919625eecf5d9c9fce5a3297934d0366b90; contrasts be74d7339114c7256ad1e4992abd87f773a9fad2. 행수·source IDs 64 unique/39 distinct work admitted, 12 slots×2, objects 7, requests 6, frame 78, RESULT 첫 3 headers 및 마지막 3 약점, 링크 source id 누락 0 확인. R02 및 X18 반례 재대조. GitHub compare base→result ahead5/behind0, 모든 10 changed paths 허용 경로 내. 독립 검토 없음; 자체검토 및 원격 읽기/정적 집계만. GitHub clone/workbench/test는 실행하지 않음.

## 첫 재개 행동 및 색인 제안
1. 정확 두 대상 저널의 현재 editor formatting guide 원본문 또는 공개 저자 request + journal matching style issue/PR/author proof를 열린 공식 주소에서 직접 확보. F01/F07은 인증 리다이렉트로 차단되었으므로 동일 원본의 공개 공식 대체 주소/편집자 문서 우선, 인증 우회 없음. 원요구의 학술지와 patch의 journal/parent href를 일치 검증. 불일치이면 A01/A02의 parent 사실을 유지하되 정식 추천과 edit branch를 분리.
2. 색인 통합 담당에게 `AF-RES-213: CSL alias vs actual editable body vs locale supply; 12×2 static, 39/23, R02 historical drift + R04 request/merge + WP child override counterexample; PARTIAL (target journal/user run unverified)`와 위 RESULT, objects/resolutions, sources/CONTRASTS 링크 전달 제안. INDEX와 중앙 control 수정은 통합 담당에게 맡긴다.

## Codex 검증 항목 — 미실행, 별도 승인과 환경 필요
이번 과제는 renderer 실행 금지. 아래는 향후 실행 권한이 있는 작업자가 별도 임시 디렉터리/격리된 테스트 환경에서 재현할 명령과 입력이며 현재 관측이 아니다. 새 파일이나 설치 환경을 사용자 profile에 적용하지 말 것. 우선 repo 자체 경계 확인:

```sh
git fetch --prune origin
git switch work/research-af-res-213
git rev-parse HEAD
git diff --name-only 87ffc1539bcf33da0fccf45eb15982a02d93e409 HEAD
python scripts/check.py --require-git
python scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

명령은 미실행, 설치/환경 의존 시 help/경로를 확인하고 오류를 기록. 새 manifest가 필요하면 `python -m workbench.session start --help`를 먼저 확인하고 승인된 작업 path를 사용; 다른 경로를 이 브랜치에 커밋하지 않는다.

**Pandoc/CSL exact bytes 준비 및 실행 절차**(인터넷 허용 수집 단계와 격리 실행 단계 분리):
```sh
set -eu
T=$(mktemp -d)
mkdir -p "$T/csl" "$T/locales" "$T/out"
S=f123868a546e6e7cec10e808ae04ef0e52bf2210
L=21a175a1d84cc1792dd73f5a627de004fba5b207
for n in nature-biotechnology nature-nanotechnology; do
 curl -fL "https://raw.githubusercontent.com/citation-style-language/styles/$S/dependent/$n.csl" -o "$T/csl/$n.csl"
done
for n in nature apa; do
 curl -fL "https://raw.githubusercontent.com/citation-style-language/styles/$S/$n.csl" -o "$T/csl/$n.csl"
done
for n in en-US en-GB fr-FR; do
 curl -fL "https://raw.githubusercontent.com/citation-style-language/locales/$L/locales-$n.xml" -o "$T/locales/locales-$n.xml"
done
for f in "$T/csl/"*.csl "$T/locales/"*.xml; do printf '%s ' "$f"; git hash-object "$f"; done
pandoc --version
pandoc --print-default-data-file=default.csl > "$T/out/default.csl"
cat > "$T/refs.json" <<'JSON'
[
 {"id":"book","type":"chapter","title":"Chapter example","container-title":"Collection","author":[{"family":"Avery","given":"Alix"},{"family":"Baker","given":"Blaise"}],"editor":[{"family":"Carter","given":"Camille"},{"family":"Davis","given":"Dorian"}],"issued":{"date-parts":[[2000,6,18]]},"publisher":"Example Press","page":"10-12"},
 {"id":"preprint","type":"article","genre":"Preprint","title":"Preprint example","author":[{"family":"Avery","given":"Alix"}],"issued":{"date-parts":[[2022,7,1]]},"URL":"https://example.invalid/preprint","DOI":"10.0000/example"},
 {"id":"journal","type":"article-journal","title":"Journal example","container-title":"Example Journal","container-title-short":"Ex. J.","author":[{"family":"Baker","given":"Blaise"}],"issued":{"date-parts":[[2022,7,2]]},"volume":"2","page":"3-4"}
]
JSON
printf '%s\n' '[@book; @preprint; @journal]' > "$T/input.md"
```
Exact blobs compare objects.csv; actual Pandoc build/citeproc and vendor locale provenance record, compare X06–08. The synthetic DOI and URL are inert fixture values, no dereference needed. In network-isolated runner, record network attempts and exit codes; run with local files only (network isolation method must be established on actual Codex runner, not assumed). Save stdout/stderr separately:
```sh
for n in nature-biotechnology nature-nanotechnology nature apa; do
 for lang in en-GB en-US fr-FR; do
  pandoc "$T/input.md" --citeproc --csl="$T/csl/$n.csl" --resource-path="$T/csl:$T" --metadata="lang:$lang" --bibliography="$T/refs.json" -t plain > "$T/out/$n-$lang.txt" 2> "$T/out/$n-$lang.stderr" || printf 'failed %s %s\n' "$n" "$lang"
 done
done
```
Record actual loaded paths/hash using platform read trace where available and network attempt count. For negative controls use copies of isolated temp fixtures: missing local nature.csl (block HTTP, expect dependent resolution failure or attempt); wrong same-basename independent style (record which file selected, never change upstream), no explicit --csl (expect Chicago default), lang omitted vs explicit fr-FR; switch DOI/URL/volume/page one field at a time, remove container-title-short and compare abbreviation option. Independently fetch X12/X13/X14 at same S and test a two-author/editor/input that actually reaches and=text/accessed; don't assume Nature and=symbol output changes. A04 editor plural override expect fr éds. only if relevant branch taken. Fixture B03–B05 expected strings separately compare with suitable CSL runner; tests not run here. If explicit FR doesn't override, parent lookup differs, exact input metadata yields different expected branch, or network fetch occurs, record source/build/version and update resolutions/CONTRASTS (not just success text).

**Zotero**: separate disposable profile with version/build provenance; inspect source bundle installed files and locale packaged resources (X01/X02), list visible vs hidden. In network-disabled environment first install exact nature.csl locally, then target alias from local + install; test unique-only filter in online repository separately if authorized. Confirm parent presence/id/hash, no HTTP attempts, citation preview with fixture item fields (chapter two editors, preprint genre/URL/DOI, journal short field), compare en-GB forced for A01/A02/A03 and FR selector for APA, custom new-id alias fr-FR or full independent copy only in test profile. Repeat with parent absent/renamed and different same ID to test missing parent path and cached engines; record actual cache hit/miss (code alone insufficient). Compare plugin MEDLINE option vs direct bibliography export and missing abbreviation metadata. No journal compliance claim unless first action finds direct authority. If setup cannot match fixed build or network trace unavailable, mark those observations unverified.
