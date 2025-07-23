import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from base.agent_executor import ADKAgentExecutor

from .agent import root_agent


def main():
    skills = [
        AgentSkill(
            id="product_information",
            name="Product Information Retrieval",
            description="Retrieve detailed information about insurance products including coverage, terms, and conditions",
            tags=["insurance", "products", "information"],
            examples=[
                "What coverage does the life insurance policy provide?",
                "Tell me about the auto insurance deductible options",
                "What are the terms and conditions for the health insurance plan?"
            ]
        ),
        AgentSkill(
            id="product_comparison",
            name="Product Comparison",
            description="Compare different insurance products based on coverage, benefits, and terms",
            tags=["insurance", "comparison", "analysis"],
            examples=[
                "Compare the basic and premium auto insurance plans",
                "What's the difference between term and whole life insurance?",
                "How do the health insurance plans differ in coverage?"
            ]
        ),
        AgentSkill(
            id="coverage_analysis",
            name="Coverage Analysis",
            description="Explain what is and isn't covered under specific insurance policies",
            tags=["insurance", "coverage", "analysis"],
            examples=[
                "What does comprehensive auto insurance cover?",
                "Is dental care covered under the health insurance plan?",
                "What exclusions apply to the homeowner's insurance?"
            ]
        ),
        AgentSkill(
            id="product_recommendations",
            name="Product Recommendations",
            description="Provide product recommendations based on customer needs and requirements",
            tags=["insurance", "recommendations", "cross-selling"],
            examples=[
                "What insurance products would you recommend for a young family?",
                "Which auto insurance plan offers the best value?",
                "What additional coverage should I consider for my home insurance?"
            ]
        )
    ]

    agent_card = AgentCard(
        name="Service Expert",
        description="Insurance Service Expert providing comprehensive product information and guidance",
        url="http://service-expert:8000/",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=skills
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