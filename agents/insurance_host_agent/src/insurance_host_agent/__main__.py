# Agent card (metadata)
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from agent import root_agent

from base.agent_executor import ADKAgentExecutor


def main():
    # Define Agent Skills using A2A framework
    orchestration_skill = AgentSkill(
        id="orchestrate_customer_support",
        name="Customer Support Orchestration",
        description="Orchestrate customer support requests by coordinating with specialized agents (cross-selling and communications agents). Acts as the central hub for routing tasks to appropriate agents based on customer needs.",
        tags=["orchestration", "customer support", "agent coordination", "task routing", "insurance"],
        examples=[
            "Help customer with insurance inquiry and identify cross-selling opportunities",
            "Coordinate between cross-selling analysis and customer communications",
            "Route customer support request to appropriate specialized agent",
            "Manage multi-step customer service workflows",
        ],
    )

    delegation_skill = AgentSkill(
        id="delegate_to_specialists",
        name="Specialist Agent Delegation",
        description="Delegate specific tasks to specialized agents including cross-selling analysis and customer communications. Ensures proper task routing and coordination between different agent capabilities.",
        tags=["delegation", "task routing", "agent communication", "workflow management", "specialization"],
        examples=[
            "Send customer profile to cross-selling agent for analysis",
            "Request communications agent to draft customer email",
            "Coordinate between multiple agents for complex customer needs",
            "Manage task handoffs between specialized agents",
        ],
    )

    customer_service_skill = AgentSkill(
        id="customer_service_support",
        name="Insurance Customer Service",
        description="Provide comprehensive customer service support for insurance-related inquiries. Handles customer interactions in German and ensures professional, helpful responses while identifying opportunities for additional services.",
        tags=["customer service", "insurance", "german language", "support", "professional communication"],
        examples=[
            "Respond to customer insurance policy questions",
            "Provide support for insurance claims and coverage",
            "Handle customer complaints and service requests",
            "Identify opportunities for policy upgrades or additional coverage",
        ],
    )

    # Agent Skills List
    agent_skills: list[AgentSkill] = [orchestration_skill, delegation_skill, customer_service_skill]

    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        url="http://insurance-host-agent:10001/",
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        skills=agent_skills,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ADKAgentExecutor(
            agent=root_agent,
        ),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)

    uvicorn.run(server.build(), host="0.0.0.0")


if __name__ == "__main__":
    main()
