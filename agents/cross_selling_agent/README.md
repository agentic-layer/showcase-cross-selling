# Cross-Selling Agent

An intelligent agent that identifies and executes cross-selling opportunities for insurance customers based on their profiles, existing policies, and communication history.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CUSTOMER_CRM_URL` | URL for customer CRM MCP server | Yes |
| `INSURANCE_PRODUCTS_URL` | URL for insurance products MCP server | Yes |
| `COMMUNICATIONS_AGENT_URL` | URL for communications agent | Yes |

## Usage

### Running the Agent

```bash
# From agent
uv run cross_selling_agent

# From workspace root
uv run --package cross_selling_agent cross_selling_agent
```

### Local Development

```bash
# Install dependencies
uv sync
```