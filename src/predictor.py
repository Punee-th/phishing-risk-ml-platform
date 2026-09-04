"""Prediction service for the phishing URL model."""

from pathlib import Path

import joblib
import pandas as pd

from src.canonicalizer import canonicalize_url
from src.feature_extractor import extract_engineered_features


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "phishing_url_model_v1_1_0.joblib"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file was not found: {MODEL_PATH}"
    )

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
threshold = float(model_package["threshold"])
feature_names = list(model_package["feature_names"])
model_version = model_package["model_version"]


def predict_url(url: str) -> dict:
    """
    Predict whether a URL is phishing or legitimate.

    Args:
        url: Raw URL submitted for classification.

    Returns:
        Prediction details containing the canonical URL,
        phishing score, threshold and model version.
    """
    features = extract_engineered_features(url)

    feature_frame = pd.DataFrame(
        [features],
        columns=feature_names
    )

    phishing_class_position = list(
        model.classes_
    ).index(0)

    phishing_score = model.predict_proba(
        feature_frame
    )[0, phishing_class_position]

    prediction = (
        "phishing"
        if phishing_score >= threshold
        else "legitimate"
    )

    return {
        "url": url,
        "canonical_url": canonicalize_url(url),
        "prediction": prediction,
        "phishing_score": round(float(phishing_score), 4),
        "threshold": threshold,
        "model_version": model_version,
    }