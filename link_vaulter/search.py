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


def get_created_at(link):
    return link.get("created_at", "")
    
def favorites_first(links: list[dict]) -> list[dict]:
    """Issue 14: favorites first, newest first within both groups"""
    favorites = []
    regular_links = []

    # Separate the links into two groups.
    for link in links:
        if link.get("favorite", False):
            favorites.append(link)
        else:
            regular_links.append(link)

    # Sort each group from newest to oldest.
    favorites = sorted(favorites, key=get_created_at, reverse=True)
    regular_links = sorted(regular_links, key=get_created_at, reverse=True)

    # Put the favorites before the regular links.
    return favorites + regular_links


def paginate(links: list[dict], page: int, per_page: int) -> list[dict]:
    """Issue 15: use one-based pages and reject invalid page sizes"""
    start = page * per_page
    return links[start : start + per_page]

