"""AF-RES-064 reader budget. Text blocks and link positions are added by the renderer."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORD_LIMIT = 500
# Count punctuation independently so minified JSON does not become one token.
TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def measure(text):
    tokens = TOKEN.findall(text)
    return {
        "words": len(tokens),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.splitlines()),
        "max_token_bytes": max((len(word.encode("utf-8")) for word in tokens), default=0),
        "sha256": sha256(text.encode("utf-8")),
    }


def budget(text, limit=WORD_LIMIT):
    for index, match in enumerate(TOKEN.finditer(text)):
        if index == limit:
            return text[:match.start()].rstrip(), True
    return text, False


def boundary_tests():
    fixtures = [(f"words_{n}", " ".join(["w"] * n), n) for n in (499, 500, 501, 611)]
    fixtures.extend([
        ("title_code_json_math", "제목\nlet x = 1;\n{\"a\":1}\n∑x² + y", 17),
        ("json_no_space", "[" + ",".join('{"key":1}' for _ in range(100)) + "]", 801),
        ("single_identifier", "한" * 8000, 1),
        ("line_ranges_and_nbsp", "line\r\n\r\nline\u00a0line", 3),
    ])
    outcomes = []
    for name, inp, size in fixtures:
        shown, cut = budget(inp)
        before = measure(inp)
        after = measure(shown)
        assert before["words"] == size, (name, before, size)
        assert after["words"] == min(size, WORD_LIMIT)
        assert cut == (size > WORD_LIMIT)
        assert inp.startswith(shown) and budget(shown) == (shown, False)
        outcomes.append({"fixture": name, "input": before, "shown": after, "truncated": cut})
    return outcomes


if __name__ == "__main__":
    print(json.dumps(boundary_tests(), indent=2, ensure_ascii=False))
