from __future__ import annotations
from urllib.parse import urlsplit

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
    tags = [tag for item in links for tag in item.get("tags", [])]
    return Counter(tags).most_common(1)[0][0]


def total_visits(links: list[dict]) -> int:
    """Issue 29: sum nonnegative visit counts while tolerating missing values."""
    return sum(item["visits"] for item in links)


# input: A list of links
# output: A integer representing the number of unique hostnames
# Method splits each link passed as a parameter and extracts the hostname and
# scheme. The method validates the formatting of the link using scheme and adds the
# hostname to a set if the scheme is valid.
def unique_domains(links: list[dict]) -> int:
    """Issue 30: count unique hostnames case-insensitively, ignoring www."""
    hostname_set = set()
    for item in links:
        u = urlsplit(item["url"])
        hostname = u.hostname
        link_scheme = u.scheme
        if hostname is not None:
            if link_scheme == "http" or link_scheme == "https" and "." in hostname:
                while 'www.' in hostname:
                    hostname = hostname.split('www.', 1)[1]
                hostname_set.add(hostname)
    return len(hostname_set)

