# Service Expert Agent

The Service Expert Agent provides comprehensive insurance product information and serves as the authoritative source for product knowledge within the cross-selling ecosystem.

## Purpose

This agent specializes in:
- Retrieving detailed insurance product information via MCP server
- Comparing different insurance products and plans
- Explaining coverage details, terms, and conditions
- Providing product recommendations for cross-selling opportunities
- Ensuring regulatory compliance in product information disclosure

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini model | - | Yes |
| `INSURANCE_PRODUCTS_MCP_URL` | URL of the insurance products MCP server | `http://insurance-products:8000` | No |

## Capabilities

The agent provides the following skills:

1. **Product Information Retrieval**: Access detailed information about insurance products including coverage, terms, and conditions
2. **Product Comparison**: Compare different insurance products based on coverage, benefits, and terms
3. **Coverage Analysis**: Explain what is and isn't covered under specific insurance policies
4. **Product Recommendations**: Provide product suggestions based on customer needs for cross-selling

## Running the Agent

### Local Development

```bash
# Install dependencies
uv sync

# Set environment variables
export GOOGLE_API_KEY="your-api-key-here"

# Run the agent
cd agents/service_expert
uv run python -m service_expert
```

### Docker

```bash
# Build the image
docker build -t service-expert --build-arg AGENT_NAME=service_expert -f agents/Dockerfile .

# Run the container
docker run -p 8000:8000 -e GOOGLE_API_KEY="your-api-key" service-expert
```

## Integration

The Service Expert Agent integrates with:
- **Insurance Products MCP Server**: For accessing current product information and data
- **Cross-Selling Agent**: Provides product expertise for recommendation generation  
- **Communication Agents**: Supplies accurate product information for customer interactions
- **Host Agents**: Acts as a specialized knowledge source in the agent ecosystem

## API Endpoints

The agent exposes standard A2A endpoints:

- `GET /agent-card`: Returns agent capabilities and skills
- `POST /query`: Process queries about insurance products
- `GET /health`: Health check endpoint

## Compliance Notes

This agent focuses solely on product information and does not access customer personal data. All product information provided follows insurance regulatory requirements and disclosure standards.