# Agent card (metadata)
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from cross_selling_agent.agent import root_agent
from base.agent_executor import ADKAgentExecutor
from base.instrument_starlette_application import instrument_starlette_application


def main():
    # Define Agent Skills using A2A framework
    customer_analysis_skill = AgentSkill(
        id="analyze_customer_profile",
        name="Customer Profile Analysis",
        description="Analyze customer CRM data to identify demographics, existing policies, financial capacity, and "
        "insurance needs. Provides comprehensive customer insights for targeted recommendations. "
        "Required input is a customer ID formated as ^cust\\d{3}$",
        tags=["crm", "customer analysis", "demographics", "insurance", "profiling"],
        examples=[
            "Analyze customer with ID cust002 for cross-selling opportunities",
            "Get customer profile and existing insurance coverage for customer with ID cust001",
            "Review cust003 demographics and financial status",
            "Identify customer segment and risk profile of cust004",
        ],
    )

    customer_email_retrieval_skill = AgentSkill(
        id="get_customer_email",
        name="Customer Email Retrieval",
        description="Retrieve customer email address from CRM system. Required input is a customer ID formated as ^cust\\d{3}$.",
        tags=["crm", "email retrieval", "customer data", "insurance"],
        examples=[
            "Get email address for customer cust001",
            "Retrieve email for customer cust002",
            "Fetch email contact for customer cust003",
        ],
    )

    customer_slackID_retrieval_skill = AgentSkill(
        id="get_customer_slackID",
        name="Customer Slack ID Retrieval",
        description="Retrieve customer Slack ID from CRM system. Required input is a customer ID formated as ^cust\\d{3}$.",
        tags=["crm", "slackID retrieval", "customer data", "insurance"],
        examples=[
            "Get Slack ID for customer cust001",
            "Retrieve Slack ID for customer cust002",
            "Fetch Slack contact for customer cust003",
        ],
    )

    customer_data_retrieval_skill = AgentSkill(
        id="get_customer_crm_data",
        name="Customer CRM Data Retrieval",
        description="Retrieve comprehensive customer data from CRM system including demographics, customer email address, "
        "address, telefon number, existing policies, "
        "communication history, and risk profile. Provides a complete view of customer for analysis."
        "Required input is a customer ID formated as ^cust\\d{3}$. If you did not receive a customer ID, "
        "ask for input.",
        tags=["crm", "customer data", "retrieval", "insurance", "profiling"],
        examples=[
            "Get CRM data for customer cust001",
            "Retrieve email address for customer cust002",
            "Retrieve demographics and existing policies for cust002",
            "Fetch communication history for customer cust003",
            "Access risk profile and segment information for cust004",
        ],
    )

    product_matching_skill = AgentSkill(
        id="match_insurance_products",
        name="Insurance Product Matching",
        description="Access comprehensive insurance product catalog and match products to customer profiles. "
        "Identifies suitable products based on eligibility criteria, target segments, and customer needs."
        "When quering for an existing customer, required input is a customer ID formated as ^cust\\d{3}$",
        tags=[
            "insurance products",
            "product matching",
            "eligibility",
            "catalog",
            "recommendations",
        ],
        examples=[
            "Find suitable life insurance products for a 35-year-old family",
            "Match home insurance products for new homeowners",
            "Identify car insurance upgrades for customer cust003",
            "Recommend health insurance add-ons based on customer profile of cust005",
        ],
    )

    cross_sell_analysis_skill = AgentSkill(
        id="cross_selling_analysis",
        name="Cross-Selling Opportunity Analysis",
        description="Perform comprehensive cross-selling analysis by combining customer data with product catalog. "
        "Identifies coverage gaps, prioritizes recommendations, and provides actionable insights for sales teams."
        "Required input is a customer ID formated as ^cust\\d{3}$",
        tags=[
            "cross-selling",
            "upselling",
            "coverage gaps",
            "sales opportunities",
            "recommendations",
        ],
        examples=[
            "Analyze cross-selling opportunities for customer cust001",
            "Identify coverage gaps in existing insurance policies of cust002",
            "Prioritize product recommendations by customer value of cust003",
            "Generate cross-selling strategy for customer cust004",
        ],
    )

    # Agent Skills List
    agent_skills: list[AgentSkill] = [
        customer_analysis_skill,
        product_matching_skill,
        cross_sell_analysis_skill,
        customer_data_retrieval_skill,
        cross_sell_analysis_skill,
        customer_email_retrieval_skill,
        customer_slackID_retrieval_skill,
    ]

    agent_card = AgentCard(
        name=root_agent.name,
        description=root_agent.description,
        url="http://cross-selling-agent:8000/",
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
