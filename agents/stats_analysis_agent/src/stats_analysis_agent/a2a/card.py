from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from stats_analysis_agent.agent import root_agent

cancellation_or_non_renewal_pattern_skill = AgentSkill(
    id="analyze_cancelation_patterns",
    name="Cancelation Analysis",
    description="Analyze customer CRM data to identify if there are certain patterns associated with cancellation"
                "of the insurance contract or non-renewal. Possible causes could be a lack of communication or major"
                "personal events such as loss of family members, jobloss, etc.",
    tags=["insurance", "cancelation", "risk management"],
    examples=[
        "Identify possible risk factors that lead to customers cancelling or abstaining from renewing their contracts."
        "Identify customers which might be at risk of soon cancelling existing contracts"
        "Develop strategies to prevent customers from potentially cancelling their contracts."
    ],
)

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

customer_segmentation_skill = AgentSkill(
    id="analyze_customer_segments",
    name="Customer Segmentation Analysis",
    description="Analyzes the entire customer base to identify key segments based on demographics,"
                "risk profiles, or income levels. Helps to understand the current customer structure"
                "and identify potential growth opportunities in underserved segments.",
    tags=["segmentation", "customer analysis", "demographics", "business intelligence", "growth"],
    examples=[
        "What is the main customer segment we are currently serving?",
        "Show the distribution of customers by risk profile.",
        "Identify growth opportunities in the low-income sector.",
        "Analyze the demographics of our current customer base.",
    ],
)

customer_behavior_analysis_skill = AgentSkill(
    id="analyze_customer_behavior",
    name="Customer Behavior Analysis",
    description="Analyzes correlations between customer characteristics (like age, income, family status) "
                "and their insurance purchasing behavior. Identifies which types of customers tend to buy specific types of insurance.",
    tags=["behavior analysis", "correlation", "customer profiling", "insurance", "sales strategy"],
    examples=[
        "What kind of insurance do high-income customers usually buy?",
        "Do parents prefer life insurance?",
        "Analyze the impact of home ownership on policy selection.",
        "Which personal traits influence the choice of insurance?",
    ],
)

product_popularity_skill = AgentSkill(
    id="analyze_product_popularity",
    name="Product Popularity Analysis",
    description="Evaluates the popularity of all insurance products by analyzing how frequently "
                "they are purchased across the entire customer base. Ranks products from most to least popular.",
    tags=["product analysis", "popularity", "ranking", "business intelligence", "sales"],
    examples=[
        "Which insurance products are the most popular?",
        "Rank our products by number of active policies.",
        "Are there any unpopular products we should review?",
        "Show me a list of the top 5 insurance products.",
    ],
)

ltv_analysis_skill = AgentSkill(
    id="analyze_ltv_drivers",
    name="Lifetime Value (LTV) Analysis",
    description="Identifies and analyzes the key personal and behavioral characteristics of customers that "
                "correlate with a high Customer Lifetime Value (LTV). Helps to understand what drives long-term customer value.",
    tags=["ltv", "customer value", "financial analysis", "business intelligence", "profiling"],
    examples=[
        "Which customer characteristics correlate with a high LTV?",
        "Analyze the LTV of different customer segments.",
        "What are the main drivers for customer lifetime value?",
        "Do homeowners have a higher LTV?",
    ],
)

product_bundle_analysis_skill = AgentSkill(
    id="analyze_product_bundles",
    name="Product Bundle Analysis",
    description="Analyzes customer portfolios to identify which insurance products are typically purchased together as a 'bundle'. "
                "Useful for creating marketing campaigns and cross-selling strategies.",
    tags=["product bundle", "cross-selling", "portfolio analysis", "marketing", "strategy"],
    examples=[
        "Which insurances are often bought together?",
        "Identify common product bundles.",
        "Is there a typical 'family package' of insurances?",
        "Analyze product combinations in customer portfolios.",
    ],
)

geographic_analysis_skill = AgentSkill(
    id="analyze_geographic_patterns",
    name="Geographic Pattern Analysis",
    description="Analyzes customer data to find correlations between their geographic location (city/region) "
                "and their insurance choices or risk profiles. Identifies regional trends and patterns.",
    tags=["geographic analysis", "location", "regional trends", "risk profiling", "market analysis"],
    examples=[
        "Are there correlations between location and insurance products?",
        "Analyze the risk profiles by city.",
        "Is car insurance more popular in urban areas?",
        "Show regional differences in customer risk profiles.",
    ],
)

risk_profile_analysis_skill = AgentSkill(
    id="analyze_risk_profile_traits",
    name="Risk Profile Trait Analysis",
    description="Identifies the common characteristics and demographics of customers within a specific risk segment, "
                "such as 'high-risk'. Helps in understanding and managing risk across the customer base.",
    tags=["risk analysis", "risk management", "customer profiling", "segmentation"],
    examples=[
        "What are the common traits of our high-risk customers?",
        "Analyze the demographics of the low-risk segment.",
        "Which factors define a high-risk customer profile?",
    ],
)

anchor_product_analysis_skill = AgentSkill(
    id="analyze_anchor_products",
    name="Anchor Product Analysis",
    description="Analyzes the purchasing history of new customers to identify the 'anchor product' - the first insurance policy they"
                "typically buy. This insight is valuable for customer acquisition strategies.",
    tags=["anchor product", "customer acquisition", "sales funnel", "marketing", "product analysis"],
    examples=[
        "What is the most common first product for new customers?",
        "Identify our anchor products.",
        "Which insurance serves as the entry point for most clients?",
    ],
)

# Agent Skills List
agent_skills: list[AgentSkill] = [cancellation_or_non_renewal_pattern_skill,
                                  customer_analysis_skill,
                                  customer_segmentation_skill,
                                  customer_behavior_analysis_skill,
                                  product_popularity_skill,
                                  ltv_analysis_skill,
                                  product_bundle_analysis_skill,
                                  geographic_analysis_skill,
                                  risk_profile_analysis_skill,
                                  anchor_product_analysis_skill]

agent_card = AgentCard(
    name=root_agent.name,
    description=root_agent.description,
    url="http://stats-analysis-agent:8000/a2a/",
    version="1.0.0",
    defaultInputModes=["text", "text/plain"],
    defaultOutputModes=["text", "text/plain"],
    capabilities=AgentCapabilities(streaming=True),
    skills=agent_skills,
)