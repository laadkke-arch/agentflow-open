# AF-RES-061 — 차용 근거와 구현 경계의 사전 계약

## 고정 범위와 시작

계획 기준은 aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75, 실제 시작은 chore/workspace-foundation@1e741fd0def88ef56b1060a478d81f1985a4e760이다. 작업 브랜치는 work/research-af-res-061, 쓰기 범위는 이 디렉터리뿐이다. manifest.json은 지정 start 명령을 현재 클라우드 checkout에서 실제 수행하여 생성했다. 공통 control은 읽기만 했다. 실행 주체는 ChatGPT root와 같은 모델의 분담자이며 사용자 PC, 별도 인간 피험자 또는 역사적 원작성자의 실행으로 부르지 않는다.

AF-RES-057 인계 71d13fea95bae733939d36463a671f659a5651d2와 본문 5c5b5299ec57eefde78029a23a62cfb48f508469의 여섯 지정 파일을 인수했다. E/D 동률 6/6, 완전 공개 원 A/B·redo 연결 0/6, PARTIAL은 인수 사실이다. 053/057의 과거 출력은 새 예측으로 세지 않는다. 상세 readback은 evidence/inherited-inputs.json.

## 네 자리와 판

공식 component 배포 기록의 published/released UTC가 2025-12-31T23:59:59Z 이하인 마지막 non-prerelease를 택한다. 저장소 최고 태그만으로 구성요소 판을 대신하지 않는다. Graphviz sfdp는 별도 패키지가 아닌 해당 Graphviz 배포의 포함 엔진으로 기록한다. AndroidX의 다른 모듈과 react-spring의 root private workspace는 대체 표본이 아니다. 메타데이터 근거는 streams/*/sources.jsonl과 frame.csv에 있다. 실제 배포 bytes 대응은 예측 봉인 후 검사하고 결손을 유지한다.

- D3: d3-force 3.0.0, 소스 156712c8c3285d77cb487e1685c5adafcd0394a4.
- GV: Graphviz 14.1.1 sfdp, 소스 a74b50c20fc624f46f72e24f981b261f6e5edf71.
- AN: androidx.dynamicanimation:dynamicanimation 1.1.0, 공식 release log endpoint d5923c378c00b537f3421786eb3a50e6f6868386; 배포 source bytes 일치는 후확인.
- RS: @react-spring/core 10.0.3, 소스 b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a.

## 결과 차폐와 시간 순서

이 파일의 첫 커밋 전에는 공식 배포 메타데이터와 선행 입력만 읽었다. 분담자 검색에 노출된 이후판 release 제목/짧은 API 문구는 각 search-log에 남긴다. 일반 학습 지식은 제거할 수 없다. root는 단일 독자로 A와 B를 모두 보므로 이 조사는 무작위 인간 A/B 실험이 아니다. 자료별 최초 독해 시각과 독자를 기록한다.

1. **①** 이 계약, 4자리 판, 후보 입력, 모집·창 규칙을 원격 커밋한다. 원전 수식·구현 코드·선정 시험 assertion을 아직 읽지 않는다.
2. 각 담당자는 **공통 공개 API만** 읽어 normal/boundary 입력과 baseline 예상·판별 불가·반증 조건을 저장한다. source order로 boundary 옵션을 확정하며 수정 이유는 남긴다. 원격 baseline 커밋 전에는 A 예제/B 원전/구현 본문/원출력을 열지 않는다.
3. A는 공식 동종 예제의 첫 적격 절 하나, B는 원전의 첫 관련 절 하나를 추가한다. 같은 baseline에서 두 보기를 각각 평가한다. A 독자는 B를 보지 않고, root B 독자는 A의 예측/자료를 최종 봉인 전 열지 않는다. root는 baseline만 인수한다. 독립 모델 표본이나 순서 효과 제거로 주장하지 않는다.
4. **②** baseline/A/B 24행, 추가 창 metadata, 명시 인용/변수 대응 중 결과 없는 내용을 봉인한다. 원출력/결과 파일은 이 커밋에 포함하지 않는다. 해시와 SHA를 남긴다. 구현 함수 읽기는 baseline/A/B 봉인 후로 미뤄 예측에 구현 정답이 유입되지 않게 한다. 이 때문에 ②의 초기 transfer는 문서·원전 대응이며 코드 대응은 ③에서 후검증한다.
5. **③** 봉인 뒤 고정 SHA의 원시험·fixture·공개 출력·저자 실험과 소스를 열고 대조한다. 같은 입력 자료가 없으면 연구자 손계산/실행으로 분리한다. 정정은 새 열/파일에 두고 봉인 예측을 덮어쓰지 않는다.
6. **④** 8행/4행 필수 표, 반환 카드, Q별 반증, 수용·분모 원장과 검사 기록을 커밋한다. 고정판 RESULT/acceptance를 원격 재열람하고 session check --fetch를 실제 수행한 뒤 HANDOFF만 마지막 단독 커밋한다.

## 입력과 두 질문

비교 단위는 4구현 × normal/boundary = 8행, 각 baseline/A/B = 24예측이다. 단위가 다른 구현의 수치를 순위화하지 않는다. 원시험 없는 자리를 제거하거나 다른 구현으로 바꾸지 않는다.

- D3-N: 두 노드 (0,0), (3,4), vx=vy=0, strength=-30, alpha=1; 공개 force 호출 1회의 velocity 변화. simulation tick 이동·velocity decay와 직접 force를 구별한다.
- D3-B: 같은 두 노드/호출에서 distanceMax=4. 무한 거리 baseline과의 domain 차이. 동일 위치/default distanceMin 및 theta 변경은 사후 보조 반례로 유지하고 주 8행에 추가하지 않는다.
- GV-N: 두 노드 (0,0), (3,4), 무방향 한 edge, K=1, 1회 force/movement. 좌표/내부 단위·iteration을 공개 API가 고정할 수 있는지 먼저 묻는다. 불가능하면 정확히 끊기는 API 지점부터 미확인; 최종 배치 그림을 한 단계 힘의 정답으로 쓰지 않는다.
- GV-B: 같은 그래프의 coincident 시작 (0,0),(0,0). overlap/approximation/초기화 정책이 공개된지 확인한다. 연구자 internal helper를 만들면 보조 실행이다.
- AN-N: 시작 0px, 목표 100px, 초기 v=0px/s, stiffness=100, dampingRatio=0.5; 16ms/250ms sample과 0..3000ms 내 target crossing. 서로 같은 시간점을 원식·API에 사용한다.
- AN-B: 시작 99.9px, 목표 100px, 초기 v=10px/s, stiffness=100, dampingRatio=1, minimumVisibleChange=1px; API의 첫 문서화된 정지 판정. 원식의 잔류 상태와 UI 종료·snap을 분리한다.
- RS-N: 시작0, 목표1, 초기velocity0, mass1/tension100/friction10; 16ms/250ms 및 0..3000ms의 target crossing. 시간·속도 단위는 API에서 확정하거나 미확인으로 남긴다.
- RS-B: 같은 기본 설정에서 공식 구성 문서의 source order로 처음 나오는 stopping/cancel/clamp 경계를 고른다. baseline 단계에서 옵션·입력을 확정한다. 기본 후보는 clamp=true이며 문서 순서가 다르면 baseline 봉인 전에 이유를 남겨 바꾼다. 모든 결과를 보기 전 정한다.

숫자 입력은 연구자가 정한 진단이며 실제 사용자 사건으로 부르지 않는다. 공개 원시험에 이 입력이 없으면 같은 입력/판 원출력 분모에서 제외하되 행을 유지한다. 가까운 원시험은 별도 연결 자료다.

## A/B 창과 원전 선택

표시 창은 각 첫 관련 절의 시작부터 최대 250 whitespace-delimited 단어이다. heading과 prose를 세며 수식 개수, 코드 행, 도판, UTF-8 bytes, 실제 시작/끝 위치를 별도 기록한다. 원문 자체는 최소 인용/위치/digest로 보존하고 전체 복제하지 않는다. 독자가 실제 본 텍스트는 생성한 창의 digest·단어수와 열람 시각으로 고정한다. 보조 저작 독해와 창 밖 노출은 별도 로그에 남긴다. 같은 단어 수를 같은 정보량으로 주장하지 않는다.

A 후보 순서: 고정 구성요소가 직접 연결한 공식 example/guide → 해당 판 공식 저장소 examples 디렉터리 경로·선언 순서. 첫 정상 motion/force setup을 설명하는 절을 고른다. 입력 또는 기대 출력이 이미 보이는 예제는 의미 노출을 표시한다. 없으면 A 부족으로 보존한다. 시험 assertion을 A 예제로 대체하지 않는다.

B 후보 순서: 수신 문서의 명시된 논문 링크 → 그 중간 논문의 최초 관련 인용 → 저자 공개판/기관 아카이브 → 같은 원리를 설명한 학술 원교재. 구분은 direct / mediated / same_equation_only / researcher_analogy / unconfirmed다. Barnes–Hut, force-directed layout, damped oscillator는 탐색어일 뿐 채택 증거가 아니다. 그래프는 Barnes–Hut 1986 또는 명시된 Hu 원논문 첫 algorithm 절, 진동은 명시 원전이 없으면 OpenStax/MIT 등 첫 damped oscillator 절을 연구자 선택으로 표시한다. 원전 원문의 실험 결과/표는 예측 봉인 뒤에 읽는다.

## 사용자 목적·반례 모집

Q1 주 요청: 각 수신 프로젝트 공식 이슈 저장소에서 선정 release 전후 365일, created UTC/번호 오름차순, component 이름+force/spring/layout/overshoot/stop/cancel 중 적격 단서가 있고 사용자 목표·입력·화면 기대가 있는 첫 이슈. PR/중복/봇/단순 설치 문제 제외. 공식 tracker가 검색 불가하면 GitHub mirror/공식 공개 논의/저자 공개 재현 순서로 시도하고 최초성 미확인으로 남긴다. 후보 제목·필터·제외를 먼저 보존하고 결과 본문은 ② 뒤 읽는다. 부족하면 검색 범위를 사후 확장하되 primary earliest 주장을 바꾸지 않는다.

반례는 (a) D3 동일 위치·거리/근사 제한 (b) sfdp 단일 단계와 최종 pack/overlap 처리 (c) 강한 감쇠·큰 frame·잔류속도·정지 threshold (d) clamp/cancel·reduced motion 실제 option 소비를 대상으로 한다. 목적 충돌은 원전 저자/라이브러리 유지보수자/UI 개발자/움직임·읽기 부담 사용자로 나눈다. 아직 하지 않은 사용자 행동 측정을 암시하지 않는다.

## 자료수와 판정

외부 고유 1차 저작 ≥20. 겹치지 않는 최소 배당은 4 component 계보, 목적/경계의 독립 이슈·설계 저작 ≥4, 원천 분야 독립 원논문/교재 ≥4(천체2·진동2), 독립 원출력·실측 저작 ≥4, 나머지 반례·접근성 ≥4. 한 태그 code/README/test는 1저작. 원문·미러·개정은 같은 work_id; issue/patch/test가 같은 사건이면 합친다. 자료수/참가자수/8비교행/24예측/실행수를 별도 계산한다. 검색 snippet, 초록만 읽음, 실패, 내부 인수, 자체 실행은 20에서 제외한다.

외부 원전의 새 적중은 **사전 A≠B + 동일 판·동일 입력의 독립 원출력 + 원전 절 근거** 셋이 있을 때만 판정한다. 연구자 보조 실행은 독립 원출력으로 승격하지 않는다. 다른 예측행 수와 그중 원출력 확보행 수를 각각 분모로 보고한다. 미확인/관측 0/해당 없음/미실시를 구별한다. 현재 자료를 읽은 사실은 독립 인간 실험 또는 설계자의 실제 행동 변화가 아니다.


## 봉인 뒤 상태 주석 — 기존 계약·예측을 덮어쓰지 않음

최종 예측 봉인은 `02359364000057f69b00594d8b43571ac72df298`이다. 위 결과 차폐 3항의 최초 계획과 달리, root가 원전 탐색 과정에서 창 밖 설명에 노출되어 B 예측을 계속 맡지 않았다. `evidence/reader-amendment.md`에 남긴 사전 정정에 따라 새 문맥의 `/root/bounded_b_reader`가 봉인 baseline과 정확한 B 창만 받아 예측했다. root의 자료 선택 노출, 같은 모델의 학습 지식, 인간 무작위 실험이 아니라는 제한은 제거되지 않는다. 이후 root는 통합을 위해 양쪽을 읽었다. 후속 독해로 사전 예측을 고치지 않았다.

배포 대응의 후확인은 `frame.csv`와 각 실행 영수증에 기록했다. Android 네 Java 파일은 배포 sources.jar와 일치하고, react-spring은 registry gitHead·tarball integrity·설치된 JS의 bytes 대응을 확인했다. 초기 metadata의 `pending/미확인`을 당시 상태로 보존하며 현재 결론은 해당 후확인을 따른다. Graphviz의 native 실행은 미실시다.

`transfer.csv`의 처음 네 행은 예측 봉인 때의 문서 대응이다. 뒤 네 `T-*-POST` 행만 봉인 후 소스 검증을 담는다. 기준→B 비교는 원전 창 추가이며, A↔B는 같은 기준에서 추가 자료의 종류를 바꾼 비교다. B-GV는 동종 Hu 논문이고 천체 원전은 그 인용 계보에 있다. B-D3는 원1986본문 접근 실패 후 학술 원강의 대체, B-AN/RS는 채택 기록 없는 연구자 선택 교재다. 네 개의 순수한 타 분야 원논문 처치를 수행했다고 해석하지 않는다.

실제 예측의 운영적 A/B 차이는 가능한 여섯 행 중 관측0이다. 빠진 GV의 A 두 행은 동률이 아니다. 따라서 차이가 난 행의 적중률은 해당 없음이며, 앞으로 원출력을 찾아도 기존 동률 예측에서 원전의 우월성이 생기지 않는다. 조건부 연속 모델 설명의 추가와 제품 동작 예측의 추가를 별도로 기록한다.
