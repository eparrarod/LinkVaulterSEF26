from datetime import datetime, timezone

import pytest

from link_vaulter.analytics import count_active, favorite_rate, most_common_tag, total_visits, unique_domains
from link_vaulter.formatting import display_host, pluralize_visits, relative_age, safe_tag_html, truncate_title
from link_vaulter.import_export import export_csv, export_json, import_csv, import_json, public_link_view
from link_vaulter.models import next_link_id, normalize_tags, normalize_title, normalize_url, restore_link
from link_vaulter.search import active_links, favorites_first, filter_any_tag, paginate, search_text
from link_vaulter.validation import has_valid_tag_length, is_nonblank_title, is_safe_url, is_unique_url, validate_import_row


def test_issue_01():
    assert normalize_url("HTTPS://Example.COM/Docs/ReadMe/") == "https://example.com/Docs/ReadMe"


def test_issue_02():
    assert normalize_title("  Pull   Requests  ") == "Pull   Requests"


def test_issue_03():
    # original assignment test
    assert normalize_tags([" Python ", "", "PYTHON", "Review"]) == ["python", "review"]


def test_issue_03_whitespace_and_case():
    assert normalize_tags(["  HELLO  ", " World "]) == ["hello", "world"]


def test_issue_03_duplicates():
    assert normalize_tags(["Python", "python", "PYTHON"]) == ["python"]


def test_issue_03_blank_tags():
    assert normalize_tags(["", "  ", "Music"]) == ["music"]


def test_issue_03_preserves_order():
    assert normalize_tags(["Music", "Coding", "music", "School"]) == [
        "music", "coding", "school"
    ]

def test_issue_03_empty_list():
    assert normalize_tags([]) == []


def test_issue_04():
    assert next_link_id([{"id": 2}, {"id": 9}]) == 10


def test_issue_05():
    original = {"id": 1, "archived": True}
    restored = restore_link(original)
    assert restored == {"id": 1, "archived": False}
    assert original == {"id": 1, "archived": True}


def test_issue_06():

    assert is_nonblank_title("  ") is False # Tests a blank title

    assert is_nonblank_title("\n") is False # Tests a title with a newline

    assert is_nonblank_title("\t") is False # Tests a title with a tab

    assert is_nonblank_title("asdf") is True # Tests a title with text

    assert is_nonblank_title("  asdf  ") is True # Tests a title with text and blank space



def test_issue_07():
    assert is_safe_url("https://example.com") is True
    assert is_safe_url("httpscript:alert(1)") is False
    assert is_safe_url("https:///missing-host") is False


def test_issue_08():
    assert has_valid_tag_length("   ") is False
    assert has_valid_tag_length("  python  ", maximum=6) is True


def test_issue_09():
    assert validate_import_row({}) == ["missing title", "missing url"]


def test_issue_10_case_insensitive():
    links = [{"url": "https://example.com/docs/", "archived": False}]
    assert is_unique_url("HTTPS://EXAMPLE.COM/docs", links) is False

def test_issue_10_archived_links():
    links = [{"url": "https://old.example.com", "archived": True}]
    assert is_unique_url("https://old.example.com", links) is True

def test_issue_10_www_subdomain():
    links = [{"url": "https://example.com/docs", "archived": False}]
    assert is_unique_url("https://www.example.com/docs", links) is True

def test_issue_10_new_url():
    links = [{"url": "https://example.com/docs", "archived": False}]
    assert is_unique_url("https://new.example.com", links) is True

def test_issue_10_archived_case_insensitive():
    links = [{"url": "https://old.example.com", "archived": True}]
    assert is_unique_url("HTTPS://OLD.EXAMPLE.COM", links) is True

def test_issue_10_different_paths():
    links = [{"url": "https://example.com/docs", "archived": False}]   
    assert is_unique_url("https://example.com/about", links) is True

def test_issue_10_trailing_slash():
    links = [{"url": "https://example.com/docs/", "archived": False}]
    assert is_unique_url("https://example.com/docs", links) is False

def test_issue_10_path_case_sensitive():
    links = [{"url": "https://example.com/Docs", "archived": False}]
    assert is_unique_url("https://example.com/docs", links) is True

def test_issue_10_exact_duplicate():
    links = [{"url": "https://example.com/docs", "archived": False}]
    assert is_unique_url("https://example.com/docs", links) is False


def test_issue_11():
    links = [{"id": 1, "archived": False}, {"id": 2, "archived": True}]
    result = active_links(links)
    assert result == [{"id": 1, "archived": False}]
    assert links == [{"id": 1, "archived": False}, {"id": 2, "archived": True}]


def test_issue_12():
    #Tests generic all upper/lowercase
    links = [{"title": "Python Guide", "url": "https://example.com"}, {"title": "Other", "url": "https://PYTHON.org"}]
    assert search_text(links, "python") == links # Test to ensure that the lowercase title works

    assert search_text(links, "PYTHON") == links # Test to ensure that the uppercase title works

    # Test to ensure that a query that fits both is not returned twice
    links = [{"title": "Python Guide", "url": "https://example.com"}, {"title": "Other", "url": "https://PYTHON.org"}, {"title": "Python", "url": "https://PYTHON.org"}]
    assert search_text(links, "") == links

    # Test to ensure that an empty string returns everything
    links = [{"title": "Python Guide", "url": "https://example.com"}, {"title": "Other", "url": "https://PYTHON.org"}, {"title": "Other", "url": "https://other.org"}]
    assert search_text(links, "") == links




def test_issue_13():
    links = [{"id": 1, "tags": ["python", "web"]}, {"id": 2, "tags": ["web"]}]
    assert filter_any_tag(links, ["python", "web"]) == links
    assert filter_any_tag(links, []) == links


def test_issue_14():
    links = [
        {"id": 1, "favorite": False, "created_at": "2026-09-03"},
        {"id": 2, "favorite": True, "created_at": "2026-09-01"},
        {"id": 3, "favorite": True, "created_at": "2026-09-02"},
    ]
    assert [x["id"] for x in favorites_first(links)] == [3, 2, 1]


def test_issue_15():
    assert paginate(list(range(10)), page=1, per_page=3) == [0, 1, 2]
    with pytest.raises(ValueError):
        paginate([], page=1, per_page=0)


def test_issue_16():
    assert display_host("https://user:pass@www.Example.com:8443/path") == "Example.com"


def test_issue_17():
    assert pluralize_visits(1) == "1 visit"


def test_issue_18():
    assert safe_tag_html('<script>alert("x")</script>') == '<span class="tag">&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;</span>'


def test_issue_19():
    assert truncate_title("abcdefghij", 8) == "abcde..."
    assert truncate_title("short", 8) == "short"


def test_issue_20():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-15T12:00:00+00:00", now) == "2 days ago"
    assert relative_age("2026-09-17T12:05:00+00:00", now) == "just now"

def test_issue_20_within_minute_now():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-17T11:59:30+00:00", now) == "just now"
    assert relative_age("2026-09-17T12:00:30+00:00", now) == "just now"

def test_issue_20_singular_plural_min():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-17T11:59:00+00:00", now) == "1 minute ago"
    assert relative_age("2026-09-17T11:58:00+00:00", now) == "2 minutes ago"

def test_issue_20_hour_day_threshold():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-17T11:01:00+00:00", now) == "59 minutes ago"
    assert relative_age("2026-09-17T11:00:00+00:00", now) == "1 hour ago"
    assert relative_age("2026-09-16T13:00:00+00:00", now) == "23 hours ago"
    assert relative_age("2026-09-16T12:00:00+00:00", now) == "1 day ago"

def test_issue_20_timezone_aware_stamps():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-17T06:00:00-05:00", now) == "1 hour ago"

def test_issue_20_negative_ages():
    now = datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc)
    assert relative_age("2026-09-19T12:00:00+00:00", now) == "just now"

def test_issue_20_invalidStamps():
    with pytest.raises(ValueError):
        relative_age("not a date")

def test_issue_21():
    result = export_json([{"title": "Café", "id": 1}])
    assert result == '[\n  {\n    "id": 1,\n    "title": "Café"\n  }\n]'


def test_issue_22():
    assert import_json('[{"title": "A"}]') == [{"title": "A"}]
    with pytest.raises(ValueError):
        import_json('{"title": "A"}')


def test_issue_23():
    payload = export_csv([{"title": "One, Two", "url": "https://x.test", "tags": ["a", "b"]}])
    assert '"One, Two"' in payload
    assert "a;b" in payload


def test_issue_24():
    payload = "title,url,tags\nA,https://a.test,python;web\n,,\n"
    assert import_csv(payload) == [{"title": "A", "url": "https://a.test", "tags": ["python", "web"]}]


def test_issue_25():
    original = {"id": 1, "title": "A", "url": "https://a.test", "tags": [], "owner_email": "student@example.edu", "internal_notes": "private"}
    result = public_link_view(original)
    assert result == {"id": 1, "title": "A", "url": "https://a.test", "tags": []}
    assert result is not original


def test_issue_26():
    assert count_active([{"archived": False}, {"archived": True}, {}]) == 2


def test_issue_27():
    links = [{"favorite": True, "archived": False}, {"favorite": False, "archived": False}, {"favorite": True, "archived": True}]
    assert favorite_rate(links) == 50.0
    assert favorite_rate([]) == 0.0


def test_issue_28():
    links = [{"tags": ["Web", "python"]}, {"tags": ["web", "Python"]}]
    assert most_common_tag(links) == "python"


def test_issue_29():
    assert total_visits([{"visits": 3}, {"visits": -2}, {}]) == 3


def test_issue_30():
    links = [
        {"url": "https://www.Example.com/a"},
        {"url": "http://example.com/b"},
        {"url": "https://docs.example.com"},
    ]
    assert unique_domains(links) == 2

