"""
A simple demonstration of Pydantic for structuring data (e.g., AI model outputs)
"""

import instructor
from openai import OpenAI
from pydantic import BaseModel


# Define a Pydantic model (like a schema for AI-generated data)
class Greeting(BaseModel):
    message: str  # Required field: a string (e.g., from an AI response)
    language: str = "English"  # Optional field with default value


# Simulate creating a structured "AI" response
# In a real AI app, this could come from an LLM like GPT, parsed into the model
hello = Greeting(message="Hello, World!")

# Print the validated data
print(hello.message)  # Output: Hello, World!
print(hello.model_dump())

# Integrate with an actual AI model
client = instructor.from_openai(OpenAI())
ai_response = client.messages.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Greet the world"}],
    response_model=Greeting,
)
print(ai_response.message)
