"""Additional tests for Issue 18: escape tag text before rendering HTML."""

import pytest

from link_vaulter.formatting import safe_tag_html


def test_script_tag_is_rendered_as_text():
    result = safe_tag_html("<script>alert(1)</script>")
    assert "<script>" not in result
    assert result == '<span class="tag">&lt;script&gt;alert(1)&lt;/script&gt;</span>'


@pytest.mark.parametrize(
    "raw, escaped",
    [
        ("<", "&lt;"),
        (">", "&gt;"),
        ("&", "&amp;"),
        ('"', "&quot;"),
        ("'", "&#x27;"),
    ],
)
def test_each_special_character_is_escaped(raw, escaped):
    assert safe_tag_html(raw) == f'<span class="tag">{escaped}</span>'


def test_ampersand_is_escaped_exactly_once():
    assert safe_tag_html("R&D") == '<span class="tag">R&amp;D</span>'
    # Text that already looks like an entity is still user text, not markup.
    assert safe_tag_html("&lt;") == '<span class="tag">&amp;lt;</span>'


def test_quotes_cannot_break_out_into_attributes():
    result = safe_tag_html('" onmouseover="alert(1)')
    assert result == '<span class="tag">&quot; onmouseover=&quot;alert(1)</span>'


def test_wrapper_remains_markup():
    result = safe_tag_html("<b>bold</b>")
    assert result.startswith('<span class="tag">')
    assert result.endswith("</span>")
    assert result.count("<") == 2  # only the wrapper's own tags


@pytest.mark.parametrize("tag", ["python", "web-dev", "c++", "café", "machine learning"])
def test_ordinary_text_stays_readable(tag):
    assert safe_tag_html(tag) == f'<span class="tag">{tag}</span>'


def test_empty_tag():
    assert safe_tag_html("") == '<span class="tag"></span>'
