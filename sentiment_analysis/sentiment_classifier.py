import pandas as pd
from pathlib import Path
import torch
from transformers import pipeline
import json
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from colorama import Fore, Style, init

init(autoreset=True)


class SentimentClassifier:
    """Sentiment classification using RoBERTa (Cardiff NLP)."""
    
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-sentiment"):
        device = 0 if torch.cuda.is_available() else -1
        self.pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,
            device=device
        )
    
    def predict(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            return {"model_output": "neutral", "confidence_score": 0.0}
        try:
            result = self.pipeline(text[:512])[0]
            label_map = {
                "LABEL_0": "negative",
                "LABEL_1": "neutral",
                "LABEL_2": "positive"
            }
            sentiment = label_map.get(result["label"], "neutral")
            return {
                "model_output": sentiment,
                "confidence_score": round(result["score"] * 100, 2)
            }
        except Exception:
            return {"model_output": "neutral", "confidence_score": 0.0}
    
    def predict_batch(self, texts: list) -> list:
        return [self.predict(t) for t in texts]


def normalize_sentiment(label: str) -> str:
    label = str(label).lower().strip()
    return {
        "positive": "positive", "pos": "positive", "1": "positive",
        "negative": "negative", "neg": "negative", "0": "negative",
        "neutral": "neutral", "neut": "neutral", "2": "neutral"
    }.get(label, label)


def load_test_data(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def calculate_metrics(df: pd.DataFrame):
    df['expected_normalized'] = df['expected_sentiment'].apply(normalize_sentiment)

    acc = accuracy_score(df['expected_normalized'], df['model_output'])
    print(f"\nOverall Accuracy: {acc * 100:.2f}%")
    
    precision, recall, f1, support = precision_recall_fscore_support(
        df['expected_normalized'],
        df['model_output'],
        labels=['positive', 'neutral', 'negative'],
        zero_division=0
    )

    print("\nPer-Class Metrics:")
    for lbl, p, r, f, s in zip(['positive','neutral','negative'], precision, recall, f1, support):
        print(f"{lbl:<8} Precision:{p:.2f} Recall:{r:.2f} F1:{f:.2f} Support:{s}")
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(
        df['expected_normalized'],
        df['model_output'],
        labels=['positive','neutral','negative']
    )
    print(cm)


def run_inference(csv_path: str, output_path: str = "output_sentiment_test.csv"):
    df = load_test_data(csv_path)
    clf = SentimentClassifier()
    predictions = clf.predict_batch(df['text'].tolist())
    df['model_output'] = [p['model_output'] for p in predictions]
    df['confidence_score'] = [p['confidence_score'] for p in predictions]
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")
    calculate_metrics(df)


def interactive_mode(clf: SentimentClassifier, output_csv="output_sentiment_test.csv"):
    print(f"\n{Fore.CYAN}Interactive Sentiment Classifier (RoBERTa){Style.RESET_ALL}")
    results = []

    while True:
        try:
            text = input("Enter text ('quit' to exit): ").strip()
            if text.lower() in ['quit', 'exit']:
                if results:
                    pd.DataFrame(results).to_csv(output_csv, index=False)
                print(f"Results saved to {output_csv}\nGoodbye!")
                break

            if not text:
                continue

            pred = clf.predict(text)
            results.append({
                'text': text,
                'expected_sentiment': '',
                'model_output': pred['model_output'],
                'confidence_score': pred['confidence_score']
            })

            print(json.dumps(pred, indent=2))

        except KeyboardInterrupt:
            if results:
                pd.DataFrame(results).to_csv(output_csv, index=False)
            print(f"\nResults saved to {output_csv}\nProgram interrupted. Goodbye!")
            break


def main():
    clf = SentimentClassifier()
    csv_path = "sentiment_test_cases_2025.csv"

    if Path(csv_path).exists():
        print(f"Running batch inference on {csv_path}...")
        run_inference(csv_path)

    interactive_mode(clf)


if __name__ == "__main__":
    main()
