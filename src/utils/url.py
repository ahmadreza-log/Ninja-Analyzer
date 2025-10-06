"""
URL utilities for normalization and validation.
"""

from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and (parsed.netloc or parsed.path))
    except Exception:
        return False


def normalize_url(url: str) -> str:
    if not url:
        return url
    url = url.strip()
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    return url


def extract_host(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or parsed.path


