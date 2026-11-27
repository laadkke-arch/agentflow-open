"""시험용 가짜 전송. 네트워크 없이 원문·검색 응답을 준다."""
import json


class FakeResponse:
    def __init__(self, url, status, body: bytes, fetched_at="2026-11-26T00:00:00Z"):
        self.url, self.status, self.body, self.fetched_at, self.headers, self.recorded = url, status, body, fetched_at, {}, "fake"

    def text(self):
        return self.body.decode("utf-8")

    def json(self):
        return json.loads(self.body)


class FakeTransport:
    def __init__(self, files: dict[str, str]):
        self.files, self.log = files, []

    def get(self, url, headers=None, note=""):
        headers = headers or {}
        self.log.append((url, dict(headers)))
        if url not in self.files:
            return FakeResponse(url, 404, b"404: Not Found")
        body = self.files[url].encode("utf-8")
        if "Range" in headers:
            a, b = headers["Range"].split("=")[1].split("-")
            return FakeResponse(url, 206, body[int(a):int(b) + 1])
        return FakeResponse(url, 200, body)
