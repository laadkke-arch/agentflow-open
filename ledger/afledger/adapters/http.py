"""HTTP 기록·재생.

mode="live"   네트워크로 받는다(기록하지 않음).
mode="record" 네트워크로 받고 응답을 fixtures에 질의·시각과 함께 쓴다.
mode="replay" fixtures에서만 읽는다. 없으면 ReplayMiss. 시험은 이 모드로 돈다(네트워크 없음).

인증 머리(Authorization)는 기록하지 않는다. 기록 키는 (방법, 주소, Range·Accept·If-None-Match 머리)의 sha256이다.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

KEY_HEADERS = ("Range", "Accept", "If-None-Match")


class ReplayMiss(LookupError):
    pass


class Response:
    def __init__(self, url, status, headers, body: bytes, fetched_at, recorded=None):
        self.url, self.status, self.headers, self.body, self.fetched_at = url, status, headers, body, fetched_at
        self.recorded = recorded   # 재생이면 기록 파일 경로

    def text(self) -> str:
        return self.body.decode("utf-8")

    def json(self):
        return json.loads(self.body.decode("utf-8"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Transport:
    def __init__(self, mode: str = "replay", fixtures: str | Path | None = None, *, token_env=("GITHUB_TOKEN", "GH_TOKEN"),
                 timeout: float = 30.0):
        assert mode in ("live", "record", "replay")
        self.mode = mode
        self.dir = Path(fixtures) if fixtures else None
        self.token_env = token_env
        self.timeout = timeout
        self.log: list[dict] = []   # 이번 실행에서 보낸 요청(주소, 상태, 바이트, 재생 여부)

    @staticmethod
    def key(method: str, url: str, headers: dict) -> str:
        h = "|".join(f"{k}={headers.get(k, '')}" for k in KEY_HEADERS)
        return hashlib.sha256(f"{method} {url} {h}".encode("utf-8")).hexdigest()[:24]

    def _path(self, k: str) -> Path:
        return self.dir / f"{k}.json"

    def get(self, url: str, headers: dict | None = None, *, note: str = "") -> Response:
        headers = dict(headers or {})
        k = self.key("GET", url, headers)
        if self.mode == "replay":
            if not self.dir or not self._path(k).exists():
                raise ReplayMiss(f"no recorded response for GET {url} {headers}")
            d = json.loads(self._path(k).read_text(encoding="utf-8"))
            body = base64.b64decode(d["body_b64"]) if "body_b64" in d else d["body"].encode("utf-8")
            r = Response(url, d["status"], d["headers"], body, d["fetched_at"], recorded=str(self._path(k)))
        else:
            r = self._live(url, headers)
            if self.mode == "record" and self.dir:
                self.dir.mkdir(parents=True, exist_ok=True)
                d = {"method": "GET", "url": url, "request_headers": headers, "note": note,
                     "fetched_at": r.fetched_at, "status": r.status, "headers": r.headers}
                try:
                    d["body"] = r.body.decode("utf-8")
                except UnicodeDecodeError:
                    d["body_b64"] = base64.b64encode(r.body).decode("ascii")
                self._path(k).write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                         encoding="utf-8")
        self.log.append({"url": url, "status": r.status, "bytes": len(r.body), "replayed": r.recorded is not None,
                         "fetched_at": r.fetched_at})
        return r

    def _live(self, url: str, headers: dict) -> Response:
        send = dict(headers)
        send.setdefault("User-Agent", "afledger-unit1")
        if url.startswith("https://api.github.com/"):
            tok = next((os.environ[e] for e in self.token_env if os.environ.get(e)), None)
            if tok:
                send["Authorization"] = f"Bearer {tok}"
        req = urllib.request.Request(url, headers=send)
        at = now_utc()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body, status, hdr = resp.read(), resp.status, resp.headers
        except urllib.error.HTTPError as e:
            body, status, hdr = e.read(), e.code, e.headers
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return Response(url, 0, {"error": f"{type(e).__name__}: {e}"}, b"", at)
        keep = {k.lower(): v for k, v in hdr.items()
                if k.lower() in ("etag", "content-range", "content-type", "content-length", "last-modified",
                                 "x-ratelimit-remaining")}
        return Response(url, status, keep, body, at)
