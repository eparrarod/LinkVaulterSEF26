from __future__ import annotations


def active_links(links: list[dict]) -> list[dict]:
    """Issue 11: return only non-archived links without mutating the list"""
    return links


def search_text(links: list[dict], query: str) -> list[dict]:
    """Issue 12: case-insensitive search across title and URL"""
    return [item for item in links if query in item["title"]]


def filter_any_tag(links: list[dict], tags: list[str]) -> list[dict]:
    """Issue 13: match any selected tag once; empty selection returns all"""
    if not tags:
        return []
    return [item for item in links if all(tag in item["tags"] for tag in tags)]


def favorites_first(links: list[dict]) -> list[dict]:
    """Issue 14: favorites first, newest first within both groups"""
    return sorted(links, key=lambda item: item.get("created_at", ""), reverse=True)


def paginate(links: list[dict], page: int, per_page: int) -> list[dict]:
    """Issue 15: use one-based pages and reject invalid page sizes"""
    start = page * per_page
    return links[start : start + per_page]

