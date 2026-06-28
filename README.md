A personal smart diary that reflects your emotional journey.
# 🪞 MoodMirror — Your Personal Emotion Tracker

> *"An intelligent diary that listens without judgment, mirroring back emotional patterns every 20 entries."*

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![NLTK](https://img.shields.io/badge/NLTK-VADER-orange)

---

## 🌟 What is MoodMirror?

MoodMirror is a personal smart diary built as part of my journey into Computer Science. Unlike traditional diaries, MoodMirror doesn't just store your words—it **listens** to them.

Write whenever you want. No daily pressure. No judgment. After every 20 entries, MoodMirror creates a **Milestone Report** that shows you patterns in your emotional life.

---

## 🎯 Why I Built This

I'm applying for the **GKS (Global Korea Scholarship)** for Computer Science. I'm not a professional programmer—I started learning Python recently. This project is my way of showing that:

- I can **identify a real human problem** and build a solution
- I'm **not afraid to learn** new technologies from scratch
- I care about building things that help people understand themselves better
- I document my journey and share my learning process

---

## ✨ Features

- 📝 **Free-form Diary**: Write entries without daily pressure
- 🎭 **Real-time Sentiment Analysis**: Uses VADER (NLTK) to detect emotional tone
- 📊 **Milestone Reports**: Every 20 entries, receive a comprehensive analysis
- 🌺 **Poetic Chapter Names**: Reports are named based on emotional patterns
- 📈 **Sentiment Charts**: Visualize your emotional journey
- ☁️ **Word Clouds**: See your most frequent thoughts
- 💭 **Gentle Interpretations**: Rule-based insights about your mood patterns
- 💌 **Letters to Future Self**: Leave messages for your next milestone

---

## 🏗️ Project Structure

MoodMirror/
├── venv/              (auto-created, don't touch)
├── .gitignore
├── README.md
├── analyzer.py        (sentiment analysis)
├── database.py        (SQLite operations)
├── report_generator.py(milestone report logic)
├── utils.py           (helper functions like keywords)
└── app.py             (Streamlit UI - main file)

---

## 🧠 Design Philosophy: Why 20 Entries?

Most mood trackers are time-based (daily, weekly). But I asked myself: *"Do people really feel things on a schedule?"*

By triggering milestones after **20 entries** (not 20 days), MoodMirror respects each user's unique rhythm. Some weeks are full of words; others are quiet. The report comes when there's enough meaningful data—not when a calendar says so.

This is **user-centered design** in practice.

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/Sariiilonn/MoodMirror.git
cd MoodMirror

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('stopwords'); nltk.download('punkt')"

# Run the app
streamlit run app.py