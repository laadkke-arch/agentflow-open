# AF-RES-168 HANDOFF — PARTIAL

- 상태: PARTIAL (원격 저장 완료; 조사 완결 아님). 결과판 SHA **15e99f8b2fc9057556327bb4f8649efda8c9c521** (SELF_CHECK 포함). 이 문서는 별도 마지막 커밋이며 자기 자신의 SHA는 파일에 사전 기록 불가. 계획 통합판 ded3420249a3d60ebbb578a8432cf262d3ffa7d7 → 실제 시작 d32c697b4345442a4c91f62b8fb0bbed19e58034(+4 commits, dot-control 변경만), dependency AF-RES-160 고정 3e93d6cdaaaa6213682da9d2588677c35b3f2517 HANDOFF PARTIAL(22 저작/독립 계보2). 이 작업에서 dot-control 변경 금지 준수. 결과판 compare ahead 10, behind 0, 파일 9, owned_path 외 0.
- 결과: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/15e99f8b2fc9057556327bb4f8649efda8c9c521/docs/workstreams/research/AF-RES-168/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/15e99f8b2fc9057556327bb4f8649efda8c9c521/docs/workstreams/research/AF-RES-168/SELF_CHECK.md), [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/15e99f8b2fc9057556327bb4f8649efda8c9c521/docs/workstreams/research/AF-RES-168/SCOPE.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/15e99f8b2fc9057556327bb4f8649efda8c9c521/docs/workstreams/research/AF-RES-168/sources.jsonl), frame.csv/claims.csv/provenance.csv/observations.csv/advice.csv. 원장 78행, 고유 산입 35저작(엄격한 release metadata 3·편집 release notes 1 제외 31), PR 11. 브라우저 정확값 동일 판 독립 원관측 0 확인(실제 수 미상). 통계/기상 각 1 underlying lineage. 파일 구조·ID·참조 검산 수행, 오류 0; 동일 작업자 자기검산이며 독립 검토 아님. CI/manifest/브라우저 실행/빌드 미수행.
- 핵심: 두 BCD 고정판(v5.6.26 / a630801ac9352a2a84c926e841b22d2c7476f824, v7.2.2 / 03681469611e3281cb0f5a2ccd0756326a0f5ed3)을 읽어 예정 16자리 보존. 2024 값별 하위셀 0/16, 2025 4/16(serif·normal 소급 상세화); 대상 Chrome131/Firefox133 유지. PR 28265는 crash와 상위 지원판 추정 명시, PR26792는 collector 출처 명시. 두 사이트 모두 Mozilla Hacks 옛 구문 주석을 참조하나 전체 셀의 공통 원천 단정 불가. BLS/FRED 같은 시리즈, KJFK raw/table 같은 시각/변환 값. 여러 링크의 호스트 수와 관측 독립성은 분리.
- 미완료 수: 정식 frame 원순위 확정 0/16, 16 미확정(접근 실패); CIU 최종 연말 ref 0/2 확정(후보 2 확보), 과거 렌더 일치 0/32 claim-time(전부 미확보); 2024 exact cell 16 결측, 2025 12 결측. 동일 대상 판 actual execution 0/16, 16 미확보. 동등 다수 사이트+독립 실측의 실제 합의 및 실제 반박 각 1 요구 미충족(0 확인). 소급 정정 전파 시차 미확인. 자료 하한의 저작 수는 넘으나 엄격한 독립 원관측/자연층 핵심 판독 미달. 현재 페이지/보강층으로 과거 결측 채우지 않음.
- 묶음별 원격 커밋·검증: ① 65a5dfdf9e36f7a6905d20131435ef253d300516 SCOPE; ② 069abab4bd95595d173a85fa8974aa187bb3652d frame, 64b6b27c9cd795ee532ff6055a7ab2393ef54532 sources; ③ 046e94cc13adc2967bbdc9208ea47cfbde564774 claims, 149a9470c2cea03ccded455009d57103bcc3caaf provenance, a8312d88ab2338497d4fd937711918214f9b42f8 observations; ④ 5c77996767df599868bba561b68304167a630080 advice; ⑤ adee2770fa27631c500506fe0821b9e8b3433307 RESULT, 329d7773585b780a45675848d54abbe806609740 SCOPE append (초기 선정 규칙/분모 그대로), 15e99f8b2fc9057556327bb4f8649efda8c9c521 SELF_CHECK. 각 변경 파일 해당 SHA로 다시 열고 내용 일치 확인. 최종 결과판 compare는 위 참조.

## 다음 첫 행동: 공개 입력·명령 (실행하지 않았음)

공개 네트워크의 Codex 또는 웹 작업자가 다음을 시행. 작업 브랜치를 새로 만들거나 원규칙을 바꾸지 말고 기존 결과판에서 재개. 작업 트리/원격 권한 규칙에 따라 자신의 owned_path에만 자료 저장. 먼저 BCD 트리 정렬의 전체 입력을 복원. 이때 실제 예상 키와 다른 키가 나오면 사전 scope 65a5df...와 현재 SCOPE/RESULT을 남기고 별도 보정 커밋에 이유·바뀐 자리·분모를 기록. 실제 선정이 확정되기 전 시험 결과부터 열지 않는다.

```sh
git clone https://github.com/laadkke-arch/agentflow-open.git agentflow-open
cd agentflow-open
git fetch origin chore/workspace-foundation work/research-af-res-168 work/research-af-res-160
git switch --track origin/work/research-af-res-168
git log -1 --format='%H %s'
git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 HEAD
# dot-control 전체 원문이 contents API에서 비었던 첫 문제: clone으로 확인
git show d32c697b4345442a4c91f62b8fb0bbed19e58034:docs/automation/dot-control.json | python -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps(d,ensure_ascii=False))'
cd ..
git clone --filter=blob:none --no-checkout https://github.com/mdn/browser-compat-data.git bcd
git clone --filter=blob:none --no-checkout https://github.com/Fyrd/caniuse.git ciu
git -C bcd ls-tree -r --name-only a630801ac9352a2a84c926e841b22d2c7476f824 css/properties | tee bcd-2024-all-keys.txt
python - <<'PY'
import re,pathlib
p=pathlib.Path('bcd-2024-all-keys.txt')
keys=sorted(set(x.removeprefix('css/properties/').removesuffix('.json') for x in p.read_text().splitlines() if re.fullmatch(r'css/properties/[^/]+\.json',x)))
for category,pattern in [('layout',r'^(align-(content|items|self)|aspect-ratio|display|flex(-.+)?|grid(-.+)?|justify-(content|items|self)|order|place-(content|items|self))$'),('typography',r'^font(-.+)?$')]:
    eligible=[k for k in keys if re.fullmatch(pattern,k)]
    print(category,'all',len(keys),'eligible',len(eligible),'ranks',list(enumerate(eligible,1)),'first4',eligible[:4])
PY
git -C ciu remote show origin
git -C ciu ls-remote --tags origin
# Replace <default> with resolved remote HEAD branch; compare committer-date and actual publication timestamp; tags have precedence per SCOPE
git -C ciu log -1 --before='2024-12-31T23:59:59Z' --format='%H %cI %s' origin/<default>
git -C ciu log -1 --before='2025-12-31T23:59:59Z' --format='%H %cI %s' origin/<default>
# Check source cell-specific commits and patches; do not infer exact row from project-wide README
git -C bcd log --format='%H %cI %s' a630801ac9352a2a84c926e841b22d2c7476f824..03681469611e3281cb0f5a2ccd0756326a0f5ed3 -- css/properties/font-family.json css/properties/font-kerning.json
git -C ciu log --format='%H %cI %s' -- features-json/flexbox.json features-json/font-feature.json
```

위 명령의 remote HEAD 및 tag 공개 시각을 확인해 최종 CIU SHA를 확정. 커밋 날짜와 공개 날짜는 별개일 수 있다. 당시 MDN/CIU 화면은 Internet Archive CDX 등 공개 보존본으로 날짜·원 URL·상태를 먼저 확인; 없으면 현재 화면으로 소급하지 않음. P1/P2의 collector report ID, openwebdocs/mdn-bcd-results의 개별 보고서, WPT 결과의 run_id·product/browser version·OS·revision·test path·status를 수집. WPT dashboard가 실제 열리지 않았으므로 0개 결과라고 하지 않음. 정확하게 같은 판/술어를 가진 관측이 우선. Chrome131/Firefox133 major의 공식 stable archived 배포판에서 exact patch/build, OS, 바이너리 해시를 확인 후 기록(이번에 full patch 미고정). fixture와 예상값이 충족되지 않으면 시작하지 않는다. 

## Codex 실행 인계: 정확 입력·기대 단언 (신규 실행 없음)

Chrome desktop 131 stable, Firefox desktop 133 stable(동일 OS와 font fixture로 맞추고 실제 full version 및 실행 환경을 결과에 명시; 최신 stable로 대체 금지). 같은 버전·기본 상태(플래그 없이)에서 syntax CSS.supports(property,value)와 computed style, used layout/glyph 결과를 각각 기록. 독립 관측은 이 실행을 두 번 링크로 세지 말고 다른 주체·별 실행 artifact가 필요. 다음은 사전 예상 테스트이며 관측값 아님.

| 예정 키/값 | 재현 입력 | 검증할 정확한 단언 |
|---|---|---|
| align-content:center | flex container width100 height100, wrap, gap0, 두 고정 item width60 height20, border/padding/margin0, align-items:flex-start | CSS.supports true 별도, 두 행 top offset 30px,50px(컨테이너 기준) |
| align-items:center | flex row 높이100px, item 높이20px, margin0 | CSS.supports true 별도, item top offset40px |
| align-self:center | flex row 높이100px, parent align-items:flex-start, item 높이20px 및 align-self:center | CSS.supports true 별도, 해당 item top offset40px |
| aspect-ratio:1 / 1 | 빈 non-replaced block width100px,height:auto, no border/padding/min/max | CSS.supports true 별도, rect width100 height100 |
| font:16px serif | 일반 span, style font:16px serif, no inherited override | CSS.supports true, computed fontSize 16px, family generic serif(선택된 실제 font를 단정하지 않음) |
| font-family:serif | 일반 span, font-family:serif, 별도 option 대조는 보강층 | CSS.supports true, computed family serif; OS 실제 glyph/option widget 결과 별도 |
| font-feature-settings:"kern" | 공개 라이선스 고정 font fixture(해시, kerning pair 및 advance delta 사전 확인), 두 span 같은 text/size, feature kern on vs "kern" 0; font ready | CSS.supports true; font loading success; pair advance가 fixture의 사전 고정 delta와 일치; fixture 없으면 render 보류 |
| font-kerning:normal | 같은 fixture, 동일한 OpenType kerning pair, font-feature-settings:normal, font-kerning:normal vs none, 동일 font/size | CSS.supports true; expected advance delta fixture 값과 일치, actual width 각각 기록 |

실행 코드/명령 환경이 미확정이므로 여기의 입력과 단언은 실제 테스트 결과 아님. 폰트 fixture 해시·pair advance 단위를 먼저 확정. 추가 WPT 해당 테스트 소스와 기대값은 fixture 후보이며 actual result 아님. 사용자가 요구한 "원관측"은 공개 당시 실행 결과를 우선 추적; 위 새 시험은 별도 보강층. 원격 자료 재현/구조검사와 브라우저 실행은 서로 다름. 

색인 제안: AF-RES-168 | CSS 값·판·출전 계보, 사이트/저작/실측 구분 | PARTIAL | RESULT 15e99f8b2fc9057556327bb4f8649efda8c9c521 | 자연층 순위·역사 표시·정확판 원실행 미확보.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| 모집·연말 CIU 확정·과거 렌더 실패 | 자연층 합의율·대표성·전파 시차 미확인 | BCD ls-tree, CIU 전체 commit/tag 및 아카이브 | 원 순위와 당시 동일 값·판의 두 실제 표 확보 |
| collector 원실행·동일 값 독립 실행 없음; align-self 36/52 주석 불일치 | 값별 기본 동작 및 독립 반박·합의 미확인 | P1/P2 report, WPT run ID·정확판, abspos bug | 같은 빌드/입력의 관측값과 독립 실행 증빙 |
| 동일 출전의 재게재는 보였으나 정정 전파·독립 뒤집힘 미확인 | A/B/C 기술 영역 일반화 불가 | BCD importer·CIU 수정 시각·별도 관측 PR | 동일 술어 판에서 독립 실측이 기존 다수와 반대이고 후속 정정 연결 |
