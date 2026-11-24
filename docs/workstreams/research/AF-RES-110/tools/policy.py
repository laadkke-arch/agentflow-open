"""Frozen, query-independent conflict checks for the already-retrieved B candidates."""
import re
import unicodedata

FORMATS = {
    "csv": r"\bcsv\b",
    "parquet": r"\bparquet\b|파케이",
    "json": r"\bjson\b",
    "markdown": r"\bmarkdown\b|마크다운|(?<!\w)\.md\b",
    "rst": r"\brestructuredtext\b|(?<!\w)\.rst\b",
    "jpeg": r"\bjpe?g\b",
    "png": r"\bpng\b",
    "tiff": r"\b(?:geo)?tiff?\b",
    "pdf": r"\bpdf\b",
    "envi": r"\benvi\b",
    "raw": r"\b(?:4bayer|cygm|rgbe|raw)\b|로우\s*파일",
}
PLATFORMS = {
    "windows": r"\bwindows\b|윈도우",
    "macos": r"\b(?:macos|mac os|os x)\b|맥os|맥에서",
    "linux": r"\blinux\b|리눅스",
}
INPUT = re.compile(
    r"(?:read|open|import|parse|load|input(?: file)?|from)\s+(?:an?\s+|the\s+)?|"
    r"(?:입력(?:은|으로)?|읽을\s*|불러올\s*|가져올\s*)"
)
NATIVE_VERSION = {
    "python": r"(?:\bpython\b|파이썬)\s*(?:v(?:ersion)?\s*)?(\d+\.\d+)(?:\.\d+)?(?![.\d])",
    "docutils": r"\bdocutils\b\s*(?:v(?:ersion)?\s*)?(\d+\.\d+)(?:\.\d+)?(?![.\d])",
}
CURRENT = re.compile(r"\b(?:current|latest) (?:stable|release|version)\b|(?:최신|현행)\s*(?:안정판|버전)")


def fields(query):
    """Return only explicit technical fields in this language's search text."""
    text = unicodedata.normalize("NFKC", query).casefold()
    format_hits = {name for name, pattern in FORMATS.items() if re.search(pattern, text)}
    input_format = None
    if len(format_hits) == 1:
        name = next(iter(format_hits))
        pattern = FORMATS[name]
        # Korean often puts the object before its verb.
        if re.search(r"(?:" + pattern +
                     r")\s*(?:파일)?\s*(?:을|를)?\s*(?:읽|불러|가져|파싱)", text) or any(
            re.match(r"(?:" + pattern + r")", text[match.end():])
            for match in INPUT.finditer(text)
        ):
            input_format = name
    platform = [name for name, pattern in PLATFORMS.items() if re.search(pattern, text)]
    versions = {}
    for component, pattern in NATIVE_VERSION.items():
        mentions = set(re.findall(pattern, text))
        if len(mentions) == 1:
            versions[component] = next(iter(mentions))
    return {"input_format": input_format, "platform": platform[0] if len(platform) == 1 else None,
            "versions": versions, "current_explicit": bool(CURRENT.search(text))}


def version(value):
    return tuple(int(part) for part in value.split("."))


def assess(applicability, requested):
    """Demote documented exclusions. An unverified applicability stays in B order."""
    conflicts = []
    for field in ("input_format", "platform"):
        value = requested[field]
        allowed = applicability.get(field)
        # A specificity constraint is comparable only along the exact same axis.
        if value and allowed and value not in allowed:
            conflicts.append(f"{field}:{value}")
    observed_version = False
    for key, value in requested["versions"].items():
        bounds = applicability.get("version_bounds", {}).get(key)
        if bounds is None:
            continue
        observed_version = True
        below = bounds.get("min") and version(value) < version(bounds["min"])
        above = bounds.get("max_exclusive") and version(value) >= version(bounds["max_exclusive"])
        if below or above:
            conflicts.append(f"{key}:{value}")
    if requested["current_explicit"] and applicability.get("historical_restriction"):
        observed_version = True
        conflicts.append("edition:explicit_current")
    return {
        "conflicts": sorted(conflicts),
        "edition_status": "conflict" if any(
            item.split(":")[0] in {"edition", *NATIVE_VERSION} for item in conflicts
        ) else ("compared" if observed_version else "unknown"),
    }
