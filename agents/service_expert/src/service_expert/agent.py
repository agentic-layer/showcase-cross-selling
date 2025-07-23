import os
from google.adk import agents
from google.adk.context import ToolContext


class ServiceExpertAgent:
    def __init__(self):
        self.model_name = "gemini-2.0-flash-exp"
        self.insurance_products_mcp_url = os.getenv("INSURANCE_PRODUCTS_MCP_URL", "http://insurance-products:8000")
        
        # Initialize the agent
        self.agent = agents.Agent(
            instructions=self._get_instructions(),
            model=self.model_name,
            tools=[
                self._query_insurance_products,
                self._compare_products,
                self._analyze_coverage,
            ]
        )
    
    def _get_instructions(self) -> str:
        return """
You are the Service Expert Agent, an authoritative source for insurance product information within the cross-selling ecosystem.

Your role is to:
1. Provide detailed, accurate, and up-to-date information about available insurance products
2. Explain coverage options, terms, and conditions in clear, understandable language
3. Compare different insurance products based on coverage, benefits, and terms
4. Support cross-selling initiatives by recommending suitable products
5. Ensure all information provided complies with insurance regulations

Key guidelines:
- Always access current product information through the insurance products MCP server
- Explain complex insurance terms in simple, customer-friendly language
- Focus on facts and avoid making sales pitches
- Highlight important coverage limitations and exclusions
- Provide balanced comparisons that help customers make informed decisions
- Do NOT access or reference customer personal data - focus solely on product information
- Ensure compliance with insurance regulations and disclosure requirements

When asked about products:
1. Query the insurance products database for current information
2. Present information clearly and comprehensively
3. Explain any technical terms or conditions
4. Highlight key benefits and limitations
5. Suggest complementary products when appropriate for cross-selling

Remember: You are an expert advisor helping customers understand their insurance options, not a sales agent.
"""

    async def _query_insurance_products(self, query: str, product_type: str = None) -> str:
        """Query the insurance products MCP server for product information.
        
        Args:
            query: The specific information to retrieve
            product_type: Optional filter for product type (auto, life, health, home, etc.)
        """
        # In a real implementation, this would make an HTTP request to the MCP server
        # For now, returning a placeholder that indicates the MCP integration point
        return f"[MCP Query] Retrieving insurance product information for: {query}" + (f" (filtered by: {product_type})" if product_type else "")

    async def _compare_products(self, product1: str, product2: str, comparison_criteria: str = None) -> str:
        """Compare two insurance products based on specified criteria.
        
        Args:
            product1: First product to compare
            product2: Second product to compare  
            comparison_criteria: Specific aspects to compare (coverage, cost, benefits, etc.)
        """
        criteria_filter = f" focusing on {comparison_criteria}" if comparison_criteria else ""
        return f"[MCP Comparison] Comparing {product1} vs {product2}{criteria_filter}"

    async def _analyze_coverage(self, product_name: str, coverage_question: str) -> str:
        """Analyze specific coverage details for an insurance product.
        
        Args:
            product_name: Name of the insurance product
            coverage_question: Specific coverage question or scenario
        """
        return f"[MCP Coverage Analysis] Analyzing coverage for {product_name}: {coverage_question}"

    async def run(self, message: str, context: ToolContext = None) -> str:
        """Execute the agent with the given message."""
        response = await self.agent.run(message, context=context)
        return response.text