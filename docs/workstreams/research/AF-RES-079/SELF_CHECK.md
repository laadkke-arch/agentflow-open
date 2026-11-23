# AF-RES-079 SELF_CHECK

검토자: root. 검색/최초 판독: root, gis_evidence, oss_evidence, standards_evidence 도구 에이전트. 관계 재판독은 별도 standards_evidence가 맡았으며 최초 판정·수선안·RESULT를 가렸다. 출처 선정은 가리지 않았고 같은 계열 도구/모델의 통계적 독립성은 입증하지 않았다. **사람 검토·독립 정확도·독립 일치율을 주장하지 않는다.** 원장 구조검토도 별도 에이전트가 수행했으나 뒤에 추가된 native 실행의 독립 재실행은 아니다. 재개2에서는 별도 비가림 도구 에이전트3개가 출처·GIS·OSS를 감사했고 GIS7개 read와 OSS18호출을 기존 환경에서 표적으로 재실행했다. 이 결과를 원래 가림 검토에 소급하거나 독립 일치율로 계산하지 않는다.

## 세부 질문별 주장·근거·반례·재개

다음 표의 행 ID는 sources.jsonl/observations.csv/relations.csv에서 찾을 수 있다. 짧게 적은 원절의 정확 commit·행과 UTC는 source 행에 보존했다. 실행을 하지 않은 공급자 시험은 정적 판독이라고 표시했다.

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
|---|---|---|---|---|---|---|
| Q1a 주소·등록 ID·배포물 중 무엇이 변했나 | G01 논리 driver와 source container 구별; C02 별도 distribution | [Rasdaman 수신 commit](https://github.com/OSGeo/gdal-extra-drivers/commit/ffe0c44714a491eb90ba82d8df74f621ac6003e7), `G-ras-code3.6`; [PIL orig archive](https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7.orig.tar.gz), `PA001/2`, `R030` | 구 등록문자열·수신 원본·배포 archive 확인 | source 존재≠빌드/배포 지원; hash일치≠서명 검증 | receiver README3.5를 exact 이동판으로 보는 가설 기각; Pillow2.0 VERSION1.1.7도 같은 배포 증거 아님 | receiver의 실행 가능한 release/support 판; 실제 설치 artifact metadata |
| Q1b 기능·포맷판·문서판이 그대로인가 | G03 driver 유지/format판 변경; G04 같은 이름 의미 변경; C03 원절 소실 | [GDAL3.9 Parquet 옵션](https://github.com/OSGeo/gdal/blob/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/doc/source/drivers/vector/parquet.rst), `G-O07/09`; [imp3.11](https://docs.python.org/3.11/library/imp.html#imp.find_module), `C03-P1` | writer beta→1.0, interleaved→struct, live anchor부재 | GIS G02–G04 양판 native 추가; G01 미확인. 현재 doc응답은 과거 redirect아님 | same path의 test.parquet 해시도 세 판에서 다름 | GN01–06의 고정입력·구consumer는확인;추가비대각좌표/null/외부consumer만 |
| Q1c 실제 도착·과거 link 이력 | 현재11사건 GET을 기록; 역사 redirect11/11 미확인 | `G01–C03-HTTP-U`, [URL 원장](evidence/url-policy-comparison.json) | 요청/상태/체인/도착/시각; fragment는 HTTP 미전송 | 현재301로 과거 redirect를 추정하지 않음 | ARG/Rasdaman301→404; C03 same200도 기능절 없음 | 당시 응답 capture나 원 발행자의 날짜 있는 redirect 운영 기록 |
| Q2a 이름 변경·대체·퇴역 선언의 주체와 판 | 정확 공지·PR과 원판을 함께 사용 | [GDAL3.7 NEWS](https://github.com/OSGeo/gdal/blob/ab9cb1a1d4928cdcf2877d8e0c6ad9fc2c79fbc9/NEWS.md), [SciPy PR11431](https://github.com/scipy/scipy/pull/11431), [PR12382](https://github.com/scipy/scipy/pull/12382), `OS-REL-06/14` | ARG3.8/3.9, KDTree 예정1.8/실제1.9, integrate실제1.14 구별 | 같은 프로젝트의 모든 기능에 일괄 적용 불가 | PR의 undocumented 표현과 구 query Returns 문서 계약을 대조; 문서 존재를 확인 | 정확 release/consumer 지원 선언 또는 실제 removal commit |
| Q2b 대상 발행자 동의·수신자 역확인 | C02 원/수신자 공지를 각각 읽음; 동의를 과장하지 않음 | [fork 공지](https://mail.python.org/pipermail/image-sig/2010-July/006423.html), [원 저자 답변](https://mail.python.org/pipermail/image-sig/2010-August/006429.html), `R014`의2020 PyPI administrator 댓글 | fork와 패치 선호, registry transfer완료 구별 | 원 저자가 모든 변경/ID병합에 동의한 증거 없음 | 현재 PythonWare200은 원 PIL 발행자 연속성이 미확인이므로 원저자 근거에서 제외 | 특정 distribution/version의 원저자 선언이 꼭 필요하면 해당 원 공지 |
| Q3a 동일 입력 정상 결과 | OSS4사건에 과거 native 대응 확보 | [49 대응 원행](streams/oss/historical/paired-observations.jsonl), `H-O01-P1-normal`, `H-O02-P1-normal`, `H-O04-P1-provider` | 같은Python3.8.20/NumPy1.19.5,4판×50호출;46 exact hash/3명시매핑 | 49비교는49자연사건이 아님; O02 simps/cumtrapz 별도 native미실행 | alias가 실제로도 맞는 O02/O04를 보존해 변화 사례만 고르지 않음 | 실제 업무에 필요한 아직 실행하지 않은 입력/개별 alias만 추가 |
| Q3b 경계·형·예외·손실 | O01 빈 형상, O03 exact반경·scalar형 불일치 확인 | `H-O01-P1/P2-empty_2d`, `H-O03-P1-normal/exact_boundary`, `H-O03-P2-normal`, `H-O04-P2-complex/wrong_shape` | 정상 scalar adapter와 전체 계약은 다름; 거리 정보 손실 | 예외 직전 경고는 원 probe에서 미포착(null); null을 경고없음으로 비교 안 함 | O03 static보류를 exact radius1.0 실제 입력으로 뒤집음; complex오류는 일치 | 구 계약을 보존할 adapter를 같은 입력·dtype·경계에 실행 |
| Q3c 규범과 실제/구현 불일치 | G03 같은3.8 manual과 writer/test가 다름; G02 시험설정이 기본과 다름 | `G-parquet-doc-3.8`, `G-parquet-writer3.8`, `G-arg-test-3.8`, `G-gdal-manager-3.8`; `G-O03/04/07` | beta1 설명 대1.0 출력 정의, defaultNO 대YES opt-in | GN01–GN11로 G02–G04 실제 실행을 추가; G01 native와 전체 규격 적합성은 미확인 | ARG fixture nodata-32768 대source-32767 정적 불일치도 보존 | GN08/09에서 default/YES, GN02/05/06에서 구consumer 확인; 남은 exact-schema는 bboxNO 조합 |
| Q4a 두 수선 규칙을 결과 전에 고정했나 | U/T·분리 불가·독립 기준을 모집 전 봉인 | [SCOPE.md](SCOPE.md), 최초 commit `dfdfe1b82ee1921f2f90c723dbd9fe8d22138ead` | U:301/308 단일 성공도착 수선, same2xx유지, 그외보류; T:typed/versioned 관계 | 301뒤404는 최종 실패; retrospective 최적화 정책 아님 | 각 domain에 같은 U classifier 적용. 실제11체인은 원칙과 맞음 | 다른 체인/다중도착 자료가 실제로 생길 때만 새 관측 추가 |
| Q4b 거짓 병합·거짓 분리를 어떤 단위로 세나 | U가 못 구별한 기능 의미·mode·인용 연속성은 따로 기록 | `G04-HTTP-U`, `G-O09/10`; `O03-HTTP-U`; `C02/C03-HTTP-U`; RESULT Q4 | 자연G04 의미누락1/8, O03mode누락1/8; 대조C02발행자연속성미확인1/3,C03원절1/3. 서로 합산안함 | 실제 운영 추천 레코드0개; 완료분리/운영오병합0. U보류6/11는오류아님 | O04 doc404지만 함수실행 성공. U에 없는 분리를 가정해 false-split만들지않음 | 원 추천 레코드·호출·판을 받아 실제수선diff를 검증 |
| Q4c 독립 기준 없는 건수 | 식별 원문기준11/11; 과거native 자연7/8, 대조0/3 | sources/observations와 [가림 검토](streams/review/REVIEW.md) | 자연G01의1·대조3에는 과거 native쌍이 없어 행동 수용 제한 | source-supported 관계와 runtime검증 분모가 다름; 모집틀전체 독립재감사는아님 | 별도agent의일치도곧groundtruth라는가설거절 | Rasdaman server/build,대조원판실행,실제업무기준별도평가 |
| Q5a 같은쌍의 P1/P2가 달라지나 | O01 정상 P1수용/P2무수정거절; G04는정상WKB P1수용/P2구consumer의geometry·CRS손실로거절 | `H-O01-P1-normal`, `H-O01-P2-normal/normal-adapter`, `G-O08/09`, `GN04/05/06` | 같은 쌍이라도 호출보존과 새환경교체 질문이 다름 | O01 P1전체는빈경계에서기각; G04 실제관측은 지정고정입력/소비자에한정 | 정상값하나로전체P1통과라고요약하는가설을빈2D로기각 | 요구된 warning/empty 정책과 consumer schema를 고정 |
| Q5b 결론불변·적용외도 남겼나 | O02실행된기능/O04는P1P2불변; G01fullCRS/write적용외 | `H-O02-*`, `H-O04-*`, `G-O01/02` | alias정상범위실제일치;read-only가원래writer였던것처럼실패분자에넣지않음 | O02같은사건의다른alias전부native검증아님 | P1/P2차이를만들려고무관한쓰기질문을강제하지않음 | 관련있는원역할/기능이새로명시되면그범위만재평가 |
| Q6a 실제외부전거/표준두기록을읽었나 | EXT01mo→ro,EXT02bhk→4수신자 실제기록 | [IANA registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry), `STD-S06/07`; [외부원장](streams/standards/external-records.json) | Deprecated/Preferred-Value/Comments·수신Added를역확인;upstream날짜와등록날짜구별 | SIL원자료접근실패;원ISO승인문은미확인.IANA namespace로만주장 | mo.txt는다른시점이름변경;bhk첫수신자를자동선택하면다른3개를잃음 | 원ISO/SIL승인기록또는옛내용의언어구별근거 |
| Q6b 옮길규칙과software시험경계 | ID비삭제·방향·일대다·날짜·원근거보존은이식가능 | [RFC5646](https://www.rfc-editor.org/rfc/rfc5646.html), [RFC8141](https://www.rfc-editor.org/rfc/rfc8141.html), [RFC3986](https://www.rfc-editor.org/rfc/rfc3986.html), `STD-S05` | 이름정규화·자원식별·위치해석을구별 | 표준별칭이함수scale/오류/정보손실을보증하지않음;LC정책을실제인명merge사례라하지않음 | 언어tag대체규칙만으로GEOARROW구consumer수용판정을내릴수없음 | 고정software입력·환경·consumer의실제출력/예외 |
| Q7a 한문서/입력/역확인이보류를바꾸나 | O03 exact radius로보류변경;C02orig해시로원판공백보완 | `H-O03-P1-exact_boundary`, `PA-O04`, archive-verification | 새로운증거의범위만기존미관측을갱신 | 원source확보로native동등성을갱신하지않음 | 현재pythonwareURL이나PILVERSION상수만으로갱신하는가설기각 | G03고정해시/G04null/EMPTY/ARGdefault·YES는GN행으로확인;G04bboxNO조합·Rasdamanbuild/server가남음 |
| Q7b 옛답재독시보존할것·복구 | 옛ID/판정/판/설정/절/원기대유지;관계append | [relations.csv](relations.csv), [first-assessment](evidence/first-assessment.json), [075 인수](streams/root/intake-075.json) | 모든26관계에옛인용보존/적용판/복구/재개가있음 | 실제생산record미제공이라수선적용실행은아님 | Lean3bytes유지+Lean4추가,Choibalsan삭제+별도Link는단순삭제로해석못함 | 원record한개에제안관계를적용한diff와역방향복구확인 |

## 필수 산출물·분모·중간 커밋 대조

| 요구 | 실제 근거 | 상태/한계 |
|---|---|---|
| 배정 시 규칙·브리프·자기항목·유일의존 확인 | evidence/assignment.json, manifest.json, streams/root/intake-075.json | 시작d73c8ec…와계획0d2b084…구별;다른PLAN#19의중간자료미전제 |
| 결과 전 모집·P1/P2·U/T 봉인 | SCOPE.md, 최초frame, `dfdfe1b…` | 원SCOPE지문유지. 로컬seal60114f7과원격same-tree경위를기록 |
| 원판·원절·관측 묶음 | `dd81c973…`, `2f0afa4d…` | 현재HTTP/정적/미관측구별;원배포물불가/후속보완을덮어쓰지않음 |
| 관계·수선·반례·가림검토 묶음 | `eaee6360a23c9415353e02c13c9f44bf425d887b` | 26관계,조건부③2행;최초판정과재판독원본유지 |
| 자연·대조·외부 분모 | frame.csv, 외부원장 | 자연GIS4+OSS4,대조3,외부2;합성/구별입력추가사건0 |
| 독립 원저작 ≥20 | sources.jsonl, EVIDENCE_MAP.md | 32계보;166출처/접근행·121본문판독행은별도분모 |
| 모집 결손 보존 | frame/streamrecruitment | 자연양판원문8/8;C02원archive후속확보로전후원문3/3. 접근실패21행은기각근거와분리 |
| 같은쌍두질문 | observations.csv, RESULT표2 | GIS3/4·OSS4/4둘다적용.G01은원역할밖요구를적용외로표시 |
| 실제 실행/미실행 구별 | OSS historical200호출/49대응, GIS GN11묶음/자연3사건;현재GDAL/root별도영수증 | 자연native7/8;대조native0/3. HTTP11은기능실행아님 |
| 가림재판독자/일치의한계 | streams/review/REVIEW.md, RECONCILIATION.md | 자연4+대조2. 별도도구agent,통계적독립일치율계산안함 |
| 출처·관측·관계 참조/소유범위 | audit.py, evidence/audit-*.json, session check영수증 | 실제종료값·검사범위수용JSON에기록. 처음실패도보존 |
| 필수 RESULT·SELF_CHECK·수용JSON | 이파일,RESULT.md,evidence/acceptance-evidence.json | 파일존재검사와내용판독을구별 |
| 원격 결과판 재독·마지막HANDOFF단독커밋 | 최종HANDOFF의고정SHA·원격해시영수증 | 결과파일커밋후수행. 이행전에는성공으로표기하지않음 |

## 재개2의 실제 GIS 구별과 감사 반영

| 질문 | 주장 또는 미확인 | 원문 URL·판·절 또는 실행 행 | 확인한 내용 | 적용 한계 | 찾아본 반례와 결과 | 답을 바꿀 최소 후속 확인 |
|---|---|---|---|---|---|---|
| Q3/Q5 정상·오류 불변 | G03의 지정 P1/P2 수용 | `GN01–03`,3.7/3.8 Parquet writer·doc/test source ID | 동일 old file hash, 새1.0 output을구3.7소비자도읽음;invalid compression/PointM거절일치 | 두대각Point·null0;일반규격·좌표변환인증아님 | 판이달라지면항상구consumer실패한다는가설기각 | 비대각좌표·실제null·특정외부consumer |
| Q3/Q5 정상종료와필수기능 | G04 P1부분수용/P2같은이름교체기각 | `GN04/05`, contract-g04-new-name-old/new-consumer | 새structfile을구판이exit0으로열지만geometry0·CRS없음 | C++Arrow14.0.1/14.0.2와PROJ등도달라GDAL단독인과아님 | 정상exit0이성공이라는가설기각 | 실제caller의필수geometry/schema명세 |
| Q5/Q7 판한정alias | GN06alias는geometry복구,bbox4필드추가 | `GN06/07`;고정GDAL3.9 parquet.rst 생성옵션 | 같은3.9에서struct null1 vsinterleaved null0/EMPTY;옛3.8도null→EMPTY | exactschema와필수subset은다른요구 | 모든alias가전schema를동일하게만든다는가설기각;옛null손실을새손실로계산안함 | 같은fixture에GEOARROW_INTERLEAVED+WRITE_COVERING_BBOX=NO;미실행 |
| Q3/Q7 원래한계와이관변화 | ARG default불가변화와기존nodata한계분리 | `GN08–11`,3.7/3.8/3.9 receipts | default3.8거절,YES복구,3.9부재;3.7부터nodata-32767 | -9999는일반pixel로남고봉인요구불충족 | 지원sentinel로fixture를바꿔성공처리하는가설거절 | -9999를보존하는이름있는변환구현과원소비자시험 |

원장104관측의 시간·증거 경로·source ID를 검산하며, 이전 정적 기대를 삭제하지 않고 GN11행을 덧붙였다. 근거 출처 R035의 포장 관련 귀속을 최초 fork 공지의 실제 내용으로 좁혔고, PythonWare의 현재 작성자 변경을 단정하던 표현을 발행자 연속성 미확인으로 수정했다. 재열람 실패403은 이전200을 반박하지 않으며 별도 시점 관측이다. 원격 봉인은 최초 GIS 취득보다47초 늦었지만 보존된 로컬60114f7(11:28:00 UTC)의 tree가 원격dfdfe와 동일해 사전 로컬봉인을 검산했다. Git시각·작성자 자체가 외부 공증은 아니라는 한계는 그대로다.

## 수용 판단

식별·계보·출처 보존과 범위를 명시한 수선 결정은 연구 원장으로 사용할 수 있다. **모든 제품·판·입력의 호환성을 승인하는 결과는 아니다.** GIS는 G02–G04의 지정 입력·구 소비자까지 실행했고 G01 Rasdaman server/build만 native 미확인이다. 원PIL/scikit-learn 역사 환경, CPython 대조 양판, 미구현 adapter, G04 bboxNO 조합 및 아직 시험하지 않은 실제 소비자·입력은 제한으로 남는다. 따라서 최종 인계는 PARTIAL과 실제 충족한 범위를 함께 적는다. 실행 불가 항목은 [REPRODUCE.md](REPRODUCE.md)의 입력·명령과 마지막 HANDOFF의 최소 첫 행동으로 재개한다.

현재 실패 URL이나 본문 미취득을 반대 증거라고 쓰지 않았다. 증거를 읽고 기각한 것은 원문/실행 행으로, 접근 실패는 access_status와 body 미확인으로 구별했다. source_required_fields 최초 검사에서 실패한 외부 접근5행의 빈 finding을 발견해 “본문 미확인, 접근상태만 확인”으로 명시했고, 최초 종료1 영수증과 수정 후 종료0을 모두 보존했다.
