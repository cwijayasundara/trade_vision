import json
from autogenstudio import AgentWorkFlowConfig, AutoGenWorkFlowManager

from dotenv import load_dotenv

load_dotenv()
# load an agent specification in JSON
agent_spec = json.load(open('agent_spec.json'))

# Create a AutoGen Workflow Configuration from the agent specification
agent_work_flow_config = AgentWorkFlowConfig(**agent_spec)

agent_work_flow = AutoGenWorkFlowManager(agent_work_flow_config)


# # Run the workflow on a task
def execute_autogen_studio(task):
    agent_work_flow.run(message=task)
    return agent_work_flow.agent_history
