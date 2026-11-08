from link_vaulter.validation import is_safe_url


def test_good_urls():
    assert is_safe_url("http://example.com") is True
    assert is_safe_url("https://example.com") is True


def test_bad_urls():
    assert is_safe_url("javascript:alert(1)") is False
    assert is_safe_url("ftp://example.com") is False
    assert is_safe_url("http://") is False