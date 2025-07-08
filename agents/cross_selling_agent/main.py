# Agent card (metadata)
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from base.agent_executor import ADKAgentExecutor
from src import root_agent


def main():
    # Define Agent Skills using A2A framework
    customer_analysis_skill = AgentSkill(
        id='analyze_customer_profile',
        name='Customer Profile Analysis',
        description='Analyze customer CRM data to identify demographics, existing policies, financial capacity, and insurance needs. Provides comprehensive customer insights for targeted recommendations.',
        tags=['crm', 'customer analysis', 'demographics', 'insurance', 'profiling'],
        examples=[
            'Analyze customer ID 12345 for cross-selling opportunities',
            'Get customer profile and existing insurance coverage',
            'Review customer demographics and financial status',
            'Identify customer segment and risk profile'
        ]
    )

    product_matching_skill = AgentSkill(
        id='match_insurance_products',
        name='Insurance Product Matching',
        description='Access comprehensive insurance product catalog and match products to customer profiles. Identifies suitable products based on eligibility criteria, target segments, and customer needs.',
        tags=['insurance products', 'product matching', 'eligibility', 'catalog', 'recommendations'],
        examples=[
            'Find suitable life insurance products for a 35-year-old family',
            'Match home insurance products for new homeowners',
            'Identify car insurance upgrades for existing customers',
            'Recommend health insurance add-ons based on customer profile'
        ]
    )

    cross_sell_analysis_skill = AgentSkill(
        id='cross_selling_analysis',
        name='Cross-Selling Opportunity Analysis',
        description='Perform comprehensive cross-selling analysis by combining customer data with product catalog. Identifies coverage gaps, prioritizes recommendations, and provides actionable insights for sales teams.',
        tags=['cross-selling', 'upselling', 'coverage gaps', 'sales opportunities', 'recommendations'],
        examples=[
            'Analyze cross-selling opportunities for customer portfolio',
            'Identify coverage gaps in existing insurance policies',
            'Prioritize product recommendations by customer value',
            'Generate cross-selling strategy for high-value customers'
        ]
    )

    # Agent Skills List
    agent_skills: list[AgentSkill] = [
        customer_analysis_skill,
        product_matching_skill,
        cross_sell_analysis_skill
    ]

    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        url="http://cross-selling-agent:10003/",
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

    uvicorn.run(server.build(), host="0.0.0.0", port=10003)


if __name__ == "__main__":
    main()
