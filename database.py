"""
database.py - SQLite database operations for MoodMirror.
Handles all storage and retrieval of entries and milestones.
"""

import sqlite3
import json
from datetime import datetime

DB_NAME = "moodmirror.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Entries table: stores each diary entry
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            text TEXT NOT NULL,
            sentiment_score REAL,
            sentiment_label TEXT,
            keywords TEXT
        )
    """)
    
    # Milestones table: stores generated reports
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            entry_count INTEGER,
            report_json TEXT,
            self_letter TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def insert_entry(text, sentiment_result, keywords):
    """Save a new diary entry."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO entries (timestamp, text, sentiment_score, sentiment_label, keywords)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        text,
        sentiment_result['compound'],
        sentiment_result['label'],
        keywords
    ))
    
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id


def get_entry_count():
    """Return total number of entries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM entries")
    result = cursor.fetchone()
    conn.close()
    return result['count']


def get_last_n_entries(n):
    """Get the most recent n entries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM entries 
        ORDER BY id DESC 
        LIMIT ?
    """, (n,))
    rows = cursor.fetchall()
    conn.close()
    return list(rows)


def get_all_entries():
    """Get all entries ordered by oldest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return list(rows)


def insert_milestone(entry_count, report_dict, self_letter=""):
    """Save a generated milestone report."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO milestones (timestamp, entry_count, report_json, self_letter)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        entry_count,
        json.dumps(report_dict),
        self_letter
    ))
    
    conn.commit()
    milestone_id = cursor.lastrowid
    conn.close()
    return milestone_id


def get_all_milestones():
    """Get all milestones ordered by oldest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM milestones ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return list(rows)


def get_latest_milestone():
    """Get the most recent milestone."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM milestones ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row