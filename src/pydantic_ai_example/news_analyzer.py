"""
Pydantic AI News Analysis Example

This script demonstrates how to use Pydantic AI to create intelligent agents
that can analyze news articles with structured, type-safe responses.
"""

import sqlite3
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


class NewsArticle(BaseModel):
    """Structured representation of a news article from our database."""

    title: str
    url: str
    summary: str
    published_at: datetime
    source: str


class NewsSentiment(BaseModel):
    """Structured sentiment analysis result."""

    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
    reasoning: str = Field(
        description="Brief explanation of the sentiment classification"
    )


class NewsTopics(BaseModel):
    """Structured topic extraction result."""

    primary_topic: str = Field(description="Main topic/category of the article")
    secondary_topics: List[str] = Field(
        description="Additional topics mentioned", max_items=3
    )
    keywords: List[str] = Field(description="Key terms and entities", max_items=5)


class NewsSummary(BaseModel):
    """Enhanced news summary with AI analysis."""

    original_title: str
    ai_summary: str = Field(description="Concise AI-generated summary in 1-2 sentences")
    key_points: List[str] = Field(description="Main bullet points", max_items=3)
    importance_score: int = Field(ge=1, le=10, description="News importance from 1-10")


class NewsDatabase:
    """Simple database service for retrieving news articles."""

    def __init__(self, db_path: str = "news.db"):
        self.db_path = db_path

    def get_recent_articles(self, limit: int = 5) -> List[NewsArticle]:
        """Fetch recent articles from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT title, url, summary, published_at, source 
            FROM news 
            ORDER BY published_at DESC 
            LIMIT ?
        """,
            (limit,),
        )

        articles = []
        for row in cursor.fetchall():
            article = NewsArticle(
                title=row[0],
                url=row[1],
                summary=row[2],
                published_at=datetime.fromisoformat(row[3]),
                source=row[4],
            )
            articles.append(article)

        conn.close()
        return articles

    def search_articles(self, keyword: str, limit: int = 3) -> List[NewsArticle]:
        """Search articles by keyword."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT title, url, summary, published_at, source 
            FROM news 
            WHERE title LIKE ? OR summary LIKE ?
            ORDER BY published_at DESC 
            LIMIT ?
        """,
            (f"%{keyword}%", f"%{keyword}%", limit),
        )

        articles = []
        for row in cursor.fetchall():
            article = NewsArticle(
                title=row[0],
                url=row[1],
                summary=row[2],
                published_at=datetime.fromisoformat(row[3]),
                source=row[4],
            )
            articles.append(article)

        conn.close()
        return articles


# Create specialized AI agents for different news analysis tasks

# Sentiment Analysis Agent
sentiment_agent = Agent[NewsDatabase, NewsSentiment](
    "openai:gpt-4o-mini",  # Using cost-effective model for simple tasks
    deps_type=NewsDatabase,
    output_type=NewsSentiment,
    system_prompt="""
    You are a news sentiment analyzer. Analyze the sentiment of news articles
    and provide structured feedback with confidence scores and reasoning.
    Be objective and consider the overall tone and implications.
    """,
)

# Topic Extraction Agent
topic_agent = Agent[NewsDatabase, NewsTopics](
    "openai:gpt-4o-mini",
    deps_type=NewsDatabase,
    output_type=NewsTopics,
    system_prompt="""
    You are a news topic classifier. Extract the main topics, categories, 
    and keywords from news articles. Focus on identifying the primary subject
    matter and related themes. Be specific and relevant.
    """,
)

# Summary Enhancement Agent
summary_agent = Agent[NewsDatabase, NewsSummary](
    "openai:gpt-4o",  # Using more capable model for complex summarization
    deps_type=NewsDatabase,
    output_type=NewsSummary,
    system_prompt="""
    You are a news summarization expert. Create concise, informative summaries
    of news articles with key points and importance ratings. Focus on clarity,
    accuracy, and highlighting the most significant information.
    """,
)


@sentiment_agent.tool
def analyze_article_sentiment(ctx: RunContext[NewsDatabase], article_text: str) -> str:
    """Tool to provide article text for sentiment analysis."""
    return f"Analyzing sentiment for: {article_text}"


@topic_agent.tool
def extract_article_topics(ctx: RunContext[NewsDatabase], article_text: str) -> str:
    """Tool to provide article text for topic extraction."""
    return f"Extracting topics from: {article_text}"


@summary_agent.tool
def enhance_article_summary(ctx: RunContext[NewsDatabase], article_text: str) -> str:
    """Tool to provide article text for summary enhancement."""
    return f"Enhancing summary for: {article_text}"


def analyze_recent_news():
    """Demonstrate Pydantic AI analysis of recent news articles."""
    print("🤖 Pydantic AI News Analysis Demo")
    print("=" * 50)

    # Initialize database service
    db = NewsDatabase()

    try:
        # Get recent articles
        articles = db.get_recent_articles(limit=3)

        if not articles:
            print("❌ No articles found in database. Run the main news scraper first!")
            return

        print(f"📰 Analyzing {len(articles)} recent articles...\n")

        for i, article in enumerate(articles, 1):
            print(f"📄 Article {i}: {article.title}")
            print(f"🔗 Source: {article.source}")
            print(f"📅 Published: {article.published_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)

            # Prepare article text for analysis
            article_text = f"Title: {article.title}\nSummary: {article.summary}"

            # Sentiment Analysis
            print("💭 Sentiment Analysis:")
            try:
                sentiment_result = sentiment_agent.run_sync(
                    f"Analyze the sentiment of this news article:\n{article_text}",
                    deps=db,
                )
                sentiment = sentiment_result.output
                print(
                    f"   Sentiment: {sentiment.sentiment} (confidence: {sentiment.confidence:.2f})"
                )
                print(f"   Reasoning: {sentiment.reasoning}")
            except Exception as e:
                print(f"   Error: {e}")

            # Topic Extraction
            print("\n🏷️  Topic Analysis:")
            try:
                topic_result = topic_agent.run_sync(
                    f"Extract topics and keywords from this news article:\n{article_text}",
                    deps=db,
                )
                topics = topic_result.output
                print(f"   Primary Topic: {topics.primary_topic}")
                print(f"   Secondary Topics: {', '.join(topics.secondary_topics)}")
                print(f"   Keywords: {', '.join(topics.keywords)}")
            except Exception as e:
                print(f"   Error: {e}")

            # Enhanced Summary
            print("\n📝 Enhanced Summary:")
            try:
                summary_result = summary_agent.run_sync(
                    f"Create an enhanced summary for this news article:\n{article_text}",
                    deps=db,
                )
                enhanced = summary_result.output
                print(f"   AI Summary: {enhanced.ai_summary}")
                print(f"   Key Points: {'; '.join(enhanced.key_points)}")
                print(f"   Importance Score: {enhanced.importance_score}/10")
            except Exception as e:
                print(f"   Error: {e}")

            print("\n" + "=" * 50 + "\n")

    except Exception as e:
        print(f"❌ Database error: {e}")
        print("Make sure the news.db file exists and contains data.")


def search_and_analyze():
    """Demonstrate searching and analyzing specific news topics."""
    print("🔍 Search and Analysis Demo")
    print("=" * 30)

    db = NewsDatabase()
    search_terms = ["Trump", "health", "technology"]

    for term in search_terms:
        print(f"🔎 Searching for articles about '{term}'...")
        articles = db.search_articles(term, limit=2)

        if articles:
            print(f"Found {len(articles)} articles:")
            for article in articles:
                print(f"  • {article.title}")

            # Analyze sentiment of the first article
            if articles:
                article_text = (
                    f"Title: {articles[0].title}\nSummary: {articles[0].summary}"
                )
                try:
                    sentiment_result = sentiment_agent.run_sync(
                        f"Analyze sentiment: {article_text}", deps=db
                    )
                    print(f"  📊 Sentiment: {sentiment_result.output.sentiment}")
                except Exception as e:
                    print(f"  ❌ Analysis error: {e}")
        else:
            print("  No articles found.")
        print()


if __name__ == "__main__":
    print("🚀 Starting Pydantic AI News Analysis Examples\n")

    # Run the analysis demos
    analyze_recent_news()
    search_and_analyze()

    print("✅ Demo completed!")
    print("\n💡 This example demonstrates:")
    print("   • Type-safe AI agents with structured outputs")
    print("   • Dependency injection with database services")
    print("   • Multiple specialized agents for different tasks")
    print("   • Error handling and real-world data integration")
