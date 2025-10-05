# Database Storage (SQLite for simplicity)
import sqlite3

from models import NewsSummary


def init_db():
    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            summary TEXT,
            published_at TEXT,
            source TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def save_news_summary(news: NewsSummary):
    conn = sqlite3.connect("news.db")
    c = conn.cursor()
    try:
        c.execute(
            """
            INSERT OR IGNORE INTO news (title, url, summary, published_at, source)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                news.title,
                str(news.url),
                news.summary,
                news.published_at.isoformat(),
                news.source,
            ),
        )
        conn.commit()
    except Exception as e:
        print(f"DB error: {e}")
    finally:
        conn.close()
