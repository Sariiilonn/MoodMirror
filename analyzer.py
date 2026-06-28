"""
analyzer.py - Sentiment analysis engine for MoodMirror.
Uses NLTK's VADER to analyze emotional tone of text.
"""

from nltk.sentiment import SentimentIntensityAnalyzer
_sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text.
    
    Args:
        text (str): The user's diary entry
        
    Returns:
        dict: {
            'compound': float (-1 to 1),
            'positive': float (0 to 1),
            'neutral': float (0 to 1),
            'negative': float (0 to 1),
            'emoji': str (emoji representation),
            'label': str (human-readable label)
        }
    """
    if not text or not text.strip():
        return {
            'compound': 0,
            'positive': 0,
            'neutral': 1,
            'negative': 0,
            'emoji': '😶',
            'label': 'Empty entry'
        }
    
    scores = _sia.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.5:
        emoji = '😄'
        label = 'Very Positive'
    elif compound >= 0.1:
        emoji = '🙂'
        label = 'Slightly Positive'
    elif compound > -0.1:
        emoji = '😐'
        label = 'Neutral'
    elif compound > -0.5:
        emoji = '😔'
        label = 'Slightly Negative'
    else:
        emoji = '😢'
        label = 'Very Negative'
    
    return {
        'compound': compound,
        'positive': scores['pos'],
        'neutral': scores['neu'],
        'negative': scores['neg'],
        'emoji': emoji,
        'label': label
    }
if __name__ == "__main__":
    test_texts = [
        "Today was absolutely wonderful! I got the scholarship!",
        "I feel tired and a bit sad today. Nothing went right.",
        "The weather is okay. Nothing special happened.",
        "I'm absolutely devastated. Everything is falling apart.",
        "I am so grateful for my friends and family. Life is beautiful."
    ]
    
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: {text}")
        print(f"Score: {result['compound']:.2f} | {result['emoji']} {result['label']}")
        print("-" * 50)