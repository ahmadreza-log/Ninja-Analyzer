"""
Datetime helpers.
"""

from datetime import datetime


def now_formatted(fmt: str = "%Y/%m/%d %H:%M:%S") -> str:
    return datetime.now().strftime(fmt)


