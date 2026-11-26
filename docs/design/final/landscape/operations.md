# 관리·운영·갱신 신호·가용성: 연구 지형

## 1. 확정·정정·열린 것

**152 · 같은 예산의 발견/관리** [152m][152s][152p] *(b: 내가 재생해 출력 일치)*
- 정책: O 요청 때만. P 목록 순환(표시일 30일 창)+원문 순환. S 공급원별 통지 72h 순번+후속 원문(48h 겹침). F는 S+curl 주 1슬롯. 예산 168h당 HIGH 24요청·786,432B·480판독초, LOW 절반. 유보 182일·신규 15·요청 364.
- **"15건"은 분모다.** 발견 수는 S·F 14/15, P 13/15, O 10~14/15. 차이 1건은 CF-2026-01(표시 1/1, 편입 1/30)이다. P가 놓친 원인은 순환과 표시일 창(`replay.py` catalog())의 겹침이고, 창을 없앤 archive-catalog에서 P도 14/15다. 15번째 CF-2025-11(편입 4/1)은 전 정책 창 밖.
- **"더 빨리"는 HIGH·주류 수요의 발견 지연 중앙값이다.** P 27h, S 57h(둘 다 찾은 13건만 놓으면 27 대 51). 차이는 curl 3건(P 약 20h, S 약 68h, 72h 순번). 자원은 S 275요청·5.3MB, P 419요청·16.7MB. LOW·희소의 공통 13건은 P 92.1h, S 27h로 뒤집힌다.
- O는 LOW·주류에서 curl 신규 0/3. F≈S라 희소 전용 슬롯 이득 없음. 안정 대조 159질의 전 정책 일치, P만 배경 재방문 112회. 복구 직접 포착 0/2(S·F는 사후 보고 2/2).
- big-catalog(바이트 2~3배): P LOW·주류 잘못된 제외 654→1,590h, O HIGH·희소 정답 309→183/364, S는 14/15·340/364 유지. 모형: 항목당 하루 요청 0.0142(주류)/0.0261(희소) 미만이면 O 전송량<S. 10만 건 P는 REST 59.9/h(한도 60).

**024 · 미리 고른 이유의 무효화** [24r] *(b: 내가 재생해 6파일 일치)*
- 64이유×16분기, 상한 20: D(정기 직접) 11/11, S(신호 후 원문) 8/11, 선별 정밀 86/913=9.4%, S는 원문 108개 덜·5,672,462B 더. O 11/11(8요청)은 사건 주소를 아는 상한. 상한 10: D 7·S 0, 40: 둘 다 11. S가 놓친 셋은 이름 유지·계약 변경(imghdr.tests, netrc, WASI 생성자).

**019·015 · 신호의 판별력** [19r][15c] *(a)*
- 019: 활동 신호 엄격 대조 사건 3/7=대조 3/7(판별력 없음). 월 직접 확인 35/35(시행 37일 전, 공지 후 16일), 월 신호 후 13/35, 연 직접 34/35. Flash 공지는 시행 1,255일 전.
- 015 엄격 혼동(TP/FN/FP): 404·410 0/3/2, archived 0/5/10, 외부 리다이렉트 1/2/7, 저장소 이동 2/3/1, 커밋 365일 2/3/19, 릴리스 365일 0/2/19, npm deprecated 0/1/2.
- 015: 당시 성립 83개 중 이후 붕괴 5(6.0%), 정확 날짜 2/77. 월·분기·연 확인 중앙 지연 12.5·58·242일(2사건).

**판·파일·층** *(b: 작업자 실행 영수증, 나는 재실행하지 않음)*
- 028 [28h]: 024의 유지 셀 무작위 32개 실행 32/32 성립. 143 [143r]: 5,370셀쌍 불변, 유일 실패는 7.8.6 dist 누락이고 문서절 신호 C가 756응답 오이월. 135 [135h]: C는 실제 변화 1쌍 놓침, 해시 D는 26쌍 중 25 요청.
- 147 [147r]: URL 마지막 값 이월은 96건 중 40건 오승인. 관측 레코드(B)로 현재 답 정확, 과거 답 112건은 전달 기록(C)만 재생. TTL 음성 캐시는 회복 1틱 지연.
- 266 [266r]: 83/83 파일 조인. 1.14.1은 분류자에 3.13이 없어도 cp313 wheel 실행 통과, 1.14.0은 requires-python 통과에도 파일 0. 한 파일은 발표 14,234초 뒤 게시.
- 216·229 [216h][229m]: 철회 배너=파일 플래그 26/26. `==8.1.0`은 철회 파일+경고, `<8.1.1` 범위는 8.0.2.
- 253 [253r]: axe 4.8.0에서 중복 ID 규칙이 기본 모드에서 빠지고 분류가 violations→incomplete.

**문서 판독** *(a)*
- 261 [261f]: docs.rs는 `--all-features`+unstable cfg 빌드. 9셀 게이트 3 제외·6 포함, 컴파일·실행 0/9. 235 [235h]: 정오표 뒤에도 옛 감사 인용 보존. 162 [162h]: 공지일≠계정별 가용(같은 계정 최초 활성 쌍 0). 059 [59h]: 중간판에서만 변화.

**정정**
- 브리프의 "15건을 더 많이"는 15건 중 1건 차이이고, 그 1건도 창 설정의 산물이다.
- O의 350/364는 보관 목록 전체를 같은 비용으로 연다는 가정의 값이고 기본값은 309/364다[r40].

**열린 것**
- 사람 판독시간, 실제 304 비율, 짧은 장애의 직접 포착, 실제 수요 분포(152의 수요열은 시드 합성)
- 공급원 3곳·신규 15건이라 정책 순위의 통계적 근거가 없다.

## 2. 근거 수준
- (a) 문서 판독: 015·019·059·162·235, 261(소스 판독)
- (b) 고정 입력 실행: 152·024는 내가 Python 3.13.18로 오프라인 재생해 출력 바이트가 같았다. 028·135·143·147·216·229·253·266은 작업자 영수증만 있다.
- (c) 사용자 미확인: 실제 요청 빈도·판독 노동·갱신이 바꾼 결정(hot/tail은 합성 요청열).

## 3. 설계 함의

**일의 배분**
1. 보유할 자산은 본문 사본이 아니라 공급원별 변경 채널 주소(릴리스 노트·changelog·정오표·철회·상태 API).
2. 희소 발견은 배경의 채널 ID 집합 차분으로 보장한다(표시일 창 금지). 통지 1회 12,288B·6초 대 원문 32,768B·30초(설정값). O만 쓰면 0/3, 전용 슬롯은 근거 없음.
3. 신선도는 변경 항목이 나타난 판의 영향 층만 재판정하고, 놓침은 무작위 감사 표본으로 잰다(028 방식).
4. 요청 때는 필요한 정확한 층만 확인한다. 항목당 수요가 하루 0.014~0.026 미만이면 배경 유지에서 뺀다(152 모형, 가정).
5. 주기 확인이 이기는 조건: 예산이 빠듯하고(024 상한 10~20) 이름 유지·계약 변경 사건이면 D, 정기 발행·주류 수요·넉넉한 예산이면 P가 빠르다(152).

**갱신 신호**
- 촉발: 해당 판의 변경 항목, 파일 단위 철회 플래그, 정오표·정정 DOI 관계, 공지된 종료 기한, 요청 시점의 원문 실패.
- 확인 큐에만 넣음: 저장소 이동, 외부 리다이렉트, 파일·해시 변화(정밀도 9.4%).
- 갱신 근거로 쓰지 않음: archived, 404만 단독, 커밋·릴리스 나이, 분류자, requires-python 통과, docs 표시, 목록 누락, HTTP 200.

**예산 축소**
- 늦출 것: 안정 인기 자료의 재독(159/159 일치, 112회 낭비), 원문 순환.
- 지킬 것: 채널 차분, 요청 시 확인.
- 손실 감지: 채널별 마지막 커서와 결번(152 recovery), 마지막 관측 나이 분포, 신호 큐 적체, 감사 표본의 숨은 무효율, 답의 보류·미확인 비율.

**사건별 처리**
- 이름: 별칭 기록, 옛 인용 유지. 같은 규칙 ID라도 도구판이 다르면 다른 의미(253).
- 주소: 리다이렉트·아카이브는 주소 별칭. 목록 누락은 삭제가 아니다(152 IETF).
- 판: 새 판은 새 레코드. 이월은 진입 로드·함수 지문이 같을 때만(143). 중간판(059)·늦은 파일(266) 주의. 철회는 파일 단위+사용자 핀 형태(229).
- 내용: 같은 URL 변경은 새 관측(Pocket은 200인데 기능 종료). 옛 답은 당시 관측으로 읽는다.
- 가용성: 폴링 포착 0/2라 저장 상태로 두지 않고 요청 때 재시도. 음성 캐시는 정확한 부재·진입 실패만(147). 단계 출시는 조건문(162).

**배포 파일·선언·문서가 다를 때**
안내 키는 목적이 실제로 소비하는 가장 좁은 산출물: 설치는 filename+sha256+태그(266), API는 export 게이트+소비자 feature 그래프(261), 점검 도구는 도구판×모드×규칙 결과(253), 철회는 파일 플래그+핀 형태(216·229). 분류자·지원 문구·docs 표시는 보조 단서.

## 4. 판단을 뒤집거나 단순화하는 근거
- **상시 크롤러는 필요 없다.** 015 붕괴 6%, 028 32/32, 143 5,370/5,370, 152 안정 159/159, 019 연 1회 직접 34/35, 024는 주소를 알면 8요청.
- **152의 신규 발견 S>P는 표시일 창 하나로 설명된다.** ID 차분을 쓰면 P와 S가 같아진다(archive-catalog). 남는 선택은 지연(P가 빠름)과 바이트(S가 1/3) 사이다.
- **기존 설계의 재검토 범위가 너무 넓다.** STORAGE.md는 새 판을 수록하면 읽은 모든 활성 주장을 재검토한다 [st]. 이는 해시 신호와 같아서 대부분 TN을 만든다(024 정밀도 9.4%, 143 D 불필요 경보 13). 261식 층별 술어로 좁히되, 진입 로드 검사 1회는 남긴다. 143의 C처럼 문서 신호만 보면 패키징 실패를 놓친다.

## 5. 다른 담당에 주는 사실
- **DB**: 관측 키는 원 URL·공급자 판·논리 키·위치·observed_at·실패 종류로 잡고, 전달 기록은 따로 둔다(147). 신규 판정은 first_seen 기준 ID로, 철회는 filename+sha256으로 한다.
- **요청**: 핀 형태(정확/범위), 인터프리터·ABI·OS, 직접 feature에 따라 안내가 갈린다(229·266·261).
- **수집**: 표시일과 편입 시각이 다르다(Wrangler 5개월, Microfrontends 29일).
- **검색**: 분류자나 docs 표시로 후보를 제외하지 않는다.
- **평가**: 차이는 1/15이고 복구는 0/2라 정책 순위를 주장할 수 없다. 감사 표본을 운영 지표로 쓴다.

[152m]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/metrics.csv
[152s]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/sensitivity.csv
[152p]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/replay.py
[24r]: https://github.com/laadkke-arch/agentflow-open/blob/4af1300841c1c39f9ef6e76d78579034d1ae0c51/docs/workstreams/research/AF-RES-024/RESULT.md
[19r]: https://github.com/laadkke-arch/agentflow-open/blob/034ba6e2360301be23c49c66cf42af5c36f9e534/docs/workstreams/research/AF-RES-019/RESULT.md
[15c]: https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/results/confusion.json
[28h]: https://github.com/laadkke-arch/agentflow-open/blob/72a5d7f4fb4489fd183669dea49dc9659d941ca8/docs/workstreams/research/AF-RES-028/HANDOFF.md
[143r]: https://github.com/laadkke-arch/agentflow-open/blob/61823fd1c98b52d44833bdada4c89708133b528a/docs/workstreams/research/AF-RES-143/RESULT.md
[135h]: https://github.com/laadkke-arch/agentflow-open/blob/880833d80f8547e91e42f1d2269c7d4d4a31c0a7/docs/workstreams/research/AF-RES-135/HANDOFF.md
[147r]: https://github.com/laadkke-arch/agentflow-open/blob/30afd115c302f468d5007e380f72228c45130c37/docs/workstreams/research/AF-RES-147/RESULT.md
[266r]: https://github.com/laadkke-arch/agentflow-open/blob/6c4daa3d77251b9434355cf54258d9494e41f2fc/docs/workstreams/research/AF-RES-266/RESULT.md
[216h]: https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/HANDOFF.md
[229m]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/matrix.csv
[253r]: https://github.com/laadkke-arch/agentflow-open/blob/520ba50d86e4aad2e67b207cff5dcb1f5d5e3edd/docs/workstreams/research/AF-RES-253/rules.csv
[261f]: https://github.com/laadkke-arch/agentflow-open/blob/8f23ff6eacd930906fca8a1a46925f607c8c08f0/docs/workstreams/research/AF-RES-261/refresh.md
[235h]: https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/HANDOFF.md
[162h]: https://github.com/laadkke-arch/agentflow-open/blob/de55ea13566bc88f497dec2bfa4b0752406aea06/docs/workstreams/research/AF-RES-162/HANDOFF.md
[59h]: https://github.com/laadkke-arch/agentflow-open/blob/e91b8abe3eee98d469ae80d7ca152ff08047c8d9/docs/workstreams/research/AF-RES-059/HANDOFF.md
[r40]: https://github.com/laadkke-arch/agentflow-open/blob/c8f4b5f106bf35994ad033846c221beae60c5012/docs/workstreams/planning/REVIEW-40.md
[st]: https://github.com/laadkke-arch/agentflow-open/blob/fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c/docs/workstreams/design/gallim/db/STORAGE.md
