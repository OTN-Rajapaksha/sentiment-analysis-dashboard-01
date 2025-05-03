# backend.py
from sentiment import analyze_sentiment
from database import insert_comment

def process_text(text: str):
    # 1) run sentiment model
    sentiment, score = analyze_sentiment(text)
    # 2) store result
    insert_comment(text, sentiment, score)
    # 3) return for UI
    return sentiment, score
