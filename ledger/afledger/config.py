"""설정 상수는 이 파일 한 곳에 둔다. 값을 바꾸면 해당 규칙 판(*_RULES)을 올리고 08-implementation.md에 적는다.

설계 근거: 07-review.md 6절 D1·D2·D4·D8·D11, 04-architecture.md 5절.
"""

# ---- 규칙 판(결과 행에 남겨 나중 규칙으로 다시 계산할 수 있게 한다)
RULE_VERSION = "unit1-r4"          # answer_run.rule_version. 설계 예제는 "final-v1+review"
NORM_RULES = "n1"                  # 주소 정규화(R-1 임시안). afledger/normalize.py가 실제 값을 정한다
MAP_RULES = "m1"                   # 판 사이 위치 대응(R-1 임시안). afledger/locate.py
BUDGET_RULES = "b2"                # 예산 셈법. b1 = D1·D11 그대로, b2 = b1 + 기한 읽기(D4)를 후속 몫과 따로 셈(08 I23). afledger/budget.py
PRIVACY_RULES = "p2"               # 꼬리표 사생활 검사. p1 = 설계 예제(영어 토큰), p2 = p1 + 한국어(privacy.py, 08 I8)
SEARCH_RULES = "s1"                # 새 검색 직접 갈래의 질의 규칙. afledger/adapters/search_github.py
INTAKE_RULES = "i2"                # 접수가 쓰는 칸별 필요 문장. afledger/intake.py
RANK_RULES = "r2"                  # 서랍 순위(R-6). r0 = 설계(bm25 합), r1 = 단위별 IDF 합, r2 = r1 + 꼬리표 길이 정규화(08 I18), r3 = 언어 칸별 정규화(I26, 채택 안 함), r4 = (칸, 언어) 검색기의 RRF(I28, 채택 안 함), r5 = r4 + 검색기 안 r2 길이 보정(I31), r6 = 꼬리표 한 줄당 최대 점수(I33)
ELIG_RULES = "e1"                  # 서랍 자격. e1 = 설계(내용어가 맞은 칸 2 이상, 서로 다른 내용어 2), e2 = 자격 칸 수를 min(2, 요청 칸 수)로. e2는 상위 10 잡음이 늘어 되돌림(08 I24)
RRF_K = 60                         # r4의 RRF 상수(Elastic rank_constant 기본값, 08 I28)
RANK_LENGTH_B = 0.75               # r2의 길이 정규화 세기(BM25 b와 같은 뜻)
DRAWER_SYMBOL_SCOPE = "eligible"   # 서랍 후보를 사용자 판 소스로 확인할 범위. "top_k"(서랍 상위 12만) | "eligible"(적격 전부, 예산 안에서 순위순). 마지막 수단(08 I18)
TOKEN_RULES = "t2"                 # 서랍 토큰화(R-5 결정: 다국어). t1 = 설계 예제(영어만). afledger/tokenize.py
INTAKE_TRANSLATE = None            # 영어 번역 접수는 비교용 선택지로만 남긴다(구현하지 않음, 08 I16). None = 원문 그대로

# ---- 예산(07 D1·D11, 06 C1)
REQUEST_FETCHES = 4                # 요청판 하나의 가져오기 수
REQUEST_BYTES = 1 << 20            # 요청판 하나가 받는 원문 바이트(1 MiB)
REQUEST_EXTERNAL_ATTEMPTS = 10     # 요청판 하나의 외부 시도(검색 호출 + 가져오기)
FOLLOW_FETCHES_PER_10_SOURCES = 3  # 후속 시계, 168시간당 감시 출처 10개마다
DEADLINE_BUDGET = "separate"       # 기한 읽기(D4)를 어느 몫으로 세나. "separate"(기한마다 3회, 후속 몫과 따로, 결정 2026-11-26) | "follow"(b1, D11 그대로). 08 I22·I23

# ---- 시계(07 D2·D4·D8)
DEADLINE_READS = (("T-24h", -24), ("T", 0), ("T+24h", 24))
ACTIVE_RULE = "shown_latest"
IMMUTABLE_KINDS = ("release", "commit", "tag", "doi")
IMMUTABLE_RECHECK_H = None
RECHECK_H = 168

# ---- 채널 ID 체계 변경 의심(06 C11)
RESET_MIN_NEW = 50
RESET_SHARE = 0.8
