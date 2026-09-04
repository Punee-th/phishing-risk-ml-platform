"""FastAPI application for phishing URL risk prediction."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.predictor import predict_url


app = FastAPI(
    title="Phishing URL Risk API",
    description=(
        "A lexical machine-learning API that estimates whether "
        "a submitted URL resembles phishing or legitimate URLs."
    ),
    version="1.1.0",
)


class PredictionRequest(BaseModel):
    """URL prediction request."""

    url: str = Field(
    ...,
    min_length=1,
    max_length=2048,
    description="URL to evaluate",
    json_schema_extra={
        "example": "https://www.adelaide.edu.au/"
    },
)


class PredictionResponse(BaseModel):
    """URL prediction response."""

    url: str
    canonical_url: str
    prediction: str
    phishing_score: float
    threshold: float
    model_version: str


@app.get("/")
def root():
    """Return basic API information."""

    return {
        "service": "Phishing URL Risk API",
        "version": "1.1.0",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check():
    """Return the API health status."""

    return {
        "status": "healthy",
        "model_version": "1.1.0",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def create_prediction(request: PredictionRequest):
    """Generate a phishing-risk prediction for a URL."""

    try:
        return predict_url(request.url)

    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error