from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from base.a2a.agent_executor import A2AAgentExecutor

from stats_analysis_agent.a2a.card import agent_card
from stats_analysis_agent.agent import root_agent

request_handler = DefaultRequestHandler(
    agent_executor=A2AAgentExecutor(
        agent=root_agent,
    ),
    task_store=InMemoryTaskStore(),
)

a2a_app = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
