import json
from autogenstudio import AgentWorkFlowConfig, AutoGenWorkFlowManager
from dotenv import load_dotenv

load_dotenv()
# load an agent specification in JSON
agent_spec = json.load(open('agent_spec.json'))

# Create a An AutoGen Workflow Configuration from the agent specification
agent_work_flow_config = AgentWorkFlowConfig(**agent_spec)

agent_work_flow = AutoGenWorkFlowManager(agent_work_flow_config)

# # Run the workflow on a task
task_query = "Draw a graph to show Tesla stock price movement for the past 4 years?"
agent_work_flow.run(message=task_query)

print(agent_work_flow.agent_history)

