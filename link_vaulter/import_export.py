from __future__ import annotations

import csv
import io
import json


def export_json(links: list[dict]) -> str:
    """Issue 21: produce stable, UTF-8-friendly, pretty JSON."""
    return json.dumps(links)


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
    # Converts the comma separated string into a dictionary
    raw_list = list(csv.DictReader(io.StringIO(payload)))

    # If no tags column then add one and have it blank
    # Or if tags is none then make it blank
    for raw in raw_list:
        if "tags" not in raw:
            raw["tags"] = ""
        elif raw["tags"] is None:
            raw["tags"] = ""

    # Removes the blank rows
    unblank_list = [raw for raw in raw_list if raw["title"].strip() != ""
                    or raw["url"].strip() != ""
                    or raw["tags"].strip() != ""]


    # Separates the tags by ; for each entry and then removes blank ones
    # And also remove any trailing space in each string
    tagged_list =[]
    for val in unblank_list:
        val["tags"] = val["tags"].strip().split(";")
        val["tags"] = [tag.strip() for tag in val["tags"]]
        tagged_list.append(val)
        val["tags"] = [tag for tag in val["tags"] if tag != ""]

    return tagged_list


def public_link_view(link: dict) -> dict:
    """Issue 25: expose public fields only and return a new dictionary."""
    return link

