"""Additional tests for Issue 2: trim titles while preserving internal spacing."""

import pytest

from link_vaulter.app import create_app
from link_vaulter.models import normalize_title


def test_trims_leading_and_trailing_spaces():
    assert normalize_title(" Pull Request Guide ") == "Pull Request Guide"


@pytest.mark.parametrize(
    "raw",
    [
        "\tPull Request Guide\t",
        "\nPull Request Guide\n",
        "\r\nPull Request Guide\r\n",
        " \t\n Pull Request Guide \n\t ",
    ],
)
def test_trims_surrounding_tabs_and_newlines(raw):
    assert normalize_title(raw) == "Pull Request Guide"


def test_preserves_internal_whitespace():
    assert normalize_title("  Pull   Requests  ") == "Pull   Requests"
    assert normalize_title(" Pull\tRequest\nGuide ") == "Pull\tRequest\nGuide"


def test_preserves_capitalization():
    assert normalize_title("  gitHUB PR Guide ") == "gitHUB PR Guide"


def test_already_clean_title_is_unchanged():
    assert normalize_title("Pull Request Guide") == "Pull Request Guide"


@pytest.mark.parametrize("raw", ["", "   ", "\t\n"])
def test_empty_or_whitespace_only_becomes_empty_string(raw):
    assert normalize_title(raw) == ""


def test_saved_link_title_is_trimmed_through_the_app():
    client = create_app(testing=True).test_client()
    response = client.post(
        "/links",
        data={"title": "\t  Pull   Request Guide \n", "url": "https://example.com/pr-guide", "tags": "git"},
    )
    assert response.status_code == 302
    saved = client.get("/api/links").get_json()[-1]
    assert saved["title"] == "Pull   Request Guide"
