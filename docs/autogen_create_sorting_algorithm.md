`create_sorting_algorithm.py`

Here's a step-by-step guide to set up two agents in [AutoGen](https://microsoft.github.io/autogen/stable//index.html) (by Microsoft) for your scenario: one agent to generate Python code for a sorting algorithm (e.g., quicksort), and another agent to test and critique it. This simulates a mini dev team, with a conversation loop where the code is generated, tested, and improved.

### Assumptions

- You have installed `pyautogen` (`pip install pyautogen`)
- You have OpenAI API access (or similar LLM backend)

## 1. Basic AutoGen Setup

```python
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load your OpenAI API config (or other LLM config)
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.getenv("OPENAI_API_KEY")
    }
]
```

## 2. Define the Agents

### Agent 1: code\_gen_agent
This agent generates Python code for a sorting algorithm.

### Agent 2: tester\_agent
This agent tests the code, critiques it, and suggests improvements.

```python
# Code generator agent
code_gen_agent = AssistantAgent(
    name="CodeGenAgent",
    system_message="You are a Python developer. Generate Python code for sorting algorithms as requested. Respond only with code and brief explanations.",
    llm_config={"config_list": config_list}
)

# Tester agent
tester_agent = AssistantAgent(
    name="TesterAgent",
    system_message=(
        "You are a code reviewer and tester. "
        "Given a Python sorting algorithm, write test cases, run them, and critique the code. "
        "Suggest improvements if needed."
    ),
    llm_config={"config_list": config_list}
)
```

## 3. Conversation Loop

You can use `UserProxyAgent` to orchestrate the conversation. Here's a simple loop:

```python
# Orchestrator agent (acts as the user, initiates the task)
user_proxy = UserProxyAgent(
    name="Orchestrator",
    system_message="You are orchestrating a conversation between CodeGenAgent (code generation) and TesterAgent (code testing)."
)

# The task prompt
task_prompt = (
    "CodeGenAgent, please write Python code for the quicksort sorting algorithm. "
    "TesterAgent, please test the code, critique it, and suggest improvements. "
    "Repeat until the code passes all tests."
)

# Start the conversation loop
user_proxy.initiate_chat(
    agent=code_gen_agent,
    message=task_prompt,
    recipient= tester_agent,
    max_turns=5  # you can adjust this
)
```

### Note

- The conversation will go: Orchestrator → CodeGenAgent → TesterAgent → CodeGenAgent (if improvements needed), etc.
- You can adjust `max_turns` to control how many back-and-forths happen.

## 4. Example Output

- **CodeGenAgent**: Writes quicksort code.
- **TesterAgent**: Writes test cases, runs them, finds bugs or edge cases, and suggests fixes.
- If issues are found, the conversation continues with improvements.

## 5. Tips

- You can further customize the agents' system messages for more sophistication.
- For more advanced loops, you can use [GroupChat](https://github.com/microsoft/autogen/blob/main/notebook/groupchat.ipynb) in AutoGen.
- You can extend this to more agents (e.g., a documentation agent).

<br>
