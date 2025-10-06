"""
Simple HTTP client wrapper around requests with sane defaults and helpers.
"""

from typing import Dict, Optional
import time
import requests


DEFAULT_HEADERS: Dict[str, str] = {
    "Accept": "*/*",
    "Accept-Encoding": "br, gzip, deflate",
    "Connection": "keep-alive",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
}


class HttpResponse:
    def __init__(self, response: requests.Response, elapsed_ms: float) -> None:
        self.response = response
        self.elapsed_ms = elapsed_ms

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def headers(self) -> requests.structures.CaseInsensitiveDict:
        return self.response.headers

    @property
    def content(self) -> bytes:
        return self.response.content

    @property
    def text(self) -> str:
        return self.response.text


class HttpClient:
    def __init__(self, timeout: int = 10, headers: Optional[Dict[str, str]] = None) -> None:
        self.timeout = timeout
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, allow_redirects: bool = True) -> HttpResponse:
        merged_headers = {**self.headers, **(headers or {})}
        t0 = time.time()
        resp = requests.get(url, timeout=self.timeout, allow_redirects=allow_redirects, headers=merged_headers)
        t1 = time.time()
        return HttpResponse(resp, elapsed_ms=round((t1 - t0) * 1000, 2))


