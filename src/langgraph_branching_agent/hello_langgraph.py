"""
A simple example of using LangGraph to create a friendly greeting for a user.
"""

from typing import TypedDict  # For defining the state schema

from langgraph.graph import END, START, StateGraph  # Core LangGraph components


# Define the state schema (a simple dict with one key: 'message')
class State(TypedDict):
    message: str


# Define a node (a function that takes the current state and returns an updated state)
def hello_node(state: State) -> State:
    # Update the state with our hello message
    return {"message": "Hello, World!"}


# Create the graph builder
graph_builder = StateGraph(State)

# Add the node to the graph
graph_builder.add_node(
    "hello", hello_node
)  # Node key is "hello", function is hello_node

# Add edges: START -> hello -> END
graph_builder.add_edge(START, "hello")  # Start from the beginning
graph_builder.add_edge("hello", END)  # End after the node

# Compile the graph into a runnable app
app = graph_builder.compile()

# Invoke the app with an initial empty state
result = app.invoke({"message": ""})  # Input is the initial state

# Print the final state
print(result["message"])
