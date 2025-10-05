# LangGraph Branching Agent

This project demonstrates a branching agent workflow using [LangGraph](https://github.com/langchain-ai/langgraph). The agent receives an input, routes it to the appropriate node (research, analysis, or escalation) based on its complexity or urgency, and visualizes the workflow for debugging.

## 📈 What Does It Do?

- Accepts a user input (e.g., a query or task description)
- Decides which node to route the input to:
    - **Research**: For simple or general requests
    - **Analysis**: For more complex, long, or analytical tasks
    - **Escalation**: For urgent or error-related issues
- Executes the corresponding node logic
- Returns a summary result
- Generates a workflow visualization (`workflow_graph.mmd`) to help debug the branching logic

## 🛠️ How Does the Code Work?

### 1. **Node Functions**
- Each node (`research_node`, `analysis_node`, `escalation_node`) is a Python function that performs a specific action and updates the workflow state.

### 2. **Decision Router**
- The `decision_router` function inspects the input and chooses which node should handle it, based on simple rules:
    - If the input mentions "urgent" or "error", it escalates.
    - If the input is long (more than 12 words), it goes to analysis.
    - Otherwise, it defaults to research.

### 3. **Graph Construction**
- Nodes are added to the LangGraph `Graph`.
- The router node is connected to each task node via conditional edges, which are triggered based on the router’s decision.
- Entry point is set to the router; exits are set on all task nodes.

### 4. **Visualization**
- The workflow graph is visualized and saved as `workflow_graph.png` for easy debugging and understanding of the branching logic.

### 5. **Running the Agent**
- The script runs three sample inputs, showing how each is routed and handled, and prints the final results.

## 🧩 Customizing

- You can expand the decision logic in `decision_router` for more sophisticated routing.
- Add more nodes for additional tasks or actions.
- Integrate with LLMs or APIs for richer node behaviors.

---

### Explanation
- **State**: A TypedDict defining what data flows through the graph (here, just a `message` string).
- **Node**: A function (`hello_node`) that processes the state. In a real app, this could call an LLM, but here it's simple.
- **Edges**: Define the flow (from start to node to end).
- **Compilation and Invocation**: Turns the graph into an executable app, which you can run with `.invoke()`.

[LangGraph documentation](https://langchain-ai.github.io/langgraph/)

<br>
