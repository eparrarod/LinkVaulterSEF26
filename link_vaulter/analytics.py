from __future__ import annotations

from collections import Counter


def count_active(links: list[dict]) -> int:
    """Issue 26: count links that are not archived."""
    return len(links)


def favorite_rate(links: list[dict]) -> float:
    """Issue 27: percentage of active links that are favorites; zero when empty."""
    favorites = sum(bool(item.get("favorite")) for item in links)
    return favorites / len(links)


def most_common_tag(links: list[dict]) -> str | None:
    """Issue 28: return the most common normalized tag; alphabetical tie-break."""
    # Clean up all tags by removing spaces, making them lowercase, and skipping empty tags
    tags = [tag.strip().lower() for item in links for tag in item.get("tags", []) if tag.strip()]

    # If there are no valid tags, return None.
    if not tags:
        return None

    counts = Counter(tags)
    # Sort by count descending, then alphabetically
    return min(counts, key=lambda tag: (-counts[tag], tag))  


def total_visits(links: list[dict]) -> int:
    """Issue 29: sum nonnegative visit counts while tolerating missing values."""
    return sum(item["visits"] for item in links)


def unique_domains(links: list[dict]) -> int:
    """Issue 30: count unique hostnames case-insensitively, ignoring www."""
    return len({item["url"].split("//")[-1].split("/")[0] for item in links})

