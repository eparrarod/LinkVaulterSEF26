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
    #   Sorted(): Return a new list containing all items from the iterable in descending order.
    #   Key: A function that serves as a key for the sort comparison. In this case, it's a lambda function that takes an item (a dictionary representing a link)
    #   and returns a tuple containing two values
    #   item.get("favorite", False): This retrieves the value associated with the "favorite"
    #   check if the link is marked as a favorite. If the "favorite" key is not present in the dictionary, it defaults to False.
    #   item.get("created_at", ""): This retrieves the value associated with the "created_at key"
    #   reverse=True: This argument specifies that the sorting should be done in descending order
    #   All together, this line sorts the links first by whether they are marked as favorites (True comes before False) and then by their creation date (newest first) within each group.
    #   The result is a new list of links sorted according to these criteria.
    return sorted(links, key=lambda item:(item.get("favorite", False), item.get("created_at", "")), reverse=True)

def paginate(links: list[dict], page: int, per_page: int) -> list[dict]:
    """Issue 15: use one-based pages and reject invalid page sizes"""
    start = page * per_page
    return links[start : start + per_page]

