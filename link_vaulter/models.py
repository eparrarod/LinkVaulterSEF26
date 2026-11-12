from __future__ import annotations

from datetime import datetime, timezone


def normalize_url(url: str) -> str:
    """Issue 01: normalize scheme/host case and one trailing slash"""
    return url.lower().rstrip("/")


def normalize_title(title: str) -> str:
    """Issue 02: trim surrounding whitespace without altering internal spacing"""
    return title


def normalize_tags(tags: list[str]) -> list[str]:
    """
    Cleans up a list of tags by removing extra spaces, converting them
    to lowercase, and removing blanks and duplicates.

    Args:
        tags: A list of tag strings to normalize.

    Returns:
        A list of cleaned, unique tags in their original order.
    """
    normalized = []

    for tag in tags:
        tag = tag.strip().lower()

        if tag and tag not in normalized:
            normalized.append(tag)

    return normalized


def next_link_id(links: list[dict]) -> int:
    """Issue 04: return one greater than the largest existing integer id"""
    return len(links) + 1


def restore_link(link: dict) -> dict:
    """Issue 05: return a restored copy without mutating the input"""
    link["archived"] = False
    return link


def new_link(link_id: int, title: str, url: str, tags: list[str]) -> dict:
    return {
        "id": link_id,
        "title": title,
        "url": url,
        "tags": tags,
        "favorite": False,
        "archived": False,
        "visits": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

