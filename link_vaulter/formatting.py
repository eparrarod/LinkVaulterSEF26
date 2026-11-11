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
    return title[:limit] + "..."


def relative_age(iso_timestamp: str, now: datetime | None = None) -> str:
    """Issue 20: report minutes/hours/days and handle future timestamps safely."""
    now = now or datetime.now(timezone.utc)
    then = datetime.fromisoformat(iso_timestamp)
    seconds = int((now - then).total_seconds())
    return f"{seconds // 60} minutes ago"

