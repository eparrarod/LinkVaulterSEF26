from __future__ import annotations

from datetime import datetime, timezone
from html import escape


def display_host(url: str) -> str:
    """Issue 16: display the hostname without credentials, port, or www."""
    return url.split("//")[-1].split("/")[0]


def pluralize_visits(count: int) -> str:
    """Issue 17: render '1 visit' and '<n> visits' correctly."""
    return f"{count} visits"


def safe_tag_html(tag: str) -> str:
    """Issue 18: escape user text before placing it inside tag markup."""
    return f'<span class="tag">{tag}</span>'


def truncate_title(title: str, limit: int = 40) -> str:
    """Issue 19: enforce total length including ellipsis; do not alter short text."""

    #If no characters then return nothing.
    if limit <= 0:
        return ""

    #If the title works then keep it unchanged.
    if len(title) <= limit:
        return title

    # If the limit can only fit elipsis, then only return elipsis.
    if limit <= 3:
        return "." * limit

    #Shorten the link to add the elipsis.
    letters_to_keep = limit - 3
    shortened_title = title[:letters_to_keep]
    return shortened_title + "..."


def relative_age(iso_timestamp: str, now: datetime | None = None) -> str:
    """Issue 20: report minutes/hours/days and handle future timestamps safely.

    Args:
        iso_timestamp: Timezone-aware ISO timestamp.
        now: Time to compare against. Defaults to the current UTC time.

    Returns:
        "just now" if under a min. old, or in the future, otherwise the largest
        whole unit (min->hours->days)
    """
    # Seconds in each unit, fixed magic #'s
    SECONDS_PER_MIN = 60
    SECONDS_PER_HOUR = 60 * SECONDS_PER_MIN
    SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR

    now = now or datetime.now(timezone.utc)
    then = datetime.fromisoformat(iso_timestamp)
    seconds = int((now - then).total_seconds())

    # under min old
    if seconds < SECONDS_PER_MIN:
        return "just now"

    # under an hour: show min
    if seconds < SECONDS_PER_HOUR:
        minutes = seconds // SECONDS_PER_MIN
        if minutes == 1:
            return "1 minute ago"
        return f"{minutes} minutes ago"

    # under a day: show hrs
    if seconds < SECONDS_PER_DAY:
        hours = seconds // SECONDS_PER_HOUR
        if hours == 1:
            return "1 hour ago"
        return f"{hours} hours ago"

    # otherwise: show days
    days = seconds // SECONDS_PER_DAY
    if days == 1:
        return "1 day ago"
    return f"{days} days ago"

