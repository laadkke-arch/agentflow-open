"""Apply the frozen bilingual terminology only as supplemental lexical tokens."""
import csv
from pathlib import Path
import re
import unicodedata

HERE = Path(__file__).resolve().parent


def normalized(text):
    return unicodedata.normalize("NFKC", text).casefold()


def alternatives(value):
    return "|".join(sorted((re.escape(normalized(term)) for term in value.split(";") if term),
                           key=len, reverse=True))


def load_terms():
    with (HERE / "concepts.tsv").open(encoding="utf-8") as source:
        return [
            (row["concept"], re.compile(r"(?<![a-z0-9])(?:" + alternatives(row["english"])
                                       + r")(?![a-z0-9])"),
             tuple(normalized(term).replace(" ", "") for term in row["korean"].split(";")))
            for row in csv.DictReader(source, delimiter="\t")
        ]


TERMS = load_terms()


def augment(text):
    folded = normalized(text)
    compact = folded.replace(" ", "")
    matches = [f"afconcept{concept}" for concept, english, korean in TERMS
               if english.search(folded) or any(term in compact for term in korean)]
    return " ".join([text, *matches])
