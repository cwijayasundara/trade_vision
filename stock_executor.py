import autogen

from autogen import AssistantAgent, UserProxyAgent

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-0125-preview"],
    },
)

print(config_list)

# Create assistant agent
assistant = AssistantAgent(name="assistant",
                           llm_config={"config_list": config_list})

# Create user proxy agent
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding",
                           "use_docker": False})


def execute_stock_price_analyser(message):
    user_proxy.initiate_chat(assistant, message=message)


request = "Draw a graph to show Tesla stock price movement for the past 4 years?"
execute_stock_price_analyser(request)
