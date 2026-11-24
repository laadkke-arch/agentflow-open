# 한국어 추천 카드: 대상+목적을 보존하는 세 가지 선택
설계 예이며 새 실험·실제 201 논문 재검증 아님. 201의 고정 routes.csv/usage.csv(2fc69a2d9092330e30097c018427a45b1bd7d0d9) C/P01/C22/C23/C26에 한정. 제품 목적은 개발자의 관련 부품·원리를 찾게 하는 것. 추천 역할(왜 읽나), 객체 종류(무엇을 열나), 근거 수준(무엇을 확인했나)을 분리한다.
## 목적별 비교
|목적|도착 객체(201 기록)|A 보이는 앵커 자체|B 주변 문맥만|C 숨김 보충(예상 이름)|공통 설명|
|---|---|---|---|---|---|
|비교 문헌|https://joss.theoj.org/papers/10.21105/joss.07120.pdf (논문)|colorspace 논문 — 비교 문헌|비교 문헌이라는 heading 아래 ‘colorspace’|colorspace<span class="visually-hidden"> — 비교 문헌</span>|seaborn 언급의 배경/비교를 읽는다. 사용의 증명은 아님.|
|호출 예|https://github.com/retostauffer/python-colorspace/blob/v1.0.0/_quarto/articles/usewith_seaborn.qmd (소스 문서)|colorspace — seaborn displot 호출 예|호출 예 heading 아래 ‘colorspace’|colorspace<span class="visually-hidden"> — seaborn displot 호출 예</span>|v1.0.0 palette를 전달하는 예. 실행 이력 아님.|
|그림/결과|https://joss.theoj.org/papers/10.21105/joss.07120.pdf (출판 PDF Fig.5)|colorspace 논문 — 출판 그림 Fig.5|출판 그림 Fig.5 heading 아래 ‘colorspace’|colorspace<span class="visually-hidden"> 논문 — 출판 그림 Fig.5</span>|Fig.5 오른쪽. 실제 실행 재현 증거 아님. 페이지 fragment 추가는 검증 전 제안.|
비교 문헌과 출판 그림은 현재 같은 PDF href다. 두 목적을 반드시 서로 다른 리소스로 만들지 않는다. 동일 href·동일 열기 동작이면 한 링크 ‘colorspace 논문 (비교·Fig.5)’ + 위치 안내로 합치는 대안 유지. 정확히 검증한 fragment/별도 artifact URL이 생겨야 별도 목적지 링크로 분리한다. 생성 경로 C22는 https://github.com/retostauffer/python-colorspace/blob/v1.0.0/paper_assets/paper_makefigures.py ; 이름은 ‘Fig.5 생성 코드 (실행 미확인)’이지 ‘실제 산출물’ 아님. 원본 이미지 바이트 링크 미확인. C 논문/생성기 높이 불일치 유지.
## 두 탐색과 음성 명령
A: 문단과 목록 모두 대상·역할 텍스트 유지 기대(W01/W02/W04); 짧은 대상+역할만 이름에, 긴 근거는 본문. 시각/음성 명령의 동일 문자열 유지(W07); 긴 제목이 반복되면 스캔 비용 상승.
B: 연속 읽기 시 프로그램적 문맥이 연결되면 목적 파악 가능(W01/W05); 링크 목록에는 같은 colorspace만 남을 위험(T01/T05/R01). 단순 인접 heading이 문맥 연결이라는 전제 금지. 동일 목적지 반복이면 중복 통합이 더 낫다(W09/D12).
C: 시각적 간결성, 기대 이름은 visible prefix+hidden suffix(W03/W08); 목록의 목적 구별은 구현 의존. 숨김을 사용하면 시각 이용자는 주변 명시 문맥 필요, 음성 명령에 visible prefix 유지. 문자열 공백(D09), macro 중복(D10/D11), pseudo 노출(D13), 언어/RTL/음성 명령, CMS 비용 확인. 숨긴 내용이 핵심 목적이면 A를 우선 비교.
대안 D: 동일 visible text+aria-describedby로 별도 설명. 이름은 동일일 수 있음(W03). 목록에서 설명을 함께 노출한다는 기기별 관측 없이는 A/C와 동등하지 않다. aria-label로 보이는 문자열 대체/삭제하지 않기.
세 카드 모두 규칙 기반 기대이며 사람 성공률/기기 음성 미측정. 실제 기기 시험에서는 같은 href 합치기 vs 별도 fragment, A/B/C/D를 비교, 두 목록·연속 탐색의 표시/음성·보이는 label 명령을 별도 기록한다. 목적지 정확성을 먼저 검증; 문구로 불확실한 증거를 승격하지 않는다.
