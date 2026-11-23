# AF-RES-086 — P3 Python 증거 독립 반증 검토

검토자: preservation 조사 담당의 별도 재계산. 검토 UTC: 2026-11-23T15:04:07.387996+00:00. 읽은 checkout HEAD: `586b33488f6338ee8309a671d270656d837df636`. root가 작성한 P3 후보 결론을 검토했으며 원자료를 재다운로드하거나 새 서비스를 실행하지 않았다. 검토한 로컬 원문·영수증·현재 HTML은 아래 범위다. preservation 산출물은 수정하지 않았다.

## 판정

**현재 후보 결론을 유지한다.** P3 주 관측창 `[2025-11-11T00:00:00Z, 2025-11-14T00:00:00Z)`에서 두 원 독자 조건의 동시 제공은 **확인0/1, 미확인1**이다. 이 값은 실패율이 아니다. 보조창의 stable/options·stable-root·1.x 실제 보관 응답은 각각 확인됐지만 같은 시점 또는 유효 게시구간의 교집합을 입증하지 못한다. raw run 성공2건과 실제 파일의 run 귀속, 원사이트 게시, 독자 응답의 시간은 별개다.

## 독립 재계산 결과

| 검토 항목 | 직접 확인 | 판정 범위 |
| --- | --- | --- |
| 주창 경계 | SCOPE의 반개구간과 CDX의from20251111/to20251113가 일치. 가장 가까운 보관 root는11월14일02:25:24Z, options는02:26:28Z,1.x는11:28:00Z | 세 응답 모두 주창 밖이다. 날짜를 현지시각으로 바꾸어 주창에 넣지 않는다 |
| 보조창 경계 | from20251012/to20251213. 시작일11월11일의30일 전부터 종료일11월13일의30일 후까지 | 요청 범위 내이며 재분모화하지 않음 |
| stable/options gzip | 29,053bytes; 직접SHA1-base32 `T4LV3TOMWOMOYJDUSVBVJH3SJHWT3UIZ`가CDXdigest와 일치 | 보관소가 인덱싱한 표현의 지문과 이번 받은 압축표현 일치. 원발행자artifact SHA로 쓰지 않음 |
| stable-root gzip | 9,606bytes; SHA1-base32 `7VWB2BHLFXHQQOJSW4Q5UB3NBQCBF7TM`가CDXdigest와 일치 | 보관 지문 일치 |
| 1.x gzip/revisit | 3,077bytes; SHA1-base32 `TFNSCYUQTKRX5KNT5DAE72C7Z55V632T`가CDXdigest와 일치 | CDX status는`-`,mimetype은`warc/revisit`이나 실제replay200·gzip본문을 읽었다. 단순status200검색만으로없다고판정하면오류 |
| gzip解凍 | 세 gzip을 실제 해제하니 각 `.decoded.txt`와 byte 일치 | 해제HTML의 지문은 압축바이트/CDXdigest와 별도 |
| options 비교 | 과거stable/options HTML146,504bytes와 현재tag/options HTML146,504bytes의 차이는 `readthedocs-version-slug` 값1개 | 아래 정규화 후 byte일치. `enable` anchor와 내용은 실제 읽음. raw HTML byte일치는 아님 |
| root 비교 | 과거stable-root와 현재tag-root는slug 외에BuildDate 소수초도 다름 | options의한필드동일결론을root까지확장하면오류 |
| 1.x 판 내용 | 과거보관본문에CPython2.7·PyPy2.7 및2021년BuildDate가 있고현재1.x본문과전체SHA256일치 | 실제구계열내용확인.2021년부터2025년까지무중단공개였다는보증은아님 |

옵션 HTML 비교에 쓴 정확한 정규화는 이 하나다. HTML 전체에서 해당 meta 값만 `<version>`으로 바꿨다. 텍스트·공백·날짜·다른 속성을 제거하지 않았다.

```python
re.sub(r'(<meta name="readthedocs-version-slug" content=")[^"]+("\s*/?>)',
       r'\1<version>\2', html)
```

추가로 bytes 정규식으로도 같은 치환을 재계산했다. 양쪽치환은각1회이며CR문자는각0개라서숨은줄바꿈정규화는없었다. 검토도중root가전체원문을`.workbench`로이동했으므로마지막재계산은이동후동일파일을읽었다.

정규화 후 SHA256은 `4cadfbce41aff09e6ba1b510c4e3ed7748bc5e40f2efc9c253565b4025108bf8`로 양쪽이 같다. 정규화 전 과거 해제HTML은 `05b8fe8ec132b722c4ee054a0f8626d9316550b6b14f43d6084107306f0db8c0`, 현재tag/options는 `4576ddf765b26c8bcc16853c229239cb6306278559fd2c1005590be67ed96a4d`다. 이 지문들은 각각 직접계산 값이며 CDX digest·서버etag·source SHA와 구분한다.

## 최소 수정 또는 명시가 필요한 사항

### A. run16의 요약 종료시각과 명령 실행시각 불일치를 숨기지 않는다

`PY-P3-BUILD16.json`(APIv3)은created19:28:06.585063Z,finished19:28:22.585063Z를 준다. 그러나 같은ID의`PY-P3-BUILDV2-16.json`은task_executed_at19:33:07.043447Z,실제mkdocs명령293986754의start19:33:12.804589Z/end19:33:20.236085Z를 준다. 이 두 시각층을 하나로 합치면 tagindex19:33:19.984472가run16생성범위안이라는근거가표면상모순된다. **route원장에v3요약시각과v2명령시각을각각보존하고,생성파일비교는명령구간을사용했다고명시**해야 한다. 원인을서비스버그나queue시간계산방식으로확정하는추가근거는이번검토에없다.

run14의mkdocs명령293986170은19:28:11.247855Z~19:28:15.993088Z다. 현재tag/options의서버mtime19:28:15.896559606은이구간에들고,현재tag/index BuildDate19:33:19.984472는run16명령구간에든다. **시간정합성은가능한귀속을좁히는근거이며파일manifest를대체하지않는다.**

더구나보관stable/options의`x-archive-orig-x-amz-meta-mtime`은19:33:20.100373631로run16구간인데,현재tag/options의서버mtime은run14구간이다. 그럼에도둘은slug외byte동일하다. 내용지문일치만으로두run중하나를고를수없다는후보결론을독립적으로지지한다. mtime은당시/현재서버의진술이며독립실행로그와같은관측자가아니다.

### B. 한 필드 정규화 일치는 options 페이지에만 쓴다

과거stable-root의BuildDate는`2025-11-12 19:33:19.982371+00:00`,현재tag-root는`2025-11-12 19:33:19.984472+00:00`다. 따라서root까지“slug하나만다르다”라고일반화하지않는다. root의소수초차이를추가정규화하면그규칙을별도로명시해야하며,이번검토는그런정규화를승인하지않는다.

### C. CDX 공석·revisit·collapse의 해석을 제한한다

주창stableprefix·legacyprefix의all-status검색도빈배열이어서현재반증검토에서주창양성자료를놓친흔적은없었다. 다만CDX검색공석은모든실제독자응답부재의증거가아니다. 보조legacy의status200필터는실제revisit를누락시켰으나후속prefix/all-status검색과replay본문확보로보강됐다.

보조검색에`collapse=digest`또는`collapse=urlkey`가있다. 반환행은중복을접은조회결과이므로“그기간의모든capture가이세개뿐”또는“그사이에변경이전혀없음”으로쓰면안된다. 동시제공주장을추가로시험하려면동일정확한URL들의기간고정·all-status·uncollapsed CDX/WARC기록과게시유효구간을읽어야한다.이번검토에서는추가네트워크요청을하지않았다.

### D. is_uploaded=false는 publish-failure가 아니다

현재`readthedocs.org/main/readthedocs/builds/models.py`의Build필드L891–895는is_uploaded를upload API의artifact유형으로설명한다. 따라서APIv2의false를일반게시실패로해석할근거가없다. 다만읽은코드는**2026-11-23현재main**이고2025년실서비스배포SHA가아니다. 적절한문장은“현재공식모델상API업로드유형필드이며이값만으로역사적publish-failure를판정할수없다”다. “2025년서비스가정확히이코드로동작했다”로승격하지않는다. 고정source코드SHA/당시모델정의가다음최소확인이다.

### E. 당시 지원판 약속과 연구용 고정판 요구를 구별한다

고정README는stable진입배지L5,stable/options/#enableL44·L140,지원종료Python독자를1.x로안내하는L53을실제로가진다. 구판유지기간·v3.3.0불변보존기간은없다. 이분리는claims.csv의owner_promise와research_assumption에반영돼있다. 현재stable이v3.3.0과다르다는것은movingalias가그기능을수행한결과일수있으며소유자약속위반을증명하지않는다.

사전prerecommendations는이미P3고정판+1.x를선택하고역사적공동제공/run귀속을보류했다. 따라서사후결과에서“싼확인은틀린링크를골랐다”라는권고뒤집힘을억지로만들면안된다. **이번P3에서는링크선택유지,역사적내용증거추가,공동제공유보유지**가정확한대조다.

## 계보·분모 검토

P3 README·release·두run·별칭·세capture·현재tag/legacy·같은서비스의같은소비자경로는`consumer-cibuildwheel`한계보다. HTTP파일과로그를여러원자료로남길수있지만소비자독립계보를증가시키지않는다. RTD현재API/versions/models계약은소비자사건과다른역할이지만같은제공자문서계보의분할은보수적으로합쳐야한다.수집코드로얻은rawresponse와원발행자해시·보관소CDXdigest를각관측주체에배치한다.

주창P3의필수경로는SCOPE의stable/options/#enable·1.x·tag/options/#enable3슬롯이다. 보조root를네번째원슬롯으로추가하지않는다. 두독자조건공동확인의분모는1이며지원되는판정은0/1미확인이다. 보조창에서개별내용이읽힌경로를주창분자에넣지않고,tag경로를당시보관하지못한공석을현재tag내용으로채우지않는다. currentHTML에서anchor가존재한다고실제브라우저렌더링·클릭시험을했다고쓰지않는다.

## 읽기 및 검산 범위

SCOPE.md, streams/python/prerecommendations.json·claims.csv·sources.jsonl, 고정README, 현재stable/options·tag/options·legacy루트HTML, 과거stableoptions/root/legacy의압축·해제본문과receipt,CDXmain/supplemental응답,APIv3build14/16,APIv2commands14/16,tagindex,RTD현재model/serializer원문을직접읽었다. 새독립공개원자료나계보를추가하지않았다. root담당자와동일자료의독립재계산이므로원자료최소량에중복으로더하지않는다.

실행한검산은gzip해제동일성3건·SHA256/sha1-base32재계산·정확한regex정규화비교·root diff·명령시각과mtime범위대조다. 모두예상된내용을확인했다. 서비스빌드·배포·실제2025년브라우저요청실행은없다. 검토후변경파일은이보고서하나뿐이다.

## 가장 작은 다음 확인

1. P3두run의파일단위artifact manifest(경로·파일해시·run ID) 또는서명된보관파일목록을얻으면run귀속판단을바꿀수있다.
2. 주창의stable/options·1.x동시응답또는내용식별된게시구간두개를얻으면0/1미확인을양성/반박으로바꿀수있다.
3. 2025년RTD실서비스소스SHA/필드계약과run16타임스탬프정의를얻으면v3요약시각과명령시각불일치를설명할수있다.
