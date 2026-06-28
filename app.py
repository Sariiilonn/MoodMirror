"""
app.py - MoodMirror Streamlit Application
Main entry point for the web interface.
"""

import streamlit as st
from analyzer import analyze_sentiment
from database import init_db, insert_entry, get_entry_count, get_last_n_entries, insert_milestone, get_all_milestones
from utils import extract_keywords
from report_generator import generate_report


st.set_page_config(page_title="MoodMirror", page_icon="🪞", layout="wide")

init_db()


def write_entry_page():
    st.header("✍️ How are you feeling today?")
    st.markdown("*Write whatever comes to mind. There are no rules.*")

    with st.form(key="entry_form", clear_on_submit=True):
        user_text = st.text_area("Your entry:", height=200, placeholder="Dear diary... today I felt...")
        submitted = st.form_submit_button("💾 Save Entry", type="primary")

    if submitted:
        if not user_text or not user_text.strip():
            st.warning("Please write something before saving.")
        else:
            sentiment = analyze_sentiment(user_text)
            keywords = extract_keywords(user_text)
            entry_id = insert_entry(user_text, sentiment, keywords)

            st.success(f"Entry saved! {sentiment['emoji']} Mood: {sentiment['label']}")
            score_1_to_10 = round((sentiment['compound'] + 1) * 4.5 + 1, 1)
            st.metric("Mood Score", f"{score_1_to_10}/10")

            total_entries = get_entry_count()
            entries_to_next = 20 - (total_entries % 20)
            if entries_to_next == 20:
                entries_to_next = 0
            st.info(f"📝 Total entries: {total_entries} | Next milestone in: {entries_to_next} entries")

            if total_entries > 0 and total_entries % 20 == 0:
                st.balloons()
                st.success("🎉 Milestone reached! Generating your report...")
                entries = get_last_n_entries(20)
                report = generate_report(entries)
                insert_milestone(total_entries, report)
                st.rerun()

    total = get_entry_count()
    remaining = 20 - (total % 20)
    if remaining == 20:
        remaining = 0
    progress = (20 - remaining) / 20 if remaining > 0 else 0
    st.progress(progress, text=f"Entries until next milestone: {remaining}/20")


def reports_page():
    st.header("📊 Your Milestone Reports")

    milestones = get_all_milestones()

    if not milestones:
        st.info("No reports yet. Write 20 entries to unlock your first milestone!")
        return

    import json
    for milestone in reversed(milestones):
        report = json.loads(milestone['report_json'])

        with st.expander(f"{report['chapter_name']} — Entry #{milestone['entry_count']}"):
            st.markdown(f"### {report['chapter_name']}")
            st.markdown(f"*Generated: {milestone['timestamp']}*")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Sentiment", f"{report['mean_sentiment']}")
            with col2:
                st.metric("Highest Point", f"{report['max_sentiment']}")
            with col3:
                st.metric("Lowest Point", f"{report['min_sentiment']}")

            if report.get('chart_path'):
                st.image(report['chart_path'], caption="Sentiment Journey")

            if report.get('wordcloud_path'):
                st.image(report['wordcloud_path'], caption="Your Word Cloud")

            if report.get('top_keywords'):
                st.markdown("**🔑 Top Keywords:**")
                keywords_text = ", ".join([f"{w} ({c}x)" for w, c in report['top_keywords']])
                st.markdown(keywords_text)

            st.markdown("### 💭 Your Mirror")
            st.markdown(report['interpretation'])


st.title("🪞 MoodMirror")
st.subheader("Your Personal Emotion Tracker")
st.markdown("---")

st.sidebar.title("📖 Navigation")
page = st.sidebar.radio("Go to:", ["✍️ Write Entry", "📊 Milestone Reports"])

if page == "✍️ Write Entry":
    write_entry_page()
else:
    reports_page()