from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re
STOP_WORDS = set(stopwords.words('english'))
STOP_WORDS.update(['im', 'ive', 'dont', 'cant', 'today', 'day', 'felt', 'feel', 'feeling', 'like', 'just', 'know'])


def extract_keywords(text, top_n=10):
    """
    Extract the most frequent meaningful words from text.
    
    Args:
        text (str): Input text
        top_n (int): Number of keywords to return
        
    Returns:
        str: Comma-separated keywords
    """
    cleaned = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = word_tokenize(cleaned)
    meaningful = [word for word in tokens 
                  if word not in STOP_WORDS and len(word) > 2]
    counter = Counter(meaningful)
    top_words = [word for word, count in counter.most_common(top_n)]
    
    return ', '.join(top_words)


def get_chapter_name(mean_sentiment):
    if mean_sentiment >= 0.3:
        return " Season of Blossoms 🌺"
    elif mean_sentiment >= 0.0:
        return " Season of Gentle Light 🌤️"
    elif mean_sentiment >= -0.3:
        return " Season of Passing Clouds 🌥️"
    elif mean_sentiment >= -0.6:
        return " Season of Heavy Rains 🌧️"
    else:
        return " Season of Storms ⛈️"