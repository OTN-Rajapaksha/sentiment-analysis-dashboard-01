# sentiment.py
from transformers import pipeline

# 3-label sentiment model (Positive / Neutral / Negative)
# We’ll use "cardiffnlp/twitter-roberta-base-sentiment" as an example.
sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

def analyze_sentiment(text: str):
    """
    Returns: label ∈ {"LABEL_0","LABEL_1","LABEL_2"} mapped to {Negative,Neutral,Positive}
    and confidence score.
    """
    res = sentiment_model(text)[0]
    label_map = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }
    label = label_map.get(res["label"], res["label"])
    return label, float(res["score"])
