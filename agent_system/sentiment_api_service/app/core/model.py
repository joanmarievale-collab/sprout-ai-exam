import torch
from transformers import pipeline
from app.core.config import get_settings

settings = get_settings()

LABEL_MAP = {
    "LABEL_0": settings.label_negative,
    "LABEL_1": settings.label_neutral,
    "LABEL_2": settings.label_positive,
}

if settings.device == "auto":
    DEVICE = 0 if torch.cuda.is_available() else -1
elif settings.device == "cuda":
    DEVICE = 0
else:
    DEVICE = -1


class SentimentService:
    def __init__(self):
        self.pipeline = pipeline(
            "sentiment-analysis",
            model=settings.model_name,
            tokenizer=settings.model_name,
            device=DEVICE
        )

    def predict(self, text: str) -> dict:
        if not text:
            return {"model_output": settings.label_neutral, "confidence_score": 0.0}

        result = self.pipeline(text[:settings.max_tokens])[0]
        sentiment = LABEL_MAP.get(result["label"], settings.label_neutral)

        return {
            "model_output": sentiment,
            "confidence_score": round(result["score"] * 100, 2)
        }
