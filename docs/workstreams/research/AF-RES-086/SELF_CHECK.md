# AF-RES-086 자가검산

## 판정

연구 판정은 **PARTIAL**이다. R1의 선택 status 원행은 읽었으나 이전 상태 순서와 당시 경로 응답이 없고, P3는 주창 두 경로의 공동 제공을 확인하지 못했다. 자료량·원장 정합성 검산 PASS는 REVIEW_READY의 대체 조건이 아니다. 실제 미확인을 음성/실패로 채점하지 않았다.

범위는 계획 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`, 시작 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`, 의존 `1f8bf039ad4f9a38b99764a11f72b515facef39c`, 사전 권고 `586b33488f6338ee8309a671d270656d837df636`이다. 각 SHA의 역할을 바꾸지 않았다. startup-contract 영수증에 계획판의 자기 행 부재와 시작판의 RUNNING 행을 모두 남겼다.

## Q1–Q7: 주장·원행·실행·반례·남은 최소 확인

| 질문 | 실제 주장과 원문/실행행 | 자기 결론이 틀릴 사례를 찾은 경로·발견 또는 공석 | 다음 최소 확인 |
|---|---|---|---|
| Q1 | P3만 stable/enable과1.x라는 두 원 독자 조건. PY-P3-README 추출 L44·53·140; P1 L18·99. R1/R2 DESCRIPTION L18/L19·README·NEWS. claims.csv에서 owner와research_assumption 구별. R1 #113의 checked_items는 발행자 체크리스트. | P3 보조창 documentation 이슈/PR6건과 R1동시대 후보3건의 원문을 조사. 구판 유지기간을 추가하는 발화는 발견하지 못함. 별도 Discussions 전수 아님. 서비스의 versioning 기능 설명을 소유자의 원 약속으로 바꾸지 않음. | 지정 소스·관측창에서 유지 기간이나 고정판 URL을 명시한 발행자 원문이 있으면 해당 claim 행과 원 분모를 재검토. |
| Q2 | P3 tag14·16은 같은63fd63b…를 사용하고 실제 MkDocs exit0. stable15 추가. routes의 generator_start/end와 API summary_finished를 별도 기록. 원 JSON·원 command 로그·BuildDate·mtime·직접 file hash를 비교. | 같은 source이므로 run 하나를 선택하는 가설을 검토했으나, tag index는run16시간대, options mtime은run14시간대. 보관 stable/options는또다른mtime인데 내용은같음. v3run16summary끝19:28:22와실제명령19:33:12~20 불일치. `is_uploaded=false` 의미는 현재 공식코드상 upload API유형이므로 실패로 승격하지 않음. | 두run별 file path/digest/artifact manifest 또는당시산출물묶음. 현재mtime만으로귀속하지말것. |
| Q3 | R1DEPLOYMENT input45e0d9eb…와STATUS6150834411 inactive@12:38:03Z,env공백,run/jobURL 원문. 선택배포12:35:07Z. 상태배열/evidence original.json 보존. | 자동inactive가이전success를암시한다는가설을현재정책과대조했으나개별전이기록없음. 주창배포11개와후속스냅샷을읽음. NEXT12:37:22는inactive직전,LAST16:07:18이후;root/leaf4/4동일. inactive=내용소실추론을지지하지않음.404로그·빈목록은실패점수없음. | 당시발행자의공개상태배열·run14035386117/job39292155301원로그와root/leaf응답지문.이전success의존재·삭제를현재90일정책만으로가정하지말것. |
| Q4 | 주창0/1공동확인,미확인1. 보조stable/options20251114022628와legacy20251114112800의내용을실독. optionsid=enable와내용,1.x의Python2.7표. gzip SHA1↔CDX 및decodedSHA256을별도재계산. | 최초status200검색이revisit을놓쳐all-status검색과payload로교정.두보조응답은주창밖·서로다른시각이라공동확인아님.현재tag와보관stable의한metadata필드제외동일성은이름다름=다른판가설의반대근거. root는BuildDate도달라같은정규화적용안함. | 주창의동시응답또는경로별판별된게시구간교집합. 빈CDX로부재/실패를확정하지말것. |
| Q5 | 사전추천3파일은586b334…대비불변. comparison.json의4목적동일,후보변경R1한건(1/4),유지3/4. 현재제공과당시제공을분리. | P1named404와같은SHA latestHTML성공을대조. R2현재2/2바이트일치는사전유보를새로해소하지만당시제공유보는유지. 사전에없는틀린주장을만들어반전성과로세지않음. R1은HTML원문으로반환가능하지만렌더링과거사이트아님. | P1oldHTML, R1당시응답, P3공동제공등별도공석.실제A/B효과실험없어0/0산출불가. |
| Q6 | 저장소별생성순첫3개를합친층화12,별도추가4. incidents.csv의UTC/번호/탈락이유. 생성·게시success+동일ref오응답+회복판지문의strong0/12,0/4. | mike/MkDocs의생성·게시실패대조와RTD11531·mike229의이름차이/내용무변화대조를읽음. Pages383→typstissue1은artifact와curl catalog차이·publishsuccess까지연결하나회복직후지문없음.2026댓글은기간밖으로제외. | typst회복dispatch의run·artifact·동시catalog응답을원사슬과연결.강한사례0을전체사건부재로해석하지말것. |
| Q7 | 두기관3저작쌍6판기록. Umap두tar파일MD5검산·실제판,matplotlib양manifest,SWHhello양directory/configure+NEWS. 비용172GET/7,377,636bodybytes와별도connector46호출구별. | DOI22705920은철회410/파일없음. Gitorious종료참여자보고+SWH보존내용은확인하나옛origin요청proxy503으로영구404단정안함. Zenodo현행파일수정정책은고정DOI=전시점불변전제를막지만본쌍실제교체증명아님. | 옛origin종료당시HTTP보관본,필요하면matplotlibZIP실제다운로드.보존파일식별을웹route게시·anchor연속성으로승격하지말것. |

## 숫자·단위 검산

- [source-audit.json](evidence/source-audit.json): 201원장행, 적격126 URL·판쌍, 같은payload3쌍을합친123자료, 보수적25계보. 정책4계보를제외해도21실제저작·사건. APIv2/v3·build/rawlog·보관/현재응답의계보를쪼개지않음.
- [route-denominators.json](evidence/route-denominators.json): 고정9슬롯,현재HTTP2008/9,현재목표판4/9,주창목표판0/9·미확인9.부가root와후속스냅샷은분모밖.
- RTD선택원로그분모4: tag30298914·16, stable15, P1latest30720077.4/4생성성공;별도publish거래0/4미확인.소스조회latest30298913과2021legacy14073318는별도문맥.
- Pages선택배포2: success직접확인0/2,남은inactive2/2.전체이전상태순서2/2미확인.RTDbuild분모와합성성공률을만들지않음.
- 원약속두조건1/6을보존.이번고정표본1/4,P3공동0/1미확인1.다른3자리공동조건0/0은산출불가.
- R현재/선택생성물2/4일치,R1후속2스냅샷×2파일4/4일치는별도계산.현재HTTP를과거HTTP로계수하지않음.
- 최초층화사건12·추가4·고정소비자4의분모를합치지않음.타분야판6개는계보6개가아니라3저작쌍.
- 비용상현재9경로458,565bytes는총조사의부분집합.사전20GET765,122bytes+추가111GET2,557,285bytes=네자리131GET3,322,407bytes.사건6GET277,631bytes+보존35GET3,777,598bytes를더해172GET7,377,636bytes.검색/connector전송량미측정을0으로대체하지않음.

## 독립 검토와 발견된 수정

| 검토 | 입력과 실제 확인 | 반영 |
|---|---|---|
| Python 반증 감사 | [python-audit.md](streams/review/python-audit.md). 보관gzip/CDXdigest·decodedHTML,한필드정규화,시각·run귀속·분모를독립재계산. | run16시각불일치,options한정정규화,CDXcollapse/200필터한계,현재모델코드의시대구분,사전권고유지를명시. |
| R 감사 | [r-audit.md](streams/review/r-audit.md).73원장/영수증/raw지문,생성4Gitblob,비용·카드·NEXT순서. | 이전success의존재/삭제암시제거,현재90일정책라벨,HTML소스vs렌더링구분,NEXT직전·LAST이후시각교정. |
| 분모 감사 | [denominator-audit.md](streams/review/denominator-audit.md). 네stream원장·적격계보·중복payload·사건분리·외부판쌍을독립계산. |126행을126독립저작으로부르지않고동일바이트제외123자료/25계보로명시.정책제외21계보도분리. |
| 통합 구조 검산 | [tools/validate_research.py](tools/validate_research.py), [local-validation.json](evidence/local-validation.json). | 최초검사에서R사전11개추출경로가json으로잘못조립됨을발견.실제txt경로로교정하고assembler를고침.원읽기·해시·판정은불변.이력은method-adjustments에보존. |

최종 내용 감사는 `streams/review/final-audit.md`에 별도로 남긴다. 독립 검토는 다른 조사자가 이미 확보된 원문과 산식을 다시 읽은 것이며, 같은 데이터를 재요약한 자기 검토로 대신하지 않았다.

## 검사 명령과 범위

```bash
python -B docs/workstreams/research/AF-RES-086/tools/validate_research.py --require-final-docs --output docs/workstreams/research/AF-RES-086/evidence/local-validation.json
git diff --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-086/manifest.json --fetch
```

세부 실행SHA·UTC·종료값은 최종 `evidence/acceptance.json`과 HANDOFF에 기록한다. 원격 고정 결과 커밋은 GitHub 파일 API와 public git fetch의 tree/blob으로 재열람한다. 그 뒤 HANDOFF만 마지막 커밋한다. HANDOFF 자체를 앞선 소스 검사에 포함됐다고 말하지 않는다.

저장소 공통 검사 `python -B scripts/check.py --require-git`는 `.workbench`와 lab 산출물을 쓰므로 주 작업트리에서 실행하면 사용자 쓰기 범위를 벗어난다. 동일한 결과SHA를 **owned_path 내부의 무시되는 별도 checkout**에 놓고 원 검사기를 수정하지 않고 실행할 수 있다. 실행 여부·정확SHA·종료값은 acceptance에 기록한다. 공통 검사가 연구의 역사적 공석을 해소하는 것은 아니다.

새 빌드·서비스 배포, 비공개 관리자 API, 계정 변경, 과금, 전체 assets 실행, 브라우저 상호작용은 수행하지 않았다. 요청된 공개 원자료 조사와 허용 경로의 저장·커밋만 수행한다. 이 항목을 검증 성공에 포함하지 않으며, 남은 역사 자료는 RESULT의 마지막 정확히3개 약점과 HANDOFF의 첫 행동으로 넘긴다.
