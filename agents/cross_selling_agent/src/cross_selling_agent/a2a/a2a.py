from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from base.instrument_starlette_application import instrument_starlette_application
from cross_selling_agent.a2a.card import agent_card
from base.a2a.agent_executor import A2AAgentExecutor
from cross_selling_agent.agent import root_agent


request_handler = DefaultRequestHandler(
    agent_executor=A2AAgentExecutor(
        agent=root_agent,
    ),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
a2a_app = server.build()
instrument_starlette_application(a2a_app)