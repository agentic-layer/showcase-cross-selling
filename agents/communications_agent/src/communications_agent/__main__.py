# Agent card (metadata)
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from base.agent_executor import ADKAgentExecutor
from base.instrument_starlette_application import instrument_starlette_application
from communications_agent.agent import root_agent


def main():
    # Define Agent Skills using A2A framework

    text_draft_skill = AgentSkill(
        id="draft_text",
        name="Text Drafting",
        description="Draft text messages based on user input. Supports various formats including plain text, markdown, "
        "and HTML. Automatically formats messages for different platforms.",
        tags=["text", "drafting", "communication", "messaging", "formatting"],
        examples=[
            "Draft a message for the cross selling strategy for the customer",
        ],
    )

    email_skill = AgentSkill(
        id="send_email",
        name="Email Communication",
        description="Send professional emails to specified recipients with subject and body content. Supports custom "
        "sender addresses and includes input validation.",
        tags=["email", "communication", "messaging", "notifications", "smtp"],
        examples=[
            "Send an email to john@example.com",
        ],
    )

    slack_skill = AgentSkill(
        id="send_slack_message",
        name="Slack Messaging",
        description="Send messages to Slack channels or direct messages using webhook integration. Supports public channels, private channels, and direct messages with automatic formatting.",
        tags=["slack", "messaging", "team communication", "webhooks", "collaboration"],
        examples=[
            "Post a message to #general channel about deployment",
            "Send a direct message to @sarah about the project",
            "Notify #alerts channel about system status",
            "Share update in #development channel",
        ],
    )

    # Agent Skills List
    agent_skills: list[AgentSkill] = [text_draft_skill, email_skill, slack_skill]

    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        url="http://communications-agent:8000/",
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
    app = server.build()
    instrument_starlette_application(app)
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
