"""
A simple example of using Pydantic AI to create a friendly greeting for a user.
Adapted from: https://ai.pydantic.dev/#hello-world-example
"""

from pydantic_ai import Agent

agent = Agent(
    # 'openai:gpt-4o-mini',
    "grok:grok-4",
    system_prompt="Be concise, reply with one sentence.",
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
# The first known use of "hello, world" was in a 1974 textbook about the C programming language.
