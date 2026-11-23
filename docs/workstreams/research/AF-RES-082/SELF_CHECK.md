# AF-RES-082 자기검산

## 판정과 원분모

**PARTIAL — 모집·자료량·사전 비교와 결과 파일은 충족, 엄격한 역사적 종단 검증은 공석을 유지한다.** 대상6자리를 교체하지 않았다. 독립 C2가 확인된1자리 중 당시 두 조건 동시 공개는 확인0/1·미확인1이다. R3자리의 역사적 Pages 성공 상태는 확인0/3·미확인3이다. 이는 실패율이 아니다.

원장 전체201행, 보수적 독립29계보, 명시적 실패/무변경 보존 최소 충족 집합7계보, 다른 분야 원발행 기록8개를 검산했다. 원장에 포함된 모집 메타데이터와 반복 읽기는 독립 자료량을 늘리지 않는다. 기간 밖 사건은 선정 태그의 성과로 합치지 않는다.

## Q별 주장·직접 근거·반대 근거·다음 확인

| Q | 주장과 유효 범위 | 원문/실행 관측·판·위치 | 반대 근거를 찾은 경로와 결과 | 빈자리·최소 후속 확인 |
|---|---|---|---|---|
| Q1 | 독자 조건은 확인7/12슬롯. C2 확인은P3뿐 | PY-P1/P2/P3-README는 고정 tag SHA. R-016·023·043의 DESCRIPTION L18·19·14. ROOT-P3-README-LOCATOR가 L44·140 enable, L53 legacy 재확인 | README·문서 index·CONTRIBUTING·MAINTAINERS·release/mission·NEWS를 읽었다. 기능 설명·공개 URL·운영 checklist를 추가 보존 약속으로 만들지 않음 | 나머지5자리 C2 미확인. 같은 태그의 실제 정책·릴리스 토론을 더 찾으면 분모만 갱신하고 자리 교체 금지 |
| Q2 | RTD는 생성·호스팅을 함께 맡을 수 있고, R 경로는 generator/branch/Pages 경계가 있음 | ROOT-RTD-CONFIG의 custom commands; PY-P1-RTD·CONF, PY-P2-RTD, PY-P3-RTD·MKDOCS. R-P001–002·011–012·020–021. 고정 pkgdown/action 구현 R-P029–037 | archive `deploy_to_branch()`는 한 함수에서 build+push. `build_site_github_pages()`는 push하지 않음. MkDocs1.6.1 gh-deploy도 생성+push. “함수/링크 하나=단계 하나” 반증 | R effective token scope·Pages UI 설정 및 전체 역사 의존 설치 로그 없음. 해당 당시 로그/권한 설정을 읽기 전 완료 주장 금지 |
| Q3 | A/B 각각2문서의 조건부 판독이다. 12안24회·고유6문서·HTTP6·reuse18 | prelinks 8ba1d686…; budget/paths 5f881c70…; ROOT-RTD-START/CONFIG·SPHINX-BUILD·PAGES-SOURCE/WORKFLOW·PKGDOWN-BUILD. 절/UTC/지문 기록 | Pages branch 게시와 artifact 게시를 합친 연구자 조립안을 기각. 원 B/P3의 Sphinx가 native MkDocs 경로에 대응한다는 증거 없음. Markdown 불가능론도 기각 | 독립/눈가림 사용자 시험0. 사후 MkDocs대안을 원 B에 소급 금지. 새 시험은 동일 동결12안/태그/예산 사용 |
| Q4 | 역사 생성, git 출력, 최종 serving, 현재 HTML은 다른 증거 | Python raw logs30720077·29061794·30298916: SHA/HTML/exit0. R 생성 commits45e0d9eb·92fecbc0·b352fa49: 입력SHA·판·내부링크. R2/R3 현재2파일씩 exact SHA-256 일치 | P1/P2 named tag inactive404 이후 SHA전체build 조회에서 latest/stable 성공 발견. R1 현재root는새판. P3 API/raw시각·파일시각 차이 유지 | P3 당시 stable/1.x 동시 capture 및 run별artifact, R Pages success 미확인. 0건조회/404를 과거실패로 판정하지 않음 |
| Q5 | path·alias·권한·활성판·재게시가 다음 행동을 바꿈 | INC01 mike175 prefix, INC02 mike188 alias, INC03 deploy-pages76 tag환경, INC04–05 RTD12181 root/robots. PY-INC-STUCK-LOG 실제exit1, R-P038 bench재게시 | 관리형서비스만으로 성공보장 안 됨. 두 링크도route자동보장 안 됨. R2/R3 실제 대표HTML 무변경 관측 포함. 이슈/PR/댓글 중복 합침 | 두 공개success런+잘못된oldURL의 강한반례는 확인0/4검토사건. 비공개서술을실행근거로승격하지않고 공개런쌍/응답추가수집 |
| Q6 | 링크·설정블록·공급자·사람작업·시간/청구를 따로 셈 | Python책임5블록, R6+외부설정미확인1. PY-INC-DOMAIN/PR/DIFF 사람작업5종류. COST자료4개는현재공식지원/제한. 예산HTTPreceipt6개 | 무료플랜을총비용0으로, 로그seconds를노동시간/과금시간으로 바꾸지 않음. OSSgenerator를별도호스팅사업자로세지않음 | 실제 잔여설정수·관리자권한·승인·작업시간·청구 모두미확인. 공개요금으로추정하지않음. 사후전체originHTTP수도산출불가 |
| Q7 | 판ID·정정관계·파일·현재접근을 분리해야 함 | PUB07–10 PLOS원논문/정정/S1/S2, PUB12–16 Zenodo두판+concept+alias. PDF각18쪽/지문. PUB17–19 의도된410tombstone | 같은 DOI라도구판/정정PDF다름; 다른주소라도같은record/HTML; DOI는남아도파일미제공. PUB11 eLife/PUB20 다른PLOS의한계까지읽음 | ZenodoZIP은미다운로드, eLife원논문/그림bytes미확인, 과거연속가용성미확인. 외부분야정책으로웹배포승인금지 |
| Q8 | 여섯 짧은 답은 조건부다. 기본A/Python3·B/R3, 준비상태에따라양쪽가능 | cards.md6슬롯; RESULT표3; 사전paths와사후actual_path분리. P1/P2현재movingvsnamed404, R1원본과생성물, Rroot/dev실제짝 | R2/R3는목적판이달라도B선택유지·route만변함. P3legacy요구는이미명시되어되묻지않음. A/RTD는HTML미준비여도생성가능하므로“HTML없으면B필수”일반화기각 | 사용자입력준비상태·정확한목표판이없으면해당한필드만확인. 기존원요구를포기한대안을동등성성공으로세지않음 |

## 반대 근거 탐색에서 수정한 초기 해석

1. 명명된 tag 사이트가404라서 해당 소스의 역사 배포가 없다고 할 수 없었다. SHA 필터의 전체 build 결과와 raw log로 latest/stable 성공을 찾았다.
2. 한 함수 안에 build+push가 있음을 고정판 코드에서 확인했다. 사용자에게 링크 두 개를 준다고 반드시 서로 다른 사업자나 명령 두 개가 필요한 것은 아니다.
3. 같은 주소의 현재200이 선정 판의 보존을 뜻하지 않았다. P1/P2/R1은 더 새 판이고, R2/R3는 실제 비교한 HTML만 동일했다.
4. 소스가 Markdown이라는 이유로 Sphinx를 기술적으로 불가능하다고 단정하지 않았다. 원 B가 native MkDocs 기능·경로를 보존하는 계약을 제공하지 않았다는 좁은 판단으로 유지했다.
5. PLOS/Zenodo의 영구 식별자도 파일 동일성과 접근성을 보장하지 않았다. 반대로 서로 다른 주소가 같은 판으로 연결된 실제 사례도 남겼다.
6. 교차검토가 “HTML 미준비만으로 B 필수”라는 과도한 일반화를 지적했다. 최종 문장을 “선택 서비스가 원본 생성을 맡지 않아 외부 생성/전달이 필요한 경우”로 고쳤다. 표2의0/1표기와 원장행/최소계보 제외규칙도 명료화했다.

## 필수 수용 기준과 수행 상태

| 요구 | 실제 상태 | 파일/근거 |
|---|---|---|
| 통합판 지침·배정행·078 인수 | 완료; 계획e7a777f2…와 실제시작f736bd55…구분 | SCOPE.md, evidence/intake.json, manifest.json |
| workbench.session start 고정 | 실제 실행, exit0, --fetch | manifest.json; 유일의존f83a48c1… |
| public/nonfork 두 목록 전체 | 58+164, 페이지끝까지취득, 이름순222 | FRAME.csv, evidence/*-frame.json |
| 기간내정식후보≤15/조직, 첫3 | Python5/R7적격후보; 원순번5·9·10/4·5·9 | 원장·frame_updates; 비적격행도유지 |
| 두조건공석·접근실패유지 | C2미확인5; 후순위대체0 | requirements.csv, attempts 원장 |
| 최초보기봉인·동일예산 | 링크byte·사전32열기준commit일치 | prelinks.csv, paths.csv, evidence/budget-seal.json |
| 직접원문≥22계보 | 29계보; 실패/스니펫비산입 | sources.jsonl, evidence/lineage-index.json |
| 실패/무변경사건≥4 | 보수적7계보, 증거수준별분리 | deployments.jsonl, validation.json |
| 타분야공개원기록≥4 | 8개; 핵심실제쌍4원기록/2계보 | PUB07·08·12·13 외 원장 |
| 실제선택/대안가능성/독자접근분모분리 | 완료; 실험성공률0/0산출불가 | RESULT분모표 |
| 동일역사배포두조건·강한반례 | **미달/미확인, PARTIAL** | Q4/Q5와다음입력명시 |
| 필수표1→2→3→분모·여섯카드 | 작성, 별도교차검토 | RESULT.md, cards.md |
| 마지막약점정확히3+다음조사 | RESULT 마지막가시절에3건 | 대상·입력·관측포함 |
| owned_path 밖수정/중앙상태수정 | 없음; 인계전workbench로확인 | scope manifest, 최종check기록 |
| 묶음별원격commit·마지막HANDOFF단독 | 진행기록은COMMIT_LOG; HANDOFF는검사후단독작성 | evidence/bundle-*-readback.json |

FRAME 정리에서 판정은 바꾸지 않았다. Python의 tag SHA/site URL, R의 정식배포 후보순번·날짜를 기존 봉인 자료에서 canonical 열로 채웠다. `available`의2022 tag가 기간내tag열에 들어 있던 표시를 `outside_period_last_observed_tag`로 옮겼으며 기존 제외상태·이유는 유지했다. P3 deep link의 정확한 줄 번호는 사후재열람으로보완했고 초기조건자체는바꾸지않았다.

## 실제 실행한 검사와 실행하지 않은 것

실행 명령:

```bash
python -B docs/workstreams/research/AF-RES-082/tools/assemble_ledgers.py
python -B docs/workstreams/research/AF-RES-082/tools/validate_research.py --final
```

현재 집계본의 최종 검산은 **exit0, 27개 검사 모두pass, pending0**이다. FRAME222·고정6·요구12/confirmed7·C2한자리, paths12·예산24/고유6/HTTP6/reuse18, source ID201개유일성, source참조208회/91종의미해결0, 독립29, 사건7, 외부분야8을 확인했다. 사전prelinks bytes와 paths사전32열을 지정원격commit객체와대조했다. 정확한입력파일지문·실행UTC·당시HEAD는 evidence/validation.json에있다. 이 검사는 연구원장의일관성을검사하며 배포실행의성공을만들어내지않는다.

인계전 고정 결과commit에서 실행할 범위검사는 다음과 같다. 실제 대상SHA·종료값·출력은 실행후별도evidence와HANDOFF에기록한다. 이문단만으로 실행완료를주장하지않는다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-082/manifest.json --fetch
```

소비프로젝트를새로빌드/배포하지않았고, 로그인·토큰권한변경·DNS변경·유료지원요청을하지않았다. 078의SQLite·PNG·ZIP격자/성능도재실행하지않았다. 이는실험누락을숨긴것이아니라이번공개기록연구의범위다. 실제시간·사업자과금·역사적사설계정설정은자료가없으므로미확인으로둔다.

## 재개 최소 입력

첫확인은 `https://api.github.com/repos/r-lib/archive/deployments/2328795124/statuses`이다. 한도응답의reset은2026-11-23T14:22:27Z였으며 제한을우회하지않았다. 다음정상공개접근에서 state·environment_url·log_url과생성commit45e0d9ebc168cf3632bc2d737c9db2318668a826의연결을확인한다. 이것이확인되어도P3역사공존과전체옛내용보존을자동으로충족하지않는다.

R2/R3는출력SHA92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1 / b352fa4902c7fc0d1edc17f957c646072bfd8b9c를입력으로공개deployment/status를찾는다. P3는2025-11-12전후stable·1.x capture, RTD30298914/30298916의artifact/타임필드정의를대조한다. 같은조건의독립판독/공개성공런쌍반례가다음연구다.
