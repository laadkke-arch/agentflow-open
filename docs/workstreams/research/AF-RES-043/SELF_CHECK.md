# AF-RES-043 · Q1–Q7 자체 점검

이 문서는 키 작성자가 하는 비가림 자체 점검이다. 입력·카드와 다른 새 문맥의 같은모델 판독자들이 원관측을 남겼고, 또 다른 같은모델 문맥이 출처 산입·수식·원장 보존을 감사했다. 사람·외부 독립모델의 재현이 아니다. 첫 결론에 맞춰 사례나 원키를 바꾸지 않았다. 원관측은③ `6c58c98d60351b9b125a8611887fec0972aeae1f`, 키는② `b3aa200fce66f0635e74aa39c4cb008cafd86eff`에 있다.

## Q1. 소비자의 실제 목적을 먼저 확인했는가

**주장.** 소프트웨어 소비문서 원장2개에서4슬롯, 정정 우선 통계/학술에서4슬롯을 유지했다. 자연 표본은 pandas 10min·dsintro, statsmodels Rolling Regression·Regression Plots다. 통계/학술은 목적이 보이는 실제 소비 저작을 연결했지만 완전 표본 수용은 미충족이다.

**직접 근거.** [pandas dsintro](https://pandas.pydata.org/pandas-docs/version/1.5.3/user_guide/dsintro.html) Series is ndarray-like L173–192, 외부href39 L185(FINAL-NP-CONS); [Rolling Regression](https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html) L89–111 및L152–160(FINAL-FF-CONS); [SCB May2024](https://apps.bea.gov/scb/issues/2024/05-may/0524-gdp-economy.htm) L25–31(FINAL-T01-C); [ONS 월간 June2024](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/june2024) §2 L96–97(FINAL-T02-C). 각 소비자의 짧은 원문 인용은 collection/*/cases.json의 consumer_short_quote/source_sentence/consumer 필드에 보존했다.

**반증 시도.** 앞의 statsmodels 후보를 읽고 목적 있는 외부 링크가 없거나 중복/탈락인 경로를 natural/frame.csv에 남겼다. 통계의 뒤 Commons 후보와 다른 학술 소비 후보가 있어도 먼저 선정한 슬롯을 교체하지 않았다. BMJ 원문 HTML/full/PDF/DOI 실패를 보완하려고 PMC 전문을 읽었으나 미러 산입 금지를 유지했다.

**미확인·판정을 뒤집을 조건.** 통계 첫10개 결과의 query별 순위, J02 소비 검색 일부 상세목록, J01 직접 발행자 소비본문이 미확인이다. 원검색 로그와 [BMJ 원문](https://bmjopen.bmj.com/content/11/2/e041022) Methods/ref16을 확보하면 추적·분류별 최소 수용이 달라질 수 있다. 새 검색을 옛 순위로 소급 기록해서는 안 된다. source-count-audit.json에28개 고유1차 하한과 엄격23/24를 따로 열거했다.

## Q2. 날짜·판·절과 두 과업의 기준을 구별했는가

**주장.** 소프트웨어 릴리스/문서갱신, 통계 기준기간/발표/개정, 논문 원문/정정 날짜를 분리했다. C기준은7/8, 원키의 H기준은4/8이며 자연 소비의 실제 외부판은4건 모두 미확인이다. 기준은 문서에서 직접 관측한 사실에 사전 목적 규칙을 적용한 연구자 해석이지, 발행자가 이 실험의 유지/교체 정답을 발표한 것은 아니다.

**직접 근거.** [Python3.11.1 릴리스](https://www.python.org/downloads/release/python-3111/) 제목·날짜L21–25, Online Documentation L52(NAT-PY-RELEASE); [BEA 최초추계](https://www.bea.gov/news/2024/gross-domestic-product-first-quarter-2024-advance-estimate) L11–17(FINAL-T01-O); [ONS 최초추계](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpfirstquarterlyestimateuk/apriltojune2024) L59–70, §2 L103(FINAL-T02-O); [J01 정정](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0301218) L100,123–126(FINAL-J01-NOTICE, FINAL-PLOS-RAW-J01).

**반증 시도.** Python release page의 Online Documentation은 exactpatch경로가 아니라 현재3.11계열 별칭이다. French 추가2022 cut은 소비 출력의2023-03 끝시점 전체를 포함하지 않으므로 소비판 입증으로 쓰지 않았다. [2026 SCB 개정](https://apps.bea.gov/scb/issues/2026/09-september/0926-nea-annual-update.htm) L479–480은 같은2024Q1값을 다시 바꾼다. 숫자가 같아도 같은판이라고 판단하지 않았다.

**미확인·판정을 뒤집을 조건.** L의 소비 당시 URL 존재와 불변바이트, 자연 소비자가 실제 사용한 대상판은 미확인이다. 소비자의 판/다운로드 기록과 해당 발행판이 생기면 H분모가 늘어난다. J02는 현재 제공2018 저작의 문구 대조와 독립2018판 대조를 구별해 S-I에서 제외한다.

## Q3. 네 구성의 정보가 통제됐는가

**주장.**32개 카드에서 같은 요소의 문자열·순서·해시는 동일하다. X가 있는7개 사례에는 판/URL 단서가 없고 UCLA X는 미확인 표시다. 그러나 자극 중립성은 미충족이다.

**직접 근거.** cards.jsonl·components.jsonl·evidence/input-seal.json의SHA-256과 input-integrity.json. [NumPy1.24 ndarray](https://numpy.org/doc/1.24/reference/generated/numpy.ndarray.html#numpy.ndarray) L201–207(FINAL-NP-OLD)에 선택된 짧은 발췌의 원문 위치가 있다. [ONS 소비문](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpmonthlyestimateuk/june2024) L97은 이미 특정 발표를 원href로 가리키므로 T02의 L주소 추가 정보가0인 사실을 확인했다.

**반증 시도.** 원B의 판고정, X의 판단서, 동일구문 중복, 이관주소를 판주소로 오인하는 경우를 모두 감사했다. N-S-01의 B에는 시간 의도 부재라는 연구자 해설이 들어 있어 보류를 암시할 수 있다. J01의 B에3806이 있는 것은 실제2021 소비본문의 관측값이며 후속2024정정 이유를 삽입한 것이 아니다.

**미확인·판정을 뒤집을 조건.** N-S-01의4개 C판독에서 공통단서의 실제 효과는 미확인이다. 이 문장과 질문의 추가 지시를 제거한 새 자극을 별도 사전등록하고 신선한 독자에게 판독하면 B 충분성/행동 불변 판단이 달라질 수 있다. 기존 카드와 원관측은 고치지 않았다.

## Q4. 두 번의 동일 예산과 실제 이동을 지켰는가

**주장.**64판독 모두1~2회의 발행요청을 기록했고, 총73요청 중12실패도 예산에 포함했다. 로컬표시32회에서 실제X28회와 미확인표시4회를 분리했다. 원장에는 처음 카드URL, 다음 실제부모·링크ID/anchor, 도착판·절·문구·실패가 있다. literal href 완전성은2/9다.

**직접 근거.** reads.csv109행, judgments.csv64행, read-seal.json, analysis-audit.md. T01-H의 B/BX는 [BEA archive](https://www.bea.gov/news/archive) 색인에서 두 회를 끝내고 BL/BLX는 [Apr25 발표](https://www.bea.gov/news/2024/gross-domestic-product-first-quarter-2024-advance-estimate) L11–17에 도달했다. J02-BLX-C의 rc-029는 첫문서 [원논문](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201631) L146의 DOI link55실패, 뒤 BL-C의 rc-038은 자신의 새 첫문서 link56을 click해 정정에 도달한 기록이다.

**반증 시도.** 주소추측·다른카드URL차용·검색·실패뒤도구전환·2회초과를 원장과 reader notes에서 확인했다. 관측된 규칙 위반은0이지만 같은독자의 기억과 방법선택은 통제되지 않았다. 원href미확인 접두사6건을 놓친③검사1건을④의7건으로 정정했다. actual부모/링크 연결9/9를 원문철자완전성9/9로 바꾸지 않았다.

**미확인·판정을 뒤집을 조건.** 도구에 드러나지 않은 literal href7건, 당시HTTP본문의 완전바이트와 내부도구동작은 미확인이다. 실제href·원응답을 남기는 고정수집방법과 균형순서 재판독이 확보되면 접근경로와 L/X 정보의 기여를 더 분리할 수 있다. 사후 재열람을 이번 판독 성공으로 더하지 않았다.

## Q5. 네 종류의 짝을 빠짐없이 재계산했는가

**주장.**8×2×4=64짝을 유지했다. C근거성과24/28, 원키H12/16, 자연재구성H4/12, 유효X의H표시14/14다. 자연/정정우선과 C/H의 분모를 따로 계산했다. 규범적 보류4건은 맞는 행동이며 나머지 접근보류는 단정오답이 아니다.

**직접 근거.** RESULT 표1/표2, pairs.csv의pair_id 및criterion_confirmed/both_resolvable/attainment_delta, analysis-summary.json의48집계, 독립계산 analysis-audit.md. [T02 원판](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpfirstquarterlyestimateuk/apriltojune2024) §2 L103은 B부터 네구성 모두같은본문을확인했다. J01은 실제초기공개HTTP를쓴B/BX에서도 원저작을읽어 H4/4다.

**반증 시도.** 원판정64행의 기존필드와③해시를 대조해 변경0을 확인했다. 표2를 배타분류하면 둘다맞음32,보류/대조미확인12,기준미확인20이며 합계64다. 왼쪽만/오른쪽만0을 이득0으로 해석하지 않고 요구근거 도달의 증감을 별도 계산했다. 단순X재표시를 원판대조에 추가하지 않았다.

**미확인·판정을 뒤집을 조건.** 자연H기준0의 비율은 해당 없음이다. J02의 원H는 독립옛문장 근거가 약해 S-I에서 제외한다. 당시판·공통입력·요청경로가 추가확인되면 분모나 효과설명은 달라질 수 있으나 현재 숫자를 먼저 고치지 않는다.

## Q6. 반례와 다른 분야의 관점을 실제로 확인했는가

**주장.** L이 유익/중복인 사례, X가 과거에는맞고현재에는정정필요한사례, 정정이 선택주장에영향없는사례, 값재일치와 절의미변경을 모두찾았다. 실제동일URL의과거·현재HTTP200 반복관측은 확보하지못했다.

**직접 근거.** [J01 정정](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0301218) L123–126; [J02 정정](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0214558) L111–117,130–134(직접HTTP의normalized node148,154도확인); [ONS superseded v1](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/apriltojune2024/previous/v1) §7 L516와 [정정본문](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/quarterlynationalaccounts/apriltojune2024) L523; [현재IHYQ](https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pn2) L382의2024Q2=0.6; [2026 SCB](https://apps.bea.gov/scb/issues/2026/09-september/0926-nea-annual-update.htm) L480의2024Q1=1.4.

**반증 시도.** ‘옛값은현재항상틀림’은 ONS0.6 재등장으로반박된다. ‘정정은인용전체를폐기’는 J02의선택된발현주장과 ONS저축분기문장만고친정정으로반박된다. ‘주소만있으면충분’은 Python실패와 UCLA판부재로반박된다. 같은통계계열의최초보고서(SCB May2024 L29–31)와 수정값보고서(SCB2026 L480)를 비교했다.

**미확인·판정을 뒤집을 조건.** J01 실제 소비자는이미3806이므로 그소비자가X때문에오도됐다는증거는없다. 이번X추가단정오류도0이며 인과적오도는미확인이다. 같은입력·요청경로의 새판독에서 X만추가할때단정오류가생기거나, 정정된주장이실제소비목적과다르다는자료가나오면판단이달라진다.

## Q7. 보관 제안과 두 감도에 증거 수준을 연결했는가

**주장.** 로컬X재표시, 판전용/저작주소, 실제발행판대조를분리하는조건부보관안을제시했다. S-X와S-I는따로계산했고 원규칙을유지했다. S-X의알려진C/H성과는24/28·12/16, S-I는24/28·10/12다.

**직접 근거.** RESULT의세증거수준표, pairs.csv의sx/si열과 analysis-summary.json48집계. [Crossref 정책](https://www.crossref.org/documentation/crossmark/participating-in-crossmark/) L146–165,185(FINAL-CROSSREF)은 DOI와최신상태관계를구별한다. [ICMJE](https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html) L59–63(FINAL-ICMJE)은정정·날짜있는새판·과거판보관·최근판인용을구별한다. 이규칙이모든개별발행자의실제준수를보장하지는않는다.

**반증 시도.** S-X에서X자체없는UCLA를단서없는발췌로간주하지않았다. S-I에서J02H를제외해직접저작주소의개선이독립옛문장기준에서도동일하다고주장하지않았다. 남는T01주소이득은날짜있는원판대조이고, T02/J01 B충분성과 Python실패도함께보고했다.

**미확인·판정을 뒤집을 조건.** 원목적의시간의도,발행판가용성,정정의선택주장영향이달라지면필요필드도달라진다. 사람시간·재방문비용·전송비는미측정이다. 기존036/039의고정결과를새효과크기로합치지않았다. 독립사용자·고정요청방법·중립자극의재현전에는하나의보관방식을모든목적에최적이라고고르지않는다.

## 마지막 원문 대조 및 보존 점검

주작성자가 Q1–Q7의대표URL·정확한절을 다시 열어 확인한17개 행은 evidence/final-source-checks.jsonl에 있고, PLOS 직접HTTP 보완은 evidence/publisher-body-verification.jsonl에 따로 있다. J02정정의직접URL실패와실제View correction클릭성공도별도행이다. 모두수집/진단이며③카드열람에합산하지않는다. 같은모델재독은자체점검이다.

카드·키해시는②와같고 원64판정의기존필드변경은0이다. 새채점은추가필드/별도adjudication으로보존했다. 전체틀의중요한약점세건은 RESULT와HANDOFF에동일한표로끝내며,근거는evidence/weaknesses.json이다. 결과·수용파일의고정원격재독과session check는결과커밋뒤에만실행하고그실제로그를마지막인계커밋에남긴다.
