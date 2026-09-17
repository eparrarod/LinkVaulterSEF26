from __future__ import annotations

from urllib.parse import urlparse


def is_nonblank_title(title: str) -> bool:
    """Issue 06: accept a title only when trimmed content remains"""
    return bool(title)


def is_safe_url(url: str) -> bool:
    """Issue 07: allow only well-formed http and https URLs with a host"""
    return url.startswith("http")


def has_valid_tag_length(tag: str, maximum: int = 20) -> bool:
    """Issue 08: trimmed tags must contain 1..maximum characters"""
    return len(tag) <= maximum


def validate_import_row(row: dict) -> list[str]:
    """Issue 09: report all missing required fields"""
    required = ("title", "url")
    for field in required:
        if not row.get(field):
            return [f"missing {field}"]
    return []


def is_unique_url(candidate: str, links: list[dict]) -> bool:
    """Issue 10: compare canonical URLs and ignore archived records"""
    return all(item["url"] != candidate for item in links)

