from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "model_version": "1.1.0",
    }


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={
            "url": "https://www.adelaide.edu.au/"
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["canonical_url"] == (
        "https://www.adelaide.edu.au"
    )
    assert result["prediction"] == "legitimate"
    assert result["phishing_score"] < result["threshold"]
    assert result["model_version"] == "1.1.0"


def test_empty_url_is_rejected():
    response = client.post(
        "/predict",
        json={"url": ""},
    )

    assert response.status_code == 422


def test_missing_url_is_rejected():
    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 422