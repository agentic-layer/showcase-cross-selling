# Agent card (metadata)
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from agent import root_agent
from agent_executor import ADKAgentExecutor

def main():
    # Define Agent Skills using A2A framework
    email_skill = AgentSkill(
        id='send_email',
        name='Email Communication',
        description='Send professional emails to specified recipients with subject and body content. Supports custom sender addresses and includes input validation.',
        tags=['email', 'communication', 'messaging', 'notifications', 'smtp'],
        examples=[
            'Send an email to john@example.com about the meeting tomorrow',
            'Email the team about project updates',
            'Send a reminder email to all stakeholders',
            'Forward important information via email'
        ]
    )

    slack_skill = AgentSkill(
        id='send_slack_message',
        name='Slack Messaging',
        description='Send messages to Slack channels or direct messages using webhook integration. Supports public channels, private channels, and direct messages with automatic formatting.',
        tags=['slack', 'messaging', 'team communication', 'webhooks', 'collaboration'],
        examples=[
            'Post a message to #general channel about deployment',
            'Send a direct message to @sarah about the project',
            'Notify #alerts channel about system status',
            'Share update in #development channel'
        ]
    )

    # Agent Skills List
    agent_skills: list[AgentSkill] = [
        email_skill,
        slack_skill
    ]

    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        url="http://communications-agent:10002/",
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

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=10002)


if __name__ == "__main__":
    main()
