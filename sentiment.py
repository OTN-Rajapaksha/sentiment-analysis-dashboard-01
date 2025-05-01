# sentiment.py

from transformers import pipeline

# Load Hugging Face's sentiment-analysis pipeline
sentiment_model = pipeline("sentiment-analysis")

# Function to analyze sentiment of a given text
def analyze_sentiment(text):
    result = sentiment_model(text)[0]  # Get the first result
    return result["label"], float(result["score"])  # Sentiment and confidence score
