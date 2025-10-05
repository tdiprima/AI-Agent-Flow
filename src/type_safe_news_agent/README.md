# Type-Safe News Agent

This project implements a type-safe agent for scraping news articles, validating their structure, and storing them in a database using Python, Pydantic, and SQLite.

## What does this project do?

- **Scrapes news articles** from one or more websites.
- **Extracts and validates** structured information (title, summary, URL, publication date, source) using Pydantic models for type safety.
- **Stores validated news summaries** in a SQLite database for further analysis or retrieval.

## How does it work?

### 1. Structured Output with Pydantic

The `NewsSummary` Pydantic model defines a strict schema for news summaries. This ensures that every article the agent processes conforms to a known, type-safe structure.

### 2. Scraping and Validation

The agent (`agent.py`) fetches HTML from news websites, parses articles using BeautifulSoup, and extracts relevant fields. For each article, it creates a `NewsSummary` instance. If the data doesn't match the schema (e.g., missing or invalid fields), the instance creation will fail, preventing bad data from entering the pipeline.

### 3. Storing Results

Validated news summaries are inserted into a SQLite database (`database.py`). Duplicate URLs are ignored to prevent storing the same article multiple times.

### 4. Running the Agent

The entry point (`main.py`) initializes the database and runs the agent against a list of news sites. You can add or change URLs in this list as needed.

### 5. Checking Stored News Summaries

After running the agent, you can examine the stored news summaries in the SQLite database using the following commands:

**View total count of stored articles:**

```bash
sqlite3 news.db "SELECT COUNT(*) FROM news;"
```

**View recent articles (latest 10):**

```bash
sqlite3 news.db "SELECT title, source, published_at FROM news ORDER BY published_at DESC LIMIT 10;"
```

**View all articles from a specific source:**

```bash
sqlite3 news.db "SELECT title, published_at FROM news WHERE source LIKE '%npr%' ORDER BY published_at DESC;"
```

**View full article details:**

```bash
sqlite3 news.db "SELECT * FROM news LIMIT 5;"
```

**Search articles by keyword:**

```bash
sqlite3 news.db "SELECT title, summary FROM news WHERE title LIKE '%keyword%' OR summary LIKE '%keyword%';"
```

The database schema includes the following fields:

- `id`: Auto-incrementing primary key
- `title`: Article headline
- `url`: Article URL (unique constraint)
- `summary`: Article description/summary
- `published_at`: Publication timestamp
- `source`: RSS feed URL

---

The implementation now respects `robots.txt` by using official RSS feeds meant for syndication, and includes proper error handling for network issues.

Handles RSS feeds instead of HTML scraping. RSS feeds have a different structure.

<br>
