from src.feature_extractor import (
    FEATURE_NAMES,
    extract_engineered_features,
)


def test_returns_all_expected_features():
    features = extract_engineered_features(
        "https://www.adelaide.edu.au"
    )

    assert list(features.keys()) == FEATURE_NAMES
    assert len(features) == 13


def test_adelaide_expected_features():
    features = extract_engineered_features(
        "https://www.adelaide.edu.au/"
    )

    assert features["url_length"] == 27
    assert features["domain_length"] == 19
    assert features["is_domain_ip"] == 0
    assert features["tld_length"] == 2
    assert features["subdomain_count"] == 2
    assert features["letter_count"] == 21
    assert features["digit_count"] == 0
    assert features["is_https"] == 1


def test_trailing_slash_produces_identical_features():
    without_slash = extract_engineered_features(
        "https://www.adelaide.edu.au"
    )

    with_slash = extract_engineered_features(
        "https://www.adelaide.edu.au/"
    )

    assert without_slash == with_slash


def test_missing_scheme_produces_identical_features():
    explicit_https = extract_engineered_features(
        "https://www.adelaide.edu.au"
    )

    missing_scheme = extract_engineered_features(
        "www.adelaide.edu.au"
    )

    assert explicit_https == missing_scheme


def test_http_changes_https_feature():
    https_features = extract_engineered_features(
        "https://example.com"
    )

    http_features = extract_engineered_features(
        "http://example.com"
    )

    assert https_features["is_https"] == 1
    assert http_features["is_https"] == 0


def test_ip_address_detection():
    features = extract_engineered_features(
        "https://192.168.1.1/login"
    )

    assert features["is_domain_ip"] == 1