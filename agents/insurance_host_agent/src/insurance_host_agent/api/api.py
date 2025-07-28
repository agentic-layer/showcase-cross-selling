from base.openai_api.openai_api import create_openai_api
from insurance_host_agent.agent import root_agent

api = create_openai_api(agent=root_agent)