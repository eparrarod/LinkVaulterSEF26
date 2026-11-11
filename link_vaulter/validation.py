from __future__ import annotations

from urllib.parse import urlparse


def is_nonblank_title(title: str) -> bool:
    """Issue 06: accept a title only when trimmed content remains"""
    testTitle = title.strip() # Removes any whitespace
    # print(testTitle)

    approvedTitle = testTitle.isalnum() # Checks if the string contains alphanumeric characters

    return approvedTitle # Returns the result of the check


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
    #   creates an empty set called hostnames to store the unique hostnames extracted from the URLs in the links list
    #   Sets automatically handle duplicates, so only unique hostnames will be stored in the set.
    hostnames = set()
    #   loops through each item in links, and for each item, checks if it is archived.
    for item in links:
        if item.get("archived"):
            continue
        url = item["url"]
        hostname = url.split("://",1)[1].split("/")[0]
        hostname = hostname.lower()
        path = url.split("://", 1)[1].partition("/")[2].rstrip("/")
        hostname = hostname + "/" + path
        hostnames.add(hostname)
    #   this splits the candidate URL into seprate parts, first one splits anything before and after the :// while the second 
    #   splits the remaining into three parts
    candidate_hostname = candidate.split("://",1)[1].split("/")[0]
    candidate_hostname = candidate_hostname.lower()

    #   this line extracts the path from the candidate URL by splitting it at the first occurrence of "://",
    #   taking the part after it, and then partitioning it at the first occurrence of "/".
    path = candidate.split("://", 1)[1].partition("/")[2].rstrip("/")
    candidate_hostname = candidate_hostname + "/" + path
    
    #   returns false if combined URL is in the set
    return candidate_hostname not in hostnames

