# Pydantic AI News Analysis Example

This example demonstrates how to use **Pydantic AI** to create intelligent, type-safe AI agents for analyzing news articles with structured outputs.

### Note!
It relies on `news.db`, created from the "type-safe news agent" example.

## What is Pydantic AI?

[Pydantic AI](https://ai.pydantic.dev/) is a Python agent framework designed to simplify building production-grade generative AI applications. It brings the "FastAPI feeling" to GenAI development with:

### Key Features:
- **Type Safety**: Full type checking and validation for AI inputs and outputs
- **Model Agnostic**: Support for OpenAI, Anthropic, Google, and other AI models  
- **Structured Responses**: Automatic validation of AI outputs using Pydantic models
- **Dependency Injection**: Clean architecture for managing services and dependencies
- **Agent Tools**: Define custom tools that agents can use during conversations
- **Streaming Support**: Handle real-time AI responses efficiently

### Why Pydantic AI?
- **Reliability**: Structured outputs prevent unpredictable AI responses
- **Developer Experience**: Familiar Pydantic syntax with excellent IDE support
- **Production Ready**: Built-in error handling, retries, and debugging support
- **Maintainable**: Clear separation of concerns and testable components

## This Example: News Analysis Agents

Our example creates three specialized AI agents that analyze news articles from the main project's SQLite database:

### 1. **Sentiment Analysis Agent** (`NewsSentiment`)
Analyzes the emotional tone of news articles with structured output:

```python
class NewsSentiment(BaseModel):
    sentiment: str = Field(description="positive, negative, or neutral")
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(description="Brief explanation")
```

### 2. **Topic Extraction Agent** (`NewsTopics`)  
Identifies main themes and keywords from articles:

```python
class NewsTopics(BaseModel):
    primary_topic: str
    secondary_topics: List[str] = Field(max_items=3)
    keywords: List[str] = Field(max_items=5)
```

### 3. **Summary Enhancement Agent** (`NewsSummary`)
Creates improved summaries with importance scoring:

```python
class NewsSummary(BaseModel):
    ai_summary: str = Field(description="Concise AI-generated summary")
    key_points: List[str] = Field(max_items=3)
    importance_score: int = Field(ge=1, le=10)
```

## How the Code Works

### 1. **Agent Creation with Dependencies**

```python
sentiment_agent = Agent[NewsDatabase, NewsSentiment](
    'openai:gpt-4o-mini',           # AI model to use
    deps_type=NewsDatabase,          # Dependency injection type
    output_type=NewsSentiment,       # Structured output type
    system_prompt="You are a news sentiment analyzer..."
)
```

### 2. **Dependency Injection**
The `NewsDatabase` class provides data access methods that agents can use:

```python
class NewsDatabase:
    def get_recent_articles(self, limit: int = 5) -> List[NewsArticle]:
        # Fetch articles from SQLite database
        
    def search_articles(self, keyword: str) -> List[NewsArticle]:
        # Search articles by keyword
```

### 3. **Agent Tools** 
Tools give agents access to external functionality:

```python
@sentiment_agent.tool
def analyze_article_sentiment(ctx: RunContext[NewsDatabase], article_text: str) -> str:
    return f"Analyzing sentiment for: {article_text}"
```

### 4. **Type-Safe Execution**
Running agents returns validated, structured data:

```python
sentiment_result = sentiment_agent.run_sync(
    "Analyze the sentiment of this article: ...",
    deps=NewsDatabase()
)
# sentiment_result.output is guaranteed to be a NewsSentiment object
print(f"Sentiment: {sentiment_result.output.sentiment}")
```

## Key Benefits Demonstrated

### ✅ **Type Safety**
- All AI outputs are validated against Pydantic models
- IDE autocomplete and type checking work perfectly
- Runtime validation prevents invalid data

### ✅ **Structured Responses**
- No more parsing raw text from AI models
- Consistent, predictable output formats
- Automatic validation of constraints (e.g., confidence scores 0-1)

### ✅ **Clean Architecture**
- Separation of data access (`NewsDatabase`) from AI logic
- Reusable agents for different analysis tasks
- Dependency injection makes testing easier

### ✅ **Error Handling**
- Built-in retries and error recovery
- Graceful handling of model failures
- Clear error messages for debugging

## Running the Example

### Prerequisites
1. Make sure you've run the main news scraper to populate `news.db`
2. Set your OpenAI API key: `export OPENAI_API_KEY="your-key-here"`

### Installation

```bash
pip install -r requirements.txt
```

### Run the Analysis

```bash
python news_analyzer.py
```

## Comparison: Traditional AI vs Pydantic AI

### Traditional Approach ❌

```python
# Unpredictable, unstructured output
response = openai.chat.completions.create(
    messages=[{"role": "user", "content": "Analyze sentiment..."}]
)
# Raw text that needs parsing
sentiment_text = response.choices[0].message.content
# Manual parsing, error-prone
if "positive" in sentiment_text.lower():
    sentiment = "positive"
# No validation, no type safety
```

### Pydantic AI Approach ✅  

```python
# Structured, validated output
result = sentiment_agent.run_sync("Analyze sentiment...")
# Guaranteed structure with type checking
sentiment: NewsSentiment = result.output
print(f"Sentiment: {sentiment.sentiment}")  # Always valid
print(f"Confidence: {sentiment.confidence}")  # Always 0.0-1.0
```

## Use Cases

This pattern is perfect for:

- 📊 **Content Analysis**: Sentiment, topics, classification
- 📰 **News Processing**: Summarization, fact-checking, categorization  
- 🛒 **E-commerce**: Product descriptions, reviews, recommendations
- 📧 **Customer Support**: Ticket routing, response generation
- 🔍 **Research**: Data extraction, literature reviews, insights

The combination of type safety, structured outputs, and clean architecture makes Pydantic AI ideal for production AI applications where reliability and maintainability matter.

---

**Next Steps**: Try modifying the agents to analyze different aspects of news articles, or create new agents for different AI tasks!

<br>
