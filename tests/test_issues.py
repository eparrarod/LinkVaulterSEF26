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
    assert normalize_tags([" Python ", "", "PYTHON", "Review"]) == ["python", "review"]


def test_issue_04():
    assert next_link_id([{"id": 2}, {"id": 9}]) == 10


def test_issue_05():
    original = {"id": 1, "archived": True}
    restored = restore_link(original)
    assert restored == {"id": 1, "archived": False}
    assert original == {"id": 1, "archived": True}


def test_issue_06():
    assert is_nonblank_title("  ") is False


def test_issue_07():
    assert is_safe_url("https://example.com") is True
    assert is_safe_url("httpscript:alert(1)") is False
    assert is_safe_url("https:///missing-host") is False


def test_issue_08():
    assert has_valid_tag_length("   ") is False
    assert has_valid_tag_length("  python  ", maximum=6) is True


def test_issue_09():
    assert validate_import_row({}) == ["missing title", "missing url"]


def test_issue_10():
    links = [
        {"url": "https://example.com/docs/", "archived": False},
        {"url": "https://old.example.com", "archived": True},
    ]
    assert is_unique_url("HTTPS://EXAMPLE.COM/docs", links) is False
    assert is_unique_url("https://old.example.com", links) is True


def test_issue_11():
    links = [{"id": 1, "archived": False}, {"id": 2, "archived": True}]
    result = active_links(links)
    assert result == [{"id": 1, "archived": False}]
    assert links == [{"id": 1, "archived": False}, {"id": 2, "archived": True}]


def test_issue_12():
    links = [{"title": "Python Guide", "url": "https://example.com"}, {"title": "Other", "url": "https://PYTHON.org"}]
    assert search_text(links, "python") == links


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

