"""Temporary test for database functions."""
from database import init_db, insert_entry, get_entry_count, get_last_n_entries
from analyzer import analyze_sentiment
from utils import extract_keywords

# Initialize database
init_db()
print("Database initialized.")

# Test with a sample entry
sample_text = "I felt really happy today! The sun was shining and I met my friends."
sentiment = analyze_sentiment(sample_text)
keywords = extract_keywords(sample_text)

entry_id = insert_entry(sample_text, sentiment, keywords)
print(f"Inserted entry with ID: {entry_id}")

# Check count
count = get_entry_count()
print(f"Total entries: {count}")

# Get last entry
entries = get_last_n_entries(1)
if entries:
    entry = entries[0]
    print(f"Last entry text: {entry['text']}")
    print(f"Sentiment: {entry['sentiment_score']} ({entry['sentiment_label']})")
    print(f"Keywords: {entry['keywords']}")

print("Database test complete!")