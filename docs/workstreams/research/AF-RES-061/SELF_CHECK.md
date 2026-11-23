# AF-RES-061 자체 검토 — 주장·반대 자료·남은 입력

## 검사 범위와 상태

상태는 **부분 인계**다. 조사·보조 검증·필수 문서·원장 정리는 끝내되, 접근/원자료 결손을 완전 수용으로 바꾸지 않는다. 앞 세션의 사전 예측과 실행을 재개 세션에서 반복하지 않았다. 원격 봉인 `02359364000057f69b00594d8b43571ac72df298`, 봉인 뒤 증거 `672366cdf4542d4ca9f579963d66c2745f4316ed`를 보존했다. 최종 실제 검사 SHA와 원격 재열람은 `HANDOFF.md`에 기록한다.

root의 의미 검토, 별도 문맥 분담자의 그래프·애니메이션·계보 검토, 구조 검사기는 서로 다른 검사다. 같은 모델의 문서 검토를 독립 인간 실험·외부 전문가 인증으로 부르지 않는다. 구조 검사는 경로·개수·봉인 해시·표·참조를 확인할 뿐 외부 주장의 참이나 제품 유용성을 자동 증명하지 않는다. [graph review](streams/final-audit/graph-review.md), [animation review](streams/final-audit/animation-review.md), [source review](streams/final-audit/source-audit.md), [검사 출력](evidence/audit-final.json).

## Q1. 실제 사용 목적과 판을 혼동했는가

**결론·근거.** 네 구성요소의 공식 목적·배포·소스 대응은 [frame](frame.csv)에 있다. D3 #166은 group filter, Graphviz #2852/원포럼은24노드/23edge의 정상 이미지 생성, react #2377은 여러 instance별 ratio 변경이라는 실제 요청이다. Android는 기간별 최초 적격 요청자가 미확인이다. 수치 주 입력8개는 연구자가 정한 진단이며 요청자의 실제 입력을 대표하지 않는다. [G044/G053/G064/R041/A017](sources.jsonl).

**내 결론을 깨는 자료를 찾은 방식.** release±365일·제목 단어·오름차순 모집표를 다시 살펴 앞선 적격 이슈를 누락했는지, 다른 engine/단순 설치/PR인지 점검했다. D324건 중 #162는 unit-test 요구, Graphviz7건 중 neato/dot/gvpr 또는 build만 쓰는 건은 제외했다. react9개 제목에서 DNS #2370을 제외했다. Android 공식 tracker·공개 HTML 날짜 검색·공식 코드 이력을 시도했으나 완전 정렬 후보목록을 얻지 못했다. [graph issue roster](streams/graph/issue-search-rosters.json), [react issue metadata](streams/react/issue-metadata.json), [Android recruitment](streams/android/issue-recruitment.json).

**반대 근거와 영향.** D3 실제 예제는 mutable v5이고 정확 component판 미확인, Graphviz 요청은15.1.1이며 선정14.1.1과 다르고 모집기간은 오른쪽이 미완성, react 요청은10.0.1이다. API 목적을 동일판 작성자의 성공으로 확대할 수 없다. Android2021 보조 이슈로2024–2026 빈 자리를 채우지 않았다.

**뒤집힐 조건·최소 입력.** 공식 tracker의 완전한 기간 목록과 첫 적격 본문, 각 요청자의 lock/version·입력·frame trace가 필요하다. 더 이른 적격 사건을 찾으면 최초성만 정정하고 봉인 주 입력은 바꾸지 않는다. 사용자 성공·우선순위는 실제 후속 보고로만 갱신한다.

## Q2. 같은 용어·식을 차용 기록으로 승격했는가

**결론·근거.** D3는 Barnes–Hut 이름과 중간 주소, Graphviz는 Hu 직접·Barnes–Hut 간접, react는 과거 소프트웨어 영감, Android와 react의 특정 진동 원저작은 미확인이다. [transfer](transfer.csv), [D001/D005/D006/D013/R038/R050](sources.jsonl).

**반증 탐색.** 고정 README·force 문서·소스 주석, sfdp 설명·Hu 문헌[2], Android 네 핵심 Java 파일/API, react 현재/과거 태그 README와 직접 연결한 react-motion stepper를 읽었다. 출판사·ADS·저자 서지·공개판·아카이브를 따라1986 원문 접근을 시도했고 실패는 [donor search log](streams/donors/search-log.jsonl)에 남겼다. README가 알려준 tweet/video는 열리지 않아 본문 독해에서 제외했다. [react search log](streams/react/search-log.jsonl).

**반대 자료.** react-spring에는 소프트웨어 영감을 실제로 명시한 문장이 있으므로 ‘아무 인용도 없다’는 결론은 틀린다. 반대로 공식 physics 용어·해석해라는 주석만으로 MIT 채택을 주장하는 것도 틀린다. Hu 자체는 동종 연구라 ‘네 B 모두 타 분야 원논문’이라는 설명을 거부한다.

**뒤집힐 조건·최소 입력.** 특정 원문·절과 구현 선택을 연결하는 유지보수자의 당시 설계 문서·commit·공개 발언. 없으면 명시 인용 관측0의 **검색 범위**만 말한다. 개발자가 그 원전을 읽지 않았다는 부재 증명은 하지 않는다.

## Q3. 변수·단위·적분·종료의 대응이 실제인가

**결론·근거.** D3의 집계 구조와 force kernel을 분리했고, Graphviz의 force와 normalized movement를 분리했다. Android는 해석해+ms/1000+float, react는1ms 속도 선행 Euler+값/ms+ceil(dt)다. [T-*-POST](transfer.csv), [G020/G025–G030/A012–A016/R024/R032](sources.jsonl).

**반증 탐색.** d3가 중력 inverse-square 크기를 쓰는지, theta0이 exact인지, Graphviz가 제안 좌표를 실제로 보존하는지와 public maxiter 전달이 있는지 코드를 추적했다. `getPos`를 읽은 뒤 random overwrite 경로를 확인하여 초기 인상을 바로잡았다. 수식 사진/주석으로 끝내지 않고 executable 계수와 caller를 읽었다. Android는 세 감쇠 branch와 threshold를, react는 단위 factor·step·fallback·stop을 추적했다.

**반대 자료·정정.** d3는 크기1/r이고 signed-zero cell을 생략한다. Graphviz header의 단순 계수와 실행 계수가 다르며 n≥45 normal quadtree는 정점 루프 전에 만든다. 모든 집계가 매 노드 이동마다 재계산된다고 일반화하지 않는다. react 문서의 precision default와 코드 fallback도 다르다. [graph audit](streams/final-audit/graph-review.json), [animation audit](streams/final-audit/animation-review.json).

**뒤집힐 조건·최소 입력.** 동일 배포 소스/JS bytes, 동일 input/time schedule로 대응식과 다른 trace가 나오면 배포 연결과 실행 경로부터 재검토한다. 물리 kg·m가 필요한 요구가 나오면 현재 화면 속성 대응만으로 충족했다고 하지 않는다.

## Q4. 정말 결과 전 예측이고 두 보기의 차이인가

**결론·근거.** 24행은 봉인 commit의 원문과 동일하다. GV A2행은 결손, 비교 가능한6행의 운영 차이는0이다. B의 조건부 수치는 수신판의 보류를 바꾸지 않았다. [predictions](predictions.csv), [seal](evidence/prediction-seal.json), [comparison rule](evidence/comparison-rule.json).

**반증 탐색.** 세 API baseline·세 A예측·B예측·창 해시와 Git tree를 대조했다. root의 창 밖 노출과 B 독자 교체가 봉인 전에 남았는지, source/결과 파일이 seal tree에 없는지 검사한다. 노출 로그와 창의 word/code/equation/figure 수를 읽어 짧은 창이 실제 동등한 정보라는 주장이 없는지 확인했다. [reader amendment](evidence/reader-amendment.md), [B exposure](streams/donor-reader/exposure.md), [graph exposure](streams/graph/exposure.md).

**반대 자료·한계.** root는 창 선택 과정에서 과다 노출됐고 학습 지식도 제거할 수 없다. A는37/239/63단어, B는247/195/213단어이며 같지 않다. D3 A의 runtime판과 Android live guide의 역사판 연결은 미확인이다. B-AN/RS는 같은 창을 공유한다. 따라서 문서 종류만의 인과 효과·인간 A/B 실험이라고 하지 않는다.

**뒤집힐 조건·최소 입력.** 기존 동률을 사후에 차이라고 재분류하지 않는다. 새 처치·독립 독자·다른 입력은 별도 사전 프로토콜과 결과 차폐로 시작해야 한다. 현재 차이행 분모0의 정확률은 해당 없음이다.

## Q5. 원시험·원출력·이번 보조 실행을 섞었는가

**결론·근거.** 주8행 모두 같은판·같은입력의 독립 보관 원출력은 미확인, 확보0/8이다. D3/AN/RS의6행 자체 출력은 보조이며 GV2행은 미실시. [observations](observations.csv). 소스 규칙과 기대/실측의 주소를 별도 열로 두었다.

**반증 탐색.** D3 선택 태그5 test군, Graphviz 관련 regression/fixture, Android 같은SHA SpringTests와 cancel 설계 시험, react SpringValue test와 snapshot을 열어 exact main input·assertion·보관 trace를 찾았다. 원래 입력과 다른 fixture를 main output으로 승격하지 않았다. [graph inventory](streams/graph/test-inventory.json), [Android test](streams/android/evidence/SpringTests.java), [R028/R052](sources.jsonl).

**반대 자료.** forceCollide coincidence 대칭은 manyBody의 답이 아니다. Graphviz의 isolated node test는 이름과 달리 neato를 호출한다. Android에는 미등록/ignored·무효한 bounce-count 분기, react에는 xit 및 duration snapshot이 있다. 이런 소스 선언을 성공한 원실험으로 세면 결론이 과장된다. 전체 upstream suite 실패라는 주장도 하지 않았다.

**검사 정정.** react stop callback의 최초 null은 연구자 listener placement 오류여서 [stop-correction](streams/react/stop-correction.json)의 재실행만 callback 판정에 썼다. 이전 artifact manifest의 CSV2개 해시는CRLF이고 committed bytes는LF다. [animation-review.json](streams/final-audit/animation-review.json)에 둘의 정확한 대응을 남겨 원 기록을 보존했다.

**뒤집힐 조건·최소 입력.** 동일판·동일 입력·schedule·원작성 주체의 retained trace가 필요하다. 현재 기기/React/native 미실행 부분은 [재현 안내](streams/android/reproduce.md)와 [react 실행 명령](streams/react/execution.md)을 따르되 새 실행은 새 영수증으로 남겨야 한다. 자체 재실행만으로 역사적 원출력 결손이 해결되지 않는다.

## Q6. 처음 결론을 깨는 경계가 있는가

**결론·근거.** 계열별로 정상 입력 밖의 실제 경계를 찾았다. 배치: coincidence·거리 cutoff·theta·mixed sign·후처리. 애니메이션: 잔류속도·snap·큰 frame·강한 감쇠·clamp·cancel·옵션 소비. [graph findings](streams/graph/findings.md), [Android findings](streams/android/findings.md), [react findings](streams/react/findings.md).

**반증 탐색.** 그래프 검색 `sfdp overlap/pos/maxiter`와 D3 per-node cutoff 이슈, 애니메이션 cancel/precision/skipAnimation·Remove animations 설계 경로를 조사했다. 원전 가정을 실제 UI에 그대로 적용할 때 반대로 되는 조건을 고른 후 기존 사후 보조 입력과 원소스 규칙을 대조했다. 처음 scale0이면 모든 animation이 끝난다는 해석을 확인하기 위해 앞 세션이 추가한 damping0 출력은 별도 v1/수정 영수증으로 남아 있다. 새 예측으로 세지 않았다.

**반대 결과.** AN-B는 내부 overshoot와 공개 무초과를 동시에 보인다. RS-B는 clamp를 켜도1ms 표본 초과가 가능하지만60Hz 표본에서는관측0이다. 따라서 임의 schedule에서 clamp가 틀렸다는 단정도 틀린다. 극단 friction3000은 고정step 반례이지 일반 사용자의 실패율이 아니다. 외부 물리 연구의theta수치와 오차율을 d3로 옮기지 않았다.

**뒤집힐 조건·최소 입력.** 실제 입력 분포·허용 오차·frame schedule·제품 요구가 필요하다. 반례의 특정 조건을 제거해도 성립하는지는 따로 검증한다. 일반 reduced-motion 지침은 해당판이 옵션을 읽는 코드·실제앱 적용과 분리하며, 실제 사용자 편안함이나 읽기 성능을 이번에 측정했다고 하지 않는다.

## Q7. 첫 링크와 실제 행동의 변화가 근거 있는가

**결론·근거.** 기본 첫 링크는 구체적인 선택·경계를 결정하는 수신 절이다. 근사오차·모델 초기조건이 목적이면 원전, 목표가 모호하면 사용자 우선순위 확인으로 바꾼다. [cards](cards.md)의4카드에는 각4관점의 조건과 최소 전환 자료가 있다.

**반증 탐색.** 원전이 항상 더 좋은 추천이라는 가정을 반박하려고 API만으로 해결된 D3filter/reactclamp 위치, 요청자가 시각적 ‘해결’을 반박한 precision 이슈를 읽었다. 그래프는 Hu의mesh 유형별 결과와 실제 overlap 사건, UI는 Heer/Robertson·Dragicevic의 측정과 W3C/WebKit의 옵션 통합을 비교했다. [G044/G047/R045–R048/D013/E002/E003/D011/D012](sources.jsonl).

**반대 자료.** staging 선호와 정확도가 다르고 adaptive pacing도 항상 우월하지 않았다. E003의2280trial 인쇄값과2880 요인곱은 일치하지 않는다. 원시자료·저자 정정 없이 메타분석 분모를 만들지 않았다. [재독해](streams/final-audit/source-audit-sources.jsonl). AndroidRemove animations 패치나 #1389의 설정 변경은 실제 저자 행동 보고지만 이번 원전 링크 처치의 효과가 아니다.

**뒤집힐 조건·최소 입력.** 원전을 받은 실제 설계자의 기존 선택·읽은 절·바꾼 결정·결과를 연결한 기록. 접근성의 경우 실제 앱·설정·사용자 목표와 결과가 필요하다. 지금은 반환안의 조건과 근거를 제시할 뿐 효과는 미실시로 둔다.

## 수용 판정과 재개 우선순위

31고유1차저작,4구현·8행,24봉인행,2필수표·4카드·Q1~Q7·반증 원장·변경범위 검사는 실제 파일과 [수용 원장](evidence/acceptance-evidence.json)을 따라 확인한다. source_id164개와 저작31개는 다른 수다. 독립출력 연구4개는 주8행의 원출력4개가 아니다. [final counts](evidence/final-counts.json), [source audit](streams/final-audit/source-audit.json).

재개 첫 행동은 [Graphviz A 선정 결손](streams/graph/gv-example-selection.json)과 [공개 입력 경계](streams/graph/transfer-notes.md)를 읽고 공식 초기화·한 단계 trace를 찾는 것이다. 기존 A예측을 채우지 않는다. 다음으로 Android의 완전한 release-window 모집 frame과 주입력의 독립 원출력을 확보한다. 원전의 설명 가치와 실제 채택/행동효과를 검증하려면 구체적인 저자·사용자 기록이 별도로 필요하다. 자료 없이 이미 끝난 보조 실행을 반복하는 것은 이 결손을 해결하지 않는다.
