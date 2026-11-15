"""Conservative GitHub repository identity; not a general URL canonicalizer.

Uses Python's URL parser. No network request or repository-existence claim.
Subpages, queries, credentials, non-GitHub hosts and encoded paths are rejected.
"""
import re
from urllib.parse import urlsplit


class RepositoryURL(ValueError):
    """An input is outside the deliberately narrow repository-root contract."""


def repository_key(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 2048:
        raise RepositoryURL("expected a nonempty repository URL of at most 2048 characters")
    # Check BEFORE urlsplit: it silently strips some controls and whitespace.
    if any(ord(c) < 33 or ord(c) == 127 for c in value) or "\\" in value:
        raise RepositoryURL("whitespace, controls and backslashes are not accepted")
    if value.startswith("git@github.com:"):
        value = "https://github.com/" + value[len("git@github.com:"):]
    try:
        parts = urlsplit(value)
        if parts.scheme not in ("https", "http", "ssh") or parts.hostname != "github.com":
            raise RepositoryURL("only GitHub repository roots are supported")
        if parts.password is not None or (parts.username is not None and not (parts.scheme == "ssh" and parts.username == "git")):
            raise RepositoryURL("credentials are not accepted")
        expected_port = {"https": 443, "http": 80, "ssh": 22}[parts.scheme]
        if parts.port not in (None, expected_port):
            raise RepositoryURL("nonstandard ports are not supported")
    except ValueError as exc:
        raise RepositoryURL(str(exc)) from exc
    if "?" in value or "#" in value or "%" in parts.path:
        raise RepositoryURL("queries, fragments and encoded paths need manual review")
    path = parts.path.removesuffix("/")
    match = re.fullmatch(r"/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)", path)
    if not match:
        raise RepositoryURL("expected exactly /owner/repository, not a subpage")
    owner, repo = match.groups()
    repo = repo.removesuffix(".git")
    if not repo or repo in (".", "..") or owner.startswith("-") or owner.endswith("-"):
        raise RepositoryURL("invalid owner or repository component")
    return f"github.com/{owner.lower()}/{repo.lower()}"
