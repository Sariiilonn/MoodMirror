"""
report_generator.py - Generates Milestone Reports for MoodMirror.
Creates visualizations and text summaries from user entries.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
import pandas as pd
from utils import get_chapter_name

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def to_display(score):
    """Convert -1 to +1 scale → 1 to 10 scale."""
    return round((score + 1) * 4.5 + 1, 1)


def generate_report(entries, previous_self_letter=None):
    """Generate a complete milestone report from 20 entries."""
    df = pd.DataFrame([{
        'id': e['id'],
        'timestamp': e['timestamp'],
        'text': e['text'],
        'score': e['sentiment_score'],
        'label': e['sentiment_label'],
        'keywords': e['keywords']
    } for e in entries])
    
    df = df.iloc[::-1].reset_index(drop=True)
    
    mean_sentiment_raw = df['score'].mean()
    min_sentiment_raw = df['score'].min()
    max_sentiment_raw = df['score'].max()
    
    chapter = get_chapter_name(mean_sentiment_raw)
    
    chart_path = generate_sentiment_chart(df, mean_sentiment_raw)
    wordcloud_path = generate_wordcloud(df)
    
    all_keywords = []
    for kw_string in df['keywords']:
        if kw_string:
            all_keywords.extend([k.strip() for k in kw_string.split(',')])
    
    from collections import Counter
    kw_counter = Counter(all_keywords)
    top_keywords = kw_counter.most_common(10)
    
    interpretation = generate_interpretation(mean_sentiment_raw, df['score'].tolist(), top_keywords)
    
    report = {
        'chapter_name': chapter,
        'entry_count': len(entries),
        'mean_sentiment': to_display(mean_sentiment_raw),
        'min_sentiment': to_display(min_sentiment_raw),
        'max_sentiment': to_display(max_sentiment_raw),
        'chart_path': chart_path,
        'wordcloud_path': wordcloud_path,
        'top_keywords': top_keywords,
        'interpretation': interpretation,
        'previous_self_letter': previous_self_letter,
        'generated_at': datetime.now().isoformat()
    }
    
    return report


def generate_sentiment_chart(df, mean_sentiment_raw):
    """Create a line chart of sentiment scores (1-10 scale)."""
    plt.figure(figsize=(10, 4))
    
    x = range(1, len(df) + 1)
    y = [to_display(s) for s in df['score'].values]
    mean_display = to_display(mean_sentiment_raw)
    
    plt.plot(x, y, marker='o', color='#6C5CE7', linewidth=2, markersize=8)
    plt.axhline(y=5.5, color='gray', linestyle='--', alpha=0.5, label='Neutral (5.5)')
    plt.axhline(y=mean_display, color='red', linestyle='--', alpha=0.5, label=f'Average: {mean_display:.1f}')
    
    colors = ['#2ECC71' if s >= 5.5 else '#E74C3C' for s in y]
    plt.scatter(x, y, c=colors, s=100, zorder=5)
    
    plt.title('Your Emotional Journey', fontsize=16, fontweight='bold')
    plt.xlabel('Entry Number', fontsize=12)
    plt.ylabel('Mood Score (1-10)', fontsize=12)
    plt.ylim(0, 11)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    chart_path = os.path.join(REPORT_DIR, f'chart_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    plt.savefig(chart_path, dpi=100)
    plt.close()
    
    return chart_path


def generate_wordcloud(df):
    """Create a word cloud from all entry texts."""
    all_text = ' '.join(df['text'].values)
    
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        collocations=False
    ).generate(all_text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Your Most Frequent Words', fontsize=16, fontweight='bold')
    plt.tight_layout(pad=0)
    
    wc_path = os.path.join(REPORT_DIR, f'wordcloud_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    plt.savefig(wc_path, dpi=100)
    plt.close()
    
    return wc_path


def generate_interpretation(mean_sentiment, scores, top_keywords):
    """Generate a human-readable interpretation."""
    
    if len(scores) >= 5:
        first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        trend = "improving" if second_half > first_half + 0.1 else \
                "declining" if second_half < first_half - 0.1 else "stable"
    else:
        trend = "stable"
    
    parts = []
    
    if mean_sentiment >= 0.3:
        parts.append("Your overall mood has been positive and bright. 🌟")
    elif mean_sentiment >= 0.0:
        parts.append("Your mood has been slightly positive, with moments of contentment. 🌤️")
    elif mean_sentiment >= -0.3:
        parts.append("Your mood has had some dips into sadness or stress. 🌥️")
    elif mean_sentiment >= -0.6:
        parts.append("This period has been emotionally challenging. 🌧️")
    else:
        parts.append("This has been an extremely difficult period. ⛈️")
    
    if trend == "improving":
        parts.append("\n📈 Your mood shows an upward trend. Things seem to be getting better!")
    elif trend == "declining":
        parts.append("\n📉 Your mood has been trending downward. Consider pausing and checking in with yourself.")
    else:
        parts.append("\n➡️ Your mood has been relatively stable across this period.")
    
    if top_keywords:
        top_words_list = [w for w, c in top_keywords[:5]]
        parts.append(f"\n🔑 Frequent words: {', '.join(top_words_list)}.")
    
    parts.append("\n💭 Suggestions:")
    if mean_sentiment < 0:
        parts.append("• Do one small thing each day that brings you comfort.")
        parts.append("• Try writing about moments of gratitude.")
        parts.append("• A short walk can shift your emotional state.")
    else:
        parts.append("• Keep nurturing what's working well.")
        parts.append("• Share your positive energy with someone who needs it.")
        parts.append("• What's one thing you'd like to try in the coming weeks?")
    
    return '\n'.join(parts)