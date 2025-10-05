from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools

# Create an agent using OpenAI's GPT-4o
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions="Provide concise answers in markdown format.",
    markdown=True,
)

# Example query
response = agent.print_response(
    "Hello, world! What's the capital of Peru?", stream=True, show_full_reasoning=True
)

# For Grok, replace OpenAIChat with:
# from agno.models.xai import Grok
# agent = Agent(
#     model=Grok(id="grok-3"),
#     tools=[ReasoningTools(add_instructions=True)],
#     instructions="Provide concise answers in markdown format.",
#     markdown=True,
# )
