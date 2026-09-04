from src.canonicalizer import canonicalize_url


def test_removes_root_trailing_slash():
    assert canonicalize_url(
        "https://www.adelaide.edu.au/"
    ) == "https://www.adelaide.edu.au"


def test_adds_https_when_scheme_is_missing():
    assert canonicalize_url(
        "www.adelaide.edu.au"
    ) == "https://www.adelaide.edu.au"


def test_lowercases_scheme_and_hostname():
    assert canonicalize_url(
        "HTTPS://WWW.ADELAIDE.EDU.AU/"
    ) == "https://www.adelaide.edu.au"


def test_removes_default_https_port():
    assert canonicalize_url(
        "https://example.com:443/"
    ) == "https://example.com"


def test_preserves_meaningful_path_and_query():
    assert canonicalize_url(
        "https://example.com/login?user=test"
    ) == "https://example.com/login?user=test"


def test_removes_fragment():
    assert canonicalize_url(
        "https://example.com/login#section"
    ) == "https://example.com/login"