import os

from autogen import AssistantAgent, UserProxyAgent

config_list = [{"model": "gpt-4o", "api_key": os.getenv("OPENAI_API_KEY")}]

code_gen_agent = AssistantAgent(
    name="CodeGenAgent",
    system_message="Generate Python code for sorting algorithms. Respond only with code and brief explanations.",
    llm_config={"config_list": config_list},
)

tester_agent = AssistantAgent(
    name="TesterAgent",
    system_message="Test the given Python sorting code. Write test cases, run them, and critique the code. Suggest improvements if needed.",
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="Orchestrator",
    system_message="You are orchestrating a conversation between CodeGenAgent and TesterAgent.",
    code_execution_config={"use_docker": False},
    human_input_mode="NEVER",
)

task_prompt = (
    "CodeGenAgent, please write Python code for the quicksort sorting algorithm. "
    "TesterAgent, please test the code, critique it, and suggest improvements. "
    "Repeat until the code passes all tests."
)

user_proxy.initiate_chat(
    agent=code_gen_agent, message=task_prompt, recipient=tester_agent, max_turns=5
)
