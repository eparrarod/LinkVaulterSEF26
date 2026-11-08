from link_vaulter.formatting import display_host


def test_removes_everything_extra():
    assert display_host("https://user:pass@www.Example.com:8443/path") == "Example.com"


def test_simple_cases():
    assert display_host("https://www.example.com/") == "example.com"
    assert display_host("https://docs.example.com/3/") == "docs.example.com"
    assert display_host("https://example.com:8080") == "example.com"