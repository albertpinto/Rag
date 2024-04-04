import os
import autogen

# Define configuration list for autogen models
config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv("OPENAI_API_KEY")
    }
]

# Configure settings for the autogen language model
llm_config = {
    "seed": 42,  # Setting a seed for reproducibility
    "config_list": config_list,
    "temperature": 0  # Disabling randomness in generation
}

# Initialize user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "/home/albert/Documents/work_dir"},
    llm_config=llm_config,
    system_message="""
    Reply TERMINATE if the task has been solved to full satisfaction. 
    Otherwise, reply CONTINUE, or provide a reason why the task is not yet solved."""
)

# Initialize assistant agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You should generate code and store it in a file as mentioned in the {code_execution_config}"
)



# Define the task to be performed
task = """
Run this end point http://localhost:8003/prompt/Where%20did%20asif%20study%20%3F
and print the results in a file.
"""

# Initiate chat with the assistant
user_proxy.initiate_chat(
    assistant,
    message=task,
)


# Define the task to be performed
task = """
Write a Python code that adds odd numbers from 1 to 1000 and prints out the result. 
After that, save the Python code in a file.
"""

# Initiate chat with the assistant
user_proxy.initiate_chat(
    assistant,
    message=task,
)
# Define the task to be performed
task = """
Give me the stock price of Nvidia and Microsoft today and store it in a file.
"""

# Initiate chat with the assistant
user_proxy.initiate_chat(
    assistant,
    message=task,
)

# Define the task to be performed
task = """
Summarize the contents of the URL https://arxiv.org/pdf/2403.15388.pdf in a text file.
"""

# Initiate chat with the assistant
user_proxy.initiate_chat(
    assistant,
    message=task,
)

