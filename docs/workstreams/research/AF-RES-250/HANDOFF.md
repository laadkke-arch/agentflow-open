# HANDOFF — AF-RES-250

## 상태: DONE (이 작업의 문헌/설계 범위만)

지명 6 판단 묶음, 15 관계쌍, 2조합×6 제외 사고실험 및 필요한 직접 자료별 하한을 충족했다. **실제 제품/모델 성능, 실행 성공, 독립 검토, 최종 스키마 채택은 미확인/미실시.** AF-RES-230/233–237의 중앙 DONE 및 자체 PARTIAL을 변경하거나 완료로 승격하지 않는다. 현재 이 작업의 중앙 상태는 시작판 RUNNING으로 읽었으며 dot-control.json 미수정. 완료 판단은 이 HANDOFF의 자체 판단이다.

- branch: `work/research-af-res-250`; owned_path: `docs/workstreams/research/AF-RES-250/`
- 시작 통합 SHA: `78b64ce8b84ef1d37c2a7100dc376c65dd97e74a`; 계획 `7369707441e2eb70e84004ca6cb3bfeefc8b4061` → 시작 +15 commits, 0 behind, dot-control만 변경. 최신 본인 RUNNING entry와 여섯 depends_on/result_commit 확인, 계획판에는 본인 항목 없음, 여섯 의존 SHA 일치. 두 control contents 빈 본문을 각각 blob f6587b49dccac907b5e2dd1e67bf3e36c1590ccd / 952d292095e8034b5fddbc98ebe56fbe9a5347c3로 직접 읽음. 지침 4개와 6 HANDOFF/RESULT/원표 읽음. 238–242의 입력/출력/정답 사용 안 함.
- **고정 결과 SHA (HANDOFF 직전)**: `b73dc0bae1e7974d0d00fe879f2b2233bdd156b3`
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/RESULT.md) — 첫 필수 표 6행, 두 번째 12행, Q1–Q7, 약점3행.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/sources.jsonl) — 원장 72행, 산입 38 distinct original works/artifacts, 23 lineage. 사례19(2/5/6/2/2/2), 결정10, 표준5(Primer Note 제외해도 REC4), 종합4. 하한 22와 8/6/4/4 충족. 서로 다른 case6은 서로 독립 재현 실험 6이 아니다.
- [packets.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/packets.md), [relations.csv](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/relations.csv), [assemblies.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/assemblies.md), [removals.csv](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/removals.csv), [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/COUNTEREXAMPLES.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/SELF_CHECK.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/b73dc0bae1e7974d0d00fe879f2b2233bdd156b3/docs/workstreams/research/AF-RES-250/SCOPE.md).

## 주요 판정/재개 조건

- A #5302 같은 원작성자 재시험 진술 + 별도 PR5305 selectedOnly diff. B BnF 두 authority/role, 하나의 Correspondance 서지에 둘 링크. C OSM 고정 style → 타일 id40551996 rank32 class school Point → sprite school_11 rect x85 y123 17×17 DPR1, atlas header334×157. W-I layers.csv 추가 대조 row 19/20 열 오류 정정(원파일 수정 없음): World style 8 layers, icon-image 0, sprite 없음. D WCAG 2018 historical quote vs 2025 2.1 note vs 2024 2.2 removed. E #8793 동일 원작성자의 문서 읽음 진술/불명확성 지속, 선택/실행 미확인. F METR dev655 issue1 232/10, issue2 36/0분, 둘 모두 author time. reviewer/acceptance join 없음.
- 15쌍: hard need0, complement10, independent5, 관측된 논리적 충돌0. 공통 원자료 없이 동일 actor나 원인 사슬을 조립하지 않음. 12회 제외에서 local decision 1 재개, 다른 좁은 결정 5 추적 유지, 교차 일반화 재개. X가 더 많은 근거를 유지하므로 읽기 계획 L5 vs X12 additional documents(+첫 문서 각각6), 동일 정보량/실측 속도 비교 아님. 최소 L/조건부 X 모두 합리적 선택; 실제 사용자 성능 미측정.
- 직접 1차의 비ASCII 문자열 파싱 결함(C04)으로 명칭 주장은 제외; ASCII filter input만 사용. C05 실제 PNG header까지만 검사, CRC/픽셀/런타임 미실행. 역사 링크의 당시 floating bytes, A 재시험 exact build·PCM, B physical title page/raw MARC, D tool results/applicability, E click/usage receipt, F 독립 reviewer/acceptance keys는 미확인. H04 개정 이력의 세부 이전/이후 수치 미확인. 조회 실패와 복구 경로 원장에 남김. 최초 read UTC 개별 시각 미재구성으로 시간창 기록. 
- 다음 첫 행동: 설계자가 목표(빠른 첫 링크 vs 판·행위자·의존 교체 검토)를 선택한 뒤 RESULT 두 표와 assemblies를 읽고, 삭제 카드의 recovery URL부터 원자료를 다시 연다. 독립 reviewer에게 패킷 ID의 좁은 주장/hold 및 아래 구조 검사를 재검토시키고, 강한 문장은 같은 actor/artifact evidence가 생길 때만 해제한다.

## 작업 커밋/검증 영수증

① scope/판정 예측 봉인 3c3edfcbf94fef8c06249a4b02bc614c618844c0 (HANDOFF 읽은 후 결과/원표/외부 자료 열기 전, 맹검 아님)
② sources a82bc8c39d2fa8f3a8f79017a4a58b10ec60571e
③ packets 8d749b75a76e983dc85972a319af06a45adea3f5; relations cde34abc7b6254c708a59416d775467915caac58; removals 19ec6a1982951e43193421ffd59902791b1c6cdc; assemblies c8574756f59c38328cbc2509f2999fd1dfac41ab
④ 수정 8ff710d3a96228d9c9c5def0e7a412abbe936b79, 2c078ffa8e869481ba699d019f1f8675be8f26b2, 599e152898cbe293b3714f9d49795e903908f2d3; COUNTEREXAMPLES 189512271e34e03f4727a594983f51856d653043
⑤ RESULT 29c48aff9817f43db2d303c5200c470832ccb278; SELF_CHECK fecddc151d1df8dd1413708d93bd5123030afce8; 규범 표준 하한을 보수적으로 보강 S05 원장 006eea9f8ecef5e1f9a694a9fc39e9df3742b82c, RESULT 1dda8c5ecaddb3bb0d4955ce257dcf8eca78f856, SELF_CHECK b73dc0bae1e7974d0d00fe879f2b2233bdd156b3
⑥ 이 파일 단독 마지막 커밋.

2026-11-25T00:20:37.113Z 최종 고정 SHA에서 9/9 파일 직접 재열람; branch head 동일. JSONL 72 parse/72 unique source_id/38 distinct counted works/23 counted lineages/필수 키 누락0. 표준 S02/03/04/05 REC 4. Pair CSV 15 unique rows/10 cols; removal CSV 12 unique rows/10 cols, L5/X12. RESULT 필수 헤더 2개 exact, data row6/12 width5, Q1–7 headings, 마지막 표3 data width4, 기타 표8/6/9행, W-I 정정20 cols. RESULT의 명시 ID 미등록0, 5 대표 파일 외부 URL과 ledger 연결 미대응0. 링크 주소를 다시 비교한 자체 구조 검사이지 모든 웹의 미래 응답 보장 아님. GitHub compare base→fixed result ahead15 behind0, 9 changed files 모두 owned_path, 외부0, dot-control 미수정. 독립 검토·실제 런타임 테스트 미실시.

## 실행 담당자에게 넘길 검증 입력·명령(미실행)

독립 검토자/실행 담당자는 기존 승인된 환경에서 read-only checkout과 별도 scratch를 사용. 아래 명령은 이번 웹 연구자가 실제 실행한 것이 아니다. 도구·버전이 미제공이면 해당 시험을 보류하고 실제 오류/입력을 원영수증으로 남긴다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-250
git diff --name-only 78b64ce8b84ef1d37c2a7100dc376c65dd97e74a b73dc0bae1e7974d0d00fe879f2b2233bdd156b3
git show b73dc0bae1e7974d0d00fe879f2b2233bdd156b3:docs/workstreams/research/AF-RES-250/RESULT.md
git show b73dc0bae1e7974d0d00fe879f2b2233bdd156b3:docs/workstreams/research/AF-RES-250/SELF_CHECK.md
git show b73dc0bae1e7974d0d00fe879f2b2233bdd156b3:docs/workstreams/research/AF-RES-250/sources.jsonl | python -c 'import sys,json,collections; a=[json.loads(x) for x in sys.stdin if x.strip()]; b=[x for x in a if x["counted"]]; print(len(a),len({x["work_id"] for x in b}),collections.Counter(x["group"] for x in b))'
git show b73dc0bae1e7974d0d00fe879f2b2233bdd156b3:docs/workstreams/research/AF-RES-250/relations.csv | python -c 'import sys,csv; a=list(csv.reader(sys.stdin)); print(len(a)-1,{len(r) for r in a})'
git show b73dc0bae1e7974d0d00fe879f2b2233bdd156b3:docs/workstreams/research/AF-RES-250/removals.csv | python -c 'import sys,csv,collections; a=list(csv.DictReader(sys.stdin)); c=collections.Counter(); [c.update({r["assembly"]:int(r["additional_original_reads_planned"])}) for r in a]; print(len(a),c)'
```
예상: 외부 수정0, 72/38/19·10·5·4, pairs15 width10, removes12 L5 X12. 불일치 시 fixed SHA와 파일 직접 대조, 수치/표 변경 전까지 보류.

A 실제 PCM 재시험: exact tested build 미확인 때문에 역사 actor의 재시험 자체를 재현했다고 표시하지 않는다. 입력으로 A02 merge 425128b2a1846e7b039dac62e89438a9bbbf8a03 및 그 parent, 같은 OS/설정, 임시 폴더에서 길이1초 mono 440Hz/880Hz 파일 두 개. 승인된 바이너리 빌드에서 issue body의 독립 track export 작업을 각각 재현하고 원파일·출력 PCM·build SHA·settings·screenshot/command log 보존.
```sh
git -C /tmp/audacity show 425128b2a1846e7b039dac62e89438a9bbbf8a03 -- src
git -C /tmp/audacity rev-parse 425128b2a1846e7b039dac62e89438a9bbbf8a03^
ffmpeg -f lavfi -i sine=frequency=440:duration=1 -ac 1 -c:a pcm_s16le /tmp/af250-a.wav
ffmpeg -f lavfi -i sine=frequency=880:duration=1 -ac 1 -c:a pcm_s16le /tmp/af250-b.wav
```
실제 binary 실행 및 export UI/CLI는 정확판에 맞춰 담당자가 기록(이 작업에서는 명령 확정 불가). 출력 두 파일의 각 dominant frequency 및 채널/길이를 비교; 섞인 출력이면 성공 추론 반전. 독립 재현은 A01 actor의 정확 build를 증명하지 않는다.

C static pixel 검증 입력: demotiles commit 601ae60796ceceda2cbd2ed3d2ea92d17a84be4b, C01–05 paths, tile 14/8711/5744 feature id40551996. Scratch checkout에서 원자료 hash/PNG 실제 crop 확인:
```sh
git -C /tmp/demotiles rev-parse HEAD
git -C /tmp/demotiles hash-object styles/osm-bright-gl-style/style.json tiles-omt/14/8711/5744.pbf styles/osm-bright-gl-style/sprite.json styles/osm-bright-gl-style/sprite.png
python -c 'from PIL import Image; i=Image.open("/tmp/demotiles/styles/osm-bright-gl-style/sprite.png"); i.verify(); i=Image.open("/tmp/demotiles/styles/osm-bright-gl-style/sprite.png"); assert i.size==(334,157); i.crop((85,123,102,140)).save("/tmp/af250-school_11.png")'
```
예상 rect17×17, C05 blob SHA 79cafb1644860690b510ec46935c78444fa768fb. PIL 미설치이면 새 설치하지 말고 보류. 실제 렌더는 기존 승인된 MapLibre GL JS 버전, style의 remote URL을 고정 checkout 서버의 matching resource로 resolve, DPR1/zoom16, tile14/8711/5744의 자식 타일 범위와 camera sweep을 로그. style/tile/index/atlas digest, load events, feature id, queryRenderedFeatures({layers:['poi-level-3']}) 결과, screenshot/viewport/zoom/DPR 별 영수증. 가시성 미일치면 runtime 주장 보류/반전, static key 연결은 input 불일치 없는 한 유지. 일반적인 렌더러 API·구동 명령을 임의 확정하지 않음. 
B/D/E/F: B01–05 raw MARC/physical title page 추가 비교(기관 ID/판/역할 원행), D01–03의 지정 적용판+검사 도구 정확 버전/raw result, E01 같은 actor의 post-link artifact/실제 선택과 historical page snapshot, F01 dev_id/issue_id에 reviewer/acceptance join 가능한 공개/허용 영수증. 없는 자료를 새로 생성하거나 개인 식별 정보를 강제로 결합하지 않는다. F 총노동 계산의 선행 조건: 일치 actor/time unit/scope, 독립 reviewer time, acceptance state, 결측 처리 및 실패 비용. 현재 결과만으로 총노동 산출 금지. 별도 사용자 비교: 고정 6 카드/2 조합, 12 삭제 입력(원장과 독립 recovery URL만 유지), 정답은 local decision/required evidence/hold/unknown 별로 채점하고 독립 검토자가 판정; 시간·추가 클릭·잘못된 인과 조립을 측정. 연구자가 이 시험은 수행하지 않았다.

## 색인 제안(중앙 변경 금지)

AF-RES-250: claim-scoped evidence packet; lineage/actor/edition/locator/hold; 6 independent local cases / 15 typed pair reviews / 12 planned leave-one-out; minimal L + conditional X; no hard cross-packet need found; 38 primary original artifacts / 23 lineages; W-I repair; no actual model/user performance or runtime validation. 결과 SHA b73dc0bae1e7974d0d00fe879f2b2233bdd156b3; 선행 6 자체 PARTIAL 보존. 중앙 색인은 담당자가 이 HANDOFF를 근거로 갱신할 것.
