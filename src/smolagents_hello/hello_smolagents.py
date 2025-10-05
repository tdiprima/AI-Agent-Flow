import os

from smolagents import CodeAgent, OpenAIServerModel, WebSearchTool

# Configure OpenAI model (replace with your API key)
model = OpenAIServerModel(
    model_id="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY")
)

# Create a CodeAgent with WebSearchTool
agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=True)

# Run the agent
agent.run("Hello, world! What's the capital of Morocco?")

# For Grok (xAI), use InferenceClientModel:
# from smolagents import InferenceClientModel
# model = InferenceClientModel(model_id="grok-3", provider="xai")
# agent = CodeAgent(tools=[WebSearchTool()], model=model, stream_outputs=True)
# agent.run("Hello, world! What's the capital of Morocco?")
