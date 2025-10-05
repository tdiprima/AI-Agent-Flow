# CrewAI Stock Alert System

## Summary

This project is a simple multi-agent system built with [CrewAI](https://github.com/joaomdmoura/crewAI) that monitors stock prices, generates insights, and sends email alerts if stock price changes exceed a specified threshold (default: 5%). The system demonstrates task chaining and tool integration in an agentic workflow.

## How It Works

- **Agents**:
  - **Researcher**: Fetches the latest and previous closing prices for a list of stocks.
  - **Analyst**: Analyzes the price changes, generates insights, and triggers an email alert if any stock moves more than the threshold.

- **Task Chaining**:
  1. The Researcher agent gathers stock price data.
  2. The Analyst agent receives this data, calculates percent changes, generates insights, and checks for significant changes.
  3. If any stock changes exceed the threshold, an email alert is sent.

- **Tool Integration**:
  - Uses [yfinance](https://pypi.org/project/yfinance/) to fetch stock prices.
  - Uses Python's `smtplib` to send email alerts.

## What It's Doing

- The system starts by having the Researcher agent collect the latest and previous closing prices for a list of stocks (e.g., AAPL, GOOGL, MSFT).
- The Analyst agent receives this data, calculates the percent change for each stock, and generates human-readable insights.
- If any stock's price has changed (up or down) by more than the threshold (default 5%), the system sends an email alert summarizing the event.
- Otherwise, it simply prints the insights.

## Customization

- You can add or remove stock symbols in `config.py`.
- Adjust the `PRICE_CHANGE_THRESHOLD` to set your own alert level.
- Update email settings with your own credentials.

---

### Explanation
- **Agent**: Represents an AI entity with a role, goal, and backstory. It uses an LLM (default is GPT-4) to think and act.
- **Task**: Defines what the agent should do, including a description and expected output.
- **Crew**: Orchestrates the agents and tasks. Calling `kickoff()` runs the process.
- This is a minimal example. In real scenarios, you can add multiple agents, tools (e.g., web search), and complex task delegation.

<br>
