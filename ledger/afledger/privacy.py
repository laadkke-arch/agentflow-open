"""공개 꼬리표 사생활 검사(04 2.1 규칙 3, 07 R-4).

p1  설계 예제 그대로. 영어 토큰([0-9a-z])만 본다. 어느 요청 원문에만 있고 원문 쪽(인용·진술)에는 없는
    다섯 글자 이상 내용어가 둘 이상이면 거절한다. 한국어 사본은 통과한다(07 M2b).
p2  p1 + 한국어. 한글 어절에서 끝의 조사·어미를 하나 떼어 낸 줄기(두 음절 이상)를 내용어로 본다.
    요청에만 있는 한국어 줄기가 KO_MIN_COUNT개 이상이거나, 영어·한국어 합이 셋 이상이거나,
    요청 문장과 공백을 접어 VERBATIM_CHARS 글자 이상(그 절반 이상이 한글) 그대로 겹치면 거절한다.
거절 문장에는 낱말·프로젝트 이름을 넣지 않는다(07 M2b, 시험 test_privacy_error_does_not_echo_the_private_words).
값은 ledger/out/measure_r4.json의 측정으로 골랐다(08 I8).
"""
from __future__ import annotations

import re

from . import config

FUNCTION_WORDS = frozenset("""
a an the and or but nor if then else so than too very just also as about above after again
against all any both each few more most other some such only own same up down out off once
until while during before between through because per via vs of in on at to for from by with
without into onto over under within upon is are was were be been being am do does did done
can could may might must shall should will would it its this that these those there here
which who whom whose what when where why how not no yes we you they he she i me my our your
their them us his her one ones lets let get gets got has have had having make makes made
""".split())

# 끝에서 하나만 떼는 조사·어미. 긴 것부터 본다. 형태 분석이 아니라 닫힌 목록이다(07 R-5에서 다시 본다).
KO_ENDINGS = sorted(set("""
은 는 이 가 을 를 의 에 에서 에게 에게서 한테 께 으로 로 으로써 로써 으로서 로서 와 과 도 만 까지 부터 보다 처럼 마다
이나 나 이며 며 이고 고 이다 다 이라 라 이란 란 이면 면 인 한 할 함 해 해야 하여 하고 하며 하면 하는 하지 했다 한다
된 될 됨 되어 되고 되며 되면 되는 된다 됐다 시킨다 시키는 지 게 도록 으면 려면 려고 어야 아야 어서 아서 어 아 기 기에
이라는 라는 이라고 라고 에도 에는 에서는 으로는 로는 과의 와의 에의 들 들을 들이 들의 들은
""".split()), key=len, reverse=True)
KO_STOP = frozenset("것 수 등 및 또는 그리고 그러나 하지만 때문 위해 대한 대해 경우 이후 이전 다른 같은 모든 각 더 덜 안 밖 위 아래 사이".split())

KO_MIN_LEN = 2
KO_MIN_COUNT = 3
VERBATIM_CHARS = 16


def ascii_tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^0-9a-z]+", text.lower()) if len(t) >= 2]


def ascii_content(text: str) -> list[str]:
    out = []
    for t in ascii_tokens(text):
        if t in FUNCTION_WORDS or t.isdigit() or t in out:
            continue
        out.append(t)
    return out


def ko_stem(word: str) -> str:
    for e in KO_ENDINGS:
        if word.endswith(e) and len(word) - len(e) >= KO_MIN_LEN:
            return word[: -len(e)]
    return word


def ko_content(text: str) -> list[str]:
    out = []
    for w in re.findall(r"[가-힣]+", text):
        s = ko_stem(w)
        if len(s) >= KO_MIN_LEN and s not in KO_STOP and s not in out:
            out.append(s)
    return out


def _fold(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _verbatim(tag: str, request: str, source_side: str, n: int) -> bool:
    """요청 문장에서 n글자 창을 밀어 꼬리표에 그대로 있고 원문 쪽에는 없는 것이 있으면 True."""
    t, r, s = _fold(tag), _fold(request), _fold(source_side)
    if len(t) < n:
        return False
    for i in range(0, max(0, len(r) - n + 1)):
        w = r[i:i + n]
        # 영어 사본은 토큰 규칙이 잡는다. 겹침 규칙은 한글이 든 창만 본다(영어 관용구 'the producer wai'가 걸린다, 08 I8)
        if len(re.findall(r"[가-힣]", w)) >= n // 2 and w in t and w not in s:
            return True
    return False


def leak(tag: str, source_side: str, request: str, rules: str | None = None) -> int:
    """꼬리표가 요청 원문을 옮겨 적었다고 볼 근거 수. 0이면 통과."""
    rules = rules or config.PRIVACY_RULES
    src_a = set(ascii_content(source_side))
    private_a = set(ascii_content(request)) - src_a
    leaked_a = [t for t in ascii_content(tag) if t in private_a and len(t) >= 5]
    if rules == "p1":
        return len(leaked_a) if len(leaked_a) >= 2 else 0
    src_k = set(ko_content(source_side))
    private_k = set(ko_content(request)) - src_k
    leaked_k = [t for t in ko_content(tag) if t in private_k]
    n = len(leaked_a) + len(leaked_k)
    if len(leaked_a) >= 2 or len(leaked_k) >= KO_MIN_COUNT or n >= 3:
        return n
    if _verbatim(tag, request, source_side, VERBATIM_CHARS):
        return max(n, 1)
    return 0


def check(tag: str, source_side: str, requests, rules: str | None = None) -> None:
    from .ledger import PrivacyError
    for r in requests:
        n = leak(tag, source_side, r, rules)
        if n:
            raise PrivacyError(f"tag repeats {n} words that appear only in a private request")
