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


def generate_report(entries, previous_self_letter=None):
    """
    Generate a complete milestone report from 20 entries.
    
    Args:
        entries (list): List of entry rows (dict-like) from database
        previous_self_letter (str, optional): Letter from previous milestone
        
    Returns:
        dict: Complete report with all components
    """
    df = pd.DataFrame([{
        'id': e['id'],
        'timestamp': e['timestamp'],
        'text': e['text'],
        'score': e['sentiment_score'],
        'label': e['sentiment_label'],
        'keywords': e['keywords']
    } for e in entries])
    df = df.iloc[::-1].reset_index(drop=True)
    mean_sentiment = df['score'].mean()
    min_sentiment = df['score'].min()
    max_sentiment = df['score'].max()
    
    mean_display = round((mean_sentiment + 1) * 4.5 + 1, 1) 
    min_display = round((min_sentiment + 1) * 4.5 + 1, 1)
    max_display = round((max_sentiment + 1) * 4.5 + 1, 1)

    chapter = get_chapter_name(mean_sentiment)
    chart_path = generate_sentiment_chart(df, mean_sentiment)
    wordcloud_path = generate_wordcloud(df)
    all_keywords = []
    for kw_string in df['keywords']:
        if kw_string:
            all_keywords.extend([k.strip() for k in kw_string.split(',')])
    
    from collections import Counter
    kw_counter = Counter(all_keywords)
    top_keywords = kw_counter.most_common(10)
    interpretation = generate_interpretation(mean_sentiment, df['score'].tolist(), top_keywords)
    report = {
      'chapter_name': chapter,
      'entry_count': len(entries),
      'mean_sentiment': round(mean_display, 1),
      'min_sentiment': round(min_display, 1),
      'max_sentiment': round(max_display, 1),
      'chart_path': chart_path,
      'wordcloud_path': wordcloud_path,
      'top_keywords': top_keywords,
      'interpretation': interpretation,
      'previous_self_letter': previous_self_letter,
      'generated_at': datetime.now().isoformat()
    }
    
    return report


def generate_sentiment_chart(df, mean_sentiment):
    """Create a line chart of sentiment scores and save it."""
    plt.figure(figsize=(10, 4))
    
    x = range(1, len(df) + 1)
    y = [(s + 1) * 4.5 + 1 for s in df['score'].values]
    
    plt.plot(x, y, marker='o', color='#6C5CE7', linewidth=2, markersize=8)
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    mean_display = (mean_sentiment + 1) * 4.5 + 1
    plt.axhline(y=mean_display, color='red', linestyle='--', alpha=0.5, label=f'Average: {mean_display:.1f}')
    colors = ["#0DA934" if s >= 5.5 else "#C31502" for s in y]
    plt.scatter(x, y, c=colors, s=100, zorder=5)
    
    plt.title('Your Emotional Journey', fontsize=16, fontweight='bold')
    plt.xlabel('Entry Number', fontsize=12)
    plt.ylabel('Mood Score(1-10)', fontsize=12)
    plt.ylim(0 , 11)
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
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis('off')
    plt.title('Your Most Frequent Words', fontsize=16, fontweight='bold')
    plt.tight_layout(pad=0)
    
    wc_path = os.path.join(REPORT_DIR, f'wordcloud_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    plt.savefig(wc_path, dpi=100)
    plt.close()
    
    return wc_path


def generate_interpretation(mean_sentiment, scores, top_keywords):
    """Generate a human-readable interpretation based on sentiment patterns."""
    
    if len(scores) >= 5:
        first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
        second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
        trend = "improving" if second_half > first_half + 0.1 else \
                "declining" if second_half < first_half - 0.1 else "stable"
    else:
        trend = "stable"
    
    parts = []
    
    if mean_sentiment >= 0.3:
        parts.append("Your overall mood during this period has been predominantly positive and bright. 🌟")
        parts.append("You seem to be in a good place emotionally. The joy in your words is noticeable.")
    elif mean_sentiment >= 0.0:
        parts.append("Your mood has been slightly positive, with moments of contentment. 🌤️")
        parts.append("There's a gentle balance in your emotional state. Life seems manageable.")
    elif mean_sentiment >= -0.3:
        parts.append("Your mood has had some dips into sadness or stress. 🌥️")
        parts.append("It's okay to not be okay. These feelings are part of being human. Consider giving yourself extra care right now.")
    elif mean_sentiment >= -0.6:
        parts.append("This period has been emotionally challenging for you. 🌧️")
        parts.append("You've been carrying a heavy load. Remember: reaching out to someone you trust can help lighten it. If these feelings persist, consider speaking with a professional.")
    else:
        parts.append("This has been an extremely difficult period. ⛈️")
        parts.append("Your words show real pain. Please know you're not alone. Consider talking to a counselor or trusted person. Your feelings are valid and you deserve support.")
    
    if trend == "improving":
        parts.append("\n📈 The good news: your mood shows an upward trend. Things seem to be getting better!")
    elif trend == "declining":
        parts.append("\n📉 Notice: your mood has been trending downward. This might be a sign to pause and check in with yourself.")
    else:
        parts.append("\n➡️ Your mood has been relatively stable across this period.")
    
    if top_keywords:
        top_words_list = [w for w, c in top_keywords[:5]]
        parts.append(f"\n🔑 Your most frequent meaningful words were: {', '.join(top_words_list)}.")
        parts.append("These words give a glimpse into what's been occupying your mind lately.")
    
    parts.append("\n💭 Suggestions for the next chapter:")
    if mean_sentiment < 0:
        parts.append("• Try to do one small thing each day that brings you comfort.")
        parts.append("• Consider writing about moments of gratitude, even tiny ones.")
        parts.append("• Physical movement, even a short walk, can shift your emotional state.")
    else:
        parts.append("• Keep nurturing what's working well in your life.")
        parts.append("• Consider sharing your positive energy with someone who might need it.")
        parts.append("• What's one thing you'd like to learn or try in the coming weeks?")
    
    return '\n'.join(parts)