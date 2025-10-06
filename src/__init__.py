"""
Ninja Analyzer - Core package initializer.
Provides shared utilities exposed for convenient imports.
"""

from .utils.url import normalize_url, is_valid_url
from .utils.bytes import format_bytes
from .utils.datetime import now_formatted

__all__ = [
    "normalize_url",
    "is_valid_url",
    "format_bytes",
    "now_formatted",
]
"""
Ninja Analyzer - Website Analysis Tool
Source package initialization file.
"""
