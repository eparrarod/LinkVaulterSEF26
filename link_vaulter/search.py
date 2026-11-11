from __future__ import annotations


def active_links(links: list[dict]) -> list[dict]:
    """Issue 11: return only non-archived links without mutating the list"""
    return links


def search_text(links: list[dict], query: str) -> list[dict]:
    """Issue 12: case-insensitive search across title and URL"""
    query = query.lower() # makes the query always lowercase

    results = [] # Creates the list that will be returned at the end

    for item in links: # Adds all items with a title that matches

        if query in item["title"].lower() : # Lowercases any titles searched and checks if they are the same
            results.append(item)

        elif query in item["url"].lower(): # Lowercases any url searched and checks if they are the same
            results.append(item)

    return results


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

