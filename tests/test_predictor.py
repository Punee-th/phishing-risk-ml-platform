from src.predictor import predict_url


def test_prediction_contains_required_fields():
    result = predict_url(
        "https://www.adelaide.edu.au"
    )

    expected_fields = {
        "url",
        "canonical_url",
        "prediction",
        "phishing_score",
        "threshold",
        "model_version",
    }

    assert set(result.keys()) == expected_fields


def test_adelaide_is_classified_as_legitimate():
    result = predict_url(
        "https://www.adelaide.edu.au"
    )

    assert result["prediction"] == "legitimate"
    assert result["phishing_score"] < result["threshold"]


def test_prediction_is_invariant_to_root_slash():
    without_slash = predict_url(
        "https://www.adelaide.edu.au"
    )

    with_slash = predict_url(
        "https://www.adelaide.edu.au/"
    )

    assert (
        without_slash["canonical_url"]
        == with_slash["canonical_url"]
    )

    assert (
        without_slash["phishing_score"]
        == with_slash["phishing_score"]
    )

    assert (
        without_slash["prediction"]
        == with_slash["prediction"]
    )


def test_model_metadata_is_returned():
    result = predict_url(
        "https://example.com"
    )

    assert result["model_version"] == "1.1.0"
    assert result["threshold"] == 0.5
    assert 0.0 <= result["phishing_score"] <= 1.0