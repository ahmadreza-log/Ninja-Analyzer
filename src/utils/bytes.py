"""
Byte-size formatting helpers.
"""


def format_bytes(size_in_bytes: int) -> str:
    if size_in_bytes is None:
        return "-"
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    return f"{size_in_bytes / (1024 * 1024):.1f} MB"


