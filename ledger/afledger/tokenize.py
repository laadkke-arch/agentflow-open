"""서랍 토큰화(07 R-5 결정: 다국어 토큰화, 규칙 판 t2). 모델 호출 없이 결정적이다.

t1  설계 예제. 영어 토큰([0-9a-z])만 본다. 한국어는 서랍에 보이지 않는다(08 I11·I12).
t2  t1 + 한국어 두 층.
    - 어절 층(word): 한글 어절에서 끝의 조사·어미를 하나 떼어 낸 줄기(두 음절 이상). 기능 어절('수', '있다', '통해' …)과
      불용 줄기는 내용어에서 뺀다(B1의 실패: 조사·기능 어절이 내용어로 세어지는 것을 막는다).
    - 형태소 수준 층(gram): 줄기의 음절 2-gram. 형태 분석기 없이 합성어·활용형이 같은 형태소를 공유하는지 본다
      ('기다려야'와 '기다린다'는 '기다', '대기열'과 '대기'는 '대기'로 만난다). 두 음절 줄기는 그 자체가 gram이다.
    맞음 단위는 질의 줄기 하나다. 줄기가 같으면 word로, 줄기의 gram 하나라도 꼬리표의 gram과 같으면 gram으로 맞는다.
    한 줄기의 gram이 여럿 맞아도 서로 다른 내용어 하나로 센다(서랍 자격 "서로 다른 내용어 둘"을 부풀리지 않게).
영어 번역 접수는 비교용 선택지로만 남긴다(config.INTAKE_TRANSLATE, 08 I16).
"""
from __future__ import annotations

import re

from . import config

RULES = config.TOKEN_RULES

# 끝에서 하나만 떼는 조사·어미. 긴 것부터 본다(닫힌 목록, 형태 분석이 아니다).
KO_ENDINGS = sorted(set("""
은 는 이 가 을 를 의 에 에서 에게 에게서 한테 께 으로 로 으로써 로써 으로서 로서 와 과 도 만 까지 부터 보다 처럼 마다
이나 나 이며 며 이고 고 이다 다 이라 라 이란 란 이면 면 인 한 할 함 해 해야 하여 하고 하며 하면 하는 하지 했다 한다
된 될 됨 되어 되고 되며 되면 되는 된다 됐다 시킨다 시키는 지 게 도록 으면 려면 려고 어야 아야 어서 아서 어 아 기 기에
이라는 라는 이라고 라고 에도 에는 에서는 으로는 로는 과의 와의 에의 들 들을 들이 들의 들은 했고 하게 되게 하도록
""".split()), key=len, reverse=True)
KO_ENDINGS_SET = frozenset(KO_ENDINGS)
KO_STOP = frozenset("것 수 등 및 또는 그리고 그러나 하지만 때문 위해 대한 대해 통해 따라 경우 이후 이전 다른 같은 모든 각 더 덜 "
                    "안 밖 위 아래 사이 때 중 뒤 앞 거나 하지 않 이미 계속 단순 각각 바로 다시 아직 먼저 함께 따로".split())
KO_FUNC_EOJEOL = re.compile(r"^(수|것|등|및|또는|그리고|위해|위한|대한|대해|통해|따라|같은|다른|모든|각|더|때|경우|"
                            r"한다|했다|된다|됐다|있다|없다|있는|없는|하는|되는|하고|되고|하며|되며|할|될|한|된|해야|하면|되면|"
                            r"이다|있고|없고|있으며|않는다|않고|않는|않게|수를|수가|것을|것이|것은|때는|때에|경우에|안|중|"
                            r"있도록|없도록|하도록|되도록|아니다|아닌|않아야|있어야|해서|하여|합니다|입니다|있습니다)$")


def ko_stem(word: str) -> str:
    for e in KO_ENDINGS:
        if word.endswith(e) and len(word) - len(e) >= 2:
            return word[: -len(e)]
    return word


def grams(stem: str) -> list[str]:
    return [stem] if len(stem) == 2 else [stem[i:i + 2] for i in range(len(stem) - 1)]


def ko_units(text: str, *, include_function=False) -> list[dict]:
    """한글 어절마다 {'word': 줄기, 'grams': [...], 'func': bool}. 기능 어절은 include_function일 때만 넣는다."""
    out, seen = [], set()
    for w in re.findall(r"[가-힣]+", text):
        # 따옴표·괄호 뒤에 떨어진 조사만의 덩어리('…'에서)도 기능 어절이다
        func = bool(KO_FUNC_EOJEOL.match(w)) or w in KO_ENDINGS_SET
        s = w if func else ko_stem(w)
        if not func and (len(s) < 2 or s in KO_STOP):
            func, s = True, w
        if func and not include_function:
            continue
        if s in seen:
            continue
        seen.add(s)
        out.append({"word": s, "grams": [] if func else grams(s), "func": func})
    return out


def index_text(text: str) -> tuple[str, str]:
    """꼬리표 색인용 (words, grams) 공백 구분 문자열. 기능 어절은 words에 넣어 감사 검색에서만 맞게 한다."""
    us = ko_units(text, include_function=True)
    words = " ".join(u["word"] for u in us)
    gs = " ".join(dict.fromkeys(g for u in us for g in u["grams"]))
    return words, gs


def match_units(query_units: list[dict], tag_words: set[str], tag_grams: set[str]) -> list[tuple[str, bool]]:
    """질의 줄기 가운데 꼬리표와 맞은 것. 돌려주는 값: [(표시 문자열, 기능어인가)]."""
    out = []
    for u in query_units:
        if u["word"] in tag_words:
            out.append((u["word"], u["func"]))
            continue
        hit = next((g for g in u["grams"] if g in tag_grams), None)
        if hit:
            out.append((f"{u['word']}~{hit}", False))
    return out
