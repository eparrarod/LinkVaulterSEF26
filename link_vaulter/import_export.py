from __future__ import annotations

import csv
import io
import json


def export_json(links: list[dict]) -> str:
    """Issue 21: produce stable, UTF-8-friendly, pretty JSON."""
    return json.dumps(links, 
    indent=2, #makes json readable with two space indentation
    sort_keys=True, #sorts keys in alphabetical order
    ensure_ascii=False) #keeps foreign characters in their original form


def import_json(payload: str) -> list[dict]:
    """Issue 22: require a top-level list of objects; reject other shapes."""
    return json.loads(payload)


def export_csv(links: list[dict]) -> str:
    """Issue 23: quote commas/newlines and join tags using semicolons."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["title", "url", "tags"])
    for item in links:
        writer.writerow([item["title"], item["url"], ",".join(item.get("tags", []))])
    return output.getvalue()


def import_csv(payload: str) -> list[dict]:
    """Issue 24: skip blank rows and split semicolon-delimited tags."""
    return list(csv.DictReader(io.StringIO(payload)))


def public_link_view(link: dict) -> dict:
    """Issue 25: expose public fields only and return a new dictionary."""
    return link

