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
    tags = [tag for item in links for tag in item.get("tags", [])]
    return Counter(tags).most_common(1)[0][0]


def total_visits(links: list[dict]) -> int:
    """Issue 29: sum nonnegative visit counts while tolerating missing values."""
    return sum(item["visits"] for item in links)


def unique_domains(links: list[dict]) -> int:
    """Issue 30: count unique hostnames case-insensitively, ignoring www."""
    
    #  set() creates a new empty set object, which is a collection of unique elements.
    #  In this case, it will be used to store unique hostnames extracted from the URLs in the links list.
    hostnames = set()
    
    #  The for loop iterates over each item in the links list. For each item, it extracts the URL and processes it to obtain the hostname.
    for item in links:
        #   url variable is equal to the item's url key dictionary item 
        url = item["url"]
        #   this splits the URL into seprate parts, first one splits anything before and after the // while the secomd 
        #splits the raining ones based on single /, finally, it returns the first index which is just the domain name
        hostname = url.split("//")[-1].split("/")[0]
        #   this makes the domain name into lowercase
        hostname = hostname.lower()
        #   checks if the doamin name starts with www. and then removes it if so, only keeping everything including and after the 4th index
        if hostname.startswith("www."):
            hostname = hostname[4:]
        #completes the first loop by adding the hostname to the hostnames set
        hostnames.add(hostname)
    #returns the length of the hostnames set, which represents the number of unique hostnames found in the links list.
    return len(hostnames)