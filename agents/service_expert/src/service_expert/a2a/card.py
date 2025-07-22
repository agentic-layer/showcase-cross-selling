from a2a.types import AgentCapabilities, AgentCard, AgentSkill

product_information: AgentSkill = AgentSkill(
    id="product_information",
    name="Product Information Retrieval",
    description="Retrieve detailed information about insurance products including coverage, terms, and conditions",
    tags=["insurance", "products", "information"],
    examples=[
        "What coverage does the life insurance policy provide?",
        "Tell me about the auto insurance deductible options",
        "What are the terms and conditions for the health insurance plan?",
    ],
)
product_comparison: AgentSkill = AgentSkill(
    id="product_comparison",
    name="Product Comparison",
    description="Compare different insurance products based on coverage, benefits, and terms",
    tags=["insurance", "comparison", "analysis"],
    examples=[
        "Compare the basic and premium auto insurance plans",
        "What's the difference between term and whole life insurance?",
        "How do the health insurance plans differ in coverage?",
    ],
)
coverage_analysis: AgentSkill = AgentSkill(
    id="coverage_analysis",
    name="Coverage Analysis",
    description="Explain what is and isn't covered under specific insurance policies",
    tags=["insurance", "coverage", "analysis"],
    examples=[
        "What does comprehensive auto insurance cover?",
        "Is dental care covered under the health insurance plan?",
        "What exclusions apply to the homeowner's insurance?",
    ],
)
product_recommendations: AgentSkill = AgentSkill(
    id="product_recommendations",
    name="Product Recommendations",
    description="Provide product recommendations based on customer needs and requirements",
    tags=["insurance", "recommendations", "cross-selling"],
    examples=[
        "What insurance products would you recommend for a young family?",
        "Which auto insurance plan offers the best value?",
        "What additional coverage should I consider for my home insurance?",
    ],
)

# Agent Skills List
agent_skills: list[AgentSkill] = [product_information, product_comparison, coverage_analysis, product_recommendations]

agent_card = AgentCard(
    name="Service Expert",
    description="Insurance Service Expert providing comprehensive product information and guidance",
    url="http://service-expert:8000/a2a/",
    defaultInputModes=["text", "text/plain"],
    defaultOutputModes=["text", "text/plain"],
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    skills=agent_skills,
)
